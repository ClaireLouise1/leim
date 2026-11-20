#!/usr/bin/env python3
"""Mutation check for Shot Spotter: plants one mistake at a time in the built page and makes sure the checker fails.
Usage: python3 src/mutate_shot_spotter.py   (~20 s)"""
import subprocess, os, sys
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC)
page = open(os.path.join(ROOT, "shot-spotter.html"), encoding="utf-8").read()
M = [
 ("medium shot drawn as a close-up", "f=uf(0.45,0.58)", "f=uf(0.25,0.3)"),
 ("close-up drawn waist up", "f=uf(0.22,0.29)", "f=uf(0.47,0.55)"),
 ("extreme long shot drawn big", "s=uf(0.28,0.4)", "s=uf(1.2,1.5)"),
 ("long shot drawn tiny", "s=uf(1.4,1.7)", "s=uf(0.3,0.4)"),
 ("extreme close-up shows the chin", "s=uf(20,26)", "s=uf(8,10)"),
 ("high angle camera put low", 'cy=uf(6,16);}else if(k==="lo")', 'cy=uf(168,176);}else if(k==="lo")'),
 ("eye-level camera off the eye line", "cy=ey;}", "cy=ey+30;}"),
 ("bird's-eye camera not pointing down", 'if(k==="bird")rot=90;', 'if(k==="bird")rot=0;'),
 ("high / low labels swapped", 'hi:"⬇️ High angle",lo:"⬆️ Low angle",eye', 'hi:"⬆️ Low angle",lo:"⬇️ High angle",eye'),
 ("why item flipped", '["Make the bull look like a threat as it charges.", "lo"]', '["Make the bull look like a threat as it charges.", "hi"]'),
 ("sound item flipped", '["A phone rings in the empty kitchen.", "di"]', '["A phone rings in the empty kitchen.", "nd"]'),
 ("music item flipped", '["The family stand at the grave in the rain.", "sa"]', '["The family stand at the grave in the rain.", "jo"]'),
 ("edit item flipped", '["Every drop of rain hangs in the air as she turns.", "slow"]', '["Every drop of rain hangs in the air as she turns.", "flash"]'),
 ("an edit item names its technique", '"We see Grandad as a boy', '"In a flashback we see Grandad as a boy'),
 ("sound answer uses the other label", 'C("🔊 Can the characters hear it?",SND[it[1]]', 'C("🔊 Can the characters hear it?",SND[it[1]==="di"?"nd":"di"]'),
 ("music labels swapped", 'te:"🥁 Low drums, getting faster",jo:"🎻 Bright, bouncy fiddle"', 'te:"🎻 Bright, bouncy fiddle",jo:"🥁 Low drums, getting faster"'),
 ("why question offers editing labels", "others(WHY,it[1])", 'others(EDT,"cut")'),
]
ok = 0
for name, a, b in M:
    assert page.count(a) == 1, (name, page.count(a))
    open("/tmp/sh_mut.html", "w", encoding="utf-8").write(page.replace(a, b))
    j = subprocess.run(["node", os.path.join(SRC, "test_shot_spotter.js"), "/tmp/sh_mut.html"], capture_output=True, text=True, env={**os.environ, "N": "150"})
    open("/tmp/sh_mut.jsonl", "w").write(j.stdout)
    r = subprocess.run([sys.executable, os.path.join(SRC, "test_shot_spotter.py"), "/tmp/sh_mut.jsonl", "/tmp/sh_mut.html"], capture_output=True, text=True)
    caught = r.returncode != 0 and j.returncode == 0 and j.stdout.count("\n") > 1000
    first = (r.stdout.splitlines() or [""])[0][:130]
    ok += caught; print("caught" if caught else "MISSED", "·", name, "·", first, flush=True)
print(f"{ok}/{len(M)} caught"); sys.exit(0 if ok == len(M) else 1)
