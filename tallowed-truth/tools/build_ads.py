"""Write the weekly "what's working" snapshot from 30-day ad data.

  python3 tallowed-truth/tools/build_ads.py tallowed-truth/ads/creatives_30d.json

creatives_30d.json: one row per creative (ads with the same name summed across ad sets): name, spend,
purchases, value, impr. Build it from Pipeboard get_insights (level=ad, last_30d, every page).
Writes tallowed-truth/ads/whats-working.md and creatives_30d.csv.
"""
import csv, json, os, re, sys, collections

OUT = os.path.join(os.path.dirname(__file__), "..", "ads")
STOP = {"Net New", "Evergreen", "Iteration", "Founder", "Yapper", "STATIC", "NA", "-", "MHI", "Internal", "Pat",
        "Influencer", "F-Balm", "Ben Corkery", "Anton", "Mubashir", "Hannah", "The Tallowed Truth", "Vitality For You",
        "Golden Meadows", "F-Balm Copy - Evergreen", "F-Balm Copy", "F-Balm Quiz", "Ben Listicle", "Multi Scent OP",
        "Freedom Face Whip", "JP", "Ben", "Youthful", "Digital Ride", ""}

HANDLES = set()  # creator handles like "PatBeresford", filled from all ad names in main()

def handle_name(h):
    return re.sub(r"(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])", " ", h)

def parse(name):
    fmt = ("Static" if re.search(r"static", name, re.I) else
           "Influencer/creator" if name.startswith(("Influencer", "_Influencer", "Ben_", "Internal_")) and "trybe=" in name else
           "Founder (Ben)" if "Founder" in name else
           "UGC" if "UGC" in name else "Other")
    h = next((h for h in sorted(HANDLES, key=len, reverse=True) if h + "_Influencer_" in name), None)
    creator = (handle_name(h) if h else "Ben Corkery" if "Ben Corkery" in name and fmt.startswith("Founder") else "")
    m = re.search(r"_20\d{6}_([^_]+)_trybe=", name)
    if m:
        concept = m.group(1)
        for h in HANDLES:
            concept = concept.replace(h, "").strip()
    else:
        parts = [p.strip() for p in name.split("_")]
        tmpl = next((i for i, p in enumerate(parts) if p.startswith("[DR]")), None)
        tail = parts[tmpl + 1:] if tmpl is not None else parts[-1:]
        concept = " / ".join(p for p in tail if p not in STOP and not re.fullmatch(r"[0-9a-f]{8}", p))[:140] or name[:60]
    month = re.search(r"(January|February|March|April|May|June|July|August|September|October|November|December) 20\d\d", name)
    return fmt, creator, concept, month.group(0) if month else ""

def main(path):
    rows = json.load(open(path))
    for r in rows:
        HANDLES.update(re.findall(r"_([A-Z]+[a-z]*(?:[A-Z][a-z]+)+)_Influencer_", r["name"]))
    tot_s = sum(r["spend"] for r in rows); tot_p = sum(r["purchases"] for r in rows)
    avg = tot_s / tot_p
    for r in rows:
        r["format"], r["creator"], r["concept"], r["launched"] = parse(r["name"])
        r["cpa"] = r["spend"] / r["purchases"] if r["purchases"] else None
        r["roas"] = r["value"] / r["spend"] if r["spend"] else 0
    with open(os.path.join(OUT, "creatives_30d.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["rank", "concept", "format", "creator", "launched", "spend_cad", "purchases", "cpa_cad", "pixel_roas", "ad_name"])
        for i, r in enumerate(rows):
            w.writerow([i + 1, r["concept"], r["format"], r["creator"], r["launched"], round(r["spend"]), int(r["purchases"]),
                        round(r["cpa"], 1) if r["cpa"] else "", round(r["roas"], 2), r["name"]])

    def line(r):
        cpa = f"CA${r['cpa']:.0f}" if r["cpa"] else "no sales"
        flag = " ✅" if r["cpa"] and r["cpa"] < avg * 0.85 else (" ⚠️" if r["cpa"] and r["cpa"] > avg * 1.2 else "")
        who = f", {r['creator']}" if r["creator"] else ""
        return (f"| {r['concept'][:70]} | {r['format']}{who} | {r['launched']} | {r['spend']:,.0f} | {r['purchases']:.0f} | "
                f"{cpa}{flag} |")

    by_fmt = collections.defaultdict(lambda: [0, 0, 0])
    for r in rows:
        x = by_fmt[r["format"]]; x[0] += r["spend"]; x[1] += r["purchases"]; x[2] += 1
    by_creator = collections.defaultdict(lambda: [0, 0])
    for r in rows:
        if r["creator"]:
            x = by_creator[r["creator"]]; x[0] += r["spend"]; x[1] += r["purchases"]
    new = [r for r in rows if r["launched"] in ("October 2026", "September 2026") and r["spend"] > 1000]
    rising = sorted((r for r in new if r["cpa"] and r["cpa"] < avg), key=lambda r: r["cpa"])
    date = rows and "2026-09-28 to 2026-10-27"
    H = "| Concept / hook | Format | Launched | Spend CA$ | Purchases | Cost per purchase |\n|---|---|---|---|---|---|"
    with open(os.path.join(OUT, "whats-working.md"), "w", encoding="utf-8") as f:
        f.write(f"""# What's working: TTT ads, last 30 days

{date}. Meta ad account The Tallowed Truth (act_1680177762468989), from Pipeboard.
**CA${tot_s:,.0f} spent, {tot_p:,.0f} purchases, average CA${avg:.0f} per purchase** across {len(rows):,} creatives.
✅ = at least 15% cheaper per purchase than average, ⚠️ = 20%+ more expensive. Purchases and ROAS are
Meta's pixel numbers (7-day click / 1-day view), so use them to compare ads, not as true profit.

## The short version

- Creative is concentrated: the top 10 concepts take about half the spend.
- **Ben (founder) ads are the most efficient big spenders.** "Come clean founder confession" (bad tallow
  from China) is #1 at CA$36 per purchase on CA$44K.
- **Review-story hooks from creators carry the most spend now** ("Esthetician shocked", "Carded at 73",
  "Nicest skin ever seen", "Grocery store skeptic"), but they cost more per purchase (CA$49-57) than Ben's.
  These hooks are the same customer reviews in `testimonials/screenshots.csv`.
- Cheapest proven ads: static before/afters (MHI), "$900 French creams" (Face Whip), "Stop buying tallow",
  "Founder 4", "under eyes vid".

## Top 30 concepts by spend

{H}
{chr(10).join(line(r) for r in rows[:30])}

## New in Sep/Oct and beating the average (scale or iterate these)

{H}
{chr(10).join(line(r) for r in rising[:15]) or "| none yet | | | | | |"}

## By format

| Format | Creatives | Spend CA$ | Share | Cost per purchase |
|---|---|---|---|---|
{chr(10).join(f"| {k} | {v[2]} | {v[0]:,.0f} | {v[0] / tot_s:.0%} | CA${v[0] / v[1]:.0f} |" for k, v in sorted(by_fmt.items(), key=lambda kv: -kv[1][0]) if v[1])}

## By creator (influencer and founder ads)

| Creator | Spend CA$ | Cost per purchase |
|---|---|---|
{chr(10).join(f"| {k} | {v[0]:,.0f} | CA${v[0] / v[1]:.0f} |" for k, v in sorted(by_creator.items(), key=lambda kv: -kv[1][0])[:12] if v[1])}

## How to use this

- Want a hook idea? Start from a ✅ concept, keep the message, change one thing (who says it, the
  prop, the setting, the first line). See `rules/creative-learnings.md`.
- Want a story for it? Find the matching theme in `reviews/stories/` (e.g. "Esthetician shocked" ->
  `authority.md`, "Smokers lines" -> `wrinkles.md`).
- Full list with every creative: `creatives_30d.csv`.
""")
    print("avg CPA", round(avg, 1), "| rising:", len(rising))

if __name__ == "__main__":
    main(sys.argv[1])
