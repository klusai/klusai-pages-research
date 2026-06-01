---
layout: page
title: "Papers"
permalink: /papers/
---

<p class="eyebrow">Research</p>

# Papers

Preprints and technical reports from the KlusAI privacy program — each built on the open
[benchmark](/leaderboard/), datasets, and models.

<ul class="post-list">
  {%- assign papers = site.papers | sort: "date" | reverse -%}
  {%- for p in papers -%}
  <li>
    <span class="post-meta">{{ p.date | date: "%b %-d, %Y" }}{% if p.status %} · {{ p.status }}{% endif %}</span>
    <h3><a href="{{ p.url | relative_url }}">{{ p.title }}</a></h3>
    {%- if p.authors %}<p class="paper-authors">{{ p.authors }}</p>{%- endif %}
    {%- if p.abstract %}<p>{{ p.abstract | truncatewords: 48 }}</p>{%- endif %}
  </li>
  {%- endfor -%}
</ul>
