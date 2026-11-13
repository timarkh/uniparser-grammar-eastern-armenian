"""Tests the isolated optimized Tsakorpus ingestion mechanics."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import random
import sys
import tempfile
import unittest
from unittest.mock import Mock


OPTIMIZED_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(OPTIMIZED_ROOT))

from optimized_indexator import corpus_actions  # noqa: E402
from optimized_indexator import positive_integer  # noqa: E402
from optimized_indexator import prepare_runtime  # noqa: E402
from optimized_indexator import put_build_settings  # noqa: E402


class FakeInstance:
    """Provides the canonical indexator surface used by action streaming."""

    def __init__(self) -> None:
        """Initializes deterministic filenames, metadata, and action methods."""

        self.filenames = [('small.json', 10), ('large.json', 20)]
        self.settings: dict = {}
        self.random = random
        self.iterSent = Mock()
        self.iterSent.get_metadata.side_effect = lambda filename: {
            'filename': filename
        }

    def exclude_text(self, metadata: dict) -> bool:
        """Keeps every fake document in the action stream."""

        return False

    def iterate_sentences(self, filename: str):
        """Yields two sentence actions for one fake document."""

        yield {'kind': 'sentence', 'filename': filename, 'position': 0}
        yield {'kind': 'sentence', 'filename': filename, 'position': 1}

    def index_doc(self, filename: str) -> dict:
        """Returns the document action after its sentence actions."""

        return {'kind': 'document', 'filename': filename}


class CorpusActionsTests(unittest.TestCase):
    """Verifies the corpus-wide stream preserves canonical state ordering."""

    def test_streams_largest_file_first_and_document_after_sentences(self) -> None:
        """Verifies deterministic file and within-document action ordering."""

        actions = list(corpus_actions(FakeInstance()))

        self.assertEqual(
            actions,
            [
                {'kind': 'sentence', 'filename': 'large.json', 'position': 0},
                {'kind': 'sentence', 'filename': 'large.json', 'position': 1},
                {'kind': 'document', 'filename': 'large.json'},
                {'kind': 'sentence', 'filename': 'small.json', 'position': 0},
                {'kind': 'sentence', 'filename': 'small.json', 'position': 1},
                {'kind': 'document', 'filename': 'small.json'},
            ],
        )

    def test_excluded_document_produces_no_actions(self) -> None:
        """Verifies metadata exclusions apply before sentence generation."""

        instance = FakeInstance()
        instance.exclude_text = lambda metadata: metadata['filename'] == 'large.json'

        actions = list(corpus_actions(instance))

        self.assertEqual(len(actions), 3)
        self.assertTrue(
            all(action['filename'] == 'small.json' for action in actions)
        )


class IndexSettingsTests(unittest.TestCase):
    """Verifies transient settings cover every generated corpus index."""

    def test_put_build_settings_targets_corpus_wildcard(self) -> None:
        """Verifies refresh and replica settings use the expected request."""

        instance = Mock()
        instance.name = 'eanc4_mini'

        put_build_settings(instance, refresh_interval='-1', replicas=0)

        instance.es.indices.put_settings.assert_called_once_with(
            index='eanc4_mini.*',
            body={
                'index': {
                    'refresh_interval': '-1',
                    'number_of_replicas': 0,
                }
            },
        )

    def test_positive_integer_rejects_zero(self) -> None:
        """Verifies worker and chunk options cannot disable forward progress."""

        with self.assertRaises(Exception):
            positive_integer('0')


class RuntimeTests(unittest.TestCase):
    """Verifies EANC4 owns every mutable indexator input and artifact."""

    def test_prepares_working_directory_inside_runtime_root(self) -> None:
        """Updates the runtime URL and keeps relative SQLite paths local."""

        with tempfile.TemporaryDirectory() as temporary:
            runtime_root = Path(temporary)
            corpus_input = runtime_root / 'corpus' / 'eanc4_micro'
            config_root = runtime_root / 'conf'
            corpus_input.mkdir(parents=True)
            config_root.mkdir()
            corpus_config = config_root / 'corpus.json'
            categories_config = config_root / 'categories.json'
            corpus_config.write_text(json.dumps({
                'corpus_name': 'eanc4_micro',
                'elastic_url': 'http://old:9200',
            }))
            categories_config.write_text('{}')
            args = argparse.Namespace(
                runtime_root=runtime_root,
                corpus_input=corpus_input,
                corpus_config=corpus_config,
                categories_config=categories_config,
                elastic_url='http://new:9200',
            )

            working_directory = prepare_runtime(args)

            self.assertEqual(working_directory, runtime_root / 'indexator')
            self.assertTrue(working_directory.is_dir())
            self.assertEqual(
                json.loads(corpus_config.read_text())['elastic_url'],
                'http://new:9200',
            )


if __name__ == '__main__':
    unittest.main()
