#!/usr/bin/env python3
"""Mutation check for English Exam Mix: plants one mistake at a time in the built page and makes sure the checker fails.
Usage: python3 src/mutate_english_exam_mix.py   (~15 s)"""
import subprocess, os, sys
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC)
page = open(os.path.join(ROOT, "english-exam-mix.html"), encoding="utf-8").read()
M = [
 ("time: a minute a mark", 'ans=M*P.min/P.marks;', 'ans=M;'),
 ("time: half a minute a mark", 'ans=M*P.min/P.marks;', 'ans=M/2;'),
 ("marks: a mark a minute", 'ans=T*P.marks/P.min;', 'ans=T;'),
 ("paper length changed", '"paper": {"min": 120, "marks": 180}', '"paper": {"min": 150, "marks": 180}'),
 ("fact card shows the wrong marks", '"📝 This question: "+M+" marks"', '"📝 This question: "+(M+3)+" marks"'),
 ("cmd: explain item labelled describe", '["Explain how the photograph adds to the article.", "expl"]', '["Explain how the photograph adds to the article.", "desc"]'),
 ("cmd: compare item reworded to describe", '["Compare the openings of the two stories.", "comp"]', '["Describe the openings of the two stories.", "comp"]'),
 ("cmd: a second command word slipped in", '["Summarise what happens in the first scene.", "sum"]', '["Summarise and explain what happens in the first scene.", "sum"]'),
 ("cmd: labels swapped", 'find:"🔎 Find it in the text",desc:"📝 Say what it is like"', 'find:"📝 Say what it is like",desc:"🔎 Find it in the text"'),
 ("cmd: answer from the next key", 'var it=rnd(D.cmd),k=it[1],ans=CMD[k];', 'var it=rnd(D.cmd),k=it[1],ans=CMD[CMDK[(CMDK.indexOf(k)+1)%6]];'),
 ("form: email task labelled letter", '"Write an email to your principal asking for a school garden.", "email"', '"Write an email to your principal asking for a school garden.", "letter"'),
 ("form: task names two forms", '"Write a diary entry about your first day at a new school."', '"Write a diary entry or a story about your first day at a new school."'),
 ("form: answer from another task", 'function qForm(){var it=rnd(D.task),k=it[1],ans=FORM[k];', 'function qForm(){var it=rnd(D.task),k=rnd(D.task)[1],ans=FORM[k];'),
 ("reader: wrong reader", '"Write a talk for your classmates about a hobby you love.", "speech", "your classmates"', '"Write a talk for your classmates about a hobby you love.", "speech", "your teachers"'),
 ("reader: a second right answer offered", 'filter(function(r){return it[0].indexOf(r)<0;})', 'map(function(r){return r===ans?ans.replace(/^(your|the|a) /,""):r;})'),
 ("reader: answer from another task", 'it=rnd(ts),ans=it[2];', 'it=rnd(ts),ans=rnd(ts)[2];'),
]
ok = 0
for name, a, b in M:
    assert page.count(a) == 1, (name, page.count(a))
    open("/tmp/xm_mut.html", "w", encoding="utf-8").write(page.replace(a, b))
    j = subprocess.run(["node", os.path.join(SRC, "test_english_exam_mix.js"), "/tmp/xm_mut.html"], capture_output=True, text=True, env={**os.environ, "N": "80"})
    open("/tmp/xm_mut.jsonl", "w").write(j.stdout)
    r = subprocess.run([sys.executable, os.path.join(SRC, "test_english_exam_mix.py"), "/tmp/xm_mut.jsonl", "/tmp/xm_mut.html"], capture_output=True, text=True)
    caught = r.returncode != 0 and j.returncode == 0 and j.stdout.count("\n") > 300
    out = (r.stdout + r.stderr).strip().splitlines()
    first = next((l for l in out if "PROBLEM" in l or "Error" in l), out[-1] if out else "")[:150]
    ok += caught; print("caught" if caught else "MISSED", "·", name, "·", first, flush=True)
print(f"{ok}/{len(M)} caught"); sys.exit(0 if ok == len(M) else 1)
