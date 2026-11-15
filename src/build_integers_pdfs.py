#!/usr/bin/env python3
"""Integers & order of operations (JC Maths topic 1): free sheet + teacher pack + Payhip cover.
Run from the repo root: python3 src/build_integers_pdfs.py OUTDIR
Writes src/integers-order-of-operations-*.html; PDFs/cover PNG go to OUTDIR (free sheet also to printables/)."""
import os, sys, random, subprocess, html, re
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC)
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/ints"; os.makedirs(OUT, exist_ok=True)
M = "−"
def f(n): return (M + str(-n)) if n < 0 else str(n)
def ev(expr):  # evaluate a display expression
    e = expr.replace(M, "-").replace("×", "*").replace("÷", "/")
    e = re.sub(r"(\([^()]*\)|\d+)²", r"(\1)**2", e)
    v = eval(e); assert abs(v - round(v)) < 1e-9, expr; return int(round(v))
LO = "N.1a, N.1b, N.1c, U.1, U.2"

# ---------- free sheet ----------
A = [("Put in order, smallest first: 4, −7, 0, −2, 9, −10", "−10, −7, −2, 0, 4, 9"),
     ("Which is bigger, −3 or −8?", "−3"),
     ("Write &lt; or &gt;: −5 ___ −1", "−5 &lt; −1"),
     ("Start at −4 and hop 7 to the right. Where do you land?", "3"),
     ("Start at 2 and hop 6 to the left. Where do you land?", "−4"),
     ("What number is halfway between −6 and 2?", "−2")]
B = ["−6 + 9", "4 − 11", "−3 − 5", "7 + (−10)", "−2 − (−8)", "−12 + 4", "5 − (−6)", "−9 + (−3)"]
C = ["(−4) × 6", "(−7) × (−3)", "−36 ÷ 9", "(−48) ÷ (−6)", "8 × (−5)", "(−2) × (−3) × (−5)", "(−6)²", "−45 ÷ (−5)"]
D = ["3 + 5 × 2", "(3 + 5) × 2", "20 − 12 ÷ 4", "4 × 3²", "18 ÷ 6 × 3", "10 − (7 − 2)", "6 + 4 × (−3)", "(−2)² + 3 × (−4)"]
E = [("At 7 a.m. it was −5 °C in Cavan. By 2 p.m. it was 6 °C. By how many degrees did the temperature rise?", "6 − (−5) = 11 degrees"),
     ("Seán has €35 in his bank account. He spends €52. What is his balance now?", "35 − 52 = −€17 (overdrawn by €17)"),
     ("Find the value of 3x² − 2x when x = −4.", "3(16) − 2(−4) = 48 + 8 = 56"),
     ("Put brackets into 2 + 4 × 6 − 1 to make the answer 35.", "(2 + 4) × 6 − 1 = 35")]
for x in B + C + D: ev(x)

def lst(items, start=1):
    return "".join(f"<li>{x} = <span class='line' style='min-width:70px'></span></li>" for x in items)

sheet = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Integers and order of operations: rules and practice | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>@page{{@bottom-left{{content:"Léim · leim.ie · Free to print for home or class · JC Maths LOs (2018 spec): {LO}"}}}}
.tight{{font-size:10.8pt;line-height:1.5}}.tight td{{padding:3px 6px}}.tight h2{{margin:14px 0 6px;font-size:14pt}}.tight .note,.tight .tip{{padding:6px 10px;margin:6px 0}}
ol.q li{{margin:7px 0}}.cols{{columns:2;column-gap:12mm}}.cols li{{break-inside:avoid}}
.ex{{border:1.5px solid var(--night);border-radius:10px;padding:6px 12px;margin:6px 0}}
.ans td{{padding:3px 6px;font-size:9.6pt}}
</style></head><body>
<div class="page tight">
  <div class="band"><div><div class="k">Junior Cycle Maths · Free revision sheet</div><h1>Integers &amp; the order of operations</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2018 specification): {LO}. Play the game: <b>leim.ie/integer-rush.html</b></p>
  <h2>1. Spot the pattern</h2>
  <p>3 × (−2) = −6 · 2 × (−2) = −4 · 1 × (−2) = −2 · 0 × (−2) = 0 · −1 × (−2) = <b>?</b></p>
  <div class="note">Each answer goes up by 2, so the next one is <b>+2</b>. That's why a negative × a negative is <b>positive</b>.</div>
  <div class="two">
   <div><h2>2. The number line</h2>
    <p>Integers (ℤ) are … −3, −2, −1, 0, 1, 2, 3 … Numbers get <b>bigger to the right</b>, so −2 &gt; −8 (−2 °C is warmer than −8 °C).</p>
    <h2>3. Adding and subtracting</h2>
    <table><tbody>
     <tr><td>Add a positive → hop right</td><td>−5 + 8 = 3</td></tr>
     <tr><td>Subtract a positive → hop left</td><td>2 − 7 = −5</td></tr>
     <tr><td><b>− −</b> side by side → <b>+</b></td><td>4 − (−3) = 4 + 3 = 7</td></tr>
     <tr><td><b>+ −</b> side by side → <b>−</b></td><td>6 + (−9) = 6 − 9 = −3</td></tr>
     <tr><td>Both negative: add, keep the −</td><td>−4 − 6 = −10</td></tr>
    </tbody></table></div>
   <div><h2>4. Multiplying and dividing</h2>
    <table><thead><tr><th>Signs</th><th>Answer</th></tr></thead><tbody>
     <tr><td>Same (+ +, or − −)</td><td><b>positive</b>: (−6) × (−3) = 18</td></tr>
     <tr><td>Different (+ −)</td><td><b>negative</b>: 20 ÷ (−4) = −5</td></tr>
    </tbody></table>
    <p>Lots of numbers? Count the minus signs: even → +, odd → −. (−2) × (−3) × (−1) = −6.</p>
    <p>Squares: (−4)² = (−4) × (−4) = <b>16</b>.</p>
    <div class="note"><b>Watch out:</b> these rules are for × and ÷. (−3) + (−5) = <b>−8</b>, not 8.</div></div>
  </div>
  <h2>5. BIMDAS: the order of operations</h2>
  <table><tbody>
   <tr><td><b>B</b>rackets</td><td>(2 + 3) × 4 = 5 × 4 = 20</td><td><b>I</b>ndices</td><td>2 × 3² = 2 × 9 = 18</td></tr>
   <tr><td><b>M D</b> × ÷ left to right</td><td>12 ÷ 3 × 2 = 4 × 2 = 8</td><td><b>A S</b> + − left to right</td><td>10 − 4 + 3 = 9</td></tr>
  </tbody></table>
  <p>2 + 3 × 4 = 2 + 12 = <b>14</b> (not 20). <b>Laws:</b> commutative (7 + 2 = 2 + 7, 4 × 5 = 5 × 4) · associative ((2 × 5) × 9 = 2 × (5 × 9)) · distributive (3 × (40 + 2) = 3 × 40 + 3 × 2 = 126).</p>
  <div class="tip"><b>Exam tip:</b> integers are inside almost every question on the paper. Show every step (examiners give part marks for correct work), put negatives in brackets when you substitute ((−3)² = 9), and check your answer makes sense.</div>
</div>

<div class="page">
  <div class="band"><div><div class="k">Practice · 34 questions</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. The number line</h2><ol class="q">{"".join(f"<li>{q} <span class='line'></span></li>" for q,a in A)}</ol>
  <div class="two"><div><h2>B. Add and subtract</h2><ol class="q" start="7">{lst(B)}</ol></div>
  <div><h2>C. Multiply and divide</h2><ol class="q" start="15">{lst(C)}</ol></div></div>
  <h2>D. BIMDAS (show each step)</h2><ol class="q cols" start="23">{lst(D)}</ol>
  <p class="small" style="margin-top:6px">Questions 31–34 are on the next page.</p>
</div>

<div class="page">
  <div class="band"><div><div class="k">Exam-style · then check</div><h1>Exam corner + answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>E. Exam-style questions (show your work)</h2>
  <ol class="q" start="31">{"".join(f"<li>{q}<span class='long'></span><span class='long'></span></li>" for q,a in E)}</ol>
  <h2 style="margin-top:12px">Answers</h2>
  <table class="ans"><tbody>
   <tr><td><b>A</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(A,1))}</td></tr>
   <tr><td><b>B</b></td><td>{" · ".join(f"{i}. {f(ev(x))}" for i,x in enumerate(B,7))}</td></tr>
   <tr><td><b>C</b></td><td>{" · ".join(f"{i}. {f(ev(x))}" for i,x in enumerate(C,15))}</td></tr>
   <tr><td><b>D</b></td><td>23. 3 + 10 = 13 · 24. 8 × 2 = 16 · 25. 20 − 3 = 17 · 26. 4 × 9 = 36 · 27. 3 × 3 = 9 · 28. 10 − 5 = 5 · 29. 6 + (−12) = −6 · 30. 4 + (−12) = −8</td></tr>
   <tr><td><b>E</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(E,31))}</td></tr>
  </tbody></table>
  <div class="note"><b>Got one wrong?</b> Find the slip: a sign (− − is +), the order (× before +), or a square ((−6)² = 36). Then play <b>Integer Rush</b> at leim.ie/integer-rush.html: the "Go back over these" list at the end shows the rule for each mistake.</div>
  <p class="small">All questions written by Léim. Léim is independent and not connected with the State Examinations Commission or the NCCA.</p>
</div>
</body></html>"""
assert [ev(x) for x in D] == [13, 16, 17, 36, 9, 5, -6, -8]

# ---------- teacher pack ----------
random.seed(1)
# Find Your Match: 12 pairs, same value, distinct values
PAIRS = [("(−3) × 4", "−20 + 8"), ("−15 ÷ (−3)", "2 − (−3)"), ("(−2)³", "−4 − 4"), ("7 − 10", "(−12) ÷ 4"),
         ("(−5)²", "5 × 5"), ("−6 + 3 × 2", "4 × 0"), ("2 + 3 × 4", "(−7) × (−2)"), ("(−1) × (−9)", "18 ÷ 2"),
         ("−10 − 6", "(−4)² × (−1)"), ("(3 + 5) ÷ (−4) + 4", "−6 − (−8)"), ("1 − 8", "(−21) ÷ 3"), ("(−6) × (−6) ÷ 2", "3 × 2² + 6")]
def ev2(x): return ev(x.replace("³", "**3").replace(")**3", ")**3"))
def evp(x):
    e = x.replace(M, "-").replace("×", "*").replace("÷", "/").replace("³", "**3")
    e = re.sub(r"(\([^()]*\)|\d+)²", r"(\1)**2", e); return eval(e)
vals = []
for a, b in PAIRS:
    va, vb = evp(a), evp(b); assert va == vb, (a, b, va, vb); vals.append(int(va))
# fix duplicates: "(3 + 5) × (−2)" = −16 duplicates "−10 − 6" = −16
assert len(set(vals)) == len(vals), sorted(vals)
cards = [(a, i) for i, (a, b) in enumerate(PAIRS)] + [(b, i) for i, (a, b) in enumerate(PAIRS)]
random.shuffle(cards)
card_html = "".join(f'<div class="c"><span class="tag">{"ABCDEFGHIJKLMNOPQRSTUVWX"[k]}</span><b>{c}</b></div>' for k, (c, i) in enumerate(cards))
order = sorted(range(12), key=lambda i: vals[i])
match_key = " · ".join(f"{PAIRS[i][0]} = {PAIRS[i][1]} = <b>{f(vals[i])}</b>" for i in order)

# Dominoes: 20 expressions with distinct integer answers, chained
DOMS = ["−7 + 3", "5 − 12", "(−6) × 3", "(−24) ÷ (−4)", "−2 − (−9)", "4 + 2 × 5", "(4 + 2) × 5", "−8 + (−5)",
        "(−3)²", "20 − 6 ÷ 2", "(−2) × (−2) × (−2)", "−1 − 1", "10 − (3 − 8)", "−30 ÷ 6", "2 × 3² + 1",
        "−9 + 10", "(−5) × (−4)", "12 ÷ (−3) × 4", "0 − 11", "3 − 4 × 3"]
dv = [evp(x) for x in DOMS]
assert all(v == int(v) for v in dv); dv = [int(v) for v in dv]
dupes = {v for v in dv if dv.count(v) > 1}
assert not dupes, (dupes, [x for x, v in zip(DOMS, dv) if v in dupes])
random.seed(20)
chain = DOMS[:]; random.shuffle(chain)
dom = []  # domino k: left = answer of chain[k-1] (or START), right = chain[k]
for k, x in enumerate(chain):
    left = "START" if k == 0 else f(int(evp(chain[k - 1])))
    dom.append((left, x))
dom.append((f(int(evp(chain[-1]))), "FINISH"))
dom_print = dom[:]; random.shuffle(dom_print)
dom_html = "".join(f'<div class="dom"><div class="h l">{l}</div><div class="h r">{r}</div></div>' for l, r in dom_print)
chain_key = "".join(f"<li>{x} = <b>{f(int(evp(x)))}</b></li>" for x in chain)

# Error hunt: worked solutions with one mistake
ERR = [("−8 + 3 × 2", "= −5 × 2 = −10", "× first: −8 + 6 = <b>−2</b>"),
       ("(−4)²", "= −16", "same signs: (−4) × (−4) = <b>16</b>"),
       ("6 − (−2)", "= 6 − 2 = 4", "− − makes +: 6 + 2 = <b>8</b>"),
       ("(−3) + (−7)", "= 10 (two negatives make a positive)", "that rule is for × and ÷ only: <b>−10</b>"),
       ("24 ÷ 4 × 2", "= 24 ÷ 8 = 3", "÷ and × left to right: 6 × 2 = <b>12</b>"),
       ("5 × (−3) − (−4)", "= −15 − 4 = −19", "− (−4) is + 4: −15 + 4 = <b>−11</b>")]
for q, w, r in ERR: pass
assert [int(evp(q)) for q, w, r in ERR] == [-2, 16, 8, -10, 12, -11]

pack = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Integers & Order of Operations Teacher Pack | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>
@page{{@bottom-left{{content:"Léim · leim.ie · Single-teacher licence · JC Maths LOs (2018 spec): {LO}";font-size:7pt}}}}
.proc td{{font-size:8.9pt;padding:3px 6px;line-height:1.32}}.proc td:first-child{{white-space:nowrap;font-weight:700;color:var(--green)}}
.p1 .note{{font-size:8.7pt;padding:6px 10px;line-height:1.35}}.p1 p{{font-size:9.5pt}}
.fym{{display:grid;grid-template-columns:repeat(4,1fr)}}
.fym .c{{border:2px dashed #9AA3AE;margin:-1px 0 0 -1px;height:37mm;display:flex;align-items:center;justify-content:center;position:relative;text-align:center;padding:4mm}}
.fym .c b{{font-size:17pt;font-weight:800}}.fym .tag{{position:absolute;top:2mm;left:3mm;font-size:7.5pt;color:var(--muted);font-weight:700}}
.doms{{display:grid;grid-template-columns:1fr 1fr;gap:2mm 6mm}}
.dom{{display:grid;grid-template-columns:1fr 1.5fr;border:2px dashed #9AA3AE;height:18.5mm}}
.dom .h{{display:flex;align-items:center;justify-content:center;text-align:center;padding:2mm;font-size:15pt;font-weight:800}}
.dom .l{{background:var(--mist);border-right:2px solid var(--ink)}}
.poster{{height:255mm;border:6px solid var(--night);border-radius:18px;padding:11mm;display:flex;flex-direction:column;justify-content:space-between}}
.poster h1{{font-size:34pt;text-align:center}}
.sg{{display:grid;grid-template-columns:1fr 1fr;gap:4mm}}.sg div{{border-radius:14px;padding:4mm;text-align:center;font-size:12.5pt;line-height:1.35}}.sg b{{display:block;font-size:24pt;font-weight:800}}
.bim{{display:grid;grid-template-columns:repeat(4,1fr);gap:3mm}}.bim div{{border-radius:12px;padding:4mm 2mm;text-align:center;font-size:11pt;line-height:1.3;background:var(--night);color:#fff}}.bim b{{display:block;font-size:26pt;color:#F6CF5A}}
.ws{{font-size:10pt;line-height:1.42}}.ws ol.q li{{margin:6px 0}}.ws .long{{height:22px}}
.eh td{{padding:5px 8px;font-size:10pt}}.eh td:first-child{{font-weight:700;width:30%}}.eh .gap{{display:block;border-bottom:1px solid #9AA3AE;height:16px}}
</style></head><body>

<div class="page p1">
  <div class="band"><div><div class="k">Junior Cycle Maths · Teacher pack</div><h1>Integers &amp; the order of operations</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2018 specification): {LO}</p>
  <div class="two">
    <div><h3>Aims</h3><p>By the end of the lesson students can order integers on the number line, add, subtract, multiply and divide with negative numbers, explain why a negative × a negative is positive, and use BIMDAS (including indices and negatives in brackets) to evaluate expressions and spot errors in worked solutions.</p></div>
    <div><h3>In this pack</h3><p>p.1 Teacher notes · p.2 Find Your Match / Human Number Line cards · p.3 Integer Dominoes (cut-up) · p.4 Wall poster · p.5 Worksheet: Error Hunt + exam-style questions · p.6 Answers. Level: 1st year (Higher and Ordinary), or 3rd-year revision. Time: about 60 minutes. All questions are original.</p></div>
  </div>
  <h2 style="margin-top:8px">Procedure</h2>
  <table class="proc"><tbody>
    <tr><td>5 min</td><td><b>Lead-in: Warmer or colder?</b> Board: <i>Dublin 4 °C · Mullingar −3 °C · Cavan −7 °C · Cork 6 °C</i>. Pairs put the towns in order coldest first and say how many degrees warmer Cork is than Cavan (13). Draw the vertical thermometer as a number line.</td></tr>
    <tr><td>8 min</td><td><b>Guided discovery.</b> Write the pattern 3 × (−2) = −6, 2 × (−2) = −4 … 0 × (−2) = 0. Pairs continue it to −1 × (−2) and −2 × (−2) and state the rule in their own words. Same idea for subtraction: 5 − 2, 5 − 1, 5 − 0, 5 − (−1)… Check with the poster (p.4).</td></tr>
    <tr><td>12 min</td><td><b>Find Your Match → Human Number Line</b> (p.2). Give each student one card (24 cards = 12 pairs; for smaller classes remove pairs). Students work out their card in their head, then mingle to find the partner whose card has the same value. Pairs then line up across the room in order of value, smallest at the left. The class checks the line, pair by pair, reading out both cards.</td></tr>
    <tr><td>12 min</td><td><b>Integer Dominoes</b> (p.3), groups of 3–4. Each domino has an answer on the left and a new calculation on the right. Start with START, find the domino whose left side answers the calculation, and build the chain to FINISH. Answer chain below.</td></tr>
    <tr><td>15 min</td><td><b>Worksheet</b> (p.5). Error Hunt in pairs (find the mistake, name the rule, fix it), then the exam-style questions alone. Feedback: which slip was the most common?</td></tr>
    <tr><td>5 min</td><td><b>Exit ticket.</b> On a mini-whiteboard: (−3)² − 2 × (−5) (answer 19). Homework: play <b>Integer Rush</b> at leim.ie/integer-rush.html (Order of operations mode) and copy three lines from the "Go back over these" list.</td></tr>
  </tbody></table>
  <div class="note"><b>Find Your Match key</b> (smallest first, the order of the human number line): {match_key}.<br>
  <b>Errors to look for:</b> applying "two negatives make a positive" to addition ((−3) + (−7) = 10) · working left to right instead of BIMDAS (2 + 3 × 4 = 20) · (−4)² = −16 · 6 − (−2) = 4 · 24 ÷ 4 × 2 = 3 (× before ÷ instead of left to right) · thinking −8 is bigger than −2. <b>Calculators:</b> use the (−) key and type the brackets; a calculator gives −4² = −16 because it squares first. <b>Support:</b> keep a number line −20 to 20 on the desk. <b>Fast finishers:</b> using −2, 3, −4 and 5 once each with any operations and brackets, make as many integers from −10 to 10 as you can.</div>
  <p class="small"><b>Domino answer chain</b> (START → FINISH):</p>
  <ol class="small" style="columns:3;column-gap:12px;font-size:7.8pt;line-height:1.35;margin:0;padding-left:16px">{chain_key}</ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">Whole class · cut along the dashed lines</div><h1>Find Your Match / Human Number Line</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.5pt">Work out your card in your head. Find the person whose card has the <b>same value</b>. Then, as a pair, take your place in the human number line: smallest on the left, biggest on the right.</p>
  <div class="fym">{card_html}</div>
</div>

<div class="page">
  <div class="band"><div><div class="k">Groups of 3–4 · cut along the dashed lines</div><h1>Integer Dominoes</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.5pt">Start with START. Work out the calculation on the right, then find the domino with that answer on its left. Keep going until you reach FINISH. No calculators!</p>
  <div class="doms">{dom_html}</div>
</div>

<div class="page">
  <div class="poster">
    <h1>Integer rules</h1>
    <div class="sg">
      <div style="background:var(--green-soft)"><b>+ × + = +</b>6 × 3 = 18</div>
      <div style="background:var(--green-soft)"><b>− × − = +</b>(−6) × (−3) = 18</div>
      <div style="background:#FBE9E8"><b>+ × − = −</b>6 × (−3) = −18</div>
      <div style="background:#FBE9E8"><b>− × + = −</b>(−6) × 3 = −18</div>
    </div>
    <p style="text-align:center;font-size:13pt">The same rules work for <b>÷</b>: (−20) ÷ (−4) = 5 · 20 ÷ (−4) = −5</p>
    <div class="sg">
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>− (−) = +</b>4 − (−3) = 4 + 3 = 7</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>+ (−) = −</b>6 + (−9) = 6 − 9 = −3</div>
    </div>
    <div class="bim">
      <div><b>B</b>Brackets</div><div><b>I</b>Indices</div><div><b>M D</b>× ÷<br>left to right</div><div><b>A S</b>+ −<br>left to right</div>
    </div>
    <p style="text-align:center;font-size:14pt;font-weight:700">2 + 3 × 4 = 2 + 12 = 14 &nbsp;·&nbsp; (−4)² = 16 &nbsp;·&nbsp; −8 &lt; −2</p>
    <p style="text-align:center;font-size:10pt;color:var(--muted)">Léim · leim.ie · Play Integer Rush: leim.ie/integer-rush.html</p>
  </div>
</div>

<div class="page ws">
  <div class="band"><div><div class="k">Worksheet</div><h1>Error Hunt + exam-style questions</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Error Hunt</h2>
  <p>Each answer has one mistake. Find it, say which rule was broken, and write the right answer.</p>
  <table class="eh"><thead><tr><th>Calculation</th><th>Student's answer</th><th>The mistake and the right answer</th></tr></thead><tbody>
  {"".join(f"<tr><td>{q}</td><td>{w}</td><td><span class='gap'></span><span class='gap'></span></td></tr>" for q,w,r in ERR)}
  </tbody></table>
  <h2>B. Exam-style questions (show all your work)</h2>
  <ol class="q">
    <li>The table shows the lowest temperature one night in four towns: <b>Birr −4 °C · Athlone −9 °C · Galway 2 °C · Carlow −1 °C</b>.<br>(a) Which town was coldest? (b) How many degrees warmer was Galway than Athlone? (c) The next night, every temperature was 3 degrees lower. What was the temperature in Carlow?<span class="long"></span><span class="long"></span></li>
    <li>Niamh's bank balance is −€28. She is paid €75 and then spends €19. What is her balance now?<span class="long"></span></li>
    <li>Evaluate 5a − b² when a = −2 and b = −3.<span class="long"></span><span class="long"></span></li>
    <li>Insert one pair of brackets to make each statement true: (a) 12 − 4 × 2 + 1 = 17 &nbsp; (b) 12 − 4 × 2 + 1 = 0<span class="long"></span></li>
    <li>Use the distributive law to work out 8 × 99 without a calculator. Show your method.<span class="long"></span></li>
  </ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">For the teacher</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Error Hunt</h2>
  <table><tbody>{"".join(f"<tr><td style='width:30%'><b>{q}</b></td><td>{r}</td></tr>" for q,w,r in ERR)}</tbody></table>
  <h2>B. Exam-style questions</h2>
  <ol class="q">
    <li>(a) Athlone (−9 °C is the smallest). (b) 2 − (−9) = <b>11 degrees</b>. (c) −1 − 3 = <b>−4 °C</b>.</li>
    <li>−28 + 75 − 19 = <b>€28</b>.</li>
    <li>5(−2) − (−3)² = −10 − 9 = <b>−19</b>. (Watch: (−3)² = 9, then subtract it.)</li>
    <li>(a) <b>(12 − 4) × 2 + 1 = 17</b> (8 × 2 + 1) &nbsp; (b) <b>12 − 4 × (2 + 1) = 0</b> (12 − 4 × 3 = 12 − 12). Without brackets the answer is 5.</li>
    <li>8 × 99 = 8 × (100 − 1) = 800 − 8 = <b>792</b>.</li>
  </ol>
  <h2>Marking tip</h2>
  <p>Give credit for each correct step, as the exam does: a correct method with one sign slip should still earn most of the marks. Ask students to circle the step where their answer went wrong before they correct it.</p>
</div>
</body></html>"""

cover = """<!doctype html><html><head><meta charset="utf-8"><style>
body{margin:0;width:1200px;height:1200px;background:#1B2430;font-family:Inter,sans-serif;color:#fff;display:flex;flex-direction:column;justify-content:space-between;padding:90px;box-sizing:border-box}
.k{display:inline-block;background:#2E7D57;border-radius:99px;padding:12px 26px;font-weight:700;font-size:28px;letter-spacing:.06em;text-transform:uppercase}
h1{font-size:98px;font-weight:800;line-height:1;letter-spacing:-.03em;margin:40px 0 0}
h1 span{background:#F6CF5A;color:#1B2430;padding:0 14px}
.sub{font-size:38px;color:#C9D1DA;margin-top:36px;line-height:1.35}
.em{font-size:56px;margin-top:30px;font-weight:800;letter-spacing:.01em;color:#F6CF5A}
.foot{display:flex;justify-content:space-between;align-items:center;font-size:34px;font-weight:700}
.price{background:#F6CF5A;color:#1B2430;border-radius:16px;padding:14px 28px}
</style></head><body>
<div><span class="k">Junior Cycle Maths · Teacher pack</span>
<h1><span>Integers</span> &amp; the order of operations</h1>
<div class="sub">Find Your Match + Human Number Line<br>Integer Dominoes · Poster · Worksheet + answers</div>
<div class="em">(−3) × (−4) = 12 · 2 + 3 × 4 = 14</div></div>
<div class="foot"><span>↗ Léim · leim.ie</span><span class="price">Ready to teach · 60 min</span></div>
</body></html>"""

if __name__ == "__main__":
    for name, txt in [("rules-and-practice", sheet), ("teacher-pack", pack), ("cover", cover)]:
        open(os.path.join(SRC, f"integers-order-of-operations-{name}.html"), "w", encoding="utf-8").write(txt)
    def pdf(name, out):
        subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--no-pdf-header-footer", f"--print-to-pdf={out}",
                        f"integers-order-of-operations-{name}.html"], cwd=SRC, check=True, capture_output=True)
        d = open(out, "rb").read(); print(name, len(re.findall(rb"/Type\s*/Page[^s]", d)), "pages")
    pdf("rules-and-practice", os.path.join(ROOT, "printables", "integers-order-of-operations-rules-and-practice.pdf"))
    pdf("teacher-pack", os.path.join(OUT, "Integers-and-Order-of-Operations-Teacher-Pack-Leim.pdf"))
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--hide-scrollbars", "--window-size=1200,1200",
                    f"--screenshot={os.path.join(OUT, 'integers-order-of-operations-cover.png')}", "integers-order-of-operations-cover.html"],
                   cwd=SRC, check=True, capture_output=True)
    print("domino chain:", [ (x, int(evp(x))) for x in chain])
