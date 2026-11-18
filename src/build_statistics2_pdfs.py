#!/usr/bin/env python3
"""Statistics 2: graphs & averages (JC Maths topic 22): free sheet + teacher pack + Payhip cover.
Run from the repo root: python3 src/build_statistics2_pdfs.py OUTDIR
Writes src/statistics-graphs-averages-*.html; PDFs/cover PNG go to OUTDIR (free sheet also to printables/).
Charts are drawn with the GAME's chart kit (src/stats_charts_bridge.js) and every chart is read back with
test_average_ace.py's readers (bar heights from the gridlines, pie angles from the arcs, histogram classes,
ordered stem-and-leaf plots); every answer is computed with Fraction and asserted."""
import os, sys, random, subprocess, re, json, math
from fractions import Fraction as F
from collections import Counter
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC)
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/stats2"; os.makedirs(OUT, exist_ok=True)
SLUG = "statistics-graphs-averages"
LO = "SP.3d, SP.3e, SP.3f, SP.3g, SP.3h"

def dec(x):
    x = F(x)
    if x.denominator == 1: return str(x.numerator)
    s = f"{float(x):.6f}".rstrip("0").rstrip("."); assert F(s) == x, x; return s
def r1(x): x = F(x); return F(math.floor(x * 10 + F(1, 2)), 10)
def mean(a): return F(sum(a), len(a))
def median(a):
    s = sorted(a); n = len(s); return F(s[(n - 1) // 2]) if n % 2 else F(s[n // 2 - 1] + s[n // 2], 2)
def mode(a):
    c = Counter(a).most_common(); assert c[0][1] > c[1][1]; return c[0][0]
def rng(a): return max(a) - min(a)
def fmean(xs, fs): return F(sum(x * f for x, f in zip(xs, fs)), sum(fs))
def fmedian(xs, fs): return median([x for x, f in zip(xs, fs) for _ in range(f)])
def angles(fs): N = sum(fs); assert 360 % N == 0; return [f * 360 // N for f in fs]
def fr(x): x = F(x); return f"{x.numerator}/{x.denominator}"

# ---------- charts from the game's kit, each read back ----------
J = json.dumps
def bar(t, c, f, ticks, yl="Frequency"): return f"barSVG({J(t)},{J(c)},{J(f)},{J(ticks)},{J(yl)})"
def pie(t, c, a, lab): return f"pieSVG({J(t)},{J(c)},{J(a)},{J(lab)})"
def hist(t, lo, w, f, xl): return f"histSVG({J(t)},{lo},{w},{J(f)},{J(xl)})"
def sl(v, key): return f"slHTML({J(v)},{J(key)})"
def btb(A, B, na, nb, key): return f"btbHTML({J(A)},{J(B)},{J(na)},{J(nb)},{J(key)})"

SP_C, SP_F = ["Hurling", "Soccer", "Rugby", "Camogie"], [8, 12, 4, 6]
HI_F = [3, 7, 9, 5]
SLV = [31, 35, 38, 42, 44, 44, 47, 50, 53, 56, 58, 61, 64, 67, 72]
E31A = [21, 25, 28, 32, 34, 36, 36, 41, 45, 48, 52]; E31B = [18, 22, 27, 29, 30, 31, 33, 35, 38]
E34 = ["Museum A", "Museum B"]; E34F = [105, 120]
P_C, P_F = ["Walk", "Bus", "Car", "Bike"], [6, 9, 3, 2]
W4A = [18, 21, 23, 24, 27, 29, 31, 35, 38]; W4B = [19, 22, 25, 26, 26, 28, 30, 33, 34, 41, 44]
CH = {
    "ruleBar": bar("How 1st years travel", P_C, P_F, list(range(10))),
    "rulePie": pie("How 1st years travel", P_C, angles(P_F), [f"{a}°" for a in angles(P_F)]),
    "ruleBtb": btb([11, 14, 18, 22, 25, 25, 31, 36], [16, 23, 27, 29, 32, 34, 34, 38, 45], "Boys", "Girls", "Key: 5 | 2 | 3 = 25 for Boys and 23 for Girls"),
    "pBar": bar("Favourite sport of 30 students", SP_C, SP_F, list(range(0, 14, 2))),
    "pHist": hist("Heights of 2nd years", 140, 10, HI_F, "Height (cm)"),
    "pSl": sl(SLV, "Key: 4 | 2 = 42 marks"),
    "e31": btb(E31A, E31B, "Class A", "Class B", "Key: 5 | 2 | 2 = 25 for Class A and 22 for Class B"),
    "e34": bar("Visitors last Sunday", E34, E34F, list(range(100, 125, 5)), ""),
    "posterBar": bar("Favourite sport", SP_C, SP_F, list(range(0, 14, 2))),
    "posterPie": pie("Favourite sport", SP_C, angles(SP_F), [f"{a}°" for a in angles(SP_F)]),
}
CHS = json.loads(subprocess.run(["node", os.path.join(SRC, "stats_charts_bridge.js")], input=json.dumps(CH), capture_output=True, text=True, check=True).stdout)
_argv = sys.argv; sys.argv = ["x"]
_ns = {}; exec(open(os.path.join(SRC, "test_average_ace.py"), encoding="utf-8").read().split("if __name__")[0], _ns); sys.argv = _argv
def barvals(k): bars, _ = _ns["read_bar"](_ns["charts"](CHS[k])[0], need_grid=(k != "e34")); return {b[0]: b[1] for b in bars}
assert barvals("pBar") == dict(zip(SP_C, SP_F)) and barvals("ruleBar") == dict(zip(P_C, P_F)) and barvals("e34") == dict(zip(E34, E34F))
for k, (C_, F_) in (("rulePie", (P_C, P_F)), ("posterPie", (SP_C, SP_F))):
    secs = _ns["read_pie"](_ns["charts"](CHS[k])[0])
    assert {s["cat"]: round(s["ang"]) for s in secs} == dict(zip(C_, angles(F_))) and all(abs(float(s["label"][:-1]) - s["ang"]) < .05 for s in secs)
assert [f for *_, f in _ns["read_hist"](_ns["charts"](CHS["pHist"])[0])] == HI_F
assert sorted(_ns["read_sl"](CHS["pSl"])) == SLV
na, nb, A_, B_ = _ns["read_btb"](CHS["e31"]); assert sorted(A_) == E31A and sorted(B_) == E31B
na, nb, A_, B_ = _ns["read_btb"](CHS["ruleBtb"]); assert median(A_) == F(47, 2) and median(B_) == 32

# ---------- free sheet ----------
L1 = [4, 7, 9, 3, 7]; L5 = [12, 5, 9, 15, 8, 10]; L6 = [9, 14, 8, 12, 10]; PM = [8, 10, 9, 12, 11, 90]
A = [(f"Find the mean of {', '.join(map(str, L1))}.", dec(mean(L1))),
     ("Find the median of the numbers in question 1.", dec(median(L1))),
     ("Find the mode of the numbers in question 1.", dec(mode(L1))),
     ("Find the range of the numbers in question 1.", dec(rng(L1))),
     (f"Find the median of {', '.join(map(str, L5))}.", dec(median(L5))),
     (f"The mean of six numbers is 11. Five of them are {', '.join(map(str, L6))}. Find the sixth.", dec(6 * 11 - sum(L6))),
     ("Aoife's mean mark over 4 tests is 70. She gets 85 in the 5th test. What is her new mean?", dec(F(4 * 70 + 85, 5))),
     ("Which average is the only one you can use for favourite colours?", "Mode"),
     (f"Weekly pocket money (€): {', '.join(map(str, PM))}. Which average gives the best typical value, and what is it?", f"Median, €{dec(median(PM))}"),
     ("The numbers 3, 5, 7, 9 have a mean of 6. The number 6 is added. What happens to the mean?", "It stays the same (6)")]
assert [a for q, a in A][:7] == ["6", "7", "7", "6", "9.5", "13", "73"] and mean([3, 5, 7, 9, 6]) == 6
GX, GF = [0, 1, 2, 3, 4], [3, 6, 5, 4, 2]; TC, TF = ["0–10", "10–20", "20–30", "30–40"], [3, 7, 8, 2]
gm = F(sum((10 * i + 5) * f for i, f in enumerate(TF)), sum(TF))
B = [("How many matches are in the table?", dec(sum(GF))), ("What is the mode?", f"{GX[GF.index(max(GF))]} goal"),
     ("What is the median?", dec(fmedian(GX, GF))), ("What is the mean number of goals?", dec(fmean(GX, GF))),
     ("Use mid-interval values to estimate the mean homework time.", dec(gm) + " minutes"), ("What is the modal class of the homework times?", TC[TF.index(max(TF))])]
assert [a for q, a in B] == ["20", "1 goal", "2", "1.8", "19.5 minutes", "20–30"]
N_SP = sum(SP_F); ang = angles(SP_F)
Cq = [("How many students chose soccer?", str(SP_F[1])), ("How many students are in the survey?", str(N_SP)),
      ("How many more chose hurling than rugby?", str(SP_F[0] - SP_F[2])), ("What is the mode?", SP_C[SP_F.index(max(SP_F))]),
      ("What percentage chose camogie?", dec(F(SP_F[3] * 100, N_SP)) + "%"), ("In a pie chart of the same data, what is the angle for hurling?", f"{ang[0]}°"),
      ("What is the angle for soccer?", f"{ang[1]}°"),
      ("How many students are shown in the histogram?", str(sum(HI_F))), ("What is the modal class?", "160–170 cm"),
      ("How many students are at least 160 cm tall?", str(HI_F[2] + HI_F[3]))]
assert [a for q, a in Cq] == ["12", "30", "4", "Soccer", "20%", "96°", "144°", "24", "160–170 cm", "14"]
D = [("What is the median mark?", dec(median(SLV))), ("What is the range?", dec(rng(SLV))), ("What is the mode?", dec(mode(SLV))),
     ("How many students scored more than 55?", str(sum(v > 55 for v in SLV)))]
assert [a for q, a in D] == ["50", "41", "44", "6"]
P32 = ["Bus", "Car", "Train", "Walk"]; P32F = [21, 18, 12, 9]; a32 = angles(P32F)
assert a32 == [126, 108, 72, 54] and sum(P32F) == 60
E = [("<b>Two classes.</b> The back-to-back stem-and-leaf plot shows the marks two classes got in a quiz. (a) Find the median and the range for each class. (b) Compare the two classes, using your answers.",
      f"(a) Class A: median <b>{dec(median(E31A))}</b>, range <b>{rng(E31A)}</b>. Class B: median <b>{dec(median(E31B))}</b>, range <b>{rng(E31B)}</b>. (b) Class A did better on average (higher median) but their marks were more spread out (bigger range)."),
     (f"<b>Getting to the concert.</b> 60 people said how they got to a concert: Bus 21, Car 18, Train 12, Walk 9. (a) Find the angle for each sector of a pie chart. (b) What percentage came by train? (c) Draw the pie chart.",
      f"(a) 360° ÷ 60 = 6° each: Bus <b>{a32[0]}°</b>, Car <b>{a32[1]}°</b>, Train <b>{a32[2]}°</b>, Walk <b>{a32[3]}°</b> (360° ✓) (b) 12/60 = <b>{dec(F(1200, 60))}%</b> (c) sectors drawn with a protractor, labelled, with a title"),
     ("<b>Means and outliers.</b> (a) The mean of five numbers is 12. A sixth number is added and the mean becomes 13. Find the sixth number. (b) Explain why the mean of 2, 3, 3, 4, 48 is not a good typical value, and give a better one.",
      f"(a) 6 × 13 − 5 × 12 = <b>{6 * 13 - 5 * 12}</b> (b) The mean is {dec(mean([2, 3, 3, 4, 48]))}, dragged up by the outlier 48; the <b>median, {dec(median([2, 3, 3, 4, 48]))}</b>, is typical."),
     ("<b>Visitors.</b> The bar chart shows the visitors to two museums last Sunday. (a) How many visitors did each museum have? (b) A newspaper says \"Museum B had four times as many visitors as Museum A\". Why does the chart make it look that way? Is it true? (c) How should the chart be drawn?",
      f"(a) A <b>{E34F[0]}</b>, B <b>{E34F[1]}</b> (b) The vertical axis starts at <b>100</b>, not 0, so B's bar (20 above 100) looks 4 times A's (5 above 100). Not true: B had only {E34F[1] - E34F[0]} more, about {dec(r1(F(E34F[1] - E34F[0], E34F[0]) * 100))}% more. (c) Start the axis at 0 with equal steps.")]
assert 6 * 13 - 5 * 12 == 18 and median([2, 3, 3, 4, 48]) == 3 and (E34F[1] - 100) == 4 * (E34F[0] - 100)

def qs(items): return "".join(f"<li>{q} <span class='line'></span></li>" for q, a in items)
def style(var):
    return re.search(var + r' = f"""<!doctype.*?<style>(.*?)</style>', open(os.path.join(SRC, "build_money1_pdfs.py"), encoding="utf-8").read(), re.S).group(1).replace("{LO}", LO).replace("{{", "{").replace("}}", "}")
SHEET_STYLE = style("sheet"); PACK_STYLE = style("pack")
assert "@bottom-left" in SHEET_STYLE and "Single-teacher licence" in PACK_STYLE and "{{" not in SHEET_STYLE + PACK_STYLE
CCSS = """svg.chart{margin:0 auto!important;border-width:1px!important}.gfig{float:right;width:62mm;margin:0 0 1mm 3mm}.gfig2{width:58mm;margin:1mm auto}
table.sl,table.btb{font-size:10pt!important;margin:0 auto!important}table.sl td,table.btb td,table.btb th{padding:1px 6px!important;border-top:0;border-bottom:0;white-space:nowrap}.key{font-size:8pt!important;margin:1px 0 3px!important;text-align:center}
.fm4{display:grid;grid-template-columns:1fr 1fr;gap:1.5mm}.fm4 div{border:1.5px solid var(--line);border-radius:8px;padding:2px 6px;font-size:9pt}.fm4 b{display:block}
.ftab{width:auto!important;margin:2px auto!important}.ftab td,.ftab th{padding:1px 8px!important;font-size:9pt!important}
.ht{width:auto;margin:2px 0}.ht td,.ht th{padding:1px 7px;font-size:8.8pt;text-align:center}.ht th{background:var(--green-soft);color:var(--ink);text-transform:none;letter-spacing:0}"""
def htab(r1_, r2_, h1, h2): return f'<table class="ht"><tr><th>{h1}</th>' + "".join(f"<td>{x}</td>" for x in r1_) + f'</tr><tr><th>{h2}</th>' + "".join(f"<td>{x}</td>" for x in r2_) + "</tr></table>"

sheet = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Statistics: graphs and averages: rules and practice | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{SHEET_STYLE}
{CCSS}
</style></head><body>
<div class="page tight">
  <div class="band"><div><div class="k">Junior Cycle Maths · Free revision sheet</div><h1>Statistics: graphs &amp; averages</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2018 specification): {LO}. Play the game: <b>leim.ie/average-ace.html</b></p>
  <div class="two">
   <div><h2>1. Three averages and the range</h2>
    <div class="fm4"><div><b>Mean</b>total ÷ how many<br>3, 5, 8, 8 → 24 ÷ 4 = 6</div><div><b>Median</b>in ORDER, the middle<br>3, 5, 8, 8 → 6.5</div><div><b>Mode</b>most often<br>3, 5, 8, 8 → 8</div><div><b>Range</b>biggest − smallest<br>8 − 3 = 5 (spread)</div></div>
    <p style="margin-top:3px"><b>Missing value:</b> mean 7 of 5 numbers → total 35; subtract the ones you know. <b>New value:</b> new total ÷ new count.</p>
    <h2>2. From a frequency table</h2>
    {htab([0, 1, 2, 3], [2, 5, 2, 1], "Goals (x)", "Matches (f)")}
    <p><b>Mean</b> = Σfx ÷ Σf = 12 ÷ 10 = 1.2. <b>Mode</b> = the value with the biggest frequency (1, not 5). <b>Median</b>: count down to values 5 and 6 → 1.</p>
    <p><b>Grouped data</b> (0–10, 10–20…): use the <b>mid-interval</b> values (5, 15…) to <b>estimate</b> the mean. "10–20" means at least 10, less than 20.</p>
    <h2>3. Which display?</h2>
    <p><b>Bar chart</b>: compare categories. <b>Pie chart</b>: parts of one whole. <b>Line plot</b>: a few small numbers, one dot each. <b>Histogram</b>: lots of numerical data in equal classes (bars touch). <b>Stem-and-leaf</b>: keeps every value, in order, with a key. <b>Back-to-back</b>: compares two groups.</p>
    <h2>4. Pie chart angles</h2>
    <div class="gfig" style="width:44mm">{CHS["rulePie"]}</div>
    <p>360° ÷ total = degrees for one person. 20 students: 18° each, so Bus 9 × 18° = 162°. Angles add up to 360°.</p></div>
   <div><h2>5. Stem-and-leaf plots</h2>
    {CHS["ruleBtb"]}
    <p>Tens on the stem, units as leaves, <b>in order</b>, with a key. In a back-to-back plot the left leaves get bigger going <b>outwards</b>: 5 | 2 is 25. Boys' median 23.5, Girls' 32.</p>
    <h2>6. Comparing two groups</h2>
    <p>Give an <b>average</b> and the <b>range</b> for each, then say what they mean in words: "The girls did better on average, and their marks were less spread out."</p>
    <h2>7. Misleading charts</h2>
    <p>Watch for: a vertical axis that <b>doesn't start at 0</b>, <b>uneven gaps</b> on a scale, a pie chart whose parts don't add to <b>100%</b>, 3-D slices, pictures that grow both ways.</p>
    <h2>8. Samples have limits</h2>
    <p>"8 of my 10 friends like it" describes your 10 friends, not all students in Ireland. A small or non-random sample can't support a big claim. Say what limits your conclusion.</p>
    <div class="note"><b>Classic mistakes:</b> median without ordering · the median's position instead of its value · the frequency as the mode · Σfx ÷ number of rows · reading the left side of a back-to-back plot backwards · pie angles that don't make 360°.</div></div>
  </div>
  <div class="tip"><b>Exam tip:</b> show the total and what you divide by; when you compare, use numbers AND words; give every chart a title, labelled axes and (for stem-and-leaf) a key.</div>
</div>

<div class="page p2">
  <div class="band"><div><div class="k">Practice · 34 questions</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Averages</h2><ol class="q">{qs(A)}</ol>
  <h2>B. Frequency tables</h2>
  <div style="display:flex;gap:6mm;align-items:center">{htab(GX, GF, "Goals", "Matches")}{htab(TC, TF, "Time (min)", "Students")}</div>
  <ol class="q" start="11">{qs(B)}</ol>
  <h2>C. Charts</h2>
  <div class="gfig" style="width:56mm">{CHS["pBar"]}<div style="height:1mm"></div>{CHS["pHist"]}</div>
  <ol class="q" start="17">{qs(Cq)}</ol>
  <h2 style="clear:both">D. Stem-and-leaf (marks out of 80)</h2>
  <div style="display:flex;gap:6mm;align-items:flex-start"><div>{CHS["pSl"]}</div><ol class="q" start="27" style="flex:1">{qs(D)}</ol></div>
  <p class="small" style="margin-top:2px">Questions 31–34 are on the next page.</p>
</div>

<div class="page">
  <div class="band"><div><div class="k">Exam-style · then check</div><h1>Exam corner + answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>E. Exam-style questions (show your work)</h2>
  <ol class="q e3" start="31">
   <li>{E[0][0]}<div class="gfig2">{CHS["e31"]}</div><span class='long'></span></li>
   <li>{E[1][0]}<span class='long'></span></li>
   <li>{E[2][0]}<span class='long'></span></li>
   <li><div class="gfig" style="width:46mm">{CHS["e34"]}</div>{E[3][0]}<span class='long'></span></li>
  </ol>
  <h2 style="margin-top:6px;clear:both">Answers</h2>
  <table class="ans"><tbody>
   <tr><td><b>A</b></td><td>{" · ".join(f"{i}. {a}" for i, (q, a) in enumerate(A, 1))}</td></tr>
   <tr><td><b>B</b></td><td>{" · ".join(f"{i}. {a}" for i, (q, a) in enumerate(B, 11))}</td></tr>
   <tr><td><b>C</b></td><td>{" · ".join(f"{i}. {a}" for i, (q, a) in enumerate(Cq, 17))}</td></tr>
   <tr><td><b>D</b></td><td>{" · ".join(f"{i}. {a}" for i, (q, a) in enumerate(D, 27))}</td></tr>
   <tr><td><b>E</b></td><td>{" · ".join(f"{i}. {a}" for i, (q, a) in enumerate(E, 31))}</td></tr>
  </tbody></table>
  <div class="note"><b>Got one wrong?</b> Check: did you put the values in order before finding the median? Did you give the value (not the frequency) as the mode? Did you divide Σfx by the total frequency? Then play <b>Average Ace</b> at leim.ie/average-ace.html: the "Go back over these" list at the end shows the rule for each mistake.</div>
  <p class="small">All questions written by Léim. Léim is independent and not connected with the State Examinations Commission or the NCCA.</p>
</div>
</body></html>"""

# ---------- teacher pack ----------
MATCH = [("Mean of 2, 4, 9", "5"), ("Median of 8, 3, 6, 1, 9", "6"), ("Mode of 4, 7, 7, 2, 4, 7", "7"), ("Range of 15, 3, 22, 9", "19"),
         ("Median of 2, 5, 8, 11", "6.5"), ("Mean of 5 numbers is 8: their total", "40"), ("Pie chart of 30 people: angle for one person", "12°"),
         ("Pie chart of 45 people: 10 chose tea. Angle?", "80°"), ("Values 1, 2, 3 with frequencies 2, 5, 3: mean", "2.1"),
         ("Back-to-back plot: left leaf 7 on stem 2", "27"), ("Mean of 4 tests is 60, 5th test 85: new mean", "65"), ("18 out of 72 chose soccer: %", "25%")]
chk = [dec(mean([2, 4, 9])), dec(median([8, 3, 6, 1, 9])), dec(mode([4, 7, 7, 2, 4, 7])), dec(rng([15, 3, 22, 9])), dec(median([2, 5, 8, 11])), dec(5 * 8),
       f"{360 // 30}°", f"{10 * 360 // 45}°", dec(fmean([1, 2, 3], [2, 5, 3])), "27", dec(F(4 * 60 + 85, 5)), dec(F(1800, 72)) + "%"]
assert [a for q, a in MATCH] == chk and len(set(chk)) == 12, chk
cards = [q for q, a in MATCH] + [a for q, a in MATCH]
random.seed(22); match_print = cards[:]; random.shuffle(match_print)
match_html = "".join(f'<div class="c"><span class="tag">Card {i}</span><div class="fc{" sm" if len(x) > 10 else ""}">{x}</div></div>' for i, x in enumerate(match_print, 1))
match_key = " · ".join(f"{match_print.index(q) + 1} → {match_print.index(a) + 1}" for q, a in MATCH)

# Class Data Swap: each fact on exactly ONE card
RT1 = [24, 27, 29, 31, 33, 35, 36, 38, 41, 44, 47]; RT3 = [21, 22, 25, 26, 28, 29, 30, 32, 34, 37, 39]
assert (median(RT1), rng(RT1), median(RT3), rng(RT3)) == (35, 23, 29, 18)
PT, PB, PW, PBk = 40, 14, 8, 6; PCar = PT - PB - PW - PBk; pa = [PB * 9, PCar * 9, PW * 9, PBk * 9]
assert PCar == 12 and pa == [126, 108, 72, 54] and sum(pa) == 360
TR = [("1st years' reaction times (hundredths of a second)", ", ".join(map(str, RT1)), "A"), ("3rd years' reaction times", ", ".join(map(str, RT3)), "B"),
      ("Median: 1st years · 3rd years", "", None), ("Range: 1st years · 3rd years", "", None), ("Who reacted faster on average?", "", None)]
PR = [("Students asked", "40", "A"), ("Bus", "14", "A"), ("Walk", "8", "B"), ("Bike", "6", "B"),
      ("Car (the rest)", "", None), ("Degrees for one student", "", None), ("Angles: Bus · Car · Walk · Bike", "", None)]
for rows in (TR, PR):
    assert all(w in ("A", "B") for _, v, w in rows if v) and any(w == "A" for *_, w in rows) and any(w == "B" for *_, w in rows)
def swap_card(who):
    def tab(title, rows):
        return f'<table class="ss"><thead><tr><th colspan="2">{title}</th></tr></thead><tbody>' + "".join(
            f"<tr><td>{k}</td><td><b>{v if w == who else ''}</b></td></tr>" for k, v, w in rows) + "</tbody></table>"
    return f'<div class="idc"><h3>Student {who} · Class Data Swap</h3><div class="two">{tab("Catch the ruler: reaction times", TR)}{tab("How we get to school (pie chart)", PR)}</div></div>'

DOMS = [("Mean of 3, 5, 10", "6"), ("Median of 1, 4, 9, 12, 20", "9"), ("Mode of 2, 3, 3, 11, 11, 11", "11"), ("Range of 14, 30, 22", "16"),
        ("Median of 3, 7, 10, 15", "8.5"), ("Mean of 10 values is 4.5: their total", "45"), ("360° ÷ 24 people", "15°"),
        ("Pie of 20 people: 5 chose rugby. Angle?", "90°"), ("A 120° sector: what fraction of the whole?", "1/3"),
        ("Display for parts of one whole", "pie chart"), ("Display to compare two groups, keeping every value", "back-to-back plot"),
        ("Display for 200 heights in classes", "histogram"), ("Best average for favourite colours", "mode"),
        ("Best typical value when there's an outlier", "median"), ("Mid-interval value of 20–30", "25"),
        ("Values 0, 1, 2, frequencies 3, 4, 5: how many values?", "12"), ("Values 0, 1, 2, frequencies 3, 4, 5: Σfx", "14"),
        ("Bars of 6, 9 and 5: how many altogether?", "20"), ("A bar chart's axis should start at…", "0"), ("Mean of 4 numbers is 7. Three are 5, 6, 9. The 4th?", "8")]
dchk = [dec(mean([3, 5, 10])), dec(median([1, 4, 9, 12, 20])), dec(mode([2, 3, 3, 11, 11, 11])), dec(rng([14, 30, 22])), dec(median([3, 7, 10, 15])), dec(F(45)),
        f"{360 // 24}°", f"{5 * 360 // 20}°", fr(F(120, 360))]
assert [a for q, a in DOMS][:9] == dchk and sum([3, 4, 5]) == 12 and 0 * 3 + 1 * 4 + 2 * 5 == 14 and 6 + 9 + 5 == 20 and 4 * 7 - (5 + 6 + 9) == 8 and (20 + 30) // 2 == 25
assert len(set(a for q, a in DOMS)) == 20
random.seed(2222); chain = DOMS[:]; random.shuffle(chain)
dom = [("START" if k == 0 else chain[k - 1][1], x[0]) for k, x in enumerate(chain)] + [(chain[-1][1], "FINISH")]
dom_print = dom[:]; random.shuffle(dom_print)
dom_html = "".join(f'<div class="dom"><div class="h l{" sm" if len(l) > 9 else ""}">{l}</div><div class="h r">{r}</div></div>' for l, r in dom_print)
chain_key = "".join(f"<li>{x} = <b>{a}</b></li>" for x, a in chain)

ERR = [("Median of 9, 2, 7, 4, 5", "7 (the middle one)", f"Put them in order first: 2, 4, 5, 7, 9. Median = <b>{dec(median([9, 2, 7, 4, 5]))}</b>"),
       ("Goals 0, 1, 2, 3 with frequencies 4, 9, 6, 1. The mode?", "9", f"9 is the frequency. The mode is the value: <b>{[0, 1, 2, 3][[4, 9, 6, 1].index(9)]} goal</b>"),
       ("Values 1, 2, 3 with frequencies 2, 3, 5. The mean?", "(1 + 2 + 3) ÷ 3 = 2", f"Use Σfx ÷ Σf: (2 + 6 + 15) ÷ 10 = <b>{dec(fmean([1, 2, 3], [2, 3, 5]))}</b>"),
       ("Pie chart of 40 people: 12 chose the bus. Angle?", "12°", f"Each person is 360° ÷ 40 = 9°: 12 × 9° = <b>{12 * 9}°</b>"),
       ("Back-to-back plot: left leaf 6 beside stem 3", "63", "The stem is the tens: <b>36</b>"),
       ("Range of 15, 8, 22, 11", "22", f"Range = biggest − smallest = 22 − 8 = <b>{rng([15, 8, 22, 11])}</b>")]
WL = [12, 15, 9, 15, 20, 13, 14]; SX, SF = [0, 1, 2, 3, 4], [4, 7, 6, 2, 1]; WP = ["Maths", "English", "Science", "Art"], [9, 7, 12, 8]
WT, WTF = ["0–20", "20–40", "40–60", "60–80"], [5, 9, 4, 2]; wtm = F(sum((20 * i + 10) * f for i, f in enumerate(WTF)), sum(WTF))
assert (mean(WL), median(WL), mode(WL), rng(WL)) == (14, 14, 15, 11)
assert (fmean(SX, SF), fmedian(SX, SF), sum(SF)) == (F(29, 20), 1, 20) and angles(WP[1]) == [90, 70, 120, 80] and wtm == 33
assert (median(W4A), rng(W4A), median(W4B), rng(W4B)) == (27, 20, 28, 25)
CH2 = {"wBtbKey": btb(W4A, W4B, "Team A", "Team B", "Key: 3 | 2 | 2 = 23 for Team A and 22 for Team B")}
CHS.update(json.loads(subprocess.run(["node", os.path.join(SRC, "stats_charts_bridge.js")], input=json.dumps(CH2), capture_output=True, text=True, check=True).stdout))
na, nb, A_, B_ = _ns["read_btb"](CHS["wBtbKey"]); assert sorted(A_) == W4A and sorted(B_) == W4B

pack = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Graphs and Averages Teacher Pack | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{PACK_STYLE}
{CCSS}
.ss td:nth-child(2){{width:44%}}.ss td,.ss th{{padding:1px 5px;font-size:8.4pt;line-height:1.22}}.fym .c{{height:15mm}}.fym .fc.sm{{font-size:8.6pt}}.p1 .proc td{{font-size:8.5pt;padding:2px 6px}}
.dom .r{{font-size:9.6pt}}.pf2{{display:grid;grid-template-columns:1fr 1fr;gap:5mm;align-items:center}}
</style></head><body>

<div class="page p1">
  <div class="band"><div><div class="k">Junior Cycle Maths · Teacher pack</div><h1>Statistics: graphs &amp; averages</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2018 specification): {LO} (types of data, samples and frequency tables come first, in Statistics 1)</p>
  <div class="two">
    <div><h3>Aims</h3><p>By the end of the lesson students can find the mean, median, mode and range from lists and frequency tables (and estimate a grouped mean), read and draw bar charts, pie charts, line plots, histograms and ordered (back-to-back) stem-and-leaf plots, choose a suitable display and average, compare two groups in words, and spot misleading charts and claims. Good preparation for CBA 2.</p></div>
    <div><h3>In this pack</h3><p>p.1 Teacher notes · p.2 Average Ace mingle cards + Class Data Swap A/B cards · p.3 Statistics Dominoes (cut-up) · p.4 Wall poster · p.5 Worksheet: Error Hunt + exam-style questions · p.6 Answers. Level: 2nd year (Higher and Ordinary), or 3rd-year revision. Time: about 60 minutes. All questions are original.</p></div>
  </div>
  <h2 style="margin-top:8px">Procedure</h2>
  <table class="proc"><tbody>
    <tr><td>5 min</td><td><b>Lead-in: fair share.</b> Four students hold up 2, 7, 3 and 4 cubes (or pens). "Make it fair without anyone leaving." Students move cubes until everyone has 4. Ask: what stayed the same? (The total.) Build mean = total ÷ how many.</td></tr>
    <tr><td>8 min</td><td><b>Guided discovery: which average?</b> Board: pocket money €8, €10, €9, €12, €11, €90. Find the mean and the median. "Which tells a new student what's typical? Why?" Elicit outliers; then favourite colours: why only the mode works.</td></tr>
    <tr><td>10 min</td><td><b>Average Ace mingle</b> (p.2, 24 cards = 12 question/answer pairs; one card each). Question card? Work it out and find the person with your answer. Answer card? Find your question. Pairs check each other's working.</td></tr>
    <tr><td>12 min</td><td><b>Class Data Swap</b> (p.2, pairs, don't show your card). Each fact is on only ONE card. Dictate your reaction times so your partner can build a back-to-back plot, then both fill every blank. Feedback: medians {median(RT1)} and {median(RT3)}; ranges {rng(RT1)} and {rng(RT3)}; Car = {PCar}; angles {", ".join(f"{a}°" for a in pa)}.</td></tr>
    <tr><td>10 min</td><td><b>Statistics Dominoes</b> (p.3), groups of 3–4. Start with START, work out the clue, find the domino with that answer on its left, and build the chain to FINISH.</td></tr>
    <tr><td>12 min</td><td><b>Worksheet</b> (p.5). Error Hunt in pairs (find the mistake, name the rule, fix it), then the exam-style questions alone.</td></tr>
    <tr><td>3 min</td><td><b>Exit ticket.</b> Median of 6, 1, 9, 4? Pie chart of 36 people: angle for 5 people? (5; 50°.) Homework: play <b>Average Ace</b> at leim.ie/average-ace.html and copy three lines from the "Go back over these" list.</td></tr>
  </tbody></table>
  <div class="note"><b>Mingle key</b> (question card → answer card): {match_key}.<br>
  <b>Errors to look for:</b> median without ordering · the position instead of the median · the frequency as the mode · Σfx ÷ number of rows · back-to-back left leaves read backwards · pie angles that don't add to 360° · "higher" with no numbers when comparing. <b>Fast finishers:</b> make up 5 numbers with mean 10, median 8 and mode 7. (e.g. 7, 7, 8, 13, 15)</div>
  <p class="small"><b>Domino answer chain</b> (START → FINISH):</p>
  <ol class="small" style="columns:2;column-gap:12px;font-size:7pt;line-height:1.22;margin:0;padding-left:16px">{chain_key}</ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">Cut up the cards · one Data Swap card per student</div><h1>Average Ace + Class Data Swap</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:8.8pt;margin:0"><b>Average Ace mingle.</b> Cut out the 24 cards and give one to each student. Question card? Work it out, then find the person with your answer. Answer card? Find the question that gives your answer. (Fewer students? Take out whole pairs.)</p>
  <div class="fym">{match_html}</div>
  <p style="font-size:8.8pt;margin:3mm 0 0"><b>Class Data Swap.</b> Don't show your card. Each fact is on only one of the two cards: ask your partner for what you're missing (dictate the times slowly), then fill in every blank on both.</p>
  {swap_card("A")}
  {swap_card("B")}
</div>

<div class="page">
  <div class="band"><div><div class="k">Groups of 3–4 · cut along the dashed lines</div><h1>Statistics Dominoes</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.4pt">Start with START. Work out the clue on the right, then find the domino with that answer on its left. Keep going until you reach FINISH.</p>
  <div class="doms">{dom_html}</div>
</div>

<div class="page">
  <div class="poster">
    <h1>Graphs &amp; averages</h1>
    <div class="ops">
      <div style="background:var(--green-soft)"><b>Mean</b>add them all up<br>÷ how many</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Median</b>put them in ORDER<br>take the middle one</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Mode</b>the one that comes up<br>most often</div>
      <div style="background:var(--green-soft)"><b>Range</b>biggest − smallest<br>(the spread)</div>
    </div>
    <div class="pf2"><div>{CHS["posterBar"]}</div><div>{CHS["posterPie"]}</div></div>
    <p style="text-align:center;margin:0"><b>Pie chart:</b> 360° ÷ total = degrees for one · <b>Stem-and-leaf:</b> in order, with a key<br><b>Compare two groups:</b> an average AND the range, in words · <b>Axis starts at 0!</b></p>
    <p style="text-align:center;font-size:10pt;color:var(--muted)">Léim · leim.ie · Play Average Ace: leim.ie/average-ace.html</p>
  </div>
</div>

<div class="page ws">
  <div class="band"><div><div class="k">Worksheet</div><h1>Error Hunt + exam-style questions</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Error Hunt</h2>
  <p>Each answer has one mistake. Find it, say which rule was broken, and write the right answer.</p>
  <table class="eh"><thead><tr><th>Question</th><th>Student's answer</th><th>The mistake and the right answer</th></tr></thead><tbody>
  {"".join(f"<tr><td>{q}</td><td>{w}</td><td><span class='gap'></span><span class='gap'></span></td></tr>" for q, w, r in ERR)}
  </tbody></table>
  <h2>B. Exam-style questions (show all your work)</h2>
  <ol class="q">
    <li>Find the mean, median, mode and range of {", ".join(map(str, WL))}.<span class="long"></span></li>
    <li>The number of brothers and sisters of 20 students: 0: 4, 1: 7, 2: 6, 3: 2, 4: 1. Find the mean, the median and the mode.<span class="long"></span></li>
    <li>36 students named their favourite subject: Maths 9, English 7, Science 12, Art 8. Find the angle for each sector of a pie chart.<span class="long"></span></li>
    <li>The ages of the players on two teams: Team A {", ".join(map(str, W4A))}; Team B {", ".join(map(str, W4B))}. (a) Draw a back-to-back stem-and-leaf plot with a key. (b) Find the median and range of each team. (c) Compare the two teams.<span class="long"></span><span class="long"></span></li>
    <li>The times (seconds) 20 students took to solve a puzzle: 0–20: 5, 20–40: 9, 40–60: 4, 60–80: 2. (a) Estimate the mean time. (b) What is the modal class? (c) Why is (a) only an estimate?<span class="long"></span></li>
  </ol>
</div>

<div class="page an">
  <div class="band"><div><div class="k">For the teacher</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>Class Data Swap</h2>
  <div class="two"><table><tbody>
   <tr><td>Medians</td><td>1st years <b>{median(RT1)}</b> · 3rd years <b>{median(RT3)}</b></td></tr><tr><td>Ranges</td><td>1st years <b>{rng(RT1)}</b> · 3rd years <b>{rng(RT3)}</b></td></tr>
   <tr><td>Faster on average</td><td><b>3rd years</b> (lower median), and their times were less spread out</td></tr></tbody></table>
  <table><tbody>
   <tr><td>Car</td><td>40 − 14 − 8 − 6 = <b>{PCar}</b></td></tr><tr><td>One student</td><td>360° ÷ 40 = <b>9°</b></td></tr>
   <tr><td>Angles</td><td>Bus <b>{pa[0]}°</b> · Car <b>{pa[1]}°</b> · Walk <b>{pa[2]}°</b> · Bike <b>{pa[3]}°</b> (360° ✓)</td></tr></tbody></table></div>
  <h2>A. Error Hunt</h2>
  <table><tbody>{"".join(f"<tr><td style='width:36%'><b>{q}</b> → {w}</td><td>{r}</td></tr>" for q, w, r in ERR)}</tbody></table>
  <h2>B. Exam-style questions</h2>
  <ol class="q">
    <li>Mean 98 ÷ 7 = <b>{mean(WL)}</b> · median <b>{median(WL)}</b> (9, 12, 13, <b>14</b>, 15, 15, 20) · mode <b>{mode(WL)}</b> · range 20 − 9 = <b>{rng(WL)}</b></li>
    <li>Mean 29 ÷ 20 = <b>{dec(fmean(SX, SF))}</b> · median (values 10 and 11) <b>{fmedian(SX, SF)}</b> · mode <b>1</b></li>
    <li>10° each: Maths <b>90°</b>, English <b>70°</b>, Science <b>120°</b>, Art <b>80°</b> (360° ✓)</li>
    <li>(a) <div style="display:inline-block;vertical-align:top">{CHS["wBtbKey"]}</div> (b) Team A: median <b>{median(W4A)}</b>, range <b>{rng(W4A)}</b>; Team B: median <b>{median(W4B)}</b>, range <b>{rng(W4B)}</b> (c) Similar typical ages (Team B one year older), but Team B's ages are more spread out.</li>
    <li>(a) (10×5 + 30×9 + 50×4 + 70×2) ÷ 20 = 660 ÷ 20 = <b>{wtm} s</b> (b) <b>20–40</b> (c) We only know each time's class, so we use the middle of the class.</li>
  </ol>
  <h2>Marking tip</h2>
  <p>As in the exam, give credit for each step: the ordered list, the total and what it's divided by, the degrees for one person. "Compare" needs an average AND a measure of spread for both groups, with numbers and a sentence. A stem-and-leaf plot needs ordered leaves and a key.</p>
</div>
</body></html>"""

cover = """<!doctype html><html><head><meta charset="utf-8"><style>
body{margin:0;width:1200px;height:1200px;background:#1B2430;font-family:Inter,sans-serif;color:#fff;display:flex;flex-direction:column;justify-content:space-between;padding:90px;box-sizing:border-box}
.k{display:inline-block;background:#2E7D57;border-radius:99px;padding:12px 26px;font-weight:700;font-size:28px;letter-spacing:.06em;text-transform:uppercase}
h1{font-size:100px;font-weight:800;line-height:1.12;letter-spacing:-.03em;margin:40px 0 0}
h1 span{background:#F6CF5A;color:#1B2430;padding:0 14px}
.sub{font-size:38px;color:#C9D1DA;margin-top:36px;line-height:1.35}
.em{font-size:50px;margin-top:30px;font-weight:800;letter-spacing:.01em;color:#F6CF5A}
.foot{display:flex;justify-content:space-between;align-items:center;font-size:34px;font-weight:700}
.price{background:#F6CF5A;color:#1B2430;border-radius:16px;padding:14px 28px}
</style></head><body>
<div><span class="k">Junior Cycle Maths · Teacher pack</span>
<h1><span>Statistics:</span><br><span>Graphs &amp; Averages</span></h1>
<div class="sub">Average Ace mingle · Class Data Swap A/B<br>Statistics Dominoes · Poster · Worksheet + answers</div>
<div class="em">Mean · median · mode · range</div></div>
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
    pdf("teacher-pack", os.path.join(OUT, "Graphs-and-Averages-Teacher-Pack-Leim.pdf"))
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--hide-scrollbars", "--window-size=1200,1200",
                    f"--screenshot={os.path.join(OUT, f'{SLUG}-cover.png')}", f"{SLUG}-cover.html"], cwd=SRC, check=True, capture_output=True)
