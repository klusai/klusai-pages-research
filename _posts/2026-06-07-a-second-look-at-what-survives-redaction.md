---
layout: post
title: "A second look at what survives redaction: a quasi-identifier diagnostic"
date: 2026-06-07
categories: benchmark methodology
---

So far we've measured leakage one way: did a specific, structured identifier — a national ID
that decodes to a birthday, a sex, and a county — slip through? That's the
re-identification-risk channel, and it's deliberately narrow: we only call something
*re-identification* when an identifier's structure earns the word.

This week we added a **second, independent diagnostic** that looks at a different kind of
residue: the **quasi-identifiers** left behind *after* redaction — combinations of attributes
like a date, a place, and a role that, taken together, can make a record stand out even when
every named entity is gone.

## A k-anonymity-violation diagnostic, within the corpus

The new diagnostic is a **within-corpus k-anonymity-violation** measure over the residual
quasi-identifiers in redacted text. It flags records whose surviving attribute combination is
rare enough that the record is **distinctive within the sample** — a signal that redaction
removed the obvious identifiers but not the quieter, combinable ones.

It's worth being precise about what this is, because the words matter here:

- It measures **sample distinctiveness** — how unusual a record is *within this corpus*.
- It is **not** population re-identification, and we don't report it as such. Saying a record
  is rare in a dataset of a few hundred documents says nothing, on its own, about whether a
  real person could be picked out of a national population.
- We reserve the term **re-identification** for the deterministic national-ID channel. For
  this diagnostic, the honest word is **residual distinctiveness**.

## Why add a second channel at all

The national-ID metric catches the sharpest case: a structured string that, alone, discloses
who someone is. But good redaction can clear every national ID and still leave a record that's
distinctive on its quasi-identifiers. A second, independent channel lets us see that residue
instead of assuming the structured-ID metric covers it. Two channels that measure different
failure modes are harder to fool than one.

This is groundwork. The diagnostic is **`dev`**, intended as an internal sensitivity signal —
**not** a validated, citable, or population-level re-identification claim. A separate strand
of work (a population-uniqueness estimator with a reference-population module) is what would
eventually let us reason about real-world uniqueness, and that is pending a census-calibrated
generator — explicitly not something we're claiming today.

→ See where this fits on the [roadmap](/roadmap/).
