#!/usr/bin/env python3
"""Money 2: income tax, net pay & compound interest (JC Maths topic 19): free sheet + teacher pack + Payhip cover.
Run from the repo root: python3 src/build_money2_pdfs.py OUTDIR
Writes src/money-tax-net-pay-compound-interest-*.html; PDFs/cover PNG go to OUTDIR (free sheet also to printables/).
Every answer is computed with Python's Fraction and asserted. Styles are read from src/build_money1_pdfs.py."""
import os, sys, random, subprocess, re
from fractions import Fraction as F
from math import floor
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC)
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/money2"; os.makedirs(OUT, exist_ok=True)
SLUG = "money-tax-net-pay-compound-interest"
LO = "N.2c, U.6"

def dec(x):
    x = F(x); k = 0
    while (x * 10 ** k).denominator != 1:
        k += 1; assert k < 8, x
    n = x * 10 ** k; s = str(abs(n.numerator)).rjust(k + 1, "0")
    s = s[:len(s) - k] + ("." + s[len(s) - k:] if k else "")
    return s
def pc(x): return dec(F(x)) + "%"
def cent(x): x = F(x); return F(floor(x * 100 + F(1, 2)), 100)     # nearest cent, half up
def m(x):
    x = F(x); assert (x * 100).denominator == 1, x; c = int(x * 100)
    return "€{:,}.{:02d}".format(c // 100, c % 100)
def grow(p, *rates):
    out = [F(p)]
    for r in rates: out.append(out[-1] * (1 + F(r) / 100))
    return out
def tax(gross, credit, cut=None):
    g = F(gross)
    gt = g / 5 if cut is None else F(cut) / 5 + (g - F(cut)) * F(2, 5)
    return gt - F(credit)
def rate2(p, a):  # same compound rate for 2 years, to 0.01%
    for k in range(1, 5001):
        r = F(k, 100)
        if F(p) * (1 + r / 100) ** 2 == F(a): return r
    raise AssertionError("no exact rate")
assert m(F(1234)) == "€1,234.00" and cent(F("3472.875")) == F("3472.88") and grow(1000, 10, 10, 10)[-1] == 1331 and tax(40000, 3000) == 5000

# ---------- free sheet ----------
A = [("Aoife works 38 hours a week at €14.80 an hour. Find her gross pay for the week.", m(38 * F("14.80"))),
     ("Cian earns €16 an hour for a basic 39-hour week and time-and-a-half for overtime. One week he works 44 hours. Find his gross pay.", m(39 * 16 + 5 * 16 * F(3, 2))),
     ("Méabh works 4 hours on a Sunday at double time. Her normal rate is €15.50 an hour. How much does she earn for those hours?", m(4 * 2 * F("15.50"))),
     ("Tadhg earns €680 gross a week. Find his gross pay for a year (52 weeks).", m(680 * 52)),
     ("Ciara earns €42,000 gross a year. How much is that a month?", m(F(42000, 12))),
     ("A payslip shows gross pay €745.00, income tax €58.40, USC €19.65 and PRSI €29.80. Find the net pay.", m(F("745") - F("58.40") - F("19.65") - F("29.80")))]
assert [a for q, a in A] == ["€562.40", "€744.00", "€124.00", "€35,360.00", "€3,500.00", "€637.15"], [a for q, a in A]
B = [("Find 20% of a gross income of €36,000 (the gross tax).", m(F(36000) / 5)),
     ("Seán earns €36,000 a year and has a tax credit of €4,000. The standard rate is 20%. Find the tax he pays.", m(tax(36000, 4000))),
     ("Find Seán's net income in question 8 (no other deductions).", m(36000 - tax(36000, 4000))),
     ("Róisín earns €52,500 a year with a tax credit of €3,750. Tax is 20%. Find her tax payable.", m(tax(52500, 3750))),
     ("Oisín earns €820 gross a week. His weekly tax credit is €75 and tax is 20%. Find his tax for the week.", m(tax(820, 75))),
     ("Niamh pays €5,100 income tax. Her tax credit is €3,900 and the rate is 20%. Find her gross income.", m((5100 + 3900) * 5)),
     ("<i>Higher Level:</i> Eoin earns €58,000. Cut-off point €44,000, rates 20% and 40%, tax credits €4,000. Find his tax.", m(tax(58000, 4000, 44000))),
     ("<i>Higher Level:</i> Gross pay €900 a week; tax €96, USC €27, PRSI 4% of gross. Find the net pay.", m(900 - 96 - 27 - F(900) * 4 / 100))]
assert [a for q, a in B] == ["€7,200.00", "€3,200.00", "€32,800.00", "€6,750.00", "€89.00", "€45,000.00", "€10,400.00", "€741.00"], [a for q, a in B]
g5 = grow(2000, 5, 5, 5); g19 = grow(8000, 2, 3); g21 = (6000 * F("1.04") - 2000) * F("1.04")
Cq = [("€2,000 is saved at 5% compound interest a year. Find the interest for the first year.", m(g5[1] - g5[0])),
      ("Find the value of the €2,000 in question 15 after 2 years.", m(g5[2])),
      ("Find the value of the €2,000 after 3 years.", m(g5[3])),
      ("How much interest is earned altogether in question 17?", m(g5[3] - 2000)),
      ("€8,000 earns 2% in year 1 and 3% in year 2 (compound). Find its value after 2 years.", m(g19[2])),
      ("What do you multiply by to add 3.5% interest?", dec(F("1.035"))),
      ("Kate borrows €6,000 at 4% compound interest. She repays €2,000 at the end of year 1. How much does she owe at the end of year 2?", m(g21)),
      ("<i>Higher Level:</i> After 2 years at 4% compound interest an investment is worth €10,816. How much was invested?", m(F(10816) / F("1.04") ** 2))]
assert [a for q, a in Cq] == ["€100.00", "€2,205.00", "€2,315.25", "€315.25", "€8,404.80", "1.035", "€4,409.60", "€10,000.00"], [a for q, a in Cq]
d24a, d24b = grow(10000, 4, 4)[-1], grow(10000, 2, 6)[-1]; assert (d24a, d24b) == (10816, 10812)
d29 = cent(grow(1500, 3, 3, 3)[-1]); assert d29 == F("1639.09")
D = [("Gross income €48,000; income tax €5,700, USC €1,050, PRSI €1,920. Find the net income.", m(48000 - 5700 - 1050 - 1920)),
     ("€10,000 for 2 years: Account A pays 4% each year; Account B pays 2% then 6%. Which is worth more, and by how much?", f"A, by {m(d24a - d24b)}"),
     ("Ella's gross pay of €600 a week goes up by 5%. Find her new gross pay.", m(600 * F("1.05"))),
     ("All of Ella's rise is taxed at 20%. How much more take-home pay does she get each week?", m(30 * F("0.8"))),
     ("Gross pay €2,900 a month; deductions €610 a month. Find the net pay for a year.", m((2900 - 610) * 12)),
     ("Income €40,000, tax payable €4,000. What percentage of the income is the tax?", pc(F(4000, 40000) * 100)),
     ("€1,500 is saved for 3 years at 3% compound interest. Find its value to the nearest cent.", m(d29)),
     ("<i>Higher Level:</i> €8,000 grows to €8,820 in 2 years at the same compound rate. Find the rate.", pc(rate2(8000, 8820)))]
assert [a for q, a in D] == ["€39,330.00", "A, by €4.00", "€630.00", "€24.00", "€27,480.00", "10%", "€1,639.09", "5%"], [a for q, a in D]
# exam-style
e1b, e1o = 37 * F("15.60"), 7 * F("15.60") * F(3, 2); e1g = e1b + e1o; e1t = tax(e1g, 76); e1n = e1g - e1t - F("18.35") - F("29.64")
assert (e1b, e1o, e1g, e1t, e1n) == (F("577.20"), F("163.80"), 741, F("72.20"), F("620.81"))
e2 = grow(12000, F("2.5"), F("2.5"), 4); assert e2[1:] == [12300, F("12607.50"), F("13111.80")]
y1 = 4500 * F("1.06") - 1500; y2 = y1 * F("1.06") - 1500; y3 = y2 * F("1.06")
assert (y1, y2, cent(y3)) == (3270, F("1966.20"), F("2084.17"))
e4t = tax(71000, 4000, 44000); e4p = F(71000) * 4 / 100; e4n = 71000 - e4t - 2300 - e4p
assert (e4t, e4p, e4n, round(float((71000 - e4n) / 710), 1)) == (15600, 2840, 50260, 29.2)
E = [("<b>The payslip.</b> Eoin earns €15.60 an hour for a basic 37-hour week and time-and-a-half for overtime. One week he works 44 hours. (a) Find his gross pay. (b) His weekly tax credit is €76 and tax is 20%. Find his tax. (c) He also pays USC of €18.35 and PRSI of €29.64. Find his net pay.",
      f"(a) {m(e1b)} + 7 × €23.40 = <b>{m(e1g)}</b> (b) €148.20 − €76 = <b>{m(e1t)}</b> (c) <b>{m(e1n)}</b>"),
     ("<b>Nóra's savings.</b> Nóra invests €12,000. The account pays 2.5% compound interest in years 1 and 2 and 4% in year 3. (a) Find the value at the end of each year. (b) Find the total interest. (c) Is that more or less than 9% of €12,000? Why?",
      f"(a) <b>{m(e2[1])}</b>, <b>{m(e2[2])}</b>, <b>{m(e2[3])}</b> (b) <b>{m(e2[3] - 12000)}</b> (c) more than €1,080: interest is earned on interest"),
     ("<b>The car loan.</b> Aaron borrows €4,500 at 6% compound interest a year. He repays €1,500 at the end of year 1 and €1,500 at the end of year 2. How much does he owe at the end of year 3, to the nearest cent?",
      f"Y1 €4,770 − €1,500 = {m(y1)}; Y2 €3,466.20 − €1,500 = {m(y2)}; Y3 × 1.06 = <b>{m(cent(y3))}</b>"),
     ("<i>Higher Level:</i> Ronan earns €71,000 a year. Cut-off point €44,000, rates 20% and 40%, tax credits €4,000. He pays USC of €2,300 and PRSI at 4% of his gross income. (a) Find his income tax. (b) Find his net income. (c) What percentage of his gross income is taken off altogether?",
      f"(a) €8,800 + €10,800 − €4,000 = <b>{m(e4t)}</b> (b) PRSI {m(e4p)}; net <b>{m(e4n)}</b> (c) <b>29.2%</b>")]

def qs(items): return "".join(f"<li>{q} <span class='line'></span></li>" for q, a in items)
SHEET_STYLE = re.search(r'sheet = f"""<!doctype.*?<style>(.*?)</style>', open(os.path.join(SRC, "build_money1_pdfs.py"), encoding="utf-8").read(), re.S).group(1).replace("{LO}", LO).replace("{{", "{").replace("}}", "}")
assert "@bottom-left" in SHEET_STYLE and "{{" not in SHEET_STYLE

sheet = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Money: income tax, net pay and compound interest: rules and practice | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{SHEET_STYLE}</style></head><body>
<div class="page tight">
  <div class="band"><div><div class="k">Junior Cycle Maths · Free revision sheet</div><h1>Money: income tax, net pay &amp; compound interest</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2018 specification): {LO}. Play the game: <b>leim.ie/payslip-puzzle.html</b></p>
  <div class="two">
   <div><h2>1. Gross pay</h2>
    <p><b>Gross pay</b> = pay before anything is taken off. Hours × rate: 38 × €15.50 = <b>€589</b>.</p>
    <p><b>Overtime:</b> time-and-a-half = 1.5 × the normal rate; double time = 2 × the normal rate. Only the extra hours get it. 52 weeks or 12 months in a year.</p>
    <h2>2. Income tax (standard rate)</h2>
    <table><tbody>
     <tr><td>Gross tax</td><td>20% of €40,000 = <b>€8,000</b></td></tr>
     <tr><td>− tax credit</td><td>€8,000 − €3,750 = <b>€4,250</b> tax payable</td></tr>
     <tr><td>Net income</td><td>€40,000 − €4,250 = <b>€35,750</b></td></tr></tbody></table>
    <p>The <b>tax credit</b> comes off the <b>tax</b>, never off the income. Backwards: (tax + credit) × 5 = gross income.</p>
    <h2>3. Two rates <span class="hl">Higher Level</span></h2>
    <p>Up to the <b>standard rate cut-off point</b>: 20%. Above it: 40%. €52,000 with a €44,000 cut-off: €8,800 + 40% of €8,000 (€3,200) = €12,000 gross tax, then take away the credits.</p>
    <h2>4. Net pay</h2>
    <p><b>Net pay</b> = gross − income tax − USC − PRSI − pension (and any other deductions). Higher Level may give a deduction as a %: PRSI at 4% of €750 = €30.</p></div>
   <div><h2>5. Compound interest</h2>
    <p>Each year's interest is worked out on the amount at the <b>start of that year</b>.</p>
    <table><thead><tr><th>Year</th><th>Start</th><th>Interest 5%</th><th>End</th></tr></thead><tbody>
     <tr><td>1</td><td>€4,000</td><td>€200</td><td>€4,200</td></tr>
     <tr><td>2</td><td>€4,200</td><td>€210</td><td>€4,410</td></tr>
     <tr><td>3</td><td>€4,410</td><td>€220.50</td><td><b>€4,630.50</b></td></tr></tbody></table>
    <p><b>Quick way:</b> 5% a year → × 1.05 each year: €4,000 × 1.05³ = €4,630.50. Interest = €4,630.50 − €4,000 = <b>€630.50</b>.</p>
    <p><b>Different rates:</b> × 1.03 × 1.04 × 1.05. <b>Loans:</b> add the year's interest, THEN take off the repayment.</p>
    <h2>6. Working backwards <span class="hl">Higher Level</span></h2>
    <p>Worth €4,410 after 2 years at 5%: €4,410 ÷ 1.05² = <b>€4,000</b>. Rate from €5,000 → €6,050 in 2 years: 6,050 ÷ 5,000 = 1.21, √1.21 = 1.1, so <b>10%</b>.</p>
    <div class="note"><b>Classic mistakes:</b> credit taken off the income · 1.5 used for 5% · interest on the first amount every year · interest given when the value is asked · taking 5% off twice to go back.</div></div>
  </div>
  <div class="tip"><b>Exam tip:</b> label each line (gross tax, tax payable, deductions, net pay; end of year 1, 2, 3). Each step earns marks. Give money to the nearest cent.</div>
</div>

<div class="page p2">
  <div class="band"><div><div class="k">Practice · 34 questions</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Gross pay and payslips</h2><ol class="q">{qs(A)}</ol>
  <h2>B. Income tax</h2><ol class="q" start="7">{qs(B)}</ol>
  <h2>C. Compound interest</h2><ol class="q" start="15">{qs(Cq)}</ol>
  <h2>D. Putting it together</h2><ol class="q" start="23">{qs(D)}</ol>
  <p class="small" style="margin-top:4px">Questions 31–34 are on the next page.</p>
</div>

<div class="page">
  <div class="band"><div><div class="k">Exam-style · then check</div><h1>Exam corner + answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>E. Exam-style questions (show your work)</h2>
  <ol class="q e3" start="31">{"".join(f"<li>{q}<span class='long'></span><span class='long'></span></li>" for q,a in E)}</ol>
  <h2 style="margin-top:10px">Answers</h2>
  <table class="ans"><tbody>
   <tr><td><b>A</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(A,1))}</td></tr>
   <tr><td><b>B</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(B,7))}</td></tr>
   <tr><td><b>C</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(Cq,15))}</td></tr>
   <tr><td><b>D</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(D,23))}</td></tr>
   <tr><td><b>E</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(E,31))}</td></tr>
  </tbody></table>
  <div class="note"><b>Got one wrong?</b> Check: did you take the tax credit off the TAX (not the income)? Did you take off EVERY deduction for net pay? For compound interest, did you work out each year's interest on the NEW amount, and did you give the value or the interest, whichever was asked? Then play <b>Payslip Puzzle</b> at leim.ie/payslip-puzzle.html: the "Go back over these" list at the end shows the rule for each mistake.</div>
  <p class="small">All questions written by Léim. Léim is independent and not connected with the State Examinations Commission or the NCCA. Tax rates, credits and cut-off points here are examples; the exam always gives you the figures to use.</p>
</div>
</body></html>"""

# ---------- teacher pack ----------
# Payslip Swap: each fact is on exactly ONE card; both students work out every blank
L_rate, L_basic, L_ot, L_cred, L_usc, L_prsi = F("15.20"), 39, 5, 75, F("17.80"), F("28.27")
l_b = L_basic * L_rate; l_o = L_ot * L_rate * F(3, 2); l_g = l_b + l_o; l_gt = l_g / 5; l_tp = l_gt - L_cred; l_n = l_g - l_tp - L_usc - L_prsi
assert (l_b, l_o, l_g, l_gt, l_tp, l_n) == (F("592.80"), 114, F("706.80"), F("141.36"), F("66.36"), F("594.37"))
s_am = grow(6000, 3, 5, 2); assert s_am[1:] == [6180, 6489, F("6618.78")]
LR = [("Hourly rate", m(L_rate), "A"), ("Basic hours", str(L_basic), "B"), ("Overtime hours", str(L_ot), "A"),
      ("Overtime rate", "time-and-a-half", "B"), ("Gross pay", "", None), ("Gross tax (20%)", "", None),
      ("Weekly tax credit", m(L_cred), "A"), ("Tax payable", "", None), ("USC", m(L_usc), "B"), ("PRSI", m(L_prsi), "A"), ("Net pay", "", None)]
SR = [("Amount invested", m(6000), "B"), ("Rate in year 1", "3%", "A"), ("Rate in year 2", "5%", "B"), ("Rate in year 3", "2%", "A"),
      ("Value at end of year 1", "", None), ("Value at end of year 2", "", None), ("Value at end of year 3", "", None), ("Total interest", "", None)]
for rows in (LR, SR):
    assert all(w in ("A", "B") for _, v, w in rows if v) and any(w == "A" for *_, w in rows) and any(w == "B" for *_, w in rows)
def swap_card(who):
    def tab(title, rows):
        return f'<table class="ss"><thead><tr><th colspan="2">{title}</th></tr></thead><tbody>' + "".join(
            f"<tr><td>{k}</td><td><b>{v if w == who else ''}</b></td></tr>" for k, v, w in rows) + "</tbody></table>"
    return f'<div class="idc"><h3>Student {who} · Payslip Swap</h3><div class="two">{tab("Liam’s payslip (one week)", LR)}{tab("Emma’s savings (compound interest)", SR)}</div></div>'

# Payday mingle: 12 question/answer pairs = 24 cards
MATCH = [("40 hours at €13.50", m(40 * F("13.50"))), ("6 h overtime, time-and-a-half, €14/h", m(6 * 14 * F(3, 2))),
         ("€650 a week. A year?", m(650 * 52)), ("€36,000 a year. A month?", m(3000)),
         ("Gross tax: 20% of €31,000", m(F(31000) / 5)), ("Gross tax €7,400, credit €3,500. Tax?", m(3900)),
         ("€25,000, credit €3,000, tax 20%. Net?", m(25000 - tax(25000, 3000))), ("Gross €900, deductions €215. Net?", m(685)),
         ("€1,000 at 10% for 2 years. Value?", m(grow(1000, 10, 10)[-1])), ("€5,000 at 4% for 2 years. Interest?", m(grow(5000, 4, 4)[-1] - 5000)),
         ("3% a year: multiply by?", dec(F("1.03"))), ("Higher Level: 20% of €44,000 + 40% of €6,000", m(F(44000) / 5 + 6000 * F(2, 5)))]
ANS = [a for q, a in MATCH]
assert ANS == ["€540.00", "€126.00", "€33,800.00", "€3,000.00", "€6,200.00", "€3,900.00", "€23,000.00", "€685.00", "€1,210.00", "€408.00", "1.03", "€11,200.00"], ANS
assert len(set(ANS)) == 12
cards = [q for q, a in MATCH] + ANS
random.seed(19); match_print = cards[:]; random.shuffle(match_print)
match_html = "".join(f'<div class="c"><span class="tag">Card {i}</span><div class="fc{" sm" if len(x) > 10 else ""}">{x}</div></div>' for i, x in enumerate(match_print, 1))
match_key = " · ".join(f"{q} → <b>{a}</b>" for q, a in MATCH)

DOMS = [("35 h at €16", m(35 * 16)), ("€14/h, 3 h at double time", m(3 * 14 * 2)), ("€500 a week for 52 weeks", m(500 * 52)),
        ("€48,000 a year. A month?", m(4000)), ("20% of €38,000", m(F(38000) / 5)), ("Gross tax €9,000 − credit €3,800", m(5200)),
        ("€30,000, credit €3,500, 20%. Tax?", m(tax(30000, 3500))), ("€30,000, credit €3,500, 20%. Net?", m(30000 - tax(30000, 3500))),
        ("Tax €4,200 + credit €3,800 is 20% of?", m((4200 + 3800) * 5)), ("€760 − tax €62 − USC €18", m(760 - 62 - 18)),
        ("€2,000 at 5%: one year's interest", m(100)), ("€2,000 at 10% for 2 years", m(grow(2000, 10, 10)[-1])),
        ("€10,000 at 2% for 2 years: interest", m(grow(10000, 2, 2)[-1] - 10000)), ("€4,000 at 5% for 3 years", m(grow(4000, 5, 5, 5)[-1])),
        ("4.5% a year: multiply by?", dec(F("1.045"))), ("€1,000: 10% then 20%", m(grow(1000, 10, 20)[-1])),
        ("Owe €3,000 at 5%, repay €1,150 after a year", m(3000 * F("1.05") - 1150)), ("Higher Level: €1,210 after 2 years at 10%. Start?", m(F(1210) / F("1.21"))),
        ("Higher Level: €2,500 → €2,704 in 2 years. Rate?", pc(rate2(2500, 2704))), ("Higher Level: €50,000, cut-off €44,000. Taxed at 40%?", m(6000))]
DANS = [a for k, a in DOMS]
assert DANS == ["€560.00", "€84.00", "€26,000.00", "€4,000.00", "€7,600.00", "€5,200.00", "€2,500.00", "€27,500.00", "€40,000.00", "€680.00",
                "€100.00", "€2,420.00", "€404.00", "€4,630.50", "1.045", "€1,320.00", "€2,000.00", "€1,000.00", "4%", "€6,000.00"], DANS
assert len(set(DANS)) == 20
random.seed(1919); chain = DOMS[:]; random.shuffle(chain)
dom = [("START" if k == 0 else chain[k - 1][1], x[0]) for k, x in enumerate(chain)] + [(chain[-1][1], "FINISH")]
dom_print = dom[:]; random.shuffle(dom_print)
dom_html = "".join(f'<div class="dom"><div class="h l{" sm" if len(l) > 9 else ""}">{l}</div><div class="h r">{r}</div></div>' for l, r in dom_print)
chain_key = "".join(f"<li>{x} = <b>{a}</b></li>" for x, a in chain)

ERR = [("Income €40,000, tax credit €3,000, tax 20%. Tax payable?", "20% of €37,000 = €7,400", f"Took the credit off the income. €8,000 − €3,000 = <b>{m(tax(40000, 3000))}</b>"),
       ("€5,000 at 4% compound for 2 years. Value?", "€5,000 + 8% = €5,400", f"That's simple interest. €5,000 × 1.04² = <b>{m(grow(5000, 4, 4)[-1])}</b>"),
       ("4 hours overtime at time-and-a-half; normal rate €12.", "4 × €12 + 1.5 = €49.50", f"Rate × 1.5 = €18 an hour. 4 × €18 = <b>{m(4 * 18)}</b>"),
       ("€3,000 at 5% compound for 3 years. Value?", "€3,000 × 1.5³ = €10,125", f"5% is × 1.05. €3,000 × 1.05³ = <b>{m(cent(grow(3000, 5, 5, 5)[-1]))}</b>"),
       ("Gross €650; tax €55, USC €15, PRSI €26. Net?", "€650 − €55 = €595", f"Every deduction comes off. €650 − €96 = <b>{m(650 - 55 - 15 - 26)}</b>"),
       ("<i>Higher Level:</i> Worth €6,615 after 2 years at 5%. Invested?", "€6,615 − 10% = €5,953.50", f"Divide by 1.05². €6,615 ÷ 1.1025 = <b>{m(F(6615) / F('1.1025'))}</b>")]
assert F(6615) / F("1.1025") == 6000 and grow(3000, 5, 5, 5)[-1] == F("3472.875")
w1g = 39 * F("17.20") + 6 * F("17.20") * F(3, 2); w1t = tax(w1g, 77); w1n = w1g - w1t - F("21.40") - F("33.02")
assert (w1g, w1t, w1n) == (F("825.60"), F("88.12"), F("683.06"))
w2 = grow(7500, 3, 3, 3); assert (cent(w2[3]), cent(w2[3]) - 7500) == (F("8195.45"), F("695.45"))
w3t = tax(45000, 3950); w3n = 45000 - w3t - 1180 - 1800; assert (w3t, w3n) == (5050, 36970)
w4 = (2400 * F("1.08") - 1000) * F("1.08"); assert w4 == F("1719.36")
w5t = tax(66000, 4000, 44000); w5r = rate2(6250, 6760); assert (w5t, w5r) == (13600, 4)

PACK_STYLE = re.search(r'pack = f"""<!doctype.*?<style>(.*?)</style>', open(os.path.join(SRC, "build_money1_pdfs.py"), encoding="utf-8").read(), re.S).group(1).replace("{LO}", LO).replace("{{", "{").replace("}}", "}")
assert "Single-teacher licence" in PACK_STYLE and "{{" not in PACK_STYLE

pack = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Money: Income Tax, Net Pay and Compound Interest Teacher Pack | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{PACK_STYLE}
.ss td:nth-child(2){{width:34%}}.ss td,.ss th{{padding:0.5px 5px;font-size:8pt;line-height:1.12}}.fym .c{{height:13.6mm}}.big3{{font-size:20pt}}.p1 .proc td{{font-size:8.5pt;padding:2px 6px}}
</style></head><body>

<div class="page p1">
  <div class="band"><div><div class="k">Junior Cycle Maths · Teacher pack</div><h1>Money: tax, net pay &amp; interest</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2018 specification): {LO} (bills, VAT and profit come first, in Money 1; currency in the speed, distance and time topic)</p>
  <div class="two">
    <div><h3>Aims</h3><p>By the end of the lesson students can work out gross pay (including overtime), income tax at the standard rate with a tax credit, net pay after deductions of given amounts, and compound interest on savings and loans for up to 3 years. Higher Level: the standard rate cut-off point and higher rate, deductions given as a %, and working backwards.</p></div>
    <div><h3>In this pack</h3><p>p.1 Teacher notes · p.2 Payday mingle cards + Payslip Swap A/B cards · p.3 Money Dominoes (cut-up) · p.4 Wall poster · p.5 Worksheet: Error Hunt + exam-style questions · p.6 Answers. Level: 2nd year (Higher and Ordinary), or 3rd-year revision. Time: about 60 minutes. All questions are original.</p></div>
  </div>
  <h2 style="margin-top:8px">Procedure</h2>
  <table class="proc"><tbody>
    <tr><td>5 min</td><td><b>Lead-in: the two savers.</b> Board "€1,000 for 3 years at 10% a year. How much at the end?" Students answer alone, then compare. Collect answers (usually €1,300 and €1,331) without saying which is right.</td></tr>
    <tr><td>8 min</td><td><b>Guided discovery.</b> Pairs fill a year-by-year table both ways: 10% of the first €1,000 each year, or 10% of what's in the account. Why does one pull ahead? What one number do we multiply by each year? (1.1.) Then: is a tax credit taken off the income or the tax? Try both on €40,000 with a €3,000 credit.</td></tr>
    <tr><td>10 min</td><td><b>Payday mingle</b> (p.2, 24 cards = 12 question/answer pairs; one card each). Question card? Work it out and find the person with your answer. Answer card? Find your question. Pairs check each other's working.</td></tr>
    <tr><td>12 min</td><td><b>Payslip Swap</b> (p.2, pairs, don't show your card). Each fact is on only ONE card. Ask your partner for what you're missing ("What's the overtime rate?"), then both fill every blank. Feedback: compare net pay ({m(l_n)}) and Emma's total ({m(s_am[3])}).</td></tr>
    <tr><td>10 min</td><td><b>Money Dominoes</b> (p.3), groups of 3–4. Start with START, work out the clue, find the domino with that answer on its left, and build the chain to FINISH.</td></tr>
    <tr><td>12 min</td><td><b>Worksheet</b> (p.5). Error Hunt in pairs (find the mistake, name the rule, fix it), then the exam-style questions alone.</td></tr>
    <tr><td>3 min</td><td><b>Exit ticket.</b> €30,000 a year, credit €3,200, tax 20%: tax payable? €2,000 at 3% compound for 2 years: value? (€2,800; €2,121.80.) Homework: play <b>Payslip Puzzle</b> at leim.ie/payslip-puzzle.html and copy three lines from the "Go back over these" list.</td></tr>
  </tbody></table>
  <div class="note"><b>Payday key:</b> {match_key}.<br>
  <b>Errors to look for:</b> taking the tax credit off the income · adding the credit · paying overtime on all the hours · using 1.5 for 5% · simple interest instead of compound · giving the interest when the value is asked · taking the repayment off before adding the year's interest · going backwards by taking the % off. <b>Support:</b> give a blank year-by-year table (start · interest · end). <b>Fast finishers:</b> how many years at 10% until €1,000 doubles? (8 years: €2,143.59)</div>
  <p class="small"><b>Domino answer chain</b> (START → FINISH):</p>
  <ol class="small" style="columns:2;column-gap:12px;font-size:7pt;line-height:1.22;margin:0;padding-left:16px">{chain_key}</ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">Cut up the cards · one Payslip Swap card per student</div><h1>Payday + Payslip Swap</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:8.8pt;margin:0"><b>Payday mingle.</b> Cut out the 24 cards and give one to each student. Question card? Work it out, then find the person with your answer. Answer card? Find the question that gives your answer. (Fewer students? Take out whole pairs.)</p>
  <div class="fym">{match_html}</div>
  <p style="font-size:8.8pt;margin:3mm 0 0"><b>Payslip Swap.</b> Don't show your card. Each fact is on only one of the two cards: ask your partner for what you're missing, then fill in every blank on both. A calculator is fine for the savings.</p>
  {swap_card("A")}
  {swap_card("B")}
</div>

<div class="page">
  <div class="band"><div><div class="k">Groups of 3–4 · cut along the dashed lines</div><h1>Money Dominoes</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.4pt">Start with START. Work out the clue on the right, then find the domino with that answer on its left. Keep going until you reach FINISH.</p>
  <div class="doms">{dom_html}</div>
</div>

<div class="page">
  <div class="poster">
    <h1>Money: tax, pay &amp; interest</h1>
    <div class="big3"><div>20% − credit<span>income tax</span></div><div>gross − all<span>net pay</span></div><div>× 1.05³<span>3 years at 5%</span></div></div>
    <div class="ops">
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Gross pay</b>hours × rate<br>overtime: × 1.5 or × 2<br>× 52 weeks · × 12 months</div>
      <div style="background:var(--green-soft)"><b>Income tax</b>20% of €40,000 = €8,000<br>− credit €3,750<br>= €4,250 tax payable</div>
      <div style="background:var(--green-soft)"><b>Net pay</b>gross − tax − USC<br>− PRSI − pension<br>= take-home pay</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Compound</b>€4,000 → €4,200<br>→ €4,410 → €4,630.50<br>interest on the interest</div>
    </div>
    <p style="text-align:center;font-size:12pt;margin:0"><b>Higher Level:</b> 20% up to the cut-off point, 40% above it · backwards: ÷ 1.05²</p>
    <p style="text-align:center;font-size:10pt;color:var(--muted)">Léim · leim.ie · Play Payslip Puzzle: leim.ie/payslip-puzzle.html</p>
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
    <li>Niamh earns €17.20 an hour for a basic 39-hour week and time-and-a-half for overtime. One week she works 45 hours. Find (a) her gross pay, (b) her tax if the rate is 20% and her weekly tax credit is €77, (c) her net pay if she also pays USC of €21.40 and PRSI of €33.02.<span class="long"></span><span class="long"></span></li>
    <li>€7,500 is invested for 3 years at 3% compound interest a year. Find the value at the end of the 3 years, to the nearest cent, and the interest earned.<span class="long"></span></li>
    <li>Pádraig earns €45,000 a year. His tax credit is €3,950 and the standard rate is 20%. He also pays USC of €1,180 and PRSI of €1,800. Find (a) his income tax, (b) his net income.<span class="long"></span><span class="long"></span></li>
    <li>Sorcha borrows €2,400 at 8% compound interest a year. She repays €1,000 at the end of year 1. How much does she owe at the end of year 2?<span class="long"></span></li>
    <li><span class="hl">Higher Level</span> (a) Gross income €66,000, cut-off point €44,000, rates 20% and 40%, tax credits €4,000. Find the income tax. (b) €6,250 grows to €6,760 in 2 years at the same compound rate. Find the rate.<span class="long"></span></li>
  </ol>
</div>

<div class="page an">
  <div class="band"><div><div class="k">For the teacher</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>Payslip Swap</h2>
  <div class="two"><table><tbody>
   <tr><td>Gross pay</td><td>39 × €15.20 + 5 × €22.80 = <b>{m(l_g)}</b></td></tr><tr><td>Gross tax</td><td>20% = <b>{m(l_gt)}</b></td></tr>
   <tr><td>Tax payable</td><td>− €75 = <b>{m(l_tp)}</b></td></tr><tr><td>Net pay</td><td>− USC − PRSI = <b>{m(l_n)}</b></td></tr></tbody></table>
  <table><tbody>
   <tr><td>End of year 1</td><td>€6,000 × 1.03 = <b>{m(s_am[1])}</b></td></tr><tr><td>End of year 2</td><td>× 1.05 = <b>{m(s_am[2])}</b></td></tr>
   <tr><td>End of year 3</td><td>× 1.02 = <b>{m(s_am[3])}</b></td></tr><tr><td>Total interest</td><td><b>{m(s_am[3] - 6000)}</b></td></tr></tbody></table></div>
  <h2>A. Error Hunt</h2>
  <table><tbody>{"".join(f"<tr><td style='width:36%'><b>{q}</b> {w}</td><td>{r}</td></tr>" for q,w,r in ERR)}</tbody></table>
  <h2>B. Exam-style questions</h2>
  <ol class="q">
    <li>(a) €670.80 + 6 × €25.80 = <b>{m(w1g)}</b> (b) €165.12 − €77 = <b>{m(w1t)}</b> (c) <b>{m(w1n)}</b></li>
    <li>€7,725 → €7,956.75 → €8,195.4525 = <b>{m(cent(w2[3]))}</b>; interest <b>{m(cent(w2[3]) - 7500)}</b></li>
    <li>(a) €9,000 − €3,950 = <b>{m(w3t)}</b> (b) €45,000 − €5,050 − €1,180 − €1,800 = <b>{m(w3n)}</b></li>
    <li>€2,592 − €1,000 = €1,592; × 1.08 = <b>{m(w4)}</b></li>
    <li>(a) €8,800 + €8,800 − €4,000 = <b>{m(w5t)}</b> (b) 6,760 ÷ 6,250 = 1.0816; √1.0816 = 1.04, so <b>{pc(w5r)}</b></li>
  </ol>
  <h2>Marking tip</h2>
  <p>Give credit for each step, as the exam does: gross pay, gross tax, tax payable and net pay each earn marks even if a later line slips; for compound interest, each year's value earns marks. For "explain" parts insist on a sentence with numbers in it.</p>
</div>
</body></html>"""

cover = """<!doctype html><html><head><meta charset="utf-8"><style>
body{margin:0;width:1200px;height:1200px;background:#1B2430;font-family:Inter,sans-serif;color:#fff;display:flex;flex-direction:column;justify-content:space-between;padding:90px;box-sizing:border-box}
.k{display:inline-block;background:#2E7D57;border-radius:99px;padding:12px 26px;font-weight:700;font-size:28px;letter-spacing:.06em;text-transform:uppercase}
h1{font-size:88px;font-weight:800;line-height:1.14;letter-spacing:-.03em;margin:40px 0 0}
h1 span{background:#F6CF5A;color:#1B2430;padding:0 14px;box-decoration-break:clone;-webkit-box-decoration-break:clone}
.sub{font-size:38px;color:#C9D1DA;margin-top:36px;line-height:1.35}
.em{font-size:50px;margin-top:30px;font-weight:800;letter-spacing:.01em;color:#F6CF5A}
.foot{display:flex;justify-content:space-between;align-items:center;font-size:34px;font-weight:700}
.price{background:#F6CF5A;color:#1B2430;border-radius:16px;padding:14px 28px}
</style></head><body>
<div><span class="k">Junior Cycle Maths · Teacher pack</span>
<h1><span>Income Tax, Net Pay</span><br><span>&amp; Compound Interest</span></h1>
<div class="sub">Payday mingle · Payslip Swap A/B<br>Money Dominoes · Poster · Worksheet + answers</div>
<div class="em">€4,000 × 1.05³ = €4,630.50</div></div>
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
    pdf("teacher-pack", os.path.join(OUT, "Money-Income-Tax-Net-Pay-Compound-Interest-Teacher-Pack-Leim.pdf"))
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--hide-scrollbars", "--window-size=1200,1200",
                    f"--screenshot={os.path.join(OUT, f'{SLUG}-cover.png')}", f"{SLUG}-cover.html"], cwd=SRC, check=True, capture_output=True)
    print("domino chain:", [(x, a) for x, a in chain])
