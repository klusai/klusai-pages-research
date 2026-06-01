---
layout: page
title: "Leaderboard"
permalink: /leaderboard/
---

<p class="eyebrow">Flagship benchmark</p>

# EuroPriv-Bench Leaderboard

Entity-level scores on the [`klusai/europriv-bench`](https://huggingface.co/datasets/klusai/europriv-bench)
test split, by model and language. Higher is better. Click a column header to sort.

Each row carries two governance markers. **Contamination** flags whether the model was trained on
that config's source data — an <span class="lb-badge contam-in">in-distribution</span> score is
inflated by train/eval overlap, while a <span class="lb-badge contam-clean">clean held-out</span>
score is a fair test. **Validation** shows whether a config has passed native-speaker / IAA
sign-off: only a <span class="lb-badge status-citable">citable</span> row may be cited as a
validated result. Everything is currently <span class="lb-badge status-dev">dev</span> — not yet
citable.

{% assign bench_v = "" %}{% for kv in site.data.leaderboard.entries %}{% if bench_v == "" %}{% assign bench_v = kv[1][0].europriv_bench_version %}{% assign tax_v = kv[1][0].taxonomy_version %}{% endif %}{% endfor %}
<p class="lb-meta">
  Schema v{{ site.data.leaderboard.schema }} ·
  Benchmark v{{ bench_v }} ·
  Taxonomy v{{ tax_v }}
</p>

<div class="table-card">
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
    <tr>
      <td><code>{{ row.model_id }}</code></td>
      <td>{{ row.adapter }}</td>
      <td>{{ row.languages[0] }}</td>
      <td>{{ row.domain }}</td>
      <td>{{ row.scores.entity_f1.precision | times: 100 | round: 1 }}</td>
      <td>{{ row.scores.entity_f1.recall | times: 100 | round: 1 }}</td>
      <td class="f1">{{ row.scores.entity_f1.f1 | times: 100 | round: 1 }}</td>
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

<p class="lb-meta">
  Each row reports entity-level precision / recall / F1 (×100) under the unified KlusAI
  privacy taxonomy. Results carry full provenance (model id, dataset config/split,
  harness &amp; taxonomy version, timestamp) in the
  <a href="https://github.com/klusai">source repository</a>.
</p>

## Re-identification leakage — the metric that matters

Detection F1 is not privacy. EuroPriv-Bench also measures **re-identification leakage**: on the
Romanian configs, a missed (un-redacted) **CNP** deterministically discloses the person's
**date of birth + sex + county**. The table counts, per model, the CNPs left un-redacted and the
quasi-identifiers thereby leaked (lower is better).

<div class="table-card">
<table id="leakage" class="lb">
  <thead>
    <tr>
      <th data-type="text">Model</th>
      <th data-type="text">Track</th>
      <th data-type="text">Contamination</th>
      <th data-type="num">Leak rate %</th>
      <th data-type="num">CNPs missed</th>
      <th data-type="num">Quasi-identifiers leaked</th>
    </tr>
  </thead>
  <tbody>
  {% for kv in site.data.leaderboard.entries %}
    {% for row in kv[1] %}
    {% if row.scores.cnp_leakage %}
    <tr>
      <td>{{ row.adapter }}</td>
      <td><code>{{ row.dataset.config }}</code></td>
      <td>
        {% if row.contamination == "in_distribution" %}<span class="lb-badge contam-in" title="Model was trained on this config's source data">in-distribution</span>
        {% elsif row.contamination == "clean_held_out" %}<span class="lb-badge contam-clean" title="No baseline was trained on this data — a fair held-out test">clean held-out</span>
        {% else %}<span class="lb-badge contam-unknown" title="Train/eval overlap not established">unknown</span>{% endif %}
      </td>
      <td>{{ row.scores.cnp_leakage.leak_rate | times: 100 | round: 1 }}</td>
      <td>{{ row.scores.cnp_leakage.cnp_missed | round: 0 }}</td>
      <td>{{ row.scores.cnp_leakage.leaked_quasi_identifiers | round: 0 }}</td>
    </tr>
    {% endif %}
    {% endfor %}
  {% endfor %}
  </tbody>
</table>
</div>

<p class="lb-meta">
  The dissociation is the point: on realistic-structure Romanian documents
  (<code>ro-realskeleton-v1</code>) the model with the <em>best</em> detection F1 leaks the
  <em>most</em> CNPs, while a model with lower F1 redacts nearly all of them. A high F1 score
  does not mean a model protects privacy — which is why this benchmark leads with leakage.
</p>

## How to submit

EuroPriv-Bench is open. Run the harness against your model and open a PR adding your
entry to <code>baselines/leaderboard.json</code> — see the
[benchmark repo](https://github.com/klusai) for the adapter contract and reproduction
steps. Entries without reproducible provenance are not listed.

<script src="{{ '/assets/js/sort-table.js' | relative_url }}?v={{ site.time | date: '%s' }}"></script>
