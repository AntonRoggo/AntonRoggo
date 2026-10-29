# The Tallowed Truth: creator brain

The Tallowed Truth (TTT) makes beef tallow skincare in Canada. Main product: **F-Balm**, a beef tallow
and raw honey face balm. This folder is the brain for TTT's creators and editors: real customer
stories, testimonial photos, what's working in the ads, and the rules for cutting videos. It is
meant to be loaded into the company Claude project, and Claude should read this file first.

## What creators ask, and where the answer is

| Question | Look in |
|---|---|
| "What reviews can I use for a video about X?" | `reviews/stories/<theme>.md` (best 40 per theme), then `reviews/reviews.csv` for more |
| "Give me the best customer stories" | `reviews/top-stories.md` |
| "Who noticed? Dermatologist, esthetician, nurse..." | `reviews/stories/authority.md`, `testimonials/screenshots.csv` (category `authority`) |
| "I need a before/after or a customer photo" | `testimonials/README.md`, `testimonials/photos.csv` |
| "I need this review on screen" | `testimonials/screenshots.csv` if it's already a screenshot; otherwise `tools/review_card.py <id>` |
| "What do people complain about? Objection hooks?" | `comments/objections.md` (under our ads, with how TTT answered), `reviews/objections.md` (1-3 star reviews) |
| "What do people ask before buying?" | `comments/questions.md` |
| "What's working in the ads right now?" | `ads/whats-working.md` (refreshed weekly), every creative in `ads/creatives_30d.csv` |
| "Give me hook ideas" | `ads/whats-working.md` (✅ concepts) + `rules/creative-learnings.md` + the stories above + `comments/` |

## Folders

| Folder | What |
|---|---|
| `reviews/` | All 40,605 Judge.me reviews (2023-06 to 2026-10), cleaned, tagged by theme, ranked by how good a story they make. See `reviews/README.md`. |
| `testimonials/` | Index of the testimonial photos (120) and review screenshots (53) in Dropbox, each linked to its review. See `testimonials/README.md`. |
| `ads/` | The weekly "what's working" snapshot from the ad account: every creative's spend and cost per purchase, by concept, format and creator. |
| `comments/` | 1,897 Facebook comments from the top ads: objections, questions and customer stories in their own words. |
| `rules/` | Creative learnings from the ad tests and calls, and the video cut rules. |
| `creators/` | Creator SOP and how to send footage. |
| `tools/` | Scripts that rebuild the indexes and render review cards. |

## Ground rules for Claude

- **Real words only.** Quote reviews word for word (typos included) and cite the review id
  (`r-xxxxxxxx`). Never invent, merge or "improve" a testimonial, and never change a number (age,
  weeks, price).
- **Match photo to words.** A photo can only go with its own review (same id).
- **Delivery, not message.** Creators change how a line is said, the order, setting or prop, not what
  the customer said (see `rules/creative-learnings.md`).
- **No medical claims.** Say what customers said happened to them ("my eczema calmed down in a week",
  as a quote); don't promise the product treats or cures anything.
- **Customer privacy.** Names are shown the way the website shows them (first name, last initial).
  There are no emails or addresses here; don't go looking for them.
- If a creator asks for something this folder can't answer (numbers, a review that isn't here, a new
  claim), say so instead of guessing.
