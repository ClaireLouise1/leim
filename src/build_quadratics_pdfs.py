#!/usr/bin/env python3
"""Quadratic equations (JC Maths topic 30): free sheet + teacher pack + Payhip cover.
Run from the repo root: python3 src/build_quadratics_pdfs.py OUTDIR
Writes src/quadratic-equations-*.html; PDFs/cover PNG go to OUTDIR (free sheet also to printables/).
Every equation is parsed back with sympy and its roots asserted.
Styles are read from src/build_money1_pdfs.py (needs: pip install --break-system-packages sympy)."""
import os, sys, random, subprocess, re
from fractions import Fraction as Fr
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC)
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/quad"; os.makedirs(OUT, exist_ok=True)
SLUG = "quadratic-equations"
LO = "AF.4, AF.5, U.6"
M = "−"

# ---------- my own maths ----------
X, K, T = sp.symbols("x k t")
TR = standard_transformations + (implicit_multiplication_application,)
def P(s): return parse_expr(s.replace("−", "-").replace("²", "**2"), local_dict={"x": X, "k": K, "t": T}, transformations=TR)
def E(s):
    l, r = s.split("=")
    return sp.expand(P(l) - P(r))
def roots(s, v=X): return sorted(Fr(int(sp.numer(z)), int(sp.denom(z))) for z in sp.solve(E(s), v))
def n(v):
    v = Fr(v); s = M if v < 0 else ""; v = abs(v)
    return s + (str(v.numerator) if v.denominator == 1 else f"{v.numerator}/{v.denominator}")
def term(k, v, first):
    if k == 0: return ""
    a = abs(k); s = ("" if a == 1 and v else str(a)) + v
    return ((M if k < 0 else "") + s) if first else ((f" {M} " if k < 0 else " + ") + s)
def quad(a, b, c, rhs="0"): return term(a, "x²", True) + term(b, "x", False) + term(c, "", False) + " = " + rhs
def fromroots(r, s): return quad(1, -(r + s), r * s)
def br(r): return "x" if r == 0 else f"(x {M} {r})" if r > 0 else f"(x + {-r})"
def fac(r, s): return (br(r) + br(s) if r != 0 else "x" + br(s)) + " = 0"
def rs(L): return " or ".join(f"x = {n(v)}" for v in sorted(set(L)))
def both(L): return " and ".join(n(v) for v in sorted(set(L)))
def d2(x):
    v = round(x * 100) / 100
    return (M if v < 0 else "") + f"{abs(v):.2f}"
def formula(s):
    rr = sorted(float(z) for z in sp.solve(E(s), X)); return f"x = {d2(rr[0])} or x = {d2(rr[1])}"
assert quad(1, -5, 6) == "x² − 5x + 6 = 0" and fromroots(3, -2) == "x² − x − 6 = 0" and fac(3, -2) == "(x − 3)(x + 2) = 0"
assert roots("x² − 5x + 6 = 0") == [2, 3] and roots(fac(0, -4)) == [-4, 0]
def chk(s, R): assert roots(s) == sorted(R), (s, roots(s), R); return rs(R)

# ---------- free sheet ----------
A = [("Is x = 3 a root of x² − 5x + 6 = 0?", "yes: 9 − 15 + 6 = 0 ✓"),
     ("Is x = −2 a root of x² + x − 6 = 0?", "no: 4 − 2 − 6 = −4"),
     ("Solve (x − 4)(x + 1) = 0.", chk("(x − 4)(x + 1) = 0", [4, -1])),
     ("Solve x(x − 9) = 0.", chk("x(x − 9) = 0", [0, 9])),
     ("Solve (x + 6)(x + 2) = 0.", chk("(x + 6)(x + 2) = 0", [-6, -2])),
     ("Make it = 0: x² + 4x = 12.", "x² + 4x − 12 = 0")]
assert 9 - 15 + 6 == 0 and 4 - 2 - 6 == -4 and E("x² + 4x = 12") == E("x² + 4x − 12 = 0")
BQ = [("x² + 5x + 6 = 0", [-3, -2]), ("x² − 8x + 15 = 0", [3, 5]), ("x² + 2x − 8 = 0", [-4, 2]), ("x² − x − 12 = 0", [-3, 4]),
      ("x² − 7x = 0", [0, 7]), ("x² + 4x = 0", [-4, 0]), ("x² − 64 = 0", [-8, 8]), ("x² = 81", [-9, 9]),
      ("x² + 3x = 10", [-5, 2]), ("x² = 6x − 8", [2, 4])]
B = [(q, chk(q, R)) for q, R in BQ]
Cq = [("Write an equation with roots 3 and 5.", fromroots(3, 5)), ("Write an equation with roots −2 and 7.", fromroots(-2, 7)),
      ("Write an equation with roots 0 and −4.", fromroots(0, -4)), ("Write an equation with roots 6 and −6.", fromroots(6, -6)),
      ("x = 2 is one root of x² + 3x − 10 = 0. Find the other root.", "x = −5"),
      ("Higher Level: x = 4 is a root of x² + kx − 12 = 0. Find k.", "k = −1")]
for (q, a), R in zip(Cq[:4], [[3, 5], [-2, 7], [-4, 0], [-6, 6]]): assert roots(a) == R, (a, R)
assert roots("x² + 3x − 10 = 0") == [-5, 2] and sp.solve(E("x² + kx − 12 = 0").subs(X, 4), K) == [-1]
assert Cq[2][1] == "x² + 4x = 0" and Cq[3][1] == "x² − 36 = 0"
D = [("A rectangle is x cm wide and (x + 4) cm long. Its area is 60 cm². Find x.", "x² + 4x − 60 = 0 → x = 6 cm (x = −10 rejected)"),
     ("The square of a positive number, plus 3 times the number, is 40. Find the number.", "x² + 3x − 40 = 0 → 5"),
     ("Two whole numbers in a row multiply to 156. Find them.", "12 and 13"),
     ("A ball's height is h = 25t − 5t² metres after t seconds. When does it land?", "t = 5 s"),
     ("Higher Level: solve 3x² − 5x − 2 = 0.", chk("3x² − 5x − 2 = 0", [Fr(-1, 3), 2])),
     ("Higher Level: solve x² + 6x + 4 = 0, giving your answers to 2 decimal places.", formula("x² + 6x + 4 = 0"))]
assert [z for z in roots("x(x + 4) = 60") if z > 0] == [6] and [z for z in roots("x² + 3x = 40") if z > 0] == [5]
assert [z for z in roots("x(x + 1) = 156") if z > 0] == [12] and roots("25t − 5t² = 0", T) == [0, 5]
assert D[5][1] == "x = −5.24 or x = −0.76", D[5][1]
Eq = [("<b>Solve and check.</b> Solve x² − 2x − 24 = 0. Check both roots.", "(x − 6)(x + 4) = 0: <b>x = 6 or x = −4</b>. Check: 36 − 12 − 24 = 0 ✓, 16 + 8 − 24 = 0 ✓"),
      ("<b>Roots.</b> (a) Write an equation with roots −3 and 5. (b) Solve x² − 9 = 0 and x² − 9x = 0.", f"(a) (x + 3)(x − 5) = 0, <b>{fromroots(-3, 5)}</b> (b) <b>x = 3 or x = −3</b>; x(x − 9) = 0, <b>x = 0 or x = 9</b>"),
      ("<b>A patio.</b> A rectangular patio is x m wide and (x + 2) m long. Its area is 35 m². (a) Show that x² + 2x − 35 = 0. (b) Find the length and width of the patio.", "(a) x(x + 2) = 35 (b) (x + 7)(x − 5) = 0, x = 5 (not −7): <b>5 m by 7 m</b>"),
      ("<b>Higher Level.</b> (a) Solve 2x² − 7x + 3 = 0. (b) Solve 2x² + 3x − 4 = 0, giving your answers to 2 decimal places.", f"(a) (2x − 1)(x − 3) = 0, <b>x = 1/2 or x = 3</b> (b) x = (−3 ± √41) ÷ 4: <b>{formula('2x² + 3x − 4 = 0').replace('x = ', '', 1)}</b>")]
assert roots("x² − 2x − 24 = 0") == [-4, 6] and fromroots(-3, 5) == "x² − 2x − 15 = 0" and roots("x² − 9 = 0") == [-3, 3] and roots("x² − 9x = 0") == [0, 9]
assert E("x(x + 2) = 35") == E("x² + 2x − 35 = 0") and [z for z in roots("x² + 2x − 35 = 0") if z > 0] == [5]
assert roots("2x² − 7x + 3 = 0") == [Fr(1, 2), 3] and formula("2x² + 3x − 4 = 0") == "x = −2.35 or x = 0.85"

def qs(items): return "".join(f"<li>{q} <span class='line'></span></li>" for q, a in items)
def style(var):
    return re.search(var + r' = f"""<!doctype.*?<style>(.*?)</style>', open(os.path.join(SRC, "build_money1_pdfs.py"), encoding="utf-8").read(), re.S).group(1).replace("{LO}", LO).replace("{{", "{").replace("}}", "}")
SHEET_STYLE = style("sheet"); PACK_STYLE = style("pack")
assert "@bottom-left" in SHEET_STYLE and "Single-teacher licence" in PACK_STYLE
EXTRA = ".wk{font-variant-numeric:tabular-nums;line-height:1.45;border:1.5px solid var(--line);border-radius:8px;padding:2px 7px;margin:3px 0;font-size:9.2pt}.wk b.h{display:block}.sys{white-space:nowrap}.nw{white-space:nowrap}"
def rect(top, side, area, w=150):
    return (f'<svg viewBox="0 0 330 140" style="width:{w}px;display:block;margin:2px auto"><rect x="80" y="32" width="200" height="94" fill="#F6CF5A" stroke="#1B2430" stroke-width="3"/>'
            f'<text x="180" y="24" font-size="19" font-weight="700" text-anchor="middle" font-family="Inter,sans-serif">{top}</text>'
            f'<text x="72" y="85" font-size="19" font-weight="700" text-anchor="end" font-family="Inter,sans-serif">{side}</text>'
            f'<text x="180" y="85" font-size="17" font-weight="700" text-anchor="middle" font-family="Inter,sans-serif">Area = {area}</text></svg>')
assert roots("x(x + 3) = 40") == [-8, 5]

sheet = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Quadratic equations: rules and practice | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{SHEET_STYLE}
{EXTRA}
</style></head><body>
<div class="page tight">
  <div class="band"><div><div class="k">Junior Cycle Maths · Free revision sheet</div><h1>Quadratic equations</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2018 specification): {LO}. Play the game: <b>leim.ie/root-rush.html</b></p>
  <div class="two">
   <div><h2>1. What is a root?</h2>
    <p>A <b>root</b> (or solution) is a value of x that makes the equation true. A quadratic (an x² equation) usually has <b>two</b> roots. Check a root by putting it in: x = 2 in x² − 5x + 6 = 0 gives 4 − 10 + 6 = 0 ✓</p>
    <h2>2. Solve in 3 steps</h2>
    <div class="wk"><b class="h">1. Make it = 0</b>x² + 2x = 15 → x² + 2x − 15 = 0<br><b class="h">2. Factorise</b>(x + 5)(x − 3) = 0<br><b class="h">3. Each bracket = 0</b>x + 5 = 0 → x = −5 · x − 3 = 0 → x = 3</div>
    <p>The roots <b>multiply to the last number</b> (−5 × 3 = −15) and <b>add to the middle number with its sign changed</b> (−5 + 3 = −2, middle term +2x).</p>
    <h2>3. Two short cuts</h2>
    <div class="wk">x² − 6x = 0 → x(x − 6) = 0 → x = 0 or x = 6<br>x² − 49 = 0 → x² = 49 → x = 7 or x = −7</div>
    <p>Never divide by x: you lose x = 0.</p></div>
   <div><h2>4. Roots → equation</h2>
    <div class="wk">Roots 4 and −2 → (x − 4)(x + 2) = 0 → x² − 2x − 8 = 0</div>
    <p>The sign in the bracket is the <b>opposite</b> of the root.</p>
    <h2>5. Word problems</h2>
    {rect("x + 3", "x", "40 cm²")}
    <p>x(x + 3) = 40 → x² + 3x − 40 = 0 → (x + 8)(x − 5) = 0. x = −8 or x = 5, but a length can't be negative: <b>x = 5 cm</b>. Always say which root you reject and why.</p>
    <h2>6. Higher Level</h2>
    <p><b>2x² …</b>: 2x² + x − 6 = 0 → (2x − 3)(x + 2) = 0 → x = 3/2 or x = −2.<br><b>The formula</b>: x = (−b ± √(b² − 4ac)) ÷ 2a. x² − 4x − 3 = 0: x = (4 ± √28) ÷ 2 = 4.65 or −0.65.<br><b>Find k</b>: x = 3 is a root of x² + kx − 21 = 0 → 9 + 3k − 21 = 0 → k = 4.</p>
    <div class="note"><b>Classic mistakes:</b> not making it = 0 first · a term moved without changing sign · root 3 from (x + 3) · only one root for x² = 49 · keeping a negative length.</div></div>
  </div>
  <div class="tip"><b>Exam tip:</b> write the factors, then both roots, then check one by putting it back in. In a word problem, answer the question that was asked, with units.</div>
</div>

<div class="page p2">
  <div class="band"><div><div class="k">Practice · 32 questions</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Roots</h2><ol class="q">{qs(A)}</ol>
  <h2>B. Solve each equation</h2><ol class="q" start="7" style="columns:2;column-gap:8mm">{"".join(f"<li class='sys'>{q}</li>" for q, a in B)}</ol>
  <h2>C. Roots → equation</h2><ol class="q" start="17">{qs(Cq)}</ol>
  <h2>D. Word problems and Higher Level</h2><ol class="q" start="23">{qs(D)}</ol>
  <p class="small" style="margin-top:4px">Questions 29–32 are on the next page.</p>
</div>

<div class="page">
  <div class="band"><div><div class="k">Exam-style · then check</div><h1>Exam corner + answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>E. Exam-style questions (show your work)</h2>
  <ol class="q e3" start="29">{"".join(f"<li>{q}<span class='long'></span><span class='long'></span></li>" for q,a in Eq)}</ol>
  <h2 style="margin-top:10px">Answers</h2>
  <table class="ans"><tbody>
   <tr><td><b>A</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(A,1))}</td></tr>
   <tr><td><b>B</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(B,7))}</td></tr>
   <tr><td><b>C</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(Cq,17))}</td></tr>
   <tr><td><b>D</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(D,23))}</td></tr>
   <tr><td><b>E</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(Eq,29))}</td></tr>
  </tbody></table>
  <div class="note"><b>Got one wrong?</b> Check: did you make it = 0 first? Do your roots multiply to the last number? Did you give both roots? Then play <b>Root Rush</b> at leim.ie/root-rush.html: the "Go back over these" list at the end shows the rule for each mistake.</div>
  <p class="small">All questions written by Léim. Léim is independent and not connected with the State Examinations Commission or the NCCA.</p>
</div>
</body></html>"""
NQ = len(A) + len(B) + len(Cq) + len(D) + len(Eq)
assert NQ == 32, NQ

# ---------- teacher pack ----------
# Garden Swap: each fact is on exactly ONE card
SW1 = [("Width", "x m", "A"), ("Length", "(x + 3) m", "A"), ("Area", "70 m²", "B"),
       ("Equation", "", None), ("x", "", None), ("Perimeter", "", None)]
g = [z for z in roots("x(x + 3) = 70") if z > 0]; assert g == [7]
SW2 = [("Her number", "positive", "A"), ("Rule", "square it, take away 2 × it", "A"), ("The answer", "48", "B"),
       ("Equation", "", None), ("Her number", "", None)]
h = [z for z in roots("x² − 2x = 48") if z > 0]; assert h == [8] and roots("x² − 2x = 48") == [-6, 8]
for rows in (SW1, SW2): assert sum(w == "A" for *_, w in rows) >= 1 and sum(w == "B" for *_, w in rows) >= 1
def swap_card(who):
    def tab(title, rows):
        return f'<table class="ss"><thead><tr><th colspan="2">{title}</th></tr></thead><tbody>' + "".join(
            f"<tr><td>{k}</td><td><b>{v if w == who else ''}</b></td></tr>" for k, v, w in rows) + "</tbody></table>"
    return f'<div class="idc"><h3>Student {who} · Garden Swap</h3><div class="two">{tab("The garden (a rectangle)", SW1)}{tab("Aoife’s number", SW2)}</div></div>'

# Root Match mingle: 12 equations, 12 different root pairs
MR = [(-2, -1), (1, 6), (-3, 4), (2, 5), (-6, 1), (0, 8), (-7, 7), (-5, -4), (3, 4), (-2, 9), (0, -3), (-8, 2)]
MATCH = []
for i, (r, s) in enumerate(MR):
    q = fromroots(r, s) if i % 3 else fac(r, s) if i in (3,) else fromroots(r, s)
    if i == 7: q = quad(1, 9, 0, "−20")          # x² + 9x = −20
    if i == 9: q = "x² = 7x + 18"
    MATCH.append((q, both([r, s])))
for (q, a), (r, s) in zip(MATCH, MR): assert roots(q) == sorted([r, s]), (q, r, s)
ANS = [a for q, a in MATCH]
assert len(set(ANS)) == 12, ANS
cards = [q for q, a in MATCH] + ANS
random.seed(30); match_print = cards[:]; random.shuffle(match_print)
match_html = "".join(f'<div class="c"><span class="tag">Card {i}</span><div class="fc{" sm" if len(x) > 10 else ""}">{x}</div></div>' for i, x in enumerate(match_print, 1))
match_key = " · ".join(f"{match_print.index(q) + 1} → {match_print.index(a) + 1}" for q, a in MATCH)

# Quadratic Dominoes: 20 clues, 20 different answers
DR = [(-1, 3), (2, 7), (-4, 5), (-6, -2), (1, 8), (-9, 2), (3, 6), (-5, 5), (0, 5), (-10, 1), (4, 9), (-3, -1), (0, -6), (-8, 3)]
DOMS = [(fromroots(r, s), both([r, s])) for r, s in DR]
DOMS[7] = ("x² = 25", DOMS[7][1]); DOMS[8] = ("x² = 5x", DOMS[8][1]); DOMS[12] = ("x² + 6x = 0", DOMS[12][1])
for (q, a), (r, s) in zip(DOMS, DR): assert roots(q) == sorted([r, s]), (q, r, s)
DOMS += [("x² + 2x = 35, x > 0", "5"), ("x = 4 is a root of x² − x − 12 = 0. The other root?", "−3"),
         ("Rectangle x by (x + 1), area 42. x = ?", "6"), ("Two whole numbers in a row multiply to 110. The smaller?", "10"),
         ("Higher Level: x = 2 is a root of x² + kx − 10 = 0. k = ?", "3"), ("Higher Level: 2x² − x − 1 = 0", "−1/2 and 1")]
assert [z for z in roots("x² + 2x = 35") if z > 0] == [5] and roots("x² − x − 12 = 0") == [-3, 4]
assert [z for z in roots("x(x + 1) = 42") if z > 0] == [6] and [z for z in roots("x(x + 1) = 110") if z > 0] == [10]
assert sp.solve(E("x² + kx − 10 = 0").subs(X, 2), K) == [3] and both(roots("2x² − x − 1 = 0")) == "−1/2 and 1"
DANS = [a for k, a in DOMS]
assert len(set(DANS)) == 20, sorted(DANS)
random.seed(3030); chain = DOMS[:]; random.shuffle(chain)
dom = [("START" if k == 0 else chain[k - 1][1], x[0]) for k, x in enumerate(chain)] + [(chain[-1][1], "FINISH")]
dom_print = dom[:]; random.shuffle(dom_print)
dom_html = "".join(f'<div class="dom"><div class="h l{" sm" if len(l) > 9 else ""}">{l}</div><div class="h r">{r}</div></div>' for l, r in dom_print)
chain_key = "".join(f"<li>{x} = <b>{a}</b></li>" for x, a in chain)

ERR = [("x² + 3x = 18 → x² + 3x + 18 = 0", "no roots", "18 changes sign when it moves: x² + 3x − 18 = 0 → (x + 6)(x − 3) = 0, <b>x = −6 or x = 3</b>"),
       ("x² − x − 20 = 0 → (x − 5)(x + 4) = 0", "x = −5 or x = 4", "The sign in the bracket is the opposite of the root: <b>x = 5 or x = −4</b>"),
       ("x² = 8x → divide by x → x = 8", "x = 8", "Dividing by x loses a root: x(x − 8) = 0, <b>x = 0 or x = 8</b>"),
       ("x² − 100 = 0 → x² = 100", "x = 10", "Two square roots: <b>x = 10 or x = −10</b>"),
       ("x² + 7x + 12 = 0 → (x + 6)(x + 2) = 0", "x = −6 or x = −2", "6 + 2 = 8, not 7. (x + 3)(x + 4) = 0, <b>x = −3 or x = −4</b>"),
       ("Width x, length x + 2, area 48 → x = 6 or x = −8", "width −8 m", "A length can't be negative: <b>width 6 m, length 8 m</b>")]
assert roots("x² + 3x − 18 = 0") == [-6, 3] and roots("x² − x − 20 = 0") == [-4, 5] and roots("x² = 8x") == [0, 8]
assert roots("x² − 100 = 0") == [-10, 10] and roots("x² + 7x + 12 = 0") == [-4, -3] and E("(x + 6)(x + 2) = 0") != E("x² + 7x + 12 = 0")
assert roots("x(x + 2) = 48") == [-8, 6]
# worksheet exam-style
assert roots("x² − 3x − 28 = 0") == [-4, 7] and fromroots(-1, 6) == "x² − 5x − 6 = 0"
assert [z for z in roots("x(x + 6) = 91") if z > 0] == [7]
assert roots("35t − 5t² = 50", T) == [2, 5]
assert roots("3x² + 10x − 8 = 0") == [-4, Fr(2, 3)] and formula("x² − 2x − 5 = 0") == "x = −1.45 or x = 3.45"

pack = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Quadratic Equations Teacher Pack | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{PACK_STYLE}
{EXTRA}
.ss td:nth-child(2){{width:34%}}.ss td,.ss th{{padding:2px 5px;font-size:8.8pt;line-height:1.3}}.fym .c{{height:14.5mm}}.fym .fc{{font-size:12pt}}.fym .fc.sm{{font-size:9.4pt;line-height:1.15}}.idc{{padding:1.5mm 4mm}}.p1 .proc td{{font-size:8.5pt;padding:2px 6px}}
.dom .r{{font-size:9.6pt}}.dom .l{{font-size:12pt}}.ops div{{font-size:12pt}}
.big3{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:4mm;text-align:center}}.big3 div{{border-radius:14px;padding:5mm 3mm;font-size:13pt;line-height:1.45}}.big3 b{{display:block;font-size:17pt;margin-bottom:2mm}}
</style></head><body>

<div class="page p1">
  <div class="band"><div><div class="k">Junior Cycle Maths · Teacher pack</div><h1>Quadratic equations</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2018 specification): {LO}</p>
  <div class="two">
    <div><h3>Aims</h3><p>By the end of the lesson students can check whether a value is a root, solve quadratic equations by factorising (including x² + bx = 0 and x² = k), write a quadratic equation from its roots, and form and solve quadratic equations from area, number and height problems, rejecting roots that don't fit. Higher Level: ax² + bx + c = 0 with a &gt; 1, the formula, and "find k".</p></div>
    <div><h3>In this pack</h3><p>p.1 Teacher notes · p.2 Root Match mingle cards + Garden Swap A/B cards · p.3 Quadratic Dominoes (cut-up) · p.4 Wall poster · p.5 Worksheet: Error Hunt + exam-style questions · p.6 Answers. Level: 3rd year (Higher and Ordinary). Time: about 60 minutes. All questions are original.</p></div>
  </div>
  <h2 style="margin-top:8px">Procedure</h2>
  <table class="proc"><tbody>
    <tr><td>5 min</td><td><b>Lead-in: guess my number.</b> "I'm thinking of a number. I multiply it by itself and get 36." Pairs write every answer. Elicit 6 AND −6. "Now: my number times (my number − 1) is 12." (4 and −3.) Two answers is normal for an x² equation.</td></tr>
    <tr><td>8 min</td><td><b>Guided discovery.</b> Pairs solve (x − 2)(x − 5) = 0, (x + 1)(x − 4) = 0 and (x + 3)(x + 5) = 0 ("one bracket must be 0"), then multiply each out. "Look at the roots and the equation. What do the roots add to? Multiply to?" Build the 3 steps: make it = 0, factorise, each bracket = 0.</td></tr>
    <tr><td>10 min</td><td><b>Root Match mingle</b> (p.2, 24 cards = 12 equation/roots pairs; one card each). Equation card? Solve it, then find the person with your roots. Roots card? Find your equation. Pairs check each root by putting it back in.</td></tr>
    <tr><td>12 min</td><td><b>Garden Swap</b> (p.2, pairs, don't show your card). Each fact is on only ONE card. Ask your partner for what you're missing, write the equation together, then both solve and reject the root that doesn't fit. Feedback: garden x = {g[0]}, so {g[0]} m by {g[0] + 3} m, perimeter {2 * (2 * g[0] + 3)} m; Aoife's number is {h[0]} (−6 doesn't count: it's positive).</td></tr>
    <tr><td>10 min</td><td><b>Quadratic Dominoes</b> (p.3), groups of 3–4. Start with START, solve the clue, find the domino with that answer on its left, and build the chain to FINISH. Two roots are written "−1 and 3".</td></tr>
    <tr><td>12 min</td><td><b>Worksheet</b> (p.5). Error Hunt in pairs (find the mistake, name it, fix it), then the exam-style questions alone. Question 5 is Higher Level.</td></tr>
    <tr><td>3 min</td><td><b>Exit ticket.</b> Solve x² − x − 6 = 0 and check one root. (x = 3 or x = −2.) Homework: play <b>Root Rush</b> at leim.ie/root-rush.html and copy three lines from the "Go back over these" list.</td></tr>
  </tbody></table>
  <div class="note"><b>Mingle key</b> (equation card → roots card): {match_key}.<br>
  <b>Errors to look for:</b> not making it = 0 first · a term moved without changing sign · root 3 from (x + 3) · dividing by x and losing x = 0 · one root only for x² = k · keeping a negative length. <b>Support:</b> a card with "the roots multiply to the last number". <b>Fast finishers:</b> write an equation whose roots are −4 and 7, then one whose roots are 1/2 and 3 (Higher Level).</div>
  <p class="small"><b>Domino answer chain</b> (START → FINISH):</p>
  <ol class="small" style="columns:2;column-gap:12px;font-size:7.2pt;line-height:1.22;margin:0;padding-left:16px">{chain_key}</ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">Cut up the cards · one Garden Swap card per student</div><h1>Root Match mingle + Garden Swap</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:8.8pt;margin:0"><b>Root Match mingle.</b> Cut out the 24 cards and give one to each student. Equation card? Solve it, then find the person with your roots. Roots card? Find the equation that gives your roots. (Fewer students? Take out whole pairs.)</p>
  <div class="fym">{match_html}</div>
  <p style="font-size:8.8pt;margin:3mm 0 0"><b>Garden Swap.</b> Don't show your card. Each fact is on only one of the two cards: ask your partner for what you're missing, write the equation together, then fill in every blank.</p>
  {swap_card("A")}
  {swap_card("B")}
</div>

<div class="page">
  <div class="band"><div><div class="k">Groups of 3–4 · cut along the dashed lines</div><h1>Quadratic Dominoes</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.4pt">Start with START. Solve the clue on the right, then find the domino with that answer on its left. Two roots are written "−1 and 3". Keep going until you reach FINISH. The last two clues are Higher Level (Ordinary Level groups can be given those answers).</p>
  <div class="doms">{dom_html}</div>
</div>

<div class="page">
  <div class="poster">
    <h1>Quadratic equations</h1>
    <div class="big3">
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>1. Make it = 0</b>x² + 2x = 15<br>x² + 2x − 15 = 0</div>
      <div style="background:var(--green-soft)"><b>2. Factorise</b>(x + 5)(x − 3) = 0</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>3. Each bracket = 0</b>x = −5<br>or x = 3</div>
    </div>
    <div class="ops">
      <div style="background:var(--green-soft)"><b>No number term</b>x² − 6x = 0<br>x(x − 6) = 0<br>x = 0 or x = 6</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>No x term</b>x² = 49<br>x = 7 or x = −7<br>(two answers!)</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Roots → equation</b>roots 4 and −2<br>(x − 4)(x + 2) = 0<br>x² − 2x − 8 = 0</div>
      <div style="background:var(--green-soft)"><b>Higher Level</b>x = (−b ± √(b² − 4ac)) ÷ 2a<br>when it won't factorise</div>
    </div>
    <p style="text-align:center;font-size:13pt;margin:0"><b>Always:</b> check a root by putting it back in · reject a negative length</p>
    <p style="text-align:center;font-size:10pt;color:var(--muted)">Léim · leim.ie · Play Root Rush: leim.ie/root-rush.html</p>
  </div>
</div>

<div class="page ws">
  <div class="band"><div><div class="k">Worksheet</div><h1>Error Hunt + exam-style questions</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Error Hunt</h2>
  <p>Each student's working has one mistake. Find it, say what went wrong, and write the right answer.</p>
  <table class="eh"><thead><tr><th>Question and working</th><th>Student's answer</th><th>The mistake and the right answer</th></tr></thead><tbody>
  {"".join(f"<tr><td>{q}</td><td>{w}</td><td><span class='gap'></span><span class='gap'></span></td></tr>" for q,w,r in ERR)}
  </tbody></table>
  <h2>B. Exam-style questions (show all your work)</h2>
  <ol class="q">
    <li>Solve x² − 3x − 28 = 0. Check one of your roots.<span class="long"></span></li>
    <li>Write a quadratic equation with roots −1 and 6, in the form x² + bx + c = 0.<span class="long"></span></li>
    <li>A rectangular pitch is x m wide and (x + 6) m long. Its area is 91 m². (a) Write an equation in x. (b) Find the width and length.<span class="long"></span></li>
    <li>A ball's height is h = 35t − 5t² metres after t seconds. (a) When is it 50 m high? (b) Why are there two answers?<span class="long"></span></li>
    <li>Higher Level: (a) solve 3x² + 10x − 8 = 0. (b) Solve x² − 2x − 5 = 0, giving your answers to 2 decimal places.<span class="long"></span></li>
  </ol>
</div>

<div class="page an">
  <div class="band"><div><div class="k">For the teacher</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>Garden Swap</h2>
  <div class="two"><table><tbody>
   <tr><td>Equation</td><td><b>x(x + 3) = 70 → x² + 3x − 70 = 0</b></td></tr><tr><td>x</td><td>(x + 10)(x − 7) = 0: <b>x = 7</b> (not −10)</td></tr>
   <tr><td>Perimeter</td><td>7 m by 10 m: <b>34 m</b></td></tr></tbody></table>
  <table><tbody>
   <tr><td>Equation</td><td><b>x² − 2x = 48 → x² − 2x − 48 = 0</b></td></tr><tr><td>Her number</td><td>(x − 8)(x + 6) = 0: <b>8</b> (−6 is not positive)</td></tr></tbody></table></div>
  <h2>A. Error Hunt</h2>
  <table><tbody>{"".join(f"<tr><td style='width:42%'><b>{q}</b></td><td>{r}</td></tr>" for q,w,r in ERR)}</tbody></table>
  <h2>B. Exam-style questions</h2>
  <ol class="q">
    <li>(x − 7)(x + 4) = 0: <b>x = 7 or x = −4</b>. Check: 49 − 21 − 28 = 0 ✓</li>
    <li>(x + 1)(x − 6) = 0: <b>x² − 5x − 6 = 0</b></li>
    <li>(a) x(x + 6) = 91 → x² + 6x − 91 = 0 (b) (x + 13)(x − 7) = 0, x = 7 (not −13): <b>7 m wide, 13 m long</b></li>
    <li>(a) 5t² − 35t + 50 = 0 → t² − 7t + 10 = 0 → (t − 2)(t − 5) = 0: <b>t = 2 s and t = 5 s</b> (b) once on the way up, once on the way down</li>
    <li>(a) (3x − 2)(x + 4) = 0: <b>x = 2/3 or x = −4</b> (b) x = (2 ± √24) ÷ 2: <b>{formula("x² − 2x − 5 = 0")}</b></li>
  </ol>
  <h2>Marking tip</h2>
  <p>Give credit for each step, as the exam does: making it = 0, correct factors, each root. One root on its own is not finished. In word problems insist on a sentence saying which root is rejected and why, and units in the answer.</p>
</div>
</body></html>"""

cover = """<!doctype html><html><head><meta charset="utf-8"><style>
body{margin:0;width:1200px;height:1200px;background:#1B2430;font-family:Inter,sans-serif;color:#fff;display:flex;flex-direction:column;justify-content:space-between;padding:90px;box-sizing:border-box}
.k{display:inline-block;background:#2E7D57;border-radius:99px;padding:12px 26px;font-weight:700;font-size:28px;letter-spacing:.06em;text-transform:uppercase}
h1{font-size:96px;font-weight:800;line-height:1.14;letter-spacing:-.03em;margin:40px 0 0}
h1 span{background:#F6CF5A;color:#1B2430;padding:0 14px;box-decoration-break:clone;-webkit-box-decoration-break:clone}
.sub{font-size:38px;color:#C9D1DA;margin-top:36px;line-height:1.35}
.em{font-size:50px;margin-top:30px;font-weight:800;letter-spacing:.01em;color:#F6CF5A}
.foot{display:flex;justify-content:space-between;align-items:center;font-size:34px;font-weight:700}
.price{background:#F6CF5A;color:#1B2430;border-radius:16px;padding:14px 28px}
</style></head><body>
<div><span class="k">Junior Cycle Maths · Teacher pack</span>
<h1><span>Quadratic</span><br><span>Equations</span></h1>
<div class="sub">Root Match mingle · Garden Swap A/B<br>Dominoes · Poster · Worksheet + answers</div>
<div class="em">x² − 5x + 6 = 0 → x = 2 or 3</div></div>
<div class="foot"><span>↗ Léim · leim.ie</span><span class="price">Ready to teach · 60 min</span></div>
</body></html>"""
assert roots("x² − 5x + 6 = 0") == [2, 3]

if __name__ == "__main__":
    for name, txt in [("rules-and-practice", sheet), ("teacher-pack", pack), ("cover", cover)]:
        plain = re.sub(r"<[^>]+>", " ", re.sub(r"<style>.*?</style>|<svg.*?</svg>", "", txt, flags=re.S))
        assert not re.search(r"[\dxyt)²]\s*-\s*[\dxyt(]|[=(]\s*-\d|(?<![\w])-\d", plain), (name, re.findall(r".{20}[\dxy)]\s*-\s*[\dxy(].{10}|.{10}[=(]\s*-\d.{10}", plain)[:3])
        open(os.path.join(SRC, f"{SLUG}-{name}.html"), "w", encoding="utf-8").write(txt)
    def pdf(name, out):
        subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--no-pdf-header-footer", f"--print-to-pdf={out}",
                        f"{SLUG}-{name}.html"], cwd=SRC, check=True, capture_output=True)
        d = open(out, "rb").read(); print(name, len(re.findall(rb"/Type\s*/Page[^s]", d)), "pages")
    pdf("rules-and-practice", os.path.join(ROOT, "printables", f"{SLUG}-rules-and-practice.pdf"))
    pdf("teacher-pack", os.path.join(OUT, "Quadratic-Equations-Teacher-Pack-Leim.pdf"))
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--hide-scrollbars", "--window-size=1200,1200",
                    f"--screenshot={os.path.join(OUT, f'{SLUG}-cover.png')}", f"{SLUG}-cover.html"], cwd=SRC, check=True, capture_output=True)
    print("domino chain:", [(x, a) for x, a in chain])
