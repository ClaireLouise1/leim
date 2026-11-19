#!/usr/bin/env python3
"""Mutation check for Technique Spotter: plants one mistake at a time in the built page and makes sure the checker fails.
Usage: python3 src/mutate_technique_spotter.py   (~30 s)"""
import subprocess, os, sys
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC)
page = open(os.path.join(ROOT, "technique-spotter.html"), encoding="utf-8").read()
M = [
 ("onomatopoeia item tagged personification", '["The bacon sizzled in the pan.", "ono"]', '["The bacon sizzled in the pan.", "per"]'),
 ("wrong vehicle in a simile", '"moon", "coin"', '"moon", "town"'),
 ("poem asks the wrong line", '["met", 1], ["ono", 2], ["sim", 3]', '["met", 1], ["ono", 2], ["sim", 2]'),
 ("sound line tagged sight", '["Thunder rumbled over the hills.", "hear"]', '["Thunder rumbled over the hills.", "see"]'),
 ("a wrong option that rhymes", '["eight", "knit", "nice"]', '["light", "knit", "nice"]'),
 ("a rhyme answer that doesn't rhyme", '["cold", "gold",', '["cold", "cloud",'),
 ("labels swapped in the code", 'sim:"🤝 Simile",met:"🪞 Metaphor"', 'sim:"🪞 Metaphor",met:"🤝 Simile"'),
 ("compare answer uses another line's thing", 'it[2]+" ↔ "+it[3],pool', 'it[2]+" ↔ "+o[0][3],pool'),
 ("which-line answer off by one", '"Line "+a[1],LINES', '"Line "+(a[1]%4+1),LINES'),
 ("sense answer wrong for sight", 'C("Which sense?",SLAB[it[1]]', 'C("Which sense?",SLAB[it[1]==="see"?"hear":it[1]]'),
 ("alliteration item without alliteration", '"Happy hens hurried home."', '"Happy chickens ran back."'),
 ("personification item without a human verb", '"The flowers danced in the breeze."', '"The flowers moved in the breeze."'),
]
ok = 0
for name, a, b in M:
    assert page.count(a) == 1, (name, page.count(a))
    open("/tmp/ts_mut.html", "w", encoding="utf-8").write(page.replace(a, b))
    j = subprocess.run(["node", os.path.join(SRC, "test_technique_spotter.js"), "/tmp/ts_mut.html"], capture_output=True, text=True, env={**os.environ, "N": "150"})
    open("/tmp/ts_mut.jsonl", "w").write(j.stdout)
    r = subprocess.run([sys.executable, os.path.join(SRC, "test_technique_spotter.py"), "/tmp/ts_mut.jsonl", "/tmp/ts_mut.html"], capture_output=True, text=True)
    caught = r.returncode != 0 and j.returncode == 0 and j.stdout.count("\n") > 1000
    ok += caught; print("caught" if caught else "MISSED", "·", name)
print(f"{ok}/{len(M)} caught"); sys.exit(0 if ok == len(M) else 1)
