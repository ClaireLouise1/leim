#!/usr/bin/env python3
"""Functions & graphs (JC Maths topic 31): free sheet + teacher pack + Payhip cover.
Run from the repo root: python3 src/build_functions_pdfs.py OUTDIR
Writes src/functions-graphs-*.html; PDFs/cover PNG go to OUTDIR (free sheet also to printables/).
Every function value, root, turning point and table is checked with sympy.
Styles are read from src/build_money1_pdfs.py (needs: pip install --break-system-packages sympy)."""
import os, sys, random, subprocess, re
from fractions import Fraction as Fr
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC)
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/func"; os.makedirs(OUT, exist_ok=True)
SLUG = "functions-graphs"
LO = "AF.7a–d, AF.1c, U.4"
M = "−"

# ---------- my own maths ----------
X, K = sp.symbols("x k")
TR = standard_transformations + (implicit_multiplication_application,)
def P(s):
    s = s.replace("−", "-").replace("²", "**2").replace("×", "*")
    s = re.sub(r"(\d)ˣ", r"(\1**x)", s)
    return parse_expr(s, local_dict={"x": X, "k": K}, transformations=TR)
def f_(s): return P(s.split("=", 1)[1]) if "=" in s else P(s)
def n(v):
    v = Fr(str(v)) if not isinstance(v, Fr) else v; s = M if v < 0 else ""; v = abs(v)
    return s + (str(v.numerator) if v.denominator == 1 else f"{v.numerator}/{v.denominator}")
def ev(s, x): return Fr(str(sp.nsimplify(f_(s).subs(X, x))))
def sol(s, k): return sorted(Fr(str(z)) for z in sp.solve(sp.Eq(f_(s), k), X))
def both(L): return " and ".join(n(v) for v in L)
def turn(s):
    e = f_(s); h = sp.solve(sp.diff(e, X), X)[0]; return f"({n(h)}, {n(e.subs(X, h))})"
def kind(s):
    e = f_(s)
    if any(a.exp.has(X) for a in e.atoms(sp.Pow)): return "exponential"
    return {1: "linear", 2: "quadratic"}[sp.degree(sp.expand(e), X)]
def tkind(ys):
    d = [b - a for a, b in zip(ys, ys[1:])]; dd = [b - a for a, b in zip(d, d[1:])]
    if len(set(d)) == 1: return "linear"
    if len(set(dd)) == 1: return "quadratic"
    assert len(set(Fr(b, a) for a, b in zip(ys, ys[1:]))) == 1; return "exponential"
assert ev("f(x) = 3x − 2", 4) == 10 and sol("f(x) = x² − 2x − 3", 0) == [-1, 3] and turn("x² − 2x − 3") == "(1, −4)"
assert kind("3 × 2ˣ") == "exponential" and kind("x(x + 2)") == "quadratic" and tkind([1, 2, 4, 8]) == "exponential"

# ---------- SVG graphs (same look as the game) ----------
GCSS = (".gl{stroke:#DCE3EA;stroke-width:.8}.ax{stroke:#5B6775;stroke-width:1.4}.tk{font:600 9.5px Inter,sans-serif;fill:#6B7785}"
        ".axl{font:italic 700 12px Inter,sans-serif;fill:#5B6775;paint-order:stroke;stroke:#fff;stroke-width:3px}"
        ".cv{fill:none;stroke-width:2.6;stroke-linecap:round;stroke-linejoin:round}.cv.a{stroke:#2962A6}.cv.b{stroke:#7A4BB3}"
        ".lnl{font:italic 800 14px Inter,sans-serif;paint-order:stroke;stroke:#fff;stroke-width:3px}.lnl.a{fill:#2962A6}.lnl.b{fill:#7A4BB3}"
        ".ml{font:800 14px Inter,sans-serif;fill:#C0392B}.skl{font:italic 600 10px Inter,sans-serif;fill:#6B7785}")
GID = [0]
def G(x0, x1, y0, y1, curves=(), sx=26, sy=16, ty=1, ly=None, xl="x", yl="y", w=None):
    ly = ly or ty; pl, pr, pt, pb = 30, 16, 20, (30 if y0 == 0 else 24)
    W = (x1 - x0) * sx + pl + pr; HH = (y1 - y0) * sy + pt + pb; GID[0] += 1; cid = f"pc{GID[0]}"
    Xf = lambda x: round(pl + (x - x0) * sx, 2); Yf = lambda y: round(pt + (y1 - y) * sy, 2)
    h = [f'<svg viewBox="0 0 {W} {HH}" style="width:{w or W}px;display:block;margin:2px auto"><defs><clipPath id="{cid}"><rect x="{Xf(x0)}" y="{Yf(y1)}" width="{(x1-x0)*sx}" height="{(y1-y0)*sy}"/></clipPath></defs>']
    for v in range(x0, x1 + 1): h.append(f'<line class="gl" x1="{Xf(v)}" y1="{Yf(y0)}" x2="{Xf(v)}" y2="{Yf(y1)}"/>')
    v = (y0 // ty) * ty
    while v <= y1:
        if v >= y0: h.append(f'<line class="gl" x1="{Xf(x0)}" y1="{Yf(v)}" x2="{Xf(x1)}" y2="{Yf(v)}"/>')
        v += ty
    h.append(f'<line class="ax" x1="{Xf(x0)}" y1="{Yf(0)}" x2="{Xf(x1)}" y2="{Yf(0)}"/><line class="ax" x1="{Xf(0)}" y1="{Yf(y0)}" x2="{Xf(0)}" y2="{Yf(y1)}"/>')
    for v in range(x0, x1 + 1):
        if v: h.append(f'<text class="tk" x="{Xf(v)}" y="{Yf(0)+12}" text-anchor="middle">{n(v)}</text>')
    v = -(-y0 // ly) * ly
    while v <= y1:
        if v: h.append(f'<text class="tk" x="{Xf(0)-4}" y="{Yf(v)+3.5}" text-anchor="end">{n(v)}</text>')
        v += ly
    h.append(f'<text class="tk" x="{Xf(0)-4}" y="{Yf(0)+12}" text-anchor="end">0</text>')
    h.append(f'<text class="axl" x="{Xf(x1)-2}" y="{Yf(0)+23 if y0 == 0 else Yf(0)-5}" text-anchor="end">{xl}</text><text class="axl" x="{Xf(0)+5}" y="{Yf(y1)+12}">{yl}</text>')
    for j, c in enumerate(curves):
        f, lab = c[0], c[1]; lo, hi = (c[2], c[3]) if len(c) > 2 else (x0, x1); k = "ab"[j]
        pts = []
        for i in range(161):
            x = lo + (hi - lo) * i / 160; y = f(x)
            if y0 - (y1 - y0) <= y <= y1 + (y1 - y0): pts.append(f"{Xf(x)},{Yf(y)}")
        h.append(f'<polyline class="cv {k}" clip-path="url(#{cid})" points="{" ".join(pts)}"/>')
        if lab:
            at = next((hi - (hi - lo) * i / 80 for i in range(81) if y0 + .1 * (y1 - y0) < f(hi - (hi - lo) * i / 80) < y1 - .1 * (y1 - y0)), hi)
            if j == 1: at = next((lo + (hi - lo) * i / 80 for i in range(81) if y0 + .1 * (y1 - y0) < f(lo + (hi - lo) * i / 80) < y1 - .1 * (y1 - y0)), lo)
            h.append(f'<text class="lnl {k}" x="{Xf(at) + (12 if j else -12)}" y="{max(14, Yf(f(at)) - 6)}" text-anchor="middle">{lab}</text>')
    return "".join(h) + "</svg>"
SHAPE = {"up": lambda u: .1 + .8 * u, "down": lambda u: .9 - .8 * u, "flat": lambda u: .5, "hill": lambda u: .1 + 3.2 * u * (1 - u),
         "valley": lambda u: .9 - 3.2 * u * (1 - u), "exp": lambda u: .05 + .85 * (2 ** (5 * u) - 1) / 31}
def sk(shape, letter="", w=105):
    f = SHAPE[shape]; pts = " ".join(f"{round(20 + 116 * i / 40, 2)},{round(92 - 80 * f(i / 40), 2)}" for i in range(41))
    return (f'<svg viewBox="0 0 150 116" style="width:{w}px;display:block;margin:0 auto">' + (f'<text class="ml" x="4" y="14">{letter}</text>' if letter else "") +
            '<line class="ax" x1="16" y1="96" x2="142" y2="96"/><line class="ax" x1="16" y1="96" x2="16" y2="6"/><text class="skl" x="140" y="110" text-anchor="end">time</text>'
            f'<polyline class="cv a" points="{pts}"/></svg>')
fq = lambda x: x * x - 2 * x - 3

# ---------- free sheet ----------
A = [("f(x) = 2x + 7. Find f(3).", n(ev("2x + 7", 3))), ("f(x) = 2x + 7. Find f(−4).", n(ev("2x + 7", -4))),
     ("g(x) = 10 − 3x. Find g(5).", n(ev("10 − 3x", 5))), ("h(x) = x² − 6. Find h(−3).", n(ev("x² − 6", -3))),
     ("f(x) = x² + 4x − 1. Find f(2).", n(ev("x² + 4x − 1", 2))), ("f(x) = 5x − 3. Find x when f(x) = 22.", "x = " + both(sol("5x − 3", 22))),
     ("f(x) = 4x + 9. Find x when f(x) = 1.", "x = " + both(sol("4x + 9", 1))), ("Is (3, 11) on the graph of f(x) = 3x + 2?", "yes: f(3) = 11")]
assert A[0][1] == "13" and A[1][1] == "−1" and A[2][1] == "−5" and A[3][1] == "3" and A[4][1] == "11" and A[5][1] == "x = 5" and A[6][1] == "x = −2" and ev("3x + 2", 3) == 11
fB = "x² − 2x − 8"; fb = lambda x: x * x - 2 * x - 8
B = [("Use the graph to solve f(x) = 0.", "x = " + " or x = ".join(n(v) for v in sol(fB, 0))), ("Write down the minimum point.", turn(fB)),
     ("Use the graph to find f(−1).", n(ev(fB, -1))), ("Use the graph to find f(5).", n(ev(fB, 5))),
     ("Use the graph to solve f(x) = −5.", "x = " + " or x = ".join(n(v) for v in sol(fB, -5))), ("Where does the graph cut the y-axis?", f"(0, {n(ev(fB, 0))})")]
assert B[0][1] == "x = −2 or x = 4" and B[1][1] == "(1, −9)" and B[2][1] == "−5" and B[3][1] == "7" and B[4][1] == "x = −1 or x = 3" and B[5][1] == "(0, −8)"
CT = [("f(x) = 4x − 1", None), ("f(x) = x² + 3", None), ("f(x) = 5 × 2ˣ", None), ("f(x) = x(x − 6)", None)]
C = [(f"Linear, quadratic or exponential? {q}", kind(q)) for q, _ in CT]
TB = [[2, 5, 8, 11, 14], [3, 6, 12, 24, 48]]
C += [(f"Linear, quadratic or exponential? x: 0, 1, 2, 3, 4 → f(x): {', '.join(map(str, ys))}", tkind(ys)) for ys in TB]
assert [a for q, a in C] == ["linear", "quadratic", "exponential", "quadratic", "linear", "exponential"]
STORIES = [("the height of a kicked ball", "hill"), ("bacteria doubling every hour", "exp"), ("a phone battery as you play", "down"), ("parking: one price all day", "flat")]
D_ORDER = ["flat", "hill", "down", "exp"]; DL = "ABCD"
D = [(f"Which graph shows: {s}?", DL[D_ORDER.index(sh)]) for s, sh in STORIES]
D += [("Higher Level: f(x) = 3 × 2ˣ. Find f(4).", n(ev("3 × 2ˣ", 4))),
      ("Higher Level: f(x) = x² + kx − 5 and f(2) = 7. Find k.", "k = " + n(sp.solve(sp.Eq(f_("x² + kx − 5").subs(X, 2), 7), K)[0]))]
assert D[4][1] == "48" and D[5][1] == "k = 4"
Eq = [("<b>A function.</b> f(x) = 3x − 5. (a) Find f(4) and f(−2). (b) Find x when f(x) = 10.", "(a) <b>7</b> and <b>−11</b> (b) 3x = 15, <b>x = 5</b>"),
      ("<b>Draw a graph.</b> f(x) = x² − 2x − 3. (a) Copy and complete the table for −2 ≤ x ≤ 4. (b) Draw the graph. (c) Use it to solve f(x) = 0 and to estimate where f(x) = 2.",
       "(a) " + ", ".join(n(ev("x² − 2x − 3", x)) for x in range(-2, 5)) + " (c) <b>x = −1 or x = 3</b>; f(x) = 2 at about <b>x = −1.4 and x = 3.4</b>"),
      ("<b>A ball.</b> Its height is h = 20t − 5t² metres after t seconds. (a) Find h at t = 1, 2, 3. (b) What is the greatest height? (c) When does it land?",
       f"(a) {n(ev('20x − 5x²', 1))} m, {n(ev('20x − 5x²', 2))} m, {n(ev('20x − 5x²', 3))} m (b) <b>20 m</b> after 2 s (c) h = 0: 5t(4 − t) = 0, <b>t = 4 s</b>"),
      ("<b>Higher Level.</b> f(x) = x² − 2x − 3 and g(x) = x + 1. (a) Solve f(x) = g(x). (b) Is the table 2, 6, 18, 54 linear, quadratic or exponential? Write its rule (x = 0, 1, 2, 3).",
       "(a) x² − 3x − 4 = 0, <b>x = −1 or x = 4</b> (b) ×3 each time: <b>exponential</b>, f(x) = 2 × 3ˣ")]
assert [ev("x² − 2x − 3", x) for x in range(-2, 5)] == [5, 0, -3, -4, -3, 0, 5] and [round(float(v), 1) for v in sp.solve(X**2 - 2*X - 5, X)] == [-1.4, 3.4]
assert [ev("20x − 5x²", t) for t in (1, 2, 3, 4)] == [15, 20, 15, 0] and sol("x² − 2x − 3", 0) == [-1, 3]
assert sp.solve(f_("x² − 2x − 3") - f_("x + 1"), X) == [-1, 4] and [ev("2 × 3ˣ", x) for x in range(4)] == [2, 6, 18, 54]

def qs(items): return "".join(f"<li>{q} <span class='line'></span></li>" for q, a in items)
def style(var):
    return re.search(var + r' = f"""<!doctype.*?<style>(.*?)</style>', open(os.path.join(SRC, "build_money1_pdfs.py"), encoding="utf-8").read(), re.S).group(1).replace("{LO}", LO).replace("{{", "{").replace("}}", "}")
SHEET_STYLE = style("sheet"); PACK_STYLE = style("pack")
assert "@bottom-left" in SHEET_STYLE and "Single-teacher licence" in PACK_STYLE
EXTRA = GCSS + ".wk{font-variant-numeric:tabular-nums;line-height:1.45;border:1.5px solid var(--line);border-radius:8px;padding:2px 7px;margin:3px 0;font-size:9.2pt}.wk b.h{display:block}.nw{white-space:nowrap}.sh3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:2mm;text-align:center;font-size:8.6pt;font-weight:700}.sk4{display:grid;grid-template-columns:repeat(4,1fr);gap:2mm}.gfig{float:right;margin:0 0 2mm 4mm}"
def mapsvg(ins, outs, pairs, w=120):
    nn = max(len(ins), len(outs)); Hh = 34 + nn * 24
    cy = lambda i, L: round(22 + (Hh - 28) / 2 - (L - 1) * 12 + i * 24, 2)
    h = f'<svg viewBox="0 0 150 {Hh}" style="width:{w}px;display:block;margin:2px auto"><ellipse cx="38" cy="{Hh/2+6}" rx="22" ry="{nn*12+6}" fill="#F3F6F9" stroke="#5B6775"/><ellipse cx="112" cy="{Hh/2+6}" rx="22" ry="{nn*12+6}" fill="#F3F6F9" stroke="#5B6775"/>'
    for i, v in enumerate(ins): h += f'<text x="38" y="{cy(i,len(ins))+5}" text-anchor="middle" font-weight="800" font-size="13">{n(v)}</text>'
    for i, v in enumerate(outs): h += f'<text x="112" y="{cy(i,len(outs))+5}" text-anchor="middle" font-weight="800" font-size="13">{n(v)}</text>'
    for a, b in pairs: h += f'<line x1="52" y1="{cy(ins.index(a),len(ins))}" x2="98" y2="{cy(outs.index(b),len(outs))}" stroke="#2962A6" stroke-width="1.6"/><circle cx="98" cy="{cy(outs.index(b),len(outs))}" r="2.4" fill="#2962A6"/>'
    return h + "</svg>"
assert all(ev("3x + 2", a) == b for a, b in [(1, 5), (2, 8), (3, 11)])

sheet = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Functions and graphs: rules and practice | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{SHEET_STYLE}
{EXTRA}
</style></head><body>
<div class="page tight">
  <div class="band"><div><div class="k">Junior Cycle Maths · Free revision sheet</div><h1>Functions &amp; graphs</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2018 specification): {LO}. Play the game: <b>leim.ie/graph-match.html</b></p>
  <div class="two">
   <div><h2>1. What is a function?</h2>
    {mapsvg([1, 2, 3], [5, 8, 11], [(1, 5), (2, 8), (3, 11)], 110)}
    <p>A <b>function</b> gives each input <b>exactly one</b> output. Here f(x) = 3x + 2. Two inputs may share an output; one input can't have two.</p>
    <h2>2. f(x) notation</h2>
    <div class="wk"><b class="h">Find an output</b>f(x) = 3x + 2 → f(4) = 3(4) + 2 = 14<br><b class="h">Find an input</b>f(x) = 11 → 3x + 2 = 11 → x = 3</div>
    <p>f(4) = 14 means the point <b>(4, 14)</b> is on the graph. Squaring a negative: (−3)² = 9.</p>
    <h2>3. Linear, quadratic or exponential?</h2>
    <div class="sh3"><div>{G(-3, 3, -5, 9, [(lambda x: 3 * x + 1, "")], sx=11, sy=5, ly=4)}Linear 3x + 1<br>same jump</div><div>{G(-3, 3, -5, 9, [(lambda x: x * x - 4, "")], sx=11, sy=5, ly=4)}Quadratic x² − 4<br>jumps change evenly</div><div>{G(-3, 3, -5, 9, [(lambda x: 2 ** x, "")], sx=11, sy=5, ly=4)}Exponential 2ˣ<br>× same number</div></div></div>
   <div><h2>4. Reading a graph</h2>
    {G(-2, 4, -4, 5, [(fq, "f", -2, 4)], sx=27, sy=15, w=190)}
    <p class="small" style="text-align:center;margin:0">f(x) = x² − 2x − 3</p>
    <ul><li><b>f(x) = 0</b>: where it crosses the x-axis: x = −1 or x = 3.</li><li><b>Minimum point</b>: the bottom of the ∪: (1, −4).</li>
    <li><b>f(x) = 2</b>: across from 2, then down: about x = −1.4 or x = 3.4.</li></ul>
    <h2>5. Graphs that tell a story</h2>
    <p>Straight line up: the same amount each time. Flat: no change. ∩: up then down (a maximum). Exponential: slow, then faster and faster.</p>
    <h2>6. Higher Level</h2>
    <p><b>f(x) = g(x)</b>: where the graphs meet. <b>Exponential</b>: f(x) = 3 × 2ˣ, f(3) = 3 × 8 = 24. <b>Find k</b>: f(x) = x² + kx − 4, f(2) = 6 → 4 + 2k − 4 = 6 → k = 3.</p>
    <div class="note"><b>Classic mistakes:</b> (−3)² = −9 · (y, x) instead of (x, y) · 2x and 2ˣ mixed up · straight lines instead of a smooth curve · one answer when there are two.</div></div>
  </div>
</div>

<div class="page p2">
  <div class="band"><div><div class="k">Practice · 30 questions</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Inputs and outputs</h2><ol class="q" style="columns:2;column-gap:8mm">{"".join(f"<li>{q}</li>" for q, a in A)}</ol>
  <h2>B. Read the graph of f(x) = x² − 2x − 8</h2>
  <div class="gfig">{G(-3, 5, -10, 8, [(fb, "f", -3, 5)], sx=22, sy=9, ly=2, w=200)}</div>
  <ol class="q" start="9">{qs(B)}</ol>
  <div style="clear:both"></div>
  <h2>C. Linear, quadratic or exponential?</h2><ol class="q" start="15" style="columns:2;column-gap:8mm">{"".join(f"<li>{q.replace('Linear, quadratic or exponential? ', '')}</li>" for q, a in C)}</ol>
  <h2>D. Stories and Higher Level</h2>
  <div class="sk4">{"".join(sk(s, DL[i]) for i, s in enumerate(D_ORDER))}</div>
  <ol class="q" start="21">{qs(D)}</ol>
  <p class="small" style="margin-top:4px">Questions 27–30 are on the next page.</p>
</div>

<div class="page">
  <div class="band"><div><div class="k">Exam-style · then check</div><h1>Exam corner + answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>E. Exam-style questions (show your work)</h2>
  <ol class="q e3" start="27">{"".join(f"<li>{q}<span class='long'></span><span class='long'></span></li>" for q,a in Eq)}</ol>
  <h2 style="margin-top:10px">Answers</h2>
  <table class="ans"><tbody>
   <tr><td><b>A</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(A,1))}</td></tr>
   <tr><td><b>B</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(B,9))}</td></tr>
   <tr><td><b>C</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(C,15))}</td></tr>
   <tr><td><b>D</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(D,21))}</td></tr>
   <tr><td><b>E</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(Eq,27))}</td></tr>
  </tbody></table>
  <div class="note"><b>Got one wrong?</b> Check: did you square the negative correctly? Is your point (x, y)? Did you give every answer? Then play <b>Graph Match</b> at leim.ie/graph-match.html: the "Go back over these" list at the end shows the rule for each mistake.</div>
  <p class="small">All questions written by Léim. Léim is independent and not connected with the State Examinations Commission or the NCCA.</p>
</div>
</body></html>"""
NQ = len(A) + len(B) + len(C) + len(D) + len(Eq)
assert NQ == 30, NQ

# ---------- teacher pack ----------
# Function Match mingle: 12 rules, 12 different tables (x = 0, 1, 2, 3)
RULES = ["2x + 1", "3x − 2", "5 − x", "4x", "x²", "x² + 1", "x² − 3x", "2x² − 1", "2ˣ", "3 × 2ˣ", "3ˣ", "x(x + 2)"]
TABS = [[ev(r, x) for x in range(4)] for r in RULES]
assert len(set(map(tuple, TABS))) == 12
# the first two outputs alone must not pick out the rule (students check the whole table)
MATCH = [(f"f(x) = {r}", "x: 0, 1, 2, 3<br>f(x): " + ", ".join(n(v) for v in t)) for r, t in zip(RULES, TABS)]
cards = [q for q, a in MATCH] + [a for q, a in MATCH]
random.seed(31); match_print = cards[:]; random.shuffle(match_print)
match_html = "".join(f'<div class="c"><span class="tag">Card {i}</span><div class="fc{" sm" if "<br>" in x else ""}">{x}</div></div>' for i, x in enumerate(match_print, 1))
match_key = " · ".join(f"{match_print.index(q) + 1} → {match_print.index(a) + 1}" for q, a in MATCH)

# Story Graph Swap A/B: each fact is on exactly ONE card
SW1 = [("Fixed charge", "€4", "A"), ("Price per km", "€2", "B"), ("Rule: f(x) = …", "", None), ("Cost of 6 km", "", None), ("Distance for €20", "", None), ("Linear, quadratic or exponential?", "", None)]
SW2 = [("One root", "x = −1", "A"), ("The other root", "x = 3", "B"), ("f(x) = x² + bx + c with", "b, c whole numbers", "A"),
       ("f(x) in brackets", "", None), ("f(x) multiplied out", "", None), ("Minimum point", "", None), ("f(5)", "", None)]
for rows in (SW1, SW2): assert sum(w == "A" for *_, w in rows) >= 1 and sum(w == "B" for *_, w in rows) >= 1
assert ev("4 + 2x", 6) == 16 and sol("4 + 2x", 20) == [8] and kind("2x + 4") == "linear"
assert sp.expand((X + 1) * (X - 3) - f_("x² − 2x − 3")) == 0 and turn("x² − 2x − 3") == "(1, −4)" and ev("x² − 2x − 3", 5) == 12
def swap_card(who):
    def tab(title, rows):
        return f'<table class="ss"><thead><tr><th colspan="2">{title}</th></tr></thead><tbody>' + "".join(
            f"<tr><td>{k}</td><td><b>{v if w == who else ''}</b></td></tr>" for k, v, w in rows) + "</tbody></table>"
    return f'<div class="idc"><h3>Student {who} · Story Graph Swap</h3><div class="two">{tab("A taxi fare", SW1)}{tab("A quadratic function f", SW2)}</div><p style="font-size:8pt;margin:1mm 0 0">Then, together: sketch both graphs on the back.</p></div>'

# Function Dominoes: 20 clues, 20 different answers (each one checked)
DOMS = [("f(x) = 2x + 5. f(3) = ?", n(ev("2x + 5", 3))), ("f(x) = x² − 4. f(−3) = ?", n(ev("x² − 4", -3))), ("g(x) = 10 − 3x. g(4) = ?", n(ev("10 − 3x", 4))),
        ("f(x) = 3x − 1 and f(x) = 20. x = ?", both(sol("3x − 1", 20))), ("h(x) = x² + 2x. h(2) = ?", n(ev("x² + 2x", 2))), ("f(x) = 2ˣ. f(5) = ?", n(ev("2ˣ", 5))),
        ("f(x) = 3 × 2ˣ. f(2) = ?", n(ev("3 × 2ˣ", 2))), ("f(x) = 5x + 3 and f(x) = −12. x = ?", both(sol("5x + 3", -12))),
        ("Roots of f(x) = (x − 4)(x + 1)", both(sol("(x − 4)(x + 1)", 0))), ("Roots of f(x) = x² − 6x + 5", both(sol("x² − 6x + 5", 0))),
        ("Minimum point of f(x) = x² − 4x − 5", turn("x² − 4x − 5")), ("Minimum point of f(x) = x² − 2x − 3", turn("x² − 2x − 3")),
        ("x: 0, 1, 2, 3 → 3, 7, 11, 15", tkind([3, 7, 11, 15]).capitalize()), ("x: 0, 1, 2, 3 → 2, 6, 18, 54", tkind([2, 6, 18, 54]).capitalize()),
        ("x: 0, 1, 2, 3 → 1, 4, 9, 16", tkind([1, 4, 9, 16]).capitalize()), ("f(x) = x² + 1. f(0) = ?", n(ev("x² + 1", 0))),
        ("f(x) = 4x − 9 and f(x) = 3. x = ?", both(sol("4x − 9", 3))), ("The point on f(x) = 2x − 1 where x = 4", f"(4, {n(ev('2x − 1', 4))})"),
        ("Higher Level: f(x) = x² + kx − 5, f(2) = 7. k = ?", n(sp.solve(sp.Eq(f_("x² + kx − 5").subs(X, 2), 7), K)[0])),
        ("Higher Level: f(x) = x², g(x) = x + 2. f(x) = g(x) when x = ?", both(sorted(Fr(str(z)) for z in sp.solve(X**2 - X - 2, X))))]
DANS = [a for k, a in DOMS]
assert DANS == ["11", "5", "−2", "7", "8", "32", "12", "−3", "−1 and 4", "1 and 5", "(2, −9)", "(1, −4)", "Linear", "Exponential", "Quadratic", "1", "3", "(4, 7)", "4", "−1 and 2"], DANS
assert len(set(DANS)) == 20
random.seed(3131); chain = DOMS[:]; random.shuffle(chain)
dom = [("START" if k == 0 else chain[k - 1][1], x[0]) for k, x in enumerate(chain)] + [(chain[-1][1], "FINISH")]
dom_print = dom[:]; random.shuffle(dom_print)
dom_html = "".join(f'<div class="dom"><div class="h l{" sm" if len(l) > 9 else ""}">{l}</div><div class="h r">{r}</div></div>' for l, r in dom_print)
chain_key = "".join(f"<li>{x} = <b>{a}</b></li>" for x, a in chain)

ERR = [("f(x) = x² + 3. f(−4) = −16 + 3", "−13", "(−4)² = 16, not −16: <b>f(−4) = 19</b>"),
       ("f(x) = 2x − 1, f(3) = 5 → the point (5, 3) is on the graph", "(5, 3)", "x comes first: <b>(3, 5)</b>"),
       ("f(x) = 3 × 2ˣ → f(3) = 3 × 2 × 3", "18", "2ˣ means 2 multiplied by itself x times: 2³ = 8, <b>f(3) = 24</b>"),
       ("Table 2, 4, 8, 16: the outputs go up, so it's linear", "linear", "The jumps (2, 4, 8) aren't the same; ×2 each time: <b>exponential</b>"),
       ("Graph of f(x) = x² − 4: solve f(x) = 0 → x = 2", "x = 2", "It crosses the x-axis twice: <b>x = −2 or x = 2</b>"),
       ("f(x) = 5x + 2 and f(x) = 17: x = 5(17) + 2", "87", "Set 5x + 2 = 17 and solve: <b>x = 3</b>")]
assert ev("x² + 3", -4) == 19 and ev("2x − 1", 3) == 5 and ev("3 × 2ˣ", 3) == 24 and tkind([2, 4, 8, 16]) == "exponential" and sol("x² − 4", 0) == [-2, 2] and sol("5x + 2", 17) == [3]
# worksheet exam-style
WT = list(range(-1, 6)); WY = [ev("x² − 4x", x) for x in WT]
assert WY == [5, 0, -3, -4, -3, 0, 5] and turn("x² − 4x") == "(2, −4)" and sol("x² − 4x", 0) == [0, 4] and [round(float(v), 1) for v in sp.solve(X**2 - 4*X - 3, X)] == [-0.6, 4.6]
assert [ev("30x − 5x²", t) for t in (1, 3)] == [25, 45] and sol("30x − 5x²", 0) == [0, 6] and sol("30x − 5x²", 40) == [2, 4]
assert sorted(sp.solve(f_("x² − 4x") - f_("x"), X)) == [0, 5] and ev("x² − 4x", 5) == 5 and [ev("4 × 2ˣ", x) for x in range(4)] == [4, 8, 16, 32]
blank = G(-1, 5, -5, 6, [], sx=34, sy=17, w=230)

pack = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Functions and Graphs Teacher Pack | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{PACK_STYLE}
{EXTRA}
.ss td:nth-child(2){{width:34%}}.ss td,.ss th{{padding:2px 5px;font-size:8.6pt;line-height:1.3}}.fym .c{{height:13mm}}.fym .fc{{font-size:12pt}}.fym .fc.sm{{font-size:8.2pt;line-height:1.2}}.idc{{padding:1mm 4mm}}.idc h3{{margin:0 0 1mm}}.p1 .proc td{{font-size:8.4pt;padding:2px 6px}}
.dom .r{{font-size:9.4pt}}.dom .l{{font-size:12pt}}.dom .l.sm{{font-size:10pt}}.ops div{{font-size:12pt}}
.big3{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:4mm;text-align:center}}.big3 div{{border-radius:14px;padding:4mm 3mm;font-size:12.5pt;line-height:1.45}}.big3 b{{display:block;font-size:16pt;margin-bottom:2mm}}
</style></head><body>

<div class="page p1">
  <div class="band"><div><div class="k">Junior Cycle Maths · Teacher pack</div><h1>Functions &amp; graphs</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2018 specification): {LO}</p>
  <div class="two">
    <div><h3>Aims</h3><p>By the end of the lesson students can say what a function is, use f(x) notation to find outputs and inputs, read roots, turning points and solutions of f(x) = k from a quadratic graph, match graphs to real situations, and tell linear, quadratic and exponential functions apart from a rule, a table or a graph. Higher Level: f(x) = g(x) from two graphs, exponential functions and "find k".</p></div>
    <div><h3>In this pack</h3><p>p.1 Teacher notes · p.2 Function Match mingle cards + Story Graph Swap A/B cards · p.3 Function Dominoes (cut-up) · p.4 Wall poster · p.5 Worksheet: Error Hunt + exam-style questions · p.6 Answers. Level: 3rd year (Higher and Ordinary). Time: about 60 minutes. All questions are original.</p></div>
  </div>
  <h2 style="margin-top:8px">Procedure</h2>
  <table class="proc"><tbody>
    <tr><td>5 min</td><td><b>Lead-in: a function machine.</b> "Give me a number." Apply a secret rule (×3, then +2) and write input → output on the board. Students guess the rule, then write it as f(x) = 3x + 2. Ask: "Could 4 ever give two different answers?" (No: that's what makes it a function.)</td></tr>
    <tr><td>8 min</td><td><b>Guided discovery.</b> Pairs make tables for x = 0 to 4 for f(x) = 3x + 1, g(x) = x² and h(x) = 2ˣ, then look at the jumps. "What happens each time x goes up by 1?" Elicit: the same jump (linear), jumps that grow evenly (quadratic), multiply by the same number (exponential). Sketch the three shapes.</td></tr>
    <tr><td>10 min</td><td><b>Function Match mingle</b> (p.2, 24 cards = 12 rule/table pairs; one card each). Rule card? Work out f(0) to f(3) and find your table. Table card? Find your rule. Warn them: several tables start the same way, so check every value.</td></tr>
    <tr><td>12 min</td><td><b>Story Graph Swap</b> (p.2, pairs, don't show your card). Each fact is on only ONE card. Ask your partner for what you're missing, then fill every blank together and sketch both graphs. Feedback: taxi f(x) = 2x + 4, 6 km costs €16, €20 goes 8 km, linear; f(x) = (x + 1)(x − 3) = x² − 2x − 3, minimum point (1, −4), f(5) = 12.</td></tr>
    <tr><td>10 min</td><td><b>Function Dominoes</b> (p.3), groups of 3–4. Start with START, answer the clue, find the domino with that answer on its left, and build the chain to FINISH. Two answers are written "−1 and 4".</td></tr>
    <tr><td>12 min</td><td><b>Worksheet</b> (p.5). Error Hunt in pairs (find the mistake, name it, fix it), then the exam-style questions alone: question 1 needs the grid. Question 4 is Higher Level.</td></tr>
    <tr><td>3 min</td><td><b>Exit ticket.</b> f(x) = x² − 5. Find f(−3), and say whether 1, 3, 9, 27 is linear, quadratic or exponential. (4; exponential.) Homework: play <b>Graph Match</b> at leim.ie/graph-match.html and copy three lines from the "Go back over these" list.</td></tr>
  </tbody></table>
  <div class="note"><b>Mingle key</b> (rule card → table card): {match_key}.<br>
  <b>Errors to look for:</b> (−3)² = −9 · points written (y, x) · 2x and 2ˣ mixed up · a quadratic graph drawn with straight lines · one answer when the curve gives two · a rule checked with the first value only. <b>Support:</b> a card with the three shapes and "same jump / even change / × same number". <b>Fast finishers:</b> invent a story for a graph that goes up, stays flat, then goes down.</div>
  <p class="small"><b>Domino answer chain</b> (START → FINISH):</p>
  <ol class="small" style="columns:2;column-gap:12px;font-size:7.2pt;line-height:1.22;margin:0;padding-left:16px">{chain_key}</ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">Cut up the cards · one Story Graph Swap card per student</div><h1>Function Match + Graph Swap</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:8.8pt;margin:0"><b>Function Match mingle.</b> Cut out the 24 cards and give one to each student. Rule card? Work out f(0), f(1), f(2) and f(3), then find your table. Table card? Find the rule that makes it. Check every value. (Fewer students? Take out whole pairs.)</p>
  <div class="fym">{match_html}</div>
  <p style="font-size:8.8pt;margin:3mm 0 0"><b>Story Graph Swap.</b> Don't show your card. Each fact is on only one of the two cards: ask your partner for what you're missing, then fill in every blank together.</p>
  {swap_card("A")}
  {swap_card("B")}
</div>

<div class="page">
  <div class="band"><div><div class="k">Groups of 3–4 · cut along the dashed lines</div><h1>Function Dominoes</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.4pt">Start with START. Answer the clue on the right, then find the domino with that answer on its left. Two answers are written "−1 and 4"; points are (x, y). Keep going until you reach FINISH. The two Higher Level clues can be given to Ordinary Level groups with their answers.</p>
  <div class="doms">{dom_html}</div>
</div>

<div class="page">
  <div class="poster">
    <h1>Functions &amp; graphs</h1>
    <div class="big3">
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Input → output</b>f(x) = 3x + 2<br>f(4) = 3(4) + 2 = 14<br>point (4, 14)</div>
      <div style="background:var(--green-soft)"><b>Read the graph</b>f(x) = 0: where it<br>crosses the x-axis<br>Turning point: top or bottom</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>A function</b>each input<br>gives exactly<br>one output</div>
    </div>
    <div class="ops">
      <div style="background:var(--green-soft)"><b>Linear</b>{G(-2, 2, -3, 6, [(lambda x: 2 * x + 1, "")], sx=22, sy=11, ly=3, w=150)}same jump: 1, 3, 5, 7</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Quadratic</b>{G(-2, 2, -3, 6, [(lambda x: x * x - 2, "")], sx=22, sy=11, ly=3, w=150)}jumps change evenly: −2, −1, 2, 7</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Exponential</b>{G(-2, 2, -3, 6, [(lambda x: 2 ** x, "")], sx=22, sy=11, ly=3, w=150)}× the same number: 1, 2, 4, 8</div>
      <div style="background:var(--green-soft)"><b>Story graphs</b>{sk("hill", w=120)}up, then down: a maximum</div>
    </div>
    <p style="text-align:center;font-size:12pt;margin:0"><b>Always:</b> (x, y) with x first · (−3)² = 9 · a smooth curve, not straight lines</p>
    <p style="text-align:center;font-size:10pt;color:var(--muted)">Léim · leim.ie · Play Graph Match: leim.ie/graph-match.html</p>
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
  <div class="gfig">{blank}</div>
  <ol class="q">
    <li>f(x) = x² − 4x. (a) Complete a table for −1 ≤ x ≤ 5. (b) Draw the graph on the grid. (c) Write down the minimum point and solve f(x) = 0. (d) Estimate where f(x) = 3.<span class="long"></span></li>
    <li>A ball's height is h = 30t − 5t² metres after t seconds. (a) Find h when t = 1 and t = 3. (b) When does it land? (c) When is it 40 m high?<span class="long"></span></li>
    <li>Is each one linear, quadratic or exponential? (a) f(x) = 7 − 2x (b) 4, 8, 16, 32 (c) f(x) = x(x + 5).<span class="long"></span></li>
    <li>Higher Level: g(x) = x. On your grid, draw g and solve f(x) = g(x). Check with algebra.<span class="long"></span></li>
  </ol>
  <div style="clear:both"></div>
</div>

<div class="page an">
  <div class="band"><div><div class="k">For the teacher</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>Story Graph Swap</h2>
  <div class="two"><table><tbody>
   <tr><td>Rule</td><td><b>f(x) = 2x + 4</b></td></tr><tr><td>Cost of 6 km</td><td><b>€16</b></td></tr><tr><td>Distance for €20</td><td>2x + 4 = 20: <b>8 km</b></td></tr><tr><td>Type</td><td><b>linear</b> (a straight line)</td></tr></tbody></table>
  <table><tbody>
   <tr><td>Brackets</td><td><b>f(x) = (x + 1)(x − 3)</b></td></tr><tr><td>Multiplied out</td><td><b>x² − 2x − 3</b></td></tr><tr><td>Minimum point</td><td><b>(1, −4)</b> (halfway between the roots)</td></tr><tr><td>f(5)</td><td>25 − 10 − 3 = <b>12</b></td></tr></tbody></table></div>
  <h2>A. Error Hunt</h2>
  <table><tbody>{"".join(f"<tr><td style='width:42%'><b>{q}</b></td><td>{r}</td></tr>" for q,w,r in ERR)}</tbody></table>
  <h2>B. Exam-style questions</h2>
  <div class="gfig">{G(-1, 5, -5, 6, [(lambda x: x * x - 4 * x, "f", -1, 5), (lambda x: x, "g", -1, 5)], sx=30, sy=15, w=200)}</div>
  <ol class="q">
    <li>(a) x = −1 to 5: {", ".join(n(v) for v in WY)} (c) minimum <b>(2, −4)</b>; f(x) = 0 at <b>x = 0 or x = 4</b> (d) about <b>x = −0.6 or x = 4.6</b></li>
    <li>(a) <b>25 m and 45 m</b> (b) 5t(6 − t) = 0: <b>t = 6 s</b> (c) t² − 6t + 8 = 0: <b>t = 2 s and t = 4 s</b></li>
    <li>(a) <b>linear</b> (b) <b>exponential</b> (×2) (c) <b>quadratic</b></li>
    <li>The graphs meet at (0, 0) and (5, 5): <b>x = 0 or x = 5</b>. Algebra: x² − 4x = x → x(x − 5) = 0 ✓</li>
  </ol>
  <div style="clear:both"></div>
  <h2>Marking tip</h2>
  <p>Give credit for a correct table, plotted points and a smooth curve, as the exam does. When reading a graph, ask students to draw the line across (or up) so you can see their method; accept estimates within half a square.</p>
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
<h1><span>Functions</span><br><span>&amp; Graphs</span></h1>
<div class="sub">Function Match mingle · Story Graph Swap A/B<br>Dominoes · Poster · Worksheet + answers</div>
<div class="em">f(x) = 3x + 2 → f(4) = 14</div></div>
<div class="foot"><span>↗ Léim · leim.ie</span><span class="price">Ready to teach · 60 min</span></div>
</body></html>"""
assert ev("3x + 2", 4) == 14

if __name__ == "__main__":
    for name, txt in [("rules-and-practice", sheet), ("teacher-pack", pack), ("cover", cover)]:
        plain = re.sub(r"<[^>]+>", " ", re.sub(r"<style>.*?</style>|<svg.*?</svg>", "", txt, flags=re.S))
        assert not re.search("[\U0001F300-\U0001FAFF\u2600-\u26FF★]", plain), (name, "emoji")
        assert not re.search(r"[\dxyt)²]\s*-\s*[\dxyt(]|[=(]\s*-\d|(?<![\w])-\d", plain), (name, re.findall(r".{20}[\dxy)]\s*-\s*[\dxy(].{10}|.{10}[=(]\s*-\d.{10}", plain)[:3])
        open(os.path.join(SRC, f"{SLUG}-{name}.html"), "w", encoding="utf-8").write(txt)
    def pdf(name, out):
        subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--no-pdf-header-footer", f"--print-to-pdf={out}",
                        f"{SLUG}-{name}.html"], cwd=SRC, check=True, capture_output=True)
        d = open(out, "rb").read(); print(name, len(re.findall(rb"/Type\s*/Page[^s]", d)), "pages")
    pdf("rules-and-practice", os.path.join(ROOT, "printables", f"{SLUG}-rules-and-practice.pdf"))
    pdf("teacher-pack", os.path.join(OUT, "Functions-and-Graphs-Teacher-Pack-Leim.pdf"))
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--hide-scrollbars", "--window-size=1200,1200",
                    f"--screenshot={os.path.join(OUT, f'{SLUG}-cover.png')}", f"{SLUG}-cover.html"], cwd=SRC, check=True, capture_output=True)
    print("domino chain:", [(x, a) for x, a in chain])
