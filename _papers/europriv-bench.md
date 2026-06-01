---
layout: paper
title: "EuroPriv-Bench: A Unified Pan-European De-identification Benchmark with Re-identification Risk Metrics"
permalink: /papers/europriv-bench/
date: 2026-06-01
venue: "KlusAI Technical Report"
authors: "KlusAI Research"
affiliation: "KlusAI"
contact: "research@klusai.com"
status: "Working paper · preliminary results (n = 1,500 docs/config) · not peer-reviewed"
data: "https://huggingface.co/datasets/klusai/europriv-bench"
code: "https://github.com/klusai/europriv-bench"
leaderboard: "/leaderboard/"
abstract: >-
  Privacy-focused NLP for European languages is served by fragmented resources: the Text
  Anonymization Benchmark provides privacy–utility metrics but is English- and legal-only;
  AI4Privacy offers cross-lingual European detection data without re-identification metrics;
  MAPA covers 24 EU languages and both legal and clinical text but as a detection toolkit, not a
  comparative leaderboard; and the privacy-filter model lineage ships strong systems for which we
  found no standardized public evaluation. We introduce EuroPriv-Bench, the first benchmark to
  unify (a) European cross-lingual breadth, (b) general and Romanian legal/clinical text, (c) one
  harmonized GDPR-aligned entity taxonomy, and (d) a re-identification-risk metric alongside
  detection F1, in one reproducible, openly-licensed, leaderboard-style suite. We build on the
  prior art rather than replacing it, re-using its label schemes through a documented crosswalk.
  Evaluating four public systems on realistic Romanian documents, we find that detection F1 does
  not track national-identifier (CNP) protection: the best detector is not the best protector.
  OpenAI privacy-filter — the weakest detector (F1 0.36) — leaks only 1.1% of CNPs (95% CI 0.7–1.8)
  because it labels 96% of them as account numbers and redacts them regardless of type, whereas the
  three type-accurate detectors all leak 19–26% (non-overlapping intervals): GLiNER, the most
  accurate at F1 0.85, leaks 22.3%, and tabularisai leaks the most, 26.1% (24.0–28.4). Coverage-based
  redaction and type-accurate detection are different objectives — F1 measures the latter, protection
  needs the former — so detection F1 is an unsafe proxy for re-identification protection, at least for
  national identifiers. We release the benchmark, harness, configs, and data so the gap is measurable.
---

## Introduction

Models advertising 94–97% F1 on English PII benchmarks tell us little about how they behave on
Dutch clinical notes or Romanian court decisions under a European privacy taxonomy. Yet the public
de-identification literature is fragmented along the axes that matter for EU deployment. The Text
Anonymization Benchmark (TAB) [<a href="#ref-1">1</a>] introduced privacy–utility metrics, but only
for English ECHR legal text. AI4Privacy [<a href="#ref-2">2</a>] provides cross-lingual European
detection data, but scores detection F1 only. MAPA [<a href="#ref-3">3</a>] covers all 24 official
EU languages across legal and clinical text, but ships as a detection toolkit, not a comparative
leaderboard. MultiGraSCCo [<a href="#ref-4">4</a>] is multilingual and GDPR-aware but clinical-only
and produced by machine translation. And the privacy-filter model lineage — OpenAI's `privacy-filter`
[<a href="#ref-6">6</a>] and OpenMed's multilingual finetune [<a href="#ref-7">7</a>] — ships capable
systems for which we found **no standardized public privacy-risk evaluation** as of June 2026.

No single artifact unifies (a) European cross-lingual breadth, (b) general and domain
(legal/clinical) text, (c) one harmonized GDPR-aligned taxonomy, and (d) a re-identification-risk
metric, in a reproducible, openly-licensed leaderboard. EuroPriv-Bench is the first to do so. Our
claim is explicitly "first *unified*", not "first": we re-use and subsume the prior art (§6). We
contribute a harmonized taxonomy with a documented crosswalk to six external schemes (§2); a
cleanly-licensed, reproducible benchmark over six European languages and a Romanian legal/clinical
track in both synthetic and realistic-document form (§3); and a national-identifier
re-identification-risk metric that exposes a dissociation between detection accuracy and privacy
protection (§4–5).

## The KP Taxonomy

Every model speaks a different label dialect: OpenAI's `privacy-filter` has 8 coarse types,
AI4Privacy ~98, HIPAA 18, MAPA a legal/medical set, OpenMed 54, and tabularisai 42. Before scoring,
we define one GDPR-aligned **KP (KlusAI Privacy) taxonomy** and a crosswalk mapping each external
scheme's labels onto it (published in full in the code repository). This is standardization, not
invention; the contribution is reconciliation.

The crosswalk is validated to be a *function* — each native label maps to exactly one KP type —
which surfaced real modelling ambiguities (e.g. HIPAA `names` is claimed by both a person and a
care-provider sense; the general type wins, and refinements do not claim the source label). National
identifiers (passport, driving-licence, social-insurance, and the Romanian CNP) form a dedicated
`NATIONAL_ID` type rather than collapsing into a generic account bucket, because they carry distinct
legal safeguards and, for the CNP, deterministic leakage (§4). Spans use BIOES tagging; combined with
the crosswalk this lets each model's native output be scored in the shared label space — including a
head-to-head with `privacy-filter`'s own BIOES output. Every model is scored only on the entity types
a given config's gold annotates, so a system is never penalized for detecting categories that config
does not cover.

## Benchmark Construction

**Cleanly-licensed sources only.** EuroPriv-Bench v0 is built from CC-BY AI4Privacy open core,
KlusAI-authored Romanian document structure, and KlusAI-generated synthetic identifiers — so the
entire suite is openly redistributable. Six general-text language configs (en, fr, es, de, it, nl)
are curated from AI4Privacy and remapped to the KP taxonomy.

**The Romanian track.** Romanian is absent from AI4Privacy and is a strong test of locale-specific
identifiers (CNP, RO IBAN/CUI, county-coded formats) that English-primary models have never seen. We
release two Romanian configs. `ro-synthetic-v1` is a development track of template-generated
documents. `ro-realskeleton-v1` is the citable track: documents that reproduce the *structure* of
real Romanian official document types (a CNAS discharge letter, a services contract, a sworn
declaration, an administrative letter) populated with procedurally-generated identifiers —
valid-checksum CNPs with consistent dates of birth, RO IBAN/CUI/CI, county addresses. The skeletons
are original KlusAI-authored documents that imitate the *functional layout* of these document types
(headings, field order, boilerplate) without copying any source text; for genuinely official texts,
Law 8/1996 art. 9(b) additionally places them outside copyright. They are released under the suite's
open license. No identifier is derived from a real data subject; all are procedurally generated.

**Provenance.** Every result row records the harness version, taxonomy version, dataset config and
split, model id, and timestamp, so any number traces to an exact configuration. Synthetic training
data is kept strictly separate from gold; generation is offset-deterministic (each identifier is
spliced into a template slot and its character span recorded by construction, then re-validated).

## Metrics

**Detection.** Strict entity-level precision/recall/F1 (exact span and type match), plus a
recall-weighted F2, since in de-identification a false negative (PII left in) is far costlier than a
false positive (something harmless redacted).

**Re-identification leakage.** Our headline metric. The Romanian CNP is not an opaque string: its
first digit encodes sex and birth-century, digits 2–7 the date of birth, and digits 8–9 the county of
registration. A single un-redacted CNP therefore discloses at least three quasi-identifiers at
once.<sup><a href="#fn-1" id="fnref-1">1</a></sup> We decode the structure directly and report, over
all gold CNPs, the fraction left unflagged (`leak_rate`) and the total quasi-identifiers thereby
exposed. **A CNP counts as protected iff the model flags at least one token overlapping its span as
PII of *any* type** — it would be redacted regardless of the predicted label; if every token of the
CNP is predicted `O`, it is a leak. This is coverage, not labels — which is exactly the property
detection F1 does not measure.

The any-overlap rule is deliberately *conservative*: a model that flags even one token of a CNP is
credited with protection, so `leak_rate` is a lower bound on real-world leakage — a redaction
pipeline keying on exact spans or types could still expose digits. (privacy-filter, below, flags
full CNP spans, so it is unaffected by this caveat.)

## Baselines and Results

We evaluate four public systems: OpenAI `privacy-filter` [<a href="#ref-6">6</a>], OpenMed
`privacy-filter-multilingual` [<a href="#ref-7">7</a>], `tabularisai/eu-pii-safeguard`
[<a href="#ref-8">8</a>], and zero-shot GLiNER `gliner_multi_pii-v1` [<a href="#ref-9">9</a>]. All
numbers are entity-F1 at n = 1,500 docs per configuration, taxonomy v0.2.0; the full F1/F2 table is on
the live leaderboard.

| Config | privacy-filter | OpenMed | tabularisai | GLiNER |
|---|---|---|---|---|
| English (general) | 0.41 | 0.60 | 0.51 | 0.50 |
| French (general) | 0.46 | 0.61 | 0.59 | 0.56 |
| German (general) | 0.50 | 0.61 | 0.63 | 0.57 |
| Italian (general) | 0.45 | 0.55 | 0.58 | 0.54 |
| Spanish (general) | 0.47 | 0.59 | 0.58 | 0.55 |
| Dutch (general) | 0.47 | 0.63 | 0.63 | 0.57 |
| Romanian (synthetic) | 0.58 | 0.74 | 0.88 | 0.81 |
| Romanian (real-skeleton) | 0.36 | 0.58 | 0.75 | 0.85 |

<p class="caption">Table 1. Entity-level detection F1 by configuration (n = 1,500 docs/config; taxonomy v0.2.0). OpenMed and tabularisai are statistically indistinguishable on the general-text average (0.598 vs 0.589, a 0.009 gap we report without a confidence interval); the Romanian tracks are led by tabularisai (synthetic) and GLiNER (real-skeleton). The general-text ranking is confounded — OpenMed and tabularisai were trained on AI4Privacy (this gold's source), GLiNER and privacy-filter were not — so it mixes in- and out-of-distribution systems; the Romanian real-skeleton track, which no baseline has seen, is the fair comparison.</p>

A model claiming 96–97% F1 on English PII drops to 0.41–0.63 across general European text under a
GDPR-aligned taxonomy, with recall the weak point throughout: recall-weighted F2 is lower than F1 in
every cell (English, for instance: privacy-filter 0.41→0.35, OpenMed 0.60→0.57, tabularisai
0.51→0.46, GLiNER 0.50→0.45). No system dominates — OpenMed and tabularisai are level on the general-text average,
tabularisai and GLiNER lead the Romanian tracks — and the gap between synthetic and realistic Romanian context is stark
(tabularisai 0.88→0.75; privacy-filter 0.58→0.36).

**The dissociation.** On `ro-realskeleton-v1` (1,500 documents, 1,520 gold CNPs), detection accuracy
does not predict protection: **the best detector is not the best protector.** The per-model contrast
is the evidence — and it is significant, because the Wilson 95% intervals on leak-rate separate the
systems (Table 2). With only four systems we do *not* lean on a correlation coefficient: the rank
order happens to run positive (Spearman ρ = +0.80), but over four points that is a descriptive
observation, not an estimate, and it is not statistically significant (p = 0.20). We therefore read
the result as "F1 does not track CNP protection," and explain *why* below — not as a monotonic law.

| Model | Detection F1 | CNP leak-rate (95% CI) | Quasi-IDs leaked |
|---|---|---|---|
| OpenAI privacy-filter | 0.36 | **1.1%** (0.7–1.8) | 51 |
| OpenMed | 0.58 | 19.5% (17.6–21.6) | 891 |
| GLiNER | **0.85** | 22.3% (20.3–24.5) | 1,017 |
| tabularisai | 0.75 | 26.1% (24.0–28.4) | 1,191 |

<p class="caption">Table 2. Detection F1 vs CNP re-identification leakage on ro-realskeleton-v1 (1,520 gold CNPs; Detection F1 is the contamination-free real-skeleton F1 from Table 1, which no baseline was trained on; Wilson 95% confidence intervals on leak-rate). "Quasi-IDs leaked" is a deterministic exposure tally — exactly 3 × missed CNPs, since each un-redacted CNP discloses sex, date of birth, and county — not an inferential estimate.</p>

The strongest detector on this track, GLiNER (F1 0.85), leaks 22.3% of CNPs; tabularisai leaks the
most (26.1%) at high precision; while the *weakest* detector, privacy-filter (F1 0.36), leaks the least
(1.1%). Its low leak-rate is earned, not accidental: of the 1,520 CNPs, privacy-filter flags 1,503,
labelling **96% (1,456) as account numbers** and 3% as phone numbers — and a flagged span is redacted
regardless of type.

This is the mechanism behind the dissociation, and it is specific. The leak metric rewards *coverage*
(any-overlap redaction) while F1 rewards *exact span and type*, so a blanket redactor like
privacy-filter maximizes protection while scoring worst on typed F1. The effect is carried by that one
model: among the three systems that actually *type* CNPs (OpenMed, GLiNER, tabularisai), leak-rate is
flat-to-rising in F1 and all leak 19.5–26.1% — no dissociation among them. The finding is therefore
not "better detectors leak more"; it is that **coverage-based redaction and type-accurate detection
are different objectives**, and detection F1 measures only the latter. (GLiNER is zero-shot, so its F1
depends on the label prompt — a confound for any cross-system F1 comparison, and a further reason we
rest the claim on the per-model leak-rate intervals rather than on F1 rankings.) The leak-rate
differences themselves are individually significant: the Wilson 95% intervals for privacy-filter and
every other model do not overlap.

On the synthetic track leakage is ≤1.9% for all models (OpenMed
1.9%, privacy-filter 0.1%, GLiNER and tabularisai 0%): templated CNPs are trivially caught, which is
why a realistic-context gold is necessary to see the effect at all.

## Related Work

EuroPriv-Bench is designed to subsume, not compete with, prior resources, re-using their splits and
metrics where applicable. TAB [<a href="#ref-1">1</a>] contributes the privacy–utility framing
(English, legal). AI4Privacy [<a href="#ref-2">2</a>] supplies the cross-lingual general substrate.
MAPA [<a href="#ref-3">3</a>] and MEDDOCAN [<a href="#ref-5">5</a>] anchor the legal/clinical and
Spanish-clinical settings. MultiGraSCCo [<a href="#ref-4">4</a>] is the closest multilingual prior
benchmark; it is clinical-only and, per its own description, produced by machine-translating a German
corpus into other languages — localized native generation avoids the structurally invalid identifiers
(e.g. checksum-invalid national IDs) that translation produces. Piiranha [<a href="#ref-10">10</a>] is
included by citation only, as its CC-BY-NC-ND license precludes redistribution or use as a base model.

## Limitations

These are preliminary results. (i) The general-text gold is itself synthetic (AI4Privacy); the only
realistic-context track is Romanian, and even there the identifiers are synthetic injected into real
structure — we measure a *synthetic-context vs real-context* gap, not a synthetic-to-real-data gap.
(ii) The cross-system F1–leakage rank correlation is **descriptive over four systems** (Spearman
ρ = +0.80, not significant, p = 0.20) and is largely carried by one blanket-redacting model
(privacy-filter); we do not treat it as an effect estimate. The claim rests instead on the per-model
leak-rate differences, which **are** individually significant (non-overlapping Wilson 95% intervals,
Table 2), and on the coverage-vs-type mechanism in §5. (iii) OpenMed and tabularisai
were trained on AI4Privacy, the source of our general-text gold, so part of their general-text lead
reflects in-distribution advantage — the Romanian track, which no baseline has seen, is the cleaner
signal. (iv) The re-identification finding rests on one identifier type (the Romanian CNP) in one
language; we make no claim it generalizes to all identifiers or languages without further evidence.
(v) The anonymization/utility and membership-inference tracks are specified but not yet populated;
the present metric is re-identification *leakage*, hence the title.

## Reproducibility

All results are produced by the open harness (`europriv-bench`, v0.2.0) over the public dataset
(`klusai/europriv-bench`, taxonomy v0.2.0); each leaderboard row carries its provenance. Wilson 95%
intervals are computed from the published per-model CNP miss counts. GLiNER is zero-shot and its label
prompts are part of the configuration (in the code). The CNP-protection rule is the harness
definition stated in §4. Re-running `europriv run` against the published configs reproduces Tables 1–2.

<h2 class="unnumbered" id="references">References</h2>

<ol>
<li id="ref-1">Pilán, Lison, Øvrelid, Papadopoulou, Sánchez, Batet. "The Text Anonymization Benchmark (TAB): A Dedicated Corpus and Evaluation Framework for Text Anonymization." <em>Computational Linguistics</em> 48(4), 2022. doi:10.1162/coli_a_00458.</li>
<li id="ref-2">AI4Privacy. "OpenPII Masking" datasets (CC-BY-4.0). Hugging Face, <code>ai4privacy/open-pii-masking-500k-ai4privacy</code>. Accessed June 2026.</li>
<li id="ref-3">Ajausks et al. "The Multilingual Anonymisation Toolkit for Public Administrations (MAPA)." EAMT 2020; CEF Telecom project 2019-EU-IA-0045. Code: <code>github.com/MAPA-Consortium</code>; models on Hugging Face under <code>BSC-LT/</code>. Accessed June 2026.</li>
<li id="ref-4">"MultiGraSCCo: A Multilingual Anonymization Benchmark with Annotations of Personal Identifiers." 2026 preprint (German GraSCCo corpus machine-translated into further languages); builds on Modersohn et al., "GraSCCo," 2022. We were unable to resolve a stable DOI/arXiv locator at access time (June 2026).</li>
<li id="ref-5">Marimon et al. "MEDDOCAN: Medical Document Anonymization track (Spanish)." IberLEF, 2019.</li>
<li id="ref-6">OpenAI. "Privacy Filter" (<code>openai/privacy-filter</code>). Hugging Face, 2026. Accessed June 2026.</li>
<li id="ref-7">OpenMed. "privacy-filter-multilingual" (<code>OpenMed/privacy-filter-multilingual</code>), 16 languages / 54 types. Hugging Face, 2026. Accessed June 2026.</li>
<li id="ref-8">tabularisai. "eu-pii-safeguard" (<code>tabularisai/eu-pii-safeguard</code>), XLM-R, 26 EU languages. Hugging Face. Accessed June 2026.</li>
<li id="ref-9">Zaratiana, Tomeh, Holat, Charnois. "GLiNER: Generalist Model for NER" (<code>urchade/gliner_multi_pii-v1</code>). 2023. arXiv:2311.08526.</li>
<li id="ref-10">iiiorg. "Piiranha-v1" (mDeBERTa-v3), license CC-BY-NC-ND-4.0. Hugging Face, 2024.</li>
</ol>

<hr>
<p class="arxiv-fn"><a id="fn-1"></a><sup>1</sup> We hold the per-CNP quasi-identifier count at three (date of birth, sex, county) as a conservative lower bound; the first digit jointly encodes sex and birth-century, and digits 8–9 encode the county of <em>registration</em> (with reserved codes for Bucharest sectors), not necessarily of residence. <a href="#fnref-1">↩</a></p>
