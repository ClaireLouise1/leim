#!/usr/bin/env python3
"""Probability 2: relative frequency & counting (JC Maths topic 26): free sheet + teacher pack + Payhip cover.
Run from the repo root: python3 src/build_probability2_pdfs.py OUTDIR
Writes src/relative-frequency-counting-*.html; PDFs/cover PNG go to OUTDIR (free sheet also to printables/).
Every answer is computed with Fraction / math.prod and asserted."""
import os, sys, random, subprocess, re
from fractions import Fraction as F
from math import prod, factorial
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC)
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/prob2"; os.makedirs(OUT, exist_ok=True)
SLUG = "relative-frequency-counting"
LO = "SP.1b, SP.2c"

def dec(x):
    x = F(x)
    for k in range(5):
        v = x * 10 ** k
        if v.denominator == 1:
            s = str(int(v)).rjust(k + 1, "0"); s = s if k == 0 else s[:-k] + "." + s[-k:]
            i, _, d = s.partition("."); i = f"{int(i):,}"; return i + ("." + d if d else "")
    raise ValueError(x)
def fr(x): x = F(x); return f"{x.numerator}/{x.denominator}" if x.denominator > 1 else str(x.numerator)
def rf(k, n): return F(k, n)
def exp(p, n): v = F(p) * n; assert v.denominator == 1, v; return int(v)
def perm(n, r): return prod(range(n - r + 1, n + 1))
assert dec(F(18, 50)) == "0.36" and dec(1000) == "1,000" and exp(F(1, 6), 300) == 50 and perm(8, 3) == 336

# ---------- free sheet ----------
A = [("A drawing pin is dropped 50 times and lands point up 18 times. Find the relative frequency of point up.", dec(rf(18, 50))),
     ("Aoife takes 40 penalties and scores 34. Find the relative frequency of scoring.", dec(rf(34, 40))),
     ("Cian flips a bottle 80 times and it lands standing up 12 times. Find the relative frequency as a percentage.", dec(rf(12, 80) * 100) + "%"),
     ("Of 250 seeds planted, 215 grew. Find the relative frequency of a seed growing.", dec(rf(215, 250))),
     ("A coin is tossed 20 times and lands heads 9 times. Find the relative frequency of heads as a fraction.", fr(rf(9, 20))),
     ("In a survey of 200 cars, 46 were red. Estimate the probability that the next car is red.", dec(rf(46, 200))),
     ("A die is rolled 120 times and a 6 comes up 26 times. Relative frequency of a 6 as a fraction?", fr(rf(26, 120))),
     ("A cup is thrown 25 times and lands on its side 17 times. Find the relative frequency of landing on its side.", dec(rf(17, 25)))]
assert [a for q, a in A] == ["0.36", "0.85", "15%", "0.86", "9/20", "0.23", "13/60", "0.68"], [a for q, a in A]
TB = [31, 36, 33, 30, 34, 36]; assert sum(TB) == 200
TBM = [17, 21, None, 19, 24, 20]; miss = 120 - sum(x for x in TBM if x)
B = [("The table shows 200 rolls of a die (above). Find the relative frequency of a 2.", dec(rf(TB[1], 200))),
     ("Same die: find the relative frequency of an even number.", dec(rf(TB[1] + TB[3] + TB[5], 200))),
     ("A second die is rolled 120 times: 1 → 17, 2 → 21, 3 → ?, 4 → 19, 5 → 24, 6 → 20. How many 3s?", str(miss)),
     ("Ciara: pin dropped 30 times, 12 point up. Seán: 50 times, 18 point up. Combined relative frequency?", dec(rf(12 + 18, 80))),
     ("Who has the better estimate in question 12, Ciara or Seán? Why?", "Seán (more trials)"),
     ("A die rolled 600 times gives 98, 101, 104, 97, 99, 101. Does it look fair? Why?", "fair: all close to 100")]
assert miss == 19 and [a for q, a in B][:4] == ["0.18", "0.51", "19", "0.375"]
C = [("A fair die is rolled 300 times. How many times would you expect a 5?", exp(F(1, 6), 300)),
     ("A fair coin is tossed 250 times. How many heads would you expect?", exp(F(1, 2), 250)),
     ("A spinner has 8 equal sectors, 3 blue. Expected blues in 400 spins?", exp(F(3, 8), 400)),
     ("2 red and 3 green counters; one is picked and put back 150 times. Expected reds?", exp(F(2, 5), 150)),
     ("Using question 1, how many times would you expect the pin to land point up in 1,000 drops?", exp(rf(18, 50), 1000)),
     ("P(the bus is late) = 0.15. On how many of the next 60 school days would you expect it to be late?", exp(F("0.15"), 60)),
     ("P(red) = 1/4. How many spins are needed to expect red 30 times?", int(30 / F(1, 4))),
     ("A bag of 20 counters: picked and put back 200 times, red 70 times. Estimate the red counters.", exp(rf(70, 200), 20))]
assert [a for q, a in C] == [50, 125, 150, 60, 360, 9, 120, 7]
D = [("A café has 4 starters, 5 mains and 3 desserts. How many lunch deals (one of each)?", 4 * 5 * 3),
     ("Saoirse has 5 tops and 3 pairs of jeans. How many outfits (top + jeans)?", 5 * 3),
     ("A bike lock has 4 dials, each 0 to 9. How many codes?", 10 ** 4),
     ("A code is one letter A to Z then one digit 0 to 9. How many codes?", 26 * 10),
     ("In how many ways can 5 friends stand in a row?", factorial(5)),
     ("10 runners: in how many ways can gold, silver and bronze be won?", perm(10, 3)),
     ("3-digit codes from the digits 1 to 6, no digit used twice. How many?", perm(6, 3)),
     ("A hoodie: 6 colours, 4 sizes, with or without a name. How many types?", 6 * 4 * 2)]
assert [a for q, a in D] == [60, 15, 10000, 260, 120, 720, 120, 48]
E = [("A paper spinner has 3 colours. It is spun 200 times: red 46, blue 92, green 62. (a) Find the relative frequency of each colour. (b) Estimate how many times it would land on blue in 1,500 spins. (c) Niamh says the spinner must be fair because every colour came up. Is she right? Explain.",
      f"(a) red <b>{dec(rf(46, 200))}</b>, blue <b>{dec(rf(92, 200))}</b>, green <b>{dec(rf(62, 200))}</b> (b) {dec(rf(92, 200))} × 1,500 = <b>{exp(rf(92, 200), 1500)}</b> (c) <b>No</b>: if fair, each would be about 200 ÷ 3 ≈ 67; blue came up 92 times and red only 46, so it looks biased."),
     ("Darragh and Róisín test the same drawing pin. Darragh: 20 drops, 14 point up. Róisín: 180 drops, 99 point up. (a) Find each relative frequency. (b) Whose estimate is better? Why? (c) Put the results together to estimate the probability. (d) Estimate how many times it lands point up in 600 drops.",
      f"(a) <b>{dec(rf(14, 20))}</b> and <b>{dec(rf(99, 180))}</b> (b) <b>Róisín's</b>: more trials (c) 113 of 200 = <b>{dec(rf(113, 200))}</b> (d) {dec(rf(113, 200))} × 600 = <b>{exp(rf(113, 200), 600)}</b>"),
     ("A pizza shop offers 3 bases, 6 toppings and 2 sizes. A pizza is one base, one topping and one size. (a) How many different pizzas? (b) A pizza is picked at random. Find P(it has the chilli topping). (c) The shop adds more toppings and now has 54 different pizzas. How many toppings now?",
      f"(a) 3 × 6 × 2 = <b>{3 * 6 * 2}</b> (b) 3 × 1 × 2 = 6 of 36: <b>{fr(F(6, 36))}</b> (c) 54 ÷ (3 × 2) = <b>{54 // 6}</b>"),
     ("A phone PIN has 4 digits, each 0 to 9. (a) How many PINs are possible? (b) How many start with 0? (c) How many have four different digits? (d) A PIN is picked at random. Find P(all four digits are different) as a decimal.",
      f"(a) <b>{10 ** 4:,}</b> (b) 1 × 10 × 10 × 10 = <b>{10 ** 3:,}</b> (c) 10 × 9 × 8 × 7 = <b>{perm(10, 4):,}</b> (d) 5,040 ÷ 10,000 = <b>{dec(F(perm(10, 4), 10 ** 4))}</b>")]
assert exp(rf(92, 200), 1500) == 690 and dec(rf(113, 200)) == "0.565" and exp(rf(113, 200), 600) == 339 and perm(10, 4) == 5040

def qs(items): return "".join(f"<li>{q} <span class='line'></span></li>" for q, a in items)
def htab(head, outs, fs, cls="dt"):
    return f"<table class='{cls}'><tr><th>{head}</th>" + "".join(f"<th>{o}</th>" for o in outs) + "</tr><tr><th>Frequency</th>" + "".join(f"<td>{f}</td>" for f in fs) + "</tr></table>"
COINT = [(10, 7), (100, 46), (1000, 503)]
coin_tbl = "<table class='dt'><tr><th>Tosses</th>" + "".join(f"<th>{n:,}</th>" for n, k in COINT) + "</tr><tr><th>Heads</th>" + "".join(f"<td>{k}</td>" for n, k in COINT) + "</tr><tr><th>Rel. freq.</th>" + "".join(f"<td>{dec(rf(k, n))}</td>" for n, k in COINT) + "</tr></table>"
DA = [96, 104, 99, 107, 93, 101]; DB = [78, 81, 74, 83, 79, 205]; assert sum(DA) == sum(DB) == 600

sheet = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Probability 2: relative frequency and counting: rules and practice | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>@page{{@bottom-left{{content:"Léim · leim.ie · Free to print for home or class · JC Maths LOs (2018 spec): {LO}"}}}}
.tight{{font-size:10pt;line-height:1.42}}.tight h2{{margin:9px 0 4px;font-size:13.5pt}}.tight .note,.tight .tip{{padding:6px 10px;margin:6px 0}}
ol.q{{padding-left:30px}}ol.q li{{margin:7px 0}}
.p2{{font-size:9pt}}.p2 ol.q li{{margin:2.4px 0}}.p2 h2{{margin:6px 0 2px}}.p2 .line{{min-width:70px}}
.ans td{{padding:3px 6px;font-size:8.8pt}}
.dt{{width:auto;margin:3px 0}}.dt td,.dt th{{text-align:center;padding:1px 6px;font-size:9pt}}
.fm{{text-align:center;font-weight:800;font-size:11pt}}
</style></head><body>
<div class="page tight">
  <div class="band"><div><div class="k">Junior Cycle Maths · Free revision sheet</div><h1>Probability 2: relative frequency &amp; counting</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2018 specification): {LO}. Play the game: <b>leim.ie/coin-dice-lab.html</b></p>
  <div class="two">
   <div><h2>1. Relative frequency</h2>
    <div class="note fm">Relative frequency = times it happened ÷ number of trials</div>
    <p>A drawing pin is dropped 50 times and lands point up 18 times: 18 ÷ 50 = <b>0.36</b> (= 36% = 9/25). Divide by the number of <b>trials</b>, not by "the rest".</p>
    <h2>2. Estimating a probability</h2>
    <p>When outcomes are not equally likely (a pin, a bent coin, a penalty), do an experiment: the relative frequency is your <b>estimate</b> of the probability. The more trials, the better the estimate.</p>
    {coin_tbl}
    <p>To combine results, <b>add the counts first</b>: 12 of 30 and 18 of 50 → 30 of 80 = 0.375.</p>
    <h2>3. Expected frequency</h2>
    <div class="note fm">Expected frequency = probability × number of trials</div>
    <p>Fair die, 300 rolls: expect 1/6 × 300 = <b>50</b> sixes (about 50, not exactly). Pin from section 1, 1,000 drops: 0.36 × 1,000 = <b>360</b>.</p></div>
   <div><h2>4. Fair or biased?</h2>
    <p>Compare the results with what you'd expect. A die rolled 600 times: expect about 100 of each.</p>
    <table class='dt'><tr><th>Score</th>{"".join(f"<th>{i}</th>" for i in range(1, 7))}</tr><tr><th>Die A</th>{"".join(f"<td>{x}</td>" for x in DA)}</tr><tr><th>Die B</th>{"".join(f"<td>{x}</td>" for x in DB)}</tr></table>
    <p>Die A: all close to 100, so <b>fair</b>. Die B: a 6 came up about twice as often as expected, so probably <b>biased</b>. Only a few trials? You can't tell.</p>
    <h2>5. The fundamental principle of counting</h2>
    <div class="note fm">m ways, then n ways → m × n ways together</div>
    <p>3 starters, 4 mains, 2 desserts: 3 × 4 × 2 = <b>24</b> meals. A lock with 3 dials (0–9): 10 × 10 × 10 = <b>1,000</b> codes.</p>
    <h2>6. When you can't repeat</h2>
    <p>The choices go down: 4 friends in a row: 4 × 3 × 2 × 1 = <b>24</b>. Gold, silver and bronze from 8 runners: 8 × 7 × 6 = <b>336</b>. A 3-dial code set at random: P(7 1 3) = <b>1/1,000</b>.</p></div>
  </div>
  <div class="tip"><b>Exam tip:</b> show the division ("18 ÷ 50 = 0.36"), write the answer the way the question asks (decimal, % or fraction), give reasons with numbers ("a 6 came up 205 times but we'd expect about 100"), and <b>multiply, don't add</b>, when counting.</div>
</div>

<div class="page p2">
  <div class="band"><div><div class="k">Practice · 34 questions</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Relative frequency (give decimals unless asked otherwise)</h2><ol class="q">{qs(A)}</ol>
  <h2>B. Results tables</h2>{htab("Score", range(1, 7), TB)}<ol class="q" start="9">{qs(B)}</ol>
  <h2>C. Expected frequency</h2><ol class="q" start="15">{qs(C)}</ol>
  <h2>D. The fundamental principle of counting</h2><ol class="q" start="23">{qs(D)}</ol>
  <p class="small" style="margin-top:4px">Questions 31–34 are on the next page.</p>
</div>

<div class="page">
  <div class="band"><div><div class="k">Exam-style · then check</div><h1>Exam corner + answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>E. Exam-style questions (show your work)</h2>
  <ol class="q" start="31">{"".join(f"<li>{q}<span class='long'></span><span class='long'></span></li>" for q, a in E)}</ol>
  <h2 style="margin-top:12px">Answers</h2>
  <table class="ans"><tbody>
   <tr><td><b>A</b></td><td>{" · ".join(f"{i}. {a}" for i, (q, a) in enumerate(A, 1))}</td></tr>
   <tr><td><b>B</b></td><td>{" · ".join(f"{i}. {a}" for i, (q, a) in enumerate(B, 9))}</td></tr>
   <tr><td><b>C</b></td><td>{" · ".join(f"{i}. {a:,}" for i, (q, a) in enumerate(C, 15))}</td></tr>
   <tr><td><b>D</b></td><td>{" · ".join(f"{i}. {a:,}" for i, (q, a) in enumerate(D, 23))}</td></tr>
   <tr><td><b>E</b></td><td>{" · ".join(f"{i}. {a}" for i, (q, a) in enumerate(E, 31))}</td></tr>
  </tbody></table>
  <div class="note"><b>Got one wrong?</b> Check: did you divide by the number of trials? Did you multiply by the number of trials for "expect"? Did you multiply (not add) the choices when counting? When you can't repeat, do the choices go down? Then play <b>Coin &amp; Dice Lab</b> at leim.ie/coin-dice-lab.html: the "Go back over these" list at the end shows the rule for each mistake.</div>
  <p class="small">All questions written by Léim. Léim is independent and not connected with the State Examinations Commission or the NCCA.</p>
</div>
</body></html>"""

# ---------- teacher pack ----------
MING = [("Pin: 50 drops, 18 point up. Relative frequency?", dec(rf(18, 50))),
        ("Fair die, 600 rolls. Expected sixes?", str(exp(F(1, 6), 600))),
        ("3 starters, 5 mains, 2 desserts. Meal deals?", str(3 * 5 * 2)),
        ("Lock: 3 dials, each 0–9. Codes?", f"{10 ** 3:,}"),
        ("Coin: 400 tosses. Expected heads?", str(exp(F(1, 2), 400))),
        ("4 friends in a row. How many ways?", str(factorial(4))),
        ("P(late) = 0.15. Late days out of 60?", str(exp(F("0.15"), 60))),
        ("12 of 40 seeds grew. Relative frequency?", dec(rf(12, 40))),
        ("Rel. freq. of red = 0.2. Reds in 350 spins?", str(exp(F("0.2"), 350))),
        ("Gold, silver, bronze from 6 runners?", str(perm(6, 3))),
        ("P(red) = 1/4. Spins to expect 20 reds?", str(int(20 / F(1, 4)))),
        ("A letter A–E, then a digit 0–9. Codes?", str(5 * 10))]
assert len(set(a for q, a in MING)) == 12, [a for q, a in MING]
random.seed(26); cards = [("Q", q) for q, a in MING] + [("A", a) for q, a in MING]; random.shuffle(cards)
ming_html = "".join(f'<div class="c"><span class="tag">{"Question" if k == "Q" else "Answer"}</span><div class="fc{" sm" if k == "Q" else ""}">{t}</div></div>' for k, t in cards)
ming_key = " · ".join(f"{q} → <b>{a}</b>" for q, a in MING)

DOMS = [("rel. freq.: 9 heads in 20 tosses", dec(rf(9, 20))), ("expected 6s in 120 rolls of a fair die", str(exp(F(1, 6), 120))),
        ("outfits: 2 shirts, 3 pairs of trousers", str(2 * 3)), ("codes: 2 dials, each 0–9", str(10 ** 2)),
        ("rel. freq.: 30 out of 200", dec(rf(30, 200))), ("expected heads in 90 tosses", str(exp(F(1, 2), 90))),
        ("P(code is 3 7) on a 2-dial lock", "1/100"), ("meal deals: 3 starters, 5 mains", str(3 * 5)),
        ("1st and 2nd place from 7 runners", str(perm(7, 2))), ("0.3 × 70 trials (expected)", str(exp(F("0.3"), 70))),
        ("rel. freq. 0.25: expected in 36 trials", str(exp(F("0.25"), 36))), ("3-digit codes, digits 1–3, repeats allowed", str(3 ** 3)),
        ("ways to arrange the letters of CORK", str(factorial(4))), ("rel. freq.: 7 out of 25 (as a %)", dec(rf(7, 25) * 100) + "%"),
        ("bag of 10, red 40 times in 200 picks: red counters?", str(exp(rf(40, 200), 10))), ("rel. freq.: 13 out of 50", dec(rf(13, 50))),
        ("tosses needed to expect 35 heads", str(int(35 / F(1, 2)))), ("hoodies: 4 colours, 2 sizes, name or no name", str(4 * 2 * 2)),
        ("5 people in a row", str(factorial(5))), ("expected 5s in 18 rolls of a fair die", str(exp(F(1, 6), 18)))]
vals = [a for k, a in DOMS]; assert len(set(vals)) == 20, sorted(vals)
random.seed(2626); chain = DOMS[:]; random.shuffle(chain)
dom = [("START" if k == 0 else chain[k - 1][1], x[0]) for k, x in enumerate(chain)] + [(chain[-1][1], "FINISH")]
dom_print = dom[:]; random.shuffle(dom_print)
dom_html = "".join(f'<div class="dom"><div class="h l">{l}</div><div class="h r">{r}</div></div>' for l, r in dom_print)
chain_key = "".join(f"<li>{x} = <b>{v}</b></li>" for x, v in chain)

ERR = [("A pin lands point up 18 times in 50 drops. Relative frequency?", "= 18/32", "Divided by the rest, not the trials: 18 ÷ 50 = <b>0.36</b>"),
       ("A fair die is rolled 60 times. How many sixes will you get?", "= exactly 10", "That's the <b>expected</b> number: you'll get <b>about 10</b>, rarely exactly"),
       ("4 starters, 3 mains, 2 desserts. Meal deals?", "= 4 + 3 + 2 = 9", "Multiply, don't add: 4 × 3 × 2 = <b>24</b>"),
       ("Ciara: 12 of 30. Seán: 18 of 50. Together?", "= (0.4 + 0.36) ÷ 2 = 0.38", "Add the counts first: 30 ÷ 80 = <b>0.375</b>"),
       ("5 heads in a row. P(tail next)?", "= more than 1/2: it's due", "A coin has no memory: still <b>1/2</b>"),
       ("Gold, silver, bronze from 8 runners?", "= 8 × 8 × 8 = 512", "No one can win two medals: 8 × 7 × 6 = <b>336</b>")]
assert rf(18, 50) == F(9, 25) and 4 * 3 * 2 == 24 and rf(30, 80) == F("0.375") and perm(8, 3) == 336
WS = [("A spinner is spun 250 times and lands on green 85 times. (a) Find the relative frequency of green. (b) Estimate how many greens in 1,000 spins.", f"(a) <b>{dec(rf(85, 250))}</b> (b) <b>{exp(rf(85, 250), 1000)}</b>"),
      ("A fair spinner has 5 equal sectors: 2 red, 2 blue, 1 yellow. It is spun 300 times. How many times would you expect (a) red (b) yellow?", f"(a) <b>{exp(F(2, 5), 300)}</b> (b) <b>{exp(F(1, 5), 300)}</b>"),
      ("A die is rolled 300 times: 1 → 52, 2 → 47, 3 → 50, 4 → 49, 5 → 53, 6 → 49. Is it fair? Give a reason with numbers.", "<b>Fair</b>: expect 50 each; every result is within 3 of 50"),
      ("A school canteen offers 4 sandwiches, 3 drinks and 5 pieces of fruit. (a) How many lunches (one of each)? (b) Two more drinks are added. How many now?", f"(a) <b>{4 * 3 * 5}</b> (b) 4 × 5 × 5 = <b>{4 * 5 * 5}</b>"),
      ("A code uses the letters A, B, C, D, E, each at most once, and has 3 letters. (a) How many codes? (b) A code is picked at random: P(it starts with A)?", f"(a) 5 × 4 × 3 = <b>{perm(5, 3)}</b> (b) 4 × 3 = 12 of 60: <b>{fr(F(12, 60))}</b>")]
assert sum([52, 47, 50, 49, 53, 49]) == 300

pack = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Relative Frequency &amp; Counting Teacher Pack | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>
@page{{@bottom-left{{content:"Léim · leim.ie · Single-teacher licence · JC Maths LOs (2018 spec): {LO}";font-size:7pt}}}}
.proc td{{font-size:8.6pt;padding:3px 6px;line-height:1.3}}.proc td:first-child{{white-space:nowrap;font-weight:700;color:var(--green)}}
.p1 .note{{font-size:8.4pt;padding:6px 10px;line-height:1.35}}.p1 p{{font-size:9.3pt}}
.fym{{display:grid;grid-template-columns:repeat(4,1fr);margin-top:2mm}}
.fym .c{{border:2px dashed #9AA3AE;margin:-1px 0 0 -1px;height:15mm;position:relative;display:flex;align-items:center;justify-content:center;padding:4mm 2mm 1mm}}
.fym .fc{{font-size:13pt;font-weight:800;text-align:center;line-height:1.2}}.fym .fc.sm{{font-size:8.8pt}}
.fym .tag{{position:absolute;top:1.2mm;left:3mm;font-size:6.5pt;color:var(--green);font-weight:800;text-transform:uppercase;letter-spacing:.04em}}
.idc{{border:2px dashed #9AA3AE;padding:2.5mm 4mm;margin-top:2.5mm}}.idc h3{{margin:0 0 1mm;font-size:11pt}}
.rec{{width:100%;border-collapse:collapse;margin:1.5mm 0}}.rec td,.rec th{{border:1px solid #9AA3AE;padding:1.4mm 2mm;font-size:8.6pt;text-align:center}}.rec th{{background:var(--mist);color:var(--ink);text-transform:none;letter-spacing:0;font-weight:700}}
.doms{{display:grid;grid-template-columns:1fr 1fr;gap:2mm 6mm}}
.dom{{display:grid;grid-template-columns:1fr 1.9fr;border:2px dashed #9AA3AE;height:18.5mm}}
.dom .h{{display:flex;align-items:center;justify-content:center;text-align:center;padding:2mm;font-size:15pt;font-weight:800}}
.dom .r{{font-size:10.2pt}}
.dom .l{{background:var(--mist);border-right:2px solid var(--ink)}}
.poster{{height:255mm;border:6px solid var(--night);border-radius:18px;padding:10mm;display:flex;flex-direction:column;justify-content:space-between}}
.poster h1{{font-size:38pt;text-align:center}}.poster p{{font-size:14pt!important}}
.big3{{display:grid;gap:5mm}}.big3 div{{border-radius:14px;padding:6mm 5mm;text-align:center;font-size:13pt;line-height:1.5}}.big3 b{{display:block;font-size:21pt;font-weight:800;margin-bottom:1mm}}
.ws{{font-size:10pt;line-height:1.42}}.ws ol.q li{{margin:6px 0}}.ws .long{{height:21px}}
.eh td{{padding:5px 8px;font-size:9.6pt}}.eh td:first-child{{font-weight:700;width:30%}}.eh .gap{{display:block;border-bottom:1px solid #9AA3AE;height:16px}}
</style></head><body>

<div class="page p1">
  <div class="band"><div><div class="k">Junior Cycle Maths · Teacher pack</div><h1>Relative frequency &amp; counting</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2018 specification): {LO} (sample spaces, two-way tables and equally likely outcomes come first, in Probability 1)</p>
  <div class="two">
    <div><h3>Aims</h3><p>By the end of the lesson students can find relative frequencies from experiments, explain why more trials give a better estimate of a probability, work out expected frequencies, judge whether a die or spinner is fair, and use the fundamental principle of counting (including choices that go down when nothing can be repeated).</p></div>
    <div><h3>In this pack</h3><p>p.1 Teacher notes · p.2 Class Experiment record + Coin &amp; Dice Lab mingle cards · p.3 Probability Dominoes (cut-up) · p.4 Wall poster · p.5 Worksheet: Error Hunt + exam-style questions · p.6 Answers. Level: 2nd year (Higher and Ordinary), or 3rd-year revision. Time: about 60 minutes. All questions are original.</p></div>
  </div>
  <h2 style="margin-top:8px">Procedure</h2>
  <table class="proc"><tbody>
    <tr><td>5 min</td><td><b>Lead-in: is it 50 : 50?</b> Hold up a drawing pin (or a plastic cup). "It lands point up or point down. So P(point up) = 1/2?" Take a vote. Elicit that the outcomes are not equally likely, so we can't count: we have to experiment.</td></tr>
    <tr><td>15 min</td><td><b>Class Experiment</b> (p.2 record, one per pair, a drawing pin or cup each). Pairs drop it 50 times, tally, and fill in the relative frequency after 10, 20, 30, 40 and 50 drops. Pool the class results on the board (add the counts, then divide). Discuss: whose 10-drop result was furthest from the class value? Why is the class value the best estimate?</td></tr>
    <tr><td>5 min</td><td><b>Guided discovery: expected frequency.</b> "If we dropped it 1,000 times, how many point up?" Students suggest a number and how they got it: relative frequency × 1,000. Then "a fair die, 300 rolls, how many sixes?" → 1/6 × 300 = 50, and "will it be exactly 50?"</td></tr>
    <tr><td>12 min</td><td><b>Coin &amp; Dice Lab mingle</b> (p.2, 24 cards = 12 question/answer pairs; one each). Question card? Work it out and find your answer. Answer card? Find your question. Pairs then explain their method to another pair. Board the counting rule from the meal-deal and lock cards: multiply the choices.</td></tr>
    <tr><td>10 min</td><td><b>Probability Dominoes</b> (p.3), groups of 3–4. Start with START, work out the clue, find the domino with that answer on its left and build the chain to FINISH. Answer chain below.</td></tr>
    <tr><td>10 min</td><td><b>Worksheet</b> (p.5). Error Hunt in pairs (find the mistake, name the rule, fix it), then the exam-style questions alone.</td></tr>
    <tr><td>3 min</td><td><b>Exit ticket.</b> 7 of 20 bottle flips land standing up: relative frequency? How many in 200 flips? (0.35; 70.) Homework: play <b>Coin &amp; Dice Lab</b> at leim.ie/coin-dice-lab.html and throw a coin 10,000 times in the lab under the game.</td></tr>
  </tbody></table>
  <div class="note"><b>Mingle key:</b> {ming_key}.<br>
  <b>Errors to look for:</b> dividing by "the rest" instead of the trials · "you will get exactly 50" · trusting 10 trials over 500 · averaging two relative frequencies from different numbers of trials · adding the choices instead of multiplying · letting one runner win two medals. <b>Fast finishers:</b> design a "fair or biased?" test for a die: how many rolls would you do, and what results would convince you?</div>
  <p class="small"><b>Domino answer chain</b> (START → FINISH):</p>
  <ol class="small" style="columns:2;column-gap:12px;font-size:7.8pt;line-height:1.35;margin:0;padding-left:16px">{chain_key}</ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">One record per pair · cut up the cards</div><h1>Class Experiment + mingle cards</h1></div><div class="logo">↗ Léim</div></div>
  <div class="idc"><h3>Class Experiment: is it 50 : 50?</h3>
   <p style="font-size:9pt;margin:0 0 1mm">Drop a drawing pin (or throw a plastic cup) 50 times. Tally each result, then fill in the relative frequency of point up (or on its side) as you go. Names: ______________________ Object: ______________</p>
   <table class="rec"><tr><th>Drops</th><th>1–10</th><th>11–20</th><th>21–30</th><th>31–40</th><th>41–50</th></tr>
   <tr><th>Tally: point up</th><td></td><td></td><td></td><td></td><td></td></tr>
   <tr><th>Point up so far</th><td></td><td></td><td></td><td></td><td></td></tr>
   <tr><th>Relative frequency so far</th><td>÷ 10 =</td><td>÷ 20 =</td><td>÷ 30 =</td><td>÷ 40 =</td><td>÷ 50 =</td></tr>
   <tr><th>Whole class</th><td colspan="5" style="text-align:left">point up ______ out of ______ drops → relative frequency ______</td></tr></table>
   <p style="font-size:9pt;margin:0">1. Which is the best estimate of P(point up): your 10 drops, your 50, or the whole class? Why? 2. How many times would you expect point up in 1,000 drops? 3. Is P(point up) = 1/2? Use your numbers.</p></div>
  <p style="font-size:8.8pt;margin:2.5mm 0 0"><b>Coin &amp; Dice Lab mingle.</b> Cut out the 24 cards and give one to each student. Question card? Work it out, then find the person with your answer. Answer card? Find the question that gives your answer. (Fewer students? Take out whole pairs.)</p>
  <div class="fym">{ming_html}</div>
</div>

<div class="page">
  <div class="band"><div><div class="k">Groups of 3–4 · cut along the dashed lines</div><h1>Probability Dominoes</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.5pt">Start with START. Work out the clue on the right, then find the domino with that answer on its left. Keep going until you reach FINISH. Write fractions in their simplest form. No calculators!</p>
  <div class="doms">{dom_html}</div>
</div>

<div class="page">
  <div class="poster">
    <h1>Probability from experiments</h1>
    <div class="big3">
      <div style="background:var(--green-soft)"><b>Relative frequency</b>= times it happened ÷ number of trials<br>18 point up in 50 drops → 18 ÷ 50 = 0.36</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Expected frequency</b>= probability × number of trials<br>fair die, 300 rolls → 1/6 × 300 = 50 sixes</div>
      <div style="background:var(--green-soft)"><b>Counting</b>m ways, then n ways → m × n ways<br>3 starters × 4 mains × 2 desserts = 24 meals<br>no repeats? the choices go down: 8 × 7 × 6</div>
    </div>
    <p style="text-align:center;font-size:17pt!important;margin:0;font-weight:800">More trials → a better estimate of the probability</p>
    <p style="text-align:center;font-size:12pt;margin:0">Results are never exactly what you expect. A coin has no memory.</p>
    <p style="text-align:center;font-size:10pt;color:var(--muted)">Léim · leim.ie · Play Coin &amp; Dice Lab: leim.ie/coin-dice-lab.html</p>
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
  <ol class="q">{"".join(f"<li>{q}<span class='long'></span></li>" for q, a in WS)}</ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">For the teacher</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>Class Experiment</h2>
  <p style="font-size:9.6pt">Answers depend on the class data. 1: the whole class (most trials). 2: relative frequency × 1,000. 3: drawing pins usually land point up well over or under half the time, so <b>no</b>; the class relative frequency is the evidence.</p>
  <h2>A. Error Hunt</h2>
  <table><tbody>{"".join(f"<tr><td style='width:32%'><b>{q}</b> {w}</td><td>{r}</td></tr>" for q, w, r in ERR)}</tbody></table>
  <h2>B. Exam-style questions</h2>
  <ol class="q">{"".join(f"<li>{a}</li>" for q, a in WS)}</ol>
  <h2>Marking tip</h2>
  <p>Give credit for each step, as the exam does: the division for a relative frequency, the multiplication for an expected frequency or a count. For "is it fair?" insist on a reason with numbers: the expected value and the result that is (or isn't) far from it. "Biased, because they're not all equal" earns little.</p>
</div>
</body></html>"""
assert exp(rf(85, 250), 1000) == 340 and perm(5, 3) == 60

cover = """<!doctype html><html><head><meta charset="utf-8"><style>
body{margin:0;width:1200px;height:1200px;background:#1B2430;font-family:Inter,sans-serif;color:#fff;display:flex;flex-direction:column;justify-content:space-between;padding:90px;box-sizing:border-box}
.k{display:inline-block;background:#2E7D57;border-radius:99px;padding:12px 26px;font-weight:700;font-size:28px;letter-spacing:.06em;text-transform:uppercase}
h1{font-size:100px;font-weight:800;line-height:1.1;letter-spacing:-.03em;margin:40px 0 0}
h1 span{background:#F6CF5A;color:#1B2430;padding:0 14px}
.sub{font-size:38px;color:#C9D1DA;margin-top:36px;line-height:1.35}
.em{font-size:48px;margin-top:30px;font-weight:800;letter-spacing:.01em;color:#F6CF5A}
.foot{display:flex;justify-content:space-between;align-items:center;font-size:34px;font-weight:700}
.price{background:#F6CF5A;color:#1B2430;border-radius:16px;padding:14px 28px}
</style></head><body>
<div><span class="k">Junior Cycle Maths · Teacher pack</span>
<h1><span>Relative Frequency</span><br><span>&amp; Counting</span></h1>
<div class="sub">Class Experiment · Coin &amp; Dice Lab mingle<br>Probability Dominoes · Poster · Worksheet + answers</div>
<div class="em">18 ÷ 50 = 0.36 · 3 × 4 × 2 = 24</div></div>
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
    pdf("teacher-pack", os.path.join(OUT, "Relative-Frequency-and-Counting-Teacher-Pack-Leim.pdf"))
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--hide-scrollbars", "--window-size=1200,1200",
                    f"--screenshot={os.path.join(OUT, f'{SLUG}-cover.png')}", f"{SLUG}-cover.html"], cwd=SRC, check=True, capture_output=True)
