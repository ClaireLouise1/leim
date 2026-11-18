#!/usr/bin/env python3
"""Geometry 2: theorems, congruent & similar triangles (JC Maths topic 24): free sheet + teacher pack + Payhip cover.
Run from the repo root: python3 src/build_geometry2_pdfs.py OUTDIR
Writes src/theorems-congruent-similar-triangles-*.html; PDFs/cover PNG go to OUTDIR (free sheet also to printables/).
Diagrams come from the Proof Builder game's kit through src/proof_figs_bridge.js and every diagram is MEASURED back with
test_proof_builder.py's reader. Every answer is computed here and asserted. Styles are read from src/build_money1_pdfs.py."""
import os, sys, random, subprocess, re, json, math
from fractions import Fraction as Fr
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC)
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/geo2"; os.makedirs(OUT, exist_ok=True)
SLUG = "theorems-congruent-similar-triangles"
LO = "GT.3b, GT.3c, GT.3d, GT.3e, U.11, U.12"

_ns = {}; exec(open(os.path.join(SRC, "test_proof_builder.py"), encoding="utf-8").read().split("if __name__")[0], _ns)
read_svg, mang, dist, classify, KEY = _ns["read_svg"], _ns["mang"], _ns["d"], _ns["classify"], _ns["KEY"]
def n(x):
    x = Fr(x).limit_denominator(1000); s = f"{float(x):.2f}".rstrip("0").rstrip(".")
    return s.replace("-", "−")

# ---------- diagrams from the game's kit ----------
FIGS = {
    "rPara": "FIX.para()", "rDiag": "FIX.diag()", "rSemi": "FIX.semi()", "rSim": "FIX.sim()", "rCases": "FIX.cases()", "rCentre": "FIX.centre()", "rCyclic": "FIX.cyclic()",
    "pA": '(()=>{var P=para(68,126,70,0),g=paraG(P,"ABCD"),c=cen(P);g.s=14;MB(g,P[0],P[1],P[3],68);LEN(g,P[0],P[1],"9 cm",c);LEN(g,P[0],P[3],"5 cm",c);return render(g,"Parallelogram ABCD");})()',
    "pB": '(()=>{var O=[0,0],r=90,B=pt(O,180,r),C=pt(O,0,r),A=pt(O,70,r),g=G();CIR(g,O,r);L(g,B,C);L(g,A,B);L(g,A,C);DOT(g,O);NM(g,O,"O",[0,30]);NM(g,A,"A",O);NM(g,B,"B",O);NM(g,C,"C",O);MB(g,B,C,A,35);return render(g,"Semicircle");})()',
    "pD": '(()=>{var s=20,B=[0,0],A=pt(B,62,6*s),C=[7.5*s,0],D=lerp(A,B,4/6),E=lerp(A,C,4/6),N={A:A,B:B,C:C,D:D,E:E,s:s},g=nestG(N),pr=[A[0]+60,A[1]],c=cen([A,B,C]);g.s=s;LEN(g,A,D,"4 cm",pr);LEN(g,D,B,"2 cm",pr);LEN(g,D,E,"5 cm",B);LEN(g,B,C,"x",c);return render(g,"Triangle with DE parallel to BC");})()',
    "e32": '(()=>{var A=[-95,45],B=[95,-45],C=[-60,-70],D=[60,70],E=[0,0],g=G();L(g,A,B);L(g,C,D);L(g,A,C);L(g,D,B);T(g,A,E);T(g,E,B);T(g,C,E,2);T(g,E,D,2);NM(g,A,"A",E);NM(g,B,"B",E);NM(g,C,"C",E);NM(g,D,"D",E);NM(g,E,"E",[0,40]);return render(g,"Two segments bisecting each other");})()',
    "e34": '(()=>{var O=[0,0],r=90,A=pt(O,180,r),B=pt(O,0,r),C=pt(O,90,r),D=pt(O,300,r),g=G();CIR(g,O,r);L(g,A,B);L(g,A,C);L(g,B,C);L(g,D,A);L(g,D,C);DOT(g,O);NM(g,O,"O",[0,-30]);NM(g,A,"A",O);NM(g,B,"B",O);NM(g,C,"C",O);NM(g,D,"D",O);T(g,A,C);T(g,C,B);return render(g,"Circle with diameter AB");})()',
    "w2": '(()=>{var P=para(70,170,100,0),g=paraG(P,"ABCD");L(g,P[1],P[3]);return render(g,"Parallelogram ABCD with diagonal BD");})()',
    "w5": '(()=>{var O=[0,0],r=90,B=pt(O,205,r),D=pt(O,335,r),A=pt(O,95,r),C=pt(O,270,r),g=G();CIR(g,O,r);L(g,O,B);L(g,O,D);POLY(g,[A,B,C,D]);g.tris=[];DOT(g,O);NM(g,O,"O",A);NM(g,A,"A",O);NM(g,B,"B",O);NM(g,C,"C",O);NM(g,D,"D",O);MB(g,O,B,D,130);return render(g,"Cyclic quadrilateral ABCD with centre O");})()',
    "posterPara": "FIX.para()", "posterSemi": "FIX.semi()", "posterCases": "FIX.cases()", "posterSim": "FIX.sim()",
}
FIG = json.loads(subprocess.run(["node", os.path.join(SRC, "proof_figs_bridge.js")], input=json.dumps(FIGS), capture_output=True, text=True, check=True).stdout)

# ---------- read every diagram back ----------
def marks(D): return {m["l"]: m for m in D["marks"]}
def ang_at(D, v, p, q):  # angle at named vertex v between named points p and q
    N = D["names"]; return _ns["angle"](N[v], N[p], N[q])
A_ = read_svg(FIG["pA"]); assert len(A_["polys"]) == 1 and _ns["is_para"](A_["polys"][0])
assert abs(mang(marks(A_)["68"]) - 68) < .3
LA = {l["t"]: dist(l["a"], l["b"]) / A_["s"] for l in A_["lens"]}; assert abs(LA["9 cm"] - 9) < .03 and abs(LA["5 cm"] - 5) < .03
pA_BCD, pA_ABC = round(ang_at(A_, "C", "B", "D")), round(ang_at(A_, "B", "A", "C"))
pA_DC = round(dist(A_["names"]["D"], A_["names"]["C"]) / A_["s"], 2)
assert (pA_BCD, pA_ABC, pA_DC) == (68, 112, 9)
B_ = read_svg(FIG["pB"]); assert abs(mang(marks(B_)["35"]) - 35) < .3
pB_A, pB_C = ang_at(B_, "A", "B", "C"), ang_at(B_, "C", "A", "B"); assert abs(pB_A - 90) < .3 and abs(pB_C - 55) < .3
D_ = read_svg(FIG["pD"]); ND = D_["names"]
assert _ns["parallel"](ND["D"], ND["E"], ND["B"], ND["C"])
pD_x = Fr(5) * Fr(4 + 2, 4); assert abs(dist(ND["B"], ND["C"]) / D_["s"] - float(pD_x)) < .03 and pD_x == Fr(15, 2)
for l in D_["lens"]:
    if "cm" in l["t"]: assert abs(_ns["numval"](l["t"]) - dist(l["a"], l["b"]) / D_["s"]) < .03
pD_AC = Fr(3) * Fr(6, 4); assert abs(dist(ND["A"], ND["C"]) / dist(ND["A"], ND["E"]) - 1.5) < .003
E32 = read_svg(FIG["e32"]); N32 = E32["names"]
assert dist(N32["A"], N32["E"]) - dist(N32["E"], N32["B"]) < .3 and abs(dist(N32["C"], N32["E"]) - dist(N32["E"], N32["D"])) < .3
assert abs(ang_at(E32, "A", "C", "E") - ang_at(E32, "B", "D", "E")) < .3   # so AC ∥ DB
E34 = read_svg(FIG["e34"]); assert abs(ang_at(E34, "C", "A", "B") - 90) < .3 and abs(ang_at(E34, "A", "C", "B") - 45) < .3 and abs(ang_at(E34, "D", "A", "C") - 45) < .3
W5 = read_svg(FIG["w5"]); assert abs(mang(marks(W5)["130"]) - 130) < .3 and abs(ang_at(W5, "A", "B", "D") - 65) < .3 and abs(ang_at(W5, "C", "B", "D") - 115) < .3
EX1 = read_svg(json.loads(subprocess.run(["node", os.path.join(SRC, "proof_figs_bridge.js")], input='{"a":"FIX.ex1()"}', capture_output=True, text=True, check=True).stdout)["a"])
assert abs(ang_at(EX1, "Q", "P", "R") - 115) < .3      # the Exam corner's parallelogram
for k in list(FIG): FIG[k] = re.sub(r' width="\d+" height="\d+"', "", FIG[k])

# ---------- free sheet ----------
A = [("Use the diagram (ABCD is a parallelogram). Find ∠BCD.", f"{pA_BCD}°"), ("Find ∠ABC.", f"{pA_ABC}°"), ("Find |DC|.", f"{n(pA_DC)} cm"),
     ("Find the perimeter of ABCD.", f"{n(2 * (9 + 5))} cm"),
     ("The diagonals of ABCD meet at O and |AO| = 6.5 cm. Find |AC|.", f"{n(Fr(13, 2) * 2)} cm"),
     ("|BD| = 8.4 cm. Find |OD|.", f"{n(Fr(42, 10) )} cm"),
     ("PQRS is a parallelogram with ∠P = (2x + 10)° and ∠R = 74°. Find x.", n(Fr(74 - 10, 2))),
     ("In a parallelogram, one angle is 3 times the angle next to it. Find the smaller angle.", f"{n(Fr(180, 4))}°")]
assert [a for q, a in A] == ["68°", "112°", "9 cm", "28 cm", "13 cm", "4.2 cm", "32", "45°"]
B = [("Use the diagram ([BC] is a diameter). Find ∠BAC.", f"{round(pB_A)}°"), ("Find ∠ACB.", f"{round(pB_C)}°"),
     ("A, B and C are on a circle and ∠BAC = 90°. What can you say about [BC]?", "it's a diameter (Corollary 4)"),
     ("[BC] is a diameter, ∠ABC = 3x and ∠ACB = 2x. Find x.", n(Fr(90, 5))),
     ("<i>Higher Level:</i> O is the centre and ∠AOB = 140°. C is on the major arc. Find ∠ACB.", f"{140 // 2}°"),
     ("<i>Higher Level:</i> C and D are on the circle, on the same side of [AB], and ∠ADB = 47°. Find ∠ACB.", "47°"),
     ("<i>Higher Level:</i> ABCD is a cyclic quadrilateral with ∠DAB = 104°. Find ∠BCD.", f"{180 - 104}°")]
assert [a for q, a in B][:2] == ["90°", "55°"] and [a for q, a in B][3:] == ["18", "70°", "47°", "76°"]
# congruence: my own classify() from the checker, with the facts written as vertex indices (A,B,C = 0,1,2)
CQ = [("|AB| = |PQ| = 5 cm, |BC| = |QR| = 7 cm, |AC| = |PR| = 9 cm.", {frozenset((0, 1)): 5, frozenset((1, 2)): 7, frozenset((0, 2)): 9}, {}),
      ("|AB| = |PQ| = 6 cm, ∠ABC = ∠PQR = 50°, |BC| = |QR| = 8 cm.", {frozenset((0, 1)): 6, frozenset((1, 2)): 8}, {1: 50}),
      ("∠A = ∠P = 40°, ∠B = ∠Q = 75°, |AB| = |PQ| = 10 cm.", {frozenset((0, 1)): 10}, {0: 40, 1: 75}),
      ("∠A = ∠P = 90°, |BC| = |QR| = 13 cm, |AB| = |PQ| = 5 cm.", {frozenset((1, 2)): 13, frozenset((0, 1)): 5}, {0: 90}),
      ("∠A = ∠P = 50°, ∠B = ∠Q = 60°, ∠C = ∠R = 70°.", {}, {0: 50, 1: 60, 2: 70})]
CN = {"SSS": "SSS", "SAS": "SAS", "ASA": "ASA", "RHS": "RHS", "no": "not enough (AAA)"}
C = [(f"Which test proves △ABC ≡ △PQR, if any? {t}", CN[classify(s, a)]) for t, s, a in CQ] + [
     ("△ABC ≡ △XYZ. Which side is equal to [BC]?", "[YZ]"), ("△ABC ≡ △XYZ and ∠ABC = 64°. Find ∠XYZ.", "64°"),
     ("What is the hypotenuse of a right-angled triangle?", "the side opposite the right angle")]
assert [a for q, a in C][:5] == ["SSS", "SAS", "ASA", "RHS", "not enough (AAA)"]
k26 = Fr(10, 4)
D = [("Use the diagram (DE ∥ BC). Find x = |BC|.", f"{n(pD_x)} cm"), ("In the diagram, |AE| = 3 cm. Find |AC|.", f"{n(pD_AC)} cm"),
     ("A triangle has sides 4 cm, 6 cm and 7 cm. In a similar triangle the shortest side is 10 cm. Find the longest side.", f"{n(7 * k26)} cm"),
     ("Are triangles with sides 3, 5, 6 and 6, 10, 12 similar?", "yes: every side × 2"),
     ("One triangle has angles 50° and 60°; another has angles 60° and 70°. Are they similar?", "yes: both are 50°, 60°, 70°"),
     ("Seán is 1.8 m tall and his shadow is 2.4 m long. At the same time a building's shadow is 16 m long. How tall is the building?", f"{n(Fr(18, 10) * Fr(16) / Fr(24, 10))} m"),
     ("<i>Higher Level:</i> In △ABC, DE ∥ BC and |AD| : |DB| = 3 : 2. |AC| = 15 cm. Find |AE|.", f"{n(Fr(15) * 3 / 5)} cm")]
assert all(Fr(b) / Fr(a) == 2 for a, b in zip((3, 5, 6), (6, 10, 12))) and sorted([50, 60, 70]) == sorted([60, 70, 180 - 130])
assert [a for q, a in D][0] == "7.5 cm" and [a for q, a in D][1] == "4.5 cm" and [a for q, a in D][2] == "17.5 cm" and [a for q, a in D][5] == "12 m" and [a for q, a in D][6] == "9 cm"
# exam-style
E = [("<b>A parallelogram.</b> ABCD is a parallelogram with ∠ABC = 72°. Its diagonals meet at M. |AM| = 3.5 cm and |BD| = 11 cm. Find (a) ∠BCD (b) ∠ADC (c) |AC| (d) |BM|. Give a reason for each.",
      f"(a) <b>{180 - 72}°</b> (co-interior) (b) <b>72°</b> (opposite angles) (c) <b>{n(Fr(7, 2) * 2)} cm</b> (d) <b>{n(Fr(11, 2))} cm</b> (diagonals bisect each other)"),
     ("<b>A proof.</b> [AB] and [CD] bisect each other at E (see the diagram). (a) Prove that △AEC ≡ △BED. (b) Hence show that AC ∥ DB.",
      "(a) |AE| = |EB| and |CE| = |ED| (E is the midpoint of both); ∠AEC = ∠BED (vertically opposite) → <b>SAS</b>. (b) ∠CAE = ∠DBE (matching angles), and these are alternate angles, so <b>AC ∥ DB</b>."),
     ("<b>Similar triangles.</b> In △PQR, S is on [PQ], T is on [PR] and ST ∥ QR. |PS| = 8 cm, |SQ| = 4 cm and |ST| = 10 cm. (a) Find |QR|. (b) |PR| = 18 cm. Find |PT|.",
      f"(a) scale factor 12 ÷ 8 = 1.5: <b>{n(10 * Fr(12, 8))} cm</b> (b) <b>{n(18 / Fr(12, 8))} cm</b>"),
     ("<b>A circle.</b> [AB] is a diameter, C is on the circle and |AC| = |BC| (diagram). (a) Find ∠ACB. (b) Find ∠CAB. (c) <i>Higher Level:</i> D is on the circle. Find ∠ADC.",
      "(a) <b>90°</b> (angle in a semicircle) (b) (180° − 90°) ÷ 2 = <b>45°</b> (isosceles) (c) <b>45°</b> (same arc AC as ∠ABC = 45°)")]

EFIG = {1: f'<div class="gfig" style="width:32mm">{FIG["e32"]}</div>', 3: f'<div class="gfig" style="width:32mm">{FIG["e34"]}</div>'}
def qs(items): return "".join(f"<li>{q} <span class='line'></span></li>" for q, a in items)
def style(var):
    return re.search(var + r' = f"""<!doctype.*?<style>(.*?)</style>', open(os.path.join(SRC, "build_money1_pdfs.py"), encoding="utf-8").read(), re.S).group(1).replace("{LO}", LO).replace("{{", "{").replace("}}", "}")
SHEET_STYLE = style("sheet"); PACK_STYLE = style("pack")
assert "@bottom-left" in SHEET_STYLE and "Single-teacher licence" in PACK_STYLE and "{{" not in SHEET_STYLE + PACK_STYLE
FIGCSS = """svg.pf{display:block;width:100%;height:auto;margin:0 auto}.gfig{float:right;width:46mm;margin:0 0 1mm 3mm}.rf{display:grid;grid-template-columns:1fr 1fr 1fr;gap:2mm;margin:1mm 0}
.rf div{font-size:8pt;text-align:center;line-height:1.25}.rf svg{max-height:27mm}"""

sheet = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Theorems, congruent and similar triangles: rules and practice | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{SHEET_STYLE}
{FIGCSS}
</style></head><body>
<div class="page tight">
  <div class="band"><div><div class="k">Junior Cycle Maths · Free revision sheet</div><h1>Theorems, congruent &amp; similar triangles</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2018 specification): {LO}. Play the game: <b>leim.ie/proof-builder.html</b></p>
  <div class="rf"><div>{FIG["rPara"]}Opposite sides equal, opposite angles equal (Theorem 9)</div><div>{FIG["rDiag"]}The diagonals bisect each other (Theorem 10)</div><div>{FIG["rSemi"]}The angle in a semicircle is 90° (Corollary 3)</div></div>
  <div class="two">
   <div><h2>1. Words of proof</h2>
    <p><b>Axiom:</b> accepted without proof. <b>Theorem:</b> proved. <b>Corollary:</b> follows quickly from a theorem. <b>Converse:</b> swap "if" and "then" (not always true!). <b>Implies (⇒):</b> if … then …. <b>Proof:</b> steps, each with a reason.</p>
    <h2>2. Parallelograms</h2>
    <p>Opposite sides equal, opposite angles equal, neighbouring angles add to 180° (co-interior), and the diagonals bisect each other. <b>Converses:</b> opposite angles equal, OR opposite sides equal, OR diagonals bisecting each other → it IS a parallelogram.</p>
    <h2>3. Circles</h2>
    <p>[BC] a diameter ⇒ ∠BAC = 90° (Corollary 3), and the converse (Corollary 4). <b>Higher Level:</b> angle at the centre = 2 × angle at the circle on the same arc (Theorem 19); angles on the same arc are equal (Corollary 2); opposite angles of a cyclic quadrilateral add to 180° (Corollary 5).</p></div>
   <div><h2>4. Congruent triangles (same shape AND size)</h2>
    <p><b>SSS</b> three sides · <b>SAS</b> two sides and the angle <b>between</b> them · <b>ASA</b> two angles and the side <b>between</b> them · <b>RHS</b> right angle, hypotenuse, one other side. <b>Not tests:</b> AAA, and SSA (angle not between the sides). △ABC ≡ △PQR: A↔P, B↔Q, C↔R.</p>
    <h2>5. Similar triangles (same shape)</h2>
    <div class="gfig" style="width:30mm">{FIG["rSim"]}</div>
    <p>Equal angles ⇒ similar ⇒ sides in proportion (Theorem 13). <b>Scale factor</b> = new side ÷ matching old side. DE ∥ BC makes △ADE similar to △ABC. <b>Higher Level:</b> DE ∥ BC cuts [AB] and [AC] in the same ratio (Theorem 12).</p>
    <div class="note" style="clear:both"><b>Classic mistakes:</b> adding instead of multiplying for similar triangles · using |AD| instead of the whole |AB| · SAS with the angle not between the sides · matching the letters in the wrong order · 180° for the angle in a semicircle.</div></div>
  </div>
  <div class="tip"><b>Exam tip:</b> one fact per line with a <b>reason</b> in brackets. In a congruence proof list three facts, then name the test: "△ABD ≡ △ACD (SSS)".</div>
</div>

<div class="page p2">
  <div class="band"><div><div class="k">Practice · 34 questions</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Parallelograms</h2>
  <div class="gfig" style="width:44mm">{FIG["pA"]}</div>
  <ol class="q">{qs(A)}</ol>
  <h2 style="clear:both">B. Circles</h2>
  <div class="gfig" style="width:34mm">{FIG["pB"]}</div>
  <ol class="q" start="9">{qs(B)}</ol>
  <h2 style="clear:both">C. Congruent triangles</h2><ol class="q" start="16">{qs(C)}</ol>
  <h2>D. Similar triangles</h2>
  <div class="gfig" style="width:34mm">{FIG["pD"]}</div>
  <ol class="q" start="24">{qs(D)}</ol>
  <p class="small" style="margin-top:4px;clear:both">Questions 31–34 are on the next page.</p>
</div>

<div class="page">
  <div class="band"><div><div class="k">Exam-style · then check</div><h1>Exam corner + answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>E. Exam-style questions (show your work, with reasons)</h2>
  <ol class="q e3" start="31">{"".join(f"<li>{EFIG.get(i, '')}{q}<span class='long'></span><span class='long'></span></li>" for i,(q,a) in enumerate(E))}</ol>
  <h2 style="margin-top:10px;clear:both">Answers</h2>
  <table class="ans"><tbody>
   <tr><td><b>A</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(A,1))}</td></tr>
   <tr><td><b>B</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(B,9))}</td></tr>
   <tr><td><b>C</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(C,16))}</td></tr>
   <tr><td><b>D</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(D,24))}</td></tr>
   <tr><td><b>E</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(E,31))}</td></tr>
  </tbody></table>
  <div class="note"><b>Got one wrong?</b> Similar triangles: did you multiply by the scale factor, and use the WHOLE side? Congruence: is the angle between the two sides? Then play <b>Proof Builder</b> at leim.ie/proof-builder.html: the "Go back over these" list at the end shows the reason for each mistake.</div>
  <p class="small">All questions written by Léim. Léim is independent and not connected with the State Examinations Commission or the NCCA.</p>
</div>
</body></html>"""

# ---------- teacher pack ----------
MATCH = [("Parallelogram: ∠A = 70°. Find ∠C.", "70°"), ("Parallelogram: ∠A = 70°. Find ∠B.", f"{180 - 70}°"),
         ("Diagonals meet at O, |AO| = 7 cm. Find |AC|.", "14 cm"), ("[BC] is a diameter. ∠BAC = ?", "90°"),
         ("[BC] is a diameter, ∠ABC = 28°. Find ∠ACB.", f"{90 - 28}°"), ("Three sides match", "SSS"),
         ("Two sides and the angle between them match", "SAS"), ("Two angles and the side between them match", "ASA"),
         ("Right angle, hypotenuse and one side match", "RHS"), ("Similar, scale factor 3: side 4 cm becomes…", f"{3 * 4} cm"),
         ("A statement accepted without proof", "Axiom"), ("Swap the \"if\" and the \"then\"", "Converse")]
ANS = [a for q, a in MATCH]
assert ANS == ["70°", "110°", "14 cm", "90°", "62°", "SSS", "SAS", "ASA", "RHS", "12 cm", "Axiom", "Converse"]
assert len(set(ANS)) == 12, ANS
cards = [q for q, a in MATCH] + ANS
random.seed(24); match_print = cards[:]; random.shuffle(match_print)
match_html = "".join(f'<div class="c"><span class="tag">Card {i}</span><div class="fc{" sm" if len(x) > 10 else ""}">{x}</div></div>' for i, x in enumerate(match_print, 1))
match_key = " · ".join(f"{match_print.index(q) + 1} → {match_print.index(a) + 1}" for q, a in MATCH)

# Proof Sort: two proofs from MY key (the checker's), lines cut up and jumbled
def sort_cards(pid, seed):
    lines = KEY[pid]; idx = list(range(len(lines))); random.seed(seed)
    while True:
        random.shuffle(idx)
        if idx != sorted(idx): break
    letters = "ABCDEF"
    strips = "".join(f'<div class="ps"><b>{letters[k]}</b> {lines[i][0]} <span>({sorted(lines[i][1])[0]})</span></div>' for k, i in enumerate(idx))
    order = ", ".join(letters[idx.index(i)] for i in range(len(lines)))
    assert _ns["valid_order"](lines, [idx[letters.index(x.strip())] for x in order.split(",")])
    return strips, order
SORT = [("T10", "The diagonals of a parallelogram bisect each other", "ABCD is a parallelogram; its diagonals meet at E.", 241),
        ("SEMI", "The angle in a semicircle is a right angle", "[BC] is a diameter, centre O, A on the circle; join O to A.", 242)]
sort_html, sort_key = "", []
for pid, title, given, seed in SORT:
    st, order = sort_cards(pid, seed); sort_html += f'<div class="psb"><h3>Proof Sort: {title}</h3><p class="small"><b>Given:</b> {given}</p>{st}</div>'; sort_key.append(f"{title}: <b>{order}</b>")

DOMS = [("Parallelogram, ∠A = 65°: ∠C", "65°"), ("Parallelogram, ∠A = 65°: ∠B", "115°"), ("Parallelogram, ∠A = 82°: ∠D", "98°"),
        ("The angle in a semicircle", "90°"), ("[BC] a diameter, ∠B = 36°: ∠C", "54°"), ("HL: angle at the centre 100°: angle at the circle", "50°"),
        ("HL: cyclic quadrilateral, ∠A = 73°: ∠C", "107°"), ("Diagonals: |AO| = 4.5 cm: |AC|", "9 cm"), ("Diagonals: |BD| = 13 cm: |OB|", "6.5 cm"),
        ("Parallelogram with sides 7 cm and 4 cm: perimeter", "22 cm"), ("Scale factor from 4 cm to 10 cm", "2.5"), ("Similar, × 3: a 5 cm side", "15 cm"),
        ("Similar, × 1.5: an 8 cm side", "12 cm"), ("Congruent test: three sides", "SSS"), ("Congruent test: two sides, angle between", "SAS"),
        ("Congruent test: two angles, side between", "ASA"), ("Congruent test: right angle, hypotenuse, side", "RHS"),
        ("Same shape, maybe a different size", "similar"), ("Same shape and the same size", "congruent"), ("Accepted without proof", "axiom")]
DANS = [a for k, a in DOMS]
assert DANS[:10] == ["65°", f"{180 - 65}°", f"{180 - 82}°", "90°", f"{90 - 36}°", f"{100 // 2}°", f"{180 - 73}°", f"{n(Fr(9, 2) * 2)} cm", f"{n(Fr(13, 2))} cm", f"{2 * (7 + 4)} cm"]
assert DANS[10:13] == [n(Fr(10, 4)), f"{3 * 5} cm", f"{n(Fr(3, 2) * 8)} cm"] and len(set(DANS)) == 20
random.seed(2424); chain = DOMS[:]; random.shuffle(chain)
dom = [("START" if k == 0 else chain[k - 1][1], x[0]) for k, x in enumerate(chain)] + [(chain[-1][1], "FINISH")]
dom_print = dom[:]; random.shuffle(dom_print)
dom_html = "".join(f'<div class="dom"><div class="h l{" sm" if len(l) > 9 else ""}">{l}</div><div class="h r">{r}</div></div>' for l, r in dom_print)
chain_key = "".join(f"<li>{x} = <b>{a}</b></li>" for x, a in chain)

ERR = [("Parallelogram, ∠A = 64°. Find ∠C.", "116°", "∠A and ∠C are opposite angles, so they are equal: <b>64°</b>"),
       ("[BC] is a diameter and ∠ABC = 40°. Find ∠ACB.", "140°", f"The angle at A is 90° (semicircle): 180° − (90° + 40°) = <b>{180 - 130}°</b>"),
       ("|AB| = |PQ|, |BC| = |QR| and ∠BAC = ∠QPR. \"Congruent by SAS.\"", "SAS", "The angle at A is NOT between [AB] and [BC]: that's SSA, <b>not a test</b>"),
       ("△ABC ≡ △PQR. \"So |AC| = |QR|.\"", "|AC| = |QR|", "Match the letters in order: [AC] ↔ <b>[PR]</b>"),
       ("Similar triangles: 4 cm ↔ 6 cm. A 10 cm side becomes?", "12 cm", f"Multiply, don't add: scale factor 1.5, 10 × 1.5 = <b>{n(10 * Fr(3, 2))} cm</b>"),
       ("Parallelogram ABCD, diagonals meet at O, |AO| = 5 cm. \"So |BD| = 10 cm.\"", "10 cm", "[AO] is half of [AC], not [BD]: <b>|AC| = 10 cm</b>; |BD| is unknown")]
x1 = Fr(180 - 30, 5); assert x1 == 30 and 3 * x1 + 15 == 105 and 2 * x1 + 15 == 75
w3 = (Fr(18) * 5 / 15, Fr(8) / 2); assert w3 == (6, 4)
x4 = Fr(90 - 15, 3); assert x4 == 25

pack = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Theorems, Congruent and Similar Triangles Teacher Pack | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{PACK_STYLE}
{FIGCSS}
.fym .c{{height:15mm}}.fym .fc{{font-size:13pt}}.fym .fc.sm{{font-size:8.8pt}}.p1 .proc td{{font-size:8.4pt;padding:2px 6px}}
.psb{{border:2px solid var(--line);border-radius:8px;padding:2mm 3mm;margin-top:2.5mm}}.psb h3{{margin:0 0 1mm;font-size:10.5pt}}
.ps{{border:1.5px dashed #9AA3AE;padding:1.6mm 2.5mm;margin:-1.5px 0 0;font-size:9.6pt}}.ps b{{color:var(--green);margin-right:3mm}}.ps span{{color:var(--muted);font-size:8.6pt}}
.pg4{{display:grid;grid-template-columns:1fr 1fr;gap:5mm}}.pg4 div{{border:2px solid var(--line);border-radius:10px;padding:3mm;font-size:11pt;text-align:center}}.pg4 svg{{max-height:52mm}}
.dom .r{{font-size:9.4pt}}.dom .l{{font-size:12pt}}
</style></head><body>

<div class="page p1">
  <div class="band"><div><div class="k">Junior Cycle Maths · Teacher pack</div><h1>Theorems, congruent &amp; similar triangles</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2018 specification): {LO}</p>
  <div class="two">
    <div><h3>Aims</h3><p>By the end of the lesson students can use Theorems 9 and 10 (parallelograms), the angle in a semicircle (Corollaries 3 and 4), the congruence tests SSS, SAS, ASA and RHS and similar triangles (Theorem 13) to find angles and lengths, explain the words axiom, theorem, corollary, converse and implies, and order and justify the steps of a short proof. Higher Level: Theorems 11, 12 and 19, Corollaries 1, 2 and 5.</p></div>
    <div><h3>In this pack</h3><p>p.1 Teacher notes · p.2 Proof Builder mingle cards + Proof Sort strips · p.3 Geometry Dominoes (cut-up) · p.4 Wall poster · p.5 Worksheet: Error Hunt + exam-style questions · p.6 Answers. Level: 2nd year (Higher and Ordinary), or 3rd-year revision. Time: about 60 minutes. All questions are original.</p></div>
  </div>
  <h2 style="margin-top:8px">Procedure</h2>
  <table class="proc"><tbody>
    <tr><td>5 min</td><td><b>Lead-in: cut the parallelogram.</b> Each pair draws a parallelogram on paper, draws one diagonal, cuts it out and cuts along the diagonal. "Do the two triangles fit on top of each other? Which sides land on which?" Elicit: congruent, so opposite sides and angles are equal (Theorem 9). Ask: "What made them fit?" (alternate angles + a shared side = ASA).</td></tr>
    <tr><td>8 min</td><td><b>Guided discovery: similar triangles.</b> Pairs draw a triangle ABC, then a line DE parallel to BC (use a set square). Measure |AD|, |AB|, |DE| and |BC|. Compare |AD| ÷ |AB| with |DE| ÷ |BC|. What do you notice? Build Theorem 13 and the idea of a scale factor.</td></tr>
    <tr><td>10 min</td><td><b>Proof Builder mingle</b> (p.2, 24 cards = 12 question/answer pairs; one card each). Question card? Work it out and find your answer. Answer card? Find your question. Pairs explain the reason to each other ("opposite angles", "SAS").</td></tr>
    <tr><td>10 min</td><td><b>Proof Sort</b> (p.2, pairs). Cut the strips of one proof, put them in a correct order and read the proof aloud with the reasons. Discuss: which lines could swap places? (The three facts before "≡" can come in any order; the "So …" line is always last.)</td></tr>
    <tr><td>12 min</td><td><b>Geometry Dominoes</b> (p.3), groups of 3–4. Start with START, work out the clue, find the domino with that answer on its left, and build the chain to FINISH. (Two dominoes are Higher Level: HL.)</td></tr>
    <tr><td>12 min</td><td><b>Worksheet</b> (p.5). Error Hunt in pairs (find the mistake, give the right reason, fix it), then the exam-style questions alone.</td></tr>
    <tr><td>3 min</td><td><b>Exit ticket.</b> Write the converse of "If a quadrilateral is a parallelogram, then its diagonals bisect each other." Is it true? Homework: play <b>Proof Builder</b> at leim.ie/proof-builder.html and copy three lines from the "Go back over these" list.</td></tr>
  </tbody></table>
  <div class="note"><b>Mingle key</b> (question card → answer card): {match_key}.<br><b>Proof Sort key:</b> {" · ".join(sort_key)} (the first three facts of each can be in any order).<br>
  <b>Errors to look for:</b> SAS with the angle not between the sides · adding instead of multiplying with similar triangles · using part of a side · matching letters in the wrong order · thinking the diagonals of a parallelogram are equal. <b>Fast finishers:</b> is the converse of "every square has four equal sides" true?</div>
  <p class="small"><b>Domino answer chain</b> (START → FINISH):</p>
  <ol class="small" style="columns:2;column-gap:12px;font-size:7.2pt;line-height:1.22;margin:0;padding-left:16px">{chain_key}</ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">Cut up the cards and the strips</div><h1>Proof Builder mingle + Proof Sort</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:8.8pt;margin:0"><b>Proof Builder mingle.</b> Cut out the 24 cards and give one to each student. Question card? Work it out, then find the person with your answer. Answer card? Find the question that gives your answer. (Fewer students? Take out whole pairs.)</p>
  <div class="fym">{match_html}</div>
  <p style="font-size:8.8pt;margin:2.5mm 0 0"><b>Proof Sort.</b> Cut along the dashed lines. Put the strips in an order that makes a correct proof, then read it aloud with the reasons.</p>
  {sort_html}
</div>

<div class="page">
  <div class="band"><div><div class="k">Groups of 3–4 · cut along the dashed lines</div><h1>Geometry Dominoes</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.4pt">Start with START. Work out the clue on the right, then find the domino with that answer on its left. Keep going until you reach FINISH. "HL" = Higher Level.</p>
  <div class="doms">{dom_html}</div>
</div>

<div class="page">
  <div class="poster">
    <h1>The geometry toolkit</h1>
    <div class="pg4">
      <div>{FIG["posterPara"]}<b>Parallelogram:</b> opposite sides and opposite angles equal; diagonals bisect each other</div>
      <div>{FIG["posterSemi"]}<b>Angle in a semicircle = 90°</b></div>
      <div>{FIG["posterCases"]}<b>Congruent:</b> SSS · SAS · ASA · RHS<br>(same shape AND size)</div>
      <div>{FIG["posterSim"]}<b>Similar:</b> equal angles ⇒ sides in proportion<br>× the scale factor</div>
    </div>
    <p style="text-align:center;font-size:13pt;margin:3mm 0 0"><b>Every line of a proof needs a reason.</b></p>
    <p style="text-align:center;font-size:10pt;color:var(--muted)">Léim · leim.ie · Play Proof Builder: leim.ie/proof-builder.html</p>
  </div>
</div>

<div class="page ws">
  <div class="band"><div><div class="k">Worksheet</div><h1>Error Hunt + exam-style questions</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Error Hunt</h2>
  <p>Each answer has one mistake. Find it, say which fact was used wrongly, and write the right answer.</p>
  <table class="eh"><thead><tr><th>Question</th><th>Student's answer</th><th>The mistake and the right answer</th></tr></thead><tbody>
  {"".join(f"<tr><td>{q}</td><td>{w}</td><td><span class='gap'></span><span class='gap'></span></td></tr>" for q,w,r in ERR)}
  </tbody></table>
  <h2>B. Exam-style questions (show all your work, with reasons)</h2>
  <div class="gfig" style="width:38mm">{FIG["w2"]}<div style="height:2mm"></div>{FIG["w5"]}</div>
  <ol class="q">
    <li>In a parallelogram, two neighbouring angles are (3x + 15)° and (2x + 15)°. Find x and the size of each angle.<span class="long"></span></li>
    <li>ABCD is a parallelogram with the diagonal [BD] (diagram). Prove that △ABD ≡ △CDB.<span class="long"></span></li>
    <li>In △ABC, D is on [AB], E is on [AC] and DE ∥ BC. |AD| = 5 cm, |AB| = 15 cm and |BC| = 18 cm. (a) Find |DE|. (b) |EC| = 8 cm. Find |AE|.<span class="long"></span></li>
    <li>[PQ] is a diameter of a circle and R is on the circle. ∠RPQ = 2x and ∠RQP = x + 15°. Find x and both angles.<span class="long"></span></li>
    <li><i>Higher Level:</i> O is the centre and ∠BOD = 130° (diagram). Find ∠BAD and ∠BCD, giving a reason for each.<span class="long"></span></li>
  </ol>
</div>

<div class="page an">
  <div class="band"><div><div class="k">For the teacher</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>Proof Sort</h2>
  <p>{" · ".join(sort_key)}. Any order of the first three facts is correct; the congruence (or similarity) line comes after them and the "So …" line comes last.</p>
  <h2>A. Error Hunt</h2>
  <table><tbody>{"".join(f"<tr><td style='width:40%'><b>{q}</b> {w}</td><td>{r}</td></tr>" for q,w,r in ERR)}</tbody></table>
  <h2>B. Exam-style questions</h2>
  <ol class="q">
    <li>Neighbouring angles add to 180° (co-interior): 5x + 30 = 180, so <b>x = {x1}</b>. The angles are <b>{3 * x1 + 15}°</b> and <b>{2 * x1 + 15}°</b>.</li>
    <li>|AB| = |CD| and |AD| = |CB| (opposite sides of a parallelogram); |BD| = |DB| (common side). So <b>△ABD ≡ △CDB (SSS)</b>. (Or ASA with alternate angles.) This is Corollary 1.</li>
    <li>(a) Scale factor 15 ÷ 5 = 3: |DE| = 18 ÷ 3 = <b>{w3[0]} cm</b>. (b) |AE| : |AC| = 1 : 3, so |EC| is 2 parts = 8 cm: |AE| = <b>{w3[1]} cm</b>.</li>
    <li>∠PRQ = 90° (angle in a semicircle), so 2x + x + 15 = 90: <b>x = {x4}</b>. ∠RPQ = <b>{2 * x4}°</b> and ∠RQP = <b>{x4 + 15}°</b>.</li>
    <li>∠BAD = 130° ÷ 2 = <b>65°</b> (angle at the centre is twice the angle at the circle, Theorem 19). ∠BCD = 180° − 65° = <b>115°</b> (opposite angles of a cyclic quadrilateral, Corollary 5).</li>
  </ol>
  <h2>Marking tip</h2>
  <p>Give credit for each step, as the exam does: each correct value, each correct reason, and in a proof the three facts and the named test. A number without a reason, or "≡" without SSS/SAS/ASA/RHS, is incomplete. For "explain" parts insist on a sentence with a reason in it.</p>
</div>
</body></html>"""

cover = """<!doctype html><html><head><meta charset="utf-8"><style>
body{margin:0;width:1200px;height:1200px;background:#1B2430;font-family:Inter,sans-serif;color:#fff;display:flex;flex-direction:column;justify-content:space-between;padding:90px;box-sizing:border-box}
.k{display:inline-block;background:#2E7D57;border-radius:99px;padding:12px 26px;font-weight:700;font-size:28px;letter-spacing:.06em;text-transform:uppercase}
h1{font-size:92px;font-weight:800;line-height:1.14;letter-spacing:-.03em;margin:40px 0 0}
h1 span{background:#F6CF5A;color:#1B2430;padding:0 14px;box-decoration-break:clone;-webkit-box-decoration-break:clone}
.sub{font-size:38px;color:#C9D1DA;margin-top:36px;line-height:1.35}
.em{font-size:50px;margin-top:30px;font-weight:800;letter-spacing:.01em;color:#F6CF5A}
.foot{display:flex;justify-content:space-between;align-items:center;font-size:34px;font-weight:700}
.price{background:#F6CF5A;color:#1B2430;border-radius:16px;padding:14px 28px}
</style></head><body>
<div><span class="k">Junior Cycle Maths · Teacher pack</span>
<h1><span>Theorems,</span><br><span>Congruent &amp; Similar</span><br><span>Triangles</span></h1>
<div class="sub">Proof Builder mingle · Proof Sort<br>Dominoes · Poster · Worksheet + answers</div>
<div class="em">SSS · SAS · ASA · RHS</div></div>
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
    pdf("teacher-pack", os.path.join(OUT, "Theorems-Congruent-Similar-Triangles-Teacher-Pack-Leim.pdf"))
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--hide-scrollbars", "--window-size=1200,1200",
                    f"--screenshot={os.path.join(OUT, f'{SLUG}-cover.png')}", f"{SLUG}-cover.html"], cwd=SRC, check=True, capture_output=True)
    print("domino chain:", [(x, a) for x, a in chain])
