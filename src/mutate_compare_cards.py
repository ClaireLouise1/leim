#!/usr/bin/env python3
"""Mutation check for Compare Cards: plants one mistake at a time in the built page and makes sure the checker fails.
Usage: python3 src/mutate_compare_cards.py   (~20 s)"""
import subprocess, os, sys
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC)
page = open(os.path.join(ROOT, "compare-cards.html"), encoding="utf-8").read()
M = [
 ("text's narrator key wrong", '"f": {"p": "3", "t": "night", "pl": "sea", "e": "happy", "tr": "brave"}', '"f": {"p": "1", "t": "night", "pl": "sea", "e": "happy", "tr": "brave"}'),
 ("text's ending key wrong", '"f": {"p": "1", "t": "day", "pl": "farm", "e": "happy", "tr": "determined"}', '"f": {"p": "1", "t": "day", "pl": "farm", "e": "sad", "tr": "determined"}'),
 ("last line changed to a sad ending", '"When the vet came, Ruth grinned."', '"When the vet came, Ruth sighed."'),
 ("line now hits a second place", '"In the square at noon, the market was packed."', '"In the square at noon, the market by the harbour was packed."'),
 ("trait word swapped", '"Ruth shared her coat with the shivering calf."', '"Ruth climbed down to the shivering calf."'),
 ("labels: night/day swapped", 't:{night:"🌙 Set at night",day:"☀️ Set by day"}', 't:{night:"☀️ Set by day",day:"🌙 Set at night"}'),
 ("labels: two traits swapped", 'kind:"🤝 Kind hero",brave:"🦁 Brave hero"', 'kind:"🦁 Brave hero",brave:"🤝 Kind hero"'),
 ("phrase: farm/town swapped", 'farm:"is set on a farm",town:"is set in a town"', 'farm:"is set in a town",town:"is set on a farm"'),
 ("both: answer from a differing category", 'var c=rnd(sameCats(A,B)),ans=lab(c,A.f[c]),one=[]', 'var c=rnd(CATS),ans=lab(c,A.f[c]),one=[]'),
 ("both: a shared label slips into the wrong pool", 'if(ha&&hb)return;(ha||hb?one:none)', '(ha||hb?one:none)'),
 ("venn: only A / only B swapped", 'opts.push([k,v,ha&&hb?2:ha?0:1])', 'opts.push([k,v,ha&&hb?2:ha?1:0])'),
 ("venn: both counted as only A", 'opts.push([k,v,ha&&hb?2:ha?0:1])', 'opts.push([k,v,ha?0:hb?1:2])'),
 ("link: groups swapped", 'ans=rnd(same?SIM:CON);', 'ans=rnd(same?CON:SIM);'),
 ("link: second sentence uses text A's value", 's2=tq(B)+" "+PH[c][B.f[c]]+".";', 's2=tq(B)+" "+PH[c][A.f[c]]+".";'),
 ("best: whereas answer gives B text A's value", 'good=tq(A)+" "+PH[c][A.f[c]]+", whereas "+tq(B)+" "+PH[c][B.f[c]]+".";bad=', 'good=tq(A)+" "+PH[c][A.f[c]]+", whereas "+tq(B)+" "+PH[c][A.f[c]]+".";bad='),
 ("best: 'both' answer built on a category they don't share", 'var c=rnd(sameCats(A,B)),v=A.f[c],w=', 'var c=rnd(diffCats(A,B)),v=A.f[c],w='),
 ("best: one-text sentence names both", 'only=tq(one)+" "+PH[k][one.f[k]]+".";', 'only="Both "+tq(A)+" and "+tq(B)+" "+both(PH[k][A.f[k]])+".";'),
]
ok = 0
for name, a, b in M:
    assert page.count(a) == 1, (name, page.count(a))
    open("/tmp/cc_mut.html", "w", encoding="utf-8").write(page.replace(a, b))
    j = subprocess.run(["node", os.path.join(SRC, "test_compare_cards.js"), "/tmp/cc_mut.html"], capture_output=True, text=True, env={**os.environ, "N": "80"})
    open("/tmp/cc_mut.jsonl", "w").write(j.stdout)
    r = subprocess.run([sys.executable, os.path.join(SRC, "test_compare_cards.py"), "/tmp/cc_mut.jsonl", "/tmp/cc_mut.html"], capture_output=True, text=True)
    caught = r.returncode != 0 and j.returncode == 0 and j.stdout.count("\n") > 300
    out = (r.stdout + r.stderr).strip().splitlines()
    first = next((l for l in out if "PROBLEM" in l or "Error" in l), out[-1] if out else "")[:150]
    ok += caught; print("caught" if caught else "MISSED", "·", name, "·", first, flush=True)
print(f"{ok}/{len(M)} caught"); sys.exit(0 if ok == len(M) else 1)
