#!/usr/bin/env python3
"""Transformations & symmetry (JC Maths topic 23): free sheet + teacher pack + Payhip cover.
Run from the repo root: python3 src/build_transformations_pdfs.py OUTDIR
Writes src/transformations-symmetry-*.html; PDFs/cover PNG go to OUTDIR (free sheet also to printables/).
Diagrams come from the Mirror Move game's grid kit through src/mirror_figs_bridge.js and every diagram is read back
by test_mirror_move.py's readers. Every answer is computed here and asserted. Styles are read from src/build_money1_pdfs.py."""
import os, sys, random, subprocess, re, json, itertools
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC)
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/transf"; os.makedirs(OUT, exist_ok=True)
SLUG = "transformations-symmetry"
LO = "GT.6a, GT.6b"

# ---------- my own transformations on (x, y) ----------
def sx(p): return (p[0], -p[1])                 # axial symmetry in the x-axis
def sy(p): return (-p[0], p[1])                 # axial symmetry in the y-axis
def so(p, c=(0, 0)): return (2 * c[0] - p[0], 2 * c[1] - p[1])   # central symmetry
def acw(p, c=(0, 0)): return (c[0] - (p[1] - c[1]), c[1] + (p[0] - c[0]))
def cw(p, c=(0, 0)): return (c[0] + (p[1] - c[1]), c[1] - (p[0] - c[0]))
def tr(p, v): return (p[0] + v[0], p[1] + v[1])
def vline(k): return lambda p: (2 * k - p[0], p[1])   # axial symmetry in the vertical line x = k
def c(p): return "(" + ", ".join(str(v).replace("-", "−") for v in p) + ")"
def cl(P): return ", ".join(c(p) for p in P)
def mv(v):
    s = []
    if v[0]: s.append(f"{abs(v[0])} {'unit' if abs(v[0]) == 1 else 'units'} {'right' if v[0] > 0 else 'left'}")
    if v[1]: s.append(f"{abs(v[1])} {'unit' if abs(v[1]) == 1 else 'units'} {'up' if v[1] > 0 else 'down'}")
    return " and ".join(s)
assert c(acw((4, 1))) == "(−1, 4)" and c(cw((4, 1))) == "(1, −4)" and c(so((3, 5), (1, 2))) == "(−1, −1)" and mv((-3, 4)) == "3 units left and 4 units up"

# ---------- diagrams from the game's kit, each read back ----------
S0 = [(-5, 1), (-2, 1), (-4, 3)]
def js(P): return "[" + ",".join(f"[{x},{y}]" for x, y in P) + "]"
FIGS = {
    "ruleAll": 'window.__leimTest.kit.FIX.ruleAll()',
    "pA": 'plane({R:6,lines:[{t:"y",c:1}],pts:[{p:[3,2],n:"A"},{p:[-2,4],n:"B"},{p:[1,-3],n:"D"}]})',
    "pD": 'plane({R:6,polys:[{P:%s,c:"ob",n:"S"},{P:img(TR([6,-5]),%s),c:"im",n:"A"},{P:img(AX({t:"y",c:0}),%s),c:"im",n:"B"},{P:img(CS([0,0]),%s),c:"im",n:"C"},{P:img(RO([0,0],true),%s),c:"im",n:"D"}]})' % ((js(S0),) * 5),
    "pE": 'cells(8,6,[[1,5],[2,4],[3,4],[0,2],[2,1],[3,1],[3,0],[5,4],[4,1]],{t:"v"})',
    "wT": 'plane({R:6,polys:[{P:[[1,2],[4,2],[1,4]],c:"ob",n:"T"}]})',
    "wP": 'cells(6,6,[[1,0],[2,0],[3,1],[4,1],[4,2],[5,3],[0,1],[0,3],[1,4]],{t:"d"})',
    "posterAll": 'window.__leimTest.kit.FIX.ruleAll()',
    "posterSq": 'window.__leimTest.kit.FIX.ruleSq()',
}
FIG = json.loads(subprocess.run(["node", os.path.join(SRC, "mirror_figs_bridge.js")], input=json.dumps(FIGS), capture_output=True, text=True, check=True).stdout)
_ns = {}; exec(open(os.path.join(SRC, "test_mirror_move.py"), encoding="utf-8").read().split("if __name__")[0], _ns)
pics = {k: _ns["read_plane"](v) for k, v in FIG.items() if 'class="tg"' in v}
assert pics["pA"]["pts"] == {"A": (3, 2), "B": (-2, 4), "D": (1, -3)}
mA = vline(1)
P_D = {p["n"]: p["P"] for p in pics["pD"]["polys"]}
KIND = {k: _ns["isometry_kinds"](P_D["S"], P_D[k]) for k in "ABCD"}
assert KIND == {"A": {"tr"}, "B": {"ax"}, "C": {"cs"}, "D": {"ro"}}, KIND
assert sorted(P_D["D"]) == sorted(cw(p) for p in S0) and sorted(P_D["B"]) == sorted(sy(p) for p in S0)
for A_, B_ in itertools.combinations(pics["pD"]["polys"], 2): assert not set(A_["P"]) & set(B_["P"])
W, H, on, f = _ns["read_cells"](FIG["pE"]); nE = _ns["complete_count"](W, H, on, f)
W, H, on2, f2 = _ns["read_cells"](FIG["wP"]); nP = _ns["complete_count"](W, H, on2, f2)
assert (nE, nP) == (5, 5), (nE, nP)
for k in list(FIG): FIG[k] = re.sub(r' style="max-width:\d+px"', "", FIG[k])

# ---------- free sheet ----------
A = [("Find the image of (4, 1) under axial symmetry in the x-axis.", c(sx((4, 1)))),
     ("Find the image of (−3, 5) under axial symmetry in the y-axis.", c(sy((-3, 5)))),
     ("Find the image of (0, −4) under axial symmetry in the x-axis.", c(sx((0, -4)))),
     ("Find the image of (−2, −6) under axial symmetry in the y-axis.", c(sy((-2, -6)))),
     ("Use the diagram. Find the image of A under axial symmetry in the line m.", c(mA((3, 2)))),
     ("Find the image of B under axial symmetry in the line m.", c(mA((-2, 4)))),
     ("Find the image of D under axial symmetry in the line m.", c(mA((1, -3)))),
     ("The image of P under axial symmetry in the y-axis is (−5, 2). Find P.", c(sy((-5, 2))))]
assert [a for q, a in A] == ["(4, −1)", "(3, 5)", "(0, 4)", "(2, −6)", "(−1, 2)", "(4, 4)", "(1, −3)", "(5, 2)"]
v10 = (5 - 2, -3 - 1)
B = [("Translate (1, 4) by 3 units right and 2 units down.", c(tr((1, 4), (3, -2)))),
     ("A translation maps (2, 1) onto (5, −3). Find the image of (−4, 0).", c(tr((-4, 0), v10))),
     ("Which point does the translation in question 10 map onto (0, 0)?", c((-v10[0], -v10[1]))),
     ("Find the image of (3, −5) under central symmetry in the origin.", c(so((3, -5)))),
     ("Find the image of (−6, −2) under central symmetry in the origin.", c(so((-6, -2)))),
     ("Find the image of (3, 5) under central symmetry in the point C(1, 2).", c(so((3, 5), (1, 2)))),
     ("Find the image of (2, 3) under central symmetry in the point C(−1, 0).", c(so((2, 3), (-1, 0)))),
     ("Under central symmetry in the origin, which point is its own image?", "(0, 0)")]
assert [a for q, a in B] == ["(4, 2)", "(−1, −4)", "(−3, 4)", "(−3, 5)", "(6, 2)", "(−1, −1)", "(−4, −3)", "(0, 0)"]
Cq = [("Rotate (4, 1) by 90° anticlockwise about (0, 0).", c(acw((4, 1)))),
      ("Rotate (4, 1) by 90° clockwise about (0, 0).", c(cw((4, 1)))),
      ("Rotate (2, −3) by 180° about (0, 0).", c(so((2, -3)))),
      ("Rotate (−2, −5) by 90° anticlockwise about (0, 0).", c(acw((-2, -5)))),
      ("Rotate (0, 3) by 90° clockwise about (0, 0).", c(cw((0, 3)))),
      ("Two rotations of 90° clockwise about (0, 0), one after the other, are the same as which single transformation?", "central symmetry in (0, 0)")]
assert cw(cw((7, 2))) == so((7, 2))
assert [a for q, a in Cq] == ["(−1, 4)", "(1, −4)", "(−2, 3)", "(5, −2)", "(3, 0)", "central symmetry in (0, 0)"]
NAME = {"tr": f"translation, {mv((6, -5))}", "ax": "axial symmetry in the y-axis", "cs": "central symmetry in the origin", "ro": "rotation of 90° clockwise about (0, 0)"}
D = [(f"Use the diagram. Name the transformation that maps S onto {k}.", NAME[next(iter(KIND[k]))]) for k in "ABCD"] + [
     ("How many axes of symmetry does a rectangle have?", "2"),
     ("How many axes of symmetry does a regular pentagon have?", "5"),
     ("Which of these has a centre of symmetry: a kite, a parallelogram or an isosceles triangle?", "a parallelogram"),
     ("Use the squared paper. How many more squares must be shaded so that m is an axis of symmetry?", str(nE))]
assert [a for q, a in D][:4] == ["translation, 6 units right and 5 units down", "axial symmetry in the y-axis", "central symmetry in the origin", "rotation of 90° clockwise about (0, 0)"]
assert _ns["AXES"]["rectangle"] == 2 and _ns["AXES"]["regular pentagon"] == 5 and _ns["CENTRE"]["parallelogram"] and not _ns["CENTRE"]["kite"]
# exam-style
T = [(1, 1), (4, 1), (2, 3)]
e1a = [sx(p) for p in T]; e1b = [tr(p, (-5, 1)) for p in T]; e1c = acw((4, 1)); e1d_from = e1a; e1d_to = [sy(p) for p in T]
# image in the x-axis → image in the y-axis is a half turn in (0, 0)
assert sorted(so(p) for p in e1a) == sorted(e1d_to)
e3a = so((-2, 3), (1, 1)); e3v = (e3a[0] + 2, e3a[1] - 3); e3c = tr((0, 0), e3v)
assert (e3a, e3v, e3c) == ((4, -1), (6, -4), (6, -4))
E = [("<b>Triangle T</b> has corners (1, 1), (4, 1) and (2, 3). (a) Write the corners of its image under axial symmetry in the x-axis. (b) Write the corners of its image under the translation 5 units left and 1 unit up. (c) Find the image of (4, 1) under a rotation of 90° anticlockwise about (0, 0). (d) Which single transformation maps the image in (a) onto the image of T in the y-axis?",
      f"(a) <b>{cl(e1a)}</b> (b) <b>{cl(e1b)}</b> (c) <b>{c(e1c)}</b> (d) <b>central symmetry in the origin</b>"),
     ("<b>The logo.</b> A logo is a regular hexagon. (a) How many axes of symmetry does it have? (b) Does it have a centre of symmetry? (c) Name a quadrilateral with exactly 2 axes of symmetry and a centre of symmetry.",
      "(a) <b>6</b> (b) <b>yes</b> (c) a <b>rectangle</b> (or a rhombus)"),
     ("<b>Centre and slide.</b> A is (−2, 3) and C is (1, 1). (a) Find A′, the image of A under central symmetry in C. (b) Describe the translation that maps A onto A′. (c) Find the image of (0, 0) under that translation.",
      f"(a) <b>{c(e3a)}</b> (b) <b>{mv(e3v)}</b> (c) <b>{c(e3c)}</b>"),
     ("<b>Spot the slip.</b> Ciara says the image of (3, 1) under a rotation of 90° clockwise about (0, 0) is (−1, 3). Explain her mistake and give the right answer.",
      f"(−1, 3) is the <b>anticlockwise</b> turn. Clockwise: <b>{c(cw((3, 1)))}</b>")]
assert c(acw((3, 1))) == "(−1, 3)"

def qs(items): return "".join(f"<li>{q} <span class='line'></span></li>" for q, a in items)
def style(var):
    return re.search(var + r' = f"""<!doctype.*?<style>(.*?)</style>', open(os.path.join(SRC, "build_money1_pdfs.py"), encoding="utf-8").read(), re.S).group(1).replace("{LO}", LO).replace("{{", "{").replace("}}", "}")
SHEET_STYLE = style("sheet"); PACK_STYLE = style("pack")
assert "@bottom-left" in SHEET_STYLE and "Single-teacher licence" in PACK_STYLE and "{{" not in SHEET_STYLE + PACK_STYLE
FIGCSS = """svg.tg{display:block;width:100%;height:auto;background:#fff}svg.tg .gl{stroke:#D5DDE5;stroke-width:.8}svg.tg .ax{stroke:#5B6775;stroke-width:1.4}
svg.tg .tk{font:600 9.5px Inter,sans-serif;fill:#5B6775}svg.tg .axl{font:italic 700 12px Inter,sans-serif;fill:#5B6775}svg.tg .sp{stroke-width:2;stroke-linejoin:round}
svg.tg .sp.ob{fill:rgba(46,125,87,.28);stroke:#2E7D57}svg.tg .sp.im{fill:rgba(41,98,166,.14);stroke:#2962A6}svg.tg .pn,svg.tg .pl{font:800 13px Inter,sans-serif;fill:#1B2430;paint-order:stroke;stroke:#fff;stroke-width:3px}
svg.tg .mir{stroke:#C0392B;stroke-width:2;stroke-dasharray:6 4}svg.tg .ml{font:italic 800 15px Inter,sans-serif;fill:#C0392B;paint-order:stroke;stroke:#fff;stroke-width:3px}
svg.tg .pt{fill:#1B2430}svg.tg .pt.cc{fill:#C0392B}svg.tg .cell{fill:#fff;stroke:#9AA6B2;stroke-width:1}svg.tg .cell.on{fill:#2E7D57}svg.tg.sy .sp.ob{fill:#E8F3EC}
.gfig{float:right;width:50mm;margin:0 0 1mm 3mm}.fm4{display:grid;grid-template-columns:1fr 1fr;gap:1.5mm}.fm4 div{border:1.5px solid var(--line);border-radius:8px;padding:2px 6px;font-size:9pt}.fm4 b{display:block}"""

sheet = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Transformations and symmetry: rules and practice | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{SHEET_STYLE}
{FIGCSS}
</style></head><body>
<div class="page tight">
  <div class="band"><div><div class="k">Junior Cycle Maths · Free revision sheet</div><h1>Transformations &amp; symmetry</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2018 specification): {LO}. Play the game: <b>leim.ie/mirror-move.html</b></p>
  <div class="two">
   <div><h2>1. The four transformations</h2>
    <div class="gfig" style="width:44mm">{FIG["ruleAll"]}</div>
    <p>The new shape is the <b>image</b> (S′, "S dash"). All four keep the <b>same shape and size</b>. In the picture:</p>
    <p><b>Translation</b> (slide), S → T: every point moves 6 left and 2 up. Not turned, not flipped.</p>
    <p><b>Axial symmetry</b> (mirror), S → A: in the x-axis. Same distance from the line on the other side; the shape is <b>flipped</b>.</p>
    <p style="clear:both"><b>Central symmetry</b> (half turn), S → C: in (0, 0). Go to the centre, then the same again. Same as a <b>rotation of 180°</b>.</p>
    <p><b>Rotation</b> (turn), S → R: 90° anticlockwise about (0, 0). Trace it and turn the page a quarter turn.</p>
    <h2>2. The quick rules</h2>
    <div class="fm4"><div><b>In the x-axis</b>(x, y) → (x, −y)</div><div><b>In the y-axis</b>(x, y) → (−x, y)</div><div><b>In the origin</b>(x, y) → (−x, −y)</div><div><b>Translation</b>add the move to x and y</div><div><b>90° anticlockwise about (0, 0)</b>(x, y) → (−y, x)</div><div><b>90° clockwise about (0, 0)</b>(x, y) → (y, −x)</div></div></div>
   <div><h2>3. Other lines and centres</h2>
    <p><b>A line m:</b> count the squares straight across to the line (at right angles), then the same number on the other side. A point ON the line is its own image.</p>
    <p><b>A centre C:</b> P(1, 4), C(2, 1): 1 right and 3 down to C, then 1 right and 3 down again → (3, −2).</p>
    <p><b>A translation from two points:</b> (2, 1) → (5, −3) is 3 right and 4 down. Do the same to every point. Backwards (which point maps onto…?): do the opposite move.</p>
    <h2>4. Symmetry in shapes</h2>
    <p>An <b>axis of symmetry</b> folds a shape exactly onto itself. A <b>centre of symmetry</b> is a point where a half turn fits it back on itself.</p>
    <table><tbody><tr><td>Square</td><td>4 axes · centre</td></tr><tr><td>Rectangle, rhombus</td><td>2 axes · centre</td></tr>
     <tr><td>Parallelogram</td><td>0 axes · centre</td></tr><tr><td>Kite, isosceles trapezium</td><td>1 axis · no centre</td></tr>
     <tr><td>Isosceles / equilateral triangle</td><td>1 / 3 axes · no centre</td></tr><tr><td>Regular polygon, n sides</td><td>n axes · centre if n is even</td></tr></tbody></table>
    <p style="margin-top:3px">A rectangle's diagonals are <b>not</b> axes of symmetry (fold one and see).</p>
    <div class="note"><b>Classic mistakes:</b> changing the wrong sign · clockwise v anticlockwise · thinking a half turn flips the shape · translating backwards · counting to m along the grid instead of straight across · "4 axes" for a rectangle.</div></div>
  </div>
  <div class="tip"><b>Exam tip:</b> name a transformation fully ("axial symmetry in the y-axis", "a rotation of 90° clockwise about (0, 0)"), move the corners one at a time, label the image, and use a ruler.</div>
</div>

<div class="page p2">
  <div class="band"><div><div class="k">Practice · 34 questions</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Axial symmetry</h2>
  <div class="gfig" style="width:46mm">{FIG["pA"]}</div>
  <ol class="q">{qs(A)}</ol>
  <h2 style="clear:both">B. Translations and central symmetry</h2><ol class="q" start="9">{qs(B)}</ol>
  <h2>C. Rotations</h2><ol class="q" start="17">{qs(Cq)}</ol>
  <h2>D. Naming and symmetry</h2>
  <div class="gfig" style="width:42mm">{FIG["pD"]}<div style="height:2mm"></div>{FIG["pE"]}</div>
  <ol class="q" start="23">{qs(D)}</ol>
  <p class="small" style="margin-top:4px;clear:both">Questions 31–34 are on the next page.</p>
</div>

<div class="page">
  <div class="band"><div><div class="k">Exam-style · then check</div><h1>Exam corner + answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>E. Exam-style questions (show your work)</h2>
  <ol class="q e3" start="31">{"".join(f"<li>{q}<span class='long'></span><span class='long'></span></li>" for q,a in E)}</ol>
  <h2 style="margin-top:10px">Answers</h2>
  <table class="ans"><tbody>
   <tr><td><b>A</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(A,1))}</td></tr>
   <tr><td><b>B</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(B,9))}</td></tr>
   <tr><td><b>C</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(Cq,17))}</td></tr>
   <tr><td><b>D</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(D,23))}</td></tr>
   <tr><td><b>E</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(E,31))}</td></tr>
  </tbody></table>
  <div class="note"><b>Got one wrong?</b> Check: did you change the right sign? Clockwise or anticlockwise? Did you count to the line m straight across? Then play <b>Mirror Move</b> at leim.ie/mirror-move.html: the "Go back over these" list at the end shows the rule for each mistake.</div>
  <p class="small">All questions written by Léim. Léim is independent and not connected with the State Examinations Commission or the NCCA.</p>
</div>
</body></html>"""

# ---------- teacher pack ----------
# Grid Swap: each fact is on exactly ONE card; both students work out every blank
GK = {"P": (2, 1), "Q": (5, 1), "R": (3, 4)}
g1 = [sy(GK[k]) for k in "PQR"]; g2 = [acw(GK[k]) for k in "PQR"]
gC, gM, gV = (1, -1), (-2, 3), (4, -3)
g3 = so(gM, gC); g4 = tr(gM, gV); g5 = (-gV[0], -gV[1])
assert (cl(g1), cl(g2), c(g3), c(g4), c(g5)) == ("(−2, 1), (−5, 1), (−3, 4)", "(−1, 2), (−1, 5), (−4, 3)", "(4, −5)", "(2, 0)", "(−4, 3)")
TRW = [("Corner P of triangle K", c(GK["P"]), "A"), ("Corner Q", c(GK["Q"]), "B"), ("Corner R", c(GK["R"]), "A"),
       ("Move 1", "axial symmetry in the y-axis", "B"), ("Move 2", "90° anticlockwise about (0, 0)", "A"),
       ("K after move 1", "", None), ("K after move 2 (start from K again)", "", None)]
TRC = [("Centre C", c(gC), "B"), ("Point M", c(gM), "A"), ("The translation maps (0, 0) onto", c(gV), "B"),
       ("M under central symmetry in C", "", None), ("M under the translation", "", None), ("The point whose image is (0, 0)", "", None)]
for rows in (TRW, TRC):
    assert any(w == "A" for *_, w in rows) and any(w == "B" for *_, w in rows)
def swap_card(who):
    def tab(title, rows):
        return f'<table class="ss"><thead><tr><th colspan="2">{title}</th></tr></thead><tbody>' + "".join(
            f"<tr><td>{k}</td><td><b>{v if w == who else ''}</b></td></tr>" for k, v, w in rows) + "</tbody></table>"
    return f'<div class="idc"><h3>Student {who} · Grid Swap</h3><div class="two">{tab("Moving triangle K", TRW)}{tab("A centre and a slide", TRC)}</div></div>'

MATCH = [("(4, 1) in the x-axis", c(sx((4, 1)))), ("(−3, 2) in the y-axis", c(sy((-3, 2)))), ("(5, −2) in the origin", c(so((5, -2)))),
         ("(1, 6): 90° anticlockwise about (0, 0)", c(acw((1, 6)))), ("(2, 3): 90° clockwise about (0, 0)", c(cw((2, 3)))),
         ("(−4, −1): 3 right and 5 up", c(tr((-4, -1), (3, 5)))), ("(0, 4): central symmetry in (1, 1)", c(so((0, 4), (1, 1)))),
         ("(0, 3): same move as (2, 1) → (6, 0)", c(tr((0, 3), (4, -1)))),
         ("Axes of symmetry of a rectangle", "2 axes"), ("Axes of symmetry of a regular hexagon", "6 axes"),
         ("Axes of symmetry of an equilateral triangle", "3 axes"), ("A half turn about a point is called…", "central symmetry")]
ANS = [a for q, a in MATCH]
assert ANS == ["(4, −1)", "(3, 2)", "(−5, 2)", "(−6, 1)", "(3, −2)", "(−1, 4)", "(2, −2)", "(4, 2)", "2 axes", "6 axes", "3 axes", "central symmetry"], ANS
assert len(set(ANS)) == 12
cards = [q for q, a in MATCH] + ANS
random.seed(23); match_print = cards[:]; random.shuffle(match_print)
match_html = "".join(f'<div class="c"><span class="tag">Card {i}</span><div class="fc{" sm" if len(x) > 10 else ""}">{x}</div></div>' for i, x in enumerate(match_print, 1))
match_key = " · ".join(f"{match_print.index(q) + 1} → {match_print.index(a) + 1}" for q, a in MATCH)

DOMS = [("(3, 4) in the x-axis", c(sx((3, 4)))), ("(3, 4) in the y-axis", c(sy((3, 4)))), ("(3, 4) in the origin", c(so((3, 4)))),
        ("(3, 4): 90° anticlockwise about (0, 0)", c(acw((3, 4)))), ("(3, 4): 90° clockwise about (0, 0)", c(cw((3, 4)))),
        ("(3, 4): 2 left and 5 down", c(tr((3, 4), (-2, -5)))), ("(−2, 5) in the x-axis", c(sx((-2, 5)))), ("(6, −1) in the y-axis", c(sy((6, -1)))),
        ("(0, 7) in the origin", c(so((0, 7)))), ("(5, 0): 90° anticlockwise about (0, 0)", c(acw((5, 0)))),
        ("(−1, 2): central symmetry in (2, 2)", c(so((-1, 2), (2, 2)))), ("(1, 1) → (4, 3) is a translation. Image of (0, 0)?", c(tr((0, 0), (3, 2)))),
        ("Axes of symmetry: square", "4"), ("Axes of symmetry: kite", "1"), ("Axes of symmetry: regular pentagon", "5"),
        ("Axes of symmetry: parallelogram", "0"), ("Axes of symmetry: regular octagon", "8"), ("Axes of symmetry: rhombus", "2"),
        ("A half turn is a rotation of…", "180°"), ("A quarter turn is a rotation of…", "90°")]
DANS = [a for k, a in DOMS]
assert DANS == ["(3, −4)", "(−3, 4)", "(−3, −4)", "(−4, 3)", "(4, −3)", "(1, −1)", "(−2, −5)", "(−6, −1)", "(0, −7)", "(0, 5)", "(5, 2)", "(3, 2)",
                "4", "1", "5", "0", "8", "2", "180°", "90°"], DANS
assert len(set(DANS)) == 20
for nm, k in [("square", "4"), ("kite", "1"), ("regular pentagon", "5"), ("parallelogram", "0"), ("regular octagon", "8"), ("rhombus", "2")]: assert _ns["AXES"][nm] == int(k)
random.seed(2323); chain = DOMS[:]; random.shuffle(chain)
dom = [("START" if k == 0 else chain[k - 1][1], x[0]) for k, x in enumerate(chain)] + [(chain[-1][1], "FINISH")]
dom_print = dom[:]; random.shuffle(dom_print)
dom_html = "".join(f'<div class="dom"><div class="h l{" sm" if len(l) > 9 else ""}">{l}</div><div class="h r">{r}</div></div>' for l, r in dom_print)
chain_key = "".join(f"<li>{x} = <b>{a}</b></li>" for x, a in chain)

ERR = [("Image of (2, 5) under axial symmetry in the x-axis?", "(−2, 5)", f"Changed the wrong sign. The x-axis keeps x: <b>{c(sx((2, 5)))}</b>"),
       ("Image of (−3, 1) under central symmetry in the origin?", "(3, 1)", f"Change BOTH signs: <b>{c(so((-3, 1)))}</b>"),
       ("Image of (4, 2) under 90° clockwise about (0, 0)?", "(−2, 4)", f"That's anticlockwise. Clockwise: <b>{c(cw((4, 2)))}</b>"),
       ("A translation maps (1, 1) onto (3, 4). Image of (5, 0)?", "(3, −3)", f"Moved the wrong way (2 left, 3 down). 2 right and 3 up: <b>{c(tr((5, 0), (2, 3)))}</b>"),
       ("How many axes of symmetry does a rectangle have?", "4", "The diagonals are not axes (fold and see): <b>2</b>"),
       ("Image of (5, 3) under central symmetry in C(2, 1)?", "(−5, −3)", f"Used the origin, not C. 3 left and 2 down to C, then again: <b>{c(so((5, 3), (2, 1)))}</b>")]
assert (c(sx((2, 5))), c(so((-3, 1))), c(cw((4, 2))), c(tr((5, 0), (2, 3))), c(so((5, 3), (2, 1)))) == ("(2, −5)", "(3, −1)", "(2, −4)", "(7, 3)", "(−1, −1)")
assert c(acw((4, 2))) == "(−2, 4)"
WT = [(1, 2), (4, 2), (1, 4)]
w1a = [sy(p) for p in WT]; w1b = [so(p) for p in WT]; w1d = [tr(p, (-4, -2)) for p in WT]
assert sorted(sx(p) for p in w1a) == sorted(w1b)    # T′ → T″ is axial symmetry in the x-axis
w2 = [acw((5, 2)), so((5, 2)), cw((5, 2))]; assert w2 == [(-2, 5), (-5, -2), (2, -5)]
w5a = so((-1, 3), (3, 1)); w5v = (4, -2); w5b = tr((2, 2), w5v); w5c = (-4, 2)
assert (w5a, w5b, tr(w5c, w5v)) == ((7, -1), (6, 0), (0, 0))
TAB = [("square", 4, True), ("rectangle", 2, True), ("rhombus", 2, True), ("parallelogram", 0, True), ("kite", 1, False)]
for nm, k, ce in TAB: assert _ns["AXES"][nm] == k and _ns["CENTRE"][nm] == ce

pack = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Transformations and Symmetry Teacher Pack | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{PACK_STYLE}
{FIGCSS}
.ss td:nth-child(2){{width:40%}}.ss td,.ss th{{padding:1.5px 5px;font-size:8.6pt;line-height:1.25}}.fym .c{{height:15mm}}.fym .fc{{font-size:13pt}}.fym .fc.sm{{font-size:9pt}}.p1 .proc td{{font-size:8.5pt;padding:2px 6px}}
.pf2{{display:grid;grid-template-columns:1.1fr 1fr;gap:6mm;align-items:center}}.pf2 svg{{max-height:85mm}}.dom .r{{font-size:9.8pt}}.dom .l{{font-size:12pt}}
.ttab td,.ttab th{{text-align:center;padding:4px 6px}}
</style></head><body>

<div class="page p1">
  <div class="band"><div><div class="k">Junior Cycle Maths · Teacher pack</div><h1>Transformations &amp; symmetry</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2018 specification): {LO}</p>
  <div class="two">
    <div><h3>Aims</h3><p>By the end of the lesson students can find and draw the image of points and shapes under translation, axial symmetry (in the axes and in other lines), central symmetry and rotations of 90° and 180°, name the transformation that maps one shape onto another, and find the axes and centres of symmetry of common shapes.</p></div>
    <div><h3>In this pack</h3><p>p.1 Teacher notes · p.2 Mirror Move mingle cards + Grid Swap A/B cards · p.3 Transformation Dominoes (cut-up) · p.4 Wall poster · p.5 Worksheet: Error Hunt + exam-style questions · p.6 Answers. Level: 2nd year (Higher and Ordinary), or 3rd-year revision. Time: about 60 minutes. All questions are original. Tracing paper helps.</p></div>
  </div>
  <h2 style="margin-top:8px">Procedure</h2>
  <table class="proc"><tbody>
    <tr><td>5 min</td><td><b>Lead-in: human transformations.</b> One student stands at the front facing the class. "Slide two steps left." "Turn a quarter turn clockwise." "Become your mirror image in the door frame" (which hand is raised now?). Elicit the words slide / flip / turn and what stays the same (size and shape).</td></tr>
    <tr><td>8 min</td><td><b>Guided discovery.</b> Pairs plot A(3, 2) and find its image in the x-axis, the y-axis and the origin by counting squares, then repeat with (−4, 1) and (2, −5). "What happens to the numbers each time?" Build the three rules. Then turn (3, 2) a quarter turn anticlockwise about (0, 0) with tracing paper: (−2, 3). Can they spot the pattern?</td></tr>
    <tr><td>10 min</td><td><b>Mirror Move mingle</b> (p.2, 24 cards = 12 question/answer pairs; one card each). Question card? Work it out and find the person with your answer. Answer card? Find your question. Pairs check each other's working on mini-whiteboards.</td></tr>
    <tr><td>12 min</td><td><b>Grid Swap</b> (p.2, pairs, don't show your card). Each fact is on only ONE card. Ask your partner for what you're missing ("Where is corner Q?"), plot it, then both fill every blank. Feedback: K after move 1 {cl(g1)}; after move 2 {cl(g2)}; M → {c(g3)}, {c(g4)}; the point {c(g5)}.</td></tr>
    <tr><td>10 min</td><td><b>Transformation Dominoes</b> (p.3), groups of 3–4. Start with START, work out the clue, find the domino with that answer on its left, and build the chain to FINISH.</td></tr>
    <tr><td>12 min</td><td><b>Worksheet</b> (p.5). Error Hunt in pairs (find the mistake, name the rule, fix it), then the exam-style questions alone.</td></tr>
    <tr><td>3 min</td><td><b>Exit ticket.</b> The image of (−2, 5) in the y-axis? Under central symmetry in (0, 0)? ((2, 5); (2, −5).) Homework: play <b>Mirror Move</b> at leim.ie/mirror-move.html and copy three lines from the "Go back over these" list.</td></tr>
  </tbody></table>
  <div class="note"><b>Mingle key</b> (question card → answer card): {match_key}.<br>
  <b>Errors to look for:</b> changing the wrong sign · mixing clockwise and anticlockwise · thinking central symmetry flips the shape · translating backwards · counting to a line m along the grid · 4 axes for a rectangle. <b>Support:</b> tracing paper and a card with the three sign rules. <b>Fast finishers:</b> which capital letters have exactly one axis of symmetry? Which have a centre of symmetry?</div>
  <p class="small"><b>Domino answer chain</b> (START → FINISH):</p>
  <ol class="small" style="columns:2;column-gap:12px;font-size:7.2pt;line-height:1.22;margin:0;padding-left:16px">{chain_key}</ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">Cut up the cards · one Grid Swap card per student</div><h1>Mirror Move + Grid Swap</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:8.8pt;margin:0"><b>Mirror Move mingle.</b> Cut out the 24 cards and give one to each student. Question card? Find the image, then find the person with your answer. Answer card? Find the question that gives your answer. (Fewer students? Take out whole pairs.)</p>
  <div class="fym">{match_html}</div>
  <p style="font-size:8.8pt;margin:3mm 0 0"><b>Grid Swap.</b> Don't show your card. Each fact is on only one of the two cards: ask your partner for what you're missing, plot the points on squared paper, then fill in every blank on both tables.</p>
  {swap_card("A")}
  {swap_card("B")}
</div>

<div class="page">
  <div class="band"><div><div class="k">Groups of 3–4 · cut along the dashed lines</div><h1>Transformation Dominoes</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.4pt">Start with START. Work out the clue on the right, then find the domino with that answer on its left. Keep going until you reach FINISH. "In the x-axis" means axial symmetry in the x-axis; "in the origin" means central symmetry in (0, 0).</p>
  <div class="doms">{dom_html}</div>
</div>

<div class="page">
  <div class="poster">
    <h1>Flip, slide, turn</h1>
    <div class="pf2"><div>{FIG["posterAll"]}</div><div style="font-size:14pt;line-height:1.45"><b>S → T</b> translation (slide)<br><b>S → A</b> axial symmetry in the x-axis (flip)<br><b>S → C</b> central symmetry in (0, 0) (half turn)<br><b>S → R</b> rotation 90° anticlockwise (quarter turn)</div></div>
    <div class="ops">
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>In the x-axis</b>(x, y) → (x, −y)</div>
      <div style="background:var(--green-soft)"><b>In the y-axis</b>(x, y) → (−x, y)</div>
      <div style="background:var(--green-soft)"><b>In the origin</b>(x, y) → (−x, −y)<br>= a rotation of 180°</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Axes of symmetry</b>square 4 · rectangle 2<br>kite 1 · parallelogram 0</div>
    </div>
    <p style="text-align:center;font-size:12pt;margin:0"><b>Same shape, same size</b>: only the position (and the way it faces) changes.</p>
    <p style="text-align:center;font-size:10pt;color:var(--muted)">Léim · leim.ie · Play Mirror Move: leim.ie/mirror-move.html</p>
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
  <div class="gfig" style="width:40mm">{FIG["wT"]}</div>
  <ol class="q">
    <li>Triangle T is shown. (a) Write the corners of T′, its image under axial symmetry in the y-axis. (b) Write the corners of T″, its image under central symmetry in the origin. (c) Which single transformation maps T′ onto T″? (d) Write the corners of the image of T under the translation that maps (1, 2) onto (−3, 0).<span class="long"></span></li>
    <li>P is (5, 2). Find its image under a rotation about (0, 0) of (a) 90° anticlockwise, (b) 180°, (c) 90° clockwise. (d) Join P and the three images in order. What shape do you get?<span class="long"></span></li>
    <li style="clear:both">The line m (a diagonal) is to be an axis of symmetry of the pattern below. How many more squares must be shaded? Shade them.<div style="width:34mm;margin:1mm 0 1mm 8mm">{FIG["wP"]}</div></li>
    <li>Copy and fill in the table for a square, a rectangle, a rhombus, a parallelogram and a kite: the number of axes of symmetry, and yes/no for a centre of symmetry.<span class="long"></span></li>
    <li>A is (−1, 3) and B is (3, 1). (a) Find the image of A under central symmetry in B. (b) The translation maps A onto B. Find the image of (2, 2). (c) Which point does this translation map onto (0, 0)?<span class="long"></span></li>
  </ol>
</div>

<div class="page an">
  <div class="band"><div><div class="k">For the teacher</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>Grid Swap</h2>
  <div class="two"><table><tbody>
   <tr><td>K after move 1 (in the y-axis)</td><td><b>{cl(g1)}</b></td></tr>
   <tr><td>K after move 2 (90° anticlockwise, from the ORIGINAL K)</td><td><b>{cl(g2)}</b></td></tr></tbody></table>
  <table><tbody>
   <tr><td>M under central symmetry in C</td><td>3 right and 4 down to C, then again: <b>{c(g3)}</b></td></tr>
   <tr><td>M under the translation</td><td>4 right and 3 down: <b>{c(g4)}</b></td></tr>
   <tr><td>The point whose image is (0, 0)</td><td>4 left and 3 up from (0, 0): <b>{c(g5)}</b></td></tr></tbody></table></div>
  <h2>A. Error Hunt</h2>
  <table><tbody>{"".join(f"<tr><td style='width:40%'><b>{q}</b> {w}</td><td>{r}</td></tr>" for q,w,r in ERR)}</tbody></table>
  <h2>B. Exam-style questions</h2>
  <ol class="q">
    <li>(a) T′: <b>{cl(w1a)}</b> (b) T″: <b>{cl(w1b)}</b> (c) <b>axial symmetry in the x-axis</b> (d) 4 left and 2 down: <b>{cl(w1d)}</b></li>
    <li>(a) <b>{c(w2[0])}</b> (b) <b>{c(w2[1])}</b> (c) <b>{c(w2[2])}</b> (d) a <b>square</b> (each quarter turn moves a corner the same distance, at right angles)</li>
    <li><b>{nP} more squares</b> (reflect each shaded square in the diagonal: (column, row) → (row, column); squares on the diagonal are their own images)</li>
    <li><table class="ttab"><thead><tr><th></th>{"".join(f"<th>{n}</th>" for n,k,ce in TAB)}</tr></thead><tbody><tr><td>Axes</td>{"".join(f"<td><b>{k}</b></td>" for n,k,ce in TAB)}</tr><tr><td>Centre</td>{"".join(f"<td><b>{'yes' if ce else 'no'}</b></td>" for n,k,ce in TAB)}</tr></tbody></table></li>
    <li>(a) 4 right and 2 down to B, then again: <b>{c(w5a)}</b> (b) 4 right and 2 down: <b>{c(w5b)}</b> (c) <b>{c(w5c)}</b></li>
  </ol>
  <h2>Marking tip</h2>
  <p>Give credit for each step, as the exam does: each correct image point, the label, and a fully named transformation each earn marks. "A reflection" without the line, or "a rotation" without the angle, direction and centre, is incomplete. For "explain" parts insist on a sentence with a reason in it.</p>
</div>
</body></html>"""

cover = """<!doctype html><html><head><meta charset="utf-8"><style>
body{margin:0;width:1200px;height:1200px;background:#1B2430;font-family:Inter,sans-serif;color:#fff;display:flex;flex-direction:column;justify-content:space-between;padding:90px;box-sizing:border-box}
.k{display:inline-block;background:#2E7D57;border-radius:99px;padding:12px 26px;font-weight:700;font-size:28px;letter-spacing:.06em;text-transform:uppercase}
h1{font-size:100px;font-weight:800;line-height:1.14;letter-spacing:-.03em;margin:40px 0 0}
h1 span{background:#F6CF5A;color:#1B2430;padding:0 14px;box-decoration-break:clone;-webkit-box-decoration-break:clone}
.sub{font-size:38px;color:#C9D1DA;margin-top:36px;line-height:1.35}
.em{font-size:50px;margin-top:30px;font-weight:800;letter-spacing:.01em;color:#F6CF5A}
.foot{display:flex;justify-content:space-between;align-items:center;font-size:34px;font-weight:700}
.price{background:#F6CF5A;color:#1B2430;border-radius:16px;padding:14px 28px}
</style></head><body>
<div><span class="k">Junior Cycle Maths · Teacher pack</span>
<h1><span>Transformations</span><br><span>&amp; Symmetry</span></h1>
<div class="sub">Mirror Move mingle · Grid Swap A/B<br>Dominoes · Poster · Worksheet + answers</div>
<div class="em">Flip · Slide · Turn</div></div>
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
    pdf("teacher-pack", os.path.join(OUT, "Transformations-and-Symmetry-Teacher-Pack-Leim.pdf"))
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--hide-scrollbars", "--window-size=1200,1200",
                    f"--screenshot={os.path.join(OUT, f'{SLUG}-cover.png')}", f"{SLUG}-cover.html"], cwd=SRC, check=True, capture_output=True)
    print("domino chain:", [(x, a) for x, a in chain])
