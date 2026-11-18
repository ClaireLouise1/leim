#!/usr/bin/env python3
"""Money 1: bills, VAT, profit & loss (JC Maths topic 18): free sheet + teacher pack + Payhip cover.
Run from the repo root: python3 src/build_money1_pdfs.py OUTDIR
Writes src/money-bills-vat-profit-loss-*.html; PDFs/cover PNG go to OUTDIR (free sheet also to printables/).
Every answer is computed with Python's Fraction and asserted."""
import os, sys, random, subprocess, re
from fractions import Fraction as F
from math import floor
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC)
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/money1"; os.makedirs(OUT, exist_ok=True)
SLUG = "money-bills-vat-profit-loss"
LO = "N.2c, U.6"

def dec(x):
    x = F(x); k = 0
    while (x * 10 ** k).denominator != 1:
        k += 1; assert k < 8, x
    n = x * 10 ** k; s = str(abs(n.numerator)).rjust(k + 1, "0")
    s = s[:len(s) - k] + ("." + s[len(s) - k:] if k else "")
    return s.rstrip("0").rstrip(".") if k else s
def pc(x): return dec(F(x)) + "%"
def cent(x): x = F(x); return F(floor(x * 100 + F(1, 2)), 100)     # nearest cent, half up
def m(x):
    x = F(x); assert (x * 100).denominator == 1, x; c = int(x * 100)
    return "€{:,}.{:02d}".format(c // 100, c % 100)
def c_(x): x = F(x); assert x < 1 and (x * 100).denominator == 1; return f"{int(x * 100)}c"
def vat(p, r): return F(p) * F(r) / 100
def with_vat(p, r): return F(p) * (1 + F(r) / 100)
def before_vat(t, r): return F(t) / (1 + F(r) / 100)
def pct_on_cost(cost, sell): return (F(sell) - F(cost)) / F(cost) * 100
def margin(cost, sell): return (F(sell) - F(cost)) / F(sell) * 100
def per100(price, size): return F(price) / F(size) * 100
assert m(F(1234, 1)) == "€1,234.00" and cent(F(16875, 1000)) == F(1688, 100) and before_vat(615, 23) == 500

# ---------- free sheet ----------
rc = [(3, F("1.45")), (2, F("2.80")), (1, F("4.99"))]; rtot = sum(q * p for q, p in rc)
mt = (23415, 24015, F("0.28"), F("19.50")); mbill = (mt[1] - mt[0]) * mt[2] + mt[3]
A = [("Receipt: 3 × €1.45, 2 × €2.80 and 1 × €4.99. What is the total?", m(rtot)),
     ("You pay for the shopping in question 1 with a €20 note. How much change do you get?", m(20 - rtot)),
     ("Electricity: previous reading 23 415, present reading 24 015. Units cost 28c and the standing charge is €19.50. Find the bill before VAT.", m(mbill)),
     ("Add VAT at 9% to the bill in question 3. Give the total to the nearest cent.", m(cent(with_vat(mbill, 9)))),
     ("A phone plan costs €20 a month and includes 200 minutes. Extra minutes cost 12c each. Ciarán uses 265 minutes. Find his bill.", m(20 + (265 - 200) * F("0.12"))),
     ("A plumber charges a call-out charge of €70 plus €48 an hour. The job takes 2.5 hours. Find the bill.", m(70 + F("2.5") * 48))]
assert [a for q, a in A] == ["€14.94", "€5.06", "€187.50", "€204.38", "€27.80", "€190.00"], [a for q, a in A]
B = [("A bike costs €80 before VAT. Find the price including VAT at 23%.", m(with_vat(80, 23))),
     ("Find the VAT at 13.5% on a hotel bill of €250.", m(vat(250, F("13.5")))),
     ("A TV costs €615 including VAT at 23%. Find the price before VAT.", m(before_vat(615, 23))),
     ("A meal costs €218 including VAT at 9%. How much of that is VAT?", m(218 - before_vat(218, 9))),
     ("A €90 jacket is reduced by 20%. Find the sale price.", m(F(90) * F(80, 100))),
     ("A lamp costs €45 after 25% off. What was the price before the sale?", m(F(45) / F(75, 100))),
     ("What number do you multiply by to add VAT at 13.5%?", dec(1 + F("13.5") / 100)),
     ("A €400 TV has VAT at 23% added, then 10% is taken off the total in a sale. Find the sale price.", m(with_vat(400, 23) * F(9, 10)))]
assert [a for q, a in B] == ["€98.40", "€33.75", "€500.00", "€18.00", "€72.00", "€60.00", "1.135", "€442.80"], [a for q, a in B]
Cq = [("A shop buys a hurley for €35 and sells it for €49. Find the profit.", m(49 - 35)),
      ("Bought for €40, sold for €50. Find the % profit on the cost price.", pc(pct_on_cost(40, 50))),
      ("Bought for €80, sold for €68. Find the % loss on the cost price.", pc(-pct_on_cost(80, 68))),
      ("A phone costs a shop €120. It is sold at a profit of 30% on the cost price. Find the selling price.", m(F(120) * F(130, 100))),
      ("A car cost €2,500 and is sold at a loss of 12%. Find the selling price.", m(F(2500) * F(88, 100))),
      ("A shop sells a jacket for €91, making 30% profit on the cost price. Find the cost price.", m(F(91) / F(130, 100))),
      ("<i>Higher Level:</i> Bought for €16, sold for €20. Find the mark-up.", pc(pct_on_cost(16, 20))),
      ("<i>Higher Level:</i> Bought for €16, sold for €20. Find the margin.", pc(margin(16, 20)))]
assert [a for q, a in Cq] == ["€14.00", "25%", "15%", "€156.00", "€2,200.00", "€70.00", "25%", "20%"], [a for q, a in Cq]
v24 = (per100(F("2.20"), 400), per100(F("5.20"), 1000)); assert v24 == (F("0.55"), F("0.52"))
v25 = (2 * 4, 3 * 4 * F(70, 100)); assert v25 == (8, F("8.40"))
D = [("A 750 g box of cereal costs €3.60. Find the cost of 100 g.", c_(per100(F("3.60"), 750))),
     ("Which is better value: 400 g for €2.20 or 1 kg for €5.20?", "1 kg (52c v 55c per 100 g)"),
     ("You need 3 notebooks at €4 each. Which is cheaper: \"3 for the price of 2\" or \"30% off each\"?", "3 for 2 (€8.00 v €8.40)"),
     ("A 500 ml bottle costs €1.10 and a 2 litre bottle costs €3.80. How much do you save buying one 2 litre bottle instead of four 500 ml bottles?", c_(4 * F("1.10") - F("3.80"))),
     ("Gym A: €30 a month. Gym B: €8 a month plus €3.50 a visit. Éabha goes 7 times a month. Which is cheaper, and by how much?", f"Gym A, by {m(8 + 7 * F('3.50') - 30)}"),
     ("A bus fare is €2.40 each way. A weekly ticket is €21. How much do you save over 5 school days (there and back) with the weekly ticket?", m(5 * 2 * F("2.40") - 21)),
     ("A pack of 6 yoghurts costs €4.50. One yoghurt on its own costs 80c. How much cheaper is each yoghurt in the pack?", c_(F("0.80") - F("4.50") / 6)),
     ("<i>Higher Level:</i> A shop buys a lamp for €54 and wants a margin of 40%. Find the selling price.", m(F(54) / F(60, 100)))]
assert [a for q, a in D] == ["48c", "1 kg (52c v 55c per 100 g)", "3 for 2 (€8.00 v €8.40)", "60c", "Gym A, by €2.50", "€3.00", "5c", "€90.00"], [a for q, a in D]
assert margin(54, 90) == 40
# exam-style
e1u = 61902 - 61052; e1s = e1u * F("0.33") + F("42.30"); e1v = cent(vat(e1s, 9)); e1t = e1s + e1v
assert (e1u, e1s, e1v, e1t) == (850, F("322.80"), F("29.05"), F("351.85"))
e2c = 50 * F("4.20"); e2sale = F(9) * F(70, 100); e2in = 35 * 9 + 15 * e2sale; e2p = e2in - e2c
assert (e2c, e2sale, e2in, e2p, pct_on_cost(e2c, e2in)) == (210, F("6.30"), F("409.50"), F("199.50"), 95)
e3b = before_vat(738, 23); e3w = cent(F(738) * F(77, 100)); assert (e3b, 738 - e3b, e3w) == (600, 138, F("568.26"))
e4m, e4g = pct_on_cost(6, 15), margin(6, 15); assert (e4m, e4g) == (150, 60)
assert F(25, 2) > F(36, 3)
E = [("<b>The electricity bill.</b> The meter read 61 052 at the start of the period and 61 902 at the end. Units cost 33c each and the standing charge is €42.30. VAT at 9% is added to the whole bill. (a) How many units were used? (b) Find the bill before VAT. (c) Find the total bill, to the nearest cent.",
      f"(a) <b>{e1u}</b> (b) {e1u} × €0.33 = €280.50, + €42.30 = <b>{m(e1s)}</b> (c) VAT {m(e1v)}, total <b>{m(e1t)}</b>"),
     ("<b>The candle stall.</b> Róisín buys 50 candles for €4.20 each. She sells 35 for €9 each and the rest at 30% off. (a) What did the candles cost her? (b) What is the sale price of one candle? (c) Find her profit and her % profit on the cost price.",
      f"(a) <b>{m(e2c)}</b> (b) <b>{m(e2sale)}</b> (c) income €315 + 15 × {m(e2sale)} = {m(e2in)}; profit <b>{m(e2p)}</b> = <b>95%</b>"),
     ("<b>The laptop.</b> A laptop costs €738 including VAT at 23%. (a) Find the price before VAT. (b) How much VAT is paid? (c) Orla says \"take 23% off €738\". What answer does she get, and why is she wrong?",
      f"(a) €738 ÷ 1.23 = <b>{m(e3b)}</b> (b) <b>{m(738 - e3b)}</b> (c) {m(e3w)}: 23% must be of the price BEFORE VAT, not of €738"),
     ("<b>Phone cases.</b> <i>Higher Level:</i> A shop buys phone cases for €6 and sells them for €15. (a) Find the mark-up and the margin. (b) Which offer is better value for a customer: \"2 for €25\" or \"3 for €36\"? Explain.",
      f"(a) mark-up <b>{pc(e4m)}</b>, margin <b>{pc(e4g)}</b> (b) €12.50 v <b>€12.00</b> each: <b>3 for €36</b>")]

def qs(items): return "".join(f"<li>{q} <span class='line'></span></li>" for q, a in items)

sheet = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Money: bills, VAT, profit and loss: rules and practice | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>@page{{@bottom-left{{content:"Léim · leim.ie · Free to print for home or class · JC Maths LOs (2018 spec): {LO}"}}}}
.tight{{font-size:10.6pt;line-height:1.45}}.tight td,.tight th{{padding:2px 6px}}.tight h2{{margin:8px 0 4px;font-size:13pt}}.tight .note,.tight .tip{{padding:6px 10px;margin:6px 0}}.tight p{{margin:3px 0}}
ol.q{{padding-left:30px}}ol.q li{{margin:7px 0}}
.ans td{{padding:3px 6px;font-size:8.9pt}}
.p2{{font-size:9.2pt;line-height:1.33}}.p2 ol.q li{{margin:3.5px 0}}.p2 h2{{margin:7px 0 3px;font-size:13pt}}.p2 .line{{min-width:70px}}
.hl{{display:inline-block;background:var(--night);color:#fff;font-size:7.5pt;font-weight:700;border-radius:99px;padding:1px 7px;vertical-align:middle}}
.e3 li{{font-size:9.6pt}}
</style></head><body>
<div class="page tight">
  <div class="band"><div><div class="k">Junior Cycle Maths · Free revision sheet</div><h1>Money: bills, VAT, profit &amp; loss</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2018 specification): {LO}. Play the game: <b>leim.ie/shop-keeper.html</b></p>
  <div class="two">
   <div><h2>1. Receipts and bills</h2>
    <p>Multiply each line first (3 × €1.25 = €3.75), then add the lines. <b>Change</b> = what you paid − the total. <b>Phone plans:</b> monthly charge + only the extras <b>over</b> the allowance. <b>Call-out charges:</b> fixed charge + hourly rate × hours.</p>
    <h2>2. Electricity and gas bills</h2>
    <table><tbody>
     <tr><td>Units used</td><td>present − previous = 24 015 − 23 415 = <b>600</b></td></tr>
     <tr><td>Cost of units</td><td>600 × €0.28 = €168.00</td></tr>
     <tr><td>+ standing charge</td><td>€168.00 + €19.50 = <b>€187.50</b></td></tr>
     <tr><td>+ VAT at 9%</td><td>€187.50 × 1.09 = €204.375 → <b>€204.38</b></td></tr></tbody></table>
    <p class="small">The standing charge is a fixed amount you pay whatever you use.</p>
    <h2>3. VAT</h2>
    <p>VAT is a tax added to the price. In Ireland the standard rate is <b>23%</b>; lower rates include <b>13.5%</b> and <b>9%</b>. The question always tells you the rate.</p>
    <p><b>Add VAT:</b> €400 × 1.23 = <b>€492</b>. <b>Before VAT:</b> €492 is 123%, so €492 ÷ 1.23 = <b>€400</b>. Never take 23% off €492 (that gives €378.84).</p>
    <h2>4. Discounts and sales</h2>
    <p>25% off €80 → €80 × 0.75 = <b>€60</b>. Price before the sale: €60 ÷ 0.75 = <b>€80</b>.</p></div>
   <div><h2>5. Profit and loss</h2>
    <p><b>Profit</b> = selling price − cost price (negative = a <b>loss</b>).</p>
    <p><b>% profit on the cost price</b> = profit ÷ <b>cost</b> × 100. Bought €40, sold €50: 10 ÷ 40 × 100 = <b>25%</b>.</p>
    <p><b>Selling price:</b> cost €40 at 25% profit → €40 × 1.25 = €50. <b>Back to the cost:</b> €50 ÷ 1.25 = €40.</p>
    <h2>6. Mark-up and margin <span class="hl">Higher Level</span></h2>
    <table><thead><tr><th></th><th>Profit as a % of…</th><th>€60 → €75</th></tr></thead><tbody>
     <tr><td><b>Mark-up</b></td><td>the <b>cost</b> price</td><td>15 ÷ 60 = <b>25%</b></td></tr>
     <tr><td><b>Margin</b></td><td>the <b>selling</b> price</td><td>15 ÷ 75 = <b>20%</b></td></tr></tbody></table>
    <p>The margin is always the smaller one. Margin 40% on a cost of €54: cost = 60% of the selling price, so €54 ÷ 0.6 = <b>€90</b>.</p>
    <h2>7. Value for money</h2>
    <p>Compare the price of the <b>same amount</b>: per 100 g, per litre or per item. 500 g for €3.40 = 68c per 100 g; 1.25 kg for €8 = 64c per 100 g, so the big bag is <b>better value</b>. "3 for the price of 2" = 33⅓% off. For plans, work out each total for <b>this</b> person.</p></div>
  </div>
  <div class="tip"><b>Exam tip:</b> write every line with € signs (units used, cost, standing charge, subtotal, VAT, total): each step earns marks. Give money to the nearest cent. Going backwards? <b>Divide</b> by 1.23, 0.75 or 1.25.</div>
</div>

<div class="page p2">
  <div class="band"><div><div class="k">Practice · 34 questions</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Bills and receipts</h2><ol class="q">{qs(A)}</ol>
  <h2>B. VAT and discounts</h2><ol class="q" start="7">{qs(B)}</ol>
  <h2>C. Profit and loss</h2><ol class="q" start="15">{qs(Cq)}</ol>
  <h2>D. Value for money</h2><ol class="q" start="23">{qs(D)}</ol>
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
  <div class="note"><b>Got one wrong?</b> Check: did you use the units USED (not the meter reading)? Did you add the standing charge? Going back to the price before VAT or before a sale, did you DIVIDE? For % profit, did you divide by the COST price? For best buys, did you compare the same amount of each? Then play <b>Shop Keeper</b> at leim.ie/shop-keeper.html: the "Go back over these" list at the end shows the rule for each mistake.</div>
  <p class="small">All questions written by Léim. Léim is independent and not connected with the State Examinations Commission or the NCCA. VAT rates are examples; the exam always tells you which rate to use.</p>
</div>
</body></html>"""

# ---------- teacher pack ----------
# Bill Swap: each fact is on exactly ONE card; both students work out every blank
ELEC = dict(prev=40236, pres=40986, unit=F("0.32"), sc=F("36.40"), rate=9)
e_units = ELEC["pres"] - ELEC["prev"]; e_cost = e_units * ELEC["unit"]; e_sub = e_cost + ELEC["sc"]; e_vat = cent(vat(e_sub, ELEC["rate"])); e_tot = e_sub + e_vat
assert (e_units, e_cost, e_sub, e_vat, e_tot) == (750, 240, F("276.40"), F("24.88"), F("301.28"))
PH = dict(fee=F("25"), inc=300, extra=F("0.15"), used=420, data_inc=20, data_used=23, gb=F("2.50"))
p_min = (PH["used"] - PH["inc"]) * PH["extra"]; p_dat = (PH["data_used"] - PH["data_inc"]) * PH["gb"]; p_tot = PH["fee"] + p_min + p_dat
assert (p_min, p_dat, p_tot) == (18, F("7.50"), F("50.50"))
ER = [("Previous reading", str(ELEC["prev"]), "A"), ("Present reading", str(ELEC["pres"]), "B"), ("Units used", "", None),
      ("Price per unit", "32c", "A"), ("Cost of units", "", None), ("Standing charge", m(ELEC["sc"]), "B"),
      ("Bill before VAT", "", None), ("VAT rate", "9%", "A"), ("VAT (nearest cent)", "", None), ("Total", "", None)]
PR = [("Monthly charge", m(PH["fee"]), "B"), ("Minutes included", str(PH["inc"]), "A"), ("Minutes used", str(PH["used"]), "B"),
      ("Price of an extra minute", "15c", "A"), ("Cost of extra minutes", "", None), ("Data included", f"{PH['data_inc']} GB", "B"),
      ("Data used", f"{PH['data_used']} GB", "A"), ("Price of an extra GB", m(PH["gb"]), "B"), ("Cost of extra data", "", None), ("Total bill", "", None)]
for rows in (ER, PR):
    assert all(w in ("A", "B") for _, v, w in rows if v) and any(w == "A" for *_, w in rows) and any(w == "B" for *_, w in rows)
def bill_card(who):
    def tab(title, rows):
        return f'<table class="ss"><thead><tr><th colspan="2">{title}</th></tr></thead><tbody>' + "".join(
            f"<tr><td>{k}</td><td><b>{v if w == who else ''}</b></td></tr>" for k, v, w in rows) + "</tbody></table>"
    return f'<div class="idc"><h3>Student {who} · Bill Swap</h3><div class="two">{tab("The Kellys’ electricity bill", ER)}{tab("Saoirse’s phone bill", PR)}</div></div>'

# Market Day mingle: 12 question/answer pairs = 24 cards
MATCH = [("€50 + VAT at 23%", m(with_vat(50, 23))), ("€246 incl. 23% VAT. Before VAT?", m(before_vat(246, 23))),
         ("25% off €36", m(F(36) * F(3, 4))), ("Bought €20, sold €26. % profit?", pc(pct_on_cost(20, 26))),
         ("Cost €40, sold at 15% profit", m(F(40) * F("1.15"))), ("Bought €50, sold €45. % loss?", pc(-pct_on_cost(50, 45))),
         ("Units: 12 450 → 12 850", "400 units"), ("400 units at 30c", m(400 * F("0.3"))),
         ("500 g for €2.10. Per 100 g?", c_(per100(F("2.10"), 500))), ("3 for 2, €7 each. Cost of 3?", m(14)),
         ("Higher Level: €40 → €50. Margin?", pc(margin(40, 50))), ("9% VAT = €9. Price before VAT?", m(F(9) / F(9, 100)))]
ANS = [a for q, a in MATCH]
assert ANS == ["€61.50", "€200.00", "€27.00", "30%", "€46.00", "10%", "400 units", "€120.00", "42c", "€14.00", "20%", "€100.00"], ANS
assert len(set(ANS)) == 12
cards = [q for q, a in MATCH] + ANS
random.seed(18); match_print = cards[:]; random.shuffle(match_print)
match_html = "".join(f'<div class="c"><span class="tag">Card {i}</span><div class="fc{" sm" if len(x) > 10 else ""}">{x}</div></div>' for i, x in enumerate(match_print, 1))
match_key = " · ".join(f"{q} → <b>{a}</b>" for q, a in MATCH)

DOMS = [("€20 + VAT at 23%", m(with_vat(20, 23))), ("€100 + VAT at 13.5%", m(with_vat(100, F("13.5")))),
        ("€300 + VAT at 9%", m(with_vat(300, 9))), ("€123 incl. 23% VAT. Before VAT?", m(before_vat(123, 23))),
        ("€218 incl. 9% VAT. The VAT?", m(218 - before_vat(218, 9))), ("10% off €70", m(63)),
        ("€30 after 25% off. Before?", m(F(30) / F(3, 4))), ("Bought €8, sold €10. Profit?", m(2)),
        ("Bought €8, sold €10. % profit?", pc(pct_on_cost(8, 10))), ("Bought €25, sold €20. % loss?", pc(-pct_on_cost(25, 20))),
        ("Cost €60 + 40% profit", m(F(60) * F("1.4"))), ("Sold €66 at 10% profit. Cost?", m(F(66) / F("1.1"))),
        ("Higher Level: €30 → €45. Mark-up?", pc(pct_on_cost(30, 45))), ("Higher Level: €35 → €50. Margin?", pc(margin(35, 50))),
        ("250 units at 36c", m(250 * F("0.36"))), ("Units: 5 100 → 5 350", "250 units"),
        ("2 kg for €6. Per 100 g?", c_(per100(6, 2000))), ("6 cans for €4.20. One can?", c_(F("4.20") / 6)),
        ("€15 a month + 40 extra minutes at 10c", m(15 + 40 * F("0.1"))), ("Call-out €50 + 2 hours at €35", m(50 + 2 * 35))]
DANS = [a for k, a in DOMS]
assert DANS == ["€24.60", "€113.50", "€327.00", "€100.00", "€18.00", "€63.00", "€40.00", "€2.00", "25%", "20%", "€84.00", "€60.00",
                "50%", "30%", "€90.00", "250 units", "30c", "70c", "€19.00", "€120.00"], DANS
assert len(set(DANS)) == 20
random.seed(1818); chain = DOMS[:]; random.shuffle(chain)
dom = [("START" if k == 0 else chain[k - 1][1], x[0]) for k, x in enumerate(chain)] + [(chain[-1][1], "FINISH")]
dom_print = dom[:]; random.shuffle(dom_print)
dom_html = "".join(f'<div class="dom"><div class="h l{" sm" if len(l) > 9 else ""}">{l}</div><div class="h r">{r}</div></div>' for l, r in dom_print)
chain_key = "".join(f"<li>{x} = <b>{a}</b></li>" for x, a in chain)

ERR = [("Price before VAT if €369 includes VAT at 23%", "€369 − 23% = €284.13", f"Took 23% of the wrong price. €369 ÷ 1.23 = <b>{m(before_vat(369, 23))}</b>"),
       ("Bought €40, sold €50. % profit on the cost?", "10 ÷ 50 × 100 = 20%", f"Divided by the SELLING price. 10 ÷ 40 × 100 = <b>{pc(pct_on_cost(40, 50))}</b>"),
       ("Readings 8 120 → 8 520, 30c a unit. Cost of units?", "8 520 × €0.30 = €2,556", f"Used the reading, not the units used (400). 400 × €0.30 = <b>{m(400 * F('0.3'))}</b>"),
       ("Plan €20 + 10c per minute over 100. Used 150 minutes.", "€20 + 150 × €0.10 = €35", f"Only minutes OVER 100 count. €20 + 50 × €0.10 = <b>{m(20 + 50 * F('0.1'))}</b>"),
       ("€48 after 20% off. Price before the sale?", "€48 + 20% = €57.60", f"Added 20% of the new price. €48 ÷ 0.8 = <b>{m(F(48) / F('0.8'))}</b>"),
       ("Which is better: 300 g for €1.50 or 500 g for €2.40?", "300 g: it's cheaper", f"Compared prices, not amounts. Per 100 g: 50c v 48c, so <b>500 g</b>")]
assert before_vat(369, 23) == 300 and F(150, 3) == 50 and F(240, 5) == 48
w1u = 37945 - 37145; w1c = w1u * F("0.31"); w1s = w1c + F("28.60"); w1v = cent(vat(w1s, 9)); w1t = w1s + w1v
assert (w1u, w1c, w1s, w1v, w1t) == (800, 248, F("276.60"), F("24.89"), F("301.49"))
w2 = with_vat(F(1450), F("13.5")); assert w2 == F("1645.75")
w3c = 24 * F("12.50"); w3in = 20 * 22 + 4 * 22 * F("0.5"); w3p = w3in - w3c
assert (w3c, w3in, w3p, pct_on_cost(w3c, w3in)) == (300, 484, 184, F(184, 3)) and round(float(F(184, 3)), 1) == 61.3
w4a, w4b = per100(F("4.80"), 750), per100(F("7.20"), 1200); assert (w4a, w4b) == (F("0.64"), F("0.6"))
w5m, w5g = pct_on_cost(F("0.90"), F("2.25")), margin(F("0.90"), F("2.25")); assert (w5m, w5g) == (150, 60)

pack = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Money: Bills, VAT, Profit and Loss Teacher Pack | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>
@page{{@bottom-left{{content:"Léim · leim.ie · Single-teacher licence · JC Maths LOs (2018 spec): {LO}";font-size:7pt}}}}
.proc td{{font-size:8.8pt;padding:3px 6px;line-height:1.3}}.proc td:first-child{{white-space:nowrap;font-weight:700;color:var(--green)}}
.p1 .note{{font-size:8.3pt;padding:6px 10px;line-height:1.33}}.p1 p{{font-size:9.4pt}}
.fym{{display:grid;grid-template-columns:repeat(4,1fr);margin-top:2mm}}
.fym .c{{border:2px dashed #9AA3AE;margin:-1px 0 0 -1px;height:13.6mm;position:relative;display:flex;align-items:center;justify-content:center;padding:3.6mm 2mm 0.6mm}}
.fym .fc{{font-size:15pt;font-weight:800;text-align:center}}.fym .fc.sm{{font-size:8.8pt;font-weight:700;line-height:1.2}}
.fym .tag{{position:absolute;top:1.2mm;left:3mm;font-size:6.5pt;color:var(--green);font-weight:800;text-transform:uppercase;letter-spacing:.04em}}
.idc{{border:2px dashed #9AA3AE;padding:2mm 4mm;margin-top:2mm;break-inside:avoid}}.idc h3{{margin:0 0 1.5mm;font-size:11pt}}.idc .two{{gap:5mm}}
.ss td,.ss th{{padding:1px 5px;font-size:8.4pt;line-height:1.25}}.ss td:nth-child(2){{width:38%}}
.doms{{display:grid;grid-template-columns:1fr 1fr;gap:2mm 6mm}}
.dom{{display:grid;grid-template-columns:1fr 1.7fr;border:2px dashed #9AA3AE;height:18mm}}
.dom .h{{display:flex;align-items:center;justify-content:center;text-align:center;padding:2mm;font-size:14pt;font-weight:800}}
.dom .l.sm{{font-size:11.5pt}}.dom .r{{font-size:10.4pt;font-weight:700}}
.dom .l{{background:var(--mist);border-right:2px solid var(--ink)}}
.poster{{height:255mm;border:6px solid var(--night);border-radius:18px;padding:10mm;display:flex;flex-direction:column;justify-content:space-between}}
.poster h1{{font-size:42pt;text-align:center}}.poster p{{font-size:14pt!important}}
.ops{{display:grid;grid-template-columns:1fr 1fr;gap:4mm}}.ops div{{border-radius:14px;padding:6mm 4mm;text-align:center;font-size:13pt;line-height:1.5}}.ops b{{display:block;font-size:21pt;font-weight:800;margin-bottom:1mm}}
.big3{{display:grid;grid-template-columns:1fr 1fr 1fr;text-align:center;font-size:28pt;font-weight:800}}.big3 span{{display:block;font-size:11pt;color:var(--muted);font-weight:700}}
.ws{{font-size:9.8pt;line-height:1.4}}.ws ol.q li{{margin:5px 0}}.ws .long{{height:20px}}
.eh td{{padding:4px 8px;font-size:9.3pt}}.eh td:first-child{{font-weight:700;width:34%}}.eh .gap{{display:block;border-bottom:1px solid #9AA3AE;height:15px}}
.hl{{display:inline-block;background:var(--night);color:#fff;font-size:7.5pt;font-weight:700;border-radius:99px;padding:1px 7px;vertical-align:middle}}
.an{{font-size:9.2pt;line-height:1.35}}.an td{{padding:2px 6px}}.an h2{{margin:7px 0 3px}}.an ol.q li{{margin:3px 0}}
</style></head><body>

<div class="page p1">
  <div class="band"><div><div class="k">Junior Cycle Maths · Teacher pack</div><h1>Money: bills, VAT, profit &amp; loss</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2018 specification): {LO} (income tax, net pay and compound interest come next, in Money 2; currency in the speed, distance and time topic)</p>
  <div class="two">
    <div><h3>Aims</h3><p>By the end of the lesson students can add up bills (meter readings, standing charges, phone plans, call-out charges), add VAT and find the price before VAT, find sale prices and prices before a sale, work out profit, loss and % profit on the cost price, and judge value for money. Higher Level: mark-up and margin.</p></div>
    <div><h3>In this pack</h3><p>p.1 Teacher notes · p.2 Market Day mingle cards + Bill Swap A/B cards · p.3 Money Dominoes (cut-up) · p.4 Wall poster · p.5 Worksheet: Error Hunt + exam-style questions · p.6 Answers. Level: 2nd year (Higher and Ordinary), or 3rd-year revision. Time: about 60 minutes. All questions are original.</p></div>
  </div>
  <h2 style="margin-top:8px">Procedure</h2>
  <table class="proc"><tbody>
    <tr><td>5 min</td><td><b>Lead-in: the VAT trap.</b> Board "A bike costs €615 with VAT at 23%. What was it before VAT?" Students write an answer alone, then compare. Collect both answers (usually €473.55 and €500) without saying which is right.</td></tr>
    <tr><td>8 min</td><td><b>Guided discovery.</b> Pairs add 23% to €100, €200, €500, then take 23% off each answer. Why don't they get back? (The second 23% is of a bigger number.) €123 is what % of €100? So how do we go back? (÷ 1.23.) Settle the lead-in: €500.</td></tr>
    <tr><td>10 min</td><td><b>Market Day mingle</b> (p.2, 24 cards = 12 question/answer pairs; one card each). Question card? Work it out and find the person with your answer. Answer card? Find your question. Pairs check each other's working.</td></tr>
    <tr><td>12 min</td><td><b>Bill Swap</b> (p.2, pairs, don't show your card). Each fact on the two bills is on only ONE card. Ask your partner for what you're missing ("What was the present reading?"), then both fill every blank. Feedback: compare totals (electricity {m(e_tot)}, phone {m(p_tot)}).</td></tr>
    <tr><td>10 min</td><td><b>Money Dominoes</b> (p.3), groups of 3–4. Start with START, work out the clue, find the domino with that answer on its left, and build the chain to FINISH.</td></tr>
    <tr><td>12 min</td><td><b>Worksheet</b> (p.5). Error Hunt in pairs (find the mistake, name the rule, fix it), then the exam-style questions alone.</td></tr>
    <tr><td>3 min</td><td><b>Exit ticket.</b> A coat costs €184.50 including VAT at 23%: price before VAT? Bought €60, sold €72: % profit on the cost? (€150; 20%.) Homework: play <b>Shop Keeper</b> at leim.ie/shop-keeper.html and copy three lines from the "Go back over these" list.</td></tr>
  </tbody></table>
  <div class="note"><b>Market Day key:</b> {match_key}.<br>
  <b>Errors to look for:</b> taking 23% off a VAT-inclusive price · adding the % back on to undo a sale · dividing by the selling price for % profit on the cost · using the meter reading instead of the units used · forgetting the standing charge · charging every minute, not just the extras · comparing pack prices instead of price per 100 g. <b>Support:</b> write "100% → 123%" over every VAT question. <b>Fast finishers:</b> a shop adds a 50% mark-up; what is its margin? (33⅓%)</div>
  <p class="small"><b>Domino answer chain</b> (START → FINISH):</p>
  <ol class="small" style="columns:2;column-gap:12px;font-size:7.5pt;line-height:1.3;margin:0;padding-left:16px">{chain_key}</ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">Cut up the cards · one Bill Swap card per student</div><h1>Market Day + Bill Swap</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:8.8pt;margin:0"><b>Market Day mingle.</b> Cut out the 24 cards and give one to each student. Question card? Work it out, then find the person with your answer. Answer card? Find the question that gives your answer. (Fewer students? Take out whole pairs.)</p>
  <div class="fym">{match_html}</div>
  <p style="font-size:8.8pt;margin:3mm 0 0"><b>Bill Swap.</b> Don't show your card. Each fact is on only one of the two cards: ask your partner for what you're missing, then fill in every blank on both bills. Give the VAT to the nearest cent. No calculators for the phone bill!</p>
  {bill_card("A")}
  {bill_card("B")}
</div>

<div class="page">
  <div class="band"><div><div class="k">Groups of 3–4 · cut along the dashed lines</div><h1>Money Dominoes</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.4pt">Start with START. Work out the clue on the right, then find the domino with that answer on its left. Keep going until you reach FINISH. No calculators!</p>
  <div class="doms">{dom_html}</div>
</div>

<div class="page">
  <div class="poster">
    <h1>Money: bills, VAT, profit &amp; loss</h1>
    <div class="big3"><div>× 1.23<span>add VAT at 23%</span></div><div>÷ 1.23<span>back to the price before VAT</span></div><div>÷ cost<span>% profit or loss</span></div></div>
    <div class="ops">
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Bills</b>Units = present − previous<br>units × price + standing charge<br>then add VAT</div>
      <div style="background:var(--green-soft)"><b>VAT &amp; sales</b>€400 × 1.23 = €492<br>€492 ÷ 1.23 = €400<br>25% off: × 0.75 · back: ÷ 0.75</div>
      <div style="background:var(--green-soft)"><b>Profit</b>selling − cost<br>% profit = profit ÷ COST × 100<br>€40 → €50 = 25%</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Best buy</b>same amount for each<br>500 g €3.40 → 68c / 100 g<br>1.25 kg €8 → 64c / 100 g ✓</div>
    </div>
    <p style="text-align:center;font-size:12pt;margin:0"><b>Higher Level:</b> mark-up = profit ÷ cost · margin = profit ÷ selling price</p>
    <p style="text-align:center;font-size:10pt;color:var(--muted)">Léim · leim.ie · Play Shop Keeper: leim.ie/shop-keeper.html</p>
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
    <li>A gas meter read 37 145 at the start of the period and 37 945 at the end. Units cost 31c and the standing charge is €28.60. VAT at 9% is added. Find (a) the units used, (b) the bill before VAT, (c) the total bill to the nearest cent.<span class="long"></span><span class="long"></span></li>
    <li>A builder quotes €1,450 before VAT for a new wall. VAT is charged at 13.5%. Find the total price.<span class="long"></span></li>
    <li>A club shop buys 24 jerseys for €12.50 each. It sells 20 for €22 each and the rest at half price. Find (a) the total cost, (b) the total income, (c) the profit as a percentage of the cost price, to one decimal place.<span class="long"></span><span class="long"></span></li>
    <li>Washing powder comes in a 750 g box for €4.80 or a 1.2 kg box for €7.20. Which is better value? Show your work.<span class="long"></span></li>
    <li><span class="hl">Higher Level</span> A café makes a smoothie for €0.90 and sells it for €2.25. Find the mark-up and the margin.<span class="long"></span></li>
  </ol>
</div>

<div class="page an">
  <div class="band"><div><div class="k">For the teacher</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>Bill Swap</h2>
  <div class="two"><table><tbody>
   <tr><td>Units used</td><td>{ELEC['pres']} − {ELEC['prev']} = <b>{e_units}</b></td></tr><tr><td>Cost of units</td><td>{e_units} × 32c = <b>{m(e_cost)}</b></td></tr>
   <tr><td>Bill before VAT</td><td>+ {m(ELEC['sc'])} = <b>{m(e_sub)}</b></td></tr><tr><td>VAT at 9%</td><td><b>{m(e_vat)}</b></td></tr><tr><td>Total</td><td><b>{m(e_tot)}</b></td></tr></tbody></table>
  <table><tbody>
   <tr><td>Extra minutes</td><td>{PH['used']} − {PH['inc']} = 120 × 15c = <b>{m(p_min)}</b></td></tr><tr><td>Extra data</td><td>{PH['data_used']} − {PH['data_inc']} = 3 GB × {m(PH['gb'])} = <b>{m(p_dat)}</b></td></tr>
   <tr><td>Total bill</td><td>{m(PH['fee'])} + {m(p_min)} + {m(p_dat)} = <b>{m(p_tot)}</b></td></tr></tbody></table></div>
  <h2>A. Error Hunt</h2>
  <table><tbody>{"".join(f"<tr><td style='width:36%'><b>{q}</b> {w}</td><td>{r}</td></tr>" for q,w,r in ERR)}</tbody></table>
  <h2>B. Exam-style questions</h2>
  <ol class="q">
    <li>(a) <b>{w1u}</b> (b) {w1u} × €0.31 = {m(w1c)}, + €28.60 = <b>{m(w1s)}</b> (c) VAT {m(w1v)}, total <b>{m(w1t)}</b></li>
    <li>€1,450 × 1.135 = <b>{m(w2)}</b></li>
    <li>(a) 24 × €12.50 = <b>{m(w3c)}</b> (b) 20 × €22 + 4 × €11 = <b>{m(w3in)}</b> (c) profit {m(w3p)}; 184 ÷ 300 × 100 = <b>61.3%</b></li>
    <li>Per 100 g: €4.80 ÷ 7.5 = {c_(w4a)}; €7.20 ÷ 12 = {c_(w4b)}. The <b>1.2 kg box</b> is better value.</li>
    <li>Profit €1.35. Mark-up 1.35 ÷ 0.90 = <b>{pc(w5m)}</b>; margin 1.35 ÷ 2.25 = <b>{pc(w5g)}</b></li>
  </ol>
  <h2>Marking tip</h2>
  <p>Give credit for each step, as the exam does: units used, cost of units, subtotal and VAT each earn marks even if a later line slips. For "which is better value?" insist on the price of the same amount for each AND a conclusion.</p>
</div>
</body></html>"""

cover = """<!doctype html><html><head><meta charset="utf-8"><style>
body{margin:0;width:1200px;height:1200px;background:#1B2430;font-family:Inter,sans-serif;color:#fff;display:flex;flex-direction:column;justify-content:space-between;padding:90px;box-sizing:border-box}
.k{display:inline-block;background:#2E7D57;border-radius:99px;padding:12px 26px;font-weight:700;font-size:28px;letter-spacing:.06em;text-transform:uppercase}
h1{font-size:100px;font-weight:800;line-height:1.12;letter-spacing:-.03em;margin:40px 0 0}
h1 span{background:#F6CF5A;color:#1B2430;padding:0 14px;box-decoration-break:clone;-webkit-box-decoration-break:clone}
.sub{font-size:38px;color:#C9D1DA;margin-top:36px;line-height:1.35}
.em{font-size:50px;margin-top:30px;font-weight:800;letter-spacing:.01em;color:#F6CF5A}
.foot{display:flex;justify-content:space-between;align-items:center;font-size:34px;font-weight:700}
.price{background:#F6CF5A;color:#1B2430;border-radius:16px;padding:14px 28px}
</style></head><body>
<div><span class="k">Junior Cycle Maths · Teacher pack</span>
<h1><span>Money: Bills, VAT,</span><br><span>Profit &amp; Loss</span></h1>
<div class="sub">Market Day mingle · Bill Swap A/B<br>Money Dominoes · Poster · Worksheet + answers</div>
<div class="em">€492 with VAT ÷ 1.23 = €400</div></div>
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
    pdf("teacher-pack", os.path.join(OUT, "Money-Bills-VAT-Profit-Loss-Teacher-Pack-Leim.pdf"))
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--hide-scrollbars", "--window-size=1200,1200",
                    f"--screenshot={os.path.join(OUT, f'{SLUG}-cover.png')}", f"{SLUG}-cover.html"], cwd=SRC, check=True, capture_output=True)
    print("domino chain:", [(x, a) for x, a in chain])
