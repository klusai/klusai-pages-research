#!/usr/bin/env python3
"""Generate the roadmap "Status & updates" section from Linear — public-safe (PoC).

This is a *bounded proof-of-concept* for RES-35. It reads the EuroPriv-Bench
Linear project (team "Research") and derives the roadmap's public
"Status & updates" section: Done -> "Shipped", In Progress/In Review ->
"In progress", next unblocked Todo -> "Up next".

PUBLIC-SAFETY IS THE WHOLE POINT. The roadmap is a public page, so this script
never echoes raw Linear content. Instead it:

  1. Maps each issue to a curated, *public-facing* theme (see THEME_RULES).
     Issues that don't match an approved public theme are DROPPED (fail-closed),
     so nothing internal can leak by accident.
  2. Runs a hard redaction guard over the final text that REFUSES to emit:
       - any Linear issue IDs (KLU-### or RES-### — issues were re-keyed
         KLU->RES, so both prefixes are blocked),
       - internal process/tooling tokens (file paths, script names, branch
         names, CI internals, "Linear", etc.),
       - unreleased / internal numbers (leak-rate percentages, F1 scores,
         confidence-interval bounds, etc.).
     If any forbidden token survives the mapping, the guard raises and the
     script exits non-zero rather than shipping leaky text.

Because the production token wiring (a Linear read token as an Actions secret)
is gated on RES-62, this PoC does NOT call the Linear API itself and does NOT
overwrite the live roadmap. It reads a Linear issues JSON dump (the shape
returned by Linear's MCP `list_issues` / the GraphQL API) from a file or stdin,
writes a proposed `_data/status.generated.json`, and offers a `--dry-run` that
diffs the generated section against the current hand-written one in roadmap.md.
Propose, don't clobber.

Usage:
    # Render the public section to stdout from a Linear dump
    ./scripts/gen_status.py --issues linear_issues.json

    # Write the proposed _data/status.generated.json (build-time data file)
    ./scripts/gen_status.py --issues linear_issues.json --emit-json

    # Diff the generated section against the live hand-written section
    ./scripts/gen_status.py --issues linear_issues.json --dry-run

    # Prove the redaction guard rejects leaky input
    ./scripts/gen_status.py --self-test

    # Read the dump from stdin
    linear-export | ./scripts/gen_status.py --issues -
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ROADMAP = REPO_ROOT / "roadmap.md"
DEFAULT_JSON_OUT = REPO_ROOT / "_data" / "status.generated.json"

# ---------------------------------------------------------------------------
# 1. Linear -> public theme mapping.
#
# Each rule matches an issue (by keyword in its title) and maps it to ONE
# curated public theme. The mapping is the redaction boundary: we emit the
# theme's hand-written public prose, never the issue's own title/description.
# Several issues can collapse into the same theme (deduplicated on output) —
# that is intended, it keeps the public list short and on-message.
#
# A theme is keyed by a stable string; "blurb" is the public sentence that
# appears in the rendered section. Themes carry an axis label (Benchmark /
# Models / Datasets / Papers / Site) used to group the "Shipped" bullets the
# way the hand-written roadmap does.
# ---------------------------------------------------------------------------

# axis -> human label used in the "Shipped" grouping
AXES = ["Benchmark", "Models", "Datasets", "Papers", "Site"]

# theme_key -> {axis, blurb}
THEMES: dict[str, dict[str, str]] = {
    "reid-metric-breadth": {
        "axis": "Benchmark",
        "blurb": "the re-identification-risk metric now spans multiple European national-identifier families, each leak measurement carrying a harness-emitted confidence interval",
    },
    "leaderboard-schema": {
        "axis": "Benchmark",
        "blurb": "the public leaderboard records contamination and citation-readiness status for every row, so in-distribution and clean held-out results are kept visibly separate",
    },
    "governance-taxonomy": {
        "axis": "Benchmark",
        "blurb": "the taxonomy is versioned under a published governance and stability contract",
    },
    "submission-ci": {
        "axis": "Benchmark",
        "blurb": "an externally-contributable submission path lets outside models be scored on the public configs, with a reproduction gate keeping the board honest",
    },
    "external-submissions": {
        "axis": "Benchmark",
        "blurb": "independent third-party systems have been scored through the open submission path, sharpening the detection-vs-protection finding across multiple external models",
    },
    "leaderboard-ux": {
        "axis": "Site",
        "blurb": "the public leaderboard leads with the re-identification finding and a clear visual, readable by non-experts while keeping every caveat intact",
    },
    "site-refresh": {
        "axis": "Site",
        "blurb": "the public research site has been refreshed to reflect current breadth",
    },
    "localepack-datasets": {
        "axis": "Datasets",
        "blurb": "a reusable locale-pack abstraction with checksum-valid identifiers and offset-correct gold underpins the first open general-domain datasets published on Hugging Face",
    },
    "t1-datasets": {
        "axis": "Datasets",
        "blurb": "the open general-domain dataset family has been extended across the first tier of European languages",
    },
    "drift-metric": {
        "axis": "Datasets",
        "blurb": "a synthetic-to-real drift measure quantifies the gap between synthetic and real contexts",
    },
    "kp-deid-model": {
        "axis": "Models",
        "blurb": "the first open de-identification protector model is published and featured on the public leaderboard as the strongest protector on the contamination-free track",
    },
    "on-device-training": {
        "axis": "Models",
        "blurb": "on-device Apple-Silicon GPU training is enabled, so full fine-tunes run locally without cloud GPUs",
    },
    "sdk": {
        "axis": "Models",
        "blurb": "the open SDK exposes a one-call PII-extraction entry point backed by the protector model",
    },
    "anonymization-track": {
        "axis": "Models",
        "blurb": "an anonymization-and-utility track has moved from stub to an early result on the privacy-utility frontier",
    },
    "multilingual-protector": {
        "axis": "Models",
        "blurb": "a multilingual protector trained across the first-tier European languages",
    },
    "cross-lingual-replication": {
        "axis": "Benchmark",
        "blurb": "the detection-does-not-track-protection finding has been replicated across several languages and decode-bearing identifiers, and across independent template families",
    },
    "legal-track": {
        "axis": "Benchmark",
        "blurb": "a structure-only legal-domain track (no copyrighted source text redistributed) extends the finding into the legal genre",
    },
    "paper-protocol": {
        "axis": "Papers",
        "blurb": "the submission and artifact-evaluation protocol is written, and a fresh prior-art rescan re-confirmed the “first unified” position",
    },
    "pareto-figure": {
        "axis": "Papers",
        "blurb": "the detection-vs-protection frontier figure and its significance test are prepared for publication",
    },
    # In-progress / up-next themes
    "validate-citable-gold": {
        "axis": "Benchmark",
        "blurb": "hardening the flagship Romanian real-skeleton track into validated, citable gold (native-speaker and inter-annotator sign-off) so its leaderboard row can be promoted to citation-ready",
    },
    "more-id-validators": {
        "axis": "Benchmark",
        "blurb": "broadening national-identifier coverage to further European jurisdictions in the single source-of-truth harness",
    },
    "paper-publication": {
        "axis": "Papers",
        "blurb": "the first paper is moving toward an open-access release with a citable archival record",
    },
    "paper-frontmatter": {
        "axis": "Papers",
        "blurb": "aligning the paper's stated language breadth with the current benchmark coverage",
    },
    "broaden-reid": {
        "axis": "Benchmark",
        "blurb": "broadening re-identification measurement beyond decode-bearing identifiers toward quasi-identifier-combination re-identification",
    },
    "ops-enablement": {
        "axis": "Site",
        "blurb": "remaining open-infrastructure enablement so the public status view can refresh automatically",
    },
}

# Ordered keyword rules: first match wins. Each entry is (theme_key, [keywords]).
# Keywords are matched case-insensitively against the issue title. This is a
# *curated allow-list*: an issue that matches nothing is dropped, never echoed.
# Ordering matters — more specific rules precede broader ones.
THEME_RULES: list[tuple[str, list[str]]] = [
    ("validate-citable-gold", ["native-speaker", "iaa", "citable-validated", "sign-off"]),
    # Datasets/model T1-breadth rules must precede the validator rule so that
    # "de/fr/es/it/nl" dataset/model issues don't get swallowed by it.
    ("t1-datasets", ["t1 localepack", "t1 datasets", "5 t1", "publish the 5", "5 packs"]),
    ("multilingual-protector", ["kp-deid v2", "multilingual protector"]),
    # More-specific national-ID *validator* breadth: require the validator context.
    ("more-id-validators", ["national-id validators", "national_id validators", "additional national-id", "more national-id"]),
    ("cross-lingual-replication", ["replicate", "pesel", "codice fiscale", "template family", "2nd id", "second language", "it-realskeleton", "pl-realskeleton"]),
    ("legal-track", ["legal-domain", "legal real-skeleton", "eur-lex", "echr"]),
    ("reid-metric-breadth", ["wilson", "national-id validator", "national_id", "re-id metric", "leakage metric"]),
    ("leaderboard-schema", ["schema 3", "contamination", "config_status"]),
    ("governance-taxonomy", ["taxonomy", "governance"]),
    ("submission-ci", ["submission ci", "no-secrets", "submission protocol", "reproduction gate"]),
    ("external-submissions", ["third-party", "external submission", "presidio", "recruit", "network: recruit", "first external"]),
    ("leaderboard-ux", ["leaderboard ux", "lead with re-id", "leaderboard tables", "pareto visual", "punchy"]),
    ("site-refresh", ["home page", "index.md", "refresh the research"]),
    ("localepack-datasets", ["localepack", "locale-pack", "ds-kp-general", "release_dataset", "synthetic.generate"]),
    ("drift-metric", ["drift metric", "synthetic→real", "synthetic-to-real"]),
    ("kp-deid-model", ["kp-deid-mdeberta", "ship kp-deid", "full kp-deid", "score on ro real-skeleton", "model card"]),
    ("on-device-training", ["mps", "metal", "mac training", "m3 ultra", "mlx", "max-utilization", "pytorch-mps"]),
    ("sdk", ["sdk", "extract_pii", "extract pii"]),
    ("anonymization-track", ["kp-anon", "anonymization", "track c"]),
    ("broaden-reid", ["broaden re-identification", "qi-combination", "name-in-context"]),
    ("paper-protocol", ["prior-art", "first unified", "submission protocol doc", "artifact-evaluation"]),
    ("pareto-figure", ["pareto-frontier figure", "mcnemar", "pareto dissociation"]),
    ("paper-publication", ["arxiv", "zenodo", "citation.cff", "doi"]),
    ("paper-frontmatter", ["front-matter", "7 languages", "language count"]),
    ("ops-enablement", ["enforce https", "actions secrets", "org-level", "ops:"]),
]

# Themes that are program *plumbing* — never surface on the public page even if
# their issue happens to be Done/in-progress.
NEVER_PUBLIC_THEMES: set[str] = set()

# Themes we deliberately keep OUT of the public "up next" list because they are
# internal ops / budget / process, not product progress.
NONPUBLIC_UPNEXT_THEMES = {"ops-enablement", "paper-frontmatter"}


def classify(issue: dict) -> str | None:
    """Map a Linear issue to a public theme key, or None to drop it."""
    title = (issue.get("title") or "").lower()
    for theme_key, keywords in THEME_RULES:
        for kw in keywords:
            if kw in title:
                return theme_key
    return None


# ---------------------------------------------------------------------------
# 2. Public-safety redaction guard.
#
# A final, independent check on the rendered text. Even though the theme
# mapping is an allow-list, the guard is the contract: if any forbidden token
# appears in what we are about to emit, we refuse to emit it.
# ---------------------------------------------------------------------------

FORBIDDEN_PATTERNS: list[tuple[str, re.Pattern]] = [
    # Linear issue identifiers (re-keyed KLU -> RES; block both, plus generic).
    ("linear issue id", re.compile(r"\b(?:KLU|RES|LIN)-\d+\b", re.IGNORECASE)),
    # Internal tooling / process tokens.
    ("internal tooling/process", re.compile(
        r"\b(?:linear|github\s+action|workflow|cron|"
        r"\.ya?ml|\.py|\.json|\.md|"
        r"config_status|schema\s*3|"
        r"mps|mlx|m3\s*ultra|"
        r"branch|secret|token|ci\b)\b",
        re.IGNORECASE,
    )),
    # Unreleased / internal numbers: leak-rate %, F1 scores, CI bounds.
    ("unreleased number (percentage)", re.compile(r"\b\d{1,3}(?:\.\d+)?\s*%")),
    ("unreleased number (F1/CI/decimal metric)", re.compile(
        r"\b(?:entity-)?f1[\s:=]*0?\.\d+|wilson|\b0\.\d{2,}\b",
        re.IGNORECASE,
    )),
    # Internal dataset/model slugs and config track names.
    ("internal slug/config", re.compile(
        r"\b(?:ds-kp-[\w-]+|kp-deid-[\w-]+|[a-z]{2}-realskeleton[\w-]*|legal-realskeleton[\w-]*)\b",
        re.IGNORECASE,
    )),
]


class RedactionError(RuntimeError):
    pass


def public_strings(model: dict) -> list[str]:
    """Every string from the model that is actually rendered on the public page.

    Excludes internal provenance fields (generated_at, source) which are build
    metadata, never shown to readers.
    """
    out: list[str] = []
    for items in model.get("shipped", {}).values():
        out.extend(items)
    out.extend(model.get("in_progress", []))
    out.extend(model.get("up_next", []))
    return out


def assert_public_safe(text: str) -> None:
    """Raise RedactionError if `text` contains anything that must not be public."""
    violations: list[str] = []
    for label, pat in FORBIDDEN_PATTERNS:
        for m in pat.finditer(text):
            violations.append(f"  - {label}: {m.group(0)!r}")
    if violations:
        raise RedactionError(
            "Refusing to emit public status: forbidden content detected:\n"
            + "\n".join(violations)
        )


# ---------------------------------------------------------------------------
# 3. Build the public status model from Linear issues.
# ---------------------------------------------------------------------------

def _theme_blurb(theme_key: str) -> dict:
    t = THEMES[theme_key]
    return {"axis": t["axis"], "text": t["blurb"]}


def build_status(issues: list[dict]) -> dict:
    """Derive the public status model (shipped / in_progress / up_next) from issues."""
    shipped: dict[str, dict] = {}     # theme_key -> blurb (dedup)
    in_progress: dict[str, dict] = {}
    up_next: dict[str, dict] = {}

    for issue in issues:
        st = (issue.get("statusType") or "").lower()
        theme = classify(issue)
        if theme is None or theme in NEVER_PUBLIC_THEMES:
            continue
        if theme not in THEMES:
            continue
        blurb = _theme_blurb(theme)
        if st == "completed":
            shipped.setdefault(theme, blurb)
        elif st == "started":  # In Progress + In Review
            in_progress.setdefault(theme, blurb)
        elif st == "unstarted":  # Todo (next unblocked)
            if theme not in NONPUBLIC_UPNEXT_THEMES:
                up_next.setdefault(theme, blurb)
        # backlog / canceled / duplicate -> not surfaced

    # Group shipped bullets by axis (the way the hand-written roadmap does).
    shipped_by_axis: dict[str, list[str]] = {a: [] for a in AXES}
    for theme, b in shipped.items():
        shipped_by_axis[b["axis"]].append(b["text"])

    return {
        "generated_at": dt.date.today().isoformat(),
        # Generic, public-safe provenance. We deliberately do NOT name the
        # internal tracker or team here, since _data/*.json is build input.
        "source": "Auto-generated from the EuroPriv-Bench program tracker.",
        "shipped": {a: v for a, v in shipped_by_axis.items() if v},
        "in_progress": [b["text"] for b in in_progress.values()],
        "up_next": [b["text"] for b in up_next.values()],
    }


# ---------------------------------------------------------------------------
# 4. Render the public Markdown section.
# ---------------------------------------------------------------------------

SECTION_HEADER = "## Status & updates"


def render_section(model: dict) -> str:
    lines: list[str] = []
    lines.append(SECTION_HEADER)
    lines.append("")
    lines.append(
        f"*Live view — last updated {model['generated_at']}. "
        "The full plan is below; this section tracks what has shipped and what is next, "
        "and is refreshed as work lands.*"
    )
    lines.append("")
    lines.append("**✓ Shipped**")
    for axis in AXES:
        items = model["shipped"].get(axis)
        if not items:
            continue
        joined = "; ".join(items)
        lines.append(f"- **{axis}** — {joined}.")
    if model["in_progress"]:
        lines.append("")
        lines.append("**▶ In progress**")
        for text in model["in_progress"]:
            lines.append(f"- {text[0].upper()}{text[1:]}.")
    if model["up_next"]:
        lines.append("")
        lines.append("**→ Up next**")
        for text in model["up_next"]:
            lines.append(f"- {text[0].upper()}{text[1:]}.")
    lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# 5. Dry-run diff against the live hand-written section.
# ---------------------------------------------------------------------------

def extract_live_section(roadmap_text: str) -> str:
    """Pull the current hand-written '## Status & updates' section from roadmap.md."""
    lines = roadmap_text.splitlines()
    start = None
    for i, ln in enumerate(lines):
        if ln.strip() == SECTION_HEADER:
            start = i
            break
    if start is None:
        return ""
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if lines[j].startswith("## "):
            end = j
            break
    return "\n".join(lines[start:end]).rstrip() + "\n"


# ---------------------------------------------------------------------------
# 6. Self-test: prove the redaction guard rejects each forbidden category.
# ---------------------------------------------------------------------------

def run_self_test() -> int:
    """Prove the redaction guard rejects each forbidden category. Returns 0 if all pass."""
    leaky_samples = [
        ("Linear issue id (RES)", "Shipped RES-61: kp-deid model."),
        ("Linear issue id (KLU, re-keyed)", "Ties to KLU-10 ops work."),
        ("internal tooling", "Generated by the GitHub Action from status.json."),
        ("internal tooling (tracker name)", "Synced from Linear nightly."),
        ("unreleased percentage", "The protector leaks 0% of CNPs."),
        ("unreleased F1 metric", "Best protector at entity-F1 0.74."),
        ("internal slug", "Scored on ro-realskeleton-v1 (config_status=dev)."),
        ("internal slug (model)", "Published kp-deid-mdeberta-280m to the hub."),
    ]
    failures = []
    for label, text in leaky_samples:
        try:
            assert_public_safe(text)
            failures.append(f"  LEAK NOT CAUGHT [{label}]: {text!r}")
        except RedactionError:
            pass  # expected
    # And a known-good string must pass cleanly.
    try:
        assert_public_safe("the first open de-identification protector model is published on the public leaderboard")
    except RedactionError as e:
        failures.append(f"  FALSE POSITIVE on safe text: {e}")
    if failures:
        print("SELF-TEST FAILED:", file=sys.stderr)
        print("\n".join(failures), file=sys.stderr)
        return 1
    print(f"Self-test passed: guard caught all {len(leaky_samples)} leaky samples and "
          "allowed the safe one.", file=sys.stderr)
    return 0


def load_issues(path: str) -> list[dict]:
    raw = sys.stdin.read() if path == "-" else Path(path).read_text(encoding="utf-8")
    data = json.loads(raw)
    if isinstance(data, dict) and "issues" in data:
        return data["issues"]
    if isinstance(data, list):
        return data
    raise ValueError("Expected a Linear issues dump: a list, or an object with an 'issues' key.")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--issues",
                   help="Path to a Linear issues JSON dump, or '-' for stdin.")
    p.add_argument("--self-test", action="store_true",
                   help="Run the redaction-guard self-test (adversarial leaky inputs) and exit.")
    p.add_argument("--emit-json", action="store_true",
                   help=f"Write the proposed status data to {DEFAULT_JSON_OUT.relative_to(REPO_ROOT)}.")
    p.add_argument("--json-out", default=str(DEFAULT_JSON_OUT),
                   help="Override the JSON output path.")
    p.add_argument("--dry-run", action="store_true",
                   help="Diff the generated section against the live hand-written section; do not write roadmap.md.")
    args = p.parse_args(argv)

    if args.self_test:
        return run_self_test()

    if not args.issues:
        p.error("--issues is required (or pass --self-test)")

    issues = load_issues(args.issues)
    model = build_status(issues)
    section = render_section(model)

    # The contract: never emit anything that isn't public-safe. We guard the
    # rendered section AND every public-facing string in the data model (the
    # bullet prose), but not the internal provenance fields (generated_at,
    # source) which are build metadata, never rendered on the page.
    assert_public_safe(section)
    for text in public_strings(model):
        assert_public_safe(text)

    if args.emit_json:
        out = Path(args.json_out)
        out.write_text(json.dumps(model, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"Wrote {out} (public-safe).", file=sys.stderr)

    if args.dry_run:
        import difflib
        live = extract_live_section(ROADMAP.read_text(encoding="utf-8")) if ROADMAP.exists() else ""
        gen = section.rstrip() + "\n"
        diff = difflib.unified_diff(
            live.splitlines(keepends=True),
            gen.splitlines(keepends=True),
            fromfile="roadmap.md (live, hand-written)",
            tofile="generated (proposed)",
        )
        sys.stdout.writelines(diff)
        print(
            "\n[dry-run] Proposed section above. The live roadmap was NOT modified "
            "(propose, don't clobber).",
            file=sys.stderr,
        )
        return 0

    # Default: print the rendered public section to stdout.
    print(section)
    return 0


if __name__ == "__main__":
    sys.exit(main())
