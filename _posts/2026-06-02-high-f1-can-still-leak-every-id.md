---
layout: post
title: "A high-F1 detector can still leak every ID it finds"
date: 2026-06-02
categories: results models
---

Our first de-identification model, **[klusai/kp-deid-mdeberta-280m](https://huggingface.co/klusai/kp-deid-mdeberta-280m)**,
just landed on the public [leaderboard](/leaderboard/) as the **best protector** on the
contamination-free Romanian **real-skeleton** track. It earns that title not by topping
detection-F1 — it doesn't — but on the metric we actually lead with: **re-identification
risk**. And in earning it, it surfaces the program's headline finding.

**Detection-F1 and re-identification protection come apart.** A model can score high on
entity-F1 and still leak the identifiers that re-identify a person; a model trained *for
protection* can sit mid-table on F1 and leak essentially nothing. The two numbers measure
different things, and on national IDs they disagree hard.

## The dissociation, on contamination-free Romanian

The `ro-realskeleton-v1` track scores each model on **1,123 distinct CNP subjects** —
Romanian national IDs in held-out, source-separated legal text that no baseline has trained
on. We report **CNP leak-rate**: the fraction of subjects whose national ID slips through.
A single missed CNP is not one missed token — it decodes to a birthday, a sex, and a county
at once, so we count what a miss exposes (the "quasi-identifiers leaked" column below).

| Model | Detection-F1 | CNP leak-rate (Wilson 95% CI) | Quasi-IDs leaked |
|---|---|---|---|
| **kp-deid-mdeberta-280m** | 0.741 | **0.0%** (0.0–0.34%) | **0** |
| GLiNER (gliner_multi_pii-v1) | **0.853** | 30.2% (27.6–32.9%) | 1,017 |
| tabularisai/eu-pii-safeguard | 0.747 | 35.4% (32.6–38.2%) | 1,191 |
| OpenMed/privacy-filter-multilingual | 0.576 | 26.4% (23.9–29.0%) | 888 |
| openai/privacy-filter | 0.363 | 1.4% (0.9–2.3%) | 48 |

Read the top two rows together. **GLiNER has the highest detection-F1 on the board (0.853)
and the second-worst leak-rate (30.2%)** — it is type-accurate on the entities it catches,
yet roughly one CNP in three walks straight through. kp-deid scores *lower* on F1 (0.741) and
leaks **0% of 1,123 CNPs**. tabularisai tells the same story from the other direction: a
strong-looking 0.747 F1, the worst leak-rate on the board (35.4%). F1 simply does not predict
who protects the person.

Why the gap? F1 rewards getting the label right; protection only needs *coverage* — redact the
13-digit string and no harm is done, whatever you call it. A detector tuned to label precisely
can still drop the spans that matter most, and detection-F1 will not flag it. (`openai/privacy-filter`
is the instructive corner case: weak F1, but it over-redacts, so its leak-rate is low too.)

## A preliminary cross-language signal: Polish PESEL, zero-shot

The same dissociation shows up in a second language and a second identifier — **zero-shot**.
kp-deid was trained on Romanian and **never saw Polish**, yet on the `pl-realskeleton-v1`
track (**1,096 distinct PESEL subjects**, the Polish national ID, which carries its own
structure and check digit) it still leaks nothing:

| Model | Detection-F1 | PESEL leak-rate (Wilson 95% CI) |
|---|---|---|
| **kp-deid-mdeberta-280m** (zero-shot) | 0.763 | **0.0%** (0.0–0.35%) |
| GLiNER (gliner_multi_pii-v1) | 0.825 | 57.8% (54.9–60.7%) |
| tabularisai/eu-pii-safeguard | 0.738 | 30.7% (28.0–33.5%) |
| OpenMed/privacy-filter-multilingual | 0.662 | 3.7% (2.8–5.0%) |
| openai/privacy-filter | 0.406 | 0.1% (0.0–0.5%) |

GLiNER again leads on the structural F1 you'd quote in a model card (0.825) and **leaks more
than half of all PESELs** (57.8%). A model that was never shown Polish protects the Polish ID;
a higher-F1 multilingual detector leaks the majority of them.

**An honest caveat, because it matters.** This Polish track is early. It is still in development
(`dev`), built from a single authored template family, and **not yet native-speaker- or IAA-validated**.
Treat it as a strong early signal that the dissociation generalizes across languages and
identifier schemes — **not** as a validated, citable headline. Full validation comes before we
lean on it.

## What is and isn't a claim here

The Romanian real-skeleton track is itself still in development (`dev`), pending native-speaker and
inter-annotator-agreement validation. So the result above is a **measured, contamination-controlled
delta** on held-out data — not yet a peer-reviewed, citable claim. We'd rather say that plainly
than round it up.

We're also not the only people pointing at re-identification risk: concurrent, independent work
like **RAT-Bench** builds a re-identification-risk leaderboard over synthetic text on U.S.
demographics. EuroPriv-Bench's angle is the part that's underserved — European legal text, a
GDPR-aligned taxonomy, and national-ID structure decoded directly. We think it's the **first
*unified* pan-European** benchmark to put detection and re-identification risk side by side on
the same gold; we don't think it's the first to care about the problem.

The takeaway is narrow and, we think, durable: **if you pick a de-identification model on
detection-F1, you can pick one that leaks the identifiers you were trying to protect.** Lead
with the leak-rate.

→ See every figure above, with its provenance, on the [leaderboard](/leaderboard/) · read the
[EuroPriv-Bench paper](/papers/europriv-bench/) · get the model:
[klusai/kp-deid-mdeberta-280m](https://huggingface.co/klusai/kp-deid-mdeberta-280m).
