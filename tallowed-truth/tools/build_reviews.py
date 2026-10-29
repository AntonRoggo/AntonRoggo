"""Build the review & story library from a Judge.me export.

  python3 tallowed-truth/tools/build_reviews.py input/ttt/judgeme_reviews.csv

Writes (all inside tallowed-truth/reviews/):
  reviews.csv          every review, no emails/IPs, tagged with themes, age, time-to-result, story score
  stories/<theme>.md   the best stories for each theme, ready to quote or pop up on screen
  top-stories.md       the 100 best stories overall
  objections.md        what 1-3 star reviewers complain about (for objection hooks)
  README.md            counts per product and theme

Re-run on a fresh export whenever new reviews come in; it rebuilds everything.
"""
import csv, re, sys, collections, os

csv.field_size_limit(10**9)
OUT = os.path.join(os.path.dirname(__file__), "..", "reviews")

PRODUCTS = [  # (handle substring, product name); first match wins
    ("black-label", "F-Balm Black Label (unscented)"), ("orange-vanilla", "F-Balm Orange Vanilla"),
    ("lavender", "F-Balm Lavender"), ("f-balmer", "F-Balmer lip balm"), ("lip-balm", "F-Balmer lip balm"),
    ("whipped-body-butter", "F-Balm Whipped Body Butter"), ("bee-free", "Bee-Free Vanilla Body Butter"),
    ("body-butter", "F-Balm Whipped Body Butter"), ("face-whip", "Freedom Face Whip"),
    ("field-balm", "Freedom Field Balm (bug balm)"), ("s-balm", "S-Balm zinc sun lotion"),
    ("soap", "Tallow soap bar"), ("bar-3-pack", "Tallow soap bar"), ("calm-balm", "Calm Balm (magnesium)"),
    ("gift", "Free gift"), ("bundle", "Bundle"), ("starter-pack", "Bundle"), ("shipping", "Shipping"), ("hat", "Merch"),
    ("snap", "Merch"), ("gift-card", "Gift card"), ("f-balm", "F-Balm (original)"),
]

def product(handle):
    if not handle:
        return "Store review"
    for key, name in PRODUCTS:
        if key in handle:
            return name
    return handle

# theme: (label, regex). Matched case-insensitively against the review body.
THEMES = {
    "wrinkles":       ("Wrinkles, fine lines, smoker's lines", r"wrinkl|fine lines?|crow'?s feet|smoker'?s? lines|laugh lines|forehead lines|lines (around|on) my|lines are|deep lines|mouth lines|lip lines"),
    "crepey-neck":    ("Crepey skin, neck, sagging, firmness", r"crep[ey]|neck|jowl|sagg|firm(er|ness)?\b|elasticity|plump"),
    "dry-skin":       ("Dry, flaky, tight skin", r"\bdry\b|dryness|flak(y|ing)|dehydrat|tight skin|parched"),
    "eczema":         ("Eczema, psoriasis, dermatitis, rosacea, rashes", r"eczema|psoria|dermatitis|rosacea|\brash|hives|seborr"),
    "acne":           ("Acne, breakouts, clogged pores", r"\bacne|break ?outs?|pimple|blemish|clog|cystic|zits?\b|pores"),
    "spots-tone":     ("Age spots, dark spots, redness, even tone", r"age spots?|dark spots?|sun spots?|pigment|discolou?r|redness|skin tone|even tone|liver spots?|melasma"),
    "scars-healing":  ("Scars, burns, cuts, wounds, healing", r"\bscars?\b|scarring|\bburns?\b|wound|stitch|surgery|incision|\bhealed\b|healing"),
    "hands-feet":     ("Cracked hands, heels, feet", r"cracked|cracking|split(ting)? (skin|fingers)|knuckle|cuticle|heels|\bfeet\b|my hands"),
    "compliments":    ("People noticed / compliments / glow", r"compliment|people (keep )?ask|asked (me )?what|asking (me )?what|noticed|glow|radiant|look(s|ing)? younger|carded|younger than"),
    "authority":      ("A professional noticed (derm, esthetician, nurse, doctor, stylist)", r"dermatolog|esthetician|aesthetician|\bnurse|\bdoctor|\bdr\.? |physician|surgeon|hair ?stylist|hairdresser|makeup artist|pharmacist|facialist|nail tech|physio"),
    "replaced-expensive": ("Replaced expensive creams, Botox, retinol", r"expensive|botox|retinol|retin-a|la mer|clinique|estee|lanc[oô]me|olay|filler|\$\d{3}|hundreds of dollars|threw (out|away)|tossed|replaced (all|every)|got rid of"),
    "menopause":      ("Menopause, hormones, over 50 skin", r"menopaus|hormon|post-?meno|peri-?meno"),
    "sensitive":      ("Sensitive / reactive skin", r"sensitive|react(s|ion|ive)|allerg|irritat|burns? when|sting"),
    "kids-baby":      ("Babies, kids, family", r"\bbaby|babies|toddler|my (son|daughter|kids?|grand(son|daughter|kids?|children))|diaper|cradle cap|newborn"),
    "men":            ("Men using it (husband, dad, son)", r"husband|my (dad|father|boyfriend)|\bhe (uses|loves|said)|my man\b|\bmen\b|beard|shav"),
    "skeptic":        ("Skeptic first: beef fat, weird, hesitant", r"skeptic|sceptic|hesitant|beef fat|weird|gross|unsure|doubt|wasn'?t sure|didn'?t think|had my doubts|reluctant"),
    "scent-texture":  ("Smell, texture, not greasy, absorbs", r"smell|scent|greas|absorb|soaks? in|texture|whipped|melts"),
    "bugs":           ("Bug repellent (Field Balm)", r"mosquito|bugs?\b|black ?fl(y|ies)|ticks?\b|deet|no-?see-?ums|bites?\b"),
    "sun":            ("Sun, sunburn, SPF", r"sunburn|sun ?screen|spf|\bzinc|sun lotion|tan\b"),
    "lips":           ("Lips, chapped lips", r"\blips?\b|chapped"),
    "service":        ("Customer service, shipping, company, values", r"customer service|shipping|delivery|arrived|ben\b|canadian|freedom|convoy|company|support"),
    "repeat-buyer":   ("Repeat buyer, stocking up, subscribed", r"re-?order|ordered (again|more)|(second|third|fourth|fifth|2nd|3rd|4th|5th) (tin|order|jar|purchase)|stock(ed|ing)? up|subscri|buying more|will buy again|never (go back|use anything else)"),
}
THEME_RE = {k: re.compile(v, re.I) for k, (_, v) in THEMES.items()}

AGE_RE = re.compile(r"\b(?:i'?m|i am|at|age|aged|turn(?:ed|ing)?|turning)\s+(\d{2})\b|\b(\d{2})[- ]?(?:years?|yrs?)[- ]old\b|\bin my (\d0)s\b|\b(\d0)s\b", re.I)
TIME_RE = re.compile(r"\b(?:in|after|within|only|just)\s+(?:a|one|two|three|four|five|six|a few|a couple(?: of)?|\d+)\s+(?:days?|weeks?|months?|nights?|uses|applications)\b|\bovernight\b|\bfirst (?:use|night|application)\b", re.I)
BEFORE_RE = re.compile(r"tried everything|nothing (else )?(worked|helped)|for years|my whole life|all my life|struggled|suffer|doctor prescribed|steroid|cortisone|desperate", re.I)
AFTER_RE = re.compile(r"\bgone\b|disappear|cleared|vanish|no longer|healed|transform|life ?chang|game ?changer|holy grail|miracle|can'?t believe|amazed|shocked|blown away|night and day|difference", re.I)
GENERIC_RE = re.compile(r"^(great|good|love|loved|awesome|excellent|amazing|nice|perfect|best)( product| stuff| balm| cream)?[.! ]*$", re.I)

def age_of(text):
    for m in AGE_RE.finditer(text):
        g = next(x for x in m.groups() if x)
        n = int(g)
        if 25 <= n <= 99:
            return n
    return ""

def review_id(handle):
    """r-<first 8 of the Judge.me uuid> (the same 8 characters are in the testimonial photo names);
    Shop app reviews get s-<last 8>."""
    if handle.startswith("review-"):
        return "r-" + handle[7:15]
    return "s-" + handle[-8:]

def short_name(name):
    parts = re.sub(r"[^\w\s-]", " ", name).split()
    if not parts:
        return "Anonymous"
    first = parts[0].capitalize()
    return f"{first} {parts[-1][0].upper()}." if len(parts) > 1 else first

def region(loc):
    parts = [p.strip() for p in loc.split(",") if p.strip()]
    return ", ".join(parts[-2:]) if parts else ""

def score(row, themes, age, timeline):
    """How good is this review as a story for an ad (0-100). Specific, emotional, credible beats long."""
    body = row["body"]
    s = min(len(body), 700) / 700 * 30                     # enough words to tell a story
    s += {"5": 15, "4": 8}.get(row["rating"], 0)
    s += 10 if age else 0
    s += 8 if timeline else 0
    s += 10 if BEFORE_RE.search(body) else 0
    s += 8 if AFTER_RE.search(body) else 0
    s += 10 if "authority" in themes else 0
    s += 6 if "compliments" in themes else 0
    s += 5 if row["picture_urls"] else 0
    problem = {"wrinkles", "crepey-neck", "dry-skin", "eczema", "acne", "spots-tone", "scars-healing", "hands-feet"}
    s += min(len(problem & set(themes)), 2) * 4
    if GENERIC_RE.match(body.strip()):
        s = min(s, 5)
    return round(min(s, 100))

def main(src):
    rows = list(csv.DictReader(open(src, encoding="utf-8-sig")))
    out = []
    for r in rows:
        body = re.sub(r"\s+\n", "\n", r["body"]).strip()
        if not body:
            continue
        themes = [k for k, rx in THEME_RE.items() if rx.search(body)]
        age = age_of(body)
        tm = TIME_RE.search(body)
        timeline = tm.group(0) if tm else ""
        out.append({
            "id": review_id(r["metaobject_handle"]),
            "date": r["review_date"][:10],
            "rating": r["rating"],
            "product": product(r["product_handle"]),
            "name": short_name(r["reviewer_name"]),
            "region": region(r["location"]),
            "age": age,
            "timeline": timeline,
            "themes": " ".join(themes),
            "story_score": score(r, themes, age, timeline),
            "photos": r["picture_urls"].replace(", ", " "),
            "verified_source": r["source"],
            "body": body,
            "our_reply": r["reply"].strip(),
        })
    out.sort(key=lambda x: (-x["story_score"], x["date"]))
    os.makedirs(os.path.join(OUT, "stories"), exist_ok=True)
    with open(os.path.join(OUT, "reviews.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys()))
        w.writeheader()
        w.writerows(out)

    def card(x):
        bits = [f"**{x['name']}**", f"{x['rating']}★", x["product"], x["date"]]
        if x["region"]: bits.append(x["region"])
        if x["age"]: bits.append(f"age {x['age']}")
        if x["timeline"]: bits.append(f"result: \"{x['timeline']}\"")
        if x["photos"]: bits.append("has photo")
        quote = x["body"].replace("\n", " ")
        return (f"### {x['id']} · score {x['story_score']}\n" + " · ".join(bits) +
                f"\nThemes: {x['themes']}\n\n> {quote}\n")

    positive = [x for x in out if x["rating"] in ("4", "5")]
    for key, (label, _) in THEMES.items():
        if key == "service":
            continue
        best = [x for x in positive if key in x["themes"].split()][:40]
        with open(os.path.join(OUT, "stories", f"{key}.md"), "w", encoding="utf-8") as f:
            f.write(f"# Best review stories: {label}\n\n"
                    f"Top {len(best)} of {sum(key in x['themes'].split() for x in positive)} positive reviews on this theme, "
                    "best story first. Quote word for word; never fix spelling or make a review spicier. "
                    "Full text and every other review: `reviews/reviews.csv` (search by id).\n\n")
            f.write("\n".join(card(x) for x in best))

    with open(os.path.join(OUT, "top-stories.md"), "w", encoding="utf-8") as f:
        f.write("# Top 100 review stories (all themes)\n\nThe strongest stories across every product: specific, "
                "with a before and after, an age, a timeline or someone who noticed. Start here for ad ideas.\n\n")
        f.write("\n".join(card(x) for x in positive[:100]))

    neg = [x for x in out if x["rating"] in ("1", "2", "3")]
    OBJ = {
        "Greasy / heavy / oily": r"greas|oily|heavy|shiny|sticky",
        "Smell (beefy, too strong, didn't like scent)": r"smell|scent|odou?r|stink|beef",
        "Broke me out / clogged pores": r"break ?out|broke (me )?out|pimple|acne|clog|bumps",
        "Didn't see a difference": r"no difference|didn'?t (see|notice)|not (much|any) (of a )?difference|nothing changed|didn'?t work|not work",
        "Irritation / reaction / rash": r"rash|itch|irritat|react|burn|red",
        "Price / small tin": r"price|expensive|cost|small|tiny|size",
        "Texture (grainy, hard, melted)": r"grain|gritty|hard|melt|texture|lump",
        "Shipping / order problems": r"shipping|deliver|arriv|late|order|customs|lost|missing|damaged|leak",
    }
    with open(os.path.join(OUT, "objections.md"), "w", encoding="utf-8") as f:
        f.write(f"# Objections: what unhappy customers say\n\n{len(neg)} reviews rated 1-3 stars out of {len(out)}. "
                "Use these to write objection-handling lines (\"I thought it would be greasy...\") and to know what "
                "NOT to promise. Five examples per objection, most detailed first.\n\n")
        for label, rx in OBJ.items():
            hits = [x for x in neg if re.search(rx, x["body"], re.I)]
            hits.sort(key=lambda x: -len(x["body"]))
            f.write(f"## {label} ({len(hits)} reviews)\n\n")
            for x in hits[:5]:
                f.write(f"- {x['rating']}★ {x['product']}, {x['id']}: \"{x['body'][:400].replace(chr(10), ' ')}\"\n")
            f.write("\n")

    prod = collections.Counter(x["product"] for x in out)
    stars = collections.Counter(x["rating"] for x in out)
    with open(os.path.join(OUT, "README.md"), "w", encoding="utf-8") as f:
        f.write(f"""# Reviews & stories

Every published Judge.me review ({len(out)} with text, {out[-1]['date'] if False else min(x['date'] for x in out)} to {max(x['date'] for x in out)}), cleaned and tagged so Claude can find the right story fast. Emails and IP addresses are removed; names are shown as the website shows them (first name, last initial).

Rebuild after a new export: `python3 tallowed-truth/tools/build_reviews.py <export.csv>`.

## Files

| File | Use it for |
|---|---|
| `top-stories.md` | The 100 best stories overall. Start here for ad ideas. |
| `stories/<theme>.md` | The 40 best stories per theme (wrinkles, crepey neck, eczema...). |
| `objections.md` | What 1-3 star reviewers say: objection hooks, and what not to promise. |
| `reviews.csv` | Every review. Columns: id, date, rating, product, name, region, age, timeline, themes, story_score, photos, verified_source, body, our_reply. |

`story_score` (0-100) ranks how well a review works as an ad story: a real before and after, an age, how fast it worked, someone who noticed (especially a professional), a photo. Long and generic scores low.

`id` is `r-` plus the first 8 characters of the Judge.me review id. Testimonial photos in Dropbox are named `<date>_<name>_<same 8 characters>_<n>.jpg`, so a photo and its review share the id.

## Stars

{chr(10).join(f"- {k}★: {v}" for k, v in sorted(stars.items(), reverse=True))}

## Reviews per product

{chr(10).join(f"- {k}: {v}" for k, v in prod.most_common())}

## Themes

| Theme | File | Positive reviews |
|---|---|---|
{chr(10).join(f"| {label} | `stories/{k}.md` | {sum(k in x['themes'].split() for x in positive)} |" for k, (label, _) in THEMES.items() if k != "service")}
""")
    print(len(out), "reviews written")

if __name__ == "__main__":
    main(sys.argv[1])
