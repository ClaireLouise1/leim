#!/usr/bin/env python3
"""Mutation check for Mood Match: plants one mistake at a time in the built page and makes sure the checker fails.
Usage: python3 src/mutate_mood_match.py   (~30 s)"""
import subprocess, os, sys
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC)
page = open(os.path.join(ROOT, "mood-match.html"), encoding="utf-8").read()
M = [
 ("joyful couplet tagged sad", '["The children {danced} across the yard / as the first snow tumbled down.", "jo"]', '["The children {danced} across the yard / as the first snow tumbled down.", "sa"]'),
 ("peaceful couplet made angry", '"The lake lies {calm} at evening, / a mirror for the hills."', '"The lake lies {furious} at evening, / a mirror for the hills."'),
 ("wrong word braced", '"The dog {snarled} at the gate, / showing every yellow tooth."', '"The dog snarled at the {gate}, / showing every yellow tooth."'),
 ("tense couplet gets a second mood word", '"I {trembled} at the cliff edge / with the black water far below."', '"I {trembled} at the cliff edge / with the calm water far below."'),
 ("tone labels swapped", 'jo:"😊 Joyful",sa:"😢 Sad"', 'jo:"😢 Sad",sa:"😊 Joyful"'),
 ("look-alike rule dropped", 'var CLOSE={sa:"no",no:"sa"};', 'var CLOSE={};'),
 ("mood-word pool offers mood-heavy words (dark, rain)", 'MOODY.indexOf(lw)<0&&', ''),
 ("friendship poem tagged nature", '{"k": "🪑 The Bench", "t": "fr"', '{"k": "🪑 The Bench", "t": "na"'),
 ("loss poem gets a home word", '"beside the back door,"', '"beside the front door,"'),
 ("theme labels swapped", 'lo:"💔 Loss",na:"🌿 Nature"', 'lo:"🌿 Nature",na:"💔 Loss"'),
 ("shift tagged the wrong way round", '{"k": "🌙 Night Walk", "a": "ca", "b": "te"', '{"k": "🌙 Night Walk", "a": "te", "b": "ca"'),
 ("shift loses its turn", '"and my heart began pounding."', '"and the stars were calm."'),
 ("shift answer arrow reversed", 'C("🔄 How does the mood change?",arrow(a,b)', 'C("🔄 How does the mood change?",arrow(b,a)'),
 ("pair shares no theme", '"The village lights come into view"', '"The motorway lights come into view"'),
 ("pair tones tagged the wrong way round", '"ta": "ca", "kb": "🌲 Forest at Night"', '"ta": "te", "kb": "🌲 Forest at Night"'),
 ("diff answer swaps A and B", 'C("🔀 How are the moods different?",lab(a,b)', 'C("🔀 How are the moods different?",lab(b,a)'),
]
ok = 0
for name, a, b in M:
    assert page.count(a) == 1, (name, page.count(a))
    open("/tmp/mm_mut.html", "w", encoding="utf-8").write(page.replace(a, b))
    j = subprocess.run(["node", os.path.join(SRC, "test_mood_match.js"), "/tmp/mm_mut.html"], capture_output=True, text=True, env={**os.environ, "N": "200"})
    open("/tmp/mm_mut.jsonl", "w").write(j.stdout)
    r = subprocess.run([sys.executable, os.path.join(SRC, "test_mood_match.py"), "/tmp/mm_mut.jsonl", "/tmp/mm_mut.html"], capture_output=True, text=True)
    caught = r.returncode != 0 and j.returncode == 0 and j.stdout.count("\n") > 1000
    first = (r.stdout.splitlines() or [""])[0][:130]
    ok += caught; print("caught" if caught else "MISSED", "·", name, "·", first, flush=True)
print(f"{ok}/{len(M)} caught"); sys.exit(0 if ok == len(M) else 1)
