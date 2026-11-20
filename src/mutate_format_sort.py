#!/usr/bin/env python3
"""Mutation check for Format Sort: plants one mistake at a time in the built page and makes sure the checker fails.
Usage: python3 src/mutate_format_sort.py   (~20 s)"""
import subprocess, os, sys
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC)
page = open(os.path.join(ROOT, "format-sort.html"), encoding="utf-8").read()
M = [
 ("report extract tagged review", '["I recommend that a second bike shed is built beside the sports hall.", "rep"]', '["I recommend that a second bike shed is built beside the sports hall.", "rev"]'),
 ("blog line turned into a speech", '"Hi everyone, and welcome back to my blog!"', '"Ladies and gentlemen, welcome to our school concert!"'),
 ("article loses its source", '"According to the county council, the new swimming pool will open in May."', '"The new swimming pool will open in May."'),
 ("speech tagged article", '["Fellow students, I want to talk to you about something that matters.", "spe"]', '["Fellow students, I want to talk to you about something that matters.", "art"]'),
 ("type labels swapped", 'art:"📰 Article",blo:"💻 Blog"', 'art:"💻 Blog",blo:"📰 Article"'),
 ("headline paired with the wrong story", '"Bees Close Bray Playground"', '"Bees Close Bray School"'),
 ("headline shares a word with another story", '"Starlings Dance Over Lough Ennell"', '"Starlings Dance Over Bray"'),
 ("vague headline names a story", '"Something Happened"', '"Something Happened in Galway"'),
 ("headline maker offers its own headline twice", 'return j!==i;}).map', 'return true;}).map'),
 ("report title tagged findings", '["Report on Safety at the School Gate", "ti"]', '["Report on Safety at the School Gate", "fi"]'),
 ("findings line made a recommendation", '"Only 12 out of 40 bikes were locked properly."', '"All bikes should be locked properly."'),
 ("sign-off tagged introduction", '["Signed: Niall O\'Brien, Transition Year", "si"]', '["Signed: Niall O\'Brien, Transition Year", "in"]'),
 ("report labels swapped", 'fi:"🔍 Findings",re:"💡 Recommendation"', 'fi:"💡 Recommendation",re:"🔍 Findings"'),
 ("praise line tagged criticism", '["The jokes are hilarious, and the whole cinema was laughing.", "pr"]', '["The jokes are hilarious, and the whole cinema was laughing.", "cr"]'),
 ("criticism turned into praise", '"Sadly, the ending is predictable."', '"Happily, the ending is clever."'),
 ("verdict tagged details", '["Overall, a film the whole family will enjoy.", "ve"]', '["Overall, a film the whole family will enjoy.", "de"]'),
]
ok = 0
for name, a, b in M:
    assert page.count(a) == 1, (name, page.count(a))
    open("/tmp/fs_mut.html", "w", encoding="utf-8").write(page.replace(a, b))
    j = subprocess.run(["node", os.path.join(SRC, "test_format_sort.js"), "/tmp/fs_mut.html"], capture_output=True, text=True, env={**os.environ, "N": "200"})
    open("/tmp/fs_mut.jsonl", "w").write(j.stdout)
    r = subprocess.run([sys.executable, os.path.join(SRC, "test_format_sort.py"), "/tmp/fs_mut.jsonl", "/tmp/fs_mut.html"], capture_output=True, text=True)
    caught = r.returncode != 0 and j.returncode == 0 and j.stdout.count("\n") > 600
    first = (r.stdout.splitlines() or [""])[0][:120]
    ok += caught; print("caught" if caught else "MISSED", "·", name, "·", first, flush=True)
print(f"{ok}/{len(M)} caught"); sys.exit(0 if ok == len(M) else 1)
