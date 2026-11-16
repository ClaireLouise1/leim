#!/usr/bin/env python3
"""Statistics 1: questions, data & tables (JC Maths topic 12): free sheet + teacher pack + Payhip cover.
Run from the repo root: python3 src/build_statistics1_pdfs.py OUTDIR
Writes src/statistics-questions-data-tables-*.html; PDFs/cover PNG go to OUTDIR (free sheet also to printables/).
Data types are checked with the same keyword classifier as src/test_data_detective.py; counts, totals and
fractions are computed from the raw data lists and asserted."""
import os, sys, random, subprocess, re
from fractions import Fraction as F
from collections import Counter
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC)
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/stats"; os.makedirs(OUT, exist_ok=True)
SLUG = "statistics-questions-data-tables"
LO = "SP.3a, SP.3b, SP.3c"
NOM, ORD, DIS, CON = "categorical nominal", "categorical ordinal", "numerical discrete", "numerical continuous"
def kind(v):
    s = v.lower()
    if s.startswith("the number of"): return DIS
    if re.search(r"\b(height|mass|time each|time to|length|temperature|arm span|amount of rain|distance|how far|time taken)\b", s): return CON
    if re.search(r"size|grade|agree|star rating|finishing position|year each|spicy|how often|rating", s): return ORD
    return NOM
def fr(x): x = F(x); return f"{x.numerator}/{x.denominator}"
def freq(data, cats): c = Counter(data); assert sum(c[k] for k in cats) == len(data); return [c[k] for k in cats]
def gate(n):  # tally marks as text-decoration gates
    g = '<span class="gt">||||</span>'; return " ".join([g] * (n // 5) + (["|" * (n % 5)] if n % 5 else []))

# ---------- free sheet ----------
A = ["the number of pets each student has", "each student's favourite type of film", "the height of each player on a basketball team",
     "the size of jumper each student wears (S, M, L, XL)", "the time each student takes to walk to school", "the county each student's mother was born in",
     "the number of goals scored in each camogie match", "how much each student agrees with \"Phones should be banned in school\" (strongly agree to strongly disagree)"]
A_ans = [DIS, NOM, CON, ORD, CON, NOM, DIS, ORD]
assert [kind(x) for x in A] == A_ans, [kind(x) for x in A]
B = [("Is this a statistical question? \"How long do students in my class sleep on a school night?\"", "Yes: the answers will vary"),
     ("Is this a statistical question? \"What time does the school bus leave?\"", "No: it has one fixed answer"),
     ("Liam asks 30 of the 520 students in his school how they get to school. What is the population?", "All 520 students in the school"),
     ("In question 11, what is the sample?", "The 30 students Liam asked"),
     ("To find out how much sport 1st years play, Ella asks the 1st-year hurling panel. Why is this sample biased?", "Hurlers play more sport than most: other 1st years are left out"),
     ("Rewrite this question so it is fair: \"Don't you agree that the school day is too long?\"", "e.g. \"What do you think of the length of the school day?\""),
     ("Is rainfall data downloaded from Met Éireann primary or secondary data?", "Secondary"),
     ("What is it called when you collect data from EVERY member of the population?", "A census")]
# C: raw data
travel = "W B B C W B Bi W B C B W B Bi B W C B W B W B C W".split()
cats = ["W", "B", "C", "Bi"]; fT = freq(travel, cats); N = len(travel)
assert fT == [8, 10, 4, 2] and N == 24
mins = [12, 27, 5, 34, 18, 22, 9, 41, 15, 26, 30, 8, 19, 23, 37, 14, 28, 3, 21, 16]
cls = [(0, 9), (10, 19), (20, 29), (30, 39), (40, 49)]; fM = [sum(a <= m <= b for m in mins) for a, b in cls]
assert sum(fM) == len(mins) == 20 and fM == [4, 6, 6, 3, 1], fM
Cq = [("Make a frequency table (with a tally column) for the travel data above. How many walk?", str(fT[0])),
      ("How many students take the bus?", str(fT[1])),
      ("How many students were asked altogether?", str(N)),
      ("How many more students take the bus than come by car?", str(fT[1] - fT[2])),
      ("What fraction of the students cycle (Bi)? Give it in its simplest form.", fr(F(fT[3], N))),
      ("What fraction of the students walk? Simplest form.", fr(F(fT[0], N))),
      ("Group the homework times in classes 0–9, 10–19, 20–29, 30–39, 40–49. How many are in 10–19?", str(fM[1])),
      ("How many homework times are 30 minutes or more?", str(fM[3] + fM[4]))]
assert [a for q, a in Cq] == ["8", "10", "24", "6", "1/12", "1/3", "6", "4"], [a for q, a in Cq]
D = [("Put in order: analyse the data, pose a question, interpret the results, collect the data.", "Pose a question, collect the data, analyse the data, interpret the results"),
     ("Which stage is this? \"Cian draws a bar chart of his results.\"", "Analyse the data"),
     ("Best way to collect data on how many cars pass the school gate between 8:30 and 9:00?", "Observation (watch and count)"),
     ("Best way to collect data on whether a paper plane flies further with bigger wings?", "An experiment"),
     ("What is wrong with these answer boxes for \"How many books did you read last year?\" 0–2 · 2–4 · 4–6", "They overlap (2 and 4 fit two boxes) and there's no box above 6"),
     ("Write better answer boxes for question 29.", "e.g. 0–2 · 3–5 · 6–8 · 9 or more")]
pets = [0, 1, 2, 1, 0, 3, 1, 2, 0, 1, 4, 1, 2, 0, 1, 1, 3, 0, 2, 1, 1, 0, 2, 1, 5]
fP = [pets.count(k) for k in range(6)]; assert sum(fP) == 25 and fP == [6, 10, 5, 2, 1, 1], fP
E = [("The number of pets owned by 25 students: " + ", ".join(map(str, pets)) + ". (a) Make a frequency table. (b) What type of data is this? (c) How many students have 2 or more pets? (d) What fraction have no pets?",
      f"(a) 0: {fP[0]}, 1: {fP[1]}, 2: {fP[2]}, 3: {fP[3]}, 4: {fP[4]}, 5: {fP[5]} (total 25) (b) <b>numerical discrete</b> (c) <b>{sum(fP[2:])}</b> (d) <b>{fr(F(fP[0], 25))}</b>"),
     ("A café asks: \"How much did you love our new menu?\" with the boxes □ A lot □ Loads. (a) Why is this question biased? (b) Rewrite the question and the boxes so they are fair.",
      "(a) \"Love\" assumes they liked it, and every box is positive. (b) e.g. \"How would you rate our new menu?\" □ Very good □ Good □ OK □ Poor □ Very poor"),
     ("Niamh wants to know how long 1st years in her school spend on their phones each day. She asks the 15 members of the computer club. (a) Give two reasons why her results may not be reliable. (b) How could she improve her sample?",
      "(a) The computer club may use screens more than other 1st years (biased), and 15 is a small sample. (b) Pick a bigger <b>random</b> sample from the full list of 1st years."),
     ("Aoife wants to find out if 3rd years spend longer on homework than 1st years. (a) Write a statistical question. (b) Name the two pieces of data she needs and their types. (c) After collecting the data, what are the next two stages?",
      "(a) e.g. \"Do 3rd years in my school spend longer on homework each night than 1st years?\" (b) year group (<b>categorical ordinal</b>) and time spent (<b>numerical continuous</b>) (c) <b>analyse the data</b>, then <b>interpret the results</b>")]
assert kind("the year each student is in") == ORD and kind("the time each student spends") == CON
assert sum(fP[2:]) == 9 and fr(F(fP[0], 25)) == "6/25"

def qs(items, start): return "".join(f"<li>{x if isinstance(x, str) else x[0]} <span class='line'></span></li>" for x in items)
TYPES4 = """<table class="t4"><tr><th></th><th>no order / counted</th><th>order / measured</th></tr>
<tr><th>Categorical<br><small>words</small></th><td><b>Nominal</b><br>favourite sport, eye colour, county</td><td><b>Ordinal</b><br>S, M, L · mild, medium, hot · star ratings</td></tr>
<tr><th>Numerical<br><small>numbers</small></th><td><b>Discrete</b> (counted)<br>siblings, goals, texts</td><td><b>Continuous</b> (measured)<br>height, mass, time, temperature</td></tr></table>"""
small_tbl = f"""<table class="ft"><tr><th>Travel</th><th>Tally</th><th>Frequency</th></tr>
<tr><td>Walk</td><td>{gate(7)}</td><td>7</td></tr><tr><td>Bus</td><td>{gate(11)}</td><td>11</td></tr><tr><td>Car</td><td>{gate(4)}</td><td>4</td></tr><tr><td><b>Total</b></td><td></td><td><b>22</b></td></tr></table>"""
CSS_COMMON = """.gt{text-decoration:line-through;text-decoration-color:#D9534F;text-decoration-thickness:1.6px;letter-spacing:1px}
.t4{width:100%;border-collapse:collapse;margin:4px 0}.t4 th,.t4 td{border:1px solid #D1D5DB;padding:3px 6px;font-size:9pt;text-align:center}.t4 th{background:var(--green-soft);color:var(--ink);text-transform:none;letter-spacing:0}
.ft{width:auto;margin:3px 0}.ft td,.ft th{padding:1px 10px;font-size:9pt}"""

sheet = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Statistics: questions, data and tables: rules and practice | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>@page{{@bottom-left{{content:"Léim · leim.ie · Free to print for home or class · JC Maths LOs (2018 spec): {LO}"}}}}
.tight{{font-size:9.6pt;line-height:1.38}}.tight h2{{margin:8px 0 3px;font-size:13pt}}.tight .note,.tight .tip{{padding:5px 10px;margin:5px 0}}.tight p{{margin:3px 0}}.tight ul{{margin:3px 0;padding-left:16px}}
ol.q{{padding-left:30px}}ol.q li{{margin:7px 0}}
.p2{{font-size:9pt;line-height:1.32}}.p2 ol.q li{{margin:2.6px 0}}.p2 .line{{min-width:70px}}.p2 h2{{margin:7px 0 3px}}.p2 .data{{font-size:9pt;margin:2px 0}}
.ans td{{padding:3px 6px;font-size:8.6pt}}
{CSS_COMMON}
</style></head><body>
<div class="page tight">
  <div class="band"><div><div class="k">Junior Cycle Maths · Free revision sheet</div><h1>Statistics: questions, data &amp; tables</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2018 specification): {LO}. Play the game: <b>leim.ie/data-detective.html</b></p>
  <div class="two">
   <div><h2>1. Four types of data</h2>
    {TYPES4}
    <p>Ask: <b>words or numbers?</b> Then: words in an <b>order</b>? Numbers <b>counted</b> or <b>measured</b>? Counted answers can't be in between (2.5 brothers); measured ones can (1.555 m).</p>
    <h2>2. A statistical question</h2>
    <p>One where the answers <b>vary</b>, so you need data: "How long do students in my class sleep?" Not: "How tall am I?" (one fixed answer).</p>
    <h2>3. Population, sample, census</h2>
    <ul><li><b>Population:</b> everyone you want to know about (all 650 students).</li><li><b>Sample:</b> the group you actually ask (40 of them).</li>
    <li><b>Census:</b> data from <b>every</b> member of the population.</li><li><b>Random sample:</b> everyone has the same chance of being picked (names from a hat, a random number generator).</li></ul>
    <h2>4. Keep it fair (no bias)</h2>
    <ul><li><b>Biased sample:</b> asks only one kind of person (the gym, your friends, the choir).</li><li><b>Leading question:</b> pushes an answer: "Don't you agree…?", "Surely…", "How much do you love…?"</li>
    <li><b>Answer boxes:</b> no overlaps, no gaps, a box for every answer: 0–2 · 3–5 · 6–8 · 9 or more.</li></ul></div>
   <div><h2>5. Collecting the data</h2>
    <p><b>Primary data:</b> you collect it. <b>Secondary data:</b> someone else did (Met Éireann, the CSO, a website).</p>
    <p><b>Survey</b> (ask people) · <b>observation</b> (watch and count) · <b>experiment</b> (change one thing, measure what happens) · <b>existing data</b> (look it up).</p>
    <div class="note"><b>The four stages of an investigation (CBA 2):</b><br>1. Pose a question → 2. Collect the data → 3. Analyse the data → 4. Interpret the results.</div>
    <h2>6. Tally marks and frequency tables</h2>
    <p>Go through the data once, one tally mark per answer. Every 5th mark crosses the other four. The <b>frequency</b> is how many times an answer comes up; the frequencies add up to the number asked.</p>
    {small_tbl}
    <h2>7. Grouped data</h2>
    <p>Lots of different numbers? Use classes of equal width: 0–9, 10–19, 20–29… Every value goes in exactly one class: 27 goes in 20–29, 30 goes in 30–39.</p></div>
  </div>
  <div class="tip"><b>Exam tip:</b> name the type of data with <b>both words</b> (numerical discrete, not just "numerical"), and when you say a sample is biased, say <b>who is left out</b>.</div>
</div>

<div class="page p2">
  <div class="band"><div><div class="k">Practice · 34 questions</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. What type of data? (nominal, ordinal, discrete or continuous)</h2><ol class="q">{qs(A, 1)}</ol>
  <h2>B. Questions, samples and bias</h2><ol class="q" start="9">{qs(B, 9)}</ol>
  <h2>C. Tally and frequency tables</h2>
  <p class="data"><b>Travel data</b> for 24 students (W = walk, B = bus, C = car, Bi = bike): {", ".join(travel)}</p>
  <p class="data"><b>Homework times</b> (minutes) for 20 students: {", ".join(map(str, mins))}</p>
  <ol class="q" start="17">{qs(Cq, 17)}</ol>
  <h2>D. Plan an investigation</h2><ol class="q" start="25">{qs(D, 25)}</ol>
  <p class="small" style="margin-top:4px">Questions 31–34 are on the next page.</p>
</div>

<div class="page">
  <div class="band"><div><div class="k">Exam-style · then check</div><h1>Exam corner + answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>E. Exam-style questions (show your work)</h2>
  <ol class="q" start="31">{"".join(f"<li>{q}<span class='long'></span><span class='long'></span></li>" for q, a in E)}</ol>
  <h2 style="margin-top:10px">Answers</h2>
  <table class="ans"><tbody>
   <tr><td><b>A</b></td><td>{" · ".join(f"{i}. {t}" for i, t in enumerate(A_ans, 1))}</td></tr>
   <tr><td><b>B</b></td><td>{" · ".join(f"{i}. {a}" for i, (q, a) in enumerate(B, 9))}</td></tr>
   <tr><td><b>C</b></td><td>Table: walk {fT[0]}, bus {fT[1]}, car {fT[2]}, bike {fT[3]} (total {N}) · {" · ".join(f"{i}. {a}" for i, (q, a) in enumerate(Cq, 17))}</td></tr>
   <tr><td><b>D</b></td><td>{" · ".join(f"{i}. {a}" for i, (q, a) in enumerate(D, 25))}</td></tr>
   <tr><td><b>E</b></td><td>{" · ".join(f"{i}. {a}" for i, (q, a) in enumerate(E, 31))}</td></tr>
  </tbody></table>
  <div class="note"><b>Got one wrong?</b> Check: did you ask "counted or measured?" Did you say who the sample leaves out? Do your frequencies add up to the total? Then play <b>Data Detective</b> at leim.ie/data-detective.html: the "Go back over these" list at the end shows the rule for each mistake.</div>
  <p class="small">All questions written by Léim. Léim is independent and not connected with the State Examinations Commission or the NCCA.</p>
</div>
</body></html>"""

# ---------- teacher pack ----------
SORT = ["the number of brothers and sisters each student has", "the height of each student", "each student's favourite sport", "the T-shirt size each student wears (S, M, L)",
        "the time each student takes to run 100 m", "the number of goals in each match", "each student's eye colour", "the star rating each customer gives a film (1 to 5 stars)",
        "the mass of each schoolbag", "the number of texts each student sent yesterday", "the county each student was born in", "how spicy each person likes curry (mild, medium, hot)",
        "the temperature at noon each day", "the number of people in each house", "how each student gets to school", "each student's Junior Cycle grade in English",
        "the length of each student's foot", "the number of books each student owns", "the brand of each student's runners", "how often each student reads (never, sometimes, often)",
        "the distance each student lives from school", "the number of points scored in each GAA match", "each student's favourite pizza topping", "the finishing position of each runner in a race"]
types = [kind(x) for x in SORT]; cnt = Counter(types)
assert len(SORT) == 24 and all(cnt[t] == 6 for t in (NOM, ORD, DIS, CON)), cnt
random.seed(12); sp = SORT[:]; random.shuffle(sp)
sort_html = "".join(f'<div class="c"><span class="tag">Card {i}</span><div class="fc">{x[0].upper() + x[1:]}</div></div>' for i, x in enumerate(sp, 1))
sort_key = " · ".join(f"<b>{t.split()[1].capitalize()}:</b> " + ", ".join(str(i) for i, x in enumerate(sp, 1) if kind(x) == t) for t in (NOM, ORD, DIS, CON))
FIX = [("1", "Don't you agree the canteen food is terrible?", "Leading question. Fair: \"How would you rate the canteen food?\" □ Very good □ Good □ OK □ Poor □ Very poor"),
       ("2", "How old are you? □ 12–13 □ 13–14 □ 14–15", "Boxes overlap (13, 14 fit twice) and older students have no box. Use □ 12 □ 13 □ 14 □ 15 □ 16 or older"),
       ("3", "How much time do you spend on your phone at lunch? □ A little □ A lot", "Vague: \"a little\" means different things. Use minutes: □ 0 □ 1–10 □ 11–20 □ 21–30 □ more than 30"),
       ("4", "What is your full name and home address?", "Not needed and too personal. Leave it out (keep surveys anonymous)"),
       ("5", "How many times did you go to the shop at lunch last week? □ 1–2 □ 3–4", "No box for 0 or for more than 4. Use □ 0 □ 1–2 □ 3–4 □ 5 or more"),
       ("Plan", "\"We'll give the questionnaire to our friends in 2nd year.\"", "Biased sample: friends are alike and only one year is asked. Pick a random sample from every year group")]
DOMS = [("number of goals in a match: what type of data?", "discrete"), ("height of a student: what type of data?", "continuous"),
        ("favourite colour: what type of data?", "nominal"), ("T-shirt size (S, M, L): what type of data?", "ordinal"),
        ("tally: two full gates and 3 more marks", "13"), ("total of the frequencies 4, 7 and 9", "20"),
        ("data from EVERY member of the population", "census"), ("the smaller group you actually ask", "sample"),
        ("everyone you want to know about", "population"), ("data from the CSO website", "secondary"),
        ("data you collect yourself", "primary"), ("\"Don't you agree that…?\"", "leading question"),
        ("the stage after \"pose a question\"", "collect the data"), ("the last stage of an investigation", "interpret the results"),
        ("watching and counting cars at the gate", "observation"), ("6 of 24 students walk: what fraction?", "1/4"),
        ("which class for 37? 0–9, 10–19, 20–29, 30–39", "30–39"), ("a sample where everyone has the same chance", "random"),
        ("9 walk, 4 cycle: how many more walk?", "5"), ("frequencies 3, ?, 8 with a total of 18", "7")]
assert kind("the number of goals") == DIS and kind("the height of a student") == CON and kind("favourite colour") == NOM and kind("T-shirt size") == ORD
assert 2 * 5 + 3 == 13 and 4 + 7 + 9 == 20 and F(6, 24) == F(1, 4) and 30 <= 37 <= 39 and 9 - 4 == 5 and 18 - 3 - 8 == 7
assert len(set(a for q, a in DOMS)) == 20
random.seed(1212); chain = DOMS[:]; random.shuffle(chain)
dom = [("START" if k == 0 else chain[k - 1][1], x[0]) for k, x in enumerate(chain)] + [(chain[-1][1], "FINISH")]
dom_print = dom[:]; random.shuffle(dom_print)
dom_html = "".join(f'<div class="dom"><div class="h l{" sm" if len(l) > 11 else ""}">{l}</div><div class="h r">{r}</div></div>' for l, r in dom_print)
chain_key = "".join(f"<li>{x} = <b>{a}</b></li>" for x, a in chain)
ERR = [("Number of brothers and sisters", "numerical continuous", "You can't have 2.5 siblings: it's counted, so <b>numerical discrete</b>"),
       ("Star rating of a film (1 to 5 stars)", "numerical discrete", "Stars are ordered categories (a rating, not a count): <b>categorical ordinal</b>"),
       ("Asking the school choir about favourite music", "a fair random sample", "Biased: choir members like singing. Pick students <b>at random</b> from the whole school"),
       ("20 students asked; frequencies 5, 8, 6", "table complete", "5 + 8 + 6 = 19: <b>one student is missing</b>, so recount"),
       ("Answer boxes 0–5 · 5–10 · 10–15", "good boxes", "5 and 10 fit two boxes and there's no box above 15: <b>0–4 · 5–9 · 10–14 · 15 or more</b>"),
       ("Liam asks 40 of 600 students. Population?", "the 40 students", "That's the sample. The population is <b>all 600 students</b>")]
assert kind("the star rating each customer gives") == ORD and 5 + 8 + 6 == 19
heights = [148, 152, 139, 161, 155, 143, 158, 150, 147, 163, 141, 156, 152, 149, 160, 145, 154, 151, 138, 157]
hc = [(135, 139), (140, 144), (145, 149), (150, 154), (155, 159), (160, 164)]; fH = [sum(a <= h <= b for h in heights) for a, b in hc]
assert fH == [2, 2, 4, 5, 4, 3] and sum(fH) == 20, fH
w2 = F(fH[4] + fH[5], 20); assert w2 == F(7, 20)
lunch = "S H S C S H S S C H S C S S H S C S S H".split(); fL = freq(lunch, ["S", "H", "C"]); assert fL == [11, 5, 4]

pack = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Statistics Teacher Pack | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>
@page{{@bottom-left{{content:"Léim · leim.ie · Single-teacher licence · JC Maths LOs (2018 spec): {LO}";font-size:7pt}}}}
.proc td{{font-size:8.9pt;padding:3px 6px;line-height:1.32}}.proc td:first-child{{white-space:nowrap;font-weight:700;color:var(--green)}}
.p1 .note{{font-size:8.5pt;padding:6px 10px;line-height:1.35}}.p1 p{{font-size:9.4pt}}
.fym{{display:grid;grid-template-columns:repeat(4,1fr);margin-top:2mm}}
.fym .c{{border:2px dashed #9AA3AE;margin:-1px 0 0 -1px;height:17mm;position:relative;display:flex;align-items:center;justify-content:center;padding:4mm 2mm 1mm}}
.fym .fc{{font-size:8.6pt;font-weight:700;text-align:center;line-height:1.22}}
.fym .tag{{position:absolute;top:1.2mm;left:3mm;font-size:6.5pt;color:var(--green);font-weight:800;text-transform:uppercase;letter-spacing:.04em}}
.hdr{{display:grid;grid-template-columns:repeat(4,1fr);gap:2mm;margin-top:2mm}}.hdr div{{border:2px dashed #9AA3AE;text-align:center;padding:2mm;font-weight:800;font-size:10pt;background:var(--green-soft)}}
.fix td{{font-size:9pt;padding:3px 6px}}.fix td:first-child{{font-weight:800;color:var(--green);width:9mm}}
.doms{{display:grid;grid-template-columns:1fr 1fr;gap:2mm 6mm}}
.dom{{display:grid;grid-template-columns:1fr 1.7fr;border:2px dashed #9AA3AE;height:18mm}}
.dom .h{{display:flex;align-items:center;justify-content:center;text-align:center;padding:2mm;font-size:13pt;font-weight:800}}
.dom .l.sm{{font-size:10.5pt}}.dom .r{{font-size:10pt}}
.dom .l{{background:var(--mist);border-right:2px solid var(--ink)}}
.poster{{height:255mm;border:6px solid var(--night);border-radius:18px;padding:10mm;display:flex;flex-direction:column;justify-content:space-between}}
.poster h1{{font-size:40pt;text-align:center}}.poster p{{font-size:14pt!important}}
.ops{{display:grid;grid-template-columns:1fr 1fr;gap:4mm}}.ops div{{border-radius:14px;padding:5mm 4mm;text-align:center;font-size:12.5pt;line-height:1.45}}.ops b{{display:block;font-size:19pt;font-weight:800;margin-bottom:1mm}}
.steps{{display:flex;gap:2mm;justify-content:center;align-items:center;font-size:13pt;font-weight:800}}.steps span{{background:var(--night);color:#fff;border-radius:10px;padding:3mm 4mm;text-align:center}}
.ws{{font-size:9.8pt;line-height:1.4}}.ws ol.q li{{margin:5px 0}}.ws .long{{height:20px}}
.eh td{{padding:4px 8px;font-size:9.4pt}}.eh td:first-child{{font-weight:700;width:30%}}.eh .gap{{display:block;border-bottom:1px solid #9AA3AE;height:15px}}
.a6{{font-size:9.2pt;line-height:1.36}}.a6 td{{font-size:8.8pt;padding:3px 6px}}.a6 h2{{margin:8px 0 3px}}.a6 ol.q li{{margin:3px 0}}
{CSS_COMMON}
</style></head><body>

<div class="page p1">
  <div class="band"><div><div class="k">Junior Cycle Maths · Teacher pack</div><h1>Statistics: questions, data &amp; tables</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2018 specification): {LO} (graphs, averages and comparing data sets are taught later, in Statistics 2)</p>
  <div class="two">
    <div><h3>Aims</h3><p>By the end of the lesson students can classify data as categorical (nominal, ordinal) or numerical (discrete, continuous), pose a statistical question, tell a population from a sample, spot biased samples and leading questions, design fair answer boxes, and organise raw data in a tally and frequency table. Good preparation for CBA 2.</p></div>
    <div><h3>In this pack</h3><p>p.1 Teacher notes · p.2 Data Sort cards + Fix the Survey · p.3 Data Dominoes (cut-up) · p.4 Wall poster · p.5 Worksheet: Error Hunt + exam-style questions · p.6 Answers. Level: 1st year (Higher and Ordinary), or 3rd-year revision. Time: about 60 minutes. All questions are original.</p></div>
  </div>
  <h2 style="margin-top:8px">Procedure</h2>
  <table class="proc"><tbody>
    <tr><td>5 min</td><td><b>Lead-in: Two questions.</b> Board: "How tall am I?" and "How tall are the students in this class?" Which one needs data? Why? Elicit "the answers vary": a <b>statistical question</b>.</td></tr>
    <tr><td>8 min</td><td><b>Guided discovery: counted or measured?</b> Ask three students their number of siblings and their height. "Could anyone have 2.5 siblings? Could anyone be 1.555 m?" Elicit <b>discrete</b> v <b>continuous</b>, then words v numbers, and order v no order.</td></tr>
    <tr><td>12 min</td><td><b>Data Sort</b> (p.2, groups of 3–4). Lay out the four header cards; groups sort the 24 cards into the four types and must agree a reason for each. Check against the key. Feedback: which cards caused arguments? (Usually star ratings and grades.)</td></tr>
    <tr><td>10 min</td><td><b>Fix the Survey</b> (p.2, pairs). Find the six problems with the class's first questionnaire and plan, and rewrite each one. Feedback: build a class checklist for a good survey.</td></tr>
    <tr><td>10 min</td><td><b>Data Dominoes</b> (p.3), groups of 3–4. Start at START, answer the clue, find the domino with that answer on its left, build the chain to FINISH. Chain below.</td></tr>
    <tr><td>12 min</td><td><b>Worksheet</b> (p.5). Error Hunt in pairs, then the exam-style questions alone. Fast finishers: ask the class the fixed lunchtime question and make a tally and frequency table.</td></tr>
    <tr><td>3 min</td><td><b>Exit ticket.</b> "Type of data: the time each student takes to get to school? Who is left out if you only ask the students on the bus?" (Numerical continuous; students who walk, cycle or come by car.) Homework: play <b>Data Detective</b> at leim.ie/data-detective.html (Fair or biased? round).</td></tr>
  </tbody></table>
  <div class="note"><b>Data Sort key:</b> {sort_key}.<br>
  <b>Errors to look for:</b> "categorical" or "numerical" with no second word · star ratings and grades called numerical · shoe size and age (leave them out of first lessons: textbooks differ) · "biased" with no reason · frequencies that don't add up to the number asked · overlapping answer boxes.</div>
  <p class="small"><b>Domino answer chain</b> (START → FINISH):</p>
  <ol class="small" style="columns:2;column-gap:12px;font-size:7.8pt;line-height:1.35;margin:0;padding-left:16px">{chain_key}</ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">Cut up the cards · groups of 3–4</div><h1>Data Sort + Fix the Survey</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.3pt;margin:0"><b>Data Sort.</b> Cut out the four headers and the 24 cards. Sort each card under the right header and agree a reason.</p>
  <div class="hdr"><div>Categorical<br>NOMINAL</div><div>Categorical<br>ORDINAL</div><div>Numerical<br>DISCRETE</div><div>Numerical<br>CONTINUOUS</div></div>
  <div class="fym">{sort_html}</div>
  <p style="font-size:9.3pt;margin:3mm 0 1mm"><b>Fix the Survey.</b> A 2nd-year class want to find out how students in their school spend lunchtime. Here is their first questionnaire and their plan. Find the problem in each line and write a better version.</p>
  <table class="fix"><tbody>{"".join(f"<tr><td>{n}</td><td style='width:47%'>{q}</td><td><span style='display:block;border-bottom:1px solid #9AA3AE;height:13px'></span><span style='display:block;border-bottom:1px solid #9AA3AE;height:13px'></span></td></tr>" for n, q, k in FIX)}</tbody></table>
</div>

<div class="page">
  <div class="band"><div><div class="k">Groups of 3–4 · cut along the dashed lines</div><h1>Data Dominoes</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.5pt">Start with START. Answer the clue on the right, then find the domino with that answer on its left. Keep going until you reach FINISH.</p>
  <div class="doms">{dom_html}</div>
</div>

<div class="page">
  <div class="poster">
    <h1>Statistics: data</h1>
    <p style="text-align:center;font-size:16pt!important;margin:0;font-weight:800">Words or numbers? Then: order? counted or measured?</p>
    <div class="ops">
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Nominal</b>categories, no order<br>favourite sport · eye colour · county</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Ordinal</b>categories in order<br>S, M, L · mild, medium, hot · star ratings</div>
      <div style="background:var(--green-soft)"><b>Discrete</b>numbers you COUNT<br>siblings · goals · texts</div>
      <div style="background:var(--green-soft)"><b>Continuous</b>numbers you MEASURE<br>height · mass · time · temperature</div>
    </div>
    <div class="steps"><span>1. Pose a<br>question</span>→<span>2. Collect<br>the data</span>→<span>3. Analyse<br>the data</span>→<span>4. Interpret<br>the results</span></div>
    <p style="text-align:center;margin:0"><b>Population</b> = everyone · <b>sample</b> = the ones you ask · <b>census</b> = ask everyone<br>Random sample · fair questions · no overlapping boxes · <b>no bias!</b></p>
    <p style="text-align:center;font-size:10pt;color:var(--muted)">Léim · leim.ie · Play Data Detective: leim.ie/data-detective.html</p>
  </div>
</div>

<div class="page ws">
  <div class="band"><div><div class="k">Worksheet</div><h1>Error Hunt + exam-style questions</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Error Hunt</h2>
  <p>Each answer has one mistake. Find it, say what's wrong, and write the right answer.</p>
  <table class="eh"><thead><tr><th>Question</th><th>Student's answer</th><th>The mistake and the right answer</th></tr></thead><tbody>
  {"".join(f"<tr><td>{q}</td><td>{w}</td><td><span class='gap'></span><span class='gap'></span></td></tr>" for q, w, r in ERR)}
  </tbody></table>
  <h2>B. Exam-style questions (show all your work)</h2>
  <ol class="q">
    <li>Name the type of data: (a) the number of emails a teacher gets each day (b) the time a candle takes to burn down (c) each student's favourite fruit (d) the level of each Irish exam paper taken (Higher, Ordinary, Foundation)<span class="long"></span></li>
    <li>The heights (cm) of 20 students: {", ".join(map(str, heights))}. (a) Make a grouped frequency table with classes 135–139, 140–144, … 160–164. (b) Which class has the most students? (c) What fraction of the students are 155 cm or taller?<span class="long"></span><span class="long"></span></li>
    <li>Twenty students said what they do at lunchtime (S = sport, H = homework club, C = chat): {", ".join(lunch)}. Make a frequency table. What type of data is this?<span class="long"></span></li>
    <li>A gym owner wants to know how often adults in his town exercise. He asks 25 people at his gym. Give two reasons why his results may be misleading, and suggest a better sample.<span class="long"></span><span class="long"></span></li>
    <li>Write a statistical question you could investigate about your class, a fair survey question for it with answer boxes, and say what type of data you would collect.<span class="long"></span><span class="long"></span></li>
  </ol>
</div>

<div class="page a6">
  <div class="band"><div><div class="k">For the teacher</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>Fix the Survey</h2>
  <table class="fix"><tbody>{"".join(f"<tr><td>{n}</td><td>{k}</td></tr>" for n, q, k in FIX)}</tbody></table>
  <h2>A. Error Hunt</h2>
  <table><tbody>{"".join(f"<tr><td style='width:34%'><b>{q}</b> → {w}</td><td>{r}</td></tr>" for q, w, r in ERR)}</tbody></table>
  <h2>B. Exam-style questions</h2>
  <ol class="q">
    <li>(a) <b>numerical discrete</b> (b) <b>numerical continuous</b> (c) <b>categorical nominal</b> (d) <b>categorical ordinal</b></li>
    <li>(a) {", ".join(f"{a}–{b}: {f}" for (a, b), f in zip(hc, fH))} (total 20) (b) <b>150–154</b> ({max(fH)} students) (c) {fH[4]} + {fH[5]} = {fH[4] + fH[5]}: <b>{fr(w2)}</b></li>
    <li>Sport {fL[0]}, homework club {fL[1]}, chat {fL[2]} (total 20) · <b>categorical nominal</b></li>
    <li>People at a gym exercise more than most adults (biased), and 25 is a small sample; the town's adults who don't go to his gym are left out. Better: a bigger <b>random</b> sample of adults from the whole town (e.g. from a full list), asked at different places and times.</li>
    <li>Any sensible answer, e.g. "How long do students in my class spend on homework each night?", "How many minutes did you spend on homework last night? □ 0–29 □ 30–59 □ 60–89 □ 90 or more": <b>numerical continuous</b> (grouped).</li>
  </ol>
  <h2>Marking tip</h2>
  <p>As in the exam, a type of data needs both words, and "biased" needs a reason (who is left out, or how the question pushes an answer). Accept any fair rewording of survey questions. A frequency table earns full marks only if the frequencies add up to the number asked.</p>
</div>
</body></html>"""
assert max(fH) == 5 and hc[fH.index(5)] == (150, 154) and fH.count(5) == 1

cover = """<!doctype html><html><head><meta charset="utf-8"><style>
body{margin:0;width:1200px;height:1200px;background:#1B2430;font-family:Inter,sans-serif;color:#fff;display:flex;flex-direction:column;justify-content:space-between;padding:90px;box-sizing:border-box}
.k{display:inline-block;background:#2E7D57;border-radius:99px;padding:12px 26px;font-weight:700;font-size:28px;letter-spacing:.06em;text-transform:uppercase}
h1{font-size:104px;font-weight:800;line-height:1.1;letter-spacing:-.03em;margin:40px 0 0}
h1 span{background:#F6CF5A;color:#1B2430;padding:0 14px}
.sub{font-size:38px;color:#C9D1DA;margin-top:36px;line-height:1.35}
.em{font-size:46px;margin-top:30px;font-weight:800;letter-spacing:.01em;color:#F6CF5A}
.foot{display:flex;justify-content:space-between;align-items:center;font-size:34px;font-weight:700}
.price{background:#F6CF5A;color:#1B2430;border-radius:16px;padding:14px 28px}
</style></head><body>
<div><span class="k">Junior Cycle Maths · Teacher pack</span>
<h1><span>Statistics:</span><br><span>Data &amp; Tables</span></h1>
<div class="sub">Data Sort cards · Fix the Survey<br>Data Dominoes · Poster · Worksheet + answers</div>
<div class="em">Counted or measured? · No bias!</div></div>
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
    pdf("teacher-pack", os.path.join(OUT, "Statistics-Teacher-Pack-Leim.pdf"))
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--hide-scrollbars", "--window-size=1200,1200",
                    f"--screenshot={os.path.join(OUT, f'{SLUG}-cover.png')}", f"{SLUG}-cover.html"], cwd=SRC, check=True, capture_output=True)
