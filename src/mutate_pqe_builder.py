#!/usr/bin/env python3
"""Mutation check for PQE Builder: plants one mistake at a time in the built page and makes sure the checker fails.
Usage: python3 src/mutate_pqe_builder.py   (~30 s)"""
import subprocess, os, sys
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC)
page = open(os.path.join(ROOT, "pqe-builder.html"), encoding="utf-8").read()
M = [
 ("line's feeling label wrong", '"keys": ["", "nervous", "determined", "joyful"]', '"keys": ["", "angry", "determined", "joyful"]'),
 ("short quote cut to words that prove nothing", '"q": ["ate his lunch alone on the wall"', '"q": ["ate his lunch"'),
 ("point names a different feeling", '"Aoife is nervous before the audition."', '"Aoife is excited before the audition."'),
 ("neutral line now shows a feeling", '"A heron fished beside the jetty"', '"A heron stood still beside the jetty"'),
 ("PQE answer taken from the next line", 'C("🔎 Which quote proves it?",dq(T.q[li])', 'C("🔎 Which quote proves it?",dq(T.q[(li+1)%4])'),
 ("PQE shows another line's point", 'textCard(T)+pointCard(T.pts[li])', 'textCard(T)+pointCard(T.pts[ks[0]])'),
 ("Point / Quote labels swapped", 'LAB={p:"💡 Point",q:"🔎 Quote"', 'LAB={p:"🔎 Quote",q:"💡 Point"'),
 ("which-part answer off by one", 'k="pqe"[i]', 'k="qep"[i]'),
 ("quote and explain swapped in an answer", '"She tells us she “asked again and again”.", "The repeated word ‘again’ shows she is stubborn."', '"The repeated word ‘again’ shows she is stubborn.", "She tells us she “asked again and again”."'),
 ("explanation answer = the retelling", 'C("🧠 Best explanation?",it[2],it.slice(3)', 'C("🧠 Best explanation?",it[3],[it[2]].concat(it.slice(4))'),
 ("good explanation made vague", '"The word ‘offered’ shows she is generous and thoughtful."', '"This shows she is generous and thoughtful."'),
 ("good explanation argues another feeling", '"‘Churned’ suggests he feels sick with worry."', '"‘Churned’ suggests he feels sick with anger."'),
 ("misquote is really the exact words", '"ate his dinner alone"', '"lunch alone"'),
 ("exact answer = the whole line", 'C("✂️ Best way to quote it?",dq(it[2]),[dq(it[1])', 'C("✂️ Best way to quote it?",dq(it[1]),[dq(it[2])'),
 ("paraphrase given quotation marks", 'dq(it[3]),it[4]]', 'dq(it[3]),dq(it[4])]'),
 ("question answer = a point that misses it", 'C("❓ Which point answers it?",it[1],it[2]', 'C("❓ Which point answers it?",it[2][0],[it[1]].concat(it[2].slice(1))'),
 ("wrong point that really answers the question", '"Aoife is cross with the judges for keeping her waiting."', '"Aoife is worried about the judges keeping her waiting."'),
]
ok = 0
for name, a, b in M:
    assert page.count(a) == 1, (name, page.count(a))
    open("/tmp/pq_mut.html", "w", encoding="utf-8").write(page.replace(a, b))
    j = subprocess.run(["node", os.path.join(SRC, "test_pqe_builder.js"), "/tmp/pq_mut.html"], capture_output=True, text=True, env={**os.environ, "N": "60"})
    open("/tmp/pq_mut.jsonl", "w").write(j.stdout)
    r = subprocess.run([sys.executable, os.path.join(SRC, "test_pqe_builder.py"), "/tmp/pq_mut.jsonl", "/tmp/pq_mut.html"], capture_output=True, text=True)
    caught = r.returncode != 0 and j.returncode == 0 and j.stdout.count("\n") > 500
    out = (r.stdout + r.stderr).strip().splitlines()
    first = next((l for l in out if "PROBLEM" in l or "Error" in l), out[-1] if out else "")[:140]
    ok += caught; print("caught" if caught else "MISSED", "·", name, "·", first, flush=True)
print(f"{ok}/{len(M)} caught"); sys.exit(0 if ok == len(M) else 1)
