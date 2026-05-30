#!/usr/bin/env bash
# Sync the EuroPriv-Bench leaderboard into the site's _data so it renders at build time.
#
# Local use (sibling checkout): ./scripts/sync_leaderboard.sh
# CI use: pass a path or raw URL as $1, or set SRC env var.
set -euo pipefail

DEST="$(cd "$(dirname "$0")/.." && pwd)/_data/leaderboard.json"
SRC="${1:-${SRC:-../europriv-bench/baselines/leaderboard.json}}"

if [[ "$SRC" == http* ]]; then
  echo "Fetching leaderboard from $SRC"
  curl -fsSL "$SRC" -o "$DEST"
else
  echo "Copying leaderboard from $SRC"
  cp "$SRC" "$DEST"
fi

# Fail loudly if the JSON is malformed — better than shipping a broken table.
python3 -c "import json,sys; json.load(open('$DEST')); print('ok:', sum(len(v) for v in json.load(open('$DEST'))['entries'].values()), 'rows')"
