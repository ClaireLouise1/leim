#!/usr/bin/env python3
"""Fractions (JC Maths topic 3): free sheet + teacher pack + Payhip cover.
Run from the repo root: python3 src/build_fractions_pdfs.py OUTDIR
Writes src/fractions-*.html; PDFs/cover PNG go to OUTDIR (free sheet also to printables/).
Every answer is computed with Python's Fraction and asserted."""
import os, sys, random, subprocess, re
from fractions import Fraction as Fr
from math import lcm
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC)
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/fractions"; os.makedirs(OUT, exist_ok=True)
SLUG = "fractions"
LO = "N.1a, N.1b, N.2a"

def P(s):
    """parse '3/4', '2 1/3', '5'"""
    s = s.strip(); m = re.fullmatch(r"(\d+) (\d+)/(\d+)", s)
    if m: return int(m[1]) + Fr(int(m[2]), int(m[3]))
    return Fr(s)
def mx(f):
    f = Fr(f)
    if f.denominator == 1: return str(f.numerator)
    w, r = divmod(f.numerator, f.denominator)
    return (f"{w} " if w else "") + f"{r}/{f.denominator}"
def ev(expr):
    """evaluate 'a op b' with fractions/mixed numbers (ops + − × ÷ of)"""
    for op in [" + ", " − ", " × ", " ÷ ", " of "]:
        if op in expr:
            a, b = expr.split(op); a, b = P(a), P(b.replace("€", ""))
            return {" + ": a + b, " − ": a - b, " × ": a * b, " ÷ ": a / b, " of ": a * b}[op]
    raise ValueError(expr)

GREEN, INK = "#2E7D57", "#1B2430"
def bar(d, on, h=9, w=60, unit="mm"):
    cw = 300 / d
    r = "".join(f'<rect x="{i*cw:.2f}" y="0" width="{cw:.2f}" height="40" fill="{GREEN if i in on else "#fff"}" stroke="{INK}" stroke-width="2.5"/>' for i in range(d))
    return f'<svg viewBox="-3 -3 306 46" style="height:{h}{unit};width:auto;vertical-align:middle" xmlns="http://www.w3.org/2000/svg">{r}</svg>'
def pie(d, on, h=20):
    import math
    o = ""
    for i in range(d):
        a1, a2 = 2*math.pi*i/d - math.pi/2, 2*math.pi*(i+1)/d - math.pi/2
        o += f'<path d="M50 50 L{50+48*math.cos(a1):.2f} {50+48*math.sin(a1):.2f} A48 48 0 0 1 {50+48*math.cos(a2):.2f} {50+48*math.sin(a2):.2f} Z" fill="{GREEN if i in on else "#fff"}" stroke="{INK}" stroke-width="2.5"/>'
    return f'<svg viewBox="0 0 100 100" style="height:{h}mm;width:auto" xmlns="http://www.w3.org/2000/svg">{o}</svg>'
def grid(r, c, on, h=18):
    o = "".join(f'<rect x="{(i%c)*30}" y="{(i//c)*30}" width="30" height="30" fill="{GREEN if i in on else "#fff"}" stroke="{INK}" stroke-width="2.5"/>' for i in range(r*c))
    return f'<svg viewBox="-2 -2 {c*30+4} {r*30+4}" style="height:{h}mm;width:auto" xmlns="http://www.w3.org/2000/svg">{o}</svg>'
def wall(height_mm=78, rows=(1, 2, 3, 4, 5, 6, 8, 10, 12), labels=True):
    rh, W, o = 40, 600, ""
    for k, d in enumerate(rows):
        cw = W / d
        fill = ["#1B2430", "#2E7D57", "#4E9C76", "#F6CF5A", "#F3E3B0", "#E7F3EC", "#C9D1DA", "#FFFFFF", "#F7F1E1"][k % 9]
        txt = "#fff" if k < 3 else INK
        for i in range(d):
            o += f'<rect x="{i*cw:.2f}" y="{k*rh}" width="{cw:.2f}" height="{rh}" fill="{fill}" stroke="{INK}" stroke-width="2"/>'
            if labels: o += f'<text x="{i*cw+cw/2:.2f}" y="{k*rh+26}" font-size="{18 if d < 10 else 14}" font-weight="800" text-anchor="middle" fill="{txt}">{"1" if d == 1 else f"1/{d}"}</text>'
    return f'<svg viewBox="-2 -2 {W+4} {len(rows)*rh+4}" style="height:{height_mm}mm;width:auto" xmlns="http://www.w3.org/2000/svg" font-family="Inter,sans-serif">{o}</svg>'

# ---------- free sheet ----------
A = [(f"What fraction of this bar is shaded? {bar(8, {0, 3, 5})}", "3/8"),
     (f"What fraction is shaded? Give it in its simplest form. {bar(10, {0, 1, 2, 3})}", mx(Fr(4, 10))),
     ("Write 18/24 in its simplest form.", mx(Fr(18, 24))), ("Write 35/50 in its simplest form.", mx(Fr(35, 50))),
     ("3/4 = ?/28. Find the missing number.", str(28 // 4 * 3)), ("Write two fractions equal to 2/5.", "e.g. 4/10, 6/15, 8/20")]
assert A[0][1] == "3/8" and A[1][1] == "2/5" and A[2][1] == "3/4" and A[3][1] == "7/10" and A[4][1] == "21" and Fr(3, 4) == Fr(21, 28)
B = [("Write 23/4 as a mixed number.", mx(Fr(23, 4))), ("Write 3 2/7 as an improper fraction.", f"{P('3 2/7').numerator}/7"),
     ("Write 41/6 as a mixed number.", mx(Fr(41, 6))), ("Write 4 3/8 as an improper fraction.", f"{P('4 3/8').numerator}/8"),
     ("Which is bigger, 5/6 or 7/9? Show how you know.", "5/6 (15/18 &gt; 14/18)"),
     ("Put in order, smallest first: 1/2, 3/8, 2/5, 5/12", ", ".join(sorted(["1/2", "3/8", "2/5", "5/12"], key=P))),
     ("What fraction of an hour is 20 minutes? (simplest form)", mx(Fr(20, 60))), ("Write 45 minutes as a fraction of 2 hours.", mx(Fr(45, 120)))]
assert [b[1] for b in B[:4]] == ["5 3/4", "23/7", "6 5/6", "35/8"] and Fr(5, 6) > Fr(7, 9) and B[5][1] == "3/8, 2/5, 5/12, 1/2" and B[6][1] == "1/3" and B[7][1] == "3/8"
Cq = ["2/7 + 3/7", "1/2 + 1/3", "3/4 + 1/6", "5/6 − 1/4", "7/8 − 2/3", "1 1/2 + 2 2/3", "3 1/4 − 1 2/3", "4 − 1 3/5"]
Dq = ["2/3 × 3/4", "5/6 × 9/10", "3/5 × 10", "3/4 ÷ 3/8", "2/3 ÷ 4", "2 1/2 × 1 1/5", "3 3/4 ÷ 1 1/4", "5/8 of 72"]
assert [mx(ev(x)) for x in Cq] == ["5/7", "5/6", "11/12", "7/12", "5/24", "4 1/6", "1 7/12", "2 2/5"], [mx(ev(x)) for x in Cq]
assert [mx(ev(x)) for x in Dq] == ["1/2", "3/4", "6", "2", "1/6", "3", "3", "45"], [mx(ev(x)) for x in Dq]
book = Fr(1, 4) * 60; jersey = Fr(2, 5) * (60 - book); none = 1 - Fr(2, 5) - Fr(1, 3); rice = P("1 2/3") * Fr(6, 4)
assert (book, jersey, 60 - book - jersey) == (15, 18, 27) and P("4 1/2") / Fr(3, 4) == 6 and none == Fr(4, 15) and none * 30 == 8 and rice == Fr(5, 2)
E = [("Cian gets €60 for his birthday. He spends 1/4 of it on a book and 2/5 of what is left on a jersey. How much money has he left?",
      f"Book €{book}, €{60-book} left, jersey €{jersey}, so <b>€{60-book-jersey}</b> left"),
     ("A plank is 4 1/2 m long. How many shelves, each 3/4 m long, can be cut from it?", f"4 1/2 ÷ 3/4 = 9/2 × 4/3 = <b>{P('4 1/2')/Fr(3,4)}</b> shelves"),
     ("In a class, 2/5 of the students play GAA, 1/3 play soccer and the rest don't play a sport. (a) What fraction don't play a sport? (b) There are 30 students. How many don't play a sport?",
      f"(a) 1 − 6/15 − 5/15 = <b>{mx(none)}</b> (b) {mx(none)} of 30 = <b>{none*30}</b>"),
     ("A recipe for 4 people uses 1 2/3 cups of rice. How much rice is needed for 6 people?", f"1 2/3 × 6/4 = 5/3 × 3/2 = <b>{mx(rice)} cups</b>")]

def qs(items): return "".join(f"<li>{q} <span class='line'></span></li>" for q, a in items)

sheet = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Fractions: rules and practice | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>@page{{@bottom-left{{content:"Léim · leim.ie · Free to print for home or class · JC Maths LOs (2018 spec): {LO}"}}}}
.tight{{font-size:10.4pt;line-height:1.46}}.tight td{{padding:3px 6px}}.tight h2{{margin:11px 0 5px;font-size:14pt}}.tight .note,.tight .tip{{padding:6px 10px;margin:6px 0}}
ol.q li{{margin:7px 0}}.cols{{columns:2;column-gap:12mm}}.cols li{{break-inside:avoid}}
.ans td{{padding:3px 6px;font-size:9.4pt}}
</style></head><body>
<div class="page tight">
  <div class="band"><div><div class="k">Junior Cycle Maths · Free revision sheet</div><h1>Fractions</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2018 specification): {LO}. Play the game: <b>leim.ie/fraction-match.html</b></p>
  <div class="two">
   <div><h2>1. Equivalent fractions</h2>
    <p>Multiply or divide the top and the bottom by the <b>same</b> number: 1/2 = 2/4 = 3/6 = 4/8. The pieces get smaller but there are more of them.</p>
    <p style="text-align:center">{bar(2, {0}, 7)} = {bar(4, {0, 1}, 7)} = {bar(8, {0, 1, 2, 3}, 7)}</p>
    <p><b>Simplest form:</b> divide top and bottom by their HCF. 12/18 → HCF 6 → <b>2/3</b>.</p>
    <h2>2. Mixed numbers</h2>
    <p>2 1/3 → 2 × 3 + 1 = 7 → <b>7/3</b>. Back again: 17/5 → 17 ÷ 5 = 3 rem 2 → <b>3 2/5</b>.</p>
    <h2>3. Comparing</h2>
    <p>Same bottom first, then compare the tops. 3/4 or 5/8? 3/4 = 6/8, so <b>3/4</b> is bigger.</p></div>
   <div><h2>4. Add and subtract</h2>
    <p><b>Same bottom:</b> add the tops, keep the bottom. 2/9 + 5/9 = 7/9.</p>
    <p><b>Different bottoms:</b> use the LCM. 1/3 + 1/4 = 4/12 + 3/12 = <b>7/12</b>.</p>
    <div class="note"><b>Never add the bottoms:</b> 1/2 + 1/3 is not 2/5. It's 3/6 + 2/6 = 5/6.</div>
    <p><b>Mixed numbers:</b> wholes, then fractions. 2 1/3 + 1 3/4 = 3 + 13/12 = <b>4 1/12</b>. If a subtraction won't go, use improper fractions: 3 1/5 − 1 3/5 = 16/5 − 8/5 = <b>1 3/5</b>.</p>
    <h2>5. Multiply and divide</h2>
    <table><tbody>
     <tr><td><b>×</b></td><td>tops × tops, bottoms × bottoms: 2/3 × 3/5 = 6/15 = 2/5</td></tr>
     <tr><td><b>÷</b></td><td>keep, change, flip: 3/4 ÷ 1/2 = 3/4 × 2/1 = 1 1/2</td></tr>
     <tr><td><b>of</b></td><td>÷ bottom, × top: 3/5 of 40 = 40 ÷ 5 × 3 = 24</td></tr>
    </tbody></table>
    <p>Mixed numbers? Change to improper fractions <b>first</b>.</p></div>
  </div>
  <div class="tip"><b>Exam tip:</b> show the common denominator (part marks!), finish in simplest form or as a mixed number if asked, and do a sense check: × a fraction less than 1 makes it smaller; ÷ makes it bigger. "2/5 <b>of what is left</b>" means of the remainder, not of the start.</div>
</div>

<div class="page">
  <div class="band"><div><div class="k">Practice · 34 questions</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <div class="two"><div><h2>A. Pictures and equivalent fractions</h2><ol class="q">{qs(A)}</ol></div>
  <div><h2>B. Mixed numbers and comparing</h2><ol class="q" start="7">{qs(B)}</ol></div></div>
  <h2>C. Add and subtract (simplest form or mixed numbers)</h2><ol class="q cols" start="15">{"".join(f"<li>{x} = <span class='line' style='min-width:80px'></span></li>" for x in Cq)}</ol>
  <h2>D. Multiply and divide</h2><ol class="q cols" start="23">{"".join(f"<li>{x} = <span class='line' style='min-width:80px'></span></li>" for x in Dq)}</ol>
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
   <tr><td><b>C</b></td><td>{" · ".join(f"{i}. {mx(ev(x))}" for i,x in enumerate(Cq,15))}</td></tr>
   <tr><td><b>D</b></td><td>{" · ".join(f"{i}. {mx(ev(x))}" for i,x in enumerate(Dq,23))}</td></tr>
   <tr><td><b>E</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(E,31))}</td></tr>
  </tbody></table>
  <div class="note"><b>Got one wrong?</b> Check: did you add the bottoms (never!)? Did you flip the second fraction when dividing? Did you change mixed numbers to improper fractions before × and ÷? Then play <b>Fraction Match</b> at leim.ie/fraction-match.html: the "Go back over these" list at the end shows the rule for each mistake.</div>
  <p class="small">All questions written by Léim. Léim is independent and not connected with the State Examinations Commission or the NCCA.</p>
</div>
</body></html>"""

# ---------- teacher pack ----------
# Find Your Match: 8 pairs (16 cards); each pair checked
FYM = [(bar(8, {0, 1, 2, 3, 4, 5}, 11), "3/4", Fr(6, 8)), (pie(6, {0, 1}, 20), "1/3", Fr(2, 6)), (grid(3, 4, set(range(8)), 18), "2/3", Fr(8, 12)),
       (bar(10, {0, 1, 2, 3}, 11), "2/5", Fr(4, 10)), ("11/4", "2 3/4", Fr(11, 4)), ("1/2 + 1/3", "5/6", ev("1/2 + 1/3")),
       ("3/4 of 20", "15", ev("3/4 of 20")), ("2/3 ÷ 1/6", "4", ev("2/3 ÷ 1/6"))]
for a, b, v in FYM: assert P(b) == v, (b, v)
cards = []
for k, (a, b, v) in enumerate(FYM):
    cards.append((f"{'ABCDEFGH'[k]}1", a)); cards.append((f"{'ABCDEFGH'[k]}2", b))
random.seed(3); order = cards[:]; random.shuffle(order)
fym_html = "".join(f'<div class="c"><span class="tag">Card {n}</span><div class="fc">{t}</div></div>' for n, t in order)
fym_key = " · ".join(f"{'ABCDEFGH'[k]}: {('picture' if a.startswith('<svg') else a)} = {b}" for k, (a, b, v) in enumerate(FYM))

# Dominoes: 20 clues, distinct answers
DOMS = ["1/2 + 1/4", "2/3 − 1/2", "3/5 × 1/3", "1/2 ÷ 1/4", "2/3 of 9", "1 1/2 + 1 1/4", "3/4 × 4/9", "5/6 − 1/3",
        "3/8 + 1/4", "3/4 ÷ 1/4", "1/3 + 1/12", "2 1/2 × 2", "9/10 − 1/2", "1 1/3 + 1 1/3", "4/5 × 5/6", "1/2 ÷ 2",
        "2/3 + 2/3", "3 − 1 1/4", "3/4 of 12", "5/6 ÷ 1/4"]
dv = [ev(x) for x in DOMS]
assert len(set(dv)) == 20, sorted(map(mx, dv))
random.seed(33)
chain = DOMS[:]; random.shuffle(chain)
dom = [("START" if k == 0 else mx(ev(chain[k - 1])), x) for k, x in enumerate(chain)] + [(mx(ev(chain[-1])), "FINISH")]
dom_print = dom[:]; random.shuffle(dom_print)
dom_html = "".join(f'<div class="dom"><div class="h l">{l}</div><div class="h r">{r}</div></div>' for l, r in dom_print)
chain_key = "".join(f"<li>{x} = <b>{mx(ev(x))}</b></li>" for x in chain)

ERR = [("1/2 + 1/3", "= 2/5", "Added the bottoms. Common denominator: 3/6 + 2/6 = <b>5/6</b>"),
       ("3/4 ÷ 1/2", "= 3/8", "Multiplied without flipping: 3/4 × 2/1 = 6/4 = <b>1 1/2</b>"),
       ("12/18 in simplest form", "= 6/9", "Not finished: divide by the HCF, 6 → <b>2/3</b>"),
       ("2 1/3 as an improper fraction", "= 5/3", "2 × 3 + 1 = 7 → <b>7/3</b>"),
       ("3 1/5 − 1 3/5", "= 2 2/5", "Took 1/5 from 3/5 the wrong way round. 16/5 − 8/5 = 8/5 = <b>1 3/5</b>"),
       ("2/5 of 30", "= 15", "Divided by 2. Divide by the bottom, times the top: 30 ÷ 5 × 2 = <b>12</b>")]
assert ev("1/2 + 1/3") == Fr(5, 6) and ev("3/4 ÷ 1/2") == Fr(3, 2) and Fr(12, 18) == Fr(2, 3) and P("2 1/3") == Fr(7, 3) and ev("3 1/5 − 1 3/5") == Fr(8, 5) and ev("2/5 of 30") == 12
W1 = [ev("4 1/6 − 2 3/4"), ev("1 3/5 × 2 1/2"), ev("2 2/3 ÷ 1 1/9")]
assert [mx(x) for x in W1] == ["1 5/12", "4", "2 2/5"], [mx(x) for x in W1]
ciara = 1 - Fr(1, 3) - Fr(2, 5); assert ciara == Fr(4, 15) and ciara * 3600 == 960 and Fr(1, 3) * 3600 == 1200 and Fr(2, 5) * 3600 == 1440
tank = Fr(5, 6) - Fr(3, 8); assert tank == Fr(11, 24) and 330 / tank == 720
assert Fr(4, 5) > Fr(7, 9) and Fr(7, 9) == Fr(35, 45) and Fr(4, 5) == Fr(36, 45) and 6 / Fr(2, 5) == 15

pack = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Fractions Teacher Pack | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>
@page{{@bottom-left{{content:"Léim · leim.ie · Single-teacher licence · JC Maths LOs (2018 spec): {LO}";font-size:7pt}}}}
.proc td{{font-size:8.9pt;padding:3px 6px;line-height:1.32}}.proc td:first-child{{white-space:nowrap;font-weight:700;color:var(--green)}}
.p1 .note{{font-size:8.7pt;padding:6px 10px;line-height:1.35}}.p1 p{{font-size:9.5pt}}
.wallq{{font-size:9.3pt;margin:2mm 0 0;padding-left:5mm}}.wallq li{{margin:1mm 0}}
.fym{{display:grid;grid-template-columns:repeat(4,1fr);margin-top:3mm}}
.fym .c{{border:2px dashed #9AA3AE;margin:-1px 0 0 -1px;height:30mm;position:relative;display:flex;align-items:center;justify-content:center}}
.fym .fc{{font-size:17pt;font-weight:800;text-align:center}}
.fym .tag{{position:absolute;top:1.5mm;left:3mm;font-size:6.8pt;color:var(--green);font-weight:800;text-transform:uppercase;letter-spacing:.04em}}
.doms{{display:grid;grid-template-columns:1fr 1fr;gap:2mm 6mm}}
.dom{{display:grid;grid-template-columns:1fr 1.6fr;border:2px dashed #9AA3AE;height:18.5mm}}
.dom .h{{display:flex;align-items:center;justify-content:center;text-align:center;padding:2mm;font-size:15pt;font-weight:800}}
.dom .r{{font-size:13pt}}
.dom .l{{background:var(--mist);border-right:2px solid var(--ink)}}
.poster{{height:255mm;border:6px solid var(--night);border-radius:18px;padding:10mm;display:flex;flex-direction:column;justify-content:space-between}}
.poster h1{{font-size:34pt;text-align:center}}
.ops{{display:grid;grid-template-columns:1fr 1fr;gap:4mm}}.ops div{{border-radius:14px;padding:4mm;text-align:center;font-size:11pt;line-height:1.4}}.ops b{{display:block;font-size:18pt;font-weight:800;margin-bottom:1mm}}
.ws{{font-size:10pt;line-height:1.42}}.ws ol.q li{{margin:6px 0}}.ws .long{{height:22px}}
.eh td{{padding:5px 8px;font-size:9.8pt}}.eh td:first-child{{font-weight:700;width:24%}}.eh .gap{{display:block;border-bottom:1px solid #9AA3AE;height:16px}}
</style></head><body>

<div class="page p1">
  <div class="band"><div><div class="k">Junior Cycle Maths · Teacher pack</div><h1>Fractions</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2018 specification): {LO} (fractions come back in ratio, probability and algebra)</p>
  <div class="two">
    <div><h3>Aims</h3><p>By the end of the lesson students can find and explain equivalent fractions, simplify using the HCF, switch between mixed numbers and improper fractions, compare fractions, and add, subtract, multiply and divide fractions and mixed numbers, including fractions of amounts and word problems.</p></div>
    <div><h3>In this pack</h3><p>p.1 Teacher notes · p.2 Fraction Wall + Find Your Match cards · p.3 Fraction Dominoes (cut-up) · p.4 Wall poster · p.5 Worksheet: Error Hunt + exam-style questions · p.6 Answers. Level: 1st year (Higher and Ordinary), or 3rd-year revision. Time: about 60 minutes. All questions are original.</p></div>
  </div>
  <h2 style="margin-top:8px">Procedure</h2>
  <table class="proc"><tbody>
    <tr><td>5 min</td><td><b>Lead-in: Fold it.</b> Each student folds a strip of paper in half, then in half again, then again. Shade half the strip. How many eighths is that? Quarters? Elicit <i>numerator</i>, <i>denominator</i>, <i>equivalent</i>.</td></tr>
    <tr><td>10 min</td><td><b>Guided discovery: the Fraction Wall</b> (p.2, one per student). Pairs answer the wall questions using only the wall (no rules given yet). Feedback: what do you do to the top and bottom to get an equivalent fraction? Why is 1/8 smaller than 1/6 even though 8 is bigger? Then board the rules from the poster (p.4): simplest form with the HCF, mixed ↔ improper.</td></tr>
    <tr><td>10 min</td><td><b>Find Your Match</b> (p.2, cut up; one card each, print twice for big classes). Students mingle, work out their card and find the partner card with the same value. Pairs stand together and explain their match to the class.</td></tr>
    <tr><td>5 min</td><td><b>Model the four operations</b> on the board with the poster: common denominators (LCM) for + and −; tops × tops for ×; keep, change, flip for ÷; improper first for mixed numbers. Ask: why does 1/2 + 1/3 = 2/5 have to be wrong? (2/5 is less than 1/2.)</td></tr>
    <tr><td>12 min</td><td><b>Fraction Dominoes</b> (p.3), groups of 3–4. Start with START, work out the clue, find the domino with that answer on its left and build the chain to FINISH. Answer chain below.</td></tr>
    <tr><td>15 min</td><td><b>Worksheet</b> (p.5). Error Hunt in pairs (find the mistake, name the rule, fix it), then the exam-style questions alone. Feedback on question 2: why is it "of what is left"?</td></tr>
    <tr><td>3 min</td><td><b>Exit ticket.</b> 2 3/4 + 1 2/3 and 3/5 ÷ 9/10 (4 5/12; 2/3). Homework: play <b>Fraction Match</b> at leim.ie/fraction-match.html (Exam mix round) and copy three lines from the "Go back over these" list.</td></tr>
  </tbody></table>
  <div class="note"><b>Find Your Match key:</b> {fym_key}.<br>
  <b>Errors to look for:</b> adding the bottoms (1/2 + 1/3 = 2/5) · finding a common denominator for × · forgetting to flip, or flipping the first fraction, for ÷ · multiplying the wholes and the fractions separately in mixed numbers · stopping before simplest form (6/9) · 2 1/3 = 5/3 · "of the rest" worked out on the whole amount · thinking 1/8 &gt; 1/6. <b>Support:</b> keep the Fraction Wall on the desk. <b>Fast finishers:</b> find a fraction exactly halfway between 1/3 and 1/2 (5/12); is there always one between any two fractions?</div>
  <p class="small"><b>Domino answer chain</b> (START → FINISH):</p>
  <ol class="small" style="columns:3;column-gap:12px;font-size:7.8pt;line-height:1.35;margin:0;padding-left:16px">{chain_key}</ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">Each student · then cut up the cards</div><h1>Fraction Wall + Find Your Match</h1></div><div class="logo">↗ Léim</div></div>
  <div style="display:grid;grid-template-columns:1.25fr 1fr;gap:5mm;align-items:start">
    <div>{wall(72)}</div>
    <div><p style="font-size:9.5pt;margin:0"><b>Use the wall to answer:</b></p>
    <ol class="wallq"><li>How many 1/6s make 1/2?</li><li>Find three fractions equal to 1/2.</li><li>Which is bigger, 2/3 or 3/4?</li><li>Find a fraction equal to 2/5 with 10 on the bottom.</li><li>Put 1/4, 1/3, 1/5 in order, smallest first. What do you notice?</li><li>What is 1/2 + 1/4? 1/3 + 1/6?</li><li>How many 1/12s fit into 2/3?</li></ol></div>
  </div>
  <p style="font-size:9.5pt;margin-top:4mm"><b>Find Your Match.</b> Cut out the cards. Work out your card, then find the person whose card has the same value.</p>
  <div class="fym">{fym_html}</div>
</div>

<div class="page">
  <div class="band"><div><div class="k">Groups of 3–4 · cut along the dashed lines</div><h1>Fraction Dominoes</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.5pt">Start with START. Work out the clue on the right (simplest form or a mixed number), then find the domino with that answer on its left. Keep going until you reach FINISH. No calculators!</p>
  <div class="doms">{dom_html}</div>
</div>

<div class="page">
  <div class="poster">
    <h1>Fractions</h1>
    <div style="text-align:center">{wall(92, rows=(1, 2, 3, 4, 6, 8, 12))}</div>
    <p style="text-align:center;font-size:12pt;margin:0"><b>Equivalent:</b> × or ÷ the top and bottom by the same number · <b>Simplest form:</b> ÷ by the HCF · <b>2 1/3 = 7/3</b> (2 × 3 + 1)</p>
    <div class="ops">
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>+ and −</b>Same bottom first (use the LCM)<br>1/3 + 1/4 = 4/12 + 3/12 = 7/12<br>Never add the bottoms!</div>
      <div style="background:var(--green-soft)"><b>×</b>Tops × tops, bottoms × bottoms<br>2/3 × 3/5 = 6/15 = 2/5</div>
      <div style="background:var(--green-soft)"><b>÷</b>Keep, change, flip<br>3/4 ÷ 1/2 = 3/4 × 2/1 = 1 1/2</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>of</b>÷ by the bottom, × by the top<br>3/5 of 40 = 40 ÷ 5 × 3 = 24</div>
    </div>
    <p style="text-align:center;font-size:12pt;margin:0"><b>Mixed numbers?</b> Change to improper fractions before × and ÷.</p>
    <p style="text-align:center;font-size:10pt;color:var(--muted)">Léim · leim.ie · Play Fraction Match: leim.ie/fraction-match.html</p>
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
    <li>Work out, giving each answer as a mixed number or a whole number: (a) 4 1/6 − 2 3/4 (b) 1 3/5 × 2 1/2 (c) 2 2/3 ÷ 1 1/9<span class="long"></span><span class="long"></span></li>
    <li>A prize of €3600 is shared. Áine gets 1/3, Brian gets 2/5 and Ciara gets the rest. (a) What fraction does Ciara get? (b) How much money does Ciara get?<span class="long"></span><span class="long"></span></li>
    <li>A water tank is 3/8 full. After 330 litres are added, it is 5/6 full. How many litres does the tank hold when it is full?<span class="long"></span><span class="long"></span></li>
    <li>Which is bigger, 7/9 or 4/5? Show how you decided.<span class="long"></span></li>
    <li>How many 2/5 kg bags of sugar can be filled from 6 kg?<span class="long"></span></li>
  </ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">For the teacher</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>Fraction Wall questions</h2>
  <p>1. 3 · 2. e.g. 2/4, 3/6, 4/8 (also 5/10, 6/12) · 3. 3/4 · 4. 4/10 · 5. 1/5, 1/4, 1/3: the bigger the bottom, the smaller the piece · 6. 3/4; 1/2 · 7. 8</p>
  <h2>A. Error Hunt</h2>
  <table><tbody>{"".join(f"<tr><td style='width:28%'><b>{q}</b></td><td>{r}</td></tr>" for q,w,r in ERR)}</tbody></table>
  <h2>B. Exam-style questions</h2>
  <ol class="q">
    <li>(a) 25/6 − 11/4 = 50/12 − 33/12 = 17/12 = <b>{mx(W1[0])}</b> (b) 8/5 × 5/2 = 40/10 = <b>{mx(W1[1])}</b> (c) 8/3 ÷ 10/9 = 8/3 × 9/10 = 72/30 = <b>{mx(W1[2])}</b></li>
    <li>(a) 1 − 5/15 − 6/15 = <b>{mx(ciara)}</b> (b) 3600 ÷ 15 × 4 = <b>€{ciara*3600}</b> (check: €1200 + €1440 + €960 = €3600)</li>
    <li>5/6 − 3/8 = 20/24 − 9/24 = 11/24 of the tank is 330 litres. 1/24 = 30 litres, so the tank holds <b>{330/tank} litres</b>.</li>
    <li>7/9 = 35/45 and 4/5 = 36/45, so <b>4/5</b> is bigger (just!).</li>
    <li>6 ÷ 2/5 = 6 × 5/2 = <b>{6/Fr(2,5)} bags</b>.</li>
  </ol>
  <h2>Marking tip</h2>
  <p>Give credit for each correct step, as the exam does: a correct common denominator or a correct flip with one arithmetic slip should still earn most of the marks. Insist on a sense check: is the answer bigger or smaller than they expected?</p>
</div>
</body></html>"""

cover = """<!doctype html><html><head><meta charset="utf-8"><style>
body{margin:0;width:1200px;height:1200px;background:#1B2430;font-family:Inter,sans-serif;color:#fff;display:flex;flex-direction:column;justify-content:space-between;padding:90px;box-sizing:border-box}
.k{display:inline-block;background:#2E7D57;border-radius:99px;padding:12px 26px;font-weight:700;font-size:28px;letter-spacing:.06em;text-transform:uppercase}
h1{font-size:140px;font-weight:800;line-height:1;letter-spacing:-.03em;margin:40px 0 0}
h1 span{background:#F6CF5A;color:#1B2430;padding:0 14px}
.sub{font-size:38px;color:#C9D1DA;margin-top:36px;line-height:1.35}
.em{font-size:56px;margin-top:30px;font-weight:800;letter-spacing:.01em;color:#F6CF5A}
.foot{display:flex;justify-content:space-between;align-items:center;font-size:34px;font-weight:700}
.price{background:#F6CF5A;color:#1B2430;border-radius:16px;padding:14px 28px}
</style></head><body>
<div><span class="k">Junior Cycle Maths · Teacher pack</span>
<h1><span>Fractions</span></h1>
<div class="sub">Fraction Wall + Find Your Match<br>Fraction Dominoes · Poster · Worksheet + answers</div>
<div class="em">1/2 + 1/3 = 5/6 · keep, change, flip</div></div>
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
    pdf("teacher-pack", os.path.join(OUT, "Fractions-Teacher-Pack-Leim.pdf"))
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--hide-scrollbars", "--window-size=1200,1200",
                    f"--screenshot={os.path.join(OUT, f'{SLUG}-cover.png')}", f"{SLUG}-cover.html"], cwd=SRC, check=True, capture_output=True)
    print("domino chain:", [(x, mx(ev(x))) for x in chain])
