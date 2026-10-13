# Surgical adaptation v2: "Hey Siri, what do dentists secretly use" → "Hey Siri, why did my skincare stop working at 50"

Supersedes [[2026-09-14-tt-hey-siri-dermatologist-adaptation]]. Changes in v2: operator's two hooks, the required line "normal dermatologists will never tell you," and the mechanism written as the exact-oil version. Everything else preserved from v1's analysis.

---

## Phase 1: Surgical analysis

### Preserve exactly
Same list as v1: the Hey Siri open and "not exactly what I expected at all"; the apology-for-your-own-face beat; the stop, the look, the lean-in whisper, "I'm probably not supposed to"; "intrigued but also kind of scared"; the nod at the posters, "they sponsor stuff, whatever"; "if those actually worked, why is it every single time you come back in here"; "okay, yeah, that's a good point"; "it just keeps coming back"; "it has to be [X]"; "get your phone out of your bag, write this down"; the bib/towel beat; the car lookup; "people my age saying the exact same thing, they had photos"; "not some $800 treatment"; the three-step results ladder; friends asking; the return visit and the wink; "at our age is no joke"; official site, not Amazon.

### Angle-specific modifications (v2 deltas only)
- Hook: dentist secret → "why did my skincare stop working when I turned 50" (V1) and "why did my skin suddenly turn super dry when I hit 50" (V3).
- "I'm probably not supposed to" → "Normal dermatologists will never tell you this." Said by the aesthetician at the whisper.
- "A toothbrush they're technically not allowed to point you to" → "a tin of beef tallow that normal dermatologists will never tell you about." The phrase repeats at the reveal, the way the source repeats "secretly use."
- Mechanism, exact-oil version: your skin makes its own oil, sebum; after 50 it barely makes any; the cream is 70 to 80% water and sits on top; beef tallow is almost the exact same oil your skin makes, so your skin absorbs it like its own.
- "Why is every time you come back your skin is drier and I'm looking at the same lines" now also answers V1: "that's why your creams stopped working, they were never doing anything but sitting there."

### Replacements required
Same as v1: 55% off and the bonuses → guarantee plus "cheaper than the $57 cream I was replacing"; strokes per minute, 99.9%, two shades, Today Show → 15,000 reviews with photos, made in-house, "lines look softer" at three days. No invented skin numbers.

## Phase 2: Change justification (v2 deltas)

| Original text | Change | Reason | Source |
|---|---|---|---|
| "what's the thing dentists secretly use to keep their own teeth clean and white" | V1 "why did my skincare stop working when I turned 50" | Operator's hook; tried-everything lane (488 reviews); dryness lane is 1.13x | "I've used many expensive creams over the years. Now this is all I use" [C173] |
| same | V3 "why did my skin suddenly turn super dry when I hit 50" | Operator's hook, kept as the bold variant with the test-data flag | Dryness 3,231 reviews, menopause 58 |
| "can I tell you something? I'm probably not supposed to." | "Can I tell you something? Normal dermatologists will never tell you this." | Required phrase | Operator |
| "it's a toothbrush they're technically not allowed to point you to" | "it's a tin of beef tallow that normal dermatologists will never tell you about" | Phrase repeats at the reveal | Operator |
| "7,000 or 8,000 strokes, push it around, don't lift it off... has to be sonic, 40,000" | "your skin makes its own oil, sebum... after 50 it barely makes any... the cream is 70 to 80 percent water, sits on top... beef tallow is almost the exact same oil your skin makes, so your skin absorbs it like its own" | Exact-oil mechanism | "79 years old and guess what, you do not produce oil anymore" [raw]; $57 winner; operator's bio-identical line |
| "why is every time you come back in here I'm scraping plaque" | "why is every time you come back in here your skin is drier and I'm looking at the same lines? Your creams stopped working because they were never doing anything but sitting there." | Answers V1 inside the hold | Dry patches 270, fine lines 536 |

## Phase 3: Execution

**HOOKS**

V1: Hey Siri, why did my skincare stop working when I turned 50?

V2: Hey Siri, what's the thing dermatologists secretly use to keep their own skin from aging?

V3: Hey Siri, why did my skin suddenly turn super dry when I hit 50?

**HOLD**

I actually found the answer to that question, and it was not exactly what I expected at all.

Last week I was at the dermatologist getting a facial, and they do this thing where you kind of apologize for your own face. You know, like, overthinking it all morning long. And now finally I'm laying there and I'm like, okay, sorry. I know. And she says, these lines are deeper than they were last time I saw you. And you've lost your glow. And I swear, I swear, I moisturize twice a day.

(Line checked 2026-09-16 against reviews and Reddit. "Your skin's gotten quite thin, the lines are starting to set" was cut: thin skin is a 70+ arms complaint, "set in" is Botox-injector language. "Lost your glow" and "deeper" are customer words.)

The aesthetician stops. She gets this look on her face. And she leans in all close and whispers something like, can I tell you something? Normal dermatologists will never tell you this.

And I'm like, what, uh, what's going on? Because I'm intrigued but also kind of scared.

Then she kind of nods around at all the posters and the brochures on the countertop over there. All the big skincare brands. They've got signs for those guys because, you know, they sponsor stuff, whatever. And she goes, you see all these creams I'm supposed to recommend? Let me ask you something. If those actually worked, why is it every single time you come back in here, your skin is drier and I'm looking at the same lines?

And I just kind of lay there like, okay. Yeah. That's a good point.

She ends up explaining it to me like this. She goes, your skin makes its own oil. It's called sebum. That's what kept your face soft your whole life. And after 50, it barely makes any. Now, even those expensive creams, the ones everybody has, the first ingredient is water. 70 to 80 percent of the jar. So the water sits on top of your skin and evaporates, and the dryness just keeps coming back. Your creams stopped working because they were never doing anything but sitting there. That's why she's looking at the same dry patches and the same lines every time I come in.

She tells me what actually works is putting the oil back. It has to be an oil your skin recognizes as its own. And beef tallow is almost the exact same oil your skin makes, so your skin absorbs it like it made it. Same thing she uses on her own face, she told me. I am not kidding, she stopped mid-facial, get your phone out of your bag, write this down. The Tallowed Truth. F-Balm.

And I'm laying there with the towel still wrapped around my hair, like, what is even happening right now?

So I get out to the car and look it up. You guys. I'm scrolling, like, how have I never heard of this brand before? Seriously do not know how. It has got over 15,000 five-star reviews, and people my age were all saying the exact same thing I've been feeling for, like, forever. They had photos. It's made in-house in Canada, five ingredients, and one woman three days in wrote, "Lines look softer."

So it turns out the thing dermatologists secretly use, it's not some $800 treatment. It's a tin of beef tallow that normal dermatologists will never tell you about. That is just so wild to me.

So, yeah. I ordered it. The first night I used it, I woke up and my skin didn't feel dry or tight. That hadn't happened in, like, ever. So I kept going, morning and night, gave it a couple more weeks, and the lines I'm talking about, the ones I apologize for every single visit, they're starting to look softer. And my skin finally felt soft again. Like, all day long, not just right after I put it on.

About a month in, a couple of my friends are asking me if I got Botox or what. And I'm like, no. I just found a moisturizer that actually works.

And I cannot forget to tell you this. I go back for my next appointment, the ones I always dreaded, like spending all morning preparing for, and the same aesthetician looks at my skin, barely says anything, and gives me a little wink.

So make sure you get to their site. There's a money-back guarantee, so honestly this is cheaper than the $57 cream I was replacing every few months anyway that wasn't doing what I needed it to do. They were sold out for a bit but it's back in stock.

Seriously, I had to share this with you because skin at our age is no joke, and it was giving me more and more anxiety every time I looked in the mirror, and it only gets drier from here.

You have to use the link below. Just make sure it is the OFFICIAL Tallowed Truth site. It cannot be an Amazon knockoff. Those are bleached and they don't work.

Related: [[the-tallowed-truth]] [[2026-09-14-tt-hey-siri-dermatologist-adaptation]] [[2026-09-13-test-results-review]]
