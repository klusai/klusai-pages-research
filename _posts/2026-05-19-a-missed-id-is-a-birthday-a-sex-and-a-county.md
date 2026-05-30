---
layout: post
title: "A missed ID number is a birthday, a sex, and a county"
date: 2026-05-19
categories: methodology metrics
---

Most PII benchmarks report one number: detection F1. It treats every missed entity as one missed
token. But for privacy, **not all misses are equal** — and detection-F1 hides exactly the misses
that matter most.

Take the Romanian **CNP** (Cod Numeric Personal), the national ID number. It isn't an opaque
string: its 13 digits *encode* the holder's data. A single un-redacted CNP deterministically
discloses:

- **date of birth** (century + year + month + day),
- **sex** (the leading digit's parity), and
- **county** of registration.

So a model that misses one CNP hasn't dropped "one token" — it has leaked **three quasi-identifiers
at once**, the exact combination that enables re-identification. A model that catches 99% of generic
PII but routinely misses national IDs can look great on F1 and still be a privacy liability.

## Measuring the thing that matters

That's why our headline metric isn't detection-F1 — it's **re-identification risk**. For national
IDs we decode the structure directly and count what a miss actually exposes. We also report a
**recall-weighted** score alongside F1, because in de-identification a false negative (PII left in)
is far costlier than a false positive (something harmless redacted).

This also reframes what "good" means. A model that flags a 13-digit string as the *wrong* type but
still redacts it hasn't leaked anything — redaction cares about coverage, not labels. Detection-F1
penalizes the mislabel; the leakage metric correctly says "no harm done." Different questions,
different metrics — and privacy needs the second one.

## Why national IDs, and why Europe

National-ID formats are where English-centric models fall down hardest: a CNP, a Spanish DNI, a
Polish PESEL each have their own structure and check digits that a model trained mostly on US/UK
data has never seen. Getting these right — and *measuring the leakage when you don't* — is central
to a European privacy benchmark, not a footnote.

We're building the gold sets to test this properly across languages and domains. The metric is
ready; the harder, more honest part — realistic documents — is what we're working on next.
