#!/usr/bin/env python3
"""Constructions (JC Maths topic 14): free sheet + teacher pack + Payhip cover.
Run from the repo root: python3 src/build_constructions_pdfs.py OUTDIR
Writes src/constructions-*.html; PDFs/cover PNG go to OUTDIR (free sheet also to printables/).
Diagrams are drawn by the Construction Steps game's own builders through src/construction_figs_bridge.js (node), and every
finished construction is re-checked by the independent geometry validators in src/test_construction_steps.py
(exactly one of the 15 validators must pass, and it must be the construction we say it is)."""
import os, sys, random, subprocess, re, json, math
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC)
sys.path.insert(0, SRC)
import test_construction_steps as TC
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/cons"; os.makedirs(OUT, exist_ok=True)
SLUG = "constructions"
LO = "GT.3a"
NAMES = TC.MYNAMES
SHORT = {1: "Bisector of an angle", 2: "Perpendicular bisector of a segment", 3: "Perpendicular from a point not on l (HL)", 4: "Perpendicular at a point on l",
         5: "Parallel line through a point", 6: "2 or 3 equal parts", 7: "Any number of equal parts (HL)", 8: "Segment of a given length on a ray",
         9: "Angle of a given size on a ray", 10: "Triangle: SSS", 11: "Triangle: SAS", 12: "Triangle: ASA", 13: "Right-angled: hypotenuse + side (RHS)",
         14: "Right-angled: side + acute angle", 15: "Rectangle"}
KEY = {1: "Arc from the vertex across both arms; equal arcs from those two points; join the vertex to where they cross.",
       2: "Compass more than half of |AB|; equal arcs from A and B above and below; join the crossings.",
       3: "Arc from P cutting l twice; equal arcs from those points on the other side; join P to the crossing.",
       4: "Arcs from P cutting l either side; wider equal arcs from those points; join P to the crossing.",
       5: "Line through P crossing l; copy the angle at the crossing up to P with arcs; join P to the new point.",
       6: "Ray from A; step off equal marks; join the last mark to B; parallels through the other marks.",
       7: "Same as 6, with as many marks as parts.",
       8: "Set the compass to the length on a ruler; arc from the start of the ray.",
       9: "Protractor centre on A, base along the ray; dot at the angle (scale from 0°); draw the ray.",
       10: "Draw one side; arcs from each end with the other two lengths; join up.",
       11: "Draw a side; draw the angle at one end; mark the second side with the compass; join up.",
       12: "Draw the side; draw both angles on the same side of it; they meet at the third corner.",
       13: "Draw the side; right angle at one end; arc of the hypotenuse from the other end; join up.",
       14: "Draw the side; right angle at one end; the given angle at the other; they meet.",
       15: "Draw one side; perpendiculars at both ends; mark the other side's length on each; join."}

SPEC = {}
def con(name, k, seed, box=(200, 150)): SPEC[name] = f"con({k},{seed},[{box[0]},{box[1]}])"
for k in range(1, 16): con(f"R{k}", k, 1400 + k)                         # rules page + poster (same as the web viewer)
NAME_Q = [10, 4, 12, 1, 6, 9]
for i, k in enumerate(NAME_Q, 1): con(f"A{i}", k, 2000 + i)
con("B7", 5, 2107); con("B8", 13, 2108)
SORT_K = [(1, 3101), (2, 3102), (4, 3104), (5, 3105), (11, 3111)]
for k, s in SORT_K: con(f"S{k}", k, s, (190, 135))
res = subprocess.run(["node", os.path.join(SRC, "construction_figs_bridge.js")], input=json.dumps(SPEC), capture_output=True, text=True, check=True)
D = json.loads(res.stdout)
# every finished drawing must validate as exactly its own construction
for name, c in D.items():
    g = TC.parse(c["full"]); w = TC.which(g, {})
    assert w == [c["k"]], (name, c["k"], w, TC.why_fail(g, {}, c["k"]))
    TC.task_matches_drawing(c["k"], TC.title_numbers(c["k"], c["title"]), g)
    for j, t in enumerate(c["steps"]): assert [i for i, p in enumerate(TC.CANON[c["k"]]) if re.search(p, t)] == [j], (name, j, t)
print("checked", len(D), "constructions")
def fig(svg, cls=""): return f'<div class="fig {cls}">{svg}</div>'

# ---------- free sheet ----------
A_ans = [NAMES[k] for k in NAME_Q]
def jumble(c, seed):
    r = random.Random(seed); idx = list(range(len(c["steps"])));
    while idx == sorted(idx): r.shuffle(idx)
    letters = "ABCDE"[:len(idx)]
    shown = [(letters[i], c["steps"][j]) for i, j in enumerate(idx)]
    order = "".join(letters[idx.index(j)] for j in range(len(idx)))
    return shown, order
B7s, B7o = jumble(D["B7"], 7); B8s, B8o = jumble(D["B8"], 8)
C = [("You bisect an angle of 128°. What size is each half?", "64°", 128 / 2 == 64),
     ("The bisector of ∠ABC makes an angle of 27° with [BA]. What size is ∠ABC?", "54°", 27 * 2 == 54),
     ("The perpendicular bisector of [AB] meets it at M. |AB| = 11 cm. Find |AM|.", "5.5 cm", 11 / 2 == 5.5),
     ("C is on the perpendicular bisector of [AB] and |CA| = 7.5 cm. Find |CB|.", "7.5 cm", True),
     ("You divide a 13.5 cm segment into 3 equal parts. How long is each part?", "4.5 cm", 13.5 / 3 == 4.5),
     ("To divide [AB] into 6 equal parts, how many equal steps do you mark on the ray?", "6", True),
     ("|AB| = 10 cm. Which compass width works for its perpendicular bisector: 4 cm, 5 cm or 6 cm?", "6 cm (more than half of 10 cm)", 6 > 10 / 2 >= 5),
     ("ASA: ∠CAB = 48° and ∠ABC = 77°. What should ∠ACB measure?", "55°", 180 - 48 - 77 == 55),
     ("Tom wants 35° but reads the wrong protractor scale. What angle does he draw?", "145°", 180 - 35 == 145),
     ("Can you construct a triangle with sides 4 cm, 5 cm and 10 cm? Why?", "No: 4 + 5 = 9, not more than 10", not (4 + 5 > 10)),
     ("Two sides of a triangle are 6 cm and 9 cm. Between what lengths must the third side be?", "more than 3 cm and less than 15 cm", True),
     ("Find the perimeter of the rectangle you construct with sides 8 cm and 3 cm.", "22 cm", 2 * (8 + 3) == 22)]
assert all(x[2] for x in C)
def deg(x): return math.degrees(x)
a23 = deg(math.acos((6 ** 2 + 5 ** 2 - 8 ** 2) / (2 * 6 * 5)))
bc24 = math.sqrt(7 ** 2 + 5 ** 2 - 2 * 7 * 5 * math.cos(math.radians(60)))
ac25 = 8 * math.sin(math.radians(65)) / math.sin(math.radians(75))
ac26 = math.sqrt(10 ** 2 - 6 ** 2); dg27 = math.hypot(7, 4)
Dq = [("Draw [AB] 10 cm long. Construct its perpendicular bisector (compass and straight edge only). Measure |AM| to M, the midpoint.", "5 cm"),
      ("Draw an angle of 84° with a protractor. Bisect it using only a compass and straight edge. Measure each half.", "42°"),
      ("Construct the triangle with sides 8 cm, 6 cm and 5 cm. Measure its largest angle.", f"about {a23:.0f}° (opposite the 8 cm side)"),
      ("Construct the triangle ABC with |AB| = 7 cm, ∠BAC = 60° and |AC| = 5 cm. Measure |BC|.", f"about {bc24:.1f} cm"),
      ("Construct the triangle ABC with |AB| = 8 cm, ∠CAB = 40° and ∠ABC = 65°. Measure ∠ACB and |AC|.", f"75°; |AC| about {ac25:.1f} cm"),
      ("Construct the right-angled triangle with the right angle at A, |AB| = 6 cm and hypotenuse |BC| = 10 cm. Measure |AC|.", f"{ac26:.0f} cm"),
      ("Construct a rectangle 7 cm by 4 cm. Measure a diagonal.", f"about {dg27:.1f} cm"),
      ("Draw [PQ] 11 cm long. Without measuring, divide it into 3 equal parts. Measure one part.", f"about {11 / 3:.1f} cm")]
assert round(a23) == 93 and f"{bc24:.1f}" == "6.2" and f"{ac25:.1f}" == "7.5" and ac26 == 8 and f"{dg27:.1f}" == "8.1"
E = [("Explain why, in the perpendicular bisector construction, the compass must be opened to more than half of |AB|.",
      "With half or less, the arcs from A and B don't cross (or only touch on [AB]), so there are no points C and D to join."),
     ("Ciara tries to construct a triangle with sides 3 cm, 5 cm and 9 cm. What goes wrong, and why?",
      "The arcs never meet: 3 + 5 = 8, which is less than 9, so no such triangle exists."),
     ("Write the steps to construct the line through a point P parallel to a line l.",
      "Line through P crossing l at Q; arc from Q cutting l (R) and QP (S); same width, arc from P cutting QP at T; compass to |RS|, arc from T crossing the arc from P at U; draw PU."),
     ("You construct a triangle with |AB| = 7 cm, ∠A = 50° and ∠B = 50°. What type of triangle do you get? How big is ∠C?",
      "Isosceles (two equal angles, so |AC| = |BC|); ∠C = 180 − 100 = 80°."),
     ("Which construction gives every point that is the same distance from A as from B?", "The perpendicular bisector of [AB]."),
     ("Sam bisects a 76° angle and measures the halves as 39° and 37°. What should each be? Give one likely reason for the error.",
      "38°. He probably changed the compass width between the two arcs, or the pencil/compass wasn't sharp and steady.")]
assert 180 - 50 - 50 == 80 and 76 / 2 == 38

CSS = """.fig svg{width:100%;height:auto;max-height:30mm;display:block;margin:0 auto}
.r15{display:grid;grid-template-columns:repeat(5,1fr);gap:1.6mm}.r15>div{border:1px solid #E5E7EB;border-radius:7px;padding:1mm 1.5mm;font-size:7pt;line-height:1.2;break-inside:avoid}
.r15 .fig svg{max-height:21mm}.r15 b{font-size:7.6pt;color:var(--green)}
.gq{display:grid;grid-template-columns:repeat(3,1fr);gap:2mm 3mm}.gq>div{border:1px solid #E5E7EB;border-radius:8px;padding:1.5mm 2mm;break-inside:avoid}
.gq .n{font-weight:800;color:var(--green);font-size:9pt}.gq .ln2{display:block;border-bottom:1px solid #9AA3AE;height:12px;margin-top:1mm}.gq .fig svg{max-height:27mm}
.jb{border:1px solid #E5E7EB;border-radius:8px;padding:1.5mm 3mm;margin:1.5mm 0}.jb ol{list-style:none;padding:0;margin:1mm 0}.jb li{margin:1px 0}"""

sheet = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Constructions: rules and practice | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>@page{{@bottom-left{{content:"Léim · leim.ie · Free to print for home or class · JC Maths LO (2018 spec): {LO}"}}}}
.tight{{font-size:9pt;line-height:1.32}}.tight h2{{margin:6px 0 3px;font-size:12.5pt}}.tight .note,.tight .tip{{padding:4px 9px;margin:4px 0}}.tight p{{margin:3px 0}}
ol.q{{padding-left:30px}}ol.q li{{margin:5px 0}}
.p2{{font-size:9pt;line-height:1.3}}.p2 ol.q li{{margin:2.6px 0}}.p2 .line{{min-width:60px}}.p2 h2{{margin:6px 0 3px}}
.cols2{{columns:2;column-gap:8mm}}
.ans td{{padding:2px 5px;font-size:7.9pt;line-height:1.28}}
{CSS}
</style></head><body>
<div class="page tight">
  <div class="band"><div><div class="k">Junior Cycle Maths · Free revision sheet</div><h1>Constructions</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcome (2018 specification): {LO}, constructions 1–15 (3 and 7 are Higher level only). Play the game: <b>leim.ie/construction-steps.html</b></p>
  <div class="two">
   <div><h2>1. The tools</h2><p><b>Compass</b>: arcs and circles, copies a length · <b>straight edge</b>: straight lines, no measuring · <b>ruler</b>: measures · <b>protractor</b>: angles · <b>set square</b>: right angles and parallel lines.</p>
   <p><b>Constructions 1 and 2</b> (angle bisector, perpendicular bisector): <b>compass and straight edge only</b>.</p></div>
   <div><h2>2. Golden rules</h2><p>Sharp pencil · <b>leave every arc showing</b> (it's your proof) · label every point · set the compass against the ruler from 0 · keep the same width when the step says so · sketch triangles first with their measurements.</p></div>
  </div>
  <h2>3. The 15 constructions</h2>
  <div class="r15">{"".join(f'<div>{fig(D[f"R{k}"]["full"])}<b>{k}. {SHORT[k]}</b><br>{KEY[k]}</div>' for k in range(1, 16))}</div>
  <h2>4. Triangles</h2>
  <p><b>SSS</b> three sides · <b>SAS</b> two sides and the angle <b>between</b> them · <b>ASA</b> two angles and the side <b>between</b> them · <b>RHS</b> right angle, hypotenuse, side. <b>Can it be a triangle?</b> The two shorter sides must add to <b>more</b> than the longest.</p>
  <div class="tip"><b>Exam tip:</b> the arcs are your working. A construction with the arcs rubbed out looks measured, and accuracy matters: lengths and angles are checked against the true values.</div>
</div>

<div class="page p2">
  <div class="band"><div><div class="k">Practice · 34 questions</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Name the construction</h2>
  <div class="gq">{"".join(f'<div><span class="n">{i}.</span>{fig(D[f"A{i}"]["full"])}<span class="ln2"></span></div>' for i in range(1, 7))}</div>
  <h2>B. Put the steps in order (write the letters)</h2>
  <div class="jb"><b>7.</b> {D["B7"]["title"]}<ol>{"".join(f"<li><b>{l}</b> {t}</li>" for l, t in B7s)}</ol>Order: <span class="line"></span></div>
  <div class="jb"><b>8.</b> {D["B8"]["title"]}<ol>{"".join(f"<li><b>{l}</b> {t}</li>" for l, t in B8s)}</ol>Order: <span class="line"></span></div>
  <h2>C. Check the numbers</h2>
  <ol class="q cols2" start="9">{"".join(f"<li>{q} <span class='line'></span></li>" for q, a, ok in C)}</ol>
</div>

<div class="page p2">
  <div class="band"><div><div class="k">Construct it · exam-style · answers</div><h1>Pencil, compass, go</h1></div><div class="logo">↗ Léim</div></div>
  <h2>D. Construct it on plain paper, then measure to check (leave your arcs showing)</h2>
  <ol class="q" start="21">{"".join(f"<li>{q} <span class='line'></span></li>" for q, a in Dq)}</ol>
  <h2>E. Exam-style questions</h2>
  <ol class="q" start="29">{"".join(f"<li>{q}<br><span class='line' style='min-width:95%'></span></li>" for q, a in E)}</ol>
  <h2 style="margin-top:6px">Answers</h2>
  <table class="ans"><tbody>
   <tr><td><b>A</b></td><td>{" · ".join(f"{i}. {a}" for i, a in enumerate(A_ans, 1))}</td></tr>
   <tr><td><b>B</b></td><td>7. {B7o} · 8. {B8o}</td></tr>
   <tr><td><b>C</b></td><td>{" · ".join(f"{i}. {a}" for i, (q, a, ok) in enumerate(C, 9))}</td></tr>
   <tr><td><b>D</b></td><td>{" · ".join(f"{i}. {a}" for i, (q, a) in enumerate(Dq, 21))} (accurate constructions are within about 1 mm and 1°)</td></tr>
   <tr><td><b>E</b></td><td>{" · ".join(f"{i}. {a}" for i, (q, a) in enumerate(E, 29))}</td></tr>
  </tbody></table>
  <p class="small">All questions written by Léim. Léim is independent and not connected with the State Examinations Commission or the NCCA.</p>
</div>
</body></html>"""

# ---------- teacher pack ----------
cards = []
for k, s in SORT_K:
    c = D[f"S{k}"]
    for j, t in enumerate(c["steps"]): cards.append((k, j, t, c["svgs"][j + 1]))
random.seed(14); order = list(range(len(cards))); random.shuffle(order)
num_of = {o: n for n, o in enumerate(order, 1)}
sort_key = " · ".join(f"<b>{SHORT[k]}:</b> " + " → ".join(str(num_of[i]) for i, (kk, j, t, s) in enumerate(cards) if kk == k) for k, s in SORT_K)
assert len(cards) == 18

DOMS = [("bisect an angle of 70°: each half", "35°", 70 / 2), ("perpendicular bisector of a 9 cm segment: |AM|", "4.5 cm", 9 / 2),
        ("divide 12 cm into 4 equal parts: each part", "3 cm", 12 / 4), ("ASA with angles 50° and 60°: the third angle", "70°", 180 - 110),
        ("wrong protractor scale when you want 40°", "140°", 180 - 40), ("perpendicular lines meet at", "90°", 90),
        ("the bisector makes 26° with one arm: the whole angle", "52°", 2 * 26), ("C is on the perpendicular bisector of [AB], |CA| = 6 cm: |CB|", "6 cm", 6),
        ("rectangle 6 cm by 4 cm: the perimeter", "20 cm", 2 * (6 + 4)), ("divide 15 cm into 3 equal parts: each part", "5 cm", 15 / 3),
        ("perpendicular bisector of a 14 cm segment: |AM|", "7 cm", 14 / 2), ("bisect a right angle: each half", "45°", 90 / 2),
        ("the three angles of any triangle add to", "180°", 180), ("divide 10 cm into 4 equal parts: each part", "2.5 cm", 10 / 4),
        ("ASA with angles 35° and 85°: the third angle", "60°", 180 - 120), ("wrong protractor scale when you want 25°", "155°", 180 - 25),
        ("sides of 3 cm and 5 cm: the third side must be less than", "8 cm", 3 + 5), ("rectangle 5 cm by 2 cm: the perimeter", "14 cm", 2 * (5 + 2)),
        ("bisect an angle of 150°: each half", "75°", 150 / 2), ("how many constructions are on the Junior Cycle course?", "15", 15)]
for q, a, v in DOMS: assert float(re.match(r"[\d.]+", a).group()) == v, (q, a, v)
assert len(set(a for q, a, v in DOMS)) == 20
random.seed(1414); chain = DOMS[:]; random.shuffle(chain)
dom = [("START" if k == 0 else chain[k - 1][1], x[0]) for k, x in enumerate(chain)] + [(chain[-1][1], "FINISH")]
dom_print = dom[:]; random.shuffle(dom_print)
dom_html = "".join(f'<div class="dom"><div class="h l">{l}</div><div class="h r">{r}</div></div>' for l, r in dom_print)
chain_key = "".join(f"<li>{x} = <b>{a}</b></li>" for x, a, v in chain)
ERR = [("Bisect ∠ABC (construction 1)", "Measured 64° with a protractor and marked 32°", "Construction 1 must use a <b>compass and straight edge only</b>: arcs, not a protractor"),
       ("Perpendicular bisector of a 10 cm segment", "Opened the compass to 4 cm", "4 cm is less than half of 10 cm, so the arcs don't cross. Use <b>more than 5 cm</b>"),
       ("Perpendicular to l at P (P on l)", "Kept the same compass width for the arcs from A and B", "With the same width they only meet at P. <b>Open the compass wider</b>"),
       ("Triangle with sides 4 cm, 5 cm and 10 cm", "The arcs didn't meet, so I joined the ends anyway", "It's impossible: 4 + 5 = 9, <b>less than 10</b>. No such triangle exists"),
       ("Draw an angle of 50°", "Drew 130° using the outer scale", "Read the scale that starts at <b>0° on the arm</b>: 180 − 50 = 130 is the wrong-scale slip"),
       ("Divide [AB] into 3 equal parts", "Drew lines through the marks perpendicular to [AB]", "The lines must be <b>parallel to the line joining the last mark to B</b>")]
w1 = deg(math.acos((6 ** 2 + 7 ** 2 - 8 ** 2) / (2 * 6 * 7))); w2 = math.hypot(9, 5); w3 = math.hypot(5.5, 4)
assert f"{w1:.1f}" == "75.5" and f"{w2:.1f}" == "10.3" and f"{w3:.1f}" == "6.8"

pack = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Constructions Teacher Pack | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>
@page{{@bottom-left{{content:"Léim · leim.ie · Single-teacher licence · JC Maths LO (2018 spec): {LO}";font-size:7pt}}}}
.proc td{{font-size:8.8pt;padding:3px 6px;line-height:1.3}}.proc td:first-child{{white-space:nowrap;font-weight:700;color:var(--green)}}
.p1 .note{{font-size:8.4pt;padding:6px 10px;line-height:1.35}}.p1 p{{font-size:9.3pt}}
.sortc{{display:grid;grid-template-columns:repeat(3,1fr)}}
.sortc .c{{border:2px dashed #9AA3AE;margin:-1px 0 0 -1px;height:36.5mm;position:relative;padding:4mm 2.5mm 1mm;display:flex;flex-direction:column;justify-content:space-between}}
.sortc .c .fig svg{{max-height:18mm}}.sortc .c .t{{font-size:7.2pt;line-height:1.18}}
.sortc .tag{{position:absolute;top:1.2mm;left:3mm;font-size:6.5pt;color:var(--green);font-weight:800;text-transform:uppercase;letter-spacing:.04em}}
.doms{{display:grid;grid-template-columns:1fr 1fr;gap:2mm 6mm}}
.dom{{display:grid;grid-template-columns:1fr 2.2fr;border:2px dashed #9AA3AE;height:18.5mm}}
.dom .h{{display:flex;align-items:center;justify-content:center;text-align:center;padding:2mm;font-size:13pt;font-weight:800}}
.dom .r{{font-size:10.2pt}}.dom .l{{background:var(--mist);border-right:2px solid var(--ink)}}
.poster{{height:255mm;border:6px solid var(--night);border-radius:18px;padding:7mm;display:flex;flex-direction:column;justify-content:space-between}}
.poster h1{{font-size:36pt;text-align:center;margin:0}}.poster p{{font-size:12pt!important}}
.pf{{display:grid;grid-template-columns:repeat(3,1fr);gap:2.5mm}}.pf>div{{background:var(--cream);border:2px solid var(--cream-line);border-radius:10px;padding:1.5mm;text-align:center;font-size:9pt;line-height:1.2;font-weight:700}}
.pf .fig svg{{max-height:26mm}}
.ws{{font-size:9.6pt;line-height:1.38}}.ws ol.q li{{margin:5px 0}}.ws .long{{display:block;border-bottom:1px solid #9AA3AE;height:18px}}
.eh td{{padding:4px 7px;font-size:9.2pt}}.eh td:first-child{{font-weight:700;width:26%}}.eh .gap{{display:block;border-bottom:1px solid #9AA3AE;height:14px}}
.a6{{font-size:9.1pt;line-height:1.35}}.a6 td{{font-size:8.7pt;padding:3px 6px}}.a6 h2{{margin:7px 0 3px}}.a6 ol.q li{{margin:3px 0}}
{CSS}
</style></head><body>

<div class="page p1">
  <div class="band"><div><div class="k">Junior Cycle Maths · Teacher pack</div><h1>Constructions</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcome (2018 specification): {LO}, constructions 1–15 (3 and 7 are Higher level only)</p>
  <div class="two">
    <div><h3>Aims</h3><p>By the end of the lesson students can carry out the Junior Cycle constructions accurately, put the steps in the right order, choose the right instruments, leave their construction arcs showing, and explain why a construction works (e.g. every point on a perpendicular bisector is the same distance from both ends).</p></div>
    <div><h3>In this pack</h3><p>p.1 Teacher notes · p.2 Step Sort cards · p.3 Construction Dominoes (cut-up) · p.4 Wall poster: the 15 constructions · p.5 Worksheet: Error Hunt + exam-style constructions · p.6 Answers. Level: 1st or 2nd year (Higher and Ordinary), or 3rd-year revision. Time: about 60 minutes. All questions are original.</p></div>
  </div>
  <h2 style="margin-top:8px">Procedure</h2>
  <table class="proc"><tbody>
    <tr><td>8 min</td><td><b>Lead-in: Same distance?</b> Students construct the perpendicular bisector of any [AB], pick three points on it and measure to A and to B. "What do you notice? Why does the compass have to be more than half of |AB|?" Elicit: every point on it is equidistant from A and B.</td></tr>
    <tr><td>12 min</td><td><b>Step Sort</b> (p.2, groups of 3–4). Cut out the 18 cards. Groups sort them into five constructions and put each one's steps in order, using the pictures (the newest part is in red). Check against the key, then each group demonstrates one construction at the board.</td></tr>
    <tr><td>10 min</td><td><b>Construction Dominoes</b> (p.3). Start at START, answer the clue, find the domino with that answer on its left, build the chain to FINISH. Chain below.</td></tr>
    <tr><td>22 min</td><td><b>Worksheet</b> (p.5). Error Hunt in pairs, then the exam-style constructions alone with compass, ruler and protractor. Partners swap and check each other's lengths and angles with a ruler and protractor (within 1 mm and 1°).</td></tr>
    <tr><td>8 min</td><td><b>Exit ticket.</b> "Bisect this angle using only a compass and straight edge" (draw one on the board). Look for: arcs showing, same width from both points. Homework: play <b>Construction Steps</b> at leim.ie/construction-steps.html.</td></tr>
  </tbody></table>
  <div class="note"><b>Step Sort key</b> (card numbers in order): {sort_key}.<br>
  <b>Errors to look for:</b> arcs rubbed out · a protractor or ruler used for constructions 1 and 2 · compass opened to half of |AB| or less · the same width kept in construction 4 (the arcs meet at P) · the compass width changed between the two arcs of the angle bisector · the wrong protractor scale (180° minus the angle) · SAS angle drawn at the wrong end · a "triangle" whose two shorter sides add to less than the longest.</div>
  <p class="small"><b>Domino answer chain</b> (START → FINISH):</p>
  <ol class="small" style="columns:2;column-gap:12px;font-size:7.6pt;line-height:1.32;margin:0;padding-left:16px">{chain_key}</ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">Cut up the cards · groups of 3–4</div><h1>Step Sort</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.2pt;margin:0 0 2mm">Cut out the 18 cards. Sort them into five constructions, then put each construction's steps in order. In each picture the newest part is drawn in red.</p>
  <div class="sortc">{"".join(f'<div class="c"><span class="tag">Card {n}</span>{fig(cards[o][3])}<div class="t">{cards[o][2]}</div></div>' for n, o in enumerate(order, 1))}</div>
</div>

<div class="page">
  <div class="band"><div><div class="k">Groups of 3–4 · cut along the dashed lines</div><h1>Construction Dominoes</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.5pt">Start with START. Work out the clue on the right, then find the domino with that answer on its left. Keep going until you reach FINISH.</p>
  <div class="doms">{dom_html}</div>
</div>

<div class="page">
  <div class="poster">
    <h1>The 15 constructions</h1>
    <p style="text-align:center;font-size:14pt!important;margin:0;font-weight:800">Leave your arcs showing!</p>
    <div class="pf">{"".join(f'<div>{fig(D[f"R{k}"]["full"])}{k}. {SHORT[k]}</div>' for k in range(1, 16))}</div>
    <p style="text-align:center;margin:0">1 and 2: <b>compass and straight edge only</b> · 3 and 7: Higher level only · Sharp pencil · Label every point</p>
    <p style="text-align:center;font-size:10pt;color:var(--muted)">Léim · leim.ie · Play Construction Steps: leim.ie/construction-steps.html</p>
  </div>
</div>

<div class="page ws">
  <div class="band"><div><div class="k">Worksheet</div><h1>Error Hunt + exam-style constructions</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Error Hunt</h2>
  <p>Each student made one mistake. Say what's wrong and how to fix it.</p>
  <table class="eh"><thead><tr><th>The task</th><th>What the student did</th><th>The mistake and the fix</th></tr></thead><tbody>
  {"".join(f"<tr><td>{q}</td><td>{w}</td><td><span class='gap'></span><span class='gap'></span></td></tr>" for q, w, r in ERR)}
  </tbody></table>
  <h2>B. Exam-style constructions (use plain paper; leave all your arcs showing)</h2>
  <ol class="q">
    <li>Construct the triangle ABC with |AB| = 8 cm, |BC| = 6 cm and |AC| = 7 cm. Measure ∠ACB.<span class="long"></span></li>
    <li>Construct the rectangle PQRS with |PQ| = 9 cm and |QR| = 5 cm. Measure the diagonal |PR|.<span class="long"></span></li>
    <li>Draw [PQ] 11 cm long. Construct its perpendicular bisector, meeting [PQ] at M. Mark the point R on the bisector, 4 cm from M. Measure |RP| and |RQ|. What do you notice, and why?<span class="long"></span><span class="long"></span></li>
    <li>(a) Draw an angle of 64° with a protractor. (b) Bisect it using only a compass and straight edge. (c) What should each half measure? (d) Why are you not allowed to use the protractor in part (b)?<span class="long"></span><span class="long"></span></li>
  </ol>
</div>

<div class="page a6">
  <div class="band"><div><div class="k">For the teacher</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>Step Sort</h2>
  <p>{sort_key}.</p>
  <h2>A. Error Hunt</h2>
  <table><tbody>{"".join(f"<tr><td style='width:36%'><b>{q}</b>: {w}</td><td>{r}</td></tr>" for q, w, r in ERR)}</tbody></table>
  <h2>B. Exam-style constructions</h2>
  <ol class="q">
    <li>SSS: draw [AB] 8 cm; arcs of 7 cm from A and 6 cm from B cross at C. ∠ACB ≈ <b>{w1:.1f}°</b> (accept 74°–77°).</li>
    <li>Draw [PQ] 9 cm; perpendiculars at P and Q; arcs of 5 cm give S and R; join SR. |PR| ≈ <b>{w2:.1f} cm</b> (accept 10.2–10.4 cm).</li>
    <li>|RP| = |RQ| ≈ <b>{w3:.1f} cm</b>. They are equal because every point on the perpendicular bisector of [PQ] is the same distance from P and Q.</li>
    <li>(c) 64 ÷ 2 = <b>32°</b>. (d) The task says compass and straight edge only: the construction must work without measuring (it shows the bisector is exact, not measured).</li>
  </ol>
  <h2>Marking tip</h2>
  <p>As in the exam, accuracy and visible construction lines both matter. A correct-looking answer with no arcs should not get full marks. Check lengths with a ruler (within about 1 mm) and angles with a protractor (within about 1°).</p>
</div>
</body></html>"""

cover = """<!doctype html><html><head><meta charset="utf-8"><style>
body{margin:0;width:1200px;height:1200px;background:#1B2430;font-family:Inter,sans-serif;color:#fff;display:flex;flex-direction:column;justify-content:space-between;padding:90px;box-sizing:border-box}
.k{display:inline-block;background:#2E7D57;border-radius:99px;padding:12px 26px;font-weight:700;font-size:28px;letter-spacing:.06em;text-transform:uppercase}
h1{font-size:120px;font-weight:800;line-height:1.1;letter-spacing:-.03em;margin:40px 0 0}
h1 span{background:#F6CF5A;color:#1B2430;padding:0 14px}
.sub{font-size:38px;color:#C9D1DA;margin-top:36px;line-height:1.35}
.em{font-size:46px;margin-top:30px;font-weight:800;letter-spacing:.01em;color:#F6CF5A}
.foot{display:flex;justify-content:space-between;align-items:center;font-size:34px;font-weight:700}
.price{background:#F6CF5A;color:#1B2430;border-radius:16px;padding:14px 28px}
</style></head><body>
<div><span class="k">Junior Cycle Maths · Teacher pack</span>
<h1><span>Constructions</span></h1>
<div class="sub">Step Sort cards · Construction Dominoes<br>Poster of all 15 · Worksheet + answers</div>
<div class="em">Compass, straight edge, leave the arcs!</div></div>
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
    pdf("teacher-pack", os.path.join(OUT, "Constructions-Teacher-Pack-Leim.pdf"))
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--hide-scrollbars", "--window-size=1200,1200",
                    f"--screenshot={os.path.join(OUT, f'{SLUG}-cover.png')}", f"{SLUG}-cover.html"], cwd=SRC, check=True, capture_output=True)
