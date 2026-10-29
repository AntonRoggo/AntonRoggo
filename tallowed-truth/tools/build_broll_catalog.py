"""Turn the B-roll scan plus visual tags into the B-roll & overlay library.

  python3 tallowed-truth/tools/build_broll_catalog.py <scan.jsonl> [--sheets <dir>]

Reads tallowed-truth/broll/tags.json ({file id: {"category": ..., "what": ..., "quality": 1-5}}), written by
looking at each clip's thumbnails. Writes tallowed-truth/broll/catalog.csv and README.md. With --sheets, also
writes numbered contact sheets of untagged clips (B-roll videos and images) for the next tagging pass.
"""
import csv
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "broll"
CATEGORIES = {
    "product": "The tin or jar: hero shots, in hand, lid off, texture, swatches",
    "application": "Putting it on: face, neck, hands, under the eyes",
    "skin-result": "Glowing skin, touching the face, mirror checks, smiling close-ups",
    "problem": "Dry, crepey, wrinkled or irritated skin; the 'before'",
    "failed-solutions": "Other creams, serums, drugstore products, the bathroom cabinet",
    "factory": "Inside the TTT facility: making, pouring, filling, machines, the team",
    "ingredients": "Raw honey, tallow, beeswax, olive oil, essential oils",
    "packing-shipping": "Packing orders, boxes, labels, shipping",
    "lifestyle": "Creators posing, routines, outdoors, family, everyday moments",
    "founder": "Ben on camera without talking (walking, working, holding product)",
    "graphic": "Statics, review screenshots, social proof, logos, lander images",
    "other": "Doesn't fit the above",
}


def main(scan, sheets=None):
    recs = [json.loads(l) for l in open(scan) if l.strip()]
    tags_path = OUT / "tags.json"
    tags = json.loads(tags_path.read_text()) if tags_path.exists() else {}
    keep = [r for r in recs if r["kind"] in ("broll", "image")]
    rows = []
    for r in keep:
        t = tags.get(r["id"], {})
        rows.append({
            "id": r["id"], "category": t.get("category", "untagged"), "what": t.get("what", ""),
            "quality": t.get("quality", ""), "kind": "video" if r["kind"] == "broll" else "image",
            "duration": r.get("duration", ""), "orientation": ("vertical" if r.get("height", 0) > r.get("width", 0) else "horizontal") if r.get("width") else "",
            "source": r["source"], "brief": r.get("brief", ""), "creator": r.get("creator", ""),
            "file": r["name"], "path": r["path"], "link": r["link"], "notion": r.get("notion", ""),
        })
    order = list(CATEGORIES) + ["untagged"]
    rows.sort(key=lambda x: (order.index(x["category"]) if x["category"] in order else 99,
                             -(x["quality"] or 0), x["source"]))
    OUT.mkdir(exist_ok=True)
    with open(OUT / "catalog.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows([r for r in rows if r["quality"] != 1])
    counts = {c: sum(1 for r in rows if r["category"] == c and r["quality"] != 1) for c in order}
    talking = sum(1 for r in recs if r["kind"] == "talking")
    errors = sum(1 for r in recs if r["kind"] == "error")
    lines = [f"# B-roll & overlays\n",
             f"Every silent clip (B-roll: no one talking) and image from the TTT asset folder and the creator brief raw "
             f"footage folders, tagged by what it shows. {len(recs)} files scanned: {sum(1 for r in recs if r['kind']=='broll')} "
             f"B-roll clips, {sum(1 for r in recs if r['kind']=='image')} images, {talking} talking takes (not listed), "
             f"{errors} could not be read. Files stay where they are in Drive; `link` opens each one.\n",
             "Quality 1-5 (5 = use first). Quality-1 files (blurry, black, accidental) are left out of the catalog.\n",
             "## Categories\n", "| Category | What's in it | Files |", "|---|---|---|"]
    lines += [f"| `{c}` | {d} | {counts[c]} |" for c, d in CATEGORIES.items()]
    if counts["untagged"]:
        lines.append(f"| `untagged` | Not looked at yet | {counts['untagged']} |")
    for c in CATEGORIES:
        best = [r for r in rows if r["category"] == c and (r["quality"] or 0) >= 4]
        if best:
            lines += [f"\n## Best {c}\n", "| What | Kind | Length | Source | Link |", "|---|---|---|---|---|"]
            lines += [f"| {r['what']} | {r['kind']} | {r['duration']} | {r['source']} | [open]({r['link']}) |" for r in best[:25]]
    lines.append("\nFull list with every file: `catalog.csv`. Rebuild: `python3 tallowed-truth/tools/build_broll_catalog.py <scan.jsonl>`.")
    (OUT / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print({c: n for c, n in counts.items() if n})
    if sheets:
        from PIL import Image, ImageDraw, ImageFont
        todo = [r for r in keep if r["id"] not in tags]
        d = Path(sheets); d.mkdir(parents=True, exist_ok=True)
        font = ImageFont.truetype("/usr/share/fonts/opentype/inter/Inter-Bold.otf", 16)
        thumbs = Path(scan).parent / "thumbs"
        index = {}
        for s in range(0, len(todo), 12):
            sheet = Image.new("RGB", (4 * 3 * 120, 3 * 230), "white")
            dr = ImageDraw.Draw(sheet)
            for i, r in enumerate(todo[s:s + 12]):
                n = s + i
                index[n] = r["id"]
                x, y = (i % 4) * 360, (i // 4) * 230
                for k, name in enumerate((r.get("thumbs") or [])[:3]):
                    p = thumbs / name
                    if p.exists():
                        im = Image.open(p)
                        im.thumbnail((118, 210) if r["kind"] == "broll" else (358, 210))  # one image fills the cell
                        sheet.paste(im, (x + k * 120, y))
                dr.rectangle((x, y, x + 52, y + 20), fill="black")
                dr.text((x + 3, y + 1), str(n), fill="yellow", font=font)
                label = f"{r['kind'][0]} {r.get('duration', '')}s" if r["kind"] == "broll" else "img"
                dr.text((x + 3, y + 211), label + " " + r["source"].split("/ ")[-1][:30], fill="black", font=font)
            sheet.save(d / f"sheet_{s // 12:03d}.jpg", quality=80)
        (d / "index.json").write_text(json.dumps(index))
        print(len(todo), "untagged ->", d)


if __name__ == "__main__":
    a = sys.argv[1:]
    main(a[0], a[a.index("--sheets") + 1] if "--sheets" in a else None)
