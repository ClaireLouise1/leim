#!/usr/bin/env python3
"""Pythagoras & right-angled triangles (JC Maths topic 25): free sheet + teacher pack + Payhip cover.
Run from the repo root: python3 src/build_pythagoras_pdfs.py OUTDIR
Writes src/pythagoras-right-angled-triangles-*.html; PDFs/cover PNG go to OUTDIR (free sheet also to printables/).
Diagrams come from the Ladder Lab game's kit through src/ladder_figs_bridge.js and every labelled diagram is MEASURED back
with test_ladder_lab.py's reader (labels against the drawing, x worked out from the labels). Every answer is computed here
with exact arithmetic (half-up rounding) and asserted. Styles are read from src/build_money1_pdfs.py."""
import os, sys, random, subprocess, re, json, math
from fractions import Fraction as F
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC)
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/pyth"; os.makedirs(OUT, exist_ok=True)
SLUG = "pythagoras-right-angled-triangles"
LO = "GT.3b, GT.3e, U.6"

_ns = {}; exec(open(os.path.join(SRC, "test_ladder_lab.py"), encoding="utf-8").read().split('if __name__ == "__main__":')[0], _ns)
read_svg, fig_lengths, solve_x, sqrt_exact, dsqrt, r1 = (_ns[k] for k in ("read_svg", "fig_lengths", "solve_x", "sqrt_exact", "dsqrt", "r1"))

def n(x):
    x = F(x); s = f"{float(x):.2f}".rstrip("0").rstrip("."); return s.replace("-", "−")
def root(x2, unit=""):
    """√x2: exact (≤ 1 d.p.) or to 1 d.p. (half up), as text"""
    x2 = F(x2); ex = sqrt_exact(x2)
    if ex is not None and ex.denominator in (1, 2, 5, 10): return n(ex) + unit
    return f"{float(r1(dsqrt(x2))):.1f}" + unit
def Q(x): return F(str(x))
def hyp(a, b, u=""): return root(Q(a) ** 2 + Q(b) ** 2, u)
def leg(c, a, u=""): return root(Q(c) ** 2 - Q(a) ** 2, u)
def right(a, b, c):
    a, b, c = sorted(map(Q, (a, b, c))); return a * a + b * b == c * c
U = lambda s: s  # readability

# ---------- diagrams from the game's kit ----------
FIGS = {"rHyp": "FIX.hyp()", "rPat": "FIX.pattern()", "rIso": 'render(isoFig(10,13,["10 cm","13 cm","x"]),"Isosceles triangle")',
        "pA": 'render(rtTri0(9,12,["9 cm","12 cm","x"]),"Right-angled triangle")', "pB": 'render(rtTri0(8,15,["8 cm","x","17 cm"]),"Right-angled triangle")',
        "e31": 'render(ladder(2.1,7.2,["2.1 m",0,"7.5 m"]),"A 7.5 m ladder")', "e34": 'render(isoFig(9.6,6,["9.6 m","6 m",0]),"Gable end of a roof")',
        "w1": 'render(rtTri0(4,0.9,["4 m","0.9 m","x"]),"A ramp",[300,120])', "posterHyp": "FIX.hyp()", "posterPat": "FIX.pattern()"}
FIG = json.loads(subprocess.run(["node", os.path.join(SRC, "ladder_figs_bridge.js")], input=json.dumps(FIGS), capture_output=True, text=True, check=True).stdout)
def xval(name):
    D = read_svg(FIG[name]); known, unk = fig_lengths(D); assert len(unk) == 1, name
    return root(solve_x(D, known, unk[0]))
assert xval("pA") == "15" and xval("pB") == "15" and xval("rIso") == "12" and xval("w1") == "4.1"
for k in ("e31", "e34"): fig_lengths(read_svg(FIG[k]))   # labels match the drawing

# ---------- free sheet questions (each answer computed) ----------
A = [("Use diagram A. Find x.", hyp(9, 12, " cm")), ("Legs 7 cm and 24 cm. Find the hypotenuse.", hyp(7, 24, " cm")),
     ("Legs 1.5 m and 2 m. Find the hypotenuse.", hyp(1.5, 2, " m")), ("Legs 6 cm and 9 cm. Find the hypotenuse to 1 d.p.", hyp(6, 9, " cm")),
     ("Legs 4 m and 7 m. Find the hypotenuse to 1 d.p.", hyp(4, 7, " m")), ("√40 lies between which two whole numbers?", "6 and 7"),
     ("√90 lies between which two whole numbers?", "9 and 10"), ("A ladder reaches 6.3 m up a wall with its foot 1.6 m from the wall. How long is it?", hyp(1.6, 6.3, " m"))]
assert [a for q, a in A] == ["15 cm", "25 cm", "2.5 m", "10.8 cm", "8.1 m", "6 and 7", "9 and 10", "6.5 m"]
assert 6 ** 2 < 40 < 7 ** 2 and 9 ** 2 < 90 < 10 ** 2
B = [("Use diagram B. Find x.", leg(17, 8, " cm")), ("Hypotenuse 26 cm, one side 10 cm. Find the other side.", leg(26, 10, " cm")),
     ("Hypotenuse 6.5 m, one side 2.5 m. Find the other side.", leg(6.5, 2.5, " m")), ("Hypotenuse 12 cm, one side 7 cm. Find the other side to 1 d.p.", leg(12, 7, " cm")),
     ("Hypotenuse 9.5 m, one side 4 m. Find the other side to 1 d.p.", leg(9.5, 4, " m")), ("A 5 m ladder has its foot 1.4 m from a wall. How high does it reach?", leg(5, 1.4, " m")),
     ("A 4 m ladder has its foot 1.1 m from a wall. How high does it reach (1 d.p.)?", leg(4, 1.1, " m")), ("An isosceles triangle has a base of 10 cm and two sides of 13 cm. Find its height.", leg(13, 5, " cm"))]
assert [a for q, a in B] == ["15 cm", "24 cm", "6 m", "9.7 cm", "8.6 m", "4.8 m", "3.8 m", "12 cm"]
def yn(a, b, c): return "Yes" if right(a, b, c) else "No"
Cq = [("Is a triangle with sides 9, 40, 41 right-angled?", f"{yn(9, 40, 41)} (81 + 1600 = 1681 = 41²)"), ("Sides 7, 10, 12?", f"{yn(7, 10, 12)} (49 + 100 = 149, 12² = 144)"),
      ("Sides 12, 35, 37?", f"{yn(12, 35, 37)} (144 + 1225 = 1369 = 37²)"), ("Sides 0.9 m, 1.2 m, 1.5 m?", f"{yn(0.9, 1.2, 1.5)} (0.81 + 1.44 = 2.25 = 1.5²)"),
      ("Triangle ABC has |AB| = 24, |BC| = 7, |AC| = 25. Which angle is a right angle?", "∠ABC (opposite the longest side [AC])"),
      ("A builder marks 0.6 m and 0.8 m along two walls and measures 1.02 m between the marks. Is the corner square?", "No: 1.02 > 1, so the angle is more than 90°"),
      ("5, 12, 13 is a Pythagorean triple. Complete the triple 10, 24, …", str(13 * 2))]
assert [yn(9, 40, 41), yn(7, 10, 12), yn(12, 35, 37), yn(0.9, 1.2, 1.5)] == ["Yes", "No", "Yes", "Yes"] and 81 + 1600 == 1681 == 41 ** 2 and 49 + 100 == 149 and 144 + 1225 == 1369 == 37 ** 2
assert right(24, 7, 25) and hyp(0.6, 0.8) == "1" and right(10, 24, 26)
D_ = [("A TV screen is 80 cm wide and 45 cm high. Find its diagonal to 1 d.p.", hyp(80, 45, " cm")), ("A rectangle has a diagonal of 13 m and one side of 5 m. Find the other side.", leg(13, 5, " m")),
      ("A boat sails 9 km north, then 12 km east. How far is it from the start?", hyp(9, 12, " km")),
      ("A field is 40 m by 30 m. How much shorter is the diagonal than walking along two sides?", n(40 + 30 - F(hyp(40, 30))) + " m"),
      ("An isosceles triangle has a base of 16 cm and two sides of 10 cm. Find its height and its area.", f"{leg(10, 8, ' cm')}, {n(F(16) * F(leg(10, 8)) / 2)} cm²"),
      ("A 5.2 m ladder reaches 4.8 m up a wall. The top slides down to 4.4 m. How far is the foot from the wall now (1 d.p.)?", leg(5.2, 4.4, " m")),
      ("Find the diagonal of a square of side 6 cm, to 1 d.p.", hyp(6, 6, " cm"))]
assert [a for q, a in D_] == ["91.8 cm", "12 m", "15 km", "20 m", "6 cm, 48 cm²", "2.8 m", "8.5 cm"]
# exam-style
e31a, e31b = leg(7.5, 2.1, " m"), leg(7.5, 2.5, " m"); assert (e31a, e31b) == ("7.2 m", "7.1 m")
assert right(20, 48, 52) and not right(6, 7, 9) and 36 + 49 == 85
e33 = hyp(3.6, 0.8, " m"); assert e33 == "3.7 m"
e34h = leg(6, 4.8); e34a = Q(9.6) * F(e34h) / 2; assert e34h == "3.6" and n(e34a) == "17.28"
E = [("<b>A ladder.</b> A 7.5 m ladder leans against a wall with its foot 2.1 m from the wall. (a) How high up the wall does it reach? (b) The foot is moved so it is 2.5 m from the wall. How high does the ladder reach now, to 1 d.p.?",
      f"(a) √(7.5² − 2.1²) = √51.84 = <b>{e31a}</b> (b) √(7.5² − 2.5²) = √50 = <b>{e31b}</b>"),
     ("<b>Right-angled?</b> Triangle PQR has |PQ| = 20 cm, |QR| = 48 cm and |PR| = 52 cm. (a) Show that it is right-angled. (b) Which angle is 90°? (c) Cian says a triangle with sides 6, 7 and 9 is right-angled. Is he right?",
      "(a) 20² + 48² = 400 + 2304 = 2704 = 52² (b) <b>∠PQR</b>, opposite the longest side (c) <b>No</b>: 6² + 7² = 85 but 9² = 81"),
     ("<b>A ramp.</b> A ramp covers a horizontal distance of 3.6 m and rises 0.8 m. Find the length of the sloping surface, to 1 d.p.",
      f"√(3.6² + 0.8²) = √13.6 = <b>{e33}</b>"),
     ("<b>A roof.</b> The gable end of a roof is an isosceles triangle with a base of 9.6 m and sloping sides of 6 m. (a) Find its height. (b) Find its area.",
      f"(a) Half the base = 4.8 m: √(6² − 4.8²) = √12.96 = <b>{e34h} m</b> (b) ½ × 9.6 × 3.6 = <b>{n(e34a)} m²</b>")]
assert Q(7.5) ** 2 - Q(2.1) ** 2 == F("51.84") and Q(7.5) ** 2 - Q(2.5) ** 2 == 50 and Q(3.6) ** 2 + Q(0.8) ** 2 == F("13.6") and 36 - Q(4.8) ** 2 == F("12.96") and 400 + 2304 == 2704 == 52 ** 2
EFIG = {0: f'<div class="gfig" style="width:26mm">{FIG["e31"]}</div>', 3: f'<div class="gfig" style="width:40mm">{FIG["e34"]}</div>'}

def qs(items): return "".join(f"<li>{q} <span class='line'></span></li>" for q, a in items)
def style(var):
    return re.search(var + r' = f"""<!doctype.*?<style>(.*?)</style>', open(os.path.join(SRC, "build_money1_pdfs.py"), encoding="utf-8").read(), re.S).group(1).replace("{LO}", LO).replace("{{", "{").replace("}}", "}")
SHEET_STYLE = style("sheet"); PACK_STYLE = style("pack")
assert "@bottom-left" in SHEET_STYLE and "Single-teacher licence" in PACK_STYLE and "{{" not in SHEET_STYLE + PACK_STYLE
FIGCSS = """svg.pf{display:block;width:100%;height:auto;margin:0 auto}.gfig{float:right;width:40mm;margin:0 0 1mm 3mm}.rf{display:grid;grid-template-columns:1fr 1fr 1fr;gap:3mm;margin:1mm 0}
.rf div{font-size:8pt;text-align:center;line-height:1.25}.rf svg{max-height:30mm}.f3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:2mm;margin:1mm 0}.f3 div{border:1.5px solid var(--line);border-radius:6px;padding:1.5mm 2mm;font-size:8.6pt}"""

sheet = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Pythagoras' theorem: rules and practice | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{SHEET_STYLE}
{FIGCSS}
</style></head><body>
<div class="page tight">
  <div class="band"><div><div class="k">Junior Cycle Maths · Free revision sheet</div><h1>Pythagoras' theorem</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2018 specification): {LO}. Play the game: <b>leim.ie/ladder-lab.html</b></p>
  <div class="rf"><div>{FIG["rHyp"]}The hypotenuse c is opposite the right angle: c² = a² + b²</div><div>{FIG["rPat"]}3² + 4² = 9 + 16 = 25 = 5²</div><div>{FIG["rIso"]}Isosceles: use HALF the base. x² = 13² − 5², x = 12 cm</div></div>
  <div class="two">
   <div><h2>1. The theorem (Theorem 14)</h2>
    <p>In a right-angled triangle, the square of the <b>hypotenuse</b> (the side opposite the right angle, always the longest) is the sum of the squares of the other two sides: <b>c² = a² + b²</b>.</p>
    <h2>2. Finding a side</h2>
    <div class="f3"><div><b>Hypotenuse: ADD</b><br>5² + 12² = 169<br>√169 = 13</div><div><b>Shorter side: SUBTRACT</b><br>13² − 5² = 144<br>√144 = 12</div><div><b>Then √</b><br>√52 = 7.21… = 7.2 (1 d.p.)</div></div>
    <p><b>Sense check:</b> the hypotenuse is longer than both other sides; a shorter side is shorter than the hypotenuse.</p>
    <h2>3. Square roots</h2>
    <p>Know 1² … 15². √50 lies between 7 (7² = 49) and 8 (8² = 64).</p></div>
   <div><h2>4. Is it right-angled? (Theorem 15)</h2>
    <p>If (longest side)² = the sum of the squares of the other two, the triangle IS right-angled, and the right angle is <b>opposite the longest side</b>. 8, 15, 17: 64 + 225 = 289 = 17², yes. 6, 9, 11: 36 + 81 = 117 ≠ 121, no.</p>
    <p><b>Pythagorean triples:</b> 3, 4, 5 · 5, 12, 13 · 8, 15, 17 · 7, 24, 25 · 20, 21, 29, and their multiples (6, 8, 10).</p>
    <h2>5. Real life</h2>
    <p>Ladder = hypotenuse · diagonal of a rectangle = hypotenuse · north then east: the distance back is the hypotenuse · builder's check: 3 m, 4 m, gap 5 m.</p>
    <div class="note"><b>Classic mistakes:</b> adding the sides (5 + 12) instead of the squares · forgetting the √ · adding when you need a shorter side · the whole base of an isosceles triangle instead of half · rounding too early.</div></div>
  </div>
  <div class="tip"><b>Exam tip:</b> write the formula with the numbers in it (x² = 6.5² − 2.5²), round only at the end, and give the units.</div>
</div>

<div class="page p2">
  <div class="band"><div><div class="k">Practice · 34 questions</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. The hypotenuse</h2>
  <div class="gfig" style="width:30mm"><b style="font-size:8pt">Diagram A</b>{FIG["pA"]}</div>
  <ol class="q">{qs(A)}</ol>
  <h2 style="clear:both">B. A shorter side</h2>
  <div class="gfig" style="width:30mm"><b style="font-size:8pt">Diagram B</b>{FIG["pB"]}</div>
  <ol class="q" start="9">{qs(B)}</ol>
  <h2 style="clear:both">C. Is it right-angled?</h2><ol class="q" start="17">{qs(Cq)}</ol>
  <h2>D. Real life</h2><ol class="q" start="24">{qs(D_)}</ol>
  <p class="small" style="margin-top:4px;clear:both">Questions 31–34 are on the next page.</p>
</div>

<div class="page">
  <div class="band"><div><div class="k">Exam-style · then check</div><h1>Exam corner + answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>E. Exam-style questions (show your work)</h2>
  <ol class="q e3" start="31">{"".join(f"<li>{EFIG.get(i, '')}{q}<span class='long'></span><span class='long'></span></li>" for i,(q,a) in enumerate(E))}</ol>
  <h2 style="margin-top:10px;clear:both">Answers</h2>
  <table class="ans"><tbody>
   <tr><td><b>A</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(A,1))}</td></tr>
   <tr><td><b>B</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(B,9))}</td></tr>
   <tr><td><b>C</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(Cq,17))}</td></tr>
   <tr><td><b>D</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(D_,24))}</td></tr>
   <tr><td><b>E</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(E,31))}</td></tr>
  </tbody></table>
  <div class="note"><b>Got one wrong?</b> Did you find the hypotenuse first? Add for the hypotenuse, subtract for a shorter side, and take the square root at the end. Then play <b>Ladder Lab</b> at leim.ie/ladder-lab.html: the "Go back over these" list at the end shows the working for each mistake.</div>
  <p class="small">All questions written by Léim. Léim is independent and not connected with the State Examinations Commission or the NCCA.</p>
</div>
</body></html>"""

# ---------- teacher pack ----------
MATCH = [("Legs 6 cm and 8 cm: hypotenuse?", hyp(6, 8, " cm")), ("Legs 5 cm and 12 cm: hypotenuse?", hyp(5, 12, " cm")),
         ("Hypotenuse 25 cm, one side 7 cm: the other side?", leg(25, 7, " cm")), ("Hypotenuse 17 cm, one side 15 cm: the other side?", leg(17, 15, " cm")),
         ("A 5 m ladder, foot 3 m from the wall: how high?", leg(5, 3, " m")), ("Rectangle 9 m by 12 m: the diagonal?", hyp(9, 12, " m")),
         ("Isosceles: base 10 cm, sides 13 cm: the height?", leg(13, 5, " cm")), ("Legs 1 cm and 1 cm: hypotenuse (1 d.p.)?", hyp(1, 1, " cm")),
         ("√30 lies between…", "5 and 6"), ("Sides 6, 9, 11: right-angled?", "No: 117 ≠ 121"), ("Sides 20, 21, 29: right-angled?", "Yes: 841 = 841"),
         ("The side opposite the right angle", "The hypotenuse")]
ANS = [a for q, a in MATCH]
assert ANS == ["10 cm", "13 cm", "24 cm", "8 cm", "4 m", "15 m", "12 cm", "1.4 cm", "5 and 6", "No: 117 ≠ 121", "Yes: 841 = 841", "The hypotenuse"], ANS
assert 25 < 30 < 36 and not right(6, 9, 11) and 36 + 81 == 117 and right(20, 21, 29) and 400 + 441 == 841 and len(set(ANS)) == 12
cards = [q for q, a in MATCH] + ANS
random.seed(25); match_print = cards[:]; random.shuffle(match_print)
match_html = "".join(f'<div class="c"><span class="tag">Card {i}</span><div class="fc{" sm" if len(x) > 10 else ""}">{x}</div></div>' for i, x in enumerate(match_print, 1))
match_key = " · ".join(f"{match_print.index(q) + 1} → {match_print.index(a) + 1}" for q, a in MATCH)

# Triangle Swap: each fact on exactly ONE card; both students work out every blank
sw = {"lad": leg(6.5, 2.5, " m"), "roof": leg(5, 4, " m"), "path": hyp(12, 9, " m"), "kite": leg(50, 30, " m"), "tv": hyp(96, 54, " cm")}
assert sw == {"lad": "6 m", "roof": "3 m", "path": "15 m", "kite": "40 m", "tv": "110.1 cm"}, sw
assert F("5.1") ** 2 > 3 ** 2 + 4 ** 2   # shed: angle more than 90°
TR = [("Length of the ladder", "6.5 m", "A"), ("Foot of the ladder from the wall", "2.5 m", "B"), ("Roof: each sloping side", "5 m", "A"), ("Roof: width of the house (the base)", "8 m", "B"),
      ("Garden: length", "12 m", "A"), ("Garden: width", "9 m", "B"),
      ("How high the ladder reaches", "", None), ("Height of the roof", "", None), ("Diagonal path across the garden", "", None)]
MR = [("Kite: string (straight)", "50 m", "B"), ("Kite: distance along the ground", "30 m", "A"), ("TV: width", "96 cm", "B"), ("TV: height", "54 cm", "A"),
      ("Shed: marks along the two walls", "3 m and 4 m", "B"), ("Shed: gap between the marks", "5.1 m", "A"),
      ("Height of the kite", "", None), ("TV diagonal (1 d.p.)", "", None), ("Is the shed corner square?", "", None)]
for rows in (TR, MR):
    assert all(w in ("A", "B") for _, v, w in rows if v) and any(w == "A" for *_, w in rows) and any(w == "B" for *_, w in rows)
def swap_card(who):
    def tab(title, rows):
        return f'<table class="ss"><thead><tr><th colspan="2">{title}</th></tr></thead><tbody>' + "".join(
            f"<tr><td>{k}</td><td><b>{v if w == who else ''}</b></td></tr>" for k, v, w in rows) + "</tbody></table>"
    return f'<div class="idc"><h3>Student {who} · Triangle Swap</h3><div class="two">{tab("The Murphys’ house", TR)}{tab("Out and about", MR)}</div></div>'

DOMS = [("Legs 3 and 4: hypotenuse", hyp(3, 4)), ("Legs 9 and 12: hypotenuse", hyp(9, 12)), ("Legs 8 and 15: hypotenuse", hyp(8, 15)),
        ("Legs 7 and 24: hypotenuse", hyp(7, 24)), ("Legs 12 and 16: hypotenuse", hyp(12, 16)), ("Legs 1.5 and 2: hypotenuse", hyp(1.5, 2)),
        ("Hypotenuse 10, side 6: other side", leg(10, 6)), ("Hypotenuse 26, side 24: other side", leg(26, 24)), ("Hypotenuse 41, side 40: other side", leg(41, 40)),
        ("Hypotenuse 6.5, side 2.5: other side", leg(6.5, 2.5)), ("Legs 2 and 3: hypotenuse (1 d.p.)", hyp(2, 3)), ("Legs 5 and 5: hypotenuse (1 d.p.)", hyp(5, 5)),
        ("Hypotenuse 9, side 4: other side (1 d.p.)", leg(9, 4)), ("√150 lies between 12 and …", "13"), ("7² + 24²", str(7 ** 2 + 24 ** 2)),
        ("Complete the triple 9, 40, …", "41"), ("Sides 5, 6, 8: right-angled?", "No"), ("Sides 33, 56, 65: right-angled?", "Yes"),
        ("The side opposite the right angle", "hypotenuse"), ("Square of side 10: diagonal (1 d.p.)", hyp(10, 10))]
DANS = [a for k, a in DOMS]
assert DANS == ["5", "15", "17", "25", "20", "2.5", "8", "10", "9", "6", "3.6", "7.1", "8.1", "13", "625", "41", "No", "Yes", "hypotenuse", "14.1"], DANS
assert 144 < 150 < 169 and right(9, 40, 41) and not right(5, 6, 8) and right(33, 56, 65) and len(set(DANS)) == 20
random.seed(2525); chain = DOMS[:]; random.shuffle(chain)
dom = [("START" if k == 0 else chain[k - 1][1], x[0]) for k, x in enumerate(chain)] + [(chain[-1][1], "FINISH")]
dom_print = dom[:]; random.shuffle(dom_print)
dom_html = "".join(f'<div class="dom"><div class="h l{" sm" if len(l) > 9 else ""}">{l}</div><div class="h r">{r}</div></div>' for l, r in dom_print)
chain_key = "".join(f"<li>{x} = <b>{a}</b></li>" for x, a in chain)

ERR = [("Legs 6 cm and 8 cm. Find the hypotenuse.", "6 + 8 = 14 cm", f"Square first: √(6² + 8²) = √100 = <b>{hyp(6, 8, ' cm')}</b>"),
       ("Hypotenuse 13 cm, one side 5 cm. Find the other side.", "√(13² + 5²) = 13.9 cm", f"A shorter side: SUBTRACT. √(13² − 5²) = √144 = <b>{leg(13, 5, ' cm')}</b>"),
       ("Legs 5 m and 7 m. Find the hypotenuse to 1 d.p.", "5² + 7² = 74 m", f"Forgot the square root: √74 = <b>{hyp(5, 7, ' m')}</b>"),
       ("Is a triangle with sides 10, 24, 26 right-angled?", "10² + 26² = 776 ≠ 24², so no", f"Test the LONGEST side: 10² + 24² = 676 = 26², so <b>{yn(10, 24, 26).lower()}</b>, it is"),
       ("Isosceles: base 12 cm, equal sides 10 cm. Find the height.", "12² − 10² = 44, h = 6.6 cm", f"Use HALF the base: √(10² − 6²) = √64 = <b>{leg(10, 6, ' cm')}</b>"),
       ("A 4 m ladder, foot 1 m from the wall. Height to 1 d.p.?", "√(4² − 1²) = √15 = 3.8 m", f"√15 = 3.872…, which rounds UP: <b>{leg(4, 1, ' m')}</b>")]
assert hyp(6, 8) == "10" and hyp(5, 7) == "8.6" and leg(4, 1) == "3.9" and 144 - 100 == 44
# worksheet exam-style
w1 = hyp(4, 0.9, " m"); w2 = right(16, 30, 34); w3a, w3b = hyp(88, 50, " cm"), leg(120, 104, " cm"); w4a, w4b = leg(50, 30, " m"), leg(65, 40, " m"); w5 = hyp(3, 1.2, " m")
assert (w1, w2, w3a, w3b, w4a, w4b, w5) == ("4.1 m", True, "101.2 cm", "59.9 cm", "40 m", "51.2 m", "3.2 m"), (w1, w3a, w3b, w4b, w5)

pack = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Pythagoras' Theorem Teacher Pack | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{PACK_STYLE}
{FIGCSS}
.ss td:nth-child(2){{width:24%}}.ss td,.ss th{{padding:1px 5px;font-size:8.6pt;line-height:1.2}}.fym .c{{height:15mm}}.fym .fc{{font-size:13pt}}.fym .fc.sm{{font-size:9pt}}.p1 .proc td{{font-size:8.4pt;padding:2px 6px}}
.idc{{break-inside:avoid}}.dom .r{{font-size:9.6pt}}.dom .l{{font-size:12pt}}.dom .l.sm{{font-size:10pt}}
.big{{text-align:center;font-size:44pt;font-weight:800;margin:2mm 0;letter-spacing:.02em}}
.pf2{{display:grid;grid-template-columns:1fr 1fr;gap:5mm;align-items:center}}.pf2 svg{{max-height:62mm;width:auto;max-width:100%}}.poster .ops div{{font-size:12pt}}
</style></head><body>

<div class="page p1">
  <div class="band"><div><div class="k">Junior Cycle Maths · Teacher pack</div><h1>Pythagoras' theorem</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2018 specification): {LO}</p>
  <div class="two">
    <div><h3>Aims</h3><p>By the end of the lesson students can name the hypotenuse, use Pythagoras' theorem (Theorem 14) to find the hypotenuse or a shorter side (with square roots, to a given accuracy), use the converse (Theorem 15) to decide whether a triangle is right-angled, and solve real-life problems: ladders, diagonals, isosceles triangles and journeys.</p></div>
    <div><h3>In this pack</h3><p>p.1 Teacher notes · p.2 Ladder Lab mingle cards + Triangle Swap A/B · p.3 Pythagoras Dominoes (cut-up) · p.4 Wall poster · p.5 Worksheet: Error Hunt + exam-style questions · p.6 Answers. Level: 2nd year (Higher and Ordinary), or 3rd-year revision. Time: about 60 minutes. All questions are original.</p></div>
  </div>
  <h2 style="margin-top:8px">Procedure</h2>
  <table class="proc"><tbody>
    <tr><td>8 min</td><td><b>Lead-in: square the sides.</b> Pairs draw right-angled triangles on squared paper with shorter sides 3 &amp; 4, 6 &amp; 8 and 5 &amp; 12 squares, measure the longest side, and fill a table with a², b² and c². "What do you notice?" Then one triangle that ISN'T right-angled: does it still work? Build c² = a² + b² and the word <b>hypotenuse</b>.</td></tr>
    <tr><td>5 min</td><td><b>The rope trick (the converse).</b> Tie 12 equally spaced knots in a loop of string. Three students pull it into a triangle with sides 3, 4 and 5 knots. What angle appears? Builders still use the 3-4-5 check: if (longest side)² = a² + b², the triangle is right-angled (Theorem 15).</td></tr>
    <tr><td>10 min</td><td><b>Ladder Lab mingle</b> (p.2, 24 cards = 12 question/answer pairs; one card each, calculators allowed). Question card? Work it out and find your answer. Answer card? Find your question. Pairs say which side is the hypotenuse and whether they added or subtracted.</td></tr>
    <tr><td>12 min</td><td><b>Triangle Swap</b> (p.2, pairs, one A and one B card). Don't show your card. Each fact is on only one card: ask your partner for what you're missing, sketch each triangle, mark the hypotenuse and fill every blank on both cards.</td></tr>
    <tr><td>12 min</td><td><b>Pythagoras Dominoes</b> (p.3), groups of 3–4, calculators allowed. Start with START, work out the clue, find the domino with that answer on its left, and build the chain to FINISH.</td></tr>
    <tr><td>10 min</td><td><b>Worksheet</b> (p.5). Error Hunt in pairs (find the mistake, fix it), then the exam-style questions alone.</td></tr>
    <tr><td>3 min</td><td><b>Exit ticket.</b> Is a triangle with sides 7 cm, 8 cm and 11 cm right-angled? Show why. Homework: play <b>Ladder Lab</b> at leim.ie/ladder-lab.html and copy three lines from the "Go back over these" list.</td></tr>
  </tbody></table>
  <div class="note"><b>Mingle key</b> (question card → answer card): {match_key}.<br>
  <b>Triangle Swap answers:</b> ladder {sw["lad"]} · roof {sw["roof"]} (half the base is 4 m) · path {sw["path"]} · kite {sw["kite"]} · TV {sw["tv"]} · shed: <b>no</b>, 5.1 m &gt; 5 m, so the angle is more than 90°.<br>
  <b>Errors to look for:</b> adding the sides instead of the squares · forgetting the √ · adding when a shorter side is needed · using the whole base of an isosceles triangle · testing the wrong side in the converse · rounding too early. <b>Exit ticket:</b> 49 + 64 = 113 ≠ 121, so no.</div>
  <p class="small"><b>Domino answer chain</b> (START → FINISH):</p>
  <ol class="small" style="columns:2;column-gap:12px;font-size:7.2pt;line-height:1.22;margin:0;padding-left:16px">{chain_key}</ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">Cut up the cards · one Triangle Swap card per student</div><h1>Ladder Lab mingle + Triangle Swap</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:8.8pt;margin:0"><b>Ladder Lab mingle.</b> Cut out the 24 cards and give one to each student. Question card? Work it out, then find the person with your answer. Answer card? Find the question that gives your answer. (Fewer students? Take out whole pairs.)</p>
  <div class="fym">{match_html}</div>
  <p style="font-size:8.8pt;margin:3mm 0 0"><b>Triangle Swap.</b> Don't show your card. Each fact is on only one of the two cards: ask your partner for what you're missing, sketch the triangle, then fill in every blank on both. A calculator is fine.</p>
  {swap_card("A")}
  {swap_card("B")}
</div>

<div class="page">
  <div class="band"><div><div class="k">Groups of 3–4 · cut along the dashed lines</div><h1>Pythagoras Dominoes</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.4pt">Start with START. Work out the clue on the right, then find the domino with that answer on its left. Keep going until you reach FINISH. "Legs" = the two shorter sides.</p>
  <div class="doms">{dom_html}</div>
</div>

<div class="page">
  <div class="poster">
    <h1>Pythagoras' theorem</h1>
    <div class="big">c² = a² + b²</div>
    <div class="pf2"><div>{FIG["posterHyp"]}</div><div>{FIG["posterPat"]}</div></div>
    <p style="text-align:center;font-size:13pt;margin:1mm 0 3mm">The <b>hypotenuse</b> c is opposite the right angle. It is always the longest side.</p>
    <div class="ops">
      <div style="background:var(--green-soft)"><b>Find the hypotenuse</b>ADD the squares<br>then √<br>5² + 12² = 169 → 13</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Find a shorter side</b>SUBTRACT from c²<br>then √<br>13² − 5² = 144 → 12</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Right-angled?</b>longest² = the sum<br>of the other two squares<br>(Theorem 15)</div>
      <div style="background:var(--green-soft)"><b>Triples</b>3, 4, 5 · 5, 12, 13<br>8, 15, 17 · 7, 24, 25<br>and their multiples</div>
    </div>
    <p style="text-align:center;font-size:10pt;color:var(--muted)">Léim · leim.ie · Play Ladder Lab: leim.ie/ladder-lab.html</p>
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
  <ol class="q">
    <li><div class="gfig" style="width:44mm">{FIG["w1"]}</div>A wheelchair ramp rises 0.9 m over a horizontal distance of 4 m (diagram). Find the length of the ramp's sloping surface.<span class="long"></span></li>
    <li style="clear:both">Triangle KLM has |KL| = 16 cm, |LM| = 30 cm and |KM| = 34 cm. Show that it is right-angled and name the right angle.<span class="long"></span></li>
    <li>(a) A TV screen is 88 cm wide and 50 cm high. Find its diagonal, to 1 d.p. (b) Another screen has a 120 cm diagonal and is 104 cm wide. Find its height, to 1 d.p.<span class="long"></span></li>
    <li>A kite's string is 50 m long and tight. The kite is directly above a point 30 m along the ground from Aoife's hand. (a) How high is the kite? (b) She lets the string out to 65 m and the kite stays at the same height. How far along the ground is it now, to 1 d.p.?<span class="long"></span></li>
    <li>A farm gate is 3 m long and 1.2 m high. (a) Find the length of the diagonal brace, to 1 d.p. (b) Planks come in 3 m and 3.5 m lengths. Which length must Liam buy? Explain.<span class="long"></span></li>
  </ol>
</div>

<div class="page an">
  <div class="band"><div><div class="k">For the teacher</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>Triangle Swap</h2>
  <p>Ladder: √(6.5² − 2.5²) = <b>{sw["lad"]}</b> · Roof: √(5² − 4²) = <b>{sw["roof"]}</b> · Path: √(12² + 9²) = <b>{sw["path"]}</b> · Kite: √(50² − 30²) = <b>{sw["kite"]}</b> · TV: √(96² + 54²) = √12,132 = <b>{sw["tv"]}</b> · Shed: 3² + 4² = 25, so a square corner needs 5 m; the gap is 5.1 m, so <b>no</b>: the angle is more than 90°.</p>
  <h2>A. Error Hunt</h2>
  <table><tbody>{"".join(f"<tr><td style='width:40%'><b>{q}</b> {w}</td><td>{r}</td></tr>" for q,w,r in ERR)}</tbody></table>
  <h2>B. Exam-style questions</h2>
  <ol class="q">
    <li>The ramp is the hypotenuse: √(4² + 0.9²) = √16.81 = <b>{w1}</b>.</li>
    <li>16² + 30² = 256 + 900 = 1156 and 34² = 1156. They are equal, so the triangle is right-angled (Theorem 15). The right angle is opposite the longest side [KM]: <b>∠KLM</b>.</li>
    <li>(a) √(88² + 50²) = √10,244 = <b>{w3a}</b>. (b) √(120² − 104²) = √3584 = <b>{w3b}</b>.</li>
    <li>(a) √(50² − 30²) = √1600 = <b>{w4a}</b>. (b) √(65² − 40²) = √2625 = <b>{w4b}</b>.</li>
    <li>(a) √(3² + 1.2²) = √10.44 = <b>{w5}</b>. (b) <b>3.5 m</b>: the brace is longer than 3 m.</li>
  </ol>
  <h2>Marking tip</h2>
  <p>Give credit for each step, as the exam does: the formula with the numbers substituted, the correct squares, the square root, then rounding and units. In "show that" questions both sides must be worked out and compared, with a conclusion that names the theorem or the right angle.</p>
</div>
</body></html>"""
assert 256 + 900 == 1156 == 34 ** 2 and 88 ** 2 + 50 ** 2 == 10244 and 120 ** 2 - 104 ** 2 == 3584 and 65 ** 2 - 40 ** 2 == 2625 and 9 + F("1.44") == F("10.44") and 16 + F("0.81") == F("16.81")
assert 96 ** 2 + 54 ** 2 == 12132 and F(w5.split()[0]) > 3

cover = """<!doctype html><html><head><meta charset="utf-8"><style>
body{margin:0;width:1200px;height:1200px;background:#1B2430;font-family:Inter,sans-serif;color:#fff;display:flex;flex-direction:column;justify-content:space-between;padding:90px;box-sizing:border-box}
.k{display:inline-block;background:#2E7D57;border-radius:99px;padding:12px 26px;font-weight:700;font-size:28px;letter-spacing:.06em;text-transform:uppercase}
h1{font-size:104px;font-weight:800;line-height:1.14;letter-spacing:-.03em;margin:40px 0 0}
h1 span{background:#F6CF5A;color:#1B2430;padding:0 14px;box-decoration-break:clone;-webkit-box-decoration-break:clone}
.sub{font-size:38px;color:#C9D1DA;margin-top:36px;line-height:1.35}
.em{font-size:64px;margin-top:30px;font-weight:800;letter-spacing:.01em;color:#F6CF5A}
.foot{display:flex;justify-content:space-between;align-items:center;font-size:34px;font-weight:700}
.price{background:#F6CF5A;color:#1B2430;border-radius:16px;padding:14px 28px}
</style></head><body>
<div><span class="k">Junior Cycle Maths · Teacher pack</span>
<h1><span>Pythagoras'</span><br><span>Theorem</span></h1>
<div class="sub">Ladder Lab mingle · Triangle Swap A/B<br>Dominoes · Poster · Worksheet + answers</div>
<div class="em">c² = a² + b²</div></div>
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
    pdf("teacher-pack", os.path.join(OUT, "Pythagoras-Theorem-Teacher-Pack-Leim.pdf"))
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--hide-scrollbars", "--window-size=1200,1200",
                    f"--screenshot={os.path.join(OUT, f'{SLUG}-cover.png')}", f"{SLUG}-cover.html"], cwd=SRC, check=True, capture_output=True)
    print("domino chain:", [(x, a) for x, a in chain])
