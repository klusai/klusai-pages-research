---
layout: post
title: "Privacy on gateway traffic: first results"
date: 2026-10-11
categories: results models
---

Our first gateway-trained models leave fewer protected identifiers exposed than the two
Presidio baselines on an eight-language chat-style test set. The 280m encoder repeats
that result across three training seeds and removes less harmless text. The mixture of
experts (MoE) also reduces leakage, but still fails the wider evaluation
contract because of over-redaction. **These are development results: independent review
of the synthetic test set is pending, and no gateway-wide contract win is established.**
The gateway-trained models remain private and are **not yet released**.

### What we measured

`gateway-traffic-v1` contains synthetic conversations in Romanian, English, German,
French, Spanish, Italian, Dutch and Polish. Each language's test split has **1,000
conversations and 4,506 identifier subjects**: 4,266 DIRECT and 240 QUASI. An identifier
subject can have repeated mentions across turns; it is not a unique person. The
UNSPECIFIED sensitivity slice has no support and is unavailable, not a measured zero. The eight
language configurations remain **`dev`**. Independent annotation review and semantic
subject/source/scenario-family/translation disjointness checks are unfinished.
Translations can share families across languages, so we report every language separately.
[Evaluation protocol][evaluation]

**Residual leak** measures the fraction of identifier subjects for which at least one
non-whitespace character survives in any protected mention. Covering only part of a name
does not protect it. **Over-redaction** measures the fraction of gold non-PII,
non-whitespace characters removed. Both should be low. Neither measures an attacker's
actual re-identification success, and character retention does not establish downstream
task usefulness. These results use exact character coverage from the recorded operators.
[Metric contract][contract]

We compare two separate baselines: **a Presidio-based deployment baseline**, with its
pinned recognizers, threshold and native replacement policy, and **stock Presidio**, using
the benchmark's English engine and exact local deletion operator. The deployment baseline
has English and Dutch pipelines and falls back to Dutch for the other six languages.
Stock Presidio uses its English engine throughout. These are specific frozen pipelines;
the comparison does not represent every possible Presidio configuration or certify parity
with a live deployment. [Deployment-baseline specification][baseline], [gateway operators][evaluation]

### Residual leakage on every language

All cells below are **percentages [95% Wilson CI]**, with the same **4,506 identifier
subjects in 1,000 conversations per cell**. The gateway-trained mDeBERTa-280m has three
independent training seeds (0, 1, 2); the gateway-trained MoE has **one scored seed (0)**
in the merged evidence used here. Each baseline has one inference run per configuration.
Seeds and languages are never pooled into a larger sample. These intervals describe
each run, not uncertainty across training seeds.

<div class="table-card" role="region" aria-label="Gateway residual leakage by language and model" tabindex="0" markdown="1">

| Language | 280m seed 0 | 280m seed 1 | 280m seed 2 | MoE seed 0 | Deployment baseline | Stock Presidio |
|---|---:|---:|---:|---:|---:|---:|
| RO | 15.80 [14.77, 16.90] | 19.37 [18.25, 20.55] | 18.82 [17.70, 19.99] | 14.96 [13.95, 16.03] | 45.61 [44.16, 47.06] | 61.16 [59.73, 62.58] |
| EN | 16.36 [15.30, 17.46] | 22.59 [21.39, 23.84] | 20.82 [19.66, 22.03] | 13.34 [12.38, 14.36] | 54.19 [52.74, 55.64] | 54.24 [52.78, 55.69] |
| DE | 14.51 [13.52, 15.57] | 18.15 [17.06, 19.31] | 18.97 [17.86, 20.15] | 14.09 [13.11, 15.14] | 44.81 [43.36, 46.26] | 53.33 [51.87, 54.78] |
| FR | 15.49 [14.46, 16.58] | 20.02 [18.88, 21.21] | 18.80 [17.68, 19.96] | 11.45 [10.55, 12.41] | 44.01 [42.56, 45.46] | 59.65 [58.21, 61.08] |
| ES | 13.52 [12.55, 14.54] | 19.02 [17.90, 20.19] | 18.86 [17.75, 20.03] | 13.89 [12.91, 14.93] | 44.83 [43.38, 46.28] | 53.53 [52.07, 54.98] |
| IT | 15.89 [14.85, 16.99] | 16.93 [15.87, 18.06] | 19.06 [17.94, 20.24] | 11.70 [10.79, 12.67] | 44.14 [42.70, 45.60] | 53.11 [51.65, 54.56] |
| NL | 14.80 [13.80, 15.87] | 18.35 [17.25, 19.51] | 18.75 [17.64, 19.92] | 13.20 [12.25, 14.22] | 44.81 [43.36, 46.26] | 56.28 [54.83, 57.72] |
| PL | 15.36 [14.33, 16.44] | 17.09 [16.02, 18.22] | 18.60 [17.49, 19.76] | 9.76 [8.93, 10.67] | 44.50 [43.05, 45.95] | 53.84 [52.38, 55.29] |

</div>

The 280m passes the disjoint-Wilson and paired privacy checks in all **24 seed-language
comparisons against each baseline**. Its paired over-redaction deltas also pass the
earlier, stricter no-increase rule in all those comparisons. This is numerical evidence
on the frozen test split; missing independent review prevents a scoped contract win.
English is its worst language for leakage in every seed, as the table shows.
[Three-seed encoder scorecard][encoder]

The MoE's worst leakage is Romanian, **14.96% [13.95, 16.03]**, and its lowest is Polish,
**9.76% [8.93, 10.67]**. Those are descriptive slices of the full matrix, not substitutes
for the other languages or a replicated architecture comparison. Its single seed passes
the numerical privacy checks against both Presidio baselines, but cannot establish
three-seed robustness. [MoE scorecard][moe], [paired comparisons][moe-json]

### How much harmless text was removed

All cells are **percentages [95% conversation-bootstrap CI]**, resampling the same
**1,000 conversations per language**, including negative examples. The non-PII character
denominators are RO 550,519; EN 576,082; DE 591,633; FR 558,749; ES 567,808; IT 572,586;
NL 558,344; PL 548,750. These are character counts, not independent statistical samples.

<div class="table-card" role="region" aria-label="Gateway over-redaction by language and model" tabindex="0" markdown="1">

| Language | 280m seed 0 | 280m seed 1 | 280m seed 2 | MoE seed 0 | Deployment baseline | Stock Presidio |
|---|---:|---:|---:|---:|---:|---:|
| RO | 6.04 [5.37, 6.69] | 6.29 [5.56, 6.99] | 3.03 [2.76, 3.31] | 4.26 [3.77, 4.78] | 27.03 [26.31, 27.77] | 17.32 [16.78, 17.95] |
| EN | 5.60 [4.99, 6.23] | 4.25 [3.75, 4.72] | 3.08 [2.79, 3.37] | 1.33 [1.16, 1.52] | 7.19 [6.31, 8.07] | 8.25 [7.56, 8.95] |
| DE | 5.74 [5.08, 6.42] | 6.04 [5.35, 6.72] | 3.41 [3.08, 3.75] | 5.13 [4.55, 5.74] | 24.76 [23.76, 25.73] | 28.87 [27.81, 29.91] |
| FR | 5.37 [4.80, 5.95] | 6.58 [5.80, 7.33] | 2.70 [2.45, 2.94] | 1.49 [1.30, 1.70] | 17.50 [16.56, 18.42] | 14.35 [13.69, 15.03] |
| ES | 8.36 [7.40, 9.30] | 7.31 [6.48, 8.11] | 3.13 [2.84, 3.42] | 2.44 [2.15, 2.74] | 25.54 [24.51, 26.47] | 22.20 [20.94, 23.31] |
| IT | 4.85 [4.34, 5.35] | 5.49 [4.87, 6.08] | 3.06 [2.79, 3.34] | 3.28 [2.93, 3.66] | 26.29 [25.27, 27.29] | 20.95 [20.14, 21.69] |
| NL | 4.98 [4.44, 5.51] | 5.78 [5.13, 6.42] | 3.38 [3.06, 3.70] | 3.71 [3.30, 4.15] | 14.98 [13.48, 16.43] | 16.79 [16.07, 17.53] |
| PL | 6.51 [5.76, 7.27] | 6.38 [5.66, 7.07] | 3.35 [3.04, 3.66] | 11.58 [10.38, 12.82] | 35.56 [34.31, 36.72] | 25.37 [24.41, 26.33] |

</div>

The tables use the merged encoder artifact for its three seeds and baseline intervals,
and the merged MoE artifact for seed 0. All bootstrap intervals use **2,000 whole-conversation
resamples**: RNG seed 125 for the encoder report and 100 for the MoE report. Baseline point
estimates agree with the original merged gateway evaluation; bootstrap endpoints can
differ between reports. Comparisons use each report's own paired draws. Wilson intervals
describe subject counts; the paired cluster intervals account for subjects sharing a
conversation. [Encoder estimates and deltas][encoder-json], [MoE estimates and deltas][moe-json],
[original gateway baselines][initial-results]

The encoder and MoE use their recorded full-conversation windowing and local masking
operators. Comparator receipts retain their original runtimes and operators; comparisons
in the wider MoE report also retain different window sizes. This post does not claim a
controlled head-to-head architecture experiment. Full-split gateway entity F1 is unavailable
because some gold spans collide on the whitespace-token grid. **All conversations remain
in the residual-leak and over-redaction scores** above. [Encoder protocol and limits][encoder],
[MoE scoring protocol][moe-protocol]

### The losses belong beside the improvements

**The MoE over-redacts Polish and German.** On Polish gateway conversations it removes
**11.58% [10.38, 12.82]** of harmless characters; on German, **5.13% [4.55, 5.74]**.
Both are below the two Presidio baselines in the table, so the contract loss must be
attributed precisely: other registered comparators do better on utility. Against the
earlier fine-tuned MoE, seed 0's paired utility delta is **+6.65 percentage points
[5.83, 7.50]** on Polish and **+2.40 [1.98, 2.81]** on German (1,000 conversation clusters
per language, one checkpoint on each side). Both intervals lie wholly above the v3
allowance. The merged report records **loss under both the earlier policy and v3**.
[Paired MoE comparisons][moe-json]

**Strict-utility calibration failed.** A separate, earlier MoE experiment selected
confidence thresholds on development data, then froze them before test scoring. Requiring
no worse point utility against every comparator during selection reduced recall. On the
Romanian gateway test, residual leakage was **56.28% [54.83, 57.72]**, **65.40%
[64.00, 66.78]** and **46.78% [45.33, 48.24]** for seeds 0, 1 and 2 respectively
(4,506 subjects, 1,000 conversations per seed; 95% Wilson CIs). It also broke the legacy
Romanian and Polish national-ID zero-leak anchors. This was a recorded loss, not a
successful calibration of the gateway-trained candidate. [Frozen calibration protocol][calibration],
[three-seed calibration results][calibration-results]

**The 280m regresses outside gateway traffic.** On TAB's English legal documents, its
all-identifier residual leak is **66.91% [65.43, 68.36]**, **83.18% [81.98, 84.31]**
and **85.88% [84.76, 86.93]** for seeds 0, 1 and 2, versus stock Presidio's **30.92%
[29.50, 32.38]** (127 documents, 3,965 identifier subjects per model; 95% Wilson CIs).
This is the all-identifier endpoint, distinct from historical TAB DIRECT-only scores.
The scorecard also records seed-1 privacy regressions against the earlier encoder on
the six general-text configurations, a Polish all-PII regression for seed 2, and an English
utility regression against stock Presidio for seed 2. General-text contamination and
the capped inference used on these non-gateway sets limit interpretation, but the
regressions remain in the report. [Encoder results and limitations][encoder]

### Why contract v3 changed prospectively

The earlier utility gate required the upper bound of the paired 95% CI for
candidate-minus-comparator over-redaction to be at most zero. That can favor a detector
that removes almost nothing, including too little private information. The failed
development-only calibration made that tradeoff concrete.

**Contract v3 allows at most +1.0 percentage point of additional harmless-character
removal at the upper bound of that paired interval**, separately for every configuration,
comparator and candidate seed. This is an absolute margin of 0.01, not a relative 1%
increase. It is a declared engineering tolerance, not evidence that users' tasks tolerate
that loss. Disjoint privacy CIs, negative paired leakage deltas, the Romanian/Polish
zero-leak anchors, at least three training seeds, reviewed and disjoint gold, and load
requirements remain unchanged. [Prospective registration and rationale][contract]

The registration records the decision on October 11 **before the gateway-trained MoE
and encoder evaluations**. It applies only to new candidate evaluations after the
introducing commit; historical predictions and verdicts cannot be retrospectively
promoted. The MoE scoring protocol pins that registration. The merged encoder scorecard
still cites the older contract and passes its stricter zero-margin numerical utility
check; we retain that provenance rather than relabelling its run as v3. The earlier
calibration remains a loss, and the gateway-trained MoE still fails v3.
[Contract registration][contract], [MoE protocol][moe-protocol], [encoder scorecard][encoder]

Independent gold review, semantic disjointness, downstream task utility, deployed operator
equivalence and end-to-end CPU latency/load acceptance remain unverified. The next work
is to resolve those gaps, reduce the MoE's over-redaction, and preserve the encoder's
quality outside gateway traffic. The [roadmap](/roadmap/) tracks that work. The models
remain private while these results and their limits are available for scrutiny.

[evaluation]: https://github.com/klusai/europriv-bench/blob/cc7be79c0c033ceed38c44527a2aed0103f440a3/docs/gateway-evaluation.md
[baseline]: https://github.com/klusai/europriv-bench/blob/14cfc44d5218e2f96081fc7ea8db5b07eb2880b3/docs/shield-baseline.md
[initial-results]: https://github.com/klusai/europriv-bench/blob/cc7be79c0c033ceed38c44527a2aed0103f440a3/docs/gateway-evaluation-results.md
[contract]: https://github.com/klusai/europriv-bench/blob/68eea8bd4ac64cbe4cf83532db48c365c06ff102/docs/gateway-contract.md
[encoder]: https://github.com/klusai/klusai-models/blob/cfc8da67adcfcc95b13e7b568d47b3c340a3c864/docs/res127-encoder-scorecard.md
[encoder-json]: https://github.com/klusai/klusai-models/blob/cfc8da67adcfcc95b13e7b568d47b3c340a3c864/docs/res127-encoder-scorecard.json
[moe]: https://github.com/klusai/europriv-bench/blob/4f5203f87bd5930ee41ce91ad3a6d065b1ece8d0/docs/gateway-moe-results.md
[moe-json]: https://github.com/klusai/europriv-bench/blob/4f5203f87bd5930ee41ce91ad3a6d065b1ece8d0/analysis/gateway-moe-comparison.json
[moe-protocol]: https://github.com/klusai/europriv-bench/blob/4f5203f87bd5930ee41ce91ad3a6d065b1ece8d0/docs/gateway-moe-scoring.md
[calibration]: https://github.com/klusai/europriv-bench/blob/2ce13cf0c698a7a1ff0b344052e008e671dc13f5/docs/res100-calibration.md
[calibration-results]: https://github.com/klusai/europriv-bench/blob/2ce13cf0c698a7a1ff0b344052e008e671dc13f5/docs/res100-calibrated-results.md
