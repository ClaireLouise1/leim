#!/usr/bin/env python3
"""Mutation check for Fact or Opinion: plants one mistake at a time in the built page and makes sure the checker fails.
Usage: python3 src/mutate_fact_or_opinion.py   (~20 s)"""
import subprocess, os, sys
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC)
page = open(os.path.join(ROOT, "fact-or-opinion.html"), encoding="utf-8").read()
M = [
 ("an opinion slipped into the fact list", '"The new bridge has two cycle lanes."', '"The new bridge has the best cycle lanes."'),
 ("a fact slipped into the opinion list", '"School lunches are boring."', '"School lunches cost €4."'),
 ("fo answer flipped", 'var isF=Math.random()<.5,s=rnd(isF?D.fo.f:D.fo.o),ans=isF?FO[0]:FO[1];', 'var isF=Math.random()<.5,s=rnd(isF?D.fo.f:D.fo.o),ans=isF?FO[1]:FO[0];'),
 ("spot text's op key wrong", '"op": [3]}', '"op": [2]}'),
 ("spot line turned into a second opinion", '"Every cake costs €2."', '"Every cake is delicious."'),
 ("spot: asks for the wrong kind", 'var want=nf===1?FO[0]:FO[1],i=ks.indexOf(want);', 'var want=nf===1?FO[1]:FO[0],i=ks.indexOf(want);'),
 ("spot: answer one line off", 'var want=nf===1?FO[0]:FO[1],i=ks.indexOf(want);', 'var want=nf===1?FO[0]:FO[1],i=(ks.indexOf(want)+1)%4;'),
 ("line: highlights a different line", 'card(T,j),{t:"line"', 'card(T,(j+1)%4),{t:"line"'),
 ("chart: two bars the same height", '["Soccer", 35]', '["Soccer", 45]'),
 ("chart: bars drawn too tall", 'G.bars.forEach(function(b,i){var h=b[1]*S,', 'G.bars.forEach(function(b,i){var h=b[1]*S*1.1,'),
 ("chart: labels in the wrong order", "esc(b[0])+'</text>';});", "esc(G.bars[(i+1)%n][0])+'</text>';});"),
 ("chart: highest picks the lowest", 'hi=vals.indexOf(Math.max.apply(null,vals))', 'hi=vals.indexOf(Math.min.apply(null,vals))'),
 ("chart: difference added", 'var d=vals[i]-vals[j],pool', 'var d=vals[i]+vals[j]-10,pool'),
 ("chart: value answer from the next bar", 'C("📊 How many: "+labs[i]+"?",String(vals[i])', 'C("📊 How many: "+labs[i]+"?",String(vals[(i+1)%B.length])'),
 ("poster: caption and headline labels swapped", 'var KEYS=["head","img","cap","when","con"];', 'var KEYS=["cap","img","head","when","con"];'),
 ("poster: contact in the when line", '"when": "Saturday 31 October, 7 p.m., Doneraile Park", "con": "Book on 087 555 0142"', '"when": "Saturday 31 October, 7 p.m., Doneraile Park", "con": "Book on Saturday 31 October, 7 p.m."'),
 ("poster: highlight on another part", "(k===hl?' hl':'')", "(k===(hl===\"head\"?\"img\":hl)?' hl':'')"),
]
ok = 0
for name, a, b in M:
    assert page.count(a) == 1, (name, page.count(a))
    open("/tmp/fo_mut.html", "w", encoding="utf-8").write(page.replace(a, b))
    j = subprocess.run(["node", os.path.join(SRC, "test_fact_or_opinion.js"), "/tmp/fo_mut.html"], capture_output=True, text=True, env={**os.environ, "N": "80"})
    open("/tmp/fo_mut.jsonl", "w").write(j.stdout)
    r = subprocess.run([sys.executable, os.path.join(SRC, "test_fact_or_opinion.py"), "/tmp/fo_mut.jsonl", "/tmp/fo_mut.html"], capture_output=True, text=True)
    caught = r.returncode != 0 and j.returncode == 0 and j.stdout.count("\n") > 300
    out = (r.stdout + r.stderr).strip().splitlines()
    first = next((l for l in out if "PROBLEM" in l or "Error" in l), out[-1] if out else "")[:150]
    ok += caught; print("caught" if caught else "MISSED", "·", name, "·", first, flush=True)
print(f"{ok}/{len(M)} caught"); sys.exit(0 if ok == len(M) else 1)
