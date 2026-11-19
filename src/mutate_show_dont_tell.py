#!/usr/bin/env python3
"""Mutation check for Show, Don't Tell: plants one mistake at a time in the built page and makes sure the checker fails.
Usage: python3 src/mutate_show_dont_tell.py   (~1 min)"""
import subprocess, os, sys
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC)
page = open(os.path.join(ROOT, "show-dont-tell.html"), encoding="utf-8").read()
M = [
 ("happy line tagged sad", '["hap", "I grinned all the way home from the match."]', '["sad", "I grinned all the way home from the match."]'),
 ("show line that names the feeling", '"I bit my nails as I waited outside the principal\'s office."', '"I bit my nails because I was nervous."'),
 ("bored line with no clue", '"I yawned for the tenth time that lesson."', '"I sat there for the tenth time that lesson."'),
 ("wrong strong verb for a cue", '"walked", "crept"]', '"walked", "raced"]'),
 ("verb sentence with no cue", '"I was starving, so I ___ my dinner in two minutes."', '"I ___ my dinner in two minutes."'),
 ("said item answered with a looked verb", '"said", "whispered"]', '"said", "glanced"]'),
 ("zoom answer not specific", '"a scruffy brown terrier", ["an animal"', '"a dog", ["an animal"'),
 ("zoom wrong option too specific", '["a car", "a vehicle", "a nice car that was quite old"]', '["a car", "a vehicle", "a battered blue Toyota van"]'),
 ("sense line tagged wrong", '["A dog growled behind the gate.", "hear"]', '["A dog growled behind the gate.", "see"]'),
 ("close feelings offered as wrong", 'function far(k){return Object.keys(FL).filter(function(x){return x!==k&&CLOSE[k].indexOf(x)<0;});}', 'function far(k){return Object.keys(FL).filter(function(x){return x!==k;});}'),
 ("feel answer swapped in code", 'return C("Which feeling?",FL[k]', 'return C("Which feeling?",FL[k==="ang"?"sad":k]'),
 ("tell trap missing", 'pool.push("I was really, really "+TELLW[k]+".");', 'pool.push(rnd(D.show)[1]);'),
 ("synonym of the answer offered as wrong", 'if(S.indexOf(it[2])<0)pool.push(rnd(S));', 'pool.push(rnd(S));'),
 ("labels swapped", 'sca:"😨 Scared",ner:"😬 Nervous"', 'sca:"😬 Nervous",ner:"😨 Scared"'),
]
ok = 0
for name, a, b in M:
    assert page.count(a) == 1, (name, page.count(a))
    open("/tmp/sd_mut.html", "w", encoding="utf-8").write(page.replace(a, b))
    j = subprocess.run(["node", os.path.join(SRC, "test_show_dont_tell.js"), "/tmp/sd_mut.html"], capture_output=True, text=True, env={**os.environ, "N": "150"})
    open("/tmp/sd_mut.jsonl", "w").write(j.stdout)
    r = subprocess.run([sys.executable, os.path.join(SRC, "test_show_dont_tell.py"), "/tmp/sd_mut.jsonl", "/tmp/sd_mut.html"], capture_output=True, text=True)
    caught = r.returncode != 0 and j.returncode == 0 and j.stdout.count("\n") > 1000
    ok += caught; print("caught" if caught else "MISSED", "·", name)
print(f"{ok}/{len(M)} caught"); sys.exit(0 if ok == len(M) else 1)
