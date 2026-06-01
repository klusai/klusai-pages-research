---
layout: page
title: "Papers"
permalink: /papers/
---

<style>
  .papers-intro { max-width: 640px; }
  .paper-list { display: grid; gap: 1.5rem; margin: 2.2rem 0 1rem; }
  .paper-card {
    position: relative; display: grid; grid-template-columns: 215px 1fr;
    border: 1px solid var(--border); border-radius: 16px; overflow: hidden;
    background: var(--surface); box-shadow: var(--shadow);
    transition: border-color .15s ease, box-shadow .2s ease, transform .15s ease;
  }
  .paper-card:hover { border-color: var(--accent); box-shadow: 0 14px 40px rgba(15,30,50,.12); transform: translateY(-3px); }
  .paper-cover {
    position: relative; overflow: hidden; padding: 1.35rem 1.3rem; min-height: 190px;
    display: flex; flex-direction: column; color: #fff;
    background: linear-gradient(145deg, #14B8A6 0%, #488EFF 100%);
  }
  .paper-cover::after {
    content: ""; position: absolute; right: -34px; bottom: -34px; width: 130px; height: 130px;
    border-radius: 50%; background: rgba(255,255,255,.13);
  }
  .paper-cover .cover-kicker { font-family: var(--font-display); font-size: .68rem; letter-spacing: .09em; text-transform: uppercase; opacity: .9; position: relative; z-index: 1; }
  .paper-cover .cover-title { font-family: var(--font-display); font-weight: 700; font-size: 1.5rem; line-height: 1.12; margin: .2rem 0 0; position: relative; z-index: 1; }
  .paper-cover .cover-sub { font-size: .8rem; line-height: 1.4; opacity: .94; margin-top: auto; position: relative; z-index: 1; }
  .paper-body { padding: 1.3rem 1.5rem; display: flex; flex-direction: column; min-width: 0; }
  .paper-meta-row { display: flex; align-items: center; gap: .6rem; font-size: .8rem; color: var(--text-secondary); }
  .paper-meta-row time { font-variant-numeric: tabular-nums; }
  .paper-badge { display: inline-block; border-radius: 999px; background: var(--accent-soft-bg); color: var(--accent-soft-text); padding: .12rem .58rem; font-size: .72rem; font-weight: 600; }
  .paper-title { font-size: 1.34rem; line-height: 1.25; margin: .35rem 0 .25rem; }
  .paper-title a { color: var(--text); text-decoration: none; }
  .paper-title a::after { content: ""; position: absolute; inset: 0; }
  .paper-card:hover .paper-title a { color: var(--accent); }
  .paper-byline { font-size: .86rem; color: var(--text-secondary); margin: 0 0 .55rem; }
  .paper-tldr { font-size: .98rem; line-height: 1.55; color: var(--text); margin: 0 0 .8rem; }
  .paper-tags { display: flex; flex-wrap: wrap; gap: .4rem; margin: 0 0 .95rem; }
  .paper-tag { font-size: .72rem; background: var(--surface-alt); color: var(--text-secondary); border-radius: 999px; padding: .18rem .62rem; }
  .paper-links { display: flex; flex-wrap: wrap; align-items: center; gap: .5rem; margin-top: auto; position: relative; z-index: 1; }
  .paper-links a { font-size: .82rem; font-weight: 500; text-decoration: none; border-radius: 999px; padding: .3rem .8rem; background: var(--surface-alt); color: var(--text-secondary); transition: background .12s, color .12s; }
  .paper-links a:hover { background: var(--accent-soft-bg); color: var(--accent-soft-text); }
  .paper-links a.paper-read { background: var(--accent-soft-bg); color: var(--accent-soft-text); margin-left: auto; }
  @media (max-width: 720px) {
    .paper-card { grid-template-columns: 1fr; }
    .paper-cover { min-height: 0; padding: 1.15rem 1.25rem; }
    .paper-cover .cover-sub { margin-top: .35rem; }
    .paper-links a.paper-read { margin-left: 0; }
  }
</style>

<p class="eyebrow">Research</p>

# Papers

<p class="papers-intro">Open research from the KlusAI privacy program. Each paper ships a working
artifact — a <a href="/leaderboard/">benchmark</a>, dataset, or model — not just a writeup.</p>

<div class="paper-list">
  {%- assign papers = site.papers | sort: "date" | reverse -%}
  {%- for p in papers -%}
  <article class="paper-card">
    <div class="paper-cover">
      <span class="cover-kicker">{{ p.venue | default: "Technical Report" }}</span>
      <span class="cover-title">{{ p.cover_title | default: p.title }}</span>
      {%- if p.cover_sub %}<span class="cover-sub">{{ p.cover_sub }}</span>{%- endif %}
    </div>
    <div class="paper-body">
      <div class="paper-meta-row">
        <time>{{ p.date | date: "%B %Y" }}</time>
        {%- if p.status %}<span class="paper-badge">{{ p.status | split: " ·" | first }}</span>{%- endif %}
      </div>
      <h2 class="paper-title"><a href="{{ p.url | relative_url }}">{{ p.title }}</a></h2>
      {%- if p.authors %}<p class="paper-byline">{{ p.authors }}{% if p.affiliation %} · {{ p.affiliation }}{% endif %}</p>{%- endif %}
      <p class="paper-tldr">{% if p.tldr %}{{ p.tldr }}{% else %}{{ p.abstract | truncatewords: 36 }}{% endif %}</p>
      {%- if p.tags %}<div class="paper-tags">{%- for t in p.tags %}<span class="paper-tag">{{ t }}</span>{%- endfor %}</div>{%- endif %}
      <div class="paper-links">
        {%- if p.data %}<a href="{{ p.data }}" target="_blank" rel="noopener">Dataset ↗</a>{%- endif %}
        {%- if p.code %}<a href="{{ p.code }}" target="_blank" rel="noopener">Code ↗</a>{%- endif %}
        {%- if p.leaderboard %}<a href="{{ p.leaderboard | relative_url }}">Leaderboard</a>{%- endif %}
        <a class="paper-read" href="{{ p.url | relative_url }}">Read paper →</a>
      </div>
    </div>
  </article>
  {%- endfor -%}
</div>
