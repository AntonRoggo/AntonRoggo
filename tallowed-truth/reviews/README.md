# Reviews & stories

Every published Judge.me review (40605 with text, 2023-06-12 to 2026-10-29), cleaned and tagged so Claude can find the right story fast. Emails and IP addresses are removed; names are shown as the website shows them (first name, last initial).

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

- 5★: 34113
- 4★: 3303
- 3★: 1799
- 2★: 659
- 1★: 731

## Reviews per product

- F-Balm (original): 26783
- Freedom Face Whip: 4157
- F-Balm Whipped Body Butter: 1842
- Freedom Field Balm (bug balm): 1666
- Store review: 1238
- S-Balm zinc sun lotion: 1123
- F-Balm Black Label (unscented): 1106
- F-Balmer lip balm: 1037
- Bundle: 654
- Bee-Free Vanilla Body Butter: 297
- F-Balm Orange Vanilla: 237
- Tallow soap bar: 158
- Shipping: 153
- F-Balm Lavender: 127
- Merch: 13
- Free gift: 10
- Calm Balm (magnesium): 4

## Themes

| Theme | File | Positive reviews |
|---|---|---|
| Wrinkles, fine lines, smoker's lines | `stories/wrinkles.md` | 1480 |
| Crepey skin, neck, sagging, firmness | `stories/crepey-neck.md` | 1065 |
| Dry, flaky, tight skin | `stories/dry-skin.md` | 3090 |
| Eczema, psoriasis, dermatitis, rosacea, rashes | `stories/eczema.md` | 1137 |
| Acne, breakouts, clogged pores | `stories/acne.md` | 989 |
| Age spots, dark spots, redness, even tone | `stories/spots-tone.md` | 534 |
| Scars, burns, cuts, wounds, healing | `stories/scars-healing.md` | 657 |
| Cracked hands, heels, feet | `stories/hands-feet.md` | 1333 |
| People noticed / compliments / glow | `stories/compliments.md` | 2333 |
| A professional noticed (derm, esthetician, nurse, doctor, stylist) | `stories/authority.md` | 174 |
| Replaced expensive creams, Botox, retinol | `stories/replaced-expensive.md` | 561 |
| Menopause, hormones, over 50 skin | `stories/menopause.md` | 96 |
| Sensitive / reactive skin | `stories/sensitive.md` | 1224 |
| Babies, kids, family | `stories/kids-baby.md` | 1063 |
| Men using it (husband, dad, son) | `stories/men.md` | 891 |
| Skeptic first: beef fat, weird, hesitant | `stories/skeptic.md` | 487 |
| Smell, texture, not greasy, absorbs | `stories/scent-texture.md` | 9547 |
| Bug repellent (Field Balm) | `stories/bugs.md` | 1449 |
| Sun, sunburn, SPF | `stories/sun.md` | 630 |
| Lips, chapped lips | `stories/lips.md` | 1536 |
| Repeat buyer, stocking up, subscribed | `stories/repeat-buyer.md` | 1047 |
