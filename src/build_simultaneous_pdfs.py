#!/usr/bin/env python3
"""Simultaneous equations (JC Maths topic 29): free sheet + teacher pack + Payhip cover.
Run from the repo root: python3 src/build_simultaneous_pdfs.py OUTDIR
Writes src/simultaneous-equations-*.html; PDFs/cover PNG go to OUTDIR (free sheet also to printables/).
Graphs come from the Line Lab grid kit through src/line_figs_bridge.js and are read back with
test_line_lab.py's reader. Every answer is computed here with exact fractions and asserted.
Styles are read from src/build_money1_pdfs.py; the figure CSS from src/build_coordinate_line_pdfs.py."""
import os, sys, random, subprocess, re, json
from fractions import Fraction as Fr
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC)
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/simul"; os.makedirs(OUT, exist_ok=True)
SLUG = "simultaneous-equations"
LO = "AF.4, U.6"
M = "−"

# ---------- my own maths ----------
def n(v):
    v = Fr(v); s = M if v < 0 else ""; v = abs(v)
    return s + (str(v.numerator) if v.denominator == 1 else f"{v.numerator}/{v.denominator}")
def term(k, v, first):
    if k == 0: return ""
    a = abs(k); s = ("" if a == 1 else str(a)) + v
    return ((M if k < 0 else "") + s) if first else ((f" {M} " if k < 0 else " + ") + s)
def lin(E):
    a, b, c = E
    return (term(a, "x", True) + term(b, "y", False) if a else term(b, "y", True)) + " = " + n(c)
def yeq(m, k): return "y = " + term(m, "x", True) + ("" if k == 0 else f" + {k}" if k > 0 else f" {M} {-k}")
def solve(E1, E2):
    d = E1[0] * E2[1] - E1[1] * E2[0]; assert d != 0
    return (Fr(E1[2] * E2[1] - E1[1] * E2[2], d), Fr(E1[0] * E2[2] - E1[2] * E2[0], d))
def fits(E, P): return E[0] * P[0] + E[1] * P[1] == E[2]
def pr(P): return f"x = {n(P[0])}, y = {n(P[1])}"
def pt(P): return f"({n(P[0])}, {n(P[1])})"
def sys2(E1, E2): return f"{lin(E1)} and {lin(E2)}"
def Y(m, k): return (-m, 1, k)          # y = mx + k as ax + by = c
assert lin((3, -1, -4)) == "3x − y = −4" and lin((-1, 2, 0)) == "−x + 2y = 0" and yeq(-1, 5) == "y = −x + 5"
assert solve((3, 2, 16), (1, -2, 0)) == (4, 2)

# ---------- graphs from the Line Lab kit, each read back ----------
FIGS = {
    "meet": 'plane({R:5,lines:[{m:[-1,1],c:[5,1],n:"l"},{m:[2,1],c:[-1,1],n:"k",end:0}],pts:[{p:[2,3],n:"(2, 3)",dx:24,dy:4}]})',
    "pG": 'plane({R:5,lines:[{m:[1,1],c:[2,1],n:"l"},{m:[-2,1],c:[-1,1],n:"k",end:0}]})',
    "w2": 'plane({R:6,lines:[{m:[1,1],c:[1,1],n:"l"},{m:[-1,1],c:[5,1],n:"k",end:0}]})',
    "poster": 'plane({R:5,lines:[{m:[-1,1],c:[5,1],n:"l"},{m:[2,1],c:[-1,1],n:"k",end:0}],pts:[{p:[2,3],n:"(2, 3)",dx:24,dy:4}]})',
}
FIG = json.loads(subprocess.run(["node", os.path.join(SRC, "line_figs_bridge.js")], input=json.dumps(FIGS), capture_output=True, text=True, check=True).stdout)
_ns = {}; exec(open(os.path.join(SRC, "test_line_lab.py"), encoding="utf-8").read().split("if __name__")[0], _ns)
pics = {k: _ns["read_plane"](v) for k, v in FIG.items()}
def drawn(name, line_name): m, c = pics[name]["lines"][line_name]; return Y(m, c)
assert pics["meet"]["lines"] == {"l": (-1, 5), "k": (2, -1)} and pics["meet"]["pts"]["(2, 3)"] == (2, 3)
assert solve(drawn("meet", "l"), drawn("meet", "k")) == (2, 3)
G1, G2 = drawn("pG", "l"), drawn("pG", "k"); PG = solve(G1, G2); assert PG == (-1, 1)
W1, W2 = drawn("w2", "l"), drawn("w2", "k"); PW = solve(W1, W2); assert PW == (2, 3)
for k in list(FIG): FIG[k] = re.sub(r' style="max-width:\d+px"', "", FIG[k])

# ---------- free sheet ----------
A = [("Is x = 3, y = 1 a solution of x + y = 4 and 2x − y = 5?", "yes: 3 + 1 = 4 ✓, 6 − 1 = 5 ✓"),
     ("Is x = 2, y = 5 a solution of 3x + y = 11 and x − y = −2?", "no: 6 + 5 = 11 ✓ but 2 − 5 = −3 ✗"),
     ("2x + 3y = 19 and x = 5. Find y.", "3"),
     ("x − 4y = 2 and y = −1. Find x.", "−2"),
     ("Which of (1, 6), (2, 4) and (3, 2) fits both 2x + y = 8 and x + y = 5?", "(3, 2)"),
     ("Two numbers add up to 10 and their difference is 4. Find them.", "7 and 3")]
assert fits((1, 1, 4), (3, 1)) and fits((2, -1, 5), (3, 1)) and fits((3, 1, 11), (2, 5)) and not fits((1, -1, -2), (2, 5))
assert Fr(19 - 10, 3) == 3 and 2 + 4 * -1 == -2
assert [p for p in [(1, 6), (2, 4), (3, 2)] if fits((2, 1, 8), p) and fits((1, 1, 5), p)] == [(3, 2)] and solve((1, 1, 10), (1, -1, 4)) == (7, 3)
BS = [((1, 1, 7), (1, -1, 3)), ((2, 1, 11), (3, -1, 9)), ((3, 2, 16), (1, 2, 8)), ((5, 1, 17), (2, 1, 8)), ((4, -3, 10), (2, 3, 14)),
      ((x := (2, 3, 12)), (5, -2, 11)), ((3, 4, 10), (1, 2, 4)), ((2, 5, 1), (3, -2, 11)), ((x2 := (4, 3, 5)), (3, 2, 4)), ((1, -3, -11), (2, 1, 6))]
B = [(sys2(e1, e2), pr(solve(e1, e2))) for e1, e2 in BS]
for e1, e2 in BS: S = solve(e1, e2); assert S[0].denominator == 1 and S[1].denominator == 1, (e1, e2, S)
assert [a for q, a in B][:3] == ["x = 5, y = 2", "x = 4, y = 3", "x = 4, y = 2"], [a for q, a in B]
CS = [((3, 1), (2, 1, 11)), ((-2, 7), (3, 1, 12)), ((1, -4), (5, -2, -1))]       # y = mx + k, then ax + by = c
Cq = [(f"{yeq(*mk)} and {lin(E)}", pr(solve(Y(*mk), E))) for mk, E in CS]
for mk, E in CS: S = solve(Y(*mk), E); assert S[0].denominator == 1 and S[1].denominator == 1, (mk, E, S)
Cq += [("Use the graph. Write down the solution of the equations of l and k.", pr(PG)),
       ("Check your answer to question 20 in both equations: l is y = x + 2, k is 2x + y = −1.", "−1 + 2 = 1 ✓ and −2 + 1 = −1 ✓"),
       ("Solve y = x + 1 and y = 3x − 5 (they are equal, so x + 1 = 3x − 5).", pr(solve(Y(1, 1), Y(3, -5))))]
assert lin(G1) == "−x + y = 2" and lin(G2) == "2x + y = −1"
assert solve(Y(1, 2), (2, 1, -1)) == PG == (-1, 1) and solve(Y(1, 1), Y(3, -5)) == (3, 4)
# word problems
t1 = solve((1, 1, 120), (8, 5, 801)); t2 = solve((2, 1, 7), (1, 3, 11)); t3 = solve((1, 1, 30), (1, -1, 8))
t4 = solve((1, 1, 40), (2, 1, 55)); hl1 = solve((3, 2, 24), (1, -1, 3)); hl2 = solve((2, 4, 7), (2, -2, 1))
assert t1 == (67, 53) and t2 == (2, 3) and t3 == (19, 11) and t4 == (15, 25) and hl1 == (6, 3) and hl2 == (Fr(3, 2), 1)
D = [("A school show sold 120 tickets: adults €8, children €5. The takings were €801. Write two equations, then find how many of each ticket were sold.", "x + y = 120, 8x + 5y = 801: 67 adult, 53 child"),
     ("2 coffees and 1 scone cost €7. 1 coffee and 3 scones cost €11. Find the price of each.", "coffee €2, scone €3"),
     ("Two numbers add up to 30. One is 8 more than the other. Find them.", "19 and 11"),
     ("A farmer has 40 hens and sheep. Between them they have 110 legs. How many of each? (Hint: 2x + 4y = 110.)", "25 hens, 15 sheep"),
     ("Higher Level: solve x/2 + y/3 = 4 and x − y = 3.", pr(hl1)),
     ("Higher Level: solve 2x + 4y = 7 and 2x − 2y = 1.", pr(hl2))]
assert solve((1, 1, 40), (2, 4, 110)) == (25, 15)
assert Fr(6, 2) + Fr(3, 3) == 4
# exam-style
e1 = solve((3, -2, 4), (5, 3, 13)); e3 = solve((1, 1, 200), (12, 7, 1890))
assert e1 == (2, 1) and e3 == (98, 102)
Eq = [("<b>Solve and check.</b> Solve 3x − 2y = 4 and 5x + 3y = 13. Check your answer in both equations.",
       "× 3 and × 2: 9x − 6y = 12, 10x + 6y = 26; add: 19x = 38, <b>x = 2</b>, <b>y = 1</b>. Check: 6 − 2 = 4 ✓, 10 + 3 = 13 ✓"),
      (f"<b>Graph and algebra.</b> On a grid, draw the lines y = x + 1 and y = −x + 5 for x from 0 to 5. (a) Write down where they cross. (b) Solve the equations with algebra to check.",
       f"(a) <b>(2, 3)</b> (b) x + 1 = −x + 5 → 2x = 4 → x = 2, y = 3 ✓"),
      ("<b>Match tickets.</b> 200 people went to a match. Adult tickets cost €12 and child tickets cost €7. The takings were €1,890. (a) Write two equations. (b) How many children went?",
       "(a) x + y = 200, 12x + 7y = 1890 (b) 5x = 490, x = 98 adults, so <b>102 children</b>"),
      ("<b>Substitution.</b> (a) Solve y = 2x − 1 and 4x − 3y = 1. (b) Higher Level: solve 3x/2 − y = 2 and x + y/2 = 6.",
       "(a) 4x − 3(2x − 1) = 1 → −2x + 3 = 1 → <b>x = 1</b>, <b>y = 1</b>. Check: 4 − 3 = 1 ✓ (b) × 2: 3x − 2y = 4 and 2x + y = 12; y = 12 − 2x → 7x = 28: <b>x = 4, y = 4</b>")]
e4 = solve(Y(2, -1), (4, -3, 1)); assert e4 == (1, 1)
assert solve((3, -2, 4), (2, 1, 12)) == (4, 4) and Fr(3 * 4, 2) - 4 == 2 and 4 + Fr(4, 2) == 6
assert solve(Y(1, 1), Y(-1, 5)) == (2, 3)

def qs(items, cls=""): return "".join(f"<li>{q} <span class='line'></span></li>" for q, a in items)
def style(var):
    return re.search(var + r' = f"""<!doctype.*?<style>(.*?)</style>', open(os.path.join(SRC, "build_money1_pdfs.py"), encoding="utf-8").read(), re.S).group(1).replace("{LO}", LO).replace("{{", "{").replace("}}", "}")
SHEET_STYLE = style("sheet"); PACK_STYLE = style("pack")
FIGCSS = re.search(r'FIGCSS = """(.*?)"""', open(os.path.join(SRC, "build_coordinate_line_pdfs.py"), encoding="utf-8").read(), re.S).group(1)
assert "@bottom-left" in SHEET_STYLE and "Single-teacher licence" in PACK_STYLE and "svg.tg" in FIGCSS
EXTRA = ".wk{font-variant-numeric:tabular-nums;line-height:1.45;border:1.5px solid var(--line);border-radius:8px;padding:2px 7px;margin:3px 0;font-size:9.2pt}.wk b.h{display:block}.sys{white-space:nowrap}"

sheet = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Simultaneous equations: rules and practice | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{SHEET_STYLE}
{FIGCSS}
{EXTRA}
</style></head><body>
<div class="page tight">
  <div class="band"><div><div class="k">Junior Cycle Maths · Free revision sheet</div><h1>Simultaneous equations</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2018 specification): {LO}. Play the game: <b>leim.ie/two-line-crossing.html</b></p>
  <div class="two">
   <div><h2>1. What is the solution?</h2>
    <div class="gfig">{FIG["meet"]}</div>
    <p>Each equation on its own has lots of answers. The <b>solution</b> is the one pair (x, y) that fits <b>both</b>. On a graph it's where the lines <b>cross</b>: x + y = 5 (l) and y = 2x − 1 (k) cross at <b>(2, 3)</b>.</p>
    <h2 style="clear:both">2. Elimination</h2>
    <p>Make the x's or y's the same size, then <b>signs different → add</b>, <b>signs the same → subtract</b>.</p>
    <div class="wk">① 2x + 3y = 12 &nbsp; ② 5x − 2y = 11<br>① × 2: 4x + 6y = 24 &nbsp; ② × 3: 15x − 6y = 33<br>Add: 19x = 57, x = 3. In ①: 6 + 3y = 12, y = 2<br>Check ②: 15 − 4 = 11 ✓</div>
    <p>Multiply <b>every</b> term, including the number on the right.</p></div>
   <div><h2>3. Substitution</h2>
    <p>When one equation says <b>y = …</b>, put it into the other. <b>Keep the bracket.</b></p>
    <div class="wk">① y = 2x − 3 &nbsp; ② 3x + 2y = 15<br>3x + 2(2x − 3) = 15 → 7x − 6 = 15 → x = 3<br>y = 2(3) − 3 = 3. Check ②: 9 + 6 = 15 ✓</div>
    <h2>4. Word problems</h2>
    <p><b>Say what x and y stand for</b>, make <b>one equation from each fact</b>, solve, then answer in words. 120 tickets, adults €8, children €5, €801: x + y = 120 and 8x + 5y = 801 → 67 adults, 53 children.</p>
    <h2>5. Higher Level</h2>
    <p>Fractions in an equation: multiply every term by the common denominator (x/2 + y/3 = 4 → 3x + 2y = 24). Answers can be fractions (x = 3/2).</p>
    <div class="note"><b>Classic mistakes:</b> adding when the signs are the same · not multiplying the number on the right · dropping the bracket in substitution · finding x but not y · a pair that fits only one equation.</div></div>
  </div>
  <div class="tip"><b>Exam tip:</b> label the equations ① and ②, write each step ("① × 2", "① + ②"), find both letters, and write the check in the other equation.</div>
</div>

<div class="page p2">
  <div class="band"><div><div class="k">Practice · 32 questions</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Check and substitute</h2><ol class="q">{qs(A)}</ol>
  <h2>B. Elimination: solve each pair</h2><ol class="q" start="7" style="columns:2;column-gap:8mm">{"".join(f"<li class='sys'>{q}</li>" for q, a in B)}</ol>
  <h2>C. Substitution and graphs</h2>
  <div class="gfig" style="width:36mm">{FIG["pG"]}</div>
  <ol class="q" start="17">{qs(Cq)}</ol>
  <h2 style="clear:both">D. Word problems and Higher Level</h2><ol class="q" start="23">{qs(D)}</ol>
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
  <div class="note"><b>Got one wrong?</b> Check: did you add when the signs were different and subtract when they were the same? Did you multiply every term? Does your answer fit BOTH equations? Then play <b>Two-Line Crossing</b> at leim.ie/two-line-crossing.html: the "Go back over these" list at the end shows the rule for each mistake.</div>
  <p class="small">All questions written by Léim. Léim is independent and not connected with the State Examinations Commission or the NCCA.</p>
</div>
</body></html>"""
NQ = len(A) + len(B) + len(Cq) + len(D) + len(Eq)
assert NQ == 32, NQ

# ---------- teacher pack ----------
# Ticket Swap: each fact is on exactly ONE card
SW1 = [("Tickets sold", "150", "A"), ("Adult ticket", "€9", "A"), ("Child ticket", "€4", "B"), ("Takings", "€1,000", "B"),
       ("Equations", "", None), ("Adult tickets sold", "", None), ("Child tickets sold", "", None)]
sw1 = solve((1, 1, 150), (9, 4, 1000)); assert sw1 == (80, 70)
SW2 = [("3 hot chocolates + 1 muffin", "€13", "A"), ("1 hot chocolate + 2 muffins", "€11", "B"),
       ("Equations", "", None), ("One hot chocolate", "", None), ("One muffin", "", None)]
sw2 = solve((3, 1, 13), (1, 2, 11)); assert sw2 == (3, 4)
for rows in (SW1, SW2): assert sum(w == "A" for *_, w in rows) >= 1 and sum(w == "B" for *_, w in rows) >= 1
def swap_card(who):
    def tab(title, rows):
        return f'<table class="ss"><thead><tr><th colspan="2">{title}</th></tr></thead><tbody>' + "".join(
            f"<tr><td>{k}</td><td><b>{v if w == who else ''}</b></td></tr>" for k, v, w in rows) + "</tbody></table>"
    return f'<div class="idc"><h3>Student {who} · Ticket Swap</h3><div class="two">{tab("The school play", SW1)}{tab("The café", SW2)}</div></div>'

# Crossing Point mingle: 12 question cards, 12 different answer cards
MS = [((1, 1, 9), (1, -1, 5)), ((2, 1, 10), (1, -1, 2)), ((3, 1, 14), (1, 1, 8)), ((1, 2, 9), (1, -2, 1)), ((2, 3, 13), (2, 1, 7)),
      ((4, 1, -3), (2, -1, -9)), ((1, 1, 2), (3, -1, 14)), ((5, 2, 1), (3, -2, -9)), ((2, -1, -1), (3, 1, 6))]
MATCH = [(f"{lin(a)}<br>{lin(b)}", pt(solve(a, b))) for a, b in MS]
MATCH += [(f"{yeq(3, -1)}<br>{lin((2, 1, 9))}", pt(solve(Y(3, -1), (2, 1, 9)))),
          ("Two numbers add to 15 and differ by 9. (bigger, smaller)", pt(solve((1, 1, 15), (1, -1, 9)))),
          ("Where y = x + 4 and y = −x + 6 cross", pt(solve(Y(1, 4), Y(-1, 6))))]
ANS = [a for q, a in MATCH]
assert len(set(ANS)) == 12, ANS
for (a, b) in MS: S = solve(a, b); assert S[0].denominator == 1 and S[1].denominator == 1
cards = [q for q, a in MATCH] + ANS
random.seed(29); match_print = cards[:]; random.shuffle(match_print)
match_html = "".join(f'<div class="c"><span class="tag">Card {i}</span><div class="fc{" sm" if len(x) > 10 else ""}">{x}</div></div>' for i, x in enumerate(match_print, 1))
match_key = " · ".join(f"{match_print.index(q) + 1} → {match_print.index(a) + 1}" for q, a in MATCH)

# Simultaneous Dominoes: 20 clues, 20 different answers
DT = [((1, 1), (1, -1), (5, 3)), ((2, 1), (1, -1), (3, 3)), ((1, 1), (1, -1), (5, 6)), ((3, 1), (1, 1), (2, 4)), ((2, 3), (2, -1), (3, 2)),
      ((1, 2), (1, -2), (1, 3)), ((4, 1), (2, 1), (2, 1)), ((3, -1), (1, 1), (3, 5)), ((1, 3), (2, -3), (4, 2)), ((5, 1), (3, 1), (1, 2)),
      ((2, 1), (1, -1), (2, -3)), ((1, -1), (1, 1), (4, -3)), ((3, 2), (1, -2), (-2, 3)), ((2, 5), (1, 1), (1, 1))]
DS = [((a[0], a[1], a[0] * P[0] + a[1] * P[1]), (b[0], b[1], b[0] * P[0] + b[1] * P[1])) for a, b, P in DT]
DOMS = [(sys2(a, b), pt(solve(a, b))) for a, b in DS]
DOMS += [(f"{yeq(2, 1)} and {lin((1, 1, 13))}", pt(solve(Y(2, 1), (1, 1, 13)))),
         (f"{yeq(-1, 9)} and {yeq(1, 1)}", pt(solve(Y(-1, 9), Y(1, 1)))),
         ("x + y = 20, x − y = 6: x = ?", n(solve((1, 1, 20), (1, -1, 6))[0])),
         ("2x + y = 17, x − y = 1: y = ?", n(solve((2, 1, 17), (1, -1, 1))[1])),
         ("Higher Level: x/2 + y = 5, x − y = 1", pt(solve((1, 2, 10), (1, -1, 1)))),
         ("Higher Level: 2x + 2y = 5, 2x − 2y = 1", pt(solve((2, 2, 5), (2, -2, 1))))]
DANS = [a for k, a in DOMS]
for (a, b) in DS: S = solve(a, b); assert S[0].denominator == 1 and S[1].denominator == 1, (a, b, S)
assert len(set(DANS)) == 20, sorted(DANS)
assert DANS[-1] == "(3/2, 1)" and DANS[-2] == "(4, 3)"
random.seed(2929); chain = DOMS[:]; random.shuffle(chain)
dom = [("START" if k == 0 else chain[k - 1][1], x[0]) for k, x in enumerate(chain)] + [(chain[-1][1], "FINISH")]
dom_print = dom[:]; random.shuffle(dom_print)
dom_html = "".join(f'<div class="dom"><div class="h l{" sm" if len(l) > 9 else ""}">{l}</div><div class="h r">{r}</div></div>' for l, r in dom_print)
chain_key = "".join(f"<li>{x} = <b>{a}</b></li>" for x, a in chain)

ERR = [("x + 2y = 8 and 3x − 2y = 8. Add: 4x = 0", "4x = 0", "Subtracted the numbers. Add them too: 4x = 16, so <b>x = 4, y = 2</b>"),
       ("3x + y = 11 and x + y = 5. Add: 4x = 16, x = 4", "x = 4, y = 1", "The y's have the same sign: subtract. 2x = 6, <b>x = 3, y = 2</b>"),
       ("2x + 3y = 13 and x − y = 4. ② × 3: 3x − 3y = 4", "x = 17/5", "Multiply every term: 3x − 3y = 12. Add: 5x = 25, <b>x = 5, y = 1</b>"),
       ("y = 2x − 1 and 3x + 2y = 12. 3x + 4x − 1 = 12", "x = 13/7", "Keep the bracket: 3x + 2(2x − 1) = 12 → 7x − 2 = 12, <b>x = 2, y = 3</b>"),
       ("x + y = 7 and x − y = 1. Add: 2x = 8", "x = 4", "Not finished: find y too. 4 + y = 7, <b>y = 3</b>"),
       ("60 tickets, adults €5, children €3, takings €220", "x + y = 220, 5x + 3y = 60", "Swapped totals: <b>x + y = 60, 5x + 3y = 220</b> → 20 adults, 40 children")]
assert solve((1, 2, 8), (3, -2, 8)) == (4, 2) and solve((3, 1, 11), (1, 1, 5)) == (3, 2) and solve((2, 3, 13), (1, -1, 4)) == (5, 1)
assert solve(Y(2, -1), (3, 2, 12)) == (2, 3) and solve((1, 1, 7), (1, -1, 1)) == (4, 3) and solve((1, 1, 60), (5, 3, 220)) == (20, 40)
assert Fr(13 + 4, 5) == Fr(17, 5) and Fr(13, 7) == Fr(12 + 1, 3 + 4)
# worksheet exam-style
w1 = solve((4, 3, 18), (2, -5, -4)); assert w1 == (3, 2)
assert PW == (2, 3) and lin(W1) == "−x + y = 1" and lin(W2) == "x + y = 5"
w3 = solve((3, 2, 14), (2, 3, 16)); assert w3 == (2, 4)
w4 = solve(Y(-3, 10), (2, -1, 5)); assert w4 == (3, 1)
w5 = solve((4, 3, 48), (1, -1, -2)); assert w5 == (6, 8) and Fr(6, 3) + Fr(8, 4) == 4
w5b = solve((6, 4, 7), (2, -4, 1)); assert w5b == (1, Fr(1, 4))

pack = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Simultaneous Equations Teacher Pack | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{PACK_STYLE}
{FIGCSS}
{EXTRA}
.ss td:nth-child(2){{width:34%}}.ss td,.ss th{{padding:2px 5px;font-size:8.8pt;line-height:1.3}}.fym .c{{height:14.5mm}}.fym .fc{{font-size:12pt}}.fym .fc.sm{{font-size:8.2pt;line-height:1.15}}.idc{{padding:1.5mm 4mm}}.p1 .proc td{{font-size:8.5pt;padding:2px 6px}}
.pf2{{display:grid;grid-template-columns:1fr 1.15fr;gap:6mm;align-items:center}}.pf2 svg{{max-height:80mm}}.dom .r{{font-size:9.2pt}}.dom .l{{font-size:12pt}}
.ops div{{font-size:12pt}}
</style></head><body>

<div class="page p1">
  <div class="band"><div><div class="k">Junior Cycle Maths · Teacher pack</div><h1>Simultaneous equations</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2018 specification): {LO}</p>
  <div class="two">
    <div><h3>Aims</h3><p>By the end of the lesson students can check whether a pair of values solves two equations, solve simultaneous linear equations by elimination, by substitution and from a graph, check the answer in the other equation, and form and solve simultaneous equations from a word problem. Higher Level: fractions in the equations and answers that are fractions.</p></div>
    <div><h3>In this pack</h3><p>p.1 Teacher notes · p.2 Crossing Point mingle cards + Ticket Swap A/B cards · p.3 Simultaneous Dominoes (cut-up) · p.4 Wall poster · p.5 Worksheet: Error Hunt + exam-style questions · p.6 Answers. Level: 3rd year (Higher and Ordinary). Time: about 60 minutes. All questions are original.</p></div>
  </div>
  <h2 style="margin-top:8px">Procedure</h2>
  <table class="proc"><tbody>
    <tr><td>5 min</td><td><b>Lead-in: think of two numbers.</b> "I'm thinking of two numbers. They add up to 10." Pairs list all the whole-number answers. "Their difference is 4." Which pair now? Elicit that two facts pin down one pair.</td></tr>
    <tr><td>8 min</td><td><b>Guided discovery.</b> Pairs make a table of values for x + y = 5 and for y = 2x − 1 (x = 0 to 4), circle the pair in both tables, then plot both lines on one grid. "Where is your circled pair on the graph?" Then: "Add x + y = 5 to x − y = 1. What happens to y?" Build elimination from there.</td></tr>
    <tr><td>10 min</td><td><b>Crossing Point mingle</b> (p.2, 24 cards = 12 question/answer pairs; one card each). Question card? Solve it, then find the person with your answer, written as (x, y). Answer card? Find your pair of equations. Pairs check the answer in both equations.</td></tr>
    <tr><td>12 min</td><td><b>Ticket Swap</b> (p.2, pairs, don't show your card). Each fact is on only ONE card. Ask your partner for what you're missing ("How much is a child ticket?"), write the equations together, then both solve. Feedback: {SW1[0][1]} tickets → {sw1[0]} adult and {sw1[1]} child; hot chocolate €{sw2[0]}, muffin €{sw2[1]}.</td></tr>
    <tr><td>10 min</td><td><b>Simultaneous Dominoes</b> (p.3), groups of 3–4. Start with START, solve the clue, find the domino with that answer on its left, and build the chain to FINISH. Answers are written as (x, y) unless the clue asks for one letter.</td></tr>
    <tr><td>12 min</td><td><b>Worksheet</b> (p.5). Error Hunt in pairs (find the mistake, name it, fix it), then the exam-style questions alone. Question 5 is Higher Level.</td></tr>
    <tr><td>3 min</td><td><b>Exit ticket.</b> Solve x + y = 9 and x − y = 3 and check your answer. (x = 6, y = 3.) Homework: play <b>Two-Line Crossing</b> at leim.ie/two-line-crossing.html and copy three lines from the "Go back over these" list.</td></tr>
  </tbody></table>
  <div class="note"><b>Mingle key</b> (question card → answer card): {match_key}.<br>
  <b>Errors to look for:</b> adding when the signs are the same · not multiplying the number on the right · dropping the bracket in substitution · finding x but not y · not checking in the other equation · totals swapped in word problems. <b>Support:</b> a card with "signs different → add, signs the same → subtract". <b>Fast finishers:</b> make up two equations whose solution is x = −2, y = 5 and swap with a partner.</div>
  <p class="small"><b>Domino answer chain</b> (START → FINISH):</p>
  <ol class="small" style="columns:2;column-gap:12px;font-size:7.2pt;line-height:1.22;margin:0;padding-left:16px">{chain_key}</ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">Cut up the cards · one Ticket Swap card per student</div><h1>Crossing Point mingle + Ticket Swap</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:8.8pt;margin:0"><b>Crossing Point mingle.</b> Cut out the 24 cards and give one to each student. Question card? Solve it, then find the person with your answer (x, y). Answer card? Find the equations that give your answer. (Fewer students? Take out whole pairs.)</p>
  <div class="fym">{match_html}</div>
  <p style="font-size:8.8pt;margin:3mm 0 0"><b>Ticket Swap.</b> Don't show your card. Each fact is on only one of the two cards: ask your partner for what you're missing, write the two equations together, then fill in every blank.</p>
  {swap_card("A")}
  {swap_card("B")}
</div>

<div class="page">
  <div class="band"><div><div class="k">Groups of 3–4 · cut along the dashed lines</div><h1>Simultaneous Dominoes</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.4pt">Start with START. Solve the clue on the right, then find the domino with that answer on its left, written as (x, y) unless the clue asks for one letter. Keep going until you reach FINISH. The last two clues are Higher Level (Ordinary Level groups can be given those answers).</p>
  <div class="doms">{dom_html}</div>
</div>

<div class="page">
  <div class="poster">
    <h1>Simultaneous equations</h1>
    <div class="pf2"><div>{FIG["poster"]}</div><div style="font-size:15pt;line-height:1.5"><b>The solution fits BOTH.</b><br>l: x + y = 5<br>k: y = 2x − 1<br>They cross at <b>(2, 3)</b><br><span style="font-size:12pt;color:var(--muted)">x = 2, y = 3</span></div></div>
    <div class="ops">
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Elimination</b>Make the x's or y's match<br>signs different → <span style="font-weight:800">add</span><br>signs the same → <span style="font-weight:800">subtract</span></div>
      <div style="background:var(--green-soft)"><b>Substitution</b>y = … ? Put it into<br>the other equation.<br>Keep the bracket!</div>
      <div style="background:var(--green-soft)"><b>Graph</b>Draw both lines.<br>Read where they cross.</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Always</b>find x AND y,<br>then check in the<br>other equation ✓</div>
    </div>
    <p style="text-align:center;font-size:13pt;margin:0"><b>Word problems:</b> say what x and y stand for · one equation per fact · answer in words</p>
    <p style="text-align:center;font-size:10pt;color:var(--muted)">Léim · leim.ie · Play Two-Line Crossing: leim.ie/two-line-crossing.html</p>
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
  <div class="gfig" style="width:40mm">{FIG["w2"]}</div>
  <ol class="q">
    <li>Solve 4x + 3y = 18 and 2x − 5y = −4. Check your answer.<span class="long"></span></li>
    <li>The lines l: y = x + 1 and k: x + y = 5 are shown. (a) Use the graph to solve the equations. (b) Check your answer with algebra.<span class="long"></span></li>
    <li style="clear:both">3 sandwiches and 2 juices cost €14. 2 sandwiches and 3 juices cost €16. (a) Write two equations. (b) Find the price of each.<span class="long"></span></li>
    <li>Solve y = 10 − 3x and 2x − y = 5.<span class="long"></span></li>
    <li>Higher Level: (a) solve x/3 + y/4 = 4 and x − y = −2. (b) Solve 6x + 4y = 7 and 2x − 4y = 1.<span class="long"></span></li>
  </ol>
</div>

<div class="page an">
  <div class="band"><div><div class="k">For the teacher</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>Ticket Swap</h2>
  <div class="two"><table><tbody>
   <tr><td>Equations</td><td><b>x + y = 150, 9x + 4y = 1000</b></td></tr><tr><td>Adult tickets</td><td>× 4 and subtract: 5x = 400, <b>{sw1[0]}</b></td></tr>
   <tr><td>Child tickets</td><td><b>{sw1[1]}</b> (720 + 280 = 1000 ✓)</td></tr></tbody></table>
  <table><tbody>
   <tr><td>Equations</td><td><b>3x + y = 13, x + 2y = 11</b></td></tr><tr><td>Hot chocolate</td><td><b>€{sw2[0]}</b></td></tr>
   <tr><td>Muffin</td><td><b>€{sw2[1]}</b> (9 + 4 = 13 ✓)</td></tr></tbody></table></div>
  <h2>A. Error Hunt</h2>
  <table><tbody>{"".join(f"<tr><td style='width:42%'><b>{q}</b></td><td>{r}</td></tr>" for q,w,r in ERR)}</tbody></table>
  <h2>B. Exam-style questions</h2>
  <ol class="q">
    <li>② × 2: 4x − 10y = −8; subtract from ①: 13y = 26, <b>y = 2</b>, <b>x = 3</b>. Check: 6 − 10 = −4 ✓</li>
    <li>(a) <b>x = 2, y = 3</b> (b) x + (x + 1) = 5 → 2x = 4 → x = 2, y = 3 ✓</li>
    <li>(a) 3x + 2y = 14, 2x + 3y = 16 (b) × 3 and × 2: 9x + 6y = 42, 4x + 6y = 32; subtract: 5x = 10: <b>sandwich €2, juice €4</b></li>
    <li>2x − (10 − 3x) = 5 → 5x = 15 → <b>x = 3</b>, <b>y = 1</b></li>
    <li>(a) × 12: 4x + 3y = 48; x = y − 2 → 7y = 56 → <b>y = 8, x = 6</b> (b) add: 8x = 8, <b>x = 1</b>; 2 − 4y = 1, <b>y = 1/4</b></li>
  </ol>
  <h2>Marking tip</h2>
  <p>Give credit for each step, as the exam does: a correct method to get rid of one letter, the first value, the second value, and the check. An answer with x only is not finished. In word problems insist on "x = adult tickets" at the start and a sentence at the end.</p>
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
<h1><span>Simultaneous</span><br><span>Equations</span></h1>
<div class="sub">Crossing Point mingle · Ticket Swap A/B<br>Dominoes · Poster · Worksheet + answers</div>
<div class="em">x + y = 5 · x − y = 1</div></div>
<div class="foot"><span>↗ Léim · leim.ie</span><span class="price">Ready to teach · 60 min</span></div>
</body></html>"""
assert solve((1, 1, 5), (1, -1, 1)) == (3, 2)

if __name__ == "__main__":
    for name, txt in [("rules-and-practice", sheet), ("teacher-pack", pack), ("cover", cover)]:
        plain = re.sub(r"<[^>]+>", " ", re.sub(r"<style>.*?</style>|<svg.*?</svg>", "", txt, flags=re.S))
        assert not re.search(r"[\dxy)]\s*-\s*[\dxy(]|[=(]\s*-\d|(?<![\w])-\d", plain), (name, re.findall(r".{20}[\dxy)]\s*-\s*[\dxy(].{10}|.{10}[=(]\s*-\d.{10}", plain)[:3])
        open(os.path.join(SRC, f"{SLUG}-{name}.html"), "w", encoding="utf-8").write(txt)
    def pdf(name, out):
        subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--no-pdf-header-footer", f"--print-to-pdf={out}",
                        f"{SLUG}-{name}.html"], cwd=SRC, check=True, capture_output=True)
        d = open(out, "rb").read(); print(name, len(re.findall(rb"/Type\s*/Page[^s]", d)), "pages")
    pdf("rules-and-practice", os.path.join(ROOT, "printables", f"{SLUG}-rules-and-practice.pdf"))
    pdf("teacher-pack", os.path.join(OUT, "Simultaneous-Equations-Teacher-Pack-Leim.pdf"))
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--hide-scrollbars", "--window-size=1200,1200",
                    f"--screenshot={os.path.join(OUT, f'{SLUG}-cover.png')}", f"{SLUG}-cover.html"], cwd=SRC, check=True, capture_output=True)
    print("domino chain:", [(x, a) for x, a in chain])
