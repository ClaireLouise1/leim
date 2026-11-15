#!/usr/bin/env python3
"""Algebra 1: variables & expressions (JC Maths topic 8): free sheet + teacher pack + Payhip cover.
Run from the repo root: python3 src/build_algebra1_pdfs.py OUTDIR   (needs: pip install --break-system-packages sympy)
Writes src/algebra-variables-expressions-*.html; PDFs/cover PNG go to OUTDIR (free sheet also to printables/).
Every answer is computed with sympy and asserted."""
import os, sys, random, subprocess, re
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC)
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/algebra1"; os.makedirs(OUT, exist_ok=True)
SLUG = "algebra-variables-expressions"
LO = "AF.2a, AF.2b, AF.3a, U.4"
TR = standard_transformations + (implicit_multiplication_application,)
SUP = {"²": "**2", "³": "**3", "⁴": "**4"}
SYM = {c: sp.Symbol(c) for c in "abcdmnpqtxy"}

def E(s):
    """'3x² − 2xy + 5' → sympy expression (single-letter variables)."""
    s = s.replace("−", "-").replace("×", "*").replace("÷", "/")
    s = re.sub(r"([a-z0-9)])([²³⁴])", lambda m: m[1] + SUP[m[2]], s)
    s = re.sub(r"([a-z])(?=[a-z])", r"\1*", s)
    return sp.expand(parse_expr(s, transformations=TR, local_dict=SYM))
def eq(a, b): return sp.expand(E(a) - E(b)) == 0
def val(expr, **v): r = E(expr).subs({SYM[k]: x for k, x in v.items()}); assert r == int(r), r; return int(r)
def n(x): return ("−" + str(-x)) if x < 0 else str(x)
def nterms(s): return len(re.split(r" [+−] ", s.lstrip("−")))
def simp(q, a):
    assert eq(q, a), (q, a)
    assert len(sp.Add.make_args(E(a))) == nterms(a), a   # the answer is fully simplified
    return a

# ---------- free sheet ----------
A = [("5x + 3x", "8x"), ("7a − 2a + a", "6a"), ("4x + 3y − x + 2y", "3x + 5y"), ("6m − 2n − 4m + 5n", "2m + 3n"),
     ("3p − 5 + 2p + 9", "5p + 4"), ("x² + 4x + 2x² − x", "3x² + 3x"), ("5ab + 2a − 3ab + a", "2ab + 3a"), ("8 − 3t − 2 + 5t", "2t + 6")]
A = [(q, simp(q, a)) for q, a in A]
B = [("7 more than n", "n + 7", "n+7"), ("4 less than x", "x − 4", "x-4"), ("n multiplied by 6", "6n", "6*n"),
     ("Double y, then add 9", "2y + 9", "2*y+9"), ("Half of p", "p/2", "p/2"), ("Subtract t from 10", "10 − t", "10-t"),
     ("Pens cost €2 each. A pencil case costs €5. Write the cost, in euro, of the case and n pens.", "2n + 5", "2*n+5"),
     ("A rectangle has length 3x and width x + 2. Write its perimeter in its simplest form.", "8x + 4", "2*(3*x)+2*(x+2)")]
for q, a, chk in B: assert sp.expand(sp.sympify(chk, locals=SYM) - E(a)) == 0, q
B = [(q, a) for q, a, c in B]
Cq = [("4x + 5 when x = 2", n(val("4x + 5", x=2))), ("4x + 5 when x = −2", n(val("4x + 5", x=-2))), ("10 − 3x when x = −4", n(val("10 − 3x", x=-4))),
      ("x² when x = −5", n(val("x²", x=-5))), ("2x² when x = −3", n(val("2x²", x=-3))), ("ab when a = −3 and b = 4", n(val("ab", a=-3, b=4))),
      ("3a − 2b when a = −1 and b = −5", n(val("3a − 2b", a=-1, b=-5))), ("a² + b² when a = −2 and b = 3", n(val("a² + b²", a=-2, b=3)))]
assert [a for q, a in Cq] == ["13", "−3", "22", "25", "18", "−12", "7", "13"], [a for q, a in Cq]
D = [("How many terms are in 5x² − 3x + 7?", str(len(sp.Add.make_args(E("5x² − 3x + 7"))))),
     ("What is the coefficient of x in 5x² − 3x + 7?", n(int(sp.Poly(E("5x² − 3x + 7")).coeff_monomial(SYM["x"])))),
     ("What is the constant term in 5x² − 3x + 7?", n(int(sp.Poly(E("5x² − 3x + 7")).coeff_monomial(1)))),
     ("Write y × y × y the short way.", "y³"),
     ("Seán says 2x + 3y = 5xy. Is he right? Explain.", "No: 2x and 3y are not like terms, so 2x + 3y can't be simplified"),
     ("Which is a like term to 4ab: 4a, 7ba, ab², 4b?", "7ba")]
assert [a for q, a in D][:4] == ["3", "−3", "7", "y³"] and eq("y × y × y", "y³") and not eq("2x + 3y", "5xy")
assert [o for o in ["4a", "7ba", "ab²", "4b"] if (E(o) / E("4ab")).is_number] == ["7ba"]
# exam-style
assert simp("6x − 2y + 3x + 5y", "9x + 3y") and simp("3n² + 2n − n² − 7n + 4", "2n² − 5n + 4")
e2 = [val("2p + 5q", p=-3, q=2), val("p² − q", p=-3, q=2), val("pq − q²", p=-3, q=2)]; assert e2 == [4, 7, -10]
e3 = [val("12m + 30", m=12), 15 * 12]; assert e3 == [174, 180]
e4p = "6x + 3"; assert eq("(x + 4) + (2x − 1) + 3x", e4p) and val(e4p, x=5) == 33 and [val(s, x=5) for s in ("x + 4", "2x − 1", "3x")] == [9, 9, 15]
E4 = [("Simplify (a) 6x − 2y + 3x + 5y (b) 3n² + 2n − n² − 7n + 4", "(a) <b>9x + 3y</b> (b) <b>2n² − 5n + 4</b>"),
      ("p = −3 and q = 2. Find the value of (a) 2p + 5q (b) p² − q (c) pq − q²", f"(a) −6 + 10 = <b>{n(e2[0])}</b> (b) 9 − 2 = <b>{n(e2[1])}</b> (c) −6 − 4 = <b>{n(e2[2])}</b>"),
      ("A gym charges a €30 joining fee plus €12 a month. (a) Write an expression for the cost, in euro, of m months. (b) Find the cost of one year. (c) Another gym charges €15 a month with no joining fee. Which gym is cheaper for one year?",
       f"(a) <b>12m + 30</b> (b) 12(12) + 30 = <b>€{e3[0]}</b> (c) €15 × 12 = €{e3[1]}, so the <b>first gym</b> is cheaper"),
      ("A triangle has sides x + 4, 2x − 1 and 3x cm. (a) Write the perimeter in its simplest form. (b) Find the perimeter when x = 5. (c) How long is the longest side when x = 5?",
       f"(a) <b>{e4p}</b> cm (b) 6(5) + 3 = <b>33 cm</b> (c) the sides are 9, 9 and 15: <b>15 cm</b>")]

def qs(items): return "".join(f"<li>{q} <span class='line'></span></li>" for q, a in items)
sheet = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Algebra: variables and expressions, rules and practice | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>@page{{@bottom-left{{content:"Léim · leim.ie · Free to print for home or class · JC Maths LOs (2018 spec): {LO}"}}}}
.tight{{font-size:10.1pt;line-height:1.42}}.tight td,.tight th{{padding:3px 6px}}.tight h2{{margin:9px 0 5px;font-size:13.5pt}}.tight .note,.tight .tip{{padding:6px 10px;margin:6px 0}}
ol.q{{padding-left:30px}}ol.q li{{margin:7px 0}}
.ans td{{padding:3px 6px;font-size:9.2pt}}
.p2{{font-size:9.5pt;line-height:1.36}}.p2 ol.q li{{margin:4px 0}}.p2 h2{{margin:8px 0 4px;font-size:13pt}}.p2 .line{{min-width:70px}}
</style></head><body>
<div class="page tight">
  <div class="band"><div><div class="k">Junior Cycle Maths · Free revision sheet</div><h1>Variables &amp; expressions</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2018 specification): {LO}. Play the game: <b>leim.ie/like-term-sweep.html</b></p>
  <div class="two">
   <div><h2>1. The words</h2>
    <p>A <b>variable</b> is a letter standing for a number that can change. An <b>expression</b> is made of <b>terms</b> joined by + and − signs: 4x² − 3x + 7 has <b>3 terms</b>. The <b>coefficient</b> of x is the number in front, sign included: <b>−3</b>. The <b>constant</b> is the term with no letter: <b>7</b>.</p>
    <h2>2. Writing it the short way</h2>
    <table><tbody><tr><td>3 × n</td><td><b>3n</b></td><td>n × n</td><td><b>n²</b></td></tr><tr><td>a × b</td><td><b>ab</b></td><td>n ÷ 2</td><td><b>n/2</b></td></tr><tr><td>n + n + n</td><td><b>3n</b></td><td>1x</td><td><b>x</b></td></tr></tbody></table>
    <h2>3. Collecting like terms</h2>
    <p><b>Like terms</b> have exactly the same letters and powers (3x and −5x; xy and yx). 3x and 3x² are <b>not</b> like terms. Each term keeps the sign in <b>front</b> of it.</p>
    <p>5a + 3b − 2a + b = <b>3a + 4b</b><br>2x² + 5x − x² − 8x + 3 = <b>x² − 3x + 3</b><br>x² + x² = 2x² (not x⁴) · 3x + 2y can't be simplified</p></div>
   <div><h2>4. Words into algebra</h2>
    <p>"5 more than n" → <b>n + 5</b> · "5 less than n" → <b>n − 5</b> (not 5 − n) · "double n, then subtract 3" → <b>2n − 3</b> · "half of n" → <b>n/2</b>.</p>
    <p>Tickets at €8 each plus a €3 booking fee: n tickets cost <b>8n + 3</b> (the fee is paid once). Perimeter: add <b>all</b> the sides.</p>
    <h2>5. Substitution</h2>
    <p>Put each number in <b>brackets</b>, then follow BIMDAS.</p>
    <table><thead><tr><th>Find</th><th>Working</th></tr></thead><tbody>
     <tr><td>5 − 2x, x = −3</td><td>5 − 2(−3) = 5 + 6 = <b>11</b></td></tr>
     <tr><td>x², x = −4</td><td>(−4)² = <b>16</b> (not −16)</td></tr>
     <tr><td>3x², x = −2</td><td>3 × 4 = <b>12</b> (square first)</td></tr>
     <tr><td>ab − b, a = −2, b = 5</td><td>−10 − 5 = <b>−15</b></td></tr></tbody></table>
    <p class="small">2x when x = 3 is 2 × 3 = 6, not 23. A number next to a letter means multiply.</p></div>
  </div>
  <div class="tip"><b>Exam tip:</b> use brackets for negative numbers and write the line where you put them in: it earns marks even if the answer slips. Check an expression by trying a number: 2 tickets should cost 8(2) + 3 = €19.</div>
</div>

<div class="page p2">
  <div class="band"><div><div class="k">Practice · 34 questions</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <div class="two"><div><h2>A. Simplify</h2><ol class="q">{qs(A)}</ol></div>
  <div><h2>C. Find the value</h2><ol class="q" start="17">{qs(Cq)}</ol></div></div>
  <h2>B. Write as an expression</h2><ol class="q" start="9">{qs(B)}</ol>
  <h2>D. Talk algebra</h2><ol class="q" start="25">{qs(D)}</ol>
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
   <tr><td><b>C</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(Cq,17))}</td></tr>
   <tr><td><b>D</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(D,25))}</td></tr>
   <tr><td><b>E</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(E4,31))}</td></tr>
  </tbody></table>
  <div class="note"><b>Got one wrong?</b> Check: did each term keep the sign in front of it? Did you only add like terms (same letters, same powers)? Did you put negative numbers in brackets and square before multiplying? Did "less than" start with the letter? Then play <b>Like-Term Sweep</b> at leim.ie/like-term-sweep.html: the "Go back over these" list at the end shows the rule for each mistake.</div>
  <p class="small">All questions written by Léim. Léim is independent and not connected with the State Examinations Commission or the NCCA.</p>
</div>
</body></html>"""

# ---------- teacher pack ----------
YEL, GRN, BLU, INK = "#F6CF5A", "#9BD3AE", "#A9C4E8", "#1B2430"
def tiles(n2, nx, n1):
    o, x = "", 2
    for _ in range(n2): o += f'<rect x="{x}" y="2" width="30" height="30" fill="{YEL}" stroke="{INK}" stroke-width="1.5"/>'; x += 34
    for _ in range(nx): o += f'<rect x="{x}" y="2" width="10" height="30" fill="{GRN}" stroke="{INK}" stroke-width="1.5"/>'; x += 14
    for _ in range(n1): o += f'<rect x="{x}" y="22" width="10" height="10" fill="{BLU}" stroke="{INK}" stroke-width="1.5"/>'; x += 14
    return f'<svg viewBox="0 0 {x} 34" style="height:11mm;width:auto">{o}</svg>'
TILES = [(1, 2, 3), (2, 1, 0), (0, 4, 2), (1, 0, 5), (2, 3, 1), (0, 2, 6)]
def tstr(n2, nx, n1):
    parts = [(n2, "x²"), (nx, "x"), (n1, "")]
    return " + ".join((str(c) if (c != 1 or k == "") else "") + k for c, k in parts if c)
WORDS = [("5 less than n", "n − 5"), ("double n, then add 1", "2n + 1"), ("subtract n from 5", "5 − n"),
         ("n squared, plus 5", "n² + 5"), ("half of n", "n/2"), ("5 more than double n", "2n + 5")]
WCHK = ["n-5", "2*n+1", "5-n", "n**2+5", "n/2", "2*n+5"]
for (w, a), c in zip(WORDS, WCHK): assert sp.expand(sp.sympify(c, locals=SYM) - E(a)) == 0, w
MATCH = [(tiles(*t), tstr(*t)) for t in TILES] + WORDS
answers = [a for q, a in MATCH]; assert len(set(answers)) == 12 and len(set(map(lambda s: str(E(s)), answers))) == 12
for t, a in zip(TILES, answers): assert E(a) == t[0] * SYM["x"] ** 2 + t[1] * SYM["x"] + t[2]
cards = [q for q, a in MATCH] + [a for q, a in MATCH]
random.seed(8); match_print = cards[:]; random.shuffle(match_print)
def fc(x): return x if x.startswith("<svg") else f'<div class="fc{" sm" if len(x) > 12 else ""}">{x}</div>'
match_html = "".join(f'<div class="c"><span class="tag">Card {i}</span>{fc(x)}</div>' for i, x in enumerate(match_print, 1))
match_key = " · ".join(f"{'tiles ' + a if q.startswith('<svg') else q} → <b>{a}</b>" for q, a in MATCH)
# Think of a Number: each trick must always give the stated result
TRICK = [("Think of a number. Add 4. Double it. Subtract 8. Halve it.", "n", "((n+4)*2-8)/2"),
         ("Think of a number. Double it. Add 10. Halve it. Take away the number you first thought of.", "5", "(2*n+10)/2-n"),
         ("Think of a number. Multiply by 3. Add 6. Divide by 3. Take away 2.", "n", "(3*n+6)/3-2")]
for t, r, c in TRICK: assert sp.simplify(sp.sympify(c, locals=SYM) - E(r)) == 0, t

DOMS = [("Simplify 3x + 4x", "7x"), ("Simplify 5a − a", "4a"), ("Simplify 2x + 3y + x", "3x + 3y"), ("Simplify x² + x²", "2x²"),
        ("Simplify 6n − 2 − n + 5", "5n + 3"), ("3 less than n", "n − 3"), ("Double n, then add 1", "2n + 1"), ("y × y × y", "y³"),
        ("a × b × 5", "5ab"), ("Half of t", "t/2"), ("4x when x = −2", n(val("4x", x=-2))), ("x² when x = −3", n(val("x²", x=-3))),
        ("10 − x when x = −2", n(val("10 − x", x=-2))), ("2x² when x = −1", n(val("2x²", x=-1))), ("ab when a = −2, b = −3", n(val("ab", a=-2, b=-3))),
        ("3a + b when a = 2, b = −1", n(val("3a + b", a=2, b=-1))), ("Coefficient of x in 7 − 4x", "−4"), ("Constant term in 3x² + x − 7", "−7"),
        ("How many terms: 2a + 3b − c + 4", "4"), ("Perimeter of a square with side x + 1", "4x + 4")]
for q, a in DOMS[:5]: simp(q.replace("Simplify ", ""), a)
assert eq("y × y × y", "y³") and eq("a × b × 5", "5ab") and eq("4(x + 1)", "4x + 4")
ANS = [a for k, a in DOMS]
assert ANS[10:16] == ["−8", "9", "12", "2", "6", "5"], ANS
assert len(set(ANS)) == 20
random.seed(88); chain = DOMS[:]; random.shuffle(chain)
dom = [("START" if k == 0 else chain[k - 1][1], x[0]) for k, x in enumerate(chain)] + [(chain[-1][1], "FINISH")]
dom_print = dom[:]; random.shuffle(dom_print)
dom_html = "".join(f'<div class="dom"><div class="h l">{l}</div><div class="h r">{r}</div></div>' for l, r in dom_print)
chain_key = "".join(f"<li>{x} = <b>{a}</b></li>" for x, a in chain)

ERR = [("Simplify 3x + 2y", "= 5xy", "Unlike terms can't be added: <b>3x + 2y</b> (it stays as it is)"),
       ("Simplify x² + x²", "= x⁴", "Adding doesn't change the power: <b>2x²</b>"),
       ("Simplify 7a − a", "= 7", "The a doesn't disappear: 7a − 1a = <b>6a</b>"),
       ("Write \"4 less than n\"", "= 4 − n", "Start with n and take 4 away: <b>n − 4</b>"),
       ("x² when x = −3", "= −9", f"(−3)² = (−3) × (−3) = <b>{val('x²', x=-3)}</b>"),
       ("2x when x = 5", "= 25", f"2x means 2 × x: <b>{val('2x', x=5)}</b>")]
assert not eq("3x + 2y", "5xy") and not eq("x² + x²", "x⁴") and eq("7a − a", "6a")
w1 = simp("4x + 7 − x − 9 + 2y", "3x + 2y − 2")
w2 = [val("2a + 3b", a=4, b=-3), val("a² − b²", a=4, b=-3), val("5 − ab", a=4, b=-3)]; assert w2 == [-1, 7, 17]
w3 = val("25n + 4", n=6); assert w3 == 154
w4 = "6x + 6"; assert eq("2(2x + 3) + 2x", w4) and val(w4, x=5) == 36
assert sp.simplify(sp.sympify("(2*n+10)/2-n", locals=SYM)) == 5

pack_style = open(os.path.join(SRC, "build_ratio_pdfs.py"), encoding="utf-8").read()
pack_style = pack_style[pack_style.index("<style>", pack_style.index('pack = f"""')) + 7:pack_style.index("</style>", pack_style.index('pack = f"""'))]
pack_style = pack_style.replace("{{", "{").replace("}}", "}").replace("{LO}", LO)
pack_style += ".fym .c{height:21mm}.fym svg{margin-top:2mm}.trk{border:2px dashed #9AA3AE;padding:3mm 4mm;margin-top:3mm;font-size:9.6pt}.trk ol{margin:1mm 0 0;padding-left:18px}.trk li{margin:2.5mm 0}"
pack = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Algebra: Variables and Expressions Teacher Pack | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{pack_style}</style></head><body>

<div class="page p1">
  <div class="band"><div><div class="k">Junior Cycle Maths · Teacher pack</div><h1>Variables &amp; expressions</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2018 specification): {LO} (expanding brackets comes later in Algebra 2, AF.3b; forming and solving equations in Linear equations, AF.2c and AF.4)</p>
  <div class="two">
    <div><h3>Aims</h3><p>By the end of the lesson students can use the words variable, term, coefficient and constant; write expressions the short way; collect like terms (including x² terms and negatives); write expressions from words and real-life contexts; and substitute positive and negative numbers into expressions.</p></div>
    <div><h3>In this pack</h3><p>p.1 Teacher notes · p.2 Think of a Number + Algebra Tiles Match cards · p.3 Algebra Dominoes (cut-up) · p.4 Wall poster · p.5 Worksheet: Error Hunt + exam-style questions · p.6 Answers. Level: 1st year (Higher and Ordinary), or 3rd-year revision. Time: about 60 minutes. All questions are original.</p></div>
  </div>
  <h2 style="margin-top:8px">Procedure</h2>
  <table class="proc"><tbody>
    <tr><td>6 min</td><td><b>Lead-in: Think of a Number.</b> Everyone thinks of a number: add 4, double it, subtract 8, halve it. "Put your hand up if you got back to your own number!" How does it work? Don't explain yet.</td></tr>
    <tr><td>8 min</td><td><b>Guided discovery: like terms.</b> Pairs test 3x + 2x and 5x with x = 2, 7 and 10, then 3x + 2y and 5xy with x = 2, y = 5. Which pair is always equal? Why? (3 lots of x plus 2 lots of x; x and y are different things.) Then x + x v x² with x = 3.</td></tr>
    <tr><td>8 min</td><td><b>Back to the trick.</b> Board: n → n + 4 → 2n + 8 → 2n → n. Pairs prove the other two tricks on p.2 the same way (the second one always gives 5), then invent their own.</td></tr>
    <tr><td>10 min</td><td><b>Algebra Tiles Match</b> (p.2, 24 cards = 12 pairs; one card each). Tile pictures and word cards find their expression. Pairs check each other and sit together. Feedback: who had "5 less than n"? Why isn't it 5 − n?</td></tr>
    <tr><td>12 min</td><td><b>Algebra Dominoes</b> (p.3), groups of 3–4: start with START, work out the clue, find the domino with that answer on its left and build the chain to FINISH. Watch the substitution dominoes: brackets for negatives.</td></tr>
    <tr><td>13 min</td><td><b>Worksheet</b> (p.5). Error Hunt in pairs (find the mistake, name the rule, fix it), then the exam-style questions alone.</td></tr>
    <tr><td>3 min</td><td><b>Exit ticket.</b> Simplify 4a − 3b + 2a + 5b; find 3 − 2x when x = −4 (6a + 2b; 11). Homework: play <b>Like-Term Sweep</b> at leim.ie/like-term-sweep.html (Substitution Slot Machine round) and copy three lines from the "Go back over these" list.</td></tr>
  </tbody></table>
  <div class="note"><b>Algebra Tiles Match key:</b> {match_key}.<br>
  <b>Errors to look for:</b> 3x + 2y = 5xy · x² + x² = x⁴ · 7a − a = 7 · losing the sign in front of a term · "5 less than n" = 5 − n · (−3)² = −9 · 2x² with x = −3 worked out as (2 × −3)² · 2x with x = 3 read as 23. <b>Support:</b> use the tiles and real numbers to test every answer. <b>Fast finishers:</b> write a Think of a Number trick that always ends on 7.</div>
  <p class="small"><b>Domino answer chain</b> (START → FINISH):</p>
  <ol class="small" style="columns:3;column-gap:12px;font-size:7.6pt;line-height:1.33;margin:0;padding-left:16px">{chain_key}</ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">One trick card per pair · one match card per student</div><h1>Think of a Number + Tiles Match</h1></div><div class="logo">↗ Léim</div></div>
  <div class="trk"><b>Think of a Number.</b> Try each trick with three different numbers. What do you notice? Then call your number n and write what happens at each step. Can you prove it always works?
    <ol>{"".join(f"<li>{t}<span class='line' style='min-width:60mm'></span></li>" for t, r, c in TRICK)}</ol>
    <p style="margin:1mm 0 0">Now invent your own trick that always gives back the number you started with.</p></div>
  <p style="font-size:9.5pt;margin:4mm 0 0"><b>Algebra Tiles Match.</b> Big square = x², long tile = x, small square = 1. Cut out the 24 cards and give one to each student. Tiles or words card? Find the person with your expression. Expression card? Find your tiles or words. (Fewer students? Take out whole pairs.)</p>
  <div class="fym">{match_html}</div>
</div>

<div class="page">
  <div class="band"><div><div class="k">Groups of 3–4 · cut along the dashed lines</div><h1>Algebra Dominoes</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.5pt">Start with START. Work out the clue on the right, then find the domino with that answer on its left. Keep going until you reach FINISH. No calculators!</p>
  <div class="doms">{dom_html}</div>
</div>

<div class="page">
  <div class="poster">
    <h1>Variables &amp; expressions</h1>
    <div class="big3"><div>4x²<span>term</span></div><div>−3<span>coefficient of x</span></div><div>7<span>constant</span></div></div>
    <p style="text-align:center;font-size:13pt;margin:0"><b>4x² − 3x + 7</b> has 3 terms · each term keeps the sign in front of it</p>
    <div class="ops">
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Like terms</b>same letters, same powers<br>3x + 5x = 8x<br>3x + 2y stays 3x + 2y</div>
      <div style="background:var(--green-soft)"><b>Powers</b>x × x = x²<br>x + x = 2x<br>x² + x² = 2x² (not x⁴)</div>
      <div style="background:var(--green-soft)"><b>Words</b>5 more than n → n + 5<br>5 less than n → n − 5<br>half of n → n/2</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Substitute</b>brackets for negatives<br>5 − 2(−3) = 11<br>(−4)² = 16</div>
    </div>
    <p style="text-align:center;font-size:12pt;margin:0"><b>Check:</b> try a number in your answer</p>
    <p style="text-align:center;font-size:10pt;color:var(--muted)">Léim · leim.ie · Play Like-Term Sweep: leim.ie/like-term-sweep.html</p>
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
    <li>Simplify 4x + 7 − x − 9 + 2y.<span class="long"></span></li>
    <li>a = 4 and b = −3. Find the value of (a) 2a + 3b (b) a² − b² (c) 5 − ab<span class="long"></span><span class="long"></span></li>
    <li>Concert tickets cost €25 each, plus a €4 booking fee for each order. (a) Write an expression for the cost, in euro, of n tickets in one order. (b) Find the cost of 6 tickets.<span class="long"></span><span class="long"></span></li>
    <li>A rectangle has length 2x + 3 and width x. (a) Write its perimeter in its simplest form. (b) Find the perimeter when x = 5.<span class="long"></span><span class="long"></span></li>
    <li>Think of a number, double it, add 10, halve it, then take away the number you first thought of. Use algebra to show that the answer is always 5.<span class="long"></span><span class="long"></span></li>
  </ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">For the teacher</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>Think of a Number</h2>
  <ol class="q">
    <li>n → n + 4 → 2n + 8 → 2n → <b>n</b> (always your number)</li>
    <li>n → 2n → 2n + 10 → n + 5 → <b>5</b> (always 5)</li>
    <li>n → 3n → 3n + 6 → n + 2 → <b>n</b> (always your number)</li>
  </ol>
  <h2>A. Error Hunt</h2>
  <table><tbody>{"".join(f"<tr><td style='width:34%'><b>{q}</b> {w}</td><td>{r}</td></tr>" for q,w,r in ERR)}</tbody></table>
  <h2>B. Exam-style questions</h2>
  <ol class="q">
    <li>x terms: 4 − 1 = 3; numbers: 7 − 9 = −2: <b>{w1}</b></li>
    <li>(a) 2(4) + 3(−3) = 8 − 9 = <b>{n(w2[0])}</b> (b) 16 − 9 = <b>{n(w2[1])}</b> (c) 5 − (4)(−3) = 5 + 12 = <b>{n(w2[2])}</b></li>
    <li>(a) <b>25n + 4</b> (the fee is paid once per order) (b) 25(6) + 4 = <b>€{w3}</b></li>
    <li>(a) 2(2x + 3) + 2x = <b>{w4}</b> (b) 6(5) + 6 = <b>{val(w4, x=5)}</b></li>
    <li>n → 2n → 2n + 10 → n + 5 → n + 5 − n = <b>5</b>, whatever n is.</li>
  </ol>
  <h2>Marking tip</h2>
  <p>Give credit for each step, as the exam does: the line with the numbers in brackets earns marks even if the arithmetic slips. In "simplify" questions, accept the terms in any order (5 − n = −n + 5), but not unlike terms joined together.</p>
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
<h1><span>Variables &amp;</span><br><span>Expressions</span></h1>
<div class="sub">Think of a Number · Algebra Tiles Match<br>Algebra Dominoes · Poster · Worksheet + answers</div>
<div class="em">3x + 2x = 5x &nbsp;·&nbsp; 5 − 2(−3) = 11</div></div>
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
    pdf("teacher-pack", os.path.join(OUT, "Variables-and-Expressions-Teacher-Pack-Leim.pdf"))
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--hide-scrollbars", "--window-size=1200,1200",
                    f"--screenshot={os.path.join(OUT, f'{SLUG}-cover.png')}", f"{SLUG}-cover.html"], cwd=SRC, check=True, capture_output=True)
    print("domino chain:", [(x, a) for x, a in chain])
