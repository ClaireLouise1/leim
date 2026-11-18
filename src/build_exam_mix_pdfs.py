#!/usr/bin/env python3
"""Problem solving & exam mix (JC Maths topic 38): free sheet + teacher pack + Payhip cover.
Run from the repo root: python3 src/build_exam_mix_pdfs.py OUTDIR
Writes src/problem-solving-exam-mix-*.html; PDFs/cover PNG go to OUTDIR (free sheet also to printables/).
Every answer is worked out here with exact Fractions and asserted. Styles are read from src/build_money1_pdfs.py."""
import os, sys, random, subprocess, re, math
from fractions import Fraction as F
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC)
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/exammix"; os.makedirs(OUT, exist_ok=True)
SLUG = "problem-solving-exam-mix"
LO = "U.5, U.6, U.7, U.8, U.9, U.10, U.13"
GAME = "leim.ie/exam-mix.html"


def eu(x, sym="€"):
    x = F(x); c = x * 100; assert c.denominator == 1, ("not whole cents", x); c = int(c)
    return sym + (f"{c // 100:,}" if c % 100 == 0 else f"{c // 100:,}.{c % 100:02d}")
def hm(m):
    assert F(m).denominator == 1; m = int(m) % 1440; return f"{m // 60:02d}:{m % 60:02d}"
def dp(x, n):
    """round half up to n d.p., refusing values too near a rounding boundary"""
    s = float(x) * 10 ** n; assert abs(s - math.floor(s) - 0.5) > 0.01, ("near boundary", x); return f"{math.floor(s + 0.5) / 10 ** n:.{n}f}"
def ceil(x): return math.ceil(F(x))
def floor(x): return math.floor(F(x))
def isq(n):
    r = math.isqrt(int(n)); assert r * r == n, n; return r
def mean(xs): return F(sum(xs), len(xs))

# ---------- free sheet: 20 problems, every answer computed ----------
P = []   # (section, question html, answer text, short working)
def add(sec, q, a, w): P.append((sec, q, a, w))
per = 2 * (15 + 9); add("A", "A garden is 15 m by 9 m. Fencing costs €12 per metre. Find the cost of fencing all the way round.", eu(per * 12), f"Perimeter 2 × (15 + 9) = {per} m. {per} × €12")
add("A", "A €120 coat is reduced by 25%, then by 20% of the new price. Find the final price.", eu(F(120) * F(75, 100) * F(80, 100)), "€120 × 0.75 = €90, × 0.8")
sm = F(350) * 3 / 7; add("A", "€350 is shared in the ratio 3 : 4. The smaller share spends ⅓ of it. How much is left?", eu(sm - sm / 3), f"1 part = €50, smaller = {eu(sm)}, spends {eu(sm / 3)}")
add("A", "Seán earns €18 an hour for 37 hours, plus 5 hours overtime at time-and-a-half. Find his gross pay.", eu(18 * 37 + F(18) * F(3, 2) * 5), "€666 + 5 × €27")
add("A", "Aoife changes €300 to dollars at €1 = $1.10. She spends $175. How many dollars has she left?", eu(F(300) * F(11, 10) - 175, "$"), "€300 × 1.10 = $330")
km = (F(19) - 4) / F(3, 2); assert km.denominator == 1
add("B", "A taxi charges €4 plus €1.50 per km. A fare is €19. How far was the trip?", f"{km} km", "4 + 1.5k = 19, 1.5k = 15")
w7 = (F(50) / 2 - 5) / 2; add("B", "A rectangle has perimeter 50 cm. Its length is 5 cm more than its width. Find its area.", f"{w7 * (w7 + 5)} cm²", f"2w + 2(w + 5) = 50, w = {w7}")
st = floor((F(100) - 3) / 5); add("B", "Stage n of a pattern uses 5n + 3 tiles. You have 100 tiles. What is the biggest stage you can build?", f"Stage {st}", "5n + 3 ≤ 100, n ≤ 19.4")
g9 = F(12) / (5 - 3); add("B", "Plan A costs €12 a month + €3 per GB. Plan B costs €5 per GB. For how many GB do they cost the same?", f"{g9} GB", "12 + 3g = 5g")
A10 = F(7) * F(26, 10) * 2; t10 = ceil(A10 / 8); assert A10 % 8 != 0
add("C", "A wall is 7 m by 2.6 m. It needs 2 coats of paint. One tin covers 8 m². How many tins are needed?", f"{t10} tins", f"7 × 2.6 × 2 = {float(A10):g} m², ÷ 8 = {float(A10 / 8):g}, round up")
c11 = isq(20 ** 2 + 21 ** 2); add("C", "A field is 20 m by 21 m. How many metres do you save by walking the diagonal instead of along two sides?", f"{20 + 21 - c11} m", f"√(20² + 21²) = {c11} m")
L12 = F(60 * 40 * 50, 1000); m12 = L12 / 4; assert m12.denominator == 1
add("C", "A fish tank is 60 cm × 40 cm × 50 cm. It fills at 4 litres a minute. How long does it take to fill?", f"{m12} min", f"{60 * 40 * 50} cm³ = {L12} litres")
s13 = F(314, 100) * 15 * 15 / 8; add("C", "A pizza has radius 15 cm. It is cut into 8 equal slices. Find the area of one slice (π = 3.14), to 1 decimal place.", f"{dp(s13, 1)} cm²", "3.14 × 15² = 706.5, ÷ 8")
r14 = math.sqrt(1.2 ** 2 + 5 ** 2); add("C", "A ramp rises 1.2 m over a horizontal distance of 5 m. Find the length of the ramp, to 2 decimal places.", f"{dp(r14, 2)} m", "√(1.2² + 5²) = √26.44")
sc = [68, 74, 59, 81]; n15 = 72 * 5 - sum(sc); add("D", "Ben's first four test scores are 68, 74, 59 and 81. He wants a mean of 72 after five tests. What must he score in test 5?", str(n15), f"5 × 72 = 360, 360 − {sum(sc)}")
add("D", "A bag has 4 red and 11 blue counters. How many red counters must be added so that P(red) = ½?", str(11 - 4), "red must equal blue")
add("D", "A spinner lands on red with probability 0.35. It is spun 200 times. How many reds would you expect?", str(F(35, 100) * 200), "0.35 × 200")
m18 = (F(25 * 152) + 178) / 26; assert m18.denominator == 1
add("D", "25 students have a mean height of 152 cm. A new student who is 178 cm tall joins. Find the new mean height.", f"{m18} cm", "25 × 152 = 3800, + 178, ÷ 26")
t19 = F(210, 60) * 60; add("E", "A bus travels 210 km at 60 km/h. It leaves at 07:50. When does it arrive?", hm(7 * 60 + 50 + t19), "3.5 h = 3 h 30 min")
tot20 = F(240) * 6 * F(123, 100); add("E", "A school buys 6 tablets at €240 each, plus VAT at 23%. (a) Find the total cost. (b) It pays in 12 equal monthly amounts. Find each amount.",
                                      f"(a) {eu(tot20)} (b) {eu(tot20 / 12)}", "€1,440 × 1.23")
assert len(P) == 20 and P[0][2] == "€576" and P[1][2] == "€72" and P[2][2] == "€100" and P[3][2] == "€801" and P[4][2] == "$155"
assert [p[2] for p in P[5:9]] == ["10 km", "150 cm²", "Stage 19", "6 GB"]
assert [p[2] for p in P[9:14]] == ["5 tins", "12 m", "30 min", "88.3 cm²", "5.14 m"]
assert [p[2] for p in P[14:18]] == ["78", "7", "70", "153 cm"] and P[18][2] == "11:20" and P[19][2] == "(a) €1,771.20 (b) €147.60"

def style(var):
    return re.search(var + r' = f"""<!doctype.*?<style>(.*?)</style>', open(os.path.join(SRC, "build_money1_pdfs.py"), encoding="utf-8").read(), re.S).group(1).replace("{LO}", LO).replace("{{", "{").replace("}}", "}")
SHEET_STYLE = style("sheet"); PACK_STYLE = style("pack")
assert "@bottom-left" in SHEET_STYLE and "Single-teacher licence" in PACK_STYLE
EXTRA = """.wk{font-variant-numeric:tabular-nums;line-height:1.45;border:1.5px solid var(--line);border-radius:8px;padding:2px 7px;margin:3px 0;font-size:9.3pt}.wk b.h{display:block}
.st4{display:grid;grid-template-columns:repeat(4,1fr);gap:2mm;margin:2mm 0}.st4 div{border:1.5px solid var(--line);border-radius:8px;padding:2px 6px;font-size:8.8pt;line-height:1.35}.st4 b{display:block;font-size:11pt}"""
SECT = {"A": "A. Number and money", "B": "B. Algebra", "C": "C. Geometry and measure", "D": "D. Statistics and probability", "E": "E. Time and exam-style"}

def practice():
    out, k = [], 0
    for s in "ABCDE":
        items = [p for p in P if p[0] == s]
        out.append(f"<h2>{SECT[s]}</h2><ol class='q' start='{k + 1}'>" + "".join(f"<li>{q}<span class='line'></span></li>" for _, q, a, w in items) + "</ol>")
        k += len(items)
    return "".join(out)

sheet = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Problem solving and exam mix: tips and practice | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{SHEET_STYLE}
{EXTRA}
</style></head><body>
<div class="page tight">
  <div class="band"><div><div class="k">Junior Cycle Maths · Free revision sheet</div><h1>Problem solving &amp; exam mix</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2018 specification): {LO}. Play the game: <b>{GAME}</b></p>
  <p>Most exam questions join two or three topics: an <b>area</b> becomes a <b>cost</b>, a <b>speed</b> becomes a <b>clock time</b>. Each step is easy on its own. The skill is spotting the steps.</p>
  <h2>1. Four steps for any problem</h2>
  <div class="st4"><div><b>1. Read</b>Underline the numbers and units. What is the question asking for?</div><div><b>2. Plan</b>Which topic? What do I need first? Draw a sketch.</div><div><b>3. Do</b>One step per line. Say what each number is.</div><div><b>4. Check</b>Units? Sensible size? Rounded the right way? Answered the question?</div></div>
  <div class="two">
   <div><h2>2. Spot the hidden middle number</h2>
    <div class="wk"><b class="h">Garden 10 m by 6 m, fence €20 per m</b>Perimeter = 2 × (10 + 6) = <b>32 m</b> → 32 × €20 = <b>€640</b></div>
    <div class="wk"><b class="h">Wall 8 m by 3 m, 1 tin covers 5 m²</b>Area = <b>24 m²</b> → 24 ÷ 5 = 4.8 → <b>5 tins</b> (round up)</div>
    <div class="wk"><b class="h">150 km at 60 km/h, leaves 10:15</b>Time = 150 ÷ 60 = <b>2.5 h</b> = 2 h 30 min → <b>12:45</b></div>
    <div class="wk"><b class="h">Mean of 5 tests must be 70; first four add to 268</b>Total needed = 5 × 70 = <b>350</b> → 350 − 268 = <b>82</b></div>
    <h2>3. How marks are given</h2>
    <p>Each part is marked in steps. A right method with one slip still gets most of the marks; a bare wrong answer gets none. If part (a) is wrong but you use it correctly in part (b), you can still get (b).</p></div>
   <div><h2>4. Traps</h2>
    <ul>
     <li><b>Two discounts:</b> 20% off then 10% off is NOT 30% off. €100 → €80 → <b>€72</b>.</li>
     <li><b>Units:</b> 1 litre = 1000 cm³ · 1 m = 100 cm · 1 m² = 10,000 cm². Change them first.</li>
     <li><b>Rounding:</b> tins, buses, boxes → round <b>up</b>. "How many can you build / buy?" → round <b>down</b>.</li>
     <li><b>Time:</b> 1.25 h = 1 h 15 min, not 1 h 25 min. 0.1 h = 6 min.</li>
     <li><b>Working backwards:</b> after a 23% VAT rise, divide by 1.23 (not take away 23%).</li>
     <li><b>Read the last line again:</b> "how much is LEFT", "how many MORE", "to 1 decimal place".</li>
    </ul>
    <div class="note"><b>Which topic is it?</b> "fence, border, edge" → perimeter · "cover, paint, carpet" → area · "fill, hold, litres" → volume · "km/h, arrive" → speed and time · "per hour, overtime, tax" → money · "chance, likely" → probability · "average" → mean.</div></div>
  </div>
  <div class="tip"><b>Exam tip:</b> never leave a part blank. Write the formula or the first step: it can earn marks. Then move on and come back.</div>
</div>

<div class="page p2">
  <div class="band"><div><div class="k">Practice · 20 problems</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <p style="margin:0">Show every step. Use a calculator where you need one.</p>
  {practice()}
</div>

<div class="page">
  <div class="band"><div><div class="k">Check your work</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <table class="ans"><tbody>{"".join(f"<tr><td><b>{i}</b></td><td><b>{a}</b> &nbsp;<span style='color:var(--muted)'>({w})</span></td></tr>" for i, (s, q, a, w) in enumerate(P, 1))}</tbody></table>
  <h2>Worked examples</h2>
  <div class="two">
   <div class="wk"><b class="h">2. Two discounts</b>25% off: €120 × 0.75 = €90. 20% off the new price: €90 × 0.8 = <b>€72</b>. (45% off would give €66: wrong.)</div>
   <div class="wk"><b class="h">8. Biggest stage</b>5n + 3 ≤ 100 → 5n ≤ 97 → n ≤ 19.4. Stage 20 needs 103 tiles, so the answer is <b>Stage 19</b> (round down).</div>
   <div class="wk"><b class="h">12. Fish tank</b>60 × 40 × 50 = 120,000 cm³. 1 litre = 1000 cm³, so 120 litres. 120 ÷ 4 = <b>30 minutes</b>.</div>
   <div class="wk"><b class="h">19. Arrival time</b>210 ÷ 60 = 3.5 h = 3 h 30 min. 07:50 + 3 h = 10:50, + 30 min = <b>11:20</b>.</div>
  </div>
  <div class="note"><b>Got one wrong?</b> Which step went wrong: the plan, the units, the rounding? Then play <b>Exam Mix</b> at {GAME}: each question shows which topic it's from, and the end screen links to the game for that topic.</div>
  <p class="small">All questions written by Léim. Léim is independent and not connected with the State Examinations Commission or the NCCA.</p>
</div>
</body></html>"""
assert F(90) * F(8, 10) == 72 and F(120) * F(55, 100) == 66 and 5 * 20 + 3 == 103 and 3 * 60 + 30 == 210

# ---------- teacher pack ----------
# Two-Step Match: 12 problem cards <-> 12 answer cards, all answers different
MATCH = [("Fence an 8 m × 5 m garden at €10 a metre", eu(2 * (8 + 5) * 10)),
         ("€60 coat: 30% off, then 10% off", eu(F(60) * F(7, 10) * F(9, 10))),
         ("120 km at 80 km/h, leave 09:30. Arrive?", hm(9 * 60 + 30 + F(120, 80) * 60)),
         ("Mean of 4, 8, 9 and x is 8. Find x.", str(8 * 4 - (4 + 8 + 9))),
         ("Wall 6 m × 2.5 m. 1 tin covers 4 m². Tins?", f"{ceil(F(6) * F(5, 2) / 4)} tins"),
         ("€90 shared 2 : 3. The bigger share?", eu(F(90) * 3 / 5)),
         ("Tank 50 cm × 40 cm × 30 cm. Litres?", f"{F(50 * 40 * 30, 1000)} litres"),
         ("Walk the diagonal of a 6 m × 8 m field", f"{isq(36 + 64)} m"),
         ("€9 an hour for 6 h + 2 h at time-and-a-half", eu(9 * 6 + F(27, 2) * 2)),
         ("Stage n: 4n + 1 tiles. 50 tiles. Biggest stage?", f"Stage {floor(F(49, 4))}"),
         ("3 red, 5 blue. Add 2 red. P(red)?", "½"),
         ("€200 + 23% VAT, paid in 4 equal parts", eu(F(200) * F(123, 100) / 4))]
assert F(3 + 2, 3 + 2 + 5) == F(1, 2)
assert [a for q, a in MATCH] == ["€260", "€37.80", "11:00", "11", "4 tins", "€54", "60 litres", "10 m", "€81", "Stage 12", "½", "€61.50"]
assert len({a for q, a in MATCH}) == 12
random.seed(38); order = list(range(24)); random.shuffle(order)
cards = [("q", i) for i in range(12)] + [("a", i) for i in range(12)]
match_print = [cards[k] for k in order]
match_html = "".join(f'<div class="c"><span class="tag">Card {k}</span><div class="fc{" qq" if t == "q" else ""}">{MATCH[i][1] if t == "a" else MATCH[i][0]}</div></div>' for k, (t, i) in enumerate(match_print, 1))
match_key = " · ".join(f"{match_print.index(('q', i)) + 1} → {match_print.index(('a', i)) + 1}" for i in range(12))

# Problem Swap: each fact on exactly ONE card
SW1 = [("Distance to the museum", "126 km", "A"), ("Average bus speed", "72 km/h", "B"), ("Bus leaves school at", "09:15", "A"),
       ("Students going", "52", "A"), ("Seats on one bus", "30", "B"), ("Cost of one bus", "€350", "B"),
       ("Journey time", "", None), ("Arrival time", "", None), ("Buses needed", "", None), ("Bus cost per student (to the cent)", "", None)]
jt = F(126, 72) * 60; assert jt == 105
buses = ceil(F(52, 30)); per_st = F(350 * buses, 52)
SW1_ans = ["1 h 45 min", hm(9 * 60 + 15 + jt), str(buses), "€" + dp(per_st, 2)]
assert SW1_ans == ["1 h 45 min", "11:00", "2", "€13.46"]
SW2 = [("Patio length", "7.5 m", "A"), ("Patio width", "4 m", "B"), ("One slab", "0.5 m × 0.5 m", "A"), ("Price of one slab", "€3.20", "B"),
       ("Area", "", None), ("Perimeter (for the edging)", "", None), ("Slabs needed", "", None), ("Cost of the slabs", "", None)]
ar = F(15, 2) * 4; slabs = ar / F(1, 4); assert slabs.denominator == 1
SW2_ans = [f"{ar} m²", f"{2 * (F(15, 2) + 4)} m", str(slabs), eu(slabs * F(16, 5))]
assert SW2_ans == ["30 m²", "23 m", "120", "€384"]
for rows in (SW1, SW2): assert sum(w == "A" for *_, w in rows) >= 1 and sum(w == "B" for *_, w in rows) >= 1
keys = [k for rows in (SW1, SW2) for k, v, w in rows if w]; assert len(keys) == len(set(keys))
def swap_card(who):
    def tab(title, rows):
        return f'<table class="ss"><thead><tr><th colspan="2">{title}</th></tr></thead><tbody>' + "".join(
            f"<tr><td>{k}</td><td><b>{v if w == who else ''}</b></td></tr>" for k, v, w in rows) + "</tbody></table>"
    return f'<div class="idc"><h3>Student {who} · Problem Swap</h3><div class="two">{tab("The school trip", SW1)}{tab("The new patio", SW2)}</div></div>'

# Mixed Dominoes: 20 clues from every strand, 20 different answers (all checked)
q17 = [x for x in range(-10, 11) if x * x - 5 * x + 6 == 0]; assert q17 == [2, 3]
DOMS = [("(−3) × (−4) + 2", str((-3) * (-4) + 2)), ("15% of 80", str(F(15, 100) * 80)), ("3x + 5 = 26", f"x = {F(26 - 5, 3)}"),
        ("Higher Level: √50 as a√b", "5√2"), ("2⁵", str(2 ** 5)), ("Mean of 3, 7, 8", str(mean([3, 7, 8]))),
        ("Triangle: 50°, 60° and ?", f"{180 - 50 - 60}°"), ("Area of a circle, r = 10, π = 3.14", f"{F(314, 100) * 100} cm²"),
        ("Hypotenuse: sides 5 and 12", str(isq(25 + 144))), ("€40 + 23% VAT", eu(F(40) * F(123, 100))), ("Factorise x² − 9", "(x − 3)(x + 3)"),
        ("Slope through (0, 1) and (2, 7)", str(F(7 - 1, 2 - 0))), ("P(even) on a fair die", "½"), ("Volume: 2 cm × 3 cm × 4 cm", f"{2 * 3 * 4} cm³"),
        ("150 km in 2.5 hours: speed", f"{F(150) / F(5, 2)} km/h"), ("Next term: 2, 6, 18, …", str(18 * 3)), ("x² − 5x + 6 = 0", "x = 2 or x = 3"),
        ("f(x) = 2x − 1. Find f(5).", str(2 * 5 - 1)), ("tan 45°", str(round(math.tan(math.radians(45))))), ("Median of 4, 9, 2, 7, 5", str(sorted([4, 9, 2, 7, 5])[2]))]
assert F(314, 100) * 100 == 314 and F(3, 6) == F(1, 2)
assert [a for c, a in DOMS] == ["14", "12", "x = 7", "5√2", "32", "6", "70°", "314 cm²", "13", "€49.20", "(x − 3)(x + 3)", "3", "½", "24 cm³", "60 km/h", "54", "x = 2 or x = 3", "9", "1", "5"]
assert len(DOMS) == 20 and len({a for c, a in DOMS}) == 20
assert 25 * 2 == 50 and 3 * 3 == 9 and (3 * 3 - 9) == 0
random.seed(3838); chain = DOMS[:]; random.shuffle(chain)
dom = [("START" if k == 0 else chain[k - 1][1], x[0]) for k, x in enumerate(chain)] + [(chain[-1][1], "FINISH")]
dom_print = dom[:]; random.shuffle(dom_print)
dom_html = "".join(f'<div class="dom"><div class="h l{" sm" if len(l) > 6 else ""}">{l}</div><div class="h r">{r}</div></div>' for l, r in dom_print)
chain_key = "".join(f"<li>{x} = <b>{a}</b></li>" for x, a in chain)

ERR = [("Jacket €80: 20% off, then 10% off", "€56", "It's not 30% off. €80 × 0.8 = €64, × 0.9 = <b>€57.60</b>", "€57.60", eu(F(80) * F(8, 10) * F(9, 10))),
       ("Wall 9 m². 1 tin covers 2 m². Tins?", "4 tins", "9 ÷ 2 = 4.5: round UP. <b>5 tins</b>", "5 tins", f"{ceil(F(9, 2))} tins"),
       ("200 km at 80 km/h, leave 10:00. Arrive?", "12:50", "2.5 h is 2 h 30 min, not 2 h 50 min: <b>12:30</b>", "12:30", hm(600 + F(200, 80) * 60)),
       ("Mean of 5 tests must be 70. First four add to 268. Test 5?", "70", "Total needed 5 × 70 = 350. 350 − 268 = <b>82</b>", "82", str(5 * 70 - 268)),
       ("Tank 40 cm × 30 cm × 25 cm. Litres?", "30,000 litres", "That's cm³. ÷ 1000: <b>30 litres</b>", "30 litres", f"{F(40 * 30 * 25, 1000)} litres"),
       ("€15 an hour, 38 h + 4 h overtime at time-and-a-half", "€630", "Overtime is €22.50 an hour: €570 + €90 = <b>€660</b>", "€660", eu(15 * 38 + F(45, 2) * 4))]
for q, wrong, r, good, calc in ERR: assert good == calc and wrong != good, (q, good, calc)
assert 40 * 30 * 25 == 30000 and 15 * 42 == 630 and F(80) * F(7, 10) == 56
# worksheet exam-style
WS1 = [F(12) * F(15, 2), None, None]; WS1[1] = ceil(WS1[0] / 20); WS1[2] = eu(WS1[1] * F(17, 2))
assert WS1[0] == 90 and WS1[1] == 5 and WS1[2] == "€42.50"
WS2 = [10 + 2 * 4, 4 * 4, F(10, 4 - 2), 10 + 2 * 8, 4 * 8]; assert WS2 == [18, 16, 5, 26, 32]
h3 = math.sqrt(5 ** 2 - 1.4 ** 2); a3 = math.degrees(math.acos(1.4 / 5)); assert dp(h3, 1) == "4.8" and dp(a3, 0) == "74"
WS4 = [F(40 - 12 - 18, 40) * 100, F(18, 40) * 360, F(12, 40)]; assert WS4 == [25, 162, F(3, 10)]
V5 = math.pi * 0.5 ** 2 * 1.2 * 1000; m5 = V5 / 15; assert dp(m5, 0) == "63"

pack = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Problem Solving &amp; Exam Mix Teacher Pack | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{PACK_STYLE}
{EXTRA}
.ss td:nth-child(2){{width:34%}}.ss td,.ss th{{padding:1px 4px;font-size:8.2pt;line-height:1.2}}.fym{{grid-template-columns:repeat(4,1fr)}}.fym .c{{height:13.5mm}}.fym .fc{{font-size:13pt}}.fym .fc.qq{{font-size:8.2pt;line-height:1.2;font-weight:600}}.idc{{padding:1mm 4mm}}.idc h3{{margin:0 0 1mm}}.p1 .proc td{{font-size:8.5pt;padding:2px 6px}}
.dom .r{{font-size:9.5pt}}.dom .l{{font-size:14pt}}.dom .l.sm{{font-size:10.5pt}}.ops div{{font-size:12pt}}
</style></head><body>

<div class="page p1">
  <div class="band"><div><div class="k">Junior Cycle Maths · Teacher pack</div><h1>Problem solving &amp; exam mix</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2018 specification): {LO}</p>
  <div class="two">
    <div><h3>Aims</h3><p>By the end of the lesson students can break a problem in context into steps, choose the right topic for each step, find the hidden middle number (a perimeter, an area, a time), use the right units and rounding, check that an answer makes sense, and set out their work so it earns step marks. A good revision lesson for 3rd year before the exam.</p></div>
    <div><h3>In this pack</h3><p>p.1 Teacher notes · p.2 Two-Step Match mingle cards + Problem Swap A/B cards · p.3 Mixed Dominoes (cut-up) · p.4 Wall poster · p.5 Worksheet: Error Hunt + exam-style questions · p.6 Answers. Level: 2nd and 3rd year (Ordinary and Higher; one question marked Higher Level). Time: about 60 minutes. Calculators needed. All questions are original.</p></div>
  </div>
  <h2 style="margin-top:8px">Procedure</h2>
  <table class="proc"><tbody>
    <tr><td>5 min</td><td><b>Lead-in: what's the hidden number?</b> Board: "Garden 10 m by 6 m. Fence €20 a metre. Cost?" Students write ONLY the number they need first (32 m). Elicit that most exam questions hide a middle step.</td></tr>
    <tr><td>8 min</td><td><b>Guided discovery.</b> Pairs sort three problems (wall + tins, journey + arrival time, five test scores) by "what do I find first?". Elicit the four steps Read · Plan · Do · Check, and two traps: round tins UP, 2.5 h = 2 h 30 min.</td></tr>
    <tr><td>10 min</td><td><b>Two-Step Match mingle</b> (p.2, 24 cards = 12 problem cards + 12 answer cards; one card each; calculators allowed). Find your partner, then tell the class your hidden middle number.</td></tr>
    <tr><td>12 min</td><td><b>Problem Swap</b> (p.2, pairs, don't show your card). Each fact is on only ONE card. Ask for what you're missing, then fill in the blanks together. Feedback: trip → <b>{SW1_ans[0]}, {SW1_ans[1]}, {SW1_ans[2]} buses, {SW1_ans[3]}</b>; patio → <b>{", ".join(SW2_ans[:2])}, {SW2_ans[2]} slabs, {SW2_ans[3]}</b>.</td></tr>
    <tr><td>10 min</td><td><b>Mixed Dominoes</b> (p.3), groups of 3–4. Start with START, work out the clue, find the domino with that answer on its left, and build the chain to FINISH. Every strand is in the chain.</td></tr>
    <tr><td>12 min</td><td><b>Worksheet</b> (p.5). Error Hunt in pairs (find the mistake, name it, fix it), then the exam-style questions alone. Question 5 is Higher Level.</td></tr>
    <tr><td>3 min</td><td><b>Exit ticket.</b> "A room is 5 m by 4 m. Carpet costs €25 per m². Cost?" (€500.) Which step is the hidden one? Homework: play <b>Exam Mix</b> at {GAME}.</td></tr>
  </tbody></table>
  <div class="note"><b>Mingle key</b> (problem card → answer card): {match_key}.<br>
  <b>Errors to look for:</b> adding two percentage discounts · rounding tins or buses down · 2.5 h read as 2 h 50 min · cm³ given as litres · overtime paid at double. <b>Support:</b> a "which topic?" key-word list on the desk (fence → perimeter, cover → area, fill → volume). <b>Fast finishers:</b> write your own two-step problem for a partner.</div>
  <p class="small"><b>Domino answer chain</b> (START → FINISH):</p>
  <ol class="small" style="columns:2;column-gap:12px;font-size:7.4pt;line-height:1.22;margin:0;padding-left:16px">{chain_key}</ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">Cut up the cards · one Problem Swap card per student</div><h1>Two-Step Match + Problem Swap</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:8.8pt;margin:0"><b>Two-Step Match mingle.</b> Cut out the 24 cards and give one to each student. Problem card? Work it out and find your answer. Answer card? Find the problem that gives it. (Fewer students? Take out whole pairs.)</p>
  <div class="fym">{match_html}</div>
  <p style="font-size:8.8pt;margin:3mm 0 0"><b>Problem Swap.</b> Don't show your card. Each fact is on only one of the two cards: ask your partner for what you're missing, then fill in every blank together.</p>
  {swap_card("A")}
  {swap_card("B")}
</div>

<div class="page">
  <div class="band"><div><div class="k">Groups of 3–4 · cut along the dashed lines</div><h1>Mixed Dominoes</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.4pt">Start with START. Work out the clue on the right, then find the domino with that answer on its left. Keep going until you reach FINISH. One clue is marked Higher Level (Ordinary Level groups can be given that answer).</p>
  <div class="doms">{dom_html}</div>
</div>

<div class="page">
  <div class="poster">
    <h1>Solve any problem</h1>
    <div class="ops">
      <div style="background:var(--green-soft)"><b>1. Read</b>numbers + units<br>What is the question<br>asking for?</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>2. Plan</b>Which topic?<br>What do I need first?<br>Draw a sketch.</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>3. Do</b>one step per line<br>Say what each<br>number is.</div>
      <div style="background:var(--green-soft)"><b>4. Check</b>units · size<br>rounding<br>answered it?</div>
    </div>
    <p style="text-align:center;font-size:17pt!important;font-weight:800;margin:4mm 0">20% off, then 10% off ≠ 30% off</p>
    <p style="text-align:center;font-size:13pt!important;margin:2mm 0">Tins and buses: round <b>up</b> · 1 litre = 1000 cm³ · 2.5 h = 2 h 30 min</p>
    <p style="text-align:center;font-size:10pt;color:var(--muted)">Léim · leim.ie · Play Exam Mix: {GAME}</p>
  </div>
</div>

<div class="page ws">
  <div class="band"><div><div class="k">Worksheet</div><h1>Error Hunt + exam-style questions</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Error Hunt</h2>
  <p>Each student's answer has one mistake. Find it, say what went wrong, and write the right answer.</p>
  <table class="eh"><thead><tr><th>Question</th><th>Student's answer</th><th>The mistake and the right answer</th></tr></thead><tbody>
  {"".join(f"<tr><td>{q}</td><td>{w}</td><td><span class='gap'></span><span class='gap'></span></td></tr>" for q, w, r, g, c in ERR)}
  </tbody></table>
  <h2>B. Exam-style questions (show all your work)</h2>
  <ol class="q">
    <li>A lawn is 12 m by 7.5 m. One box of seed covers 20 m² and costs €8.50. (a) Find the area. (b) How many boxes are needed? (c) Find the cost.<span class="long"></span></li>
    <li>Plan A costs €10 a month + €2 per GB. Plan B costs €4 per GB. (a) Find the cost of 4 GB on each plan. (b) For how many GB do they cost the same? (c) Which plan is cheaper for 8 GB?<span class="long"></span></li>
    <li>A 5 m ladder leans against a wall. Its foot is 1.4 m from the wall. (a) How high up the wall does it reach? (b) Find the angle it makes with the ground, to the nearest degree.<span class="long"></span></li>
    <li>In a survey of 40 students, 12 walk to school, 18 get the bus and the rest come by car. (a) What percentage come by car? (b) Find the pie-chart angle for bus. (c) One student is picked at random. Find P(walks).<span class="long"></span></li>
    <li>Higher Level: a cylinder-shaped tank has radius 0.5 m and height 1.2 m. Water flows in at 15 litres a minute. How long does it take to fill, to the nearest minute? (1 m³ = 1000 litres)<span class="long"></span></li>
  </ol>
</div>

<div class="page an">
  <div class="band"><div><div class="k">For the teacher</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>Problem Swap</h2>
  <div class="two"><table><tbody>
   <tr><td>Journey time</td><td>126 ÷ 72 = 1.75 h = <b>{SW1_ans[0]}</b></td></tr><tr><td>Arrival</td><td>09:15 + 1 h 45 min = <b>{SW1_ans[1]}</b></td></tr>
   <tr><td>Buses</td><td>52 ÷ 30 = 1.7…, round up: <b>{SW1_ans[2]}</b></td></tr><tr><td>Per student</td><td>2 × €350 = €700, ÷ 52 = <b>{SW1_ans[3]}</b></td></tr></tbody></table>
  <table><tbody>
   <tr><td>Area</td><td>7.5 × 4 = <b>{SW2_ans[0]}</b></td></tr><tr><td>Perimeter</td><td>2 × (7.5 + 4) = <b>{SW2_ans[1]}</b></td></tr>
   <tr><td>Slabs</td><td>one slab = 0.25 m², 30 ÷ 0.25 = <b>{SW2_ans[2]}</b></td></tr><tr><td>Cost</td><td>120 × €3.20 = <b>{SW2_ans[3]}</b></td></tr></tbody></table></div>
  <h2>A. Error Hunt</h2>
  <table><tbody>{"".join(f"<tr><td style='width:40%'><b>{q}</b></td><td>{r}</td></tr>" for q, w, r, g, c in ERR)}</tbody></table>
  <h2>B. Exam-style questions</h2>
  <ol class="q">
    <li>(a) 12 × 7.5 = <b>{WS1[0]} m²</b> (b) 90 ÷ 20 = 4.5 → <b>{WS1[1]} boxes</b> (c) 5 × €8.50 = <b>{WS1[2]}</b></li>
    <li>(a) A: €10 + €8 = <b>€{WS2[0]}</b>; B: <b>€{WS2[1]}</b> (b) 10 + 2g = 4g → <b>{WS2[2]} GB</b> (c) A: €{WS2[3]}, B: €{WS2[4]}, so <b>Plan A</b></li>
    <li>(a) √(5² − 1.4²) = √23.04 = <b>{dp(h3, 1)} m</b> (b) cos A = 1.4 ÷ 5 = 0.28, A = <b>{dp(a3, 0)}°</b></li>
    <li>(a) 10 by car: 10 ÷ 40 = <b>{WS4[0]}%</b> (b) 18/40 × 360° = <b>{WS4[1]}°</b> (c) 12/40 = <b>3/10</b></li>
    <li>V = π × 0.5² × 1.2 = 0.942… m³ = 942.5 litres. 942.5 ÷ 15 = 62.8 → <b>{dp(m5, 0)} minutes</b></li>
  </ol>
  <h2>Marking tip</h2>
  <p>Mark in steps, as the exam does: the hidden middle number (perimeter, area, time), the second step done with it, then units and rounding. If a student's first step is wrong but used correctly afterwards, give the later marks.</p>
</div>
</body></html>"""

cover = """<!doctype html><html><head><meta charset="utf-8"><style>
body{margin:0;width:1200px;height:1200px;background:#1B2430;font-family:Inter,sans-serif;color:#fff;display:flex;flex-direction:column;justify-content:space-between;padding:90px;box-sizing:border-box}
.k{display:inline-block;background:#2E7D57;border-radius:99px;padding:12px 26px;font-weight:700;font-size:28px;letter-spacing:.06em;text-transform:uppercase}
h1{font-size:104px;font-weight:800;line-height:1.18;letter-spacing:-.02em;margin:56px 0 20px}
h1 span{background:#F6CF5A;color:#1B2430;padding:0 18px;border-radius:14px;-webkit-box-decoration-break:clone;box-decoration-break:clone}
.sub{font-size:40px;line-height:1.4;color:#DDE3EA}
.em{font-size:46px;margin-top:30px;font-weight:800;letter-spacing:.01em;color:#F6CF5A}
.foot{display:flex;justify-content:space-between;align-items:center;font-size:34px;font-weight:700}
.price{background:#F6CF5A;color:#1B2430;border-radius:16px;padding:14px 28px}
</style></head><body>
<div><span class="k">Junior Cycle Maths · Teacher pack</span>
<h1><span>Problem Solving</span><br><span>&amp; Exam Mix</span></h1>
<div class="sub">Two-Step Match mingle · Problem Swap A/B<br>Dominoes · Poster · Worksheet + answers</div>
<div class="em">Read · Plan · Do · Check</div></div>
<div class="foot"><span>↗ Léim · leim.ie</span><span class="price">Ready to teach · 60 min</span></div>
</body></html>"""

if __name__ == "__main__":
    for name, txt in [("rules-and-practice", sheet), ("teacher-pack", pack), ("cover", cover)]:
        plain = re.sub(r"<[^>]+>", " ", re.sub(r"<style>.*?</style>|<svg.*?</svg>", "", txt, flags=re.S))
        assert not re.search(r"[\d)]\s*-\s*[\d(√]|[=(]\s*-\d|(?<![\w])-\d", plain), (name, re.findall(r".{20}[\d)]\s*-\s*[\d(].{10}", plain)[:3])
        open(os.path.join(SRC, f"{SLUG}-{name}.html"), "w", encoding="utf-8").write(txt)
    def pdf(name, out):
        subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--no-pdf-header-footer", f"--print-to-pdf={out}",
                        f"{SLUG}-{name}.html"], cwd=SRC, check=True, capture_output=True)
        d = open(out, "rb").read(); print(name, len(re.findall(rb"/Type\s*/Page[^s]", d)), "pages")
    pdf("rules-and-practice", os.path.join(ROOT, "printables", f"{SLUG}-rules-and-practice.pdf"))
    pdf("teacher-pack", os.path.join(OUT, "Problem-Solving-Exam-Mix-Teacher-Pack-Leim.pdf"))
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--hide-scrollbars", "--window-size=1200,1200",
                    f"--screenshot={os.path.join(OUT, f'{SLUG}-cover.png')}", f"{SLUG}-cover.html"], cwd=SRC, check=True, capture_output=True)
    print("domino chain:", chain)
