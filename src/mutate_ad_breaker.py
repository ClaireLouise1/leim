#!/usr/bin/env python3
"""Mutation check for Ad Breaker: plants one mistake at a time in the built page and makes sure the checker fails.
Usage: python3 src/mutate_ad_breaker.py   (~20 s)"""
import subprocess, os, sys
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC)
page = open(os.path.join(ROOT, "ad-breaker.html"), encoding="utf-8").read()
M = [
 ("star line tagged free", '["Famous chef Gráinne Lynch cooks with Crispa oil.", "star"]', '["Famous chef Gráinne Lynch cooks with Crispa oil.", "free"]'),
 ("statistic tagged exaggeration", '["Brushwell toothpaste fights 99% of germs.", "stat"]', '["Brushwell toothpaste fights 99% of germs.", "exag"]'),
 ("bandwagon line gains a number", '"Everybody\'s talking about Crumbly cookies."', '"Everybody\'s talking about Crumbly cookies, 2 for 1."'),
 ("hurry line loses its hurry", '"Hurry! The Mega Sale ends tonight."', '"The Mega Sale is on in the shop."'),
 ("exaggeration line made plain", '"Shiny Floor polish works like magic."', '"Shiny Floor polish cleans wooden floors."'),
 ("ad tagged with the wrong audience", '"brand": "Cramly", "who": "te"', '"brand": "Cramly", "who": "ol"'),
 ("older-people ad given a teen clue", '"Grow flowers for the grandkids to pick."', '"Grow flowers to show your mates."'),
 ("fact tagged opinion", '["Rollo bikes have 21 gears.", "f"]', '["Rollo bikes have 21 gears.", "o"]'),
 ("opinion line turned into a fact", '"Cosytoes socks are gorgeous."', '"Cosytoes socks are made in Cavan."'),
 ("best slogan loses its device", '"Rollo: ready to roll!"', '"Rollo: buy one now!"'),
 ("best slogan made long", '"Sparkle: no mess, no stress."', '"Sparkle: no mess, no stress, no dirt, no fuss at all."'),
 ("dull slogan made catchy", '"Fizzpop is a drink."', '"Fizzpop: fab and fizzy."'),
 ("picture tagged with the wrong meaning", '["🍯 Honey", ["🐝", "🌳", "🦋"], "nat"]', '["🍯 Honey", ["🐝", "🌳", "🦋"], "lux"]'),
 ("picture with a mixed message", '["🍬 Sweets", ["🎉", "🎊", "🥳"], "fun"]', '["🍬 Sweets", ["🎉", "💎", "🥳"], "fun"]'),
 ("trick labels swapped", 'stat:"📊 Statistic",exag:"🚀 Exaggeration"', 'stat:"🚀 Exaggeration",exag:"📊 Statistic"'),
 ("close meaning offered as wrong", 'return x!==k&&x!==CLOSE[k];', 'return x!==k;'),
]
ok = 0
for name, a, b in M:
    assert page.count(a) == 1, (name, page.count(a))
    open("/tmp/ab_mut.html", "w", encoding="utf-8").write(page.replace(a, b))
    j = subprocess.run(["node", os.path.join(SRC, "test_ad_breaker.js"), "/tmp/ab_mut.html"], capture_output=True, text=True, env={**os.environ, "N": "200"})
    open("/tmp/ab_mut.jsonl", "w").write(j.stdout)
    r = subprocess.run([sys.executable, os.path.join(SRC, "test_ad_breaker.py"), "/tmp/ab_mut.jsonl", "/tmp/ab_mut.html"], capture_output=True, text=True)
    caught = r.returncode != 0 and j.returncode == 0 and j.stdout.count("\n") > 600
    first = (r.stdout.splitlines() or [""])[0][:120]
    ok += caught; print("caught" if caught else "MISSED", "·", name, "·", first, flush=True)
print(f"{ok}/{len(M)} caught"); sys.exit(0 if ok == len(M) else 1)
