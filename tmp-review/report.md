# Architecture and Code Review: Eastern Armenian Morphological Analyzer

## Scope and executive assessment

This repository is a data-first, rule-based morphological analyzer for Modern Eastern Armenian (`hye`).  Its central proposition is sound: express inflection in UniParser grammar files, describe lexical entries declaratively, and use the upstream `uniparser-morph` engine for analysis rather than reimplementing an FST/parser in this project.  The result is compact at the Python layer, linguistically transparent, and capable of returning lemma, part of speech, grammatical tags, and glosses.  The README also describes optional Constraint Grammar (CG3) disambiguation and reports approximately 93% token recall on literary text.

The repository’s main asset is its linguistic coverage, not its Python code.  It contains a 4,739-line paradigm grammar and five generated lexicon partitions totalling about 656,000 lines.  The corpus material is also significant: the EANC frequency list and its analyzed/unrecognized derivatives account for roughly 143 MB of the approximately 220 MB checkout.  The architecture is therefore appropriate for a research grammar: the grammar and dictionary are readable, reviewable text data rather than opaque model weights.

The principal engineering risk is release reproducibility.  On this checkout, the package-data directory contains only `__init__.py`, while the runtime constructor requires nine data files.  `pre_build.py` creates/copies only five of them, and the remaining three (`derivations.txt`, `stem_conversions.txt`, and `clitics.txt`) have no tracked source in this repository.  In addition, the generated package files are ignored by Git and no setuptools build hook invokes the preparation script.  Consequently, a clean source checkout is not presently self-contained or importable without external/release-only artifacts.  This should be treated as the first maintenance priority.

## Architecture and execution path

The runtime surface is intentionally thin.  `EasternArmenianAnalyzer` subclasses `uniparser_morph.Analyzer`, resolves package resources via `importlib.resources`, assigns their paths to the inherited analyzer, and calls `load_grammar()` in its constructor.  Its only behavioral extension is `analyze_words()`: it preserves the upstream API while locating the bundled CG3 grammar when `disambiguate=True`.  This is a good separation of responsibilities.  The upstream library owns parsing mechanics; this repository owns language-specific data and resource selection.

The intended data flow is:

```text
source/dict*.csv  +  source/script.py ──> hye-lexemes-{N,V,A,ADV,rest}.txt
                                            │
paradigms.txt + lexicon shards + CG3 ──> pre_build.py ──> package data
                                                           │
                         installed package ──> EasternArmenianAnalyzer ──> Analyzer
```

`source/script.py` is the substantive generation component.  It reads a tab-separated lexical source, derives stems by inflection class, normalizes selected paradigm aliases, adds several orthographic alternatives, and emits UniParser `-lexeme` blocks partitioned by POS.  Its explicitly encoded exceptions—especially pronouns, irregular verbs, plural forms, and vowel alternations—are a reasonable fit for Armenian morphology.  The use of a separate `paradigms.txt` makes affix behavior independently inspectable, while lexicon records connect an orthographic lexeme and stem to a grammatical class, gloss, translation, and paradigm.

`pre_build.py` then concatenates all `hye-lexemes-*` files, deduplicating complete lexeme blocks with a Python `set`, sorts them, and produces `lexemes.txt`.  It copies paradigms, lexical rules, suppression rules, and the CG3 grammar into package data.  Its optional `parse_wordlists()` routine runs the full analyzer against the EANC frequency list and writes derived evaluation-like artifacts.

The conceptual layering is strong: declarative paradigms; lexical entries; an upstream engine; and a post-analysis disambiguator.  The implementation layering is weaker because source generation, packaging preparation, and corpus regeneration are coupled in a single script entry point.  Running `python pre_build.py` always follows preparation with an expensive whole-wordlist analysis.  Those should be distinct, explicit commands.

## Code review

The production Python API is concise and idiomatic.  `importlib.resources.files()` plus `as_file()` is the right packaging-aware mechanism for accessing assets from a wheel or zip-like distribution.  The analyzer accepts a single token or nested token lists and exposes upstream XML/JSON modes without needless wrapping.  The docstrings are useful, and the `disambiguate` flag makes the optional dependency visible at the call site.

There are several correctness and maintainability concerns:

1. **Runtime/package mismatch (critical).** `__init__.py` unconditionally asks for `derivations.txt`, `stem_conversions.txt`, and `clitics.txt`; none is tracked or generated in the checked-out package data.  In contrast, `MANIFEST.in` only states broad inclusion rules.  Even after running `prepare_files()`, the missing resources remain.  Add the assets (empty, valid files if the engine permits them) to version control, or stop requesting unsupported optional files.  Add an installation smoke test that creates `EasternArmenianAnalyzer` from a built wheel.

2. **No integrated build step.** `pyproject.toml` only selects setuptools and `setup.cfg` has no custom build command.  `pre_build.py` is not automatically run by `pip build`, `pip install .`, or an sdist build.  Build artifacts should be generated deterministically in a setuptools command/hook or, preferably, committed as canonical package data alongside clearly versioned sources.  The release path should not depend on undocumented manual sequencing.

3. **Non-deterministic detail in generation.** `add_orth_variation()` collects alternatives in a `set` and joins it directly.  Python set iteration order is not a stable data contract, so otherwise identical source inputs can yield order-only diffs.  Sort variants before joining.  Likewise, `collect_lemmata()` should use context managers and `pathlib` for clearer resource handling.

4. **Generator logic is hard to validate.** `source/script.py` contains a long chain of inflection-class conditions and literal exceptions.  This is linguistically normal but lacks tests for each rule family.  Several branches are duplicated (`N72`), and one condition tests `N63` twice (`['N63a', 'N63']`) after an earlier `N63` return, making its intended special case unreachable for `N63`.  Refactor only after encoding current expected outputs as fixtures; otherwise a cleanup risks grammar regressions.

5. **Obsolete/unclear auxiliary script.** `source/script_verbs.py` references filenames outside `source/`, contains a likely malformed multi-line conditional, and writes an `OOPS` sentinel under broad conditions.  It appears unused by the current pipeline.  Either document it as archival or remove/repair it after confirming it has no users.

6. **Operational observability.** There is no logging, version metadata for grammar assets, or explicit detection of missing CG3.  The inherited engine may cover some diagnostics, but this wrapper should raise a focused message when package data are incomplete and explain that CG3 must be installed when disambiguation is requested.

## Assets, quality, and data stewardship

The core assets are well chosen.  POS-sharded lexicons make diffs and linguistic ownership more manageable than a monolithic file; `bad_analyses.txt` provides a controlled mechanism to suppress known false positives; and `armenian_disambiguation.cg3` supplies contextual pruning after broad morphological generation.  The `source/dict.csv` (77,687 lines) and `dict6000.csv` (6,031 lines) preserve a plausible derivation source for the generated grammar, while the wordlists provide a useful coverage baseline and regression corpus.

However, source-of-truth boundaries are not documented.  It is unclear whether maintainers should edit the CSV source, the generated `hye-lexemes-*` files, or both.  A contributor can easily make a lexicon change that disappears on regeneration, or update `paradigms.txt` without rebuilding package data.  Add a short `CONTRIBUTING.md` covering the canonical edit path, required regeneration commands, expected output diffs, and how to validate a proposed lexical/paradigm change.

The wordlist assets are valuable but are poorly separated from product packaging concerns.  They are not package data, are very large, and appear to be generated from a 100-million-word EANC source.  Keep a small curated regression set in the repository, document the provenance/licensing/version of the full corpus outputs, and consider Git LFS, release assets, or an optional data download for the 94 MB analyzed list.  This will improve clone time and make ordinary code reviews more focused.  The existing recall claim should also state its corpus split, tokenization policy, date/version, and whether case/unknown-token normalization was applied.

## Recommended roadmap

**P0 — make the repository buildable.** Reconcile the runtime resource list, track or generate every required file, split `prepare_files` from corpus analysis, and add a clean-environment wheel installation test.  Verify an analysis of a handful of representative tokens, JSON/XML output, and the behavior when CG3 is unavailable.

**P1 — establish regression protection.** Add pytest tests for analyzer construction, representative paradigms (noun, adjective, verb, pronoun, clitic/derivation if supported), known suppressed analyses, and deterministic output from `source/script.py`.  Store a compact golden fixture rather than reprocessing the full EANC list in CI.  Add a CI workflow that builds an sdist and wheel, installs each, and runs the smoke tests.

**P2 — clarify ownership and modernize tooling.** Document the canonical source files and release workflow; replace bare file handling with context managers; make generation deterministic; and either rehabilitate or retire legacy scripts.  Pin or test against a supported range of `uniparser-morph` versions, since grammar compatibility is an API boundary.

**P3 — improve research usability.** Publish reproducible evaluation instructions and corpus provenance, version grammar/data independently from the Python wrapper where useful, and expose lightweight metadata such as grammar revision and supported resource capabilities.  These changes preserve the project’s appealing declarative linguistic design while making it dependable for both package users and grammar contributors.

## Review method and limitations

This review is based on the checked-out tracked files, repository status, file counts/sizes, packaging metadata, the public wrapper, `pre_build.py`, and the source-generation scripts.  No linguistic recall benchmark was rerun, no external `cg3` binary was installed, and no release artifact from PyPI was inspected.  Therefore, the package-data finding applies decisively to this checkout; a separately assembled published wheel may contain additional assets.  The recommended wheel smoke test is the fastest way to resolve that distinction and prevent it from recurring.
