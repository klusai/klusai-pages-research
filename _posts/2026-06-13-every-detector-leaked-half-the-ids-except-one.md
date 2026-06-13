---
layout: post
title: "Every detector leaked half the IDs on real court text — except one"
date: 2026-06-13
categories: results models
---

A few weeks ago we argued that [a high-F1 detector can still leak every ID it
finds](/results/models/2026/06/02/high-f1-can-still-leak-every-id.html) — but the evidence was on
our own *synthetic* national-ID tracks. The obvious objection: *show it on real data.* So we did.
On **real ECHR court judgments** — the peer-reviewed [Text Anonymization Benchmark](/leaderboard/)
(TAB; Pilán et al. 2022), manually annotated, that no model on our board trained on — the
dissociation holds, and it is starker than on synthetic text.

## The protector test, on real legal gold

TAB marks every identifier as **DIRECT** (directly re-identifying — a name, a case number) or
**QUASI** (needs combination). We score what a de-identifier is *for*: the **DIRECT-identifier
leak rate** — the fraction of distinct direct identifiers left un-redacted in the residual. Lower is
better. Here are the six models on our board, ranked by that leak rate, with their detection-F1
beside it:

| Model | DIRECT-leak (↓ better) | Detection-F1 |
|---|---|---|
| spaCy `en_core_web_lg` | 49.6% | 0.480 |
| Presidio | 50.0% | **0.589** |
| GLiNER (`gliner_multi_pii-v1`) | 59.9% | 0.357 |
| tabularisai/eu-pii-safeguard | 62.5% | 0.073 |
| GLiNER2 (`gliner2-base-v1`) | 65.1% | 0.545 |
| kp-deid-mdeberta-280m (ours) | 67.4% | 0.199 |

Read the F1 column against the leak column. **Presidio tops detection-F1 (0.589) and still leaks
half of all direct identifiers.** GLiNER2 is second on F1 (0.545) and second-*worst* on leakage
(65.1%). The ranking you'd quote from a model card has almost nothing to do with who protects the
person. And note our own shipped 280M is *last* here: it was trained to nail structured national-IDs
on synthetic text — a different job than catching names and case numbers in real legal prose. On
real judgments, **every one of these models leaves roughly half to two-thirds of the direct
identifiers in place.**

## Except one

Train a model on **real legal document structure** instead — real CJEU judgment layouts (a
different court from ECHR, so this is genuine zero-shot, with zero document overlap) with
synthetic, checksum-valid identifiers spliced in — and the picture inverts:

| Model | DIRECT-leak (↓ better) | Detection-F1 |
|---|---|---|
| **kp-deid (CJEU-structure, ours)** | **9.5%** | 0.340 |
| spaCy (next best) | 49.6% | 0.480 |
| Presidio | 50.0% | 0.589 |

**9.5% versus the field's best of 49.6% — it leaves ~5× fewer direct identifiers behind.** And it
does this while sitting *mid-table* on detection-F1 (0.340). The mechanism is the whole point: it
reliably *touches* the identifier tokens — redacting them — even when it disagrees with the gold on
the exact span boundary or the entity type. Strict detection-F1 punishes that disagreement; a person's
privacy does not care about it.

We checked the obvious cheat — is it just redacting everything? No: it marks **9.1%** of tokens as
PII while the gold marks **11.3%** (it under-redacts overall), with only **4.3%** false-positive
redaction. It is not blunt; it is aimed.

## What is, and isn't, a claim here

This one we're willing to lean on, within its scope:

- **It's robust.** Three independent training seeds give DIRECT-leak {9.5%, 9.9%, 9.9%} — a 0.4-point
  spread, nowhere near the gap to the field.
- **It's significant.** A paired bootstrap over the 264 shared direct-identifier subjects puts the
  gap to the runner-up at **Δ = −40 points, 95% CI [−47.7, −32.2]** — comfortably below zero.
- **It's on real, external, peer-reviewed gold** (TAB ECHR), contamination-free.

And the honest boundaries:

- **We do not top detection-F1.** On TAB, synthetic training caps our detection-F1 around 0.34, well
  short of Presidio's 0.589. We're not claiming the detection crown; we're claiming the protection one.
- **One board, one domain, one language** (English legal) so far. Extending the re-id win across
  languages and domains is the next step, not a done deal.
- **Re-identification leak-rate is the metric we lead with** — competitors report detection-F1. But it
  isn't a metric we invented to flatter ourselves: it's computed directly from TAB's own
  externally-annotated DIRECT/QUASI labels.
- The winning checkpoint isn't published yet; the numbers above are reproducible from the benchmark
  and our scorecard, and the model will follow.

The takeaway is the same as last time, now on real court text and with the protector identified:
**if you choose a de-identification model by its detection-F1, you can choose one that leaks half the
identifiers you were trying to protect.** Train for structure, score for leakage, and lead with the
number that measures the harm.

→ See the figures and provenance on the [leaderboard](/leaderboard/) · read the
[EuroPriv-Bench paper](/papers/europriv-bench/).
