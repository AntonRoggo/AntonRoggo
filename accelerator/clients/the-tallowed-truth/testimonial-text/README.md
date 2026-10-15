# Testimonial Text (clean review screenshots)

Star rating plus the review text only (no name, badge or "Read less"), matching the screenshots Anton keeps in Dropbox `/[01] Clients/The Tallowed Truth/Testimonial Text`. Rebuild with `node tools/review_cards.js accelerator/clients/the-tallowed-truth/testimonial-text/reviews.json output/` (text is verbatim, only repeated spaces collapsed).

| File in Dropbox | Reviewer | Date | Source | Used in |
|---|---|---|---|---|
| Stacey N - Glowing skin compliments.png | Stacey N. | 2024-07-03 | Loox export | glowing skin static |
| Mindy S - Fourth order fewer wrinkles.png | Mindy S. | 2025-07-08 | Loox export | Founder 4 - Copy |
| Judy B - Carded at 73.png | Judy Beaudoin | 2026-08-31 | Judge.me d50f79e6 | Carded at 73 |
| Sandi M - Plastic surgeon.png | Sandi Melkonian | 2026-05-05 | Judge.me b072bac3 | Feedback from a plastic surgeon |

Not found in Judge.me (all products, full-text search) or the Loox export as of 2026-10-15, so probably from email, DMs or Facebook comments:
- Allison, 64: "You look 10 years younger than the last time I was in here." (Noticed at 64)
- Janet: "After 7 days, they're starting to fade away." (Weird mouth wrinkles hack)
- Cecilia Camacho: "I got asked yesterday if I had 'work' done!!!!" (static reviews + ingredients)

How to find a review: Judge.me `https://api.judge.me/reviews/all_reviews_js_based?url=thetallowedtruth.myshopify.com&shop_domain=thetallowedtruth.myshopify.com&platform=shopify&review_type=all-reviews&per_page=30&page=1&search=<words>` searches every product; the Loox export (`tallowed_truth_reviews.xlsx` in the client's Dropbox folder) covers reviews up to mid-2026.
