#!/usr/bin/env python3
"""Mutation check for Story Spine: plants one mistake at a time in the built page and makes sure the checker fails.
Usage: python3 src/mutate_story_spine.py   (~1 min)"""
import subprocess, os, sys
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC)
page = open(os.path.join(ROOT, "story-spine.html"), encoding="utf-8").read()
M = [
 ("spine line about something else", '"Because of that, Fionn had to stand in goal for the cup final."', '"Because of that, the swans flew south for the winter."'),
 ("spine line that fits another story", '"Every day, Leah practised the drums in the shed for two hours."', '"Every day, Leah practised the drums in the bakery for two hours."'),
 ("spine phrase missing", '"Until finally, the hens felt safe and laid more eggs than ever."', '"In the end, the hens felt safe and laid more eggs than ever."'),
 ("off-track event that belongs", '"Dad paints the kitchen yellow."', '"Dad paints the guitar yellow."'),
 ("on-track event that doesn't link", '"We search the sand dunes until dark."', '"We search the car park until dark."'),
 ("narrator tagged wrong", '["The teacher handed me the trophy.", 1]', '["The teacher handed me the trophy.", 3]'),
 ("third-person line with a first-person word", '"The old house frightened the twins."', '"The old house frightened us."'),
 ("steady: right line in the wrong tense", '"I saw a fox in the garden.", "I see a fox in the garden."', '"I see a fox in the garden.", "I saw a fox in the garden."'),
 ("steady: narrator-only option also changes tense", '"They ate their sandwiches beside the cairn."', '"They eat their sandwiches beside the cairn!"'),
 ("ending that doesn't solve the problem", '"In the end, we patched the hole with tape and slept in our coats."', '"In the end, we went home and watched a film."'),
 ("from-nowhere ending that links", '"In the end, my teacher turned into a frog and hopped away."', '"In the end, my teacher turned into a frog and ate the power cable."'),
 ("another story's ending that fits this one", "handed it back.\"", "handed it back on Saturday.\""),
 ("spine answer from the wrong gap", 'C("🦴 What happens next?",body(S.lines[g],g)', 'C("🦴 What happens next?",body(S.lines[g%4+1],g%4+1)'),
 ("cut answer off by one", 'LINES[pos-1],LINES', 'LINES[pos%4],LINES'),
 ("narrator labels swapped", 'var POV={1:"🙋 First person (I)",3:"👀 Third person (he / she)"};', 'var POV={3:"🙋 First person (I)",1:"👀 Third person (he / she)"};'),
 ("ending: another story may be this story", 'other=rnd(D.ends.filter(function(x){return x!==E;}))', 'other=rnd(D.ends)'),
]
ok = 0
for name, a, b in M:
    assert page.count(a) == 1, (name, page.count(a))
    open("/tmp/sp_mut.html", "w", encoding="utf-8").write(page.replace(a, b))
    j = subprocess.run(["node", os.path.join(SRC, "test_story_spine.js"), "/tmp/sp_mut.html"], capture_output=True, text=True, env={**os.environ, "N": "60"})
    open("/tmp/sp_mut.jsonl", "w").write(j.stdout)
    r = subprocess.run([sys.executable, os.path.join(SRC, "test_story_spine.py"), "/tmp/sp_mut.jsonl", "/tmp/sp_mut.html"], capture_output=True, text=True)
    caught = r.returncode != 0 and j.returncode == 0 and j.stdout.count("\n") > 500
    ok += caught; print("caught" if caught else "MISSED", "·", name, flush=True)
print(f"{ok}/{len(M)} caught"); sys.exit(0 if ok == len(M) else 1)
