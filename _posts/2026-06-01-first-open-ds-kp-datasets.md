---
layout: post
title: "The first open datasets in the EuroPriv-Bench suite"
date: 2026-06-01
categories: datasets release
---

The first open **EuroPriv-Bench datasets** are now on Hugging Face — general-domain
bring-up sets in Romanian, English, and Polish, **50,000 documents each**:

- **[klusai/ds-kp-general-ro-50k](https://huggingface.co/datasets/klusai/ds-kp-general-ro-50k)** — Romanian
- **[klusai/ds-kp-general-en-50k](https://huggingface.co/datasets/klusai/ds-kp-general-en-50k)** — English
- **[klusai/ds-kp-general-pl-50k](https://huggingface.co/datasets/klusai/ds-kp-general-pl-50k)** — Polish

These aren't the first synthetic-PII datasets — the field has plenty. They're the first
datasets in the EuroPriv-Bench suite, and they're built to a quality bar most synthetic-PII
sets miss.

## The bar: valid IDs, correct spans, honest provenance

Synthetic PII is easy to generate and easy to get subtly wrong. We held these sets to four
properties, each one checkable:

- **Checksum-valid locale identifiers.** Where an identifier carries a check digit, the
  emitted value passes it: Romanian CNP, Polish PESEL and NIP, IBAN (mod-97), payment cards
  (Luhn). Invalid or fake-checksum IDs are **not** emitted. A benchmark that quietly ships
  malformed national IDs can't tell you whether a model handles real ones.
- **Offset-correct gold spans, by construction.** Because the PII is injected into the text,
  we know exactly where every entity sits — no post-hoc span alignment to drift. We verify it
  anyway: **100% byte-equality** between each gold span and the substring it points at, and
  **100% BIOES validity** on the tag sequence.
- **Zero train/gold overlap.** Training material and gold are kept strictly apart, so a model
  can't score on rows it has effectively seen.
- **Uniform provenance, per dataset.** Each card records source and license, the generator
  seed, and the taxonomy version — the same fields, the same shape, every time.

## Cleanly-licensed, openly redistributable

The whole set is **CC-BY**. We sourced cleanly-licensed material only, so the datasets are
openly redistributable end to end — no "results you can see but data you can't." That's a
precondition for the kind of reproducibility EuroPriv-Bench is built around: a number you
can't trace to data you can load isn't one you can check.

## How it fits the program

These sets feed the EuroPriv-Bench models and benchmark — the general-domain foundation the
detection and re-identification-risk evaluations run on. Romanian matters here in particular:
it isn't in the common training corpora, so a Romanian gold set tests models on genuinely
unseen ground.

Re-identification risk, not detection-F1, is the metric we lead with — a missed national ID
isn't one missed token, it's a leaked birthday, sex, and county at once. Clean, checksum-valid
IDs are what make that measurement honest: you can only count what a miss exposes if the ID
you're decoding is structurally real.

This is the general-domain bring-up. Legal and clinical synthesis come next.

→ See where these feed in on the [leaderboard](/leaderboard/), or read the
[roadmap](/roadmap/).
