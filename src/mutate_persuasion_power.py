#!/usr/bin/env python3
"""Mutation check for Persuasion Power: plants one mistake at a time in the built page and makes sure the checker fails.
Usage: python3 src/mutate_persuasion_power.py   (~20 s)"""
import subprocess, os, sys
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC)
page = open(os.path.join(ROOT, "persuasion-power.html"), encoding="utf-8").read()
M = [
 ("question tagged as repetition", '["Who wants a town with nowhere safe to play?", "rq"]', '["Who wants a town with nowhere safe to play?", "rep"]'),
 ("statistic tagged emotive", '["Half of the students we asked said the canteen was too small.", "stat"]', '["Half of the students we asked said the canteen was too small.", "emo"]'),
 ("rule-of-three line loses its list", '"Sport teaches teamwork, patience and respect."', '"Sport teaches teamwork and respect."'),
 ("direct-address line with a number too", '"Your vote can change this town."', '"Your vote can change this town in 2 weeks."'),
 ("emotive line with no emotive word", '"Lonely pensioners sit at home with nobody to talk to."', '"Older people sit at home with nobody to talk to."'),
 ("repetition line with no repeat", '"We need action. We need it now."', '"We need action now."'),
 ("best reason with no evidence", '"More bins would cut litter: for example, the bin by the pier is full by noon every Saturday."', '"More bins would cut litter, and that would be nice."'),
 ("best reason made rude", '"Coding is useful in many jobs, such as medicine, farming and music."', '"Coding is useful in many jobs, such as medicine, unlike for lazy people."'),
 ("off-topic reason now on topic with evidence", '"The drama club meets on Fridays."', '"Plastic bottles cost the school 200 euro a year."'),
 ("best reply agrees", '"But discipline can also be learned through sport, music or a part-time job."', '"I agree that discipline matters most of all."'),
 ("best reply off the point", '"However, a refillable bottle is just as convenient and saves money too."', '"However, the canteen should open earlier."'),
 ("rude reply made polite and on topic", '"However, people who love uniforms are boring."', '"However, uniforms cannot stop bullying online."'),
 ("call to action that is not an order", '"Sign our petition today and help us plant fifty new trees."', '"Our petition about the trees is on the wall."'),
 ("call to action for the wrong topic", '"Email the principal and ask for a later start time."', '"Email the principal and ask for a new canteen."'),
 ("technique labels swapped", 'stat:"📊 Statistic",emo:"💔 Emotive language"', 'stat:"💔 Emotive language",emo:"📊 Statistic"'),
 ("back answer taken from the wrong slot", 'return C("💪 Best reason?",it[1],it[2]', 'return C("💪 Best reason?",it[2][2],[it[1],it[2][0],it[2][1]]'),
]
ok = 0
for name, a, b in M:
    assert page.count(a) == 1, (name, page.count(a))
    open("/tmp/pp_mut.html", "w", encoding="utf-8").write(page.replace(a, b))
    j = subprocess.run(["node", os.path.join(SRC, "test_persuasion_power.js"), "/tmp/pp_mut.html"], capture_output=True, text=True, env={**os.environ, "N": "200"})
    open("/tmp/pp_mut.jsonl", "w").write(j.stdout)
    r = subprocess.run([sys.executable, os.path.join(SRC, "test_persuasion_power.py"), "/tmp/pp_mut.jsonl", "/tmp/pp_mut.html"], capture_output=True, text=True)
    caught = r.returncode != 0 and j.returncode == 0 and j.stdout.count("\n") > 600
    first = (r.stdout.splitlines() or [""])[0][:120]
    ok += caught; print("caught" if caught else "MISSED", "·", name, "·", first, flush=True)
print(f"{ok}/{len(M)} caught"); sys.exit(0 if ok == len(M) else 1)
