#!/usr/bin/env python3
"""Mutation check for Tense Trap: plants one mistake at a time in the built page and makes sure the checker fails.
Usage: python3 src/mutate_tense_trap.py   (~1 min)"""
import subprocess, os, sys
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC)
page = open(os.path.join(ROOT, "tense-trap.html"), encoding="utf-8").read()
M = [
 ("past answer swapped for present", '["Yesterday I ___ to school in the rain.", "walked", ["walk", "will walk"]]', '["Yesterday I ___ to school in the rain.", "walk", ["walked", "will walk"]]'),
 ("present answer missing its -s", '["Every Friday, the shop ___ early.", "closes", ["closed", "will close"]]', '["Every Friday, the shop ___ early.", "close", ["closed", "will close"]]'),
 ("future answer swapped for past", '["Tomorrow Mam ___ us to the airport.", "will drive", ["drove", "has driven"]]', '["Tomorrow Mam ___ us to the airport.", "drove", ["will drive", "has driven"]]'),
 ("time cue changed so the answer no longer fits", '"Last night we ___ a film about sharks."', '"Tomorrow night we ___ a film about sharks."'),
 ("slip mark on a past verb", '"Niamh {opened} the door, {looked} outside and {*sees} a fox. It {ran} away."', '"Niamh {*opened} the door, {looked} outside and {sees} a fox. It {ran} away."'),
 ("second present verb planted in a slip story", '"Oisín {packed} his bag, {*says} goodbye and {walked} to the station. The train {was} late."', '"Oisín {packed} his bag, {*says} goodbye and {walks} to the station. The train {was} late."'),
 ("agreement answer flipped (each)", '["Each of the girls ___ a medal.", "has", "have"]', '["Each of the girls ___ a medal.", "have", "has"]'),
 ("agreement answer flipped (one of)", '["One of my friends ___ in a band.", "plays", "play"]', '["One of my friends ___ in a band.", "play", "plays"]'),
 ("agreement answer flipped (and)", '["Dad and Grandad ___ fishing every Sunday.", "go", "goes"]', '["Dad and Grandad ___ fishing every Sunday.", "goes", "go"]'),
 ("agreement answer flipped (there are)", '["There ___ three dogs in the garden.", "are", "is"]', '["There ___ three dogs in the garden.", "is", "are"]'),
 ("irregular table: seen and saw swapped", 'see:["saw","seen"]', 'see:["seen","saw"]'),
 ("helper-verb rule broken", 'pp=HELP.test(it[0].split("___")[0])', 'pp=!HELP.test(it[0].split("___")[0])'),
 ("irregular: wrong participle", 'write:["wrote","written"]', 'write:["wrote","writ"]'),
 ("pronoun: subject answer made object", '["Tom and ___ went to the match.", "i", "I"]', '["Tom and ___ went to the match.", "i", "me"]'),
 ("pronoun: object answer made subject", '["The bus left without ___.", "we", "us"]', '["The bus left without ___.", "we", "we"]'),
 ("pronoun table: him/her swapped", 'OBJ={i:"me",he:"him",she:"her"', 'OBJ={i:"me",he:"her",she:"him"'),
]
ok = 0
for name, a, b in M:
    assert page.count(a) == 1, (name, page.count(a))
    open("/tmp/tt_mut.html", "w", encoding="utf-8").write(page.replace(a, b))
    j = subprocess.run(["node", os.path.join(SRC, "test_tense_trap.js"), "/tmp/tt_mut.html"], capture_output=True, text=True, env={**os.environ, "N": "200"})
    open("/tmp/tt_mut.jsonl", "w").write(j.stdout)
    r = subprocess.run([sys.executable, os.path.join(SRC, "test_tense_trap.py"), "/tmp/tt_mut.jsonl", "/tmp/tt_mut.html"], capture_output=True, text=True)
    caught = r.returncode != 0 and j.returncode == 0 and j.stdout.count("\n") > 800
    first = (r.stdout.splitlines() or [""])[0][:130]
    ok += caught; print("caught" if caught else "MISSED", "·", name, "·", first, flush=True)
print(f"{ok}/{len(M)} caught"); sys.exit(0 if ok == len(M) else 1)
