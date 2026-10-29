"""Pick the ad comments worth using: real results, real objections, real pre-purchase questions.

  python3 tallowed-truth/tools/relevant_comments.py

Reads comments/comments.csv (from build_comments.py), writes comments/relevant.md and
comments/relevant.csv. Drops political/contest/off-topic comments, one-liners and generic praise.
"""
import csv, os, re

HERE = os.path.join(os.path.dirname(__file__), "..", "comments")
USED = re.compile(r"\b(i'?ve been|been using|i use|i used|using it|use it|my (skin|face|wife|husband|son|daughter|mom|lips|hands|feet|heels)|"
                  r"since|after|weeks?|days?|months?|year|first (time|application|night)|ordered|bought|tin|jar)\b", re.I)
RESULT = re.compile(r"wrinkl|lines|11s|crep|eczema|psoria|rosacea|dry|flak|crack|heal|spots?|acne|break ?out|scar|burn|"
                    r"glow|soft|smooth|compliment|younger|noticed|gone|disappear|fad|clear|difference|itch|rash|smell|greas", re.I)
USED_IT = re.compile(r"been using|using (it|this|f|the|mine)|i use (it|this|the|f)|used (it|this|f)|got mine|received (my|mine)|"
                     r"my first (order|tin|jar)|since (using|i started)|after using|started using|i put|i apply|applied|"
                     r"(week|month|year)s? (in|now|of using)|tried it", re.I)
POS = re.compile(r"\blove|amazing|\bgreat\b|\bbest\b|works|wonderful|recommend|glad|impressed|so soft|so good|magic|"
                 r"not greasy|no smell|no break ?outs|don'?t find it expensive|not expensive|worth|lasts|helped|healed|fading|"
                 r"gone|disappear|cleared", re.I)
BAD = re.compile(r"disappoint|no (change|difference|improvement)|see no|not (seen|noticed) (a|any)|nothing|haven'?t seen|"
                 r"can'?t handle|(?<!not )(?<!isn't )(?<!isnt )greasy|stink|smell(s|ing)? like (a )?cow|broke|break(s)? (me|my face) out|"
                 r"clog|rash|itch|hives|waste|scam|(?<!not )(?<!n't find it )(?<!nt find it )expensive|pricey|reaction|tearing|burn|gritty|"
                 r"heavy|struggling|sadly|doesn'?t (work|do|help)|didn'?t (work|do|help)|worse|stop using|had to stop|refund|returning|more wrinkles", re.I)
NOT_YET = re.compile(r"need to try|want to try|wanna try|going to try|gonna try|can'?t wait|haven'?t tried|will try|"
                     r"thinking (of|about) (trying|buying)|waiting (for|on) my", re.I)
NOISE = re.compile(r"liberal|trudeau|carney|government|tax|vote|woke|politic|strong and free|commie|trump|maga|convoy|prayer|heavenly|scripture|lord jesus", re.I)

def bucket(r):
    t = r["comment"].replace("’", "'").replace("‘", "'")
    if NOISE.search(t) or len(t) < 40:
        return None
    pos, bad = len(POS.findall(t)), len(BAD.findall(t))
    if r["kind"] == "question" and not USED_IT.search(t):
        return "Questions before buying"
    if bad > pos:
        return "Real objections"
    if r["objections"] or (r["kind"] == "objection"):
        return "Doubts answered by customers"
    if r["kind"] == "question":
        return "Questions from users"
    if RESULT.search(t) and pos and not NOT_YET.search(t) and r["kind"] in ("story", "praise", "other"):
        return "Customer results"
    return None

def main():
    rows = list(csv.DictReader(open(os.path.join(HERE, "comments.csv"), encoding="utf-8")))
    keep = []
    for r in rows:
        b = bucket(r)
        if b:
            r["section"] = b
            r["score"] = int(r["likes"]) * 3 + min(len(r["comment"]), 400) // 40 + (3 if r["ttt_answer"] else 0)
            keep.append(r)
    order = ["Customer results", "Doubts answered by customers", "Real objections", "Questions before buying",
             "Questions from users"]
    keep.sort(key=lambda r: (order.index(r["section"]), -r["score"]))
    with open(os.path.join(HERE, "relevant.csv"), "w", newline="", encoding="utf-8") as f:
        cols = ["section", "objections", "likes", "date", "comment", "ttt_answer", "ad", "post_id"]
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader(); w.writerows(keep)
    with open(os.path.join(HERE, "relevant.md"), "w", encoding="utf-8") as f:
        f.write(f"# Relevant ad comments\n\n{len(keep)} of {len(rows)} comments are worth reading: real results, real "
                "doubts and real questions. Political, contest and one-word comments are left out. Most liked first.\n\n"
                "- **Customer results**: people who use it saying what changed. Real wording for script lines.\n"
                "- **Doubts answered by customers**: someone raises a doubt (greasy, smell, price, breakouts) and answers "
                "it from their own use. The best objection-handling lines there are.\n"
                "- **Real objections**: complaints. Know them, answer them in scripts, don't promise against them.\n"
                "- **Questions before buying / from users**: what to answer inside the video.\n\n"
                "Comments are public but unnamed here: use them for hooks, script lines and objection handling, not as "
                "on-screen testimonials (use reviews for that).\n")
        for sec in order:
            items = [r for r in keep if r["section"] == sec]
            f.write(f"\n## {sec} ({len(items)})\n\n")
            for r in items:
                tag = f" [{r['objections']}]" if r["objections"] else ""
                f.write(f"- \"{r['comment']}\" ({r['likes']} likes, {r['date']}){tag}\n")
                if r["ttt_answer"]:
                    f.write(f"  - TTT answered: \"{r['ttt_answer']}\"\n")
    from collections import Counter
    print(len(keep), Counter(r["section"] for r in keep))

if __name__ == "__main__":
    main()
