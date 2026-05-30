---
layout: post
title: "Introducing EuroPriv-Bench"
date: 2026-05-30
categories: benchmark release
---

We're releasing **EuroPriv-Bench** — the first *unified* pan-European de-identification
benchmark. It puts privacy NLP for European languages on a single, GDPR-aligned taxonomy
and a privacy-utility metric, rather than the fragmented, English-centric, detection-F1-only
picture that exists today.

## The gap it exposes

Models advertising **96–97% F1** on English PII benchmarks tell you little about how they
behave on, say, Dutch clinical notes under a European privacy taxonomy. When we hold current
baselines to that bar, F1 drops to **0.44–0.61** across `en/fr/es/de/it/nl` — with recall
(the privacy-critical failure mode) the weakest link.

→ **[See the live leaderboard](/leaderboard/)**

## What's in v0

- 6 European language configs from cleanly-licensed open sources, remapped to the unified
  KlusAI privacy taxonomy and fully attributed.
- A reproducible harness with provenance baked into every result (model id, dataset
  config/split, harness &amp; taxonomy version, timestamp).
- Baselines for the current public de-identification models.

## What's next

More baselines (multilingual de-id models, GLiNER, Presidio), larger sample sizes, and the
legal/clinical splits — plus under-served languages including Romanian. Follow along here or
on [GitHub](https://github.com/klusai).

*EuroPriv-Bench is open — see [How to submit](/leaderboard/#how-to-submit).*
