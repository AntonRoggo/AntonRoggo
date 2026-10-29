"""Export the story library as one spreadsheet for people (Google Drive / Excel).

  python3 tallowed-truth/tools/export_sheet.py output/TTT-Story-Library.xlsx

Tabs: How to use, Top 100, one tab per theme (best 40), Authority screenshots, Result screenshots,
Photos. Built from reviews/reviews.csv and testimonials/*.csv, so re-run after rebuilding those.
"""
import csv, os, sys
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill

csv.field_size_limit(10**9)
HERE = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, os.path.dirname(__file__))
from build_reviews import THEMES

def load(p):
    return list(csv.DictReader(open(os.path.join(HERE, p), encoding="utf-8")))

def tab(wb, title, header, rows, widths):
    ws = wb.create_sheet(title[:31])
    ws.append(header)
    for c in ws[1]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="3C8274")
    for r in rows:
        ws.append(r)
    for i, w in enumerate(widths):
        ws.column_dimensions[chr(65 + i)].width = w
    for row in ws.iter_rows(min_row=2):
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.freeze_panes = "A2"

def main(out):
    reviews = load("reviews/reviews.csv")
    pos = [r for r in reviews if r["rating"] in ("4", "5")]
    H = ["Review id", "Score", "Name", "Stars", "Product", "Date", "Age", "How fast", "Themes", "Review (word for word)", "Photo"]
    W = [12, 7, 14, 6, 22, 11, 6, 16, 28, 90, 12]
    def row(r):
        return [r["id"], int(r["story_score"]), r["name"], int(r["rating"]), r["product"], r["date"],
                r["age"], r["timeline"], r["themes"], r["body"], "yes" if r["photos"] else ""]
    wb = Workbook()
    ws = wb.active
    ws.title = "How to use"
    for line in [
        "TTT Story Library: the best customer stories, ready for scripts and pop-ups.",
        f"Built from all {len(reviews):,} Judge.me reviews. Score = how good a story it makes (before/after, age, how fast, who noticed, photo).",
        "Top 100 = best overall. Each theme tab = best 40 on that theme. Screenshots and Photos tabs = files already in Dropbox.",
        "Quote reviews word for word. Never change a number or tidy the wording.",
        "Need a review on screen that has no screenshot? Ask the TTT Brain in Claude for a review card with its id.",
        "Comments tabs = relevant comments under our Facebook ads (no names). Use them for hooks and objection lines, not as on-screen testimonials.",
        "Source of truth is the TTT brain repo; this sheet is a copy, regenerated when reviews are refreshed.",
    ]:
        ws.append([line])
    ws.column_dimensions["A"].width = 140
    tab(wb, "Top 100", H, [row(r) for r in pos[:100]], W)
    for key, (label, _) in THEMES.items():
        if key == "service":
            continue
        best = [r for r in pos if key in r["themes"].split()][:40]
        tab(wb, key.replace("-", " ").title(), H, [row(r) for r in best], W)
    shots = load("testimonials/screenshots.csv")
    SH = ["Who noticed", "Name", "Claim", "Review id", "Stars", "Product", "Full review", "Dropbox file"]
    SW = [16, 14, 40, 12, 6, 22, 80, 60]
    tab(wb, "Screenshots - authority", SH, [[s["authority"], s["name"], s["claim"], s["review_id"], s["rating"],
        s["product"], s["review"], s["dropbox_path"]] for s in shots if s["category"] == "authority"], SW)
    tab(wb, "Screenshots - results", SH, [["", s["name"], s["claim"], s["review_id"], s["rating"],
        s["product"], s["review"], s["dropbox_path"]] for s in shots if s["category"] != "authority"], SW)
    photos = load("testimonials/photos.csv")
    tab(wb, "Photos", ["Kind", "What", "Review id", "Name", "Stars", "Review", "Source", "Used in ads", "Dropbox file"],
        [[p["kind"], p["description"], p["review_id"], p["name"], p["rating"], p["review"], p["source"],
          p["used_in_ads"], p["dropbox_path"]] for p in photos], [16, 40, 12, 14, 6, 70, 30, 12, 60])
    rel = os.path.join(HERE, "comments", "relevant.csv")
    if os.path.exists(rel):
        com = list(csv.DictReader(open(rel, encoding="utf-8")))
        for sec in ["Customer results", "Doubts answered by customers", "Real objections", "Questions before buying"]:
            tab(wb, "Comments - " + sec.split()[0].lower() if sec != "Doubts answered by customers" else "Comments - doubts answered",
                ["Comment (word for word)", "Likes", "Date", "Objection", "How TTT answered"],
                [[c["comment"], int(c["likes"]), c["date"], c["objections"], c["ttt_answer"]] for c in com if c["section"] == sec],
                [90, 7, 11, 24, 60])
    wb.save(out)
    print(out, os.path.getsize(out) // 1024, "KB")

if __name__ == "__main__":
    main(sys.argv[1])
