# Ads: what's working

| File | What |
|---|---|
| `whats-working.md` | The weekly snapshot: top concepts, new ones beating the average, by format and creator. Read this first. |
| `creatives_30d.csv` | Every creative in the last 30 days: concept, format, creator, launch month, spend, purchases, cost per purchase, pixel ROAS, full ad name. |
| `creatives_30d.json` | The same, raw (input for `tools/build_ads.py`). |

Source: Pipeboard (Meta) on The Tallowed Truth ad account (act_1680177762468989), `get_insights` at
ad level for the last 30 days, every page, with ads of the same name summed across ad sets.

## Weekly refresh (before the creator call)

1. Pull `get_insights` (level ad, last_30d, limit 500, action_breakdowns []) and page through `after`.
2. Sum by ad name into `creatives_30d.json` (name, spend, purchases, value, impr, top_ad, n_ads).
3. `python3 tallowed-truth/tools/build_ads.py tallowed-truth/ads/creatives_30d.json`
4. Pull comments for the top ads (`get_post_comments`, see `comments/README.md`) and rebuild comments.
5. After the call, write any new learning into `rules/creative-learnings.md`.

## Known gaps

- Comments only work for ads posted from The Tallowed Truth page. Most top spend now runs from Ben's
  founder page (590106480853626, which Pipeboard can't see), Vitality For You and Golden Meadows. To
  read those comments, the Facebook login connected to Pipeboard needs a role on those pages, then
  reconnect at pipeboard.co/connections and accept every permission (`pages_read_user_content`).
- Hook rate, hold rate and the first 3 seconds of each video aren't in here yet.
