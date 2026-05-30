---
layout: home
title: "Research"
list_title: "/latest posts"
---

**KlusAI Research** is the open home of our privacy-focused models program:
benchmarks, datasets, models, and papers for **privacy-preserving NLP across
European languages** — PII/PHI detection, anonymization, and re-identification-risk
evaluation in the legal and clinical domains.

This is the research hub. For the company and product, see
[klusai.com](https://klusai.com).

## EuroPriv-Bench — our flagship

**[EuroPriv-Bench](/leaderboard/)** is the first *unified* pan-European
de-identification benchmark. Unlike prior work that reports only detection-F1 on
English, EuroPriv-Bench measures **privacy-utility / re-identification risk** on a
single GDPR-aligned taxonomy across 20 European languages, spanning legal and
clinical text.

The headline finding: models advertising **96–97% F1** on English PII drop to
**0.44–0.61 F1** once you hold them to a unified European taxonomy across
languages.

<p><a class="btn" href="{{ '/leaderboard/' | relative_url }}">See the live leaderboard →</a></p>

## Artifacts

| | |
|---|---|
| 🤗 **Benchmark** | [`klusai/europriv-bench`](https://huggingface.co/datasets/klusai/europriv-bench) on Hugging Face |
| 💻 **Code** | [github.com/klusai](https://github.com/klusai) — benchmark harness, datasets, models |
| 📄 **Papers** | arXiv preprints (linked from each post as they ship) |

## What we publish here

- **Leaderboards** — versioned, provenance-tracked results you can cite.
- **Release notes & methodology** — the technical story behind each artifact.
- **Paper companions** — reproducible numbers tracing back to a commit.
