---
layout: post
title: "Making the benchmark honest: a harder external eval, and our first real data"
date: 2026-06-07
categories: benchmark datasets
---

Two changes landed this week that make EuroPriv-Bench harder to game — including by us.
We added an **external, third-party detection eval** that pulls our own synthetic scores
apart, and we wired in the **first real-data gold config** in the suite. Both make our
numbers look worse, on purpose. A benchmark you can't fail isn't measuring anything.

## A synthetic eval that everyone aces isn't an eval

Our own synthetic detection sets were doing their job for span discipline — checksum-valid
IDs, offset-correct gold — but they had a quieter problem: on the cleanest configs, the
detection scores had **saturated**. A control run sat at **entity-F1 1.000**. When the
strongest baselines all crowd the ceiling, the metric has stopped discriminating between
them, and any ranking you read off it is noise.

So we adopted the **Ai4Privacy** open-core (`openpii-1m`, CC-BY-4.0) as an **external,
independent** detection eval — text we didn't author, scored through the same harness and
the same GDPR-aligned taxonomy crosswalk. It
de-saturates immediately: across the same models, entity-F1 now spreads over a **0.41–0.67
band** instead of pinning at 1.000. That spread is the point — the eval now separates models
that the synthetic control could not.

One licensing note, because it's the kind of thing that's easy to get wrong: Ai4Privacy
ships a larger **500k tier that is Llama-licensed**, which fails our cleanly-licensed-only
gate. We caught it and **excluded that tier**; only the CC-BY-4.0 open-core feeds the eval.
A benchmark that quietly ingests non-redistributable data can't claim to be open.

## Real legal data is harder than our synthetic — and we'd rather show it

The bigger step: we integrated **TAB** (the Text Anonymization Benchmark, English legal text
derived from European Court of Human Rights judgments, MIT-licensed) as the **first real-data
gold config** in the suite. Everything in EuroPriv-Bench until now was synthetic — clean by
construction. TAB is human-written, human-annotated court text: **127 documents**, projected
into our taxonomy with **zero misaligned spans** after alignment. It carries a new status,
`config_status = real-external-gold`, to mark it as exactly that: real, externally-sourced,
not one of our own synthetic skeletons.

The honest finding is that real legal English is **hard**, and it humbles our own model:

| Model | TAB entity-F1 (real legal EN) |
|---|---|
| Microsoft Presidio | **0.589** |
| klusai/kp-deid-mdeberta-280m | 0.199 |

Read that the right way. The strongest system on this real-legal config is **Presidio, at
0.589** — far below the near-ceiling numbers everyone posts on synthetic data. And **our own
`kp-deid` sits at 0.199**: it was trained on Romanian, and on real English legal text it is
**out of distribution** and struggles. We are not the leader here, and the table says so.
That's the value of a real-data config — it shows where the synthetic-trained model doesn't
transfer, instead of flattering it.

## Status, said plainly

Both additions are **`config_status = dev`** for the Ai4Privacy detection eval and
**`real-external-gold`** for TAB — measured, contamination-controlled signals, **not**
validated, citable, or SOTA claims. The TAB-derived gold config is **private** for now
(licensing/redistribution review pending), so there's no public config to load yet — the
numbers above are reproducible internally against the committed harness, and we'll say so
on every row.

None of this changes the metric we lead with. Detection-F1 is a detection number; the
re-identification-risk metric still leads on the national-ID tracks, where a missed ID
decodes to a birthday, a sex, and a county. What this week did was make the *detection* side
honest: an external eval that separates models, and a real-data config that refuses to let
our own model off easy.

→ See the public configs and their provenance on the [leaderboard](/leaderboard/), or read
the [roadmap](/roadmap/) for where the real-data and external-eval work sits.
