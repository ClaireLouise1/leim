#!/usr/bin/env python3
"""Mutation check for Who Said It?: plants one mistake at a time in the built page and makes sure the checker fails.
Usage: python3 src/mutate_who_said_it.py   (~2 min)"""
import subprocess, os, sys
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC)
page = open(os.path.join(ROOT, "who-said-it.html"), encoding="utf-8").read()
A = '  ["rj", "Capulet orders Juliet to marry Paris.", "Hang thee, young baggage!"],\n'
B = '  ["rj", "Juliet drinks the Friar\'s potion.", "Romeo, I come! this do I drink to thee."],\n'
M = [
 ("speaker swapped in the data", '["rj", "Thus with a kiss I die.", "ro"', '["rj", "Thus with a kiss I die.", "ju"'),
 ("wrong act and scene", '"O happy dagger!", "ju", "5.3"', '"O happy dagger!", "ju", "4.3"'),
 ("Romeo / Juliet labels swapped", 'ro:"Romeo",ju:"Juliet"', 'ro:"Juliet",ju:"Romeo"'),
 ("Brutus / Cassius labels swapped", 'br:"Brutus",cu:"Cassius"', 'br:"Cassius",cu:"Brutus"'),
 ("quote put in the wrong play", '["jc", "it was Greek to me"', '["mv", "it was Greek to me"'),
 ("technique flipped", '["jc", "Was this ambition?", "qu"]', '["jc", "Was this ambition?", "si"]'),
 ("oxymoron / simile labels swapped", 'ox:"🔀 Oxymoron",si:"🤝 Simile"', 'ox:"🤝 Simile",si:"🔀 Oxymoron"'),
 ("old word meaning wrong", '"{Tarry} a little; there is something else.", "wait"', '"{Tarry} a little; there is something else.", "go away"'),
 ("old word answer taken from the pool", 'C("📜 What does it mean?",m,', 'C("📜 What does it mean?",pool[0],'),
 ("look-alike meanings no longer filtered", 'return x!==m&&!close(x,m);', 'return x!==m;'),
 ("plot answer reversed", 'var ans=[0,1,2,3]', 'var ans=[3,2,1,0]'),
 ("plot moments not sorted", '.slice(0,4).sort(function(a,b){return a-b;})', '.slice(0,4)'),
 ("two plot moments in the wrong order", A + B, B + A),
 ("which-play answer wrong", 'C("📚 Which play?",PLAY[it[0]],others(PLAY,it[0])', 'C("📚 Which play?",PLAY[it[0]==="rj"?"mv":it[0]],others(PLAY,it[0]==="rj"?"mv":it[0])'),
 ("who options from another play", 'others(L,it[2]).filter', 'others(CH[p==="rj"?"jc":"rj"],"x").filter'),
 ("act and scene swapped in the explanation", 'return "Act "+p[0]+", Scene "+p[1];', 'return "Act "+p[1]+", Scene "+p[0];'),
 ("couplet changed so it no longer rhymes", 'or worse days endure.', 'or worse days follow.'),
]
ok = 0
for name, a, b in M:
    assert page.count(a) == 1, (name, page.count(a))
    open("/tmp/wsi_mut.html", "w", encoding="utf-8").write(page.replace(a, b))
    j = subprocess.run(["node", os.path.join(SRC, "test_who_said_it.js"), "/tmp/wsi_mut.html"], capture_output=True, text=True, env={**os.environ, "N": "60"})
    open("/tmp/wsi_mut.jsonl", "w").write(j.stdout)
    r = subprocess.run([sys.executable, os.path.join(SRC, "test_who_said_it.py"), "/tmp/wsi_mut.jsonl", "/tmp/wsi_mut.html"], capture_output=True, text=True)
    caught = r.returncode != 0 and j.returncode == 0 and j.stdout.count("\n") > 500
    out = (r.stdout + r.stderr).strip().splitlines()
    first = next((l for l in out if "PROBLEM" in l or "Error" in l), out[-1] if out else "")[:140]
    ok += caught; print("caught" if caught else "MISSED", "·", name, "·", first, flush=True)
print(f"{ok}/{len(M)} caught"); sys.exit(0 if ok == len(M) else 1)
