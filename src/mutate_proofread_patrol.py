#!/usr/bin/env python3
"""Mutation check for Proofread Patrol: plants one mistake at a time in the built page and makes sure the checker fails.
Usage: python3 src/mutate_proofread_patrol.py   (~2 min)"""
import subprocess, os, sys
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC)
page = open(os.path.join(ROOT, "proofread-patrol.html"), encoding="utf-8").read()
M = [
 ("spelling fix is itself misspelled", "{wierd>weird}", "{wierd>wierd}"),
 ("slip and fix swapped (a real word marked as a slip)", "{seperate>separate}", "{separate>seperate}"),
 ("mix-up fix is the wrong word", "{weather>whether}", "{whether>weather}"),
 ("should of marked right", "should {of>have} left", "should {have>of} left"),
 ("agreement fix wrong", "Each of the players {have>has}", "Each of the players {has>have}"),
 ("pronoun fix wrong", "Liam and {me>I} went", "Liam and {I>me} went"),
 ("irregular verb fix wrong", "I have {saw>seen}", "I have {seen>saw}"),
 ("fewer / less answer flipped", '["I drink ___ milk than my brother does.", "less"]', '["I drink ___ milk than my brother does.", "fewer"]'),
 ("who / whom answer flipped", '["The man ___ we met at the shop was very friendly.", "whom"]', '["The man ___ we met at the shop was very friendly.", "who"]'),
 ("a passage loses a slip mark but keeps the slip", "a strong wind all day.", "a strong wind all dya."),
 ("count off by one", 'var COUNT=["None","1 slip","2 slips","3 slips"]', 'var COUNT=["1 slip","None","2 slips","3 slips"]'),
 ("patrol answer is the fix, not the slip", 'C("🔎 Tap the slip",slip,pool', 'C("🔎 Tap the slip",fix,pool'),
 ("patrol card shows the fixed sentence", 'card(esc(shown(s))),{t:"patrol"', 'card(esc(fixed(s))),{t:"patrol"'),
 ("bracket answer uses a dash on one side", 'style==="b"?s.replace("[","(").replace("]",")")', 'style==="b"?s.replace("[","(").replace("]"," –")'),
 ("a pair of commas (also right) offered as wrong", 'out.push(a.join(" ")+", "+o+x.join(" ")+c+", "+b.join(" "));', 'out.push(a.join(" ")+", "+x.join(" ")+", "+b.join(" "));'),
 ("a second, unmarked slip in a sentence", "Hold the rope tight or you will {loose>lose} it.", "Hold the rope tihgt or you will {loose>lose} it."),
 ("count card shows the fixed passage", 'card(esc(shown(t)),esc(it[0]))', 'card(esc(fixed(t)),esc(it[0]))'),
]
ok = 0
for name, a, b in M:
    assert page.count(a) == 1, (name, page.count(a))
    open("/tmp/pp_mut.html", "w", encoding="utf-8").write(page.replace(a, b))
    j = subprocess.run(["node", os.path.join(SRC, "test_proofread_patrol.js"), "/tmp/pp_mut.html"], capture_output=True, text=True, env={**os.environ, "N": "150"})
    open("/tmp/pp_mut.jsonl", "w").write(j.stdout)
    r = subprocess.run([sys.executable, os.path.join(SRC, "test_proofread_patrol.py"), "/tmp/pp_mut.jsonl", "/tmp/pp_mut.html"], capture_output=True, text=True)
    caught = r.returncode != 0 and j.returncode == 0 and j.stdout.count("\n") > 1000
    first = (r.stdout.splitlines() or [""])[0][:130]
    ok += caught; print("caught" if caught else "MISSED", "·", name, "·", first, flush=True)
print(f"{ok}/{len(M)} caught"); sys.exit(0 if ok == len(M) else 1)
