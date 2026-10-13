#!/usr/bin/env python3
"""Beat check: did an iteration add or drop beats versus the reference?

Usage: python3 tools/beat_check.py <reference-file> <draft-file> [--hook N]

Splits both scripts into spoken sentences (ignores [VISUAL ...] lines and markdown
headings), matches each draft sentence to its closest reference sentence, and lists:
  ADDED    draft sentences with no close match in the reference (new beats, padding)
  DROPPED  reference sentences with no close match in the draft
  SWAPPED  matched but reworded (shown so swaps are deliberate, not drift)
--hook N skips the first N draft sentences (a new hook the operator asked for).
Exit code 1 if anything was ADDED, so it can gate a delivery.
"""
import re, sys, difflib

def sentences(text):
    out = []
    for line in text.split('\n'):
        s = line.strip()
        if not s or s.startswith('#') or s.startswith('|') or re.match(r'^\[.*\]$', s):
            continue
        s = re.sub(r'\[[^\]]*\]', '', s)
        out += [x.strip() for x in re.split(r'(?<=[.!?])\s+(?=[A-Z"])', s) if len(x.strip()) > 2]
    return out

def norm(s):
    return re.sub(r'[^a-z0-9 ]', '', s.lower())

def main():
    args = sys.argv[1:]
    hook = 0
    if '--hook' in args:
        i = args.index('--hook'); hook = int(args[i + 1]); del args[i:i + 2]
    ref, draft = (sentences(open(p).read()) for p in args[:2])
    draft = draft[hook:]
    used, added, swapped = set(), [], []
    for d in draft:
        best, score = None, 0
        for j, r in enumerate(ref):
            sc = difflib.SequenceMatcher(None, norm(d), norm(r)).ratio()
            if sc > score: best, score = j, sc
        if score < 0.5: added.append(d)
        else:
            used.add(best)
            if score < 0.95: swapped.append((ref[best], d, score))
    dropped = [r for j, r in enumerate(ref) if j not in used]
    print(f'Reference: {len(ref)} sentences. Draft (after hook): {len(draft)} sentences.\n')
    for label, rows in (('ADDED', added), ('DROPPED', dropped)):
        print(f'{label} ({len(rows)})')
        for r in rows: print(f'  + {r}' if label == 'ADDED' else f'  - {r}')
        print()
    print(f'SWAPPED ({len(swapped)})')
    for r, d, sc in swapped: print(f'  ref:   {r}\n  draft: {d}  [{sc:.2f}]\n')
    sys.exit(1 if added else 0)

if __name__ == '__main__':
    main()
