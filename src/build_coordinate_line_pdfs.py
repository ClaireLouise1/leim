#!/usr/bin/env python3
"""Coordinate geometry of the line (JC Maths topic 28): free sheet + teacher pack + Payhip cover.
Run from the repo root: python3 src/build_coordinate_line_pdfs.py OUTDIR
Writes src/coordinate-geometry-line-*.html; PDFs/cover PNG go to OUTDIR (free sheet also to printables/).
Diagrams come from the Line Lab game's grid kit through src/line_figs_bridge.js and every diagram is read back
by test_line_lab.py's reader. Every answer is computed here with exact fractions and asserted.
Styles are read from src/build_money1_pdfs.py."""
import os, sys, random, subprocess, re, json, math
from fractions import Fraction as Fr
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC)
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/cline"; os.makedirs(OUT, exist_ok=True)
SLUG = "coordinate-geometry-line"
LO = "GT.5a, GT.5b, GT.5c"
M = "−"

# ---------- my own maths ----------
def n(v):
    v = Fr(v); s = M if v < 0 else ""; v = abs(v)
    if v.denominator == 1: return s + str(v.numerator)
    if v.denominator == 2: return s + str(float(v))
    raise ValueError(v)
def fs(v):
    v = Fr(v); return (M if v < 0 else "") + str(abs(v.numerator)) + ("" if v.denominator == 1 else "/" + str(v.denominator))
def c(p): return "(" + n(p[0]) + ", " + n(p[1]) + ")"
UF = {Fr(1, 2): "½", Fr(1, 3): "⅓", Fr(2, 3): "⅔", Fr(1, 4): "¼", Fr(3, 4): "¾"}
def eq(m, k):
    m, k = Fr(m), Fr(k); assert k.denominator == 1
    if m == 0: return f"y = {n(k)}"
    a = abs(m); t = (M if m < 0 else "") + ("" if a == 1 else str(a.numerator) if a.denominator == 1 else UF.get(a, f"({a})")) + "x"
    return "y = " + t + ("" if k == 0 else f" + {k}" if k > 0 else f" − {-k}")
def slope(A, B): return Fr(B[1] - A[1], B[0] - A[0])
def mid(A, B): return (Fr(A[0] + B[0], 2), Fr(A[1] + B[1], 2))
def dist(A, B): return math.sqrt((B[0] - A[0]) ** 2 + (B[1] - A[1]) ** 2)
def d1(x):
    assert abs(x * 10 - math.floor(x * 10) - .5) > .05; return f"{x:.1f}"
def line(m, P): return (Fr(m), Fr(P[1]) - Fr(m) * P[0])        # (slope, c) through P
def meet(L1, L2): x = (L2[1] - L1[1]) / (L1[0] - L2[0]); return (x, L1[0] * x + L1[1])
def on(L, P): return L[0] * P[0] + L[1] == P[1]
def E(L): return eq(*L)
assert eq(Fr(-1, 2), 2) == "y = −½x + 2" and eq(3, -1) == "y = 3x − 1" and eq(-1, 0) == "y = −x" and c((Fr(3, 2), -3)) == "(1.5, −3)"

# ---------- diagrams from the game's kit, each read back ----------
FIGS = {
    "slope": 'FIX.slope()',
    "pB": 'plane({R:5,lines:[{m:[3,2],c:[0,1],n:"l"}],pts:[{p:[-2,-3],n:"A",dx:-10,dy:4},{p:[2,3],n:"B",dx:-10,dy:2}]})',
    "pC": 'plane({R:5,lines:[{m:[-1,2],c:[2,1],n:"m"}],pts:[{p:[0,2]},{p:[4,0]}]})',
    "pD": 'plane({R:5,lines:[{m:[1,1],c:[1,1],n:"l"},{m:[-2,1],c:[4,1],n:"k",end:0}]})',
    "w2": 'plane({R:6,lines:[{m:[1,2],c:[-1,1],n:"l"},{m:[-2,1],c:[4,1],n:"k",end:0}]})',
    "poster": 'FIX.slope()',
}
FIG = json.loads(subprocess.run(["node", os.path.join(SRC, "line_figs_bridge.js")], input=json.dumps(FIGS), capture_output=True, text=True, check=True).stdout)
_ns = {}; exec(open(os.path.join(SRC, "test_line_lab.py"), encoding="utf-8").read().split("if __name__")[0], _ns)
pics = {k: _ns["read_plane"](v) for k, v in FIG.items()}
assert pics["pB"]["lines"]["l"] == (Fr(3, 2), 0) and pics["pB"]["pts"]["A"] == (-2, -3) and pics["pB"]["pts"]["B"] == (2, 3)
assert pics["pC"]["lines"]["m"] == (Fr(-1, 2), 2)
assert pics["pD"]["lines"]["l"] == (1, 1) and pics["pD"]["lines"]["k"] == (-2, 4)
assert pics["w2"]["lines"]["l"] == (Fr(1, 2), -1) and pics["w2"]["lines"]["k"] == (-2, 4)
assert pics["slope"]["lines"]["l"] == (Fr(2, 3), Fr(-1, 3))
for k in list(FIG): FIG[k] = re.sub(r' style="max-width:\d+px"', "", FIG[k])

# ---------- free sheet ----------
A = [("Find the midpoint of (2, 5) and (6, 1).", c(mid((2, 5), (6, 1)))),
     ("Find the midpoint of (−3, 4) and (5, −2).", c(mid((-3, 4), (5, -2)))),
     ("Find the midpoint of (−1, −6) and (4, 0).", c(mid((-1, -6), (4, 0)))),
     ("M(2, 1) is the midpoint of [AB] and A is (−1, 3). Find B.", c((2 * 2 + 1, 2 * 1 - 3))),
     ("Find the distance between (1, 2) and (4, 6).", n(int(dist((1, 2), (4, 6))))),
     ("Find the distance between (−2, 3) and (4, −5).", n(int(dist((-2, 3), (4, -5))))),
     ("Find the distance between (0, 0) and (3, 5), to 1 decimal place.", d1(dist((0, 0), (3, 5)))),
     ("P is (−4, 1) and Q is (2, 4). Find |PQ| to 1 decimal place.", d1(dist((-4, 1), (2, 4))))]
assert mid((-1, 3), (5, -1)) == (2, 1) and dist((1, 2), (4, 6)) == 5 and dist((-2, 3), (4, -5)) == 10
assert [a for q, a in A] == ["(4, 3)", "(1, 1)", "(1.5, −3)", "(5, −1)", "5", "10", "5.8", "6.7"]
TX = ((0, 5), (10, 25))
B = [("Find the slope of the line through (1, 2) and (3, 8).", fs(slope((1, 2), (3, 8)))),
     ("Find the slope of the line through (−2, 5) and (2, −3).", fs(slope((-2, 5), (2, -3)))),
     ("Find the slope of the line through (0, −1) and (6, 3).", fs(slope((0, -1), (6, 3)))),
     ("Find the slope of the line through (−4, −2) and (5, −2).", fs(slope((-4, -2), (5, -2)))),
     ("Use the diagram. Find the slope of the line l.", fs(pics["pB"]["lines"]["l"][0])),
     ("The line through (2, k) and (5, 10) has slope 2. Find k.", n(10 - 2 * 3)),
     ("A taxi's fares are shown by a straight-line graph through (0, 5) and (10, 25), x in km and y in euro. Find the slope and say what it means.", f"{fs(slope(*TX))}: €{fs(slope(*TX))} per km"),
     ("What does the point (0, 5) on the taxi graph tell you?", "a €5 fixed charge")]
assert [a for q, a in B][:6] == ["3", "−2", "2/3", "0", "3/2", "4"] and slope((2, 4), (5, 10)) == 2
Cq = [("Write down the slope of y = 4x − 7 and the point where it meets the y-axis.", "4; (0, −7)"),
      ("What is the slope of the line y = 6 − 3x?", "−3"),
      ("Find the equation of the line through (2, 5) with slope 3.", E(line(3, (2, 5)))),
      ("Find the equation of the line through (−1, 4) with slope −2.", E(line(-2, (-1, 4)))),
      ("Find the equation of the line through (1, 1) and (3, 7).", E(line(slope((1, 1), (3, 7)), (1, 1)))),
      ("Is the point (3, 5) on the line y = 2x − 1? Show how you know.", "yes: 2 × 3 − 1 = 5"),
      ("Use the diagram. Find the equation of the line m.", E(pics["pC"]["lines"]["m"])),
      ("Where does the line y = 3x − 6 cross the x-axis?", c((2, 0)))]
assert [a for q, a in Cq][2:5] == ["y = 3x − 1", "y = −2x + 2", "y = 3x − 2"] and on((2, -1), (3, 5)) and on((3, -6), (2, 0))
Lp, Lk = pics["pD"]["lines"]["l"], pics["pD"]["lines"]["k"]; P_D = meet(Lp, Lk)
D = [("What is the slope of any line parallel to y = 5x + 2?", "5"),
     ("Find the equation of the line through (0, −3) parallel to y = 2x + 7.", E(line(2, (0, -3)))),
     ("Find the equation of the line through (2, 1) parallel to y = −x + 4.", E(line(-1, (2, 1)))),
     ("Use the diagram. Where do the lines l and k meet?", c(P_D)),
     ("Higher Level: what is the slope of a line perpendicular to y = ⅔x − 1?", fs(-1 / Fr(2, 3))),
     ("Higher Level: find the slope of the line 2x + 5y − 10 = 0.", fs(Fr(-2, 5)))]
assert P_D == (1, 2) and [a for q, a in D] == ["5", "y = 2x − 3", "y = −x + 3", "(1, 2)", "−3/2", "−2/5"]
# exam-style
eA, eB = (-2, 7), (4, -5); eL = line(slope(eA, eB), eA)
assert (mid(eA, eB), slope(eA, eB), d1(dist(eA, eB)), E(eL), on(eL, (5, -7))) == ((1, 1), -2, "13.4", "y = −2x + 3", True)
tk = ((0, 30), (8, 190)); tm = slope(*tk); assert tm == 20 and (250 - 30) / tm == 11
l33, k33 = (2, -1), (-1, 5); assert on(l33, (2, 3)) and on(k33, (2, 3)) and on(k33, (5, 0)) and E(line(2, (0, 4))) == "y = 2x + 4"
p34 = (3, 2); pp = line(Fr(-1, 3), (3, 0)); assert pp == (Fr(-1, 3), 1) and on(pp, (6, -1)) and p34[0] * Fr(-1, 3) == -1
Eq = [(f"<b>The segment [AB].</b> A is (−2, 7) and B is (4, −5). (a) Find the midpoint of [AB]. (b) Find the slope of AB. (c) Find |AB| to 1 decimal place. (d) Find the equation of AB. (e) Is (5, −7) on the line AB?",
       f"(a) <b>(1, 1)</b> (b) <b>−2</b> (c) √180 = <b>13.4</b> (d) <b>{E(eL)}</b> (e) <b>yes</b>: −2 × 5 + 3 = −7"),
      ("<b>Filling a tank.</b> A straight-line graph of the water in a tank goes through (0, 30) and (8, 190), with x in minutes and y in litres. (a) Find the slope and say what it means. (b) What does (0, 30) tell you? (c) Write the equation of the line. (d) When will the tank hold 250 litres?",
       "(a) <b>20</b>: 20 litres per minute (b) <b>30 litres</b> at the start (c) <b>y = 20x + 30</b> (d) 20x + 30 = 250, <b>11 minutes</b>"),
      ("<b>Two lines.</b> l: y = 2x − 1 and k: y = −x + 5. (a) Write down the slope of each line. (b) Show that (2, 3) is on both lines. (c) Where does k cross the x-axis? (d) Find the equation of the line through (0, 4) parallel to l.",
       "(a) <b>2</b> and <b>−1</b> (b) 2 × 2 − 1 = 3 ✓, −2 + 5 = 3 ✓ (c) <b>(5, 0)</b> (d) <b>y = 2x + 4</b>"),
      ("<b>Higher Level.</b> The line p is 3x − y + 2 = 0. (a) Write p in the form y = mx + c. (b) Find the slope of a line perpendicular to p. (c) Find the equation of the line through (3, 0) perpendicular to p. (d) Is (6, −1) on the line in (c)?",
       "(a) <b>y = 3x + 2</b> (b) <b>−1/3</b> (c) <b>y = −⅓x + 1</b> (d) <b>yes</b>: −⅓ × 6 + 1 = −1")]

def qs(items): return "".join(f"<li>{q} <span class='line'></span></li>" for q, a in items)
def style(var):
    return re.search(var + r' = f"""<!doctype.*?<style>(.*?)</style>', open(os.path.join(SRC, "build_money1_pdfs.py"), encoding="utf-8").read(), re.S).group(1).replace("{LO}", LO).replace("{{", "{").replace("}}", "}")
SHEET_STYLE = style("sheet"); PACK_STYLE = style("pack")
assert "@bottom-left" in SHEET_STYLE and "Single-teacher licence" in PACK_STYLE and "{{" not in SHEET_STYLE + PACK_STYLE
FIGCSS = """svg.tg{display:block;width:100%;height:auto;background:#fff}svg.tg .gl{stroke:#D5DDE5;stroke-width:.8}svg.tg .ax{stroke:#5B6775;stroke-width:1.4}
svg.tg .tk{font:600 9.5px Inter,sans-serif;fill:#5B6775}svg.tg .axl{font:italic 700 12px Inter,sans-serif;fill:#5B6775}
svg.tg .ln{stroke-width:2.6;stroke-linecap:round}svg.tg .ln.a{stroke:#2962A6}svg.tg .ln.b{stroke:#7A4BB3}
svg.tg .lnl{font:italic 800 15px Inter,sans-serif;paint-order:stroke;stroke:#fff;stroke-width:3px}svg.tg .lnl.a{fill:#2962A6}svg.tg .lnl.b{fill:#7A4BB3}
svg.tg .stp{stroke:#C0392B;stroke-width:1.8;stroke-dasharray:5 3}svg.tg .sl{font:700 11px Inter,sans-serif;fill:#C0392B;paint-order:stroke;stroke:#fff;stroke-width:3px}
svg.tg .pt{fill:#1B2430}svg.tg .pl{font:800 13px Inter,sans-serif;fill:#1B2430;paint-order:stroke;stroke:#fff;stroke-width:3px}
.gfig{float:right;width:44mm;margin:0 0 1mm 3mm}.fm4{display:grid;grid-template-columns:1fr 1fr;gap:1.5mm}.fm4 div{border:1.5px solid var(--line);border-radius:8px;padding:2px 6px;font-size:9pt}.fm4 b{display:block}"""

sheet = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Coordinate geometry of the line: rules and practice | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{SHEET_STYLE}
{FIGCSS}
</style></head><body>
<div class="page tight">
  <div class="band"><div><div class="k">Junior Cycle Maths · Free revision sheet</div><h1>Coordinate geometry of the line</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2018 specification): {LO}. Play the game: <b>leim.ie/line-lab.html</b></p>
  <div class="two">
   <div><h2>1. Slope</h2>
    <div class="gfig">{FIG["slope"]}</div>
    <p>The <b>slope</b> m is <b>rise ÷ run</b>: how far the line goes up for each step across. A(−1, −1) to B(2, 1): run 3, rise 2, slope <b>2/3</b>.</p>
    <p><b>m = (y₂ − y₁) ÷ (x₂ − x₁)</b></p>
    <p style="clear:both">Rises left to right: <b>positive</b>. Falls: <b>negative</b>. Flat: <b>zero</b>.</p>
    <p>In a real graph the slope is the <b>rate</b> (€ per km, litres per minute) and the point on the y-axis is the <b>starting value</b> (a fixed charge).</p>
    <h2>2. Midpoint and distance</h2>
    <div class="fm4"><div><b>Midpoint</b>((x₁ + x₂) ÷ 2, (y₁ + y₂) ÷ 2)<br>add, then halve</div><div><b>Distance</b>√((x₂ − x₁)² + (y₂ − y₁)²)<br>it's Pythagoras</div></div>
    <p style="margin-top:3px">(1, 2) to (4, 6): across 3, up 4, distance √(9 + 16) = <b>5</b>. Midpoint (2.5, 4).</p></div>
   <div><h2>3. The equation of a line</h2>
    <p><b>y = mx + c</b>: m is the slope, the line meets the y-axis at <b>(0, c)</b>. Get y on its own first: y = 6 − 3x has slope <b>−3</b>.</p>
    <p><b>y − y₁ = m(x − x₁)</b>: one point and the slope. Through (2, 5), slope 3: y − 5 = 3(x − 2) → <b>y = 3x − 1</b>.</p>
    <p><b>Two points:</b> find the slope first, then use either point.</p>
    <p><b>On the line?</b> Put in x; if you get the point's y, yes. <b>Axes:</b> x = 0 on the y-axis, y = 0 on the x-axis.</p>
    <h2>4. Parallel, perpendicular, meeting</h2>
    <p><b>Parallel</b> lines have the <b>same slope</b>. <b>Where lines meet:</b> read the crossing point, then check it in both equations.</p>
    <p><b>Higher Level:</b> <b>perpendicular</b> slopes multiply to −1 (flip and change the sign: 2/3 → −3/2). <b>ax + by + c = 0</b>: get y on its own; slope = −a ÷ b.</p>
    <div class="note"><b>Classic mistakes:</b> run ÷ rise · losing a minus (5 − (−2) = 7) · subtracting for the midpoint · 3 + 4 instead of √(3² + 4²) · reading c as the slope · not getting y on its own first.</div></div>
  </div>
  <div class="tip"><b>Exam tip:</b> write the formula, label (x₁, y₁) and (x₂, y₂), use brackets for negatives, and check your equation with the points you were given.</div>
</div>

<div class="page p2">
  <div class="band"><div><div class="k">Practice · 34 questions</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Midpoint and distance</h2><ol class="q">{qs(A)}</ol>
  <h2>B. Slope</h2>
  <div class="gfig" style="width:36mm">{FIG["pB"]}</div>
  <ol class="q" start="9">{qs(B)}</ol>
  <h2 style="clear:both">C. The equation of a line</h2>
  <div class="gfig" style="width:36mm">{FIG["pC"]}</div>
  <ol class="q" start="17">{qs(Cq)}</ol>
  <h2 style="clear:both">D. Parallel, perpendicular and meeting</h2>
  <div class="gfig" style="width:34mm">{FIG["pD"]}</div>
  <ol class="q" start="25">{qs(D)}</ol>
  <p class="small" style="margin-top:4px;clear:both">Questions 31–34 are on the next page.</p>
</div>

<div class="page">
  <div class="band"><div><div class="k">Exam-style · then check</div><h1>Exam corner + answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>E. Exam-style questions (show your work)</h2>
  <ol class="q e3" start="31">{"".join(f"<li>{q}<span class='long'></span><span class='long'></span></li>" for q,a in Eq)}</ol>
  <h2 style="margin-top:10px">Answers</h2>
  <table class="ans"><tbody>
   <tr><td><b>A</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(A,1))}</td></tr>
   <tr><td><b>B</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(B,9))}</td></tr>
   <tr><td><b>C</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(Cq,17))}</td></tr>
   <tr><td><b>D</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(D,25))}</td></tr>
   <tr><td><b>E</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(Eq,31))}</td></tr>
  </tbody></table>
  <div class="note"><b>Got one wrong?</b> Check: rise on top, run underneath? Brackets round the negatives? Did you get y on its own first? Then play <b>Line Lab</b> at leim.ie/line-lab.html: the "Go back over these" list at the end shows the rule for each mistake.</div>
  <p class="small">All questions written by Léim. Léim is independent and not connected with the State Examinations Commission or the NCCA.</p>
</div>
</body></html>"""

# ---------- teacher pack ----------
# Line Swap: each fact is on exactly ONE card
sA, sB = (-1, 2), (3, 10)
s_mid, s_m, s_len, s_L = mid(sA, sB), slope(sA, sB), d1(dist(sA, sB)), line(slope(sA, sB), sA)
lL, kL = (Fr(2), Fr(1)), (Fr(-1), Fr(7)); s_meet = meet(lL, kL); s_par = line(2, (1, 0))
assert (c(s_mid), fs(s_m), s_len, E(s_L), c(s_meet), E(s_par)) == ("(1, 6)", "2", "8.9", "y = 2x + 4", "(2, 5)", "y = 2x − 2")
SW1 = [("Point A", c(sA), "A"), ("Point B", c(sB), "B"), ("Midpoint of [AB]", "", None), ("Slope of AB", "", None), ("|AB| (1 d.p.)", "", None), ("Equation of AB", "", None)]
SW2 = [("Line l", E(lL), "A"), ("Slope of line k", "−1", "B"), ("Line k meets the y-axis at", "(0, 7)", "B"),
       ("Equation of k", "", None), ("Where l and k meet", "", None), ("Line through (1, 0) parallel to l", "", None)]
for rows in (SW1, SW2): assert any(w == "A" for *_, w in rows) and any(w == "B" for *_, w in rows)
def swap_card(who):
    def tab(title, rows):
        return f'<table class="ss"><thead><tr><th colspan="2">{title}</th></tr></thead><tbody>' + "".join(
            f"<tr><td>{k}</td><td><b>{v if w == who else ''}</b></td></tr>" for k, v, w in rows) + "</tbody></table>"
    return f'<div class="idc"><h3>Student {who} · Line Swap</h3><div class="two">{tab("The segment [AB]", SW1)}{tab("Two lines", SW2)}</div></div>'

# mingle: each question value matches exactly one answer card
MATCH = [("Slope through (1, 2) and (4, 8)", fs(slope((1, 2), (4, 8)))), ("Midpoint of (0, 4) and (6, −2)", c(mid((0, 4), (6, -2)))),
         ("Distance from (0, 0) to (6, 8)", n(int(dist((0, 0), (6, 8))))), ("Slope of y = 5 − 4x", "−4"),
         ("y = 3x + 2 meets the y-axis at", "(0, 2)"), ("The line through (1, 4) with slope 3", E(line(3, (1, 4)))),
         ("Slope of a line parallel to y = ½x + 6", "½"), ("Higher Level: slope of a line perpendicular to y = −3x + 1", "⅓"),
         ("y = 2x − 8 meets the x-axis at", c((4, 0))), ("(k, 9) is on y = 2x + 1. k = ?", n((9 - 1) // 2)),
         ("M(2, 3) is the midpoint of [AB], A(0, 1). B = ?", c((4, 5))), ("The line through (0, −1) and (2, 5)", E(line(slope((0, -1), (2, 5)), (0, -1))))]
ANS = [a for q, a in MATCH]
assert ANS == ["2", "(3, 1)", "10", "−4", "(0, 2)", "y = 3x + 1", "½", "⅓", "(4, 0)", "4", "(4, 5)", "y = 3x − 1"], ANS
assert len(set(ANS)) == 12 and on((2, -8), (4, 0)) and mid((0, 1), (4, 5)) == (2, 3)
cards = [q for q, a in MATCH] + ANS
random.seed(28); match_print = cards[:]; random.shuffle(match_print)
match_html = "".join(f'<div class="c"><span class="tag">Card {i}</span><div class="fc{" sm" if len(x) > 10 else ""}">{x}</div></div>' for i, x in enumerate(match_print, 1))
match_key = " · ".join(f"{match_print.index(q) + 1} → {match_print.index(a) + 1}" for q, a in MATCH)

DOMS = [("Slope through (0, 0) and (2, 6)", fs(slope((0, 0), (2, 6)))), ("Slope through (1, 5) and (3, 1)", fs(slope((1, 5), (3, 1)))),
        ("Slope through (0, 1) and (4, 4)", fs(slope((0, 1), (4, 4)))), ("Slope through (−2, 3) and (4, 3)", fs(slope((-2, 3), (4, 3)))),
        ("Midpoint of (2, 2) and (6, 8)", c(mid((2, 2), (6, 8)))), ("Midpoint of (−4, 1) and (2, −5)", c(mid((-4, 1), (2, -5)))),
        ("Midpoint of (0, 0) and (5, 3)", c(mid((0, 0), (5, 3)))), ("Distance (1, 1) to (4, 5)", n(int(dist((1, 1), (4, 5))))),
        ("Distance (−3, 0) to (9, 5)", n(int(dist((-3, 0), (9, 5))))), ("Slope of y = 7x − 2", "7"),
        ("Slope of y = 9 − x", "−1"), ("y = 4x − 6 meets the y-axis at", "(0, −6)"), ("y = 2x + 10 meets the x-axis at", c((-5, 0))),
        ("Line through (0, 3), slope 5", E(line(5, (0, 3)))), ("Line through (2, 1), slope 2", E(line(2, (2, 1)))),
        ("Line through (1, 2) and (3, 6)", E(line(slope((1, 2), (3, 6)), (1, 2)))), ("Parallel to y = −4x + 1 through (0, 0)", E(line(-4, (0, 0)))),
        ("(3, k) is on y = 3x − 5. k = ?", n(3 * 3 - 5)), ("Higher Level: slope of 3x + y − 5 = 0", "−3"),
        ("Higher Level: perpendicular slope to y = 2x + 3", fs(Fr(-1, 2)))]
DANS = [a for k, a in DOMS]
assert DANS == ["3", "−2", "3/4", "0", "(4, 5)", "(−1, −2)", "(2.5, 1.5)", "5", "13", "7", "−1", "(0, −6)", "(−5, 0)", "y = 5x + 3",
                "y = 2x − 3", "y = 2x", "y = −4x", "4", "−3", "−1/2"], DANS
assert len(set(DANS)) == 20, sorted(DANS)
random.seed(2828); chain = DOMS[:]; random.shuffle(chain)
dom = [("START" if k == 0 else chain[k - 1][1], x[0]) for k, x in enumerate(chain)] + [(chain[-1][1], "FINISH")]
dom_print = dom[:]; random.shuffle(dom_print)
dom_html = "".join(f'<div class="dom"><div class="h l{" sm" if len(l) > 9 else ""}">{l}</div><div class="h r">{r}</div></div>' for l, r in dom_print)
chain_key = "".join(f"<li>{x} = <b>{a}</b></li>" for x, a in chain)

ERR = [("Slope through (1, 3) and (5, 11)?", "1/2", f"Run ÷ rise. Rise ÷ run: 8 ÷ 4 = <b>{fs(slope((1, 3), (5, 11)))}</b>"),
       ("Midpoint of (−2, 6) and (4, 0)?", "(−3, 3)", f"Subtracted the x's. Add, then halve: <b>{c(mid((-2, 6), (4, 0)))}</b>"),
       ("Distance from (0, 0) to (5, 12)?", "17", f"Added 5 + 12. √(5² + 12²) = √169 = <b>{n(int(dist((0, 0), (5, 12))))}</b>"),
       ("Slope of y = 8 − 3x?", "8", "Read the number on its own. y = −3x + 8: slope <b>−3</b>"),
       ("Slope through (−1, 4) and (3, −4)?", "0", f"Lost the minus: −4 − 4 = −8, run 3 − (−1) = 4: <b>{fs(slope((-1, 4), (3, -4)))}</b>"),
       ("Line through (2, 7) parallel to y = 3x + 5?", "y = 3x + 5", f"That's the same line. Same slope through (2, 7): <b>{E(line(3, (2, 7)))}</b>")]
assert (fs(slope((1, 3), (5, 11))), c(mid((-2, 6), (4, 0))), fs(slope((-1, 4), (3, -4))), E(line(3, (2, 7)))) == ("2", "(1, 3)", "−2", "y = 3x + 1")
# worksheet exam-style
w1A, w1B = (-1, -3), (3, 5); w1L = line(slope(w1A, w1B), w1A)
assert (c(mid(w1A, w1B)), fs(slope(w1A, w1B)), d1(dist(w1A, w1B)), E(w1L)) == ("(1, 1)", "2", "8.9", "y = 2x − 1")
wl, wk = pics["w2"]["lines"]["l"], pics["w2"]["lines"]["k"]; wP = meet(wl, wk)
assert wP == (2, 0) and E(wl) == "y = ½x − 1" and E(wk) == "y = −2x + 4" and wl[0] * wk[0] == -1
w3 = ((0, 12), (6, 3)); w3m = slope(*w3); assert w3m == Fr(-3, 2) and E(line(w3m, (0, 12))) == "y = −(3/2)x + 12" and Fr(12) / Fr(3, 2) == 8
w4L = line(Fr(-1, 2), (4, 1)); assert E(w4L) == "y = −½x + 3" and on(w4L, (-2, 4))
w5 = (Fr(-4, 6), Fr(12, 6)); assert w5 == (Fr(-2, 3), 2) and E(w5) == "y = −⅔x + 2" and on(w5, (3, 0))

pack = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Coordinate Geometry of the Line Teacher Pack | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{PACK_STYLE}
{FIGCSS}
.ss td:nth-child(2){{width:40%}}.ss td,.ss th{{padding:2px 5px;font-size:8.8pt;line-height:1.3}}.fym .c{{height:16mm}}.fym .fc{{font-size:13pt}}.fym .fc.sm{{font-size:8.6pt}}.p1 .proc td{{font-size:8.5pt;padding:2px 6px}}
.pf2{{display:grid;grid-template-columns:1fr 1.15fr;gap:6mm;align-items:center}}.pf2 svg{{max-height:80mm}}.dom .r{{font-size:9.4pt}}.dom .l{{font-size:12pt}}
.ops div{{font-size:13pt}}
</style></head><body>

<div class="page p1">
  <div class="band"><div><div class="k">Junior Cycle Maths · Teacher pack</div><h1>Coordinate geometry of the line</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2018 specification): {LO}</p>
  <div class="two">
    <div><h3>Aims</h3><p>By the end of the lesson students can find the midpoint, length and slope of a line segment, interpret slope as a rate of change and the y-intercept as a starting value, find and use the equation of a line (y = mx + c and y − y₁ = m(x − x₁)), recognise parallel lines, read where two lines meet, and (Higher Level) use perpendicular slopes and ax + by + c = 0.</p></div>
    <div><h3>In this pack</h3><p>p.1 Teacher notes · p.2 Line Lab mingle cards + Line Swap A/B cards · p.3 Line Dominoes (cut-up) · p.4 Wall poster · p.5 Worksheet: Error Hunt + exam-style questions · p.6 Answers. Level: 3rd year (Higher and Ordinary). Time: about 60 minutes. All questions are original. Squared paper helps.</p></div>
  </div>
  <h2 style="margin-top:8px">Procedure</h2>
  <table class="proc"><tbody>
    <tr><td>5 min</td><td><b>Lead-in: which is steeper?</b> Show two ramps drawn on the board (or two ski slopes): one rises 2 for every 3 across, one rises 3 for every 5. Pairs decide which is steeper and how they know. Elicit "rise ÷ run".</td></tr>
    <tr><td>8 min</td><td><b>Guided discovery.</b> Pairs fill in a table for y = 2x + 1 and y = 2x − 3 (x = −2 to 2), plot both on one grid and compare. "What's the same? What's different? Where do the 2 and the −3 show up on the graph?" Build y = mx + c, then ask what y = −2x + 1 would look like.</td></tr>
    <tr><td>10 min</td><td><b>Line Lab mingle</b> (p.2, 24 cards = 12 question/answer pairs; one card each). Question card? Work it out and find the person with your answer. Answer card? Find your question. Pairs check each other's working on mini-whiteboards.</td></tr>
    <tr><td>12 min</td><td><b>Line Swap</b> (p.2, pairs, don't show your card). Each fact is on only ONE card. Ask your partner for what you're missing ("Where is point B?"), then both fill every blank. Feedback: midpoint {c(s_mid)}, slope {fs(s_m)}, |AB| {s_len}, {E(s_L)}; k: y = −x + 7; meet at {c(s_meet)}; {E(s_par)}.</td></tr>
    <tr><td>10 min</td><td><b>Line Dominoes</b> (p.3), groups of 3–4. Start with START, work out the clue, find the domino with that answer on its left, and build the chain to FINISH.</td></tr>
    <tr><td>12 min</td><td><b>Worksheet</b> (p.5). Error Hunt in pairs (find the mistake, name it, fix it), then the exam-style questions alone. Questions 2(d) and 5 are Higher Level.</td></tr>
    <tr><td>3 min</td><td><b>Exit ticket.</b> The slope and midpoint of (1, 2) and (5, 10)? (2; (3, 6).) Homework: play <b>Line Lab</b> at leim.ie/line-lab.html and copy three lines from the "Go back over these" list.</td></tr>
  </tbody></table>
  <div class="note"><b>Mingle key</b> (question card → answer card): {match_key}.<br>
  <b>Errors to look for:</b> run ÷ rise · losing a minus with negatives · subtracting for the midpoint · adding instead of squaring for distance · reading c as the slope · not getting y on its own first · parallel slope with the wrong sign. <b>Support:</b> a card with the formulas and (x₁, y₁), (x₂, y₂) labels. <b>Fast finishers:</b> find two points whose midpoint is (0, 0) and whose distance apart is 10.</div>
  <p class="small"><b>Domino answer chain</b> (START → FINISH):</p>
  <ol class="small" style="columns:2;column-gap:12px;font-size:7.2pt;line-height:1.22;margin:0;padding-left:16px">{chain_key}</ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">Cut up the cards · one Line Swap card per student</div><h1>Line Lab mingle + Line Swap</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:8.8pt;margin:0"><b>Line Lab mingle.</b> Cut out the 24 cards and give one to each student. Question card? Work it out, then find the person with your answer. Answer card? Find the question that gives your answer. (Fewer students? Take out whole pairs.)</p>
  <div class="fym">{match_html}</div>
  <p style="font-size:8.8pt;margin:3mm 0 0"><b>Line Swap.</b> Don't show your card. Each fact is on only one of the two cards: ask your partner for what you're missing, then fill in every blank on both tables.</p>
  {swap_card("A")}
  {swap_card("B")}
</div>

<div class="page">
  <div class="band"><div><div class="k">Groups of 3–4 · cut along the dashed lines</div><h1>Line Dominoes</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.4pt">Start with START. Work out the clue on the right, then find the domino with that answer on its left. Keep going until you reach FINISH. Equations are written as y = mx + c. The last two clues are Higher Level (Ordinary Level groups can be given those answers).</p>
  <div class="doms">{dom_html}</div>
</div>

<div class="page">
  <div class="poster">
    <h1>Lines: the key facts</h1>
    <div class="pf2"><div>{FIG["poster"]}</div><div style="font-size:15pt;line-height:1.5"><b>Slope = rise ÷ run</b><br>A(−1, −1) to B(2, 1):<br>run 3, rise 2, slope 2/3<br><span style="font-size:12pt;color:var(--muted)">Rises: positive · falls: negative · flat: 0</span></div></div>
    <div class="ops">
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Slope</b>m = (y₂ − y₁) ÷ (x₂ − x₁)</div>
      <div style="background:var(--green-soft)"><b>Midpoint</b>((x₁ + x₂) ÷ 2, (y₁ + y₂) ÷ 2)</div>
      <div style="background:var(--green-soft)"><b>Distance</b>√((x₂ − x₁)² + (y₂ − y₁)²)</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Equation</b>y = mx + c<br>y − y₁ = m(x − x₁)</div>
    </div>
    <p style="text-align:center;font-size:13pt;margin:0"><b>Parallel:</b> same slope &nbsp;·&nbsp; <b>Perpendicular (HL):</b> m₁ × m₂ = −1</p>
    <p style="text-align:center;font-size:10pt;color:var(--muted)">Léim · leim.ie · Play Line Lab: leim.ie/line-lab.html</p>
  </div>
</div>

<div class="page ws">
  <div class="band"><div><div class="k">Worksheet</div><h1>Error Hunt + exam-style questions</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Error Hunt</h2>
  <p>Each answer has one mistake. Find it, say what went wrong, and write the right answer.</p>
  <table class="eh"><thead><tr><th>Question</th><th>Student's answer</th><th>The mistake and the right answer</th></tr></thead><tbody>
  {"".join(f"<tr><td>{q}</td><td>{w}</td><td><span class='gap'></span><span class='gap'></span></td></tr>" for q,w,r in ERR)}
  </tbody></table>
  <h2>B. Exam-style questions (show all your work)</h2>
  <div class="gfig" style="width:40mm">{FIG["w2"]}</div>
  <ol class="q">
    <li>A is (−1, −3) and B is (3, 5). Find (a) the midpoint of [AB], (b) the slope of AB, (c) |AB| to 1 decimal place, (d) the equation of AB.<span class="long"></span></li>
    <li>The lines l and k are shown. (a) Write the equation of each line. (b) Where do l and k meet? Check it in both equations. (c) Where does k cross the x-axis? (d) Higher Level: show that l and k are perpendicular.<span class="long"></span></li>
    <li style="clear:both">A barrel is leaking. A straight-line graph of the water in it goes through (0, 12) and (6, 3), with x in hours and y in litres. (a) Find the slope and say what it means. (b) Write the equation. (c) When will the barrel be empty?<span class="long"></span></li>
    <li>Find the equation of the line through (4, 1) with slope −½. Is (−2, 4) on this line?<span class="long"></span></li>
    <li>Higher Level: write 4x + 6y − 12 = 0 in the form y = mx + c, and show that (3, 0) is on the line.<span class="long"></span></li>
  </ol>
</div>

<div class="page an">
  <div class="band"><div><div class="k">For the teacher</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>Line Swap</h2>
  <div class="two"><table><tbody>
   <tr><td>Midpoint of [AB]</td><td><b>{c(s_mid)}</b></td></tr><tr><td>Slope of AB</td><td>8 ÷ 4 = <b>{fs(s_m)}</b></td></tr>
   <tr><td>|AB|</td><td>√(16 + 64) = √80 = <b>{s_len}</b></td></tr><tr><td>Equation of AB</td><td><b>{E(s_L)}</b></td></tr></tbody></table>
  <table><tbody>
   <tr><td>Equation of k</td><td><b>y = −x + 7</b></td></tr><tr><td>Where l and k meet</td><td><b>{c(s_meet)}</b> (2 × 2 + 1 = 5 ✓, −2 + 7 = 5 ✓)</td></tr>
   <tr><td>Through (1, 0) parallel to l</td><td><b>{E(s_par)}</b></td></tr></tbody></table></div>
  <h2>A. Error Hunt</h2>
  <table><tbody>{"".join(f"<tr><td style='width:40%'><b>{q}</b> {w}</td><td>{r}</td></tr>" for q,w,r in ERR)}</tbody></table>
  <h2>B. Exam-style questions</h2>
  <ol class="q">
    <li>(a) <b>(1, 1)</b> (b) 8 ÷ 4 = <b>2</b> (c) √80 = <b>8.9</b> (d) y − (−3) = 2(x − (−1)) → <b>y = 2x − 1</b></li>
    <li>(a) l: <b>{E(wl)}</b>, k: <b>{E(wk)}</b> (b) <b>{c(wP)}</b>: ½ × 2 − 1 = 0 ✓, −2 × 2 + 4 = 0 ✓ (c) <b>(2, 0)</b> (the same point) (d) ½ × (−2) = −1 ✓</li>
    <li>(a) (3 − 12) ÷ 6 = <b>−3/2</b>: the barrel loses 1.5 litres every hour (b) <b>y = −(3/2)x + 12</b> (c) 0 = −1.5x + 12 → <b>after 8 hours</b></li>
    <li>y − 1 = −½(x − 4) → <b>{E(w4L)}</b>; −½ × (−2) + 3 = 4 ✓ <b>yes</b></li>
    <li>6y = −4x + 12 → <b>{E(w5)}</b>; −⅔ × 3 + 2 = 0 ✓</li>
  </ol>
  <h2>Marking tip</h2>
  <p>Give credit for each step, as the exam does: the formula, the numbers substituted correctly (with brackets for negatives), and the answer. An equation that is right but not tidied into the form asked for usually loses only the last mark. In context questions insist on units and a sentence: "€2 per km", not just "2".</p>
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
<h1><span>Coordinate Geometry</span><br><span>of the Line</span></h1>
<div class="sub">Line Lab mingle · Line Swap A/B<br>Dominoes · Poster · Worksheet + answers</div>
<div class="em">y = mx + c</div></div>
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
    pdf("teacher-pack", os.path.join(OUT, "Coordinate-Geometry-of-the-Line-Teacher-Pack-Leim.pdf"))
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--hide-scrollbars", "--window-size=1200,1200",
                    f"--screenshot={os.path.join(OUT, f'{SLUG}-cover.png')}", f"{SLUG}-cover.html"], cwd=SRC, check=True, capture_output=True)
    print("domino chain:", [(x, a) for x, a in chain])
