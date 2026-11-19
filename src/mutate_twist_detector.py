#!/usr/bin/env python3
"""Mutation check for Twist Detector: plants one mistake at a time in the built page and makes sure the checker fails.
Usage: python3 src/mutate_talk_tips.py   (~1 min)"""
import subprocess, os, sys
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC)
page = open(os.path.join(ROOT, "twist-detector.html"), encoding="utf-8").read()
M = [
 ("clue line number wrong", '"clue": 3, "twist": "It turned out Sam', '"clue": 2, "twist": "It turned out Sam'),
 ("twist that comes from nowhere", '"It turned out to be a new alarm clock that Grandad had ordered online."', '"It turned out to be a bomb that a spy had ordered online."'),
 ("plain ending that is also a twist", '"Tom shrugged and went back to his homework."', '"Tom realised the sawdust was from his own school project."'),
 ("random ending that links to the story", '"It turned out the coach was a secret agent."', '"It turned out the changing room hook was a secret agent."'),
 ("twist links to two lines", '"It turned out the caretaker left it there for anyone caught in the rain."', '"It turned out the caretaker left the umbrella there for anyone caught in the rain."'),
 ("story lines out of order", '"Max had chased a seagull over the rocks and now there was no sign of him.", "Suddenly, a muddy brown head popped up from behind a rock pool."', '"Suddenly, a muddy brown head popped up from behind a rock pool.", "Max had chased a seagull over the rocks and now there was no sign of him."'),
 ("ending line with no ending marker", '"In the end, his painting won first prize."', '"His painting won first prize."'),
 ("hook tagged wrong", '"Oisín dived into the freezing lake before anyone could stop him.", "a"', '"Oisín dived into the freezing lake before anyone could stop him.", "m"'),
 ("dialogue tagged mystery", '"“Don\'t open that door!” screamed Tara.", "d"', '"“Don\'t open that door!” screamed Tara.", "m"'),
 ("hook that is weak", '"There was something strange about the new boy\'s shadow."', '"This is a story about the new boy\'s shadow."'),
 ("place tagged wrong", '["Pine needles crunched under my boots and an owl hooted.", "fo"]', '["Pine needles crunched under my boots and an owl hooted.", "fa"]'),
 ("place line with two places", '"Thick moss covered the fallen branches."', '"Thick moss covered the fallen branches by the tide."'),
 ("labels swapped", 'cl:"💥 Climax",en:"🏁 Ending"', 'cl:"🏁 Ending",en:"💥 Climax"'),
 ("part answer off by one in code", 'return C("Which part of the story?",PART[k]', 'return C("Which part of the story?",PART[PK[(i+1)%4]]'),
 ("order answer from wrong mapping", 'var ans=[1,2,3].map(function(n){return lets[idx.indexOf(n)];})', 'var ans=[1,2,3].map(function(n){return lets[n-1];})'),
 ("clue answer in code", 'C("🔎 Which line planted the clue?",LINES[T.clue-1]', 'C("🔎 Which line planted the clue?",LINES[T.clue%3]'),
]
ok = 0
for name, a, b in M:
    assert page.count(a) == 1, (name, page.count(a))
    open("/tmp/td_mut.html", "w", encoding="utf-8").write(page.replace(a, b))
    j = subprocess.run(["node", os.path.join(SRC, "test_twist_detector.js"), "/tmp/td_mut.html"], capture_output=True, text=True, env={**os.environ, "N": "60"})
    open("/tmp/td_mut.jsonl", "w").write(j.stdout)
    r = subprocess.run([sys.executable, os.path.join(SRC, "test_twist_detector.py"), "/tmp/td_mut.jsonl", "/tmp/td_mut.html"], capture_output=True, text=True)
    caught = r.returncode != 0 and j.returncode == 0 and j.stdout.count("\n") > 500
    ok += caught; print("caught" if caught else "MISSED", "·", name, flush=True)
print(f"{ok}/{len(M)} caught"); sys.exit(0 if ok == len(M) else 1)
