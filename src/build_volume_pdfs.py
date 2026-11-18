#!/usr/bin/env python3
"""Volume, surface area & nets (JC Maths topic 33): free sheet + teacher pack + Payhip cover.
Run from the repo root: python3 src/build_volume_pdfs.py OUTDIR
Writes src/volume-surface-area-nets-*.html; PDFs/cover PNG go to OUTDIR (free sheet also to printables/).
Diagrams come from the Pack It game's kit through src/pack_it_figs_bridge.js, and every labelled diagram is
MEASURED back with test_pack_it.py's reader (each label against the drawn edge, radii against the ellipses,
nets face by face). Every answer is computed here with exact fractions (π answers half-up, never near a
rounding boundary) and asserted. Styles are read from src/build_money1_pdfs.py."""
import os, sys, random, subprocess, re, json, math
from fractions import Fraction as F
from decimal import Decimal, ROUND_HALF_UP
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC)
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/vol"; os.makedirs(OUT, exist_ok=True)
SLUG = "volume-surface-area-nets"
LO = "GT.2b, GT.2d, GT.2e"

_ns = {}; exec(open(os.path.join(SRC, "test_pack_it.py"), encoding="utf-8").read().split("def main():")[0], _ns)
read_svg, classify_net, area_ = _ns["read_svg"], _ns["classify_net"], _ns["area"]

def fmt(x, dp=2):
    d = Decimal(x.numerator) / Decimal(x.denominator) if isinstance(x, F) else Decimal(repr(x))
    s = format(d.quantize(Decimal(1).scaleb(-dp), rounding=ROUND_HALF_UP), "f")
    if "." in s: s = s.rstrip("0").rstrip(".")
    i, _, f = s.partition("."); return "{:,}".format(int(i)) + ("." + f if f else "")
def P1(c, u):  # c·π with the π button, 1 d.p.
    x = float(c) * math.pi; t = x * 10 - math.floor(x * 10); assert abs(t - 0.5) > 0.01, ("rounding boundary", x); return fmt(x, 1) + " " + u
def P2(c, u):
    x = float(c) * math.pi; t = x * 100 - math.floor(x * 100); assert abs(t - 0.5) > 0.01, ("rounding boundary", x); return fmt(x, 2) + " " + u
def PI(c, u): c = F(c); assert (c * 100).denominator == 1; return ("" if c == 1 else fmt(c)) + "π " + u
def N(x, u, dp=2): x = F(x); assert (x * 10 ** dp).denominator == 1, x; return fmt(x, dp) + " " + u
SV = lambda r: F(4, 3) * F(r) ** 3

# ---------- diagrams from the game's kit ----------
FIGS = {"rCub": "FIX.rCub()", "rTri": "FIX.rTri()", "rCyl": "FIX.rCyl()", "rSph": "FIX.rSph()", "rHemi": "FIX.rHemi()",
        "nCub": "FIX.nCub()", "nTri": "FIX.nTri()", "nCyl": "FIX.nCyl()",
        "dA": 'render(triPrism(5,12,13,20,"cm"),[200,120])', "dB": 'render(cylinder(4,10,"cm","r"),[110,140])',
        "q13": 'render(netCyl(2,4,"cm",false),[160,120])', "q1": 'render(cuboid(8,5,3,"cm"),[150,90])',
        "e28": 'render(cuboid(2,0.8,0.5,"m"),[170,80])', "e29": 'render(cylinder(3.5,11,"cm","r"),[90,130])',
        "pCub": 'render(cuboid(5,3,2,"cm"),[200,110])', "pCyl": 'render(cylinder(3,7,"cm","r"),[130,150])', "pSph": 'render(sphere(3,"cm","r"),[130,130])',
        "w4": 'render(cylinder(3.3,19.8,"cm","r"),[80,170])'}
FIG = json.loads(subprocess.run(["node", os.path.join(SRC, "pack_it_figs_bridge.js")], input=json.dumps(FIGS), capture_output=True, text=True, check=True).stdout)
FIG = {k: v.replace('class="sf"', 'class="sf pf"', 1) for k, v in FIG.items()}
def labels(k): D = read_svg(FIG[k].replace('class="sf pf"', 'class="sf"', 1)); return {kk: v[0] for kk, v in D["L"].items()}, D
LA, _ = labels("dA"); assert LA == {"a": 5, "b": 12, "c": 13, "L": 20} and 5 ** 2 + 12 ** 2 == 13 ** 2
LB, _ = labels("dB"); assert LB == {"r": 4, "h": 10}
assert labels("q1")[0] == {"l": 8, "w": 5, "h": 3}
assert classify_net(labels("q13")[1]) == "Cylinder" and classify_net(labels("nTri")[1]) == "Triangular prism" and classify_net(labels("nCub")[1]) == "Cuboid"
assert labels("e28")[0] == {"l": 2, "w": F("0.8"), "h": F("0.5")} and labels("e29")[0] == {"r": F("3.5"), "h": 11} and labels("w4")[0] == {"r": F("3.3"), "h": F("19.8")}

# ---------- free sheet questions (each answer computed) ----------
A = [("The cuboid in the picture (8 × 5 × 3 cm): volume.", N(8 * 5 * 3, "cm³", 0)),
     ("The same cuboid: total surface area.", N(2 * (40 + 24 + 15), "cm²", 0)),
     ("A cube with edges of 7 cm: volume.", N(7 ** 3, "cm³", 0)), ("The same cube: surface area.", N(6 * 49, "cm²", 0)),
     ("A cuboid holds 360 cm³. It is 12 cm long and 5 cm wide. How high is it?", N(F(360, 12 * 5), "cm")),
     ("A tank is 50 cm × 30 cm × 40 cm. How many litres does it hold?", N(F(50 * 30 * 40, 1000), "litres")),
     ("An open box (no lid) is 20 cm × 15 cm × 10 cm. Area of card?", N(20 * 15 + 2 * 20 * 10 + 2 * 15 * 10, "cm²", 0))]
assert [a for q, a in A] == ["120 cm³", "158 cm²", "343 cm³", "294 cm²", "6 cm", "60 litres", "1,000 cm²"]
B = [("Diagram A: area of one end.", N(F(5 * 12, 2), "cm²")), ("Diagram A: volume.", N(F(5 * 12, 2) * 20, "cm³", 0)),
     ("Diagram A: total surface area.", N(5 * 12 + (5 + 12 + 13) * 20, "cm²", 0)),
     ("A prism's end has an area of 18 cm². It is 25 cm long. Volume?", N(18 * 25, "cm³", 0)),
     ("A triangular prism: how many faces, edges and vertices?", "5, 9, 6"),
     ("Which solid does the net on the right make?", "a cylinder"), ("The net of a cube with edges of 4 cm: its area.", N(6 * 16, "cm²", 0))]
assert [a for q, a in B] == ["30 cm²", "600 cm³", "660 cm²", "450 cm³", "5, 9, 6", "a cylinder", "96 cm²"]
Cq = [("Diagram B: volume, in terms of π.", PI(4 * 4 * 10, "cm³")), ("Diagram B: curved surface area (π button, 1 d.p.).", P1(2 * 4 * 10, "cm²")),
      ("Diagram B: total surface area of the closed cylinder (π button, 1 d.p.).", P1(2 * 16 + 2 * 4 * 10, "cm²")),
      ("A cylinder has a diameter of 14 cm and a height of 10 cm. Volume (π = 22/7)?", N(F(22, 7) * 49 * 10, "cm³")),
      ("A sphere of radius 6 cm: volume, in terms of π.", PI(SV(6), "cm³")), ("A sphere of radius 5 cm: surface area (π = 3.14).", N(F(314, 100) * 4 * 25, "cm²")),
      ("A hemisphere of radius 9 cm: volume, in terms of π.", PI(SV(9) / 2, "cm³")), ("A cylinder holds 245π cm³ and has a radius of 7 cm. Height?", N(F(245, 49), "cm"))]
assert [a for q, a in Cq] == ["160π cm³", "251.3 cm²", "351.9 cm²", "1,540 cm³", "288π cm³", "314 cm²", "486π cm³", "5 cm"]
D_ = [("A tank 40 cm long and 25 cm wide holds water. A 3,000 cm³ stone sinks in. How far does the water rise?", N(F(3000, 40 * 25), "cm")),
      ("A cylinder of radius 6 cm holds water. A ball of radius 3 cm sinks in. How far does the water rise?", N(SV(3) / 36, "cm")),
      ("How many boxes 12 × 10 × 8 cm fit in a container 50 × 30 × 24 cm, all the same way round?", N((50 // 12) * (30 // 10) * (24 // 8), "boxes", 0)),
      ("A silo is a cylinder (radius 3 m, height 5 m) with a hemisphere on top. Volume, in terms of π.", PI(9 * 5 + SV(3) / 2, "m³")),
      ("<i>Higher Level.</i> A sphere has a volume of 36π cm³. Find its radius.", N(3, "cm"))]
assert SV(3) == 36 and F(50 * 30 * 24, 12 * 10 * 8) == F(75, 2)
assert [a for q, a in D_] == ["3 cm", "1 cm", "36 boxes", "63π m³", "3 cm"]
e28 = (N(F(2) * F("0.8") * F("0.5"), "m³"), N(F("0.8") * 1000, "litres", 0), N(800 / F(20), "minutes", 0))
e29 = (N(F(22, 7) * F("3.5") ** 2 * 11, "cm³"), N(F(22, 7) * 2 * F("3.5") * 11, "cm²"))
e30 = (N(SV(6) / 16, "cm"), PI(2 * 16 + 2 * 4 * (SV(6) / 16), "cm²"))
assert e28 == ("0.8 m³", "800 litres", "40 minutes") and e29 == ("423.5 cm³", "242 cm²") and e30 == ("18 cm", "176π cm²"), (e28, e29, e30)
E = [("<b>The water trough.</b> A trough is a cuboid 2 m long, 0.8 m wide and 0.5 m deep. (a) Find its volume in m³. (b) How many litres does it hold? (c) A hose fills it at 20 litres a minute. How long does it take?",
      f"(a) 2 × 0.8 × 0.5 = <b>{e28[0]}</b> (b) × 1,000 = <b>{e28[1]}</b> (c) 800 ÷ 20 = <b>{e28[2]}</b>"),
     ("<b>A tin of beans.</b> A tin has a radius of 3.5 cm and a height of 11 cm. Use π = 22/7. (a) Find its volume. (b) The label goes all the way round the side. Find the area of the label.",
      f"(a) 22/7 × 3.5² × 11 = <b>{e29[0]}</b> (b) 2 × 22/7 × 3.5 × 11 = <b>{e29[1]}</b>"),
     ("<i>Higher Level.</i> <b>Melting.</b> A metal sphere of radius 6 cm is melted down and made into a solid cylinder of radius 4 cm. (a) Find the height of the cylinder. (b) Find the total surface area of the cylinder, in terms of π.",
      f"(a) 288π = π × 4² × h, so h = 288 ÷ 16 = <b>{e30[0]}</b> (b) 2π × 4² + 2π × 4 × 18 = 32π + 144π = <b>{e30[1]}</b>")]
EFIG = {0: f'<div class="gfig" style="width:40mm">{FIG["e28"]}</div>', 1: f'<div class="gfig" style="width:22mm">{FIG["e29"]}</div>'}

def qs(items): return "".join(f"<li>{q} <span class='line'></span></li>" for q, a in items)
def style(var):
    return re.search(var + r' = f"""<!doctype.*?<style>(.*?)</style>', open(os.path.join(SRC, "build_money1_pdfs.py"), encoding="utf-8").read(), re.S).group(1).replace("{LO}", LO).replace("{{", "{").replace("}}", "}")
SHEET_STYLE = style("sheet"); PACK_STYLE = style("pack")
assert "@bottom-left" in SHEET_STYLE and "Single-teacher licence" in PACK_STYLE and "{{" not in SHEET_STYLE + PACK_STYLE
FIGCSS = """svg.pf{display:block;width:100%;height:auto;margin:0 auto;max-width:none!important}
svg.pf .fr,svg.pf .nt,svg.pf .nc,svg.pf .ball{fill:#E8F3EC;stroke:#2E7D57;stroke-width:2;stroke-linejoin:round}svg.pf .sd{fill:#CFE6D7;stroke:#2E7D57;stroke-width:2;stroke-linejoin:round}
svg.pf .top{fill:#F2FAF4;stroke:#2E7D57;stroke-width:2}svg.pf .hd{fill:none;stroke:#2E7D57;stroke-width:1.2;stroke-dasharray:4 4}svg.pf .eq{fill:none;stroke:#2E7D57;stroke-width:1.4}
svg.pf .wt{fill:rgba(52,152,219,.35)}svg.pf .wl{fill:rgba(52,152,219,.45);stroke:#2980B9}svg.pf .rl{stroke:#C0392B;stroke-width:1.6;stroke-dasharray:5 3}svg.pf .dm{stroke:#2E7D57;stroke-dasharray:3 3}
svg.pf .rt{fill:none;stroke:#C0392B;stroke-width:1.4}svg.pf .dt{fill:#1B2430}svg.pf .fl{font:700 13px Inter,sans-serif;fill:#1B2430}svg.pf .fl.q{fill:#C0392B}
.gfig{float:right;width:40mm;margin:0 0 1mm 3mm}.rf{display:grid;grid-template-columns:repeat(5,1fr);gap:2mm;margin:1mm 0}.rf div{font-size:7.8pt;text-align:center;line-height:1.25}.rf svg{max-height:24mm}
.nf{display:grid;grid-template-columns:1fr 1fr 1fr;gap:3mm;margin:1mm 0}.nf div{font-size:8pt;text-align:center}.nf svg{max-height:26mm}"""

sheet = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Volume, surface area &amp; nets: rules and practice | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{SHEET_STYLE}
{FIGCSS}
</style></head><body>
<div class="page tight">
  <div class="band"><div><div class="k">Junior Cycle Maths · Free revision sheet</div><h1>Volume, surface area &amp; nets</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2018 specification): {LO}. Play the game: <b>leim.ie/pack-it.html</b></p>
  <div class="rf"><div>{FIG["rCub"]}<b>Cuboid</b><br>V = l × w × h<br>SA = 2(lw + lh + wh)</div><div>{FIG["rTri"]}<b>Prism</b><br>V = end area × length</div><div>{FIG["rCyl"]}<b>Cylinder</b><br>V = πr²h<br>curved SA = 2πrh</div><div>{FIG["rSph"]}<b>Sphere</b><br>V = ⁴⁄₃πr³<br>SA = 4πr²</div><div>{FIG["rHemi"]}<b>Hemisphere</b><br>V = ⅔πr³<br>solid SA = 3πr²</div></div>
  <div class="two">
   <div><h2>1. Volume or surface area?</h2>
    <p><b>Volume</b> = the space inside (cm³, m³, litres). <b>Surface area</b> = the area of all the outside faces (cm², m²). <b>1 litre = 1,000 cm³</b> · <b>1 m³ = 1,000 litres</b>.</p>
    <h2>2. Prisms and cylinders</h2>
    <p>Volume = <b>area of the end × length</b>. A triangular end: ½ × base × perpendicular height (not the sloping side). A cube: V = a³, SA = 6a². A closed cylinder: SA = 2πr² + 2πrh; no lid: πr² + 2πrh.</p>
    <h2>3. Nets</h2>
    <div class="nf"><div>{FIG["nCub"]}Cuboid: 6 rectangles</div><div>{FIG["nTri"]}2 triangles + 3 rectangles</div><div>{FIG["nCyl"]}2 circles + 1 rectangle</div></div>
    <p>The net's area = the surface area. The cylinder's rectangle is 2πr long.</p></div>
   <div><h2>4. Pack it, fill it, splash it</h2>
    <p><b>Boxes in a container:</b> count along each edge, round DOWN, multiply (don't divide the volumes). <b>Missing length:</b> volume ÷ the other two. <b>Water rising:</b> rise = volume sunk ÷ base area (in a cylinder π cancels). <b>Combined solids:</b> add the parts.</p>
    <h2>5. π and units</h2>
    <p>Follow the instruction: π button, 3.14, 22/7 or in terms of π (36π stays 36π). r is the RADIUS: halve a diameter first. Round only at the end.</p>
    <p><b>Higher Level:</b> work backwards (⁴⁄₃πr³ = 288π → r³ = 216 → r = 6). Melting or recasting: the volumes are equal.</p>
    <div class="note"><b>Classic mistakes:</b> diameter used as r · forgetting a face (or the missing lid) · cm² for a volume · 1 litre = 100 cm³ · dividing volumes to count boxes · the sloping side as the height.</div></div>
  </div>
  <div class="tip"><b>Exam tip:</b> the cylinder and sphere formulas are in the <i>Formulae and Tables</i> booklet. Write the formula, put in the numbers, then the answer with units.</div>
</div>

<div class="page p2">
  <div class="band"><div><div class="k">Practice · 30 questions · use a calculator</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Cuboids and cubes</h2>
  <div class="gfig" style="width:42mm">{FIG["q1"]}</div>
  <ol class="q">{qs(A)}</ol>
  <h2 style="clear:both">B. Prisms and nets</h2>
  <div class="gfig" style="width:46mm"><b style="font-size:8pt">Diagram A</b>{FIG["dA"]}<div style="margin-top:2mm">{FIG["q13"]}</div></div>
  <ol class="q" start="8">{qs(B)}</ol>
  <h2 style="clear:both">C. Cylinders and spheres</h2>
  <div class="gfig" style="width:30mm"><b style="font-size:8pt">Diagram B</b>{FIG["dB"]}</div>
  <ol class="q" start="15">{qs(Cq)}</ol>
  <h2 style="clear:both">D. Splash and combine</h2><ol class="q" start="23">{qs(D_)}</ol>
  <p class="small" style="margin-top:4px;clear:both">Questions 28–30 are on the next page.</p>
</div>

<div class="page">
  <div class="band"><div><div class="k">Exam-style · then check</div><h1>Exam corner + answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>E. Exam-style questions (show your work)</h2>
  <ol class="q e3" start="28">{"".join(f"<li>{EFIG.get(i, '')}{q}<span class='long'></span><span class='long'></span></li>" for i,(q,a) in enumerate(E))}</ol>
  <h2 style="margin-top:10px;clear:both">Answers</h2>
  <table class="ans"><tbody>
   <tr><td><b>A</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(A,1))}</td></tr>
   <tr><td><b>B</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(B,8))}</td></tr>
   <tr><td><b>C</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(Cq,15))}</td></tr>
   <tr><td><b>D</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(D_,23))}</td></tr>
   <tr><td><b>E</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(E,28))}</td></tr>
  </tbody></table>
  <div class="note"><b>Got one wrong?</b> Check you used the radius, then check the units. Then play <b>Pack It</b> at leim.ie/pack-it.html: the "Go back over these" list at the end shows the working for each mistake.</div>
  <p class="small">All questions written by Léim. Léim is independent and not connected with the State Examinations Commission or the NCCA.</p>
</div>
</body></html>"""

# ---------- teacher pack ----------
MATCH = [("Cube, edge 3: volume?", N(27, "cm³", 0)), ("Cube, edge 3: surface area?", N(6 * 9, "cm²", 0)),
         ("Cuboid 5 × 4 × 2: volume?", N(40, "cm³", 0)), ("Cuboid 5 × 4 × 2: surface area?", N(2 * (20 + 10 + 8), "cm²", 0)),
         ("Cylinder r 2, h 5: volume?", PI(4 * 5, "cm³")), ("Cylinder r 3, h 4: curved area?", PI(2 * 3 * 4, "cm²")),
         ("Sphere r 3: volume?", PI(SV(3), "cm³")), ("Sphere r 5: surface area?", PI(4 * 25, "cm²")),
         ("Prism: end 12 cm², length 10: volume?", N(120, "cm³", 0)), ("8,000 cm³ in litres?", N(8, "litres", 0)),
         ("Triangular prism: how many faces?", "5 faces"), ("Hemisphere r 3: volume?", PI(SV(3) / 2, "cm³"))]
ANS = [a for q, a in MATCH]
assert ANS == ["27 cm³", "54 cm²", "40 cm³", "76 cm²", "20π cm³", "24π cm²", "36π cm³", "100π cm²", "120 cm³", "8 litres", "5 faces", "18π cm³"], ANS
assert len(set(ANS)) == 12
cards = [q for q, a in MATCH] + ANS
random.seed(33); match_print = cards[:]; random.shuffle(match_print)
match_html = "".join(f'<div class="c"><span class="tag">Card {i}</span><div class="fc{" sm" if len(x) > 10 else ""}">{x}</div></div>' for i, x in enumerate(match_print, 1))
match_key = " · ".join(f"{match_print.index(q) + 1} → {match_print.index(a) + 1}" for q, a in MATCH)

sw = {"tank": N(F(80 * 30 * 40, 1000), "litres", 0), "glass": N(80 * 30 + 2 * 80 * 40 + 2 * 30 * 40, "cm²", 0), "butt": P1(F(30 * 30 * 90, 1000), "litres"),
      "rise": N(SV(6) / 64, "cm"), "box": N(F(9 * 12, 2) * 20, "cm³", 0), "card": N(9 * 12 + (9 + 12 + 15) * 20, "cm²", 0)}
assert sw == {"tank": "96 litres", "glass": "11,200 cm²", "butt": "254.5 litres", "rise": "4.5 cm", "box": "1,080 cm³", "card": "828 cm²"}, sw
TR = [("Fish tank (no lid): length", "80 cm", "A"), ("Fish tank: width", "30 cm", "B"), ("Fish tank: height", "40 cm", "A"),
      ("Water butt (cylinder): radius", "30 cm", "B"), ("Water butt: height", "90 cm", "A"),
      ("Litres in the fish tank", "", None), ("Area of glass in the fish tank", "", None), ("Litres in the water butt (1 d.p.)", "", None)]
MR = [("Tin of water: radius", "8 cm", "A"), ("Ball dropped in: radius", "6 cm", "B"),
      ("Gift box (triangular prism): the two short sides of the end", "9 cm and 12 cm", "A"), ("Gift box: sloping side", "15 cm", "B"), ("Gift box: length", "20 cm", "B"),
      ("How far the water rises", "", None), ("Volume of the gift box", "", None), ("Card in the gift box", "", None)]
for rows in (TR, MR):
    assert any(w == "A" for *_, w in rows) and any(w == "B" for *_, w in rows)
assert 9 ** 2 + 12 ** 2 == 15 ** 2
def swap_card(who):
    def tab(title, rows):
        return f'<table class="ss"><thead><tr><th colspan="2">{title}</th></tr></thead><tbody>' + "".join(
            f"<tr><td>{k}</td><td><b>{v if w == who else ''}</b></td></tr>" for k, v, w in rows) + "</tbody></table>"
    return f'<div class="idc"><h3>Student {who} · Tank Swap</h3><div class="two">{tab("Tanks", TR)}{tab("Tins and boxes", MR)}</div></div>'

DOMS = [("Cube edge 2: volume", N(8, "cm³", 0)), ("Cube edge 2: surface area", N(24, "cm²", 0)), ("Cuboid 6 × 3 × 2: volume", N(36, "cm³", 0)),
        ("Cuboid 6 × 3 × 2: surface area", N(2 * (18 + 12 + 6), "cm²", 0)), ("Cylinder r 1, h 7: volume", PI(7, "cm³")),
        ("Cylinder r 5, h 2: curved area", PI(2 * 5 * 2, "cm²")), ("Closed cylinder r 2, h 4: total area", PI(2 * 4 + 2 * 2 * 4, "cm²")),
        ("Sphere r 6: surface area", PI(4 * 36, "cm²")), ("Sphere r 6: volume", PI(SV(6), "cm³")), ("Hemisphere r 3: volume", PI(SV(3) / 2, "cm³")),
        ("Solid hemisphere r 2: total area", PI(3 * 4, "cm²")), ("Prism: end 15 cm², length 4", N(60, "cm³", 0)),
        ("Prism, end sides 3, 4, 5, length 7: volume", N(F(3 * 4, 2) * 7, "cm³", 0)), ("2.5 litres in cm³", N(2500, "cm³", 0)),
        ("3 m³ in litres", N(3000, "litres", 0)), ("Cube volume 125 cm³: edge", N(5, "cm")), ("Cuboid volume 48 cm³, base 4 × 3: height", N(F(48, 12), "cm")),
        ("Triangular prism: edges", "9 edges"), ("Net of a cylinder", "2 circles + 1 rectangle"), ("HL: sphere volume 972π cm³: radius", N(9, "cm"))]
assert SV(9) == 972
DANS = [a for k, a in DOMS]
assert len(set(DANS)) == 20, DANS
random.seed(3333); chain = DOMS[:]; random.shuffle(chain)
dom = [("START" if k == 0 else chain[k - 1][1], x[0]) for k, x in enumerate(chain)] + [(chain[-1][1], "FINISH")]
dom_print = dom[:]; random.shuffle(dom_print)
dom_html = "".join(f'<div class="dom"><div class="h l{" sm" if len(l) > 9 else ""}">{l}</div><div class="h r">{r}</div></div>' for l, r in dom_print)
chain_key = "".join(f"<li>{x} = <b>{a}</b></li>" for x, a in chain)

ERR = [("Cylinder, diameter 10 cm, height 8 cm: volume in terms of π.", "π × 10² × 8 = 800π cm³", f"Used the diameter. Radius 5: π × 5² × 8 = <b>{PI(25 * 8, 'cm³')}</b>"),
       ("Cuboid 6 × 4 × 3 cm: total surface area.", "6 × 4 × 3 = 72 cm²", f"That's the volume. 2(24 + 18 + 12) = <b>{N(2 * 54, 'cm²', 0)}</b>"),
       ("Sphere, radius 6 cm: volume in terms of π.", "4π × 6² = 144π cm³", f"That's the surface area formula. ⁴⁄₃π × 6³ = <b>{PI(SV(6), 'cm³')}</b>"),
       ("Tank 30 × 20 × 10 cm: how many litres?", "6,000 ÷ 100 = 60 litres", f"1 litre = 1,000 cm³: 6,000 ÷ 1,000 = <b>{N(6, 'litres', 0)}</b>"),
       ("How many 10 cm cubes fit in a 25 cm cube box?", "15,625 ÷ 1,000 = 15.6, so 15", f"Count along each edge: 2 × 2 × 2 = <b>{(25 // 10) ** 3}</b> (the gaps can't hold a cube)"),
       ("Open box 10 × 8 × 5 cm (no lid): area of card.", "2(80 + 50 + 40) = 340 cm²", f"No lid: one 10 × 8 face only. 80 + 100 + 80 = <b>{N(80 + 2 * 50 + 2 * 40, 'cm²', 0)}</b>")]
assert [e[2][-12:] for e in ERR] and (25 // 10) ** 3 == 8
w1 = (N(25 * 10 * F("1.5"), "m³"), N(375 * 1000, "litres", 0), N(F(375000, 500) / 60, "hours", 1))
w2 = (PI(16 * 12, "cm³"), int(6000 // (192 * math.pi)))
w3 = (N(F(40 * 30, 2) * 200, "cm³", 0), N(F(40 * 30, 2) * 200 / 1000, "litres", 0))
r3 = F("3.3"); cyl = r3 ** 2 * (6 * r3); balls = 3 * SV(r3)
assert (cyl * 1000).denominator == 1 and (balls * 1000).denominator == 1
w4 = (fmt(cyl, 3) + "π cm³", fmt(balls, 3) + "π cm³", (cyl - balls) / cyl)
w5 = (N(15, "cm"), PI(4 * 225, "cm²"), P1(4 * 225, "cm²"))
assert w1 == ("375 m³", "375,000 litres", "12.5 hours") and w2 == ("192π cm³", 9) and w3 == ("120,000 cm³", "120 litres"), (w1, w2, w3)
assert w4[2] == F(1, 3) and SV(15) == 4500 and w5 == ("15 cm", "900π cm²", "2,827.4 cm²"), (w4, w5)
CYL = cyl; BALLS = balls

pack = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Volume, Surface Area &amp; Nets Teacher Pack | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{PACK_STYLE}
{FIGCSS}
.ss td:nth-child(2){{width:24%}}.ss td,.ss th{{padding:1px 5px;font-size:8.5pt;line-height:1.2}}.fym .c{{height:14mm}}.fym .fc{{font-size:13pt}}.fym .fc.sm{{font-size:9pt}}.p1 .proc td{{font-size:8.4pt;padding:2px 6px}}
.idc{{break-inside:avoid}}.dom .r{{font-size:9.6pt}}.dom .l{{font-size:12pt}}.dom .l.sm{{font-size:10pt}}
.big{{text-align:center;font-size:30pt;font-weight:800;margin:1mm 0}}
.pf3{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:4mm;align-items:end;text-align:center;font-size:11pt}}.pf3 svg{{max-height:48mm;width:auto;max-width:100%}}.poster .ops div{{font-size:12pt}}
</style></head><body>

<div class="page p1">
  <div class="band"><div><div class="k">Junior Cycle Maths · Teacher pack</div><h1>Volume, surface area &amp; nets</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2018 specification): {LO}</p>
  <div class="two">
    <div><h3>Aims</h3><p>By the end of the lesson students can draw and recognise the nets of cuboids, prisms and cylinders, and find the volume and surface area of cuboids, cylinders, triangular prisms, spheres, hemispheres and combinations of these, in real-life problems (litres, packing, water rising), with and without π.</p></div>
    <div><h3>In this pack</h3><p>p.1 Teacher notes · p.2 Pack It mingle cards + Tank Swap A/B · p.3 Volume Dominoes (cut-up) · p.4 Wall poster · p.5 Worksheet: Error Hunt + exam-style questions · p.6 Answers. Level: 3rd year (Higher and Ordinary). Time: about 60 minutes. All questions are original.</p></div>
  </div>
  <h2 style="margin-top:8px">Procedure</h2>
  <table class="proc"><tbody>
    <tr><td>8 min</td><td><b>Lead-in: layers.</b> Build a 4 × 2 layer of cubes (or sugar cubes). How many in 1, 2, 3 layers? 10 layers? Students find volume = base area × height, then stretch it to any prism and a cylinder. Unfold an empty cereal box to show a net.</td></tr>
    <tr><td>10 min</td><td><b>Pack It mingle</b> (p.2, 24 cards = 12 question/answer pairs; one card each, calculators allowed). Question card? Work it out and find your answer. Answer card? Find your question. Pairs say the formula they used.</td></tr>
    <tr><td>12 min</td><td><b>Tank Swap</b> (p.2, pairs, one A and one B card). Don't show your card. Each fact is on only one card: ask your partner for what you're missing, sketch each solid and fill every blank.</td></tr>
    <tr><td>12 min</td><td><b>Volume Dominoes</b> (p.3), groups of 3–4. Start with START, work out the clue, find the domino with that answer on its left, and build the chain to FINISH. Answers with π stay in terms of π.</td></tr>
    <tr><td>15 min</td><td><b>Worksheet</b> (p.5). Error Hunt in pairs, then the exam-style questions alone. Optional: bring in a tin, measure it and check the litres on the label.</td></tr>
    <tr><td>3 min</td><td><b>Exit ticket.</b> A cylinder has radius 5 cm and height 10 cm. Find its volume in terms of π. Homework: play <b>Pack It</b> at leim.ie/pack-it.html.</td></tr>
  </tbody></table>
  <div class="note"><b>Mingle key</b> (question card → answer card): {match_key}.<br>
  <b>Tank Swap answers:</b> fish tank {sw["tank"]} · glass {sw["glass"]} · water butt {sw["butt"]} · water rises {sw["rise"]} · gift box {sw["box"]} · card {sw["card"]}.<br>
  <b>Errors to look for:</b> diameter used as r · a face missed (or the lid of an open box counted) · cm² for a volume · 1 litre = 100 cm³ · dividing volumes to count boxes · the sloping side used as the height. <b>Exit ticket:</b> {PI(250, "cm³")}.</div>
  <p class="small"><b>Domino answer chain</b> (START → FINISH):</p>
  <ol class="small" style="columns:2;column-gap:12px;font-size:7.2pt;line-height:1.22;margin:0;padding-left:16px">{chain_key}</ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">Cut up the cards · one Tank Swap card per student</div><h1>Pack It mingle + Tank Swap</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:8.8pt;margin:0"><b>Pack It mingle.</b> Cut out the 24 cards and give one to each student. Question card? Work it out, then find the person with your answer. Answer card? Find the question that gives your answer. Lengths are in cm; leave π in the answer. (Fewer students? Take out whole pairs.)</p>
  <div class="fym">{match_html}</div>
  <p style="font-size:8.8pt;margin:3mm 0 0"><b>Tank Swap.</b> Don't show your card. Each fact is on only one of the two cards: ask your partner for what you're missing, sketch the solid, then fill in every blank. Use the π button.</p>
  {swap_card("A")}
  {swap_card("B")}
</div>

<div class="page">
  <div class="band"><div><div class="k">Groups of 3–4 · cut along the dashed lines</div><h1>Volume Dominoes</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.4pt">Start with START. Work out the clue on the right, then find the domino with that answer on its left. Keep going until you reach FINISH. Lengths are in cm unless it says otherwise. HL = Higher Level.</p>
  <div class="doms">{dom_html}</div>
</div>

<div class="page">
  <div class="poster">
    <h1>Volume &amp; surface area</h1>
    <div class="big">Volume = area of the end × length</div>
    <div class="pf3"><div>{FIG["pCub"]}Cuboid: V = l × w × h</div><div>{FIG["pCyl"]}Cylinder: V = πr²h</div><div>{FIG["pSph"]}Sphere: V = ⁴⁄₃πr³</div></div>
    <div class="ops">
      <div style="background:var(--green-soft)"><b>Surface area</b>add every face<br>= the area of the net</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>r = radius</b>halve the diameter first</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>1 litre</b>= 1,000 cm³<br>1 m³ = 1,000 litres</div>
      <div style="background:var(--green-soft)"><b>Water rises</b>rise = volume ÷ base area</div>
    </div>
    <p style="text-align:center;font-size:10pt;color:var(--muted)">Léim · leim.ie · Play Pack It: leim.ie/pack-it.html</p>
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
    <li>A swimming pool is a cuboid 25 m long, 10 m wide and 1.5 m deep. (a) Find its volume in m³. (b) How many litres is that? (c) A pump fills it at 500 litres a minute. How many hours does it take?<span class="long"></span></li>
    <li>A candle is a cylinder with radius 4 cm and height 12 cm. (a) Find its volume in terms of π. (b) How many whole candles can be made from 6,000 cm³ of wax?<span class="long"></span></li>
    <li>A water trough is a triangular prism 200 cm long. Its end is a right-angled triangle with sides 30 cm, 40 cm and 50 cm. Find its volume in cm³ and in litres.<span class="long"></span></li>
    <li><div class="gfig" style="width:16mm">{FIG["w4"]}</div>Three tennis balls, each of radius 3.3 cm, fit exactly in a cylinder-shaped tube (radius 3.3 cm, height 19.8 cm). (a) Find the volume of the tube in terms of π. (b) Find the volume of the three balls in terms of π. (c) What fraction of the tube is empty space?<span class="long"></span></li>
    <li style="clear:both"><i>Higher Level.</i> A sphere has a volume of 4,500π cm³. (a) Find its radius. (b) Find its surface area, in terms of π and to 1 d.p.<span class="long"></span></li>
  </ol>
</div>

<div class="page an">
  <div class="band"><div><div class="k">For the teacher</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>Tank Swap</h2>
  <p>Fish tank: 80 × 30 × 40 = 96,000 cm³ = <b>{sw["tank"]}</b> · Glass (no lid): 2,400 + 2 × 3,200 + 2 × 1,200 = <b>{sw["glass"]}</b> · Water butt: π × 30² × 90 = 254,469 cm³ = <b>{sw["butt"]}</b> · Ball: ⁴⁄₃π × 6³ = 288π; 288π ÷ (π × 8²) = <b>{sw["rise"]}</b> · Gift box: ½ × 9 × 12 × 20 = <b>{sw["box"]}</b> · Card: 2 × 54 + (9 + 12 + 15) × 20 = <b>{sw["card"]}</b>.</p>
  <h2>A. Error Hunt</h2>
  <table><tbody>{"".join(f"<tr><td style='width:40%'><b>{q}</b> {w}</td><td>{r}</td></tr>" for q,w,r in ERR)}</tbody></table>
  <h2>B. Exam-style questions</h2>
  <ol class="q">
    <li>(a) 25 × 10 × 1.5 = <b>{w1[0]}</b> (b) × 1,000 = <b>{w1[1]}</b> (c) 375,000 ÷ 500 = 750 minutes = <b>{w1[2]}</b>.</li>
    <li>(a) π × 4² × 12 = <b>{w2[0]}</b> (= 603.2 cm³). (b) 6,000 ÷ 603.19 = 9.9…, so <b>{w2[1]} candles</b> (round down: the 10th isn't complete).</li>
    <li>End ½ × 30 × 40 = 600 cm². 600 × 200 = <b>{w3[0]}</b> = <b>{w3[1]}</b>.</li>
    <li>(a) π × 3.3² × 19.8 = <b>{w4[0]}</b> (b) 3 × ⁴⁄₃π × 3.3³ = <b>{w4[1]}</b> (c) (215.622 − 143.748) ÷ 215.622 = 71.874 ÷ 215.622 = <b>⅓</b>. The balls fill two thirds of the tube, whatever the radius.</li>
    <li>(a) ⁴⁄₃πr³ = 4,500π → r³ = 3,375 → r = <b>{w5[0]}</b> (b) 4π × 15² = <b>{w5[1]}</b> = <b>{w5[2]}</b>.</li>
  </ol>
  <h2>Marking tip</h2>
  <p>Give credit for each step, as the exam does: the right formula, the numbers substituted (radius, not diameter), the calculation, then rounding and units (cm³ for volume, cm² for area). Count the faces before adding.</p>
</div>
</body></html>"""
assert abs(6000 / (192 * math.pi) - 9.947) < 0.001 and abs(192 * math.pi - 603.19) < 0.01 and abs(30 * 30 * 90 * math.pi - 254469) < 1
assert w4[:2] == ("215.622π cm³", "143.748π cm³")

cover = """<!doctype html><html><head><meta charset="utf-8"><style>
body{margin:0;width:1200px;height:1200px;background:#1B2430;font-family:Inter,sans-serif;color:#fff;display:flex;flex-direction:column;justify-content:space-between;padding:90px;box-sizing:border-box}
.k{display:inline-block;background:#2E7D57;border-radius:99px;padding:12px 26px;font-weight:700;font-size:28px;letter-spacing:.06em;text-transform:uppercase}
h1{font-size:96px;font-weight:800;line-height:1.16;letter-spacing:-.03em;margin:40px 0 0}
h1 span{background:#F6CF5A;color:#1B2430;padding:0 14px;box-decoration-break:clone;-webkit-box-decoration-break:clone}
.sub{font-size:38px;color:#C9D1DA;margin-top:36px;line-height:1.35}
.em{font-size:60px;margin-top:30px;font-weight:800;letter-spacing:.02em;color:#F6CF5A}
.foot{display:flex;justify-content:space-between;align-items:center;font-size:34px;font-weight:700}
.price{background:#F6CF5A;color:#1B2430;border-radius:16px;padding:14px 28px}
</style></head><body>
<div><span class="k">Junior Cycle Maths · Teacher pack</span>
<h1><span>Volume, Surface</span><br><span>Area &amp; Nets</span></h1>
<div class="sub">Pack It mingle · Tank Swap A/B<br>Dominoes · Poster · Worksheet + answers</div>
<div class="em">V = πr²h</div></div>
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
    pdf("teacher-pack", os.path.join(OUT, "Volume-Surface-Area-Nets-Teacher-Pack-Leim.pdf"))
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--hide-scrollbars", "--window-size=1200,1200",
                    f"--screenshot={os.path.join(OUT, f'{SLUG}-cover.png')}", f"{SLUG}-cover.html"], cwd=SRC, check=True, capture_output=True)
    print("domino chain:", [(x, a) for x, a in chain])
