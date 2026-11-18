#!/usr/bin/env python3
"""Inequalities (JC Maths topic 34): free sheet + teacher pack + Payhip cover.
Run from the repo root: python3 src/build_inequalities_pdfs.py OUTDIR
Writes src/inequalities-*.html; PDFs/cover PNG go to OUTDIR (free sheet also to printables/).
Number lines and graphs come from the Number-Line Shade kit through src/number_line_figs_bridge.js and are
read back with test_number_line_shade.py's reader. Every answer is computed with exact fractions and asserted.
Styles are read from src/build_money1_pdfs.py."""
import os, sys, random, subprocess, re, json
from fractions import Fraction as Fr
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC)
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/ineq"; os.makedirs(OUT, exist_ok=True)
SLUG = "inequalities"
LO = "AF.4, AF.7c, U.6"
M = "−"

# ---------- the checker's own maths (parse + solve with exact fractions) ----------
_ns = {}; exec(open(os.path.join(SRC, "test_number_line_shade.py"), encoding="utf-8").read().split("if __name__")[0], _ns)
parse_ineq, int_list, read_nl, Iv, same, matches_picture = (_ns[k] for k in ("parse_ineq", "int_list", "read_nl", "Iv", "same", "matches_picture"))
def n(v):
    v = Fr(v); s = M if v < 0 else ""; v = abs(v)
    return s + (str(v.numerator) if v.denominator == 1 else f"{v.numerator}/{v.denominator}")
def show(iv, v="x"):
    if iv.lo is not None and iv.hi is not None: return f"{n(iv.lo)} {'≤' if iv.loIn else '<'} {v} {'≤' if iv.hiIn else '<'} {n(iv.hi)}"
    if iv.lo is not None: return f"{v} {'≥' if iv.loIn else '>'} {n(iv.lo)}"
    return f"{v} {'≤' if iv.hiIn else '<'} {n(iv.hi)}"
def sol(q): return show(parse_ineq(q)[0])                       # "2x + 1 < 9" -> "x < 4"
def lst(q):                                                      # "... , x ∈ ℕ" -> "{1, 2, 3}"
    iv, st = parse_ineq(q); L = int_list(iv, st); assert L and len(L) < 30, q
    return "{" + ", ".join(n(x) for x in L) + "}"
def big(q): iv, st = parse_ineq(q); return n(max(int_list(iv, st, -300, 300)))
def small(q): iv, st = parse_ineq(q); return n(min(int_list(iv, st, -300, 300)))
def count(q): iv, st = parse_ineq(q); return str(len(int_list(iv, st)))
def floor_(a, b): return Fr(a, b).numerator // Fr(a, b).denominator
def ceil_(a, b): return -((-Fr(a, b).numerator) // Fr(a, b).denominator)
assert sol("2x + 1 < 9") == "x < 4" and sol("5 − 2x > 11") == "x < −3" and sol("−1 < 2x + 3 ≤ 11") == "−2 < x ≤ 4"
assert lst("2x + 1 < 9, x ∈ ℕ") == "{1, 2, 3}" and small("2x + 3 > 8, x ∈ ℤ") == "3" and sol("(x + 2)/3 ≥ 4") == "x ≥ 10"

# ---------- figures from the game's kit, each read back ----------
def NL(lo=None, loIn=False, hi=None, hiIn=False, st="R", L=-2, R=8):
    j = lambda v: "null" if v is None else str(v)
    return f'nl({{lo:{j(lo)},loIn:{str(loIn).lower()},hi:{j(hi)},hiIn:{str(hiIn).lower()}}},"{st}",{L},{R})'
FIGS = {
    "A": NL(lo=3), "B": NL(hi=3, hiIn=True), "C": NL(lo=-1, loIn=True, hi=4, L=-3, R=7),
    "D": NL(hi=4, st="N", L=0, R=10), "E": NL(lo=-2, loIn=True, st="Z", L=-5, R=5), "F": NL(lo=-2, loIn=True, L=-5, R=5),
    "q1": NL(lo=-1, loIn=True, L=-5, R=5), "q2": NL(hi=2, L=-4, R=6), "q3": NL(lo=-3, hi=1, hiIn=True, L=-5, R=5),
    "g1": "graphSVG(1,1,3)", "e3": "graphSVG(-1,5,2)", "w4": "graphSVG(1,-2,1)",
    "pA": NL(lo=2, L=-2, R=8), "pB": NL(hi=2, hiIn=True, L=-2, R=8),
}
# Shade Match mingle: 12 question cards, 12 number-line answer cards
MATCH = [("x + 3 > 5", (2, False, None, False, "R", -2, 8)), ("2x ≤ 8", (None, False, 4, True, "R", -1, 9)),
         ("3x − 1 ≥ 5", (2, True, None, False, "R", -2, 8)), ("x − 4 < −3", (None, False, 1, False, "R", -4, 6)),
         ("4x + 2 < 2x + 8", (None, False, 3, False, "R", -2, 8)), ("2(x + 1) ≥ 0", (-1, True, None, False, "R", -5, 5)),
         ("−2 ≤ x < 3", (-2, True, 3, False, "R", -5, 5)), ("x < 4, x ∈ ℕ", (None, False, 4, False, "N", 0, 10)),
         ("2x + 1 ≤ 9, x ∈ ℕ", (None, False, 4, True, "N", 0, 10)), ("x ≥ −1, x ∈ ℤ", (-1, True, None, False, "Z", -5, 5)),
         ("−x > 2 (Higher Level)", (None, False, -2, False, "R", -7, 3)), ("1 < x + 3 ≤ 5, x ∈ ℤ", (-2, False, 2, True, "Z", -5, 5))]
for i, (q, (lo, li, hi, hii, st, L, R)) in enumerate(MATCH): FIGS[f"m{i}"] = NL(lo, li, hi, hii, st, L, R)
FIG = json.loads(subprocess.run(["node", os.path.join(SRC, "number_line_figs_bridge.js")], input=json.dumps(FIGS), capture_output=True, text=True, check=True).stdout)
def pic(k): return read_nl(FIG[k])
def fits(k, q): iv, st = parse_ineq(q); return matches_picture(pic(k), iv, st)
for k, q in [("A", "x > 3"), ("B", "x ≤ 3"), ("C", "−1 ≤ x < 4"), ("D", "x < 4, x ∈ ℕ"), ("E", "x ≥ −2, x ∈ ℤ"), ("F", "x ≥ −2"),
             ("q1", "x ≥ −1"), ("q2", "x < 2"), ("q3", "−3 < x ≤ 1"), ("pA", "x > 2"), ("pB", "x ≤ 2")]: assert fits(k, q), k
assert not fits("A", "x ≥ 3") and not fits("D", "x < 4, x ∈ ℤ") and not fits("E", "x ≥ −2")
# every mingle picture fits its own card and no other card
mq = [re.sub(r" \(Higher Level\)", "", q) for q, _ in MATCH]
for i in range(12):
    assert [j for j in range(12) if fits(f"m{i}", mq[j])] == [i], (i, [j for j in range(12) if fits(f"m{i}", mq[j])])
def graph_read(k):  # the line's slope sign, the crossing x and the level k, measured from the drawing
    h = FIG[k]; a = lambda t: dict(re.findall(r'([\w-]+)="([^"]*)"', re.search(r"<%s[^>]*>" % t, h).group(0)))
    top = a("svg"); xa, ya = int(top["data-xa"]), int(top["data-ya"]); sx, sy = Fr(top["data-sx"]), Fr(top["data-sy"]); p, H = int(top["data-p"]), int(top["data-h"])
    fn = a('line class="fn"'); kl = a('line class="kl"')
    X = lambda px: (Fr(px) - p) / sx + xa; Y = lambda py: (H - p - Fr(py)) / sy + ya
    x1, y1, x2, y2 = X(fn["x1"]), Y(fn["y1"]), X(fn["x2"]), Y(fn["y2"]); kk = round(Y(kl["y1"])); m = (y2 - y1) / (x2 - x1)
    return round(m), round(x1 + (kk - y1) / m), kk
assert graph_read("g1") == (1, 2, 3) and graph_read("e3") == (-1, 3, 2) and graph_read("w4") == (1, 3, 1)
for k in list(FIG):
    FIG[k] = re.sub(r' style="max-width:\d+px;display:block;margin:[^"]*"', "", FIG[k])
    FIG[k] = FIG[k].replace(' style="max-width:360px;display:block;margin:4px auto;background:#fff;border:2px solid var(--line);border-radius:12px"', "")

# ---------- free sheet ----------
A = [("Write the inequality shown in picture (1).", "x ≥ −1"), ("Picture (2).", "x < 2"), ("Picture (3).", "−3 < x ≤ 1"),
     ("Write as an inequality: x is at least 7.", "x ≥ 7"), ("Write as an inequality: x is at most −2.", "x ≤ −2"),
     ("Which of −3, 0, 2 and 5 make x &gt; 0 true?", "2 and 5")]
BQ = ["x + 5 < 9", "x − 3 ≥ −1", "3x ≤ 12", "2x + 1 > 9", "5x − 4 ≥ 11", "3x + 2 < x + 10", "4(x − 1) ≤ 12", "7 + 2x > 1"]
B = [(f"Solve {q}, x ∈ ℝ." + (" Show it on a number line." if i == 4 else ""), sol(q)) for i, q in enumerate(BQ)]
assert [a for q, a in B] == ["x < 4", "x ≥ 2", "x ≤ 4", "x > 4", "x ≥ 3", "x < 4", "x ≤ 4", "x > −3"]
CQ = [("List the values: 3x − 1 < 11, x ∈ ℕ.", lst("3x − 1 < 11, x ∈ ℕ")), ("List the values: x + 4 ≤ 7, x ∈ ℕ.", lst("x + 4 ≤ 7, x ∈ ℕ")),
      ("List the values: −2 ≤ x < 2, x ∈ ℤ.", lst("−2 ≤ x < 2, x ∈ ℤ")), ("How many values? −1 < x ≤ 4, x ∈ ℤ.", count("−1 < x ≤ 4, x ∈ ℤ")),
      ("Smallest value of x: 2x + 3 > 8, x ∈ ℤ.", small("2x + 3 > 8, x ∈ ℤ")), ("Largest value of x: 3x − 2 ≤ 12, x ∈ ℤ.", big("3x − 2 ≤ 12, x ∈ ℤ")),
      ("Smallest value of x: 4x + 1 ≥ 2x + 8, x ∈ ℤ.", small("4x + 1 ≥ 2x + 8, x ∈ ℤ")), ("List the values: 5x < 2x + 13, x ∈ ℕ.", lst("5x < 2x + 13, x ∈ ℕ"))]
assert [a for q, a in CQ] == ["{1, 2, 3}", "{1, 2, 3}", "{−2, −1, 0, 1}", "5", "3", "4", "4", "{1, 2, 3, 4}"], [a for q, a in CQ]
gm, gx, gk = graph_read("g1")
D = [("A taxi costs €3 plus €2 per km. You have €20. What is the greatest whole number of km you can go?", str(floor_(20 - 3, 2))),
     ("A lift can carry 500 kg. A worker weighs 75 kg. Boxes weigh 20 kg each. What is the greatest number of boxes the worker can bring?", str(floor_(500 - 75, 20))),
     ("Ella has €40 and saves €15 a week. She needs €200. What is the fewest number of weeks?", str(ceil_(200 - 40, 15))),
     (f"The graph shows y = x + 1 and the dashed line y = 3. For which values of x is y &lt; 3?", "x < 2"),
     ("Higher Level: solve 4 − 3x ≥ 10.", sol("4 − 3x ≥ 10")), ("Higher Level: solve −3 ≤ 2x + 1 < 9.", sol("−3 ≤ 2x + 1 < 9")),
     ("Higher Level: solve (x − 1)/2 > 3.", sol("(x − 1)/2 > 3")), ("Higher Level: list the values: −5 < 3x + 1 ≤ 10, x ∈ ℤ.", lst("−5 < 3x + 1 ≤ 10, x ∈ ℤ"))]
assert [a for q, a in D] == ["8", "21", "11", "x < 2", "x ≤ −2", "−2 ≤ x < 4", "x > 7", "{−1, 0, 1, 2, 3}"], [a for q, a in D]
assert (gm, gx, gk) == (1, 2, 3)   # y = x + 1 meets y = 3 at x = 2 and rises, so y < 3 for x < 2
# exam-style
E1 = sol("3(x + 2) ≤ x + 14"); E1b = lst("3(x + 2) ≤ x + 14, x ∈ ℕ"); assert E1 == "x ≤ 4" and E1b == "{1, 2, 3, 4}"
E2 = floor_(400 - 120, 8); assert E2 == 35 and 120 + 8 * 35 == 400
em, ex_, ek = graph_read("e3"); assert (em, ex_, ek) == (-1, 3, 2) and sol("−x + 5 ≥ 2") == "x ≤ 3"
E4a = sol("2 − 5x < 17"); E4b = lst("−7 ≤ 2x − 1 < 5, x ∈ ℤ"); assert E4a == "x > −3" and E4b == "{−3, −2, −1, 0, 1, 2}"
Eq = [("<b>Solve and show.</b> (a) Solve 3(x + 2) ≤ x + 14, x ∈ ℝ. (b) Show your answer on a number line. (c) List the values of x if x ∈ ℕ.",
       f"(a) 3x + 6 ≤ x + 14 → 2x ≤ 8 → <b>{E1}</b> (b) closed dot at 4, shaded left, arrow (c) <b>{E1b}</b>"),
      ("<b>The school bus.</b> A bus costs €120 to hire plus €8 for each student. The class has €400. (a) Write an inequality in s, the number of students. (b) What is the greatest number of students who can go?",
       f"(a) <b>120 + 8s ≤ 400</b> (b) 8s ≤ 280 → s ≤ 35: <b>{E2} students</b> (exactly €400 is allowed)"),
      ("<b>From a graph.</b> The graph shows y = −x + 5 and the dashed line y = 2. (a) Use the graph to find the values of x for which y ≥ 2. (b) Check with algebra.",
       "(a) the line meets y = 2 at x = 3 and is above it to the left: <b>x ≤ 3</b> (b) −x + 5 ≥ 2 → 3 ≥ x ✓"),
      ("<b>Higher Level.</b> (a) Solve 2 − 5x &lt; 17. (b) List the values of x for which −7 ≤ 2x − 1 &lt; 5, x ∈ ℤ, and show them on a number line.",
       f"(a) −5x &lt; 15 → divide by −5, flip: <b>{E4a}</b> (b) −6 ≤ 2x &lt; 6 → −3 ≤ x &lt; 3: <b>{E4b}</b>, six dots")]

EFIG = f'<div class="gfig" style="width:42mm">{FIG["e3"]}</div>'
def qs(items): return "".join(f"<li>{q} <span class='line'></span></li>" for q, a in items)
def style(var):
    return re.search(var + r' = f"""<!doctype.*?<style>(.*?)</style>', open(os.path.join(SRC, "build_money1_pdfs.py"), encoding="utf-8").read(), re.S).group(1).replace("{LO}", LO).replace("{{", "{").replace("}}", "}")
SHEET_STYLE = style("sheet"); PACK_STYLE = style("pack")
assert "@bottom-left" in SHEET_STYLE and "Single-teacher licence" in PACK_STYLE
FIGCSS = """svg.nl,svg.gr{display:block;width:100%;height:auto;margin:0 auto}svg.gr{background:#fff;border:1.5px solid var(--line);border-radius:6px}
.gfig{float:right;width:40mm;margin:0 0 1mm 3mm}.nlf{border:1.5px solid var(--line);border-radius:8px;padding:1px 6px 0;margin:2px 0;font-size:9pt}.nlf b{display:block}
.nl3{display:grid;grid-template-columns:repeat(3,1fr);gap:2mm;margin:1mm 0 2mm}.nl3 div{border:1.5px solid var(--line);border-radius:8px;padding:1px 4px 0;font-size:8.6pt;font-weight:700}
.sg{display:grid;grid-template-columns:repeat(4,1fr);gap:1.5mm;margin:1mm 0}.sg div{border:1.5px solid var(--line);border-radius:8px;text-align:center;font-size:8.4pt;padding:1px}.sg b{display:block;font-size:15pt;line-height:1.1}"""
EXTRA = ".wk{font-variant-numeric:tabular-nums;line-height:1.45;border:1.5px solid var(--line);border-radius:8px;padding:2px 7px;margin:3px 0;font-size:9.2pt}.wk b.h{display:block}"

sheet = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Inequalities: rules and practice | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{SHEET_STYLE}
{FIGCSS}
{EXTRA}
</style></head><body>
<div class="page tight">
  <div class="band"><div><div class="k">Junior Cycle Maths · Free revision sheet</div><h1>Inequalities</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2018 specification): {LO}. Play the game: <b>leim.ie/number-line-shade.html</b></p>
  <div class="two">
   <div><h2>1. The four signs</h2>
    <div class="sg"><div><b>&lt;</b>less than</div><div><b>&gt;</b>greater than</div><div><b>≤</b>less than or equal to</div><div><b>≥</b>greater than or equal to</div></div>
    <p><b>at least</b> 5 → x ≥ 5 · <b>at most</b> 5 → x ≤ 5 · <b>more than</b> 5 → x &gt; 5 · <b>under</b> 5 → x &lt; 5</p>
    <h2>2. On a number line</h2>
    <div class="nlf"><b>x &gt; 3: open dot (3 not included)</b>{FIG["A"]}</div>
    <div class="nlf"><b>x ≤ 3: closed dot (3 included)</b>{FIG["B"]}</div>
    <div class="nlf"><b>−1 ≤ x &lt; 4: shade from dot to dot</b>{FIG["C"]}</div>
    <h2>3. ℕ, ℤ or ℝ?</h2>
    <div class="nlf"><b>x &lt; 4, x ∈ ℕ (1, 2, 3 …): dots only</b>{FIG["D"]}</div>
    <div class="nlf"><b>x ≥ −2, x ∈ ℤ (negatives too): dots and …</b>{FIG["E"]}</div>
    <div class="nlf"><b>x ≥ −2, x ∈ ℝ (every number): a shaded line</b>{FIG["F"]}</div></div>
   <div><h2>4. Solving</h2>
    <p>Just like an equation: do the same to both sides.</p>
    <div class="wk"><b class="h">4x − 3 ≤ 2x + 9</b>2x − 3 ≤ 9 (subtract 2x) → 2x ≤ 12 (add 3) → <b>x ≤ 6</b> (÷ 2)</div>
    <p>Check with a number from your answer: x = 0 → −3 ≤ 9 ✓</p>
    <h2>5. Whole-number answers</h2>
    <p><b>2x + 1 &lt; 9, x ∈ ℕ</b> → x &lt; 4 → {{1, 2, 3}}. ℕ starts at 1.<br><b>2x + 3 &gt; 8, x ∈ ℤ</b> → x &gt; 2.5 → smallest value 3.<br><b>−1 &lt; x ≤ 3, x ∈ ℤ</b> → {{0, 1, 2, 3}}: 4 values.</p>
    <h2>6. Real life and graphs</h2>
    <p>€4 + €2 per km, €15 to spend: 4 + 2k ≤ 15 → k ≤ 5.5 → <b>5 km</b>. Round <b>down</b> for a limit, <b>up</b> for a target. From a graph: find where the line crosses the level, then read which side is below or above.</p>
    <h2>7. Higher Level</h2>
    <div class="wk"><b class="h">5 − 2x &gt; 11</b>−2x &gt; 6 → divide by −2 and <b>FLIP</b>: x &lt; −3</div>
    <div class="wk"><b class="h">−1 &lt; 2x + 3 ≤ 11</b>all three parts: −4 &lt; 2x ≤ 8 → −2 &lt; x ≤ 4</div>
    <div class="wk"><b class="h">(x + 2)/3 ≥ 4</b>× 3: x + 2 ≥ 12 → x ≥ 10</div>
    <div class="note"><b>Classic mistakes:</b> open and closed dots mixed up · 0 in an ℕ answer · a shaded line when x ∈ ℤ · forgetting to flip when dividing by a negative · rounding the wrong way in a word problem.</div></div>
  </div>
  <div class="tip"><b>Exam tip:</b> one step per line. On a number line, check three things: the dot (open or closed), the direction, and dots or a shaded line.</div>
</div>

<div class="page p2">
  <div class="band"><div><div class="k">Practice · 34 questions</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Read and write</h2>
  <div class="nl3"><div>(1){FIG["q1"]}</div><div>(2){FIG["q2"]}</div><div>(3){FIG["q3"]}</div></div>
  <ol class="q" style="columns:2;column-gap:8mm">{qs(A)}</ol>
  <h2>B. Solve, x ∈ ℝ</h2><ol class="q" start="7" style="columns:2;column-gap:8mm">{qs(B)}</ol>
  <h2>C. Whole numbers</h2><ol class="q" start="15" style="columns:2;column-gap:8mm">{qs(CQ)}</ol>
  <h2>D. Words, graphs and Higher Level</h2>
  <div class="gfig" style="width:46mm">{FIG["g1"]}</div>
  <ol class="q" start="23">{qs(D)}</ol>
  <p class="small" style="margin-top:4px">Questions 31–34 are on the next page.</p>
</div>

<div class="page">
  <div class="band"><div><div class="k">Exam-style · then check</div><h1>Exam corner + answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>E. Exam-style questions (show your work)</h2>
  <ol class="q e3" start="31">{"".join(f"<li>{EFIG if i == 2 else ''}{q}<span class='long'></span><span class='long'></span></li>" for i,(q,a) in enumerate(Eq))}</ol>
  <h2 style="margin-top:10px;clear:both">Answers</h2>
  <table class="ans"><tbody>
   <tr><td><b>A</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(A,1))}</td></tr>
   <tr><td><b>B</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(B,7))} (Q11: closed dot at 3, shaded right)</td></tr>
   <tr><td><b>C</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(CQ,15))}</td></tr>
   <tr><td><b>D</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(D,23))}</td></tr>
   <tr><td><b>E</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(Eq,31))}</td></tr>
  </tbody></table>
  <div class="note"><b>Got one wrong?</b> Check: open or closed dot? Did ℕ start at 1? Did you flip the sign when you divided by a negative? Did you round the sensible way? Then play <b>Number-Line Shade</b> at leim.ie/number-line-shade.html: the "Go back over these" list at the end shows the rule for each mistake.</div>
  <p class="small">All questions written by Léim. Léim is independent and not connected with the State Examinations Commission or the NCCA.</p>
</div>
</body></html>"""
NQ = len(A) + len(B) + len(CQ) + len(D) + len(Eq)
assert NQ == 34, NQ

# ---------- teacher pack ----------
random.seed(34); order = list(range(24)); random.shuffle(order)
cards = [("q", i) for i in range(12)] + [("a", i) for i in range(12)]
match_print = [cards[k] for k in order]
def card_html(c):
    kind, i = c
    hl = "<br><span style='font-size:7pt;color:var(--muted)'>Higher Level</span>" if "Higher" in MATCH[i][0] else ""
    return f'<div class="fc{" sm" if len(mq[i]) > 12 else ""}">{mq[i]}{hl}</div>' if kind == "q" else f'<div class="mnl">{FIG[f"m{i}"]}</div>'
match_html = "".join(f'<div class="c"><span class="tag">Card {k}</span>{card_html(c)}</div>' for k, c in enumerate(match_print, 1))
match_key = " · ".join(f"{match_print.index(('q', i)) + 1} → {match_print.index(('a', i)) + 1}" for i in range(12))

# Budget Swap: each fact on exactly ONE card
SW1 = [("Bus hire for the trip", "€150", "A"), ("Ticket for each student", "€12", "B"), ("Money in the class fund", "€500", "A"),
       ("Inequality (n students)", "", None), ("Greatest number of students", "", None)]
sw1 = floor_(500 - 150, 12); assert sw1 == 29 and 150 + 12 * 29 <= 500 < 150 + 12 * 30
SW2 = [("Money raised so far", "€85", "B"), ("Price of one cake", "€3", "A"), ("Target", "€250", "B"),
       ("Inequality (c cakes)", "", None), ("Fewest cakes to sell", "", None)]
sw2 = ceil_(250 - 85, 3); assert sw2 == 55 and 85 + 3 * 55 >= 250 > 85 + 3 * 54
for rows in (SW1, SW2): assert sum(w == "A" for *_, w in rows) >= 1 and sum(w == "B" for *_, w in rows) >= 1
def swap_card(who):
    def tab(title, rows):
        return f'<table class="ss"><thead><tr><th colspan="2">{title}</th></tr></thead><tbody>' + "".join(
            f"<tr><td>{k}</td><td><b>{v if w == who else ''}</b></td></tr>" for k, v, w in rows) + "</tbody></table>"
    return f'<div class="idc"><h3>Student {who} · Budget Swap</h3><div class="two">{tab("The class trip", SW1)}{tab("The cake sale", SW2)}</div></div>'

# Inequality Dominoes: 20 clues, 20 different answers (different as solution sets too)
DOMS = [("x + 4 > 9", sol("x + 4 > 9")), ("3x ≤ 12", sol("3x ≤ 12")), ("2x − 3 ≥ 7", sol("2x − 3 ≥ 7")), ("5x + 1 < 16", sol("5x + 1 < 16")),
        ("x/2 > 3", sol("x/2 > 3")), ("4x − 2 ≤ 2x + 8", sol("4x − 2 ≤ 2x + 8")), ("3(x − 2) > 3", sol("3(x − 2) > 3")),
        ("x is at least −2", "x ≥ −2"), ("x is less than 7", "x < 7"),
        ("x < 4, x ∈ ℕ", lst("x < 4, x ∈ ℕ")), ("2x + 1 ≤ 9, x ∈ ℕ", lst("2x + 1 ≤ 9, x ∈ ℕ")), ("−1 ≤ x < 2, x ∈ ℤ", lst("−1 ≤ x < 2, x ∈ ℤ")),
        ("2x + 3 > 10, x ∈ ℤ: smallest x", small("2x + 3 > 10, x ∈ ℤ")), ("3x − 2 ≤ 17, x ∈ ℤ: largest x", big("3x − 2 ≤ 17, x ∈ ℤ")),
        ("−3 < x ≤ 4, x ∈ ℤ: how many values?", count("−3 < x ≤ 4, x ∈ ℤ")),
        ("Taxi: €5 + €2 per km, €24: most km", str(floor_(24 - 5, 2))), ("Save €10 a week from €30, need €105: fewest weeks", str(ceil_(105 - 30, 10))),
        ("Higher Level: −2x > 8", sol("−2x > 8")), ("Higher Level: 6 − x ≥ 9", sol("6 − x ≥ 9")), ("Higher Level: 1 < 2x − 3 ≤ 7", sol("1 < 2x − 3 ≤ 7"))]
DANS = [a for k, a in DOMS]
assert len(set(DANS)) == 20, sorted(DANS)
ineqs = [parse_ineq(a)[0] for a in DANS if a.startswith("x") or re.match(r"−?\d+ [<≤] x", a)]
for i in range(len(ineqs)):
    for j in range(i + 1, len(ineqs)): assert ineqs[i].key() != ineqs[j].key()
nums = [a for a in DANS if re.fullmatch(r"\d+", a)]; assert len(nums) == len(set(nums)), nums
random.seed(3434); chain = DOMS[:]; random.shuffle(chain)
dom = [("START" if k == 0 else chain[k - 1][1], x[0]) for k, x in enumerate(chain)] + [(chain[-1][1], "FINISH")]
dom_print = dom[:]; random.shuffle(dom_print)
dom_html = "".join(f'<div class="dom"><div class="h l{" sm" if len(l) > 9 else ""}">{l}</div><div class="h r">{r}</div></div>' for l, r in dom_print)
chain_key = "".join(f"<li>{x} = <b>{a}</b></li>" for x, a in chain)

ERR = [("2x + 5 &gt; 11 → 2x &gt; 16", "x &gt; 8", f"Subtract 5, don't add: 2x &gt; 6, <b>{sol('2x + 5 > 11')}</b>"),
       ("x ≤ 3, x ∈ ℕ", "{0, 1, 2, 3}", f"ℕ starts at 1: <b>{lst('x ≤ 3, x ∈ ℕ')}</b>"),
       ("x &gt; 2 on a number line", "closed dot at 2, shaded right", "&gt; does not include 2: <b>open dot</b> at 2, shaded right"),
       ("3x − 1 ≥ 10, x ∈ ℤ: smallest x. 3x ≥ 11, x ≥ 3.67", "3", f"3 is too small (8 ≥ 10 is false). Round up: <b>{small('3x − 1 ≥ 10, x ∈ ℤ')}</b>"),
       ("Higher Level: −3x &lt; 12 → divide by −3", "x &lt; −4", f"Dividing by a negative flips the sign: <b>{sol('−3x < 12')}</b>"),
       ("Higher Level: −1 &lt; 2x + 3 ≤ 9 → −4 &lt; 2x ≤ 9", "−2 &lt; x ≤ 4.5", f"Subtract 3 from ALL three parts: −4 &lt; 2x ≤ 6, <b>{sol('−1 < 2x + 3 ≤ 9')}</b>")]
assert sol("2x + 5 > 11") == "x > 3" and small("3x − 1 ≥ 10, x ∈ ℤ") == "4" and sol("−3x < 12") == "x > −4" and sol("−1 < 2x + 3 ≤ 9") == "−2 < x ≤ 3"
assert lst("x ≤ 3, x ∈ ℕ") == "{1, 2, 3}"
# worksheet exam-style
w1 = sol("5x − 2 > 3x + 6"); w2 = lst("2(x + 1) ≤ 11, x ∈ ℕ"); w3 = floor_(40 - 4, 9); w5a = sol("3 − 4x ≥ −13"); w5b = lst("−7 < 3x + 2 ≤ 8, x ∈ ℤ")
assert w1 == "x > 4" and w2 == "{1, 2, 3, 4}" and w3 == 4 and w5a == "x ≤ 4" and w5b == "{−2, −1, 0, 1, 2}"
wm, wx, wk = graph_read("w4"); assert (wm, wx, wk) == (1, 3, 1)   # y = x − 2 meets y = 1 at x = 3, rising: y > 1 for x > 3

pack = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Inequalities Teacher Pack | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{PACK_STYLE}
{FIGCSS}
{EXTRA}
.ss td:nth-child(2){{width:30%}}.ss td,.ss th{{padding:2px 5px;font-size:8.8pt;line-height:1.3}}.fym{{grid-template-columns:repeat(3,1fr)}}.fym .c{{height:15.5mm}}.fym .fc{{font-size:12.5pt}}.fym .fc.sm{{font-size:9pt;line-height:1.15}}.idc{{padding:1.5mm 4mm}}.p1 .proc td{{font-size:8.5pt;padding:2px 6px}}
.fym .mnl{{width:100%}}.fym .mnl svg{{width:100%}}.dom .r{{font-size:9.2pt}}.dom .l{{font-size:12pt}}.dom .l.sm{{font-size:10.5pt}}
.ops div{{font-size:12pt}}.pnl{{display:grid;grid-template-columns:1fr 1fr;gap:6mm}}.pnl div{{font-size:15pt;font-weight:800;text-align:center}}
</style></head><body>

<div class="page p1">
  <div class="band"><div><div class="k">Junior Cycle Maths · Teacher pack</div><h1>Inequalities</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2018 specification): {LO}</p>
  <div class="two">
    <div><h3>Aims</h3><p>By the end of the lesson students can read and write the four inequality signs, show a solution on a number line (open and closed dots; dots for ℕ and ℤ, a shaded line for ℝ), solve linear inequalities, list or count whole-number solutions, read a solution from a graph, and form and solve an inequality from a real-life problem. Higher Level: dividing by a negative (flip the sign), double inequalities and fractions.</p></div>
    <div><h3>In this pack</h3><p>p.1 Teacher notes · p.2 Shade Match mingle cards + Budget Swap A/B cards · p.3 Inequality Dominoes (cut-up) · p.4 Wall poster · p.5 Worksheet: Error Hunt + exam-style questions · p.6 Answers. Level: 3rd year (Higher and Ordinary). Time: about 60 minutes. All questions are original.</p></div>
  </div>
  <h2 style="margin-top:8px">Procedure</h2>
  <table class="proc"><tbody>
    <tr><td>5 min</td><td><b>Lead-in: the height sign.</b> "You must be at least 120 cm for this ride." Who can go: 119 cm? 120 cm? 135.5 cm? Write h ≥ 120 and draw it on a number line together. Elicit open vs closed dot from "under 12s go free".</td></tr>
    <tr><td>8 min</td><td><b>Guided discovery.</b> Pairs start with 6 &gt; 2 and do the same thing to both sides: + 3, − 10, × 2, ÷ 2, × (−1), ÷ (−2). Which ones are still true? Elicit the flip rule (Higher Level). Ordinary Level groups: solve 2x + 1 &lt; 9 like an equation and test x = 3, 4, 5.</td></tr>
    <tr><td>10 min</td><td><b>Shade Match mingle</b> (p.2, 24 cards = 12 inequality cards + 12 number-line cards; one card each). Inequality card? Solve it, then find the number line that shows your answer. Number-line card? Find your inequality. Pairs check: dot, direction, dots or shaded line.</td></tr>
    <tr><td>12 min</td><td><b>Budget Swap</b> (p.2, pairs, don't show your card). Each fact is on only ONE card. Ask your partner for what you're missing ("How much is the bus?"), write the inequality together, then solve and round the sensible way. Feedback: class trip → <b>{sw1} students</b> (round down); cake sale → <b>{sw2} cakes</b>.</td></tr>
    <tr><td>10 min</td><td><b>Inequality Dominoes</b> (p.3), groups of 3–4. Start with START, solve the clue, find the domino with that answer on its left, and build the chain to FINISH.</td></tr>
    <tr><td>12 min</td><td><b>Worksheet</b> (p.5). Error Hunt in pairs (find the mistake, name it, fix it), then the exam-style questions alone. Question 5 is Higher Level.</td></tr>
    <tr><td>3 min</td><td><b>Exit ticket.</b> Solve 3x − 4 &lt; 11 and list the values if x ∈ ℕ. ({sol("3x − 4 < 11")}: {lst("3x − 4 < 11, x ∈ ℕ")}.) Homework: play <b>Number-Line Shade</b> at leim.ie/number-line-shade.html.</td></tr>
  </tbody></table>
  <div class="note"><b>Mingle key</b> (inequality card → number-line card): {match_key}.<br>
  <b>Errors to look for:</b> open and closed dots swapped · 0 in an ℕ answer · a shaded line for x ∈ ℤ · not flipping when dividing by a negative · only subtracting from two parts of a double inequality · rounding up for a limit or down for a target. <b>Support:</b> "Is the end number allowed? Yes → closed dot." <b>Fast finishers:</b> write an inequality whose ℕ answer is {{1, 2, 3, 4, 5}} in three different ways.</div>
  <p class="small"><b>Domino answer chain</b> (START → FINISH):</p>
  <ol class="small" style="columns:2;column-gap:12px;font-size:7.2pt;line-height:1.22;margin:0;padding-left:16px">{chain_key}</ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">Cut up the cards · one Budget Swap card per student</div><h1>Shade Match mingle + Budget Swap</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:8.8pt;margin:0"><b>Shade Match mingle.</b> Cut out the 24 cards and give one to each student. Inequality card? Solve it, then find the number line that shows your answer. Number-line card? Find your inequality. (Fewer students? Take out whole pairs.)</p>
  <div class="fym">{match_html}</div>
  <p style="font-size:8.8pt;margin:3mm 0 0"><b>Budget Swap.</b> Don't show your card. Each fact is on only one of the two cards: ask your partner for what you're missing, write the inequality together, then fill in every blank.</p>
  {swap_card("A")}
  {swap_card("B")}
</div>

<div class="page">
  <div class="band"><div><div class="k">Groups of 3–4 · cut along the dashed lines</div><h1>Inequality Dominoes</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.4pt">Start with START. Solve the clue on the right, then find the domino with that answer on its left. Keep going until you reach FINISH. The last three clues are Higher Level (Ordinary Level groups can be given those answers).</p>
  <div class="doms">{dom_html}</div>
</div>

<div class="page">
  <div class="poster">
    <h1>Inequalities</h1>
    <div class="sg" style="gap:4mm"><div><b style="font-size:40pt">&lt;</b>less than</div><div><b style="font-size:40pt">&gt;</b>greater than</div><div><b style="font-size:40pt">≤</b>less than or equal</div><div><b style="font-size:40pt">≥</b>greater than or equal</div></div>
    <div class="pnl"><div>x &gt; 2 · open dot{FIG["pA"]}</div><div>x ≤ 2 · closed dot{FIG["pB"]}</div></div>
    <div class="ops">
      <div style="background:var(--green-soft)"><b>Solve</b>like an equation:<br>same to both sides</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>ℕ · ℤ · ℝ</b>ℕ and ℤ: dots<br>ℝ: a shaded line<br>ℕ starts at 1</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Higher Level</b>× or ÷ by a negative:<br><span style="font-weight:800">FLIP the sign</span><br>−2x &gt; 6 → x &lt; −3</div>
      <div style="background:var(--green-soft)"><b>Real life</b>a limit → round down<br>a target → round up</div>
    </div>
    <p style="text-align:center;font-size:13pt;margin:0"><b>Words:</b> at least ≥ · at most ≤ · more than &gt; · under &lt;</p>
    <p style="text-align:center;font-size:10pt;color:var(--muted)">Léim · leim.ie · Play Number-Line Shade: leim.ie/number-line-shade.html</p>
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
  <div class="gfig" style="width:36mm">{FIG["w4"]}</div>
  <ol class="q">
    <li>Solve 5x − 2 &gt; 3x + 6, x ∈ ℝ, and show your answer on a number line.<span class="long"></span></li>
    <li>List the values of x for which 2(x + 1) ≤ 11, x ∈ ℕ.<span class="long"></span></li>
    <li>Liam has €40. Cinema tickets cost €9 each and he must also buy one €4 popcorn. (a) Write an inequality in t, the number of tickets. (b) What is the greatest number of tickets he can buy?<span class="long"></span></li>
    <li>The graph shows y = x − 2 and the dashed line y = 1. For which values of x is y &gt; 1? Check with algebra.<span class="long"></span></li>
    <li style="clear:both">Higher Level: (a) solve 3 − 4x ≥ −13. (b) List the values of x for which −7 &lt; 3x + 2 ≤ 8, x ∈ ℤ.<span class="long"></span></li>
  </ol>
</div>

<div class="page an">
  <div class="band"><div><div class="k">For the teacher</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>Budget Swap</h2>
  <div class="two"><table><tbody>
   <tr><td>Inequality</td><td><b>150 + 12n ≤ 500</b></td></tr><tr><td>Working</td><td>12n ≤ 350 → n ≤ 29.17</td></tr>
   <tr><td>Greatest number of students</td><td><b>{sw1}</b> (round down: 30 would cost €510)</td></tr></tbody></table>
  <table><tbody>
   <tr><td>Inequality</td><td><b>85 + 3c ≥ 250</b></td></tr><tr><td>Working</td><td>3c ≥ 165 → c ≥ 55</td></tr>
   <tr><td>Fewest cakes</td><td><b>{sw2}</b> (85 + 165 = 250 ✓)</td></tr></tbody></table></div>
  <h2>A. Error Hunt</h2>
  <table><tbody>{"".join(f"<tr><td style='width:42%'><b>{q}</b></td><td>{r}</td></tr>" for q,w,r in ERR)}</tbody></table>
  <h2>B. Exam-style questions</h2>
  <ol class="q">
    <li>2x &gt; 8 → <b>{w1}</b>: open dot at 4, shaded to the right with an arrow</li>
    <li>2x + 2 ≤ 11 → x ≤ 4.5 → <b>{w2}</b></li>
    <li>(a) <b>9t + 4 ≤ 40</b> (b) 9t ≤ 36 → t ≤ 4: <b>{w3} tickets</b></li>
    <li>The line meets y = 1 at x = 3 and is above it to the right: <b>x &gt; 3</b>. Check: x − 2 &gt; 1 → x &gt; 3 ✓</li>
    <li>(a) −4x ≥ −16 → divide by −4, flip: <b>{w5a}</b> (b) −9 &lt; 3x ≤ 6 → −3 &lt; x ≤ 2: <b>{w5b}</b></li>
  </ol>
  <h2>Marking tip</h2>
  <p>Give credit for each step, as the exam does: a correct first step, the solved inequality, and the number line or list. On a number line look for three things: the right dot, the right direction, and dots (ℕ, ℤ) or a shaded line (ℝ). In word problems insist on a sentence answer that has been rounded the sensible way.</p>
</div>
</body></html>"""

cover = """<!doctype html><html><head><meta charset="utf-8"><style>
body{margin:0;width:1200px;height:1200px;background:#1B2430;font-family:Inter,sans-serif;color:#fff;display:flex;flex-direction:column;justify-content:space-between;padding:90px;box-sizing:border-box}
.k{display:inline-block;background:#2E7D57;border-radius:99px;padding:12px 26px;font-weight:700;font-size:28px;letter-spacing:.06em;text-transform:uppercase}
h1{font-size:110px;font-weight:800;line-height:1.14;letter-spacing:-.03em;margin:40px 0 0}
h1 span{background:#F6CF5A;color:#1B2430;padding:0 14px;box-decoration-break:clone;-webkit-box-decoration-break:clone}
.sub{font-size:38px;color:#C9D1DA;margin-top:36px;line-height:1.35}
.em{font-size:50px;margin-top:30px;font-weight:800;letter-spacing:.01em;color:#F6CF5A}
.foot{display:flex;justify-content:space-between;align-items:center;font-size:34px;font-weight:700}
.price{background:#F6CF5A;color:#1B2430;border-radius:16px;padding:14px 28px}
</style></head><body>
<div><span class="k">Junior Cycle Maths · Teacher pack</span>
<h1><span>Inequalities</span></h1>
<div class="sub">Shade Match mingle · Budget Swap A/B<br>Dominoes · Poster · Worksheet + answers</div>
<div class="em">2x + 1 &lt; 9 → x &lt; 4</div></div>
<div class="foot"><span>↗ Léim · leim.ie</span><span class="price">Ready to teach · 60 min</span></div>
</body></html>"""
assert sol("2x + 1 < 9") == "x < 4"

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
    pdf("teacher-pack", os.path.join(OUT, "Inequalities-Teacher-Pack-Leim.pdf"))
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--hide-scrollbars", "--window-size=1200,1200",
                    f"--screenshot={os.path.join(OUT, f'{SLUG}-cover.png')}", f"{SLUG}-cover.html"], cwd=SRC, check=True, capture_output=True)
    print("domino chain:", [(x, a) for x, a in chain])
