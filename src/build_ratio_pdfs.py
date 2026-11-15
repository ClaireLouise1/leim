#!/usr/bin/env python3
"""Ratio & proportion (JC Maths topic 7): free sheet + teacher pack + Payhip cover.
Run from the repo root: python3 src/build_ratio_pdfs.py OUTDIR
Writes src/ratio-proportion-*.html; PDFs/cover PNG go to OUTDIR (free sheet also to printables/).
Every answer is computed with Python's Fraction and asserted."""
import os, sys, random, subprocess, re
from fractions import Fraction as F
from math import gcd
from functools import reduce
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC)
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/ratio"; os.makedirs(OUT, exist_ok=True)
SLUG = "ratio-proportion"
LO = "N.2b, N.3a"

def dec(x):
    x = F(x); k = 0
    while (x * 10 ** k).denominator != 1:
        k += 1; assert k < 8, x
    n = x * 10 ** k; s = str(abs(n.numerator)).rjust(k + 1, "0")
    s = s[:len(s) - k] + ("." + s[len(s) - k:] if k else "")
    return s.rstrip("0").rstrip(".") if k else s
def pc(x): return dec(F(x) * 100) + "%"
def m(x):
    x = F(x); assert (x * 100).denominator == 1, x; c = x * 100; return "€%d.%02d" % (c.numerator // 100, c.numerator % 100)
def fr(x): x = F(x); return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"
def rt(*xs):
    g = reduce(gcd, xs); return " : ".join(str(x // g) for x in xs)
def share(total, *r): return [F(total) * x / sum(r) for x in r]
def unitary(have_n, have_amt, want_n): return F(have_amt) / have_n * want_n
def mapkm(cm, sc): return F(cm) * sc / 100000
def mapcm(km, sc): return F(km) * 100000 / sc
assert rt(12, 18) == "2 : 3" and m(F(52, 10)) == "€5.20" and mapkm(6, 25000) == F(3, 2)

# ---------- free sheet ----------
A = [("Simplify 12 : 20", rt(12, 20)), ("Simplify 45 : 30", rt(45, 30)), ("Simplify 8 : 12 : 20", rt(8, 12, 20)),
     ("Write 40 cm : 2 m in its simplest form", rt(40, 200)), ("Write 750 g : 2 kg in its simplest form", rt(750, 2000)),
     ("Write 20 minutes : 1 hour in its simplest form", rt(20, 60))]
assert [a for q, a in A] == ["3 : 5", "3 : 2", "2 : 3 : 5", "1 : 5", "3 : 8", "1 : 3"], [a for q, a in A]
B = [("Share €40 in the ratio 3 : 5.", " and ".join(m(x) for x in share(40, 3, 5))),
     ("Share €90 in the ratio 4 : 5.", " and ".join(m(x) for x in share(90, 4, 5))),
     ("Share 72 sweets in the ratio 5 : 7.", " and ".join(dec(x) for x in share(72, 5, 7))),
     ("Share €120 in the ratio 1 : 2 : 3.", ", ".join(m(x) for x in share(120, 1, 2, 3))),
     ("Share €350 in the ratio 2 : 5.", " and ".join(m(x) for x in share(350, 2, 5))),
     ("Boys to girls in a club is 4 : 5. There are 28 boys. How many girls?", dec(F(28) / 4 * 5)),
     ("Cordial to water is 1 : 6. There is 900 ml of water. How much cordial?", dec(F(900) / 6) + " ml"),
     ("Money is shared in the ratio 3 : 8. One person gets €45 more than the other. How much was shared?", m(F(45) / (8 - 3) * 11))]
assert [a for q, a in B] == ["€15.00 and €25.00", "€40.00 and €50.00", "30 and 42", "€20.00, €40.00, €60.00", "€100.00 and €250.00", "35", "150 ml", "€99.00"], [a for q, a in B]
Cq = [("5 pens cost €3.25. How much do 8 pens cost?", m(unitary(5, F(325, 100), 8))),
      ("A recipe for 4 people uses 300 g of pasta. How much for 10 people?", dec(unitary(4, 300, 10)) + " g"),
      ("A recipe for 6 people uses 450 ml of milk. How much for 4 people?", dec(unitary(6, 450, 4)) + " ml"),
      ("3 kg of potatoes cost €7.50. How much do 5 kg cost?", m(unitary(3, F(75, 10), 5))),
      ("A map has a scale of 1 : 25 000. 8 cm on the map is how many km?", dec(mapkm(8, 25000)) + " km"),
      ("A map has a scale of 1 : 50 000. 4.5 km in real life is how many cm on the map?", dec(mapcm(F(45, 10), 50000)) + " cm"),
      ("Which is better value: 6 rolls for €2.70 or 8 rolls for €3.44?", "8 for €3.44 (43c each v 45c)"),
      ("A car uses 6 litres of petrol per 100 km. How much petrol for 250 km?", dec(unitary(100, 6, 250)) + " litres")]
assert F(270, 6) == 45 and F(344, 8) == 43
assert [a for q, a in Cq][:6] + [a for q, a in Cq][7:] == ["€5.20", "750 g", "300 ml", "€12.50", "2 km", "9 cm", "15 litres"], [a for q, a in Cq]
D = [("Class A: 18 of 24 students passed. Class B: 21 of 30 passed. Which class had MORE passes?", "Class B (21 > 18): absolute"),
     ("Which class did better RELATIVELY? Show the percentages.", f"Class A ({pc(F(18, 24))} v {pc(F(21, 30))})"),
     ("Bread went from €2.00 to €2.40. Milk went from €1.00 to €1.30. Which had the bigger ABSOLUTE increase?", "Bread (40c v 30c)"),
     ("Which had the bigger RELATIVE (percentage) increase?", f"Milk ({pc(F(30, 100))} v {pc(F(40, 200))})"),
     ("A town grew from 4,000 to 5,000 people. What is the absolute increase?", "1,000 people"),
     ("What is the relative (percentage) increase for the town?", pc(F(1000, 4000))),
     ("Red to blue is 2 : 3. What fraction of the counters are red?", fr(F(2, 5))),
     ("Fill the gap: 4 : 7 = 28 : ?", dec(F(28) / 4 * 7))]
assert [a for q, a in D][5:] == ["25%", "2/5", "49"] and pc(F(18, 24)) == "75%" and pc(F(21, 30)) == "70%"
# exam-style
e1 = share(630, 2, 3, 4); assert e1 == [140, 210, 280]
e2 = [unitary(8, x, 20) for x in (200, 120, 80)]; assert e2 == [500, 300, 200] and rt(200, 120, 80) == "5 : 3 : 2"
e3a, e3b = mapkm(9, 20000), mapcm(F(6, 10), 20000); assert (e3a, e3b) == (F(18, 10), 3)
e4a, e4b = F(600, 400) * 100, F(390, 250) * 100; assert (e4a, e4b) == (150, 156)
e4c, e4d = F(45, 60), F(52, 80); assert pc(e4c) == "75%" and pc(e4d) == "65%"
E = [("Ana, Barry and Cáit share €630 in the ratio 2 : 3 : 4. (a) How much does each get? (b) What fraction of the money does Cáit get?",
      f"(a) 9 parts, 1 part = €70: <b>€140, €210, €280</b> (b) <b>4/9</b>"),
     ("A recipe for 8 cookies uses 200 g of flour, 120 g of butter and 80 g of sugar. (a) How much of each is needed for 20 cookies? (b) Write flour : butter : sugar in its simplest form.",
      f"(a) ÷ 8 then × 20: <b>500 g, 300 g, 200 g</b> (b) <b>{rt(200, 120, 80)}</b>"),
     ("A map has a scale of 1 : 20 000. (a) A walk is 9 cm long on the map. How long is it in km? (b) A park is 600 m long. How long is it on the map?",
      f"(a) 9 × 20 000 = 180 000 cm = <b>{dec(e3a)} km</b> (b) 60 000 cm ÷ 20 000 = <b>{dec(e3b)} cm</b>"),
     ("(a) Coffee: 400 g for €6.00 or 250 g for €3.90. Which is better value? (b) Club X: 45 of its 60 members played in a match. Club Y: 52 of its 80 members played. Which club had the bigger proportion playing?",
      f"(a) Per 100 g: €1.50 v €1.56, so <b>400 g</b> (b) X {pc(e4c)} v Y {pc(e4d)}: <b>Club X</b>")]

def qs(items): return "".join(f"<li>{q} <span class='line'></span></li>" for q, a in items)
def bar(parts, names, w=11):
    rows = "".join(f'<div class="bm"><span>{n}</span>' + "".join('<i></i>' for _ in range(p)) + '</div>' for p, n in zip(parts, names))
    return f'<div class="bars">{rows}</div>'

sheet = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Ratio and proportion: rules and practice | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>@page{{@bottom-left{{content:"Léim · leim.ie · Free to print for home or class · JC Maths LOs (2018 spec): {LO}"}}}}
.tight{{font-size:10.1pt;line-height:1.42}}.tight td,.tight th{{padding:3px 6px}}.tight h2{{margin:9px 0 5px;font-size:13.5pt}}.tight .note,.tight .tip{{padding:6px 10px;margin:6px 0}}
ol.q{{padding-left:30px}}ol.q li{{margin:7px 0}}.cols{{columns:2;column-gap:12mm}}.cols li{{break-inside:avoid}}
.ans td{{padding:3px 6px;font-size:9.2pt}}
.p2{{font-size:9.5pt;line-height:1.36}}.p2 ol.q li{{margin:4px 0}}.p2 h2{{margin:8px 0 4px;font-size:13pt}}.p2 .line{{min-width:70px}}
.bars{{margin:4px 0 6px}}.bm{{display:flex;align-items:center;gap:0;margin:3px 0}}.bm span{{width:52px;font-weight:700;font-size:9.5pt}}
.bm i{{display:inline-block;width:30px;height:16px;border:1.5px solid var(--ink);margin-left:-1.5px;background:#F6CF5A}}.bm:nth-child(2) i{{background:#9BD3AE}}.bm:nth-child(3) i{{background:#A9C4E8}}
</style></head><body>
<div class="page tight">
  <div class="band"><div><div class="k">Junior Cycle Maths · Free revision sheet</div><h1>Ratio &amp; proportion</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2018 specification): {LO}. Play the game: <b>leim.ie/share-it-out.html</b></p>
  <div class="two">
   <div><h2>1. What a ratio means</h2>
    <p>"Girls to boys is 3 : 4" means 3 girls for every 4 boys. <b>Order matters</b>: boys to girls is 4 : 3. <b>Simplify</b> by dividing every number by the HCF: 12 : 18 = <b>2 : 3</b> (÷ 6). <b>Same units first:</b> 50 cm : 2 m = 50 : 200 = <b>1 : 4</b>. Equivalent ratios: multiply both by the same number (3 : 5 = 12 : 20). Adding the same number does NOT work.</p>
    <h2>2. Sharing in a ratio</h2>
    <p>Share €60 in the ratio 1 : 2 : 3. Add the parts: 1 + 2 + 3 = 6. One part = €60 ÷ 6 = €10. Shares: <b>€10, €20, €30</b>. Check they add up to €60.</p>
    {bar([1, 2, 3], ["Ruth", "Seán", "Tara"])}
    <p>Each share is a <b>fraction of the total</b>: Tara gets 3/6 = 1/2. In 2 : 3, the first person gets 2/5 (the bottom is the total number of parts).</p>
    <h2>3. One share or the difference known</h2>
    <p>Red : blue = 3 : 5 and there are 21 red. 3 parts = 21, so 1 part = 7 and blue = 5 × 7 = <b>35</b>. Ratio 2 : 7, one gets €35 more: 7 − 2 = 5 parts = €35, 1 part = €7, total 9 × 7 = <b>€63</b>.</p></div>
   <div><h2>4. Proportion: the unitary method</h2>
    <p>Find <b>one</b> first, then multiply. 4 tickets cost €18. 1 costs €18 ÷ 4 = €4.50, so 7 cost <b>€31.50</b>. Recipe for 6 uses 300 g → 50 g each → 9 people need <b>450 g</b> (not 303 g).</p>
    <h2>5. Map scales</h2>
    <table><thead><tr><th>Scale 1 : 25 000</th><th>Working</th></tr></thead><tbody>
     <tr><td>6 cm on the map</td><td>6 × 25 000 = 150 000 cm = 1 500 m = <b>1.5 km</b></td></tr>
     <tr><td>2 km in real life</td><td>2 km = 200 000 cm, ÷ 25 000 = <b>8 cm</b></td></tr></tbody></table>
    <p class="small">100 cm = 1 m · 1 000 m = 1 km · so 100 000 cm = 1 km</p>
    <h2>6. Best buy</h2>
    <p>Find the price of <b>one</b> (or of 100 g) in each pack. 6 for €4.20 = 70c each; 10 for €6.50 = 65c each, so the 10-pack is <b>better value</b>.</p>
    <h2>7. Absolute v relative</h2>
    <p><b>Absolute</b> = how many or how much (Class B had 15 passes, Class A 12). <b>Relative</b> = as a fraction or % of the whole (A: 12/20 = 60%, B: 15/30 = 50%), so <b>A did better relatively</b>. Relative change = change ÷ <b>start</b>.</p></div>
  </div>
  <div class="tip"><b>Exam tip:</b> write the "1 part" step (€840 ÷ 12 = €70): it earns marks even if a later line slips. Check your shares add to the total. Convert to the same units, and give the answer in the units asked for.</div>
</div>

<div class="page p2">
  <div class="band"><div><div class="k">Practice · 34 questions</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <div class="two"><div><h2>A. Simplify</h2><ol class="q">{qs(A)}</ol></div>
  <div><h2>B. Sharing</h2><ol class="q" start="7">{qs(B[:5])}</ol></div></div>
  <ol class="q" start="12">{qs(B[5:])}</ol>
  <h2>C. Proportion, maps and best buys</h2><ol class="q" start="15">{qs(Cq)}</ol>
  <h2>D. Absolute v relative (and a few more)</h2><ol class="q" start="23">{qs(D)}</ol>
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
   <tr><td><b>C</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(Cq,15))}</td></tr>
   <tr><td><b>D</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(D,23))}</td></tr>
   <tr><td><b>E</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(E,31))}</td></tr>
  </tbody></table>
  <div class="note"><b>Got one wrong?</b> Check: did you keep the order of the ratio? Did you add the parts to get the total number of parts? Did you find ONE first (unitary method)? Did you change to the same units? For "who did better", did you compare fractions or percentages, not just the numbers? Then play <b>Share It Out</b> at leim.ie/share-it-out.html: the "Go back over these" list at the end shows the rule for each mistake.</div>
  <p class="small">All questions written by Léim. Léim is independent and not connected with the State Examinations Commission or the NCCA.</p>
</div>
</body></html>"""

# ---------- teacher pack ----------
# Recipe Swap: pancakes. per person amounts
ING = [("Flour", 50, "g"), ("Milk", 75, "ml"), ("Eggs", F(1, 2), ""), ("Sugar", 10, "g"), ("Butter", 15, "g")]
A_KNOWS = {"Flour", "Eggs", "Butter"}  # Card A (4 people) shows these; Card B (6 people) shows Milk, Sugar
def amt(per, n, u): v = F(per) * n; assert v.denominator == 1; return f"{v} {u}".strip() if u else f"{v}"
RS = [(n, amt(p, 4, u), amt(p, 6, u), amt(p, 10, u)) for n, p, u in ING]
assert [r[1:] for r in RS] == [("200 g", "300 g", "500 g"), ("300 ml", "450 ml", "750 ml"), ("2", "3", "5"), ("40 g", "60 g", "100 g"), ("60 g", "90 g", "150 g")]
def recipe_card(title, who):
    rows = "".join(f"<tr><td>{r[0]}</td><td><b>{r[1] if (who == 'A' and r[0] in A_KNOWS) else ''}</b></td><td><b>{r[2] if (who == 'B' and r[0] not in A_KNOWS) else ''}</b></td><td></td></tr>" for r in RS)
    return f"""<div class="idc"><h3>{title}</h3><table class="ss"><thead><tr><th>Ingredient</th><th>For 4 people</th><th>For 6 people</th><th>For 10 people</th></tr></thead><tbody>{rows}</tbody></table></div>"""

# Ratio Match: 12 question/answer pairs = 24 mingle cards
MATCH = [("Share €30 in the ratio 1 : 2. The bigger share?", m(share(30, 1, 2)[1])),
         ("Simplify 18 : 24", rt(18, 24)),
         ("Share €45 in the ratio 4 : 5. The bigger share?", m(share(45, 4, 5)[1])),
         ("50 cm : 2 m in its simplest form", rt(50, 200)),
         ("2 : 7 = 8 : ?", dec(F(8) / 2 * 7)),
         ("Red : blue = 2 : 3. What fraction is red?", fr(F(2, 5))),
         ("4 pens cost €2. What do 6 cost?", m(unitary(4, 2, 6))),
         ("Map 1 : 50 000. 2 cm is how many km?", dec(mapkm(2, 50000)) + " km"),
         ("Recipe for 4 uses 200 g. How much for 6?", dec(unitary(4, 200, 6)) + " g"),
         ("Ratio 1 : 4. One gets 24 more. The total?", dec(F(24) / 3 * 5)),
         ("12 out of 20 as a percentage", pc(F(12, 20))),
         ("Share 60 sweets in 1 : 2 : 3. The biggest share?", dec(share(60, 1, 2, 3)[2]))]
assert [a for q, a in MATCH] == ["€20.00", "3 : 4", "€25.00", "1 : 4", "28", "2/5", "€3.00", "1 km", "300 g", "40", "60%", "30"]
assert len(set(a for q, a in MATCH)) == 12
cards = [q for q, a in MATCH] + [a for q, a in MATCH]
random.seed(7); match_print = cards[:]; random.shuffle(match_print)
match_html = "".join(f'<div class="c"><span class="tag">Card {i}</span><div class="fc{" sm" if len(x) > 12 else ""}">{x}</div></div>' for i, x in enumerate(match_print, 1))
match_key = " · ".join(f"{q} → <b>{a}</b>" for q, a in MATCH)

DOMS = [("Simplify 6 : 9", rt(6, 9)), ("Simplify 20 : 15", rt(20, 15)), ("30 cm : 1 m, simplest form", rt(30, 100)),
        ("€24 in 1 : 3. Smaller share?", m(share(24, 1, 3)[0])), ("€40 in 3 : 5. Bigger share?", m(share(40, 3, 5)[1])),
        ("€60 in 1 : 2 : 3. Biggest share?", m(share(60, 1, 2, 3)[2])), ("2 : 5 = ? : 15", dec(F(15) / 5 * 2)),
        ("3 : 4 = 15 : ?", dec(F(15) / 3 * 4)), ("Boys : girls = 1 : 3. Fraction boys?", fr(F(1, 4))),
        ("Ratio 2 : 3. Fraction for the 3?", fr(F(3, 5))), ("5 apples cost €2. One costs?", dec(F(200, 5)) + "c"),
        ("3 cost €1.50. 7 cost?", m(unitary(3, F(150, 100), 7))), ("Recipe for 2: 150 g. For 6?", dec(unitary(2, 150, 6)) + " g"),
        ("Map 1 : 10 000. 5 cm = ? m", dec(F(5) * 10000 / 100) + " m"), ("Map 1 : 100 000. 3 cm = ? km", dec(mapkm(3, 100000)) + " km"),
        ("9 out of 12 as a %", pc(F(9, 12))), ("€40 → €50: relative increase", pc(F(10, 40))), ("€40 → €50: absolute increase", m(10)),
        ("Ratio 2 : 5, difference 12. Total?", dec(F(12) / 3 * 7)), ("Red : blue = 3 : 2. 12 red. Blue?", dec(F(12) / 3 * 2))]
ANS = [a for k, a in DOMS]
assert ANS == ["2 : 3", "4 : 3", "3 : 10", "€6.00", "€25.00", "€30.00", "6", "20", "1/4", "3/5", "40c", "€3.50", "450 g", "500 m", "3 km", "75%", "25%", "€10.00", "28", "8"], ANS
assert len(set(ANS)) == 20
random.seed(77); chain = DOMS[:]; random.shuffle(chain)
dom = [("START" if k == 0 else chain[k - 1][1], x[0]) for k, x in enumerate(chain)] + [(chain[-1][1], "FINISH")]
dom_print = dom[:]; random.shuffle(dom_print)
dom_html = "".join(f'<div class="dom"><div class="h l">{l}</div><div class="h r">{r}</div></div>' for l, r in dom_print)
chain_key = "".join(f"<li>{x} = <b>{a}</b></li>" for x, a in chain)

ERR = [("Simplify 12 : 16", "= 6 : 8", f"Not fully simplified. ÷ 4 (the HCF): <b>{rt(12, 16)}</b>"),
       ("Share €35 in the ratio 2 : 5. Smaller share?", "= €17.50", f"Split it in half. 2 + 5 = 7 parts, 1 part = €5: <b>{m(share(35, 2, 5)[0])}</b>"),
       ("Red : blue = 3 : 4. Fraction red?", "= 3/4", f"The bottom must be the TOTAL parts (7): <b>{fr(F(3, 7))}</b>"),
       ("Recipe for 4 uses 200 g. For 6?", "= 202 g", f"Added 2 instead of scaling. 50 g each × 6: <b>{dec(unitary(4, 200, 6))} g</b>"),
       ("50 cm : 2 m in simplest form", "= 25 : 1", f"Units not the same. 50 : 200: <b>{rt(50, 200)}</b>"),
       ("A: 12 of 20 passed. B: 15 of 30 passed. Who did better?", "= B (15 > 12)", f"Only absolute. Relatively A {pc(F(12, 20))} v B {pc(F(15, 30))}: <b>A</b>")]
w1 = share(480, 3, 4, 5); assert w1 == [120, 160, 200]
w2a, w2b = share(35, 1, 2, 4)[1], F(12) * 4; assert (w2a, w2b) == (10, 48)
w3a, w3b = mapkm(14, 25000), mapcm(F(15, 10), 25000); assert (w3a, w3b) == (F(35, 10), 6)
w4a, w4b = F(240) / F(15, 10), F(85) / F(5, 10); assert (w4a, w4b) == (160, 170)
w5a, w5b = F(18, 24), F(21, 30); assert pc(w5a) == "75%" and pc(w5b) == "70%"

pack = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Ratio and Proportion Teacher Pack | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>
@page{{@bottom-left{{content:"Léim · leim.ie · Single-teacher licence · JC Maths LOs (2018 spec): {LO}";font-size:7pt}}}}
.proc td{{font-size:8.9pt;padding:3px 6px;line-height:1.32}}.proc td:first-child{{white-space:nowrap;font-weight:700;color:var(--green)}}
.p1 .note{{font-size:8.6pt;padding:6px 10px;line-height:1.35}}.p1 p{{font-size:9.5pt}}
.fym{{display:grid;grid-template-columns:repeat(4,1fr);margin-top:2mm}}
.fym .c{{border:2px dashed #9AA3AE;margin:-1px 0 0 -1px;height:15mm;position:relative;display:flex;align-items:center;justify-content:center;padding:3mm 2mm 1mm}}
.fym .fc{{font-size:17pt;font-weight:800;text-align:center}}.fym .fc.sm{{font-size:9.6pt;font-weight:700;line-height:1.25}}
.fym .tag{{position:absolute;top:1.2mm;left:3mm;font-size:6.5pt;color:var(--green);font-weight:800;text-transform:uppercase;letter-spacing:.04em}}
.idc{{border:2px dashed #9AA3AE;padding:2.5mm 4mm;margin-top:2.5mm}}.idc h3{{margin:0 0 2mm}}
.ss td,.ss th{{padding:2px 6px;font-size:9.2pt}}.ss td:nth-child(n+2){{width:21%}}
.doms{{display:grid;grid-template-columns:1fr 1fr;gap:2mm 6mm}}
.dom{{display:grid;grid-template-columns:1fr 1.7fr;border:2px dashed #9AA3AE;height:18.5mm}}
.dom .h{{display:flex;align-items:center;justify-content:center;text-align:center;padding:2mm;font-size:15pt;font-weight:800}}
.dom .r{{font-size:10.6pt;font-weight:700}}
.dom .l{{background:var(--mist);border-right:2px solid var(--ink)}}
.poster{{height:255mm;border:6px solid var(--night);border-radius:18px;padding:10mm;display:flex;flex-direction:column;justify-content:space-between}}
.poster h1{{font-size:44pt;text-align:center}}.poster p{{font-size:14pt!important}}
.ops{{display:grid;grid-template-columns:1fr 1fr;gap:4mm}}.ops div{{border-radius:14px;padding:6mm 4mm;text-align:center;font-size:13.5pt;line-height:1.5}}.ops b{{display:block;font-size:21pt;font-weight:800;margin-bottom:1mm}}
.big3{{display:grid;grid-template-columns:1fr 1fr 1fr;text-align:center;font-size:28pt;font-weight:800}}.big3 span{{display:block;font-size:11pt;color:var(--muted);font-weight:700}}
.ws{{font-size:10pt;line-height:1.42}}.ws ol.q li{{margin:6px 0}}.ws .long{{height:22px}}
.eh td{{padding:5px 8px;font-size:9.6pt}}.eh td:first-child{{font-weight:700;width:32%}}.eh .gap{{display:block;border-bottom:1px solid #9AA3AE;height:16px}}
</style></head><body>

<div class="page p1">
  <div class="band"><div><div class="k">Junior Cycle Maths · Teacher pack</div><h1>Ratio &amp; proportion</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2018 specification): {LO} (currency, speed, distance and time come later under N.3b; bills, VAT and value-for-money money questions under N.2c)</p>
  <div class="two">
    <div><h3>Aims</h3><p>By the end of the lesson students can write and simplify ratios (including mixed units), share an amount in a ratio of two or three parts, work from one share or the difference, use the unitary method for recipes, prices and map scales, choose the best-value pack, and tell an absolute comparison from a relative one.</p></div>
    <div><h3>In this pack</h3><p>p.1 Teacher notes · p.2 Share It Out mingle cards + Recipe Swap A/B cards · p.3 Ratio Dominoes (cut-up) · p.4 Wall poster · p.5 Worksheet: Error Hunt + exam-style questions · p.6 Answers. Level: 1st year (Higher and Ordinary), or 3rd-year revision. Time: about 60 minutes. All questions are original.</p></div>
  </div>
  <h2 style="margin-top:8px">Procedure</h2>
  <table class="proc"><tbody>
    <tr><td>5 min</td><td><b>Lead-in: Who did better?</b> Board "Class A: 12 of 20 passed. Class B: 15 of 30 passed." Hands up for A, B or the same. Ask both sides why. Don't settle it yet.</td></tr>
    <tr><td>8 min</td><td><b>Guided discovery: the sharing pattern.</b> Pairs share €20, €45 and €100 in the ratio 2 : 3 any way they like (bar model on the board: 2 boxes and 3 boxes). What fraction does the first person always get? Why is it 2/5, not 2/3? Then €350 in 2 : 3 in their heads (€140, €210).</td></tr>
    <tr><td>10 min</td><td><b>Share It Out mingle</b> (p.2, 24 cards = 12 question/answer pairs; one card each). Students with a question card work it out, then find the person holding the answer. Pairs check each other's working and sit together. Feedback: which pairs used "1 part"?</td></tr>
    <tr><td>12 min</td><td><b>Recipe Swap</b> (p.2, pairs: Student A has the pancake recipe for 4 people, Student B for 6 people, each with gaps; don't show your card). Ask your partner for the amounts you're missing and work out your own column from theirs ("How much milk is in your recipe?"). Then both fill the 10-people column. Feedback: why does finding 1 person first always work?</td></tr>
    <tr><td>10 min</td><td><b>Ratio Dominoes</b> (p.3), groups of 3–4. Start with START, work out the clue, find the domino with that answer on its left, and build the chain to FINISH. Answer chain below.</td></tr>
    <tr><td>12 min</td><td><b>Worksheet</b> (p.5). Error Hunt in pairs (find the mistake, name the rule, fix it), then the exam-style questions alone. Revisit the lead-in: Class A (60%) beat Class B (50%) relatively, B had more passes absolutely.</td></tr>
    <tr><td>3 min</td><td><b>Exit ticket.</b> Share €56 in the ratio 3 : 4; simplify 45 cm : 1.5 m (€24 and €32; 3 : 10). Homework: play <b>Share It Out</b> at leim.ie/share-it-out.html (Who did better? round) and copy three lines from the "Go back over these" list.</td></tr>
  </tbody></table>
  <div class="note"><b>Share It Out mingle key:</b> {match_key}.<br>
  <b>Errors to look for:</b> dividing by 2 instead of the total number of parts · reversing the order (boys : girls v girls : boys) · writing 3 : 4 as 3/4 instead of 3/7 · adding to scale a recipe · not changing to the same units · cm → km in one step (÷ 100 000) · comparing 15 and 12 instead of 15/30 and 12/20. <b>Support:</b> draw the bar model every time. <b>Fast finishers:</b> share €100 in the ratio 1 : 2 : 3 to the nearest cent; which gets the leftover cent?</div>
  <p class="small"><b>Domino answer chain</b> (START → FINISH):</p>
  <ol class="small" style="columns:3;column-gap:12px;font-size:7.6pt;line-height:1.33;margin:0;padding-left:16px">{chain_key}</ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">Cut up the cards · one recipe card per student</div><h1>Share It Out + Recipe Swap</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.5pt;margin:0"><b>Share It Out mingle.</b> Cut out the 24 cards and give one to each student. Question card? Work it out, then find the person with your answer. Answer card? Find the question that gives your answer. (Fewer students? Take out whole pairs.)</p>
  <div class="fym">{match_html}</div>
  <p style="font-size:9.5pt;margin:4mm 0 0"><b>Recipe Swap: pancakes.</b> Don't show your card. Ask your partner for the amounts you're missing, then work out your own column. Last of all, both fill in the column for 10 people. No calculators!</p>
  {recipe_card("Student A · Pancakes for 4 people", "A")}
  {recipe_card("Student B · Pancakes for 6 people", "B")}
</div>

<div class="page">
  <div class="band"><div><div class="k">Groups of 3–4 · cut along the dashed lines</div><h1>Ratio Dominoes</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.5pt">Start with START. Work out the clue on the right, then find the domino with that answer on its left. Keep going until you reach FINISH. No calculators!</p>
  <div class="doms">{dom_html}</div>
</div>

<div class="page">
  <div class="poster">
    <h1>Ratio &amp; proportion</h1>
    <div class="big3"><div>2 : 3<span>the ratio</span></div><div>5<span>parts in total</span></div><div>2/5 · 3/5<span>each share</span></div></div>
    <p style="text-align:center;font-size:12pt;margin:0"><b>Order matters:</b> boys : girls is not girls : boys · <b>same units</b> before you simplify</p>
    <div class="ops">
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Simplify</b>÷ both by the HCF<br>12 : 18 = 2 : 3<br>50 cm : 2 m = 1 : 4</div>
      <div style="background:var(--green-soft)"><b>Share</b>€60 in 1 : 2 : 3<br>6 parts → 1 part = €10<br>€10 · €20 · €30</div>
      <div style="background:var(--green-soft)"><b>Find ONE first</b>4 cost €18 → 1 costs €4.50<br>7 cost €31.50<br>Map 1 : 25 000: 6 cm = 1.5 km</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Who did better?</b>Absolute: 15 &gt; 12<br>Relative: 12/20 = 60%<br>15/30 = 50% → A wins</div>
    </div>
    <p style="text-align:center;font-size:12pt;margin:0"><b>Check:</b> the shares add up to the total</p>
    <p style="text-align:center;font-size:10pt;color:var(--muted)">Léim · leim.ie · Play Share It Out: leim.ie/share-it-out.html</p>
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
    <li>Three friends share €480 in the ratio 3 : 4 : 5. How much does each get?<span class="long"></span></li>
    <li>Concrete is made from cement, sand and gravel in the ratio 1 : 2 : 4. (a) How much sand is in 35 kg of concrete? (b) A builder has 12 kg of cement. How much gravel does she need?<span class="long"></span><span class="long"></span></li>
    <li>A map has a scale of 1 : 25 000. (a) A road is 14 cm long on the map. How long is it in km? (b) A lake is 1.5 km long. How long is it on the map?<span class="long"></span><span class="long"></span></li>
    <li>Juice comes in a 1.5 litre carton for €2.40 or a 500 ml carton for €0.85. Which is better value? Show your work.<span class="long"></span><span class="long"></span></li>
    <li>Team A won 18 of its 24 matches. Team B won 21 of its 30 matches. (a) Which team won more matches? (b) Which team had the better record? (c) Explain the difference.<span class="long"></span><span class="long"></span></li>
  </ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">For the teacher</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>Recipe Swap (per person: 50 g flour, 75 ml milk, ½ egg, 10 g sugar, 15 g butter)</h2>
  <table><thead><tr><th>Ingredient</th><th>For 4</th><th>For 6</th><th>For 10</th></tr></thead><tbody>
  {"".join(f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td><b>{r[3]}</b></td></tr>" for r in RS)}
  </tbody></table>
  <h2>A. Error Hunt</h2>
  <table><tbody>{"".join(f"<tr><td style='width:34%'><b>{q}</b> {w}</td><td>{r}</td></tr>" for q,w,r in ERR)}</tbody></table>
  <h2>B. Exam-style questions</h2>
  <ol class="q">
    <li>12 parts, 1 part = €40: <b>{", ".join(m(x) for x in w1)}</b> (check: they add to €480)</li>
    <li>(a) 7 parts, 1 part = 5 kg, sand = <b>{w2a} kg</b> (b) gravel is 4 × the cement: <b>{w2b} kg</b></li>
    <li>(a) 14 × 25 000 = 350 000 cm = <b>{dec(w3a)} km</b> (b) 1.5 km = 150 000 cm, ÷ 25 000 = <b>{dec(w3b)} cm</b></li>
    <li>Per litre: €2.40 ÷ 1.5 = {m(w4a/100)}; €0.85 × 2 = {m(w4b/100)}. The <b>1.5 litre carton</b> is better value.</li>
    <li>(a) <b>Team B</b> (21 v 18, absolute) (b) A {pc(w5a)} v B {pc(w5b)}: <b>Team A</b> (relative) (c) B played more matches, so it can win more of them while winning a smaller proportion.</li>
  </ol>
  <h2>Marking tip</h2>
  <p>Give credit for each step, as the exam does: "12 parts, 1 part = €40" earns marks even if a share slips. For "which is better?" insist on a reason (price of one, or the two percentages) and a clear conclusion.</p>
</div>
</body></html>"""

cover = """<!doctype html><html><head><meta charset="utf-8"><style>
body{margin:0;width:1200px;height:1200px;background:#1B2430;font-family:Inter,sans-serif;color:#fff;display:flex;flex-direction:column;justify-content:space-between;padding:90px;box-sizing:border-box}
.k{display:inline-block;background:#2E7D57;border-radius:99px;padding:12px 26px;font-weight:700;font-size:28px;letter-spacing:.06em;text-transform:uppercase}
h1{font-size:112px;font-weight:800;line-height:1.12;letter-spacing:-.03em;margin:40px 0 0}
h1 span{background:#F6CF5A;color:#1B2430;padding:0 14px;box-decoration-break:clone;-webkit-box-decoration-break:clone}
.sub{font-size:38px;color:#C9D1DA;margin-top:36px;line-height:1.35}
.em{font-size:50px;margin-top:30px;font-weight:800;letter-spacing:.01em;color:#F6CF5A}
.foot{display:flex;justify-content:space-between;align-items:center;font-size:34px;font-weight:700}
.price{background:#F6CF5A;color:#1B2430;border-radius:16px;padding:14px 28px}
</style></head><body>
<div><span class="k">Junior Cycle Maths · Teacher pack</span>
<h1><span>Ratio &amp;</span><br><span>Proportion</span></h1>
<div class="sub">Share It Out mingle · Recipe Swap A/B<br>Ratio Dominoes · Poster · Worksheet + answers</div>
<div class="em">€60 in 1 : 2 : 3 → €10, €20, €30</div></div>
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
    pdf("teacher-pack", os.path.join(OUT, "Ratio-and-Proportion-Teacher-Pack-Leim.pdf"))
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--hide-scrollbars", "--window-size=1200,1200",
                    f"--screenshot={os.path.join(OUT, f'{SLUG}-cover.png')}", f"{SLUG}-cover.html"], cwd=SRC, check=True, capture_output=True)
    print("domino chain:", [(x, a) for x, a in chain])
