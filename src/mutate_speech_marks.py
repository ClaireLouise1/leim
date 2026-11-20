#!/usr/bin/env python3
"""Mutation check for Speech Marks Sprint: plants one mistake at a time in the built page and makes sure the checker fails.
Usage: python3 src/mutate_speech_marks.py   (~30 s)"""
import subprocess, os, sys
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC)
page = open(os.path.join(ROOT, "speech-marks-sprint.html"), encoding="utf-8").read()
M = [
 ("statement tagged as a question", '["I\'m starving", "said Dara", "a"]', '["I\'m starving", "asked Dara", "a"]'),
 ("comma moved outside the speech marks", '''return it[2]==="a"?'"'+sp+END_A[k]+'" '+tag+".":''', '''return it[2]==="a"?'"'+sp+'"'+END_A[k]+" "+tag+".":'''),
 ("statement ends with a full stop before the tag", 'var END_A={s:",",', 'var END_A={s:".",'),
 ("no comma after said", '''tag+', "'+sp+END_B[k]+'"';}''', '''tag+' "'+sp+END_B[k]+'"';}'''),
 ("shouted no longer a shout", 'EV=["shouted","yelled",', 'EV=["yelled",'),
 ("ambiguous comma offered for a shout", 'x!==(a?",":".")', 'x!==(a?"?":".")'),
 ("inside-mark answer uses the wrong layout", 'mk=(a?END_A:END_B)[k]', 'mk=(a?END_B:END_A)[k]'),
 ("semicolon item tagged colon", '["Dara loves hurling ___ his sister prefers soccer.", "s"]', '["Dara loves hurling ___ his sister prefers soccer.", "c"]'),
 ("semicolon item gets a joining word", '"Mam likes tea ___ Dad drinks coffee."', '"Mam likes tea ___ and Dad drinks coffee."'),
 ("colon / semicolon labels swapped", 'var JL={c:"Colon :",s:"Semicolon ;"};', 'var JL={c:"Semicolon ;",s:"Colon :"};'),
 ("is no longer moves back to was", 'var BACK={am:"was",is:"was"', 'var BACK={am:"was",is:"is"'),
 ("I becomes he for a girl", 'PR={f:{I:"she"', 'PR={f:{I:"he"'),
 ("speaker's gender flipped in the data", '["I am tired", "said Niamh", "f"]', '["I am tired", "said Niamh", "m"]'),
 ("reported question uses that", '" asked if "', '" asked that "'),
 ("reported sentence starts lower case", 'function who(tag){return cap(tag.split(" ").slice(1).join(" "));}', 'function who(tag){return tag.split(" ").slice(1).join(" ");}'),
 ("speech keeps its own end mark", '["Run", "cried Fionn", "a"]', '["Run!", "cried Fionn", "a"]'),
 ("capital pronoun after the speech", '["The bus is late again", "Mam said", "a"]', '["The bus is late again", "She said", "a"]'),
]
ok = 0
for name, a, b in M:
    assert page.count(a) == 1, (name, page.count(a))
    open("/tmp/sm_mut.html", "w", encoding="utf-8").write(page.replace(a, b))
    j = subprocess.run(["node", os.path.join(SRC, "test_speech_marks.js"), "/tmp/sm_mut.html"], capture_output=True, text=True, env={**os.environ, "N": "200"})
    open("/tmp/sm_mut.jsonl", "w").write(j.stdout)
    r = subprocess.run([sys.executable, os.path.join(SRC, "test_speech_marks.py"), "/tmp/sm_mut.jsonl", "/tmp/sm_mut.html"], capture_output=True, text=True)
    caught = r.returncode != 0 and j.returncode == 0 and j.stdout.count("\n") > 1000
    first = (r.stdout.splitlines() or [""])[0][:130]
    ok += caught; print("caught" if caught else "MISSED", "·", name, "·", first, flush=True)
print(f"{ok}/{len(M)} caught"); sys.exit(0 if ok == len(M) else 1)
