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
cite_order: [tab, ai4privacy, mapa, multigrascco, meddocan, openai, openmed, tabularisai, gliner, piiranha, ratbench, gliner2pii, spy, medprivbench, privacibench, piibench, deusser]
cover_title: "EuroPriv-Bench"
cover_sub: "Pan-European de-identification benchmark · 7 languages · re-identification-risk metric"
tldr: "Detection F1 doesn't predict privacy: the weakest PII detector leaks the fewest Romanian national IDs (1.4%), while the strongest leak 26–35%. A unified, openly-licensed pan-European de-identification benchmark that scores re-identification risk — not just detection F1."
tags: [De-identification, Re-identification risk, Romanian CNP, GDPR taxonomy, 7 languages]
abstract: >-
  Privacy-focused NLP for European languages is served by fragmented resources: the Text
  Anonymization Benchmark provides privacy–utility metrics but is English- and legal-only;
  AI4Privacy offers cross-lingual European detection data without re-identification metrics;
  MAPA covers 24 EU languages and both legal and clinical text but as a detection toolkit, not a
  comparative leaderboard; and MultiGraSCCo is multilingual but clinical-only and translation-based.
  Concurrent, independent work — RAT-Bench — contributes a hosted re-identification-risk benchmark
  but is built on U.S. demographics (English/Spanish/Chinese), with no legal text and no
  GDPR-aligned taxonomy; recent PII models such as GLiNER2-PII ship strong systems with no
  standardized European evaluation, and a 2025 survey of the field flags exactly this missing
  standardized multilingual benchmark. We introduce EuroPriv-Bench, the first unified,
  openly-licensed leaderboard for European cross-lingual legal and clinical de-identification with a
  harmonized GDPR-aligned entity taxonomy and a re-identification-risk metric. It unifies
  (a) European cross-lingual breadth, (b) both legal and clinical text, (c) one harmonized
  GDPR-aligned entity taxonomy, and (d) a re-identification-risk metric alongside detection F1, in
  one reproducible, openly-licensed, leaderboard-style suite. We build on the
  prior art rather than replacing it, re-using its label schemes through a documented crosswalk.
  Evaluating four public systems on realistic Romanian documents, we find that detection F1 does
  not track national-identifier (CNP) protection: the best detector is not the best protector.
  OpenAI privacy-filter — the weakest detector (F1 0.36) — leaks only 1.4% of CNPs (95% CI 0.9–2.3)
  because it labels 96% of them as account numbers and redacts them regardless of type, whereas the
  three detectors that type CNPs all leak 26–35% — privacy-filter's Wilson interval lies entirely
  below all three (non-overlapping). GLiNER, the most accurate at F1 0.85, leaks 30.2%; tabularisai,
  despite a lower F1 (0.75), leaks the most, 35.4% (32.6–38.2). Coverage-based
  redaction and type-accurate detection are different objectives — F1 measures the latter, protection
  needs the former — so detection F1 is an unsafe proxy for re-identification protection, at least for
  national identifiers. We release the benchmark, harness, configs, and data so the gap is measurable.
---

## Introduction

Models advertising 94–97% F1 on English PII benchmarks tell us little about how they behave on
Dutch clinical notes or Romanian court decisions under a European privacy taxonomy. Yet the public
de-identification literature is fragmented along the axes that matter for EU deployment. The Text
Anonymization Benchmark (TAB) {% include cite.html key="tab" %} introduced privacy–utility metrics, but only
for English ECHR legal text. AI4Privacy {% include cite.html key="ai4privacy" %} provides cross-lingual European
detection data, but scores detection F1 only. MAPA {% include cite.html key="mapa" %} covers all 24 official
EU languages across legal and clinical text, but ships as a detection toolkit, not a comparative
leaderboard. MultiGraSCCo {% include cite.html key="multigrascco" %} is multilingual and GDPR-aware but clinical-only
and produced by machine translation. Concurrent, independent work — RAT-Bench {% include cite.html key="ratbench" %} —
contributes a hosted re-identification-risk benchmark, but is built on U.S. demographics
(English/Spanish/Chinese), with no legal text and no GDPR-aligned taxonomy. Recent PII models such as
GLiNER2-PII {% include cite.html key="gliner2pii" %} ship strong systems with **no standardized European
evaluation**, and a 2025 survey of the field {% include cite.html key="deusser" %} flags exactly this missing
standardized multilingual benchmark. And the privacy-filter model lineage — OpenAI's `privacy-filter`
{% include cite.html key="openai" %} and OpenMed's multilingual finetune {% include cite.html key="openmed" %} — ships capable
systems for which we found **no standardized public privacy-risk evaluation** as of June 2026.

EuroPriv-Bench is, to our knowledge, the first unified, openly-licensed leaderboard for European
cross-lingual legal *and* clinical de-identification with a harmonized GDPR-aligned entity taxonomy
and a re-identification-risk metric. No single prior artifact unifies (a) European cross-lingual
breadth, (b) both legal and clinical text, (c) one harmonized GDPR-aligned taxonomy, and (d) a
re-identification-risk metric, in a reproducible, openly-licensed leaderboard. Our
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
once.[^cnp] We decode the structure directly and report, over
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

We evaluate four public systems: OpenAI `privacy-filter` {% include cite.html key="openai" %}, OpenMed
`privacy-filter-multilingual` {% include cite.html key="openmed" %}, `tabularisai/eu-pii-safeguard`
{% include cite.html key="tabularisai" %}, and zero-shot GLiNER `gliner_multi_pii-v1` {% include cite.html key="gliner" %}. All
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

**The dissociation.** On `ro-realskeleton-v1` (1,500 documents, 1,123 gold CNPs), detection accuracy
does not predict protection: **the best detector is not the best protector.** The per-model contrast
is the evidence — and it is significant, because the Wilson 95% intervals on leak-rate separate the
systems (Table 2). With only four systems we do *not* lean on a correlation coefficient: the rank
order happens to run positive (Spearman ρ = +0.80), but over four points that is a descriptive
observation, not an estimate, and it is not statistically significant (exact permutation p = 0.33).
We therefore read
the result as "F1 does not track CNP protection," and explain *why* below — not as a monotonic law.

| Model | Detection F1 | CNP leak-rate (95% CI) | Quasi-IDs leaked |
|---|---|---|---|
| OpenAI privacy-filter | 0.36 | **1.4%** (0.9–2.3) | 48 |
| OpenMed | 0.58 | 26.4% (23.9–29.0) | 888 |
| GLiNER | **0.85** | 30.2% (27.6–32.9) | 1,017 |
| tabularisai | 0.75 | 35.4% (32.6–38.2) | 1,191 |

<p class="caption">Table 2. Detection F1 vs CNP re-identification leakage on ro-realskeleton-v1 (1,123 gold CNPs; Detection F1 is the contamination-free real-skeleton F1 from Table 1, which no baseline was trained on; Wilson 95% confidence intervals on leak-rate). "Quasi-IDs leaked" is a deterministic exposure tally — exactly 3 × missed CNPs, since each un-redacted CNP discloses sex, date of birth, and county — not an inferential estimate.</p>

The strongest detector on this track, GLiNER (F1 0.85), leaks 30.2% of CNPs; tabularisai leaks the
most (35.4%) at high precision; while the *weakest* detector, privacy-filter (F1 0.36), leaks the least
(1.4%). Its low leak-rate is earned, not accidental: of the 1,123 CNPs, privacy-filter flags 1,107,
labelling **96% (1,456) as account numbers** and 3% as phone numbers[^labeldump] — and a flagged span is redacted
regardless of type.

This is the mechanism behind the dissociation, and it is specific. The leak metric rewards *coverage*
(any-overlap redaction) while F1 rewards *exact span and type*, so a blanket redactor like
privacy-filter maximizes protection while scoring worst on typed F1. The effect is carried by that one
model: among the three systems that actually *type* CNPs (OpenMed, GLiNER, tabularisai), leak-rate is
flat-to-rising in F1 and all leak 26.4–35.4% — no dissociation among them. The finding is therefore
not "better detectors leak more"; it is that **coverage-based redaction and type-accurate detection
are different objectives**, and detection F1 measures only the latter. (GLiNER is zero-shot, so its F1
depends on the label prompt — a confound for any cross-system F1 comparison, and a further reason we
rest the claim on the per-model leak-rate intervals rather than on F1 rankings.) The one clean
statistical separation is privacy-filter's: its Wilson 95% interval (0.9–2.3%) does not overlap any
other model's. The three type-accurate detectors are not all mutually separable — OpenMed–GLiNER and
GLiNER–tabularisai overlap (though OpenMed and tabularisai do not), so they form a connected chain
through GLiNER rather than a clean ordering — so among them we make no graded significance claim. The
sharp, significant contrast is the blanket redactor versus everything else.

On the synthetic track leakage is ≤1.9% for all models (OpenMed
1.9%, privacy-filter 0.1%, GLiNER and tabularisai 0%): templated CNPs are trivially caught, which is
why a realistic-context gold is necessary to see the effect at all.

## Related Work

EuroPriv-Bench is designed to subsume, not compete with, prior resources, re-using their splits and
metrics where applicable. We position it against the closest prior and concurrent artifacts along six
axes: (a) EU cross-lingual coverage, (b) legal text, (c) clinical text, (d) a harmonized GDPR-aligned
entity taxonomy, (e) a re-identification-risk metric, and (f) an open, reproducible leaderboard.
Table 3 summarizes coverage: every prior artifact is missing at least two of these axes, and
EuroPriv-Bench is the first to fill all six in a single suite.

| Artifact | (a) EU x-ling | (b) legal | (c) clinical | (d) GDPR tax. | (e) re-id metric | (f) leaderboard |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| TAB {% include cite.html key="tab" %} | ✗ | ✓ | ✗ | ✗ | ✓ | ✗ |
| AI4Privacy {% include cite.html key="ai4privacy" %} | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ |
| MAPA {% include cite.html key="mapa" %} | ✓ | ✓ | ✓ | ✗ | ✗ | ✗ |
| MultiGraSCCo {% include cite.html key="multigrascco" %} | ✓ | ✗ | ✓ | ✗ | ✗ | ✗ |
| MEDDOCAN {% include cite.html key="meddocan" %} | ✗ | ✗ | ✓ | ✗ | ✗ | ✗ |
| RAT-Bench {% include cite.html key="ratbench" %} | ✗ | ✗ | ✓ | ✗ | ✓ | ✓ |
| GLiNER2-PII {% include cite.html key="gliner2pii" %} | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ |
| SPY {% include cite.html key="spy" %} | ✗ | ✓ | ✓ | ✗ | ✗ | ✗ |
| MedPriv-Bench {% include cite.html key="medprivbench" %} | ✗ | ✗ | ✓ | ✗ | ✗ | ✗ |
| PrivaCI-Bench {% include cite.html key="privacibench" %} | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |
| PIIBench {% include cite.html key="piibench" %} | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ |
| **EuroPriv-Bench (ours)** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

<p class="caption">Table 3. Coverage of related and concurrent artifacts. Columns: (a) EU cross-lingual, (b) legal-domain de-identification text, (c) clinical-domain de-identification text, (d) harmonized GDPR taxonomy, (e) span/document-level re-identification-risk metric, (f) open reproducible leaderboard. Every prior row is missing ≥2 columns; only EuroPriv-Bench fills all six.</p>

The closest EU-breadth, dual-domain prior art is MAPA {% include cite.html key="mapa" %} (24 EU languages,
legal *and* clinical), but it is a detection toolkit with no re-identification metric and no open
leaderboard. The legal-domain re-identification lineage is anchored by TAB {% include cite.html key="tab" %},
which pairs a privacy–utility / re-identification framing with legal text but is English-only.
AI4Privacy {% include cite.html key="ai4privacy" %} contributes cross-lingual European detection data without
a re-identification metric or a GDPR-aligned taxonomy. MultiGraSCCo {% include cite.html key="multigrascco" %} is
the closest multilingual prior benchmark; it is clinical-only and, per its own description, produced by
machine-translating a German corpus into other languages — localized native generation avoids the
structurally invalid identifiers (e.g. checksum-invalid national IDs) that translation produces.
MEDDOCAN {% include cite.html key="meddocan" %} is a clinical de-identification track but Spanish-only.
EuroPriv-Bench is best understood as the unification of what MAPA (EU breadth + dual domain) and TAB
(legal text + re-identification metric) each establish in isolation, under one harmonized GDPR-aligned
taxonomy.

RAT-Bench {% include cite.html key="ratbench" %} is concurrent and independent work: a 2026 hosted
re-identification-risk leaderboard. It is complementary rather than overlapping — it is built on U.S.
demographic statistics over English, Spanish, and Chinese, contains no legal text, and uses no
GDPR-aligned taxonomy, so it does not address the European legal/clinical de-identification setting
EuroPriv-Bench targets. Recent PII models and corpora are similarly partial: GLiNER2-PII
{% include cite.html key="gliner2pii" %} is a strong multilingual (seven-language, 42-type) PII model but ships
no benchmark, no re-identification metric, and no legal or clinical coverage; the SPY benchmark
{% include cite.html key="spy" %} does contain legal and clinical de-identification text, but it is English-only
synthetic data with no EU cross-lingual breadth, no GDPR-aligned taxonomy, and no re-identification-risk
metric; MedPriv-Bench {% include cite.html key="medprivbench" %} is a clinical-only LLM-QA privacy-utility
benchmark; PrivaCI-Bench {% include cite.html key="privacibench" %} evaluates contextual integrity and legal
compliance rather than span-level de-identification; and PIIBench {% include cite.html key="piibench" %}
consolidates ten public PII datasets for detection only. A 2025 survey of text anonymization
{% include cite.html key="deusser" %} explicitly flags the absence of a standardized multilingual
de-identification benchmark — the gap EuroPriv-Bench is built to close.

Piiranha {% include cite.html key="piiranha" %} is included by citation only, as its CC-BY-NC-ND license
precludes redistribution or use as a base model.

## Limitations

These are preliminary results. (i) The general-text gold is itself synthetic (AI4Privacy); the only
realistic-context track is Romanian, and even there the identifiers are synthetic injected into real
structure — we measure a *synthetic-context vs real-context* gap, not a synthetic-to-real-data gap.
(ii) The cross-system F1–leakage rank correlation is **descriptive over four systems** (Spearman
ρ = +0.80, not significant, exact permutation p = 0.33) and is largely carried by one blanket-redacting
model (privacy-filter); we do not treat it as an effect estimate. The claim rests instead on
privacy-filter's leak-rate, whose Wilson 95% interval is separated from every other model's
(non-overlapping, Table 2), and on the coverage-vs-type mechanism in §5 — the three type-accurate
detectors are *not* all mutually separable (the adjacent pairs overlap through GLiNER; only OpenMed
and tabularisai separate), so the protective effect we report is privacy-filter's blanket coverage,
not a graded one across detectors. (iii) OpenMed and tabularisai
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

{% include references.html %}

[^cnp]: We hold the per-CNP quasi-identifier count at three (date of birth, sex, county) as a conservative lower bound; the first digit jointly encodes sex and birth-century, and digits 8–9 encode the county of *registration* (with reserved codes for Bucharest sectors), not necessarily of residence.

[^labeldump]: The per-predicted-label breakdown (96% ACCOUNT_ID, 3% phone) is not a scored leaderboard metric; it comes from the harness's per-label prediction dump for privacy-filter on this config (regenerated by `europriv run --dump-predictions`), and is internally consistent with the 1,107/1,123 flagged and 16 missed.
