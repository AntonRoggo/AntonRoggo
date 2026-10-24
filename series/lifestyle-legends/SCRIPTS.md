# Lifestyle Legends: scripts

Every script is built **line for line on a winning reel's transcript**. Each table puts the winner's line next to yours, so you can see exactly what each line copies. Each script also has **three hooks**, each copied from a proven hook formula, and you can film any of them. The editing breakdown of each winner is in [BREAKDOWNS.md](BREAKDOWNS.md).

## What the winners actually do

| | Origin Story | Origin Story, short | Guess the Legend | In Their Footsteps |
|---|---|---|---|---|
| **Winner it copies** | [Let's Talk About It](https://www.instagram.com/reel/DaWEza9y-Dg/), 6.0M, 3,241× | [Jon Favreau](https://www.instagram.com/reel/DDSdkJGoVRs/), 5.8M, 556× | [Guess the footballer](https://www.instagram.com/reel/DdjfzUURsA3/), 97K, 12× | [Stevenson Trail](https://www.tiktok.com/@heleneinbetween/video/7646771334520769805), 578K, 65× |
| **Length** | about 2 min | 26 s | 62 s | 99 s |
| **How much story** | One thread: one dream, the thing that killed it, one pivot, proof, the lesson. Five or six facts. | Seven sentences, one setback, one move. | About 12 career steps, one per clause. | Barely any of the legend's life. It's the creator's own experience, with the legend as the reason. |
| **When the name comes** | **First second**: "Jordan Howlett. More popularly known as…" | **First sentence** | **Hidden until 90%**: "By now, you probably know…" | **Named in passing at ~10 s** ("Stevenson's Trail"), paid off at his landmark at ~85 s |

**What changed from the last drafts**
- **Less story.** The old scripts packed 10–14 life events into each video. The winners pick one thread.
- **Name timing.** The Origin Story now says the name in the first line, as the winner does. Hook 2 for each legend keeps the name off the audio, Lens on Legends style; the name tag goes on screen instead. Lens repeats its hook beat later in the story too ("moved back to London alone" at 26–39 s), so the later crash or shell line still works with hook 2.
- **Guess format.** Guess the Legend now copies the winner's actual sentence pattern: present tense, every clause starts with a verb, no ages, then "A ship awaits… This chapter ends when… By now, you probably know…".
- **Footsteps format.** In Their Footsteps is now about *your* experience, copying the Stevenson Trail beats ("No X, no Y, just me…", "Here's how it works", "This is not roughing it", "Standing there, I couldn't believe…", "That's the power of…"). The legend frames it rather than being the story.
- **Short cuts.** A 30-second version of each Origin Story, built on the Favreau winner, for when you want it short. It also works as a text post with no filming.

## How to use this

Each script has a plan in `plans/`, so once you've filmed it the editor can cut it:

```bash
python3 edit_legend.py series/lifestyle-legends/plans/<plan name>.json --draft
```

- Put the footage in `input/<plan name>/`, using the file names under each script.
- The first panel starts at 0 s, so the plan works whichever hook you film.
- In the "On screen" column, **top** is the story panel above you, **full** covers the whole frame, and the bold text is the blue pill label.
- **Lines marked ✎ are personal.** Only say them if they're true for you, or swap in your own version.
- Before posting, check every fact marked ✓. They're from memory and haven't been checked against sources.

**Images.** Hemingway's World War I photos are generally public domain (check each one). Most Cousteau, Chouinard and later Hemingway photos are still under copyright. Use your own footage of places and objects, film yourself holding the book, buy a licence, or use an illustrated scene. Never use a fake photoreal image of a real person.


## Legend 1: Jacques Cousteau

### A. The Origin Story: `cousteau_a_origin`

**Built line for line on:** [Let's Talk About It (@sydney.yancy.ugc)](https://www.instagram.com/reel/DaWEza9y-Dg/), 6.0M views · 3,241× · 10% engagement. The winner runs about 2 min, with the name in the first second. Shape: one dream → the thing that killed it → one pivot → proof → the lesson. Five or six facts, one thread.

**Yours:** 295 words, about 118 s. Look and pacing from [Lens on Legends: Dua Lipa](https://www.instagram.com/reel/DYul8wohxIL/) (259×): a new picture every sentence, uppercase captions, a branded end card. **Film:** One take to camera on the rocks above the sea. Plus two clips of you: swimming in the Med, and an underwater POV with goggles.

**Three hooks.** Film all three; the plan works with any of them.

| # | Hook | Copied from |
|---|---|---|
| 1 | "Jacques Cousteau. Better known as the man in the red cap. He basically invented scuba diving, and he's still the most famous ocean explorer who ever lived." | [Let's Talk About It](https://www.instagram.com/reel/DaWEza9y-Dg/), 6.0M · 3,241×: *[Name]. More popularly known as [nickname]. [Age], [status].* |
| 2 | "At twenty-six, he crashed his car, broke both arms, and lost his dream of flying." | [Lens on Legends: Dua Lipa](https://www.instagram.com/reel/DYul8wohxIL/), 735K · 259×: *At [age], [subject] [did a major life-changing thing].* |
| 3 | "The French Navy knew him as a pilot who'd never fly. The world knows him as Jacques Cousteau." | [Babbu Maan (@currentyug)](https://www.instagram.com/reel/DdZDoR5hjBn/), 2.3M · 67×: *The local community calls them [title], but the world knows them by [name].* |

| Beat | The winner said | You say | On screen |
|---|---|---|---|
| Hook | *Jordan Howlett. More popularly known as Jordan the Stallion. He's 28 years old and easily one of the most recognizable content creators on the planet.* | *(your hook)* | top `portrait.jpg` · **JACQUES COUSTEAU** |
| Personal stake | *And last week I learned a little bit about his background and I can't stop thinking about it, his story is wild.* | And last week I learned what his life looked like before any of that, and I can't stop thinking about it. His story is wild. | you, full screen |
| Series line | *This is Let's Talk About It. A series where I share the unique stories of people who inspire me… So let's talk about it.* | This is Lifestyle Legends, a series where I share the stories of people who lived first and figured out the work later. So let's get into it. | you, full screen |
| The dream | *As a kid Jordan had dreams of being a professional baseball player.* | As a kid, Jacques wanted to fly. | top `naval_aviation.jpg` · **THE DREAM: FLYING** |
| The grind | *In college he was broke and sleeping in a 97 Chevy Suburban but was still playing D1 baseball and being scouted by the MLB.* | He was a sickly kid who got thrown out of school, but he still made it into the French Naval Academy, training to be a pilot. | top `naval_academy.jpg` · **FRENCH NAVAL ACADEMY** |
| The dream dies | *His dream was at his fingertips until COVID came, canceled his final season… and his dream was over.* | His dream was at his fingertips, until a car crash broke both his arms, and his flying career was over before it started. | top `old_car.jpg` · **1936: THE CRASH** |
| The pivot | *Rather than shutting down, he used the experience to make a YouTube documentary called Dear Baseball and emailed 150 people a day to get noticed.* | Rather than giving up, he swam in the Mediterranean every single day to get his arms working again. | full `swim.mp4` · **THE REHAB** |
| The question | *And who was he noticed by? None other than LeBron.* | And who changed everything? A friend, who handed him a pair of swimming goggles. | top `goggles.jpg` · **THE GOGGLES** |
| The breakthrough | *Less than a week later he started creating content revealing the secrets of fast food recipes and he went viral.* | He put his face in the water, saw a world nobody had ever filmed, and a few years later he co-invented the Aqua-Lung so he could stay down there. | full `underwater.mp4`<br>top `aqualung.jpg` · **1943: THE AQUA-LUNG** |
| Proof: a number | *His videos are generating around 90 million views a month.* | Every scuba diver on earth is breathing through a version of that idea. |  |
| Proof: names | *Celebrities like Kevin Hart, Method Man, Donald Glover, Will Smith, Tom Holland have all worked with him… not the other way around.* | He sailed the world on his ship Calypso, won an Oscar and the top prize at Cannes, and a whole generation grew up wanting to explore the ocean because of him. | top `calypso.jpg` · **CALYPSO**<br>top `silent_world.jpg` · **CANNES + OSCAR** |
| The lesson | *Life is going to hand you negative circumstances, career enders, and you can let it define you or you can rewrite your story.* | Life is going to take away the thing you planned on. You can let it end you, or you can put your face in the water and find the next thing. | you, full screen |
| The lesson, part 2 | *In a world that favors instant gratification what really gets results is hard work, determination, tenacity and an unwavering belief in yourself.* | He wanted the sky. He got the whole ocean instead. |  |
| Follow (Lens on Legends) | *Follow Lens on Legends for more untold stories about the icons who didn't just make history, they rewrote the rules to get there.* | Follow for the next legend: the climber who ate cat food and built Patagonia. |  |

End card from "Follow": **LIFESTYLE LEGENDS** / NEXT: YVON CHOUINARD. Lines marked ✎ are personal: say them only if they're true for you, or swap in your version.

<details><summary>Footage and images to gather</summary>

- `01_talk.mp4`: you talking to camera
- `portrait.jpg`: Cousteau in the red cap (check licence) or an illustration
- `naval_aviation.jpg`: 1930s French naval aviation photo
- `naval_academy.jpg`: École navale, 1930s postcard
- `old_car.jpg`: 1930s car on a mountain road
- `swim.mp4`: YOU: swimming in the Mediterranean
- `goggles.jpg`: Vintage swimming goggles on a rock
- `underwater.mp4`: YOU: underwater POV, fish and rocks
- `aqualung.jpg`: Early Aqua-Lung regulator and tanks
- `calypso.jpg`: The ship Calypso
- `silent_world.jpg`: Poster or book cover of The Silent World

</details>

✓ Check before posting: expelled from school (the 17 broken windows story); École navale, training for naval aviation; the 1936 car crash that broke both arms and ended his flying; rehab swimming and the goggles from Philippe Tailliez; Aqua-Lung with Émile Gagnan, 1943; Calypso; The Silent World won the 1956 Palme d'Or and the 1957 Oscar.

### A-short. The Origin Story, short cut: `cousteau_a_short`

**Built line for line on:** [Jon Favreau (@winning.therapy)](https://www.instagram.com/reel/DDSdkJGoVRs/), 5.8M views · 556×. The winner runs 26 s (106 words), with the name in the first sentence. Shape: seven sentences: setup → setback → stuck → decision → the move → 'it wasn't just X' → result and lesson.

**Yours:** 116 words, about 29 s. Post it as a talking head, or as a text post over a clip, like the winner. **Film:** One take to camera, 30 seconds, or post it as a text card over an ocean clip.

**Three hooks.** Film all three; the plan works with any of them.

| # | Hook | Copied from |
|---|---|---|
| 1 | "In 1936, Jacques Cousteau was training to be a navy pilot, thinking his life was set." | [Jon Favreau](https://www.instagram.com/reel/DDSdkJGoVRs/), 5.8M · 556×: *In [year], [person] [got X], thinking it would be [his big break]. But…* |
| 2 | "In 1956, this was the most famous man under the sea. Twenty years earlier, he couldn't lift his arms." | [Alan Bond (@glasshouse.aus)](https://www.instagram.com/reel/DdpupJ_BinY/), 58K · 67×: *In [year], this was the [superlative] man in [place]. [Years] earlier, [opposite].* |
| 3 | "This navy cadet broke both his arms, and ended up inventing scuba diving." | [Rohan Oza (@theventure)](https://www.instagram.com/reel/DcW8st3Rd1p/), 243K · 9.8×: *This [kind of person] [humble start] and built [huge result].* |

| Beat | The winner said | You say | On screen |
|---|---|---|---|
| Setup | *In 1993, Jon Favreau landed a small but memorable role in the hit film Rudy, thinking it would be his big break.* | *(your hook)* | top `portrait_navy.jpg` · **JACQUES COUSTEAU** |
| Setback | *But after the movie's success, work didn't follow.* | But a car crash broke both his arms, and ended it. | top `old_car.jpg` · **THE CRASH** |
| Stuck | *He found himself stuck, unable to land substantial roles, questioning his future in Hollywood.* | He found himself swimming every morning, just to make his arms work again. | full `swim.mp4` |
| Decision | *Frustrated, Favreau decided to take control of his career.* | Then a friend handed him goggles, and he decided that's where his life was going. | top `goggles.jpg` · **THE GOGGLES** |
| The move | *Drawing from his struggles, he wrote Swingers, a low-budget film about friendship, heartbreak, and navigating the grind of Hollywood.* | Drawing on what he saw down there, he co-invented the Aqua-Lung, the scuba tank as we know it. | top `aqualung.jpg` · **THE AQUA-LUNG** |
| Reframe | *It wasn't just a script—it was a lifeline.* | It wasn't just an invention. It was a door into a new world. | full `underwater.mp4` |
| Result and lesson | *By betting on himself, Favreau created a cult classic that launched his career, proving that sometimes the only way forward is to create your own opportunities.* | By following the thing that found him, Cousteau became the most famous ocean explorer ever, proving that sometimes the plan falling apart is the plan. | top `portrait.jpg` · **JACQUES COUSTEAU** |
| Sign-off (ours) | *(none in the winner)* | Follow for more Lifestyle Legends. |  |

End card from "Follow": **LIFESTYLE LEGENDS** / FULL STORY ON THE PAGE. Lines marked ✎ are personal: say them only if they're true for you, or swap in your version.

<details><summary>Footage and images to gather</summary>

- `01_talk.mp4`: you talking to camera
- `portrait_navy.jpg`: Young Cousteau in naval uniform (check licence) or an illustration
- `old_car.jpg`: 1930s car on a mountain road
- `swim.mp4`: YOU: swimming in the sea
- `goggles.jpg`: Vintage swimming goggles
- `aqualung.jpg`: Early Aqua-Lung
- `underwater.mp4`: YOU: underwater POV
- `portrait.jpg`: Cousteau in the red cap

</details>

✓ Check before posting: same facts as the long version.

### B. Guess the Legend: `cousteau_b_guess`

**Built line for line on:** [Guess the footballer (@jackgrimse)](https://www.instagram.com/reel/DdjfzUURsA3/), 97K views · 12×. The winner runs 62 s, with the name hidden until 90% of the way through. Shape: one breathless present-tense run-on. Each clause starts with a verb and is one step. No ages, no pauses.

**Yours:** 182 words, about 59 s. Split screen: clue image on top with a blue pill, you underneath, captions on the seam. **Film:** One take to camera, no pauses. A red cap in your hand is the silent last clue.

**Three hooks.** Film all three; the plan works with any of them.

| # | Hook | Copied from |
|---|---|---|
| 1 | "Can you imagine experiencing this explorer's rollercoaster life," | [Guess the footballer](https://www.instagram.com/reel/DdjfzUURsA3/), 97K · 12×: *Can you imagine experiencing this [type]'s rollercoaster [career]…* |
| 2 | "Can you guess this legend from the story of his life," | [Guess the footballer (caption)](https://www.instagram.com/reel/DdjfzUURsA3/), 97K · 12×: *Can you guess this [type] from the story of their [career]…* |
| 3 | "In the 1920s, nobody knew this sickly French schoolboy would end up famous," | [DiCaprio in Paris (@historic)](https://www.instagram.com/reel/DTL2tXCgGar/), 2.2M · 17.8×: *In [year], a [future legend] [did something ordinary], completely unnoticed…* |

| Beat | The winner said | You say | On screen |
|---|---|---|---|
| Hook | *Can you imagine experiencing this footballer's rollercoaster career,* | *(your hook)* | top `portrait.jpg` (pixelated) · **GUESS THE LEGEND** |
| Hard start | *growing up in government housing after his dad walked out on the family,* | growing up a sickly kid in France who gets thrown out of school for breaking windows, | top `school.jpg` · **THE TROUBLEMAKER** |
| First break | *focuses on football and earns a scholarship to Man City's youth academy,* | saves up for a movie camera and takes it apart to see how it works, | top `camera.jpg` · **FIRST CAMERA** |
| Leaves home | *goes on loan to a London club in search of first-team football,* | joins the navy in search of a life flying planes, | top `naval_aviation.jpg` · **THE NAVY** |
| Struggle, then rise | *struggles to fit in at first, but his game speaks for itself and starts generating national attention,* | makes it through training, but a car crash breaks both his arms and ends it, | top `old_car.jpg` · **THE CRASH** |
| Conflict | *returns to Manchester because of the owner's ego at his loan club,* | swims in the Mediterranean every day just to get his arms working again, | full `swim.mp4` · **THE REHAB** |
| Earns it | *battles for a place in Pep Guardiola's squad and earns a spot in the starting XI by the end of the season,* | borrows a pair of goggles, looks under the water, and decides that's his life now, | top `goggles.jpg` · **THE GOGGLES** |
| Twist | *provides the assist that sends his former club down, but joins permanently in the summer and brings them back to the Premier League.* | helps invent a way to breathe underwater in the middle of a world war, and takes it straight into the same sea. | top `aqualung.jpg` · **THE INVENTION** |
| Peak | *An England call-up awaits, and in the coming seasons he helps his club win the FA Cup… and qualify for the Champions League in the process.* | A ship awaits, and in the coming years he films the ocean like nobody before him, and wins an Oscar and the top prize at Cannes in the process. | top `calypso.jpg` (pixelated) · **THE SHIP** |
| Chapter ends | *This chapter ends when he is sold to FC Barcelona for a club-record fee.* | This chapter ends with a red cap, a TV show, and a whole generation wanting to explore the sea. | top `red_cap.jpg` · **LAST CLUE** |
| Reveal | *By now, you probably know that this is the story of Jamie Tartt.* | By now, you probably know that this is the story of Jacques Cousteau. | top `portrait.jpg` · **JACQUES COUSTEAU** |
| CTA | *Comment below when you figured it out.* | Comment below when you figured it out. |  |

End card from "Comment": **GUESS THE LEGEND** / COMMENT WHEN YOU GOT IT. Lines marked ✎ are personal: say them only if they're true for you, or swap in your version.

<details><summary>Footage and images to gather</summary>

- `01_talk.mp4`: you talking to camera
- `portrait.jpg`: Portrait of Cousteau, face pixelated by the editor
- `school.jpg`: 1920s French school, old postcard
- `camera.jpg`: 1920s home movie camera
- `naval_aviation.jpg`: 1930s naval aviation photo
- `old_car.jpg`: 1930s car on a mountain road
- `swim.mp4`: YOU: swimming in the sea
- `goggles.jpg`: Vintage swimming goggles
- `aqualung.jpg`: Early scuba regulator
- `calypso.jpg`: The ship, name on the hull pixelated
- `red_cap.jpg`: YOU: holding a red wool cap

</details>

✓ Check before posting: same facts as the long version.

### C. In Their Footsteps: `cousteau_c_footsteps`

**Built line for line on:** [Stevenson Trail (@heleneinbetween)](https://www.tiktok.com/@heleneinbetween/video/7646771334520769805), 578K views · 65× · 11% engagement. The winner runs 99 s, with the the legend is the reason, not the subject: named in passing at ~10 s, paid off at his landmark at ~85 s. Shape: contrast hook → 'no X, no Y, just me' → how it works → the day → the senses → 'this is not roughing it' → what changed for me → his landmark → the moral.

**Yours:** 282 words, about 85 s. Full-screen B-roll every 1.5–3 s, you on camera ~25%, big title over the first seconds. **Film:** Two days on the Riviera: Le Mourillon beach in Toulon (selfie with goggles, underwater POV, the old port), then the Oceanographic Museum in Monaco.

**Opening title:** *Following Cousteau / along the Riviera*

**Three hooks.** Film all three; the plan works with any of them.

| # | Hook | Copied from |
|---|---|---|
| 1 | "This is totally normal in the south of France and almost nobody knows it: a free beach where the father of scuba diving first looked under the sea." | [Stevenson Trail](https://www.tiktok.com/@heleneinbetween/video/7646771334520769805), 578K · 65×: *This is totally normal in [place A] and doesn't even exist in [place B].* |
| 2 | "This is one of the most important beaches in the history of the ocean." | [Hever Castle (@history_alice)](https://www.tiktok.com/@history_alice/video/7672324997637082390), 471K · 13×: *This is one of the most important [rooms] in [history].* |
| 3 | "I came to this beach because of a man in a red cap." | [Stevenson Trail (caption)](https://www.tiktok.com/@heleneinbetween/video/7646771334520769805), 578K · 65×: *I picked this [trip] because of a [book].* |

| Beat | The winner said | You say | On screen |
|---|---|---|---|
| Hook | *This is totally normal in Europe and doesn't even exist in the USA: inn-to-inn hiking.* | *(your hook)* |  |
| No X, just me | *No tent, no backpack full of gear, just me, my snacks, my tripod, and 156 miles of France on Stevenson's Trail.* | No boat, no dive shop, no tank. Just me, a pair of goggles, and the beach in Toulon where Jacques Cousteau first looked under the water in 1936. | top `portrait_navy.jpg` · **LE MOURILLON, 1936** |
| How it works | *Here's how it works. You stay in family-run village inns and small hotels along the way.* | Here's how it works. Le Mourillon is a public beach in Toulon, and the rocks start right off the sand. | full `beach.mp4` · **LE MOURILLON, TOULON** |
| How it works, part 2 | *Every morning you leave your bag at reception, a Sherpa service moves all your stuff while you walk with just snacks and water.* | You walk in with goggles, swim out ten metres, put your face down, and that's it. | full `underwater.mp4` |
| The day | *I'd walk anywhere from 8 to 20 miles per day, stopping for picnic lunches of crusty baguettes… and afternoon coffee in village cafés.* | ✎ I'd swim in the morning, eat lunch in the old port, and read about what he saw down here in the afternoon. | full `port.mp4` |
| The evening | *Then I'd arrive at my next village inn, take a hot shower, and enjoy a proper French dinner every single night.* | ✎ Then I'd sit on the harbour wall with a coffee and dry off in the sun. |  |
| The senses | *Walking Stevenson's Trail is like walking through idyllic France, through volcanic plateaus, fields of poppies, past stone houses dripping with climbing roses…* | Swimming here is like looking through a window: fish, rocks covered in weed, light coming down in lines, a whole world two metres under the tourists. | full `underwater2.mp4` |
| Reframe | *This is not roughing it. It was challenging, but getting a hot shower and a five-course French meal every night was magnificent.* | This is not a dive trip. It's a pair of goggles and five minutes, and it changed his whole life. |  |
| Proof | *I loved long-distance walking so much that this was my second one…* | ✎ I swim in this sea almost every day, and I'd never once bothered to look down. | you, full screen |
| The turn | *But here's what really changed my life. Long-distance walking gave me a passion I never knew I had…* | But here's what really got me. He only started swimming because a crash had wrecked his arms, and he needed them back. |  |
| His landmark | *On my final day the trail dropped me… into the town of Saint-Jean-du-Gard, the same village where Robert Louis Stevenson ended his own journey in 1878.* | On my last day I followed the coast to Monaco, to the Oceanographic Museum, the same building Cousteau ran for more than thirty years. | top `museum.mp4` · **OCEANOGRAPHIC MUSEUM, MONACO** |
| The feeling | *Standing there, I couldn't believe what I'd done.* | Standing there, I couldn't believe it all started with a pair of goggles on that little beach. |  |
| Transformation | *Two years ago I'd never call myself a hiker. Now I've walked hundreds of miles, lost 60 pounds…* | ✎ A week ago I'd never put my face in the water. Now I can't stop. | you, full screen |
| The moral | *That's the power of choosing yourself.* | That's the power of looking down. |  |
| Follow (ours) | *(none in the winner)* | Follow for the next legend's footsteps. |  |

End card from "Follow": **LIFESTYLE LEGENDS** / NEXT: CHOUINARD'S SURF RULE. Lines marked ✎ are personal: say them only if they're true for you, or swap in your version.

<details><summary>Footage and images to gather</summary>

- `01_mourillon.mp4`: you talking to camera
- `02_monaco.mp4`: you talking to camera
- `portrait_navy.jpg`: Young Cousteau in naval uniform (check licence) or an illustration
- `beach.mp4`: YOU: walking onto the beach
- `underwater.mp4`: YOU: underwater POV off the rocks
- `port.mp4`: YOU: lunch in Toulon's old port
- `underwater2.mp4`: YOU: more underwater shots
- `museum.mp4`: YOU: walking up to the museum

</details>

✓ Check before posting: Le Mourillon, Toulon as the 1936 goggles beach; director of the Oceanographic Museum of Monaco, 1957–1988.

---

## Legend 2: Yvon Chouinard

### A. The Origin Story: `chouinard_a_origin`

**Built line for line on:** [Let's Talk About It (@sydney.yancy.ugc)](https://www.instagram.com/reel/DaWEza9y-Dg/), 6.0M views · 3,241× · 10% engagement. The winner runs about 2 min, with the name in the first second. Shape: one dream → the thing that killed it → one pivot → proof → the lesson. Five or six facts, one thread.

**Yours:** 284 words, about 114 s. Look and pacing from [Lens on Legends: Dua Lipa](https://www.instagram.com/reel/DYul8wohxIL/) (259×): a new picture every sentence, uppercase captions, a branded end card. **Film:** One take to camera at a crag or a surf break. Plus clips of you: a car boot full of gear, and surfing.

**Three hooks.** Film all three; the plan works with any of them.

| # | Hook | Copied from |
|---|---|---|
| 1 | "Yvon Chouinard. Better known as the man who built Patagonia, then gave the whole three-billion-dollar company away." | [Let's Talk About It](https://www.instagram.com/reel/DaWEza9y-Dg/), 6.0M · 3,241×: *[Name]. More popularly known as [nickname]. [Age], [status].* |
| 2 | "At eighteen, he was living on a dollar a day and eating cat food, just so he could keep climbing." | [Lens on Legends: Dua Lipa](https://www.instagram.com/reel/DYul8wohxIL/), 735K · 259×: *At [age], [subject] [did a major life-changing thing].* |
| 3 | "This broke climber made his own gear in a junkyard forge, and built a three-billion-dollar company." | [Rohan Oza (@theventure)](https://www.instagram.com/reel/DcW8st3Rd1p/), 243K · 9.8×: *This [kind of person] [humble start] and built [huge result].* |

| Beat | The winner said | You say | On screen |
|---|---|---|---|
| Hook | *Jordan Howlett. More popularly known as Jordan the Stallion. He's 28 years old and easily one of the most recognizable content creators on the planet.* | *(your hook)* | top `portrait.jpg` · **YVON CHOUINARD** |
| Personal stake | *And last week I learned a little bit about his background and I can't stop thinking about it, his story is wild.* | And last week I learned what his life looked like before any of that, and I can't stop thinking about it. His story is wild. | you, full screen |
| Series line | *This is Let's Talk About It. A series where I share the unique stories of people who inspire me… So let's talk about it.* | This is Lifestyle Legends, a series where I share the stories of people who lived first and figured out the work later. So let's get into it. | you, full screen |
| The dream | *As a kid Jordan had dreams of being a professional baseball player.* | As a kid, Yvon found climbing, and all he wanted was to live in Yosemite. | top `yosemite.jpg` · **THE DREAM: YOSEMITE** |
| The grind | *In college he was broke and sleeping in a 97 Chevy Suburban but was still playing D1 baseball and being scouted by the MLB.* | He was broke, living on about a dollar a day, sometimes eating dented tins of cat food, but he was still climbing every big wall he could. | top `cat_food.jpg` · **A DOLLAR A DAY** |
| The dream dies | *His dream was at his fingertips until COVID came, canceled his final season… and his dream was over.* | His dream was at his fingertips, but he couldn't afford the gear, and the gear he could buy wasn't good enough for those walls. | top `old_pitons.jpg` · **THE PROBLEM** |
| The pivot | *Rather than shutting down, he used the experience to make a YouTube documentary called Dear Baseball and emailed 150 people a day to get noticed.* | Rather than quitting, he bought a used forge from a junkyard, taught himself to blacksmith, and made his own. | top `forge.jpg` · **THE JUNKYARD FORGE** |
| The question | *And who was he noticed by? None other than LeBron.* | And who wanted them? Everyone he climbed with. | you, full screen |
| The breakthrough | *Less than a week later he started creating content revealing the secrets of fast food recipes and he went viral.* | He sold them out of the back of his car for a dollar fifty each, and by 1970 he was the biggest climbing gear supplier in America. | top `car_boot.mp4` · **$1.50 EACH** |
| Proof: a number | *His videos are generating around 90 million views a month.* | That little gear business turned into Patagonia, worth around three billion dollars. | top `patagonia.jpg` · **PATAGONIA** |
| Proof: names | *Celebrities like Kevin Hart, Method Man, Donald Glover, Will Smith, Tom Holland have all worked with him… not the other way around.* | It ran on one rule: when the surf's up, go surfing. And in 2022 he gave the whole thing away to fight climate change. | full `surf.mp4` · **COMPANY POLICY**<br>top `headline.png` · **2022: GIVES IT AWAY** |
| The lesson | *Life is going to hand you negative circumstances, career enders, and you can let it define you or you can rewrite your story.* | Life is going to tell you to grow up and get serious. You can listen, or you can keep doing the thing you love until it turns into the work. | you, full screen |
| The lesson, part 2 | *In a world that favors instant gratification what really gets results is hard work, determination, tenacity and an unwavering belief in yourself.* | Chouinard never wanted a business. He just wanted to keep climbing. |  |
| Follow (Lens on Legends) | *Follow Lens on Legends for more untold stories about the icons who didn't just make history, they rewrote the rules to get there.* | Follow for the next legend: the writer who got blown up at eighteen and won the Nobel Prize. |  |

End card from "Follow": **LIFESTYLE LEGENDS** / NEXT: ERNEST HEMINGWAY. Lines marked ✎ are personal: say them only if they're true for you, or swap in your version.

<details><summary>Footage and images to gather</summary>

- `01_talk.mp4`: you talking to camera
- `portrait.jpg`: Photo of Chouinard (licensed) or an illustration
- `yosemite.jpg`: El Capitan or Camp 4, old photo
- `cat_food.jpg`: A dented tin of cat food
- `old_pitons.jpg`: Old soft-iron pitons
- `forge.jpg`: An old coal forge and anvil
- `car_boot.mp4`: YOU: opening a car boot full of climbing gear
- `patagonia.jpg`: Patagonia shopfront or logo
- `surf.mp4`: YOU: surfing
- `headline.png`: Screenshot of the news headline

</details>

✓ Check before posting: living on about $1 a day and the cat food story; the used forge from a junkyard (1957); pitons at $1.50 from his car; biggest US climbing hardware supplier by 1970; Patagonia's flextime rule; 2022 transfer, ~$3B; the 'billionaire' and age claims if you add any.

### A-short. The Origin Story, short cut: `chouinard_a_short`

**Built line for line on:** [Jon Favreau (@winning.therapy)](https://www.instagram.com/reel/DDSdkJGoVRs/), 5.8M views · 556×. The winner runs 26 s (106 words), with the name in the first sentence. Shape: seven sentences: setup → setback → stuck → decision → the move → 'it wasn't just X' → result and lesson.

**Yours:** 111 words, about 28 s. Post it as a talking head, or as a text post over a clip, like the winner. **Film:** One take to camera, 30 seconds, or a text card over a climbing or surf clip.

**Three hooks.** Film all three; the plan works with any of them.

| # | Hook | Copied from |
|---|---|---|
| 1 | "In 1957, Yvon Chouinard was a broke climber living in Yosemite, thinking he could climb forever." | [Jon Favreau](https://www.instagram.com/reel/DDSdkJGoVRs/), 5.8M · 556×: *In [year], [person] [got X], thinking it would be [his big break]. But…* |
| 2 | "In 2022, this man gave away a three-billion-dollar company. Sixty-five years earlier, he was eating cat food." | [Alan Bond (@glasshouse.aus)](https://www.instagram.com/reel/DdpupJ_BinY/), 58K · 67×: *In [year], this was the [superlative] man in [place]. [Years] earlier, [opposite].* |
| 3 | "This climber ate cat food to stay in Yosemite, and ended up giving away a three-billion-dollar company." | [Rohan Oza (@theventure)](https://www.instagram.com/reel/DcW8st3Rd1p/), 243K · 9.8×: *This [kind of person] [humble start] and built [huge result].* |

| Beat | The winner said | You say | On screen |
|---|---|---|---|
| Setup | *In 1993, Jon Favreau landed a small but memorable role in the hit film Rudy, thinking it would be his big break.* | *(your hook)* | top `yosemite.jpg` · **YVON CHOUINARD** |
| Setback | *But after the movie's success, work didn't follow.* | But the gear he could afford wasn't good enough for the walls he wanted. | top `old_pitons.jpg` · **THE PROBLEM** |
| Stuck | *He found himself stuck, unable to land substantial roles, questioning his future in Hollywood.* | He found himself living on a dollar a day, sometimes eating cat food. | top `cat_food.jpg` · **A DOLLAR A DAY** |
| Decision | *Frustrated, Favreau decided to take control of his career.* | Frustrated, he decided to make his own. |  |
| The move | *Drawing from his struggles, he wrote Swingers, a low-budget film about friendship, heartbreak, and navigating the grind of Hollywood.* | He bought a used forge from a junkyard, taught himself to blacksmith, and sold gear from his car. | top `forge.jpg` · **THE JUNKYARD FORGE** |
| Reframe | *It wasn't just a script—it was a lifeline.* | It wasn't just gear. It was his ticket to keep climbing. | full `climb.mp4` |
| Result and lesson | *By betting on himself, Favreau created a cult classic that launched his career, proving that sometimes the only way forward is to create your own opportunities.* | By refusing to give up the life he loved, Chouinard built Patagonia, proving that the best businesses start as a way to keep doing what you love. | top `patagonia.jpg` · **PATAGONIA** |
| Sign-off (ours) | *(none in the winner)* | Follow for more Lifestyle Legends. |  |

End card from "Follow": **LIFESTYLE LEGENDS** / FULL STORY ON THE PAGE. Lines marked ✎ are personal: say them only if they're true for you, or swap in your version.

<details><summary>Footage and images to gather</summary>

- `01_talk.mp4`: you talking to camera
- `yosemite.jpg`: El Capitan or Camp 4, old photo
- `old_pitons.jpg`: Old soft-iron pitons
- `cat_food.jpg`: A dented tin of cat food
- `forge.jpg`: An old coal forge and anvil
- `climb.mp4`: YOU: climbing
- `patagonia.jpg`: Patagonia shopfront or logo

</details>

✓ Check before posting: same facts as the long version.

### B. Guess the Legend: `chouinard_b_guess`

**Built line for line on:** [Guess the footballer (@jackgrimse)](https://www.instagram.com/reel/DdjfzUURsA3/), 97K views · 12×. The winner runs 62 s, with the name hidden until 90% of the way through. Shape: one breathless present-tense run-on. Each clause starts with a verb and is one step. No ages, no pauses.

**Yours:** 165 words, about 53 s. Split screen: clue image on top with a blue pill, you underneath, captions on the seam. **Film:** One take to camera in a fleece, outdoors, no pauses.

**Three hooks.** Film all three; the plan works with any of them.

| # | Hook | Copied from |
|---|---|---|
| 1 | "Can you imagine experiencing this climber's rollercoaster life," | [Guess the footballer](https://www.instagram.com/reel/DdjfzUURsA3/), 97K · 12×: *Can you imagine experiencing this [type]'s rollercoaster [career]…* |
| 2 | "Can you guess this legend from the story of his life," | [Guess the footballer (caption)](https://www.instagram.com/reel/DdjfzUURsA3/), 97K · 12×: *Can you guess this [type] from the story of their [career]…* |
| 3 | "In the 1950s, this broke climber was sleeping in the dirt in Yosemite, completely unknown," | [DiCaprio in Paris (@historic)](https://www.instagram.com/reel/DTL2tXCgGar/), 2.2M · 17.8×: *In [year], a [future legend] [did something ordinary], completely unnoticed…* |

| Beat | The winner said | You say | On screen |
|---|---|---|---|
| Hook | *Can you imagine experiencing this footballer's rollercoaster career,* | *(your hook)* | top `portrait.jpg` (pixelated) · **GUESS THE LEGEND** |
| Hard start | *growing up in government housing after his dad walked out on the family,* | growing up a French-speaking outsider at a California school, | top `1940s_california.jpg` · **THE OUTSIDER** |
| First break | *focuses on football and earns a scholarship to Man City's youth academy,* | falls into falconry, which drops him straight into climbing, | top `falcon.jpg` · **FALCONRY** |
| Leaves home | *goes on loan to a London club in search of first-team football,* | heads for Yosemite in search of the biggest walls in America, | top `yosemite.jpg` · **YOSEMITE** |
| Struggle, then rise | *struggles to fit in at first, but his game speaks for itself and starts generating national attention,* | lives on a dollar a day and eats cat food, but his climbing speaks for itself, | top `cat_food.jpg` · **A DOLLAR A DAY** |
| Conflict | *returns to Manchester because of the owner's ego at his loan club,* | can't stand the gear you can buy, so he teaches himself to blacksmith and forges his own, | top `forge.jpg` · **SELF-TAUGHT BLACKSMITH** |
| Earns it | *battles for a place in Pep Guardiola's squad and earns a spot in the starting XI by the end of the season,* | sells it out of the back of his car and ends up running the biggest climbing gear company in America, | top `car_boot.mp4` · **FROM HIS CAR** |
| Twist | *provides the assist that sends his former club down, but joins permanently in the summer and brings them back to the Premier League.* | then quits his best-selling product because it's damaging the rock, and starts selling clothes instead. | top `scarred_rock.jpg` · **QUITS HIS BEST SELLER** |
| Peak | *An England call-up awaits, and in the coming seasons he helps his club win the FA Cup… and qualify for the Champions League in the process.* | A rugby shirt from Scotland awaits, and in the coming decades his clothing company is worth billions, with surfing written into company policy in the process. | top `rugby_shirt.jpg` · **THE RUGBY SHIRT** |
| Chapter ends | *This chapter ends when he is sold to FC Barcelona for a club-record fee.* | This chapter ends when he gives the entire company away to fight climate change. | top `headline.png` (pixelated) · **LAST CLUE** |
| Reveal | *By now, you probably know that this is the story of Jamie Tartt.* | By now, you probably know that this is the story of Yvon Chouinard. | top `portrait.jpg` · **YVON CHOUINARD** |
| CTA | *Comment below when you figured it out.* | Comment below when you figured it out. |  |

End card from "Comment": **GUESS THE LEGEND** / COMMENT WHEN YOU GOT IT. Lines marked ✎ are personal: say them only if they're true for you, or swap in your version.

<details><summary>Footage and images to gather</summary>

- `01_talk.mp4`: you talking to camera
- `portrait.jpg`: Portrait of Chouinard, face pixelated
- `1940s_california.jpg`: 1940s Southern California street
- `falcon.jpg`: A falcon on a glove
- `yosemite.jpg`: El Capitan, old photo
- `cat_food.jpg`: A dented tin of cat food
- `forge.jpg`: An old coal forge and anvil
- `car_boot.mp4`: YOU: car boot full of gear
- `scarred_rock.jpg`: Scarred granite crack
- `rugby_shirt.jpg`: A striped 1970s rugby shirt
- `headline.png`: News headline, company name pixelated

</details>

✓ Check before posting: the 1970 rugby shirt from Scotland that started the clothing line; phasing out pitons because they scarred the rock.

### C. In Their Footsteps: `chouinard_c_footsteps`

**Built line for line on:** [Stevenson Trail (@heleneinbetween)](https://www.tiktok.com/@heleneinbetween/video/7646771334520769805), 578K views · 65× · 11% engagement. The winner runs 99 s, with the the legend is the reason, not the subject: named in passing at ~10 s, paid off at his landmark at ~85 s. Shape: contrast hook → 'no X, no Y, just me' → how it works → the day → the senses → 'this is not roughing it' → what changed for me → his landmark → the moral.

**Yours:** 251 words, about 76 s. Full-screen B-roll every 1.5–3 s, you on camera ~25%, big title over the first seconds. **Film:** A week (or a day) living by the rule: dawn surf, laptop while still salty, an afternoon climb. Film the forecast check on your phone.

**Opening title:** *Living by Patagonia's / one rule*

**Three hooks.** Film all three; the plan works with any of them.

| # | Hook | Copied from |
|---|---|---|
| 1 | "This is totally normal at one company and doesn't exist anywhere else: when the surf's up, you go surfing." | [Stevenson Trail](https://www.tiktok.com/@heleneinbetween/video/7646771334520769805), 578K · 65×: *This is totally normal in [place A] and doesn't even exist in [place B].* |
| 2 | "This is one of the most famous rules in business history, and this week I'm living by it." | [Hever Castle (@history_alice)](https://www.tiktok.com/@history_alice/video/7672324997637082390), 471K · 13×: *This is one of the most important [rooms] in [history].* |
| 3 | "I'm living by this rule this week because of a book." | [Stevenson Trail (caption)](https://www.tiktok.com/@heleneinbetween/video/7646771334520769805), 578K · 65×: *I picked this [trip] because of a [book].* |

| Beat | The winner said | You say | On screen |
|---|---|---|---|
| Hook | *This is totally normal in Europe and doesn't even exist in the USA: inn-to-inn hiking.* | *(your hook)* |  |
| No X, just me | *No tent, no backpack full of gear, just me, my snacks, my tripod, and 156 miles of France on Stevenson's Trail.* | No alarm, no commute, no meetings before ten. Just me, my board, my laptop, and one rule from Yvon Chouinard's book, Let My People Go Surfing. | top `book.jpg` · **LET MY PEOPLE GO SURFING** |
| How it works | *Here's how it works. You stay in family-run village inns and small hotels along the way.* | Here's how it works. You check the surf forecast when you wake up. | full `forecast.mp4` |
| How it works, part 2 | *Every morning you leave your bag at reception, a Sherpa service moves all your stuff while you walk with just snacks and water.* | If it's good, you go. The work waits until you're back, and it gets done around the waves. |  |
| The day | *I'd walk anywhere from 8 to 20 miles per day, stopping for picnic lunches of crusty baguettes… and afternoon coffee in village cafés.* | ✎ I'd surf at dawn, work on the laptop still salty, and go climbing in the afternoon. | full `surf_dawn.mp4`<br>top `laptop.mp4` · **THEN WORK**<br>full `climb.mp4` |
| The evening | *Then I'd arrive at my next village inn, take a hot shower, and enjoy a proper French dinner every single night.* | ✎ Then I'd finish the day's work at sunset, with nothing left on the list. |  |
| The senses | *Walking Stevenson's Trail is like walking through idyllic France, through volcanic plateaus, fields of poppies, past stone houses dripping with climbing roses…* | Living by this rule is like getting your mornings back: cold water, an empty line-up, coffee on the tailgate, the whole day still in front of you. | full `morning_broll.mp4` |
| Reframe | *This is not roughing it. It was challenging, but getting a hot shower and a five-course French meal every night was magnificent.* | ✎ This isn't skipping work. It's harder, honestly, because you have to be done before the wind comes up. | you, full screen |
| Proof | *I loved long-distance walking so much that this was my second one…* | ✎ I did it for a full week. |  |
| The turn | *But here's what really changed my life. Long-distance walking gave me a passion I never knew I had…* | ✎ But here's what really changed my mind. I got more done in four hours than I usually get done in eight. |  |
| His landmark | *On my final day the trail dropped me… into the town of Saint-Jean-du-Gard, the same village where Robert Louis Stevenson ended his own journey in 1878.* | On my last day I reread the chapter where he explains it, the same rule he ran a three-billion-dollar company on, right up until he gave it away. | top `headline.png` · **2022: HE GIVES IT AWAY** |
| The feeling | *Standing there, I couldn't believe what I'd done.* | Sitting there with wet hair, I couldn't believe I'd ever done it the other way. |  |
| Transformation | *Two years ago I'd never call myself a hiker. Now I've walked hundreds of miles, lost 60 pounds…* | ✎ A week ago my mornings belonged to my inbox. Now they belong to the ocean. | you, full screen |
| The moral | *That's the power of choosing yourself.* | That's the power of letting yourself go surfing. |  |
| Follow (ours) | *(none in the winner)* | Follow for the next legend's footsteps. |  |

End card from "Follow": **LIFESTYLE LEGENDS** / NEXT: HEMINGWAY'S PARIS. Lines marked ✎ are personal: say them only if they're true for you, or swap in your version.

<details><summary>Footage and images to gather</summary>

- `01_dawn.mp4`: you talking to camera
- `02_afternoon.mp4`: you talking to camera
- `book.jpg`: YOU: holding the book
- `forecast.mp4`: YOU: checking the forecast on your phone in bed
- `surf_dawn.mp4`: YOU: dawn surf
- `laptop.mp4`: YOU: working on a laptop in a towel
- `climb.mp4`: YOU: climbing
- `morning_broll.mp4`: YOU: line-up, coffee, tailgate
- `headline.png`: Screenshot of the news headline

</details>

✓ Check before posting: Patagonia's flextime policy, explained in Let My People Go Surfing; every ✎ line must be true for you.

---

## Legend 3: Ernest Hemingway

### A. The Origin Story: `hemingway_a_origin`

**Built line for line on:** [Let's Talk About It (@sydney.yancy.ugc)](https://www.instagram.com/reel/DaWEza9y-Dg/), 6.0M views · 3,241× · 10% engagement. The winner runs about 2 min, with the name in the first second. Shape: one dream → the thing that killed it → one pivot → proof → the lesson. Five or six facts, one thread.

**Yours:** 285 words, about 114 s. Look and pacing from [Lens on Legends: Dua Lipa](https://www.instagram.com/reel/DYul8wohxIL/) (259×): a new picture every sentence, uppercase captions, a branded end card. **Film:** One take to camera on a boat or a harbour wall. Plus a clip of you deep-sea fishing or on a boat.

**Three hooks.** Film all three; the plan works with any of them.

| # | Hook | Copied from |
|---|---|---|
| 1 | "Ernest Hemingway. Better known as the man who wrote The Old Man and the Sea. Nobel Prize, Pulitzer Prize, and one of the most famous writers who ever lived." | [Let's Talk About It](https://www.instagram.com/reel/DaWEza9y-Dg/), 6.0M · 3,241×: *[Name]. More popularly known as [nickname]. [Age], [status].* |
| 2 | "At eighteen, he was blown up by a mortar shell in Italy, with more than two hundred pieces of shrapnel in his legs." | [Lens on Legends: Dua Lipa](https://www.instagram.com/reel/DYul8wohxIL/), 735K · 259×: *At [age], [subject] [did a major life-changing thing].* |
| 3 | "Did you know the writer who won the Nobel Prize for a book about fishing actually got blown up in a war at eighteen?" | [Ronaldo, Part 187 (@aoieducation)](https://tiktok.com/@aoieducation/video/7648258694446124296), 3.6M · 8×: *Did you know [subject] who holds [achievement] actually [surprising background]?* |

| Beat | The winner said | You say | On screen |
|---|---|---|---|
| Hook | *Jordan Howlett. More popularly known as Jordan the Stallion. He's 28 years old and easily one of the most recognizable content creators on the planet.* | *(your hook)* | top `portrait_1918.jpg` · **ERNEST HEMINGWAY** |
| Personal stake | *And last week I learned a little bit about his background and I can't stop thinking about it, his story is wild.* | And last week I learned what his life looked like before any of that, and I can't stop thinking about it. His story is wild. | you, full screen |
| Series line | *This is Let's Talk About It. A series where I share the unique stories of people who inspire me… So let's talk about it.* | This is Lifestyle Legends, a series where I share the stories of people who lived first and figured out the work later. So let's get into it. | you, full screen |
| The dream | *As a kid Jordan had dreams of being a professional baseball player.* | As a kid, Ernest grew up hunting and fishing in the Michigan woods, and he wanted adventure more than anything. | top `michigan.jpg` · **THE DREAM: ADVENTURE** |
| The grind | *In college he was broke and sleeping in a 97 Chevy Suburban but was still playing D1 baseball and being scouted by the MLB.* | The army turned him down for a bad eye, but he still got to the war, driving ambulances for the Red Cross in Italy. | top `ambulance.jpg` · **RED CROSS AMBULANCE** |
| The dream dies | *His dream was at his fingertips until COVID came, canceled his final season… and his dream was over.* | His adventure was at his fingertips, until a mortar shell exploded next to him and put more than two hundred pieces of shrapnel in his legs. | top `hospital_1918.jpg` · **1918: WOUNDED** |
| The pivot | *Rather than shutting down, he used the experience to make a YouTube documentary called Dear Baseball and emailed 150 people a day to get noticed.* | Rather than going home and settling down, he went looking for more: broke in Paris, the bulls in Pamplona, marlin fishing off Cuba on his own boat. | top `paris_1920s.jpg` · **BROKE IN PARIS**<br>top `pamplona.jpg` · **PAMPLONA**<br>full `fishing.mp4` · **THE PILAR** |
| The question | *And who was he noticed by? None other than LeBron.* | And what did he do with all of it? He wrote it down. | you, full screen |
| The breakthrough | *Less than a week later he started creating content revealing the secrets of fast food recipes and he went viral.* | The war became A Farewell to Arms. Pamplona became The Sun Also Rises. The Gulf Stream became The Old Man and the Sea. | top `farewell.jpg` · **A FAREWELL TO ARMS**<br>top `sun_also_rises.jpg` · **THE SUN ALSO RISES**<br>top `old_man.jpg` · **THE OLD MAN AND THE SEA** |
| Proof: a number | *His videos are generating around 90 million views a month.* | That last one won him the Pulitzer, and then the Nobel Prize. | top `nobel.jpg` · **1954: NOBEL PRIZE** |
| Proof: names | *Celebrities like Kevin Hart, Method Man, Donald Glover, Will Smith, Tom Holland have all worked with him… not the other way around.* | He even survived two plane crashes in two days, and got to read his own obituaries. | top `obituary.jpg` · **READS HIS OWN OBITUARY** |
| The lesson | *Life is going to hand you negative circumstances, career enders, and you can let it define you or you can rewrite your story.* | Life is going to tell you to wait until you've got something to say. You can wait, or you can go and live something worth saying. | you, full screen |
| The lesson, part 2 | *In a world that favors instant gratification what really gets results is hard work, determination, tenacity and an unwavering belief in yourself.* | Hemingway lived it first. Then he wrote one true sentence about it. |  |
| Follow (Lens on Legends) | *Follow Lens on Legends for more untold stories about the icons who didn't just make history, they rewrote the rules to get there.* | Follow for the next legend. |  |

End card from "Follow": **LIFESTYLE LEGENDS** / NEXT WEEK: A NEW LEGEND. Lines marked ✎ are personal: say them only if they're true for you, or swap in your version.

<details><summary>Footage and images to gather</summary>

- `01_talk.mp4`: you talking to camera
- `portrait_1918.jpg`: Hemingway in uniform in Milan, 1918 (public domain)
- `michigan.jpg`: Michigan lake and woods, early 1900s
- `ambulance.jpg`: WWI Red Cross ambulance in Italy
- `hospital_1918.jpg`: Hemingway in the Milan hospital, 1918 (public domain)
- `paris_1920s.jpg`: Paris café, 1920s
- `pamplona.jpg`: Running of the bulls, 1920s
- `fishing.mp4`: YOU: deep-sea fishing or out on a boat
- `farewell.jpg`: YOU holding a copy
- `sun_also_rises.jpg`: YOU holding a copy
- `old_man.jpg`: YOU holding a copy
- `nobel.jpg`: Nobel medal or 1954 headline
- `obituary.jpg`: 1954 headline reporting him dead

</details>

✓ Check before posting: wounded at Fossalta di Piave, 8 July 1918, aged 18; 'more than two hundred' fragments; rejected by the army for his eyesight; the books-from-life pairings; Pulitzer 1953, Nobel 1954; the two 1954 plane crashes and premature obituaries.

### A-short. The Origin Story, short cut: `hemingway_a_short`

**Built line for line on:** [Jon Favreau (@winning.therapy)](https://www.instagram.com/reel/DDSdkJGoVRs/), 5.8M views · 556×. The winner runs 26 s (106 words), with the name in the first sentence. Shape: seven sentences: setup → setback → stuck → decision → the move → 'it wasn't just X' → result and lesson.

**Yours:** 121 words, about 30 s. Post it as a talking head, or as a text post over a clip, like the winner. **Film:** One take to camera, 30 seconds, or a text card over an old war or ocean clip.

**Three hooks.** Film all three; the plan works with any of them.

| # | Hook | Copied from |
|---|---|---|
| 1 | "In 1918, Ernest Hemingway went to war as an ambulance driver, thinking it would be the adventure of his life." | [Jon Favreau](https://www.instagram.com/reel/DDSdkJGoVRs/), 5.8M · 556×: *In [year], [person] [got X], thinking it would be [his big break]. But…* |
| 2 | "In 1954, this man won the Nobel Prize. Thirty-six years earlier, he was lying in a field in Italy, full of shrapnel." | [Alan Bond (@glasshouse.aus)](https://www.instagram.com/reel/DdpupJ_BinY/), 58K · 67×: *In [year], this was the [superlative] man in [place]. [Years] earlier, [opposite].* |
| 3 | "This eighteen-year-old ambulance driver got blown up in a war, and turned it into the Nobel Prize." | [Rohan Oza (@theventure)](https://www.instagram.com/reel/DcW8st3Rd1p/), 243K · 9.8×: *This [kind of person] [humble start] and built [huge result].* |

| Beat | The winner said | You say | On screen |
|---|---|---|---|
| Setup | *In 1993, Jon Favreau landed a small but memorable role in the hit film Rudy, thinking it would be his big break.* | *(your hook)* | top `portrait_1918.jpg` · **ERNEST HEMINGWAY** |
| Setback | *But after the movie's success, work didn't follow.* | But a mortar shell exploded next to him, and filled his legs with shrapnel. | top `ambulance.jpg` · **1918: WOUNDED** |
| Stuck | *He found himself stuck, unable to land substantial roles, questioning his future in Hollywood.* | He found himself in a Milan hospital, in love with a nurse who'd turn him down by letter. | top `hospital_1918.jpg` · **THE HOSPITAL** |
| Decision | *Frustrated, Favreau decided to take control of his career.* | Instead of going home quiet, he decided to live everything he could. |  |
| The move | *Drawing from his struggles, he wrote Swingers, a low-budget film about friendship, heartbreak, and navigating the grind of Hollywood.* | Drawing on all of it, he wrote it down: the war became A Farewell to Arms. | top `farewell.jpg` · **A FAREWELL TO ARMS** |
| Reframe | *It wasn't just a script—it was a lifeline.* | It wasn't just writing. It was his life, one true sentence at a time. |  |
| Result and lesson | *By betting on himself, Favreau created a cult classic that launched his career, proving that sometimes the only way forward is to create your own opportunities.* | By living it first, Hemingway won the Nobel Prize, proving that the best stories are the ones you go out and get. | top `nobel.jpg` · **1954: NOBEL PRIZE** |
| Sign-off (ours) | *(none in the winner)* | Follow for more Lifestyle Legends. |  |

End card from "Follow": **LIFESTYLE LEGENDS** / FULL STORY ON THE PAGE. Lines marked ✎ are personal: say them only if they're true for you, or swap in your version.

<details><summary>Footage and images to gather</summary>

- `01_talk.mp4`: you talking to camera
- `portrait_1918.jpg`: Hemingway in uniform, 1918 (public domain)
- `ambulance.jpg`: WWI Red Cross ambulance in Italy
- `hospital_1918.jpg`: Hemingway in the Milan hospital, 1918
- `farewell.jpg`: YOU holding a copy
- `nobel.jpg`: Nobel medal or 1954 headline

</details>

✓ Check before posting: the nurse (Agnes von Kurowsky) turning him down by letter; same facts as the long version.

### B. Guess the Legend: `hemingway_b_guess`

**Built line for line on:** [Guess the footballer (@jackgrimse)](https://www.instagram.com/reel/DdjfzUURsA3/), 97K views · 12×. The winner runs 62 s, with the name hidden until 90% of the way through. Shape: one breathless present-tense run-on. Each clause starts with a verb and is one step. No ages, no pauses.

**Yours:** 166 words, about 54 s. Split screen: clue image on top with a blue pill, you underneath, captions on the seam. **Film:** One take to camera, no pauses. A fishing rod or an old typewriter beside you is a nice silent clue.

**Three hooks.** Film all three; the plan works with any of them.

| # | Hook | Copied from |
|---|---|---|
| 1 | "Can you imagine experiencing this writer's rollercoaster life," | [Guess the footballer](https://www.instagram.com/reel/DdjfzUURsA3/), 97K · 12×: *Can you imagine experiencing this [type]'s rollercoaster [career]…* |
| 2 | "Can you guess this legend from the story of his life," | [Guess the footballer (caption)](https://www.instagram.com/reel/DdjfzUURsA3/), 97K · 12×: *Can you guess this [type] from the story of their [career]…* |
| 3 | "In the 1920s, this broke young American walked around Paris completely unknown," | [DiCaprio in Paris (@historic)](https://www.instagram.com/reel/DTL2tXCgGar/), 2.2M · 17.8×: *In [year], a [future legend] [did something ordinary], completely unnoticed…* |

| Beat | The winner said | You say | On screen |
|---|---|---|---|
| Hook | *Can you imagine experiencing this footballer's rollercoaster career,* | *(your hook)* | top `portrait.jpg` (pixelated) · **GUESS THE LEGEND** |
| Hard start | *growing up in government housing after his dad walked out on the family,* | growing up hunting and fishing in the Michigan woods, desperate for adventure, | top `michigan.jpg` · **THE WOODS** |
| First break | *focuses on football and earns a scholarship to Man City's youth academy,* | skips college and lands a job as a newspaper reporter, | top `newsroom.jpg` · **THE REPORTER** |
| Leaves home | *goes on loan to a London club in search of first-team football,* | gets turned down by the army, so goes to war driving ambulances in search of the real thing, | top `ambulance.jpg` · **THE WAR** |
| Struggle, then rise | *struggles to fit in at first, but his game speaks for itself and starts generating national attention,* | gets hit by a mortar shell, but keeps going, and comes home with a medal for bravery, | top `hospital_1918.jpg` (pixelated) · **THE SHELL** |
| Conflict | *returns to Manchester because of the owner's ego at his loan club,* | falls for his nurse, who dumps him by letter, | top `nurse.jpg` · **THE NURSE** |
| Earns it | *battles for a place in Pep Guardiola's squad and earns a spot in the starting XI by the end of the season,* | moves to Paris with no money and writes in cafés every morning, | top `paris_1920s.jpg` · **PARIS** |
| Twist | *provides the assist that sends his former club down, but joins permanently in the summer and brings them back to the Premier League.* | runs with the bulls in Pamplona, then turns the whole trip into a bestselling novel. | top `pamplona.jpg` · **PAMPLONA** |
| Peak | *An England call-up awaits, and in the coming seasons he helps his club win the FA Cup… and qualify for the Champions League in the process.* | A boat awaits, and in the coming years he fishes for marlin off Cuba, survives two plane crashes in two days, and reads his own obituary in the process. | full `fishing.mp4` · **THE BOAT** |
| Chapter ends | *This chapter ends when he is sold to FC Barcelona for a club-record fee.* | This chapter ends when he wins the Nobel Prize for a story about an old fisherman. | top `old_man.jpg` (pixelated) · **LAST CLUE** |
| Reveal | *By now, you probably know that this is the story of Jamie Tartt.* | By now, you probably know that this is the story of Ernest Hemingway. | top `portrait.jpg` · **ERNEST HEMINGWAY** |
| CTA | *Comment below when you figured it out.* | Comment below when you figured it out. |  |

End card from "Comment": **GUESS THE LEGEND** / COMMENT WHEN YOU GOT IT. Lines marked ✎ are personal: say them only if they're true for you, or swap in your version.

<details><summary>Footage and images to gather</summary>

- `01_talk.mp4`: you talking to camera
- `portrait.jpg`: Portrait of Hemingway, face pixelated
- `michigan.jpg`: Michigan lake and woods, early 1900s
- `newsroom.jpg`: 1910s newsroom
- `ambulance.jpg`: WWI Red Cross ambulance
- `hospital_1918.jpg`: Milan hospital, 1918, face pixelated
- `nurse.jpg`: WWI Red Cross nurses
- `paris_1920s.jpg`: Paris café, 1920s
- `pamplona.jpg`: Running of the bulls, 1920s
- `fishing.mp4`: YOU: deep-sea fishing
- `old_man.jpg`: Book cover with the author's name pixelated

</details>

✓ Check before posting: the Italian Silver Medal of Military Valour; same facts as the long version.

### C. In Their Footsteps: `hemingway_c_footsteps`

**Built line for line on:** [Stevenson Trail (@heleneinbetween)](https://www.tiktok.com/@heleneinbetween/video/7646771334520769805), 578K views · 65× · 11% engagement. The winner runs 99 s, with the the legend is the reason, not the subject: named in passing at ~10 s, paid off at his landmark at ~85 s. Shape: contrast hook → 'no X, no Y, just me' → how it works → the day → the senses → 'this is not roughing it' → what changed for me → his landmark → the moral.

**Yours:** 276 words, about 84 s. Full-screen B-roll every 1.5–3 s, you on camera ~25%, big title over the first seconds. **Film:** A few days in Paris on the A Moveable Feast route: 74 rue du Cardinal Lemoine (the plaque), writing in a café, the Luxembourg Gardens, Shakespeare and Company, and a last morning at La Closerie des Lilas.

**Opening title:** *Writing like broke / Hemingway in Paris*

**Three hooks.** Film all three; the plan works with any of them.

| # | Hook | Copied from |
|---|---|---|
| 1 | "This is totally normal in Paris and doesn't exist anywhere else: you can still sit and write in the café where Hemingway wrote his first novel." | [Stevenson Trail](https://www.tiktok.com/@heleneinbetween/video/7646771334520769805), 578K · 65×: *This is totally normal in [place A] and doesn't even exist in [place B].* |
| 2 | "This is one of the most important café tables in the history of books." | [Hever Castle (@history_alice)](https://www.tiktok.com/@history_alice/video/7672324997637082390), 471K · 13×: *This is one of the most important [rooms] in [history].* |
| 3 | "I came to Paris because of one sentence from Hemingway." | [Stevenson Trail (caption)](https://www.tiktok.com/@heleneinbetween/video/7646771334520769805), 578K · 65×: *I picked this [trip] because of a [book].* |

| Beat | The winner said | You say | On screen |
|---|---|---|---|
| Hook | *This is totally normal in Europe and doesn't even exist in the USA: inn-to-inn hiking.* | *(your hook)* |  |
| No X, just me | *No tent, no backpack full of gear, just me, my snacks, my tripod, and 156 miles of France on Stevenson's Trail.* | No laptop, no phone, no plan. Just me, a notebook, and the Paris that Ernest Hemingway lived in when he was twenty-two and broke. | top `hemingway_hadley.jpg` · **PARIS, 1921** |
| How it works | *Here's how it works. You stay in family-run village inns and small hotels along the way.* | Here's how it works. You start at his first apartment, 74 rue du Cardinal Lemoine, where he lived with no hot water. | full `apartment.mp4` · **74 RUE DU CARDINAL LEMOINE** |
| How it works, part 2 | *Every morning you leave your bag at reception, a Sherpa service moves all your stuff while you walk with just snacks and water.* | Then you walk to a café, order one coffee, and do what he did: write one true sentence, then the next one. | top `cafe_writing.mp4` · **ONE TRUE SENTENCE** |
| The day | *I'd walk anywhere from 8 to 20 miles per day, stopping for picnic lunches of crusty baguettes… and afternoon coffee in village cafés.* | ✎ I'd write all morning, walk the Luxembourg Gardens at lunch like he did when he was too broke to eat, and spend the afternoon at Shakespeare and Company. | full `gardens.mp4`<br>top `bookshop.mp4` · **SHAKESPEARE AND COMPANY** |
| The evening | *Then I'd arrive at my next village inn, take a hot shower, and enjoy a proper French dinner every single night.* | Then I'd stop writing while I still knew what came next, like he said to, so the next morning was easy. | you, full screen |
| The senses | *Walking Stevenson's Trail is like walking through idyllic France, through volcanic plateaus, fields of poppies, past stone houses dripping with climbing roses…* | Walking his Paris is like walking through his book: zinc bars, chestnut trees, the river, old men playing chess in the gardens. | full `paris_broll.mp4` |
| Reframe | *This is not roughing it. It was challenging, but getting a hot shower and a five-course French meal every night was magnificent.* | This isn't a tourist trail. It's a notebook and a city, and it's exactly what made him. |  |
| Proof | *I loved long-distance walking so much that this was my second one…* | ✎ I wrote more in those few days than I have all year. | you, full screen |
| The turn | *But here's what really changed my life. Long-distance walking gave me a passion I never knew I had…* | But here's what really got me. He wasn't waiting for a big life to write about. He was out getting one. |  |
| His landmark | *On my final day the trail dropped me… into the town of Saint-Jean-du-Gard, the same village where Robert Louis Stevenson ended his own journey in 1878.* | On my last morning I sat at La Closerie des Lilas, the same café where Hemingway wrote much of his first novel. | top `closerie.mp4` · **LA CLOSERIE DES LILAS** |
| The feeling | *Standing there, I couldn't believe what I'd done.* | Sitting there, I couldn't believe it was still just a café. |  |
| Transformation | *Two years ago I'd never call myself a hiker. Now I've walked hundreds of miles, lost 60 pounds…* | ✎ A week ago I hadn't written anything in years. Now I've got a notebook full. | you, full screen |
| The moral | *That's the power of choosing yourself.* | That's the power of one true sentence. |  |
| Follow (ours) | *(none in the winner)* | Follow for the next legend's footsteps. |  |

End card from "Follow": **LIFESTYLE LEGENDS** / NEXT WEEK: A NEW LEGEND. Lines marked ✎ are personal: say them only if they're true for you, or swap in your version.

<details><summary>Footage and images to gather</summary>

- `01_street.mp4`: you talking to camera
- `02_closerie.mp4`: you talking to camera
- `hemingway_hadley.jpg`: Ernest and Hadley Hemingway, early 1920s (check licence)
- `apartment.mp4`: YOU: in front of the building and its plaque
- `cafe_writing.mp4`: YOU: writing in a notebook at a café
- `gardens.mp4`: YOU: walking the Luxembourg Gardens
- `bookshop.mp4`: YOU: outside and inside the bookshop
- `paris_broll.mp4`: YOU: Paris B-roll
- `closerie.mp4`: YOU: at a table at La Closerie des Lilas

</details>

✓ Check before posting: 74 rue du Cardinal Lemoine flat with no hot water; writing much of The Sun Also Rises at La Closerie des Lilas; walking the Luxembourg Gardens when hungry (A Moveable Feast); Sylvia Beach's original Shakespeare and Company was at 12 rue de l'Odéon; today's shop on the Seine is a later one that carries the name, so don't say he went to that one; every ✎ line must be true for you.

---

## The bench: Ep 04 and beyond

| | Legend | Why they fit | Data signal |
|---|---|---|---|
| 1 | **Robert Louis Stevenson** | Sickly kid from a family of lighthouse engineers. Trained as a lawyer and never really practised. Walked the Cévennes with a donkey, then wrote *Treasure Island*. | His trail *is* the Stevenson Trail winner (65×, 11% engagement), so the In Their Footsteps version would copy it almost exactly. The trail is in France. |
| 2 | **Jack London** | Oyster pirate at 15, sailor, hobo and gold-rusher, then a bestselling author who learned to surf at Waikiki. | A *Call of the Wild* film-clip reel did 53.7M views (15×). |
| 3 | **Ian Fleming** | Failed at everything his family wanted, then wrote James Bond at 43 after a morning swim in Jamaica. | Bond has the biggest name recognition. |
| 4 | **Anthony Bourdain** | Line cook into his 40s; *Kitchen Confidential* at 44. His first oyster in France changed his life. | A Bourdain tribute reel did 3.2M views (9×). His death needs care: never make it the twist. |

The older London and Fleming drafts didn't follow the winner templates, so I took them out. They're still in git history, and I'll rewrite them on these templates when one of them is up next.
