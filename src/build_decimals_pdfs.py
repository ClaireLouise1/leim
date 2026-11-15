#!/usr/bin/env python3
"""Decimals, rounding & estimation (JC Maths topic 4): free sheet + teacher pack + Payhip cover.
Run from the repo root: python3 src/build_decimals_pdfs.py OUTDIR
Writes src/decimals-rounding-estimation-*.html; PDFs/cover PNG go to OUTDIR (free sheet also to printables/).
Every answer is computed with Python's Decimal and asserted."""
import os, sys, random, subprocess, re
from decimal import Decimal as D, ROUND_HALF_UP as H
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC)
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/decimals"; os.makedirs(OUT, exist_ok=True)
SLUG = "decimals-rounding-estimation"
LO = "N.1e, N.2a"

def dp(x, d): x = D(x); return x.quantize(D(1).scaleb(-d), H) if d >= 0 else (x / D(10) ** -d).quantize(D(1), H) * D(10) ** -d
def sf(x, s): x = D(x); return dp(x, s - 1 - x.adjusted())
def c(expr):
    a, op, b = re.fullmatch(r"([\d.]+) ([+−×÷]) ([\d.]+)", expr).groups(); a, b = D(a), D(b)
    return {"+": a + b, "−": a - b, "×": a * b, "÷": a / b}[op]
def t(x):
    """tidy: no trailing zeros, no exponent"""
    s = format(D(x).normalize(), "f"); return s
def plain(x): return format(D(x), "f")

# ---------- free sheet ----------
A = [("What is the value of the 6 in 15.068?", "0.06"),
     ("Put in order, smallest first: 0.6, 0.06, 0.66, 0.606", ", ".join(sorted(["0.6", "0.06", "0.66", "0.606"], key=D))),
     ("4.7 × 100 =", t(D("4.7") * 100)), ("52 ÷ 1000 =", t(D(52) / 1000)),
     ("Write 3/8 as a decimal.", t(D(3) / 8)), ("Write 0.45 as a fraction in its simplest form.", "9/20")]
assert [a for q, a in A] == ["0.06", "0.06, 0.6, 0.606, 0.66", "470", "0.052", "0.375", "9/20"] and D("0.45") == D(9) / 20
B = [("7.4682 to 1 decimal place", plain(dp("7.4682", 1))), ("7.4682 to 2 decimal places", plain(dp("7.4682", 2))),
     ("38516 to the nearest hundred", plain(dp("38516", -2))), ("38516 to the nearest thousand", plain(dp("38516", -3))),
     ("0.03072 to 2 significant figures", plain(sf("0.03072", 2))), ("6047 to 2 significant figures", plain(sf("6047", 2))),
     ("19.996 to 2 decimal places", plain(dp("19.996", 2))), ("12.95 to the nearest whole number", plain(dp("12.95", 0)))]
assert [a for q, a in B] == ["7.5", "7.47", "38500", "39000", "0.031", "6000", "20.00", "13"], [a for q, a in B]
Cq = ["14.6 + 3.85", "9 − 4.27", "23.4 − 8.76", "0.7 × 0.6", "2.35 × 4", "1.2 × 0.03", "6.3 ÷ 0.7", "4.5 ÷ 0.09"]
assert [t(c(x)) for x in Cq] == ["18.45", "4.73", "14.64", "0.42", "9.4", "0.036", "9", "50"], [t(c(x)) for x in Cq]
Dq = [("6.8 × 3.12", "7 × 3 = 21"), ("48.7 × 0.21", "50 × 0.2 = 10"), ("812 ÷ 39.6", "800 ÷ 40 = 20"), ("0.58 × 0.92", "0.6 × 0.9 = 0.54"),
      ("41.3 ÷ 0.48", "40 ÷ 0.5 = 80"), ("€2.95 × 19", "€3 × 20 = €60")]
def est(x):
    a, op, b = re.fullmatch(r"€?([\d.]+) ([×÷]) ([\d.]+)", x).groups(); a, b = sf(a, 1), sf(b, 1)
    return a * b if op == "×" else a / b
for x, a in Dq: assert D(a.split("= ")[1].replace("€", "")) == est(x), (x, est(x))
reas = c("3.9 × 52.1"); assert reas == D("203.19")
paint = dp(D("38.2") / D("11.5"), 1); assert paint == D("3.3")
bill = D("12.50") + (163 - 100) * D("0.09"); assert bill == D("18.17")
mean = dp(sum(map(D, ["4.27", "3.86", "5.12", "4.9"])) / 4, 2); assert mean == D("4.54") and sum(map(D, ["4.27", "3.86", "5.12", "4.9"])) == D("18.15")
apples = D("3.8") * D("2.15"); assert apples == D("8.17") and sf("3.8", 1) * sf("2.15", 1) == 8
E = [("A litre of paint covers 11.5 m². A wall has an area of 38.2 m². (a) How many litres are needed, correct to 1 decimal place? (b) Paint is sold in 1-litre tins. How many tins must be bought?",
      f"(a) 38.2 ÷ 11.5 = 3.32… = <b>{paint} litres</b> (b) <b>4 tins</b> (3 isn't enough)"),
     ("Aoife's phone plan costs €12.50 a month plus 9c for every text after the first 100. In May she sends 163 texts. How much is her bill?",
      f"63 × €0.09 = €5.67, so €12.50 + €5.67 = <b>€{bill}</b>"),
     ("Jack's long-jump results (in metres) are 4.27, 3.86, 5.12 and 4.9. Find the mean, correct to 2 decimal places.",
      f"18.15 ÷ 4 = 4.5375 = <b>{mean} m</b>"),
     ("Apples cost €2.15 per kg. (a) Estimate the cost of 3.8 kg. (b) Work out the exact cost. Is it reasonable?",
      f"(a) 4 × €2 = <b>€8</b> (b) <b>€{apples}</b>, close to €8, so yes")]

def qs(items): return "".join(f"<li>{q} <span class='line'></span></li>" for q, a in items)

sheet = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Decimals, rounding and estimation: rules and practice | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>@page{{@bottom-left{{content:"Léim · leim.ie · Free to print for home or class · JC Maths LOs (2018 spec): {LO}"}}}}
.tight{{font-size:10.2pt;line-height:1.44}}.tight td,.tight th{{padding:3px 6px}}.tight h2{{margin:10px 0 5px;font-size:14pt}}.tight .note,.tight .tip{{padding:6px 10px;margin:6px 0}}
ol.q li{{margin:7px 0}}.cols{{columns:2;column-gap:12mm}}.cols li{{break-inside:avoid}}
.ans td{{padding:3px 6px;font-size:9.4pt}}.pv td,.pv th{{text-align:center}}
</style></head><body>
<div class="page tight">
  <div class="band"><div><div class="k">Junior Cycle Maths · Free revision sheet</div><h1>Decimals, rounding &amp; estimation</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2018 specification): {LO}. Play the game: <b>leim.ie/round-it.html</b></p>
  <div class="two">
   <div><h2>1. Place value</h2>
    <table class="pv"><thead><tr><th>Tens</th><th>Units</th><th>.</th><th>Tenths</th><th>Hundredths</th><th>Thousandths</th></tr></thead><tbody><tr><td>2</td><td>5</td><td>.</td><td>4</td><td>7</td><td>3</td></tr></tbody></table>
    <p>In 25.473 the 7 is worth <b>0.07</b>. To compare decimals, give them the same number of places: 0.5 = 0.50 &gt; 0.45.</p>
    <h2>2. × and ÷ by 10, 100, 1000</h2>
    <p>The digits move one place for every zero: <b>left</b> for × (bigger), <b>right</b> for ÷ (smaller). 3.47 × 100 = <b>347</b>; 3.47 ÷ 100 = <b>0.0347</b>.</p>
    <h2>3. Fractions ↔ decimals</h2>
    <p>1/2 = 0.5 · 1/4 = 0.25 · 3/4 = 0.75 · 1/5 = 0.2 · 1/8 = 0.125 · 1/10 = 0.1. Decimal → fraction: 0.35 = 35/100 = <b>7/20</b>.</p>
    <h2>4. Decimal sums</h2>
    <p><b>+ −</b> line up the points (7 − 2.35 → 7.00 − 2.35 = 4.65). <b>×</b> multiply without the points, then count the places: 0.3 × 0.4 = <b>0.12</b>. <b>÷</b> make the divisor whole: 4.8 ÷ 0.6 = 48 ÷ 6 = <b>8</b>.</p></div>
   <div><h2>5. Rounding</h2>
    <p>Find the last digit you keep. Look at the <b>next</b> digit: <b>5 or more</b> round up, <b>less than 5</b> leave it. Fill whole-number gaps with zeros.</p>
    <table><thead><tr><th>6.2849 to…</th><th></th></tr></thead><tbody>
     <tr><td>nearest whole number</td><td><b>6</b></td></tr><tr><td>1 decimal place</td><td><b>6.3</b></td></tr>
     <tr><td>2 decimal places</td><td><b>6.28</b></td></tr><tr><td>3 significant figures</td><td><b>6.28</b></td></tr></tbody></table>
    <p><b>Significant figures:</b> count from the first digit that isn't zero. 0.004637 to 2 s.f. = <b>0.0046</b>; 48372 to 2 s.f. = <b>48000</b>.</p>
    <h2>6. Estimate first</h2>
    <p>Round every number to <b>1 significant figure</b>: 4.87 × 21.3 ≈ 5 × 20 = <b>100</b>. If your answer is about 10 times too big or small, check the decimal point.</p>
    <div class="note"><b>Round at the end, not the middle:</b> 4.56 × 2.34 = 10.6704 → <b>10.7</b>. Rounding first (4.6 × 2.3 = 10.58) gives 10.6: wrong.</div></div>
  </div>
  <div class="tip"><b>Exam tip:</b> read the instruction twice. Decimal places and significant figures are different (0.04637: 2 d.p. = 0.05, 2 s.f. = 0.046). Money always has 2 decimal places: €9.80, not €9.8. When the question says "estimate", write the rounded sum down.</div>
</div>

<div class="page">
  <div class="band"><div><div class="k">Practice · 34 questions</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <div class="two"><div><h2>A. Place value</h2><ol class="q">{qs(A)}</ol></div>
  <div><h2>B. Rounding</h2><ol class="q" start="7">{qs(B)}</ol></div></div>
  <h2>C. Decimal sums (no calculator)</h2><ol class="q cols" start="15">{"".join(f"<li>{x} = <span class='line' style='min-width:80px'></span></li>" for x in Cq)}</ol>
  <h2>D. Estimate by rounding each number to 1 significant figure</h2><ol class="q cols" start="23">{"".join(f"<li>{x} ≈ <span class='line' style='min-width:80px'></span></li>" for x, a in Dq)}
   <li>Which is the right answer to 3.9 × 52.1? 2.0319 · 20.319 · 203.19 · 2031.9 <span class='line' style='min-width:60px'></span></li>
   <li>Estimate 7.8 × 7.8 <span class='line' style='min-width:80px'></span></li></ol>
  <p class="small" style="margin-top:6px">Questions 31–34 are on the next page.</p>
</div>

<div class="page">
  <div class="band"><div><div class="k">Exam-style · then check</div><h1>Exam corner + answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>E. Exam-style questions (show your work)</h2>
  <ol class="q" start="31">{"".join(f"<li>{q}<span class='long'></span><span class='long'></span></li>" for q,a in E)}</ol>
  <h2 style="margin-top:12px">Answers</h2>
  <table class="ans"><tbody>
   <tr><td><b>A</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(A,1))}</td></tr>
   <tr><td><b>B</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(B,7))}</td></tr>
   <tr><td><b>C</b></td><td>{" · ".join(f"{i}. {t(c(x))}" for i,x in enumerate(Cq,15))}</td></tr>
   <tr><td><b>D</b></td><td>{" · ".join(f"{i}. {a}" for i,(x,a) in enumerate(Dq,23))} · 29. {reas} (estimate 4 × 50 = 200) · 30. 8 × 8 = 64</td></tr>
   <tr><td><b>E</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(E,31))}</td></tr>
  </tbody></table>
  <div class="note"><b>Got one wrong?</b> Check: did you look at the <b>next</b> digit when rounding? Did you keep zeros as place holders (38500, not 385)? Did you count the decimal places when multiplying? Did you round too early? Then play <b>Round It</b> at leim.ie/round-it.html: the "Go back over these" list at the end shows the rule for each mistake.</div>
  <p class="small">All questions written by Léim. Léim is independent and not connected with the State Examinations Commission or the NCCA.</p>
</div>
</body></html>"""
assert sf("3.9", 1) * sf("52.1", 1) == 200 and sf("7.8", 1) ** 2 == 64

# ---------- teacher pack ----------
HNL = ["0.5", "0.45", "0.405", "0.54", "0.05", "0.9", "0.09", "0.099", "0.19", "0.3", "0.33", "0.303", "0.7", "0.07", "0.77", "0.707"]
assert len(set(map(D, HNL))) == 16
hnl_sorted = sorted(HNL, key=D)
random.seed(4); hnl_print = HNL[:]; random.shuffle(hnl_print)
hnl_html = "".join(f'<div class="c"><span class="tag">Card {i}</span><div class="fc">{x}</div></div>' for i, x in enumerate(hnl_print, 1))

AUC = [("4.8 × 0.5 = 2.4", c("4.8 × 0.5") == D("2.4"), "Right"),
       ("0.3 × 0.3 = 0.9", c("0.3 × 0.3") == D("0.9"), "Wrong: 0.09 (2 decimal places)"),
       ("7.25 to 1 decimal place = 7.3", dp("7.25", 1) == D("7.3"), "Right (the next digit is 5: round up)"),
       ("0.0482 to 2 significant figures = 0.05", sf("0.0482", 2) == D("0.05"), "Wrong: 0.048 (that was 2 decimal places)"),
       ("36.4 ÷ 0.4 = 91", c("36.4 ÷ 0.4") == 91, "Right (364 ÷ 4)"),
       ("0.7 is bigger than 0.65", D("0.7") > D("0.65"), "Right (0.70 &gt; 0.65)"),
       ("5.1 × 19.8 = 10.098", c("5.1 × 19.8") == D("10.098"), "Wrong: estimate 5 × 20 = 100, so 100.98"),
       ("3.14 × 100 = 31.4", c("3.14 × 100") == D("31.4"), "Wrong: 314 (2 places left)"),
       ("12 − 4.56 = 7.44", c("12 − 4.56") == D("7.44"), "Right"),
       ("48250 to the nearest thousand = 48000", dp("48250", -3) == 48000, "Right (2 is less than 5)")]
for s, truth, k in AUC: assert truth == k.startswith("Right"), s
assert c("5.1 × 19.8") == D("100.98") and c("0.3 × 0.3") == D("0.09") and sf("0.0482", 2) == D("0.048")

DOMS = [("6.38 to 1 d.p.", dp("6.38", 1)), ("0.25 × 4", c("0.25 × 4")), ("2.7 + 1.45", c("2.7 + 1.45")), ("5 − 1.6", c("5 − 1.6")),
        ("0.6 × 0.3", c("0.6 × 0.3")), ("4.2 ÷ 0.7", c("4.2 ÷ 0.7")), ("1/4 as a decimal", D(1) / 4), ("0.0371 to 2 s.f.", sf("0.0371", 2)),
        ("47.3 to the nearest 10", dp("47.3", -1)), ("3.456 to 2 d.p.", dp("3.456", 2)), ("8.4 ÷ 100", c("8.4 ÷ 100")), ("0.07 × 1000", c("0.07 × 1000")),
        ("3/5 as a decimal", D(3) / 5), ("9.95 to 1 d.p.", dp("9.95", 1)), ("2.5 × 1.2", c("2.5 × 1.2")), ("12.6 − 4.9", c("12.6 − 4.9")),
        ("1.8 ÷ 0.02", c("1.8 ÷ 0.02")), ("0.5 + 0.75", c("0.5 + 0.75")), ("263 to 1 s.f.", sf("263", 1)), ("0.9 × 0.9", c("0.9 × 0.9"))]
assert len(set(v for k, v in DOMS)) == 20, sorted(v for k, v in DOMS)
def show(clue, v): return plain(v) if (" d.p." in clue or "s.f." in clue or "nearest" in clue) else t(v)
assert show("9.95 to 1 d.p.", dp("9.95", 1)) == "10.0" and show("263 to 1 s.f.", sf("263", 1)) == "300" and show("47.3 to the nearest 10", dp("47.3", -1)) == "50"
random.seed(44); chain = DOMS[:]; random.shuffle(chain)
dom = [("START" if k == 0 else show(*chain[k - 1]), x[0]) for k, x in enumerate(chain)] + [(show(*chain[-1]), "FINISH")]
dom_print = dom[:]; random.shuffle(dom_print)
dom_html = "".join(f'<div class="dom"><div class="h l">{l}</div><div class="h r">{r}</div></div>' for l, r in dom_print)
chain_key = "".join(f"<li>{x} = <b>{show(x, v)}</b></li>" for x, v in chain)

ERR = [("3.47 × 10", "= 3.470", "Added a zero. The digits move 1 place left: <b>34.7</b>"),
       ("0.4 × 0.2", "= 0.8", "2 decimal places in the question, so 2 in the answer: <b>0.08</b>"),
       ("5.38 to 1 d.p.", "= 5.3", "Looked at the wrong digit or cut it off. The 8 rounds the 3 up: <b>5.4</b>"),
       ("27 640 to the nearest thousand", "= 28", "Lost the place holders: <b>28 000</b>"),
       ("0.00563 to 2 s.f.", "= 0.01", "Counted the zeros at the front. Start at the 5: <b>0.0056</b>"),
       ("8 − 3.25", "= 5.25", "Didn't line up the points: 8.00 − 3.25 = <b>4.75</b>")]
assert c("3.47 × 10") == D("34.7") and c("0.4 × 0.2") == D("0.08") and dp("5.38", 1) == D("5.4") and dp("27640", -3) == 28000 and sf("0.00563", 2) == D("0.0056") and c("8 − 3.25") == D("4.75")
taxi = D("4.20") + D("1.35") * D("12.6"); assert taxi == D("21.21")
W2 = (D("12.4") * D("0.49")) / D("2.1"); assert dp(W2, 2) == D("2.89") and sf("12.4", 1) * sf("0.49", 1) / sf("2.1", 1) == D("2.5")
box = D("0.85") * 24; assert box == D("20.40") and D("20.40") < 21
per = D("6.75") / D("1.5"); per2 = D("10.20") / D("2.4"); assert per == D("4.5") and per2 == D("4.25")
ran = D("42.195") / D("3.5"); assert dp(ran, 1) == D("12.1")

pack = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Decimals &amp; Rounding Teacher Pack | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>
@page{{@bottom-left{{content:"Léim · leim.ie · Single-teacher licence · JC Maths LOs (2018 spec): {LO}";font-size:7pt}}}}
.proc td{{font-size:8.9pt;padding:3px 6px;line-height:1.32}}.proc td:first-child{{white-space:nowrap;font-weight:700;color:var(--green)}}
.p1 .note{{font-size:8.7pt;padding:6px 10px;line-height:1.35}}.p1 p{{font-size:9.5pt}}
.fym{{display:grid;grid-template-columns:repeat(4,1fr);margin-top:2mm}}
.fym .c{{border:2px dashed #9AA3AE;margin:-1px 0 0 -1px;height:24mm;position:relative;display:flex;align-items:center;justify-content:center}}
.fym .fc{{font-size:24pt;font-weight:800;text-align:center}}
.fym .tag{{position:absolute;top:1.5mm;left:3mm;font-size:6.8pt;color:var(--green);font-weight:800;text-transform:uppercase;letter-spacing:.04em}}
.auc td,.auc th{{padding:4px 7px;font-size:9.6pt}}.auc td:nth-child(n+3){{width:16%}}
.doms{{display:grid;grid-template-columns:1fr 1fr;gap:2mm 6mm}}
.dom{{display:grid;grid-template-columns:1fr 1.6fr;border:2px dashed #9AA3AE;height:18.5mm}}
.dom .h{{display:flex;align-items:center;justify-content:center;text-align:center;padding:2mm;font-size:15pt;font-weight:800}}
.dom .r{{font-size:12.5pt}}
.dom .l{{background:var(--mist);border-right:2px solid var(--ink)}}
.poster{{height:255mm;border:6px solid var(--night);border-radius:18px;padding:10mm;display:flex;flex-direction:column;justify-content:space-between}}
.poster h1{{font-size:44pt;text-align:center}}.poster p{{font-size:14pt!important}}
.ops{{display:grid;grid-template-columns:1fr 1fr;gap:4mm}}.ops div{{border-radius:14px;padding:7mm 4mm;text-align:center;font-size:14pt;line-height:1.5}}.ops b{{display:block;font-size:22pt;font-weight:800;margin-bottom:1mm}}
.pv2 td,.pv2 th{{text-align:center;font-size:24pt;padding:10px;font-weight:800}}.pv2 th{{font-size:10.5pt}}
.ws{{font-size:10pt;line-height:1.42}}.ws ol.q li{{margin:6px 0}}.ws .long{{height:22px}}
.eh td{{padding:5px 8px;font-size:9.8pt}}.eh td:first-child{{font-weight:700;width:26%}}.eh .gap{{display:block;border-bottom:1px solid #9AA3AE;height:16px}}
</style></head><body>

<div class="page p1">
  <div class="band"><div><div class="k">Junior Cycle Maths · Teacher pack</div><h1>Decimals &amp; rounding</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2018 specification): {LO} (rounding and estimating come back in every measurement, money and statistics question)</p>
  <div class="two">
    <div><h3>Aims</h3><p>By the end of the lesson students can read and compare decimals using place value, multiply and divide by 10, 100 and 1000, switch between fractions and decimals, add, subtract, multiply and divide decimals by hand, round to decimal places, significant figures and the nearest 10/100/1000, and estimate to check whether an answer is reasonable.</p></div>
    <div><h3>In this pack</h3><p>p.1 Teacher notes · p.2 Human Number Line cards + Estimation Auction · p.3 Rounding Dominoes (cut-up) · p.4 Wall poster · p.5 Worksheet: Error Hunt + exam-style questions · p.6 Answers. Level: 1st year (Higher and Ordinary), or 3rd-year revision. Time: about 60 minutes. All questions are original.</p></div>
  </div>
  <h2 style="margin-top:8px">Procedure</h2>
  <table class="proc"><tbody>
    <tr><td>5 min</td><td><b>Lead-in: Which is bigger?</b> Board 0.5 and 0.45. Hands up for each. Ask a student who chose 0.45 why (\"45 is bigger than 5\"). Don't correct yet.</td></tr>
    <tr><td>12 min</td><td><b>Human Number Line</b> (p.2 cards; one each). Mark 0 and 1 at opposite ends of the room. Students stand where their number belongs, with no talking for the first minute, then they may move each other and must explain. Check left to right against the key. Feedback: how did you decide 0.405 goes before 0.45? Elicit the rule: same number of places first (0.405 vs 0.450). Revisit the lead-in.</td></tr>
    <tr><td>8 min</td><td><b>Guided discovery: rounding.</b> Board 6.2849 and the four rounding instructions from the poster (p.4). Pairs try them before you show the rule. Ask: what's the difference between 2 decimal places and 2 significant figures? When do we need zeros as place holders?</td></tr>
    <tr><td>10 min</td><td><b>Estimation Auction</b> (p.2, one sheet per team of 3–4, €100 each). Teams decide which statements are right and bid (min €10) on the ones they believe. Reveal one by one: right = double your money; wrong = lose it. The winning team explains how estimating (5 × 20 = 100) caught the decimal-point slip.</td></tr>
    <tr><td>12 min</td><td><b>Rounding Dominoes</b> (p.3), groups of 3–4. Start with START, work out the clue, find the domino with that answer on its left, and build the chain to FINISH. Answer chain below.</td></tr>
    <tr><td>10 min</td><td><b>Worksheet</b> (p.5). Error Hunt in pairs (find the mistake, name the rule, fix it), then the exam-style questions alone. Feedback on question 3: why does rounding too early lose marks?</td></tr>
    <tr><td>3 min</td><td><b>Exit ticket.</b> 0.0748 to 2 s.f. and 2.4 × 0.3 (0.075; 0.72). Homework: play <b>Round It</b> at leim.ie/round-it.html (Is it reasonable? round) and copy three lines from the "Go back over these" list.</td></tr>
  </tbody></table>
  <div class="note"><b>Human Number Line key</b> (smallest → biggest): {", ".join(hnl_sorted)}.<br>
  <b>Errors to look for:</b> \"longer is bigger\" (0.405 &gt; 0.5) · \"add a zero\" for × 10 with decimals (3.470) · counting the decimal places wrongly when multiplying (0.3 × 0.3 = 0.9) · rounding by cutting off (5.38 → 5.3) · dropping place holders (28 for 28 000) · counting leading zeros as significant figures · rounding in the middle of a calculation · €9.8 instead of €9.80. <b>Support:</b> a place-value grid on the desk. <b>Fast finishers:</b> find a number that is 3.5 to 1 d.p. and 3.46 to 2 d.p. (e.g. 3.459); what are the smallest and biggest numbers that round to 4.7?</div>
  <p class="small"><b>Domino answer chain</b> (START → FINISH):</p>
  <ol class="small" style="columns:3;column-gap:12px;font-size:7.8pt;line-height:1.35;margin:0;padding-left:16px">{chain_key}</ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">Cut up the cards · one auction sheet per team</div><h1>Number Line + Auction</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.5pt;margin:0"><b>Human Number Line.</b> Cut out the cards and give one to each student. Line up from 0 to 1. (Big class? Print twice and make two lines.)</p>
  <div class="fym">{hnl_html}</div>
  <h2 style="margin-top:5mm">Estimation Auction</h2>
  <p style="font-size:9.5pt">Your team has <b>€100</b>. Bid on the statements you think are <b>right</b> (at least €10 each). Right: you win double. Wrong: you lose your bid. <b>Estimate first!</b></p>
  <table class="auc"><thead><tr><th>#</th><th>Statement</th><th>Right or wrong?</th><th>Our bid</th></tr></thead><tbody>
  {"".join(f"<tr><td>{i}</td><td><b>{s}</b></td><td></td><td>€</td></tr>" for i,(s,tr,k) in enumerate(AUC,1))}
  </tbody></table>
  <p style="font-size:9.5pt;margin-top:3mm">Money left at the end: €_______</p>
</div>

<div class="page">
  <div class="band"><div><div class="k">Groups of 3–4 · cut along the dashed lines</div><h1>Rounding Dominoes</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.5pt">Start with START. Work out the clue on the right, then find the domino with that answer on its left. Keep going until you reach FINISH. No calculators! (d.p. = decimal places, s.f. = significant figures)</p>
  <div class="doms">{dom_html}</div>
</div>

<div class="page">
  <div class="poster">
    <h1>Decimals &amp; rounding</h1>
    <table class="pv2"><thead><tr><th>Hundreds</th><th>Tens</th><th>Units</th><th>.</th><th>Tenths</th><th>Hundredths</th><th>Thousandths</th></tr></thead><tbody><tr><td>1</td><td>2</td><td>5</td><td>.</td><td>4</td><td>7</td><td>3</td></tr></tbody></table>
    <p style="text-align:center;font-size:12pt;margin:0"><b>Compare:</b> same number of places first: 0.5 = 0.50 &gt; 0.45 · <b>× 10, 100, 1000:</b> digits move left · <b>÷:</b> digits move right</p>
    <div class="ops">
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Rounding</b>Look at the NEXT digit<br>5 or more: round up<br>less than 5: leave it</div>
      <div style="background:var(--green-soft)"><b>Significant figures</b>Start at the first digit that isn't 0<br>0.004637 → 0.0046 (2 s.f.)<br>48372 → 48000 (2 s.f.)</div>
      <div style="background:var(--green-soft)"><b>× and ÷</b>0.3 × 0.4: 3 × 4 = 12, 2 places → 0.12<br>4.8 ÷ 0.6 = 48 ÷ 6 = 8</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Estimate</b>Round to 1 s.f.<br>4.87 × 21.3 ≈ 5 × 20 = 100<br>Round at the END, not the middle</div>
    </div>
    <p style="text-align:center;font-size:12pt;margin:0"><b>Money:</b> always 2 decimal places: €9.80</p>
    <p style="text-align:center;font-size:10pt;color:var(--muted)">Léim · leim.ie · Play Round It: leim.ie/round-it.html</p>
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
    <li>A taxi charges €4.20 plus €1.35 per km. How much is a 12.6 km journey?<span class="long"></span><span class="long"></span></li>
    <li>(a) Estimate (12.4 × 0.49) ÷ 2.1 by rounding each number to 1 significant figure. (b) Use a calculator to find the answer correct to 2 decimal places.<span class="long"></span><span class="long"></span></li>
    <li>A marathon is 42.195 km. Orla runs it in 3.5 hours. Find her average speed in km/h, correct to 1 decimal place. Why should she not round 42.195 to 42 first?<span class="long"></span><span class="long"></span></li>
    <li>Juice costs €0.85 a carton. Does €21 buy 24 cartons? Show your work.<span class="long"></span></li>
    <li>Best buy: 1.5 kg of rice for €6.75 or 2.4 kg for €10.20? Find the price per kg of each.<span class="long"></span><span class="long"></span></li>
  </ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">For the teacher</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>Estimation Auction</h2>
  <table><tbody>{"".join(f"<tr><td style='width:6%'>{i}</td><td style='width:40%'>{s}</td><td>{k}</td></tr>" for i,(s,tr,k) in enumerate(AUC,1))}</tbody></table>
  <h2>A. Error Hunt</h2>
  <table><tbody>{"".join(f"<tr><td style='width:28%'><b>{q}</b></td><td>{r}</td></tr>" for q,w,r in ERR)}</tbody></table>
  <h2>B. Exam-style questions</h2>
  <ol class="q">
    <li>1.35 × 12.6 = 17.01, plus 4.20 = <b>€{taxi:.2f}</b></li>
    <li>(a) 10 × 0.5 ÷ 2 = <b>2.5</b> (b) 6.076 ÷ 2.1 = 2.893… = <b>{dp(W2, 2)}</b> (close to 2.5, so reasonable)</li>
    <li>42.195 ÷ 3.5 = 12.055… = <b>{dp(ran, 1)} km/h</b>. Rounding first (42 ÷ 3.5 = 12) gives a different answer: round at the end.</li>
    <li>24 × €0.85 = €20.40, which is less than €21, so <b>yes</b> (60c change).</li>
    <li>€6.75 ÷ 1.5 = <b>€{per:.2f}</b>/kg; €10.20 ÷ 2.4 = <b>€{per2:.2f}</b>/kg, so the <b>2.4 kg bag</b> is better value.</li>
  </ol>
  <h2>Marking tip</h2>
  <p>Give credit for each step, as the exam does: the correct unrounded answer with a rounding slip still earns most of the marks. Insist on writing the estimate, and on 2 decimal places for money.</p>
</div>
</body></html>"""

cover = """<!doctype html><html><head><meta charset="utf-8"><style>
body{margin:0;width:1200px;height:1200px;background:#1B2430;font-family:Inter,sans-serif;color:#fff;display:flex;flex-direction:column;justify-content:space-between;padding:90px;box-sizing:border-box}
.k{display:inline-block;background:#2E7D57;border-radius:99px;padding:12px 26px;font-weight:700;font-size:28px;letter-spacing:.06em;text-transform:uppercase}
h1{font-size:112px;font-weight:800;line-height:1.08;letter-spacing:-.03em;margin:40px 0 0}
h1 span{background:#F6CF5A;color:#1B2430;padding:0 14px}
.sub{font-size:38px;color:#C9D1DA;margin-top:36px;line-height:1.35}
.em{font-size:52px;margin-top:30px;font-weight:800;letter-spacing:.01em;color:#F6CF5A}
.foot{display:flex;justify-content:space-between;align-items:center;font-size:34px;font-weight:700}
.price{background:#F6CF5A;color:#1B2430;border-radius:16px;padding:14px 28px}
</style></head><body>
<div><span class="k">Junior Cycle Maths · Teacher pack</span>
<h1><span>Decimals</span><br><span>&amp; Rounding</span></h1>
<div class="sub">Human Number Line · Estimation Auction<br>Rounding Dominoes · Poster · Worksheet + answers</div>
<div class="em">0.5 &gt; 0.45 · 4.87 × 21.3 ≈ 100</div></div>
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
    pdf("teacher-pack", os.path.join(OUT, "Decimals-and-Rounding-Teacher-Pack-Leim.pdf"))
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--hide-scrollbars", "--window-size=1200,1200",
                    f"--screenshot={os.path.join(OUT, f'{SLUG}-cover.png')}", f"{SLUG}-cover.html"], cwd=SRC, check=True, capture_output=True)
    print("domino chain:", [(x, show(x, v)) for x, v in chain])
