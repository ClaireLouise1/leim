#!/usr/bin/env python3
"""Mutation check for Spell Strike: plant one mistake at a time in a copy of spell-strike.html and make sure
src/test_spell_strike.py catches it. Usage: python3 src/mutate_spell_strike.py"""
import subprocess, os, sys
SRC = open("spell-strike.html", encoding="utf-8").read()
M = [
 ("spell answer misspelt", '["definitely", "I\'m', '["definately", "I\'m'),
 ("spell wrong option is a real word", '["seperate", "separete", "seprate"]', '["separated", "separete", "seprate"]'),
 ("spell wrong option far away", '["rythm", "rhythem", "rythym"]', '["rhyme", "rhythem", "rythym"]'),
 ("their -> there", '["The players left ___ boots in the dressing room.", "their"', '["The players left ___ boots in the dressing room.", "there"'),
 ("they're -> their", '["I hope ___ happy in the new house.", "they\'re"', '["I hope ___ happy in the new house.", "their"'),
 ("too -> to", '["This tea is ___ hot.", "too"', '["This tea is ___ hot.", "to"'),
 ("could of", '["I could ___ won that race.", "have"', '["I could ___ won that race.", "of"'),
 ("than -> then", '["Cork is bigger ___ Galway.", "than"', '["Cork is bigger ___ Galway.", "then"'),
 ("loose -> lose", '["My tooth is ___.", "loose"', '["My tooth is ___.", "lose"'),
 ("brought -> bought", '"She ___ her dog to school for the day.", "brought"', '"She ___ her dog to school for the day.", "bought"'),
 ("plural wrong", '["potato", "potatoes"', '["potato", "potatos"'),
 ("irregular plural wrong", '["mouse", "mice"', '["mouse", "mouses"'),
 ("ending: no double", '["stop", "ed", "stopped"]', '["stop", "ed", "stoped"]'),
 ("ending: keep e", '["hope", "ing", "hoping"]', '["hope", "ing", "hopeing"]'),
 ("ending: y kept before ing", '["cry", "ing", "crying"]', '["cry", "ing", "criing"]'),
 ("visit doubled", '["visit", "ing", "visiting"]', '["visit", "ing", "visitting"]'),
 ("no capital at the start", 'return up?cap(x):x;', 'return x;'),
 ("group option dropped", 'where:["where","were","wear"]', 'where:["where","were"]'),
]
caught = 0
for name, old, new in M:
    assert SRC.count(old) == 1, (name, SRC.count(old))
    open("/tmp/mut.html", "w", encoding="utf-8").write(SRC.replace(old, new))
    js = subprocess.run("N=150 node src/test_spell_strike.js /tmp/mut.html > /tmp/mut.jsonl", shell=True)
    r = subprocess.run(["python3", "src/test_spell_strike.py", "/tmp/mut.jsonl", "/tmp/mut.html"], capture_output=True, text=True)
    ok = r.returncode != 0
    caught += ok
    print("CAUGHT " if ok else "MISSED ", name, "|", (r.stdout.strip().splitlines() or [""])[0][:110])
print(f"{caught}/{len(M)} caught")
sys.exit(0 if caught == len(M) else 1)
