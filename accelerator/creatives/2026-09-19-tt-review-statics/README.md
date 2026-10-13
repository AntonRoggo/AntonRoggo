# TT review statics: 4 styles x 8 customer quotes (2026-09-19)

32 finals, 1856 x 2304 PNG (4:5), in four folders by format. Uploaded to Drive: finished / 1 - Sticky Note, 2 - Megaphone, 3 - Email Card, 4 - Caption Strips (https://drive.google.com/drive/folders/1fiRq-UzPdU71Z99gG78qozVS93k77uIk).

## Method
Higgsfield, Nano Banana 2, 2k, 4:5, one credit pair per image (2 credits). Each image is a text edit of the operator's own September 12 original, not a fresh generation, so the style holds:
- Sticky note: text-removed base 4c0505f9, quote handwritten onto the blank note.
- Megaphone: text-removed base d021015f, then a label-corrected base 94b8c398 (see below).
- Email card: text-removed base e0e4b15e.
- Caption strips: original 87efdce4, strip wording replaced.
Prompt shape: [SOURCE] / [TRANSFORMATION] / [TYPOGRAPHY] / [NEGATIVE], quote given verbatim with "reads exactly," line breaks specified for the strips.

## Quotes (verbatim from the review export)
q1 "I'm 59 and my wrinkles have almost disappeared!! I look way better than my Botoxed friends lol!"
q2 "After four days my Mom thought I had gone to my Botox appt."
q3 "I find this beef tallow works exactly like Botox. It is a miracle without the costly price and the toxins of Botox."
q4 "I have a deep forehead crease that is almost gone with 1 weeks use"
q5 "I'M 71 AND PEOPLE DON'T BELIEVE ME... THEY ALWAYS ASK WHAT I USE, AND ARE ALWAYS SURPRISED WHEN I TELL THEM ABOUT YOUR BEEF TALLOW PRODUCT!" (full on the email card; cut to "...WHAT I USE" elsewhere)
q6 "Has taken 5 years off my face. Crows feet gone."
q7 "My upper lip I have deep smoker lines and they are diminishing! I'm so happy I use it day and night."
q8 the 63-year-old smoker review (full on the email card; cut to "I am a 63 year old woman who always smoked... My skin has never felt and looked better." elsewhere)

## What proofreading caught (all fixed; rejects are in _superseded/)
- The sticky-note base carries a footer typo, "Individual experiences very." Three outputs inherited it; repaired to "vary."
- The megaphone base's small jar label has been misspelled since September ("thetallowedtrutk.com," "Freadum"), and the model re-garbled it differently each time ("net vegan"). Fixed the base once using the sticky-note jar as a label reference, then rebuilt all eight from it.
- One megaphone output printed the prompt instruction "(with no full stop)" on the ad; one doubled "they are." Both redone. Lesson: never put a formatting instruction next to the caption text; state "exactly two pieces of text."
- Minor, left as is: caption-strips q6 has no quotation marks; email q8 has no space after the second ellipsis.

## Reuse
The label-corrected megaphone base (job 94b8c398) should replace d021015f for any future megaphone variants. ledger.tsv has the first-pass job IDs; finals differ for all megaphone files and sticky q1, q7, q8.
