---
layout: post
title: "The leaderboard is open — and it now carries three external detectors"
date: 2026-06-03
categories: benchmark results
---

EuroPriv-Bench's submission path is open: a **no-secrets CI** that runs the harness
against your model and adds the row, with provenance baked in. To open it honestly we
ran it ourselves on three independent, third-party detectors that were never tuned to
compete on re-identification risk — **Microsoft Presidio**, **GLiNER2** (Fastino), and
**spaCy** (Explosion). They now sit on the public [leaderboard](/leaderboard/) next to
our own model.

We lead with **re-identification risk**, not detection-F1. A missed national ID isn't one
missed token: a Romanian CNP decodes to a birthday, a sex, and a county at once. So the
question the board asks first is not *how many entities did you label correctly* — it's
*what fraction of subjects had their national ID slip through*.

## What the three external systems are — and aren't

None of these tools was built to model national-ID **structure**. They do ordinary named-entity
recognition, and they do it as designed; they were never tuned for the re-identification metric
the board leads with. That's exactly why they're a useful, honest baseline.

- **spaCy `en_core_web_lg`** (Explosion) — a general-purpose English NER pipeline.
- **GLiNER2 `gliner2-base-v1`** (Fastino) — a zero-shot span tagger you point at PII labels.
- **Presidio** (`presidio-analyzer` + `en_core_web_lg`, Microsoft) — a PII framework that
  pairs NER with **deterministic recognizers** (regexes, checksums) for structured IDs.

## The numbers, on contamination-free Romanian

The `ro-realskeleton-v1` track scores each model on **1,123 distinct CNP subjects** in
held-out, source-separated legal text. We report **CNP leak-rate**: the fraction of subjects
whose national ID slips through.

| Model | Detection-F1 | CNP leak-rate (Wilson 95% CI) | Quasi-IDs leaked |
|---|---|---|---|
| spaCy `en_core_web_lg` | 0.143 | **89.0%** (87.1–90.7%) | 3,000 |
| GLiNER2 `gliner2-base-v1` | 0.642 | **28.6%** (26.0–31.3%) | 963 |
| Microsoft Presidio | 0.472 | **0.0%** (0.0–0.34%) | 0 |
| *(contrast)* kp-deid-mdeberta-280m | 0.741 | 0.0% (0.0–0.34%) | 0 |

Read the spread. **spaCy leaks roughly 89% of CNPs** — its general NER never modelled the
13-digit structure, so the IDs walk straight through (3,000 quasi-identifiers exposed). **GLiNER2
leaks ~29%**, better but still roughly one CNP in three. **Presidio leaks 0%** — not because it
out-detects the others on F1 (it sits mid-table at 0.472), but because its deterministic
recognizers catch the national-ID *string* whatever the surrounding NER does. Structure-aware
coverage, not detection-F1, is what protects the person — and that's the case the board is built
to make.

For contrast, our own [kp-deid-mdeberta-280m](https://huggingface.co/klusai/kp-deid-mdeberta-280m)
also leaks 0%, at a higher F1 (0.741) — but the point of this post is the three external rows, not
the in-house one.

## An honest caveat about status

These real-skeleton tracks are in development (`config_status = dev`): built from authored
template families and **not yet native-speaker- or inter-annotator-agreement-validated**. Treat
the figures above as **measured, contamination-controlled signals** — not validated, citable, or
SOTA claims. The leaderboard marks every such row `dev` for exactly this reason, and validation
comes before we lean on any of it.

We're also not the only people pointing at re-identification risk: concurrent, independent work
such as **RAT-Bench** builds a re-identification-risk leaderboard over synthetic U.S. demographics.
EuroPriv-Bench's angle is the underserved part — European legal text, a GDPR-aligned taxonomy, and
national-ID structure decoded directly. We think it's the **first *unified* pan-European** benchmark
to put detection and re-identification risk on the same gold; we don't claim to be first to care.

## Bring your model

The submission CI is open and runs without secrets — same harness, same provenance, same `dev`/
`citable` discipline for everyone. If you maintain a de-identification model, add your row.

→ See every figure with its provenance on the [leaderboard](/leaderboard/) · open a submission via
[How to submit](/leaderboard/#how-to-submit) · read the [EuroPriv-Bench paper](/papers/europriv-bench/).
