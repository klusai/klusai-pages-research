---
layout: paper
title: "Detection Is Not Re-identification: A Unified Dissociation and an Open Protector for European De-identification"
permalink: /papers/dissociation-protector/
date: 2026-06-14
venue: "KlusAI Technical Report"
authors: "KlusAI Research"
affiliation: "KlusAI"
contact: "research@klusai.com"
status: "Working paper · preliminary findings · not peer-reviewed · synthetic real-skeleton tracks are config_status = dev (gated); TAB direct-identifier result is on real external gold, citable in scope"
data: "https://huggingface.co/datasets/klusai/europriv-bench"
code: "https://github.com/klusai/europriv-bench"
model: "https://huggingface.co/klusai/kp-deid-xlmr-560m-legal"
leaderboard: "/leaderboard/"
cite_order: [tab, ratbench, ai4privacy, mapa, multigrascco, meddocan, gliner2pii, spy, gliner, openai, openmed, tabularisai]
cover_title: "Detection ≠ Re-identification"
cover_sub: "A unified dissociation · 3 national-ID schemes (RO/PL/IT) · real legal gold (TAB ECHR) · an openly-released protector"
tldr: "On real external legal gold (TAB ECHR; Pilán et al. 2022), a CJEU-structure-trained checkpoint attains the lowest direct-identifier leak rate, 0.095 (95% CI 0.065–0.136, n = 264 DIRECT subjects), versus the next-best 0.496 (spaCy) and 0.500 (Presidio) — a paired-bootstrap improvement of Δ = −0.40 (95% CI −0.477 to −0.322), 3-seed confirmed; it is openly released as klusai/kp-deid-xlmr-560m-legal. The point is the dissociation, not a leaderboard win: detection F1 does not track re-identification protection. The same dissociation holds across three decode-bearing national-ID schemes (RO CNP, PL PESEL, IT codice fiscale) where a high-F1 detector (GLiNER, F1 0.85) still leaks 30.2% of CNP subjects while an openly-released protector leaks 0% at F1 0.74. We reserve 're-identification' for the deterministic national-ID channel; the TAB axis is direct-identifier protection that bounds re-identification risk. Synthetic real-skeleton numbers are config_status = dev (a finding, not yet citable); the TAB direct-identifier result is on real external gold and is citable within its stated scope (single board, single architecture, TAB-EN-legal). No SOTA claim."
tags: [De-identification, Re-identification risk, Detection-protection dissociation, Romanian CNP, TAB ECHR, Open protector]
abstract: >-
  High aggregate detection scores are the standard way de-identification systems are reported and
  trusted. We show this aggregate masks the failures that matter most: the rare, high-stakes tokens
  that actually carry re-identification. Using the EuroPriv-Bench leaderboard, we present the first
  unified demonstration that detection entity-F1 and re-identification protection are dissociated — a
  high-F1 detector can still leak the decode-bearing national identifiers (Romanian CNP, Polish PESEL,
  Italian codice fiscale) through which a subject is provably re-identified — and we show the same
  dissociation survives on externally annotated, real legal gold (TAB ECHR). On the Romanian
  real-skeleton track a strong general PII detector reaches entity-F1 0.85 yet leaks 30.2% of distinct
  CNP subjects; a span-only spaCy baseline at F1 0.14 leaks 89%; while an openly-released protector
  trained for the redaction objective leaks 0% at F1 0.74. The dissociation holds across three
  national-ID schemes in three languages (RO/PL/IT) and across two Romanian template families, and is
  statistically significant under an item-paired McNemar test (e.g. p = 1.79 × 10⁻¹⁰² vs the F1
  leader). We reserve the term re-identification for this deterministic national-ID channel. On real
  external legal gold (TAB ECHR English; Pilán et al. 2022) we report a complementary, citable result
  on a separate axis: a CJEU-structure-trained checkpoint attains the lowest direct-identifier leak
  rate, 0.095 (95% CI 0.065–0.136, n = 264 DIRECT subjects, single seed; seed-robustness reported
  separately), versus the next-best 0.496 (spaCy) and 0.500 (Presidio) — a paired-bootstrap
  improvement of Δ = −0.40 (95% CI −0.477 to −0.322, n = 264 paired DIRECT subjects), 3-seed
  confirmed. We frame this as direct-identifier protection / re-identification-risk reduction on real
  legal gold — a broader axis than, and reported separately from, the deterministic national-ID
  re-identification channel above. We do not lead detection-F1 on TAB (synthetic training caps at
  0.340 vs Presidio 0.589); the dissociation is the point. This TAB checkpoint is openly released as
  klusai/kp-deid-xlmr-560m-legal; the openly-released kp-deid-mdeberta-280m protector is a different
  (280M) model evaluated on the national-ID tracks — both models are public and we keep them crisply
  distinct. We release the protector and the analysis harness. The synthetic real-skeleton results are
  config_status = dev (a finding, gated pending native-speaker + inter-annotator-agreement review); the
  TAB direct-identifier results are on real external gold and are citable within their stated scope. No
  SOTA claim is made anywhere in this paper.
---

> **Working paper — preliminary findings; not peer-reviewed.** The synthetic real-skeleton national-ID
> numbers are `config_status = dev`: a finding, pending native-speaker and inter-annotator-agreement
> validation, and **not yet citable**; no "best/strongest/SOTA" wording rests on them. The TAB
> direct-identifier result is on **real, externally peer-reviewed gold** and is citable **within its
> stated scope** (single board, single architecture, TAB-EN-legal). We make **no SOTA claim** anywhere.

## Introduction

**Thesis.** *Aggregate detection-F1 masks failures on the rare, high-stakes tokens that carry
re-identification: national IDs are the clearest provable case — deterministic and decode-bearing —
but not the whole of it.*

De-identification systems are routinely ranked by an aggregate detection metric (entity-level F1 or
recall). We argue this is the wrong target for a *privacy* guarantee. A single missed decode-bearing
national identifier — e.g. a Romanian CNP, which encodes date of birth, sex, and county of
registration — re-identifies a subject regardless of how many low-stakes spans were caught. Because
such identifiers are rare relative to the token mass, a model can post a high aggregate F1 while still
leaking them at a high rate.

This is, to our knowledge, the first *unified* demonstration — across three national-ID schemes,
three languages, and two template families on one reproducible leaderboard, *and on externally
annotated real legal gold (TAB ECHR)* — that detection accuracy and re-identification protection are
*dissociated*. We claim "first *unified*", not "first": the individual ingredients exist in the prior
art (§Related Work), but no prior artifact combines them; we re-verify this positioning against the
EuroPriv-Bench prior-art scan before any broadened public claim. We make the dissociation visual (a
Pareto frontier, Figure 1), statistically significant (item-paired McNemar on the synthetic tracks; a
paired bootstrap on the real TAB gold), and actionable (an openly-released protector that escapes the
leak axis on the national-ID tracks, and a structure-trained protector that leads the
direct-identifier-leak axis on real legal gold). *Re-identification* is used **only** for the
deterministic national-ID channel; the TAB DIRECT axis is reported as *direct-identifier protection*
that bounds re-identification *risk*; all other channels are framed as residual distinctiveness.

This paper builds on EuroPriv-Bench {% include cite.html key="tab" %}[^bench] — the unified
pan-European de-identification benchmark and leaderboard — and contributes a result that is orthogonal
to the benchmark itself: a unified *detection ≠ re-identification* dissociation and an open protector.

### Contributions

1. A unified **detection ≠ re-identification** dissociation grounded in public leaderboard numbers
   across RO/PL/IT national-ID schemes and two Romanian template families.
2. An item-paired significance test (McNemar) on per-subject national-ID protection, and a
   Pareto-frontier visualization of F1 vs leak (Figure 1).
3. A **real-gold confirmation on TAB ECHR**: the same dissociation holds on externally annotated legal
   gold, and a CJEU-structure-trained checkpoint (`kp-cjeu-structure`) leads the direct-identifier-leak
   (re-identification-*risk*) axis — DIRECT-leak 0.095 vs runner-up ≈0.50, 3-seed robust and
   paired-bootstrap significant (Δ = −0.40, 95% CI −0.477 to −0.322, n = 264), zero-shot from a
   contamination-controlled CJEU real-*structure* corpus. This checkpoint is **openly released** as
   [`klusai/kp-deid-xlmr-560m-legal`](https://huggingface.co/klusai/kp-deid-xlmr-560m-legal) and is
   distinct from the (also public) protector of contribution 4; the latter ranks 7th on this TAB axis
   and we never conflate the two.
4. An openly-released protector (`kp-deid-mdeberta-280m`) that sits *off* the detection-optimal
   frontier on the national-ID tracks: 0% national-ID leak at non-maximal F1. "The protector" is
   therefore not a single model — `kp-deid-mdeberta-280m` leads the national-ID axis, while a distinct,
   also openly-released protector (`klusai/kp-deid-xlmr-560m-legal`) leads the TAB direct-identifier
   axis.
5. A **preliminary, in-progress** second mechanism (name-in-context residual leak) reported as
   corroborating evidence only, and a quasi-identifier-combination metric stated as future work.

## Two Leak Axes, Two Evidentiary Bases

We measure identifier disclosure on the post-detection *residual* (what a de-identification model
would leave un-redacted), never on raw text, along two distinct axes that must not be conflated.

**Axis 1 — deterministic national-ID re-identification (synthetic gold).** This is the channel for
which we reserve the term *re-identification*. A subject is one distinct, checksum-valid national-ID
value within one document, keyed by `(doc, country, normalized value)` and deduplicated (a CNP
repeated across the CNP and CASS fields is one subject). The subject is *protected* iff **every**
occurrence is redacted and *leaks* iff **any** occurrence survives; the leak-rate is the fraction of
distinct decode-bearing subjects left un-redacted, with a 95% Wilson interval. A miss is
decode-bearing because the value deterministically discloses date of birth, sex, and county. This
metric runs on the *synthetic* real-skeleton tracks (`ro/pl/it-realskeleton-v1`); the identifiers, and
therefore the leak counts, are generated, not drawn from a real population (`config_status = dev`,
gated pending native-speaker + IAA validation). We reuse the EuroPriv-Bench harmonized GDPR-aligned
taxonomy rather than re-deriving it.

All headline numbers on this axis are read from the distinct-subject configs `ro/pl/it-realskeleton-v1`
(n = 1,123 / 1,096 / 1,111 distinct national-ID subjects after dedup), **not** the leaderboard file's
occurrence-level `legal-realskeleton-v1` view (n = 1,500 occurrences, pre-dedup); we never mix the two
bases within a number.

**Axis 2 — DIRECT/QUASI identifier leak on real legal gold (TAB).** This axis is grounded in a *real*,
externally peer-reviewed, human-annotated corpus: the Text Anonymization Benchmark (TAB)
{% include cite.html key="tab" %}, 127 European Court of Human Rights judgments remapped onto the
EuroPriv-Bench KP taxonomy (`tab-echr-legal-en-v1`, `config_status = real-external-gold`). Because the
annotations are externally peer-reviewed human gold, this track does **not** depend on the program's
own native-speaker/IAA gate, which validates only *our* synthetic skeletons. We deliberately keep the
label distinct from Axis 1: a leaked DIRECT/QUASI identifier is a *residual identifier disclosure*, not
a deterministic decode, so we do not call it re-identification. A lower direct-identifier leak rate
means lower re-identification *risk*.

The two metrics share the per-subject, post-detection-residual, "leak iff any occurrence survives"
machinery and Wilson-CI reporting, but differ in three load-bearing ways: (i) the national-ID metric
scores *synthetic* `dev`-track subjects while the TAB metric scores *real* externally-annotated
subjects (so the TAB axis is not under the synthetic-track gate); (ii) a national-ID subject is keyed
by a checksum-validated normalized value and a miss is a *deterministic decode* (DOB + sex + county) —
which is why we call it re-identification — whereas a TAB subject is keyed by an annotated coreference
id + identifier type and a miss is a *residual disclosure* graded DIRECT vs QUASI; (iii) the
national-ID metric splits by decode-bearing vs coverage-only family, while the TAB metric splits by the
human-annotated DIRECT/QUASI sensitivity the national-ID schemes do not carry.

## The Detection ≠ Re-identification Dissociation (Synthetic National-ID Tracks)

On the Romanian real-skeleton track (`ro-realskeleton-v1`, n = 1,123 distinct CNP subjects), detection
F1 and CNP leak-rate move *together*, not against each other, among content-NER detectors. A strong
general PII detector (GLiNER `multi_pii`) reaches entity-F1 0.85 yet leaks 30.2% of distinct CNP
subjects; a span-only spaCy baseline at F1 0.14 leaks 89.0%; whereas the kp-deid protector leaks 0% at
F1 0.74 — it sits *off* the detection-optimal frontier (Figure 1, Table 1). Higher detection accuracy
did not buy privacy protection.

<figure class="arxiv-figure">
  <div class="arxiv-figure-frame">
    <picture>
      <source srcset="{{ '/assets/papers/pareto_dissociation_ro_realskeleton.svg' | relative_url }}" type="image/svg+xml" />
      <img src="{{ '/assets/papers/pareto_dissociation_ro_realskeleton.png' | relative_url }}"
           alt="Scatter of detection entity-F1 (x) against CNP re-identification leak-rate (y) on ro-realskeleton-v1, with Wilson 95% confidence-interval error bars. Content-NER detectors lie on a 'bad' frontier where higher F1 does not imply lower leak; the kp-deid protector sits off it at near-zero leak-rate." />
    </picture>
  </div>
  <figcaption>Figure 1. Detection accuracy does <em>not</em> buy re-identification protection. Each point is one scored model on <code>ro-realskeleton-v1</code>: detection entity-F1 (x) vs per-subject CNP re-identification leak-rate (y), with 95% Wilson CI error bars (n = 1,123 distinct CNP subjects). Content-NER detectors lie on the "bad" frontier (higher F1 ⇏ lower leak); kp-deid (ringed) sits off it at 0% leak. <code>config_status = dev</code> (contamination-controlled, <strong>not yet citable-validated</strong>; gated pending native-speaker + inter-annotator-agreement review). Figure regenerated from the live leaderboard — no number is hardcoded.</figcaption>
</figure>

| Track (ID scheme) | Model | Detection F1 | Re-id leak-rate |
|---|---|---|---|
| RO (CNP) | GLiNER multi-pii | 0.85 | 30.2% |
| RO (CNP) | GLiNER2-base | 0.64 | 28.6% |
| RO (CNP) | OpenMed privacy-filter-ml | 0.58 | 26.4% |
| RO (CNP) | spaCy `en_core_web_lg` | 0.14 | 89.0% |
| RO (CNP) | **kp-deid (ours)** | 0.74 | **0%** |
| PL (PESEL) | GLiNER multi-pii | 0.82 | 57.8% |
| PL (PESEL) | **kp-deid (ours)** | 0.76 | **0%** |
| IT (codice fiscale) | GLiNER multi-pii | 0.86 | 36.2% |
| IT (codice fiscale) | **kp-deid (ours)** | 0.70 | **0%** |

<p class="caption">Table 1. Detection F1 vs national-ID re-identification leak-rate across three national-ID schemes in three languages (real-skeleton tracks). Leak-rate = fraction of distinct gold national-ID subjects left un-redacted. All entries <code>config_status = dev</code>; numbers read from the distinct-subject configs <code>ro/pl/it-realskeleton-v1</code> (n = 1,123 / 1,096 / 1,111 after dedup), not the file's occurrence-level <code>legal-realskeleton-v1</code> (n = 1,500) view. kp-deid (ours) is the only system at 0% leak on every track.</p>

**It holds across schemes, languages, and template families.** The dissociation is not a Romanian
artifact. It reproduces on Polish PESEL (GLiNER F1 0.82, leak 57.8%; kp-deid F1 0.76, leak 0%) and
Italian codice fiscale (GLiNER F1 0.86, leak 36.2%; kp-deid F1 0.70, leak 0%). It also holds across two
independent Romanian template families that share no skeleton text (official correspondence, n = 190
distinct CNP subjects; academic registry, n = 250): a difference-of-proportions test with Newcombe
(1998) hybrid-score CIs shows the per-family gap (typed-detector leak minus protector leak) CI excludes
zero for the *typed content-NER* detectors in both families. The qualifier "typed content-NER" is
load-bearing: the rule/recognizer-based Presidio and the privacy-filter classifier do *not* exclude
zero in the official-correspondence family (their CNP behavior is unstable across the two families),
which is why we scope the Presidio CNP "tie" below to the whole-track n = 1,123 basis rather than the
family split.

**Statistical significance (item-paired McNemar).** We test per-subject national-ID protection with an
item-paired McNemar test (each distinct gold subject's national ID was either redacted or leaked; exact
two-sided binomial p on the discordant pairs). On `ro-realskeleton-v1`, kp-deid vs the F1 leader
(GLiNER) gives discordant counts b = 339, c = 0 (p = 1.79 × 10⁻¹⁰²): kp-deid protects subjects GLiNER
leaks, never the reverse. kp-deid vs privacy-filter gives b = 16, c = 0 (p = 3.05 × 10⁻⁵). A genuine
tie is reported honestly: kp-deid vs Presidio gives b = c = 0, p = 1 (both reach 0% CNP leak *on the
whole-track n = 1,123 distinct-subject basis used for this test*) — the correct null result, not
evidence for either system. We scope the tie to that basis deliberately: on the smaller per-family
split Presidio's CNP leak is unstable (0% in Family A, 90% in Family B), while kp-deid leaks 0% in both
families and on the whole track.

## The Dissociation on Real Legal Gold (TAB)

The synthetic real-skeleton tracks establish the dissociation under contamination-controlled but
synthetic conditions. We now show it survives on *externally annotated, real legal gold*: the Text
Anonymization Benchmark (TAB) {% include cite.html key="tab" %}, drawn from European Court of Human
Rights (ECHR) judgments. TAB ships its own human DIRECT/QUASI identifier annotations, so the
re-identification-*risk* axis is defined by an external party, not by us. We score it with the
per-subject fraction of TAB-annotated DIRECT identifiers left un-redacted on the post-detection residual
(lower is safer; n = 264 distinct DIRECT subjects, 3,701 QUASI subjects). We call this the
*re-identification-risk axis* (a lower direct-identifier leak means lower re-identification risk), but
the measured quantity is a *direct-identifier leak rate*, not a re-identification rate — the latter is
reserved for the deterministic national-ID channel.

| Rank | Model | DIRECT-leak ↓ | 95% CI | Detection F1 |
|---|---|---|---|---|
| **1** | **kp-cjeu-structure (ours)**† | **0.095** | [0.065, 0.136] | 0.340 |
| 2 | spaCy `en_core_web_lg` | 0.496 | [0.436, 0.556] | 0.480 |
| 3 | Presidio | 0.500 | [0.440, 0.560] | 0.589 |
| 4 | GLiNER multi-pii | 0.599 | — | 0.357 |
| 5 | tabularisai eu-pii-safeguard | 0.625 | — | 0.073 |
| 6 | GLiNER2-base | 0.651 | — | 0.545 |
| 7 | kp-deid-mdeberta-280m (ours) | 0.674 | — | 0.199 |
| 8 | kp-cjeu-realprose (ours)† | 0.867 | — | 0.265 |

<p class="caption">Table 2. Re-identification-risk board on <strong>real legal gold</strong> (TAB ECHR, English; <code>tab-echr-legal-en-v1</code>), ranked by per-subject DIRECT-identifier leak-rate (ascending; lower = less re-identification risk) on the post-detection residual. n = 264 distinct DIRECT subjects; 95% CIs are Wilson intervals on these 264 subjects (single seed; seed-robustness below). Detection F1 is strict entity-F1 on the same docs. "DIRECT-leak" is the privacy axis; QUASI leaks are residual distinctiveness, not direct re-identification. †Scored from a local checkpoint (identical weights); the #1 row is <strong>openly released</strong> as <code>klusai/kp-deid-xlmr-560m-legal</code>. <code>config_status = real-external-gold</code> (citable within scope; not under the synthetic-track gate). No SOTA / best-protector wording.</p>

The structure-trained protector `kp-cjeu-structure` leaks 9.5% of distinct DIRECT subjects, roughly 5×
fewer than the next-best system (spaCy 49.6%, Presidio 50.0%); its Wilson CI [0.065, 0.136] does not
overlap theirs. It reaches this from a real-legal-*structure* / synthetic-PII training corpus (CJEU)
evaluated *zero-shot* on ECHR/TAB, with a verified contamination guard (CJEU ≠ ECHR; 0 document and
0 verbatim-sentence overlap). The local-checkpoint rows run through the *identical* leak and strict
entity-F1 code path as the adapter-scored entries (same tokenizer, span-matching, and gold); only the
weight-loading differs — so the "Presidio leads detection / we lead protection" dissociation is not a
scoring-pipeline artifact.

**Detection-F1 and leak are dissociated on real data too.** The *highest* detection-F1 system,
Presidio (0.589), is only the 3rd-safest (50.0% DIRECT-leak); the second strongest detector,
GLiNER2-base (F1 0.545), is 6th-safest (65.1% leak). Conversely the #1-on-privacy `kp-cjeu-structure`
sits at detection-F1 0.340 (5th on detection) yet leaks 5× fewer DIRECT identifiers than anything above
it. Strict entity-F1 penalises span-boundary and entity-type disagreement that does not matter for
privacy, while the re-id-risk metric rewards what does — not *leaving identifiers behind*. On
externally annotated real legal text, ranking by detection accuracy and ranking by direct-identifier
protection produce essentially *different* orderings: the dissociation is not an artifact of synthetic
data.

**The #1 is 3-seed robust and paired-bootstrap significant.** Across three seeds (0, 1, 2), DIRECT-leak
is {0.0947, 0.0985, 0.0985} (mean 0.097, range 0.004) — two orders of magnitude below the gap to spaCy
(0.496); detection-F1 across the same seeds is {0.340, 0.309, 0.317}. On the 264 DIRECT subjects shared
with the runner-up (spaCy), the per-subject DIRECT-leak difference is Δ(kp − spacy) = −0.40 (0.0947 vs
0.4962), 95% CI [−0.477, −0.322] over 2,000 resamples — fully below zero, so `kp-cjeu-structure` leaks
significantly fewer DIRECT identifiers than the next-best system.

**The win is not over-tagging.** A trivial way to drive leak toward zero is to redact everything;
`kp-cjeu-structure` does *not* do this. On TAB it predicts non-`O` (would-redact) tokens at 9.1%,
*below* the gold non-`O` rate of 11.3% — it under-tags overall rather than blanket-redacting. Its
over-redaction rate (false-positive redacted tokens) is 4.3%, a low utility cost. The low leak comes
from efficiently touching the *right* identifier tokens, not from carpet redaction.

**We do not lead detection-F1 (a citable negative).** On TAB *detection*-F1, synthetic training caps
below Presidio's 0.589: a generic-synthetic recipe reaches only 0.244, the real-*structure* (CJEU)
recipe is the best of the synthetic regimes at 0.340, and the real-*prose* recipe is 0.265 — all far
below Presidio. Synthesis closes the *protection* gap (direct-identifier leak), not the raw detection
gap. We lead the direct-identifier-protection axis, not detection-F1.

**Scope and honesty.** We report this on *one* board (TAB, English legal). The leak metric is *ours*
(competitors publish only detection-F1) but it is grounded in TAB's own external DIRECT/QUASI
annotations, not a self-serving construct; the claim is "`kp-cjeu-structure` leads on direct-identifier
protection (re-identification *risk*)," not "beats competitors on detection-F1." The training corpus is
real legal *structure* with checksum-/format-valid *synthetic* PII (not real PII). The TAB-leading
checkpoint is openly released as
[`klusai/kp-deid-xlmr-560m-legal`](https://huggingface.co/klusai/kp-deid-xlmr-560m-legal); the
openly-released `kp-deid-mdeberta-280m` protector is a *different* model and ranks 7th on this TAB axis.
We make no "best/strongest/SOTA" claim. Breadth (other languages and domains) is the multilingual
follow-up.

## An Open Protector that Escapes the Leak Axis

We release [`kp-deid-mdeberta-280m`](https://huggingface.co/klusai/kp-deid-mdeberta-280m), a 280M-parameter
protector trained for the redaction objective rather than for span detection. It attains 0% national-ID
leak on all three real-skeleton tracks (RO/PL/IT) at competitive but non-maximal detection F1 (Table 1),
i.e. it sits off the detection-optimal frontier. The model and scoring harness are openly released;
results are reproduced by CI through the public submission protocol, never self-reported.

This 0% figure is specific to the *synthetic* national-ID channel. On the *real* TAB ECHR gold, the
same released `kp-deid-mdeberta-280m` is *not* the model that escapes the leak axis: it ranks 7th of 8
on DIRECT-identifier leak (0.674). The model that leads the real-gold direct-identifier axis is the
structure-trained `kp-cjeu-structure` (9.5% leak), a *distinct* checkpoint that is itself openly
released as [`klusai/kp-deid-xlmr-560m-legal`](https://huggingface.co/klusai/kp-deid-xlmr-560m-legal).
"The protector" is therefore better read as a *family* of redaction-trained models, both now public:
the `kp-deid-mdeberta-280m` model (280M, mDeBERTa backbone) leads the synthetic national-ID axis, while
`klusai/kp-deid-xlmr-560m-legal` (560M, XLM-R backbone) leads the real TAB direct-identifier axis. A
reader must not carry the synthetic-track "0% leak" onto TAB.

Both are trained for the redaction objective on real legal *structure* populated with
checksum-/format-valid *synthetic* PII; no real personal data and no TAB/ECHR source text, annotations,
or documents enter training. A documented model card with full training-data provenance is in
preparation; a broadened multilingual `kp-deid` v2 is future work.

## Corroborating Evidence: A Second, Independent Mechanism (Preliminary)

**Preliminary / in-progress — corroborating only; not a headline result and not yet reconciled with the
board.** Beyond the deterministic national-ID channel, an early analysis measures a second,
*independent* channel: a `PERSON` full name left un-redacted on the post-detection residual — a
*name-in-context leak*, i.e. *residual distinctiveness*, which we explicitly do **not** call
re-identification. On `ro-realskeleton-v1` (whole-track distinct-subject basis, where Presidio's
national-ID leak is 0%), Presidio leaks 0% of national IDs but ~13.7% of names; spaCy shows the inverse
profile (high ID leak, low name leak); kp-deid leaks 0% on both. A per-document 2×2 cross-tab indicates
the two channels are largely independent — different systems fail on different channels — which is why
an aggregate detection score hides both.

**Why this is not yet citable.** The name channel's sample basis (`split:test`; 440 national-ID
subjects and 681 name subjects) is *not yet reconciled* with the n = 1,123 used for the board-grounded
national-ID numbers, and the analysis predates the synthetic-track validation gate. We therefore present
it as corroboration of the *shape* of the dissociation, not as a measured headline number.

## Related Work

This paper builds on the EuroPriv-Bench benchmark and leaderboard, which itself subsumes the prior
de-identification art (TAB {% include cite.html key="tab" %}, AI4Privacy
{% include cite.html key="ai4privacy" %}, MAPA {% include cite.html key="mapa" %}, MultiGraSCCo
{% include cite.html key="multigrascco" %}, MEDDOCAN {% include cite.html key="meddocan" %}, GLiNER2-PII
{% include cite.html key="gliner2pii" %}, SPY {% include cite.html key="spy" %}). Our contribution is
orthogonal to the benchmark: a *unified dissociation* result and an open protector.

**TAB as an external real-data anchor.** TAB {% include cite.html key="tab" %} is the established,
peer-reviewed gold standard for legal de-identification: human-annotated ECHR judgments with a published
taxonomy that separates *direct* identifiers (names, case numbers) from *quasi*-identifiers. Because the
synthetic real-skeleton tracks are `config_status = dev` (gated on native-speaker review), we
additionally evaluate against TAB as an *external* anchor on real human-labelled text, where no
native-speaker validation gate applies. On TAB's direct-identifier leak axis (over 264 paired
direct-identifier subjects), our protector trained on real CJEU judgment *structure* (`kp-cjeu-structure`)
attains a 0.095 direct leak rate, ranking #1 — ahead of spaCy (0.496), Presidio (0.500), GLiNER (0.599),
tabularisai (0.625), GLiNER2 (0.651), and our own `kp-deid-mdeberta-280m` (0.674). The lead is robust
across three seeds and significant under a paired bootstrap against runner-up spaCy (Δ = −0.40, 95% CI
[−0.477, −0.322]), and is not an over-tagging artefact (predicted non-`O` 9.1% < gold 11.3%;
over-redaction 4.3%). Crucially, the same anchor exhibits the dissociation on an independent gold set:
the detection-F1 leader on TAB is Presidio (0.589), yet Presidio leaves 50% of direct identifiers in the
residual. We frame the TAB result as *direct-identifier protection on real legal gold* that bounds
re-identification *risk*, and reserve *re-identification* for the deterministic, decode-bearing
national-ID channel (CNP / PESEL / codice fiscale) of the main study; the two are distinct channels
measured on distinct data and should not be conflated. The TAB result reuses TAB's own externally-annotated
DIRECT/QUASI types; only the leak-rate aggregation is ours, and competitors are scored on TAB detection-F1
with their published configs (reproducible by CI), never self-reported.

**Concurrent re-identification-risk work.** The closest concurrent and independent work is RAT-Bench
{% include cite.html key="ratbench" %}, a hosted re-identification-risk leaderboard; it is complementary
rather than overlapping — it is built on U.S. demographics (English/Spanish/Chinese), contains no legal
text, and uses no GDPR-aligned taxonomy, so it does not address either the European national-ID
re-identification setting or the European legal direct-identifier setting studied here. The
privacy-filter lineage — OpenAI `privacy-filter` {% include cite.html key="openai" %} and OpenMed's
multilingual finetune {% include cite.html key="openmed" %} — and `tabularisai/eu-pii-safeguard`
{% include cite.html key="tabularisai" %} and zero-shot GLiNER {% include cite.html key="gliner" %} are
the public systems we evaluate as baselines.

**Scope and caveats on the TAB claim.** The TAB direct-identifier ranking is a citable result on real
external gold and is *not* subject to the synthetic-track validation gate. However, it is bounded: a
single board (TAB ECHR, English legal text), the direct-identifier axis only, and a single protector
architecture/recipe. We make no "best/strongest/SOTA" claim and no multilingual or cross-domain
generalization claim from it. We also bound the *priority* claim: the "first *unified*" positioning is
scoped by the prior-art scan underlying EuroPriv-Bench, which predates this paper's 3-national-ID,
legal, and TAB external-anchor expansion; we re-verify that scan before broadening any public priority
claim and treat "first *unified*" as provisional until then.

## Limitations

- **Synthetic-track numbers not yet validated (`config_status = dev`).** The national-ID /
  real-skeleton numbers are findings on contamination-controlled but `dev`-status *synthetic* tracks,
  gated pending native-speaker review + inter-annotator agreement on `ro-realskeleton`. SOTA / "best
  protector" claims on these tracks are gated. (The TAB direct-identifier results are on real external
  gold and are exempt from this gate.)
- **Synthetic real-skeleton data.** The real-skeleton tracks are synthetic; the leak-rate measures
  protection on synthetic subjects, not a population re-identification rate against a real reference
  population.
- **TAB result is single-board, single-architecture, single-language.** The direct-identifier-protection
  leadership is measured on one board (TAB, English ECHR legal text only) with a single model
  architecture; breadth across languages/domains is future work. It does *not* establish general
  de-identification SOTA.
- **TAB direct-identifier ≠ deterministic re-identification.** The TAB axis measures *direct-identifier*
  leak (names, case numbers, addresses), a broader and non-deterministic notion than the decode-bearing
  national-ID re-identification used on the synthetic tracks. We report it as re-identification-*risk*
  reduction, not as a measured re-identification rate.
- **Two distinct, both-public protectors.** `kp-cjeu-structure` (the #1 on direct-identifier leak) is
  openly released as `klusai/kp-deid-xlmr-560m-legal`. The openly-released protector evaluated on the
  national-ID tracks (`kp-deid-mdeberta-280m`) is a different (280M) model and ranks 7th on the TAB
  direct-identifier axis (leak 0.674). Both are public; we do not conflate the two.
- **Single seed for the reported point, 3-seed confirmed.** The published TAB number uses seed 0;
  robustness is confirmed across seeds {0, 1, 2} (direct-leak {0.0947, 0.0985, 0.0985}, detection-F1
  {0.340, 0.309, 0.317}). The leak metric is ours (competitors publish only detection-F1), though
  grounded in TAB's own DIRECT/QUASI annotations.
- **Name-in-context channel is preliminary.** Its sample basis is not reconciled with the board's
  n = 1,123 and it predates the validation gate.
- **No QI-combination metric yet.** We do not yet measure k-anonymity-style re-identification from
  *combinations* of quasi-identifiers (the gold lacks binned QI tagging); see future work.
- **Prior-art recency.** The "first *unified*" positioning must be re-verified against the prior-art
  scan before any public claim.

## Future Work

- **QI-combination re-identification metric.** Tag binned quasi-identifier tuples in gold (DOB/age band,
  sex, locality/NUTS, nationality, profession, rare-condition flag) to enable a k-anonymity-violation
  diagnostic — moving from *residual distinctiveness* toward measured population re-identification risk.
  The TAB QUASI channel (3,701 subjects) is the natural bridge.
- **Multilingual / cross-domain breadth on real gold.** Extend the TAB-style external-gold evaluation
  beyond English ECHR legal text to additional languages and domains so the direct-identifier-protection
  result is no longer single-board / single-architecture.
- **Model card and provenance for `klusai/kp-deid-xlmr-560m-legal`.** The TAB-leading checkpoint is
  openly released; the remaining follow-up is the documented model card and training-data provenance.
- **Reconcile and validate the name-in-context channel** against n = 1,123 post-validation.
- **kp-deid v2 multilingual protector** and broadened track coverage.
- **Native-speaker + inter-annotator-agreement validation** to clear the `dev` tracks and unlock citable
  claims on the synthetic national-ID axis.

## Resources

- **Open model (TAB direct-identifier leader):** [`klusai/kp-deid-xlmr-560m-legal`](https://huggingface.co/klusai/kp-deid-xlmr-560m-legal)
- **Open model (national-ID protector):** [`klusai/kp-deid-mdeberta-280m`](https://huggingface.co/klusai/kp-deid-mdeberta-280m)
- **Leaderboard:** [/leaderboard/](/leaderboard/)
- **Benchmark dataset:** [klusai/europriv-bench](https://huggingface.co/datasets/klusai/europriv-bench)
- **Harness and analysis code:** [github.com/klusai/europriv-bench](https://github.com/klusai/europriv-bench)

{% include references.html %}

[^bench]: EuroPriv-Bench — the unified pan-European de-identification benchmark and leaderboard this paper builds on — is described in its own [working-paper landing page]({{ '/papers/europriv-bench/' | relative_url }}); the present paper contributes the dissociation result and the open protector, orthogonal to the benchmark itself.
