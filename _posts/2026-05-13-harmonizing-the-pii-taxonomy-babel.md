---
layout: post
title: "Harmonizing the PII taxonomy Babel"
date: 2026-05-13
categories: methodology taxonomy
---

Every PII model speaks a different dialect. OpenAI's privacy-filter has 8 coarse types;
AI4Privacy uses ~98; HIPAA defines 18; the EU's MAPA project has its own legal-and-medical
set; OpenMed expands to 54; tabularisai to 42. If you want to compare these models on the same
data — the whole point of a benchmark — you first have to make them agree on what a "name" or an
"ID number" even is.

So before any scoring, we built one **GDPR-aligned crosswalk**: a single harmonized taxonomy with
a documented mapping from each external scheme's labels onto it. It's deliberately *standardization,
not invention* — the interesting work is reconciliation, not coining new categories.

## The rule that makes it sound

A crosswalk is only trustworthy if **each native label maps to exactly one harmonized type** —
i.e. `native → harmonized` is a *function*. We enforce that at load time, and it immediately
caught real modelling bugs:

- **HIPAA `names`** was claimed by both `PERSON` and `PROVIDER`. But you can't recover "this name
  is a clinician, not a patient" from a flat `names` label — so `PROVIDER` is a refinement that
  doesn't get to claim the source label. `names → PERSON`.
- **MAPA `ORGANIZATION`** was claimed by `COURT`, `FACILITY`, *and* `ORG_PARTY`. Same fix: the
  general owner wins; the refinements are ours, not the source's.
- **`medical_record_numbers`** sat in both the generic account bucket and the clinical `MRN` type.
  The clinical-specific type wins.

Each of these would have silently corrupted comparisons — a model credited for the "wrong" type, or
double-counted. Failing loudly at build time beats discovering it in a results table.

## What we deliberately left out

Schemes like tabularisai's carry GDPR **Article 9 special categories** — ethnicity, religion,
political opinion, sexual orientation. These are real, high-stakes identifiers, but they need
careful design (and they're not in our gold yet), so for now they map to *nothing* rather than
being force-fit. Better an honest gap than a sloppy mapping.

## Why it matters

Without a harmonized taxonomy, "model A scores higher than model B" can just mean "A's label set
happens to line up better with this dataset." The crosswalk — plus scoring every model only on the
types the gold actually annotates — is what lets a leaderboard mean something across models that
were never designed to agree.

→ See it in action on the [leaderboard](/leaderboard/), or read the code on
[GitHub](https://github.com/klusai).
