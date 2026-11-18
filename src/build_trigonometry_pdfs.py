#!/usr/bin/env python3
"""Trigonometry (JC Maths topic 32): free sheet + teacher pack + Payhip cover.
Run from the repo root: python3 src/build_trigonometry_pdfs.py OUTDIR
Writes src/trigonometry-*.html; PDFs/cover PNG go to OUTDIR (free sheet also to printables/).
Diagrams come from the Clinometer Challenge game's kit through src/clinometer_figs_bridge.js, and every labelled
diagram is MEASURED back with test_clinometer.py's reader (angle and lengths against the drawing, then solved from
the labels). Every answer is computed here (half-up rounding, never near a rounding boundary) and asserted.
Styles are read from src/build_money1_pdfs.py."""
import os, sys, random, subprocess, re, json, math
from fractions import Fraction as F
from decimal import Decimal, ROUND_HALF_UP
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC)
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/trig"; os.makedirs(OUT, exist_ok=True)
SLUG = "trigonometry"
LO = "GT.4, U.6"

_ns = {}; exec(open(os.path.join(SRC, "test_clinometer.py"), encoding="utf-8").read().split('if __name__ == "__main__":')[0], _ns)
read_svg, triangle, solve, solve_angle = (_ns[k] for k in ("read_svg", "triangle", "solve", "solve_angle"))

def sn(a): return math.sin(math.radians(a))
def cs(a): return math.cos(math.radians(a))
def tn(a): return math.tan(math.radians(a))
def asn(x): return math.degrees(math.asin(x))
def acs(x): return math.degrees(math.acos(x))
def atn(x): return math.degrees(math.atan(x))
def rnd(x, dp=1):
    t = x * 10 ** dp - math.floor(x * 10 ** dp); assert abs(t - 0.5) > 0.01, ("rounding boundary", x)
    s = str(Decimal(repr(x)).quantize(Decimal(1).scaleb(-dp), rounding=ROUND_HALF_UP)); return s
def L1(x, u): return rnd(x, 1) + " " + u          # a length to 1 d.p.
def DG(x): return rnd(x, 0) + "°"                  # an angle to the nearest degree

# ---------- diagrams from the game's kit ----------
FIGS = {"rNames": "FIX.names()", "rElev": "FIX.elev()", "rDep": "FIX.dep()", "rPat": "FIX.pattern()",
        "dA": 'render(ttri(8,15,{o:"8",a:"15",h:"17"},"θ",true),"Diagram A",[240,170])',
        "dB": 'render(ttri(12*Math.sin(35*Math.PI/180),12*Math.cos(35*Math.PI/180),{o:"x",a:0,h:"12 cm"},"35",true),"Diagram B",[240,170])',
        "dC": 'render(ttri(5,8,{o:"5 cm",a:"8 cm",h:0},"θ",true),"Diagram C",[240,170])',
        "e28": 'render(scene("elev",30,30*Math.tan(41*Math.PI/180),{d:"30 m",e:"1.6 m"},"41",{obj:"#7A8594",eye:1.6}),"Building",[240,200])',
        "e29": 'render(scene("dep",80/Math.tan(12*Math.PI/180),80,{h:"80 m",d:"x"},"12",{obj:"#9C8C6E"}),"Cliff",[300,120])',
        "w4": 'render(scene("dep",55/Math.tan(28*Math.PI/180),55,{h:"55 m",d:0},"28",{obj:"#9C8C6E"}),"Lighthouse",[300,130])',
        "posterNames": "FIX.names()", "posterElev": "FIX.elev()", "posterDep": "FIX.dep()"}
FIG = json.loads(subprocess.run(["node", os.path.join(SRC, "clinometer_figs_bridge.js")], input=json.dumps(FIGS), capture_output=True, text=True, check=True).stdout)
TA = triangle(read_svg(FIG["dA"])); assert TA["known"] == {"o": 8, "a": 15, "h": 17} and TA["alpha"] is None
TB = triangle(read_svg(FIG["dB"])); assert TB["alpha"] == 35 and TB["unk"] == "o" and L1(solve(TB)["o"], "cm") == "6.9 cm"
TC = triangle(read_svg(FIG["dC"])); assert DG(solve_angle(TC)) == "32°"
T28 = triangle(read_svg(FIG["e28"])); assert T28["alpha"] == 41 and T28["extra"] == [F("1.6")]
T29 = triangle(read_svg(FIG["e29"])); assert T29["alpha"] == 90 - 12 and L1(solve(T29)["o"], "m") == "376.4 m"
assert abs(solve(T29)["o"] - 80 / tn(12)) < 1e-6   # the boat distance is the side opposite the 78° angle at the top
T_w4 = triangle(read_svg(FIG["w4"])); assert T_w4["alpha"] == 62

# ---------- free sheet questions (each answer computed) ----------
A = [("Diagram A: which side is opposite θ?", "8"), ("Diagram A: which side is adjacent to θ?", "15"),
     ("Diagram A: write sin θ as a fraction.", "8/17"), ("Diagram A: write cos θ as a fraction.", "15/17"), ("Diagram A: write tan θ as a fraction.", "8/15"),
     ("sin 40° to 4 d.p.", rnd(sn(40), 4)), ("tan 72° to 4 d.p.", rnd(tn(72), 4))]
assert [a for q, a in A][5:] == ["0.6428", "3.0777"] and 8 ** 2 + 15 ** 2 == 17 ** 2
B = [("Diagram B: find x.", L1(solve(TB)["o"], "cm")), ("Hypotenuse 20 cm, angle 50°: find the adjacent side.", L1(20 * cs(50), "cm")),
     ("Adjacent 9 m, angle 28°: find the opposite side.", L1(9 * tn(28), "m")), ("Opposite 7 cm, angle 41°: find the hypotenuse.", L1(7 / sn(41), "cm")),
     ("Adjacent 15 m, angle 58°: find the hypotenuse.", L1(15 / cs(58), "m")), ("Opposite 11 cm, angle 33°: find the adjacent side.", L1(11 / tn(33), "cm")),
     ("Hypotenuse 8 m, angle 25°. Which finds the opposite side: 8 × sin 25°, 8 ÷ sin 25° or 8 × tan 25°?", "8 × sin 25°")]
assert [a for q, a in B] == ["6.9 cm", "12.9 cm", "4.8 m", "10.7 cm", "28.3 m", "16.9 cm", "8 × sin 25°"]
Cq = [("Diagram C: find θ.", DG(solve_angle(TC))), ("Opposite 6 cm, hypotenuse 10 cm: find θ.", DG(asn(0.6))), ("Adjacent 7 m, hypotenuse 12 m: find θ.", DG(acs(7 / 12))),
      ("Opposite 9 cm, adjacent 4 cm: find θ.", DG(atn(9 / 4))), ("sin⁻¹(0.45)", DG(asn(0.45))), ("tan⁻¹(1.8)", DG(atn(1.8))), ("cos A = 0.3. Find A to 1 d.p.", rnd(acs(0.3), 1) + "°")]
assert [a for q, a in Cq] == ["32°", "37°", "54°", "66°", "27°", "61°", "72.5°"]
D_ = [("A tree is 25 m away. The angle of elevation of its top is 38°. How tall is it?", L1(25 * tn(38), "m")),
      ("A kite string is 60 m long and makes 53° with the ground. How high is the kite?", L1(60 * sn(53), "m")),
      ("A 6 m ladder reaches 5.5 m up a wall. Find the angle it makes with the ground.", DG(asn(5.5 / 6))),
      ("From the top of a 45 m lighthouse, the angle of depression of a boat is 18°. How far is the boat from the lighthouse?", L1(45 / tn(18), "m")),
      ("<i>Higher Level.</i> From 30 m away, the angles of elevation of the top of a tower and the top of a flagpole on it are 40° and 47°. How tall is the flagpole?", L1(30 * (tn(47) - tn(40)), "m"))]
assert [a for q, a in D_] == ["19.5 m", "47.9 m", "66°", "138.5 m", "7.0 m"]
e27 = (rnd(6 * sn(4), 2) + " m", rnd(6 * cs(4), 2) + " m"); e28 = (L1(30 * tn(41) + 1.6, "m"), DG(atn(30 * tn(41) / 50)))
e29 = (L1(80 / tn(12), "m"), L1(80 / sn(12), "m")); e30 = ("12 cm", "12/15 = 4/5", DG(asn(0.8)))
assert e27 == ("0.42 m", "5.99 m") and e28 == ("27.7 m", "28°") and e29 == ("376.4 m", "384.8 m") and e30[2] == "53°" and 15 ** 2 - 9 ** 2 == 144
E = [("<b>A ramp.</b> A ramp is 6 m long and makes an angle of 4° with the ground. Find (a) the height it rises and (b) the horizontal distance it covers, both to 2 decimal places.",
      f"(a) 6 × sin 4° = <b>{e27[0]}</b> (b) 6 × cos 4° = <b>{e27[1]}</b>"),
     ("<b>The clinometer.</b> Oisín stands 30 m from a building. The angle of elevation of the top is 41° and his eyes are 1.6 m above the ground. (a) Find the height of the building. (b) What is the angle of elevation from 50 m away?",
      f"(a) 30 × tan 41° = 26.07… + 1.6 = <b>{e28[0]}</b> (b) tan⁻¹(26.07… ÷ 50) = <b>{e28[1]}</b>"),
     ("<b>A cliff.</b> From the top of an 80 m cliff, the angle of depression of a boat is 12°. (a) How far is the boat from the foot of the cliff? (b) How far is it from the top of the cliff in a straight line?",
      f"(a) 80 ÷ tan 12° = <b>{e29[0]}</b> (b) 80 ÷ sin 12° = <b>{e29[1]}</b>"),
     ("<b>Sides and angles.</b> Triangle PQR has |∠PQR| = 90°, |PQ| = 9 cm and |PR| = 15 cm. (a) Find |QR|. (b) Write sin ∠QPR as a fraction. (c) Find |∠QPR| to the nearest degree.",
      f"(a) √(15² − 9²) = <b>{e30[0]}</b> (b) <b>{e30[1]}</b> (c) sin⁻¹(0.8) = <b>{e30[2]}</b>")]
EFIG = {1: f'<div class="gfig" style="width:38mm">{FIG["e28"]}</div>', 2: f'<div class="gfig" style="width:52mm">{FIG["e29"]}</div>'}

def qs(items): return "".join(f"<li>{q} <span class='line'></span></li>" for q, a in items)
def style(var):
    return re.search(var + r' = f"""<!doctype.*?<style>(.*?)</style>', open(os.path.join(SRC, "build_money1_pdfs.py"), encoding="utf-8").read(), re.S).group(1).replace("{LO}", LO).replace("{{", "{").replace("}}", "}")
SHEET_STYLE = style("sheet"); PACK_STYLE = style("pack")
assert "@bottom-left" in SHEET_STYLE and "Single-teacher licence" in PACK_STYLE and "{{" not in SHEET_STYLE + PACK_STYLE
FIGCSS = """svg.pf{display:block;width:100%;height:auto;margin:0 auto}.gfig{float:right;width:40mm;margin:0 0 1mm 3mm}.rf{display:grid;grid-template-columns:1fr 1fr 1fr;gap:3mm;margin:1mm 0}
.rf div{font-size:8pt;text-align:center;line-height:1.25}.rf svg{max-height:30mm}.f3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:2mm;margin:1mm 0}.f3 div{border:1.5px solid var(--line);border-radius:6px;padding:1.5mm 2mm;font-size:8.6pt}
.soh{display:grid;grid-template-columns:1fr 1fr 1fr;gap:2mm;margin:1mm 0;text-align:center}.soh div{background:var(--green-soft);border-radius:6px;padding:1.5mm;font-size:9pt}.soh b{display:block;font-size:15pt}"""

sheet = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Trigonometry: rules and practice | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{SHEET_STYLE}
{FIGCSS}
</style></head><body>
<div class="page tight">
  <div class="band"><div><div class="k">Junior Cycle Maths · Free revision sheet</div><h1>Trigonometry</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2018 specification): {LO}. Play the game: <b>leim.ie/clinometer-challenge.html</b></p>
  <div class="rf"><div>{FIG["rNames"]}Label the sides from the angle θ</div><div>{FIG["rElev"]}Elevation: looking UP from the horizontal</div><div>{FIG["rDep"]}Depression: looking DOWN from the horizontal</div></div>
  <div class="two">
   <div><h2>1. Name the sides</h2>
    <p><b>Hypotenuse:</b> opposite the right angle (longest). <b>Opposite:</b> across from θ. <b>Adjacent:</b> next to θ. Change the angle and opposite/adjacent swap.</p>
    <h2>2. SOH CAH TOA</h2>
    <div class="soh"><div><b>SOH</b>sin θ = O ÷ H</div><div><b>CAH</b>cos θ = A ÷ H</div><div><b>TOA</b>tan θ = O ÷ A</div></div>
    <p>Use the ratio with the side you <b>have</b> and the side you <b>want</b>. The ratio depends only on the angle, not on the size of the triangle (similar triangles).</p>
    <h2>3. Finding a side</h2>
    <div class="f3"><div><b>x on top: ×</b><br>sin 35° = x ÷ 12<br>x = 12 × sin 35° = 6.9</div><div><b>x on the bottom: ÷</b><br>sin 40° = 8 ÷ x<br>x = 8 ÷ sin 40° = 12.4</div><div><b>An angle: ⁻¹</b><br>tan θ = 5 ÷ 8<br>θ = tan⁻¹(5 ÷ 8) = 32°</div></div></div>
   <div><h2>4. The calculator</h2>
    <p>Always in <b>DEG</b> mode: sin 30° must give 0.5 (−0.988 means RAD). sin⁻¹, cos⁻¹, tan⁻¹ are on SHIFT. Keep the full value until the last step.</p>
    <h2>5. Elevation and depression</h2>
    <p>Both are measured from the <b>horizontal</b>. The angle of depression from the top equals the angle of elevation from the bottom (alternate angles). Measured from someone's eyes? Add their <b>eye height</b> at the end.</p>
    <p><b>Higher Level:</b> two angles from one point: find both heights, subtract. One ratio from another: tan A = 3/4 → sides 3, 4, 5 (Pythagoras) → sin A = 3/5.</p>
    <div class="note"><b>Classic mistakes:</b> RAD mode · labelling from the wrong angle · × when x is on the bottom · sin instead of sin⁻¹ · depression measured from the vertical cliff · rounding too early.</div></div>
  </div>
  <div class="tip"><b>Exam tip:</b> write the ratio with the numbers in it (tan 32° = h ÷ 18) before you press any buttons, then round only at the end and give units.</div>
</div>

<div class="page p2">
  <div class="band"><div><div class="k">Practice · 30 questions · sides 1 d.p., angles nearest degree</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Name the sides and the ratios</h2>
  <div class="gfig" style="width:32mm"><b style="font-size:8pt">Diagram A</b>{FIG["dA"]}</div>
  <ol class="q">{qs(A)}</ol>
  <h2 style="clear:both">B. Find a side</h2>
  <div class="gfig" style="width:32mm"><b style="font-size:8pt">Diagram B</b>{FIG["dB"]}</div>
  <ol class="q" start="8">{qs(B)}</ol>
  <h2 style="clear:both">C. Find an angle</h2>
  <div class="gfig" style="width:32mm"><b style="font-size:8pt">Diagram C</b>{FIG["dC"]}</div>
  <ol class="q" start="15">{qs(Cq)}</ol>
  <h2 style="clear:both">D. Elevation and depression</h2><ol class="q" start="22">{qs(D_)}</ol>
  <p class="small" style="margin-top:4px;clear:both">Questions 27–30 are on the next page.</p>
</div>

<div class="page">
  <div class="band"><div><div class="k">Exam-style · then check</div><h1>Exam corner + answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>E. Exam-style questions (show your work)</h2>
  <ol class="q e3" start="27">{"".join(f"<li>{EFIG.get(i, '')}{q}<span class='long'></span><span class='long'></span></li>" for i,(q,a) in enumerate(E))}</ol>
  <h2 style="margin-top:10px;clear:both">Answers</h2>
  <table class="ans"><tbody>
   <tr><td><b>A</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(A,1))}</td></tr>
   <tr><td><b>B</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(B,8))}</td></tr>
   <tr><td><b>C</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(Cq,15))}</td></tr>
   <tr><td><b>D</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(D_,22))}</td></tr>
   <tr><td><b>E</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(E,27))}</td></tr>
  </tbody></table>
  <div class="note"><b>Got one wrong?</b> Check DEG mode, then label the sides again from the angle you are using. Then play <b>Clinometer Challenge</b> at leim.ie/clinometer-challenge.html: the "Go back over these" list at the end shows the working for each mistake.</div>
  <p class="small">All questions written by Léim. Léim is independent and not connected with the State Examinations Commission or the NCCA.</p>
</div>
</body></html>"""

# ---------- teacher pack ----------
MATCH = [("Hyp 10, 30°: opposite?", rnd(10 * sn(30), 0)), ("Hyp 20, 60°: adjacent?", rnd(20 * cs(60), 0)),
         ("Adjacent 4, 45°: opposite?", rnd(4 * tn(45), 0)), ("Opposite 6, hyp 12: angle?", "30°"),
         ("Opposite 7, adjacent 7: angle?", "45°"), ("Adjacent 5, hyp 10: angle?", "60°"), ("sin 90°", "1"), ("sin 30°", "0.5"),
         ("Opposite 3, hyp 5: sin θ?", "3/5"), ("Opposite 3, adjacent 4: tan θ?", "3/4"), ("Adjacent 12, hyp 13: cos θ?", "12/13"),
         ("Hyp 8, 25°: opposite (1 d.p.)?", rnd(8 * sn(25), 1))]
assert abs(asn(6 / 12) - 30) < 1e-9 and abs(atn(1) - 45) < 1e-9 and abs(acs(0.5) - 60) < 1e-9 and abs(sn(90) - 1) < 1e-12 and abs(sn(30) - 0.5) < 1e-12
assert abs(10 * sn(30) - 5) < 1e-9 and abs(20 * cs(60) - 10) < 1e-9 and abs(4 * tn(45) - 4) < 1e-9
ANS = [a for q, a in MATCH]
assert ANS == ["5", "10", "4", "30°", "45°", "60°", "1", "0.5", "3/5", "3/4", "12/13", "3.4"], ANS
assert len(set(ANS)) == 12
cards = [q for q, a in MATCH] + ANS
random.seed(32); match_print = cards[:]; random.shuffle(match_print)
match_html = "".join(f'<div class="c"><span class="tag">Card {i}</span><div class="fc{" sm" if len(x) > 10 else ""}">{x}</div></div>' for i, x in enumerate(match_print, 1))
match_key = " · ".join(f"{match_print.index(q) + 1} → {match_print.index(a) + 1}" for q, a in MATCH)

sw = {"tree": L1(20 * tn(35), "m"), "kite": L1(40 * sn(50), "m"), "ramp": DG(asn(0.6 / 5)), "boat": L1(50 / tn(20), "m"), "lad": DG(acs(1.5 / 6))}
assert sw == {"tree": "14.0 m", "kite": "30.6 m", "ramp": "7°", "boat": "137.4 m", "lad": "76°"}, sw
TR = [("Tree: distance from the tree", "20 m", "A"), ("Tree: angle of elevation of the top", "35°", "B"), ("Kite: length of the string (tight)", "40 m", "B"),
      ("Kite: angle of the string with the ground", "50°", "A"), ("Ramp: length of the sloping surface", "5 m", "A"), ("Ramp: height it rises", "0.6 m", "B"),
      ("Height of the tree", "", None), ("Height of the kite", "", None), ("Angle of the ramp", "", None)]
MR = [("Cliff: height", "50 m", "B"), ("Cliff top to the boat: angle of depression", "20°", "A"), ("Ladder: length", "6 m", "A"), ("Ladder: foot from the wall", "1.5 m", "B"),
      ("Distance from the boat to the foot of the cliff", "", None), ("Angle between the ladder and the ground", "", None)]
for rows in (TR, MR):
    assert all(w in ("A", "B") for _, v, w in rows if v) and any(w == "A" for *_, w in rows) and any(w == "B" for *_, w in rows)
def swap_card(who):
    def tab(title, rows):
        return f'<table class="ss"><thead><tr><th colspan="2">{title}</th></tr></thead><tbody>' + "".join(
            f"<tr><td>{k}</td><td><b>{v if w == who else ''}</b></td></tr>" for k, v, w in rows) + "</tbody></table>"
    return f'<div class="idc"><h3>Student {who} · Height Swap</h3><div class="two">{tab("In the park", TR)}{tab("At the coast and at home", MR)}</div></div>'

DOMS = [("Hypotenuse 10, 30°: opposite", rnd(10 * sn(30), 0)), ("Hypotenuse 10, 60°: opposite", rnd(10 * sn(60), 1)), ("Adjacent 10, 40°: opposite", rnd(10 * tn(40), 1)),
        ("Opposite 5, 20°: hypotenuse", rnd(5 / sn(20), 1)), ("Adjacent 6, 50°: hypotenuse", rnd(6 / cs(50), 1)), ("Opposite 9, 35°: adjacent", rnd(9 / tn(35), 1)),
        ("Hypotenuse 15, 70°: adjacent", rnd(15 * cs(70), 1)), ("Opposite 4, hypotenuse 8: θ", "30°"), ("Opposite 10, adjacent 10: θ", "45°"),
        ("Adjacent 3, hypotenuse 6: θ", "60°"), ("Opposite 5, adjacent 12: θ", DG(atn(5 / 12))), ("Opposite 7, hypotenuse 9: θ", DG(asn(7 / 9))),
        ("tan⁻¹(2)", DG(atn(2))), ("sin 30°", "0.5"), ("tan 45°", "1"), ("Sides 5, 12, 13: tan of the angle opposite 5", "5/12"),
        ("HL: tan A = 5/12, so sin A =", "5/13"), ("HL: cos A = 0.6, so tan A =", "4/3"), ("SOH: sin =", "O ÷ H"), ("Measured DOWN from the horizontal", "depression")]
DANS = [a for k, a in DOMS]
assert DANS == ["5", "8.7", "8.4", "14.6", "9.3", "12.9", "5.1", "30°", "45°", "60°", "23°", "51°", "63°", "0.5", "1", "5/12", "5/13", "4/3", "O ÷ H", "depression"], DANS
assert len(set(DANS)) == 20 and 5 ** 2 + 12 ** 2 == 13 ** 2 and abs(asn(0.5) - 30) < 1e-9
random.seed(3232); chain = DOMS[:]; random.shuffle(chain)
dom = [("START" if k == 0 else chain[k - 1][1], x[0]) for k, x in enumerate(chain)] + [(chain[-1][1], "FINISH")]
dom_print = dom[:]; random.shuffle(dom_print)
dom_html = "".join(f'<div class="dom"><div class="h l{" sm" if len(l) > 9 else ""}">{l}</div><div class="h r">{r}</div></div>' for l, r in dom_print)
chain_key = "".join(f"<li>{x} = <b>{a}</b></li>" for x, a in chain)

ERR = [("Hypotenuse 10 cm, angle 40°: find the opposite side.", f"10 × cos 40° = {L1(10 * cs(40), 'cm')}", f"The opposite needs SOH: 10 × sin 40° = <b>{L1(10 * sn(40), 'cm')}</b>"),
       ("Opposite 6 m, angle 35°: find the hypotenuse.", f"6 × sin 35° = {L1(6 * sn(35), 'm')}", f"x is on the bottom, so DIVIDE: 6 ÷ sin 35° = <b>{L1(6 / sn(35), 'm')}</b>"),
       ("Opposite 5 cm, adjacent 9 cm: find θ.", "tan(5 ÷ 9) = 0.0097", f"Use tan⁻¹ (SHIFT tan): tan⁻¹(5 ÷ 9) = <b>{DG(atn(5 / 9))}</b>"),
       ("Find sin 30°.", f"sin 30 = {rnd(math.sin(30), 3).replace('-', '−')}", "Calculator in RAD mode. In DEG: <b>0.5</b>"),
       ("A 40 m cliff, angle of depression 25° to a boat. How far is the boat from the cliff?", f"40 × tan 25° = {L1(40 * tn(25), 'm')}", f"The angle at the boat is 25°, and the cliff is opposite it: 40 ÷ tan 25° = <b>{L1(40 / tn(25), 'm')}</b>"),
       ("A 5 m ladder, foot 1.2 m from the wall. Angle with the ground?", f"sin⁻¹(1.2 ÷ 5) = {DG(asn(1.2 / 5))}", f"1.2 m is ADJACENT to the angle at the foot: cos⁻¹(1.2 ÷ 5) = <b>{DG(acs(1.2 / 5))}</b>")]
assert [e[1] for e in ERR] == ["10 × cos 40° = 7.7 cm", "6 × sin 35° = 3.4 m", "tan(5 ÷ 9) = 0.0097", "sin 30 = −0.988", "40 × tan 25° = 18.7 m", "sin⁻¹(1.2 ÷ 5) = 14°"]
assert abs(math.tan(5 / 9 * math.pi / 180) - 0.0097) < 0.00005
w1 = (L1(75 * sn(48), "m"), L1(75 * (sn(48) - sn(35)), "m")); w2 = rnd(0.5 / sn(6), 2) + " m"; w3 = L1(22 * tn(37) + 1.5, "m")
w4 = L1(55 / tn(16) - 55 / tn(28), "m"); w5 = (L1(20 * sn(36), "cm"), L1(20 * cs(36), "cm"), L1(200 * sn(36) * cs(36), "cm²"))
assert (w1, w2, w3, w4, w5) == (("55.7 m", "12.7 m"), "4.78 m", "18.1 m", "88.4 m", ("11.8 cm", "16.2 cm", "95.1 cm²")), (w1, w2, w3, w4, w5)

pack = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Trigonometry Teacher Pack | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{PACK_STYLE}
{FIGCSS}
.ss td:nth-child(2){{width:20%}}.ss td,.ss th{{padding:1px 5px;font-size:8.6pt;line-height:1.2}}.fym .c{{height:15mm}}.fym .fc{{font-size:13pt}}.fym .fc.sm{{font-size:9pt}}.p1 .proc td{{font-size:8.4pt;padding:2px 6px}}
.idc{{break-inside:avoid}}.dom .r{{font-size:9.6pt}}.dom .l{{font-size:12pt}}.dom .l.sm{{font-size:10pt}}
.big{{text-align:center;font-size:40pt;font-weight:800;margin:1mm 0;letter-spacing:.04em}}
.pf3{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:4mm;align-items:end;text-align:center;font-size:11pt}}.pf3 svg{{max-height:48mm;width:auto;max-width:100%}}.poster .ops div{{font-size:12pt}}
</style></head><body>

<div class="page p1">
  <div class="band"><div><div class="k">Junior Cycle Maths · Teacher pack</div><h1>Trigonometry</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2018 specification): {LO}</p>
  <div class="two">
    <div><h3>Aims</h3><p>By the end of the lesson students can label the opposite, adjacent and hypotenuse from a given angle, use sin, cos and tan (SOH CAH TOA) to find a side, use sin⁻¹, cos⁻¹ and tan⁻¹ to find an angle (0°–90°), and solve real-life problems with angles of elevation and depression.</p></div>
    <div><h3>In this pack</h3><p>p.1 Teacher notes · p.2 Clinometer mingle cards + Height Swap A/B · p.3 Trigonometry Dominoes (cut-up) · p.4 Wall poster · p.5 Worksheet: Error Hunt + exam-style questions · p.6 Answers. Level: 3rd year (Higher and Ordinary). Time: about 60 minutes. All questions are original.</p></div>
  </div>
  <h2 style="margin-top:8px">Procedure</h2>
  <table class="proc"><tbody>
    <tr><td>8 min</td><td><b>Lead-in: same angle, same ratio.</b> Each pair draws a right-angled triangle with a 35° angle, any size. Measure the opposite and the hypotenuse and work out opposite ÷ hypotenuse. Collect answers on the board: all about 0.57. Then everyone types sin 35°. Name the three sides and build SOH CAH TOA.</td></tr>
    <tr><td>5 min</td><td><b>DEG check.</b> Everyone types sin 30°. Anyone who doesn't get 0.5 switches to DEG mode now.</td></tr>
    <tr><td>10 min</td><td><b>Clinometer mingle</b> (p.2, 24 cards = 12 question/answer pairs; one card each, calculators allowed). Question card? Work it out and find your answer. Answer card? Find your question. Pairs say which ratio they used.</td></tr>
    <tr><td>12 min</td><td><b>Height Swap</b> (p.2, pairs, one A and one B card). Don't show your card. Each fact is on only one card: ask your partner for what you're missing, sketch each triangle, label O, A, H and fill every blank.</td></tr>
    <tr><td>12 min</td><td><b>Trigonometry Dominoes</b> (p.3), groups of 3–4, calculators allowed. Start with START, work out the clue, find the domino with that answer on its left, and build the chain to FINISH. Sides are to 1 d.p., angles to the nearest degree.</td></tr>
    <tr><td>10 min</td><td><b>Worksheet</b> (p.5). Error Hunt in pairs, then the exam-style questions alone. Optional: make a clinometer from a protractor, a straw and a weight on a string and measure the height of the school.</td></tr>
    <tr><td>3 min</td><td><b>Exit ticket.</b> A 10 m ladder makes 70° with the ground. How high up the wall does it reach? Homework: play <b>Clinometer Challenge</b> at leim.ie/clinometer-challenge.html.</td></tr>
  </tbody></table>
  <div class="note"><b>Mingle key</b> (question card → answer card): {match_key}.<br>
  <b>Height Swap answers:</b> tree 20 × tan 35° = {sw["tree"]} · kite 40 × sin 50° = {sw["kite"]} · ramp sin⁻¹(0.6 ÷ 5) = {sw["ramp"]} · boat 50 ÷ tan 20° = {sw["boat"]} · ladder cos⁻¹(1.5 ÷ 6) = {sw["lad"]}.<br>
  <b>Errors to look for:</b> RAD mode · labelling from the wrong angle · multiplying when x is on the bottom · sin instead of sin⁻¹ · depression measured from the vertical · rounding too early. <b>Exit ticket:</b> 10 × sin 70° = {L1(10 * sn(70), "m")}.</div>
  <p class="small"><b>Domino answer chain</b> (START → FINISH):</p>
  <ol class="small" style="columns:2;column-gap:12px;font-size:7.2pt;line-height:1.22;margin:0;padding-left:16px">{chain_key}</ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">Cut up the cards · one Height Swap card per student</div><h1>Clinometer mingle + Height Swap</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:8.8pt;margin:0"><b>Clinometer mingle.</b> Cut out the 24 cards and give one to each student. Question card? Work it out, then find the person with your answer. Answer card? Find the question that gives your answer. "Hyp" = hypotenuse. (Fewer students? Take out whole pairs.)</p>
  <div class="fym">{match_html}</div>
  <p style="font-size:8.8pt;margin:3mm 0 0"><b>Height Swap.</b> Don't show your card. Each fact is on only one of the two cards: ask your partner for what you're missing, sketch the triangle, then fill in every blank. Sides to 1 d.p., angles to the nearest degree.</p>
  {swap_card("A")}
  {swap_card("B")}
</div>

<div class="page">
  <div class="band"><div><div class="k">Groups of 3–4 · cut along the dashed lines</div><h1>Trigonometry Dominoes</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.4pt">Start with START. Work out the clue on the right, then find the domino with that answer on its left. Keep going until you reach FINISH. Sides to 1 d.p., angles to the nearest degree. HL = Higher Level.</p>
  <div class="doms">{dom_html}</div>
</div>

<div class="page">
  <div class="poster">
    <h1>Trigonometry</h1>
    <div class="big">SOH CAH TOA</div>
    <div class="pf3"><div>{FIG["posterNames"]}Label from the angle θ</div><div>{FIG["posterElev"]}Angle of elevation</div><div>{FIG["posterDep"]}Angle of depression</div></div>
    <div class="ops">
      <div style="background:var(--green-soft)"><b>sin θ = O ÷ H</b>cos θ = A ÷ H<br>tan θ = O ÷ A<br>"hyp" = hypotenuse</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Find a side</b>x on top: multiply<br>x on the bottom: divide</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Find an angle</b>SHIFT: sin⁻¹, cos⁻¹, tan⁻¹<br>θ = tan⁻¹(O ÷ A)</div>
      <div style="background:var(--green-soft)"><b>DEG mode</b>sin 30° = 0.5<br>Round at the end</div>
    </div>
    <p style="text-align:center;font-size:10pt;color:var(--muted)">Léim · leim.ie · Play Clinometer Challenge: leim.ie/clinometer-challenge.html</p>
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
    <li>A kite string is 75 m long and makes an angle of 48° with the ground. (a) How high is the kite, to 1 d.p.? (b) The wind drops and the angle becomes 35°. How much lower is the kite?<span class="long"></span></li>
    <li>A ramp must be no steeper than 6°. It has to rise 0.5 m. Find the shortest possible length of the ramp, to 2 d.p.<span class="long"></span></li>
    <li>Róisín stands 22 m from a tree. With a clinometer she measures the angle of elevation of the top as 37°. Her eyes are 1.5 m above the ground. Find the height of the tree, to 1 d.p.<span class="long"></span></li>
    <li><div class="gfig" style="width:46mm">{FIG["w4"]}</div><i>Higher Level.</i> From the top of a 55 m lighthouse, the angles of depression of two boats in a line with it are 28° and 16°. How far apart are the boats, to 1 d.p.?<span class="long"></span></li>
    <li style="clear:both">In triangle ABC, |∠ABC| = 90°, |AC| = 20 cm and |∠BAC| = 36°. Find |BC| and |AB| to 1 d.p., and the area of the triangle.<span class="long"></span></li>
  </ol>
</div>

<div class="page an">
  <div class="band"><div><div class="k">For the teacher</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>Height Swap</h2>
  <p>Tree: 20 × tan 35° = <b>{sw["tree"]}</b> · Kite: 40 × sin 50° = <b>{sw["kite"]}</b> · Ramp: sin⁻¹(0.6 ÷ 5) = <b>{sw["ramp"]}</b> · Boat: the angle at the boat is 20° (alternate angles), 50 ÷ tan 20° = <b>{sw["boat"]}</b> · Ladder: cos⁻¹(1.5 ÷ 6) = <b>{sw["lad"]}</b>.</p>
  <h2>A. Error Hunt</h2>
  <table><tbody>{"".join(f"<tr><td style='width:40%'><b>{q}</b> {w}</td><td>{r}</td></tr>" for q,w,r in ERR)}</tbody></table>
  <h2>B. Exam-style questions</h2>
  <ol class="q">
    <li>(a) 75 × sin 48° = <b>{w1[0]}</b>. (b) 75 × sin 35° = 43.0… m, so it is 55.73… − 43.01… = <b>{w1[1]}</b> lower.</li>
    <li>sin 6° = 0.5 ÷ L, so L = 0.5 ÷ sin 6° = <b>{w2}</b> (any shorter ramp would be steeper than 6°).</li>
    <li>22 × tan 37° = 16.57… m. Add the eye height: 16.57… + 1.5 = <b>{w3}</b>.</li>
    <li>The angles at the boats are 28° and 16°. Near boat: 55 ÷ tan 28° = 103.4… m. Far boat: 55 ÷ tan 16° = 191.8… m. Apart: <b>{w4}</b>.</li>
    <li>|BC| = 20 × sin 36° = <b>{w5[0]}</b> · |AB| = 20 × cos 36° = <b>{w5[1]}</b> · Area = ½ × 16.18… × 11.75… = <b>{w5[2]}</b>.</li>
  </ol>
  <h2>Marking tip</h2>
  <p>Give credit for each step, as the exam does: the sides labelled from the angle, the right ratio written with the numbers in it, the calculator step, then rounding and units. An answer from a calculator in RAD mode loses the calculation marks but can keep the method marks.</p>
</div>
</body></html>"""
assert abs(55 / tn(28) - 103.44) < 0.01 and abs(55 / tn(16) - 191.81) < 0.01 and abs(75 * sn(35) - 43.018) < 0.001 and abs(22 * tn(37) - 16.578) < 0.001

cover = """<!doctype html><html><head><meta charset="utf-8"><style>
body{margin:0;width:1200px;height:1200px;background:#1B2430;font-family:Inter,sans-serif;color:#fff;display:flex;flex-direction:column;justify-content:space-between;padding:90px;box-sizing:border-box}
.k{display:inline-block;background:#2E7D57;border-radius:99px;padding:12px 26px;font-weight:700;font-size:28px;letter-spacing:.06em;text-transform:uppercase}
h1{font-size:104px;font-weight:800;line-height:1.14;letter-spacing:-.03em;margin:40px 0 0}
h1 span{background:#F6CF5A;color:#1B2430;padding:0 14px;box-decoration-break:clone;-webkit-box-decoration-break:clone}
.sub{font-size:38px;color:#C9D1DA;margin-top:36px;line-height:1.35}
.em{font-size:64px;margin-top:30px;font-weight:800;letter-spacing:.04em;color:#F6CF5A}
.foot{display:flex;justify-content:space-between;align-items:center;font-size:34px;font-weight:700}
.price{background:#F6CF5A;color:#1B2430;border-radius:16px;padding:14px 28px}
</style></head><body>
<div><span class="k">Junior Cycle Maths · Teacher pack</span>
<h1><span>Trigonometry</span></h1>
<div class="sub">Clinometer mingle · Height Swap A/B<br>Dominoes · Poster · Worksheet + answers</div>
<div class="em">SOH CAH TOA</div></div>
<div class="foot"><span>↗ Léim · leim.ie</span><span class="price">Ready to teach · 60 min</span></div>
</body></html>"""

if __name__ == "__main__":
    for txt in (sheet, pack):
        assert not re.search("[\U0001F300-\U0001FAFF☀-➿★]", txt), "emoji in a PDF"
    for name, txt in [("rules-and-practice", sheet), ("teacher-pack", pack), ("cover", cover)]:
        open(os.path.join(SRC, f"{SLUG}-{name}.html"), "w", encoding="utf-8").write(txt)
    def pdf(name, out):
        subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--no-pdf-header-footer", f"--print-to-pdf={out}",
                        f"{SLUG}-{name}.html"], cwd=SRC, check=True, capture_output=True)
        d = open(out, "rb").read(); print(name, len(re.findall(rb"/Type\s*/Page[^s]", d)), "pages")
    pdf("rules-and-practice", os.path.join(ROOT, "printables", f"{SLUG}-rules-and-practice.pdf"))
    pdf("teacher-pack", os.path.join(OUT, "Trigonometry-Teacher-Pack-Leim.pdf"))
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--hide-scrollbars", "--window-size=1200,1200",
                    f"--screenshot={os.path.join(OUT, f'{SLUG}-cover.png')}", f"{SLUG}-cover.html"], cwd=SRC, check=True, capture_output=True)
    print("domino chain:", [(x, a) for x, a in chain])
