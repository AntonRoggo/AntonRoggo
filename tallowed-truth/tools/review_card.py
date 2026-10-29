"""Render a review as a pop-up card in the same style as the website's Judge.me reviews
(teal stars, dark grey Inter text on white), so any review can go on screen without a screenshot.

  python3 tallowed-truth/tools/review_card.py r-b072bac3 [r-... ...] [--name] [--max-chars 420] [--out output/cards]
  python3 tallowed-truth/tools/review_card.py "r-07671545@And here’s the best part"   # start at that sentence
  python3 tallowed-truth/tools/review_card.py --comment "text" --out x.png             # a Facebook comment

--name adds "Sandi M." under the text. Long reviews are cut at the last full
sentence under --max-chars and end with "..."; never edit the words themselves.
"id@words" starts the card at the sentence holding those words (shown as "... " first), for when the
payoff sits in the middle of a long review.
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

EMOJI = re.compile("[\U0001F000-\U0001FAFF\u2600-\u27BF\uFE0F\u200D]")

def trim(text, limit):
    text = re.sub(r"\s+", " ", EMOJI.sub("", text)).strip()  # Inter has no emoji; they'd print as boxes
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

def excerpt(text, words):
    """The review from the start of the sentence holding `words`, with "... " in front."""
    text = re.sub(r"\s+", " ", text).strip()
    i = text.find(words)
    if i < 0:
        raise SystemExit(f"not in the review: {words}")
    start = max(text.rfind(". ", 0, i), text.rfind("! ", 0, i), text.rfind("? ", 0, i))
    return "... " + text[start + 2 if start >= 0 else 0:]

def card(review, show_name, limit, start=None):
    font, bold = ImageFont.truetype(FONT, SIZE), ImageFont.truetype(FONT_BOLD, SIZE - 6)
    probe = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    body = excerpt(review["body"], start) if start else review["body"]
    lines = wrap(probe, trim(body, limit), font, W - 2 * PAD)
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

def comment_card(text, label="Comment on our Facebook ad"):
    """A Facebook-style comment bubble: grey rounded box, small bold label, the comment word for word."""
    font, bold = ImageFont.truetype(FONT, SIZE), ImageFont.truetype(FONT_BOLD, SIZE - 8)
    probe = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    lines = wrap(probe, re.sub(r"\s+", " ", EMOJI.sub("", text)).strip(), font, W - 2 * PAD)
    lh = int(SIZE * LEAD)
    h = PAD + 40 + 16 + lh * len(lines) + PAD - 10
    im = Image.new("RGBA", (W, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, W - 1, h - 1), radius=36, fill=(240, 242, 245))
    d.text((PAD, PAD - 4), label, font=bold, fill=(5, 5, 5))
    y = PAD + 40 + 16
    for ln in lines:
        d.text((PAD, y), ln, font=font, fill=(5, 5, 5))
        y += lh
    return im

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ids", nargs="*")
    ap.add_argument("--comment", help="render this Facebook comment instead of a review (--out is the .png path)")
    ap.add_argument("--name", action="store_true")
    ap.add_argument("--max-chars", type=int, default=420)
    ap.add_argument("--out", default="output/cards")
    a = ap.parse_args()
    if a.comment:
        comment_card(a.comment).save(a.out)
        print(a.out)
        return
    starts = {i.split("@", 1)[0]: (i.split("@", 1)[1] if "@" in i else None) for i in a.ids}
    want = set(starts)
    os.makedirs(a.out, exist_ok=True)
    for r in csv.DictReader(open(os.path.join(HERE, "..", "reviews", "reviews.csv"), encoding="utf-8")):
        if r["id"] in want:
            path = os.path.join(a.out, r["id"] + ".png")
            card(r, a.name, a.max_chars, starts[r["id"]]).save(path)
            print(path)
            want.discard(r["id"])
    for missing in want:
        print("not found:", missing)

if __name__ == "__main__":
    main()
