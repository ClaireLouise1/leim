#!/usr/bin/env python3
"""Mutation check for Format Fixer: plants one mistake at a time in the built page and makes sure the checker fails.
Usage: python3 src/mutate_format_fixer.py   (~20 s)"""
import subprocess, os, sys
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC)
page = open(os.path.join(ROOT, "format-fixer.html"), encoding="utf-8").read()
M = [
 ("formal line tagged informal", '["I look forward to hearing from you.", "f"]', '["I look forward to hearing from you.", "i"]'),
 ("informal line tagged formal", '["Can\'t wait to see you!", "i"]', '["Can\'t wait to see you!", "f"]'),
 ("Sir/Madam tagged sincerely", '["Dear Sir or Madam,", "fa"]', '["Dear Sir or Madam,", "si"]'),
 ("named greeting tagged faithfully", '["Dear Mrs O\'Brien,", "si"]', '["Dear Mrs O\'Brien,", "fa"]'),
 ("friend tagged sincerely", '["Dear Ellie,", "in"]', '["Dear Ellie,", "si"]'),
 ("letter sign-off does not match greeting", '"close": "Thank you again for your time.", "sign": "Yours sincerely,"', '"close": "Thank you again for your time.", "sign": "Yours faithfully,"'),
 ("slang inside a formal letter", '"body": "The left boot split open after only two matches."', '"body": "The left boot was wrecked after only two matches."'),
 ("tone answer still casual", '"I would like a full refund, please."', '"I\'d like a full refund, please."'),
 ("tone wrong option that is formal", '"Cheers for the workshop."', '"Thank you for the workshop."'),
 ("letter parts in the wrong order", 'var ORDER=["addr","date","their","greet"', 'var ORDER=["addr","date","greet","their"'),
 ("part labels swapped", 'open:"🎯 Opening line",close:"🙏 Closing line"', 'open:"🙏 Closing line",close:"🎯 Opening line"'),
 ("missing part not removed", 'letterHTML(L,keys.filter(function(x){return x!==k;}))', 'letterHTML(L,keys)'),
 ("sign-off labels swapped", 'var SO={fa:"Yours faithfully,",si:"Yours sincerely,"', 'var SO={fa:"Yours sincerely,",si:"Yours faithfully,"'),
 ("register answer flipped in code", 'return C("Formal or informal?",FI[it[1]]', 'return C("Formal or informal?",FI[it[1]==="f"?"i":"f"]'),
 ("email subject line not marked", '"subj": "Subject: Work experience"', '"subj": "Work experience"'),
 ("date in the wrong form", '"date": "15 June 2026"', '"date": "June the fifteenth"'),
]
ok = 0
for name, a, b in M:
    assert page.count(a) == 1, (name, page.count(a))
    open("/tmp/ff_mut.html", "w", encoding="utf-8").write(page.replace(a, b))
    j = subprocess.run(["node", os.path.join(SRC, "test_format_fixer.js"), "/tmp/ff_mut.html"], capture_output=True, text=True, env={**os.environ, "N": "200"})
    open("/tmp/ff_mut.jsonl", "w").write(j.stdout)
    r = subprocess.run([sys.executable, os.path.join(SRC, "test_format_fixer.py"), "/tmp/ff_mut.jsonl", "/tmp/ff_mut.html"], capture_output=True, text=True)
    caught = r.returncode != 0 and j.returncode == 0 and j.stdout.count("\n") > 1000
    first = (r.stdout.splitlines() or [""])[0][:110]
    ok += caught; print("caught" if caught else "MISSED", "·", name, "·", first, flush=True)
print(f"{ok}/{len(M)} caught"); sys.exit(0 if ok == len(M) else 1)
