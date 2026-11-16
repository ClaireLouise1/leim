#!/usr/bin/env python3
"""Probability 1: chance & sample spaces (JC Maths topic 11): free sheet + teacher pack + Payhip cover.
Run from the repo root: python3 src/build_probability1_pdfs.py OUTDIR
Writes src/probability-chance-sample-spaces-*.html; PDFs/cover PNG go to OUTDIR (free sheet also to printables/).
Every probability is computed with Fraction by counting equally likely outcomes, and asserted."""
import os, sys, random, subprocess, re
from fractions import Fraction as F
from itertools import product
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC)
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/prob"; os.makedirs(OUT, exist_ok=True)
SLUG = "probability-chance-sample-spaces"
LO = "SP.1a, SP.2a, SP.2b"

def isp(n): return n > 1 and all(n % d for d in range(2, int(n ** .5) + 1))
def P(space, cond):
    space = list(space); return F(sum(1 for s in space if cond(s)), len(space))
def fr(x):
    x = F(x); return "0" if x == 0 else "1" if x == 1 else f"{x.numerator}/{x.denominator}"
def word(p): return "impossible" if p == 0 else "certain" if p == 1 else "even chance" if p == F(1, 2) else "unlikely" if p < F(1, 2) else "likely"
DIE = range(1, 7); DICE = list(product(DIE, DIE)); COIN = "HT"
def bag(**c): return [k for k, n in c.items() for _ in range(n)]
def cards(n): return range(1, n + 1)
def letters(w): return list(w)
assert P(DICE, lambda s: sum(s) == 7) == F(1, 6) and fr(F(3, 6)) == "1/2"

# ---------- free sheet ----------
A = [("Rolling a 7 on a fair die", P(DIE, lambda n: n == 7)), ("Rolling a number less than 7 on a fair die", P(DIE, lambda n: n < 7)),
     ("Getting heads when you toss a fair coin", P(COIN, lambda c: c == "H")), ("Rolling a 6 on a fair die", P(DIE, lambda n: n == 6)),
     ("Rolling a number bigger than 1 on a fair die", P(DIE, lambda n: n > 1)), ("Picking a red counter from a bag of 9 red and 1 blue", P(bag(red=9, blue=1), lambda c: c == "red"))]
assert [word(p) for q, p in A] == ["impossible", "certain", "even chance", "unlikely", "likely", "likely"]
B3 = bag(red=3, blue=5, green=2)
B = [("You roll a fair die. Find P(a prime number).", P(DIE, isp)),
     ("You roll a fair die. Find P(a multiple of 3).", P(DIE, lambda n: n % 3 == 0)),
     ("Cards numbered 1 to 20: find P(a multiple of 4).", P(cards(20), lambda n: n % 4 == 0)),
     ("Cards numbered 1 to 20: find P(a prime number).", P(cards(20), isp)),
     ("A bag has 3 red, 5 blue and 2 green counters. Find P(blue).", P(B3, lambda c: c == "blue")),
     ("Same bag: find P(not green).", P(B3, lambda c: c != "green")),
     ("Same bag: find P(red or green).", P(B3, lambda c: c in ("red", "green"))),
     ("The letters of BALLYBUNION are put on cards. Find P(B).", P(letters("BALLYBUNION"), lambda c: c == "B"))]
assert [fr(p) for q, p in B] == ["1/2", "1/3", "1/4", "2/5", "1/2", "4/5", "1/2", "2/11"], [fr(p) for q, p in B]
C = [("P(rain in Cork tomorrow) = 0.6. Find P(no rain).", "0.4", 1 - F("0.6") == F("0.4")),
     ("P(winning a raffle prize) = 3/7. Find P(not winning).", fr(1 - F(3, 7)), True),
     ("P(the bus is late) = 12%. Find P(the bus is not late).", "88%", 100 - 12 == 88),
     ("A bag has 24 counters and P(red) = 3/8. How many are red?", str(24 * F(3, 8)), True),
     ("A spinner has 10 equal sectors and P(blue) = 3/10. How many sectors are blue?", str(10 * F(3, 10)), True),
     ("Which of these can NOT be a probability: 0.7, 5/4, 0, 85%?", "5/4", not (0 <= F(5, 4) <= 1))]
assert [a for q, a, ok in C] == ["0.4", "4/7", "88%", "9", "3", "5/4"] and all(ok for q, a, ok in C)
S2 = ["".join(s) for s in product(COIN, COIN)]
SRB = [a + b for a, b in product("RB", "123")]
SPROD = [a * b for a, b in product(range(1, 4), DIE)]
D = [("List the sample space when you toss two coins.", "{" + ", ".join(S2) + "}"),
     ("List the sample space when you spin a spinner with sectors R, B, then a spinner numbered 1 to 3.", "{" + ", ".join(SRB) + "}"),
     ("How many outcomes are there when you toss a coin and roll a die?", str(len(list(product(COIN, DIE))))),
     ("Two dice are rolled and the scores added. How many cells are in the two-way table?", str(len(DICE))),
     ("Two dice: find P(a total of 9).", fr(P(DICE, lambda s: sum(s) == 9))),
     ("Two dice: find P(both dice show the same number).", fr(P(DICE, lambda s: s[0] == s[1]))),
     ("Two dice: find P(a total greater than 9).", fr(P(DICE, lambda s: sum(s) > 9))),
     ("Two dice: which total is most likely?", str(max(range(2, 13), key=lambda t: sum(1 for s in DICE if sum(s) == t)))),
     ("A spinner numbered 1 to 3 is spun and a die is rolled; the scores are multiplied. Find P(the product is even).", fr(F(sum(1 for x in SPROD if x % 2 == 0), len(SPROD)))),
     ("A coin is tossed, then a spinner numbered 1 to 4 is spun. Use a tree diagram to find P(a head and an even number).", fr(P(product(COIN, range(1, 5)), lambda s: s[0] == "H" and s[1] % 2 == 0)))]
assert [a for q, a in D] == ["{HH, HT, TH, TT}", "{R1, R2, R3, B1, B2, B3}", "12", "36", "1/9", "1/6", "1/6", "7", "2/3", "1/4"], [a for q, a in D]
# exam-style
mar = bag(red=5, yellow=3, green=4)
rem = next(x for x in range(5) if F(4 - x, 12 - x) == F(1, 5)); assert rem == 2
SP = [(a, b) for a in range(1, 5) for b in range(1, 4)]
c3 = ["".join(s) for s in product(COIN, repeat=3)]
E = [("A bag has 5 red, 3 yellow and 4 green marbles. One is taken at random. (a) Find P(yellow). (b) Find P(not red). (c) How many green marbles must be taken out of the bag so that P(green) = 1/5?",
      f"(a) <b>{fr(P(mar, lambda c: c == 'yellow'))}</b> (b) <b>{fr(P(mar, lambda c: c != 'red'))}</b> (c) take out 2: 2/10 = 1/5, so <b>{rem}</b>"),
     ("Spinner A is numbered 1 to 4 and spinner B is numbered 1 to 3 (equal sectors). Both are spun and the scores multiplied. (a) Draw a two-way table. (b) Find P(the product is 6). (c) Find P(the product is greater than 5).",
      f"(a) 12 cells (b) 2×3, 3×2: <b>{fr(P(SP, lambda s: s[0] * s[1] == 6))}</b> (c) 6, 6, 8, 9, 12: <b>{fr(P(SP, lambda s: s[0] * s[1] > 5))}</b>"),
     ("A fair coin is tossed three times. (a) Use a tree diagram to list the sample space. (b) Find P(exactly two heads). (c) Find P(at least one tail).",
      f"(a) {', '.join(c3)} (b) <b>{fr(P(c3, lambda s: s.count('H') == 2))}</b> (c) <b>{fr(P(c3, lambda s: 'T' in s))}</b>"),
     ("Seán says: \"The probability that Cork win their next match is 0.6, so the probability that they lose is 0.4.\" Explain why Seán may be wrong.",
      "P(not win) = 0.4, but <b>not winning</b> includes a <b>draw</b>. P(lose) is 0.4 only if a draw is impossible.")]
assert fr(P(mar, lambda c: c == "yellow")) == "1/4" and fr(P(mar, lambda c: c != "red")) == "7/12"
assert fr(P(SP, lambda s: s[0] * s[1] == 6)) == "1/6" and fr(P(SP, lambda s: s[0] * s[1] > 5)) == "5/12"
assert fr(P(c3, lambda s: s.count("H") == 2)) == "3/8" and fr(P(c3, lambda s: "T" in s)) == "7/8"

def qs(items): return "".join(f"<li>{x[0]} <span class='line'></span></li>" for x in items)
dice_tbl = "<table class='dt'><tr><th>+</th>" + "".join(f"<th>{b}</th>" for b in DIE) + "</tr>" + "".join(
    f"<tr><th>{a}</th>" + "".join(f"<td{' class=hl' if a + b == 7 else ''}>{a + b}</td>" for b in DIE) + "</tr>" for a in DIE) + "</table>"
def tree(a, b, w=220):
    ends = len(a) * len(b); H = ends * 17 + 10; o = f'<svg viewBox="0 0 220 {H}" width="{w}" style="display:block">'; k = 0
    for i, x in enumerate(a):
        y1 = (i + .5) * H / len(a)
        o += f'<line x1="8" y1="{H/2}" x2="70" y2="{y1}" stroke="#1B2430" stroke-width="1.5"/><text x="78" y="{y1+4}" font-size="12" font-weight="800">{x}</text>'
        for z in b:
            y2 = (k + .5) * H / ends; k += 1
            o += f'<line x1="90" y1="{y1}" x2="140" y2="{y2}" stroke="#1B2430" stroke-width="1.2"/><text x="146" y="{y2+4}" font-size="12" font-weight="800">{z}</text><text x="172" y="{y2+4}" font-size="12" font-weight="700" fill="#2E7D57">{x}{z}</text>'
    return o + "</svg>"
SCALE = """<svg viewBox="-28 0 376 62" width="100%" style="display:block;margin:2px 0 4px"><line x1="20" y1="22" x2="300" y2="22" stroke="#1B2430" stroke-width="2.5"/>
<g font-family="Inter,sans-serif" text-anchor="middle" fill="#1B2430" font-weight="800"><line x1="20" y1="15" x2="20" y2="29" stroke="#1B2430" stroke-width="2"/><line x1="160" y1="15" x2="160" y2="29" stroke="#1B2430" stroke-width="2"/><line x1="300" y1="15" x2="300" y2="29" stroke="#1B2430" stroke-width="2"/>
<text x="20" y="11" font-size="12">0</text><text x="160" y="11" font-size="12">1/2</text><text x="300" y="11" font-size="12">1</text>
<text x="20" y="46" font-size="11">Impossible</text><text x="90" y="46" font-size="11" fill="#2E7D57">Unlikely</text><text x="160" y="46" font-size="11">Even chance</text><text x="230" y="46" font-size="11" fill="#2E7D57">Likely</text><text x="300" y="46" font-size="11">Certain</text></g></svg>"""

sheet = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Probability: chance and sample spaces: rules and practice | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>@page{{@bottom-left{{content:"Léim · leim.ie · Free to print for home or class · JC Maths LOs (2018 spec): {LO}"}}}}
.tight{{font-size:10pt;line-height:1.42}}.tight h2{{margin:9px 0 4px;font-size:13.5pt}}.tight .note,.tight .tip{{padding:6px 10px;margin:6px 0}}
ol.q{{padding-left:30px}}ol.q li{{margin:7px 0}}
.p2{{font-size:9.4pt}}.p2 ol.q li{{margin:3.6px 0}}.p2 h2{{margin:8px 0 3px}}
.ans td{{padding:3px 6px;font-size:9pt}}
.dt{{width:auto;margin:3px 0}}.dt td,.dt th{{text-align:center;padding:1px 6px;font-size:9pt}}.dt td.hl{{background:var(--sun);font-weight:800}}
.fm{{text-align:center;font-weight:800;font-size:11.5pt}}
</style></head><body>
<div class="page tight">
  <div class="band"><div><div class="k">Junior Cycle Maths · Free revision sheet</div><h1>Probability: chance &amp; sample spaces</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2018 specification): {LO}. Play the game: <b>leim.ie/spin-and-predict.html</b></p>
  <div class="two">
   <div><h2>1. The probability scale</h2>
    <p>A probability is a number from <b>0</b> (impossible) to <b>1</b> (certain). Write it as a fraction, a decimal or a percentage: 1/4 = 0.25 = 25%. It can never be below 0 or above 1.</p>
    {SCALE}
    <h2>2. Equally likely outcomes</h2>
    <p>A fair die, a fair coin, a spinner with <b>equal</b> sectors, a card or counter picked at random: every outcome has the same chance.</p>
    <div class="note fm">P(event) = outcomes that fit ÷ total outcomes</div>
    <p>Roll a die: P(prime) = 3/6 = 1/2 (2, 3, 5). Bag of 2 red, 5 blue, 3 green: P(red or green) = 5/10 = 1/2. Always divide by the <b>total</b>, not by "the rest".</p>
    <h2>3. "Not"</h2>
    <p>An event either happens or it doesn't, so <b>P(not A) = 1 − P(A)</b>. P(rain) = 0.3 → P(no rain) = 0.7. P(a 6) = 1/6 → P(not a 6) = 5/6.</p></div>
   <div><h2>4. Sample spaces</h2>
    <p>The <b>sample space</b> is the list of every possible outcome. Work in order. Two coins: <b>{{HH, HT, TH, TT}}</b>. HT and TH are different, so there are 4 outcomes, not 3.</p>
    <h2>5. Two-way tables</h2>
    <p>Two dice, scores added: 6 × 6 = 36 equally likely cells. A total of 7 is in 6 cells: P(7) = 6/36 = 1/6.</p>
    {dice_tbl}
    <h2>6. Tree diagrams</h2>
    <p>Toss a coin, then spin R, B, G. Each branch splits again: 2 × 3 = 6 outcomes. P(H and G) = 1/6.</p>
    {tree("HT", "RBG")}</div>
  </div>
  <div class="tip"><b>Exam tip:</b> "3 out of 8" and "3 : 5" are not probabilities: write <b>3/8</b>. List outcomes in order so nothing is missed or written twice, and check every answer is between 0 and 1.</div>
</div>

<div class="page p2">
  <div class="band"><div><div class="k">Practice · 34 questions</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Impossible, unlikely, even chance, likely or certain?</h2><ol class="q">{qs(A)}</ol>
  <h2>B. Equally likely outcomes (give fractions in their simplest form)</h2><ol class="q" start="7">{qs(B)}</ol>
  <h2>C. "Not" and "how many?"</h2><ol class="q" start="15">{"".join(f"<li>{q} <span class='line'></span></li>" for q, a, ok in C)}</ol>
  <h2>D. Sample spaces, tables and trees</h2><ol class="q" start="21">{qs(D)}</ol>
  <p class="small" style="margin-top:4px">Questions 31–34 are on the next page.</p>
</div>

<div class="page">
  <div class="band"><div><div class="k">Exam-style · then check</div><h1>Exam corner + answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>E. Exam-style questions (show your work)</h2>
  <ol class="q" start="31">{"".join(f"<li>{q}<span class='long'></span><span class='long'></span></li>" for q, a in E)}</ol>
  <h2 style="margin-top:12px">Answers</h2>
  <table class="ans"><tbody>
   <tr><td><b>A</b></td><td>{" · ".join(f"{i}. {word(p)} ({fr(p)})" for i, (q, p) in enumerate(A, 1))}</td></tr>
   <tr><td><b>B</b></td><td>{" · ".join(f"{i}. {fr(p)}" for i, (q, p) in enumerate(B, 7))}</td></tr>
   <tr><td><b>C</b></td><td>{" · ".join(f"{i}. {a}" for i, (q, a, ok) in enumerate(C, 15))}</td></tr>
   <tr><td><b>D</b></td><td>{" · ".join(f"{i}. {a}" for i, (q, a) in enumerate(D, 21))}</td></tr>
   <tr><td><b>E</b></td><td>{" · ".join(f"{i}. {a}" for i, (q, a) in enumerate(E, 31))}</td></tr>
  </tbody></table>
  <div class="note"><b>Got one wrong?</b> Check: did you divide by the total number of outcomes? Did you count repeated letters? Did you list HT and TH separately? Is your answer between 0 and 1? Then play <b>Spin &amp; Predict</b> at leim.ie/spin-and-predict.html: the "Go back over these" list at the end shows the rule for each mistake.</div>
  <p class="small">All questions written by Léim. Léim is independent and not connected with the State Examinations Commission or the NCCA.</p>
</div>
</body></html>"""

# ---------- teacher pack ----------
LINE = [("Rolling a 7 on a fair die", P(DIE, lambda n: n == 7)), ("Rolling a 1 on a fair die", P(DIE, lambda n: n == 1)),
        ("Getting heads when you toss a coin", F(1, 2)), ("Rolling a number less than 7 on a die", P(DIE, lambda n: n < 7)),
        ("A red counter from a bag of 9 red and 1 blue", P(bag(r=9, b=1), lambda c: c == "r")), ("A blue counter from a bag of 9 red and 1 blue", P(bag(r=9, b=1), lambda c: c == "b")),
        ("Rolling an even number on a die", P(DIE, lambda n: n % 2 == 0)), ("A total of 12 when you roll two dice", P(DICE, lambda s: sum(s) == 12)),
        ("Two heads when you toss two coins", P(S2, lambda s: s == "HH")), ("At least one head when you toss two coins", P(S2, lambda s: "H" in s)),
        ("A vowel from the letters of CORK", P(letters("CORK"), lambda c: c in "AEIOU")), ("Rolling a number bigger than 2 on a die", P(DIE, lambda n: n > 2)),
        ("A prime number from cards numbered 1 to 10", P(cards(10), isp)), ("Green on a spinner with 5 equal sectors, 3 of them green", F(3, 5)),
        ("The letter K from the letters of KILKENNY", P(letters("KILKENNY"), lambda c: c == "K")), ("A total of 7 when you roll two dice", P(DICE, lambda s: sum(s) == 7))]
line_sorted = sorted(LINE, key=lambda x: x[1])
random.seed(11); line_print = LINE[:]; random.shuffle(line_print)
line_html = "".join(f'<div class="c"><span class="tag">Card {i}</span><div class="fc">{x}</div></div>' for i, (x, p) in enumerate(line_print, 1))
num = {x: i for i, (x, p) in enumerate(line_print, 1)}
line_key = ", ".join(f"card {num[x]} ({fr(p)})" for x, p in line_sorted)
# Fair Game? two dice
GAMES = [("Add the scores. Player A wins with a total of 6, 7 or 8. Player B wins with any other total.", lambda s: sum(s) in (6, 7, 8), lambda s: sum(s) not in (6, 7, 8)),
         ("Add the scores. Player A wins with an odd total. Player B wins with an even total.", lambda s: sum(s) % 2 == 1, lambda s: sum(s) % 2 == 0),
         ("Multiply the scores. Player A wins with an even answer. Player B wins with an odd answer.", lambda s: s[0] * s[1] % 2 == 0, lambda s: s[0] * s[1] % 2 == 1),
         ("Add the scores. Player A wins with a total of 8 or more. Player B wins with 6 or less. A total of 7: roll again.", lambda s: sum(s) >= 8, lambda s: sum(s) <= 6)]
gres = [(sum(map(a, DICE)), sum(map(b, DICE))) for g, a, b in GAMES]
assert gres == [(16, 20), (18, 18), (27, 9), (15, 15)], gres
def verdict(x, y): return "fair" if x == y else f"not fair: {'A' if x > y else 'B'} is more likely to win"
games_html = "".join(f'<div class="idc"><h3>Game {i}: Fair or not?</h3><p style="font-size:9.8pt;margin:0 0 1mm">Roll two dice. {g}</p><p style="font-size:9pt;margin:0">A wins in ____ cells · B wins in ____ cells · Fair? ______ · A fairer rule: __________________________</p></div>' for i, (g, a, b) in enumerate(GAMES, 1))

DOMS = [("P(a 6 on a fair die)", F(1, 6)), ("P(heads on a coin)", F(1, 2)), ("P(a 7 on a fair die)", F(0)), ("P(less than 7 on a die)", F(1)),
        ("P(a multiple of 3 on a die)", F(1, 3)), ("P(NOT a 6 on a die)", F(5, 6)), ("two dice: P(a total of 12)", F(1, 36)), ("two coins: P(two heads)", F(1, 4)),
        ("two coins: P(at least one head)", F(3, 4)), ("outcomes when you roll two dice", 36), ("outcomes for a coin and a die", 12), ("outcomes when you toss three coins", 8),
        ("1 − 0.35", F("0.65")), ("2 red, 3 blue counters: P(red)", F(2, 5)), ("three coins: P(exactly two heads)", F(3, 8)), ("a coin and a die: P(H and a 6)", F(1, 12)),
        ("outcomes when you toss two coins", 4), ("3 red, 7 blue counters: P(not red)", F(7, 10)), ("P(no rain) if P(rain) = 0.7", F("0.3")), ("two dice: P(a total of 9)", F(1, 9))]
chk = [P(DIE, lambda n: n == 6), F(1, 2), P(DIE, lambda n: n == 7), P(DIE, lambda n: n < 7), P(DIE, lambda n: n % 3 == 0), P(DIE, lambda n: n != 6),
       P(DICE, lambda s: sum(s) == 12), P(S2, lambda s: s == "HH"), P(S2, lambda s: "H" in s), len(DICE), 2 * 6, len(c3), 1 - F("0.35"),
       P(bag(r=2, b=3), lambda c: c == "r"), P(c3, lambda s: s.count("H") == 2), P(list(product(COIN, DIE)), lambda s: s == ("H", 6)), len(S2),
       P(bag(r=3, b=7), lambda c: c != "r"), 1 - F("0.7"), P(DICE, lambda s: sum(s) == 9)]
for (k, v), c in zip(DOMS, chk): assert v == c, (k, v, c)
def dshow(v):
    if isinstance(v, int): return str(v)
    if v in (F("0.65"), F("0.3")): return str(float(v))
    return fr(v)
assert len(set(dshow(v) for k, v in DOMS)) == 20 and len(set(chk)) == 20
random.seed(1111); chain = DOMS[:]; random.shuffle(chain)
dom = [("START" if k == 0 else dshow(chain[k - 1][1]), x[0]) for k, x in enumerate(chain)] + [(dshow(chain[-1][1]), "FINISH")]
dom_print = dom[:]; random.shuffle(dom_print)
dom_html = "".join(f'<div class="dom"><div class="h l">{l}</div><div class="h r">{r}</div></div>' for l, r in dom_print)
chain_key = "".join(f"<li>{x} = <b>{dshow(v)}</b></li>" for x, v in chain)

ERR = [("3 red and 5 blue counters: P(red)", "= 3/5", "Divided by the rest, not the total: <b>3/8</b>"),
       ("Toss two coins: the sample space", "= {HH, HT, TT}", "TH is missing (HT and TH are different): <b>{HH, HT, TH, TT}</b>"),
       ("P(rain) = 0.3. P(no rain)?", "= 0.6", "P(not) = 1 − P: 1 − 0.3 = <b>0.7</b>"),
       ("Roll a die: P(an even number)", "= 3", "That's the number of outcomes, not a probability: 3/6 = <b>1/2</b>"),
       ("Letters of TIPPERARY: P(P)", "= 1/7", "Counted each different letter once. TIPPERARY has 9 letters and 2 are P: <b>2/9</b>"),
       ("Two dice: P(a total of 4)", "= 1/11", "The 11 totals aren't equally likely. Use the table: 3 of 36 cells, <b>1/12</b>")]
assert P(bag(r=3, b=5), lambda c: c == "r") == F(3, 8) and 1 - F("0.3") == F("0.7") and P(DIE, lambda n: n % 2 == 0) == F(1, 2)
assert P(letters("TIPPERARY"), lambda c: c == "P") == F(2, 9) and P(DICE, lambda s: sum(s) == 4) == F(1, 12) and len(set("TIPPERARY")) == 7
sp8 = ["r"] * 3 + ["b"] * 4 + ["g"]
w1 = (P(sp8, lambda c: c == "r"), P(sp8, lambda c: c != "b"), P(sp8, lambda c: c == "y")); assert w1 == (F(3, 8), F(1, 2), 0)
w2 = (P(cards(30), lambda n: n % 5 == 0), P(cards(30), lambda n: int(n ** .5) ** 2 == n)); assert w2 == (F(1, 5), F(1, 6))
cd = list(product(COIN, DIE)); w3 = P(cd, lambda s: s[0] == "T" and s[1] % 2 == 1); assert len(cd) == 12 and w3 == F(1, 4)
w4 = 40 * F("0.35"); assert w4 == 14
diffs = [abs(a - b) for a, b in DICE]; w5 = (F(diffs.count(0), 36), max(range(6), key=diffs.count), F(sum(d >= 3 for d in diffs), 36))
assert w5 == (F(1, 6), 1, F(1, 3)) and diffs.count(1) == 10

pack = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Probability Teacher Pack | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>
@page{{@bottom-left{{content:"Léim · leim.ie · Single-teacher licence · JC Maths LOs (2018 spec): {LO}";font-size:7pt}}}}
.proc td{{font-size:8.9pt;padding:3px 6px;line-height:1.32}}.proc td:first-child{{white-space:nowrap;font-weight:700;color:var(--green)}}
.p1 .note{{font-size:8.6pt;padding:6px 10px;line-height:1.35}}.p1 p{{font-size:9.5pt}}
.fym{{display:grid;grid-template-columns:repeat(4,1fr);margin-top:2mm}}
.fym .c{{border:2px dashed #9AA3AE;margin:-1px 0 0 -1px;height:20mm;position:relative;display:flex;align-items:center;justify-content:center;padding:4mm 2mm 1mm}}
.fym .fc{{font-size:10.5pt;font-weight:800;text-align:center;line-height:1.25}}
.fym .tag{{position:absolute;top:1.2mm;left:3mm;font-size:6.5pt;color:var(--green);font-weight:800;text-transform:uppercase;letter-spacing:.04em}}
.idc{{border:2px dashed #9AA3AE;padding:2.5mm 4mm;margin-top:2.5mm}}.idc h3{{margin:0 0 1mm;font-size:11pt}}
.doms{{display:grid;grid-template-columns:1fr 1fr;gap:2mm 6mm}}
.dom{{display:grid;grid-template-columns:1fr 1.9fr;border:2px dashed #9AA3AE;height:18.5mm}}
.dom .h{{display:flex;align-items:center;justify-content:center;text-align:center;padding:2mm;font-size:15pt;font-weight:800}}
.dom .r{{font-size:10.4pt}}
.dom .l{{background:var(--mist);border-right:2px solid var(--ink)}}
.poster{{height:255mm;border:6px solid var(--night);border-radius:18px;padding:10mm;display:flex;flex-direction:column;justify-content:space-between}}
.poster h1{{font-size:40pt;text-align:center}}.poster p{{font-size:14pt!important}}
.ops{{display:grid;grid-template-columns:1fr 1fr;gap:4mm}}.ops div{{border-radius:14px;padding:6mm 4mm;text-align:center;font-size:13pt;line-height:1.5}}.ops b{{display:block;font-size:20pt;font-weight:800;margin-bottom:1mm}}
.ws{{font-size:10pt;line-height:1.42}}.ws ol.q li{{margin:6px 0}}.ws .long{{height:21px}}
.eh td{{padding:5px 8px;font-size:9.6pt}}.eh td:first-child{{font-weight:700;width:30%}}.eh .gap{{display:block;border-bottom:1px solid #9AA3AE;height:16px}}
</style></head><body>

<div class="page p1">
  <div class="band"><div><div class="k">Junior Cycle Maths · Teacher pack</div><h1>Probability: chance &amp; sample spaces</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2018 specification): {LO} (relative frequency, experiments and the fundamental principle of counting are taught later)</p>
  <div class="two">
    <div><h3>Aims</h3><p>By the end of the lesson students can place events on a 0–1 probability scale, use the words impossible, unlikely, even chance, likely and certain, find probabilities of equally likely outcomes, use P(not A) = 1 − P(A), and list sample spaces systematically with lists, two-way tables and tree diagrams.</p></div>
    <div><h3>In this pack</h3><p>p.1 Teacher notes · p.2 Probability Line-Up cards + Fair Game? cards · p.3 Probability Dominoes (cut-up) · p.4 Wall poster · p.5 Worksheet: Error Hunt + exam-style questions · p.6 Answers. Level: 1st year (Higher and Ordinary), or 3rd-year revision. Time: about 60 minutes. All questions are original.</p></div>
  </div>
  <h2 style="margin-top:8px">Procedure</h2>
  <table class="proc"><tbody>
    <tr><td>5 min</td><td><b>Lead-in: Would you rather?</b> "I roll a die. You win €1 if it's a 6, or €1 if it's a prime number. Which bet do you take?" Vote, then ask how they could be sure. Elicit "count the outcomes".</td></tr>
    <tr><td>12 min</td><td><b>Probability Line-Up</b> (p.2 cards; one each). Stretch a string or draw a long line on the board from 0 (impossible) to 1 (certain). Students stand (or stick their card) where their event belongs, then justify it with a number. Equal probabilities stand together. Check against the key. Feedback: which cards share a place? Why is CORK's vowel at 1/4?</td></tr>
    <tr><td>8 min</td><td><b>Guided discovery: two coins.</b> Board "Toss two coins. P(one head and one tail)?" Many say 1/3 (HH, HT, TT). Hold up a 1c and a 2c coin: is "1c head, 2c tail" the same as "1c tail, 2c head"? Pairs list the outcomes in order: HH, HT, TH, TT, so the answer is 2/4 = 1/2.</td></tr>
    <tr><td>12 min</td><td><b>Fair Game?</b> (p.2, pairs, one game card each). Fill in a two-way table for two dice, count the cells for A and for B and decide whether the game is fair. Pairs who finish swap cards. Feedback: which games are fair? How would you fix the others?</td></tr>
    <tr><td>10 min</td><td><b>Probability Dominoes</b> (p.3), groups of 3–4. Start with START, work out the clue, find the domino with that answer on its left and build the chain to FINISH. Answer chain below.</td></tr>
    <tr><td>10 min</td><td><b>Worksheet</b> (p.5). Error Hunt in pairs (find the mistake, name the rule, fix it), then the exam-style questions alone.</td></tr>
    <tr><td>3 min</td><td><b>Exit ticket.</b> A bag has 4 red and 6 blue counters: P(blue)? P(not blue)? (3/5; 2/5). Homework: play <b>Spin &amp; Predict</b> at leim.ie/spin-and-predict.html (Tables &amp; trees round) and copy three lines from the "Go back over these" list.</td></tr>
  </tbody></table>
  <div class="note"><b>Line-Up key</b> (0 → 1): {line_key}.<br>
  <b>Fair Game? key:</b> {" · ".join(f"Game {i}: A {x}, B {y} cells, {verdict(x, y)}" for i, (x, y) in enumerate(gres, 1))}.<br>
  <b>Errors to look for:</b> dividing by "the rest" (3 red, 5 blue → 3/5) · HT and TH counted once · counting each repeated letter once · answers as "3 out of 8" or ratios · treating the 11 totals of two dice as equally likely · probabilities above 1. <b>Fast finishers:</b> invent your own fair game for two dice, then explain why 7 is the most likely total.</div>
  <p class="small"><b>Domino answer chain</b> (START → FINISH):</p>
  <ol class="small" style="columns:2;column-gap:12px;font-size:7.8pt;line-height:1.35;margin:0;padding-left:16px">{chain_key}</ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">Cut up the cards · one Line-Up card per student</div><h1>Probability Line-Up + Fair Game?</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.5pt;margin:0"><b>Probability Line-Up.</b> Cut out the 16 cards and give one to each student. Place your event on the line from 0 (impossible) to 1 (certain) and say its probability. (Big class? Print twice.)</p>
  <div class="fym">{line_html}</div>
  <p style="font-size:9.5pt;margin:3mm 0 0"><b>Fair Game?</b> A game is fair if both players have the same chance of winning. One card per pair: fill in a two-way table for two dice (6 × 6), count the cells where A wins and where B wins, and decide.</p>
  {games_html}
</div>

<div class="page">
  <div class="band"><div><div class="k">Groups of 3–4 · cut along the dashed lines</div><h1>Probability Dominoes</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.5pt">Start with START. Work out the clue on the right, then find the domino with that answer on its left. Keep going until you reach FINISH. Give fractions in their simplest form. No calculators!</p>
  <div class="doms">{dom_html}</div>
</div>

<div class="page">
  <div class="poster">
    <h1>Probability</h1>
    <div style="text-align:center">{SCALE.replace('width="100%"', 'width="100%" style="max-width:170mm;margin:0 auto"')}</div>
    <p style="text-align:center;font-size:17pt!important;margin:0;font-weight:800">P(event) = outcomes that fit ÷ total outcomes</p>
    <div class="ops">
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>"Not"</b>P(not A) = 1 − P(A)<br>P(rain) = 0.3<br>P(no rain) = 0.7</div>
      <div style="background:var(--green-soft)"><b>Sample space</b>every possible outcome<br>Two coins: HH, HT, TH, TT<br>HT ≠ TH!</div>
      <div style="background:var(--green-soft)"><b>Two-way table</b>two dice: 6 × 6 = 36 cells<br>P(total 7) = 6/36 = 1/6</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Tree diagram</b>coin, then spinner R, B, G<br>2 × 3 = 6 outcomes<br>P(H and G) = 1/6</div>
    </div>
    <p style="text-align:center;font-size:12pt;margin:0"><b>Divide by the total,</b> list outcomes in order, and check: 0 ≤ P ≤ 1.</p>
    <p style="text-align:center;font-size:10pt;color:var(--muted)">Léim · leim.ie · Play Spin &amp; Predict: leim.ie/spin-and-predict.html</p>
  </div>
</div>

<div class="page ws">
  <div class="band"><div><div class="k">Worksheet</div><h1>Error Hunt + exam-style questions</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Error Hunt</h2>
  <p>Each answer has one mistake. Find it, say which rule was broken, and write the right answer.</p>
  <table class="eh"><thead><tr><th>Question</th><th>Student's answer</th><th>The mistake and the right answer</th></tr></thead><tbody>
  {"".join(f"<tr><td>{q}</td><td>{w}</td><td><span class='gap'></span><span class='gap'></span></td></tr>" for q, w, r in ERR)}
  </tbody></table>
  <h2>B. Exam-style questions (show all your work)</h2>
  <ol class="q">
    <li>A spinner has 8 equal sectors: 3 red, 4 blue and 1 green. Find (a) P(red) (b) P(not blue) (c) P(yellow).<span class="long"></span></li>
    <li>Cards numbered 1 to 30 are shuffled and one is picked. Find (a) P(a multiple of 5) (b) P(a square number).<span class="long"></span></li>
    <li>A coin is tossed and a die is rolled. (a) List the sample space. (b) Find P(a tail and an odd number).<span class="long"></span><span class="long"></span></li>
    <li>A bag has 40 counters. The probability of picking a blue counter is 0.35. How many counters are blue? How many are not blue?<span class="long"></span></li>
    <li>Two dice are rolled and the smaller score is taken from the bigger one. (a) Draw a two-way table. (b) Find P(the difference is 0). (c) Which difference is most likely? (d) Find P(a difference of 3 or more).<span class="long"></span><span class="long"></span></li>
  </ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">For the teacher</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>Fair Game?</h2>
  <p style="font-size:9.6pt">{" · ".join(f"<b>Game {i}:</b> A {x}, B {y}: {verdict(x, y)}" for i, (x, y) in enumerate(gres, 1))}. Possible fix for Game 1: A wins with a total of 2, 6, 7, 8 or 12 (18 cells each). Game 3: any rule that gives each player 18 cells.</p>
  <h2>A. Error Hunt</h2>
  <table><tbody>{"".join(f"<tr><td style='width:32%'><b>{q}</b> {w}</td><td>{r}</td></tr>" for q, w, r in ERR)}</tbody></table>
  <h2>B. Exam-style questions</h2>
  <ol class="q">
    <li>(a) <b>{fr(w1[0])}</b> (b) 4 of 8: <b>{fr(w1[1])}</b> (c) <b>0</b> (impossible)</li>
    <li>(a) 5, 10, …, 30: 6 of 30 = <b>{fr(w2[0])}</b> (b) 1, 4, 9, 16, 25: 5 of 30 = <b>{fr(w2[1])}</b></li>
    <li>(a) H1, H2, H3, H4, H5, H6, T1, T2, T3, T4, T5, T6 (12) (b) T1, T3, T5: 3 of 12 = <b>{fr(w3)}</b></li>
    <li>40 × 0.35 = <b>{w4}</b> blue; 40 − 14 = <b>26</b> not blue</li>
    <li>(a) 36 cells (b) 6 of 36 = <b>{fr(w5[0])}</b> (c) <b>{w5[1]}</b> (10 cells) (d) 3, 4, 5: 6 + 4 + 2 = 12 cells, <b>{fr(w5[2])}</b></li>
  </ol>
  <h2>Marking tip</h2>
  <p>Give credit for each step, as the exam does: a correct list or table with one miscount still earns most of the marks. Insist on probabilities written as fractions, decimals or percentages (never "3 out of 8" or a ratio), and on fractions in their simplest form when the question asks for it.</p>
</div>
</body></html>"""
assert sum(1 for d in DICE if sum(d) in (2, 6, 7, 8, 12)) == 18

cover = """<!doctype html><html><head><meta charset="utf-8"><style>
body{margin:0;width:1200px;height:1200px;background:#1B2430;font-family:Inter,sans-serif;color:#fff;display:flex;flex-direction:column;justify-content:space-between;padding:90px;box-sizing:border-box}
.k{display:inline-block;background:#2E7D57;border-radius:99px;padding:12px 26px;font-weight:700;font-size:28px;letter-spacing:.06em;text-transform:uppercase}
h1{font-size:104px;font-weight:800;line-height:1.1;letter-spacing:-.03em;margin:40px 0 0}
h1 span{background:#F6CF5A;color:#1B2430;padding:0 14px}
.sub{font-size:38px;color:#C9D1DA;margin-top:36px;line-height:1.35}
.em{font-size:50px;margin-top:30px;font-weight:800;letter-spacing:.01em;color:#F6CF5A}
.foot{display:flex;justify-content:space-between;align-items:center;font-size:34px;font-weight:700}
.price{background:#F6CF5A;color:#1B2430;border-radius:16px;padding:14px 28px}
</style></head><body>
<div><span class="k">Junior Cycle Maths · Teacher pack</span>
<h1><span>Probability</span><br><span>&amp; Sample Spaces</span></h1>
<div class="sub">Probability Line-Up · Fair Game? cards<br>Probability Dominoes · Poster · Worksheet + answers</div>
<div class="em">P(not A) = 1 − P(A) · HT ≠ TH</div></div>
<div class="foot"><span>↗ Léim · leim.ie</span><span class="price">Ready to teach · 60 min</span></div>
</body></html>"""

if __name__ == "__main__":
    for name, txt in [("rules-and-practice", sheet), ("teacher-pack", pack), ("cover", cover)]:
        open(os.path.join(SRC, f"{SLUG}-{name}.html"), "w", encoding="utf-8").write(txt)
    def pdf(name, out):
        subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--no-pdf-header-footer", f"--print-to-pdf={out}",
                        f"{SLUG}-{name}.html"], cwd=SRC, check=True, capture_output=True)
        d = open(out, "rb").read(); print(name, len(re.findall(rb"/Type\s*/Page[^s]", d)), "pages")
    pdf("rules-and-practice", os.path.join(ROOT, "printables", f"{SLUG}-rules-and-practice.pdf"))
    pdf("teacher-pack", os.path.join(OUT, "Probability-Teacher-Pack-Leim.pdf"))
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--hide-scrollbars", "--window-size=1200,1200",
                    f"--screenshot={os.path.join(OUT, f'{SLUG}-cover.png')}", f"{SLUG}-cover.html"], cwd=SRC, check=True, capture_output=True)
