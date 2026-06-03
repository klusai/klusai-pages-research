---
layout: page
title: "Leaderboard"
permalink: /leaderboard/
---

<style>
/* ---- KLU-117 leaderboard UX (scoped, no Sass / no JS build) ---- */
/* Plain-language lead */
.lb-headline { font-size: 1.18rem; font-weight: 600; line-height: 1.45; margin: 0.6rem 0 0.4rem; }
.lb-tldr { color: var(--text-secondary); max-width: 46rem; margin: 0 0 1rem; }

/* Hero stat band */
.lb-statband {
  display: flex; flex-wrap: wrap; gap: 0.5rem; margin: 0.5rem 0 1.3rem;
}
.lb-stat {
  background: var(--surface-alt); border: 1px solid var(--border); border-radius: 999px;
  padding: 0.3rem 0.85rem; font-size: 0.85rem; color: var(--text-secondary); white-space: nowrap;
}
.lb-stat b { color: var(--text); font-weight: 600; }

/* Pareto figure — white card, theme-safe (mirrors .arxiv-figure-frame from _layouts/paper.html).
   Breaks out of the narrow (760px) article column into a full-width hero, centered on the viewport. */
figure.lb-figure {
  width: min(1080px, calc(100vw - 3rem));
  position: relative; left: 50%; transform: translateX(-50%);
  margin: 1.4rem 0 1.8rem; text-align: center;
}
figure.lb-figure .lb-figure-frame {
  background: #fff; border: 1px solid var(--border); border-radius: 12px; padding: 0.9rem;
  box-shadow: var(--shadow);
}
figure.lb-figure img { display: block; width: 100%; height: auto; }
figure.lb-figure figcaption {
  font-family: Georgia, serif; font-size: 0.82rem; color: var(--text-secondary);
  text-align: center; margin: 0.6rem auto 0; max-width: 92%;
}

/* Leak-rate bar (CSS only; numeric value kept inline & first for sortability) */
td.leakcell { min-width: 9.5rem; }
.leakbar-wrap { display: flex; align-items: center; gap: 0.5rem; justify-content: flex-end; }
.leakbar-num { font-variant-numeric: tabular-nums; min-width: 3.1rem; text-align: right; }
.leakbar-track {
  flex: 1 1 auto; height: 0.62rem; min-width: 4rem; border-radius: 999px;
  background: var(--surface-alt); overflow: hidden;
}
.leakbar-fill { display: block; height: 100%; border-radius: 999px; }
.leakbar-fill.lvl-none { background: #1f9d6b; }      /* ~0% — protects */
.leakbar-fill.lvl-low  { background: #4caf76; }
.leakbar-fill.lvl-mid  { background: #d9a300; }      /* amber */
.leakbar-fill.lvl-high { background: #d2563b; }      /* red — leaks */

/* De-emphasise in_distribution rows in the detection table (memorisation / train-eval overlap) */
table.lb tr.row-indist td { color: var(--text-secondary); }
table.lb tr.row-indist td code { opacity: 0.85; }
.indist-note { display: inline-block; font-size: 0.7rem; color: var(--text-secondary); font-style: italic; margin-left: 0.35rem; }

/* "How to read this" / show-all expanders */
details.lb-details { margin: 0.8rem 0 1.2rem; border: 1px solid var(--border); border-radius: 12px; background: var(--surface); padding: 0.2rem 1rem; }
details.lb-details > summary { cursor: pointer; font-weight: 600; padding: 0.6rem 0; }
details.lb-details[open] > summary { border-bottom: 1px solid var(--border); margin-bottom: 0.6rem; }
details.lb-details p { font-size: 0.9rem; }

/* ---- KLU-120: full-width, height-bounded data tables (single-line rows + sticky header) ----
   The 8–10 column tables wrapped hard inside the 760px article column, tripling row height and
   pushing right-hand columns off-screen. Break them out to full width (breakout on an OUTER wrapper
   so the transform doesn't interfere with the inner scroll container's sticky header), force
   single-line rows, and bound height so the page stays compact and each table is viewport-framable. */
.lb-breakout {
  width: min(1100px, calc(100vw - 3rem));
  position: relative; left: 50%; transform: translateX(-50%);
  margin: 1.1rem 0;
}
.lb-breakout .table-card { margin: 0; }
.table-card.lb-tight table.lb td { white-space: nowrap; }
.table-card.lb-tight table.lb th,
.table-card.lb-tight table.lb td { padding-top: 0.42rem; padding-bottom: 0.42rem; }
.table-card.lb-scroll { max-height: 70vh; overflow: auto; }
.table-card.lb-scroll table.lb thead th {
  position: sticky; top: 0; z-index: 2; background: var(--surface);
}
</style>

<p class="eyebrow">Flagship benchmark</p>

# EuroPriv-Bench Leaderboard

<p class="lb-headline">Detection ≠ protection: on realistic Romanian documents the highest-F1 detector still leaks ~30% of national IDs (CNPs), while the model that protects best leaks 0%.</p>

<p class="lb-tldr">
For privacy, the number that matters is <strong>re-identification leakage</strong> — how many decode-bearing
national IDs a model leaves un-redacted — not detection F1. A leaked ID silently discloses identifying
attributes (a Romanian CNP encodes date of birth, sex and county), so the best detector is <em>not</em>
necessarily the best protector. Everything below is <span class="lb-badge status-dev">dev</span> (pending
native-speaker / inter-annotator-agreement sign-off) — read it as a strong early signal, not a validated,
citable result.
</p>

<div class="lb-statband">
  <span class="lb-stat"><b>8</b> models</span>
  <span class="lb-stat"><b>3</b> decode-bearing national IDs (CNP · PESEL · Codice Fiscale)</span>
  <span class="lb-stat"><b>3</b> leakage tracks: RO · PL · IT</span>
  <span class="lb-stat">detection across <b>8</b> languages</span>
  <span class="lb-stat">re-id leak rate <b>0%–96%</b></span>
</div>

<figure class="lb-figure">
  <div class="lb-figure-frame">
    <picture>
      <source srcset="{{ '/assets/papers/pareto_dissociation_ro_realskeleton.svg' | relative_url }}" type="image/svg+xml" />
      <img src="{{ '/assets/papers/pareto_dissociation_ro_realskeleton.png' | relative_url }}"
           alt="Scatter plot of detection F1 (x-axis) against CNP re-identification leak rate (y-axis) for eight models on ro-realskeleton-v1; higher F1 does not imply lower leakage.">
    </picture>
  </div>
  <figcaption>
    Detection–protection dissociation: detection F1 (x) vs CNP re-identification leak rate (y) on
    <code>ro-realskeleton-v1</code>, <code>dev</code> split, n=1123 CNPs. Higher F1 does not imply lower leakage.
  </figcaption>
</figure>

## Re-identification leakage — the metric that matters

Detection F1 is not privacy. EuroPriv-Bench measures **re-identification leakage**: a missed
(un-redacted) national ID deterministically discloses identifying attributes — on the Romanian
configs a leaked **CNP** discloses **date of birth + sex + county**, on the Polish track a leaked
**PESEL** discloses **date of birth + sex**, and on the Italian track a leaked **Codice Fiscale**
discloses **date of birth + sex + place of birth**. The bar shows the leak rate (long/red = leaks,
tiny/green ≈ protects); the table also counts national IDs left un-redacted and the quasi-identifiers
thereby leaked (lower is better).

<div class="lb-breakout">
<div class="table-card lb-tight">
<table id="leakage" class="lb">
  <thead>
    <tr>
      <th data-type="text">Model</th>
      <th data-type="text">Track</th>
      <th data-type="text">Contamination</th>
      <th data-type="text">Validation</th>
      <th data-type="num">Leak rate</th>
      <th data-type="num">95% CI</th>
      <th data-type="num">IDs missed</th>
      <th data-type="num">Quasi-identifiers leaked</th>
    </tr>
  </thead>
  <tbody>
  {% for kv in site.data.leaderboard.entries %}
    {% for row in kv[1] %}
    {% assign leak = row.scores.cnp_leakage | default: row.scores.national_id_leakage %}
    {% if leak %}
    {% if row.scores.cnp_leakage %}{% assign ids_missed = leak.cnp_missed %}{% else %}{% assign ids_missed = leak.decode_bearing_missed %}{% endif %}
    {% assign leak_pct = leak.leak_rate | times: 100 %}
    <tr>
      <td><code>{{ row.model_id }}</code></td>
      <td><code>{{ row.dataset.config }}</code></td>
      <td>
        {% if row.contamination == "in_distribution" %}<span class="lb-badge contam-in" title="Model was trained on this config's source data">in-distribution</span>
        {% elsif row.contamination == "clean_held_out" %}<span class="lb-badge contam-clean" title="No baseline was trained on this data — a fair held-out test">clean held-out</span>
        {% else %}<span class="lb-badge contam-unknown" title="Train/eval overlap not established">unknown</span>{% endif %}
      </td>
      <td>
        {% if row.config_status == "citable-validated" %}<span class="lb-badge status-citable" title="Passed native-speaker / inter-annotator-agreement sign-off — citable as a validated result">citable</span>
        {% else %}<span class="lb-badge status-dev" title="Development config — not yet validated, must not be cited as a validated benchmark result">dev</span>{% endif %}
      </td>
      <td class="leakcell">
        <span class="leakbar-wrap">
          <span class="leakbar-num">{{ leak_pct | round: 1 }}%</span>
          <span class="leakbar-track">
            {% if leak_pct >= 25 %}{% assign lvl = "lvl-high" %}{% elsif leak_pct >= 10 %}{% assign lvl = "lvl-mid" %}{% elsif leak_pct >= 1 %}{% assign lvl = "lvl-low" %}{% else %}{% assign lvl = "lvl-none" %}{% endif %}
            <span class="leakbar-fill {{ lvl }}" style="width: {{ leak_pct | round: 1 }}%;"></span>
          </span>
        </span>
      </td>
      <td>{{ leak.leak_rate_ci_low | times: 100 | round: 1 }}–{{ leak.leak_rate_ci_high | times: 100 | round: 1 }}</td>
      <td>{{ ids_missed | round: 0 }}</td>
      <td>{{ leak.leaked_quasi_identifiers | round: 0 }}</td>
    </tr>
    {% endif %}
    {% endfor %}
  {% endfor %}
  </tbody>
</table>
</div>
</div>

<p class="lb-meta">
  The dissociation is the point: on realistic-structure Romanian documents
  (<code>ro-realskeleton-v1</code>) the model with the <em>best</em> detection F1 leaks ~30% of
  CNPs, while a purpose-built protector redacts every one. The same pattern repeats zero-shot on the
  Polish PESEL and Italian Codice Fiscale tracks. The mechanism is general — aggregate detection F1
  can stay high while a model misses the rare, high-stakes tokens that carry the re-identification —
  and <strong>decode-bearing national identifiers (RO CNP, PL PESEL, IT codice fiscale)</strong> are
  the clearest, provable case of it, which is why this benchmark leads with leakage. Extending the
  measure to quasi-identifier-combination re-identification is in progress, so the broad reading is a
  hypothesis under test rather than a settled law. All tracks are still
  <span class="lb-badge status-dev">dev</span> (pending native-speaker / inter-annotator-agreement
  validation) — read their leak rates as strong early signals, not yet validated headline results.
</p>

## Detection scores — by model and language

Entity-level scores on the [`klusai/europriv-bench`](https://huggingface.co/datasets/klusai/europriv-bench)
test split, by model and language. Higher F1 is better; the table defaults to **best-first**. Click a
column header to re-sort. Rows where the model was trained on the config's own source data are greyed
(<span class="lb-badge contam-in">in-distribution</span>) — their scores are inflated by train/eval
overlap and are not a fair test.

<details class="lb-details">
  <summary>How to read this — contamination &amp; validation</summary>
  <p>Each row carries two governance markers. <strong>Contamination</strong> flags whether the model was
  trained on that config's source data — an <span class="lb-badge contam-in">in-distribution</span> score
  is inflated by train/eval overlap (e.g. a perfect 100/100/100 is a memorisation artefact, not a win),
  while a <span class="lb-badge contam-clean">clean held-out</span> score is a fair test.
  <strong>Validation</strong> shows whether a config has passed native-speaker / inter-annotator-agreement
  (IAA) sign-off: only a <span class="lb-badge status-citable">citable</span> row may be cited as a
  validated result. Everything is currently <span class="lb-badge status-dev">dev</span> — not yet citable.</p>
  <p>Each row reports entity-level precision / recall / F1 (×100) under the unified KlusAI privacy
  taxonomy. Results carry full provenance (model id, dataset config/split, harness &amp; taxonomy version,
  timestamp) in the <a href="https://github.com/klusai">source repository</a>.</p>
</details>

{% assign bench_v = "" %}{% for kv in site.data.leaderboard.entries %}{% if bench_v == "" %}{% assign bench_v = kv[1][0].europriv_bench_version %}{% assign tax_v = kv[1][0].taxonomy_version %}{% endif %}{% endfor %}
<p class="lb-meta">
  Schema v{{ site.data.leaderboard.schema }} ·
  Benchmark v{{ bench_v }} ·
  Taxonomy v{{ tax_v }}
</p>

<div class="lb-breakout">
<div class="table-card lb-tight lb-scroll">
<table id="leaderboard" class="lb">
  <thead>
    <tr>
      <th data-type="text">Model</th>
      <th data-type="text">Adapter</th>
      <th data-type="text">Lang</th>
      <th data-type="text">Domain</th>
      <th data-type="num">Precision</th>
      <th data-type="num">Recall</th>
      <th data-type="num" class="f1">F1</th>
      <th data-type="num">n</th>
      <th data-type="text">Contamination</th>
      <th data-type="text">Validation</th>
    </tr>
  </thead>
  <tbody>
  {% for kv in site.data.leaderboard.entries %}
    {% for row in kv[1] %}
    <tr{% if row.contamination == "in_distribution" %} class="row-indist"{% endif %}>
      <td><code>{{ row.model_id }}</code></td>
      <td>{{ row.adapter }}</td>
      <td>{{ row.languages[0] }}</td>
      <td>{{ row.domain }}</td>
      <td>{{ row.scores.entity_f1.precision | times: 100 | round: 1 }}</td>
      <td>{{ row.scores.entity_f1.recall | times: 100 | round: 1 }}</td>
      <td class="f1">{{ row.scores.entity_f1.f1 | times: 100 | round: 1 }}{% if row.contamination == "in_distribution" and row.scores.entity_f1.f1 >= 1.0 %}<span class="indist-note">memorised</span>{% endif %}</td>
      <td>{{ row.n }}</td>
      <td>
        {% if row.contamination == "in_distribution" %}<span class="lb-badge contam-in" title="Model was trained on this config's source data — score inflated by train/eval overlap">in-distribution</span>
        {% elsif row.contamination == "clean_held_out" %}<span class="lb-badge contam-clean" title="No baseline was trained on this data — a fair held-out test">clean held-out</span>
        {% else %}<span class="lb-badge contam-unknown" title="Train/eval overlap not established">unknown</span>{% endif %}
      </td>
      <td>
        {% if row.config_status == "citable-validated" %}<span class="lb-badge status-citable" title="Passed native-speaker / inter-annotator-agreement sign-off — citable as a validated result">citable</span>
        {% else %}<span class="lb-badge status-dev" title="Development config — not yet validated, must not be cited as a validated benchmark result">dev</span>{% endif %}
      </td>
    </tr>
    {% endfor %}
  {% endfor %}
  </tbody>
</table>
</div>
</div>

<p class="lb-meta">
  Each row reports entity-level precision / recall / F1 (×100) under the unified KlusAI
  privacy taxonomy. Results carry full provenance (model id, dataset config/split,
  harness &amp; taxonomy version, timestamp) in the
  <a href="https://github.com/klusai">source repository</a>.
</p>

## How to submit

EuroPriv-Bench is open. Run the harness against your model and open a PR adding your
entry to <code>baselines/leaderboard.json</code> — see the
[benchmark repo](https://github.com/klusai) for the adapter contract and reproduction
steps. Entries without reproducible provenance are not listed.

<script src="{{ '/assets/js/sort-table.js' | relative_url }}?v={{ site.time | date: '%s' }}"></script>
