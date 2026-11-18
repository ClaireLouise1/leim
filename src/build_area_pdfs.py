#!/usr/bin/env python3
"""Area, perimeter & scale drawings (JC Maths topic 21): free sheet + teacher pack + Payhip cover.
Run from the repo root: python3 src/build_area_pdfs.py OUTDIR
Writes src/area-perimeter-scale-drawings-*.html; PDFs/cover PNG go to OUTDIR (free sheet also to printables/).
Diagrams come from the Floor Planner game's figure kit through src/floor_figs_bridge.js, and every diagram's
labels are re-checked by test_floor_planner's drawing reader. Every answer is computed (Fraction / math.pi) and asserted.
Styles are read from src/build_money1_pdfs.py."""
import os, sys, random, subprocess, re, json, math
from fractions import Fraction as F
from math import floor, ceil
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC)
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/area"; os.makedirs(OUT, exist_ok=True)
SLUG = "area-perimeter-scale-drawings"
LO = "GT.2a, GT.2c"
PI = F(math.pi)

def dec(x, dp=None):
    x = F(x)
    if dp is not None: x = F(floor(x * 10 ** dp + F(1, 2)), 10 ** dp)
    k = 0
    while (x * 10 ** k).denominator != 1:
        k += 1; assert k < 8, x
    n = x * 10 ** k; s = str(abs(n.numerator)).rjust(k + 1, "0")
    s = s[:len(s) - k] + ("." + s[len(s) - k:] if k else "")
    i, _, f = s.partition(".")
    return "{:,}".format(int(i)) + ("." + f if f else "")
def dpf(x, dp):   # fixed decimal places (for "to 2 decimal places" answers)
    x = F(floor(F(x) * 10 ** dp + F(1, 2)), 10 ** dp); s = dec(x)
    if dp and "." not in s: s += "." + "0" * dp
    elif dp: s += "0" * (dp - len(s.split(".")[1]))
    return s
def cent(x): x = F(x); return F(floor(x * 100 + F(1, 2)), 100)
def e(x):
    x = F(x); assert (x * 100).denominator == 1, x; c = int(x * 100); return "€{:,}.{:02d}".format(c // 100, c % 100)
def m(x, u="m", dp=None): return dec(x, dp) + " " + u
def m2(x, u="m", dp=None): return dec(x, dp) + " " + u + "²"
def pi_(c, u): return ("" if c == 1 else dec(c)) + "π " + u
def L_area(W, H, cw, ch): return F(W) * F(H) - F(cw) * F(ch)
assert dec(F("1147.5")) == "1,147.5" and dpf(F("3.0097"), 2) == "3.01" and dpf(6.8, 2) == "6.80" and pi_(F(81), "cm²") == "81π cm²"

# ---------- diagrams from the game's kit, each re-checked ----------
FIGS = {
    "ruleL": 'draw(Lfig({W:10,H:7,cw:4,ch:3,f:0},"m",[0,5,1,4]),[150,100])',
    "ruleSemi": 'draw(semiFig(3,"d","m"),[130,65])',
    "pL": 'draw(Lfig({W:9,H:7,cw:4,ch:3,f:1},"m",[0,5,1,4]),[150,110])',
    "pTri": 'draw(triFig(14,6,8,"cm"),[150,90])',
    "pPara": 'draw(paraFig(11,5,12,"cm"),[150,110])',
    "wL": 'draw(Lfig({W:8,H:6,cw:3,ch:2.5,f:0},"m",[0,5,2,3]),[150,110])',
    "posterTri": 'draw(triFig(8,3,4,"cm"),[150,80])',
    "posterCirc": 'draw(circleFig(3,"r","cm"),[90,90])',
}
FIG = json.loads(subprocess.run(["node", os.path.join(SRC, "floor_figs_bridge.js")], input=json.dumps(FIGS), capture_output=True, text=True, check=True).stdout)
sys.path.insert(0, SRC)
_argv = sys.argv; sys.argv = ["x", "/dev/null"]
_chk = open(os.path.join(SRC, "test_floor_planner.py"), encoding="utf-8").read().split("# ---------- main")[0]
_ns = {}; exec(_chk, _ns); sys.argv = _argv
for k, svg in FIG.items():
    fig = _ns["read_fig"]({"html": svg})
    for bad_ in ("drawn_wrong", "badlabel", "label_mismatch", "label_not_edge", "bad_height", "r_mismatch"):
        assert not fig.get(bad_), (k, bad_)
    FIG[k] = re.sub(r' style="max-width:\d+px"', "", svg)
def shoelace(k): return _ns["shoelace"](_ns["read_fig"]({"html": FIG[k]})["P"])
assert shoelace("ruleL") == 58 and shoelace("pL") == 51 and shoelace("pTri") == 56 and shoelace("pPara") == 132 and shoelace("wL") == F("40.5")

# ---------- free sheet ----------
A = [("A rectangular floor is 7 m by 4.5 m. Find its area.", m2(F(7) * F("4.5"))),
     ("Find the perimeter of the floor in question 1.", m(2 * (7 + F("4.5")))),
     ("A square tile has sides of 6.5 cm. Find its area.", m2(F("6.5") ** 2, "cm")),
     ("A rectangle has an area of 48 m² and a length of 8 m. Find its width.", m(F(48, 8))),
     ("The L-shaped room on the right: find the lengths of the two sides that are not labelled.", "4 m and 3 m"),
     ("Find the perimeter of the L-shaped room.", m(2 * (9 + 7))),
     ("Find the area of the L-shaped room.", m2(L_area(9, 7, 4, 3))),
     ("Flooring costs €22.50 per m². Find the cost of flooring the L-shaped room.", e(L_area(9, 7, 4, 3) * F("22.5")))]
assert [a for q, a in A] == ["31.5 m²", "23 m", "42.25 cm²", "6 m", "4 m and 3 m", "32 m", "51 m²", "€1,147.50"], [a for q, a in A]
B = [("Find the area of the triangle on the right.", m2(F(14 * 8, 2), "cm")),
     ("Find the area of the parallelogram on the right.", m2(11 * 12, "cm")),
     ("Find the perimeter of the parallelogram.", m(2 * (11 + 13), "cm")),
     ("A right-angled triangle has sides 6 cm, 8 cm and 10 cm. The right angle is between the 6 cm and 8 cm sides. Find its area.", m2(F(6 * 8, 2), "cm")),
     ("A triangle has an area of 45 cm² and a base of 10 cm. Find its perpendicular height.", m(F(2 * 45, 10), "cm")),
     ("The end wall of a shed is 6 m wide. The walls are 4 m high and the top of the roof is 6.5 m high. Find the area of the end wall.", m2(6 * 4 + F(1, 2) * 6 * F("2.5"))),
     ("A parallelogram has an area of 72 cm² and a base of 9 cm. Find its perpendicular height.", m(F(72, 9), "cm"))]
assert [a for q, a in B] == ["56 cm²", "132 cm²", "48 cm", "24 cm²", "9 cm", "31.5 m²", "8 cm"], [a for q, a in B]
Cq = [("A circle has a radius of 5 cm. Find its circumference (π button, 1 decimal place).", m(2 * 5 * PI, "cm", 1)),
      ("Find the area of the circle in question 16 (π button, 1 decimal place).", m2(25 * PI, "cm", 1)),
      ("A circle has a diameter of 14 cm. Using π = 22/7, find its circumference.", m(F(22, 7) * 14, "cm")),
      ("Using π = 22/7, find the area of the circle in question 18.", m2(F(22, 7) * 49, "cm")),
      ("A circle has a radius of 9 cm. Find its area in terms of π.", pi_(81, "cm²")),
      ("A circle has a circumference of 20π cm. Find its radius.", m(10, "cm")),
      ("A semicircle has a diameter of 10 m. Find its perimeter (π button, 1 decimal place).", m(5 * PI + 10, "m", 1)),
      ("A wheel with a diameter of 70 cm turns 200 times. Using π = 22/7, how far does it travel, in metres?", m(F(22, 7) * 70 * 200 / 100))]
assert [a for q, a in Cq] == ["31.4 cm", "78.5 cm²", "44 cm", "154 cm²", "81π cm²", "10 cm", "25.7 m", "440 m"], [a for q, a in Cq]
D = [("A plan has a scale of 1 : 50. A wall is 8.4 cm long on the plan. How long is the real wall, in metres?", m(F("8.4") * 50 / 100)),
     ("A plan has a scale of 1 : 100. A real wall is 6.5 m long. How long is it on the plan?", m(F("6.5") * 100 / 100, "cm")),
     ("A wall 7.5 m long is drawn 3 cm long on a plan. What is the scale?", "1 : " + dec(F(750, 3))),
     ("On a plan with scale 1 : 50, a room is 8 cm by 6 cm. Find the real area of the room in m².", m2(F(8 * 50, 100) * F(6 * 50, 100))),
     ("A map has a scale of 1 : 25,000. Two farms are 8 cm apart on the map. How far apart are they, in km?", m(F(8 * 25000, 100000), "km")),
     ("A map has a scale of 1 : 50,000. A walk is 6 km long. How long is it on the map?", m(F(6 * 100000, 50000), "cm")),
     ("On a plan, 1 cm represents 2.5 m. A hall is 4.8 cm long on the plan. How long is the real hall?", m(F("4.8") * F("2.5")))]
assert [a for q, a in D] == ["4.2 m", "6.5 cm", "1 : 250", "12 m²", "2 km", "12 cm", "12 m"], [a for q, a in D]
# exam-style
e1 = 96 - PI * F(9, 4); e1b = ceil(e1 / 20); e1c = 2 * (12 + 8) - F("1.2")
assert (dec(e1, 1), e1b, e1c) == ("88.9", 5, F("38.8"))
e2p = 170 + 64 * PI; e2a = 85 * 64 + PI * 32 ** 2; e2l = ceil(5000 / e2p)
assert (dec(e2p, 0), dec(e2a, 0), e2l) == ("371", "8,657", 14)
e3 = (F(9 * 20, 100), F("4.5") * 20 / 100); assert e3 == (F("1.8"), F("0.9")) and e3[0] * e3[1] == F("1.62") and F(120, 20) == 6
E = [("<b>The back garden.</b> A rectangular lawn is 12 m by 8 m. A round pond with a radius of 1.5 m is dug in the middle of it. (a) Find the area of grass left, to 1 decimal place. (b) A box of lawn feed covers 20 m². How many boxes are needed for the grass? (c) A fence goes around the edge of the lawn except for a gate 1.2 m wide. How long is the fence?",
      f"(a) 96 − π × 1.5² = <b>{m2(e1, dp=1)}</b> (b) 88.93 ÷ 20 = 4.45 → <b>{e1b} boxes</b> (c) 40 − 1.2 = <b>{m(e1c)}</b>"),
     ("<b>The running track.</b> A track has two straights 85 m long and a semicircle at each end. The semicircles have a diameter of 64 m. (a) Find the length of one lap of the inside edge, to the nearest metre. (b) Find the area inside the track, to the nearest m². (c) How many complete laps must a runner do to run at least 5 km?",
      f"(a) 170 + 64π = <b>{m(e2p, dp=0)}</b> (b) 85 × 64 + π × 32² = <b>{m2(e2a, dp=0)}</b> (c) 5,000 ÷ 371.06 = 13.47 → <b>{e2l} laps</b>"),
     ("<b>The kitchen plan.</b> Ella draws her kitchen to a scale of 1 : 20. The table is 9 cm by 4.5 cm on the plan. (a) Find the real length and width of the table. (b) Find the real area of the table top. (c) A round table with a diameter of 1.2 m is drawn on the same plan. What is its diameter on the plan? (d) Find the area of the round table top in terms of π.",
      f"(a) <b>1.8 m</b> by <b>0.9 m</b> (b) <b>1.62 m²</b> (c) 120 ÷ 20 = <b>6 cm</b> (d) π × 0.6² = <b>{pi_(F('0.36'), 'm²')}</b>"),
     ("<b>Same base, same area.</b> A triangle and a parallelogram both have a base of 10 cm and an area of 40 cm². (a) Find the perpendicular height of each. (b) Ciara draws a triangle with a base of 10 cm and a sloping side of 8 cm. She says its area is ½ × 10 × 8 = 40 cm². Explain her mistake.",
      "(a) triangle <b>8 cm</b>, parallelogram <b>4 cm</b> (b) 8 cm is the sloping side, not the perpendicular height. The height is shorter than 8 cm, so the area is less than 40 cm²")]

def qs(items): return "".join(f"<li>{q} <span class='line'></span></li>" for q, a in items)
def style(var):
    return re.search(var + r' = f"""<!doctype.*?<style>(.*?)</style>', open(os.path.join(SRC, "build_money1_pdfs.py"), encoding="utf-8").read(), re.S).group(1).replace("{LO}", LO).replace("{{", "{").replace("}}", "}")
SHEET_STYLE = style("sheet"); PACK_STYLE = style("pack")
assert "@bottom-left" in SHEET_STYLE and "Single-teacher licence" in PACK_STYLE and "{{" not in SHEET_STYLE + PACK_STYLE
FIGCSS = """svg.fig{display:block;width:100%;height:auto}svg.fig .sh{fill:#E8F3EC;stroke:#2E7D57;stroke-width:2.2;stroke-linejoin:round}
svg.fig .fd{stroke:#C0392B;stroke-width:1.6;stroke-dasharray:5 4}svg.fig .fr{stroke:#2E7D57;stroke-width:1.3;stroke-dasharray:4 3}
svg.fig .rt{fill:none;stroke:#C0392B;stroke-width:1.4}svg.fig .dt{fill:#1B2430}svg.fig .fl{font:700 14px Inter,sans-serif;fill:#1B2430}
.gfig{float:right;width:46mm;margin:0 0 1mm 3mm}.fm4{display:grid;grid-template-columns:1fr 1fr;gap:1.5mm}.fm4 div{border:1.5px solid var(--line);border-radius:8px;padding:2px 6px;font-size:9pt}.fm4 b{display:block}"""

sheet = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Area, perimeter and scale drawings: rules and practice | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{SHEET_STYLE}
{FIGCSS}
</style></head><body>
<div class="page tight">
  <div class="band"><div><div class="k">Junior Cycle Maths · Free revision sheet</div><h1>Area, perimeter &amp; scale drawings</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2018 specification): {LO}. Play the game: <b>leim.ie/floor-planner.html</b></p>
  <div class="two">
   <div><h2>1. Perimeter or area?</h2>
    <p><b>Perimeter</b> = the distance around the edge, in m or cm (fencing, skirting, a frame). <b>Area</b> = the space inside, in m² or cm² (flooring, paint, tiles).</p>
    <div class="fm4"><div><b>Rectangle</b>A = l × w · P = 2(l + w)</div><div><b>Triangle</b>A = ½ × base × ⊥ height</div><div><b>Parallelogram</b>A = base × ⊥ height</div><div><b>Circle</b>C = 2πr = πd · A = πr²</div></div>
    <p style="margin-top:3px">⊥ height = the <b>perpendicular</b> height (at right angles to the base), never the sloping side. The formulas are in the <i>Formulae and Tables</i> booklet.</p>
    <h2>2. L-shapes</h2>
    <div class="gfig" style="width:40mm">{FIG["ruleL"]}</div>
    <p><b>Missing sides first:</b> 10 − 6 = 4 m, 7 − 4 = 3 m. <b>Area</b> = big rectangle − corner: 70 − 12 = <b>58 m²</b>. <b>Perimeter</b> = all six sides = <b>34 m</b>.</p>
    <p style="clear:both">End wall with a pointed roof = rectangle + triangle. Window with a round top = rectangle + semicircle.</p>
    <h2>3. Circles and π</h2>
    <p>d = 2r. Area uses the <b>radius</b>. Follow the instruction: <b>π button</b>, <b>π = 3.14</b>, <b>π = 22/7</b>, or <b>in terms of π</b> (r = 6: area 36π, circumference 12π). Back again: C = 18π → r = 9; A = 49π → r = 7.</p></div>
   <div>
    <div class="gfig" style="width:34mm">{FIG["ruleSemi"]}</div>
    <p><b>Semicircle</b>, d = 6 m: area ½ × π × 3² = <b>14.1 m²</b>; perimeter ½ × π × 6 + 6 = <b>15.4 m</b> (add the straight edge!). A quarter circle has two straight edges.</p>
    <p style="clear:both"><b>Wheels:</b> one turn = one circumference (π × d).</p>
    <h2>4. Real-life floors</h2>
    <table><tbody><tr><td>Cost</td><td>area × price per m²</td></tr>
     <tr><td>Packs, tins, boxes</td><td>area ÷ what one covers, then <b>round UP</b></td></tr>
     <tr><td>Tiles</td><td>same units first: 3 m × 2 m, 50 cm tiles: 6 × 4 = 24</td></tr>
     <tr><td>Skirting board</td><td>perimeter − the doorway</td></tr></tbody></table>
    <h2>5. Scale drawings</h2>
    <p><b>1 : 50</b> = 1 cm on the plan is 50 cm in real life. Plan → real <b>× 50</b>; real → plan <b>÷ 50</b>; then ÷ 100 for m (÷ 100,000 for km). <b>The scale:</b> 6 m drawn 3 cm: 600 ÷ 3 → <b>1 : 200</b>. <b>Real area:</b> change each length first, then multiply (9 cm × 7.2 cm at 1 : 50 = 4.5 m × 3.6 m = 16.2 m²), never plan area × 50.</p>
    <div class="note"><b>Classic mistakes:</b> the sloping side as the height · forgetting ½ · the diameter in πr² · no straight edge on a semicircle · m instead of m² · rounding packs down · mixing cm and m.</div></div>
  </div>
  <div class="tip"><b>Exam tip:</b> mark the missing lengths on the diagram, write the formula, put the numbers in, then give the answer WITH units. Round only at the end, the way the question asks.</div>
</div>

<div class="page p2">
  <div class="band"><div><div class="k">Practice · 34 questions</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Rectangles and L-shapes</h2>
  <div class="gfig">{FIG["pL"]}</div>
  <ol class="q">{qs(A)}</ol>
  <h2 style="clear:both">B. Triangles and parallelograms</h2>
  <div class="gfig" style="width:40mm">{FIG["pTri"]}<div style="height:2mm"></div>{FIG["pPara"]}</div>
  <ol class="q" start="9">{qs(B)}</ol>
  <h2 style="clear:both">C. Circles</h2><ol class="q" start="16">{qs(Cq)}</ol>
  <h2>D. Scale drawings and maps</h2><ol class="q" start="24">{qs(D)}</ol>
  <p class="small" style="margin-top:4px">Questions 31–34 are on the next page.</p>
</div>

<div class="page">
  <div class="band"><div><div class="k">Exam-style · then check</div><h1>Exam corner + answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>E. Exam-style questions (show your work)</h2>
  <ol class="q e3" start="31">{"".join(f"<li>{q}<span class='long'></span><span class='long'></span></li>" for q,a in E)}</ol>
  <h2 style="margin-top:10px">Answers</h2>
  <table class="ans"><tbody>
   <tr><td><b>A</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(A,1))}</td></tr>
   <tr><td><b>B</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(B,9))}</td></tr>
   <tr><td><b>C</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(Cq,16))}</td></tr>
   <tr><td><b>D</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(D,24))}</td></tr>
   <tr><td><b>E</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(E,31))}</td></tr>
  </tbody></table>
  <div class="note"><b>Got one wrong?</b> Check: did you use the perpendicular height, and the radius (not the diameter) in πr²? Did you add the straight edge of a semicircle? Did you change every length to real life before working out an area from a plan? Then play <b>Floor Planner</b> at leim.ie/floor-planner.html: the "Go back over these" list at the end shows the rule for each mistake.</div>
  <p class="small">All questions written by Léim. Léim is independent and not connected with the State Examinations Commission or the NCCA.</p>
</div>
</body></html>"""

# ---------- teacher pack ----------
# Plan Swap: each fact is on exactly ONE card; both students work out every blank
ps_l, ps_w = F(11 * 50, 100), F(8 * 50, 100); ps_a = ps_l * ps_w; ps_p = ceil(ps_a / F("2.5")); ps_c = ps_p * 55
assert (ps_l, ps_w, ps_a, ps_p, ps_c) == (F("5.5"), 4, 22, 9, 495)
pt_a = PI * F("6.25"); pt_pc = cent(pt_a * 40); pt_c = 5 * PI; pt_ec = cent(pt_c * F("6.5"))
assert (dec(pt_a, 1), pt_pc, dec(pt_c, 1), pt_ec) == ("19.6", F("785.40"), "15.7", F("102.10"))
TR = [("Scale of the plan", "1 : 50", "A"), ("Length on the plan", "11 cm", "B"), ("Width on the plan", "8 cm", "A"),
      ("One pack covers", "2.5 m²", "A"), ("Price of one pack", "€55.00", "B"),
      ("Real length and width", "", None), ("Floor area", "", None), ("Packs needed", "", None), ("Cost", "", None)]
MR = [("Diameter of the patio", "5 m", "A"), ("Paving price per m²", "€40.00", "B"), ("Edging price per metre", "€6.50", "B"),
      ("Radius", "", None), ("Area (1 d.p.)", "", None), ("Paving cost (full area, to the cent)", "", None), ("Circumference (1 d.p.)", "", None), ("Edging cost (full length, to the cent)", "", None)]
for rows in (TR, MR):
    assert all(w in ("A", "B") for _, v, w in rows if v) and any(w == "A" for *_, w in rows) and any(w == "B" for *_, w in rows)
def swap_card(who):
    def tab(title, rows):
        return f'<table class="ss"><thead><tr><th colspan="2">{title}</th></tr></thead><tbody>' + "".join(
            f"<tr><td>{k}</td><td><b>{v if w == who else ''}</b></td></tr>" for k, v, w in rows) + "</tbody></table>"
    return f'<div class="idc"><h3>Student {who} · Plan Swap</h3><div class="two">{tab("The Byrnes’ new floor", TR)}{tab("The round patio (π button)", MR)}</div></div>'

MATCH = [("Rectangle 9 m × 6 m: area?", m2(54)), ("Rectangle 9 m × 6 m: perimeter?", m(30)),
         ("Triangle: base 10 cm, ⊥ height 7 cm: area?", m2(F(70, 2), "cm")), ("Parallelogram: base 12 cm, ⊥ height 5 cm: area?", m2(60, "cm")),
         ("Circle, r = 10 cm, π = 3.14: area?", m2(F("3.14") * 100, "cm")), ("Circle, d = 14 cm, π = 22/7: circumference?", m(F(22, 7) * 14, "cm")),
         ("Circle, r = 4 cm: area in terms of π?", pi_(16, "cm²")), ("Semicircle, d = 8 m: area in terms of π?", pi_(8, "m²")),
         ("Plan 1 : 50. 6 cm on the plan: real length?", m(3)), ("Plan 1 : 200. Real wall 18 m: on the plan?", m(9, "cm")),
         ("Floor 12 m² at €25 per m²: cost?", e(300)), ("Floor 10 m², one pack covers 3 m²: packs?", f"{ceil(F(10, 3))} packs")]
ANS = [a for q, a in MATCH]
assert ANS == ["54 m²", "30 m", "35 cm²", "60 cm²", "314 cm²", "44 cm", "16π cm²", "8π m²", "3 m", "9 cm", "€300.00", "4 packs"], ANS
assert len(set(ANS)) == 12
cards = [q for q, a in MATCH] + ANS
random.seed(21); match_print = cards[:]; random.shuffle(match_print)
match_html = "".join(f'<div class="c"><span class="tag">Card {i}</span><div class="fc{" sm" if len(x) > 10 else ""}">{x}</div></div>' for i, x in enumerate(match_print, 1))
match_key = " · ".join(f"{match_print.index(q) + 1} → {match_print.index(a) + 1}" for q, a in MATCH)

DOMS = [("Rectangle 8 m × 2.5 m: area", m2(20)), ("Square, side 7 cm: perimeter", m(28, "cm")), ("Triangle, base 9 cm, ⊥ height 6 cm: area", m2(27, "cm")),
        ("Parallelogram, base 7 cm, ⊥ height 5 cm: area", m2(35, "cm")), ("Circle r = 3 cm: area in terms of π", pi_(9, "cm²")),
        ("Circle d = 20 cm: circumference in terms of π", pi_(20, "cm")), ("Circle r = 7 cm, π = 22/7: area", m2(F(22, 7) * 49, "cm")),
        ("Circle r = 5 m, π = 3.14: circumference", m(F("3.14") * 10)), ("Circumference 12π cm: radius", m(6, "cm")), ("Area 64π cm²: radius", m(8, "cm")),
        ("Semicircle d = 6 m: area in terms of π", pi_(F("4.5"), "m²")), ("Quarter circle r = 4 m: area in terms of π", pi_(4, "m²")),
        ("Plan 1 : 50, 9 cm: real length", m(F("4.5"))), ("Plan 1 : 100, real 7 m: on the plan", m(7, "cm")), ("6 m wall drawn 3 cm: the scale", "1 : 200"),
        ("Map 1 : 25,000, 4 cm: real distance", m(1, "km")), ("15 m² floor, packs cover 2 m²", f"{ceil(F(15, 2))} packs"),
        ("3 m × 2 m floor, 50 cm square tiles", f"{6 * 4} tiles"), ("Perimeter 20 m, doorway 1 m: skirting", m(19)),
        ("Triangle area 30 cm², base 12 cm: ⊥ height", m(5, "cm"))]
DANS = [a for k, a in DOMS]
assert DANS == ["20 m²", "28 cm", "27 cm²", "35 cm²", "9π cm²", "20π cm", "154 cm²", "31.4 m", "6 cm", "8 cm", "4.5π m²", "4π m²", "4.5 m", "7 cm",
                "1 : 200", "1 km", "8 packs", "24 tiles", "19 m", "5 cm"], DANS
assert len(set(DANS)) == 20
random.seed(2121); chain = DOMS[:]; random.shuffle(chain)
dom = [("START" if k == 0 else chain[k - 1][1], x[0]) for k, x in enumerate(chain)] + [(chain[-1][1], "FINISH")]
dom_print = dom[:]; random.shuffle(dom_print)
dom_html = "".join(f'<div class="dom"><div class="h l{" sm" if len(l) > 9 else ""}">{l}</div><div class="h r">{r}</div></div>' for l, r in dom_print)
chain_key = "".join(f"<li>{x} = <b>{a}</b></li>" for x, a in chain)

ERR = [("Triangle: base 10 cm, sloping side 6 cm, ⊥ height 5 cm. Area?", "½ × 10 × 6 = 30 cm²", f"Use the perpendicular height: ½ × 10 × 5 = <b>{m2(25, 'cm')}</b>"),
       ("Circle with diameter 10 cm. Area (π button, 1 d.p.)?", "π × 10² = 314.2 cm²", f"Use the radius, 5: π × 5² = <b>{m2(25 * PI, 'cm', 1)}</b>"),
       ("Semicircle with diameter 6 m. Perimeter (π = 3.14)?", "½ × 3.14 × 6 = 9.42 m", f"Add the straight edge: 9.42 + 6 = <b>{m(F('9.42') + 6)}</b>"),
       ("Rectangle 6 m by 4 m. Area?", "6 + 4 + 6 + 4 = 20 m²", f"That's the perimeter (20 m). Area = 6 × 4 = <b>{m2(24)}</b>"),
       ("Floor 17 m². One pack covers 2 m². Packs?", "17 ÷ 2 = 8.5, so 8 packs", f"8 packs leave a gap: round UP to <b>{ceil(F(17, 2))} packs</b>"),
       ("Plan 1 : 50: room 8 cm by 6 cm. Real area?", "8 × 6 × 50 = 2,400 cm² = 0.24 m²", f"Lengths first: 4 m × 3 m = <b>{m2(12)}</b>")]
assert F("3.14") * 3 == F("9.42")
w1 = L_area(8, 6, 3, F("2.5")); assert (w1, w1 * 18) == (F("40.5"), 729)
w2c = F("1.2") * PI; assert dpf(w2c, 2) == "3.77"
w3 = floor(F(100000) / (64 * PI)); assert w3 == 497
w4 = (240 // 15) * (150 // 15); w4b = ceil(F(w4, 12)); assert (w4, w4b) == (160, 14)
w5 = (F(F("3.6") * 50000, 100000), F(F("4.5") * 100000, 50000)); assert w5 == (F("1.8"), 9)

pack = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Area, Perimeter and Scale Drawings Teacher Pack | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{PACK_STYLE}
{FIGCSS}
.ss td:nth-child(2){{width:30%}}.ss td,.ss th{{padding:1px 5px;font-size:8.6pt;line-height:1.2}}.fym .c{{height:15mm}}.fym .fc.sm{{font-size:8.6pt}}.p1 .proc td{{font-size:8.5pt;padding:2px 6px}}
.pf2{{display:grid;grid-template-columns:1fr 1fr;gap:6mm;align-items:center}}.pf2 svg{{max-height:42mm}}.dom .r{{font-size:9.6pt}}
</style></head><body>

<div class="page p1">
  <div class="band"><div><div class="k">Junior Cycle Maths · Teacher pack</div><h1>Area, perimeter &amp; scale drawings</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2018 specification): {LO} (volume, surface area and nets come later, in topic 33)</p>
  <div class="two">
    <div><h3>Aims</h3><p>By the end of the lesson students can tell perimeter from area, find the area and perimeter of rectangles, L-shapes, triangles, parallelograms, circles, semicircles and shapes made from them (with the π button, 3.14, 22/7 or in terms of π), solve real-life floor problems (cost, packs, tiles, skirting), and read and draw scaled plans and maps.</p></div>
    <div><h3>In this pack</h3><p>p.1 Teacher notes · p.2 Floor Planner mingle cards + Plan Swap A/B cards · p.3 Area Dominoes (cut-up) · p.4 Wall poster · p.5 Worksheet: Error Hunt + exam-style questions · p.6 Answers. Level: 2nd year (Higher and Ordinary), or 3rd-year revision. Time: about 60 minutes. All questions are original.</p></div>
  </div>
  <h2 style="margin-top:8px">Procedure</h2>
  <table class="proc"><tbody>
    <tr><td>5 min</td><td><b>Lead-in: the perimeter trap.</b> Board two rooms: 5 m × 5 m and 9 m × 1 m. "Both have a perimeter of 20 m. Do they need the same amount of flooring?" Students vote, then check (25 m² v 9 m²). Which word goes with skirting board, and which with flooring?</td></tr>
    <tr><td>8 min</td><td><b>Guided discovery.</b> Pairs get an 8 cm × 4 cm rectangle, a triangle and a parallelogram with the same base and height on squared paper. Cut the triangle from corner to corner of the rectangle: what fraction is it? Cut a triangle off the parallelogram and slide it across: what shape appears? Build A = ½bh and A = bh, and ask why the sloping side never appears.</td></tr>
    <tr><td>10 min</td><td><b>Floor Planner mingle</b> (p.2, 24 cards = 12 question/answer pairs; one card each). Question card? Work it out and find the person with your answer. Answer card? Find your question. Pairs check each other's working.</td></tr>
    <tr><td>12 min</td><td><b>Plan Swap</b> (p.2, pairs, don't show your card). Each fact is on only ONE card. Ask your partner for what you're missing ("What is the scale?"), then both fill every blank. Feedback: floor {m2(ps_a)}, {ps_p} packs, {e(ps_c)}; patio paving {e(pt_pc)}, edging {e(pt_ec)}.</td></tr>
    <tr><td>10 min</td><td><b>Area Dominoes</b> (p.3), groups of 3–4. Start with START, work out the clue, find the domino with that answer on its left, and build the chain to FINISH.</td></tr>
    <tr><td>12 min</td><td><b>Worksheet</b> (p.5). Error Hunt in pairs (find the mistake, name the rule, fix it), then the exam-style questions alone.</td></tr>
    <tr><td>3 min</td><td><b>Exit ticket.</b> A circle has a radius of 6 cm: area in terms of π? A 7 m wall on a 1 : 50 plan? (36π cm²; 14 cm.) Homework: play <b>Floor Planner</b> at leim.ie/floor-planner.html and copy three lines from the "Go back over these" list.</td></tr>
  </tbody></table>
  <div class="note"><b>Mingle key</b> (question card → answer card): {match_key}.<br>
  <b>Errors to look for:</b> the sloping side as the height · forgetting ½ · the diameter in πr² · no straight edge on a semicircle · m for an area · rounding packs down · plan area × the scale. <b>Support:</b> a formula card with each shape drawn and its height marked. <b>Fast finishers:</b> a 20 m loop of rope: which rectangle encloses the most area? Can a circle beat it? (5 m × 5 m = 25 m²; circle ≈ 31.8 m²)</div>
  <p class="small"><b>Domino answer chain</b> (START → FINISH):</p>
  <ol class="small" style="columns:2;column-gap:12px;font-size:7pt;line-height:1.22;margin:0;padding-left:16px">{chain_key}</ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">Cut up the cards · one Plan Swap card per student</div><h1>Floor Planner + Plan Swap</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:8.8pt;margin:0"><b>Floor Planner mingle.</b> Cut out the 24 cards and give one to each student. Question card? Work it out, then find the person with your answer. Answer card? Find the question that gives your answer. (Fewer students? Take out whole pairs.)</p>
  <div class="fym">{match_html}</div>
  <p style="font-size:8.8pt;margin:3mm 0 0"><b>Plan Swap.</b> Don't show your card. Each fact is on only one of the two cards: ask your partner for what you're missing, then fill in every blank on both. A calculator is fine.</p>
  {swap_card("A")}
  {swap_card("B")}
</div>

<div class="page">
  <div class="band"><div><div class="k">Groups of 3–4 · cut along the dashed lines</div><h1>Area Dominoes</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.4pt">Start with START. Work out the clue on the right, then find the domino with that answer on its left. Keep going until you reach FINISH. ⊥ height = perpendicular height.</p>
  <div class="doms">{dom_html}</div>
</div>

<div class="page">
  <div class="poster">
    <h1>Area &amp; perimeter</h1>
    <div class="pf2"><div>{FIG["posterTri"]}</div><div style="font-size:15pt;line-height:1.5"><b>Triangle</b> ½ × base × ⊥ height<br><b>Parallelogram</b> base × ⊥ height<br><b>Rectangle</b> length × width</div></div>
    <div class="pf2"><div style="max-width:42mm;margin:auto">{FIG["posterCirc"]}</div><div style="font-size:15pt;line-height:1.5"><b>Circle</b> d = 2r<br>Circumference = 2πr = πd<br>Area = πr²</div></div>
    <div class="ops">
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Perimeter</b>around the edge<br>m or cm<br>fencing, skirting</div>
      <div style="background:var(--green-soft)"><b>Area</b>the space inside<br>m² or cm²<br>flooring, paint, tiles</div>
      <div style="background:var(--green-soft)"><b>Scale 1 : 50</b>plan → real: × 50<br>real → plan: ÷ 50<br>then ÷ 100 for metres</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Packs &amp; tins</b>area ÷ what one covers<br>then ROUND UP</div>
    </div>
    <p style="text-align:center;font-size:12pt;margin:0"><b>Semicircle perimeter</b> = half the circumference + the diameter</p>
    <p style="text-align:center;font-size:10pt;color:var(--muted)">Léim · leim.ie · Play Floor Planner: leim.ie/floor-planner.html</p>
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
  <div class="gfig" style="width:44mm">{FIG["wL"]}</div>
  <ol class="q">
    <li>The diagram shows an L-shaped hall. (a) Find the two sides that are not labelled. (b) Find the perimeter. (c) Find the area. (d) Carpet costs €18 per m². Find the cost of carpeting the hall.<span class="long"></span></li>
    <li>A round table top has a diameter of 1.2 m. (a) Find its area in terms of π. (b) Find its circumference, to 2 decimal places.<span class="long"></span></li>
    <li>A wheel has a diameter of 64 cm. How many complete turns does it make in 1 km?<span class="long"></span></li>
    <li>A wall 2.4 m wide and 1.5 m high is covered with square tiles 15 cm by 15 cm. (a) How many tiles are needed? (b) Tiles come in boxes of 12. How many boxes are needed?<span class="long"></span></li>
    <li>A map has a scale of 1 : 50,000. (a) A lake is 3.6 cm long on the map. How long is it in real life, in km? (b) How long is a 4.5 km walk on the map?<span class="long"></span></li>
  </ol>
</div>

<div class="page an">
  <div class="band"><div><div class="k">For the teacher</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>Plan Swap</h2>
  <div class="two"><table><tbody>
   <tr><td>Real length and width</td><td>11 × 50 = 550 cm = <b>{m(ps_l)}</b>; 8 × 50 = 400 cm = <b>{m(ps_w)}</b></td></tr><tr><td>Floor area</td><td>5.5 × 4 = <b>{m2(ps_a)}</b></td></tr>
   <tr><td>Packs needed</td><td>22 ÷ 2.5 = 8.8 → <b>{ps_p} packs</b></td></tr><tr><td>Cost</td><td>9 × €55 = <b>{e(ps_c)}</b></td></tr></tbody></table>
  <table><tbody>
   <tr><td>Radius</td><td><b>2.5 m</b></td></tr><tr><td>Area</td><td>π × 2.5² = <b>{m2(pt_a, dp=1)}</b></td></tr>
   <tr><td>Paving cost</td><td>19.635 × €40 = <b>{e(pt_pc)}</b></td></tr><tr><td>Circumference</td><td>π × 5 = <b>{m(pt_c, dp=1)}</b></td></tr>
   <tr><td>Edging cost</td><td>15.708 × €6.50 = <b>{e(pt_ec)}</b></td></tr></tbody></table></div>
  <h2>A. Error Hunt</h2>
  <table><tbody>{"".join(f"<tr><td style='width:36%'><b>{q}</b> {w}</td><td>{r}</td></tr>" for q,w,r in ERR)}</tbody></table>
  <h2>B. Exam-style questions</h2>
  <ol class="q">
    <li>(a) 6 − 2.5 = <b>3.5 m</b> and 8 − 3 = <b>5 m</b> (b) <b>{m(2 * (8 + 6))}</b> (c) 8 × 6 − 3 × 2.5 = <b>{m2(w1)}</b> (d) 40.5 × 18 = <b>{e(w1 * 18)}</b></li>
    <li>(a) π × 0.6² = <b>{pi_(F('0.36'), 'm²')}</b> (b) π × 1.2 = <b>{dpf(w2c, 2)} m</b></li>
    <li>1 km = 100,000 cm. One turn = π × 64 = 201.06 cm. 100,000 ÷ 201.06 = 497.4 → <b>{w3} complete turns</b></li>
    <li>(a) 240 ÷ 15 = 16 and 150 ÷ 15 = 10: <b>{w4} tiles</b> (b) 160 ÷ 12 = 13.3 → <b>{w4b} boxes</b></li>
    <li>(a) 3.6 × 50,000 = 180,000 cm = <b>{m(w5[0], 'km')}</b> (b) 450,000 cm ÷ 50,000 = <b>{m(w5[1], 'cm')}</b></li>
  </ol>
  <h2>Marking tip</h2>
  <p>Give credit for each step, as the exam does: the missing lengths, the formula, the substitution and the answer with the right units each earn marks. Accept answers in terms of π only when the question asks for them; otherwise check the rounding instruction. For "explain" parts insist on a sentence with numbers in it.</p>
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
<h1><span>Area, Perimeter</span><br><span>&amp; Scale Drawings</span></h1>
<div class="sub">Floor Planner mingle · Plan Swap A/B<br>Area Dominoes · Poster · Worksheet + answers</div>
<div class="em">Triangle = ½ × base × height</div></div>
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
    pdf("teacher-pack", os.path.join(OUT, "Area-Perimeter-Scale-Drawings-Teacher-Pack-Leim.pdf"))
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--hide-scrollbars", "--window-size=1200,1200",
                    f"--screenshot={os.path.join(OUT, f'{SLUG}-cover.png')}", f"{SLUG}-cover.html"], cwd=SRC, check=True, capture_output=True)
    print("domino chain:", [(x, a) for x, a in chain])
