---
layout: home
title: "Research"
list_title: "Latest posts"
---
<section class="hero">
  <div class="wrap">
    <p class="badge">Applied Research · AI Services · Ventures</p>
    <h1>Privacy-preserving NLP for<br><span class="accent-word">European languages</span></h1>
    <p class="lead">
      The open research hub of KlusAI — benchmarks, datasets, models and papers for
      PII/PHI detection, anonymization, and re-identification-risk evaluation across
      European languages (7 live, scaling to 20), spanning the legal and clinical domains.
    </p>
    <div class="cta-row">
      <a class="btn btn-primary" href="{{ '/leaderboard/' | relative_url }}">See the live leaderboard →</a>
      <a class="btn btn-ghost" href="https://huggingface.co/datasets/klusai/europriv-bench">Benchmark on Hugging Face</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap narrow">
    <p class="eyebrow">Flagship benchmark</p>
    <h2>EuroPriv-Bench</h2>
    <p>
      EuroPriv-Bench is the first <em>unified</em> pan-European de-identification benchmark.
      Unlike prior work that reports only detection-F1 on English, it measures
      <strong>privacy-utility / re-identification risk</strong> on a single GDPR-aligned
      taxonomy across European languages (7 live, scaling to 20), spanning legal and clinical text.
    </p>
    <p>
      The headline finding: <strong>detection-F1 is not privacy</strong>. On realistic-structure
      Romanian documents, the model with the <em>best</em> detection F1 leaks the <em>most</em>
      national IDs — and each un-redacted Romanian CNP discloses a person's date of birth, sex,
      and county. A high F1 score does not mean a model protects privacy.
    </p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Artifacts</p>
      <h2>Open from day one</h2>
    </div>
    <div class="card-grid cols-3">
      <div class="card">
        <div class="icon-tile">HF</div>
        <div>
          <h3>Benchmark</h3>
          <p>EuroPriv-Bench — versioned, provenance-tracked, openly redistributable.</p>
          <div class="chip-row">
            <a class="chip chip-accent" href="https://huggingface.co/datasets/klusai/europriv-bench">Hugging Face ↗</a>
          </div>
        </div>
      </div>
      <div class="card">
        <div class="icon-tile">&lt;/&gt;</div>
        <div>
          <h3>Code</h3>
          <p>The benchmark harness, dataset curation, and model training pipelines.</p>
          <div class="chip-row">
            <a class="chip chip-muted" href="https://github.com/klusai">GitHub ↗</a>
          </div>
        </div>
      </div>
      <div class="card">
        <div class="icon-tile">arXiv</div>
        <div>
          <h3>Papers</h3>
          <p>Preprints with reproducible numbers that trace back to a commit.</p>
          <div class="chip-row">
            <span class="chip chip-muted">Coming soon</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap narrow">
    <p class="eyebrow">What we publish here</p>
    <h2>A citable home for the program</h2>
    <ul>
      <li><strong>Leaderboards</strong> — versioned, provenance-tracked results you can cite.</li>
      <li><strong>Release notes &amp; methodology</strong> — the technical story behind each artifact.</li>
      <li><strong>Paper companions</strong> — reproducible numbers tracing back to a commit.</li>
    </ul>
    <p>For the company and product, see <a href="https://klusai.com">klusai.com</a>.</p>
  </div>
</section>
