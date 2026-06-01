---
layout: paper
title: "EuroPriv-Bench: A Unified Pan-European De-identification Benchmark with Privacy–Utility Metrics"
permalink: /papers/europriv-bench/
date: 2026-06-01
venue: "KlusAI Technical Report"
authors: "KlusAI Research"
affiliation: "KlusAI · research@klusai.com"
status: "Working paper · preliminary results (n = 1,500 per configuration) · not peer-reviewed"
data: "https://huggingface.co/datasets/klusai/europriv-bench"
code: "https://github.com/klusai/europriv-bench"
leaderboard: "/leaderboard/"
abstract: >-
  Privacy-focused NLP for European languages is served by fragmented resources: the Text
  Anonymization Benchmark provides privacy–utility metrics but is English- and legal-only;
  AI4Privacy offers cross-lingual European detection data without re-identification metrics;
  MAPA spans 24 EU languages and both legal and clinical text but is a detection toolkit, not a
  leaderboard; and the privacy-filter model lineage ships strong systems with no standardized
  evaluation at all. We introduce EuroPriv-Bench, the first benchmark to unify (a) European
  cross-lingual breadth, (b) both general and Romanian legal/clinical text, (c) a single
  harmonized GDPR-aligned entity taxonomy, and (d) re-identification-risk metrics alongside
  detection F1, in one reproducible, openly-licensed, leaderboard-style suite. We build on the
  prior art rather than replacing it, re-using its label schemes through a documented crosswalk.
  Evaluating four public de-identification systems, we find that detection F1 and privacy risk
  rank models oppositely: the strongest detector (tabularisai) leaks 26% of Romanian national
  identifiers (CNPs) on realistic documents, while the weakest detector (OpenAI privacy-filter)
  leaks only 1.1% — because it over-flags numeric strings and thus redacts CNPs even while
  mislabeling them. We argue detection F1 alone is an unsafe proxy for privacy protection, and
  release the benchmark, harness, and data to make the gap measurable.
---

## Introduction

Models advertising 94–97% F1 on English PII benchmarks tell us little about how they behave on
Dutch clinical notes or Romanian court decisions under a European privacy taxonomy. Yet the public
de-identification literature is fragmented along exactly the axes that matter for deployment in the
EU. The Text Anonymization Benchmark (TAB) [1] introduced privacy–utility metrics, but only for
English ECHR legal text. AI4Privacy [2] provides cross-lingual European detection data, but scores
detection F1 only. MAPA [3] covers all 24 official EU languages across legal and clinical text, but
ships as a detection toolkit, not a comparative leaderboard. MultiGraSCCo [4] is multilingual and
GDPR-aware but clinical-only and produced by machine translation. And the privacy-filter model
lineage — OpenAI's `privacy-filter` [6] and OpenMed's multilingual finetune [7] — ships capable
systems with **no published evaluation** at all.

No single artifact unifies (a) European cross-lingual breadth, (b) both general and domain
(legal/clinical) text, (c) one harmonized GDPR-aligned taxonomy, and (d) re-identification-risk
metrics in a reproducible, openly-licensed leaderboard. EuroPriv-Bench is the first to do so. We
make three contributions: a harmonized **KP taxonomy** with a documented crosswalk to six external
schemes (§2); a **cleanly-licensed, reproducible benchmark** spanning six European languages and a
Romanian legal/clinical track in both synthetic and realistic-document form (§3); and a
**re-identification-risk metric** for national identifiers that exposes a dissociation between
detection accuracy and privacy protection (§4–5). Our claim is explicitly "first *unified*", not
"first": we re-use and subsume the prior art.

## The KP Taxonomy

Every model speaks a different label dialect: OpenAI's `privacy-filter` has 8 coarse types,
AI4Privacy ~98, HIPAA 18, MAPA a legal/medical set, OpenMed 54, and tabularisai 42. Before scoring,
we define one GDPR-aligned **KP (KlusAI Privacy) taxonomy** and a crosswalk that maps each external
scheme's labels onto it. This is standardization, not invention; the contribution is reconciliation.

The crosswalk is validated to be a *function* — each native label maps to exactly one KP type —
which surfaced real modelling ambiguities (e.g. HIPAA `names` is claimed by both a person and a
care-provider sense; the general type wins, refinements do not claim the source label). National
identifiers (passport, driving-licence, social-insurance, and the Romanian CNP) form a dedicated
`NATIONAL_ID` type rather than collapsing into a generic account bucket, because they carry distinct
legal safeguards and, for the CNP, deterministic leakage (§4). Labels use BIOES tagging, making the
space directly comparable with `privacy-filter`. Every model is scored only on the entity types the
gold annotates, so a system is never penalized for detecting categories a given config does not
cover.

## Benchmark Construction

**Cleanly-licensed sources only.** EuroPriv-Bench v0 is built from CC-BY AI4Privacy open core,
Romanian official document structure (non-copyright under Law 8/1996 art. 9(b)), and KlusAI-generated
synthetic data — so the entire suite is openly redistributable. Six general-text language configs
(en, fr, es, de, it, nl) are curated from AI4Privacy and remapped to the KP taxonomy.

**The Romanian track.** Romanian is absent from AI4Privacy and is a strong test of locale-specific
identifiers (CNP, RO IBAN/CUI, county-coded formats) that English-primary models have never seen. We
release two Romanian configs. `ro-synthetic-v1` is a development track of template-generated
documents. `ro-realskeleton-v1` is the citable track: documents that faithfully reproduce the
**structure** of real Romanian official document types (a CNAS discharge letter, a services
contract, a sworn declaration, an administrative letter) populated with **synthetic** identifiers —
valid-checksum CNPs with consistent dates of birth, RO IBAN/CUI/CI, county addresses. Because the
skeletons are authored reproductions of public structure and all identifiers are synthetic, the
artifact contains no real personal data.

**Provenance.** Every result row records the harness version, taxonomy version, dataset config and
split, model id, and timestamp, so any number traces to an exact configuration. Synthetic training
data is kept strictly separate from gold; generation is offset-deterministic (each PII value is
spliced into a template slot and its character span recorded by construction, then re-validated).

## Metrics

**Detection.** Strict entity-level precision/recall/F1 (exact span and type match), plus a
recall-weighted F2, since in de-identification a false negative (PII left in) is far costlier than a
false positive (something harmless redacted).

**Re-identification leakage.** Our headline metric. The Romanian CNP is not an opaque string: its 13
digits encode the holder's **date of birth**, **sex**, and **county** of registration. A single
un-redacted CNP is therefore a *deterministic* disclosure of three quasi-identifiers at once. We
decode the structure directly and report, over all gold CNPs, the fraction a model fails to flag
(`leak_rate`) and the total quasi-identifiers thereby exposed. A model that flags a CNP under the
*wrong* type still redacts it and leaks nothing — redaction cares about coverage, not labels — so
this metric measures privacy protection, which detection F1 does not.

## Baselines and Results

We evaluate four public systems: OpenAI `privacy-filter` [6] (sparse-MoE token classifier),
OpenMed `privacy-filter-multilingual` [7], `tabularisai/eu-pii-safeguard` [8] (XLM-R, 26 EU
languages), and zero-shot GLiNER `gliner_multi_pii-v1` [9]. All numbers are entity-F1 at n = 1,500
per configuration, taxonomy v0.2.0; the full F1/F2 table is on the live leaderboard.

| Config | privacy-filter | OpenMed | tabularisai | GLiNER |
|---|---|---|---|---|
| English (general) | 0.415 | 0.599 | 0.515 | 0.500 |
| French (general) | 0.464 | 0.611 | 0.594 | 0.559 |
| German (general) | 0.500 | 0.608 | 0.634 | 0.572 |
| Italian (general) | 0.451 | 0.550 | 0.579 | 0.541 |
| Spanish (general) | 0.465 | 0.591 | 0.583 | 0.552 |
| Dutch (general) | 0.471 | 0.631 | 0.629 | 0.567 |
| Romanian (synthetic) | 0.576 | 0.741 | 0.876 | 0.813 |
| Romanian (real-skeleton) | 0.363 | 0.576 | 0.747 | 0.853 |

A model claiming 96–97% F1 on English PII drops to 0.42–0.63 across general European text under a
GDPR-aligned taxonomy, with recall the weak point throughout. No system dominates: OpenMed and
tabularisai lead on general text, while on realistic Romanian documents the gap between synthetic and
real context is stark (tabularisai 0.876 → 0.747; privacy-filter 0.576 → 0.363).

**The dissociation.** The re-identification metric reorders the field. On `ro-realskeleton-v1`
(~1,520 gold CNPs):

| Model | Detection F1 (RO real) | CNP leak_rate ↓ | Quasi-identifiers leaked |
|---|---|---|---|
| OpenAI privacy-filter | 0.363 (worst) | **0.011** (best) | 51 |
| OpenMed | 0.576 | 0.195 | 891 |
| GLiNER | 0.853 (best) | 0.223 | 1,017 |
| tabularisai | 0.747 | 0.261 (worst) | 1,191 |

The strongest detectors are the **worst** privacy protectors. `privacy-filter` — last on detection —
leaks only 1.1% of CNPs, because it aggressively flags long numeric strings as account numbers and
thus redacts CNPs even while mislabeling them. `tabularisai`, the most accurate general detector,
leaks 26% — it is precise, so it declines to flag CNPs it is unsure about, missing 397 of them and
exposing 1,191 quasi-identifiers. On the synthetic track every model leaks ≈ 0%, which is precisely
why a *realistic-context* gold is necessary: templated CNPs are trivially caught and hide the risk.

## Related Work

EuroPriv-Bench is designed to subsume, not compete with, prior resources, re-using their splits and
metrics where applicable. TAB [1] contributes the privacy–utility framing (English, legal). AI4Privacy
[2] supplies the cross-lingual general substrate. MAPA [3] and MEDDOCAN [5] anchor the legal/clinical
and Spanish-clinical settings. MultiGraSCCo [4] is the closest multilingual prior benchmark, but is
clinical-only and machine-translation-projected; localized native generation avoids the structurally
invalid identifiers MT produces. Piiranha [10] is included by citation only (CC-BY-NC-ND license
precludes redistribution or use as a base model).

## Limitations

These are preliminary results. (i) The general-text gold is itself synthetic (AI4Privacy);
the only realistic-context track is Romanian, and even there the PII is synthetic injected into real
structure — we measure a *synthetic-context vs real-context* gap, not a synthetic-to-real-PII gap.
(ii) n = 1,500 per config; confidence intervals are not yet reported. (iii) OpenMed and tabularisai
were trained on AI4Privacy, the source of our general-text gold, so part of their lead reflects
in-distribution advantage — the Romanian track, which no baseline has seen, is the cleaner signal.
(iv) Anonymization/utility and membership-inference tracks are specified but not yet populated.

## Conclusion

Privacy-focused NLP for Europe lacks a common yardstick. EuroPriv-Bench provides one — unified,
openly-licensed, reproducible — and its first finding is consequential: **detection F1 is an unsafe
proxy for privacy protection.** A national identifier missed is a birth date, a sex, and a county
disclosed, and the models that score best on detection are not the ones that protect best. We release
everything and invite submissions.

## References

<ol>
<li>Pilán, Lison, Øvrelid, Papadopoulou, Sánchez, Batet. "The Text Anonymization Benchmark (TAB)." <em>Computational Linguistics</em> 48(4), 2022.</li>
<li>AI4Privacy. "OpenPII Masking" datasets (CC-BY-4.0). Hugging Face, 2024.</li>
<li>MAPA Consortium. "Multilingual Anonymisation toolkit for Public Administrations," 24 EU languages, 2022.</li>
<li>"MultiGraSCCo: A Multilingual Anonymization Benchmark with Annotations of Personal Identifiers." 2026.</li>
<li>Marimon et al. "MEDDOCAN: Medical Document Anonymization (Spanish)." IberLEF, 2019.</li>
<li>OpenAI. "Privacy Filter" (<code>openai/privacy-filter</code>), 2026.</li>
<li>OpenMed. "privacy-filter-multilingual," 16 langs / 54 types, 2026.</li>
<li>tabularisai. "eu-pii-safeguard," XLM-R, 26 EU languages, 2025.</li>
<li>Zaratiana et al. "GLiNER: Generalist NER" (<code>gliner_multi_pii-v1</code>), 2023.</li>
<li>iiiorg. "Piiranha-v1" (mDeBERTa-v3), CC-BY-NC-ND, 2024.</li>
</ol>
