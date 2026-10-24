"""Generate series/lifestyle-legends/SCRIPTS.md and plans/*.json from one source.

Run from anywhere: python3 series/lifestyle-legends/tools/gen_scripts.py

Every script is built line for line on a winning reel's transcript: each line
of ours sits next to the winner's line it copies. Every script has three
hooks taken from proven winning hooks. Panel cue words are checked against the
script with the editor's own word matcher, for all three hooks, so the plan
works whichever hook you film.
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO))
from edit_legend import find_word  # noqa: E402

SERIES = "Lifestyle Legends"
CENSOR = [0.25, 0.05, 0.5, 0.5]

# --- the winning reels each script copies --------------------------------------
SKELETONS = {
    "lets_talk": dict(
        name="Let's Talk About It (@sydney.yancy.ugc)", url="https://www.instagram.com/reel/DaWEza9y-Dg/",
        stats="6.0M views · 3,241× · 10% engagement", length="about 2 min", wps=2.5,
        reveal="name in the first second",
        shape="one dream → the thing that killed it → one pivot → proof → the lesson. Five or six facts, one thread",
        look="Look and pacing from [Lens on Legends: Dua Lipa](https://www.instagram.com/reel/DYul8wohxIL/) (259×): a new picture every sentence, uppercase captions, a branded end card"),
    "favreau": dict(
        name="Jon Favreau (@winning.therapy)", url="https://www.instagram.com/reel/DDSdkJGoVRs/",
        stats="5.8M views · 556×", length="26 s (106 words)", wps=4.0,
        reveal="name in the first sentence",
        shape="seven sentences: setup → setback → stuck → decision → the move → 'it wasn't just X' → result and lesson",
        look="Post it as a talking head, or as a text post over a clip, like the winner"),
    "guess": dict(
        name="Guess the footballer (@jackgrimse)", url="https://www.instagram.com/reel/DdjfzUURsA3/",
        stats="97K views · 12×", length="62 s", wps=3.1,
        reveal="name hidden until 90% of the way through",
        shape="one breathless present-tense run-on. Each clause starts with a verb and is one step. No ages, no pauses",
        look="Split screen: clue image on top with a blue pill, you underneath, captions on the seam"),
    "helene": dict(
        name="Stevenson Trail (@heleneinbetween)", url="https://www.tiktok.com/@heleneinbetween/video/7646771334520769805",
        stats="578K views · 65× · 11% engagement", length="99 s", wps=3.3,
        reveal="the legend is the reason, not the subject: named in passing at ~10 s, paid off at his landmark at ~85 s",
        shape="contrast hook → 'no X, no Y, just me' → how it works → the day → the senses → 'this is not roughing it' → what changed for me → his landmark → the moral",
        look="Full-screen B-roll every 1.5–3 s, you on camera ~25%, big title over the first seconds"),
}

# --- proven hooks (madlib, reel, link, stats) ----------------------------------
HOOKS = {
    "lets_talk": ("[Name]. More popularly known as [nickname]. [Age], [status].",
                  "Let's Talk About It", "https://www.instagram.com/reel/DaWEza9y-Dg/", "6.0M · 3,241×"),
    "lens": ("At [age], [subject] [did a major life-changing thing].",
             "Lens on Legends: Dua Lipa", "https://www.instagram.com/reel/DYul8wohxIL/", "735K · 259×"),
    "babbu": ("The local community calls them [title], but the world knows them by [name].",
              "Babbu Maan (@currentyug)", "https://www.instagram.com/reel/DdZDoR5hjBn/", "2.3M · 67×"),
    "aoi": ("Did you know [subject] who holds [achievement] actually [surprising background]?",
            "Ronaldo, Part 187 (@aoieducation)", "https://tiktok.com/@aoieducation/video/7648258694446124296", "3.6M · 8×"),
    "favreau": ("In [year], [person] [got X], thinking it would be [his big break]. But…",
                "Jon Favreau", "https://www.instagram.com/reel/DDSdkJGoVRs/", "5.8M · 556×"),
    "bond": ("In [year], this was the [superlative] man in [place]. [Years] earlier, [opposite].",
             "Alan Bond (@glasshouse.aus)", "https://www.instagram.com/reel/DdpupJ_BinY/", "58K · 67×"),
    "venture": ("This [kind of person] [humble start] and built [huge result].",
                "Rohan Oza (@theventure)", "https://www.instagram.com/reel/DcW8st3Rd1p/", "243K · 9.8×"),
    "guess": ("Can you imagine experiencing this [type]'s rollercoaster [career]…",
              "Guess the footballer", "https://www.instagram.com/reel/DdjfzUURsA3/", "97K · 12×"),
    "guess_caption": ("Can you guess this [type] from the story of their [career]…",
                      "Guess the footballer (caption)", "https://www.instagram.com/reel/DdjfzUURsA3/", "97K · 12×"),
    "historic": ("In [year], a [future legend] [did something ordinary], completely unnoticed…",
                 "DiCaprio in Paris (@historic)", "https://www.instagram.com/reel/DTL2tXCgGar/", "2.2M · 17.8×"),
    "helene": ("This is totally normal in [place A] and doesn't even exist in [place B].",
               "Stevenson Trail", "https://www.tiktok.com/@heleneinbetween/video/7646771334520769805", "578K · 65×"),
    "alice": ("This is one of the most important [rooms] in [history].",
              "Hever Castle (@history_alice)", "https://www.tiktok.com/@history_alice/video/7672324997637082390", "471K · 13×"),
    "helene_caption": ("I picked this [trip] because of a [book].",
                       "Stevenson Trail (caption)", "https://www.tiktok.com/@heleneinbetween/video/7646771334520769805", "578K · 65×"),
}

# --- the winners' lines, beat by beat ------------------------------------------
LETS_TALK = [
    ("Hook", "Jordan Howlett. More popularly known as Jordan the Stallion. He's 28 years old and easily one of the most recognizable content creators on the planet."),
    ("Personal stake", "And last week I learned a little bit about his background and I can't stop thinking about it, his story is wild."),
    ("Series line", "This is Let's Talk About It. A series where I share the unique stories of people who inspire me… So let's talk about it."),
    ("The dream", "As a kid Jordan had dreams of being a professional baseball player."),
    ("The grind", "In college he was broke and sleeping in a 97 Chevy Suburban but was still playing D1 baseball and being scouted by the MLB."),
    ("The dream dies", "His dream was at his fingertips until COVID came, canceled his final season… and his dream was over."),
    ("The pivot", "Rather than shutting down, he used the experience to make a YouTube documentary called Dear Baseball and emailed 150 people a day to get noticed."),
    ("The question", "And who was he noticed by? None other than LeBron."),
    ("The breakthrough", "Less than a week later he started creating content revealing the secrets of fast food recipes and he went viral."),
    ("Proof: a number", "His videos are generating around 90 million views a month."),
    ("Proof: names", "Celebrities like Kevin Hart, Method Man, Donald Glover, Will Smith, Tom Holland have all worked with him… not the other way around."),
    ("The lesson", "Life is going to hand you negative circumstances, career enders, and you can let it define you or you can rewrite your story."),
    ("The lesson, part 2", "In a world that favors instant gratification what really gets results is hard work, determination, tenacity and an unwavering belief in yourself."),
    ("Follow (Lens on Legends)", "Follow Lens on Legends for more untold stories about the icons who didn't just make history, they rewrote the rules to get there."),
]
FAVREAU = [
    ("Setup", "In 1993, Jon Favreau landed a small but memorable role in the hit film Rudy, thinking it would be his big break."),
    ("Setback", "But after the movie's success, work didn't follow."),
    ("Stuck", "He found himself stuck, unable to land substantial roles, questioning his future in Hollywood."),
    ("Decision", "Frustrated, Favreau decided to take control of his career."),
    ("The move", "Drawing from his struggles, he wrote Swingers, a low-budget film about friendship, heartbreak, and navigating the grind of Hollywood."),
    ("Reframe", "It wasn't just a script—it was a lifeline."),
    ("Result and lesson", "By betting on himself, Favreau created a cult classic that launched his career, proving that sometimes the only way forward is to create your own opportunities."),
    ("Sign-off (ours)", "(none in the winner)"),
]
GUESS = [
    ("Hook", "Can you imagine experiencing this footballer's rollercoaster career,"),
    ("Hard start", "growing up in government housing after his dad walked out on the family,"),
    ("First break", "focuses on football and earns a scholarship to Man City's youth academy,"),
    ("Leaves home", "goes on loan to a London club in search of first-team football,"),
    ("Struggle, then rise", "struggles to fit in at first, but his game speaks for itself and starts generating national attention,"),
    ("Conflict", "returns to Manchester because of the owner's ego at his loan club,"),
    ("Earns it", "battles for a place in Pep Guardiola's squad and earns a spot in the starting XI by the end of the season,"),
    ("Twist", "provides the assist that sends his former club down, but joins permanently in the summer and brings them back to the Premier League."),
    ("Peak", "An England call-up awaits, and in the coming seasons he helps his club win the FA Cup… and qualify for the Champions League in the process."),
    ("Chapter ends", "This chapter ends when he is sold to FC Barcelona for a club-record fee."),
    ("Reveal", "By now, you probably know that this is the story of Jamie Tartt."),
    ("CTA", "Comment below when you figured it out."),
]
HELENE = [
    ("Hook", "This is totally normal in Europe and doesn't even exist in the USA: inn-to-inn hiking."),
    ("No X, just me", "No tent, no backpack full of gear, just me, my snacks, my tripod, and 156 miles of France on Stevenson's Trail."),
    ("How it works", "Here's how it works. You stay in family-run village inns and small hotels along the way."),
    ("How it works, part 2", "Every morning you leave your bag at reception, a Sherpa service moves all your stuff while you walk with just snacks and water."),
    ("The day", "I'd walk anywhere from 8 to 20 miles per day, stopping for picnic lunches of crusty baguettes… and afternoon coffee in village cafés."),
    ("The evening", "Then I'd arrive at my next village inn, take a hot shower, and enjoy a proper French dinner every single night."),
    ("The senses", "Walking Stevenson's Trail is like walking through idyllic France, through volcanic plateaus, fields of poppies, past stone houses dripping with climbing roses…"),
    ("Reframe", "This is not roughing it. It was challenging, but getting a hot shower and a five-course French meal every night was magnificent."),
    ("Proof", "I loved long-distance walking so much that this was my second one…"),
    ("The turn", "But here's what really changed my life. Long-distance walking gave me a passion I never knew I had…"),
    ("His landmark", "On my final day the trail dropped me… into the town of Saint-Jean-du-Gard, the same village where Robert Louis Stevenson ended his own journey in 1878."),
    ("The feeling", "Standing there, I couldn't believe what I'd done."),
    ("Transformation", "Two years ago I'd never call myself a hiker. Now I've walked hundreds of miles, lost 60 pounds…"),
    ("The moral", "That's the power of choosing yourself."),
    ("Follow (ours)", "(none in the winner)"),
]
WINNERS = {"lets_talk": LETS_TALK, "favreau": FAVREAU, "guess": GUESS, "helene": HELENE}
VERSIONS = {"lets_talk": ("A", "The Origin Story"), "favreau": ("A-short", "The Origin Story, short cut"),
            "guess": ("B", "Guess the Legend"), "helene": ("C", "In Their Footsteps")}


def top(at, file, label, desc, **extra):
    return {"at": at, "file": file, "label": label, "desc": desc, **extra}


def full(at, file="talk", label=None, desc=None, **extra):
    d = {"at": at, "full": file, "desc": desc, **extra}
    if label:
        d["label"] = label
    return d


SERIES_LINE = ("This is Lifestyle Legends, a series where I share the stories of people "
               "who lived first and figured out the work later. So let's get into it.")
STAKE = "And last week I learned what his life looked like before any of that, and I can't stop thinking about it. His story is wild."
ME = "✎ "   # a personal line: say it only if it's true for you, or swap in your version

SCRIPTS = [
# =============================================================== COUSTEAU
dict(id="cousteau_a_origin", legend="Jacques Cousteau", ep="Ep 01", skeleton="lets_talk",
     film="One take to camera on the rocks above the sea. Plus two clips of you: swimming in the Med, and an underwater POV with goggles.",
     talk=["01_talk.mp4"], highlight=["fly", "goggles", "Calypso", "Oscar", "ocean", "sky"],
     hooks=[("Jacques Cousteau. Better known as the man in the red cap. He basically invented scuba diving, and he's still the most famous ocean explorer who ever lived.", "lets_talk"),
            ("At twenty-six, he crashed his car, broke both arms, and lost his dream of flying.", "lens"),
            ("The French Navy knew him as a pilot who'd never fly. The world knows him as Jacques Cousteau.", "babbu")],
     lines=[
        [top(0, "portrait.jpg", "Jacques Cousteau", "Cousteau in the red cap (check licence) or an illustration")],
        (STAKE, [full("learned")]),
        (SERIES_LINE, [full("series")]),
        ("As a kid, Jacques wanted to fly.", [top("kid", "naval_aviation.jpg", "The dream: flying", "1930s French naval aviation photo")]),
        ("He was a sickly kid who got thrown out of school, but he still made it into the French Naval Academy, training to be a pilot.",
         [top("sickly", "naval_academy.jpg", "French Naval Academy", "École navale, 1930s postcard")]),
        ("His dream was at his fingertips, until a car crash broke both his arms, and his flying career was over before it started.",
         [top("fingertips", "old_car.jpg", "1936: the crash", "1930s car on a mountain road")]),
        ("Rather than giving up, he swam in the Mediterranean every single day to get his arms working again.",
         [full("Rather", "swim.mp4", "The rehab", "YOU: swimming in the Mediterranean")]),
        ("And who changed everything? A friend, who handed him a pair of swimming goggles.",
         [top("changed", "goggles.jpg", "The goggles", "Vintage swimming goggles on a rock")]),
        ("He put his face in the water, saw a world nobody had ever filmed, and a few years later he co-invented the Aqua-Lung so he could stay down there.",
         [full("put", "underwater.mp4", desc="YOU: underwater POV, fish and rocks"),
          top("later", "aqualung.jpg", "1943: the Aqua-Lung", "Early Aqua-Lung regulator and tanks")]),
        ("Every scuba diver on earth is breathing through a version of that idea.", []),
        ("He sailed the world on his ship Calypso, won an Oscar and the top prize at Cannes, and a whole generation grew up wanting to explore the ocean because of him.",
         [top("sailed", "calypso.jpg", "Calypso", "The ship Calypso"),
          top("Oscar", "silent_world.jpg", "Cannes + Oscar", "Poster or book cover of The Silent World")]),
        ("Life is going to take away the thing you planned on. You can let it end you, or you can put your face in the water and find the next thing.",
         [full("Life")]),
        ("He wanted the sky. He got the whole ocean instead.", []),
        ("Follow for the next legend: the climber who ate cat food and built Patagonia.", []),
     ],
     end_card=dict(at="Follow", title=SERIES, sub="Next: Yvon Chouinard"),
     verify=["expelled from school (the 17 broken windows story)", "École navale, training for naval aviation",
             "the 1936 car crash that broke both arms and ended his flying", "rehab swimming and the goggles from Philippe Tailliez",
             "Aqua-Lung with Émile Gagnan, 1943", "Calypso; The Silent World won the 1956 Palme d'Or and the 1957 Oscar"]),

dict(id="cousteau_a_short", legend="Jacques Cousteau", ep="Ep 01 · short", skeleton="favreau",
     film="One take to camera, 30 seconds, or post it as a text card over an ocean clip.",
     talk=["01_talk.mp4"], highlight=["goggles", "Aqua-Lung", "ocean"],
     hooks=[("In 1936, Jacques Cousteau was training to be a navy pilot, thinking his life was set.", "favreau"),
            ("In 1956, this was the most famous man under the sea. Twenty years earlier, he couldn't lift his arms.", "bond"),
            ("This navy cadet broke both his arms, and ended up inventing scuba diving.", "venture")],
     lines=[
        [top(0, "portrait_navy.jpg", "Jacques Cousteau", "Young Cousteau in naval uniform (check licence) or an illustration")],
        ("But a car crash broke both his arms, and ended it.", [top("crash", "old_car.jpg", "The crash", "1930s car on a mountain road")]),
        ("He found himself swimming every morning, just to make his arms work again.", [full("found", "swim.mp4", desc="YOU: swimming in the sea")]),
        ("Then a friend handed him goggles, and he decided that's where his life was going.", [top("friend", "goggles.jpg", "The goggles", "Vintage swimming goggles")]),
        ("Drawing on what he saw down there, he co-invented the Aqua-Lung, the scuba tank as we know it.", [top("Drawing", "aqualung.jpg", "The Aqua-Lung", "Early Aqua-Lung")]),
        ("It wasn't just an invention. It was a door into a new world.", [full("door", "underwater.mp4", desc="YOU: underwater POV")]),
        ("By following the thing that found him, Cousteau became the most famous ocean explorer ever, proving that sometimes the plan falling apart is the plan.",
         [top("following", "portrait.jpg", "Jacques Cousteau", "Cousteau in the red cap")]),
        ("Follow for more Lifestyle Legends.", []),
     ],
     end_card=dict(at="Follow", title=SERIES, sub="Full story on the page"),
     verify=["same facts as the long version"]),

dict(id="cousteau_b_guess", legend="Jacques Cousteau", ep="Guess who #1", skeleton="guess",
     film="One take to camera, no pauses. A red cap in your hand is the silent last clue.",
     talk=["01_talk.mp4"], highlight=["goggles", "Oscar", "Cannes"],
     hooks=[("Can you imagine experiencing this explorer's rollercoaster life,", "guess"),
            ("Can you guess this legend from the story of his life,", "guess_caption"),
            ("In the 1920s, nobody knew this sickly French schoolboy would end up famous,", "historic")],
     lines=[
        [top(0, "portrait.jpg", "Guess the legend", "Portrait of Cousteau, face pixelated by the editor", censor=CENSOR)],
        ("growing up a sickly kid in France who gets thrown out of school for breaking windows,", [top("growing", "school.jpg", "The troublemaker", "1920s French school, old postcard")]),
        ("saves up for a movie camera and takes it apart to see how it works,", [top("saves", "camera.jpg", "First camera", "1920s home movie camera")]),
        ("joins the navy in search of a life flying planes,", [top("joins", "naval_aviation.jpg", "The navy", "1930s naval aviation photo")]),
        ("makes it through training, but a car crash breaks both his arms and ends it,", [top("training", "old_car.jpg", "The crash", "1930s car on a mountain road")]),
        ("swims in the Mediterranean every day just to get his arms working again,", [full("swims", "swim.mp4", "The rehab", "YOU: swimming in the sea")]),
        ("borrows a pair of goggles, looks under the water, and decides that's his life now,", [top("borrows", "goggles.jpg", "The goggles", "Vintage swimming goggles")]),
        ("helps invent a way to breathe underwater in the middle of a world war, and takes it straight into the same sea.", [top("helps", "aqualung.jpg", "The invention", "Early scuba regulator")]),
        ("A ship awaits, and in the coming years he films the ocean like nobody before him, and wins an Oscar and the top prize at Cannes in the process.",
         [top("ship", "calypso.jpg", "The ship", "The ship, name on the hull pixelated", censor=[0.0, 0.3, 1.0, 0.3])]),
        ("This chapter ends with a red cap, a TV show, and a whole generation wanting to explore the sea.", [top("chapter", "red_cap.jpg", "Last clue", "YOU: holding a red wool cap")]),
        ("By now, you probably know that this is the story of Jacques Cousteau.", [top("By", "portrait.jpg", "Jacques Cousteau", "The same portrait, no pixelation")]),
        ("Comment below when you figured it out.", []),
     ],
     end_card=dict(at="Comment", title="Guess the Legend", sub="Comment when you got it"),
     verify=["same facts as the long version"]),

dict(id="cousteau_c_footsteps", legend="Jacques Cousteau", ep="Ep 01 · In his footsteps", skeleton="helene",
     film="Two days on the Riviera: Le Mourillon beach in Toulon (selfie with goggles, underwater POV, the old port), then the Oceanographic Museum in Monaco.",
     talk=["01_mourillon.mp4", "02_monaco.mp4"], highlight=["goggles", "ocean"],
     title=dict(text="Following Cousteau\nalong the Riviera", until="Here's"),
     hooks=[("This is totally normal in the south of France and almost nobody knows it: a free beach where the father of scuba diving first looked under the sea.", "helene"),
            ("This is one of the most important beaches in the history of the ocean.", "alice"),
            ("I came to this beach because of a man in a red cap.", "helene_caption")],
     lines=[
        [],
        ("No boat, no dive shop, no tank. Just me, a pair of goggles, and the beach in Toulon where Jacques Cousteau first looked under the water in 1936.",
         [top("Jacques", "portrait_navy.jpg", "Le Mourillon, 1936", "Young Cousteau in naval uniform (check licence) or an illustration")]),
        ("Here's how it works. Le Mourillon is a public beach in Toulon, and the rocks start right off the sand.", [full("Here's", "beach.mp4", "Le Mourillon, Toulon", "YOU: walking onto the beach")]),
        ("You walk in with goggles, swim out ten metres, put your face down, and that's it.", [full("walk", "underwater.mp4", desc="YOU: underwater POV off the rocks")]),
        (ME + "I'd swim in the morning, eat lunch in the old port, and read about what he saw down here in the afternoon.", [full("eat", "port.mp4", desc="YOU: lunch in Toulon's old port")]),
        (ME + "Then I'd sit on the harbour wall with a coffee and dry off in the sun.", []),
        ("Swimming here is like looking through a window: fish, rocks covered in weed, light coming down in lines, a whole world two metres under the tourists.", [full("window", "underwater2.mp4", desc="YOU: more underwater shots")]),
        ("This is not a dive trip. It's a pair of goggles and five minutes, and it changed his whole life.", []),
        (ME + "I swim in this sea almost every day, and I'd never once bothered to look down.", [full("bothered")]),
        ("But here's what really got me. He only started swimming because a crash had wrecked his arms, and he needed them back.", []),
        ("On my last day I followed the coast to Monaco, to the Oceanographic Museum, the same building Cousteau ran for more than thirty years.",
         [top("Monaco", "museum.mp4", "Oceanographic Museum, Monaco", "YOU: walking up to the museum")]),
        ("Standing there, I couldn't believe it all started with a pair of goggles on that little beach.", []),
        (ME + "A week ago I'd never put my face in the water. Now I can't stop.", [full("week")]),
        ("That's the power of looking down.", []),
        ("Follow for the next legend's footsteps.", []),
     ],
     end_card=dict(at="Follow", title=SERIES, sub="Next: Chouinard's surf rule"),
     verify=["Le Mourillon, Toulon as the 1936 goggles beach", "director of the Oceanographic Museum of Monaco, 1957–1988"]),

# =============================================================== CHOUINARD
dict(id="chouinard_a_origin", legend="Yvon Chouinard", ep="Ep 02", skeleton="lets_talk",
     film="One take to camera at a crag or a surf break. Plus clips of you: a car boot full of gear, and surfing.",
     talk=["01_talk.mp4"], highlight=["climb", "cat", "forge", "Patagonia", "surf's"],
     hooks=[("Yvon Chouinard. Better known as the man who built Patagonia, then gave the whole three-billion-dollar company away.", "lets_talk"),
            ("At eighteen, he was living on a dollar a day and eating cat food, just so he could keep climbing.", "lens"),
            ("This broke climber made his own gear in a junkyard forge, and built a three-billion-dollar company.", "venture")],
     lines=[
        [top(0, "portrait.jpg", "Yvon Chouinard", "Photo of Chouinard (licensed) or an illustration")],
        (STAKE, [full("learned")]),
        (SERIES_LINE, [full("series")]),
        ("As a kid, Yvon found climbing, and all he wanted was to live in Yosemite.", [top("kid", "yosemite.jpg", "The dream: Yosemite", "El Capitan or Camp 4, old photo")]),
        ("He was broke, living on about a dollar a day, sometimes eating dented tins of cat food, but he was still climbing every big wall he could.",
         [top("dented", "cat_food.jpg", "A dollar a day", "A dented tin of cat food")]),
        ("His dream was at his fingertips, but he couldn't afford the gear, and the gear he could buy wasn't good enough for those walls.",
         [top("fingertips", "old_pitons.jpg", "The problem", "Old soft-iron pitons")]),
        ("Rather than quitting, he bought a used forge from a junkyard, taught himself to blacksmith, and made his own.",
         [top("Rather", "forge.jpg", "The junkyard forge", "An old coal forge and anvil")]),
        ("And who wanted them? Everyone he climbed with.", [full("wanted")]),
        ("He sold them out of the back of his car for a dollar fifty each, and by 1970 he was the biggest climbing gear supplier in America.",
         [top("sold", "car_boot.mp4", "$1.50 each", "YOU: opening a car boot full of climbing gear")]),
        ("That little gear business turned into Patagonia, worth around three billion dollars.", [top("business", "patagonia.jpg", "Patagonia", "Patagonia shopfront or logo")]),
        ("It ran on one rule: when the surf's up, go surfing. And in 2022 he gave the whole thing away to fight climate change.",
         [full("ran", "surf.mp4", "Company policy", "YOU: surfing"), top("climate", "headline.png", "2022: gives it away", "Screenshot of the news headline")]),
        ("Life is going to tell you to grow up and get serious. You can listen, or you can keep doing the thing you love until it turns into the work.", [full("Life")]),
        ("Chouinard never wanted a business. He just wanted to keep climbing.", []),
        ("Follow for the next legend: the writer who got blown up at eighteen and won the Nobel Prize.", []),
     ],
     end_card=dict(at="Follow", title=SERIES, sub="Next: Ernest Hemingway"),
     verify=["living on about $1 a day and the cat food story", "the used forge from a junkyard (1957)",
             "pitons at $1.50 from his car", "biggest US climbing hardware supplier by 1970",
             "Patagonia's flextime rule", "2022 transfer, ~$3B", "the 'billionaire' and age claims if you add any"]),

dict(id="chouinard_a_short", legend="Yvon Chouinard", ep="Ep 02 · short", skeleton="favreau",
     film="One take to camera, 30 seconds, or a text card over a climbing or surf clip.",
     talk=["01_talk.mp4"], highlight=["cat", "forge", "Patagonia"],
     hooks=[("In 1957, Yvon Chouinard was a broke climber living in Yosemite, thinking he could climb forever.", "favreau"),
            ("In 2022, this man gave away a three-billion-dollar company. Sixty-five years earlier, he was eating cat food.", "bond"),
            ("This climber ate cat food to stay in Yosemite, and ended up giving away a three-billion-dollar company.", "venture")],
     lines=[
        [top(0, "yosemite.jpg", "Yvon Chouinard", "El Capitan or Camp 4, old photo")],
        ("But the gear he could afford wasn't good enough for the walls he wanted.", [top("afford", "old_pitons.jpg", "The problem", "Old soft-iron pitons")]),
        ("He found himself living on a dollar a day, sometimes eating cat food.", [top("found", "cat_food.jpg", "A dollar a day", "A dented tin of cat food")]),
        ("Frustrated, he decided to make his own.", []),
        ("He bought a used forge from a junkyard, taught himself to blacksmith, and sold gear from his car.", [top("junkyard", "forge.jpg", "The junkyard forge", "An old coal forge and anvil")]),
        ("It wasn't just gear. It was his ticket to keep climbing.", [full("ticket", "climb.mp4", desc="YOU: climbing")]),
        ("By refusing to give up the life he loved, Chouinard built Patagonia, proving that the best businesses start as a way to keep doing what you love.",
         [top("refusing", "patagonia.jpg", "Patagonia", "Patagonia shopfront or logo")]),
        ("Follow for more Lifestyle Legends.", []),
     ],
     end_card=dict(at="Follow", title=SERIES, sub="Full story on the page"),
     verify=["same facts as the long version"]),

dict(id="chouinard_b_guess", legend="Yvon Chouinard", ep="Guess who #2", skeleton="guess",
     film="One take to camera in a fleece, outdoors, no pauses.",
     talk=["01_talk.mp4"], highlight=["cat"],
     hooks=[("Can you imagine experiencing this climber's rollercoaster life,", "guess"),
            ("Can you guess this legend from the story of his life,", "guess_caption"),
            ("In the 1950s, this broke climber was sleeping in the dirt in Yosemite, completely unknown,", "historic")],
     lines=[
        [top(0, "portrait.jpg", "Guess the legend", "Portrait of Chouinard, face pixelated", censor=CENSOR)],
        ("growing up a French-speaking outsider at a California school,", [top("growing", "1940s_california.jpg", "The outsider", "1940s Southern California street")]),
        ("falls into falconry, which drops him straight into climbing,", [top("falls", "falcon.jpg", "Falconry", "A falcon on a glove")]),
        ("heads for Yosemite in search of the biggest walls in America,", [top("heads", "yosemite.jpg", "Yosemite", "El Capitan, old photo")]),
        ("lives on a dollar a day and eats cat food, but his climbing speaks for itself,", [top("lives", "cat_food.jpg", "A dollar a day", "A dented tin of cat food")]),
        ("can't stand the gear you can buy, so he teaches himself to blacksmith and forges his own,", [top("stand", "forge.jpg", "Self-taught blacksmith", "An old coal forge and anvil")]),
        ("sells it out of the back of his car and ends up running the biggest climbing gear company in America,", [top("sells", "car_boot.mp4", "From his car", "YOU: car boot full of gear")]),
        ("then quits his best-selling product because it's damaging the rock, and starts selling clothes instead.", [top("quits", "scarred_rock.jpg", "Quits his best seller", "Scarred granite crack")]),
        ("A rugby shirt from Scotland awaits, and in the coming decades his clothing company is worth billions, with surfing written into company policy in the process.",
         [top("rugby", "rugby_shirt.jpg", "The rugby shirt", "A striped 1970s rugby shirt")]),
        ("This chapter ends when he gives the entire company away to fight climate change.", [top("chapter", "headline.png", "Last clue", "News headline, company name pixelated", censor=[0.0, 0.0, 1.0, 0.4])]),
        ("By now, you probably know that this is the story of Yvon Chouinard.", [top("By", "portrait.jpg", "Yvon Chouinard", "The same portrait, no pixelation")]),
        ("Comment below when you figured it out.", []),
     ],
     end_card=dict(at="Comment", title="Guess the Legend", sub="Comment when you got it"),
     verify=["the 1970 rugby shirt from Scotland that started the clothing line", "phasing out pitons because they scarred the rock"]),

dict(id="chouinard_c_footsteps", legend="Yvon Chouinard", ep="Ep 02 · In his footsteps", skeleton="helene",
     film="A week (or a day) living by the rule: dawn surf, laptop while still salty, an afternoon climb. Film the forecast check on your phone.",
     talk=["01_dawn.mp4", "02_afternoon.mp4"], highlight=["surf's", "surfing"],
     title=dict(text="Living by Patagonia's\none rule", until="Here's"),
     hooks=[("This is totally normal at one company and doesn't exist anywhere else: when the surf's up, you go surfing.", "helene"),
            ("This is one of the most famous rules in business history, and this week I'm living by it.", "alice"),
            ("I'm living by this rule this week because of a book.", "helene_caption")],
     lines=[
        [],
        ("No alarm, no commute, no meetings before ten. Just me, my board, my laptop, and one rule from Yvon Chouinard's book, Let My People Go Surfing.",
         [top("Yvon", "book.jpg", "Let My People Go Surfing", "YOU: holding the book")]),
        ("Here's how it works. You check the surf forecast when you wake up.", [full("Here's", "forecast.mp4", desc="YOU: checking the forecast on your phone in bed")]),
        ("If it's good, you go. The work waits until you're back, and it gets done around the waves.", []),
        (ME + "I'd surf at dawn, work on the laptop still salty, and go climbing in the afternoon.",
         [full("dawn", "surf_dawn.mp4", desc="YOU: dawn surf"), top("laptop", "laptop.mp4", "Then work", "YOU: working on a laptop in a towel"),
          full("climbing", "climb.mp4", desc="YOU: climbing")]),
        (ME + "Then I'd finish the day's work at sunset, with nothing left on the list.", []),
        ("Living by this rule is like getting your mornings back: cold water, an empty line-up, coffee on the tailgate, the whole day still in front of you.",
         [full("mornings", "morning_broll.mp4", desc="YOU: line-up, coffee, tailgate")]),
        (ME + "This isn't skipping work. It's harder, honestly, because you have to be done before the wind comes up.", [full("skipping")]),
        (ME + "I did it for a full week.", []),
        (ME + "But here's what really changed my mind. I got more done in four hours than I usually get done in eight.", []),
        ("On my last day I reread the chapter where he explains it, the same rule he ran a three-billion-dollar company on, right up until he gave it away.",
         [top("reread", "headline.png", "2022: he gives it away", "Screenshot of the news headline")]),
        ("Sitting there with wet hair, I couldn't believe I'd ever done it the other way.", []),
        (ME + "A week ago my mornings belonged to my inbox. Now they belong to the ocean.", [full("inbox")]),
        ("That's the power of letting yourself go surfing.", []),
        ("Follow for the next legend's footsteps.", []),
     ],
     end_card=dict(at="Follow", title=SERIES, sub="Next: Hemingway's Paris"),
     verify=["Patagonia's flextime policy, explained in Let My People Go Surfing", "every ✎ line must be true for you"]),

# =============================================================== HEMINGWAY
dict(id="hemingway_a_origin", legend="Ernest Hemingway", ep="Ep 03", skeleton="lets_talk",
     film="One take to camera on a boat or a harbour wall. Plus a clip of you deep-sea fishing or on a boat.",
     talk=["01_talk.mp4"], highlight=["adventure", "shrapnel", "Nobel", "obituaries", "true"],
     hooks=[("Ernest Hemingway. Better known as the man who wrote The Old Man and the Sea. Nobel Prize, Pulitzer Prize, and one of the most famous writers who ever lived.", "lets_talk"),
            ("At eighteen, he was blown up by a mortar shell in Italy, with more than two hundred pieces of shrapnel in his legs.", "lens"),
            ("Did you know the writer who won the Nobel Prize for a book about fishing actually got blown up in a war at eighteen?", "aoi")],
     lines=[
        [top(0, "portrait_1918.jpg", "Ernest Hemingway", "Hemingway in uniform in Milan, 1918 (public domain)")],
        (STAKE, [full("learned")]),
        (SERIES_LINE, [full("series")]),
        ("As a kid, Ernest grew up hunting and fishing in the Michigan woods, and he wanted adventure more than anything.", [top("kid", "michigan.jpg", "The dream: adventure", "Michigan lake and woods, early 1900s")]),
        ("The army turned him down for a bad eye, but he still got to the war, driving ambulances for the Red Cross in Italy.", [top("army", "ambulance.jpg", "Red Cross ambulance", "WWI Red Cross ambulance in Italy")]),
        ("His adventure was at his fingertips, until a mortar shell exploded next to him and put more than two hundred pieces of shrapnel in his legs.",
         [top("fingertips", "hospital_1918.jpg", "1918: wounded", "Hemingway in the Milan hospital, 1918 (public domain)")]),
        ("Rather than going home and settling down, he went looking for more: broke in Paris, the bulls in Pamplona, marlin fishing off Cuba on his own boat.",
         [top("Rather", "paris_1920s.jpg", "Broke in Paris", "Paris café, 1920s"), top("bulls", "pamplona.jpg", "Pamplona", "Running of the bulls, 1920s"),
          full("marlin", "fishing.mp4", "The Pilar", "YOU: deep-sea fishing or out on a boat")]),
        ("And what did he do with all of it? He wrote it down.", [full("what")]),
        ("The war became A Farewell to Arms. Pamplona became The Sun Also Rises. The Gulf Stream became The Old Man and the Sea.",
         [top("Farewell", "farewell.jpg", "A Farewell to Arms", "YOU holding a copy"), top("Sun", "sun_also_rises.jpg", "The Sun Also Rises", "YOU holding a copy"),
          top("Gulf", "old_man.jpg", "The Old Man and the Sea", "YOU holding a copy")]),
        ("That last one won him the Pulitzer, and then the Nobel Prize.", [top("last", "nobel.jpg", "1954: Nobel Prize", "Nobel medal or 1954 headline")]),
        ("He even survived two plane crashes in two days, and got to read his own obituaries.", [top("survived", "obituary.jpg", "Reads his own obituary", "1954 headline reporting him dead")]),
        ("Life is going to tell you to wait until you've got something to say. You can wait, or you can go and live something worth saying.", [full("Life")]),
        ("Hemingway lived it first. Then he wrote one true sentence about it.", []),
        ("Follow for the next legend.", []),
     ],
     end_card=dict(at="Follow", title=SERIES, sub="Next week: a new legend"),
     verify=["wounded at Fossalta di Piave, 8 July 1918, aged 18", "'more than two hundred' fragments", "rejected by the army for his eyesight",
             "the books-from-life pairings", "Pulitzer 1953, Nobel 1954", "the two 1954 plane crashes and premature obituaries"]),

dict(id="hemingway_a_short", legend="Ernest Hemingway", ep="Ep 03 · short", skeleton="favreau",
     film="One take to camera, 30 seconds, or a text card over an old war or ocean clip.",
     talk=["01_talk.mp4"], highlight=["shrapnel", "Nobel"],
     hooks=[("In 1918, Ernest Hemingway went to war as an ambulance driver, thinking it would be the adventure of his life.", "favreau"),
            ("In 1954, this man won the Nobel Prize. Thirty-six years earlier, he was lying in a field in Italy, full of shrapnel.", "bond"),
            ("This eighteen-year-old ambulance driver got blown up in a war, and turned it into the Nobel Prize.", "venture")],
     lines=[
        [top(0, "portrait_1918.jpg", "Ernest Hemingway", "Hemingway in uniform, 1918 (public domain)")],
        ("But a mortar shell exploded next to him, and filled his legs with shrapnel.", [top("mortar", "ambulance.jpg", "1918: wounded", "WWI Red Cross ambulance in Italy")]),
        ("He found himself in a Milan hospital, in love with a nurse who'd turn him down by letter.", [top("found", "hospital_1918.jpg", "The hospital", "Hemingway in the Milan hospital, 1918")]),
        ("Instead of going home quiet, he decided to live everything he could.", []),
        ("Drawing on all of it, he wrote it down: the war became A Farewell to Arms.", [top("Drawing", "farewell.jpg", "A Farewell to Arms", "YOU holding a copy")]),
        ("It wasn't just writing. It was his life, one true sentence at a time.", []),
        ("By living it first, Hemingway won the Nobel Prize, proving that the best stories are the ones you go out and get.", [top("living", "nobel.jpg", "1954: Nobel Prize", "Nobel medal or 1954 headline")]),
        ("Follow for more Lifestyle Legends.", []),
     ],
     end_card=dict(at="Follow", title=SERIES, sub="Full story on the page"),
     verify=["the nurse (Agnes von Kurowsky) turning him down by letter", "same facts as the long version"]),

dict(id="hemingway_b_guess", legend="Ernest Hemingway", ep="Guess who #3", skeleton="guess",
     film="One take to camera, no pauses. A fishing rod or an old typewriter beside you is a nice silent clue.",
     talk=["01_talk.mp4"], highlight=["Nobel"],
     hooks=[("Can you imagine experiencing this writer's rollercoaster life,", "guess"),
            ("Can you guess this legend from the story of his life,", "guess_caption"),
            ("In the 1920s, this broke young American walked around Paris completely unknown,", "historic")],
     lines=[
        [top(0, "portrait.jpg", "Guess the legend", "Portrait of Hemingway, face pixelated", censor=CENSOR)],
        ("growing up hunting and fishing in the Michigan woods, desperate for adventure,", [top("growing", "michigan.jpg", "The woods", "Michigan lake and woods, early 1900s")]),
        ("skips college and lands a job as a newspaper reporter,", [top("skips", "newsroom.jpg", "The reporter", "1910s newsroom")]),
        ("gets turned down by the army, so goes to war driving ambulances in search of the real thing,", [top("turned", "ambulance.jpg", "The war", "WWI Red Cross ambulance")]),
        ("gets hit by a mortar shell, but keeps going, and comes home with a medal for bravery,", [top("mortar", "hospital_1918.jpg", "The shell", "Milan hospital, 1918, face pixelated", censor=CENSOR)]),
        ("falls for his nurse, who dumps him by letter,", [top("falls", "nurse.jpg", "The nurse", "WWI Red Cross nurses")]),
        ("moves to Paris with no money and writes in cafés every morning,", [top("moves", "paris_1920s.jpg", "Paris", "Paris café, 1920s")]),
        ("runs with the bulls in Pamplona, then turns the whole trip into a bestselling novel.", [top("runs", "pamplona.jpg", "Pamplona", "Running of the bulls, 1920s")]),
        ("A boat awaits, and in the coming years he fishes for marlin off Cuba, survives two plane crashes in two days, and reads his own obituary in the process.",
         [full("boat", "fishing.mp4", "The boat", "YOU: deep-sea fishing")]),
        ("This chapter ends when he wins the Nobel Prize for a story about an old fisherman.", [top("chapter", "old_man.jpg", "Last clue", "Book cover with the author's name pixelated", censor=[0.0, 0.0, 1.0, 0.3])]),
        ("By now, you probably know that this is the story of Ernest Hemingway.", [top("By", "portrait.jpg", "Ernest Hemingway", "The same portrait, no pixelation")]),
        ("Comment below when you figured it out.", []),
     ],
     end_card=dict(at="Comment", title="Guess the Legend", sub="Comment when you got it"),
     verify=["the Italian Silver Medal of Military Valour", "same facts as the long version"]),

dict(id="hemingway_c_footsteps", legend="Ernest Hemingway", ep="Ep 03 · In his footsteps", skeleton="helene",
     film="A few days in Paris on the A Moveable Feast route: 74 rue du Cardinal Lemoine (the plaque), writing in a café, the Luxembourg Gardens, Shakespeare and Company, and a last morning at La Closerie des Lilas.",
     talk=["01_street.mp4", "02_closerie.mp4"], highlight=["true", "Paris"],
     title=dict(text="Writing like broke\nHemingway in Paris", until="Here's"),
     hooks=[("This is totally normal in Paris and doesn't exist anywhere else: you can still sit and write in the café where Hemingway wrote his first novel.", "helene"),
            ("This is one of the most important café tables in the history of books.", "alice"),
            ("I came to Paris because of one sentence from Hemingway.", "helene_caption")],
     lines=[
        [],
        ("No laptop, no phone, no plan. Just me, a notebook, and the Paris that Ernest Hemingway lived in when he was twenty-two and broke.",
         [top("Ernest", "hemingway_hadley.jpg", "Paris, 1921", "Ernest and Hadley Hemingway, early 1920s (check licence)")]),
        ("Here's how it works. You start at his first apartment, 74 rue du Cardinal Lemoine, where he lived with no hot water.",
         [full("Here's", "apartment.mp4", "74 rue du Cardinal Lemoine", "YOU: in front of the building and its plaque")]),
        ("Then you walk to a café, order one coffee, and do what he did: write one true sentence, then the next one.", [top("walk", "cafe_writing.mp4", "One true sentence", "YOU: writing in a notebook at a café")]),
        (ME + "I'd write all morning, walk the Luxembourg Gardens at lunch like he did when he was too broke to eat, and spend the afternoon at Shakespeare and Company.",
         [full("Luxembourg", "gardens.mp4", desc="YOU: walking the Luxembourg Gardens"), top("Shakespeare", "bookshop.mp4", "Shakespeare and Company", "YOU: outside and inside the bookshop")]),
        ("Then I'd stop writing while I still knew what came next, like he said to, so the next morning was easy.", [full("stop")]),
        ("Walking his Paris is like walking through his book: zinc bars, chestnut trees, the river, old men playing chess in the gardens.", [full("zinc", "paris_broll.mp4", desc="YOU: Paris B-roll")]),
        ("This isn't a tourist trail. It's a notebook and a city, and it's exactly what made him.", []),
        (ME + "I wrote more in those few days than I have all year.", [full("days")]),
        ("But here's what really got me. He wasn't waiting for a big life to write about. He was out getting one.", []),
        ("On my last morning I sat at La Closerie des Lilas, the same café where Hemingway wrote much of his first novel.",
         [top("Closerie", "closerie.mp4", "La Closerie des Lilas", "YOU: at a table at La Closerie des Lilas")]),
        ("Sitting there, I couldn't believe it was still just a café.", []),
        (ME + "A week ago I hadn't written anything in years. Now I've got a notebook full.", [full("notebook#2")]),
        ("That's the power of one true sentence.", []),
        ("Follow for the next legend's footsteps.", []),
     ],
     end_card=dict(at="Follow", title=SERIES, sub="Next week: a new legend"),
     verify=["74 rue du Cardinal Lemoine flat with no hot water", "writing much of The Sun Also Rises at La Closerie des Lilas",
             "walking the Luxembourg Gardens when hungry (A Moveable Feast)",
             "Sylvia Beach's original Shakespeare and Company was at 12 rue de l'Odéon; today's shop on the Seine is a later one that carries the name, so don't say he went to that one",
             "every ✎ line must be true for you"]),
]


# --------------------------------------------------------------------------
def anchor_for(at, words, lo, hi):
    """Return at or at#n so that it resolves inside tokens [lo, hi)."""
    if isinstance(at, (int, float)):
        return at
    base, _, n0 = str(at).partition("#")
    for n in range(int(n0 or 1), 30):
        cand = base if n == 1 else f"{base}#{n}"
        i = find_word(cand, words)
        if i is None:
            break
        if lo <= i < hi:
            return cand
    raise SystemExit(f"anchor '{at}' not found in its line")


def tokens(hook, script):
    lines = [hook] + [l.replace(ME, "") for l, _ in script["lines"][1:]]
    words, ranges = [], []
    for line in lines:
        toks = line.split()
        ranges.append((len(words), len(words) + len(toks)))
        words += [{"text": t} for t in toks]
    return words, ranges


def build(script):
    hook_panels = script["lines"][0]
    variants = [tokens(h, script) for h, _ in script["hooks"]]
    words, ranges = variants[0]
    panels = []
    body = script["lines"][1:]
    for p in hook_panels:
        panels.append({k: v for k, v in p.items() if k != "desc" and v is not None})
    for (_, ps), (lo, hi), idx in zip(body, ranges[1:], range(1, len(ranges))):
        for p in ps:
            p = {k: v for k, v in p.items() if k != "desc" and v is not None}
            p["at"] = anchor_for(p["at"], words, lo, hi)
            for w2, r2 in variants[1:]:        # must land on the same line whichever hook is filmed
                i = find_word(p["at"], w2)
                if i is None or not (r2[idx][0] <= i < r2[idx][1]):
                    raise SystemExit(f"{script['id']}: cue '{p['at']}' moves with another hook; pick another word")
            panels.append(p)
    ec = dict(script["end_card"])
    ec["at"] = anchor_for(ec["at"], words, *ranges[-1]) if ec["at"].lower() in body[-1][0].lower() \
        else anchor_for(ec["at"], words, *ranges[-2])
    plan = {
        "footage": f"input/{script['id']}",
        "series_tag": f"{SERIES} · {script['ep']}",
        "highlight": script["highlight"],
        "sequence": [{"talk": t} for t in script["talk"]],
        "panels": panels,
        "end_card": ec,
    }
    if script.get("title"):
        t = dict(script["title"])
        t["until"] = anchor_for(t["until"], words, 0, len(words))
        plan["title"] = t
    return plan, len(words)


def screen(ps):
    cells = []
    for p in ps:
        if p.get("full") == "talk":
            cells.append("you, full screen")
        elif p.get("full"):
            lab = f" · **{p['label'].upper()}**" if p.get("label") else ""
            cells.append(f"full `{p['full']}`{lab}")
        else:
            cz = " (pixelated)" if p.get("censor") else ""
            cells.append(f"top `{p['file']}`{cz} · **{p['label'].upper()}**")
    return "<br>".join(cells)


def md(script, n_words):
    sk = SKELETONS[script["skeleton"]]
    version, fmt = VERSIONS[script["skeleton"]]
    secs = round(n_words / sk["wps"])
    out = [f"### {version}. {fmt}: `{script['id']}`", ""]
    out.append(f"**Built line for line on:** [{sk['name']}]({sk['url']}), {sk['stats']}. "
               f"The winner runs {sk['length']}, with the {sk['reveal']}. Shape: {sk['shape']}.")
    out.append("")
    out.append(f"**Yours:** {n_words} words, about {secs} s. {sk['look']}. **Film:** {script['film']}")
    out.append("")
    if script.get("title"):
        t = script["title"]["text"].replace(chr(10), " / ")
        out.append(f"**Opening title:** *{t}*")
        out.append("")
    out.append("**Three hooks.** Film all three; the plan works with any of them.")
    out.append("")
    out.append("| # | Hook | Copied from |")
    out.append("|---|---|---|")
    for i, (h, src) in enumerate(script["hooks"], 1):
        madlib, name, url, stats = HOOKS[src]
        out.append(f"| {i} | \"{h}\" | [{name}]({url}), {stats}: *{madlib}* |")
    out.append("")
    out.append("| Beat | The winner said | You say | On screen |")
    out.append("|---|---|---|---|")
    winner = WINNERS[script["skeleton"]]
    hook_cell = "*(your hook)*"
    rows = [(hook_cell, script["lines"][0])] + [(l, ps) for l, ps in script["lines"][1:]]
    for i, (line, ps) in enumerate(rows):
        beat, said = winner[i] if i < len(winner) else ("(extra)", "")
        out.append(f"| {beat} | *{said}* | {line} | {screen(ps)} |")
    out.append("")
    ec = script["end_card"]
    out.append(f"End card from \"{ec['at']}\": **{ec['title'].upper()}** / {ec['sub'].upper()}. "
               f"Lines marked ✎ are personal: say them only if they're true for you, or swap in your version.")
    out.append("")
    files = {}
    for ps in [script["lines"][0]] + [ps for _, ps in script["lines"][1:]]:
        for p in ps:
            f = p.get("file") or (p["full"] if p.get("full") != "talk" else None)
            if f and f not in files:
                files[f] = p.get("desc") or ""
    out.append("<details><summary>Footage and images to gather</summary>")
    out.append("")
    for t in script["talk"]:
        out.append(f"- `{t}`: you talking to camera")
    for f, d in files.items():
        out.append(f"- `{f}`: {d}")
    out.append("")
    out.append("</details>")
    out.append("")
    out.append("✓ Check before posting: " + "; ".join(script["verify"]) + ".")
    out.append("")
    return "\n".join(out)


def main():
    plans_dir = REPO / "series/lifestyle-legends/plans"
    for old in plans_dir.glob("*.json"):
        old.unlink()
    sections = {}
    for s in SCRIPTS:
        winner = WINNERS[s["skeleton"]]
        assert len(s["lines"]) <= len(winner), f"{s['id']}: more lines than the winner"
        plan, n = build(s)
        (plans_dir / f"{s['id']}.json").write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n")
        sections.setdefault(s["legend"], []).append(md(s, n))
    here = Path(__file__).parent
    head = (here / "scripts_head.md").read_text()
    bench = (here / "option_three.md").read_text()
    body = "\n---\n\n".join(f"## Legend {i}: {legend}\n\n" + "\n".join(parts)
                              for i, (legend, parts) in enumerate(sections.items(), 1))
    (REPO / "series/lifestyle-legends/SCRIPTS.md").write_text(head + "\n" + body + "\n---\n\n" + bench)
    print(f"{len(SCRIPTS)} scripts, plans in {plans_dir}")


if __name__ == "__main__":
    main()
