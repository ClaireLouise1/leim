#!/usr/bin/env python3
"""Speed, distance, time & currency (JC Maths topic 20): free sheet + teacher pack + Payhip cover.
Run from the repo root: python3 src/build_speed_currency_pdfs.py OUTDIR
Writes src/speed-distance-time-currency-*.html; PDFs/cover PNG go to OUTDIR (free sheet also to printables/).
Every answer is computed with Python's Fraction and asserted. Styles are read from src/build_money1_pdfs.py."""
import os, sys, random, subprocess, re
from fractions import Fraction as F
from math import floor
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC)
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/speed"; os.makedirs(OUT, exist_ok=True)
SLUG = "speed-distance-time-currency"
LO = "N.3b, GT.1, U.6"

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
def cent(x): x = F(x); return F(floor(x * 100 + F(1, 2)), 100)     # nearest cent, half up
def mon(sym, x):
    x = F(x); assert (x * 100).denominator == 1, x; c = int(x * 100)
    return sym + "{:,}.{:02d}".format(c // 100, c % 100)
def e(x): return mon("€", x)
def kmh(x, dp=None): return dec(x, dp) + " km/h"
def km(x): return dec(x) + " km"
def hm(t):
    t = F(t); assert t.denominator == 1, t; t = int(t); h, m = divmod(t, 60)
    return f"{h} h {m} min" if h and m else f"{h} h" if h else f"{m} min"
def clk(t): t = int(t) % 1440; return f"{t // 60:02d}:{t % 60:02d}"
def tm(h, m=0): return h * 60 + m
def speed(d, t): return F(d) * 60 / t          # km, minutes → km/h
def ttime(d, s): return F(d) * 60 / F(s)        # km, km/h → minutes
assert hm(150) == "2 h 30 min" and clk(tm(8, 50) + 150) == "11:20" and e(cent(F(250) / F("1.08"))) == "€231.48" and dec(1234.5) == "1,234.5"

# ---------- distance-time graph (same look as the game) ----------
def graph(start, pts, names, box="width:100%"):
    T = pts[-1][0]; mx = max(d for t, d in pts); sy = 10 if mx <= 60 else 20; Y = -(-mx // sy) * sy; Tm = -(-T // 30) * 30
    x0, x1, y0, y1 = 46, 326, 200, 18
    X = lambda t: x0 + (x1 - x0) * t / Tm; Yc = lambda d: y0 - (y0 - y1) * d / Y
    o = [f'<svg viewBox="0 0 340 238" style="{box}" class="dtg">']
    for t in range(0, Tm + 1, 15): o.append(f'<line x1="{X(t):.2f}" y1="{y1}" x2="{X(t):.2f}" y2="{y0}" stroke="{"#E3E8ED" if t % 30 else "#C2CCD6"}" stroke-width=".7"/>')
    d = 0
    while d <= Y:
        o.append(f'<line x1="{x0}" y1="{Yc(d):.2f}" x2="{x1}" y2="{Yc(d):.2f}" stroke="{"#E3E8ED" if d % sy else "#C2CCD6"}" stroke-width=".7"/>'); d += sy / 2
    for t in range(0, Tm + 1, 30): o.append(f'<text x="{X(t):.2f}" y="{y0 + 14}" font-size="9.5" font-weight="600" text-anchor="middle">{clk(start + t)}</text>')
    for d in range(0, Y + 1, sy): o.append(f'<text x="{x0 - 5}" y="{Yc(d) + 4:.2f}" font-size="9.5" font-weight="600" text-anchor="end">{d}</text>')
    o.append(f'<text x="{(x0 + x1) / 2}" y="234" font-size="10" font-weight="700" fill="#5B6573" text-anchor="middle">Time</text>')
    o.append(f'<text x="11" y="{(y0 + y1) / 2}" font-size="10" font-weight="700" fill="#5B6573" text-anchor="middle" transform="rotate(-90 11 {(y0 + y1) / 2})">Distance from home (km)</text>')
    o.append(f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y0}" stroke="#1B2430" stroke-width="1.3"/><line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y1}" stroke="#1B2430" stroke-width="1.3"/>')
    o.append('<polyline fill="none" stroke="#2E7D57" stroke-width="2.6" stroke-linejoin="round" points="' + " ".join(f"{X(t):.2f},{Yc(d):.2f}" for t, d in pts) + '"/>')
    for i, (t, d) in enumerate(pts):
        o.append(f'<circle cx="{X(t):.2f}" cy="{Yc(d):.2f}" r="3.4" fill="#1B2430"/>')
        if i: o.append(f'<text x="{X(t) - (10 if i == len(pts) - 1 else 0):.2f}" y="{Yc(d) - 8:.2f}" font-size="12" font-weight="800" fill="#C0392B" text-anchor="middle">{names[i]}</text>')
    return "".join(o) + "</svg>"
def segs(pts, names): return [(names[i], names[i + 1], pts[i + 1][1] - pts[i][1], pts[i + 1][0] - pts[i][0]) for i in range(len(pts) - 1)]

# ---------- free sheet ----------
A = [("A car travels 240 km in 3 hours. Find its average speed.", kmh(speed(240, 180))),
     ("A bus travels at 60 km/h for 2 h 30 min. How far does it go?", km(60 * F(150, 60))),
     ("How long does it take to travel 180 km at 72 km/h?", hm(ttime(180, 72))),
     ("Write 1 h 45 min in hours, as a decimal.", dec(F(105, 60)) + " hours"),
     ("Write 2.4 hours in hours and minutes.", hm(F("2.4") * 60)),
     ("A train travels 117 km in 1 h 18 min. Find its average speed.", kmh(speed(117, 78))),
     ("Kate leaves at 08:50 and drives 195 km at 78 km/h. When does she arrive?", clk(tm(8, 50) + ttime(195, 78))),
     ("A cyclist rides at 18 km/h for 40 minutes. How far does she go?", km(18 * F(40, 60)))]
assert [a for q, a in A] == ["80 km/h", "150 km", "2 h 30 min", "1.75 hours", "2 h 24 min", "90 km/h", "11:20", "12 km"], [a for q, a in A]
B = [("Seán drives 100 km in 1 h 15 min, then 80 km in 45 min. Find his average speed for the whole journey.", kmh(speed(180, 120))),
     ("A lorry travels for 2 hours at 90 km/h, then 1 hour at 60 km/h. Find its average speed.", kmh(F(2 * 90 + 60, 3))),
     ("Méabh cycles 60 km to the lake at 30 km/h and back at 20 km/h. Find her average speed for the round trip.", kmh(F(120, F(60, 30) + F(60, 20)))),
     ("Change 72 km/h into metres per second.", dec(F(72000, 3600)) + " m/s"),
     ("Change 15 m/s into km/h.", kmh(15 * F(36, 10))),
     ("Oisín runs 400 m in 50 seconds. Find his average speed in m/s.", dec(F(400, 50)) + " m/s"),
     ("Ciara drives 150 km in 2 h, stops for 30 min, then drives 120 km in 1 h 30 min. Find her average speed, including the stop.", kmh(speed(270, 120 + 30 + 90)))]
assert [a for q, a in B] == ["90 km/h", "80 km/h", "24 km/h", "20 m/s", "54 km/h", "8 m/s", "67.5 km/h"], [a for q, a in B]
GS, GP, GN = 780, [(0, 0), (45, 30), (75, 30), (105, 55), (165, 0)], "OABCD"
SG = segs(GP, GN); sp = {f"{a} to {b}": speed(abs(dd), dt) for a, b, dd, dt in SG}
assert sp == {"O to A": 40, "A to B": 0, "B to C": 50, "C to D": 55}
Cq = [("How far from home was Ruth at 13:45?", km(30)),
      ("How long did Ruth stop for?", hm(30)),
      ("Find Ruth's speed from O to A.", kmh(sp["O to A"])),
      ("Find Ruth's speed from B to C.", kmh(sp["B to C"])),
      ("Find Ruth's speed from C to D.", kmh(sp["C to D"])),
      ("On which part was Ruth fastest? How can you tell from the graph?", "C to D (steepest)"),
      ("Find Ruth's average speed for the whole journey, including the stop.", kmh(speed(sum(abs(s[2]) for s in SG), GP[-1][0])))]
assert Cq[-1][1] == "40 km/h" and GP[1] == (45, 30)
p29 = cent(F(85) / F("0.86")); assert p29 == F("98.84")
D = [("€1 = £0.86. Change €400 into sterling.", mon("£", 400 * F("0.86"))),
     ("€1 = $1.08. Change €750 into US dollars.", mon("$", 750 * F("1.08"))),
     ("€1 = £0.86. Change £172 into euro.", e(F(172) / F("0.86"))),
     ("€1 = $1.08. Change $250 into euro, to the nearest cent.", e(cent(F(250) / F("1.08")))),
     ("A bank takes 2% commission, then changes the rest at €1 = $1.10. How many dollars do you get for €500?", mon("$", 500 * F("0.98") * F("1.1"))),
     ("Ultan changes €300 and gets £258. Find the rate: €1 = £?", "£" + dec(F(258, 300))),
     ("Headphones cost £85 in Newry and €96 in Dundalk. €1 = £0.86. Where are they cheaper, and by how much?", f"Dundalk, by {e(p29 - 96)}"),
     ("€1 = CHF 0.94. Change €620 into Swiss francs.", mon("CHF ", 620 * F("0.94")))]
assert [a for q, a in D] == ["£344.00", "$810.00", "€200.00", "€231.48", "$539.00", "£0.86", "Dundalk, by €2.84", "CHF 582.80"], [a for q, a in D]
# exam-style
e1t = ttime(255, 85); e1v = speed(255, tm(3, 45)); e1d = speed(255, tm(3, 15))
assert (e1t, clk(tm(7, 45) + e1t), e1v, dec(e1d, 1)) == (180, "10:45", 68, "78.5")
e2o, e2b, e2a = speed(6, 90), speed(6, 75), speed(12, 90 + 60 + 75); assert (e2o, e2b, e2a) == (4, F("4.8"), F("3.2"))
e3d = 1500 * F("1.12"); e3l = e3d - 1420; e3b = cent(e3l / F("1.16")); e3c = cent(e3l / F("1.12"))
assert (e3d, e3l, e3b, e3c, e3c - e3b) == (1680, 260, F("224.14"), F("232.14"), 8)
e4t1, e4t2 = ttime(3, 12), ttime(3, 10); e4v = speed(6, e4t1 + e4t2); assert (e4t1, e4t2, dec(e4v, 1)) == (15, 18, "10.9")
E = [("<b>The school tour.</b> A coach travels 255 km. It leaves at 07:45 and its average speed is 85 km/h. (a) How long does the journey take? (b) When does it arrive? (c) The journey home takes 3 h 45 min, including a 30-minute stop. Find the average speed for the journey home. (d) Find the average speed when the coach was moving, to 1 decimal place.",
      f"(a) <b>{hm(e1t)}</b> (b) <b>10:45</b> (c) 255 ÷ 3.75 = <b>{kmh(e1v)}</b> (d) 255 ÷ 3.25 = <b>{kmh(e1d, 1)}</b>"),
     ("<b>The beach walk.</b> Emma walks 6 km to the beach in 1 h 30 min, stays for 1 hour, then walks home in 1 h 15 min. (a) Find her speed on the way there. (b) Find her speed on the way back. (c) Find her average speed for the whole trip, including the hour at the beach. (d) Sketch a distance–time graph of her trip.",
      f"(a) <b>{kmh(e2o)}</b> (b) <b>{kmh(e2b)}</b> (c) 12 ÷ 3.75 = <b>{kmh(e2a)}</b> (d) up, flat for 1 h, then down to 0, steeper than the way there"),
     ("<b>New York.</b> Jack changes €1,500 into dollars at €1 = $1.12. He spends $1,420 and changes the rest back at €1 = $1.16. (a) How many dollars does he get? (b) How many euro does he get back, to the nearest cent? (c) How much more would he have got back if the rate had stayed at $1.12?",
      f"(a) <b>{mon('$', e3d)}</b> (b) $260 ÷ 1.16 = <b>{e(e3b)}</b> (c) {e(e3c)} − {e(e3b)} = <b>{e(e3c - e3b)}</b>"),
     ("<b>The fun run.</b> Liam runs the first 3 km at 12 km/h and the next 3 km at 10 km/h. (a) How long does each half take? (b) Find his average speed for the 6 km, to 1 decimal place. (c) Explain why it isn't 11 km/h. (d) A sprinter runs 100 m in 12.5 s. Find her speed in m/s and in km/h.",
      f"(a) <b>15 min</b>, <b>18 min</b> (b) 6 ÷ 0.55 = <b>{kmh(e4v, 1)}</b> (c) more time is spent at 10 km/h (d) <b>8 m/s</b> = <b>28.8 km/h</b>")]
assert F(100) / F("12.5") == 8 and 8 * F("3.6") == F("28.8")

def qs(items): return "".join(f"<li>{q} <span class='line'></span></li>" for q, a in items)
def style(var, ext=""):
    return re.search(var + r' = f"""<!doctype.*?<style>(.*?)</style>', open(os.path.join(SRC, "build_money1_pdfs.py"), encoding="utf-8").read(), re.S).group(1).replace("{LO}", LO).replace("{{", "{").replace("}}", "}")
SHEET_STYLE = style("sheet"); PACK_STYLE = style("pack")
assert "@bottom-left" in SHEET_STYLE and "Single-teacher licence" in PACK_STYLE and "{{" not in SHEET_STYLE + PACK_STYLE

RULE_G = graph(600, [(0, 0), (60, 40), (90, 40), (120, 0)], "OABC", "width:100%;max-height:44mm")
sheet = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Speed, distance, time and currency: rules and practice | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{SHEET_STYLE}
.tri3{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:2mm;text-align:center;margin:3px 0}}.tri3 div{{border:1.5px solid var(--line);border-radius:8px;padding:3px;font-weight:800}}.tri3 span{{display:block;font-weight:500;font-size:8pt;color:var(--muted)}}
.gfig{{float:right;width:62mm;margin:0 0 2mm 3mm}}
</style></head><body>
<div class="page tight">
  <div class="band"><div><div class="k">Junior Cycle Maths · Free revision sheet</div><h1>Speed, distance, time &amp; currency</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2018 specification): {LO}. Play the game: <b>leim.ie/road-trip.html</b></p>
  <div class="two">
   <div><h2>1. The three formulas</h2>
    <div class="tri3"><div>S = D ÷ T<span>speed</span></div><div>D = S × T<span>distance</span></div><div>T = D ÷ S<span>time</span></div></div>
    <p>km and hours → km/h. Metres and seconds → m/s. 240 km in 3 h: 240 ÷ 3 = <b>80 km/h</b>.</p>
    <h2>2. Time in hours</h2>
    <table style="font-size:9pt;white-space:nowrap"><tbody><tr><td>15 min = 0.25 h</td><td>30 min = 0.5 h</td><td>45 min = 0.75 h</td></tr><tr><td>6 min = 0.1 h</td><td>12 min = 0.2 h</td><td>20 min = ⅓ h</td></tr></tbody></table>
    <p>Minutes ÷ 60 = hours: 2 h 24 min = <b>2.4 h</b> (NOT 2.24). Back again: only the decimal part × 60: 1.35 h = 1 h + 0.35 × 60 = <b>1 h 21 min</b>.</p>
    <p><b>Arrival time</b> = leaving time + journey time: 09:40 + 2 h 35 min = <b>12:15</b>.</p>
    <h2>3. Average speed</h2>
    <p><b>Total distance ÷ total time</b>, stops included. 120 km at 60 km/h (2 h), back at 40 km/h (3 h): 240 ÷ 5 = <b>48 km/h</b>, not the mean (50).</p>
    <h2>4. km/h and m/s</h2>
    <p>m/s × 3.6 = km/h; km/h ÷ 3.6 = m/s. 20 m/s = <b>72 km/h</b>.</p></div>
   <div><h2>5. Distance–time graphs</h2>
    {RULE_G}
    <p><b>Up</b> = moving away · <b>flat</b> = stopped · <b>down</b> = coming back. <b>Steeper = faster.</b> O to A: 40 km in 1 h = 40 km/h; stopped 30 min; B to C: 40 km in 30 min = 80 km/h. Whole trip: 80 km ÷ 2 h = 40 km/h.</p>
    <h2>6. Currency</h2>
    <table><tbody><tr><td>€ → other</td><td><b>× the rate</b>: €1 = £0.86, €250 × 0.86 = £215</td></tr>
     <tr><td>other → €</td><td><b>÷ the rate</b>: £215 ÷ 0.86 = €250</td></tr>
     <tr><td>Commission</td><td>take the % off the euro first, then change the rest</td></tr>
     <tr><td>The rate</td><td>£344 for €400: 344 ÷ 400 = 0.86</td></tr></tbody></table>
    <p><b>Where is it cheaper?</b> Change both prices into euro, then compare. Round money to the nearest cent at the end.</p>
    <div class="note"><b>Classic mistakes:</b> 2 h 30 min as 2.3 h · the mean of two speeds · leaving out a stop · multiplying to go back into euro · reading the distance off a graph when the speed is asked.</div></div>
  </div>
  <div class="tip"><b>Exam tip:</b> write the time in hours first, then the formula, then the numbers, then the answer WITH units. Each step earns marks.</div>
</div>

<div class="page p2">
  <div class="band"><div><div class="k">Practice · 34 questions</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Speed, distance and time</h2><ol class="q">{qs(A)}</ol>
  <h2>B. Average speed and units</h2><ol class="q" start="9">{qs(B)}</ol>
  <h2>C. The graph shows Ruth's drive from home</h2>
  <div class="gfig">{graph(GS, GP, GN)}</div>
  <ol class="q" start="16">{qs(Cq)}</ol>
  <div style="clear:both"></div>
  <h2>D. Currency</h2><ol class="q" start="23">{qs(D)}</ol>
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
   <tr><td><b>D</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(D,23))}</td></tr>
   <tr><td><b>E</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(E,31))}</td></tr>
  </tbody></table>
  <div class="note"><b>Got one wrong?</b> Check: did you change the minutes into hours (÷ 60) before dividing? For average speed, did you use the TOTAL distance and the TOTAL time, stops included? For currency, did you multiply going out of euro and divide coming back? Then play <b>Road Trip</b> at leim.ie/road-trip.html: the "Go back over these" list at the end shows the rule for each mistake.</div>
  <p class="small">All questions written by Léim. Léim is independent and not connected with the State Examinations Commission or the NCCA. Exchange rates here are examples; the exam always gives you the rate to use.</p>
</div>
</body></html>"""

# ---------- teacher pack ----------
# Journey Swap: each fact is on exactly ONE card; both students work out every blank
j_t = ttime(270, 90); j_arr = tm(8, 30) + j_t + 45; j_avg = speed(270, j_t + 45)
assert (j_t, clk(j_arr), j_avg) == (180, "12:15", 72)
s_gbp = 800 * F("0.85"); s_left = s_gbp - 595; s_back = cent(s_left / F("0.88"))
assert (s_gbp, s_left, s_back) == (680, 85, F("96.59"))
TR = [("Distance to Westport", "270 km", "A"), ("Leave home at", "08:30", "B"), ("Average driving speed", "90 km/h", "A"),
      ("Lunch stop", "45 min", "B"), ("Driving time", "", None), ("Arrival time", "", None), ("Average speed, stop included", "", None)]
MR = [("Euro changed", e(800), "B"), ("Rate going", "€1 = £0.85", "A"), ("Sterling received", "", None), ("Sterling spent", "£595.00", "A"),
      ("Sterling left", "", None), ("Rate coming home", "€1 = £0.88", "B"), ("Euro back (nearest cent)", "", None)]
for rows in (TR, MR):
    assert all(w in ("A", "B") for _, v, w in rows if v) and any(w == "A" for *_, w in rows) and any(w == "B" for *_, w in rows)
def swap_card(who):
    def tab(title, rows):
        return f'<table class="ss"><thead><tr><th colspan="2">{title}</th></tr></thead><tbody>' + "".join(
            f"<tr><td>{k}</td><td><b>{v if w == who else ''}</b></td></tr>" for k, v, w in rows) + "</tbody></table>"
    return f'<div class="idc"><h3>Student {who} · Journey Swap</h3><div class="two">{tab("The Kellys’ road trip", TR)}{tab("Aisling’s holiday money (UK)", MR)}</div></div>'

MATCH = [("300 km in 4 h: speed?", kmh(speed(300, 240))), ("40 km/h for 2 h 15 min: distance?", km(40 * F(135, 60))),
         ("240 km at 96 km/h: time?", hm(ttime(240, 96))), ("1 h 12 min in hours?", dec(F(72, 60)) + " h"),
         ("Leave 14:35, drive 2 h 40 min. Arrive?", clk(tm(14, 35) + 160)), ("10 m/s in km/h?", kmh(10 * F(36, 10))),
         ("100 km in 1 h + 50 km in 1 h 30 min: average?", kmh(speed(150, 150))), ("Graph flat 11:00 to 11:45: stopped for?", hm(45)),
         ("€250 at €1 = £0.84", mon("£", 250 * F("0.84"))), ("€600 at €1 = $1.15", mon("$", 600 * F("1.15"))),
         ("$324 at €1 = $1.08, in euro?", e(F(324) / F("1.08"))), ("€1,000 gave £865: €1 = £?", "£" + dec(F(865, 1000)))]
ANS = [a for q, a in MATCH]
assert ANS == ["75 km/h", "90 km", "2 h 30 min", "1.2 h", "17:15", "36 km/h", "60 km/h", "45 min", "£210.00", "$690.00", "€300.00", "£0.865"], ANS
assert len(set(ANS)) == 12
cards = [q for q, a in MATCH] + ANS
random.seed(20); match_print = cards[:]; random.shuffle(match_print)
match_html = "".join(f'<div class="c"><span class="tag">Card {i}</span><div class="fc{" sm" if len(x) > 10 else ""}">{x}</div></div>' for i, x in enumerate(match_print, 1))
match_key = " · ".join(f"{q} → <b>{a}</b>" for q, a in MATCH)

DOMS = [("200 km in 2 h 30 min: speed", kmh(speed(200, 150))), ("70 km/h for 3 h", km(210)), ("150 km at 60 km/h: time", hm(ttime(150, 60))),
        ("45 min in hours", dec(F(45, 60)) + " h"), ("0.2 h in minutes", hm(F("0.2") * 60)), ("2 h at 50, then 1 h at 80: average", kmh(F(180, 3))),
        ("25 m/s in km/h", kmh(25 * F(36, 10))), ("54 km/h in m/s", dec(F(54000, 3600)) + " m/s"), ("Leave 10:40, travel 1 h 50 min", clk(tm(10, 40) + 110)),
        ("100 m in 20 s", dec(F(100, 20)) + " m/s"), ("€200 at €1 = £0.85", mon("£", 200 * F("0.85"))), ("€500 at €1 = $1.10", mon("$", 500 * F("1.1"))),
        ("£430 at €1 = £0.86, in euro", e(F(430) / F("0.86"))), ("$216 at €1 = $1.08, in euro", e(F(216) / F("1.08"))), ("€300 gave £261: €1 = £?", "£" + dec(F(261, 300))),
        ("2% commission on €400", e(8)), ("60 km there at 40, back at 60: average", kmh(F(120, F(60, 40) + 1))), ("A flat line on a distance–time graph", "stopped"),
        ("24 km in 20 min: speed", kmh(speed(24, 20))), ("90 km/h for 40 min", km(90 * F(40, 60)))]
DANS = [a for k, a in DOMS]
assert DANS == ["80 km/h", "210 km", "2 h 30 min", "0.75 h", "12 min", "60 km/h", "90 km/h", "15 m/s", "12:30", "5 m/s", "£170.00", "$550.00", "€500.00",
                "€200.00", "£0.87", "€8.00", "48 km/h", "stopped", "72 km/h", "60 km"], DANS
assert len(set(DANS)) == 20
random.seed(2020); chain = DOMS[:]; random.shuffle(chain)
dom = [("START" if k == 0 else chain[k - 1][1], x[0]) for k, x in enumerate(chain)] + [(chain[-1][1], "FINISH")]
dom_print = dom[:]; random.shuffle(dom_print)
dom_html = "".join(f'<div class="dom"><div class="h l{" sm" if len(l) > 9 else ""}">{l}</div><div class="h r">{r}</div></div>' for l, r in dom_print)
chain_key = "".join(f"<li>{x} = <b>{a}</b></li>" for x, a in chain)

ERR = [("150 km in 2 h 30 min. Speed?", "150 ÷ 2.3 = 65.2 km/h", f"2 h 30 min = 2.5 h. 150 ÷ 2.5 = <b>{kmh(speed(150, 150))}</b>"),
       ("80 km/h for 45 min. Distance?", "80 ÷ 0.75 = 106.7 km", f"Distance = speed × time: 80 × 0.75 = <b>{km(80 * F(3, 4))}</b>"),
       ("1.25 hours in hours and minutes?", "1 h 25 min", f"0.25 × 60 = 15 min, so <b>{hm(75)}</b>"),
       ("60 km at 30 km/h, back at 60 km/h. Average speed?", "(30 + 60) ÷ 2 = 45 km/h", f"120 km in 2 h + 1 h = 3 h: <b>{kmh(F(120, 3))}</b>"),
       ("Change £258 into euro at €1 = £0.86.", "258 × 0.86 = €221.88", f"Into euro: divide. 258 ÷ 0.86 = <b>{e(F(258) / F('0.86'))}</b>"),
       ("A graph is flat at 20 km from 10:00 to 10:30. Speed?", "20 km/h", "Flat = not moving: the speed is <b>0 km/h</b> (stopped for 30 min)")]
assert F(258) / F("0.86") == 300
w1t = ttime(286, 104); assert (w1t, clk(tm(6, 55) + w1t)) == (165, "09:40")
w2 = speed(84 + 126, 70 + 20 + 90); assert w2 == 70
w3 = cent(900 * F("0.985") * F("1.12")); assert w3 == F("992.88")
w4 = 30 * F("3.6"); w4t = ttime(27, w4); assert (w4, w4t) == (108, 15)
w5 = cent(F("79.99") / F("0.87")); assert (w5, F("89.50") - w5) == (F("91.94"), F("-2.44"))

pack = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Speed, Distance, Time and Currency Teacher Pack | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{PACK_STYLE}
.ss td:nth-child(2){{width:34%}}.ss td,.ss th{{padding:1px 5px;font-size:8.6pt;line-height:1.2}}.fym .c{{height:16mm}}.big3{{font-size:22pt}}.p1 .proc td{{font-size:8.5pt;padding:2px 6px}}
</style></head><body>

<div class="page p1">
  <div class="band"><div><div class="k">Junior Cycle Maths · Teacher pack</div><h1>Speed, distance, time &amp; currency</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2018 specification): {LO} (straight-line graphs and slope come later, in coordinate geometry)</p>
  <div class="two">
    <div><h3>Aims</h3><p>By the end of the lesson students can find speed, distance and time (changing minutes into hours and back), work out arrival times and average speed for journeys with more than one part or a stop, change between km/h and m/s, read distance–time graphs, and convert between euro and other currencies, including commission and comparing prices.</p></div>
    <div><h3>In this pack</h3><p>p.1 Teacher notes · p.2 Road Trip mingle cards + Journey Swap A/B cards · p.3 Travel Dominoes (cut-up) · p.4 Wall poster · p.5 Worksheet: Error Hunt + exam-style questions · p.6 Answers. Level: 2nd year (Higher and Ordinary), or 3rd-year revision. Time: about 60 minutes. All questions are original.</p></div>
  </div>
  <h2 style="margin-top:8px">Procedure</h2>
  <table class="proc"><tbody>
    <tr><td>5 min</td><td><b>Lead-in: the 2.30 trap.</b> Board "A coach travels 150 km in 2 h 30 min. What is its average speed?" Students answer alone on mini-whiteboards. Collect answers (usually 65.2 and 60 km/h) without saying which is right.</td></tr>
    <tr><td>8 min</td><td><b>Guided discovery.</b> Pairs fill a table for a car at a steady speed (30 min → 50 km, 1 h → 100 km, 1 h 30 min → 150 km). What is distance ÷ time each time? What must 30 minutes be in hours? Resolve the lead-in, then build S = D ÷ T, D = S × T, T = D ÷ S. Then: Niamh drives there at 60 km/h and back at 40 km/h. Is her average 50?</td></tr>
    <tr><td>10 min</td><td><b>Road Trip mingle</b> (p.2, 24 cards = 12 question/answer pairs; one card each). Question card? Work it out and find the person with your answer. Answer card? Find your question. Pairs check each other's working.</td></tr>
    <tr><td>12 min</td><td><b>Journey Swap</b> (p.2, pairs, don't show your card). Each fact is on only ONE card. Ask your partner for what you're missing ("What time do they leave?"), then both fill every blank. Feedback: arrival {clk(j_arr)}, average {kmh(j_avg)}; euro back {e(s_back)}.</td></tr>
    <tr><td>10 min</td><td><b>Travel Dominoes</b> (p.3), groups of 3–4. Start with START, work out the clue, find the domino with that answer on its left, and build the chain to FINISH.</td></tr>
    <tr><td>12 min</td><td><b>Worksheet</b> (p.5). Error Hunt in pairs (find the mistake, name the rule, fix it), then the exam-style questions alone.</td></tr>
    <tr><td>3 min</td><td><b>Exit ticket.</b> 90 km in 1 h 15 min: speed? €350 at €1 = £0.86: sterling? (72 km/h; £301.) Homework: play <b>Road Trip</b> at leim.ie/road-trip.html and copy three lines from the "Go back over these" list.</td></tr>
  </tbody></table>
  <div class="note"><b>Road Trip key:</b> {match_key}.<br>
  <b>Errors to look for:</b> 2 h 30 min as 2.3 · dividing for distance · the mean of two speeds · leaving out stops · multiplying to go back into euro · forgetting the commission · reading a distance off the graph when a speed is asked. <b>Support:</b> a minutes → hours strip (15 = 0.25, 20 = ⅓, 30 = 0.5, 45 = 0.75). <b>Fast finishers:</b> how long does light take to reach us from the Sun, 150,000,000 km at 300,000 km/s? (500 s = 8 min 20 s)</div>
  <p class="small"><b>Domino answer chain</b> (START → FINISH):</p>
  <ol class="small" style="columns:2;column-gap:12px;font-size:7pt;line-height:1.22;margin:0;padding-left:16px">{chain_key}</ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">Cut up the cards · one Journey Swap card per student</div><h1>Road Trip + Journey Swap</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:8.8pt;margin:0"><b>Road Trip mingle.</b> Cut out the 24 cards and give one to each student. Question card? Work it out, then find the person with your answer. Answer card? Find the question that gives your answer. (Fewer students? Take out whole pairs.)</p>
  <div class="fym">{match_html}</div>
  <p style="font-size:8.8pt;margin:3mm 0 0"><b>Journey Swap.</b> Don't show your card. Each fact is on only one of the two cards: ask your partner for what you're missing, then fill in every blank on both. A calculator is fine.</p>
  {swap_card("A")}
  {swap_card("B")}
</div>

<div class="page">
  <div class="band"><div><div class="k">Groups of 3–4 · cut along the dashed lines</div><h1>Travel Dominoes</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.4pt">Start with START. Work out the clue on the right, then find the domino with that answer on its left. Keep going until you reach FINISH.</p>
  <div class="doms">{dom_html}</div>
</div>

<div class="page">
  <div class="poster">
    <h1>Speed, distance, time &amp; money</h1>
    <div class="big3"><div>D ÷ T<span>speed</span></div><div>S × T<span>distance</span></div><div>D ÷ S<span>time</span></div></div>
    <div class="ops">
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Minutes → hours</b>÷ 60<br>45 min = 0.75 h<br>2 h 30 min = 2.5 h (not 2.3)</div>
      <div style="background:var(--green-soft)"><b>Average speed</b>TOTAL distance<br>÷ TOTAL time<br>stops included</div>
      <div style="background:var(--green-soft)"><b>Distance–time graph</b>up = away · flat = stopped<br>down = coming back<br>steeper = faster</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Currency</b>€ → other: × rate<br>other → €: ÷ rate<br>€1 = £0.86: €250 = £215</div>
    </div>
    <p style="text-align:center;font-size:12pt;margin:0"><b>m/s × 3.6 = km/h</b> · km/h ÷ 3.6 = m/s · 20 m/s = 72 km/h</p>
    <p style="text-align:center;font-size:10pt;color:var(--muted)">Léim · leim.ie · Play Road Trip: leim.ie/road-trip.html</p>
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
  <ol class="q">
    <li>A train leaves at 06:55 and travels 286 km at an average speed of 104 km/h. (a) How long does the journey take, in hours and minutes? (b) At what time does it arrive?<span class="long"></span></li>
    <li>Ronan drives 84 km in 1 h 10 min, stops for 20 minutes, then drives 126 km in 1 h 30 min. Find his average speed for the whole journey, including the stop.<span class="long"></span></li>
    <li>A bank takes 1.5% commission from the euro and changes the rest at €1 = $1.12. How many dollars do you get for €900?<span class="long"></span></li>
    <li>A train travels at 30 m/s. (a) Write this speed in km/h. (b) How long does it take to travel 27 km at this speed?<span class="long"></span></li>
    <li>A jacket costs £79.99 in Belfast and €89.50 in Cork. The rate is €1 = £0.87. Where is it cheaper, and by how much?<span class="long"></span></li>
  </ol>
</div>

<div class="page an">
  <div class="band"><div><div class="k">For the teacher</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>Journey Swap</h2>
  <div class="two"><table><tbody>
   <tr><td>Driving time</td><td>270 ÷ 90 = <b>{hm(j_t)}</b></td></tr><tr><td>Arrival time</td><td>08:30 + 3 h + 45 min = <b>{clk(j_arr)}</b></td></tr>
   <tr><td>Average speed</td><td>270 ÷ 3.75 = <b>{kmh(j_avg)}</b></td></tr></tbody></table>
  <table><tbody>
   <tr><td>Sterling received</td><td>800 × 0.85 = <b>{mon("£", s_gbp)}</b></td></tr><tr><td>Sterling left</td><td>£680 − £595 = <b>{mon("£", s_left)}</b></td></tr>
   <tr><td>Euro back</td><td>85 ÷ 0.88 = <b>{e(s_back)}</b></td></tr></tbody></table></div>
  <h2>A. Error Hunt</h2>
  <table><tbody>{"".join(f"<tr><td style='width:36%'><b>{q}</b> {w}</td><td>{r}</td></tr>" for q,w,r in ERR)}</tbody></table>
  <h2>B. Exam-style questions</h2>
  <ol class="q">
    <li>(a) 286 ÷ 104 = 2.75 h = <b>{hm(w1t)}</b> (b) 06:55 + 2 h 45 min = <b>{clk(tm(6, 55) + w1t)}</b></li>
    <li>210 km in 1 h 10 min + 20 min + 1 h 30 min = 3 h: <b>{kmh(w2)}</b></li>
    <li>€900 − 1.5% = €886.50; × 1.12 = <b>{mon("$", w3)}</b></li>
    <li>(a) 30 × 3.6 = <b>{kmh(w4)}</b> (b) 27 ÷ 108 = 0.25 h = <b>{hm(w4t)}</b></li>
    <li>£79.99 ÷ 0.87 = {e(w5)}. <b>Cork is cheaper by {e(w5 - F("89.50"))}</b></li>
  </ol>
  <h2>Marking tip</h2>
  <p>Give credit for each step, as the exam does: the time in hours, the formula, the substitution and the answer with units each earn marks. For currency, credit the correct operation (× or ÷) even if the rounding slips. For "explain" parts insist on a sentence with numbers in it.</p>
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
<h1><span>Speed, Distance, Time</span><br><span>&amp; Currency</span></h1>
<div class="sub">Road Trip mingle · Journey Swap A/B<br>Travel Dominoes · Poster · Worksheet + answers</div>
<div class="em">150 km in 2 h 30 min = 60 km/h</div></div>
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
    pdf("teacher-pack", os.path.join(OUT, "Speed-Distance-Time-Currency-Teacher-Pack-Leim.pdf"))
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--hide-scrollbars", "--window-size=1200,1200",
                    f"--screenshot={os.path.join(OUT, f'{SLUG}-cover.png')}", f"{SLUG}-cover.html"], cwd=SRC, check=True, capture_output=True)
    print("domino chain:", [(x, a) for x, a in chain])
