---
layout: post
title: "What a neutral leaderboard must control for"
date: 2026-05-23
categories: methodology benchmark
---

When we ran the first cross-lingual baselines, one model led on most European languages. The easy
headline would be "model X wins." The honest footnote is more interesting — and it's the kind of
thing a benchmark exists to surface.

That model was **fine-tuned on AI4Privacy** — the same synthetic corpus our v0 gold is derived
from. It isn't cheating; it's good work. But it means part of its lead is **home-field advantage**:
it has seen data drawn from the same distribution it's being tested on. A leaderboard that prints
the ranking without flagging this is quietly misleading.

## Contamination is the default, not the exception

In privacy NLP, a handful of open corpora (AI4Privacy chief among them) are *both* the common
training data *and* the common evaluation data. So overlap between a model's training set and your
benchmark's source is the normal case, not a rare one. A credible leaderboard has to assume it and
design around it:

- **Provenance on every row** — we record the dataset, config, split, and versions behind each
  score, so a number can always be traced and a contaminated comparison can be spotted.
- **Held-out, source-separated gold** — training and evaluation kept strictly apart, with synthetic
  generation kept separate from the gold.
- **Data nobody has trained on** — the real differentiator. Results on a corpus that *no* baseline
  has seen are the only ones immune to this effect.

That last point is why we're investing in **under-served languages and real-document gold** rather
than just scaling up the AI4Privacy-derived splits. Romanian, for instance, isn't in AI4Privacy at
all — so a Romanian gold set tests every model on genuinely unseen ground.

## The point

"Neutral scorer" isn't a slogan; it's a set of obligations: flag contamination, publish provenance,
and keep building evaluation data that the field hasn't already trained on. We'd rather report a
smaller, honest gap than a big one that won't survive scrutiny.

→ Every score on the [leaderboard](/leaderboard/) carries its provenance.
