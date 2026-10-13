#!/usr/bin/env python3
"""Pre-push check for ClickUp ad briefs (markdown). Run it before every brief push.

Catches the failures that slipped through before:
  - a character from ANOTHER brief shows up in this one
    (2026-10-10: ChampionsBelt Scene 4 was FrontPageChief's countdown, with Dan and Karen)
  - a speaker who is not in this brief's CAST (warning: minor roles like "Instructor" are fine)
  - a scene number is missing or repeated (ChampionsBelt lost Scene 5)
  - banned mechanism words and em dashes

Usage:
  python3 tools/brief_check.py <brief.md> [more.md ...]
Other briefs in the same folder are used as the cross-check list.
Exit code 1 if any brief has an ERROR.
"""
import glob
import os
import re
import sys

BANNED = ["fluid", "trapped", "pooling", "water retention", "wastewater", "kidney", "edema"]
BANNED_EXACT = ["pool"]  # whole word only, so "pool" flags but "spool" doesn't

LABELS = {"VISUAL", "SOUND", "MUSIC", "PACE", "NOTE", "TITLE CARD", "ON-SCREEN",
          "ON-SCREEN TEXT", "ON-SCREEN GRAPHIC", "CUT TO", "HOLD BODY", "CAST", "Leads",
          "Hold", "Version", "Scene"}
ROLES = {"Coordinator", "Photographer", "Son", "Daughter", "Instructor", "Recruit", "Doctor",
         "Nurse", "Probie", "Classmate", "Dad", "Mom", "Wife", "Husband", "Sister", "Brother",
         "Chief", "Coach", "Sheriff", "Captain", "Sergeant", "Officer", "Lawyer", "Leads", "Hold",
         "Woman", "Man", "Crowd", "Fans", "Old", "Young", "Class", "Ring", "Dads", "Kids",
         "Moms", "Spin", "Restaurant", "Wedding", "Version", "Scene", "City", "Manager", "Yearbook",
         "Guests", "Friends", "Diners", "Squad", "Current", "Alumni", "Front",
         # common words that show up in bold cast labels ("**The alumni squad**", "**Morning crowd**")
         "The", "Her", "His", "She", "They", "Their", "Morning", "Night", "Flight", "Crew", "Passengers", "Parade", "Team", "Church",
         "Neighbors", "School", "Pickup", "Teacher", "Boss", "Coworker", "Parents", "Players", "Teammates", "Staff", "Bar", "Office", "Every", "All"}


def cast_block(text):
    m = re.search(r"\*\*CAST\*\*(.*?)\n\*\*(?:VERSION 1|H1:?)\*\*", text, re.S)
    return m.group(1) if m else ""


def cast_names(text):
    """Every proper name in this brief's cast section (bold labels and plain cast lists)."""
    block = cast_block(text)
    names = set()

    def add(label):
        label = re.sub(r"\(.*?\)", "", label).strip(" :.")
        for part in label.split():
            if re.fullmatch(r"[A-Z][a-z]{2,}", part) and part not in ROLES and part not in LABELS:
                names.add(part)

    # Bold labels: **Celeste Bennett:**, **Dana:**
    for raw in re.findall(r"\*\*([^*]+?)\*\*", block):
        add(raw)
    # Plain cast lists in bullets: "*   Celeste, the coordinator, Tracy." / "**Scene 1:** Rachel (17), Danielle"
    for line in block.splitlines():
        line = re.sub(r"^\s*\*\s+", "", line)
        line = re.sub(r"^\*\*Scene \d+:\*\*", "", line).strip()
        line = re.split(r"\*\*", line)[0]
        for item in line.split(","):
            item = re.sub(r"\(.*?\)", "", item).strip(" .")
            if re.fullmatch(r"[A-Z][a-z]{2,}(?: [a-z ]+)?", item):
                add(item.split()[0])
    return names


def speakers(text):
    body = re.split(r"\*\*(?:VERSION 1|H1:?)\*\*", text, maxsplit=1)[-1]
    out = set()
    for line in body.splitlines():
        m = re.match(r"\*\*([^*]+?)(?:\s*\([^)]*\))?:\*\*", line.strip())
        if m:
            out.add(m.group(1).strip())
    return out


def check(path, text, others):
    errors, warnings = [], []
    own = cast_names(text)
    body = re.split(r"\*\*(?:VERSION 1|H1:?)\*\*", text, maxsplit=1)[-1]

    # 1. Characters from another brief's cast
    for other, names in others.items():
        if other == path:
            continue
        for n in sorted(names - own):
            hits = len(re.findall(r"\b" + re.escape(n) + r"\b", body))
            if hits:
                errors.append(f"'{n}' is a character in {os.path.basename(other)} and appears "
                              f"{hits}x here, but is not in this CAST")

    # 2. Speakers not in this cast (warning)
    for spk in sorted(speakers(text)):
        words = re.findall(r"[A-Z][a-z]+", spk)
        if spk in LABELS or any(w in own or w in ROLES for w in words) or not words:
            continue
        warnings.append(f"speaker not in CAST: {spk}")

    # 3. Scene numbering
    nums = [int(n) for n in re.findall(r"^\*\*Scene (\d+)", text, re.M)]
    if nums:
        missing = sorted(set(range(1, max(nums) + 1)) - set(nums))
        dupes = sorted({n for n in nums if nums.count(n) > 1})
        if missing:
            errors.append(f"missing scene number(s): {missing}")
        if dupes:
            errors.append(f"repeated scene header(s): {dupes}")

    # 4. Banned words and em dashes
    low = text.lower()
    for b in BANNED:
        for m in re.finditer(re.escape(b), low):
            errors.append(f"banned word '{b}' on line {text[:m.start()].count(chr(10)) + 1}")
    for b in BANNED_EXACT:
        for m in re.finditer(r"\b" + b + r"\b", low):
            errors.append(f"banned word '{b}' on line {text[:m.start()].count(chr(10)) + 1}")
    for m in re.finditer("—", text):
        errors.append(f"em dash on line {text[:m.start()].count(chr(10)) + 1}")

    status = "OK" if not errors else f"{len(errors)} ERROR(S)"
    print(f"== {os.path.basename(path)}: {status}" + (f", {len(warnings)} warning(s)" if warnings else ""))
    for e in errors:
        print("   ERROR  ", e)
    for w in warnings:
        print("   warn   ", w)
    return not errors


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    paths = [os.path.abspath(p) for p in argv]
    others = {}
    for d in {os.path.dirname(p) for p in paths}:
        for f in glob.glob(os.path.join(d, "*.md")):
            others[os.path.abspath(f)] = cast_names(open(f, encoding="utf-8").read())
    ok = True
    for p in paths:
        ok &= check(p, open(p, encoding="utf-8").read(), others)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
