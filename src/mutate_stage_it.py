#!/usr/bin/env python3
"""Mutation check for Stage It: plants one mistake at a time in the built page and makes sure the checker fails.
Usage: python3 src/mutate_stage_it.py   (~20 s)"""
import subprocess, os, sys
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC)
page = open(os.path.join(ROOT, "stage-it.html"), encoding="utf-8").read()
M = [
 ("spooky scene tagged happy", '["🏰 Midnight in an abandoned castle. A ghost drifts across the hall.", "sp"]', '["🏰 Midnight in an abandoned castle. A ghost drifts across the hall.", "ha"]'),
 ("sad scene gains a danger word", '"🪑 An old man sits alone in his empty kitchen."', '"🪑 An old man sits alone as smoke fills his kitchen."'),
 ("peaceful scene loses its clue", '"🛏️ A baby sleeps peacefully in her cot."', '"🛏️ A baby is in her cot."'),
 ("lighting labels swapped", 'sa:"🌫️ Soft, grey light",da:"🔴 Flashing red light"', 'sa:"🔴 Flashing red light",da:"🌫️ Soft, grey light"'),
 ("sound labels swapped", 'ha:"🎉 Cheering and lively music",sa:"🎻 A slow, sad violin"', 'ha:"🎻 A slow, sad violin",sa:"🎉 Cheering and lively music"'),
 ("voice direction tagged movement", '["(whispering)", "voi"]', '["(whispering)", "mov"]'),
 ("movement direction turned into a face", '"(She crosses to the window.)"', '"(She smiles at the window.)"'),
 ("prop direction tagged face", '["(She pours two cups of tea.)", "act"]', '["(She pours two cups of tea.)", "face"]'),
 ("costume note tagged set", '["A long red cloak for the queen.", "cos"]', '["A long red cloak for the queen.", "set"]'),
 ("sound note made a lighting note", '"Thunder rumbles overhead."', '"Lightning flashes, then a blackout."'),
 ("prop note tagged sound", '["A suitcase for Seán to carry.", "pro"]', '["A suitcase for Seán to carry.", "sou"]'),
 ("nature conflict tagged society", '["A family is cut off by flood water for three days.", "nat"]', '["A family is cut off by flood water for three days.", "soc"]'),
 ("person conflict turned inner", '"Niamh blames her best friend for losing the match."', '"Niamh can\'t decide whether to forgive her best friend."'),
 ("angry line tagged happy", '["slamming the door", "Don\'t talk to me ever again!", "an"]', '["slamming the door", "Don\'t talk to me ever again!", "ha"]'),
 ("sad direction swapped for a happy one", '["sobbing", "He\'s not coming back, is he?", "sa"]', '["laughing", "He\'s not coming back, is he?", "sa"]'),
 ("close feeling offered as wrong", 'return x!==k&&x!==CLOSE[k];', 'return x!==k;'),
]
ok = 0
for name, a, b in M:
    assert page.count(a) == 1, (name, page.count(a))
    open("/tmp/si_mut.html", "w", encoding="utf-8").write(page.replace(a, b))
    j = subprocess.run(["node", os.path.join(SRC, "test_stage_it.js"), "/tmp/si_mut.html"], capture_output=True, text=True, env={**os.environ, "N": "200"})
    open("/tmp/si_mut.jsonl", "w").write(j.stdout)
    r = subprocess.run([sys.executable, os.path.join(SRC, "test_stage_it.py"), "/tmp/si_mut.jsonl", "/tmp/si_mut.html"], capture_output=True, text=True)
    caught = r.returncode != 0 and j.returncode == 0 and j.stdout.count("\n") > 600
    first = (r.stdout.splitlines() or [""])[0][:120]
    ok += caught; print("caught" if caught else "MISSED", "·", name, "·", first, flush=True)
print(f"{ok}/{len(M)} caught"); sys.exit(0 if ok == len(M) else 1)
