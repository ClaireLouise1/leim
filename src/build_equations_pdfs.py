#!/usr/bin/env python3
"""Linear equations (JC Maths topic 16): free sheet + teacher pack + Payhip cover.
Run from the repo root: python3 src/build_equations_pdfs.py OUTDIR   (needs: pip install --break-system-packages sympy)
Writes src/linear-equations-*.html; PDFs/cover PNG go to OUTDIR (free sheet also to printables/).
Every equation is solved with sympy and every answer asserted."""
import os, sys, random, subprocess, re
from fractions import Fraction
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC)
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/equations"; os.makedirs(OUT, exist_ok=True)
SLUG = "linear-equations"
LO = "AF.2c, AF.4, U.3"
TR = standard_transformations + (implicit_multiplication_application,)
x = sp.Symbol("x")

def E(s):
    s = s.replace("−", "-").replace("×", "*").replace("€", "")
    return parse_expr(s, local_dict={"x": x}, transformations=TR)
def S(eq):
    """the one solution of a linear equation written as text"""
    l, r = eq.split(" = ")
    v = sp.solve(sp.Eq(E(l), E(r)), x); assert len(v) == 1, (eq, v); return sp.Rational(v[0])
def chk(eq, a):
    v = S(eq); assert v == Fraction(str(a).replace("−", "-")), (eq, a, v); return a
def n(v): return ("−" + str(-v)) if v < 0 else str(v)
def lhs_rhs(eq, v):
    l, r = eq.split(" = "); return E(l).subs(x, v), E(r).subs(x, v)

INK, YEL, MINT = "#1B2430", "#F6CF5A", "#E9F5EE"
def bal(kL, mL, kR, mR, h="30mm"):
    """balance scales: bags (x) and single counters; same layout as the game"""
    PL = 190; o = ""
    def pan(k, m, cx):
        s = ""; rows = -(-m // 6)
        for i in range(m):
            r, c = divmod(i, 6); inrow = min(6, m - r * 6); x0 = cx - (inrow * 21 - 3) / 2 + c * 21; y = PL - 21 * (r + 1)
            s += f'<rect x="{x0}" y="{y}" width="18" height="18" rx="3" fill="{MINT}" stroke="{INK}" stroke-width="1.6"/><text x="{x0 + 9}" y="{y + 13.5}" font-size="11" text-anchor="middle">1</text>'
        for j in range(k):
            bx = cx - (k * 32 - 4) / 2 + j * 32; by = PL - 21 * rows - 40
            s += f'<path d="M{bx + 4} {by + 8} Q{bx + 14} {by - 1} {bx + 24} {by + 8} L{bx + 28} {by + 36} L{bx} {by + 36} Z" fill="{YEL}" stroke="{INK}" stroke-width="2"/><text x="{bx + 14}" y="{by + 28}" font-size="16" text-anchor="middle">x</text>'
        return s
    o = pan(kL, mL, 85) + pan(kR, mR, 255)
    o += f'<rect x="8" y="{PL}" width="324" height="8" rx="3" fill="{INK}"/><path d="M170 {PL + 8} L150 {PL + 38} L190 {PL + 38} Z" fill="#2E7D5B"/>'
    top = min(PL - 21 * -(-mL // 6) - (42 if kL else 0), PL - 21 * -(-mR // 6) - (42 if kR else 0)) - 8
    return f'<svg viewBox="0 {top} 340 {PL + 42 - top}" style="height:{h};width:auto"><g font-family="Inter,sans-serif" font-weight="800" fill="{INK}">{o}</g></svg>'

# ---------- free sheet ----------
A = [("x + 9 = 4", "−5"), ("x − 6 = 11", "17"), ("7x = 42", "6"), ("−3x = 18", "−6"),
     ("x/4 = 5", "20"), ("3x + 5 = 26", "7"), ("5x − 8 = 17", "5"), ("20 − 3x = 2", "6")]
B = [("5x + 2 = 3x + 14", "6"), ("7x − 4 = 2x + 21", "5"), ("4x + 9 = x − 3", "−4"), ("2x − 5 = 6x + 15", "−5"),
     ("3(x + 4) = 27", "5"), ("5(x − 2) = 3x + 4", "7"), ("4(x + 1) = 2(x + 7)", "5"), ("3(2x − 1) − 2(x + 3) = 11", "5")]
C = [("x/3 + 4 = 9", "15"), ("(x + 4)/5 = 3", "11"), ("x/2 − 3 = 5", "16"), ("(2x − 1)/3 = 5", "8"),
     ("x/2 + x/3 = 15", "18"), ("x/4 − x/6 = 2", "24"), ("(x + 3)/2 = (x + 9)/4", "3"), ("(x + 1)/3 + (x − 1)/2 = 4", "5")]
for grp in (A, B, C):
    for q, a in grp: chk(q, a)
# D: words — each with the equation we expect, solved and asserted
D = [("I think of a number, multiply it by 5 and subtract 3. The answer is 32. Find the number.", "5x − 3 = 32", "7", "7"),
     ("I think of a number, add 4, then double the result. The answer is 26. Find the number.", "2(x + 4) = 26", "9", "9"),
     ("Three consecutive whole numbers add up to 72. Find them.", "x + (x + 1) + (x + 2) = 72", "23", "23, 24, 25"),
     ("Aoife is 4 years older than Cian. Their ages add up to 30. How old is each?", "x + (x + 4) = 30", "13", "Cian 13, Aoife 17"),
     ("The angles of a triangle are x°, 2x° and (x + 40)°. Find x.", "x + 2x + (x + 40) = 180", "35", "35 (angles 35°, 70°, 75°)"),
     ("A rectangle is (x + 6) cm long and x cm wide. Its perimeter is 40 cm. Find x and the area.", "2(x + 6) + 2x = 40", "7", "x = 7; 13 cm × 7 cm = 91 cm²")]
for q, e, a, full in D: chk(e, a)
assert 23 + 24 + 25 == 72 and 13 + 17 == 30 and 35 + 70 + 75 == 180 and 13 * 7 == 91
EX = [("Solve 2(3x − 4) − (x − 3) = 3(x + 5).", chk("2(3x − 4) − (x − 3) = 3(x + 5)", "10"),
       "6x − 8 − x + 3 = 3x + 15 → 5x − 5 = 3x + 15 → 2x = 20 → <b>x = 10</b> (check: 45 = 45)"),
      ("A taxi charges €4 plus €2 for every km. (a) Write an expression for the cost of an x km trip. (b) Liam's trip cost €28. Write an equation and find how far he went.",
       chk("2x + 4 = 28", "12"), "(a) <b>2x + 4</b> (b) 2x + 4 = 28 → 2x = 24 → <b>12 km</b>"),
      ("Solve (x − 2)/3 − (x − 4)/5 = 2.", chk("(x − 2)/3 − (x − 4)/5 = 2", "14"),
       "× 15: 5(x − 2) − 3(x − 4) = 30 → 5x − 10 − 3x + 12 = 30 → 2x + 2 = 30 → <b>x = 14</b> (check: 4 − 2 = 2)"),
      ("Niamh has €x. Ciara has €15 more than Niamh, and Seán has twice as much as Niamh. Together they have €95. (a) Write an equation. (b) How much does each person have?",
       chk("x + (x + 15) + 2x = 95", "20"), "(a) <b>x + (x + 15) + 2x = 95</b> (b) 4x + 15 = 95 → x = 20: <b>Niamh €20, Ciara €35, Seán €40</b>")]
assert lhs_rhs("2(3x − 4) − (x − 3) = 3(x + 5)", 10) == (45, 45) and 20 + 35 + 40 == 95

def qs(items, k=0): return "".join(f"<li>{it[0] if k else it[0]} <span class='line'></span></li>" for it in items)
sheet = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Linear equations, rules and practice | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>@page{{@bottom-left{{content:"Léim · leim.ie · Free to print for home or class · JC Maths LOs (2018 spec): {LO}"}}}}
.tight{{font-size:11.9pt;line-height:1.55}}.tight td,.tight th{{padding:3px 6px}}.tight h2{{margin:15px 0 6px;font-size:15pt}}.tight .note,.tight .tip{{padding:6px 10px;margin:6px 0}}.tight p{{margin:3px 0}}
ol.q{{padding-left:30px}}ol.q li{{margin:7px 0}}
.ans td{{padding:3px 6px;font-size:9.2pt}}
.p2{{font-size:11.4pt;line-height:1.45}}.p2 ol.q li{{margin:15px 0}}.p2 h2{{margin:14px 0 6px;font-size:14pt}}.p2 .line{{min-width:70px}}
.wk{{line-height:1.6}}.wk i{{color:#5B6673;font-style:normal;font-size:9pt}}
.bl{{display:flex;gap:4mm;align-items:center}}
</style></head><body>
<div class="page tight">
  <div class="band"><div><div class="k">Junior Cycle Maths · Free revision sheet</div><h1>Linear equations</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2018 specification): {LO}. Play the game: <b>leim.ie/balance-it.html</b></p>
  <div class="two">
   <div><h2>1. Keep it balanced</h2>
    <div class="bl">{bal(3, 2, 0, 14, "30mm")}<p>3x + 2 = 14<br>"=" means both sides have the <b>same value</b>. Do the <b>same thing to both sides</b> and it stays balanced.</p></div>
    <h2>2. Undo, last thing first</h2>
    <p class="wk"><b>4x − 7 = 21</b><br>4x = 28 <i>(+7 both sides)</i><br>x = 7 <i>(÷4 both sides)</i><br>Check: 4(7) − 7 = 21 ✓</p>
    <p>+ undoes −, × undoes ÷: x + 9 = 4 → x = −5; −3x = 18 → x = −6; x/4 = 5 → x = 20.</p>
    <h2>3. Letters on both sides</h2>
    <p class="wk"><b>5x + 3 = 2x + 18</b><br>3x + 3 = 18 <i>(−2x both sides)</i><br>3x = 15 → x = 5</p>
    <p>A term that moves across the = changes its sign.</p>
    <h2>4. Brackets: expand first</h2>
    <p class="wk"><b>3(x − 4) = 2(x + 1)</b><br>3x − 12 = 2x + 2 → x = 14</p></div>
   <div><h2>5. Fractions: clear them first</h2>
    <p>Multiply <b>every term</b> by the LCM of the bottom numbers.</p>
    <p class="wk"><b>x/2 + x/3 = 10</b> <i>(LCM 6)</i><br>3x + 2x = 60 → 5x = 60 → x = 12</p>
    <p class="wk"><b>(x + 2)/5 = 3</b> → x + 2 = 15 → x = 13</p>
    <p>Don't forget the number on its own: the 10 becomes 60.</p>
    <h2>6. Equations from words</h2>
    <p>Say what x stands for, write the other amounts using x, find what is equal, solve, then answer in words.</p>
    <p class="wk">"I think of a number, multiply it by 4 and add 7. The answer is 31."<br>4x + 7 = 31 → 4x = 24 → x = 6</p>
    <p>Consecutive numbers: x, x + 1, x + 2 · angles in a triangle: 180° · perimeter: add all the sides.</p>
    <h2>7. Always check</h2>
    <p>Put your answer into the <b>original</b> equation: both sides must give the same number.</p></div>
  </div>
  <div class="tip"><b>Exam tip:</b> show every step on its own line (method marks), do the same to both sides and to <b>every</b> term, and watch the signs when you expand a bracket or move a term. In word problems, say what x is and answer with units.</div>
</div>

<div class="page p2">
  <div class="band"><div><div class="k">Practice · 34 questions</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <div class="two"><div><h2>A. One and two steps</h2><ol class="q">{qs(A)}</ol></div>
  <div><h2>B. Letters on both sides, brackets</h2><ol class="q" start="9">{qs(B)}</ol></div></div>
  <div class="two"><div><h2>C. Fractions</h2><ol class="q" start="17">{qs(C)}</ol></div>
  <div><h2>D. From words (write an equation first)</h2><ol class="q" start="25">{"".join(f"<li>{q} <span class='line'></span></li>" for q, e, a, f in D)}</ol></div></div>
  <p class="small" style="margin-top:6px">Questions 31–34 are on the next page.</p>
</div>

<div class="page">
  <div class="band"><div><div class="k">Exam-style · then check</div><h1>Exam corner + answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>E. Exam-style questions (show your work)</h2>
  <ol class="q" start="31">{"".join(f"<li>{q}<span class='long'></span><span class='long'></span></li>" for q, a, w in EX)}</ol>
  <h2 style="margin-top:12px">Answers</h2>
  <table class="ans"><tbody>
   <tr><td><b>A</b></td><td>{" · ".join(f"{i}. x = {a}" for i, (q, a) in enumerate(A, 1))}</td></tr>
   <tr><td><b>B</b></td><td>{" · ".join(f"{i}. x = {a}" for i, (q, a) in enumerate(B, 9))}</td></tr>
   <tr><td><b>C</b></td><td>{" · ".join(f"{i}. x = {a}" for i, (q, a) in enumerate(C, 17))}</td></tr>
   <tr><td><b>D</b></td><td>{" · ".join(f"{i}. {e} → {f}" for i, (q, e, a, f) in enumerate(D, 25))}</td></tr>
   <tr><td><b>E</b></td><td>{" · ".join(f"{i}. {w}" for i, (q, a, w) in enumerate(EX, 31))}</td></tr>
  </tbody></table>
  <div class="note"><b>Got one wrong?</b> Put your answer back into the question: do both sides match? Did you do the same to <b>both</b> sides? Multiply <b>every</b> term in a bracket, and every term (the whole numbers too) when you clear fractions? Change the sign of a term that moved across the =? Then play <b>Balance It</b> at leim.ie/balance-it.html: the "Go back over these" list at the end shows the rule for each mistake.</div>
  <p class="small">All questions written by Léim. Léim is independent and not connected with the State Examinations Commission or the NCCA.</p>
</div>
</body></html>"""

# ---------- teacher pack ----------
# Equation Relay: each runner's p = the previous runner's answer
RELAY = {
 "A": [("Solve 4x − 7 = 13.", "4x − 7 = 13", "5"),
       ("Your number is p. Solve 3(x − p) = x + 7.", "3(x − p) = x + 7", "11"),
       ("Your number is p. Solve x/2 + p = 3x − 4.", "x/2 + p = 3x − 4", "6"),
       ("Your number is p. Solve (x + p)/5 = x − 6.", "(x + p)/5 = x − 6", "9")],
 "B": [("Solve 5x + 9 = 2x + 21.", "5x + 9 = 2x + 21", "4"),
       ("Your number is p. Solve 2(x + p) = 5x − 1.", "2(x + p) = 5x − 1", "3"),
       ("Your number is p. Solve x/p + x/2 = 10.", "x/p + x/2 = 10", "12"),
       ("Your number is p. Solve p − 2x = x − 3.", "p − 2x = x − 3", "5")]}
for k, steps in RELAY.items():
    p = None
    for q, e, a in steps:
        chk(e if p is None else e.replace("p", f"({p})"), a); p = a
# Word-to-Equation Match: 12 pairs (word card ↔ equation card)
MATCH = [("I think of a number, double it and add 5. I get 17.", "2x + 5 = 17", 6),
         ("I think of a number, add 5, then double it. I get 18.", "2(x + 5) = 18", 4),
         ("Five less than three times a number is 16.", "3x − 5 = 16", 7),
         ("A number divided by 3, plus 4, is 9.", "x/3 + 4 = 9", 15),
         ("Three consecutive numbers add up to 51.", "x + (x + 1) + (x + 2) = 51", 16),
         ("A rectangle is x cm wide and (x + 3) cm long. Its perimeter is 26 cm.", "2x + 2(x + 3) = 26", 5),
         ("The angles of a triangle are x°, x° and 80°.", "x + x + 80 = 180", 50),
         ("Tom is 3 years older than Ann (x). Their ages add up to 25.", "x + (x + 3) = 25", 11),
         ("4 pens at €x each and a €3 ruler cost €11.", "4x + 3 = 11", 2),
         ("4 times a number is the same as the number plus 27.", "4x = x + 27", 9),
         ("Half of a number is 7 less than the number.", "x/2 = x − 7", 14),
         ("Share €36 so that Bríd gets twice as much as Pól (x).", "x + 2x = 36", 12)]
for w, e, a in MATCH: chk(e, a)
eqs = [e for w, e, a in MATCH]
assert len(set(a for w, e, a in MATCH)) == 12 and len(set(eqs)) == 12  # different answers, so pairs can check themselves
cards = [w for w, e, a in MATCH] + eqs
random.seed(16); match_print = cards[:]; random.shuffle(match_print)
def fc(t): return f'<div class="fc{" sm" if len(t) > 22 else " md" if len(t) > 13 else ""}">{t}</div>'
match_html = "".join(f'<div class="c"><span class="tag">Card {i}</span>{fc(t)}</div>' for i, t in enumerate(match_print, 1))
num_of = {t: i for i, t in enumerate(match_print, 1)}
match_key = " · ".join(f"{num_of[w]} ↔ {num_of[e]} (x = {a})" for w, e, a in MATCH)

DOMS = [("Solve x + 7 = 6", "−1"), ("Solve 4x = 36", "9"), ("Solve x/5 = 3", "15"), ("Solve 2x − 1 = 13", "7"),
        ("Solve 3x + 8 = 2", "−2"), ("Solve 10 − x = −1", "11"), ("Solve 5x + 1 = 3x + 7", "3"), ("Solve 6x − 4 = 2x + 4", "2"),
        ("Solve x + 12 = 4x", "4"), ("Solve 2(x + 3) = 16", "5"), ("Solve 3(x − 1) = 2x + 7", "10"), ("Solve 4(x + 2) = 2(x + 12)", "8"),
        ("Solve x/2 + 3 = 9", "12"), ("Solve (x + 1)/2 = 7", "13"), ("Solve x/2 + x/3 = 5", "6"), ("Solve (x + 4)/2 = x − 5", "14"),
        ("Solve 7 − 2x = 17", "−5"), ("3 consecutive numbers add to 51. Smallest?", "16"), ("Think of a number, × 3, − 4: get 50", "18"), ("Solve x/4 − 1 = −2", "−4")]
for q, a in DOMS:
    if q.startswith("Solve "): chk(q[6:], a)
assert chk("x + (x + 1) + (x + 2) = 51", "16") and chk("3x − 4 = 50", "18")
ANS = [a for q, a in DOMS]; assert len(set(ANS)) == 20
random.seed(1616); chain = DOMS[:]; random.shuffle(chain)
dom = [("START" if k == 0 else chain[k - 1][1], c[0]) for k, c in enumerate(chain)] + [(chain[-1][1], "FINISH")]
dom_print = dom[:]; random.shuffle(dom_print)
def dclue(t): return t.replace("Solve ", "Solve<br>") if len(t) < 30 else t
dom_html = "".join(f'<div class="dom"><div class="h l">{l}</div><div class="h r{" sm" if len(r) > 26 else ""}">{dclue(r)}</div></div>' for l, r in dom_print)
chain_key = "".join(f"<li>{q} → <b>{a}</b></li>" for q, a in chain)

ERR = [("x + 8 = 3", "x = 3 + 8 = 11", "Subtract 8 from both sides: <b>x = −5</b>", "−5", "11"),
       ("4x = 20", "x = 20 − 4 = 16", "4x means 4 × x, so divide by 4: <b>x = 5</b>", "5", "16"),
       ("3(x − 2) = 12", "3x − 2 = 12, so x = 14/3", "The 3 multiplies both terms: 3x − 6 = 12, <b>x = 6</b>", "6", "14/3"),
       ("5x + 4 = 2x + 19", "7x = 15", "Subtract 2x (don't add it): 3x = 15, <b>x = 5</b>", "5", "15/7"),
       ("x/3 + 2 = 6", "x + 2 = 18, so x = 16", "Multiply EVERY term by 3: x + 6 = 18, <b>x = 12</b>", "12", "16"),
       ("−2x = 10", "x = 5", "Divide by −2: <b>x = −5</b>", "−5", "5")]
for q, w, r, good, bad in ERR:
    chk(q, good); assert S(q) != Fraction(bad.replace("−", "-"))
W = [("Solve 6x − 5 = 2x + 23.", chk("6x − 5 = 2x + 23", "7"), "4x − 5 = 23 → 4x = 28 → <b>x = 7</b> (check: 37 = 37)"),
     ("Solve 3(2x + 1) = 4(x + 3) + 1.", chk("3(2x + 1) = 4(x + 3) + 1", "5"), "6x + 3 = 4x + 13 → 2x = 10 → <b>x = 5</b> (check: 33 = 33)"),
     ("Solve (x + 1)/3 + (x + 3)/4 = 4.", chk("(x + 1)/3 + (x + 3)/4 = 4", "5"), "× 12: 4(x + 1) + 3(x + 3) = 48 → 7x + 13 = 48 → 7x = 35 → <b>x = 5</b> (check: 2 + 2 = 4)"),
     ("A school orders x boxes of pencils at €6 a box and (x + 4) boxes of pens at €4 a box. The bill is €116. (a) Write an equation. (b) How many boxes of each were ordered?",
      chk("6x + 4(x + 4) = 116", "10"), "(a) <b>6x + 4(x + 4) = 116</b> (b) 10x + 16 = 116 → x = 10: <b>10 boxes of pencils, 14 boxes of pens</b> (check: 60 + 56 = 116)"),
     ("Two angles on a straight line are (3x + 10)° and (x + 30)°. (a) Write an equation. (b) Find x and the size of each angle.",
      chk("(3x + 10) + (x + 30) = 180", "35"), "(a) <b>(3x + 10) + (x + 30) = 180</b> (b) 4x + 40 = 180 → x = 35: <b>115° and 65°</b>")]
assert lhs_rhs("6x − 5 = 2x + 23", 7) == (37, 37) and lhs_rhs("3(2x + 1) = 4(x + 3) + 1", 5) == (33, 33) and 60 + 56 == 116 and 115 + 65 == 180
EXIT = [chk("4(x − 1) = 2x + 6", "5"), chk("3x + 4 = 25", "7")]

pack_style = open(os.path.join(SRC, "build_ratio_pdfs.py"), encoding="utf-8").read()
pack_style = pack_style[pack_style.index("<style>", pack_style.index('pack = f"""')) + 7:pack_style.index("</style>", pack_style.index('pack = f"""'))]
pack_style = pack_style.replace("{{", "{").replace("}}", "}").replace("{LO}", LO)
pack_style += (".fym .c{height:24mm}.fym .fc.md{font-size:13pt}.fym .fc.sm{font-size:9.3pt}.trk{border:2px dashed #9AA3AE;padding:2.5mm 4mm;margin-top:2mm;font-size:9.6pt}.trk ol{margin:1mm 0 0;padding-left:18px}.trk li{margin:1.8mm 0}"
               ".relays{display:grid;grid-template-columns:1fr 1fr;gap:3mm}.dom .r{font-size:11pt}.dom .r.sm{font-size:9.6pt;line-height:1.25}.nw{white-space:nowrap}")
def nw(q): return re.sub(r"(Solve )(.+?)\.$", r'\1<span class="nw">\2</span>.', q)
pack = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Linear Equations Teacher Pack | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{pack_style}</style></head><body>

<div class="page p1">
  <div class="band"><div><div class="k">Junior Cycle Maths · Teacher pack</div><h1>Linear equations</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2018 specification): {LO} (simultaneous equations, quadratic equations and inequalities come later, AF.4)</p>
  <div class="two">
    <div><h3>Aims</h3><p>By the end of the lesson students understand "=" as balance; solve linear equations by doing the same to both sides, including letters on both sides, brackets and fractions; form an equation from words; and check a solution by substituting.</p></div>
    <div><h3>In this pack</h3><p>p.1 Teacher notes · p.2 Equation Relay + Word-to-Equation Match cards · p.3 Equation Dominoes (cut-up) · p.4 Wall poster · p.5 Worksheet: Error Hunt + exam-style questions · p.6 Answers. Level: 2nd year (Higher and Ordinary), or 3rd-year revision. Time: about 60 minutes. All questions are original.</p></div>
  </div>
  <h2 style="margin-top:8px">Procedure</h2>
  <table class="proc"><tbody>
    <tr><td>6 min</td><td><b>Lead-in: the scales.</b> Draw a balance with 3 bags + 2 counters on the left and 14 counters on the right (as on the poster). "Each bag holds the same number. How many?" Take suggestions; ask what moves keep it level. Write the moves as algebra: 3x + 2 = 14 → 3x = 12 → x = 4.</td></tr>
    <tr><td>8 min</td><td><b>Guided discovery.</b> Pairs solve 5x + 1 = 2x + 10 with the scales (take 2 bags off both sides first), then 3(x − 4) = 2(x + 1) and x/2 + x/3 = 10. What has to happen first each time? (Expand; clear the fractions by multiplying EVERY term by 6.) Check each answer by substituting.</td></tr>
    <tr><td>10 min</td><td><b>Word-to-Equation Match</b> (p.2, 24 cards = 12 pairs; one card each). Word cards find their equation; pairs then solve it and check in the words. Feedback: "double it and add 5" v "add 5, then double it": why are the equations different?</td></tr>
    <tr><td>10 min</td><td><b>Equation Relay</b> (p.2), teams of 4 in a line. Runner 1 solves and passes the answer (not the card) to runner 2, who uses it as p, and so on. The last runner brings the final number to you: if it's wrong, the team finds the broken step.</td></tr>
    <tr><td>10 min</td><td><b>Equation Dominoes</b> (p.3), groups of 3–4: start with START, solve the clue, find the domino with that answer on its left and build the chain to FINISH.</td></tr>
    <tr><td>13 min</td><td><b>Worksheet</b> (p.5). Error Hunt in pairs (find the mistake, name the rule, fix it), then the exam-style questions alone.</td></tr>
    <tr><td>3 min</td><td><b>Exit ticket.</b> Solve 4(x − 1) = 2x + 6; "I think of a number, multiply it by 3 and add 4. The answer is 25." (x = {EXIT[0]}; {EXIT[1]}). Homework: play <b>Balance It</b> at leim.ie/balance-it.html (From words and Check &amp; fix rounds) and copy three lines from the "Go back over these" list.</td></tr>
  </tbody></table>
  <div class="note"><b>Word-to-Equation Match key</b> (word card ↔ equation card): {match_key}.<br>
  <b>Errors to look for:</b> doing something to one side only · x + 8 = 3 → x = 11 · 4x = 20 → x = 16 · 3(x − 2) = 3x − 2 · moving a term without changing its sign · clearing fractions but not the whole number · −2x = 10 → x = 5. <b>Support:</b> draw the scales; write the move ("−2 both sides") beside each line; check by substituting. <b>Fast finishers:</b> make up a "think of a number" puzzle whose answer is −3 and swap with a partner.</div>
  <p class="small"><b>Equation Relay answers:</b> A: {" → ".join(a for q, e, a in RELAY["A"])} · B: {" → ".join(a for q, e, a in RELAY["B"])}. <b>Domino answer chain</b> (START → FINISH):</p>
  <ol class="small" style="columns:2;column-gap:12px;font-size:7.6pt;line-height:1.3;margin:0;padding-left:16px">{chain_key}</ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">One relay per team of 4 · one match card per student</div><h1>Equation Relay + Match cards</h1></div><div class="logo">↗ Léim</div></div>
  <div class="relays">{"".join(f'<div class="trk"><b>Equation Relay {k}.</b> Cut into 4 strips. Runners 2–4: p is the answer passed to you.<ol>' + "".join(f"<li><b>Runner {i}:</b> {nw(q)}</li>" for i, (q, e, a) in enumerate(st, 1)) + "</ol></div>" for k, st in RELAY.items())}</div>
  <p style="font-size:9.5pt;margin:3mm 0 0"><b>Word-to-Equation Match.</b> Cut out the 24 cards and give one to each student. Word card? Find the person with your equation. Equation card? Find the words that match it. Then solve it together and check the answer in the words. (Fewer students? Take out whole pairs.)</p>
  <div class="fym">{match_html}</div>
</div>

<div class="page">
  <div class="band"><div><div class="k">Groups of 3–4 · cut along the dashed lines</div><h1>Equation Dominoes</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.5pt">Start with START. Solve the clue on the right, then find the domino with that answer on its left. Keep going until you reach FINISH. No calculators!</p>
  <div class="doms">{dom_html}</div>
</div>

<div class="page">
  <div class="poster">
    <h1>Keep it balanced</h1>
    <div style="display:flex;justify-content:center;align-items:center;gap:8mm">{bal(3, 2, 0, 14, "46mm")}<div style="font-size:19pt;font-weight:800;line-height:1.55;white-space:nowrap">3x + 2 = 14<br><span style="color:#5B6673;font-size:12pt">−2 both sides</span><br>3x = 12<br><span style="color:#5B6673;font-size:12pt">÷3 both sides</span><br>x = 4</div></div>
    <p style="text-align:center;font-size:17pt!important;margin:0"><b>Whatever you do to one side, do to the other.</b></p>
    <div class="ops">
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Undo</b>+ ↔ − &nbsp; × ↔ ÷<br>last thing first</div>
      <div style="background:var(--green-soft)"><b>Both sides</b>x terms to one side<br>numbers to the other</div>
      <div style="background:var(--green-soft)"><b>Brackets</b>expand first<br>3(x − 4) = 3x − 12</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Fractions</b>× the LCM<br>EVERY term</div>
    </div>
    <p style="text-align:center;font-size:13pt;margin:0"><b>Check:</b> put your answer back in. Both sides must match.</p>
    <p style="text-align:center;font-size:10pt;color:var(--muted)">Léim · leim.ie · Play Balance It: leim.ie/balance-it.html</p>
  </div>
</div>

<div class="page ws">
  <div class="band"><div><div class="k">Worksheet</div><h1>Error Hunt + exam-style questions</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Error Hunt</h2>
  <p>Each answer has one mistake. Find it, say which rule was broken, and write the right answer. Check it by substituting.</p>
  <table class="eh"><thead><tr><th>Equation</th><th>Student's working</th><th>The mistake and the right answer</th></tr></thead><tbody>
  {"".join(f"<tr><td>{q}</td><td>{w}</td><td><span class='gap'></span><span class='gap'></span></td></tr>" for q, w, r, g, b in ERR)}
  </tbody></table>
  <h2>B. Exam-style questions (show all your work)</h2>
  <ol class="q">{"".join(f"<li>{q}<span class='long'></span>{'<span class=long></span>' if len(q) > 60 else ''}</li>" for q, a, w in W)}</ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">For the teacher</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>Equation Relay</h2>
  <ol class="q">
    <li><b>Relay A:</b> {" → ".join(a for q, e, a in RELAY["A"])} (last step: (x + 6)/5 = x − 6 → x + 6 = 5x − 30 → x = 9)</li>
    <li><b>Relay B:</b> {" → ".join(a for q, e, a in RELAY["B"])} (last step: 12 − 2x = x − 3 → 15 = 3x → x = 5)</li>
  </ol>
  <h2>Word-to-Equation Match</h2>
  <p style="font-size:9.4pt">{" · ".join(f"{w} → <b>{e}</b>, x = {a}" for w, e, a in MATCH)}</p>
  <h2>A. Error Hunt</h2>
  <table><tbody>{"".join(f"<tr><td style='width:34%'><b>{q}</b>: {w}</td><td>{r}</td></tr>" for q, w, r, g, b in ERR)}</tbody></table>
  <h2>B. Exam-style questions</h2>
  <ol class="q">{"".join(f"<li>{w}</li>" for q, a, w in W)}</ol>
  <h2>Marking tip</h2>
  <p>Give credit for each correct step, as the exam does: a correct equation from the words earns marks even if the solving slips, and a correct method carried through after an early slip still earns method marks. Expect students to check their answer by substituting.</p>
</div>
</body></html>"""

cover = """<!doctype html><html><head><meta charset="utf-8"><style>
body{margin:0;width:1200px;height:1200px;background:#1B2430;font-family:Inter,sans-serif;color:#fff;display:flex;flex-direction:column;justify-content:space-between;padding:90px;box-sizing:border-box}
.k{display:inline-block;background:#2E7D57;border-radius:99px;padding:12px 26px;font-weight:700;font-size:28px;letter-spacing:.06em;text-transform:uppercase}
h1{font-size:112px;font-weight:800;line-height:1.12;letter-spacing:-.03em;margin:40px 0 0}
h1 span{background:#F6CF5A;color:#1B2430;padding:0 14px;box-decoration-break:clone;-webkit-box-decoration-break:clone}
.sub{font-size:38px;color:#C9D1DA;margin-top:36px;line-height:1.35}
.em{font-size:50px;margin-top:30px;font-weight:800;letter-spacing:.01em;color:#F6CF5A}
.foot{display:flex;justify-content:space-between;align-items:center;font-size:34px;font-weight:700}
.price{background:#F6CF5A;color:#1B2430;border-radius:16px;padding:14px 28px}
</style></head><body>
<div><span class="k">Junior Cycle Maths · Teacher pack</span>
<h1><span>Linear</span><br><span>Equations</span></h1>
<div class="sub">Equation Relay · Word-to-Equation Match<br>Equation Dominoes · Poster · Worksheet + answers</div>
<div class="em">3x + 2 = 14 &nbsp;→&nbsp; 3x = 12 &nbsp;→&nbsp; x = 4</div></div>
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
    pdf("teacher-pack", os.path.join(OUT, "Linear-Equations-Teacher-Pack-Leim.pdf"))
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--hide-scrollbars", "--window-size=1200,1200",
                    f"--screenshot={os.path.join(OUT, f'{SLUG}-cover.png')}", f"{SLUG}-cover.html"], cwd=SRC, check=True, capture_output=True)
    print("domino chain:", chain)
