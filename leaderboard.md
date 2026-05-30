---
layout: page
title: "Leaderboard"
permalink: /leaderboard/
---

# EuroPriv-Bench Leaderboard

Entity-level scores on the [`klusai/europriv-bench`](https://huggingface.co/datasets/klusai/europriv-bench)
test split, by model and language. Higher is better. Click a column header to sort.

{% assign bench_v = "" %}{% for kv in site.data.leaderboard.entries %}{% if bench_v == "" %}{% assign bench_v = kv[1][0].europriv_bench_version %}{% assign tax_v = kv[1][0].taxonomy_version %}{% endif %}{% endfor %}
<p class="lb-meta">
  Schema v{{ site.data.leaderboard.schema }} ·
  Benchmark v{{ bench_v }} ·
  Taxonomy v{{ tax_v }}
</p>

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
    </tr>
    {% endfor %}
  {% endfor %}
  </tbody>
</table>

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

<script src="{{ '/assets/js/sort-table.js' | relative_url }}"></script>
