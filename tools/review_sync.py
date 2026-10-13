"""Mirror the review tool's database into git as one Markdown file per video.

  python3 tools/review_sync.py <dump_dir> [--out reviews]

<dump_dir> is where ArtifactData `list` with `out_dir` saved the collections
(<dump_dir>/videos/*.json, <dump_dir>/notes/*.json). Writes reviews/<video id>.md with every
version, what changed, and every note with Claude's reply, so the full feedback history lives
in the repo next to editing-lessons.md. The review tool stays the live inbox; git is the record.
"""
import argparse, datetime, glob, json, os

def load(d, coll):
    out = {}
    for p in sorted(glob.glob(os.path.join(d, coll, "*.json"))):
        with open(p) as f:
            out[os.path.splitext(os.path.basename(p))[0]] = json.load(f)
    return out

def day(ms):
    return datetime.datetime.fromtimestamp(ms / 1000, datetime.timezone.utc).strftime("%Y-%m-%d") if ms else "?"

def tc(t):
    m, s = divmod(float(t or 0), 60)
    return f"{int(m)}:{s:04.1f}"

ap = argparse.ArgumentParser()
ap.add_argument("dump_dir")
ap.add_argument("--out", default="reviews")
a = ap.parse_args()
videos, notes = load(a.dump_dir, "videos"), load(a.dump_dir, "notes")
os.makedirs(a.out, exist_ok=True)
STATE = {"open": "open", "sent": "with Claude", "done": "done", "wontfix": "not changed"}
for vid, v in videos.items():
    title = v.get("groupTitle") or v.get("title") or vid
    lines = [f"# {title} · {v.get('cut', '')}".rstrip(" ·"), ""]
    status = v.get("status", "?")
    if status in ("approved", "posted"):
        status += f" (v{v.get('approvedVersion')}, {day(v.get('approvedAt'))})"
    lines += [f"- Status: {status}", f"- Video id: `{vid}`"]
    for k, label in (("source", "Source footage"), ("recipe", "Recipe"), ("final", "Final file")):
        if v.get(k):
            lines.append(f"- {label}: {v[k]}")
    mine = [dict(n, id=i) for i, n in notes.items() if n.get("video") == vid]
    for ver in v.get("versions", []):
        n = ver.get("n")
        lines += ["", f"## v{n} ({day(ver.get('createdAt'))})", ""]
        if ver.get("changes"):
            lines += [ver["changes"].strip(), ""]
        vn = sorted((x for x in mine if x.get("version") == n), key=lambda x: x.get("t", 0))
        if vn:
            lines.append("Notes:")
            for x in vn:
                text = " ".join(str(x.get("text", "")).split())
                state = STATE.get(x.get("status"), x.get("status"))
                fixed = f", fixed in v{x['fixedIn']}" if x.get("fixedIn") else ""
                lines.append(f"- `{tc(x.get('t'))}` {text} ({state}{fixed})")
                if x.get("reply"):
                    lines.append(f"  - Claude: {' '.join(str(x['reply']).split())}")
                if x.get("lesson"):
                    lines.append(f"  - Lesson: {x['lesson']}")
    with open(os.path.join(a.out, f"{vid}.md"), "w") as f:
        f.write("\n".join(lines).rstrip() + "\n")
    print(os.path.join(a.out, f"{vid}.md"))
