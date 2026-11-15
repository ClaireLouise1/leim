#!/usr/bin/env python3
"""Units of measure, time & timetables (JC Maths topic 10): free sheet + teacher pack + Payhip cover.
Run from the repo root: python3 src/build_units_pdfs.py OUTDIR
Writes src/units-time-timetables-*.html; PDFs/cover PNG go to OUTDIR (free sheet also to printables/).
Every answer is computed (minutes as integers, amounts with Fraction) and asserted."""
import os, sys, random, subprocess, re
from fractions import Fraction as F
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC)
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/units"; os.makedirs(OUT, exist_ok=True)
SLUG = "units-time-timetables"
LO = "GT.1"
U = {"mm": 1, "cm": 10, "m": 1000, "km": 10**6, "g": 1, "kg": 1000, "t": 10**6, "ml": 1, "l": 1000}

def dec(x):
    x = F(x); k = 0
    while (x * 10 ** k).denominator != 1:
        k += 1; assert k < 8, x
    n = x * 10 ** k; s = str(abs(n.numerator)).rjust(k + 1, "0")
    return s[:len(s) - k] + ("." + s[len(s) - k:] if k else "")
def amt(s):
    v, u = s.split(); return F(v) * U[u]
def conv(s, u): return dec(amt(s) / U[u]) + " " + u
def tm(s):
    m = re.fullmatch(r"(\d{1,2}):(\d{2})( am| pm)?", s); h = int(m[1])
    if m[3]: h = h % 12 + (12 if m[3] == " pm" else 0)
    return h * 60 + int(m[2])
def hm(m): m %= 1440; return "%02d:%02d" % (m // 60, m % 60)
def t12(m): m %= 1440; h = m // 60; return "%d:%02d %s" % (h % 12 or 12, m % 60, "am" if h < 12 else "pm")
def dur(m): h, r = divmod(m, 60); return f"{h} h {r} min" if h and r else (f"{h} h" if h else f"{r} min")
def dmin(s):
    m = re.fullmatch(r"(?:(\d+) h)?(?: ?(\d+) min)?", s); return int(m[1] or 0) * 60 + int(m[2] or 0)
def gap(a, b): return (tm(b) - tm(a)) % 1440
assert hm(tm("4:25 pm")) == "16:25" and t12(tm("21:15")) == "9:15 pm" and conv("3.4 km", "m") == "3400 m" and dur(148) == "2 h 28 min"

# ---------- free sheet ----------
A = [("4:25 pm", hm(tm("4:25 pm"))), ("9:05 am", hm(tm("9:05 am"))), ("12:40 am", hm(tm("12:40 am"))),
     ("21:15", t12(tm("21:15"))), ("12:30", t12(tm("12:30"))), ("00:05", t12(tm("00:05")))]
assert [a for q, a in A] == ["16:25", "09:05", "00:40", "9:15 pm", "12:30 pm", "12:05 am"]
B = [("3.4 km", "m"), ("750 g", "kg"), ("2.5 l", "ml"), ("45 mm", "cm"), ("1.25 m", "cm"), ("360 ml", "l"), ("0.8 t", "kg"), ("2500 m", "km")]
Bans = [conv(a, u) for a, u in B]
assert Bans == ["3400 m", "0.75 kg", "2500 ml", "4.5 cm", "125 cm", "0.36 l", "800 kg", "2.5 km"], Bans
C = [("Write 75 minutes in hours, as a decimal.", dec(F(75, 60)) + " h"),
     ("Write 2.4 hours in hours and minutes.", dur(int(F("2.4") * 60))),
     ("How long is it from 08:47 to 11:15?", dur(gap("08:47", "11:15"))),
     ("What time is 2 h 35 min after 13:50?", hm(tm("13:50") + 155)),
     ("How many minutes are in 3 h 20 min?", str(dmin("3 h 20 min"))),
     ("How many seconds are in 4.5 minutes?", dec(F("4.5") * 60)),
     ("Write 1.75 hours in hours and minutes.", dur(int(F("1.75") * 60))),
     ("A night bus leaves at 22:40 and arrives at 01:15. How long is the journey?", dur(gap("22:40", "01:15")))]
assert [a for q, a in C] == ["1.25 h", "2 h 24 min", "2 h 28 min", "16:25", "200", "270", "1 h 45 min", "2 h 35 min"], [a for q, a in C]
STOPS = ["Douglas", "Ballinlough", "South Mall", "Parnell Place"]
TT = [["07:10", "07:21", "07:33", "07:40"], ["07:35", "07:46", "07:59", "08:07"], ["08:05", None, "08:22", "08:28"], ["08:30", "08:41", "08:54", "09:02"]]
jt = [gap(b[0], b[3]) for b in TT]
assert jt == [30, 32, 23, 32]
latest_sm = max((b for b in TT if tm(b[2]) <= tm("08:00")), key=lambda b: tm(b[0]))[0]
wait_bl = min(tm(b[1]) for b in TT if b[1] and tm(b[1]) > tm("07:30")) - tm("07:30")
D = [("How long does the 07:10 bus take from Douglas to Parnell Place?", dur(jt[0])),
     ("Which bus does not stop at Ballinlough?", [b[0] for b in TT if b[1] is None][0]),
     ("How long does the 08:05 bus take from Douglas to Parnell Place?", dur(jt[2])),
     ("Which bus is quickest from Douglas to Parnell Place?", TT[jt.index(min(jt))][0]),
     ("You must be at South Mall by 08:00. What is the latest bus you can catch from Douglas?", latest_sm),
     ("You get to the Ballinlough stop at 07:30. How long do you wait for a bus?", dur(wait_bl)),
     ("How long does the 08:30 bus take from Ballinlough to South Mall?", dur(gap(TT[3][1], TT[3][2]))),
     ("Aoife gets to the Douglas stop at 07:37. How long until the next bus?", dur(gap("07:37", "08:05")))]
assert [a for q, a in D] == ["30 min", "08:05", "23 min", "08:05", "07:35", "16 min", "13 min", "28 min"], [a for q, a in D]
tt_html = "<table class='tt'><tr><th>Stop</th>" + "".join(f"<th>Bus {i}</th>" for i in range(1, 5)) + "</tr>" + "".join(
    f"<tr><th>{s}</th>" + "".join(f"<td>{b[j] or '—'}</td>" for b in TT) + "</tr>" for j, s in enumerate(STOPS)) + "</table>"
# exam-style
tr = gap("06:55", "09:28"); assert dur(tr) == "2 h 33 min" and hm(tm("09:28") + 17) == "09:45"
tins = -(-amt("3.6 l") // amt("750 ml")); left = tins * 750 - 3600; assert (tins, left) == (5, 150)
swim = 48 * 25; assert conv(f"{swim} m", "km") == "1.2 km" and F(36, 60) == F(3, 5)
ham = 40 * F("2.25") + 20; assert ham == 110 and hm(tm("19:00") - 110) == "17:10"
E = [("A train leaves Cork at 06:55 and arrives in Dublin Heuston at 09:28. (a) How long is the journey? (b) One morning it is 17 minutes late. When does it arrive?",
      f"(a) <b>{dur(tr)}</b> (b) <b>09:45</b>"),
     ("A wall needs 3.6 litres of paint. Paint comes in 750 ml tins. (a) How many tins must be bought? (b) How much paint is left over?",
      f"(a) 3600 ÷ 750 = 4.8, so <b>{tins} tins</b> (b) {tins} × 750 = 3750 ml; <b>{left} ml</b> left"),
     ("Niamh swims 48 lengths of a 25 m pool in 36 minutes. (a) How far does she swim, in km? (b) Write 36 minutes in hours, as a decimal.",
      f"(a) 48 × 25 = 1200 m = <b>1.2 km</b> (b) 36 ÷ 60 = <b>0.6 h</b>"),
     ("A ham needs 40 minutes per kg plus 20 minutes. It weighs 2.25 kg. Dinner is at 19:00. What is the latest time it can go in the oven?",
      "40 × 2.25 = 90 min, + 20 = 110 min = 1 h 50 min. 19:00 − 1 h 50 min = <b>17:10</b>")]

def qs(items): return "".join(f"<li>{q} <span class='line'></span></li>" for q, a in items)

sheet = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Units of measure, time and timetables: rules and practice | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>@page{{@bottom-left{{content:"Léim · leim.ie · Free to print for home or class · JC Maths LOs (2018 spec): {LO}"}}}}
.tight{{font-size:10.2pt;line-height:1.44}}.tight td,.tight th{{padding:3px 6px}}.tight h2{{margin:10px 0 5px;font-size:14pt}}.tight .note,.tight .tip{{padding:6px 10px;margin:6px 0}}
ol.q{{padding-left:30px}}ol.q li{{margin:7px 0}}.cols{{columns:2;column-gap:12mm}}.cols li{{break-inside:avoid}}
.p2{{font-size:9.6pt}}.p2 ol.q li{{margin:4px 0}}
.ans td{{padding:3px 6px;font-size:9.2pt}}
.tt{{width:auto;margin:4px 0 6px}}.tt td,.tt th{{text-align:center;padding:3px 8px;font-size:9.6pt}}.tt tr th:first-child{{text-align:left}}
</style></head><body>
<div class="page tight">
  <div class="band"><div><div class="k">Junior Cycle Maths · Free revision sheet</div><h1>Units, time &amp; timetables</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2018 specification): {LO}. Play the game: <b>leim.ie/clock-dash.html</b></p>
  <div class="two">
   <div><h2>1. Metric units</h2>
    <table><thead><tr><th>Measure</th><th>Units</th></tr></thead><tbody>
     <tr><td>Length</td><td>1 km = 1000 m · 1 m = 100 cm · 1 cm = 10 mm</td></tr>
     <tr><td>Mass</td><td>1 kg = 1000 g · 1 tonne = 1000 kg</td></tr>
     <tr><td>Capacity</td><td>1 litre = 1000 ml</td></tr></tbody></table>
    <p><b>Big → small: multiply</b> (3.4 km = 3400 m). <b>Small → big: divide</b> (250 g = 0.25 kg). Change to the <b>same unit</b> before adding, comparing or dividing: 1.2 kg + 350 g = 1200 g + 350 g = 1550 g.</p>
    <h2>2. The 24-hour clock</h2>
    <p><b>am:</b> keep the hour (7:05 am = 07:05; 12:40 am = 00:40). <b>pm:</b> add 12 (2:35 pm = 14:35), but 12:30 pm = 12:30. Back again: 13–23, take away 12 and write pm (19:05 = 7:05 pm).</p>
    <h2>3. Hours are not decimals</h2>
    <p>An hour has <b>60</b> minutes. Minutes → hours: ÷ 60 (45 min = 0.75 h). Decimal hours → minutes: × 60 (0.4 h = 24 min, so 2.4 h = 2 h 24 min, not 2 h 40 min).</p></div>
   <div><h2>4. How long is it? Count on</h2>
    <p>08:47 → 11:15: 08:47 → 09:00 = 13 min; 09:00 → 11:00 = 2 h; 11:00 → 11:15 = 15 min. Total <b>2 h 28 min</b>. Don't take away like ordinary numbers (1115 − 847 = 268 gives "2 h 68 min", which can't be right).</p>
    <h2>5. Adding time</h2>
    <p>13:50 + 2 h 35 min: add the hours (15:50), then the minutes (15:50 + 35 min = 16:25). Every 60 minutes makes another hour.</p>
    <h2>6. Reading a timetable</h2>
    <p>Each column is one bus; each row is a stop. Read <b>down</b> to follow one bus. A dash (—) means it doesn't stop there. For "the latest bus to get there by…", find the last arrival that's early enough, then go up the column.</p>
    <div class="note"><b>Other units of time:</b> 60 seconds = 1 minute · 24 hours = 1 day · 7 days = 1 week · 365 days = 1 year (366 in a leap year).</div></div>
  </div>
  <div class="tip"><b>Exam tip:</b> always write the unit in your answer (450 g, not 450). When a question mixes units, change everything to the smaller unit first. Check: a smaller unit means a bigger number.</div>
</div>

<div class="page p2">
  <div class="band"><div><div class="k">Practice · 34 questions</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <div class="two"><div><h2>A. The 24-hour clock</h2><ol class="q">{"".join(f"<li>{'Write in 24-hour clock' if ('am' in q or 'pm' in q) else 'Write in 12-hour clock'}: <b>{q}</b> <span class='line' style='min-width:70px'></span></li>" for q, a in A)}</ol></div>
  <div><h2>B. Convert</h2><ol class="q" start="7">{"".join(f"<li>{a} = <span class='line' style='min-width:60px'></span> {u}</li>" for a, u in B)}</ol></div></div>
  <h2>C. Time</h2><ol class="q" start="15">{qs(C)}</ol>
  <h2>D. Timetable: the 207 bus</h2>{tt_html}<ol class="q" start="23">{qs(D)}</ol>
  <p class="small" style="margin-top:4px">Questions 31–34 are on the next page.</p>
</div>

<div class="page">
  <div class="band"><div><div class="k">Exam-style · then check</div><h1>Exam corner + answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>E. Exam-style questions (show your work)</h2>
  <ol class="q" start="31">{"".join(f"<li>{q}<span class='long'></span><span class='long'></span></li>" for q,a in E)}</ol>
  <h2 style="margin-top:12px">Answers</h2>
  <table class="ans"><tbody>
   <tr><td><b>A</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(A,1))}</td></tr>
   <tr><td><b>B</b></td><td>{" · ".join(f"{i}. {a}" for i,a in enumerate(Bans,7))}</td></tr>
   <tr><td><b>C</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(C,15))}</td></tr>
   <tr><td><b>D</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(D,23))}</td></tr>
   <tr><td><b>E</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(E,31))}</td></tr>
  </tbody></table>
  <div class="note"><b>Got one wrong?</b> Check: did you divide minutes by 60 (not 100)? Did you count on for time differences? Did you change to the same units first, and multiply when going to a smaller unit? Then play <b>Clock Dash</b> at leim.ie/clock-dash.html: the "Go back over these" list at the end shows the rule for each mistake.</div>
  <p class="small">All questions and timetables written by Léim (the timetables are made up for practice). Léim is independent and not connected with the State Examinations Commission or the NCCA.</p>
</div>
</body></html>"""

# ---------- teacher pack ----------
LINE = ["1.2 m", "950 mm", "0.8 m", "105 cm", "1 m", "1500 mm", "0.65 m", "112 cm", "90 cm", "1.35 m", "1180 mm", "0.7 m", "125 cm", "60 cm", "1.45 m", "1025 mm"]
assert len(set(amt(x) for x in LINE)) == 16
line_sorted = sorted(LINE, key=amt)
random.seed(10); line_print = LINE[:]; random.shuffle(line_print)
line_html = "".join(f'<div class="c"><span class="tag">Card {i}</span><div class="fc">{x}</div></div>' for i, x in enumerate(line_print, 1))
# Timetable Swap: A knows rows 0 and 2, B knows rows 1 and 3
SW_STOPS = ["Blarney", "Blackpool", "Patrick Street", "Cork Airport"]
SW = [["07:15", "07:27", "07:38", "07:59"], ["07:45", "07:57", "08:10", "08:33"], ["08:10", None, "08:31", "08:50"], ["08:40", "08:53", "09:05", "09:27"]]
swj = [gap(b[0], b[3]) for b in SW]; assert swj == [44, 48, 40, 47]
for b in SW:
    ts = [tm(x) for x in b if x]; assert ts == sorted(ts)
SWQ_A = [("How long does the 07:15 bus take to get to Cork Airport?", dur(swj[0])),
         ("Which bus does not stop at Blackpool?", [b[0] for b in SW if b[1] is None][0]),
         ("Check-in for your flight closes at 09:00. What's the latest bus you can catch from Blarney?",
          max((b for b in SW if tm(b[3]) <= tm("09:00")), key=lambda b: tm(b[0]))[0])]
SWQ_B = [("You get to the Blackpool stop at 07:50. How long do you wait?", dur(min(tm(b[1]) for b in SW if b[1] and tm(b[1]) > tm("07:50")) - tm("07:50"))),
         ("Which bus is quickest from Blarney to Cork Airport?", SW[swj.index(min(swj))][0]),
         ("How long does the 08:40 bus take from Patrick Street to Cork Airport?", dur(gap(SW[3][2], SW[3][3])))]
assert [a for q, a in SWQ_A + SWQ_B] == ["44 min", "08:10", "08:10", "7 min", "08:10", "22 min"], [a for q, a in SWQ_A + SWQ_B]
def sw_card(who, rows, qsl):
    body = "".join(f"<tr><th>{s}</th>" + "".join(f"<td>{(SW[b][j] or '—') if j in rows else ''}</td>" for b in range(4)) + "</tr>" for j, s in enumerate(SW_STOPS))
    return (f'<div class="idc"><h3>Student {who} · Bus 226 to Cork Airport</h3><table class="ss"><tr><th>Stop</th>' + "".join(f"<th>Bus {i}</th>" for i in range(1, 5)) +
            f"</tr>{body}</table><p style='font-size:9pt;margin:2mm 0 1mm'>Ask your partner for the missing times (\"When does Bus 2 get to Blackpool?\"). Then answer:</p><ol style='font-size:9pt;margin:0;padding-left:18px'>" +
            "".join(f"<li>{q} ______</li>" for q, a in qsl) + "</ol></div>")

DOMS = [("2:45 pm in 24-hour clock", "14:45"), ("19:20 in 12-hour clock", "7:20 pm"), ("0.75 h in minutes", "45 min"), ("1 h 12 min in hours", "1.2 h"),
        ("3.2 km in m", "3200 m"), ("450 g in kg", "0.45 kg"), ("2.5 l in ml", "2500 ml"), ("80 mm in cm", "8 cm"), ("10:50 to 12:15", "1 h 25 min"),
        ("09:40 + 1 h 35 min", "11:15"), ("seconds in 2.5 min", "150"), ("hours in 3 days", "72"), ("1.6 h in h and min", "1 h 36 min"), ("1.8 m in cm", "180 cm"),
        ("0.3 t in kg", "300 kg"), ("0.2 l in ml", "200 ml"), ("23:50 to 00:30", "40 min"), ("90 min in hours", "1.5 h"), ("3 h 5 min in minutes", "185"), ("12:30 am in 24-hour clock", "00:30")]
chk = {"2:45 pm in 24-hour clock": hm(tm("2:45 pm")), "19:20 in 12-hour clock": t12(tm("19:20")), "0.75 h in minutes": dur(45), "1 h 12 min in hours": dec(F(72, 60)) + " h",
       "3.2 km in m": conv("3.2 km", "m"), "450 g in kg": conv("450 g", "kg"), "2.5 l in ml": conv("2.5 l", "ml"), "80 mm in cm": conv("80 mm", "cm"),
       "10:50 to 12:15": dur(gap("10:50", "12:15")), "09:40 + 1 h 35 min": hm(tm("09:40") + 95), "seconds in 2.5 min": dec(F("2.5") * 60), "hours in 3 days": "72",
       "1.6 h in h and min": dur(int(F("1.6") * 60)), "1.8 m in cm": conv("1.8 m", "cm"), "0.3 t in kg": conv("0.3 t", "kg"), "0.2 l in ml": conv("0.2 l", "ml"),
       "23:50 to 00:30": dur(gap("23:50", "00:30")), "90 min in hours": dec(F(90, 60)) + " h", "3 h 5 min in minutes": str(dmin("3 h 5 min")), "12:30 am in 24-hour clock": hm(tm("12:30 am"))}
for k, v in DOMS: assert chk[k] == v, (k, chk[k], v)
assert len(set(v for k, v in DOMS)) == 20
random.seed(1010); chain = DOMS[:]; random.shuffle(chain)
dom = [("START" if k == 0 else chain[k - 1][1], x[0]) for k, x in enumerate(chain)] + [(chain[-1][1], "FINISH")]
dom_print = dom[:]; random.shuffle(dom_print)
dom_html = "".join(f'<div class="dom"><div class="h l">{l}</div><div class="h r">{r}</div></div>' for l, r in dom_print)
chain_key = "".join(f"<li>{x} = <b>{v}</b></li>" for x, v in chain)

ERR = [("3:20 pm in 24-hour clock", "= 13:20", "Added 10, not 12: <b>15:20</b>"),
       ("08:45 to 10:20", "= 1 h 75 min", "Took away like ordinary numbers. Count on: 15 min + 1 h 20 min = <b>1 h 35 min</b>"),
       ("1 h 30 min as a decimal", "= 1.3 h", "Minutes ÷ 60: 30 ÷ 60 = 0.5, so <b>1.5 h</b>"),
       ("2.4 h in hours and minutes", "= 2 h 40 min", "0.4 × 60 = 24: <b>2 h 24 min</b>"),
       ("0.35 kg in grams", "= 35 g", "1 kg = 1000 g, so × 1000: <b>350 g</b>"),
       ("1.2 l + 300 ml", "= 301.2 ml", "Same units first: 1200 ml + 300 ml = <b>1500 ml</b> (1.5 l)")]
assert hm(tm("3:20 pm")) == "15:20" and dur(gap("08:45", "10:20")) == "1 h 35 min" and F(90, 60) == F(3, 2) and dur(int(F("2.4") * 60)) == "2 h 24 min" and conv("0.35 kg", "g") == "350 g" and amt("1.2 l") + 300 == 1500
w1 = gap("16:48", "17:31"); assert dur(w1) == "43 min"
w2 = 12 * 400; assert conv(f"{w2} m", "km") == "4.8 km"
w3 = hm(tm("20:10") + int(F("1.75") * 60)); assert w3 == "21:55"
w4 = -(-2000 // 330); assert w4 == 7 and 6 * 330 == 1980
w5 = 80 * 54; assert w5 == 4320 and dur(w5 // 60) == "1 h 12 min" and w5 % 60 == 0

pack = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Units, Time &amp; Timetables Teacher Pack | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>
@page{{@bottom-left{{content:"Léim · leim.ie · Single-teacher licence · JC Maths LOs (2018 spec): {LO}";font-size:7pt}}}}
.proc td{{font-size:8.9pt;padding:3px 6px;line-height:1.32}}.proc td:first-child{{white-space:nowrap;font-weight:700;color:var(--green)}}
.p1 .note{{font-size:8.7pt;padding:6px 10px;line-height:1.35}}.p1 p{{font-size:9.5pt}}
.fym{{display:grid;grid-template-columns:repeat(4,1fr);margin-top:2mm}}
.fym .c{{border:2px dashed #9AA3AE;margin:-1px 0 0 -1px;height:17mm;position:relative;display:flex;align-items:center;justify-content:center}}
.fym .fc{{font-size:21pt;font-weight:800;text-align:center}}
.fym .tag{{position:absolute;top:1.2mm;left:3mm;font-size:6.5pt;color:var(--green);font-weight:800;text-transform:uppercase;letter-spacing:.04em}}
.idc{{border:2px dashed #9AA3AE;padding:3mm 4mm;margin-top:3mm}}.idc h3{{margin:0 0 2mm}}
.ss{{width:auto}}.ss td,.ss th{{padding:2px 7px;font-size:9.2pt;text-align:center}}.ss td{{min-width:15mm;height:5mm}}.ss tr th:first-child{{text-align:left}}
.doms{{display:grid;grid-template-columns:1fr 1fr;gap:2mm 6mm}}
.dom{{display:grid;grid-template-columns:1fr 1.6fr;border:2px dashed #9AA3AE;height:18.5mm}}
.dom .h{{display:flex;align-items:center;justify-content:center;text-align:center;padding:2mm;font-size:14pt;font-weight:800}}
.dom .r{{font-size:11pt}}
.dom .l{{background:var(--mist);border-right:2px solid var(--ink)}}
.poster{{height:255mm;border:6px solid var(--night);border-radius:18px;padding:10mm;display:flex;flex-direction:column;justify-content:space-between}}
.poster h1{{font-size:40pt;text-align:center}}.poster p{{font-size:14pt!important}}
.ops{{display:grid;grid-template-columns:1fr 1fr;gap:4mm}}.ops div{{border-radius:14px;padding:6mm 4mm;text-align:center;font-size:13pt;line-height:1.5}}.ops b{{display:block;font-size:20pt;font-weight:800;margin-bottom:1mm}}
.big3{{display:grid;grid-template-columns:1fr 1fr 1fr;text-align:center;font-size:19pt;font-weight:800;white-space:nowrap}}.big3 span{{display:block;font-size:11pt;color:var(--muted);font-weight:700}}
.ws{{font-size:10pt;line-height:1.42}}.ws ol.q li{{margin:6px 0}}.ws .long{{height:22px}}
.eh td{{padding:5px 8px;font-size:9.8pt}}.eh td:first-child{{font-weight:700;width:30%}}.eh .gap{{display:block;border-bottom:1px solid #9AA3AE;height:16px}}
</style></head><body>

<div class="page p1">
  <div class="band"><div><div class="k">Junior Cycle Maths · Teacher pack</div><h1>Units, time &amp; timetables</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2018 specification): {LO} (units and time come back in timetables, speed, area, volume and money questions; speed, distance and time are taught later)</p>
  <div class="two">
    <div><h3>Aims</h3><p>By the end of the lesson students can convert between metric units of length, mass and capacity, compare and add amounts in mixed units, switch between the 12-hour and 24-hour clock, change between minutes and decimal hours, find time differences by counting on, and read timetables to plan a journey.</p></div>
    <div><h3>In this pack</h3><p>p.1 Teacher notes · p.2 Unit Line-Up cards + Timetable Swap A/B cards · p.3 Time Dominoes (cut-up) · p.4 Wall poster · p.5 Worksheet: Error Hunt + exam-style questions · p.6 Answers. Level: 1st year (Higher and Ordinary), or 3rd-year revision. Time: about 60 minutes. All questions and timetables are original.</p></div>
  </div>
  <h2 style="margin-top:8px">Procedure</h2>
  <table class="proc"><tbody>
    <tr><td>5 min</td><td><b>Lead-in: True or false?</b> Board "1.5 hours = 1 hour 50 minutes" and "1.5 km = 1500 m". Hands up for each. Ask why they're different. Don't settle it yet.</td></tr>
    <tr><td>10 min</td><td><b>Unit Line-Up</b> (p.2 cards; one each, 16 lengths in mm, cm and m). Students line up from shortest to longest without talking for the first minute, then they may move each other and must explain. Check against the key. Feedback: how did you compare 112 cm and 1180 mm? Elicit "same unit first" and "small unit → bigger number".</td></tr>
    <tr><td>8 min</td><td><b>Guided discovery: hours aren't decimals.</b> Board 0.5 h, 0.25 h, 0.1 h, 1.5 h, 2.75 h. Pairs turn them into minutes (a clock face helps). What's the rule? (× 60.) Back to the lead-in. Then 08:47 → 11:15 by counting on, and why 1115 − 847 doesn't work.</td></tr>
    <tr><td>12 min</td><td><b>Timetable Swap</b> (p.2, pairs: A and B each have half the times of the same bus timetable; don't show your card). Ask each other for the missing times ("When does Bus 2 get to Blackpool?"), fill the table, then answer the three questions on your card and check your partner's answers.</td></tr>
    <tr><td>10 min</td><td><b>Time Dominoes</b> (p.3), groups of 3–4. Start with START, work out the clue, find the domino with that answer on its left, and build the chain to FINISH. Answer chain below.</td></tr>
    <tr><td>12 min</td><td><b>Worksheet</b> (p.5). Error Hunt in pairs (find the mistake, name the rule, fix it), then the exam-style questions alone. Feedback on question 4: why do you need 7 cans and not 6?</td></tr>
    <tr><td>3 min</td><td><b>Exit ticket.</b> 1.25 h in hours and minutes, and 6:40 pm in 24-hour clock (1 h 15 min; 18:40). Homework: play <b>Clock Dash</b> at leim.ie/clock-dash.html (Bus timetables round) and copy three lines from the "Go back over these" list.</td></tr>
  </tbody></table>
  <div class="note"><b>Unit Line-Up key</b> (shortest → longest): {", ".join(line_sorted)}.<br>
  <b>Errors to look for:</b> 1.5 h = 1 h 50 min · subtracting times like ordinary numbers (2 h 68 min) · 3:20 pm = 13:20 · 19:05 = 9:05 pm · 12:30 am = 12:30 · × 100 instead of × 1000 (0.35 kg = 35 g) · dividing when going to a smaller unit · adding amounts in different units · answers with no unit. <b>Support:</b> a clock face and a "km → m → cm → mm" unit ladder on the desk. <b>Fast finishers:</b> how many seconds are in a week? Which is longer: 0.3 of a day or 7 hours?</div>
  <p class="small"><b>Domino answer chain</b> (START → FINISH):</p>
  <ol class="small" style="columns:2;column-gap:12px;font-size:7.8pt;line-height:1.35;margin:0;padding-left:16px">{chain_key}</ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">Cut up the cards · one swap card per student</div><h1>Unit Line-Up + Timetable Swap</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.5pt;margin:0"><b>Unit Line-Up.</b> Cut out the 16 cards and give one to each student. Line up from the shortest to the longest. (Big class? Print twice and make two lines.)</p>
  <div class="fym">{line_html}</div>
  <p style="font-size:9.5pt;margin:4mm 0 0"><b>Timetable Swap.</b> You each have half of the same timetable. Don't show your card! Ask for the missing times, fill the table, then answer your questions.</p>
  {sw_card("A", (0, 2), SWQ_A)}
  {sw_card("B", (1, 3), SWQ_B)}
</div>

<div class="page">
  <div class="band"><div><div class="k">Groups of 3–4 · cut along the dashed lines</div><h1>Time Dominoes</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.5pt">Start with START. Work out the clue on the right, then find the domino with that answer on its left. Keep going until you reach FINISH. No calculators!</p>
  <div class="doms">{dom_html}</div>
</div>

<div class="page">
  <div class="poster">
    <h1>Units &amp; time</h1>
    <div class="big3"><div>1 km = 1000 m<span>length</span></div><div>1 kg = 1000 g<span>mass</span></div><div>1 l = 1000 ml<span>capacity</span></div></div>
    <p style="text-align:center;font-size:12pt;margin:0"><b>Big → small:</b> × (3.4 km = 3400 m) · <b>small → big:</b> ÷ (250 g = 0.25 kg) · 1 m = 100 cm · 1 cm = 10 mm · 1 t = 1000 kg</p>
    <div class="ops">
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>24-hour clock</b>pm: add 12 → 2:35 pm = 14:35<br>12:40 am = 00:40<br>19:05 = 7:05 pm</div>
      <div style="background:var(--green-soft)"><b>Hours ≠ decimals</b>60 min in an hour<br>0.5 h = 30 min · 0.1 h = 6 min<br>45 min = 45 ÷ 60 = 0.75 h</div>
      <div style="background:var(--green-soft)"><b>Count on</b>08:47 → 09:00 = 13 min<br>09:00 → 11:00 = 2 h<br>11:00 → 11:15 = 15 min</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Timetables</b>Column = one bus<br>Row = one stop<br>— = doesn't stop</div>
    </div>
    <p style="text-align:center;font-size:12pt;margin:0"><b>Same units first,</b> and always write the unit in your answer.</p>
    <p style="text-align:center;font-size:10pt;color:var(--muted)">Léim · leim.ie · Play Clock Dash: leim.ie/clock-dash.html</p>
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
    <li>A bus leaves Mallow at 16:48 and arrives in Cork at 17:31. How long is the journey?<span class="long"></span></li>
    <li>Darragh runs 12 laps of a 400 m track. How far does he run, in km?<span class="long"></span></li>
    <li>A film is 1.75 hours long. It starts at 20:10. When does it end?<span class="long"></span><span class="long"></span></li>
    <li>How many 330 ml cans of water are needed to fill a 2 litre jug? Explain.<span class="long"></span><span class="long"></span></li>
    <li>A phone charges 1% every 54 seconds. How long does it take to charge from 20% to 100%? Give your answer in hours and minutes.<span class="long"></span><span class="long"></span></li>
  </ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">For the teacher</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>Timetable Swap</h2>
  <table class="ss"><tr><th>Stop</th>{"".join(f"<th>Bus {i}</th>" for i in range(1, 5))}</tr>{"".join(f"<tr><th>{s}</th>" + "".join(f"<td>{SW[b][j] or '—'}</td>" for b in range(4)) + "</tr>" for j, s in enumerate(SW_STOPS))}</table>
  <p style="font-size:9.6pt;margin-top:2mm"><b>A:</b> {" · ".join(f"{i}. {a}" for i, (q, a) in enumerate(SWQ_A, 1))} (arrives 08:50) &nbsp; <b>B:</b> {" · ".join(f"{i}. {a}" for i, (q, a) in enumerate(SWQ_B, 1))} (journeys 44, 48, 40, 47 min)</p>
  <h2>A. Error Hunt</h2>
  <table><tbody>{"".join(f"<tr><td style='width:32%'><b>{q}</b> {w}</td><td>{r}</td></tr>" for q,w,r in ERR)}</tbody></table>
  <h2>B. Exam-style questions</h2>
  <ol class="q">
    <li>16:48 → 17:00 = 12 min; 17:00 → 17:31 = 31 min: <b>{dur(w1)}</b></li>
    <li>12 × 400 = 4800 m = <b>4.8 km</b></li>
    <li>1.75 h = 1 h 45 min; 20:10 + 1 h 45 min = <b>{w3}</b></li>
    <li>2 l = 2000 ml; 2000 ÷ 330 = 6.06…; 6 cans = 1980 ml isn't quite full, so <b>{w4} cans</b></li>
    <li>80% to charge; 80 × 54 = 4320 s = 72 min = <b>1 h 12 min</b></li>
  </ol>
  <h2>Marking tip</h2>
  <p>Give credit for each step, as the exam does: a correct method with one slip (e.g. counting on correctly but adding wrongly) still earns most of the marks. Insist on units in every answer, and on 24-hour times written with four digits (09:05).</p>
</div>
</body></html>"""

cover = """<!doctype html><html><head><meta charset="utf-8"><style>
body{margin:0;width:1200px;height:1200px;background:#1B2430;font-family:Inter,sans-serif;color:#fff;display:flex;flex-direction:column;justify-content:space-between;padding:90px;box-sizing:border-box}
.k{display:inline-block;background:#2E7D57;border-radius:99px;padding:12px 26px;font-weight:700;font-size:28px;letter-spacing:.06em;text-transform:uppercase}
h1{font-size:104px;font-weight:800;line-height:1.1;letter-spacing:-.03em;margin:40px 0 0}
h1 span{background:#F6CF5A;color:#1B2430;padding:0 14px}
.sub{font-size:38px;color:#C9D1DA;margin-top:36px;line-height:1.35}
.em{font-size:50px;margin-top:30px;font-weight:800;letter-spacing:.01em;color:#F6CF5A}
.foot{display:flex;justify-content:space-between;align-items:center;font-size:34px;font-weight:700}
.price{background:#F6CF5A;color:#1B2430;border-radius:16px;padding:14px 28px}
</style></head><body>
<div><span class="k">Junior Cycle Maths · Teacher pack</span>
<h1><span>Units, Time</span><br><span>&amp; Timetables</span></h1>
<div class="sub">Unit Line-Up · Timetable Swap A/B<br>Time Dominoes · Poster · Worksheet + answers</div>
<div class="em">1.5 h = 1 h 30 min · 2:35 pm = 14:35</div></div>
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
    pdf("teacher-pack", os.path.join(OUT, "Units-Time-Timetables-Teacher-Pack-Leim.pdf"))
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--hide-scrollbars", "--window-size=1200,1200",
                    f"--screenshot={os.path.join(OUT, f'{SLUG}-cover.png')}", f"{SLUG}-cover.html"], cwd=SRC, check=True, capture_output=True)
