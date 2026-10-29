# Testimonial photos and review screenshots

Everything here is a pop-up an editor can put on screen. The files live in Dropbox; this folder is the
index. Get a file with the Dropbox connector (`download_link` on the `dropbox_path`).

| Dropbox folder | What | Index |
|---|---|---|
| `/[01] Clients/The Tallowed Truth/Testimonial Pics/` | 120 customer photos | `photos.csv` |
| `/[01] Clients/The Tallowed Truth/Testimonial Text/` | 53 review screenshots (Judge.me cards, already chosen as the best) | `screenshots.csv` |

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

## Photo kinds (face-selfie: 73, lifestyle: 20, problem-closeup: 8, product-in-hand: 8, not-usable: 6, before-after: 5)

### Before/afters
| File | What | Review id | Name |
|---|---|---|---|
| 2026-05-21_c-stephens_69feb9a0_0.jpg | BEFORE (labelled), 70s, no makeup; pair with _1. Her review is 4 stars and modest (less dry, no big change yet): don't sell it as dramatic | r-69feb9a0 | C S. |
| 2026-05-21_c-stephens_69feb9a0_1.jpg | AFTER (labelled), 70s; pair with _0 | r-69feb9a0 | C S. |
| Cl4j2keYN.jpg | face before (top) and after (bottom), 60s |  |  |
| R50v5pqz__mid.jpg | face side by side (Pic Stitch), 60s |  |  |
| hP6iXNZpN_mid.jpg | hands side by side (Pic Stitch), 70s |  |  |

### Problem close-ups (rashes, cracked skin, burns: the "before" of a story)
| File | What | Review id |
|---|---|---|
| 5-DexRlZf_mid.jpg | back of a tattooed hand |  |
| ChrIgUM2y_mid.jpg | smooth hand after use |  |
| K-75RqkJY_mid.jpg | palm with a red rash |  |
| W0WH4MJju_mid.jpg | smooth back of a hand |  |
| clsOrFa8o_mid.jpg | cracked red heel |  |
| iJlRfHopF_mid.jpg | red burn/blister on skin |  |
| nlNpV3UE-_mid.jpg | red eczema-like rash on the back of a hand |  |
| pK6cwHOoD_mid.jpg | red rash patch on a tattooed hand |  |

### Product in hand (customer holding the tin)
| File | What | Review id | Name |
|---|---|---|---|
| 2026-04-29_lisa-nicholls_5f40db1b_0.jpg | 60s-70s, holding the S-Balm tin | r-5f40db1b | Lisa N. |
| 2026-05-23_mitzi-chitty_6be40edf_0.jpg | 60s, holding F-Balm Unscented and Face Whip | r-6be40edf | Mitzi C. |
| 2026-05-23_mitzi-chitty_a540b3c4_0.jpg | 60s, holding Freedom Field Balm | r-a540b3c4 | Mitzi C. |
| 2026-08-16_best-body-fitness-main-c_e472abaf_0.jpg | man 40s-50s hiking, holding Field Balm | r-e472abaf | Best M. |
| 2026-09-06_julie-ann-cetinski_6bc5aa25_0.jpg | 40s, holding a tin next to her face | r-6bc5aa25 | Julie-ann C. |
| 2026-10-05_stacey-lee-robson_17749d03_0.jpg | 30s-40s, towel on head, holding F-Balm | r-17749d03 | Stacey L. |
| YpDZ0HV6G.jpg | 50s, F-Balm tin next to her face, big smile |  |  |
| rKhIS2Boj.jpg | 60s, glasses, holding F-Balm in a bathroom |  |  |

Face selfies and lifestyle shots: see `photos.csv` (`kind`, `description` with rough age, `review`).

## Review screenshots: a professional noticed (35)
| Who noticed | Name | Claim | Review id |
|---|---|---|---|
| Dermatologist | Elizabeth J | Dermatologist wanted to know what I was doing at 62 | r-5e37ffa5 |
| Dermatologist | Julie R | Dermatologist said skin looks great at 65 | r-7be0149f |
| Dermatologist | Tracy H | Husbands dermatologist asked what he uses | r-bf43b7c6 |
| Esthetician | Andrea M | Esthetician surprised fewer extractions | s-08c0efa0 |
| Esthetician | Barb M | Esthetician asked if I had laser | r-34009b46 |
| Esthetician | Becky R | Compliments from my esthetician | r-4aa71c12 |
| Esthetician | Christine | Esthetician daughter impressed | r-6d494ae8 |
| Esthetician | Christine H | Facial lady kept saying how great my skin looked | r-bc3835f8 |
| Esthetician | Dea K | Aesthetician said skin looks healthy | r-90a77ef6 |
| Esthetician | Diana B | Aesthetician says skin looking better at 72 | r-54da1c2a |
| Esthetician | Dineen B | Esthetician recommended it | r-7a1c3e76 |
| Esthetician | Mark N | Aesthetician daughter noticed | r-6492d95b |
| Esthetician | Pamela D | Retired esthetician recommends | r-651024bd |
| Esthetician | Shari W | Esthetician 24 years never seen skin like mine at 64 | r-959aa813 |
| Esthetician | Shelley G | Esthetician asked what I was doing differently | r-44708537 |
| Esthetician | Stephanie W | Esthetician noticed elasticity | r-9e3fa319 |
| Esthetician | Susan Z | Aesthetician said great shape for 68 | r-be8f8824 |
| Nurse | Heidi W | Burn nurses want to try it | r-a595499f |
| Nurse | Jacqueline C | Intake nurse said moist skin vs other patients | r-363451c0 |
| Nurse | Jenniffer A | Nurses asked what I use | r-d4f7cd62 |
| Nurse | Roberta K | Dermatology clinic nurse said skin looked great | r-689ec0ff |
| Other Pro | Cecilia M | Hairstylist said no wrinkles at 63 | r-11efe90e |
| Other Pro | Karen H | Physiotherapist noticed | r-b873b0e2 |
| Other Pro | Lois D | Pharmacist would not have thought I was a senior | r-08583301 |
| Other Pro | Shanina P | Wedding makeup artist impressed at 46 | r-4691a6e4 |
| Other Pro | Suzan H | Nail tech noticed | r-0ac22c35 |
| Surgeon or Doctor | Amy C | Noticed at the doctors office | r-0fe59563 |
| Surgeon or Doctor | Carlos R | Moms doctor said scar healed nicely | r-3b6fd970 |
| Surgeon or Doctor | Curtis Q | Doctors and nurses impressed burn healing | r-98c521f4 |
| Surgeon or Doctor | Jamie V | Plastic surgeon amazed | r-5bbb6e5f |
| Surgeon or Doctor | Michele T | Surgeon said scar looks amazing | r-4a465028 |
| Surgeon or Doctor | Paul F | Doctor uses tallow herself | r-500bacb5 |
| Surgeon or Doctor | Ruth L | Doctor asked if I had laser at 63 | r-4843177e |
| Surgeon or Doctor | Sandi M | Plastic surgeon asked what I use at almost 70 | r-b072bac3 |
| Surgeon or Doctor | Terry W | Doctor impressed Field Balm | r-32dbe163 |

## Review screenshots: results (18)
| Name | Claim | Review id |
|---|---|---|
| Barberella H | Upper lip wrinkles disappearing | r-acb0bdac |
| Chantal S | Deep smoker lines diminishing | r-26a6cded |
| Donald B wife | Wrinkles almost gone at 59 vs Botox friends | r-10e4c1bf |
| Donita R | Mouth lines lessened | r-44214f4e |
| Eric C | Son's eczema went away in a week | r-eff6c97e |
| Eric C | Son's eczema went away in a week | r-eff6c97e |
| Jane H | Crepey neck smooth in one week at 51 | r-d951e987 |
| Judy B | Carded at 73 | r-d50f79e6 |
| Laura T | Less wrinkles in 3 weeks at 62 | r-4505767f |
| Linda J | Wrinkles disappearing at 77 | r-655d2c9e |
| Mindy S | Fourth order fewer wrinkles | r-deb473b1 |
| Sandi M | Plastic surgeon | r-b072bac3 |
| Heather H | 69 and people say I look 50 | r-b8261688 |
| Stacey N | Glowing skin compliments | r-4a8fd193 |
| Stacy E | Crepey neck greatly diminished | r-cd4d9f81 |
| Suzy G | Crepey skin on throat disappeared | r-35c9edfe |
| Sylvia W | Mouth wrinkles not as deep in a week | r-4d2a9483 |
| Therese B | Crepeyness almost gone | r-545d9bfb |
