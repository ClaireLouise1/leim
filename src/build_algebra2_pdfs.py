#!/usr/bin/env python3
"""Algebra 2: expanding & simplifying (JC Maths topic 15): free sheet + teacher pack + Payhip cover.
Run from the repo root: python3 src/build_algebra2_pdfs.py OUTDIR   (needs: pip install --break-system-packages sympy)
Writes src/algebra-expanding-simplifying-*.html; PDFs/cover PNG go to OUTDIR (free sheet also to printables/).
Every answer is computed with sympy and asserted."""
import os, sys, random, subprocess, re
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC)
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/algebra2"; os.makedirs(OUT, exist_ok=True)
SLUG = "algebra-expanding-simplifying"
LO = "AF.3a, AF.3b"
TR = standard_transformations + (implicit_multiplication_application,)
SUP = {"²": "**2", "³": "**3", "⁴": "**4"}
SYM = {c: sp.Symbol(c) for c in "abmnpqtxy"}

def E(s):
    """'(x + 3)(2x − 5)', '−3a × 2b', '(x − 4)²' → expanded sympy expression (single-letter variables)."""
    s = s.replace("−", "-").replace("×", "*").replace("□", "B")
    s = re.sub(r"([a-z0-9)])([²³⁴])", lambda m: m[1] + SUP[m[2]], s)
    s = re.sub(r"([a-z])(?=[a-z(])", r"\1*", s)
    s = s.replace(")(", ")*(")
    s = re.sub(r"(\d)\(", r"\1*(", s)
    return sp.expand(parse_expr(s, transformations=TR, local_dict=dict(SYM, B=sp.Symbol("B"))))
def eq(a, b): return sp.expand(E(a) - E(b)) == 0
def val(expr, **v): r = E(expr).subs({SYM[k]: x for k, x in v.items()}); assert r == int(r), r; return int(r)
def n(x): return ("−" + str(-x)) if x < 0 else str(x)
def nterms(s): return len(re.split(r"(?<=\S) [+−] ", s))
def simp(q, a):
    """a must equal q AND be fully expanded and simplified (no brackets, one term per power)."""
    assert eq(q, a), (q, a, E(q))
    assert "(" not in a and len(sp.Add.make_args(E(a))) == nterms(a), a
    return a

INK, YEL, MINT = "#1B2430", "#F6CF5A", "#E9F5EE"
def area(rows, cols, fill=True, h=None, q=None, card=False):
    """Area model SVG: rows/cols are term strings; cells = row × column (computed and checked)."""
    cw, rh, L, T = (52, 32, 44, 26) if card else (70, 44, 50, 26)
    fs = 21 if card else 15
    W, H = L + cw * len(cols) + 4, T + rh * len(rows) + 4
    o = ""
    for j, c in enumerate(cols): o += f'<text x="{L + cw * j + cw / 2}" y="{T - 7}" text-anchor="middle">{c}</text>'
    for i, r in enumerate(rows):
        o += f'<text x="{L - 8}" y="{T + rh * i + rh / 2 + 5}" text-anchor="end">{r}</text>'
        for j, c in enumerate(cols):
            o += f'<rect x="{L + cw * j}" y="{T + rh * i}" width="{cw}" height="{rh}" fill="{YEL if q == (i, j) else MINT if (i + j) % 2 else "#fff"}" stroke="{INK}" stroke-width="1.6"/>'
            if fill or q == (i, j):
                cell = "?" if q == (i, j) else cellstr(r, c)
                o += f'<text x="{L + cw * j + cw / 2}" y="{T + rh * i + rh / 2 + 5}" text-anchor="middle">{cell}</text>'
    st = f"height:{h};width:auto" if h else "width:100%"
    return f'<svg viewBox="0 0 {W} {H}" style="{st}"><g font-family="Inter,sans-serif" font-weight="700" font-size="{fs}" fill="{INK}">{o}</g></svg>'
CELLS = {}
def cellstr(r, c):
    s = CELLS[(r, c)]; assert eq(s, f"({r})*({c})"), (r, c, s); return s
def setcells(table):
    for (r, c), s in table.items(): CELLS[(r, c)] = s
setcells({("x", "x"): "x²", ("x", "−5"): "−5x", ("+3", "x"): "3x", ("+3", "−5"): "−15",
          ("2x", "x"): "2x²", ("2x", "+4"): "8x", ("+1", "x"): "x", ("+1", "+4"): "4"})

# ---------- free sheet ----------
A = [("3(x + 5)", "3x + 15"), ("−4(x − 2)", "−4x + 8"), ("x(x + 7)", "x² + 7x"), ("2a(3a − 5)", "6a² − 10a"),
     ("5x × 3x", "15x²"), ("−2y × 4", "−8y"), ("−(3x − 8)", "−3x + 8"), ("4ab × 3a", "12a²b")]
A = [(q, simp(q, a)) for q, a in A]
B = [("3(x + 4) + 2(x − 1)", "5x + 10"), ("5(2x − 3) − 3(x − 4)", "7x − 3"), ("7x − (2x − 5)", "5x + 5"), ("4(a + 3) − (a − 6)", "3a + 18"),
     ("2x(x + 3) + 5x", "2x² + 11x"), ("3(2y − 1) − 2(y + 4)", "4y − 11"), ("x(x − 2) − 3(x − 2)", "x² − 5x + 6"), ("6 − 2(3 − x)", "2x")]
B = [(q, simp(q, a)) for q, a in B]
C = [("(x + 3)(x + 5)", "x² + 8x + 15"), ("(x + 2)(x − 7)", "x² − 5x − 14"), ("(x − 4)(x − 6)", "x² − 10x + 24"), ("(2x + 1)(x + 3)", "2x² + 7x + 3"),
     ("(3x − 2)(x + 4)", "3x² + 10x − 8"), ("(a + 3)(b − 2)", "ab − 2a + 3b − 6"), ("(x + 5)(x − 5)", "x² − 25"), ("(2x − 3)(3x − 1)", "6x² − 11x + 3")]
C = [(q, simp(q, a)) for q, a in C]
D = [("(x + 6)²", "x² + 12x + 36"), ("(x − 5)²", "x² − 10x + 25"), ("(2x + 3)²", "4x² + 12x + 9"), ("(3x − 1)(3x + 1)", "9x² − 1")]
D = [(q, simp(q, a)) for q, a in D]
assert val("(x + 4)²", x=1) == 25 and val("x² + 16", x=1) == 17 and not eq("(x + 4)²", "x² + 16")
D += [("Ciara says (x + 4)² = x² + 16. Put in x = 1 to show she is wrong.", "(1 + 4)² = 25 but 1 + 16 = 17, so she is wrong: (x + 4)² = x² + 8x + 16"),
      ("(x + 7)(x − 2) = x² + □x − 14. What number goes in the box?", "5")]
assert sp.solve(sp.Poly(E("(x + 7)(x − 2)") - E("x² + □x − 14"), SYM["x"]).all_coeffs(), sp.Symbol("B")) == {sp.Symbol("B"): 5}
# exam-style
e1 = simp("(x + 5)(x − 3) − x(x + 1)", "x − 15")
r1, s1 = simp("(x + 7)(x + 2)", "x² + 9x + 14"), simp("(x + 4)²", "x² + 8x + 16")
assert eq(f"({s1}) − ({r1})", "2 − x") and val("(x + 7)(x + 2)", x=5) == 84 and val("(x + 4)²", x=5) == 81
assert eq("(n + 3)² − (n + 1)²", "4n + 8") and 23 ** 2 - 21 ** 2 == 4 * 20 + 8 == 88
e4 = simp("(x + 3)(x² − 2x + 4)", "x³ + x² − 2x + 12")
E4 = [("Expand and simplify (x + 5)(x − 3) − x(x + 1).", f"x² + 2x − 15 − x² − x = <b>{e1}</b>"),
      ("A rectangle is x + 7 cm long and x + 2 cm wide. A square has sides of x + 4 cm. (a) Write each area without brackets. (b) Show that the square's area minus the rectangle's area is 2 − x. (c) Which shape is bigger when x = 5?",
       f"(a) rectangle <b>{r1}</b>, square <b>{s1}</b> (b) {s1} − {r1} = <b>2 − x</b> (c) 2 − 5 = −3, so the <b>rectangle</b> is bigger by 3 cm² (84 v 81)"),
      ("(a) Show that (n + 3)² − (n + 1)² = 4n + 8. (b) Use this to work out 23² − 21² without a calculator.",
       "(a) n² + 6n + 9 − (n² + 2n + 1) = <b>4n + 8</b> (b) n = 20: 4(20) + 8 = <b>88</b>"),
      ("<i>Higher Level.</i> Expand and simplify (x + 3)(x² − 2x + 4).", f"x³ − 2x² + 4x + 3x² − 6x + 12 = <b>{e4}</b>")]

def qs(items): return "".join(f"<li>{q} <span class='line'></span></li>" for q, a in items)
rule_area = area(["x", "+3"], ["x", "−5"], h="27mm")
sheet = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Algebra: expanding and simplifying, rules and practice | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>@page{{@bottom-left{{content:"Léim · leim.ie · Free to print for home or class · JC Maths LOs (2018 spec): {LO}"}}}}
.tight{{font-size:11pt;line-height:1.5}}.tight td,.tight th{{padding:3px 6px}}.tight h2{{margin:12px 0 5px;font-size:14pt}}.tight .note,.tight .tip{{padding:6px 10px;margin:6px 0}}.tight p{{margin:3px 0}}
ol.q{{padding-left:30px}}ol.q li{{margin:7px 0}}
.ans td{{padding:3px 6px;font-size:9.2pt}}
.p2{{font-size:9.5pt;line-height:1.36}}.p2 ol.q li{{margin:5px 0}}.p2 h2{{margin:8px 0 4px;font-size:13pt}}.p2 .line{{min-width:70px}}
.am{{display:flex;gap:4mm;align-items:center}}
</style></head><body>
<div class="page tight">
  <div class="band"><div><div class="k">Junior Cycle Maths · Free revision sheet</div><h1>Expanding &amp; simplifying</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2018 specification): {LO}. Play the game: <b>leim.ie/bracket-blaster.html</b></p>
  <div class="two">
   <div><h2>1. Multiplying terms</h2>
    <p>Numbers × numbers, letters × letters: 3x × 4x = <b>12x²</b> · 2a × 5b = <b>10ab</b> · x² × x = <b>x³</b> (add the powers). Same signs give +, different signs give −.</p>
    <h2>2. One bracket</h2>
    <p>Multiply <b>every</b> term inside:</p>
    <table><tbody><tr><td>3(x − 4)</td><td><b>3x − 12</b> (not 3x − 4)</td></tr><tr><td>−2(x − 5)</td><td><b>−2x + 10</b> (− × − = +)</td></tr>
    <tr><td>x(x + 3)</td><td><b>x² + 3x</b></td></tr><tr><td>−(x − 6)</td><td><b>−x + 6</b> (every sign changes)</td></tr></tbody></table>
    <h2>3. Expand, then simplify</h2>
    <p>3(x + 2) − 2(x − 4)<br>= 3x + 6 − 2x + 8<br>= <b>x + 14</b> (collect like terms last)</p>
    <h2>4. Squares</h2>
    <p>(x + 4)² = (x + 4)(x + 4) = <b>x² + 8x + 16</b><br>(x − 3)² = x² − 6x + 9 (not x² − 9 or x² + 9)<br>(2x + 5)² = <b>4x² + 20x + 25</b></p></div>
   <div><h2>5. Double brackets: the area model</h2>
    <p>Every term × every term. One bracket along the top, one down the side; each box = row × column; add the boxes.</p>
    <div class="am">{rule_area}<p>(x + 3)(x − 5)<br>= x² − 5x + 3x − 15<br>= <b>x² − 2x − 15</b></p></div>
    <p><b>Spot the pattern:</b> (x + a)(x + b) = x² + (a + b)x + ab. The middle number is the two numbers added, the last is the two multiplied: (x + 6)(x − 2) = x² + 4x − 12.</p>
    <p>(2x + 1)(x − 4) = 2x² − 8x + x − 4 = <b>2x² − 7x − 4</b><br>(a + 2)(b − 3) = <b>ab − 3a + 2b − 6</b> (no like terms)</p>
    <h2>6. Difference of two squares</h2>
    <p>(x + 7)(x − 7) = x² − 7x + 7x − 49 = <b>x² − 49</b>: the middle terms cancel.</p>
    <h2>7. Higher Level: three terms</h2>
    <p>(x + 2)(x² − x + 3) = x³ − x² + 3x + 2x² − 2x + 6 = <b>x³ + x² + x + 6</b></p></div>
  </div>
  <div class="tip"><b>Exam tip:</b> write all four terms of a double bracket before you collect, and write (x + 3)² as (x + 3)(x + 3) first. <b>Check with a number:</b> put x = 1 into the question and your answer: they must give the same value.</div>
</div>

<div class="page p2">
  <div class="band"><div><div class="k">Practice · 34 questions</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <div class="two"><div><h2>A. Expand (multiply out)</h2><ol class="q">{qs(A)}</ol></div>
  <div><h2>B. Expand and simplify</h2><ol class="q" start="9">{qs(B)}</ol></div></div>
  <div class="two"><div><h2>C. Double brackets</h2><ol class="q" start="17">{qs(C)}</ol></div>
  <div><h2>D. Squares and special products</h2><ol class="q" start="25">{qs(D)}</ol></div></div>
  <p class="small" style="margin-top:6px">Questions 31–34 are on the next page.</p>
</div>

<div class="page">
  <div class="band"><div><div class="k">Exam-style · then check</div><h1>Exam corner + answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>E. Exam-style questions (show your work)</h2>
  <ol class="q" start="31">{"".join(f"<li>{q}<span class='long'></span><span class='long'></span></li>" for q,a in E4)}</ol>
  <h2 style="margin-top:12px">Answers</h2>
  <table class="ans"><tbody>
   <tr><td><b>A</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(A,1))}</td></tr>
   <tr><td><b>B</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(B,9))}</td></tr>
   <tr><td><b>C</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(C,17))}</td></tr>
   <tr><td><b>D</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(D,25))}</td></tr>
   <tr><td><b>E</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(E4,31))}</td></tr>
  </tbody></table>
  <div class="note"><b>Got one wrong?</b> Check: did you multiply <b>every</b> term in the bracket? Did a minus in front of a bracket change every sign inside? Did your double bracket have four terms before you collected? Did you keep the middle term in a square? Then play <b>Bracket Blaster</b> at leim.ie/bracket-blaster.html: the "Go back over these" list at the end shows the rule for each mistake.</div>
  <p class="small">All questions written by Léim. Léim is independent and not connected with the State Examinations Commission or the NCCA.</p>
</div>
</body></html>"""

# ---------- teacher pack ----------
# Bracket Relay: each runner works on the previous runner's answer
RELAY = {
 "A": [("Expand and simplify (x + 3)(x + 2).", "(x + 3)(x + 2)", "x² + 5x + 6"),
       ("Take your answer and subtract x(x + 1). Simplify.", "x² + 5x + 6 − x(x + 1)", "4x + 6"),
       ("Multiply your answer by 2, then add 3(x − 4). Simplify.", "2(4x + 6) + 3(x − 4)", "11x"),
       ("Find the value of your answer when x = −3.", None, "−33")],
 "B": [("Expand and simplify (x − 4)².", "(x − 4)²", "x² − 8x + 16"),
       ("Take your answer and add 2x(x + 4). Simplify.", "x² − 8x + 16 + 2x(x + 4)", "3x² + 16"),
       ("Take your answer and subtract (x + 4)(x − 4). Simplify.", "3x² + 16 − (x + 4)(x − 4)", "2x² + 32"),
       ("Find the value of your answer when x = −2.", None, "40")]}
for k, steps in RELAY.items():
    prev = None
    for q, ex, a in steps:
        if ex: simp(ex, a); prev = a
        else: assert int(E(prev).subs(SYM["x"], -3 if k == "A" else -2)) == int(a.replace("−", "-")), (k, a)
    assert steps[1][1].startswith(steps[0][2]) and steps[2][1].count(steps[1][2]) == 1
# Area Model Match: 12 pairs; 6 picture cards (area models with the sides only) + 6 bracket cards
PICS = [(["x", "+4"], ["x", "+2"]), (["x", "−3"], ["x", "+5"]), (["2x", "+1"], ["x", "+3"]), (["x", "+6"], ["x", "−6"]), (["x", "−2"], ["x", "−2"]), (["3"], ["x", "−7"])]
PIC_ANS = ["x² + 6x + 8", "x² + 2x − 15", "2x² + 7x + 3", "x² − 36", "x² − 4x + 4", "3x − 21"]
for (r, c), a in zip(PICS, PIC_ANS): simp("(" + " ".join(r).replace("+", "+ ").replace("−", "− ").strip() + ")*(" + " ".join(c).replace("+", "+ ").replace("−", "− ") + ")", a)
TXT = [("(x + 5)(x + 1)", "x² + 6x + 5"), ("(x − 4)(x − 3)", "x² − 7x + 12"), ("(x + 7)(x − 2)", "x² + 5x − 14"), ("(x + 3)²", "x² + 6x + 9"),
       ("x(x − 8)", "x² − 8x"), ("−2(x − 5)", "−2x + 10")]
TXT = [(q, simp(q, a)) for q, a in TXT]
MATCH = [(area(r, c, fill=False, h="19mm", card=True), a) for (r, c), a in zip(PICS, PIC_ANS)] + TXT
answers = [a for q, a in MATCH]; assert len(set(answers)) == 12 and len(set(str(E(s)) for s in answers)) == 12
cards = [q for q, a in MATCH] + [a for q, a in MATCH]
random.seed(15); match_print = cards[:]; random.shuffle(match_print)
def nw(q): return re.sub(r"(\S*\([^)]*\)\S*)", r'<span style="white-space:nowrap">\1</span>', q)
def fc(x): return x if x.startswith("<svg") else f'<div class="fc{" md" if len(x) > 13 else ""}">{x}</div>'
match_html = "".join(f'<div class="c"><span class="tag">Card {i}</span>{fc(x)}</div>' for i, x in enumerate(match_print, 1))
def picname(r, c): return "(" + " ".join(r).replace(" +", " + ").replace(" −", " − ") + ")(" + " ".join(c).replace(" +", " + ").replace(" −", " − ") + ")"
match_key = " · ".join(f"{('picture ' + picname(*PICS[i])) if q.startswith('<svg') else q} → <b>{a}</b>" for i, (q, a) in enumerate(MATCH))

DOMS = [("Expand 3(x + 4)", "3x + 12"), ("Expand −2(x − 5)", "−2x + 10"), ("Expand x(x + 6)", "x² + 6x"), ("4x × 3x", "12x²"),
        ("−3a × 2b", "−6ab"), ("Expand 5(2x − 1)", "10x − 5"), ("Simplify 2(x + 3) + 3(x − 1)", "5x + 3"), ("Simplify 4(x + 2) − 2(x + 1)", "2x + 6"),
        ("Simplify 9x − (4x + 2)", "5x − 2"), ("Expand (x + 2)(x + 5)", "x² + 7x + 10"), ("Expand (x + 4)(x − 3)", "x² + x − 12"), ("Expand (x − 2)(x − 6)", "x² − 8x + 12"),
        ("Expand (2x + 1)(x + 3)", "2x² + 7x + 3"), ("Expand (x + 5)²", "x² + 10x + 25"), ("Expand (x − 4)²", "x² − 8x + 16"), ("Expand (x + 9)(x − 9)", "x² − 81"),
        ("(x + 3)(x − 7) = x² + □x − 21. □ = ?", "−4"), ("Expand (a + 2)(b + 3)", "ab + 3a + 2b + 6"), ("(x + 2)(x − 1) when x = −3", "4"), ("Area: sides x + 1 and x + 6", "x² + 7x + 6")]
for q, a in DOMS:
    if q.startswith("(x + 3)(x − 7)"): assert sp.solve(sp.Poly(E("(x + 3)(x − 7)") - E("x² + □x − 21"), SYM["x"]).all_coeffs(), sp.Symbol("B")) == {sp.Symbol("B"): -4}
    elif "when x = −3" in q: assert val("(x + 2)(x − 1)", x=-3) == 4
    elif q.startswith("Area"): simp("(x + 1)(x + 6)", a)
    else: simp(re.sub(r"^(Expand|Simplify) ", "", q), a)
ANS = [a for q, a in DOMS]; assert len(set(ANS)) == 20 and len(set(str(E(a.replace("□", "0"))) for a in ANS)) == 20
random.seed(1515); chain = DOMS[:]; random.shuffle(chain)
dom = [("START" if k == 0 else chain[k - 1][1], x[0]) for k, x in enumerate(chain)] + [(chain[-1][1], "FINISH")]
dom_print = dom[:]; random.shuffle(dom_print)
dom_html = "".join(f'<div class="dom"><div class="h l{" sm" if len(l) > 11 else ""}">{l}</div><div class="h r">{r}</div></div>' for l, r in dom_print)
chain_key = "".join(f"<li>{x} = <b>{a}</b></li>" for x, a in chain)

ERR = [("Expand 4(x + 3)", "= 4x + 3", "The 4 multiplies both terms: <b>4x + 12</b>"),
       ("Expand −3(x − 2)", "= −3x − 6", "−3 × −2 = +6: <b>−3x + 6</b>"),
       ("Expand (x + 5)²", "= x² + 25", "(x + 5)(x + 5) has middle terms: <b>x² + 10x + 25</b>"),
       ("Expand x(x + 2)", "= x² + 2", "x × 2 = 2x: <b>x² + 2x</b>"),
       ("Expand (x + 3)(x − 4)", "= x² − x + 12", "3 × −4 = −12: <b>x² − x − 12</b>"),
       ("2x × 3x", "= 6x", "x × x = x²: <b>6x²</b>")]
for q, w, r in ERR:
    qq = q.replace("Expand ", ""); wrong = w.replace("= ", ""); right = re.findall(r"<b>(.+?)</b>", r)[-1]
    assert not eq(qq, wrong) and simp(qq, right)
w1 = simp("3(2x − 5) − 4(x − 3)", "2x − 3"); w2 = simp("(x − 7)(x + 2)", "x² − 5x − 14")
w3 = simp("(2x − 3)²", "4x² − 12x + 9"); assert eq("(2x − 3)² − (2x + 3)²", "−24x")
w4 = simp("(x + 5)² − x²", "10x + 25"); assert val(w4, x=3) == 55 == 8 ** 2 - 3 ** 2
w5 = simp("(x + 1)(x² + 3x − 2)", "x³ + 4x² + x − 2")
assert simp("2(x − 3) − (x − 5)", "x − 1") and simp("(x − 6)²", "x² − 12x + 36") and (20 + 3) * (10 + 4) == 200 + 80 + 30 + 12 == 322

pack_style = open(os.path.join(SRC, "build_ratio_pdfs.py"), encoding="utf-8").read()
pack_style = pack_style[pack_style.index("<style>", pack_style.index('pack = f"""')) + 7:pack_style.index("</style>", pack_style.index('pack = f"""'))]
pack_style = pack_style.replace("{{", "{").replace("}}", "}").replace("{LO}", LO)
pack_style += (".fym .c{height:25mm}.fym .fc.md{font-size:15pt}.fym svg{margin-top:2mm}.trk{border:2px dashed #9AA3AE;padding:2.5mm 4mm;margin-top:2mm;font-size:9.4pt}.trk ol{margin:1mm 0 0;padding-left:18px}.trk li{margin:1.6mm 0}"
               ".relays{display:grid;grid-template-columns:1fr 1fr;gap:3mm}.dom .l{font-size:12pt}.dom .l.sm{font-size:9.6pt;line-height:1.2}")
pack = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Algebra: Expanding and Simplifying Teacher Pack | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{pack_style}</style></head><body>

<div class="page p1">
  <div class="band"><div><div class="k">Junior Cycle Maths · Teacher pack</div><h1>Expanding &amp; simplifying</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2018 specification): {LO} (factorising comes later in Algebra 3, AF.3d; dividing and algebraic fractions in Algebra 4, AF.3a/AF.3c)</p>
  <div class="two">
    <div><h3>Aims</h3><p>By the end of the lesson students can multiply terms; expand a single bracket (including a negative or a letter outside); expand and simplify sums and differences of brackets; expand double brackets with the area model; square a bracket; and recognise the difference of two squares. Higher Level: a bracket with three terms.</p></div>
    <div><h3>In this pack</h3><p>p.1 Teacher notes · p.2 Bracket Relay + Area Model Match cards · p.3 Expanding Dominoes (cut-up) · p.4 Wall poster · p.5 Worksheet: Error Hunt + exam-style questions · p.6 Answers. Level: 2nd year (Higher and Ordinary), or 3rd-year revision. Time: about 60 minutes. All questions are original.</p></div>
  </div>
  <h2 style="margin-top:8px">Procedure</h2>
  <table class="proc"><tbody>
    <tr><td>6 min</td><td><b>Lead-in: 23 × 14 without a calculator.</b> Draw a rectangle split into (20 + 3) by (10 + 4): 200 + 80 + 30 + 12 = 322. Then swap 20 for x: (x + 3)(x + 4). Pairs fill the four boxes: x² + 4x + 3x + 12 = x² + 7x + 12.</td></tr>
    <tr><td>8 min</td><td><b>Guided discovery.</b> Pairs expand (x + 2)(x + 3), (x + 4)(x + 1), (x + 5)(x + 2), (x + 6)(x − 2) with the area model. Where do the middle and last numbers come from? (Added; multiplied.) Then test the claim "(x + 3)² = x² + 9" with x = 1 and draw its area model: which boxes are missing?</td></tr>
    <tr><td>10 min</td><td><b>Area Model Match</b> (p.2, 24 cards = 12 pairs; one card each). Picture and bracket cards find their expansion. Pairs check by putting x = 1 into both cards. Feedback: why is (x + 6)(x − 6) only two terms?</td></tr>
    <tr><td>10 min</td><td><b>Bracket Relay</b> (p.2), teams of 4 in a line. Runner 1 does step 1 and passes the answer (not the card) to runner 2, and so on. The last runner brings the final number to you: if it's wrong, the team finds the broken step.</td></tr>
    <tr><td>10 min</td><td><b>Expanding Dominoes</b> (p.3), groups of 3–4: start with START, work out the clue, find the domino with that answer on its left and build the chain to FINISH.</td></tr>
    <tr><td>13 min</td><td><b>Worksheet</b> (p.5). Error Hunt in pairs (find the mistake, name the rule, fix it), then the exam-style questions alone.</td></tr>
    <tr><td>3 min</td><td><b>Exit ticket.</b> Expand and simplify 2(x − 3) − (x − 5); expand (x − 6)² (x − 1; x² − 12x + 36). Homework: play <b>Bracket Blaster</b> at leim.ie/bracket-blaster.html (Spot the slip round) and copy three lines from the "Go back over these" list.</td></tr>
  </tbody></table>
  <div class="note"><b>Area Model Match key:</b> {match_key}.<br>
  <b>Errors to look for:</b> 3(x + 4) = 3x + 4 · −2(x − 5) = −2x − 10 · −(x − 6) = −x − 6 · x(x + 3) = x² + 3 · 2x × 3x = 6x · (x + 3)² = x² + 9 · (x + 3)(x − 4) with +12 at the end · collecting x² with x. <b>Support:</b> draw the area model every time; check with x = 1. <b>Fast finishers:</b> (x + 1)(x² + 3x − 2), or explain why (n + 1)² − n² is always odd.</div>
  <p class="small"><b>Bracket Relay answers:</b> A: {" → ".join(a for q, e, a in RELAY["A"])} · B: {" → ".join(a for q, e, a in RELAY["B"])}. <b>Domino answer chain</b> (START → FINISH):</p>
  <ol class="small" style="columns:2;column-gap:12px;font-size:7.6pt;line-height:1.3;margin:0;padding-left:16px">{chain_key}</ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">One relay per team of 4 · one match card per student</div><h1>Bracket Relay + Area Model Match</h1></div><div class="logo">↗ Léim</div></div>
  <div class="relays">{"".join(f'<div class="trk"><b>Bracket Relay {k}.</b> Cut into 4 strips. Each runner uses the answer passed to them.<ol>' + "".join(f"<li><b>Runner {i}:</b> {nw(q)}</li>" for i, (q, e, a) in enumerate(st, 1)) + "</ol></div>" for k, st in RELAY.items())}</div>
  <p style="font-size:9.5pt;margin:3mm 0 0"><b>Area Model Match.</b> Cut out the 24 cards and give one to each student. Picture or bracket card? Find the person with your expansion. Expansion card? Find your picture or brackets. Check by putting x = 1 into both cards. (Fewer students? Take out whole pairs.)</p>
  <div class="fym">{match_html}</div>
</div>

<div class="page">
  <div class="band"><div><div class="k">Groups of 3–4 · cut along the dashed lines</div><h1>Expanding Dominoes</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.5pt">Start with START. Work out the clue on the right, then find the domino with that answer on its left. Keep going until you reach FINISH. No calculators!</p>
  <div class="doms">{dom_html}</div>
</div>

<div class="page">
  <div class="poster">
    <h1>Expanding brackets</h1>
    <div class="big3"><div>3(x − 4)<span>= 3x − 12</span></div><div>−(x − 6)<span>= −x + 6</span></div><div>(x + 3)²<span>= x² + 6x + 9</span></div></div>
    <div style="display:flex;justify-content:center">{area(["x", "+3"], ["x", "−5"], h="48mm")}</div>
    <p style="text-align:center;font-size:13pt;margin:0"><b>(x + 3)(x − 5) = x² − 5x + 3x − 15 = x² − 2x − 15</b></p>
    <div class="ops">
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>One bracket</b>multiply EVERY term<br>−2(x − 5) = −2x + 10</div>
      <div style="background:var(--green-soft)"><b>Two brackets</b>every term × every term<br>4 boxes, then collect</div>
      <div style="background:var(--green-soft)"><b>Squares</b>(x − 4)² = (x − 4)(x − 4)<br>= x² − 8x + 16</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Difference of squares</b>(x + 7)(x − 7)<br>= x² − 49</div>
    </div>
    <p style="text-align:center;font-size:12pt;margin:0"><b>Check:</b> put x = 1 into the question and your answer</p>
    <p style="text-align:center;font-size:10pt;color:var(--muted)">Léim · leim.ie · Play Bracket Blaster: leim.ie/bracket-blaster.html</p>
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
    <li>Expand and simplify 3(2x − 5) − 4(x − 3).<span class="long"></span></li>
    <li>Expand and simplify (x − 7)(x + 2).<span class="long"></span></li>
    <li>(a) Expand (2x − 3)². (b) Show that (2x − 3)² − (2x + 3)² = −24x.<span class="long"></span><span class="long"></span></li>
    <li>A square tile has sides of x + 5 cm. A square hole with sides of x cm is cut out of the middle. (a) Show that the area left is 10x + 25 cm². (b) Find the area left when x = 3, and check it using the side lengths.<span class="long"></span><span class="long"></span></li>
    <li><i>Higher Level.</i> Expand and simplify (x + 1)(x² + 3x − 2).<span class="long"></span></li>
  </ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">For the teacher</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>Bracket Relay</h2>
  <ol class="q">
    <li><b>Relay A:</b> {" → ".join(a for q, e, a in RELAY["A"])} (11(−3) = −33)</li>
    <li><b>Relay B:</b> {" → ".join(a for q, e, a in RELAY["B"])} (2(4) + 32 = 40)</li>
  </ol>
  <h2>A. Error Hunt</h2>
  <table><tbody>{"".join(f"<tr><td style='width:34%'><b>{q}</b> {w}</td><td>{r}</td></tr>" for q,w,r in ERR)}</tbody></table>
  <h2>B. Exam-style questions</h2>
  <ol class="q">
    <li>6x − 15 − 4x + 12 = <b>{w1}</b> (−4 × −3 = +12)</li>
    <li>x² + 2x − 7x − 14 = <b>{w2}</b></li>
    <li>(a) (2x − 3)(2x − 3) = 4x² − 6x − 6x + 9 = <b>{w3}</b> (b) (2x + 3)² = 4x² + 12x + 9; 4x² − 12x + 9 − 4x² − 12x − 9 = <b>−24x</b></li>
    <li>(a) (x + 5)² − x² = x² + 10x + 25 − x² = <b>{w4}</b> (b) 10(3) + 25 = <b>55 cm²</b>; check: 8 × 8 − 3 × 3 = 64 − 9 = 55 ✓</li>
    <li>x³ + 3x² − 2x + x² + 3x − 2 = <b>{w5}</b></li>
  </ol>
  <h2>Marking tip</h2>
  <p>Give credit for each step, as the exam does: the line with all four terms of a double bracket earns marks even if the collecting slips. Accept the terms in any order (−2x + 10 = 10 − 2x), but the answer must have no brackets and no like terms left.</p>
</div>
</body></html>"""

cover = """<!doctype html><html><head><meta charset="utf-8"><style>
body{margin:0;width:1200px;height:1200px;background:#1B2430;font-family:Inter,sans-serif;color:#fff;display:flex;flex-direction:column;justify-content:space-between;padding:90px;box-sizing:border-box}
.k{display:inline-block;background:#2E7D57;border-radius:99px;padding:12px 26px;font-weight:700;font-size:28px;letter-spacing:.06em;text-transform:uppercase}
h1{font-size:104px;font-weight:800;line-height:1.12;letter-spacing:-.03em;margin:40px 0 0}
h1 span{background:#F6CF5A;color:#1B2430;padding:0 14px;box-decoration-break:clone;-webkit-box-decoration-break:clone}
.sub{font-size:38px;color:#C9D1DA;margin-top:36px;line-height:1.35}
.em{font-size:50px;margin-top:30px;font-weight:800;letter-spacing:.01em;color:#F6CF5A}
.foot{display:flex;justify-content:space-between;align-items:center;font-size:34px;font-weight:700}
.price{background:#F6CF5A;color:#1B2430;border-radius:16px;padding:14px 28px}
</style></head><body>
<div><span class="k">Junior Cycle Maths · Teacher pack</span>
<h1><span>Expanding &amp;</span><br><span>Simplifying</span></h1>
<div class="sub">Bracket Relay · Area Model Match<br>Expanding Dominoes · Poster · Worksheet + answers</div>
<div class="em">(x + 3)² = x² + 6x + 9 &nbsp;·&nbsp; not x² + 9</div></div>
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
    pdf("teacher-pack", os.path.join(OUT, "Expanding-and-Simplifying-Teacher-Pack-Leim.pdf"))
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--hide-scrollbars", "--window-size=1200,1200",
                    f"--screenshot={os.path.join(OUT, f'{SLUG}-cover.png')}", f"{SLUG}-cover.html"], cwd=SRC, check=True, capture_output=True)
    print("domino chain:", [(x, a) for x, a in chain])
