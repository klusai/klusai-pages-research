---
layout: home
title: "KlusAI Research"
list_title: "Latest posts"
---
<section class="hero">
  <div class="wrap">
    <p class="badge">EU-Sovereign AI Platform · Applied Research · Vertical Products</p>
    <h1>Privacy-preserving NLP for<br><span class="accent-word">European languages</span></h1>
    <p class="lead">
      The open research hub of KlusAI — benchmarks, datasets, models and papers for
      PII/PHI detection, anonymization, and re-identification-risk evaluation across
      European languages (8 published datasets: ro, en, pl, de, fr, es, it, nl — scaling
      toward EU-24), spanning the legal and clinical domains.
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
      <strong>re-identification risk</strong> alongside detection on a single GDPR-aligned
      taxonomy. Eight languages are published — ro, en, pl, de, fr, es, it, nl. Seven have
      general-text tracks (de, en, es, fr, it, nl, ro), and three carry contamination-controlled,
      decode-bearing real-skeleton tracks: Romanian (CNP), Polish (PESEL), and Italian (codice
      fiscale). The roadmap scales toward the full EU-24.
    </p>
    <p>
      The headline finding: <strong>detection-F1 does not track re-identification protection —
      demonstrated on decode-bearing national identifiers (RO CNP, PL PESEL, IT codice fiscale)</strong>.
      The deeper mechanism is general but the proof is not yet: an aggregate detection-F1 can stay
      high while a model misses the <em>rare, high-stakes tokens</em> that actually carry the
      re-identification. National IDs are the clearest, <strong>provable</strong> case of that —
      each un-redacted national ID deterministically discloses several quasi-identifiers at once (a
      Romanian CNP, for instance, decodes date of birth, sex, and county) — not the whole of it.
      On contamination-free, realistic-structure documents the dissociation holds across
      <strong>three decode-bearing identifiers in three languages</strong> (RO CNP, PL PESEL, IT
      codice fiscale), across <strong>two independent Romanian template families</strong>, and is
      reproduced by independent third-party submissions on the public board: spaCy, with no
      structured-ID recognizer, leaks <strong>89.0%</strong> of Romanian CNPs at a detection-F1 of
      just 0.14, while GLiNER — the strongest detector on the track (F1 0.85) — still leaks 30.2%.
      The contrast is KlusAI's reference de-identifier kp-deid, the <strong>strongest protector
      that still detects — 0% CNP leakage at detection-F1 0.74</strong>. These are measured,
      contamination-controlled signals on development-track gold (<code>config_status = dev</code>),
      pending native-speaker and inter-annotator-agreement validation — a finding, not yet a
      validated or citable claim. Extending the measure to quasi-identifier-combination
      re-identification is in progress, so the broad reading remains a hypothesis under test.
    </p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Artifacts</p>
      <h2>Open from day one</h2>
    </div>
    <div class="card-grid cols-4">
      <div class="card">
        <div class="icon-tile">HF</div>
        <div>
          <h3>Benchmark</h3>
          <p>EuroPriv-Bench — versioned, provenance-tracked, openly redistributable. The live
          leaderboard is open for external submissions.</p>
          <div class="chip-row">
            <a class="chip chip-accent" href="https://huggingface.co/datasets/klusai/europriv-bench">Hugging Face ↗</a>
            <a class="chip chip-muted" href="{{ '/leaderboard/#how-to-submit' | relative_url }}">Submit a model →</a>
          </div>
        </div>
      </div>
      <div class="card">
        <div class="icon-tile">kp</div>
        <div>
          <h3>Models</h3>
          <p>The KlusAI Privacy (kp-*) family — kp-deid-mdeberta-280m is the strongest protector
          that still detects (0% CNP leakage at detection-F1 0.74).</p>
          <div class="chip-row">
            <a class="chip chip-accent" href="https://huggingface.co/klusai/kp-deid-mdeberta-280m">Hugging Face ↗</a>
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
          <p>The EuroPriv-Bench preprint — reproducible numbers that trace back to a commit.
          In-progress working paper; arXiv pending.</p>
          <div class="chip-row">
            <a class="chip chip-accent" href="{{ '/papers/europriv-bench/' | relative_url }}">Read the paper →</a>
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
