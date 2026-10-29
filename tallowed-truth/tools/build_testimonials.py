"""Catalogue the testimonial photos and review screenshots in Dropbox and link them to their reviews.

  python3 tallowed-truth/tools/build_testimonials.py <pics_dir> <screenshots_dir>

The dirs are local copies of the Dropbox folders (download each shared folder as a zip). Visual tags
for the photos live in PHOTO_TAGS below (filled in by looking at every photo); add a line when new
photos are added. Writes tallowed-truth/testimonials/photos.csv, screenshots.csv and README.md.
"""
import csv, os, re, sys, unicodedata

csv.field_size_limit(10**9)
HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, "..", "testimonials")
REVIEWS = os.path.join(HERE, "..", "reviews", "reviews.csv")
PICS_DROPBOX = "/[01] Clients/The Tallowed Truth/Testimonial Pics/"
TEXT_DROPBOX = "/[01] Clients/The Tallowed Truth/Testimonial Text/"

# kind: before-after | problem-closeup | product-in-hand | face-selfie | lifestyle | not-usable
# Ages are guesses from the photo, only to help pick a match for the creator's audience.
PHOTO_TAGS = {
    "04rCKXT5D_mid.jpg": ("face-selfie", "50s, no makeup, close-up, natural light"),
    "2026-04-16_victoria-golubenko_6d57981e_0.jpg": ("face-selfie", "40s, glasses, short dark hair"),
    "2026-04-21_alli-l-thesolotravler50_d8ffa219_0.jpg": ("lifestyle", "40s-50s, outdoors with a toddler"),
    "2026-04-27_jeri-lee-hogan_812c4f24_0.jpg": ("face-selfie", "50s, close-up, wearing scrubs"),
    "2026-04-29_lisa-nicholls_5f40db1b_0.jpg": ("product-in-hand", "60s-70s, holding the S-Balm tin"),
    "2026-04-29_murray-mashford_8e034961_0.jpg": ("lifestyle", "man 60s, outdoors feeding ducks"),
    "2026-04-30_leanne-fisher_5087ebb4_0.jpg": ("face-selfie", "50s, glasses"),
    "2026-05-05_sandi-melkonian_b072bac3_0.jpg": ("lifestyle", "Sandi, 70, hugging her high-school friend (the plastic surgeon story)"),
    "2026-05-08_linda-yelinek_6b0225cb_0.jpg": ("lifestyle", "50s, glowing skin, at a table"),
    "2026-05-15_cecilia-a-davis_c5eb79e3_0.png": ("not-usable", "screenshot of an AI watercolour portrait"),
    "2026-05-19_billie-elder_cc481388_0.jpg": ("face-selfie", "40s-50s, curly hair, sunlit glow"),
    "2026-05-19_billie-elder_f7264981_0.jpg": ("face-selfie", "40s-50s, curly hair"),
    "2026-05-20_sandra-michelle-roy_8ee95283_0.jpg": ("face-selfie", "50s, blonde waves"),
    "2026-05-21_c-stephens_69feb9a0_0.jpg": ("before-after", "BEFORE (labelled), 70s, no makeup; pair with _1. Her review is 4 stars and modest (less dry, no big change yet): don't sell it as dramatic"),
    "2026-05-21_c-stephens_69feb9a0_1.jpg": ("before-after", "AFTER (labelled), 70s; pair with _0"),
    "2026-05-23_anonymous_404e1c2f_0.jpg": ("face-selfie", "60s, in a car, sunglasses"),
    "2026-05-23_anonymous_404e1c2f_1.jpg": ("face-selfie", "60s, outdoors, sunglasses"),
    "2026-05-23_mitzi-chitty_6be40edf_0.jpg": ("product-in-hand", "60s, holding F-Balm Unscented and Face Whip"),
    "2026-05-23_mitzi-chitty_a540b3c4_0.jpg": ("product-in-hand", "60s, holding Freedom Field Balm"),
    "2026-05-25_anonymous_71fcaae6_0.jpg": ("face-selfie", "60s, beach, curly hair"),
    "2026-05-25_rebecca-fox_09e793b8_0.jpg": ("face-selfie", "50s, red top"),
    "2026-05-28_delilah-mcginnis-waldner_c6ecf1af_0.jpg": ("face-selfie", "40s-50s, at work with a headset"),
    "2026-05-28_virginia-palma_9942a1bb_0.jpg": ("lifestyle", "couple 60s on a boat"),
    "2026-05-28_virginia-palma_dded9286_0.jpg": ("lifestyle", "couple 60s selfie"),
    "2026-05-29_lee-hess_b2ee457f_0.jpg": ("face-selfie", "70s, no makeup, close-up"),
    "2026-06-01_anonymous_6f98a4b7_0.jpg": ("face-selfie", "70s, smiling"),
    "2026-06-05_natalia-timacheva_71b5d819_0.jpg": ("face-selfie", "40s, polished portrait"),
    "2026-06-07_suzie-burt_b0d4d507_0.jpg": ("face-selfie", "50s-60s, natural, bob haircut"),
    "2026-06-08_velma-whatley_391afc8a_0.jpg": ("lifestyle", "70s, at a restaurant with a drink"),
    "2026-06-09_lindsay-robertson_1de86241_0.jpg": ("lifestyle", "couple 50s-60s travelling (Parthenon)"),
    "2026-06-11_melanie-eastcott_0ae560b4_0.jpg": ("face-selfie", "60s, blonde, smiling"),
    "2026-06-15_mary-york_61464476_0.jpg": ("lifestyle", "60s-70s, hiking in the mountains"),
    "2026-06-17_teresita-santiago_9560733f_0.jpg": ("face-selfie", "50s, relaxed on a couch"),
    "2026-06-19_robyn-gale_f62e2697_0.jpg": ("face-selfie", "50s-60s, sports top, glowing"),
    "2026-06-21_donna-grant_fc95a457_0.jpg": ("face-selfie", "50s, has an 'I'm Blessed' sticker on it"),
    "2026-06-26_victoria-and-john-home-l_e5192393_0.jpg": ("face-selfie", "70s, short grey hair"),
    "2026-06-27_heidi-thorson-dean_579e546d_0.jpg": ("face-selfie", "50s, glasses, blonde-grey"),
    "2026-06-28_krista-mcguire_f00963ab_0.jpg": ("face-selfie", "50s, in a car"),
    "2026-06-28_yvonne-henshall_bdc8089b_0.jpg": ("not-usable", "photo of a printed portrait"),
    "2026-07-02_jennifer-hyland_678ad145_0.jpg": ("face-selfie", "50s, grey hair, in a car (stopped 3 times by women asking)"),
    "2026-07-02_jennifer-hyland_678ad145_1.jpg": ("face-selfie", "50s, at a desk"),
    "2026-07-02_jennifer-hyland_678ad145_2.jpg": ("face-selfie", "50s, white tee"),
    "2026-07-06_florence-c-bower-arsenau_d2e8bc7a_0.jpg": ("face-selfie", "60s, close-up, skin texture visible"),
    "2026-07-08_renie-praver_549be46c_0.jpg": ("lifestyle", "group of four women 60s"),
    "2026-07-08_renie-praver_549be46c_1.jpg": ("face-selfie", "60s, smiling"),
    "2026-07-10_lynn-marie-longo_5de4f111_0.jpg": ("not-usable", "dim selfie, 3-star review"),
    "2026-08-16_best-body-fitness-main-c_e472abaf_0.jpg": ("product-in-hand", "man 40s-50s hiking, holding Field Balm"),
    "2026-08-19_tanya-takacs_79d4f9df_0.jpg": ("face-selfie", "60s, grey hair, outdoors"),
    "2026-08-21_perrycorinna_f258ddcf_0.jpg": ("not-usable", "screenshot of a photo-editing app"),
    "2026-08-21_vicki-juliano_2c20c0a4_0.jpg": ("lifestyle", "70s, sunflower field"),
    "2026-08-24_tricia-cancel_3d0a09ea_0.jpg": ("face-selfie", "40s, fresh from the shower, no makeup"),
    "2026-08-25_andrea-kristensen_fddf26e8_0.jpg": ("face-selfie", "40s-50s, professional headshot"),
    "2026-08-31_sharon-o-fallon_7de3c5fc_0.jpg": ("face-selfie", "60s, in a car, scarf"),
    "2026-09-02_kari-guthrie_204ff715_0.jpg": ("lifestyle", "grandmother 60s with daughter and grandchild"),
    "2026-09-06_arlene-downton_33572655_0.jpg": ("face-selfie", "50s-60s, glasses, at home"),
    "2026-09-06_julie-ann-cetinski_6bc5aa25_0.jpg": ("product-in-hand", "40s, holding a tin next to her face"),
    "2026-09-08_sonja-tkachuk_407a6852_0.jpg": ("lifestyle", "60s, forest with a big dog"),
    "2026-09-08_tammy-kornelsen_72e4ac9e_0.jpg": ("face-selfie", "50s, at the office"),
    "2026-09-09_paulette-grissom_f8a94d66_0.jpg": ("face-selfie", "40s, framed selfie"),
    "2026-09-13_sherley-brownrigg_fea0932d_0.jpg": ("face-selfie", "30s-40s, at the gym, no makeup"),
    "2026-09-13_sherley-brownrigg_fea0932d_1.jpg": ("face-selfie", "30s-40s, in a car"),
    "2026-09-16_dory-sitte_7592ac7a_0.jpg": ("face-selfie", "70s, white hair, stylish portrait"),
    "2026-09-18_kathy-mould_2fc951d5_0.png": ("lifestyle", "couple 60s on a couch"),
    "2026-09-21_lorraine-scott_904494a8_0.jpg": ("not-usable", "screenshot of a 2022 Facebook post"),
    "2026-09-26_anonymous_60ae0065_0.jpg": ("face-selfie", "70s-80s, glasses"),
    "2026-10-05_stacey-lee-robson_17749d03_0.jpg": ("product-in-hand", "30s-40s, towel on head, holding F-Balm"),
    "2026-10-08_kimberly-miller_d1362839_0.jpg": ("face-selfie", "60s, curly blonde, glasses"),
    "2026-10-11_anonymous_9eddd411_0.jpg": ("lifestyle", "man 40s outdoors in the mountains"),
    "5-DexRlZf_mid.jpg": ("problem-closeup", "back of a tattooed hand"),
    "56WPw5Q2t.jpg": ("face-selfie", "60s, close-up around the eyes"),
    "5bQHAmkTh_mid.jpg": ("face-selfie", "50s, blonde, smiling, no makeup"),
    "5x8Lk06SC.jpg": ("face-selfie", "60s, beach, curly hair"),
    "7ziJ_k39D_mid.jpg": ("face-selfie", "40s-50s, close-up"),
    "8HGyUSG1n_mid.jpg": ("face-selfie", "50s, glasses, blonde"),
    "8i107gG4x_mid.jpg": ("face-selfie", "50s, outdoors, glowing"),
    "8kOO5oVs1.jpg": ("face-selfie", "60s, in a car, red lipstick"),
    "ChrIgUM2y_mid.jpg": ("problem-closeup", "smooth hand after use"),
    "Cl4j2keYN.jpg": ("before-after", "face before (top) and after (bottom), 60s"),
    "CmCvctC5-.jpg": ("face-selfie", "50s, outdoors, sunglasses"),
    "D5hn58OO1_mid.jpg": ("face-selfie", "60s, glasses, messy bun"),
    "HHsMktdd0.jpg": ("face-selfie", "50s, full length, blazer"),
    "IQtvA6R0Y_mid.jpg": ("face-selfie", "50s, eyes closed in the sun"),
    "K-75RqkJY_mid.jpg": ("problem-closeup", "palm with a red rash"),
    "L3wwQ0DQx_mid.jpg": ("face-selfie", "60s, blonde, floral top"),
    "LA-N8Oa1v_mid.jpg": ("face-selfie", "70s, grey hair, glasses"),
    "M0jILKjWb_mid.jpg": ("face-selfie", "60s, long grey hair, smiling"),
    "N6eQqQoiq_mid.jpg": ("face-selfie", "40s, in a car"),
    "QoF428Vm_.jpg": ("face-selfie", "50s, blonde"),
    "R50v5pqz__mid.jpg": ("before-after", "face side by side (Pic Stitch), 60s"),
    "RckWr8lD0_mid.jpg": ("face-selfie", "60s, blonde, floral top"),
    "SR_OpU1F1_mid.jpg": ("face-selfie", "50s, standing portrait"),
    "SpLQmHD9V_mid.jpg": ("face-selfie", "50s, grey-blonde"),
    "Syc37cfM4.jpg": ("lifestyle", "60s, seated portrait, long grey hair"),
    "Uqmuhj2fG.jpg": ("lifestyle", "60s, on a cruise ship"),
    "W0WH4MJju_mid.jpg": ("problem-closeup", "smooth back of a hand"),
    "WQQW5ok9E.jpg": ("face-selfie", "50s, blonde, pink top"),
    "X-NZP59n_5.jpg": ("face-selfie", "60s, blonde"),
    "YpDZ0HV6G.jpg": ("product-in-hand", "50s, F-Balm tin next to her face, big smile"),
    "bIs06eaBK.jpg": ("not-usable", "black-and-white art portrait"),
    "cJJAJ47kG_mid.jpg": ("face-selfie", "50s, headband, kitchen"),
    "clsOrFa8o_mid.jpg": ("problem-closeup", "cracked red heel"),
    "fCRfQnUVO_mid.jpg": ("face-selfie", "40s, in a car, glowing"),
    "gJXDFGKI6_mid.jpg": ("face-selfie", "40s, dark curly hair"),
    "hP6iXNZpN_mid.jpg": ("before-after", "hands side by side (Pic Stitch), 70s"),
    "iJlRfHopF_mid.jpg": ("problem-closeup", "red burn/blister on skin"),
    "jNe-4miQL_mid.jpg": ("face-selfie", "70s, no makeup, close-up"),
    "jncaI15i3.jpg": ("lifestyle", "50s, at brunch"),
    "jwyGucWeJ.jpg": ("face-selfie", "50s-60s, blonde, freckles, close-up glow"),
    "k1eRyzEyX_mid.jpg": ("face-selfie", "60s, tanned, short hair"),
    "ltI6nv0zt.jpg": ("face-selfie", "60s, short grey hair, outdoors"),
    "lzhWZ0Dvz_mid.jpg": ("face-selfie", "40s-50s, long dark hair"),
    "nBkHMUPhC.jpg": ("face-selfie", "60s, grey curly hair, smiling"),
    "nlNpV3UE-_mid.jpg": ("problem-closeup", "red eczema-like rash on the back of a hand"),
    "nlSA7jCx6_mid.jpg": ("face-selfie", "60s, blonde, floral top"),
    "pK6cwHOoD_mid.jpg": ("problem-closeup", "red rash patch on a tattooed hand"),
    "pUoyiTgxi_mid.jpg": ("lifestyle", "60s, beach at sunset, cap and sunglasses"),
    "rKhIS2Boj.jpg": ("product-in-hand", "60s, glasses, holding F-Balm in a bathroom"),
    "t4gmRtsTS.jpg": ("face-selfie", "man 40s"),
    "thYowujD5.jpg": ("lifestyle", "70s, holding a bouquet of roses"),
    "y9vR7YsoY_mid.jpg": ("face-selfie", "70s, no makeup, towel on head"),
}

# Screenshots the name match can't find (typo in the reviewer's name, or no name in the file).
MANUAL = {
    "Authority - Esthetician - Shari W - Esthetician 24 years never seen skin like mine at 64.png": "r-959aa813",
    "Authority - Other Pro - Karen H - Physiotherapist noticed.png": "r-b873b0e2",
    "Suzy G - Crepey skin on throat disappeared.png": "r-35c9edfe",
    "Eric Eczema Review Son.png": "r-eff6c97e",
    "Eric Eczema Review Son Larger.png": "r-eff6c97e",
    "Screenshot 2026-10-05 at 12.17.53\u202fPM.png": "r-b8261688",
}

def main(pics_dir, text_dir):
    reviews = list(csv.DictReader(open(REVIEWS, encoding="utf-8")))
    by_id = {r["id"]: r for r in reviews}
    os.makedirs(OUT, exist_ok=True)

    photos = []
    for f in sorted(os.listdir(pics_dir)):
        if not f.lower().endswith((".jpg", ".jpeg", ".png")):
            continue
        m = re.match(r"\d{4}-\d\d-\d\d_.+_([0-9a-f]{8})_\d+\.", f)
        rid = "r-" + m.group(1) if m else ""
        r = by_id.get(rid, {})
        kind, note = PHOTO_TAGS.get(f, ("untagged", "new photo: look at it and add a tag"))
        photos.append({
            "file": f, "dropbox_path": PICS_DROPBOX + f, "kind": kind, "description": note,
            "review_id": rid, "name": r.get("name", ""), "rating": r.get("rating", ""),
            "product": r.get("product", ""), "themes": r.get("themes", ""),
            "review": r.get("body", "").replace("\n", " ")[:600],
            "source": "Judge.me review photo" if rid else "unknown (older review app or social; ask before using)",
            "used_in_ads": "",
        })
    order = ["before-after", "problem-closeup", "product-in-hand", "face-selfie", "lifestyle", "not-usable", "untagged"]
    photos.sort(key=lambda p: (order.index(p["kind"]), p["file"]))
    with open(os.path.join(OUT, "photos.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(photos[0].keys()))
        w.writeheader(); w.writerows(photos)

    shots = []
    for f in sorted(os.listdir(text_dir)):
        if not f.lower().endswith(".png"):
            continue
        f = f.replace("#U202f", "\u202f")  # zip downloads mangle the narrow space in macOS screenshot names
        stem = f[:-4]
        parts = [p.strip() for p in stem.split(" - ")]
        if f.startswith("Eric Eczema"):
            category, profession, name, claim = "result", "", "Eric C", "Son's eczema went away in a week"
        elif f.startswith("Screenshot"):
            category, profession, name, claim = "result", "", "Heather H", "69 and people say I look 50"
        elif parts[0] == "Authority" and len(parts) >= 4:
            category, profession, name, claim = "authority", parts[1], parts[2], " - ".join(parts[3:])
        elif len(parts) >= 2:
            category, profession, name, claim = "result", "", parts[0], " - ".join(parts[1:])
        else:
            category, profession, name, claim = "unlabelled", "", "", stem
        shots.append({"file": f, "dropbox_path": TEXT_DROPBOX + f, "category": category,
                      "authority": profession, "name": name, "claim": claim,
                      **(found(by_id[MANUAL[unicodedata.normalize("NFC", f)]]) if unicodedata.normalize("NFC", f) in MANUAL
                         else match(name, claim, reviews))})
    with open(os.path.join(OUT, "screenshots.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(shots[0].keys()))
        w.writeheader(); w.writerows(shots)
    write_readme(photos, shots)
    print(len(photos), "photos,", len(shots), "screenshots,",
          sum(1 for s in shots if s["review_id"]), "screenshots matched to a review")

STOP = set("a an the my i in at of to and was is said asked what had has her his he she for with vs "
           "not as at than more less noticed looks look skin".split())

def match(name, claim, reviews):
    """Find the review a screenshot shows: same first name and last initial, most claim words in the text."""
    empty = {"review_id": "", "rating": "", "product": "", "review": ""}
    toks = name.replace(".", "").split()
    if not toks:
        return empty
    first = toks[0].lower()
    initial = toks[1][0].lower() if len(toks) > 1 else ""
    words = {w for w in re.findall(r"[a-z0-9]+", claim.lower()) if w not in STOP}
    best, best_score = None, 0
    for r in reviews:
        rn = r["name"].lower().replace(".", "").split()
        if not rn or rn[0] != first or (initial and (len(rn) < 2 or rn[1][0] != initial)):
            continue
        body = r["body"].lower()
        s = sum(1 for w in words if w in body)
        if s > best_score:
            best, best_score = r, s
    if not best or best_score < max(1, len(words) // 3):
        return empty
    return found(best)

def found(r):
    return {"review_id": r["id"], "rating": r["rating"], "product": r["product"],
            "review": r["body"].replace("\n", " ")}


def write_readme(photos, shots):
    from collections import Counter
    kinds = Counter(p["kind"] for p in photos)
    def rows(items, cols):
        return "\n".join("| " + " | ".join(str(i[c]).replace("|", "/") for c in cols) + " |" for i in items)
    ba = [p for p in photos if p["kind"] == "before-after"]
    pc = [p for p in photos if p["kind"] == "problem-closeup"]
    ph = [p for p in photos if p["kind"] == "product-in-hand"]
    auth = sorted((s for s in shots if s["category"] == "authority"), key=lambda s: s["authority"])
    res = [s for s in shots if s["category"] != "authority"]
    with open(os.path.join(OUT, "README.md"), "w", encoding="utf-8") as f:
        f.write(f"""# Testimonial photos and review screenshots

Everything here is a pop-up an editor can put on screen. The files live in Dropbox; this folder is the
index. Get a file with the Dropbox connector (`download_link` on the `dropbox_path`).

| Dropbox folder | What | Index |
|---|---|---|
| `{PICS_DROPBOX}` | {len(photos)} customer photos | `photos.csv` |
| `{TEXT_DROPBOX}` | {len(shots)} review screenshots (Judge.me cards, already chosen as the best) | `screenshots.csv` |

Rebuild after adding files: download both folders as zips, then
`python3 tallowed-truth/tools/build_testimonials.py <pics_dir> <screenshots_dir>`. New photos show up
as `untagged` until someone looks at them and adds a line to `PHOTO_TAGS` in the script.

## Need a review that isn't screenshotted yet?

Don't screenshot the website. Find it in `reviews/` and render it as a card in the same style:
`python3 tallowed-truth/tools/review_card.py <review id> [--name]` writes `output/cards/<id>.png`
(white rounded card, teal stars, Inter text, 1000 px wide for a 9:16 video). Cut long reviews with
`--max-chars`; never change the customer's words. Then add the PNG to the Testimonial Text folder
named `<Name> - <claim>.png`, so the next person can find it.

## Rules for using testimonials

- Quote word for word, typos and all. No made-up or "tidied" reviews.
- Photo and text must be the same customer (same review id). Never put one person's photo on another
  person's words.
- Photos with `source` = unknown came from an older review app or social media. Ask Anton before using
  them in a paid ad.
- Faces: only use a customer's face in an ad if it came with their review (Judge.me photos were
  shared publicly with the review). Don't crop people out of group shots to make a "before/after".
- Before/afters must be real pairs from the same person, same angle where possible; never lighten,
  smooth or filter one side.
- `used_in_ads` is empty until we match these to the winning ads (Pipeboard). Fill it in when you know.

## Photo kinds ({", ".join(f"{k}: {v}" for k, v in kinds.most_common())})

### Before/afters
| File | What | Review id | Name |
|---|---|---|---|
{rows(ba, ["file", "description", "review_id", "name"])}

### Problem close-ups (rashes, cracked skin, burns: the "before" of a story)
| File | What | Review id |
|---|---|---|
{rows(pc, ["file", "description", "review_id"])}

### Product in hand (customer holding the tin)
| File | What | Review id | Name |
|---|---|---|---|
{rows(ph, ["file", "description", "review_id", "name"])}

Face selfies and lifestyle shots: see `photos.csv` (`kind`, `description` with rough age, `review`).

## Review screenshots: a professional noticed ({len(auth)})
| Who noticed | Name | Claim | Review id |
|---|---|---|---|
{rows(auth, ["authority", "name", "claim", "review_id"])}

## Review screenshots: results ({len(res)})
| Name | Claim | Review id |
|---|---|---|
{rows(res, ["name", "claim", "review_id"])}
""")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
