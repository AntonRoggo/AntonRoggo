"""Build the ad-comment library from Pipeboard get_post_comments results.

  python3 tallowed-truth/tools/build_comments.py <dir of saved get_post_comments results> <creatives_30d.json>

Each file is a saved tool result ({"result": "<json string>"} with post_id and comments). The
creatives file is the 30-day spend per creative (built from get_insights), used to say which ad a
post belongs to. Writes tallowed-truth/comments/: comments.csv, stories.md, objections.md,
questions.md, README.md. Commenter names are never stored; TTT's replies keep only the answer.
"""
import csv, glob, json, os, re, sys, collections

HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, "..", "comments")

# post id -> creative rank in creatives_30d.json (from bulk_get_ad_creatives effective_object_story_id)
POST_CREATIVES = {
    "778514201856919": [10], "695292733512400": [14], "720606164314390": [16], "925191683855836": [18],
    "447132791661730": [29], "629117316796609": [31], "598242103217464": [37], "876648245376847": [47],
    "628837376824603": [49, 77], "588339074207767": [53, 97], "736795639362109": [56], "766166199758386": [57],
    "789269810781358": [58], "2193100897904229": [65], "632553789786295": [67], "926961133678891": [68],
    "724996837208656": [69], "728346426873697": [73, 116], "1038887965819540": [75], "1011490625225941": [76],
    "436972382677771": [82, 100], "709261152115558": [87], "580475551660786": [88], "723811393993867": [90],
    "927019457006392": [92],
}

KINDS = {  # first match wins, in this order
    "political/off-topic": r"liberal|trudeau|carney|ford\b|tax(es|ing)|government|vote|woke|politic|vaccine|convoy|communis|maga|trump",
    "contest": r"strong and free",
    "question": r"\?\s*$|^(is|does|do|can|will|where|what|how|why|are|which|any)\b",
    "story": r"\b(i|my|me|i'?ve|i'?m)\b.*\b(skin|face|wrinkl|lines?|eczema|psoria|dry|spots?|heels|hands|lips|acne|scar|burn|neck|crep|glow|soft)",
    "praise": r"love|amazing|best|great|works|wonderful|recommend|awesome|thank",
}
KIND_RE = {k: re.compile(v, re.I) for k, v in KINDS.items()}
OBJECTIONS = {
    "Doesn't work / no difference": r"no (difference|change)|not (see|notice)|didn'?t (work|do|see|notice)|doesn'?t (work|do)|nothing|haven'?t seen|don'?t (find|see|notice) a difference|won'?t|not a miracle|miracle worker|bs\b|scam",
    "Too fast to be true (instant results)": r"that fast|in seconds|already\?|one application|first time\?|instant|ridiculous|ya right|yeah right|just rubbed",
    "Greasy / heavy": r"greas|vaseline|oily|heavy|absorb",
    "Smell (cow, beef)": r"smell|stink|cow|beefy|odou?r",
    "Breakouts / clogged pores": r"break ?out|broke (me )?out|clog|acne|pimple|comedogenic|pores",
    "Reaction / sensitivity": r"reaction|\brash|hives|itch(y|ing)?\b|\bred(ness)?\b|\bburn(ed|ing|t)\b|tearing|allerg|\bsting",
    "Price": r"expensive|price|cost|afford|\$\d|cheaper",
    "Tallow / beef fat is gross or weird": r"beef fat|animal fat|gross|disgust|yuck|tallow is fat|from the cow",
    "Trust (fake reviews, actors, offers)": r"fake|actor|paid|scam|scares me|bogo|buy one get one|never get a response|before and after",
}
OBJ_RE = {k: re.compile(v, re.I) for k, v in OBJECTIONS.items()}
# A comment only counts as an objection if it is negative about that thing, not "it smells so good".
NEG = re.compile(r"\bnot\b|\bno\b|n'?t\b|never|\btoo\b|hate|disappoint|\bstop|\bbad\b|\bbut\b|worse|wast|scam|"
                 r"expensive|pricey|greas|stink|clog|break ?out|broke (me )?out|rash|hives|itch|reaction|gross|"
                 r"ridiculous|ya right|yeah right|fake|\bbs\b|nothing|smells? like|\bcow\b|gritty|vaseline|\?", re.I)

STARTERS = set("hi hey hello yes yep no we thanks thank love glad please it many some the our this that you absolutely great "
               "appreciate sorry lol haha omg wow so feel all happy aww awesome up don't tallow not it's that's there here only just "
               "unfortunately f-balm a an i".split())

def strip_name(msg):
    """TTT's replies start with the commenter's name ("Janice Taylor some tell us..."). Drop it."""
    words = msg.split()
    i = 0
    while i < min(4, len(words) - 1) and words[i][:1].isupper() and words[i].lower().strip(",!.") not in STARTERS:
        i += 1
    return " ".join(words[i:]).lstrip(", ") if 1 <= i <= 4 else msg

def objections(msg):
    return [o for o, rx in OBJ_RE.items() if rx.search(msg)] if NEG.search(msg) else []

def kind(msg):
    for k in ("political/off-topic", "contest"):
        if KIND_RE[k].search(msg):
            return k
    if objections(msg) and not KIND_RE["question"].search(msg):
        return "objection"
    for k in ("question", "story", "praise"):
        if KIND_RE[k].search(msg):
            return k
    return "other"

def main(src_dir, creatives_path):
    creatives = json.load(open(creatives_path))
    rows, seen = [], set()
    for f in sorted(glob.glob(os.path.join(src_dir, "*"))):
        try:
            d = json.loads(json.loads(open(f).read(), strict=False)["result"], strict=False)
        except Exception as e:
            print("skip", f, e)
            continue
        pid = d["post_id"].split("_")[-1]
        ads = [creatives[i] for i in POST_CREATIVES.get(pid, []) if i < len(creatives)]
        ad_name = ads[0]["name"] if ads else ""
        spend = round(sum(a["spend"] for a in ads))
        for c in d["comments"]:
            if c["id"] in seen or not c.get("message", "").strip():
                continue
            seen.add(c["id"])
            msg = re.sub(r"\s+", " ", c["message"]).strip()
            answer = next((strip_name(r["message"]) for r in c.get("replies") or []
                           if (r.get("from") or {}).get("name") == "The Tallowed Truth"), "")
            k = kind(msg)
            objs = objections(msg) if k in ("objection", "question") else []
            rows.append({"post_id": d["post_id"], "ad": ad_name[:160], "ad_spend_30d": spend,
                         "date": c.get("created_time", "")[:10], "likes": c.get("like_count", 0),
                         "replies": c.get("comment_count", len(c.get("replies") or [])),
                         "kind": k, "objections": "; ".join(objs), "comment": msg, "ttt_answer": answer})
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "comments.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)

    def q(r):
        return f"- \"{r['comment']}\" ({r['likes']} likes, {r['date']})"

    stories = sorted((r for r in rows if r["kind"] == "story"), key=lambda r: (-int(r["likes"]), -len(r["comment"])))
    with open(os.path.join(OUT, "stories.md"), "w", encoding="utf-8") as fh:
        fh.write("# Customer stories from ad comments\n\nPeople telling their own results under our Facebook ads, "
                 "most liked first. Unlike reviews, these are public comments with no name attached here: use them "
                 "for script ideas and wording (how real customers say it), not as an on-screen testimonial "
                 "without permission.\n\n")
        fh.write("\n".join(q(r) for r in stories[:80]) + "\n")

    with open(os.path.join(OUT, "objections.md"), "w", encoding="utf-8") as fh:
        fh.write(f"# Objections in ad comments\n\nWhat skeptics and unhappy buyers say under our ads ({len(rows)} "
                 "comments read, from the top ads on the TTT page). Each objection is a hook or a line to answer "
                 "inside a script. Where TTT replied, the answer is shown: that's the approved way to handle it.\n\n")
        counts = collections.Counter(o for r in rows for o in r["objections"].split("; ") if o)
        for o, n in counts.most_common():
            hits = sorted((r for r in rows if o in r["objections"]), key=lambda r: (-int(r["likes"]), -len(r["comment"])))
            fh.write(f"## {o} ({n})\n\n")
            for r in hits[:8]:
                fh.write(q(r) + "\n")
                if r["ttt_answer"]:
                    fh.write(f"  - TTT answered: \"{r['ttt_answer']}\"\n")
            fh.write("\n")

    qs = sorted((r for r in rows if r["kind"] == "question"), key=lambda r: (-int(r["likes"]), r["date"]))
    with open(os.path.join(OUT, "questions.md"), "w", encoding="utf-8") as fh:
        fh.write("# Questions people ask under our ads\n\nEvery question is a doubt someone had before buying. "
                 "Answer the common ones inside the video (\"you're probably wondering...\").\n\n")
        for r in qs[:120]:
            fh.write(q(r) + (f"\n  - TTT answered: \"{r['ttt_answer']}\"" if r["ttt_answer"] else "") + "\n")

    kinds = collections.Counter(r["kind"] for r in rows)
    with open(os.path.join(OUT, "README.md"), "w", encoding="utf-8") as fh:
        fh.write(f"""# Ad comments

{len(rows)} Facebook comments from {len({r['post_id'] for r in rows})} of the top ads on The Tallowed Truth page
(pulled with Pipeboard, up to 100 top-level comments per ad, 2026-10-29). Comments are sorted into:
{", ".join(f"{k} {v}" for k, v in kinds.most_common())}.

| File | Use it for |
|---|---|
| `relevant.md` | **Start here.** The comments worth reading, in four groups: customer results, doubts answered by customers, real objections, questions (`tools/relevant_comments.py`). |
| `objections.md` | What skeptics say, grouped, with how TTT answered. Objection hooks and lines to handle doubts in a script. |
| `questions.md` | What people ask before buying. Answer the common ones in the video. |
| `stories.md` | Customers telling their own results in the comments. Real wording for scripts. |
| `comments.csv` | Everything: post, ad name, ad's 30-day spend, date, likes, kind, objections, comment, TTT's answer. |

No commenter names are stored. Don't put a comment on screen as a testimonial; use reviews for that.

Not included yet: ads that run from other pages (Ben's founder page, Vitality For You, Golden Meadows,
Non-Woke Daily), which is most of the current top spend, and the TTT Insider group. Pipeboard needs
page access for those (see `ads/README.md`).

Rebuild: save each `get_post_comments` result into one folder, then
`python3 tallowed-truth/tools/build_comments.py <folder> <creatives_30d.json>`.
""")
    print(len(rows), "comments;", dict(kinds))

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
