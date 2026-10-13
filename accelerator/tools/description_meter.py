#!/usr/bin/env python3
"""Description meter: how 'read-story' vs 'video-ready' a script is.

Usage: python3 tools/description_meter.py <script-file> [--target song|vo|drama|bof]

Measures the spoken words only (stage directions in [ ] or ( ), and lines starting
with VISUAL / OST / TIME / AUDIO / Visual are ignored), reports where the script
sits on the scale in workflows/video-description-scale.md, and lists the lines
that carry description the camera should carry instead.
"""
import re, sys, statistics as st

TARGETS = {  # from the Lymphoria winners, measured 2026-10-01
    'song':  dict(words=(900, 1700), sent=(4.5, 6.0), frag=40, intens=2.0, place=2.5, scen=3.0),
    'vo':    dict(words=(1200, 2100), sent=(5.5, 7.0), frag=40, intens=2.5, place=2.5, scen=3.0),
    'drama': dict(words=(400, 1600), sent=(4.0, 7.5),  # floor 4.0: Veteran Reunion winner runs 4.2
                   frag=40, intens=3.0, place=4.5, scen=1.5),
    'bof':   dict(words=(20, 200), sent=(4.0, 9.0), frag=20, intens=3.0, place=1.0, scen=1.0),
}
SCENERY = r'\b(sunset|sunrise|golden hour|fluorescent|lamp|candle(s)?|torch(es)?|breeze|rain|snow|ocean|pacific|sky|waves|mahogany|granite|quartz|marble|wooden|oak|chandelier|curtains?|wicker|overlooking|string lights|lantern(s)?)\b'
APPEAR = r'\b(blonde|brunette|glossy|lipstick|highlights|backless|sundress|silk|linen|velvet|coral|emerald|crisp|sculpted|radiant|glowing|elegant|stunning|gorgeous|toned|tan(ned)?)\b'
BLOCKING = r'\b(stepped (back|toward|away|beside)|half-step|leaned (in|over|across)|drifted|cut me off|by the coat rack|turned (his|her) head|crossed (his|her) arms|walked (straight|right) (over|past|up))\b'
FACE = r"\b((his|her) (face|jaw|mouth|eyes) (went|dropped|fell|lit|widened)|jaw (literally )?dropped|went (white|red|pale)|froze)\b"
INNER = r"\b(i thought|i felt|i told myself|i realized|i wondered|something (clicked|broke)|my (heart|chest|throat|ribs)|crept into|the ugliest thought)\b"
INTENS = r'\b(completely|literally|truly|entirely|exactly|absolutely|genuinely|actually|really|totally|utterly|incredibly|visibly|immediately|suddenly|slowly|quietly|gently|calmly)\b'
PLACE = r'\b(overlooking|under the|across the|beside the|next to the|in front of|at the end of|behind the|on the edge of|out onto|through the|along the|by the window)\b'
THROAT = r"^(let me back up|here('| i)s (the|what) (biggest|thing)|so here's what happened|i want to be honest)"

def spoken_lines(text):
    for raw in text.split('\n'):
        s = raw.strip()
        if not s or re.match(r'^(\||#|---|(\*\*)?(VISUAL|Visual|OST|ON-SCREEN|TIME|AUDIO|Format|Naming|Related|Filed)\b|\(Visual)', s):
            continue
        # emoji-tagged A/V scripts: only 🗣 lines are spoken; 🎬 🎥 ⏱ ➡ and scene headers are not
        if s.startswith(('🎬', '🎥', '⏱', '➡')) or re.match(r'^(HOOK|SCENE|HOLD)\b', s):
            continue
        s = re.sub(r'^🗣\s*', '', s)
        s = re.sub(r'\[[^\]]*\]', '', s)
        s = re.sub(r'\((?:[^()]*?)\)', '', s)
        s = re.sub(r"^[A-Z][A-Z .'/]+(\([^)]*\))?:\s*", '', s)
        if s.strip():
            yield s.strip()

def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    target = 'song'
    if '--target' in sys.argv:
        target = sys.argv[sys.argv.index('--target') + 1]
    t = TARGETS[target]
    lines = list(spoken_lines(open(sys.argv[1]).read()))
    text = '\n'.join(lines)
    words = re.findall(r"[A-Za-z0-9'’]+", text); n = max(len(words), 1)
    sents = [s for s in re.split(r'(?<=[.!?])\s+|\n', text) if re.search(r'[A-Za-z]', s)]
    sl = [len(s.split()) for s in sents]
    low = text.lower()
    per1k = lambda p: round(1000 * len(re.findall(p, low)) / n, 1)
    m = dict(words=n, sent=round(st.mean(sl), 1), frag=round(100 * sum(x <= 4 for x in sl) / len(sl)),
             intens=per1k(INTENS), place=per1k(PLACE), scen=per1k(SCENERY) + per1k(APPEAR))
    print(f'Target: {target}')
    def row(k, label, ok):
        print(f"  {'OK ' if ok else 'FIX'} {label}: {m[k]}  (target {t[k]})")
    row('words', 'spoken words', t['words'][0] <= m['words'] <= t['words'][1])
    row('sent', 'avg words per sentence', t['sent'][0] <= m['sent'] <= t['sent'][1])
    row('frag', '% short lines (4 words or fewer)', m['frag'] >= t['frag'])
    row('intens', 'adverbs/intensifiers per 1k', m['intens'] <= t['intens'])
    row('place', 'place phrases per 1k', m['place'] <= t['place'])
    row('scen', 'scenery + appearance per 1k', m['scen'] <= t['scen'])
    print('\nLines to move to visuals or cut:')
    checks = [('scenery', SCENERY), ('appearance', APPEAR), ('blocking', BLOCKING), ('face-narration', FACE),
              ('interior', INNER), ('adverb', INTENS), ('throat-clearing', THROAT)]
    for s in lines:
        tags = [name for name, p in checks if re.search(p, s.lower())]
        if tags:
            print(f"  [{', '.join(tags)}] {s[:140]}")

if __name__ == '__main__':
    main()
