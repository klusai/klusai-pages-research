---
layout: post
title: "October update"
date: 2026-10-11
categories: results models
---

The programme restarted on October 11. The next horizon is a deployment-grade privacy
layer for EU AI gateway traffic. We have useful evidence to build on, and gaps that need
to stay visible. A good legal-text result is a starting point; it does not establish
protection on gateway conversations.

## The legal specialist joins the uniform board

`klusai/kp-deid-xlmr-560m-legal` now appears on the same board as the other detectors,
following [europriv-bench #47](https://github.com/klusai/europriv-bench/pull/47).
Its strongest result is still on TAB, the external English court-text benchmark:

| Model | TAB DIRECT-identifier leak rate | 95% Wilson CI |
|---|---:|---:|
| kp-deid-xlmr-560m-legal | **9.47%** | **6.50–13.61%** |
| Stock Presidio | 50.0% | 44.01–55.99% |

That is the best TAB direct-identifier leak rate on the board. The comparison covers
**127 documents and 264 DIRECT subjects**, using the legal seed0 checkpoint and one
Presidio run. The CIs are disjoint on this held-out config. The
[source ledger](https://github.com/klusai/klusai-models/blob/1f5296c843e32910c3bada14b8c58e3d5383ddf4/docs/north-star-gap.md#2-acceptance-ledger-evidence-gap-closure)
also records three legal training seeds, but the interval above belongs to seed0;
it is not an interval over training seeds.

The same model leaks **100% of CNPs on `ro-synthetic-v1`**, with a **95% Wilson CI of
[99.62–100.00]%**: all **1,017 subjects** across **1,500 documents**, one checkpoint.
The source marks that config `dev` and `in_distribution`; it is not a held-out win.
We report the failure alongside the legal result. This is a **specialist, not a general
privacy model**. The [leaderboard](/leaderboard/) exposes both results and their config status.

There is a metric boundary too. TAB's historical DIRECT score treats an occurrence as
covered when any predicted token is redacted, then requires coverage of every occurrence
of the entity. Part of a name can survive. This is a direct-identifier leakage proxy,
not measured attacker re-identification probability or proof of complete residual removal.

## A first CPU measurement, with its limits

The [CPU study merged in klusai-models #27](https://github.com/klusai/klusai-models/pull/27)
measured the adapters on the same **200 chat-length inputs** on an Apple M3 Ultra:

| Checkpoint | CPU p95 | Unrounded p95 [95% bootstrap CI] |
|---|---:|---:|
| 280m | **148 ms** | 147.97 [142.55–157.88] ms |
| 560m legal | **284 ms** | 284.41 [206.66–347.89] ms |

One seed0 checkpoint per model, one timed pass, CPU fp32, batch size one. The intervals
come from **5,000 input-bootstrap resamples** (RNG seed 120), conditional on this corpus
and pass. Other work was running on the shared host. Tokenization, model inference and
span alignment are included; model loading, transport, queues and redaction operators
are not. These timings do not establish idle-host capacity or end-to-end gateway latency.

## What happens next

The **MoE fine-tune GPU wave**, **gateway-traffic benchmark** and **panel validation** are
in progress. Human-gated programme steps are being replaced by pre-registered LLM-panel
validation. Passing work will be labelled **`panel-validated`**; that describes panel
review and must never be presented as native-speaker validation. Existing development
configs remain development configs until their protocol passes.

The acceptance lines are lower leakage than the pinned Presidio-based deployment
baseline with disjoint CIs, preserved utility, and measured CPU latency under the agreed
load. Stock Presidio on TAB is not that deployment baseline. We have **not yet verified**
those gateway acceptance lines, a general-model claim, or completed panel validation.
The [roadmap](/roadmap/) now separates merged evidence from work in progress and what
still has to pass.
