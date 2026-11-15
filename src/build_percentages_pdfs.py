#!/usr/bin/env python3
"""Percentages (JC Maths topic 6): free sheet + teacher pack + Payhip cover.
Run from the repo root: python3 src/build_percentages_pdfs.py OUTDIR
Writes src/percentages-*.html; PDFs/cover PNG go to OUTDIR (free sheet also to printables/).
Every answer is computed with Python's Fraction and asserted."""
import os, sys, random, subprocess, re
from fractions import Fraction as F
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC)
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/percentages"; os.makedirs(OUT, exist_ok=True)
SLUG = "percentages"
LO = "N.2a, N.2b"

def dec(x):
    """exact decimal string of a terminating fraction (no trailing zeros)"""
    x = F(x); k = 0
    while (x * 10 ** k).denominator != 1:
        k += 1; assert k < 8, x
    n = x * 10 ** k; s = str(abs(n.numerator)).rjust(k + 1, "0")
    s = s[:len(s) - k] + ("." + s[len(s) - k:] if k else "")
    return s.rstrip("0").rstrip(".") if k else s
def pc(x): return dec(F(x) * 100) + "%"
def m(x):
    x = F(x); assert (x * 100).denominator == 1, x; return "€%d.%02d" % (x.numerator * 100 // x.denominator // 100, (x * 100).numerator % 100)
def fr(x): x = F(x); return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"
def P(p): return F(p) / 100
assert pc(F(3, 8)) == "37.5%" and dec(F(7, 100)) == "0.07" and m(F(576, 10)) == "€57.60" and fr(P(35)) == "7/20"

# ---------- free sheet ----------
A = [("Write 3/20 as a percentage.", pc(F(3, 20))), ("Write 0.07 as a percentage.", pc(F(7, 100))),
     ("Write 120% as a decimal.", dec(P(120))), ("Write 45% as a fraction in its simplest form.", fr(P(45))),
     ("Write 5/8 as a percentage.", pc(F(5, 8))),
     ("Put in order, smallest first: 0.3, 2/5, 33%, 0.35", ", ".join(sorted(["0.3", "2/5", "33%", "0.35"], key=lambda s: F(s.rstrip("%")) / (100 if "%" in s else 1))))]
assert [a for q, a in A] == ["15%", "7%", "1.2", "9/20", "62.5%", "0.3, 33%, 0.35, 2/5"], [a for q, a in A]
Bq = [(10, 340), (5, 340), (15, 340), (25, 64), (75, 64), (1, 850), (35, 80), (12, 250)]
B = [(f"{p}% of {q}", dec(P(p) * q)) for p, q in Bq]
assert [a for q, a in B] == ["34", "17", "51", "16", "48", "8.5", "28", "30"], [a for q, a in B]
Cq = [("Decrease €60 by 20%", F(60) * P(80)), ("Increase €40 by 15%", F(40) * P(115)), ("Decrease €250 by 8%", F(250) * P(92)),
      ("Increase €75 by 4%", F(75) * P(104)), ("To increase by 6%, multiply by…", P(106)), ("To decrease by 35%, multiply by…", P(65)),
      ("A €36 top is in a 25% off sale. Sale price?", F(36) * P(75)), ("€1,200 rent goes up by 2.5%. New rent?", F(1200) * P(F(205, 2)))]
def cans(q, v): return dec(v) if "multiply" in q else m(v)
assert [cans(q, v) for q, v in Cq] == ["€48.00", "€46.00", "€230.00", "€78.00", "1.06", "0.65", "€27.00", "€1230.00"], [cans(q, v) for q, v in Cq]
Dq = [("Aoife got 42 out of 60 in a test. What percentage is that?", pc(F(42, 60))),
      ("18 of the 24 students in a class have a phone. What percentage is that?", pc(F(18, 24))),
      ("Write €45 as a percentage of €180.", pc(F(45, 180))),
      ("Write 350 g as a percentage of 2 kg.", pc(F(350, 2000))),
      ("A price goes from €80 to €92. Find the percentage increase.", pc(F(92 - 80, 80))),
      ("A price goes from €250 to €200. Find the percentage decrease.", pc(F(250 - 200, 250))),
      ("After 30% off, a coat costs €84. What was the original price?", m(F(84) / P(70))),
      ("30% of a number is 27. What is the number?", dec(F(27) / P(30)))]
assert [a for q, a in Dq] == ["70%", "75%", "25%", "17.5%", "15%", "20%", "€120.00", "90"], [a for q, a in Dq]
# exam-style
walk, cyc = F(560) * P(45), F(560) / 4; bus = 560 - walk - cyc
assert (walk, cyc, bus, pc(bus / 560)) == (252, 140, 168, "30%")
shopA, shopB = F(95) * P(80), F(95) - 15; assert (shopA, shopB) == (76, 80)
back = (F(95) - shopA) / shopA; assert pc(back) == "25%"
tick = F(78) / P(120); slip = F(78) * P(80); assert tick == 65 and m(slip) == "€62.40"
s1 = F(400) * P(110) * P(90); assert s1 == 396
E = [("A school has 560 students. 45% walk to school, 1/4 cycle and the rest come by bus. (a) How many come by bus? (b) What percentage come by bus?",
      f"(a) 45% of 560 = 252; 1/4 of 560 = 140; bus 560 − 252 − 140 = <b>168</b> (b) 168/560 × 100 = <b>{pc(bus/560)}</b>"),
     ("A hoodie costs €95. Shop A takes 20% off. Shop B takes €15 off. (a) Which is cheaper, and by how much? (b) After the sale, Shop A puts its price back up to €95. Find the percentage increase.",
      f"(a) A: 0.8 × 95 = €76; B: €80. <b>Shop A, by €4</b> (b) 19 ÷ 76 × 100 = <b>{pc(back)}</b> (not 20%: it's worked out on €76)"),
     ("After a 20% increase, a ticket costs €78. (a) What did it cost before? (b) Why is 20% off €78 the wrong method?",
      f"(a) 120% = €78, 1% = €0.65, 100% = <b>€{tick}</b> (b) 0.8 × 78 = €62.40: the 20% was of the OLD price, not €78"),
     ("A €400 bike goes up by 10%, then the new price is cut by 10%. Is it back to €400? Explain.",
      f"400 × 1.1 = €440, then 440 × 0.9 = <b>€{s1}</b>. <b>No</b>: the 10% cut is 10% of €440, a bigger amount")]

def qs(items, start=0): return "".join(f"<li>{q} <span class='line'></span></li>" for q, a in items)

sheet = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Percentages: rules and practice | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>@page{{@bottom-left{{content:"Léim · leim.ie · Free to print for home or class · JC Maths LOs (2018 spec): {LO}"}}}}
.tight{{font-size:10.2pt;line-height:1.44}}.tight td,.tight th{{padding:3px 6px}}.tight h2{{margin:10px 0 5px;font-size:14pt}}.tight .note,.tight .tip{{padding:6px 10px;margin:6px 0}}
ol.q{{padding-left:30px}}ol.q li{{margin:7px 0}}.cols{{columns:2;column-gap:12mm}}.cols li{{break-inside:avoid}}
.ans td{{padding:3px 6px;font-size:9.4pt}}.eqt td,.eqt th{{text-align:center}}
</style></head><body>
<div class="page tight">
  <div class="band"><div><div class="k">Junior Cycle Maths · Free revision sheet</div><h1>Percentages</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2018 specification): {LO}. Play the game: <b>leim.ie/percent-pop.html</b></p>
  <div class="two">
   <div><h2>1. Percent = out of 100</h2>
    <p>45% = 45/100 = 0.45. <b>% → decimal:</b> ÷ 100 (7% = <b>0.07</b>, not 0.7). <b>Decimal → %:</b> × 100 (0.375 = 37.5%). <b>Fraction → %:</b> make the bottom 100, or divide and × 100 (3/20 = 15/100 = 15%). <b>% → fraction:</b> over 100, then simplify (35% = 7/20).</p>
    <table class="eqt"><thead><tr><th>Fraction</th><th>Decimal</th><th>%</th></tr></thead><tbody>
     {"".join(f"<tr><td>{fr(x)}</td><td>{dec(x)}</td><td>{pc(x)}</td></tr>" for x in [F(1,2),F(1,4),F(3,4),F(1,5),F(1,10),F(1,20),F(1,8)])}
     <tr><td>1/3</td><td>0.333…</td><td>33⅓%</td></tr></tbody></table>
    <h2>2. A percentage of an amount</h2>
    <p>Build it from <b>10%</b> (÷ 10), <b>5%</b> (half of 10%) and <b>1%</b> (÷ 100). 35% of €80: 10% = €8, 30% = €24, 5% = €4, so 35% = <b>€28</b>. Calculator: 0.35 × 80. Swap trick: 8% of 25 = 25% of 8 = <b>2</b>.</p>
    <h2>3. One amount as a % of another</h2>
    <p>Fraction × 100: 18 out of 24 = 18/24 × 100 = <b>75%</b>. Same units first (350 g of 2 kg = 350/2000).</p></div>
   <div><h2>4. Increase and decrease</h2>
    <table><thead><tr><th>Change</th><th>Multiply by</th></tr></thead><tbody>
     <tr><td>decrease by 20%</td><td><b>0.8</b> (you keep 80%)</td></tr><tr><td>increase by 15%</td><td><b>1.15</b> (115%)</td></tr>
     <tr><td>decrease by 4%</td><td><b>0.96</b></td></tr><tr><td>increase by 2.5%</td><td><b>1.025</b></td></tr></tbody></table>
    <h2>5. Percentage change</h2>
    <p>Change ÷ <b>original</b> × 100. €50 → €60: 10 ÷ 50 × 100 = <b>20% increase</b>. Always divide by the starting amount.</p>
    <h2>6. Back to the start</h2>
    <p>After 20% off, a jacket costs €48. €48 is <b>80%</b>, so 1% = €0.60 and 100% = <b>€60</b> (or 48 ÷ 0.8).</p>
    <div class="note"><b>Classic mistake:</b> adding 20% back on: 48 × 1.2 = €57.60, not €60. The 20% was of the OLD price. Ask: "which amount is 100%?"</div></div>
  </div>
  <div class="tip"><b>Exam tip:</b> show the step ("10% = €8, so 30% = €24") because it earns marks even if the last line slips. Money has 2 decimal places (€57.60). Check the answer makes sense: a sale price must be less than the old price.</div>
</div>

<div class="page">
  <div class="band"><div><div class="k">Practice · 34 questions</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <div class="two"><div><h2>A. Fractions, decimals, %</h2><ol class="q">{qs(A)}</ol></div>
  <div><h2>B. Percentage of (no calculator)</h2><ol class="q" start="7">{"".join(f"<li>{q} = <span class='line' style='min-width:80px'></span></li>" for q, a in B)}</ol></div></div>
  <h2>C. Increase and decrease</h2><ol class="q cols" start="15">{"".join(f"<li>{q} <span class='line' style='min-width:70px'></span></li>" for q, v in Cq)}</ol>
  <h2>D. As a percentage, percentage change, back to the start</h2><ol class="q" start="23">{"".join(f"<li>{q} <span class='line' style='min-width:70px'></span></li>" for q, a in Dq)}</ol>
  <p class="small" style="margin-top:6px">Questions 31–34 are on the next page.</p>
</div>

<div class="page">
  <div class="band"><div><div class="k">Exam-style · then check</div><h1>Exam corner + answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>E. Exam-style questions (show your work)</h2>
  <ol class="q" start="31">{"".join(f"<li>{q}<span class='long'></span><span class='long'></span></li>" for q,a in E)}</ol>
  <h2 style="margin-top:12px">Answers</h2>
  <table class="ans"><tbody>
   <tr><td><b>A</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(A,1))}</td></tr>
   <tr><td><b>B</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(B,7))}</td></tr>
   <tr><td><b>C</b></td><td>{" · ".join(f"{i}. {cans(q,v)}" for i,(q,v) in enumerate(Cq,15))}</td></tr>
   <tr><td><b>D</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(Dq,23))}</td></tr>
   <tr><td><b>E</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(E,31))}</td></tr>
  </tbody></table>
  <div class="note"><b>Got one wrong?</b> Check: did you ÷ 100 properly (7% = 0.07)? For a percentage change, did you divide by the <b>original</b>? For "the price before", did you find 1% first instead of adding the % back on? Then play <b>Percent Pop</b> at leim.ie/percent-pop.html: the "Go back over these" list at the end shows the rule for each mistake.</div>
  <p class="small">All questions written by Léim. Léim is independent and not connected with the State Examinations Commission or the NCCA.</p>
</div>
</body></html>"""

# ---------- teacher pack ----------
TRIO_VALS = [F(1, 4), F(3, 5), F(1, 8), F(7, 20), F(9, 10), F(3, 25), F(3, 2), F(1, 20)]
assert len(set(TRIO_VALS)) == 8
cards = []
for x in TRIO_VALS: cards += [fr(x), dec(x), pc(x)]
assert len(set(cards)) == 24
random.seed(6); trio_print = cards[:]; random.shuffle(trio_print)
trio_html = "".join(f'<div class="c"><span class="tag">Card {i}</span><div class="fc">{x}</div></div>' for i, x in enumerate(trio_print, 1))
trio_key = " · ".join(f"{fr(x)} = {dec(x)} = {pc(x)}" for x in TRIO_VALS)

# Sale Shop: same 5 items, two shops
ITEMS = ["Hoodie", "Runners", "Headphones", "Backpack", "Football"]
SA = [(60, ("p", 25)), (90, ("p", 30)), (75, ("p", 20)), (40, ("p", 15)), (24, ("p", 50))]   # Shop A: % off
SB = [(58, ("e", 10)), (80, ("e", 15)), (62, ("e", 4)), (38, ("e", 5)), (18, ("e", 4))]     # Shop B: € off
def final(price, d): return F(price) * P(100 - d[1]) if d[0] == "p" else F(price - d[1])
def dstr(d): return f"{d[1]}% off" if d[0] == "p" else f"€{d[1]} off"
SHOP = []
for it, (pa, da), (pb, db) in zip(ITEMS, SA, SB):
    fa, fb = final(pa, da), final(pb, db); assert fa != fb, it
    SHOP.append((it, pa, da, fa, pb, db, fb, "A" if fa < fb else "B", abs(fa - fb)))
assert [s[7] for s in SHOP] == ["A", "A", "B", "B", "A"], [s[7] for s in SHOP]
assert all(s[3] != s[6] for s in SHOP)
def shop_card(name, which):
    rows = "".join(f"<tr><td>{s[0]}</td><td>€{s[1] if which=='A' else s[4]}</td><td><b>{dstr(s[2] if which=='A' else s[5])}</b></td><td></td><td></td></tr>" for s in SHOP)
    return f"""<div class="idc"><h3>{name}</h3><table class="ss"><thead><tr><th>Item</th><th>Price</th><th>Sale</th><th>My sale price</th><th>Partner's sale price</th></tr></thead><tbody>{rows}</tbody></table></div>"""

DOMS = [("10% of 70", F(7)), ("25% of 48", F(12)), ("3/5 as a %", F(60)), ("0.035 as a %", F(35, 10)), ("15% of 60", F(9)),
        ("1/8 as a %", F(25, 2)), ("5% of 360", F(18)), ("× for +20%", F(12, 10)), ("€40 − 30%", F(28)), ("€50 + 10%", F(55)),
        ("24 out of 30 as a %", F(80)), ("€80 → €100: % up", F(25)), ("75% of 20", F(15)), ("2% of 50", F(1)), ("× for −45%", F(55, 100)),
        ("1% of 50", F(1, 2)), ("90% of 40", F(36)), ("14 is 20% of…", F(70)), ("€50 → €40: % down", F(20)), ("40% of 5", F(2))]
def show(clue, v):
    if "% up" in clue or "% down" in clue or "as a %" in clue: return dec(v) + "%"
    if clue.startswith("€"): return m(v)
    return dec(v)
# checks of each clue
chk = {"10% of 70": 7, "25% of 48": 12, "3/5 as a %": 60, "0.035 as a %": F(35, 10), "15% of 60": 9, "1/8 as a %": F(25, 2), "5% of 360": 18,
       "× for +20%": F(6, 5), "€40 − 30%": F(40) * P(70), "€50 + 10%": F(50) * P(110), "24 out of 30 as a %": F(24, 30) * 100,
       "€80 → €100: % up": F(20, 80) * 100, "75% of 20": 15, "2% of 50": 1, "× for −45%": P(55), "1% of 50": F(1, 2),
       "90% of 40": 36, "14 is 20% of…": F(14) / P(20), "€50 → €40: % down": F(10, 50) * 100, "40% of 5": 2}
for k, v in DOMS: assert chk[k] == v, k
assert len(set(show(k, v) for k, v in DOMS)) == 20, sorted(show(k, v) for k, v in DOMS)
random.seed(66); chain = DOMS[:]; random.shuffle(chain)
dom = [("START" if k == 0 else show(*chain[k - 1]), x[0]) for k, x in enumerate(chain)] + [(show(*chain[-1]), "FINISH")]
dom_print = dom[:]; random.shuffle(dom_print)
dom_html = "".join(f'<div class="dom"><div class="h l">{l}</div><div class="h r">{r}</div></div>' for l, r in dom_print)
chain_key = "".join(f"<li>{x} = <b>{show(x, v)}</b></li>" for x, v in chain)

ERR = [("6% as a decimal", "= 0.6", "÷ 100 moves the digits 2 places: <b>0.06</b>"),
       ("3/8 as a percentage", "= 38%", "3 ÷ 8 = 0.375, × 100: <b>37.5%</b>"),
       ("Increase €70 by 10%", "= €80", "Added 10 euro, not 10%. 10% of €70 = €7: <b>€77.00</b>"),
       ("€40 → €50: % increase", "= 20%", "Divided by the new price. 10 ÷ 40 × 100 = <b>25%</b>"),
       ("After 25% off it's €60. Old price?", "= €75", "Added 25% of €60 back on. €60 = 75%, so 1% = €0.80: <b>€80.00</b>"),
       ("To decrease by 15%, multiply by…", "= 0.15", "You keep 85%: <b>0.85</b>")]
assert dec(P(6)) == "0.06" and pc(F(3, 8)) == "37.5%" and F(70) * P(110) == 77 and pc(F(10, 40)) == "25%" and F(60) / P(75) == 80 and dec(P(85)) == "0.85"
w1 = F(48) * P(115); assert w1 == F(552, 10)
w2a = F(36, 120); assert pc(w2a) == "30%"
w3 = F(2400) * P(96) * P(96); assert m(w3) == "€2211.84"
w4 = F(34) / P(85); assert w4 == 40
w5 = F(240) * P(35); w5b = F(240) * P(25); assert (w5, w5b) == (84, 60)

pack = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Percentages Teacher Pack | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>
@page{{@bottom-left{{content:"Léim · leim.ie · Single-teacher licence · JC Maths LOs (2018 spec): {LO}";font-size:7pt}}}}
.proc td{{font-size:8.9pt;padding:3px 6px;line-height:1.32}}.proc td:first-child{{white-space:nowrap;font-weight:700;color:var(--green)}}
.p1 .note{{font-size:8.7pt;padding:6px 10px;line-height:1.35}}.p1 p{{font-size:9.5pt}}
.fym{{display:grid;grid-template-columns:repeat(4,1fr);margin-top:2mm}}
.fym .c{{border:2px dashed #9AA3AE;margin:-1px 0 0 -1px;height:15.5mm;position:relative;display:flex;align-items:center;justify-content:center}}
.fym .fc{{font-size:19pt;font-weight:800;text-align:center}}
.fym .tag{{position:absolute;top:1.2mm;left:3mm;font-size:6.5pt;color:var(--green);font-weight:800;text-transform:uppercase;letter-spacing:.04em}}
.idc{{border:2px dashed #9AA3AE;padding:3mm 4mm;margin-top:3mm}}.idc h3{{margin:0 0 2mm}}
.ss td,.ss th{{padding:2px 6px;font-size:9.2pt}}.ss td:nth-child(n+4){{width:21%}}
.doms{{display:grid;grid-template-columns:1fr 1fr;gap:2mm 6mm}}
.dom{{display:grid;grid-template-columns:1fr 1.6fr;border:2px dashed #9AA3AE;height:18.5mm}}
.dom .h{{display:flex;align-items:center;justify-content:center;text-align:center;padding:2mm;font-size:15pt;font-weight:800}}
.dom .r{{font-size:12.5pt}}
.dom .l{{background:var(--mist);border-right:2px solid var(--ink)}}
.poster{{height:255mm;border:6px solid var(--night);border-radius:18px;padding:10mm;display:flex;flex-direction:column;justify-content:space-between}}
.poster h1{{font-size:46pt;text-align:center}}.poster p{{font-size:14pt!important}}
.ops{{display:grid;grid-template-columns:1fr 1fr;gap:4mm}}.ops div{{border-radius:14px;padding:7mm 4mm;text-align:center;font-size:14pt;line-height:1.5}}.ops b{{display:block;font-size:22pt;font-weight:800;margin-bottom:1mm}}
.big3{{display:grid;grid-template-columns:1fr 1fr 1fr;text-align:center;font-size:30pt;font-weight:800}}.big3 span{{display:block;font-size:11pt;color:var(--muted);font-weight:700}}
.ws{{font-size:10pt;line-height:1.42}}.ws ol.q li{{margin:6px 0}}.ws .long{{height:22px}}
.eh td{{padding:5px 8px;font-size:9.8pt}}.eh td:first-child{{font-weight:700;width:30%}}.eh .gap{{display:block;border-bottom:1px solid #9AA3AE;height:16px}}
</style></head><body>

<div class="page p1">
  <div class="band"><div><div class="k">Junior Cycle Maths · Teacher pack</div><h1>Percentages</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2018 specification): {LO} (percentages run through every money, statistics and probability question; VAT, interest and tax come later under N.2c)</p>
  <div class="two">
    <div><h3>Aims</h3><p>By the end of the lesson students can switch between fractions, decimals and percentages, order them, find a percentage of an amount without a calculator, write one amount as a percentage of another, increase and decrease by a percentage using a multiplier, find a percentage change, and work back to the original amount.</p></div>
    <div><h3>In this pack</h3><p>p.1 Teacher notes · p.2 Percent Trios cards + Sale Shop A/B cards · p.3 Percentage Dominoes (cut-up) · p.4 Wall poster · p.5 Worksheet: Error Hunt + exam-style questions · p.6 Answers. Level: 1st year (Higher and Ordinary), or 3rd-year revision. Time: about 60 minutes. All questions are original.</p></div>
  </div>
  <h2 style="margin-top:8px">Procedure</h2>
  <table class="proc"><tbody>
    <tr><td>5 min</td><td><b>Lead-in: Which is bigger?</b> Board 3/8 and 38%. Hands up for each. Ask both sides why. Don't settle it yet.</td></tr>
    <tr><td>10 min</td><td><b>Percent Trios</b> (p.2 cards; one each, 24 cards = 8 trios). Students mingle and find the two people whose cards are worth the same as theirs (fraction, decimal, percentage). Trios stand in order from smallest to biggest. Feedback: how did you know 0.12 and 3/25 match? Revisit the lead-in (3/8 = 37.5%).</td></tr>
    <tr><td>8 min</td><td><b>Guided discovery: the swap trick.</b> Board 8% of 25, 12% of 50, 36% of 75. Pairs work them out, then swap the numbers (25% of 8…). What do they notice? Why does it always work (both are x × y ÷ 100)? Then build 35% of 80 from 10% and 5%.</td></tr>
    <tr><td>12 min</td><td><b>Sale Shop</b> (p.2, pairs: Student A gets Shop A, Student B gets Shop B; don't show your card). Each works out their own sale prices, then they ask each other ("How much are the runners in your shop?") and decide where to buy each item. Feedback: which deal type ("% off" or "€ off") is better for cheap items? For dear ones?</td></tr>
    <tr><td>10 min</td><td><b>Percentage Dominoes</b> (p.3), groups of 3–4. Start with START, work out the clue, find the domino with that answer on its left, and build the chain to FINISH. Answer chain below.</td></tr>
    <tr><td>12 min</td><td><b>Worksheet</b> (p.5). Error Hunt in pairs (find the mistake, name the rule, fix it), then the exam-style questions alone. Feedback on question 4: why can't you add 15% back on?</td></tr>
    <tr><td>3 min</td><td><b>Exit ticket.</b> 15% of €60, and the price before 10% off if it now costs €45 (€9; €50). Homework: play <b>Percent Pop</b> at leim.ie/percent-pop.html (Back to the start round) and copy three lines from the "Go back over these" list.</td></tr>
  </tbody></table>
  <div class="note"><b>Percent Trios key:</b> {trio_key}.<br>
  <b>Errors to look for:</b> 6% = 0.6 · 3/8 = 38% · "10% more" = add €10 · dividing by the new amount for a percentage change · adding the % back on to find an old price · multiplying by 0.15 to "take 15% off" · €46.5 instead of €46.50. <b>Support:</b> a 100-square grid on the desk and the 10% / 5% / 1% ladder. <b>Fast finishers:</b> a price goes up 10% then down 10%: is it back where it started? Which is better for the shopper, 20% off then 10% off, or 30% off?</div>
  <p class="small"><b>Domino answer chain</b> (START → FINISH):</p>
  <ol class="small" style="columns:3;column-gap:12px;font-size:7.8pt;line-height:1.35;margin:0;padding-left:16px">{chain_key}</ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">Cut up the cards · one shop card per student</div><h1>Percent Trios + Sale Shop</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.5pt;margin:0"><b>Percent Trios.</b> Cut out the 24 cards and give one to each student. Find the two people whose cards are worth the same as yours. (Fewer students? Take out whole trios.)</p>
  <div class="fym">{trio_html}</div>
  <p style="font-size:9.5pt;margin:4mm 0 0"><b>Sale Shop.</b> Work out the sale price of each item in your shop. Then ask your partner for their prices and tick the cheaper shop. No calculators!</p>
  {shop_card("Student A · Shop A: % off everything", "A")}
  {shop_card("Student B · Shop B: € off everything", "B")}
</div>

<div class="page">
  <div class="band"><div><div class="k">Groups of 3–4 · cut along the dashed lines</div><h1>Percentage Dominoes</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.5pt">Start with START. Work out the clue on the right, then find the domino with that answer on its left. Keep going until you reach FINISH. No calculators! ("× for +20%" means: what do you multiply by to increase by 20%?)</p>
  <div class="doms">{dom_html}</div>
</div>

<div class="page">
  <div class="poster">
    <h1>Percentages</h1>
    <div class="big3"><div>3/4<span>fraction</span></div><div>0.75<span>decimal</span></div><div>75%<span>percentage</span></div></div>
    <p style="text-align:center;font-size:12pt;margin:0"><b>% → decimal:</b> ÷ 100 (7% = 0.07) · <b>decimal → %:</b> × 100 · <b>fraction → %:</b> make the bottom 100</p>
    <div class="ops">
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>% of</b>10% = ÷ 10 · 5% = half of 10%<br>35% of 80 = 24 + 4 = 28<br>x% of y = y% of x</div>
      <div style="background:var(--green-soft)"><b>Up and down</b>−20%: × 0.8<br>+15%: × 1.15<br>−4%: × 0.96</div>
      <div style="background:var(--green-soft)"><b>% change</b>change ÷ ORIGINAL × 100<br>€50 → €60: 10 ÷ 50 = 20%</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Back to the start</b>After 20% off: €48 = 80%<br>1% = €0.60 → 100% = €60<br>NOT 48 × 1.2</div>
    </div>
    <p style="text-align:center;font-size:12pt;margin:0"><b>Money:</b> always 2 decimal places: €57.60</p>
    <p style="text-align:center;font-size:10pt;color:var(--muted)">Léim · leim.ie · Play Percent Pop: leim.ie/percent-pop.html</p>
  </div>
</div>

<div class="page ws">
  <div class="band"><div><div class="k">Worksheet</div><h1>Error Hunt + exam-style questions</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Error Hunt</h2>
  <p>Each answer has one mistake. Find it, say which rule was broken, and write the right answer.</p>
  <table class="eh"><thead><tr><th>Question</th><th>Student's answer</th><th>The mistake and the right answer</th></tr></thead><tbody>
  {"".join(f"<tr><td>{q}</td><td>{w}</td><td><span class='gap'></span><span class='gap'></span></td></tr>" for q,w,r in ERR)}
  </tbody></table>
  <h2>B. Exam-style questions (show all your work)</h2>
  <ol class="q">
    <li>A €48 concert ticket goes up by 15%. Find the new price.<span class="long"></span></li>
    <li>In a survey of 120 students, 36 said maths is their favourite subject. What percentage is that? Show it on a 100-square or a bar.<span class="long"></span><span class="long"></span></li>
    <li>A car worth €2,400 loses 4% of its value each year. Find its value after 2 years.<span class="long"></span><span class="long"></span></li>
    <li>After a 15% discount, a game costs €34. (a) Find the price before the discount. (b) Niamh says "34 × 1.15". What answer does she get and why is it wrong?<span class="long"></span><span class="long"></span></li>
    <li>Of the €240 Darragh earns in a month, he saves 35% and spends 25% on his phone and bus. How much is left for everything else?<span class="long"></span><span class="long"></span></li>
  </ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">For the teacher</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>Sale Shop</h2>
  <table><thead><tr><th>Item</th><th>Shop A</th><th>Shop B</th><th>Cheaper</th></tr></thead><tbody>
  {"".join(f"<tr><td>{s[0]}</td><td>€{s[1]} − {dstr(s[2])} = <b>{m(s[3])}</b></td><td>€{s[4]} − {dstr(s[5])} = <b>{m(s[6])}</b></td><td>Shop {s[7]} by {m(s[8])}</td></tr>" for s in SHOP)}
  </tbody></table>
  <h2>A. Error Hunt</h2>
  <table><tbody>{"".join(f"<tr><td style='width:32%'><b>{q}</b> {w}</td><td>{r}</td></tr>" for q,w,r in ERR)}</tbody></table>
  <h2>B. Exam-style questions</h2>
  <ol class="q">
    <li>48 × 1.15 = <b>{m(w1)}</b> (10% = €4.80, 5% = €2.40, so +€7.20)</li>
    <li>36/120 × 100 = <b>{pc(w2a)}</b> (30 squares shaded)</li>
    <li>2400 × 0.96 = €2,304; 2304 × 0.96 = <b>€2,211.84</b> (not €2,208: the second 4% is of €2,304)</li>
    <li>(a) €34 = 85%, 1% = €0.40, 100% = <b>€{w4}.00</b> (b) 34 × 1.15 = €39.10: the 15% was of the old price, not €34</li>
    <li>Saves 35% = €{w5}, spends 25% = €{w5b}; left: 240 − {w5} − {w5b} = <b>€{240-w5-w5b}.00</b> (or 40% of €240)</li>
  </ol>
  <h2>Marking tip</h2>
  <p>Give credit for each step, as the exam does: "10% = €4.80" written down earns marks even if the final line slips. Insist on 2 decimal places for money and on a sense check (a sale price is lower; an increase gives a bigger number).</p>
</div>
</body></html>"""
assert 2304 * F(96, 100) == F(221184, 100) and F(34) * P(115) == F(391, 10) and 240 - w5 - w5b == F(240) * P(40)

cover = """<!doctype html><html><head><meta charset="utf-8"><style>
body{margin:0;width:1200px;height:1200px;background:#1B2430;font-family:Inter,sans-serif;color:#fff;display:flex;flex-direction:column;justify-content:space-between;padding:90px;box-sizing:border-box}
.k{display:inline-block;background:#2E7D57;border-radius:99px;padding:12px 26px;font-weight:700;font-size:28px;letter-spacing:.06em;text-transform:uppercase}
h1{font-size:120px;font-weight:800;line-height:1.08;letter-spacing:-.03em;margin:40px 0 0}
h1 span{background:#F6CF5A;color:#1B2430;padding:0 14px}
.sub{font-size:38px;color:#C9D1DA;margin-top:36px;line-height:1.35}
.em{font-size:52px;margin-top:30px;font-weight:800;letter-spacing:.01em;color:#F6CF5A}
.foot{display:flex;justify-content:space-between;align-items:center;font-size:34px;font-weight:700}
.price{background:#F6CF5A;color:#1B2430;border-radius:16px;padding:14px 28px}
</style></head><body>
<div><span class="k">Junior Cycle Maths · Teacher pack</span>
<h1><span>Percentages</span></h1>
<div class="sub">Percent Trios · Sale Shop role-play<br>Percentage Dominoes · Poster · Worksheet + answers</div>
<div class="em">3/4 = 0.75 = 75% · €48 = 80% → €60</div></div>
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
    pdf("teacher-pack", os.path.join(OUT, "Percentages-Teacher-Pack-Leim.pdf"))
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--hide-scrollbars", "--window-size=1200,1200",
                    f"--screenshot={os.path.join(OUT, f'{SLUG}-cover.png')}", f"{SLUG}-cover.html"], cwd=SRC, check=True, capture_output=True)
    print("domino chain:", [(x, show(x, v)) for x, v in chain])
    print("shop:", [(s[0], m(s[3]), m(s[6]), s[7]) for s in SHOP])
