"""Runs the Tsakorpus indexator with a throughput-optimized bulk pipeline."""

from __future__ import annotations

import argparse
import importlib
import json
import os
from pathlib import Path
import sys
import time
from types import ModuleType
from typing import Iterator


def load_indexator_module(indexator_dir: Path) -> ModuleType:
    """Loads the canonical indexator module from its existing checkout."""

    resolved_dir = indexator_dir.resolve()
    module_path = resolved_dir / 'indexator.py'
    if not module_path.is_file():
        raise FileNotFoundError(f'Indexator entry point does not exist: {module_path}')

    search_dir = resolved_dir.parent / 'search' / 'web_app'
    sys.path.insert(0, str(search_dir))
    sys.path.insert(0, str(resolved_dir))
    return importlib.import_module('indexator')


def corpus_actions(instance: object) -> Iterator[dict]:
    """Yields every sentence and document through one corpus-wide bulk stream."""

    filenames = sorted(instance.filenames, key=lambda pair: -pair[1])
    for filename, _file_size in filenames:
        if (
            'sample_size' in instance.settings
            and 0 < instance.settings['sample_size'] < 1
            and instance.random.random() > instance.settings['sample_size']
        ):
            continue

        metadata = instance.iterSent.get_metadata(filename)
        if instance.exclude_text(metadata):
            print('Document excluded by meta:', filename)
            continue

        yield from instance.iterate_sentences(filename)
        yield instance.index_doc(filename)


def consume_parallel_bulk(
    module: ModuleType,
    instance: object,
    actions: Iterator[dict],
    *,
    workers: int,
    chunk_size: int,
    max_chunk_bytes: int,
) -> None:
    """Consumes all parallel bulk results and preserves item-level failures."""

    results = module.parallel_bulk(
        instance.es,
        actions,
        thread_count=workers,
        queue_size=workers * 2,
        chunk_size=chunk_size,
        max_chunk_bytes=max_chunk_bytes,
        request_timeout=180,
        raise_on_error=True,
        raise_on_exception=True,
    )
    for success, item in results:
        if not success:
            raise RuntimeError(f'Elasticsearch rejected a bulk action: {item}')


def index_corpus(
    module: ModuleType,
    instance: object,
    *,
    workers: int,
    chunk_size: int,
    max_chunk_bytes: int,
) -> None:
    """Indexes sentences in parallel and vocabulary with the legacy bulk path."""

    if not instance.filenames:
        print('There are no files in this corpus.')
        return

    sentence_started = time.monotonic()
    consume_parallel_bulk(
        module,
        instance,
        corpus_actions(instance),
        workers=workers,
        chunk_size=chunk_size,
        max_chunk_bytes=max_chunk_bytes,
    )
    print(
        'Optimized sentence/document stream indexed in',
        f'{time.monotonic() - sentence_started:.3f}',
        'seconds.',
    )

    # Vocabulary already forms one corpus-wide stream, so keep its established
    # synchronous path to avoid competing Elasticsearch writers.
    vocabulary_started = time.monotonic()
    module.bulk(
        instance.es,
        instance.iterate_words(),
        chunk_size=1000,
        request_timeout=120,
    )
    print(
        'Legacy vocabulary stream indexed in',
        f'{time.monotonic() - vocabulary_started:.3f}',
        'seconds.',
    )
    if instance.settings.get('generate_dictionary'):
        instance.generate_dictionary()


def put_build_settings(
    instance: object,
    *,
    refresh_interval: str,
    replicas: int,
) -> None:
    """Applies transient build or final settings to all corpus indices."""

    instance.es.indices.put_settings(
        index=f'{instance.name}.*',
        body={
            'index': {
                'refresh_interval': refresh_interval,
                'number_of_replicas': replicas,
            }
        },
    )


def load_corpus(
    module: ModuleType,
    instance: object,
    *,
    workers: int,
    chunk_size: int,
    max_chunk_bytes: int,
    final_refresh_interval: str,
    final_replicas: int,
) -> None:
    """Builds the corpus while suppressing refresh and replica overhead."""

    started = time.monotonic()
    if not instance.delete_indices():
        return

    instance.analyze_dir()
    instance.create_indices()
    instance.clean_dirs()
    put_build_settings(instance, refresh_interval='-1', replicas=0)
    completed = False
    try:
        index_corpus(
            module,
            instance,
            workers=workers,
            chunk_size=chunk_size,
            max_chunk_bytes=max_chunk_bytes,
        )
        instance.es.indices.refresh(index=f'{instance.name}.*')
        completed = True
    finally:
        if completed:
            put_build_settings(
                instance,
                refresh_interval=final_refresh_interval,
                replicas=final_replicas,
            )

    print(
        'Corpus indexed in',
        f'{time.monotonic() - started:.3f}',
        'seconds:',
        instance.dID,
        'documents,',
        instance.sID,
        'sentences,',
        instance.totalNumWords,
        'words,',
        sum(len(frequencies) for frequencies in instance.wordFreqs),
        'word types (different words).',
    )


def positive_integer(value: str) -> int:
    """Parses one positive command-line integer."""

    parsed = int(value)
    if parsed < 1:
        raise argparse.ArgumentTypeError('value must be at least 1')
    return parsed


def parse_args() -> argparse.Namespace:
    """Parses the isolated optimized-indexer command line."""

    parser = argparse.ArgumentParser(
        description='Runs Tsakorpus indexing with optimized bulk ingestion.',
    )
    parser.add_argument(
        '--indexator-dir',
        type=Path,
        required=True,
        help='Path to the canonical Tsakorpus indexator directory.',
    )
    parser.add_argument('--corpus-input', type=Path, required=True)
    parser.add_argument('--corpus-config', type=Path, required=True)
    parser.add_argument('--categories-config', type=Path, required=True)
    parser.add_argument('--elastic-url', required=True)
    parser.add_argument('--runtime-root', type=Path, required=True)
    parser.add_argument('--workers', type=positive_integer, default=2)
    parser.add_argument('--chunk-size', type=positive_integer, default=500)
    parser.add_argument(
        '--max-chunk-mb',
        type=positive_integer,
        default=16,
        help='Maximum uncompressed bulk request size.',
    )
    parser.add_argument('--final-refresh-interval', default='30s')
    parser.add_argument('--final-replicas', type=int, choices=(0, 1), default=1)
    parser.add_argument(
        '-y',
        nargs='?',
        const='yes',
        help='Overwrite existing indices.',
    )
    return parser.parse_args()


def prepare_runtime(args: argparse.Namespace) -> Path:
    """Validates EANC4-owned inputs and selects the scratch working directory."""

    runtime_root = args.runtime_root.resolve()
    corpus_input = args.corpus_input.resolve()
    corpus_config = args.corpus_config.resolve()
    categories_config = args.categories_config.resolve()
    for path in (corpus_input, corpus_config, categories_config):
        if not path.exists():
            raise FileNotFoundError(path)

    expected_config = runtime_root / 'conf' / 'corpus.json'
    expected_categories = runtime_root / 'conf' / 'categories.json'
    if corpus_config != expected_config or categories_config != expected_categories:
        raise ValueError('Configuration files must be inside the runtime root')

    config = json.loads(corpus_config.read_text(encoding='utf-8'))
    expected_corpus = runtime_root / 'corpus' / config['corpus_name']
    if corpus_input != expected_corpus:
        raise ValueError('Corpus input must match the configured runtime corpus')
    config['elastic_url'] = args.elastic_url
    corpus_config.write_text(
        json.dumps(config, ensure_ascii=False, indent=2, sort_keys=True) + '\n',
        encoding='utf-8',
    )

    working_directory = runtime_root / 'indexator'
    working_directory.mkdir(parents=True, exist_ok=True)
    return working_directory


def main() -> None:
    """Loads the canonical implementation and runs its optimized ingestion path."""

    args = parse_args()
    os.chdir(prepare_runtime(args))
    module = load_indexator_module(args.indexator_dir)
    module.parallel_bulk = importlib.import_module(
        'elasticsearch.helpers'
    ).parallel_bulk

    # The canonical module imports random directly; expose it on the instance
    # so corpus sampling retains exactly the same implementation and seed.
    instance = module.Indexator(overwrite=args.y is not None)
    instance.random = module.random
    load_corpus(
        module,
        instance,
        workers=args.workers,
        chunk_size=args.chunk_size,
        max_chunk_bytes=args.max_chunk_mb * 1024 * 1024,
        final_refresh_interval=args.final_refresh_interval,
        final_replicas=args.final_replicas,
    )


if __name__ == '__main__':
    main()
