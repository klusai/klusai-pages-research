---
layout: post
title: "The GPU isn't always the answer"
date: 2026-05-27
categories: engineering notes
---

We benchmark a lot of models, so harness throughput matters. The intuition — "we have a 60-core
M3 Ultra GPU, use it" — turned out to be exactly wrong for this workload, in an instructive way.

The model under test is `openai/privacy-filter`: a sparse Mixture-of-Experts with only **50M
active parameters**, doing short-sequence token classification. We measured inference per example,
several ways:

| setup | s/example |
|---|---|
| MPS (Apple GPU, PyTorch), single | 0.81 |
| MLX (Apple GPU), batched | 0.085 |
| CPU, batch=32, **28 threads** | 0.083 |
| CPU, batch=32, **4 threads** | **0.041** |

Two surprises:

**1. The GPU lost.** Both the PyTorch-MPS and the MLX paths were *slower* than CPU. With so few
active parameters and short sequences, there isn't enough work per item to amortize the overhead of
getting data onto the GPU — and the MoE's routing ops fall off the Metal fast path and bounce back
to the CPU anyway. GPUs win on *big* compute (large models, long sequences, training); they don't
on a tiny MoE doing short spans.

**2. More threads were slower.** PyTorch's default (28 BLAS threads here) ran at **half the speed**
of 4 threads — the ops are small enough that thread-coordination overhead dominates.

## What actually used the machine

The real lever was **parallelism at the job level**: run many small, thread-capped jobs at once.
Seven worker processes × 4 threads saturates the 28 cores, each job at its own fastest point. A
full sweep (multiple models × multiple language configs) that crawled before now finishes in a
couple of minutes — a ~7× wall-clock win, and identical (deterministic) numbers.

## The lesson

Profile before you reach for the accelerator. "Use the GPU" and "use all the cores" are heuristics,
not laws — and for small models on short inputs, both can cost you. The GPU still earns its keep
here: just for the *other* job, training our own models, where the compute is actually large.
