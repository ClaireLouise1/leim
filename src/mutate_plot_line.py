#!/usr/bin/env python3
"""Mutation check for Plot Line: plants one mistake at a time in the built page and makes sure the checker fails.
Usage: python3 src/mutate_plot_line.py   (~1 min)"""
import subprocess, os, sys
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC)
page = open(os.path.join(ROOT, "plot-line.html"), encoding="utf-8").read()
M = [
 ("arc lines swapped (climax before rising)", '"At half-time they were losing by three goals, and their captain was injured.", "At that moment, Darragh, the smallest player on the team, was sent on."', '"At that moment, Darragh, the smallest player on the team, was sent on.", "At half-time they were losing by three goals, and their captain was injured."'),
 ("falling action with no aftermath opener", '"Afterwards, Kevin fed the robin every day for three weeks."', '"Kevin fed the robin every day for three weeks."'),
 ("resolution that is really rising action", '"In the end, the mural had both their names in the corner."', '"The mural was ruined again and had both their names in the corner."'),
 ("exposition with trouble in it", '"Every summer, Niamh stayed on her uncle\'s farm near Ennis."', '"Every summer, Niamh got lost on her uncle\'s farm near Ennis."'),
 ("theme tagged wrong", '"Kate decided to give her brother a second chance.", "fo"', '"Kate decided to give her brother a second chance.", "fa"'),
 ("theme moment with two themes", '"The whole class was punished for something one boy did."', '"The whole class was punished for something one boy did, and he said sorry."'),
 ("look-alike theme allowed as wrong", 'var CLOSE={fr:["be"],be:["fr"],co:["gr"],gr:["co"]};', 'var CLOSE={};'),
 ("mood tagged wrong", '["Snow fell softly on the quiet street.", "pe"]', '["Snow fell softly on the quiet street.", "gl"]'),
 ("mood line with two moods", '"A heavy thud came from the attic, then nothing."', '"A heavy thud came from the empty attic, then nothing."'),
 ("change traits back to front", '"By the end, she volunteered to give the speech on the school tour.", "sh", "cf"]', '"By the end, she volunteered to give the speech on the school tour.", "cf", "sh"]'),
 ("change end line shows no trait", '"At the end, she was welcomed into the drama club."', '"At the end, she went to the drama club."'),
 ("stage labels swapped", 'cl:"💥 Climax",fa:"📉 Falling action"', 'cl:"📉 Falling action",fa:"💥 Climax"'),
 ("stage answer off by one in code", 'return C("📈 Which stage of the plot?",STAGE[k]', 'return C("📈 Which stage of the plot?",STAGE[SK[(i+1)%5]]'),
 ("order answer from wrong mapping", 'var ans=[1,2,3,4].map(function(n){return lets[idx.indexOf(n)];})', 'var ans=[1,2,3,4].map(function(n){return lets[n-1];})'),
 ("change answer with the wrong end trait in code", 'C("🔄 How did they change?",lab(s,e)', 'C("🔄 How did they change?",lab(s,K[(K.indexOf(e)+1)%8])'),
 ("theme answer from the wrong item", 'C("💡 Which theme?",THEME[k]', 'C("💡 Which theme?",THEME[rnd(D.theme)[1]]'),
]
ok = 0
for name, a, b in M:
    assert page.count(a) == 1, (name, page.count(a))
    open("/tmp/pl_mut.html", "w", encoding="utf-8").write(page.replace(a, b))
    j = subprocess.run(["node", os.path.join(SRC, "test_plot_line.js"), "/tmp/pl_mut.html"], capture_output=True, text=True, env={**os.environ, "N": "60"})
    open("/tmp/pl_mut.jsonl", "w").write(j.stdout)
    r = subprocess.run([sys.executable, os.path.join(SRC, "test_plot_line.py"), "/tmp/pl_mut.jsonl", "/tmp/pl_mut.html"], capture_output=True, text=True)
    caught = r.returncode != 0 and j.returncode == 0 and j.stdout.count("\n") > 250
    ok += caught; print("caught" if caught else "MISSED", "·", name, "|", (r.stdout.strip().splitlines() or [""])[0][:90], flush=True)
print(f"{ok}/{len(M)} caught"); sys.exit(0 if ok == len(M) else 1)
