# Optimized Tsakorpus indexing experiment

This directory contains an isolated ingestion experiment. The optimized runner changes only ingestion mechanics:

- streams sentences and documents through one corpus-wide bulk pipeline instead of starting one synchronous bulk operation per source document;
- uses bounded `parallel_bulk` workers so action generation and Elasticsearch ingestion overlap;
- disables periodic refreshes and replicas while constructing the indices;
- performs one explicit refresh and restores the requested final refresh and replica settings after a successful build;
- reports separate sentence/document and vocabulary timings.

## Run

EANC4 invokes the optimized entry point directly. The canonical Tsakorpus checkout supplies immutable implementation code; EANC4 supplies the staged corpus, configuration, Elasticsearch endpoint, and an EANC4-owned runtime directory.

```bash
/home/dlevonian/eanc/.venv-tsakorpus-index/bin/python \
  /home/dlevonian/eanc/uniparser-grammar-eastern-armenian/optimized/optimized_indexator.py \
  --indexator-dir /home/dlevonian/eanc/tsakorpus_eastern_armenian/indexator \
  --corpus-input <eanc4-runtime>/corpus/eanc4_micro \
  --corpus-config <eanc4-runtime>/conf/corpus.json \
  --categories-config <eanc4-runtime>/conf/categories.json \
  --elastic-url http://localhost:9200 \
  --runtime-root <eanc4-runtime> \
  --workers 2 \
  --chunk-size 500 \
  --max-chunk-mb 16 \
  --final-replicas 0 \
  -y yes
```

The runtime root must contain the passed configuration and corpus paths. The process creates its working directory there, so legacy relative SQLite scratch files never enter this repository. EANC4 removes the temporary runtime after Stage 3 and retains logs and reports in its evidence directory.

Use `--final-replicas 1` for a multi-node production deployment. A single-node development cluster should use zero replicas to avoid a permanently unassigned replica shard.

## Benchmark protocol

1. Record Elasticsearch health and delete only the disposable mini indices.
2. Run the canonical indexator once and record its final summary, index counts, primary-store bytes, and Stage 4 results.
3. Run this implementation against the identical Stage 2 input and record the same evidence.
4. Accept the optimization only when wall time is at most 822 seconds, document/sentence/word-type counts are identical, and all 21 Stage 4 checks pass.
5. If the target is missed, test worker counts `2`, `3`, and `4` independently. Do not increase concurrency without measuring Elasticsearch bulk rejections, CPU utilization, heap pressure, and disk saturation.

The runner restores final settings only after a successful refresh. If indexing fails, it deliberately leaves refresh disabled and replicas at zero on the incomplete disposable indices, making the failed state visible rather than disguising it as a completed build.
