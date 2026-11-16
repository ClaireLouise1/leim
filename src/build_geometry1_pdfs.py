#!/usr/bin/env python3
"""Geometry 1: lines, angles & triangles (JC Maths topic 13): free sheet + teacher pack + Payhip cover.
Run from the repo root: python3 src/build_geometry1_pdfs.py OUTDIR
Writes src/lines-angles-triangles-*.html; PDFs/cover PNG go to OUTDIR (free sheet also to printables/).
Diagrams are drawn by the Angle Chase game's own render() through src/angle_figs_bridge.js (node), and every
answer is checked twice: by the arithmetic here AND by the independent angle-fact solver in src/test_angle_chase.py,
which measures the drawing and reads the facts off the picture."""
import os, sys, random, subprocess, re, json
from collections import Counter
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC)
sys.path.insert(0, SRC)
import test_angle_chase as TC
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/geo1"; os.makedirs(OUT, exist_ok=True)
SLUG = "lines-angles-triangles"
LO = "GT.3b, GT.3c"

# ---------- diagram specs (JS for the bridge) ----------
def js_str(s): return json.dumps(str(s))
def box(w, h): return f"[{w},{h}]"
def cross(r0, a, marks, bx=(230, 160)):  # marks: [(sector 0-3, label)]
    st = [r0, r0 + a, r0 + 180, r0 + 180 + a]; val = [a, 180 - a, a, 180 - a]
    ms = "".join(f"M(g,O,{st[s]},{val[s]},{js_str(l)});" for s, l in marks)
    return f"(()=>{{const g=G();L(g,pt(O,{r0},100),pt(O,{r0 + 180},100));L(g,pt(O,{r0 + a},100),pt(O,{r0 + a + 180},100));{ms}return render(g,'Two lines crossing',{box(*bx)});}})()"
def straight(r0, parts, labels, bx=(230, 150)):
    c = 0; s = f"L(g,pt(O,{r0},105),pt(O,{r0 + 180},105));"
    for i, (p, l) in enumerate(zip(parts, labels)):
        if i: s += f"L(g,O,pt(O,{r0 + c},95));"
        s += f"M(g,O,{r0 + c},{p},{js_str(l)});"; c += p
    assert c == 180
    return f"(()=>{{const g=G();{s}return render(g,'Angles on a straight line',{box(*bx)});}})()"
def point(r0, parts, labels, bx=(220, 175)):
    c = 0; s = ""
    for p, l in zip(parts, labels): s += f"L(g,O,pt(O,{r0 + c},95));M(g,O,{r0 + c},{p},{js_str(l)});"; c += p
    assert c == 360
    return f"(()=>{{const g=G();{s}return render(g,'Angles at a point',{box(*bx)});}})()"
def parf(a, marks, bx=(260, 180)):  # marks: [(vertex 0 top / 1 bottom, sector, label)]
    ms = "".join(f"M(p.g,p.V[{v}],p.st[{s}],p.val[{s}],{js_str(l)});" for v, s, l in marks)
    return f"(()=>{{const p=par({a});{ms}return render(p.g,'Two parallel lines and a transversal',{box(*bx)});}})()"
def trif(A, B, labels, ticks=(), ext=None, names=None, base=170, bx=(250, 175)):
    """labels: interior angle labels at P0, P1, P2 (None = no mark). ext: (label, which) → the base is extended past P1
    ('r') or past P0 ('l'), and the exterior angle there gets the label."""
    s = f"const P=triP({A},{B},{base}),g=G();g.tris.push(P);L(g,P[1],P[2]);L(g,P[2],P[0]);"
    if ext and ext[1] == "r": s += f"L(g,P[0],[{base + 85},0]);MB(g,P[1],[{base + 85},0],P[2],{js_str(ext[0])});"
    elif ext and ext[1] == "l": s += f"L(g,[-85,0],P[1]);MB(g,P[0],[-85,0],P[2],{js_str(ext[0])});"
    elif ext and ext[1] == "both": s += f"L(g,[-60,0],[{base + 60},0]);MB(g,P[0],[-60,0],P[2],{js_str(ext[0][0])});MB(g,P[1],[{base + 60},0],P[2],{js_str(ext[0][1])});"
    else: s += "L(g,P[0],P[1]);"
    for i, l in enumerate(labels):
        if l is not None: s += f"MB(g,P[{i}],P[{(i + 1) % 3}],P[{(i + 2) % 3}],{js_str(l)});"
    for i, j in ticks: s += f"T(g,P[{i}],P[{j}]);"
    if names:
        s += f"g.names.push({{p:pt(P[2],90,16),t:'{names[2]}'}},{{p:[-14,-10],t:'{names[0]}'}},{{p:[{base + 6},-16],t:'{names[1]}'}}" + (f",{{p:[{base + 85},-16],t:'{names[3]}'}}" if len(names) > 3 else "") + ");"
    return f"(()=>{{{s}return render(g,'Triangle',{box(*bx)});}})()"
def partri(A, B, labels, bx=(260, 180)):
    """Triangle L R T between parallel lines (L, R on the bottom line, T on the top). labels: dict with keys
    'TL' (angle at T between the top line and TL), 'TR', 'L', 'R', 'T' (apex)."""
    s = (f"const Lp=[0,0],Rp=[170,0],d=170*Math.sin({B}*Math.PI/180)/Math.sin({A + B}*Math.PI/180),Tp=pt(Lp,{A},d),h=Tp[1],g=G();g.tris.push([Lp,Rp,Tp]);"
         "L(g,[-60,0],[235,0],1);L(g,[Tp[0]-105,h],[Tp[0]+105,h],1);L(g,Lp,Tp);L(g,Rp,Tp);")
    ref = {"TL": "MB(g,Tp,[Tp[0]-100,h],Lp,{})", "TR": "MB(g,Tp,[Tp[0]+100,h],Rp,{})", "L": "MB(g,Lp,Rp,Tp,{})", "R": "MB(g,Rp,Tp,Lp,{})", "T": "MB(g,Tp,Lp,Rp,{})"}
    for k, l in labels.items(): s += ref[k].format(js_str(l)) + ";"
    return f"(()=>{{{s}return render(g,'Triangle between parallel lines',{box(*bx)});}})()"

FIGS = {}   # name -> (js, {label: expected value}, one-step kind or None)
def fig(name, js, expect, kind=None): FIGS[name] = (js, expect, kind)

# rules figures (page 1 of the sheet and the poster): no answers to check, letters only
RULES = [("straight", straight(0, [55, 125], ["a", "b"]), "Angles on a straight line add to 180°", "a + b = 180°"),
         ("point", point(20, [120, 110, 130], ["a", "b", "c"]), "Angles at a point add to 360°", "a + b + c = 360°"),
         ("vo", cross(25, 100, [(0, "a"), (2, "b")]), "Vertically opposite angles are equal (Theorem 1)", "a = b"),
         ("tri", trif(55, 70, ["a", "b", "c"]), "Angles in a triangle add to 180° (Theorem 4)", "a + b + c = 180°"),
         ("iso", trif(68, 68, ["a", "b", None], ticks=[(0, 2), (1, 2)], base=150), "Isosceles triangle: base angles are equal (Theorem 2)", "a = b"),
         ("ext", trif(55, 65, ["a", None, "b"], ext=("e", "r"), base=150), "Exterior angle = sum of the two interior opposite angles (Theorem 6)", "e = a + b"),
         ("alt", parf(62, [(0, 3, "a"), (1, 1, "b")]), "Alternate angles are equal (Theorem 3)", "a = b"),
         ("cor", parf(62, [(0, 0, "a"), (1, 0, "b")]), "Corresponding angles are equal (Theorem 5)", "a = b"),
         ("coi", parf(62, [(0, 3, "a"), (1, 0, "b")]), "Co-interior angles add to 180°", "a + b = 180°")]
for n, js, t, e in RULES: fig("rule_" + n, js, {})

# ---------- free sheet ----------
A = [("What type of angle is 35°?", "acute"), ("What type of angle is 147°?", "obtuse"), ("What type of angle is 215°?", "reflex"),
     ("A triangle has angles of 90°, 36° and 54°. Is it acute-angled, right-angled or obtuse-angled?", "right-angled"),
     ("A triangle has sides of 7 cm, 7 cm and 4 cm. Is it scalene, isosceles or equilateral?", "isosceles"),
     ("In ∠KLM, which point is the vertex?", "L")]
assert TC.classify_angle(35) == "Acute" and TC.classify_angle(147) == "Obtuse" and TC.classify_angle(215) == "Reflex" and 90 + 36 + 54 == 180
B = [  # (js, answer, reason)
    (straight(0, [128, 52], ["128", "x"]), 52, "straight line", "str"),
    (point(15, [140, 95, 125], ["140", "95", "x"]), 125, "angles at a point", "pt"),
    (cross(15, 64, [(0, "64"), (2, "x")]), 64, "vertically opposite", "vo"),
    (cross(-10, 62, [(1, "118"), (2, "x")]), 62, "straight line", "str"),
    (trif(47, 68, ["47", "68", "x"]), 65, "angles in a triangle", "tri"),
    (trif(90, 33, ["rt", "33", "x"]), 57, "angles in a triangle", "tri"),
    (trif(72, 72, ["72", "x", None], ticks=[(0, 2), (1, 2)], base=150), 72, "isosceles: base angles equal", "iso"),
    (trif(60, 60, ["x", None, None], ticks=[(0, 1), (1, 2), (2, 0)], base=150), 60, "equilateral: 180 ÷ 3", "equi"),
    (trif(58, 73, ["58", None, "49"], ext=("x", "r")), 107, "exterior angle = 58 + 49", "ext"),
    (parf(70, [(0, 0, "70"), (1, 0, "x")]), 70, "corresponding angles", "cor"),
    (parf(55, [(0, 2, "55"), (1, 0, "x")]), 55, "alternate angles", "alt"),
    (parf(65, [(0, 2, "65"), (1, 1, "x")]), 115, "co-interior angles", "coi")]
for i, (js, a, r, k) in enumerate(B, 7): fig(f"B{i}", js, {"x": a}, None if k == "equi" else k)
C = [("Could a triangle have angles of 100° and 85°? Explain.", "No: 100 + 85 = 185, more than 180°"),
     ("Two angles of a triangle are 42° and 75°. Find the third angle.", f"{180 - 42 - 75}°"),
     ("An isosceles triangle has an apex angle of 38°. Find each base angle.", f"{(180 - 38) // 2}°"),
     ("An isosceles triangle has base angles of 66°. Find the apex angle.", f"{180 - 2 * 66}°"),
     ("Three angles at a point are 150°, 85° and x. Find x.", f"{360 - 150 - 85}°"),
     ("How many degrees are in each angle of an equilateral triangle? Why?", "60°: the three equal angles share 180°")]
assert C[1][1] == "63°" and C[2][1] == "71°" and C[3][1] == "48°" and C[4][1] == "125°"
D = [  # two-step chases
    (parf(68, [(0, 0, "68"), (1, 0, "y"), (1, 2, "x")]), 68, "y = 68 (corr.), x = y (vert. opp.)"),
    (parf(122, [(1, 1, "58"), (0, 1, "y"), (0, 0, "x")]), 122, "y = 58 (corr.), x = 180 − 58 (str. line)"),
    (trif(64, 64, [None, "y", "52"], ticks=[(0, 2), (1, 2)], ext=("x", "r"), base=150), 116, "y = 128 ÷ 2 = 64 (isosceles), x = 180 − 64 (str. line)"),
    (trif(57, 71, ["y", "z", "x"], ext=(("123", "109"), "both"), base=200), 52, "y = 57, z = 71 (str. lines), x = 180 − 128 (triangle)"),
    (partri(54, 63, {"TL": "54", "L": "y", "R": "63", "T": "x"}), 63, "y = 54 (alternate), x = 180 − 117 (triangle)"),
    (trif(55, 55, ["x", None, "70"], ticks=[(0, 2), (1, 2)], base=150), 55, "(180 − 70) ÷ 2 (isosceles, triangle)")]
for i, (js, a, r) in enumerate(D, 25): fig(f"D{i}", js, {"x": a})
# E: exam-style
fig("E31", parf(74, [(0, 0, "74"), (0, 2, "a"), (1, 0, "b"), (1, 1, "c")], bx=(280, 190)), {"a": 74, "b": 74, "c": 106})
fig("E32", trif(64, 64, [None, "q", "52"], ticks=[(0, 2), (1, 2)], ext=("s", "r"), names=["Q", "R", "P", "S"], base=150, bx=(280, 190)), {"q": 64, "s": 116})
E = [("The two lines with arrows are parallel. Find the angles a, b and c, giving a reason for each.", "E31",
      "a = <b>74°</b> (vertically opposite) · b = <b>74°</b> (corresponding) · c = 180 − 74 = <b>106°</b> (straight line with b; or co-interior)"),
     ("In the triangle PQR, |PQ| = |PR| and ∠QPR = 52°. QR is extended to S. (a) Find q, the size of ∠PRQ. (b) Find s, the size of ∠PRS. Give a reason for each step.", "E32",
      "(a) q = (180 − 52) ÷ 2 = <b>64°</b> (isosceles: equal base angles; angles in a triangle add to 180°) (b) s = 180 − 64 = <b>116°</b> (straight line), or 52 + 64 = 116 (exterior angle)"),
     ("A triangle has angles of 35°, 75° and y. (a) Find y. (b) Is the triangle acute-angled, right-angled or obtuse-angled? (c) Could a triangle have angles of 95° and 90°? Explain.", None,
      "(a) y = 180 − 110 = <b>70°</b> (b) <b>acute-angled</b> (all less than 90°) (c) <b>No</b>: 95 + 90 = 185, more than 180°, before the third angle"),
     ("Explain why a triangle can never have two obtuse angles.", None,
      "Two obtuse angles are each more than 90°, so together they are more than 180°. But all <b>three</b> angles of a triangle add to exactly 180°, so it's impossible.")]
assert 180 - 35 - 75 == 70 and max(35, 75, 70) < 90

# ---------- teacher pack ----------
SORT_CAT = [("vo", "Vertically opposite", "a = b"), ("str", "On a straight line", "a + b = 180°"), ("alt", "Alternate", "a = b"),
            ("cor", "Corresponding", "a = b"), ("coi", "Co-interior", "a + b = 180°")]
# each card: (transversal angle, (vertex, sector) of a, (vertex, sector) of b)
SORT = [(58, (0, 0), (0, 2)), (115, (1, 1), (1, 3)), (72, (0, 3), (0, 1)), (130, (1, 2), (1, 0)),
        (62, (0, 0), (0, 1)), (118, (1, 2), (1, 3)), (75, (1, 1), (1, 2)), (50, (0, 3), (0, 0)),
        (64, (0, 3), (1, 1)), (120, (0, 2), (1, 0)), (55, (1, 1), (0, 3)), (128, (1, 0), (0, 2)),
        (66, (0, 1), (1, 1)), (112, (0, 3), (1, 3)), (52, (1, 2), (0, 2)), (125, (0, 0), (1, 0)),
        (60, (0, 3), (1, 0)), (124, (0, 2), (1, 1)), (70, (1, 0), (0, 3)), (110, (1, 1), (0, 2))]
SORT_KIND = ["vo"] * 4 + ["str"] * 4 + ["alt"] * 4 + ["cor"] * 4 + ["coi"] * 4
random.seed(13); order = list(range(20)); random.shuffle(order)
for n, k in enumerate(order, 1):
    a, (v1, s1), (v2, s2) = SORT[k]
    fig(f"S{n}", parf(a, [(v1, s1, "a"), (v2, s2, "b")], bx=(200, 140)), {})
    val = [a, 180 - a, a, 180 - a]
    fig(f"S{n}chk", parf(a, [(v1, s1, str(val[s1])), (v2, s2, "x")]), {"x": val[s2]}, SORT_KIND[k])
sort_key = " · ".join(f"<b>{t}:</b> " + ", ".join(str(n) for n, k in enumerate(order, 1) if SORT_KIND[k] == c) for c, t, e in SORT_CAT)

DOMS = [("x and 65° are on a straight line", "115°"), ("x and 48° are vertically opposite", "48°"), ("a triangle has angles 50°, 60° and x", "70°"),
        ("angles at a point: 100°, 120° and x", "140°"), ("x and 72° are alternate angles", "72°"), ("x and 81° are corresponding angles", "81°"),
        ("x and 106° are co-interior angles", "74°"), ("isosceles triangle with an apex of 44°: each base angle", "68°"),
        ("isosceles triangle with base angles of 25°: the apex", "130°"), ("each angle of an equilateral triangle", "60°"),
        ("exterior angle; the interior opposite angles are 35° and 50°", "85°"), ("exterior angle 120°; one interior opposite angle is 45°: the other", "75°"),
        ("a right-angled triangle has an angle of 28°: the third angle", "62°"), ("a straight line split into 30°, 55° and x", "95°"),
        ("a right angle", "90°"), ("a straight angle", "180°"), ("a full turn", "360°"), ("the reflex angle that makes a full turn with 40°", "320°"),
        ("x and 133° are vertically opposite", "133°"), ("a triangle has angles 25°, 35° and x", "120°")]
CHK = [180 - 65, 48, 180 - 110, 360 - 220, 72, 81, 180 - 106, (180 - 44) // 2, 180 - 50, 60, 85, 120 - 45, 90 - 28, 180 - 85, 90, 180, 360, 320, 133, 180 - 60]
assert [int(a[:-1]) for q, a in DOMS] == CHK and len(set(a for q, a in DOMS)) == 20
random.seed(1313); chain = DOMS[:]; random.shuffle(chain)
dom = [("START" if k == 0 else chain[k - 1][1], x[0]) for k, x in enumerate(chain)] + [(chain[-1][1], "FINISH")]
dom_print = dom[:]; random.shuffle(dom_print)
dom_html = "".join(f'<div class="dom"><div class="h l">{l}</div><div class="h r">{r}</div></div>' for l, r in dom_print)
chain_key = "".join(f"<li>{x} = <b>{a}</b></li>" for x, a in chain)
ERR = [("70° and x on a straight line", "x = 360 − 70 = 290°", "A straight line is 180°, not 360°: x = <b>110°</b>"),
       ("Triangle with angles 45°, 75° and x", "x = 45 + 75 = 120°", "Added instead of taking away: x = 180 − 120 = <b>60°</b>"),
       ("Isosceles triangle, apex 50°: find a base angle", "50° (the angles are equal)", "The two BASE angles are equal: (180 − 50) ÷ 2 = <b>65°</b>"),
       ("x and 64° are alternate angles", "x = 180 − 64 = 116°", "Alternate angles are <b>equal</b>: x = <b>64°</b> (co-interior angles add to 180°)"),
       ("Give the reason for x = 64° above", "Z angles", "Write the proper name: <b>alternate angles</b>"),
       ("Exterior angle; interior opposite angles 40° and 70°", "180 − (40 + 70) = 70°", "70° is the interior angle at that corner. The exterior angle = 40 + 70 = <b>110°</b>")]
fig("W1", parf(112, [(0, 1, "68"), (0, 0, "a"), (1, 1, "b"), (1, 3, "c")], bx=(280, 190)), {"a": 112, "b": 68, "c": 68})
fig("W2", partri(48, 70, {"TL": "48", "TR": "70", "T": "x", "L": "y"}, bx=(280, 190)), {"x": 62, "y": 48})
fig("W4", trif(38, 66, ["38", None, "w"], ext=("114", "r"), bx=(280, 190)), {"w": 76})

# ---------- draw + check every diagram ----------
res = subprocess.run(["node", os.path.join(SRC, "angle_figs_bridge.js")], input=json.dumps({k: v[0] for k, v in FIGS.items()}),
                     capture_output=True, text=True, check=True)
SVG = json.loads(res.stdout)
for name, (js, expect, kind) in FIGS.items():
    TC.probs.clear()
    q = {"mk": name, "en": "", "frame": "", "answer": "", "wrong": []}
    lines, ticks, tris, marks = TC.parse(SVG[name])
    x, direct, vals, marks = TC.solve(q, lines, ticks, tris, marks)
    got = {m["l"]: vals.get(i) for i, m in enumerate(marks) if re.fullmatch(r"[a-z]", m["l"])}
    for lab, v in expect.items():
        assert got.get(lab) == v, (name, lab, got.get(lab), v)
    if kind: assert direct == {kind}, (name, direct, kind)
    assert not TC.probs, (name, TC.probs)
print("checked", len(FIGS), "diagrams")
def S(n, cls=""): return f'<div class="fig {cls}">{SVG[n]}</div>'

CSS_COMMON = """.fig svg{width:100%;height:auto;max-height:34mm;display:block;margin:0 auto}
.gq{display:grid;grid-template-columns:repeat(4,1fr);gap:2mm 3mm}.gq>div{border:1px solid #E5E7EB;border-radius:8px;padding:1.5mm 2mm;break-inside:avoid}
.gq .n{font-weight:800;color:var(--green);font-size:9pt}.gq .ln2{display:block;border-bottom:1px solid #9AA3AE;height:12px;margin-top:1mm}
.g3{grid-template-columns:repeat(3,1fr)}
.facts{display:grid;grid-template-columns:repeat(3,1fr);gap:2mm}.facts>div{background:var(--cream);border:1px solid var(--cream-line);border-radius:8px;padding:1.5mm 2mm;font-size:8.2pt;line-height:1.25;text-align:center}
.facts .fig svg{max-height:22mm}"""

sheet = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Lines, angles and triangles: rules and practice | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>@page{{@bottom-left{{content:"Léim · leim.ie · Free to print for home or class · JC Maths LOs (2018 spec): {LO}"}}}}
.tight{{font-size:9.3pt;line-height:1.36}}.tight h2{{margin:7px 0 3px;font-size:13pt}}.tight .note,.tight .tip{{padding:5px 10px;margin:5px 0}}.tight p{{margin:3px 0}}.tight ul{{margin:3px 0;padding-left:16px}}
ol.q{{padding-left:30px}}ol.q li{{margin:6px 0}}
.p2{{font-size:9pt;line-height:1.3}}.p2 ol.q li{{margin:2.4px 0}}.p2 .line{{min-width:60px}}.p2 h2{{margin:6px 0 3px}}
.cols2{{columns:2;column-gap:8mm}}
.p3 .gq .fig svg{{max-height:25mm}}.p3 .ef{{float:right;width:46mm;margin:0 0 1mm 3mm}}.p3 .ef svg{{max-height:27mm}}.p3 ol.q li::after{{content:"";display:block;clear:both}}.p3 .ans td{{font-size:8.1pt;padding:2px 5px}}
.ans td{{padding:3px 6px;font-size:8.5pt}}
{CSS_COMMON}
</style></head><body>
<div class="page tight">
  <div class="band"><div><div class="k">Junior Cycle Maths · Free revision sheet</div><h1>Lines, angles &amp; triangles</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2018 specification): {LO}. Play the game: <b>leim.ie/angle-chase.html</b></p>
  <div class="two">
   <div><h2>1. Angle words</h2>
    <p><b>Acute</b> &lt; 90° · <b>right angle</b> = 90° (little square) · <b>obtuse</b> between 90° and 180° · <b>straight angle</b> = 180° · <b>reflex</b> between 180° and 360°.</p>
    <p>∠ABC is the angle at <b>B</b>: the middle letter is the <b>vertex</b>.</p>
    <p><b>Parallel</b> lines never meet (arrows) · <b>perpendicular</b> lines meet at 90° · a <b>transversal</b> cuts across other lines · a <b>line segment</b> has two end points; a <b>ray</b> goes on forever one way.</p></div>
   <div><h2>2. Triangles</h2>
    <p><b>By sides:</b> scalene (all different) · isosceles (two equal, marked with dashes) · equilateral (all equal, every angle 60°).</p>
    <p><b>By angles</b> (look at the biggest): acute-angled (all &lt; 90°) · right-angled (one = 90°) · obtuse-angled (one &gt; 90°).</p></div>
  </div>
  <h2>3. The angle facts (learn the names: they are your reasons)</h2>
  <div class="facts">{"".join(f'<div>{S("rule_" + n)}<b>{t}</b><br>{e}</div>' for n, js, t, e in RULES)}</div>
  <h2>4. How to chase an angle</h2>
  <p>Mark what you know. Find a fact that joins a known angle to an unknown one. Write each step on its own line <b>with the reason</b>: <i>y = 180° − 72° = 108° (straight line)</i>. Keep going until you reach the angle you want. Check that each triangle adds to 180°.</p>
  <div class="tip"><b>Exam tip:</b> the reason earns marks. Write <b>alternate</b> and <b>corresponding</b>, never "Z" or "F". Exam diagrams usually aren't drawn to scale, so don't measure: use the facts.</div>
</div>

<div class="page p2">
  <div class="band"><div><div class="k">Practice · 34 questions</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Angle words</h2><ol class="q cols2">{"".join(f"<li>{q} <span class='line'></span></li>" for q, a in A)}</ol>
  <h2>B. Find x and give the reason</h2>
  <div class="gq">{"".join(f'<div><span class="n">{i}.</span>{S(f"B{i}")}<span class="ln2"></span></div>' for i in range(7, 19))}</div>
  <h2>C. Triangles and angles</h2><ol class="q" start="19">{"".join(f"<li>{q} <span class='line'></span></li>" for q, a in C)}</ol>
  <p class="small" style="margin-top:3px">Questions 25–34 are on the next page.</p>
</div>

<div class="page p2 p3">
  <div class="band"><div><div class="k">Two-step chases · exam-style · answers</div><h1>Chase it, then check</h1></div><div class="logo">↗ Léim</div></div>
  <h2>D. Two-step chases: find y (and z) first, then x. Give a reason for each step.</h2>
  <div class="gq g3">{"".join(f'<div><span class="n">{i}.</span>{S(f"D{i}")}<span class="ln2"></span></div>' for i in range(25, 31))}</div>
  <h2>E. Exam-style questions (show your work)</h2>
  <ol class="q" start="31">{"".join(f"<li>" + (S(f, "ef") if f else "") + q + "</li>" for q, f, a in E)}</ol>
  <h2 style="margin-top:6px">Answers</h2>
  <table class="ans"><tbody>
   <tr><td><b>A</b></td><td>{" · ".join(f"{i}. {a}" for i, (q, a) in enumerate(A, 1))}</td></tr>
   <tr><td><b>B</b></td><td>{" · ".join(f"{i}. {a}° ({r})" for i, (js, a, r, k) in enumerate(B, 7))}</td></tr>
   <tr><td><b>C</b></td><td>{" · ".join(f"{i}. {a}" for i, (q, a) in enumerate(C, 19))}</td></tr>
   <tr><td><b>D</b></td><td>{" · ".join(f"{i}. {a}°: {r}" for i, (js, a, r) in enumerate(D, 25))}</td></tr>
   <tr><td><b>E</b></td><td>{" · ".join(f"{i}. {a}" for i, (q, f, a) in enumerate(E, 31))}</td></tr>
  </tbody></table>
  <p class="small">All questions written by Léim. Léim is independent and not connected with the State Examinations Commission or the NCCA.</p>
</div>
</body></html>"""

pack = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Lines, Angles &amp; Triangles Teacher Pack | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>
@page{{@bottom-left{{content:"Léim · leim.ie · Single-teacher licence · JC Maths LOs (2018 spec): {LO}";font-size:7pt}}}}
.proc td{{font-size:8.8pt;padding:3px 6px;line-height:1.3}}.proc td:first-child{{white-space:nowrap;font-weight:700;color:var(--green)}}
.p1 .note{{font-size:8.4pt;padding:6px 10px;line-height:1.35}}.p1 p{{font-size:9.3pt}}
.sortc{{display:grid;grid-template-columns:repeat(4,1fr)}}
.sortc .c{{border:2px dashed #9AA3AE;margin:-1px 0 0 -1px;height:39mm;position:relative;padding:5mm 2mm 1mm;display:flex;align-items:center}}
.sortc .c .fig{{width:100%}}.sortc .c svg{{max-height:31mm}}
.sortc .tag{{position:absolute;top:1.2mm;left:3mm;font-size:6.5pt;color:var(--green);font-weight:800;text-transform:uppercase;letter-spacing:.04em}}
.hdr{{display:grid;grid-template-columns:repeat(5,1fr);gap:2mm;margin-top:2mm}}.hdr div{{border:2px dashed #9AA3AE;text-align:center;padding:2mm;font-weight:800;font-size:9.5pt;background:var(--green-soft)}}
.doms{{display:grid;grid-template-columns:1fr 1fr;gap:2mm 6mm}}
.dom{{display:grid;grid-template-columns:1fr 2.2fr;border:2px dashed #9AA3AE;height:18.5mm}}
.dom .h{{display:flex;align-items:center;justify-content:center;text-align:center;padding:2mm;font-size:13pt;font-weight:800}}
.dom .r{{font-size:10pt}}.dom .l{{background:var(--mist);border-right:2px solid var(--ink)}}
.poster{{height:255mm;border:6px solid var(--night);border-radius:18px;padding:8mm;display:flex;flex-direction:column;justify-content:space-between}}
.poster h1{{font-size:38pt;text-align:center;margin:0}}.poster p{{font-size:13pt!important}}
.pf{{display:grid;grid-template-columns:repeat(3,1fr);gap:3mm}}.pf>div{{background:var(--cream);border:2px solid var(--cream-line);border-radius:12px;padding:2mm;text-align:center;font-size:10.5pt;line-height:1.25}}
.pf .fig svg{{max-height:40mm}}
.ws{{font-size:9.6pt;line-height:1.38}}.ws ol.q li{{margin:5px 0;min-height:34mm}}.ws ol.q li::after{{content:"";display:block;clear:both}}.ws .long{{height:18px}}.ws .ef{{float:right;width:62mm;margin:0 0 1mm 4mm}}.ws .ef svg{{max-height:33mm}}
.eh td{{padding:4px 7px;font-size:9.2pt}}.eh td:first-child{{font-weight:700;width:28%}}.eh .gap{{display:block;border-bottom:1px solid #9AA3AE;height:14px}}
.a6{{font-size:9.1pt;line-height:1.35}}.a6 td{{font-size:8.7pt;padding:3px 6px}}.a6 h2{{margin:7px 0 3px}}.a6 ol.q li{{margin:3px 0}}
{CSS_COMMON}
</style></head><body>

<div class="page p1">
  <div class="band"><div><div class="k">Junior Cycle Maths · Teacher pack</div><h1>Lines, angles &amp; triangles</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2018 specification): {LO} (constructions are taught next; congruent and similar triangles and the other theorems come in Geometry 2)</p>
  <div class="two">
    <div><h3>Aims</h3><p>By the end of the lesson students can name and classify angles and triangles, use the angle facts (straight line, point, vertically opposite, triangle, isosceles, exterior angle, alternate, corresponding, co-interior) to find missing angles, and give the correct <b>reason</b> for every step, as the exam asks.</p></div>
    <div><h3>In this pack</h3><p>p.1 Teacher notes · p.2 Angle Sort cards · p.3 Angle Dominoes (cut-up) · p.4 Wall poster · p.5 Worksheet: Error Hunt + exam-style questions · p.6 Answers. Level: 1st year (Higher and Ordinary), or 3rd-year revision. Time: about 60 minutes. All questions are original.</p></div>
  </div>
  <h2 style="margin-top:8px">Procedure</h2>
  <table class="proc"><tbody>
    <tr><td>8 min</td><td><b>Lead-in: Torn corners.</b> Each student draws any triangle, colours the corners, tears them off and lines them up. "What shape do they make? Did it matter which triangle?" Elicit: the angles of every triangle add to <b>180°</b> (Theorem 4).</td></tr>
    <tr><td>8 min</td><td><b>Guided discovery: parallel lines.</b> Students draw a transversal across two lines of their lined copy and measure all eight angles. "Which angles are equal? Which pairs add to 180°?" Name them: vertically opposite, alternate, corresponding, co-interior.</td></tr>
    <tr><td>12 min</td><td><b>Angle Sort</b> (p.2, groups of 3–4). Cut out the five headers and 20 cards. Groups sort each card by the pair of angles marked a and b, and must say whether a = b or a + b = 180°. Check against the key.</td></tr>
    <tr><td>10 min</td><td><b>Angle Dominoes</b> (p.3). Start at START, work out the clue, find the domino with that answer on its left, build the chain to FINISH. Chain below.</td></tr>
    <tr><td>17 min</td><td><b>Worksheet</b> (p.5). Error Hunt in pairs, then the exam-style questions alone, writing a reason for every step. Fast finishers: invent a two-step chase for a partner.</td></tr>
    <tr><td>5 min</td><td><b>Exit ticket.</b> Draw two parallel lines and a transversal; mark one angle 70°. "Mark an angle equal to it and name the reason. Mark an angle of 110° and name the reason." Homework: play <b>Angle Chase</b> at leim.ie/angle-chase.html (Name the reason round).</td></tr>
  </tbody></table>
  <div class="note"><b>Angle Sort key:</b> {sort_key}.<br>
  <b>Errors to look for:</b> 360° used for a straight line · adding the two given angles instead of subtracting from 180° · "the angles are equal" in an isosceles triangle without saying which ones · alternate and co-interior mixed up · "Z angles" / "F angles" written as reasons · measuring a diagram that isn't drawn to scale.</div>
  <p class="small"><b>Domino answer chain</b> (START → FINISH):</p>
  <ol class="small" style="columns:2;column-gap:12px;font-size:7.6pt;line-height:1.32;margin:0;padding-left:16px">{chain_key}</ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">Cut up the cards · groups of 3–4</div><h1>Angle Sort</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.2pt;margin:0">Cut out the five headers and the 20 cards. The arrows show parallel lines. Sort each card by the pair of angles <b>a</b> and <b>b</b>, and say whether a = b or a + b = 180°.</p>
  <div class="hdr">{"".join(f"<div>{t}<br><span style='font-weight:600'>{e}</span></div>" for c, t, e in SORT_CAT)}</div>
  <div class="sortc" style="margin-top:2mm">{"".join(f'<div class="c"><span class="tag">Card {n}</span>{S(f"S{n}")}</div>' for n in range(1, 21))}</div>
</div>

<div class="page">
  <div class="band"><div><div class="k">Groups of 3–4 · cut along the dashed lines</div><h1>Angle Dominoes</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.5pt">Start with START. Work out the clue on the right, then find the domino with that answer on its left. Keep going until you reach FINISH.</p>
  <div class="doms">{dom_html}</div>
</div>

<div class="page">
  <div class="poster">
    <h1>Angle facts</h1>
    <p style="text-align:center;font-size:15pt!important;margin:0;font-weight:800">Every step needs a reason!</p>
    <div class="pf">{"".join(f'<div>{S("rule_" + n)}<b>{t}</b><br>{e}</div>' for n, js, t, e in RULES)}</div>
    <p style="text-align:center;margin:0">Say <b>alternate</b> and <b>corresponding</b>, not "Z" and "F" · Exam diagrams aren't to scale: don't measure!</p>
    <p style="text-align:center;font-size:10pt;color:var(--muted)">Léim · leim.ie · Play Angle Chase: leim.ie/angle-chase.html</p>
  </div>
</div>

<div class="page ws">
  <div class="band"><div><div class="k">Worksheet</div><h1>Error Hunt + exam-style questions</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Error Hunt</h2>
  <p>Each answer has one mistake. Find it, say what's wrong, and write the right answer.</p>
  <table class="eh"><thead><tr><th>Question</th><th>Student's answer</th><th>The mistake and the right answer</th></tr></thead><tbody>
  {"".join(f"<tr><td>{q}</td><td>{w}</td><td><span class='gap'></span><span class='gap'></span></td></tr>" for q, w, r in ERR)}
  </tbody></table>
  <h2>B. Exam-style questions (give a reason for every step)</h2>
  <ol class="q">
    <li>The lines with arrows are parallel. Find a, b and c.{S("W1", "ef")}<span class="long"></span></li>
    <li>The lines with arrows are parallel. Find x and y.{S("W2", "ef")}<span class="long"></span></li>
    <li style="min-height:0">Can a triangle have two right angles? Use an angle fact to explain.<span class="long"></span><span class="long"></span></li>
    <li>The base of the triangle is extended. Find w in two different ways.{S("W4", "ef")}<span class="long"></span></li>
  </ol>
</div>

<div class="page a6">
  <div class="band"><div><div class="k">For the teacher</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>Angle Sort</h2>
  <p>{sort_key}. Vertically opposite, alternate and corresponding: <b>a = b</b>. On a straight line and co-interior: <b>a + b = 180°</b>.</p>
  <h2>A. Error Hunt</h2>
  <table><tbody>{"".join(f"<tr><td style='width:34%'><b>{q}</b> → {w}</td><td>{r}</td></tr>" for q, w, r in ERR)}</tbody></table>
  <h2>B. Exam-style questions</h2>
  <ol class="q">
    <li>a = 180 − 68 = <b>112°</b> (straight line) · b = <b>68°</b> (corresponding) · c = <b>68°</b> (vertically opposite to b)</li>
    <li>x = 180 − (48 + 70) = <b>62°</b> (angles on a straight line, at the top) · y = <b>48°</b> (alternate angles). Check: the angle at the bottom right is 70° (alternate), and 48 + 70 + 62 = 180 (angles in a triangle) ✓</li>
    <li><b>No.</b> Two right angles make 90 + 90 = 180°, which leaves 0° for the third angle, but the three angles of a triangle add to exactly 180°.</li>
    <li>w = 114 − 38 = <b>76°</b> (exterior angle = sum of the two interior opposite angles). Or: the inside angle next to the 114° is 180 − 114 = 66° (straight line), then w = 180 − (38 + 66) = <b>76°</b> (angles in a triangle) ✓</li>
  </ol>
  <h2>Marking tip</h2>
  <p>As in the exam, a correct angle with no reason (or "Z angles") should not get full marks when a reason is asked for. Accept any correct chain of facts, e.g. "co-interior" instead of "corresponding then straight line". Give follow-through marks for later steps done correctly from an earlier slip.</p>
</div>
</body></html>"""

cover = """<!doctype html><html><head><meta charset="utf-8"><style>
body{margin:0;width:1200px;height:1200px;background:#1B2430;font-family:Inter,sans-serif;color:#fff;display:flex;flex-direction:column;justify-content:space-between;padding:90px;box-sizing:border-box}
.k{display:inline-block;background:#2E7D57;border-radius:99px;padding:12px 26px;font-weight:700;font-size:28px;letter-spacing:.06em;text-transform:uppercase}
h1{font-size:100px;font-weight:800;line-height:1.1;letter-spacing:-.03em;margin:40px 0 0}
h1 span{background:#F6CF5A;color:#1B2430;padding:0 14px}
.sub{font-size:38px;color:#C9D1DA;margin-top:36px;line-height:1.35}
.em{font-size:46px;margin-top:30px;font-weight:800;letter-spacing:.01em;color:#F6CF5A}
.foot{display:flex;justify-content:space-between;align-items:center;font-size:34px;font-weight:700}
.price{background:#F6CF5A;color:#1B2430;border-radius:16px;padding:14px 28px}
</style></head><body>
<div><span class="k">Junior Cycle Maths · Teacher pack</span>
<h1><span>Lines, Angles</span><br><span>&amp; Triangles</span></h1>
<div class="sub">Angle Sort cards · Angle Dominoes<br>Poster · Worksheet + answers</div>
<div class="em">Find the angle · give the reason</div></div>
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
    pdf("teacher-pack", os.path.join(OUT, "Lines-Angles-Triangles-Teacher-Pack-Leim.pdf"))
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--hide-scrollbars", "--window-size=1200,1200",
                    f"--screenshot={os.path.join(OUT, f'{SLUG}-cover.png')}", f"{SLUG}-cover.html"], cwd=SRC, check=True, capture_output=True)
