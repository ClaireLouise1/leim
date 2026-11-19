#!/usr/bin/env python3
"""Mutation check for Paragraph Builder's checker: plants one wrong answer at a time in paragraph-builder.html and makes sure
src/test_paragraph_builder.py catches every one. Usage (repo root): python3 src/mutate_paragraph_builder.py"""
import subprocess, sys
src = open("paragraph-builder.html", encoding="utf-8").read()
M = [
 ("topic answer off by one", 'C("⭐ Topic sentence?",LINES[i]', 'C("⭐ Topic sentence?",LINES[(i+1)%4]'),
 ("odd answer off by one", 'C("🚫 Doesn\'t belong?",LINES[i]', 'C("🚫 Doesn\'t belong?",LINES[i===3?2:i+1]'),
 ("order answer reversed", '.join(" → ");\n    var why', '.reverse().join(" → ");\n    var why'),
 ("TiPToP answer swapped", 'C("↩️ Why a new paragraph?",TIP[k]', 'C("↩️ Why a new paragraph?",TIP[k==="ti"?"pl":k]'),
 ("link pool from own group", 'if(x!==g)pool.push', 'if(x!=="add")pool.push'),
 ("tip data: place marked person", '"Back at home, I opened it carefully.",\n   "pl"', '"Back at home, I opened it carefully.",\n   "pe"'),
 ("link data: result marked adding", '"many houses were flooded.",\n   "As a result"', '"many houses were flooded.",\n   "In addition"'),
 ("seq data: steps swapped", '"First, boil the water in the kettle.",\n   "Next, pour', '"Finally, boil the water in the kettle.",\n   "Next, pour'),
 ("odd data: odd sentence on topic", '"My uncle drives a taxi in Wexford."', '"My uncle has seen puffins in Wexford."'),
 ("para data: topic sentence swapped", '"topic": "Dogs are loyal and loving pets.",\n   "sup": [\n    "A dog will often wait by the door for its owner to come home.",',
  '"topic": "A dog will often wait by the door for its owner to come home.",\n   "sup": [\n    "Dogs are loyal and loving pets.",'),
]
caught = 0
for name, old, new in M:
    assert src.count(old) == 1, (name, src.count(old))
    open("/tmp/mut-pb.html", "w", encoding="utf-8").write(src.replace(old, new))
    g = subprocess.run("N=80 node src/test_paragraph_builder.js /tmp/mut-pb.html > /tmp/mut-pb.jsonl && python3 src/test_paragraph_builder.py /tmp/mut-pb.jsonl /tmp/mut-pb.html",
                       shell=True, capture_output=True, text=True)
    ok = g.returncode != 0 and "problems" in g.stdout
    caught += ok
    print(("caught " if ok else "MISSED ") + name, "|", [l for l in g.stdout.splitlines() if "problems" in l])
print(f"{caught}/{len(M)} caught")
sys.exit(0 if caught == len(M) else 1)
