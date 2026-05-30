# klusai.github.io — KlusAI Research hub

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
scripts/         sync_leaderboard.sh
.github/         daily leaderboard sync workflow
CNAME            research.klusai.com
```

## Local preview

```bash
bundle install
bundle exec jekyll serve     # http://127.0.0.1:4000
```

## Updating the leaderboard

The leaderboard renders from `_data/leaderboard.json`. Refresh it from a sibling
`europriv-bench` checkout:

```bash
./scripts/sync_leaderboard.sh
```

In CI this happens daily via `.github/workflows/sync-leaderboard.yml` (needs the
`EUROPRIV_TOKEN` secret while `europriv-bench` is private).

## One-time setup (GitHub UI — needs org admin)

1. **Make the repo public** (Settings → General → Danger Zone) so Pages can publish.
2. **Settings → Pages** → Source: deploy from `main`; Custom domain: `research.klusai.com`; Enforce HTTPS.
3. **DNS** at the klusai.com provider: `research CNAME klusai.github.io.`
