#!/usr/bin/env python3
"""Mutation check for Talk Tips: plants one mistake at a time in the built page and makes sure the checker fails.
Usage: python3 src/mutate_talk_tips.py   (~3 min)"""
import subprocess, os, sys
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC)
page = open(os.path.join(ROOT, "talk-tips.html"), encoding="utf-8").read()
M = [
 ("good habit tagged avoid", '["do", "Look up at your audience"]', '["avoid", "Look up at your audience"]'),
 ("bad habit tagged do", '["avoid", "Stare at the floor"]', '["do", "Stare at the floor"]'),
 ("hook that announces the topic", '"What did you eat for breakfast this morning?"', '"Today I\'m going to talk about healthy breakfasts."'),
 ("hook off topic", '"Have you ever been woken up by a dog licking your face?"', '"Have you ever been woken up at six in the morning?"'),
 ("weak opener that is a fine hook", '"Today I\'m going to talk about "+t+"."', '"Did you know "+t+" can change your life?"'),
 ("hook type rule broken in code", 'return /\\?$/.test(s)?"q"', 'return /\\?$/.test(s)?"f"'),
 ("signpost tagged wrong", '["Moving on, let\'s look at the problems.", "m"]', '["Moving on, let\'s look at the problems.", "e"]'),
 ("end signpost tagged start", '["To sum up, dogs make great pets.", "e"]', '["To sum up, dogs make great pets.", "s"]'),
 ("good reply changes the subject", '"What did you put on your pizza?"', '"What did you put on your homework?"'),
 ("poor reply that is a good reply", '"Ugh, I hate cats."', '"What are the kittens called?"'),
 ("good reply is not a question", '"How far can you run now?"', '"You can run far now."'),
 ("discussion phrase tagged wrong", '["With respect, I disagree.", "di"]', '["With respect, I disagree.", "ag"]'),
 ("ask-for-more tagged join in", '["Why do you think that?", "as"]', '["Why do you think that?", "jo"]'),
 ("labels swapped", 's:"🚀 Start",m:"➡️ Next point"', 's:"➡️ Next point",m:"🚀 Start"'),
 ("answer swapped in code", 'return C("Good habit?",TIP[it[0]]', 'return C("Good habit?",TIP[it[0]==="do"?"avoid":"do"]'),
]
ok = 0
for name, a, b in M:
    assert page.count(a) == 1, (name, page.count(a))
    open("/tmp/tt_mut.html", "w", encoding="utf-8").write(page.replace(a, b))
    j = subprocess.run(["node", os.path.join(SRC, "test_talk_tips.js"), "/tmp/tt_mut.html"], capture_output=True, text=True, env={**os.environ, "N": "60"})
    open("/tmp/tt_mut.jsonl", "w").write(j.stdout)
    r = subprocess.run([sys.executable, os.path.join(SRC, "test_talk_tips.py"), "/tmp/tt_mut.jsonl", "/tmp/tt_mut.html"], capture_output=True, text=True)
    caught = r.returncode != 0 and j.returncode == 0 and j.stdout.count("\n") > 500
    ok += caught; print("caught" if caught else "MISSED", "·", name, flush=True)
print(f"{ok}/{len(M)} caught"); sys.exit(0 if ok == len(M) else 1)
