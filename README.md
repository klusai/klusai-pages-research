# klusai-pages-research — KlusAI Research hub

> **Repo rename:** `klusai.github.io` → `klusai-pages-research` (June 2026). GitHub redirects old clone URLs. Custom domain unchanged.

> **Visibility:** `klusai-pages-*` repos are **private** (org policy). The site at research.klusai.com stays public via GitHub Pages on GitHub Team.

Public research site for the KlusAI privacy-models program. Served at
**https://research.klusai.com** (GitHub Pages + custom domain). The company/product
site lives separately at [klusai.com](https://klusai.com).

Built with Jekyll + the `minima` remote theme (same setup as `mihainadas.github.io`),
so GitHub Pages builds it with no extra config.

## Structure

```
_config.yml      site config, nav, theme, program links
index.md         landing page (program overview)
leaderboard.md   EuroPriv-Bench leaderboard — renders _data/leaderboard.json at build
about.md         program overview
_data/           leaderboard.json (synced from europriv-bench)
_posts/          release notes / announcements
assets/          leaderboard sort JS + theme overrides
scripts/         sync_leaderboard.sh, gen_status.py (+ sample_linear_issues.json)
.github/         daily leaderboard sync + status-proposer workflows
CNAME            research.klusai.com
```

## Local preview

```bash
bundle install
bundle exec jekyll serve     # http://127.0.0.1:4000
```

On the shared Mac Studio, run **`pages-preview`** in this repo for a GitHub Pages
parity preview reachable from your laptop / Claude-in-Chrome over the tailnet (it
prints a Tailnet URL). Installed via `kai services install pages-preview` (see
`klusai-infra`).

## PR checks and auto-merge

With Ruby 3.2, run `bundle install` then `make check`. This builds with the
`github-pages` gem in production/safe mode, rejects Liquid syntax and filter
errors, and checks generated internal links and assets with HTMLProofer (no
external URL requests). Optional Liquid variables stay optional. To put build
output outside the checkout, use `make check SITE_DEST=/path/to/scratch/site`.

The PR/main workflow reports the `test` job. Auto-merge follows the
`klusai/europriv-bench` pattern: it stays inactive unless main visibly requires
`test`, honors draft/hold/review gates, and never checks out PR code in its
privileged workflow. Repository admins must enable squash and auto-merge and
configure required checks before it can arm; keep "Require branches to be up to
date" off for parity with that pattern.

Keep main protected with required `test`. Leaderboard sync pushes only to an
`automation/sync-leaderboard-*` branch and opens a PR labelled `automerge`, reusing
the open sync PR on later runs. Runs are serialized and duplicate sync PRs fail
closed; existing `hold`/`needs-review` labels and draft status remain effective.

Sync uses `GITHUB_TOKEN` with contents, pull-requests and actions write permissions.
Token-created PR events do not automatically run unattended workflows (some
GitHub configurations offer approval-required runs), so sync explicitly invokes
`workflow_dispatch` for `ci.yml` on the PR branch and `auto-merge.yml` on main.
The `test` check therefore belongs to the PR head commit; privileged auto-merge
only reads PR metadata and retains the required-`test` guard. Dispatch is retried
even if a pending PR's data is unchanged. No protection bypass or extra token is
needed. See GitHub's [workflow-trigger documentation](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow).

Before enabling sync, merge these workflows into main, create the `automerge`
label if absent, and allow GitHub Actions to create pull requests in repository
settings (subject to organization policy). Hosted dispatch/check association and
auto-merge must be verified after deployment; local checks cannot exercise them.

## Updating the leaderboard

The leaderboard renders from `_data/leaderboard.json`. Refresh it from a sibling
`europriv-bench` checkout:

```bash
./scripts/sync_leaderboard.sh
```

In CI this happens daily via `.github/workflows/sync-leaderboard.yml` (needs the
`EUROPRIV_TOKEN` secret while `europriv-bench` is private).

## Status & updates section (PoC — RES-35)

`scripts/gen_status.py` auto-generates the roadmap's **Status & updates** section
from the EuroPriv-Bench program tracker (Done → ✓ Shipped, In Progress / In Review
→ ▶, next public Todo → →). It is **public-safe by construction**: every issue is
mapped to curated public-facing prose via an allow-list (unmatched issues are
dropped, never echoed), and a final redaction guard refuses to emit any internal
issue IDs, process/tooling tokens, or unreleased numbers.

```bash
# Prove the redaction guard rejects leaky input
./scripts/gen_status.py --self-test

# Render the proposed public section from a Linear issues dump (or the sample)
./scripts/gen_status.py --issues scripts/sample_linear_issues.json

# Diff the proposal against the live hand-written section (does NOT touch roadmap.md)
./scripts/gen_status.py --issues scripts/sample_linear_issues.json --dry-run
```

This is a **bounded PoC**: it *proposes* a section (and can `--emit-json` a
`_data/status.generated.json`), but it never overwrites the live roadmap. The CI
proposer (`.github/workflows/propose-status.yml`, manual-only) uploads the diff as
a build artifact for human review. Live Linear access needs a `LINEAR_TOKEN` Actions
secret, which is gated on **RES-62**; until then the loop-maintained hand-written
section stands and the workflow falls back to the checked-in sample fixture.

## One-time setup (GitHub UI — needs org admin)

1. **Keep the repo private** — all `klusai-pages-*` repos are private; GitHub Team publishes Pages from private repos.
2. **Settings → Pages** → Source: deploy from `main`; Custom domain: `research.klusai.com`; Enforce HTTPS.
3. **DNS** at the klusai.com provider: `research CNAME klusai.github.io.` (unchanged after repo rename)
