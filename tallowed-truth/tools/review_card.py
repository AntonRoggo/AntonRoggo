"""Render a review as a pop-up card in the same style as the website's Judge.me reviews
(teal stars, dark grey Inter text on white), so any review can go on screen without a screenshot.

  python3 tallowed-truth/tools/review_card.py r-b072bac3 [r-... ...] [--name] [--max-chars 420] [--out output/cards]

--name adds "Sandi M." under the text. Long reviews are cut at the last full
sentence under --max-chars and end with "..."; never edit the words themselves.
Writes <out>/<id>.png (transparent outside a rounded white card, 1080 px wide for 9:16 video).
"""
import argparse, csv, math, os, re
from PIL import Image, ImageDraw, ImageFont

csv.field_size_limit(10**9)
HERE = os.path.dirname(__file__)
TEAL, TEXT, GREY = (60, 130, 116), (51, 51, 51), (120, 120, 120)
FONT = "/usr/share/fonts/opentype/inter/Inter-Regular.otf"
FONT_BOLD = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"
W, PAD, SIZE, LEAD = 1000, 48, 38, 1.5

def star(d, cx, cy, r, fill):
    pts = []
    for i in range(10):
        a = math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(a), cy - rr * math.sin(a)))
    d.polygon(pts, fill=fill)

def trim(text, limit):
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= limit:
        return text
    cut = text[:limit]
    end = max(cut.rfind(". "), cut.rfind("! "), cut.rfind("? "))
    return (cut[:end + 1] if end > limit * 0.5 else cut.rsplit(" ", 1)[0]) + " ..."

def wrap(d, text, font, width):
    lines, line = [], ""
    for word in text.split(" "):
        test = (line + " " + word).strip()
        if d.textlength(test, font=font) <= width:
            line = test
        else:
            lines.append(line)
            line = word
    return lines + [line]

def card(review, show_name, limit):
    font, bold = ImageFont.truetype(FONT, SIZE), ImageFont.truetype(FONT_BOLD, SIZE - 6)
    probe = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    lines = wrap(probe, trim(review["body"], limit), font, W - 2 * PAD)
    lh = int(SIZE * LEAD)
    h = PAD + 44 + 30 + lh * len(lines) + (lh + 10 if show_name else 0) + PAD - 10
    im = Image.new("RGBA", (W, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, W - 1, h - 1), radius=28, fill="white")
    for i in range(int(review["rating"] or 5)):
        star(d, PAD + 22 + i * 52, PAD + 22, 24, TEAL)
    y = PAD + 44 + 30
    for ln in lines:
        d.text((PAD, y), ln, font=font, fill=TEXT)
        y += lh
    if show_name:
        d.text((PAD, y + 10), f"{review['name']}", font=bold, fill=GREY)
    return im

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ids", nargs="+")
    ap.add_argument("--name", action="store_true")
    ap.add_argument("--max-chars", type=int, default=420)
    ap.add_argument("--out", default="output/cards")
    a = ap.parse_args()
    want = set(a.ids)
    os.makedirs(a.out, exist_ok=True)
    for r in csv.DictReader(open(os.path.join(HERE, "..", "reviews", "reviews.csv"), encoding="utf-8")):
        if r["id"] in want:
            path = os.path.join(a.out, r["id"] + ".png")
            card(r, a.name, a.max_chars).save(path)
            print(path)
            want.discard(r["id"])
    for missing in want:
        print("not found:", missing)

if __name__ == "__main__":
    main()
