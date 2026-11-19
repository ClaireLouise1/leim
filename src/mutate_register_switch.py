#!/usr/bin/env python3
"""Mutation check for Register Switch: plants one mistake at a time in the built page and makes sure the checker fails.
Usage: python3 src/mutate_register_switch.py   (~20 s)"""
import subprocess, os, sys
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC)
page = open(os.path.join(ROOT, "register-switch.html"), encoding="utf-8").read()
M = [
 ("formal and informal lines swapped", '"I wish to complain about the poor bus service in our town.", "The bus is so late every day, it\'s a joke!"', '"The bus is so late every day, it\'s a joke!", "I wish to complain about the poor bus service in our town."'),
 ("slang inside a formal line", '"I would be grateful for a full refund."', '"I would be grateful for a full refund, cheers."'),
 ("informal line made formal", '"Running late, soz! Be there in ten mins."', '"I apologise, I will be there in ten minutes."'),
 ("formal reader moved to informal situation", '"👦 Chat with your brother: the park needs bins"', '"📰 Letter to the newspaper editor about the bins"'),
 ("polite line tagged blunt", '["Would you mind closing the window?", "p"]', '["Would you mind closing the window?", "b"]'),
 ("blunt line tagged polite", '["Shut the door.", "b"]', '["Shut the door.", "p"]'),
 ("polite answer still an order", '"Could you close the door, please?"', '"Close the door, please!"'),
 ("blunt wrong option made polite", '"Lend me your charger!"', '"Could you lend me your charger?"'),
 ("tone tagged wrong", '["Dad was furious about the broken window.", "an"]', '["Dad was furious about the broken window.", "sa"]'),
 ("tone line with two tones", '"I miss my old school and my friends there."', '"I miss my old school and I am worried about the new one."'),
 ("slang braces on a plain word", '"The old bridge looks {dodgy} after the storm."', '"The old {bridge} looks unsafe after the storm."'),
 ("two slang words in one sentence", '"The trip to Dublin was {epic} and everyone enjoyed it."', '"The trip to Dublin was {epic} and loads enjoyed it."'),
 ("tone labels swapped", 'sa:"😢 Sad",an:"😠 Angry"', 'sa:"😠 Angry",an:"😢 Sad"'),
 ("polite/blunt labels swapped", 'var POLL={p:"😊 Polite",b:"🙄 Blunt"}', 'var POLL={p:"🙄 Blunt",b:"😊 Polite"}'),
 ("switch answer flipped in code", 'sit=f?it[0]:it[1],ans=f?it[2]:it[3]', 'sit=f?it[0]:it[1],ans=f?it[3]:it[2]'),
 ("slang answer taken from the wrong word", 'return C("🔍 Which word is too slangy?",w,ws', 'return C("🔍 Which word is too slangy?",ws[0],ws.slice(1).concat([w])'),
]
ok = 0
for name, a, b in M:
    assert page.count(a) == 1, (name, page.count(a))
    open("/tmp/rs_mut.html", "w", encoding="utf-8").write(page.replace(a, b))
    j = subprocess.run(["node", os.path.join(SRC, "test_register_switch.js"), "/tmp/rs_mut.html"], capture_output=True, text=True, env={**os.environ, "N": "200"})
    open("/tmp/rs_mut.jsonl", "w").write(j.stdout)
    r = subprocess.run([sys.executable, os.path.join(SRC, "test_register_switch.py"), "/tmp/rs_mut.jsonl", "/tmp/rs_mut.html"], capture_output=True, text=True)
    caught = r.returncode != 0 and j.returncode == 0 and j.stdout.count("\n") > 800
    first = (r.stdout.splitlines() or [""])[0][:120]
    ok += caught; print("caught" if caught else "MISSED", "·", name, "·", first, flush=True)
print(f"{ok}/{len(M)} caught"); sys.exit(0 if ok == len(M) else 1)
