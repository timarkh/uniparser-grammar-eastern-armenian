# Lemma Enrichment Memo

A precision-first, reproducible pipeline for classifying Eastern Armenian lemma candidates extracted from press corpora.

## Purpose

The pipeline identifies candidates that can be safely proposed for addition to the EANC grammatical dictionary. It favors precision over recall: uncertain entries are retained for review rather than automatically accepted.

Frequency determines processing priority, not linguistic validity.

## Input and output

Input is a CSV, TSV, or Parquet table containing at least:

* `lex`
* `pos`
* `frequency`

The original columns—`wordform`, `pos`, `tags`, `lex`, `flextype`, and `frequency`—are preserved when present.

The pipeline appends:

* `candidate_type`: final classification
* `reason`: optional short explanation or decisive rule
* `eanc_lex`: canonical EANC lemma when the candidate is an existing wordform

Possible classifications include `valid_lemma`, `eanc_wordform`, `inflected_form`, `clipped_stem`, `abbreviation`, `western_or_classical`, `noise`, and `uncertain`.

## Sequential transform architecture

Each row passes through an ordered sequence of deterministic transforms:

1. **Reference lookup**
   Match the candidate against the existing EANC grammatical dictionary and annotated EANC wordforms. Existing wordforms are linked to their canonical lemma and excluded from proposed additions.

2. **Candidate classification**
   Apply high-confidence rules in fixed precedence order. These detect invalid scripts, malformed strings, abbreviations, inflected or prefixed forms, clipped stems, non-target orthography, and other recurrent Stanza-derived noise.

3. **EANC-backed refinement**
   Use EANC lexical and wordform evidence to revise provisional labels. Direct morphological evidence takes precedence over surface-form heuristics.

4. **Same-POS one-edit gate**
   Compare unresolved candidates with known lemmas of the same part of speech. A one-edit neighbor is treated as possible typo evidence, but not rejected solely because a similar lemma exists.

5. **Verb-collision gate**
   Apply stricter checks to verbal candidates whose forms collide with known inflections, productive prefixes, or likely analyzer errors.

6. **Final adjudication**
   Preserve clear additions as `valid_lemma`; assign clear failure categories where supported; send conflicting or insufficiently supported cases to `uncertain`.

Because transforms are ordered, later rules refine earlier provisional decisions without creating an opaque aggregate score. Every classification is traceable to its decisive rule.

## Operating principles

* Precision is more important than recall.
* Uncertainty causes abstention, not automatic acceptance.
* The top 30,000 candidates form the current working set; the frequency tail is deferred, not declared invalid.
* Existing EANC evidence outranks general string heuristics.
* Part of speech is considered when comparing candidates with known lemmas.
* Original lexical and morphological fields are never silently rewritten.
* The same input and reference files always produce the same output.

## Reproducibility

The classifier runs entirely offline. It requires no web access, external API, or LLM call. All reference data and rules are packaged locally, making the result reproducible and suitable for processing the full candidate set chunk by chunk.

The frozen validation case contains 1,000 candidates and should produce 567 `valid_lemma` classifications, with `դունայթել` classified as `uncertain`. These checks detect changes in rule ordering or reference handling.

## Iterations

Pipeline A established the initial precision-oriented heuristic baseline. 
Pipeline B added EANC annotated-wordform evidence. 
Pipeline C is the final stricter implementation: it uses explicit rule precedence, EANC-backed refinement, same-POS edit checks, and dedicated verb-collision handling to reduce false positives while accepting lower recall.
