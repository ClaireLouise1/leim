#!/usr/bin/env python3
"""Mutation check for Word Ladder: plant one mistake at a time in a copy of word-ladder.html and make sure
src/test_word_ladder.py catches it. Usage: python3 src/mutate_word_ladder.py"""
import subprocess, sys
SRC = open("word-ladder.html", encoding="utf-8").read()
M = [
 ("ladder word unrelated", '["damp", "wet", "soaked"]', '["damp", "wet", "sunny"]'),
 ("strong word not an adjective", '["peckish", "hungry", "starving"], "I\'m very hungry', '["peckish", "hungry", "starvation"], "I\'m very hungry'),
 ("very sentence lost its phrase", '"Your boots are very dirty."', '"Your boots are dirty."'),
 ("avoid list emptied (brilliant fits 'very good')", '"Your essay is very good.", ["brilliant", "delicious", "stunning"]', '"Your essay is very good.", ["delicious"]'),
 ("strongest picks the middle", 'return C("🪜 Top of the ladder?",w[2],[w[0],w[1]]', 'return C("🪜 Top of the ladder?",w[1],[w[0],w[2]]'),
 ("synonym is not a synonym", '["tidy", "neat", "messy"]', '["tidy", "dirty", "messy"]'),
 ("antonym is a synonym", '["brave", "courageous", "cowardly"]', '["brave", "courageous", "bold"]'),
 ("antonym is unrelated", '["empty", "vacant", "full"]', '["empty", "vacant", "green"]'),
 ("pair shows the wrong word", 'b=same?it[1]:it[2]', 'b=same?it[2]:it[1]'),
 ("prefix wrong (unlegal)", '["il", "legal", "not legal"]', '["un", "legal", "not legal"]'),
 ("prefix avoid list emptied (unread)", '["re", "read", "read again", ["un", "mis"]]', '["re", "read", "read again"]'),
 ("prefix meaning wrong", '["mis", "spell", "spell wrongly", ["un"]]', '["mis", "spell", "spell again", ["un"]]'),
 ("family: wrong class word", '["Please drive ___ near the school.", "carefully"', '["Please drive ___ near the school.", "careful"'),
 ("family: two right options", '["She sang ___ in the shower.", "happily", ["happy", "happiness", "unhappiness"]', '["She sang ___ in the shower.", "happily", ["happy", "happiness", "unhappily"]'),
 ("family: class label wrong", '["Try to ___ your answer.", "simplify", ["simple", "simply", "simplicity"], "v"]', '["Try to ___ your answer.", "simplify", ["simple", "simply", "simplicity"], "a"]'),
 ("ABC: last picks first", 's=ws.slice().sort(),ans=last?s[3]:s[0]', 's=ws.slice().sort(),ans=last?s[0]:s[0]'),
 ("guide word off the page", '["fish", "flag", "five", ["fly", "first", "flat"]]', '["fish", "flag", "fly", ["five", "first", "flat"]]'),
 ("meaning swapped", '["The {bat} flew out of the cave.", "🦇 an animal that flies at night", ["🏏 a stick for hitting a ball"]]', '["The {bat} flew out of the cave.", "🏏 a stick for hitting a ball", ["🦇 an animal that flies at night"]]'),
]
caught = 0
for name, old, new in M:
    assert SRC.count(old) == 1, (name, SRC.count(old))
    open("/tmp/mut.html", "w", encoding="utf-8").write(SRC.replace(old, new))
    subprocess.run("N=150 node src/test_word_ladder.js /tmp/mut.html > /tmp/mut.jsonl", shell=True)
    r = subprocess.run(["python3", "src/test_word_ladder.py", "/tmp/mut.jsonl", "/tmp/mut.html"], capture_output=True, text=True)
    ok = r.returncode != 0
    caught += ok
    print("CAUGHT " if ok else "MISSED ", name, "|", (r.stdout.strip().splitlines() or [""])[0][:110])
print(f"{caught}/{len(M)} caught")
sys.exit(0 if caught == len(M) else 1)
