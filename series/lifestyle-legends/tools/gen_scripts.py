"""Generate series/lifestyle-legends/SCRIPTS.md and plans/*.json from one source.

Run from anywhere: python3 series/lifestyle-legends/tools/gen_scripts.py

Every panel anchor is checked against the script text with the editor's own
word matcher, so the plans line up with what's said.
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO))
from edit_legend import find_word  # noqa: E402

SERIES = "Lifestyle Legends"
SERIES_LINE = ("This is Lifestyle Legends: the people who lived first "
               "and figured out the work later.")
CENSOR = [0.25, 0.05, 0.5, 0.5]

# reference reels each format is built on, shown at the top of every script
REFS = {
    "The Origin Story": [
        ("Lens on Legends: Dua Lipa", "https://www.instagram.com/reel/DYul8wohxIL/", "main reference, 259×"),
        ("Let's Talk About It", "https://www.instagram.com/reel/DaWEza9y-Dg/", "the series line, 3,241×"),
        ("Jon Favreau", "https://www.instagram.com/reel/DDSdkJGoVRs/", "text-post version, 556×"),
    ],
    "Guess the Legend": [
        ("Guess the footballer", "https://www.instagram.com/reel/DdjfzUURsA3/", "main reference, 12×"),
    ],
    "In Their Footsteps": [
        ("Stevenson Trail", "https://www.tiktok.com/@heleneinbetween/video/7646771334520769805", "main reference, 65×"),
        ("Hever Castle", "https://www.tiktok.com/@history_alice/video/7672324997637082390", "evidence shots, 13×"),
        ("Harry DuBois", "https://www.instagram.com/reel/DcEVwdNxIA5/", "title + list hook, 14×"),
    ],
}
BREAKDOWN_ANCHOR = {"The Origin Story": "a-the-origin-story",
                    "Guess the Legend": "b-guess-the-legend",
                    "In Their Footsteps": "c-in-their-footsteps"}

# panel helpers: (anchor, kind, file, label, desc, extra)
def top(at, file, label, desc, **extra):
    return {"at": at, "file": file, "label": label, "desc": desc, **extra}


def full(at, file="talk", label=None, desc=None, **extra):
    d = {"at": at, "full": file, "desc": desc, **extra}
    if label:
        d["label"] = label
    return d


SCRIPTS = [
# ------------------------------------------------------- JACQUES COUSTEAU
dict(id="cousteau_a_origin", legend="Jacques Cousteau", version="A", ep="Ep 01", group="main",
     fmt="The Origin Story", length="about 95 s",
     ref="Lens on Legends, Dua Lipa: one bold fact first, short declarative sentences, a payoff flurry, the detail nobody tells, and a callback to the hook",
     film="One take to camera on the rocks above the sea, slow and serious. Plus two clips of you: swimming in the Med, and an underwater POV with goggles or a mask.",
     talk=["01_talk.mp4"],
     highlight=["goggles", "Aqua-Lung", "Calypso", "Oscar", "ocean", "sky"],
     lines=[
        ("At twenty-six, Jacques Cousteau crashed his car, broke both arms, and lost his dream of being a pilot.",
         [top("Jacques", "portrait_navy.jpg", "Jacques Cousteau", "Young Cousteau in naval uniform (check licence) or an illustration")]),
        (SERIES_LINE, [full("This")]),
        ("He was a sickly kid, and a troublemaker. He got thrown out of school for breaking seventeen windows.",
         [top("sickly", "school.jpg", "The troublemaker", "1920s French school or boarding school, old postcard")]),
        ("At thirteen, he saved up for a movie camera, and took it apart to see how it worked.",
         [top("saved", "camera.jpg", "Age 13: first camera", "1920s Pathé home movie camera")]),
        ("He joined the French Navy to fly planes.",
         [top("joined", "naval_aviation.jpg", "The French Navy", "1930s French naval aviation photo")]),
        ("Then the crash ended all of it.", [full("crash")]),
        ("To get his arms working again, he started swimming every day in the Mediterranean.",
         [full("swimming", "swim.mp4", "The rehab", "YOU: swimming laps in the Mediterranean")]),
        ("One summer morning in 1936, a friend handed him a pair of swimming goggles.",
         [top("summer", "goggles.jpg", "1936: the goggles", "Vintage swimming goggles on a rock")]),
        ("He put his face under the water, and that was it.",
         [full("face", "underwater.mp4", desc="YOU: underwater POV, fish and rocks")]),
        ("He wrote: sometimes we are lucky enough to know that our lives have been changed.",
         [full("wrote")]),
        ("There was one problem. You could only stay down as long as you could hold your breath.", []),
        ("So during the war, he and an engineer named Emile Gagnan built a way to breathe underwater. They called it the Aqua-Lung.",
         [top("engineer", "aqualung.jpg", "1943: the Aqua-Lung", "Early Aqua-Lung regulator and tanks")]),
        ("Every scuba tank on earth comes from that idea.", []),
        ("Then he got hold of an old minesweeper, named it Calypso, and sailed it around the world with a camera.",
         [top("minesweeper", "calypso.jpg", "Calypso", "The ship Calypso")]),
        ("His film The Silent World won the top prize at Cannes, and an Oscar.",
         [top("Silent", "silent_world.jpg", "Cannes + Oscar", "Poster or book cover of The Silent World")]),
        ("Then the TV shows, the red cap, and a whole generation who wanted to explore the ocean.",
         [top("TV", "red_cap.jpg", "The red cap", "A red wool cap on a ship's rail (YOU can shoot this)")]),
        ("And the part nobody tells you: he became one of the loudest voices fighting to protect the sea he'd spent his life filming.",
         [top("nobody", "older.jpg", "The protector", "Older Cousteau (check licence) or open ocean")]),
        ("He wanted the sky. He got the whole ocean instead.", [full("wanted")]),
        ("Follow for the next legend: the climber who ate cat food and built Patagonia.", []),
     ],
     end_card=dict(at="Follow", title=SERIES, sub="Next: Yvon Chouinard"),
     verify=["the 1936 car accident and the end of his naval-aviation training", "expelled for breaking 17 windows",
             "buying a movie camera at 13 and taking it apart", "goggles from Philippe Tailliez at Le Mourillon, 1936",
             "the 'lucky enough' quote from The Silent World", "Aqua-Lung with Émile Gagnan, 1943",
             "Calypso, a former minesweeper", "The Silent World: Palme d'Or 1956, Oscar 1957",
             "his campaigns against dumping waste in the sea"]),

dict(id="cousteau_b_guess", legend="Jacques Cousteau", version="B", ep="Guess who #1", group="main",
     fmt="Guess the Legend", length="about 50 s",
     ref="Guess the footballer: one breathless present-tense run-on, a new image every clue, the reveal at about 90%, then 'comment when you knew'",
     film="One take to camera, no pauses, leaning in like you're quizzing a friend. A red cap in your hand is the silent last clue.",
     talk=["01_talk.mp4"],
     highlight=["guess", "goggles", "Oscar"],
     lines=[
        ("Can you imagine living this explorer's life? Comment the second you know who it is.",
         [top("imagine", "portrait.jpg", "Guess the legend", "Portrait of Cousteau, face pixelated by the editor", censor=CENSOR)]),
        ("A sickly kid who gets thrown out of school for breaking windows,",
         [top("sickly", "school.jpg", "The troublemaker", "1920s French school, old postcard")]),
        ("buys his first movie camera at thirteen,",
         [top("buys", "camera.jpg", "Age 13", "1920s home movie camera")]),
        ("joins the navy to become a pilot,",
         [top("navy", "naval_aviation.jpg", "The navy", "1930s naval aviation photo")]),
        ("then a car crash breaks both his arms and ends it.",
         [top("crash", "old_car.jpg", "The crash", "1930s car on a mountain road")]),
        ("He swims in the sea every day to recover,",
         [full("swims", "swim.mp4", "The rehab", "YOU: swimming in the sea")]),
        ("puts on a pair of goggles, and never looks back.",
         [top("goggles", "goggles.jpg", "The goggles", "Vintage swimming goggles")]),
        ("During the war, he helps invent a way to breathe underwater,",
         [top("war", "aqualung.jpg", "The invention", "Early scuba regulator")]),
        ("sails an old minesweeper around the world with a camera,",
         [top("minesweeper", "calypso.jpg", "The ship", "The ship, name on the hull pixelated", censor=[0.0, 0.3, 1.0, 0.3])]),
        ("and wins an Oscar for showing everyone what's down there.",
         [top("Oscar", "oscar.jpg", "The Oscar", "An Oscar statuette or 1950s premiere photo")]),
        ("Last clue: the red cap.",
         [top("Last", "red_cap.jpg", "Last clue", "YOU: holding a red wool cap")]),
        ("It's Jacques Cousteau.",
         [top("Jacques", "portrait.jpg", "Jacques Cousteau", "The same portrait, no pixelation")]),
        ("Comment when you got it, and follow for the next one.", [full("got")]),
     ],
     end_card=dict(at="follow", title="Guess the Legend", sub="Next: a climber turned billionaire"),
     verify=["the same facts as version A"]),

dict(id="cousteau_c_footsteps", legend="Jacques Cousteau", version="C", ep="Ep 01 · In his footsteps", group="main",
     fmt="In Their Footsteps", length="about 75 s",
     ref="Stevenson Trail + Hever Castle: a title over a selfie hook in the real place, B-roll every 1.5–3 s, you back on camera at the emotional beats, ending at the legend's landmark",
     film="Two days on the Riviera. 01 at Le Mourillon beach in Toulon (selfie, goggles in hand), 02 outside the Oceanographic Museum in Monaco. Plus underwater POV and the drive along the coast.",
     talk=["01_mourillon.mp4", "02_monaco.mp4"],
     title=dict(text="Following Cousteau\nalong the Riviera", until="1936"),
     highlight=["goggles", "Aqua-Lung", "ocean"],
     lines=[
        ("This little beach in Toulon is where Jacques Cousteau first put his face in the sea.", []),
        ("In 1936 he was a navy officer with two broken arms, swimming here every day to get them working again.",
         [top("1936", "portrait_navy.jpg", "Le Mourillon, 1936", "Young Cousteau in naval uniform (check licence) or an illustration")]),
        ("A friend gave him a pair of goggles. He looked down, and that was it.",
         [top("goggles", "goggles.jpg", "The goggles", "Vintage goggles on these rocks")]),
        ("So I brought goggles.", [full("brought")]),
        ("This is what he saw.",
         [full("This", "underwater.mp4", desc="YOU: underwater POV off Le Mourillon")]),
        ("Seven years later, he and an engineer invented the Aqua-Lung, and took it into this same sea.",
         [top("Seven", "aqualung.jpg", "1943: the Aqua-Lung", "Early Aqua-Lung regulator and tanks")]),
        ("Then I followed the coast to Monaco.",
         [full("followed", "coast_drive.mp4", desc="YOU: driving or on the train along the coast")]),
        ("Cousteau ran the Oceanographic Museum here for more than thirty years.",
         [top("Oceanographic", "museum.mp4", "Oceanographic Museum, Monaco", "YOU: walking up to the museum")]),
        ("The man who wanted to fly ended up with the whole ocean.", [full("man")]),
        ("Honestly, I get it. Put your face in the water for five minutes and tell me you don't.", []),
        ("Follow for the next legend's footsteps.", []),
     ],
     end_card=dict(at="Follow", title=SERIES, sub="Next: Chouinard's surf rule"),
     verify=["Le Mourillon, Toulon as the 1936 goggles beach", "the Aqua-Lung's first sea dives off the Provence coast",
             "director of the Oceanographic Museum of Monaco, 1957–1988"]),

# ----------------------------------------------------------- YVON CHOUINARD
dict(id="chouinard_a_origin", legend="Yvon Chouinard", version="A", ep="Ep 02", group="main",
     fmt="The Origin Story", length="about 90 s",
     ref="Lens on Legends, Dua Lipa + Let's Talk About It: a two-sentence hook from tiny to huge, the series line, short sentences, the detail nobody tells, a callback",
     film="One take to camera at a crag or a surf break. Plus clips of you: a car boot full of gear, and surfing.",
     talk=["01_talk.mp4"],
     highlight=["forge", "cat", "Patagonia", "surf's", "Earth"],
     lines=[
        ("At eighteen, Yvon Chouinard bought a used forge from a junkyard. Sixty-five years later, he gave away a three-billion-dollar company.",
         [top("Yvon", "forge.jpg", "1957", "An old coal forge and anvil")]),
        (SERIES_LINE, [full("This")]),
        ("He was the French kid in a California school who barely spoke English.",
         [top("French", "young.jpg", "The outsider", "Photo of young Chouinard (licensed) or a 1940s California schoolyard")]),
        ("He found falconry. Falconry led him to climbing. Climbing led him to Yosemite.",
         [top("falconry", "yosemite.jpg", "Yosemite", "El Capitan or Camp 4, old photo")]),
        ("He couldn't afford gear. So he taught himself to blacksmith, and made his own.",
         [top("afford", "pitons.jpg", "Homemade pitons", "Old steel pitons")]),
        ("He sold it from the back of his car. A dollar fifty each.",
         [top("sold", "car_boot.mp4", "$1.50 each", "YOU: opening a car boot full of climbing gear")]),
        ("He lived on about a dollar a day. Sometimes that meant cat food.",
         [top("lived", "cat_food.jpg", "The diet", "A dented tin of cat food")]),
        ("By 1970, he was the biggest climbing gear supplier in America.", [full("biggest")]),
        ("Then he saw his gear was scarring the rock he loved. So he stopped selling it.",
         [top("scarring", "scarred_rock.jpg", "Scarring the rock", "Close-up of a scarred granite crack")]),
        ("He started selling clothes instead. He called the company Patagonia.",
         [top("clothes", "patagonia.jpg", "1973: Patagonia", "Patagonia shopfront or logo")]),
        ("The rule at work? When the surf's up, go surfing.",
         [full("rule", "surf.mp4", "Company policy", "YOU: surfing")]),
        ("In 2022, he gave the whole company away to fight climate change. Earth is now the only shareholder.",
         [top("gave", "headline.png", "2022", "Screenshot of the news headline")]),
        ("The part nobody tells you: he always said he hated being called a businessman.", [full("nobody")]),
        ("The kid with the junkyard forge just wanted to keep climbing.", []),
        ("Follow for the next legend: the writer who got blown up at eighteen, and won the Nobel Prize.", []),
     ],
     end_card=dict(at="Follow", title=SERIES, sub="Next: Ernest Hemingway"),
     verify=["1957 used forge from a junkyard (he was 18)", "spoke only French at school in California",
             "falconry led to climbing", "pitons at $1.50, living on about $1 a day", "the cat food story",
             "biggest US climbing hardware supplier by 1970", "phasing out pitons (1972 'clean climbing')",
             "Patagonia 1973", "2022 transfer, ~$3B, 'Earth is now our only shareholder'",
             "his line about hating to admit being a businessman (Let My People Go Surfing)"]),

dict(id="chouinard_b_guess", legend="Yvon Chouinard", version="B", ep="Guess who #2", group="main",
     fmt="Guess the Legend", length="about 50 s",
     ref="Guess the footballer: one breathless present-tense run-on, a new image every clue, the reveal at about 90%, then 'comment when you knew'",
     film="One take to camera in a fleece, outdoors, no pauses.",
     talk=["01_talk.mp4"],
     highlight=["guess", "cat"],
     lines=[
        ("Can you imagine living this climber's life? Comment the second you know who it is.",
         [top("imagine", "portrait.jpg", "Guess the legend", "Portrait of Chouinard, face pixelated", censor=CENSOR)]),
        ("A French-speaking outsider in a California school,",
         [top("outsider", "1940s_california.jpg", "The outsider", "1940s Southern California street")]),
        ("gets into falconry, which gets him into climbing,",
         [top("falconry", "falcon.jpg", "Falconry", "A falcon on a glove")]),
        ("teaches himself blacksmithing to make his own gear,",
         [top("blacksmithing", "forge.jpg", "Self-taught blacksmith", "An old coal forge and anvil")]),
        ("sells it from the back of his car, lives on a dollar a day, eats cat food,",
         [top("sells", "cat_food.jpg", "The diet", "A dented tin of cat food")]),
        ("builds the biggest climbing gear company in America, then quits his best seller because it's damaging the rock,",
         [top("quits", "scarred_rock.jpg", "Quits his best seller", "Scarred granite crack")]),
        ("brings home a rugby shirt from Scotland and starts selling clothes,",
         [top("rugby", "rugby_shirt.jpg", "The rugby shirt", "A striped 1970s rugby shirt")]),
        ("writes a book called Let My People Go Surfing,",
         [top("book", "book.jpg", "The book", "YOU: holding the book, company name covered", censor=[0.0, 0.7, 1.0, 0.3])]),
        ("and in 2022 gives the entire company away to fight climate change.",
         [top("entire", "headline.png", "Last clue", "News headline, company name pixelated", censor=[0.0, 0.0, 1.0, 0.4])]),
        ("It's Yvon Chouinard. The founder of Patagonia.",
         [top("Yvon", "portrait.jpg", "Yvon Chouinard", "The same portrait, no pixelation")]),
        ("Comment when you got it, and follow for the next one.", [full("got")]),
     ],
     end_card=dict(at="follow", title="Guess the Legend", sub="Next: a writer who fished for marlin"),
     verify=["the 1970 rugby shirt from Scotland that started the clothing line"]),

dict(id="chouinard_c_footsteps", legend="Yvon Chouinard", version="C", ep="Ep 02 · In his footsteps", group="main",
     fmt="In Their Footsteps", length="about 70 s",
     ref="Harry DuBois + Stevenson Trail: a stacked-accomplishments hook under a big title, you living it in fast B-roll, back on camera for what you learned",
     film="A 'surf's up' workday: talk takes at dawn and in the afternoon, B-roll of the surf, laptop work while still wet, and a climb.",
     talk=["01_dawn.mp4", "02_afternoon.mp4"],
     title=dict(text="Living by Patagonia's\none rule for a day", until="name"),
     highlight=["surf's", "surfing", "Patagonia"],
     lines=[
        ("He forged his own climbing gear, ate cat food to stay in Yosemite, and built a three-billion-dollar company around one rule. Today I'm following it.", []),
        ("His name is Yvon Chouinard, and the rule is the title of his book: Let My People Go Surfing.",
         [top("His", "portrait.jpg", "Yvon Chouinard", "Photo of Chouinard (licensed) or an illustration"),
          top("book", "book.jpg", "The rule", "YOU: holding the book")]),
        ("When the surf's up, you go surfing. You fit the work around it.",
         [full("surf's", "surf_dawn.mp4", "Dawn patrol", "YOU: dawn surf session")]),
        ("So: surf first.", [full("So")]),
        ("Then the laptop, still salty.",
         [top("laptop", "laptop.mp4", "Then work", "YOU: working on a laptop in a towel")]),
        ("Then a climb in the afternoon.",
         [full("climb", "climb.mp4", desc="YOU: bouldering or a scramble")]),
        ("Here's what surprised me: I got more done in four hours than on a normal day.", [full("Here's")]),
        ("Chouinard's trick is flexibility. Chase the good conditions, and fit the work around them.",
         [top("trick", "portrait.jpg", "The trick", "Same Chouinard photo")]),
        ("He built a company that way, then gave it all away.",
         [top("gave", "headline.png", "2022: gives it away", "Screenshot of the news headline")]),
        ("Follow for the next legend's footsteps.", []),
     ],
     end_card=dict(at="Follow", title=SERIES, sub="Next: Hemingway's Paris"),
     verify=["Patagonia's flextime ('let my people go surfing') policy",
             "only say the 'four hours' line if it's true for you"]),
# ------------------------------------------------------- ERNEST HEMINGWAY
dict(id="hemingway_a_origin", legend="Ernest Hemingway", version="A", ep="Ep 03", group="main",
     fmt="The Origin Story", length="about 100 s",
     ref="Lens on Legends, Dua Lipa: an age-and-shock hook, short sentences, a new picture every line, a payoff flurry, the detail nobody tells, and a moral that turns the series line around",
     film="One take to camera on a boat or a harbour wall, slow and deliberate. Plus a clip of you deep-sea fishing or on a boat.",
     talk=["01_talk.mp4"],
     highlight=["shrapnel", "Pilar", "Nobel", "obituaries", "true"],
     lines=[
        ("At eighteen, Ernest Hemingway was blown up by a mortar shell in Italy, with more than two hundred pieces of shrapnel in his legs.",
         [top("Ernest", "portrait_1918.jpg", "Ernest Hemingway, 18", "Hemingway in uniform in Milan, 1918 (public domain)")]),
        ("Everything he went on to write, he lived first.", []),
        (SERIES_LINE, [full("This")]),
        ("And Hemingway is the purest case. He only wrote what he'd lived.", []),
        ("He grew up hunting and fishing in the woods of northern Michigan with his father.",
         [top("hunting", "michigan.jpg", "Northern Michigan", "Michigan lake and woods, early 1900s")]),
        ("Straight out of high school, he became a newspaper reporter. The style guide said: use short sentences. He never forgot it.",
         [top("reporter", "newsroom.jpg", "Age 18: reporter", "1910s newspaper newsroom")]),
        ("The army turned him down for a bad eye, so he went to Italy to drive ambulances for the Red Cross.",
         [top("army", "ambulance.jpg", "Red Cross ambulance", "WWI Red Cross ambulance in Italy")]),
        ("That's where the shell found him.", [full("shell")]),
        ("In the hospital, he fell in love with his nurse. She turned him down by letter.",
         [top("hospital", "nurse.jpg", "The nurse", "WWI Red Cross nurses in Milan, 1918")]),
        ("That war, and that heartbreak, became A Farewell to Arms.",
         [top("heartbreak", "farewell.jpg", "A Farewell to Arms", "First-edition cover (check licence) or YOU holding a copy")]),
        ("In his twenties he was broke in Paris, so hungry he'd take the long way round to avoid the smell of the bakeries.",
         [top("broke", "paris_1920s.jpg", "Paris, 1920s", "Paris street or café, 1920s")]),
        ("He ran with the bulls in Pamplona, and wrote The Sun Also Rises.",
         [top("bulls", "pamplona.jpg", "Pamplona", "Running of the bulls, 1920s")]),
        ("He fished for marlin off Key West and Cuba on his own boat, the Pilar.",
         [full("marlin", "fishing.mp4", "The Pilar", "YOU: deep-sea fishing or out on a boat")]),
        ("Out of that came The Old Man and the Sea, a Pulitzer, and then the Nobel Prize.",
         [top("Old", "old_man.jpg", "The Old Man and the Sea", "YOU holding a copy of the book"),
          top("Nobel", "nobel.jpg", "1954: Nobel Prize", "Nobel medal image or 1954 headline")]),
        ("And the part nobody tells you: in 1954 he survived two plane crashes in two days, and got to read his own obituaries.",
         [top("nobody", "obituary.jpg", "Reads his own obituary", "1954 newspaper headline reporting him dead")]),
        ("His rule for writing was simple: write one true sentence.", [full("rule")]),
        ("He didn't figure out the work later. For him, the living was the work.", []),
        ("Follow for the next legend.", []),
     ],
     end_card=dict(at="Follow", title=SERIES, sub="Next week: a new legend"),
     verify=["wounded at Fossalta di Piave on 8 July 1918, aged 18", "'more than two hundred' shrapnel fragments",
             "Kansas City Star style sheet ('use short sentences')", "rejected by the army for poor eyesight",
             "nurse Agnes von Kurowsky turning him down by letter", "the hunger-in-Paris detail from A Moveable Feast",
             "Pilar, bought 1934", "Pulitzer 1953, Nobel 1954", "the two 1954 plane crashes and premature obituaries",
             "the 'one true sentence' line (A Moveable Feast)"]),

dict(id="hemingway_b_guess", legend="Ernest Hemingway", version="B", ep="Guess who #3", group="main",
     fmt="Guess the Legend", length="about 50 s",
     ref="Guess the footballer: one breathless present-tense run-on, a new image every clue, the reveal at about 90%, then 'comment when you knew'",
     film="One take to camera, no pauses. A fishing rod or an old typewriter beside you is a nice silent clue.",
     talk=["01_talk.mp4"],
     highlight=["guess", "Nobel"],
     lines=[
        ("Can you imagine living this writer's life? Comment the second you know who it is.",
         [top("imagine", "portrait.jpg", "Guess the legend", "Portrait of Hemingway, face pixelated by the editor", censor=CENSOR)]),
        ("Grows up hunting and fishing in the Michigan woods,",
         [top("Grows", "michigan.jpg", "The woods", "Michigan lake and woods, early 1900s")]),
        ("becomes a newspaper reporter at eighteen,",
         [top("newspaper", "newsroom.jpg", "Age 18", "1910s newsroom")]),
        ("drives ambulances in a world war and gets hit by a mortar shell,",
         [top("ambulances", "ambulance.jpg", "The war", "WWI Red Cross ambulance")]),
        ("falls for his nurse, who dumps him by letter,",
         [top("nurse", "nurse.jpg", "The nurse", "WWI Red Cross nurses")]),
        ("lives broke in Paris with the most famous writers of the twenties,",
         [top("Paris", "paris_1920s.jpg", "Paris", "Paris café, 1920s")]),
        ("runs with the bulls in Pamplona,",
         [top("bulls", "pamplona.jpg", "Pamplona", "Running of the bulls, 1920s")]),
        ("fishes for marlin off Cuba on his own boat,",
         [full("marlin", "fishing.mp4", "The boat", "YOU: deep-sea fishing")]),
        ("survives two plane crashes in two days and reads his own obituary,",
         [top("survives", "obituary.jpg", "The obituary", "1954 headline, name pixelated", censor=[0.0, 0.0, 1.0, 0.45])]),
        ("and wins the Nobel Prize for a story about an old fisherman.",
         [top("Nobel", "old_man.jpg", "Last clue", "Book cover with the author's name pixelated", censor=[0.0, 0.0, 1.0, 0.3])]),
        ("It's Ernest Hemingway.",
         [top("Ernest", "portrait.jpg", "Ernest Hemingway", "The same portrait, no pixelation")]),
        ("Comment when you got it, and follow for the next one.", [full("got")]),
     ],
     end_card=dict(at="follow", title="Guess the Legend", sub="Next: another legend"),
     verify=["the same facts as version A"]),

dict(id="hemingway_c_footsteps", legend="Ernest Hemingway", version="C", ep="Ep 03 · In his footsteps", group="main",
     fmt="In Their Footsteps", length="about 80 s",
     ref="Stevenson Trail + Hever Castle: a title over a selfie hook in the real place, the legend as the reason for the day, B-roll every 1.5–3 s, evidence shots (plaques, the bookshop), and what you learned",
     film="One day in Paris, the A Moveable Feast route: talk takes on the street, outside 74 rue du Cardinal Lemoine (the plaque), writing in a café, the Luxembourg Gardens, the bookshop. Can't get to Paris? Do his Key West day on your coast instead: write standing up at dawn, fish all afternoon.",
     talk=["01_street.mp4", "02_afternoon.mp4"],
     title=dict(text="One day as broke\nHemingway in Paris", until="1921"),
     highlight=["true", "Paris"],
     lines=[
        ("I came to Paris to live one day exactly like a broke, twenty-two-year-old Ernest Hemingway.", []),
        ("In 1921 he moved here with his wife Hadley and almost no money.",
         [top("1921", "hemingway_hadley.jpg", "Paris, 1921", "Ernest and Hadley Hemingway, early 1920s (check licence)")]),
        ("Step one: his first apartment, 74 rue du Cardinal Lemoine. No hot water, and a shared toilet on the landing.",
         [full("Step", "apartment.mp4", "Step 1: 74 rue du Cardinal Lemoine", "YOU: in front of the building and its plaque")]),
        ("Step two: write in a café. His rule: write one true sentence, then the next one.",
         [top("two", "cafe_writing.mp4", "Step 2: one true sentence", "YOU: writing in a notebook at a café table")]),
        ("And stop while you still know what happens next, so tomorrow is easy.", [full("stop")]),
        ("Step three: the Luxembourg Gardens. He walked here when he was too broke to eat, because there was nothing to smell.",
         [full("three", "gardens.mp4", "Step 3: the gardens", "YOU: walking through the Luxembourg Gardens")]),
        ("Step four: the bookshop. Shakespeare and Company lent him books when he couldn't afford them.",
         [top("four", "bookshop.mp4", "Step 4: Shakespeare and Company", "YOU: outside and inside Shakespeare and Company")]),
        ("Here's what I learned. He wasn't waiting for a big life to write about. He went out and got one, then sat down and wrote it.",
         [full("Here's")]),
        ("Follow for the next legend's footsteps.", []),
     ],
     end_card=dict(at="Follow", title=SERIES, sub="Next week: a new legend"),
     verify=["arrived in Paris in December 1921, aged 22", "74 rue du Cardinal Lemoine flat with no hot water and a toilet on the landing",
             "the 'stop while you know what happens next' habit", "walking the Luxembourg Gardens when hungry (A Moveable Feast)",
             "Sylvia Beach's original Shakespeare and Company was at 12 rue de l'Odéon; today's shop on the Seine is a later one that carries the name, so say that on camera or film the old address"]),

# ---------------------------------------------------------------- JACK LONDON
dict(id="london_a_origin", legend="Jack London", version="A", ep="Ep 04", group="option",
     fmt="The Origin Story", length="about 80 s",
     film="One take to camera on a dock or harbour wall, golden hour. Then a surf clip of you for the Hawaii beat.",
     talk=["01_talk.mp4"],
     highlight=["pirate", "pirates", "scurvy", "surf", "Klondike"],
     lines=[
        ("At fifteen, Jack London borrowed three hundred dollars and became a pirate.",
         [top("Jack", "portrait.jpg", "Jack London", "Portrait of young Jack London (public domain, Wikimedia Commons)")]),
        (SERIES_LINE, [full("This")]),
        ("Jack grew up broke in Oakland, working ten-hour shifts in a cannery for ten cents an hour.",
         [top("Oakland", "cannery.jpg", "Age 14: cannery worker", "1890s cannery workers (Library of Congress)")]),
        ("So he borrowed three hundred dollars from the woman who'd nursed him as a baby, bought a little sloop called the Razzle Dazzle, and started raiding oyster beds in San Francisco Bay at night.",
         [top("sloop", "sloop.jpg", "The Razzle Dazzle", "Old oyster sloop on San Francisco Bay"),
          top("raiding", "oysters_night.mp4", "Oyster pirate", "YOU: shucking oysters on a dock at night by torchlight")]),
        ("The waterfront called him the Prince of the Oyster Pirates.", []),
        ("At seventeen he sailed to Japan on a sealing ship.",
         [top("Japan", "sealing_ship.jpg", "1893: sealing ship to Japan", "1890s sealing schooner")]),
        ("At eighteen he was riding freight trains across America, and got thrown in jail for vagrancy.",
         [top("freight", "freight_train.jpg", "Age 18: hobo", "Hobos on a freight train, 1890s")]),
        ("At twenty-one he went north for the Klondike gold rush.",
         [top("Klondike", "klondike.jpg", "1897: Klondike gold rush", "Chilkoot Pass, 1898 (public domain)")]),
        ("He found no gold. He came home with scurvy, no money, and a head full of stories.",
         [full("found")]),
        ("So he made himself write a thousand words a day, and editors kept sending them back.",
         [top("himself", "notebook.mp4", "1,000 words a day", "YOU: writing in a notebook, close on the pen")]),
        ("Then The Call of the Wild came out, and he became one of the most famous writers in the world.",
         [top("Call", "call_of_the_wild.jpg", "1903: The Call of the Wild", "1903 first-edition cover (public domain)")]),
        ("And the part nobody tells you? Already famous, he sailed to Hawaii and learned to surf at Waikiki.",
         [top("Hawaii", "waikiki_1907.jpg", "1907: learns to surf", "Waikiki surfers, early 1900s (public domain)"),
          full("surf", "surf.mp4", desc="YOU: paddling out and catching a wave")]),
        ("He wrote one of the first articles that made the world care about surfing.", []),
        ("He didn't plan a career. He lived first, and wrote it down later.", [full("plan")]),
        ("Follow for the next legend.", []),
     ],
     end_card=dict(at="Follow", title=SERIES, sub="Next week: a new legend"),
     verify=["the $300 loan from Virginia Prentiss at 15 and the Razzle Dazzle",
             "cannery wages (10 cents an hour, 10+ hour shifts)", "sealing voyage at 17 (1893)",
             "30 days for vagrancy at 18 (1894)", "Klondike 1897 and scurvy",
             "1,000 words a day", "Waikiki 1907 and his surfing article 'A Royal Sport'"]),

dict(id="london_b_guess", legend="Jack London", version="B", ep="Guess who #4", group="option",
     fmt="Guess the Legend", length="about 50 s",
     film="One take to camera, anywhere with character (a dock, a bar, a beach). Lean in like you're quizzing a friend.",
     talk=["01_talk.mp4"],
     highlight=["guess", "jail", "scurvy"],
     lines=[
        ("Can you guess this legend from the story of his life? Comment the second you know.",
         [top("guess", "portrait.jpg", "Guess the legend", "Portrait of Jack London, face pixelated by the editor", censor=CENSOR)]),
        ("Age fourteen: working in a cannery for ten cents an hour.",
         [top("cannery", "cannery.jpg", "Age 14", "1890s cannery workers")]),
        ("Age fifteen: buys a boat with borrowed money and steals oysters at night.",
         [top("boat", "sloop.jpg", "Age 15", "Old oyster sloop")]),
        ("Then switches sides and joins the fish patrol, catching the pirates he used to sail with.",
         [top("switches", "fish_patrol.jpg", "Switches sides", "California Fish Patrol boat or 1890s patrol photo")]),
        ("Age seventeen: sails to Japan on a sealing ship.",
         [top("Japan", "sealing_ship.jpg", "Age 17", "1890s sealing schooner")]),
        ("Age eighteen: thirty days in jail for vagrancy.",
         [top("jail", "jail.jpg", "Age 18", "1890s jail or penitentiary photo")]),
        ("Age twenty-one: the Klondike. No gold. Scurvy.",
         [top("Klondike", "klondike.jpg", "Age 21", "Chilkoot Pass, 1898")]),
        ("Age twenty-seven: writes a book about a dog that sells millions.",
         [top("dog", "sled_dog.jpg", "Age 27", "Historic sled-dog photo")]),
        ("Age thirty-one: learns to surf in Hawaii.",
         [top("surf", "waikiki_1907.jpg", "Age 31", "Waikiki surfers, early 1900s")]),
        ("Still nothing? You probably read his book in school.",
         [top("Still", "call_of_the_wild.jpg", "Last clue", "1903 cover with the title pixelated", censor=[0.1, 0.05, 0.8, 0.35])]),
        ("It's Jack London.",
         [top("Jack", "portrait.jpg", "Jack London", "The same portrait, no pixelation")]),
        ("Comment when you got it, and follow for the next one.", [full("got")]),
     ],
     end_card=dict(at="follow", title="Guess the Legend", sub="Next: another legend"),
     verify=["ages for each beat (born January 1876)", "California Fish Patrol after the oyster piracy"]),

dict(id="london_c_footsteps", legend="Jack London", version="C", ep="Ep 04 · In his footsteps", group="option",
     fmt="In Their Footsteps", length="about 75 s",
     film="Two talk takes: 01 on a dock at night with oysters, 02 next morning on the beach with a board. Plus b-roll of you on a boat, writing, and surfing.",
     talk=["01_dock_night.mp4", "02_beach_morning.mp4"],
     highlight=["oysters", "surf", "work"],
     lines=[
        ("I'm shucking oysters on a dock at midnight because of a writer who used to steal them.", []),
        ("In 1891, a fifteen-year-old named Jack London raided oyster beds like these in San Francisco Bay.",
         [top("Jack", "portrait.jpg", "Jack London", "Portrait of young Jack London")]),
        ("He did it in a sloop called the Razzle Dazzle, bought with three hundred borrowed dollars.",
         [top("sloop", "sloop.jpg", "The Razzle Dazzle", "Old oyster sloop")]),
        ("Then he went to sea, rode the rails, chased gold in the Klondike, and came home broke.",
         [full("sea", "boat.mp4", desc="YOU: on a boat or sailing, wide shot")]),
        ("Everything he lived, he wrote down. A thousand words a day.",
         [top("Everything", "notebook.mp4", "1,000 words a day", "YOU: writing in a notebook on the dock")]),
        ("So that's the plan for this trip: live it first, write it down after.", [full("plan")]),
        ("And the next morning, I'm doing what he did once he was already famous.", []),
        ("In 1907 he sailed to Hawaii and learned to surf at Waikiki.",
         [top("Hawaii", "waikiki_1907.jpg", "Waikiki, 1907", "Waikiki surfers, early 1900s")]),
        ("He got so sunburned he was stuck in bed, and went straight back out.",
         [full("sunburned", "surf.mp4", desc="YOU: catching a wave")]),
        ("Here's what I think he figured out. The adventure wasn't a break from the work. It was the work.",
         [full("Here's")]),
        ("Follow for the next legend's footsteps.", []),
     ],
     end_card=dict(at="Follow", title=SERIES, sub="Next week: a new legend"),
     verify=["1891 oyster piracy at 15", "the sunburn after his first surf sessions in 1907"]),

# --------------------------------------------------------------- IAN FLEMING
dict(id="fleming_a_origin", legend="Ian Fleming", version="A", ep="Ep 04", group="option",
     fmt="The Origin Story", length="about 85 s",
     film="One take to camera by the sea, linen shirt. Plus a snorkel clip of you for the routine beat.",
     talk=["01_talk.mp4"],
     highlight=["failed", "stockbroker", "Goldeneye", "Bond"],
     lines=[
        ("Ian Fleming. The man who invented James Bond. By forty, he'd failed at almost everything.",
         [top("Ian", "portrait.jpg", "Ian Fleming", "Portrait of Ian Fleming (check licence) or an illustrated portrait")]),
        (SERIES_LINE, [full("This")]),
        ("His big brother was the famous one, a best-selling travel writer. Ian was the problem child.",
         [top("brother", "family.jpg", "The famous brother", "1920s English country house or family photo")]),
        ("He left military academy early. He failed the Foreign Office exam.",
         [top("military", "sandhurst.jpg", "Strike one, strike two", "Royal Military College, Sandhurst (old postcard)")]),
        ("He became a stockbroker, and later called himself the worst stockbroker in the world.",
         [top("stockbroker", "stock_exchange.jpg", "The worst stockbroker", "1930s London Stock Exchange")]),
        ("Then the war came. He became the right-hand man to the head of British naval intelligence, planning operations straight out of a spy novel.",
         [top("war", "admiralty.jpg", "Naval intelligence", "The Admiralty building, London, 1940s")]),
        ("In 1944 he visited Jamaica, and told a friend he'd live there one day.",
         [top("visited", "jamaica_map.jpg", "Jamaica, 1944", "Old map of Jamaica")]),
        ("Two years later he built a house on the water and called it Goldeneye.",
         [top("Goldeneye", "goldeneye.jpg", "Goldeneye", "Goldeneye house or the cove at Oracabessa")]),
        ("He even got his newspaper to give him two months off every winter to go there.", [full("newspaper")]),
        ("Every morning: swim the reef, then write about two thousand words.",
         [full("swim", "snorkel.mp4", "The routine", "YOU: snorkelling over a reef")]),
        ("At forty-three, he sat down at Goldeneye and wrote Casino Royale.",
         [top("Casino", "casino_royale.jpg", "1952: Casino Royale", "YOU holding a copy of Casino Royale")]),
        ("He named his spy after the author of a bird book on his shelf, because he wanted the dullest name he could find.",
         [top("bird", "birds_book.jpg", "Birds of the West Indies", "The bird book by ornithologist James Bond")]),
        ("Fourteen Bond books. Every one written in the Jamaican winter.",
         [top("Bond books", "bond_books.jpg", "14 Bond books", "YOU: a stack of the paperbacks")]),
        ("He failed at the careers everyone wanted for him, then built one around the life he wanted.",
         [full("careers")]),
        ("Follow for the next legend.", []),
     ],
     end_card=dict(at="Follow", title=SERIES, sub="Next week: a new legend"),
     verify=["left Sandhurst early; failed the Foreign Office exam", "the 'worst stockbroker' self-description",
             "assistant to Admiral Godfrey, Director of Naval Intelligence", "1944 Jamaica visit; Goldeneye built 1946",
             "Sunday Times contract with two months off each winter", "Casino Royale written early 1952, age 43",
             "named after ornithologist James Bond, 'the dullest name'", "14 Bond books written at Goldeneye"]),

dict(id="fleming_b_guess", legend="Ian Fleming", version="B", ep="Guess who #4", group="option",
     fmt="Guess the Legend", length="about 50 s",
     film="One take to camera. A martini on the table is a nice silent clue.",
     talk=["01_talk.mp4"],
     highlight=["guess", "strike"],
     lines=[
        ("Can you guess this legend from the story of his life? Comment the second you know.",
         [top("guess", "portrait.jpg", "Guess the legend", "Portrait of Ian Fleming, face pixelated", censor=CENSOR)]),
        ("Rich family. Famous older brother. He's the disappointment.",
         [top("Rich", "family.jpg", "The disappointment", "1920s English country house")]),
        ("Leaves military academy early. Strike one.",
         [top("military", "sandhurst.jpg", "Strike one", "Sandhurst, old postcard")]),
        ("Fails the Foreign Office exam. Strike two.",
         [top("Fails", "foreign_office.jpg", "Strike two", "The Foreign Office, London")]),
        ("Becomes a stockbroker, and says he's the worst one in the world. Strike three.",
         [top("stockbroker", "stock_exchange.jpg", "Strike three", "1930s London Stock Exchange")]),
        ("Then the war: he's planning secret operations for naval intelligence.",
         [top("war", "admiralty.jpg", "World War II", "The Admiralty, 1940s")]),
        ("After the war, he builds a house above a reef in Jamaica.",
         [top("house", "goldeneye.jpg", "The hideout", "The cove at Oracabessa, Jamaica")]),
        ("He swims every morning, and writes every morning.",
         [full("swims", "snorkel.mp4", desc="YOU: snorkelling over a reef")]),
        ("At forty-three, he writes his first novel in about two months.",
         [top("novel", "typewriter.jpg", "First novel", "Old typewriter on a terrace")]),
        ("Last clue: his main character likes his martini shaken, not stirred.",
         [top("Last", "martini.jpg", "Last clue", "YOU: a martini on the bar")]),
        ("It's Ian Fleming. The man who invented James Bond.",
         [top("Ian", "portrait.jpg", "Ian Fleming", "The same portrait, no pixelation")]),
        ("Comment when you got it, and follow for the next one.", [full("got")]),
     ],
     end_card=dict(at="follow", title="Guess the Legend", sub="Next: another legend"),
     verify=["Casino Royale written in about two months (Jan–Mar 1952)"]),

dict(id="fleming_c_footsteps", legend="Ian Fleming", version="C", ep="Ep 04 · In his footsteps", group="option",
     fmt="In Their Footsteps", length="about 70 s",
     film="A full 'Fleming day' somewhere with a reef: talk takes in the morning and evening, b-roll of the swim, writing on a terrace, lunch and a nap.",
     talk=["01_morning.mp4", "02_evening.mp4"],
     highlight=["swim", "2,000", "Bond"],
     lines=[
        ("I'm about to live one day exactly like the man who wrote James Bond.", []),
        ("His name was Ian Fleming, and he wrote Casino Royale at a house on the water in Jamaica called Goldeneye.",
         [top("Ian", "portrait.jpg", "Ian Fleming", "Portrait of Ian Fleming (check licence)"),
          top("Goldeneye", "goldeneye.jpg", "Goldeneye, Jamaica", "The cove at Oracabessa")]),
        ("His routine was simple. Wake up, swim the reef.",
         [full("swim", "snorkel.mp4", "Step 1: swim", "YOU: snorkelling over a reef")]),
        ("Then he'd sit down and write about two thousand words before lunch.",
         [top("sit", "writing.mp4", "Step 2: 2,000 words", "YOU: writing on a terrace, sea behind")]),
        ("Lunch. A long nap. A little more work in the evening.",
         [full("Lunch", "lunch_nap.mp4", "Step 3: lunch, nap", "YOU: lunch with a view, then a hammock")]),
        ("That's it. That's the schedule that built fourteen Bond books.",
         [top("schedule", "bond_books.jpg", "14 books", "YOU: a stack of the paperbacks")]),
        ("So, I did it. Here's my two thousand words, written with salt still in my hair.",
         [top("Here's", "my_pages.mp4", "My 2,000 words", "YOU: flipping through your written pages")]),
        ("Honest review: the swim makes the writing easier. Your brain shows up already awake.", [full("Honest")]),
        ("Fleming didn't separate the life from the work. The sea is all over those books.", []),
        ("Follow for the next legend's footsteps.", []),
     ],
     end_card=dict(at="Follow", title=SERIES, sub="Next week: a new legend"),
     verify=["his routine (morning swim, about 2,000 words, nap, evening revision) from his essay 'How to Write a Thriller'",
             "only say the 'honest review' line if it's true for you"]),
]


def anchor_for(at, words, lo, hi):
    """Return at or at#n so that it resolves inside tokens [lo, hi)."""
    for n in range(1, 30):
        cand = at if n == 1 else f"{at}#{n}"
        i = find_word(cand, words)
        if i is None:
            break
        if lo <= i < hi:
            return cand
    raise SystemExit(f"anchor '{at}' not found in its line")


def build(script):
    words, ranges = [], []
    for line, _ in script["lines"]:
        toks = line.split()
        ranges.append((len(words), len(words) + len(toks)))
        words += [{"text": t} for t in toks]
    panels = []
    for (line, ps), (lo, hi) in zip(script["lines"], ranges):
        for p in ps:
            p = {k: v for k, v in p.items() if k != "desc" and v is not None}
            p["at"] = anchor_for(p["at"], words, lo, hi)
            panels.append(p)
    ec = dict(script["end_card"])
    ec["at"] = anchor_for(ec["at"], words, *ranges[-1]) if ec["at"] in script["lines"][-1][0] \
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


def md(script, n_words):
    out = [f"### {script['version']}. {script['fmt']}: `{script['id']}`", ""]
    out.append(f"**Length:** {script['length']} ({n_words} words). **Film:** {script['film']}")
    out.append("")
    refs = " · ".join(f"[{name}]({url}) ({note})" for name, url, note in REFS[script["fmt"]])
    out.append(f"**Watch first:** {refs}. "
               f"[Editing breakdown](BREAKDOWNS.md#{BREAKDOWN_ANCHOR[script['fmt']]})")
    out.append("")
    if script.get("ref"):
        out.append(f"**What to copy:** {script['ref']}.")
        out.append("")
    if script.get("title"):
        t = script["title"]["text"].replace(chr(10), " / ")
        out.append(f"**Opening title** (until \"{script['title']['until']}\"): *{t}*")
        out.append("")
    out.append("| Say | On screen |")
    out.append("|---|---|")
    for line, ps in script["lines"]:
        cells = []
        for p in ps:
            if p.get("full") == "talk":
                cells.append("you, full screen")
            elif p.get("full"):
                lab = f" · pill **{p['label'].upper()}**" if p.get("label") else ""
                cells.append(f"full screen `{p['full']}`{lab}")
            else:
                cz = " (pixelated)" if p.get("censor") else ""
                cells.append(f"top `{p['file']}`{cz} · pill **{p['label'].upper()}**")
        out.append(f"| {line} | {'<br>'.join(cells)} |")
    out.append("")
    ec = script["end_card"]
    out.append(f"End card from \"{ec['at']}\": **{ec['title'].upper()}** / {ec['sub'].upper()}")
    out.append("")
    files = {}
    for _, ps in script["lines"]:
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
    sections, groups = {}, {}
    for s in SCRIPTS:
        plan, n = build(s)
        (plans_dir / f"{s['id']}.json").write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n")
        sections.setdefault(s["legend"], []).append(md(s, n))
        groups[s["legend"]] = s.get("group", "option")
    here = Path(__file__).parent
    head = (here / "scripts_head.md").read_text()
    options = (here / "option_three.md").read_text()
    main_legends = [l for l in sections if groups[l] == "main"]
    ready = [l for l in sections if groups[l] != "main"]
    body = "\n---\n\n".join(f"## Legend {i}: {legend}\n\n" + "\n".join(sections[legend])
                              for i, legend in enumerate(main_legends, 1))
    body += "\n---\n\n" + options + "\n" + "\n---\n\n".join(
        f"### Bench, ready to film: {legend}\n\n" + "\n".join(sections[legend]).replace("\n### ", "\n#### ").replace("### ", "#### ", 1)
        for legend in ready)
    (REPO / "series/lifestyle-legends/SCRIPTS.md").write_text(head + "\n" + body)
    print(f"{len(SCRIPTS)} scripts, plans in {plans_dir}")


if __name__ == "__main__":
    main()
