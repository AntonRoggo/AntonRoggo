# Ad comments

1897 Facebook comments from 21 of the top ads on The Tallowed Truth page
(pulled with Pipeboard, up to 100 top-level comments per ad, 2026-10-29). Comments are sorted into:
other 609, praise 434, question 429, objection 150, story 145, political/off-topic 130.

| File | Use it for |
|---|---|
| `relevant.md` | **Start here.** The 400-odd comments worth reading, in four groups: customer results, doubts answered by customers, real objections, questions. |
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
