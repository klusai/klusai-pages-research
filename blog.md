---
layout: page
title: "Blog"
permalink: /blog/
---

<p class="eyebrow">Notes from the privacy program</p>

Methodology, engineering, and results as we build EuroPriv-Bench and the KlusAI privacy models.

<ul class="post-list">
  {%- for post in site.posts -%}
  <li>
    <span class="post-meta">{{ post.date | date: "%b %-d, %Y" }}</span>
    <h3><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h3>
    {%- if site.show_excerpts -%}{{ post.excerpt }}{%- endif -%}
  </li>
  {%- endfor -%}
</ul>
