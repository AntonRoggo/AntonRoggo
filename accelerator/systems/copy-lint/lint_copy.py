#!/usr/bin/env python3
"""copy-lint: enforce the machine-checkable rules from brand/voice.md on files in copy/.

Hard fail (exit 2): em dashes. The Script bans them everywhere.
Warnings (exit 0, reported): en dashes, oxford triplets (AI tell), vague pronoun openers.
Taste rules (hedged claims, show-don't-summarize) stay human. A linter cannot read taste.

Modes:
  lint_copy.py <file>    lint one file, human-readable report
  lint_copy.py --hook    read Claude Code PostToolUse JSON on stdin, lint only files under copy/
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
COPY_DIR = (ROOT / "copy").resolve()

EM_DASH = "—"
EN_DASH = "–"
HORIZ_BAR = "―"

TRIPLET = re.compile(r"\b[\w'’-]+, [\w'’-]+,? (?:and|or) [\w'’-]+\b")
VAGUE_OPEN = re.compile(
    r"(?:^|[.!?]\s+)(It|This|That)\s+"
    r"(?:is|was|means|makes|helps|works|does|has|will|can|feels|sounds|gets|keeps|takes|turns|seems)\b"
)


def lint(path: Path):
    fails, warns = [], []
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return fails, warns
    for n, line in enumerate(text.splitlines(), 1):
        if EM_DASH in line or HORIZ_BAR in line:
            fails.append(f"line {n}: em dash. Banned everywhere. Use a comma, a period, or a colon: {line.strip()[:80]}")
        if EN_DASH in line:
            warns.append(f"line {n}: en dash, usually an em dash in disguise: {line.strip()[:80]}")
        m = TRIPLET.search(line)
        if m:
            warns.append(f"line {n}: triplet '{m.group(0)}'. AI tell. Doublet is the default; a survivor earns its own line.")
        m = VAGUE_OPEN.search(line)
        if m:
            warns.append(f"line {n}: sentence opens on vague '{m.group(1)}'. Name the actual noun.")
    return fails, warns


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--hook":
        try:
            payload = json.load(sys.stdin)
        except json.JSONDecodeError:
            return 0
        fp = (payload.get("tool_input") or {}).get("file_path") or (payload.get("tool_response") or {}).get("filePath")
        if not fp:
            return 0
        path = Path(fp).resolve()
        try:
            path.relative_to(COPY_DIR)
        except ValueError:
            return 0  # not headed for copy/, not our jurisdiction
        if not path.exists():
            return 0
        fails, warns = lint(path)
        if fails:
            print(f"copy-lint FAILED on {path.name} ({len(fails)} violations). Fix before this ships:", file=sys.stderr)
            for f in fails:
                print(f"  {f}", file=sys.stderr)
            for w in warns:
                print(f"  warning, {w}", file=sys.stderr)
            return 2
        if warns:
            ctx = f"copy-lint warnings on {path.name} (review, not blockers):\n" + "\n".join(f"  {w}" for w in warns)
            print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": ctx}}))
        return 0

    # direct mode
    if len(sys.argv) < 2:
        print("usage: lint_copy.py <file> | --hook", file=sys.stderr)
        return 1
    path = Path(sys.argv[1]).resolve()
    if not path.exists():
        print(f"no such file: {path}", file=sys.stderr)
        return 1
    fails, warns = lint(path)
    for f in fails:
        print(f"FAIL  {f}")
    for w in warns:
        print(f"warn  {w}")
    if not fails and not warns:
        print(f"clean: {path.name}")
    return 2 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
