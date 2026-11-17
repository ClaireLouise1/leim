#!/usr/bin/env python3
"""Indices & standard form (JC Maths topic 17): free sheet + teacher pack + Payhip cover.
Run from the repo root: python3 src/build_indices_pdfs.py OUTDIR   (needs: pip install --break-system-packages sympy)
Writes src/indices-standard-form-*.html; PDFs/cover PNG go to OUTDIR (free sheet also to printables/).
Every answer is worked out with sympy (via test_power_up's text reader) and asserted."""
import os, sys, random, subprocess, re
import sympy as sp
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC)
sys.path.insert(0, SRC)
import test_power_up as T
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/indices"; os.makedirs(OUT, exist_ok=True)
SLUG = "indices-standard-form"
LO = "N.1c, N.1f"
E = T.E


def same(q, a):
    assert T.eq(E(q), E(a)), (q, a, E(q), E(a)); return a


def sf(q, a):
    assert T.is_sf(a) and T.eq(E(q), E(a)), (q, a); return a


def fi(b, top):  # fractional index for the PDFs
    return f'{b}<sup class="fx">{top}</sup>'


# ---------- free sheet ----------
A = [("2⁶", "64"), ("3⁴", "81"), ("(−3)²", "9"), ("−3²", "−9"), ("(−2)⁵", "−32"), ("√121", "11")]
for q, a in A: same(q, a)
A += [("Write 1,000,000 as a power of 10.", "10⁶"), ("√50 lies between which two whole numbers?", "7 and 8")]
assert E("10⁶") == 1000000 and 7 ** 2 < 50 < 8 ** 2
B = [("4 + 3² × 2", "22"), ("(4 + 3)²", "49"), ("2 × 5³", "250"), ("√(10² − 6²)", "8"),
     ("x⁴ × x⁵", "x⁹"), ("7⁸ ÷ 7³", "7⁵"), ("(a³)⁴", "a¹²"), ("3x² × 5x⁴", "15x⁶")]
for q, a in B: same(q, a)
C = [("20y⁹ ÷ 4y³", "5y⁶"), ("2a²b × 3ab⁴", "6a³b⁵"), ("(2⁴ × 2⁵) ÷ 2⁷ (give the value)", "4"), ("5⁷ ÷ 5⁴ (give the value)", "125")]
for q, a in C: same(q.split(" (")[0], a)
n = sp.Symbol("n", positive=True)
FN = [("2ⁿ × 2⁴ = 2¹¹", "7"), ("(3ⁿ)² = 3¹⁰", "5"), ("4ⁿ = 64", "3")]
for q, a in FN:
    l, r = q.split(" = "); s = sp.solve(sp.Eq(E(l), E(r)), n); assert s == [int(a)], (q, s)
C += [(f"Find n: {q}", a) for q, a in FN]
assert not T.eq(E("2³ × 2⁴"), E("4⁷")) and T.eq(E("2³ × 2⁴"), E("2⁷"))
C += [("True or false? 2³ × 2⁴ = 4⁷. Explain.", "False: the base stays 2, so 2⁷")]
D = [("Write 6,400 in standard form.", sf("6400", "6.4 × 10³")),
     ("Write 2,050,000 in standard form.", sf("2050000", "2.05 × 10⁶")),
     ("Write 3.2 × 10⁴ as an ordinary number.", same("3.2 × 10⁴", "32,000")),
     ("Put in order, smallest first: 4.1 × 10⁵, 9.9 × 10⁴, 1.2 × 10⁶.", "9.9 × 10⁴, 4.1 × 10⁵, 1.2 × 10⁶"),
     ("Work out (5 × 10³) × (4 × 10²). Give your answer in standard form.", sf("(5 × 10³) × (4 × 10²)", "2 × 10⁶")),
     ("Work out (6 × 10⁸) ÷ (2 × 10³). Give your answer in standard form.", sf("(6 × 10⁸) ÷ (2 × 10³)", "3 × 10⁵"))]
assert E("9.9 × 10⁴") < E("4.1 × 10⁵") < E("1.2 × 10⁶")
x = T.SYM["x"]
assert E("16^(3/4)") == 8 and E("5⁻²") == sp.Rational(1, 25) and E("7⁰") == 1 and sp.Rational(1, 9) == sp.Integer(3) ** -2
assert sf("384000", "3.84 × 10⁵") and sf("(3.84 × 10⁵) ÷ (1.6 × 10⁴)", "2.4 × 10¹") and E("2.4 × 10¹") == 24
assert T.eq(E("(2⁴)³"), E("2¹²")) and 2 ** 12 == 4096 and T.eq(E("(2⁴)²"), E("2⁸")) and 6 * 2 ** 8 == 1536
assert T.eq(E("(3x²)³ ÷ x⁴"), E("27x²"))
assert sf("0.000075", "7.5 × 10⁻⁵") and sf("(5 × 10⁻³) × (4 × 10⁻²)", "2 × 10⁻⁴")
EX = [(f"<b>Higher Level.</b> Work out (a) {fi(16, '3/4')} (b) 5⁻² (c) 7⁰. (d) Solve 3ˣ = 1/9.",
       "(a) fourth root of 16 = 2, 2³ = <b>8</b> (b) 1/5² = <b>1/25</b> (c) <b>1</b> (d) 1/9 = 3⁻², so <b>x = −2</b>"),
      ("The Moon is about 384,000 km from the Earth. (a) Write this in standard form. (b) A spacecraft travels at 1.6 × 10⁴ km per hour. How many hours does it take to reach the Moon?",
       "(a) <b>3.84 × 10⁵ km</b> (b) (3.84 × 10⁵) ÷ (1.6 × 10⁴) = 2.4 × 10¹ = <b>24 hours</b>"),
      ("A cube has edges 2⁴ cm long. (a) Write its volume as a power of 2. (b) Work out the volume. (c) Each face has area (2⁴)² cm². Write the total surface area as 6 × a power of 2, then work it out.",
       "(a) (2⁴)³ = <b>2¹² cm³</b> (b) <b>4,096 cm³</b> (c) 6 × 2⁸ = <b>1,536 cm²</b>"),
      ("<b>Higher Level.</b> (a) Simplify (3x²)³ ÷ x⁴. (b) Write 0.000075 in standard form. (c) Work out (5 × 10⁻³) × (4 × 10⁻²) in standard form.",
       "(a) 27x⁶ ÷ x⁴ = <b>27x²</b> (b) <b>7.5 × 10⁻⁵</b> (c) 20 × 10⁻⁵ = <b>2 × 10⁻⁴</b>")]
assert len(A) + len(B) + len(C) + len(D) + len(EX) == 34, (len(A), len(B), len(C), len(D))


def qs(items): return "".join(f"<li>{q} <span class='line'></span></li>" for q, a in items)


def wq(q):  # bare expressions get "Work out" / "Simplify"
    return q if re.search(r"[A-Za-z]{3}", q) else (("Simplify " if re.search(r"[a-z]", q) else "Work out ") + q)


sheet = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Indices and standard form, rules and practice | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>@page{{@bottom-left{{content:"Léim · leim.ie · Free to print for home or class · JC Maths LOs (2018 spec): {LO}"}}}}
.tight{{font-size:11.7pt;line-height:1.5}}.tight td,.tight th{{padding:3px 6px}}.tight h2{{margin:11px 0 5px;font-size:14pt}}.tight .note,.tight .tip{{padding:6px 10px;margin:6px 0}}.tight p{{margin:3px 0}}
ol.q{{padding-left:30px}}ol.q li{{margin:7px 0}}
.ans td{{padding:3px 6px;font-size:9.2pt}}
.p2{{font-size:11.2pt;line-height:1.45}}.p2 ol.q li{{margin:13px 0}}.p2 h2{{margin:12px 0 6px;font-size:14pt}}.p2 .line{{min-width:70px}}
.wk{{line-height:1.55}}.wk i{{color:#5B6673;font-style:normal;font-size:9pt}}
.lw{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:3mm;margin:4px 0}}.lw div{{background:var(--cream);border:1.5px solid var(--cream-line);border-radius:8px;padding:5px 7px;font-size:9.6pt}}.lw b{{display:block;font-size:12.5pt}}
.hl{{display:inline-block;background:var(--night);color:#fff;font-size:7.5pt;font-weight:700;border-radius:99px;padding:1px 7px;vertical-align:middle}}
sup.fx{{font-size:.62em}}
</style></head><body>
<div class="page tight">
  <div class="band"><div><div class="k">Junior Cycle Maths · Free revision sheet</div><h1>Indices &amp; standard form</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2018 specification): {LO}. Play the game: <b>leim.ie/power-up.html</b></p>
  <div class="two">
   <div><h2>1. Index notation</h2>
    <p>In 2⁵, 2 is the <b>base</b> and 5 is the <b>index</b>: 2⁵ = 2 × 2 × 2 × 2 × 2 = <b>32</b> (not 10).</p>
    <p>10⁶ = 1,000,000 (6 zeros). (−3)² = 9 but −3² = −9: the index only belongs to what it touches.</p>
    <h2>2. Square roots</h2>
    <p>√49 = 7 because 7² = 49. 49{fi('', '½')} = √49. √50 is between 7 and 8 (7² = 49, 8² = 64). √(36 + 64) = √100 = 10, not 6 + 8.</p>
    <h2>3. BIMDAS</h2>
    <p class="wk">Brackets, Indices, ÷ ×, + −<br><b>5 + 3² × 2</b> = 5 + 9 × 2 = 5 + 18 = 23<br>4 × 2³ = 4 × 8 = 32 &nbsp;<i>(not 8³)</i></p>
    <h2>4. Standard form</h2>
    <p><b>a × 10ⁿ</b> with 1 ≤ a &lt; 10 and n a whole number.</p>
    <p class="wk">45,000 → 4.5 (the point moved 4 places) → <b>4.5 × 10⁴</b><br>3.07 × 10⁵ → move the point 5 right → 307,000</p>
    <p>Not standard form: 45 × 10³, 0.45 × 10⁵. Compare the powers of 10 first.</p></div>
   <div><h2>5. The laws of indices</h2>
    <div class="lw"><div><b>aᵖ × a<sup>q</sup> = a<sup>p+q</sup></b>add</div><div><b>aᵖ ÷ a<sup>q</sup> = a<sup>p−q</sup></b>subtract</div><div><b>(aᵖ)<sup>q</sup> = a<sup>pq</sup></b>multiply</div></div>
    <p>x³ × x⁵ = x⁸ · 5⁹ ÷ 5³ = 5⁶ · (2³)⁴ = 2¹². The base stays the same: 2³ × 2⁴ = 2⁷, not 4⁷.</p>
    <p>Numbers in front: 3x² × 4x⁵ = 12x⁷ · 12x⁷ ÷ 3x² = 4x⁵. x³ + x⁴ can't be joined.</p>
    <p>Find n: 2ⁿ × 2³ = 2¹⁰ → n + 3 = 10 → n = 7.</p>
    <h2>6. Calculating in standard form</h2>
    <p class="wk">(4 × 10³) × (5 × 10²) = 20 × 10⁵ = <b>2 × 10⁶</b><br>(8 × 10⁹) ÷ (2 × 10³) = <b>4 × 10⁶</b><br><i>numbers first, then the indices, then tidy up</i></p>
    <h2>7. Zero, negative &amp; fractional <span class="hl">Higher Level</span></h2>
    <p>a⁰ = 1 · 2⁻³ = 1/2³ = 1/8 (not negative) · 8{fi('', '1/3')} = 2 · 27{fi('', '2/3')} = 3² = 9 (root first) · (2x³)² = 4x⁶ · 2ˣ = 1/8 = 2⁻³, so x = −3 · 0.00036 = 3.6 × 10⁻⁴</p></div>
  </div>
  <div class="tip"><b>Exam tip:</b> write the law you used (2⁵ × 2³ = 2⁵⁺³ = 2⁸), give the answer in the form asked for ("as a power of 2", "in standard form"), and copy calculator answers in standard form properly with × 10 and the index.</div>
</div>

<div class="page p2">
  <div class="band"><div><div class="k">Practice · 34 questions</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <div class="two"><div><h2>A. Powers and roots</h2><ol class="q">{"".join(f"<li>{wq(q)} <span class='line'></span></li>" for q, a in A)}</ol></div>
  <div><h2>B. BIMDAS and the laws</h2><ol class="q" start="9">{"".join(f"<li>{wq(q)} <span class='line'></span></li>" for q, a in B)}</ol></div></div>
  <div class="two"><div><h2>C. More laws, find n</h2><ol class="q" start="17">{"".join(f"<li>{wq(q)} <span class='line'></span></li>" for q, a in C)}</ol></div>
  <div><h2>D. Standard form</h2><ol class="q" start="25">{qs(D)}</ol></div></div>
  <p class="small" style="margin-top:6px">Questions 31–34 are on the next page.</p>
</div>

<div class="page">
  <div class="band"><div><div class="k">Exam-style · then check</div><h1>Exam corner + answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>E. Exam-style questions (show your work)</h2>
  <ol class="q" start="31">{"".join(f"<li>{q}<span class='long'></span><span class='long'></span></li>" for q, a in EX)}</ol>
  <h2 style="margin-top:12px">Answers</h2>
  <table class="ans"><tbody>
   <tr><td><b>A</b></td><td>{" · ".join(f"{i}. {a}" for i, (q, a) in enumerate(A, 1))}</td></tr>
   <tr><td><b>B</b></td><td>{" · ".join(f"{i}. {a}" for i, (q, a) in enumerate(B, 9))}</td></tr>
   <tr><td><b>C</b></td><td>{" · ".join(f"{i}. {a}" for i, (q, a) in enumerate(C, 17))}</td></tr>
   <tr><td><b>D</b></td><td>{" · ".join(f"{i}. {a}" for i, (q, a) in enumerate(D, 25))}</td></tr>
   <tr><td><b>E</b></td><td>{" · ".join(f"{i}. {a}" for i, (q, a) in enumerate(EX, 31))}</td></tr>
  </tbody></table>
  <div class="note"><b>Got one wrong?</b> Did you multiply the base by the index (2⁵ = 10)? Add the indices when multiplying, subtract when dividing, multiply for a power of a power, and keep the base the same. Do indices before × and +. In standard form, the front number must be between 1 and 10. Then play <b>Power Up</b> at leim.ie/power-up.html: the "Go back over these" list at the end shows the rule for each mistake.</div>
  <p class="small">All questions written by Léim. Léim is independent and not connected with the State Examinations Commission or the NCCA.</p>
</div>
</body></html>"""

# ---------- teacher pack ----------
# Index Law Match: 12 question cards ↔ 12 answer cards; each question equals exactly one answer
MATCH = [("x³ × x⁴", "x⁷"), ("x¹⁰ ÷ x²", "x⁸"), ("(x²)³", "x⁶"), ("2x³ × 3x²", "6x⁵"), ("12x⁹ ÷ 4x³", "3x⁶"),
         ("(x⁴)² ÷ x⁵", "x³"), ("x × x⁸", "x⁹"), ("5x² × 2x²", "10x⁴"), ("x⁶ × x⁶ ÷ x²", "x¹⁰"),
         ("2⁵ × 2³", "2⁸"), ("3⁹ ÷ 3⁷", "9"), ("(5²)² ÷ 5³", "5")]
for q, a in MATCH:
    hits = [b for p, b in MATCH if T.eq(E(q), E(b))]
    assert hits == [a], (q, hits)
cards = [q for q, a in MATCH] + [a for q, a in MATCH]
random.seed(17); match_print = cards[:]; random.shuffle(match_print)
num_of = {t: i for i, t in enumerate(match_print, 1)}
match_html = "".join(f'<div class="c"><span class="tag">Card {i}</span><div class="fc">{t}</div></div>' for i, t in enumerate(match_print, 1))
match_key = " · ".join(f"{num_of[q]} ↔ {num_of[a]}" for q, a in MATCH)
# Standard Form Line-Up: 16 cards, some in standard form, some ordinary; all different values
LINE = ["3.2 × 10⁴", "45,000", "9.9 × 10³", "1.05 × 10⁵", "7 × 10²", "2,300", "6.1 × 10⁴", "610,000",
        "8 × 10⁵", "1.2 × 10⁶", "950", "5.5 × 10³", "4.08 × 10⁴", "12,500", "2 × 10⁵", "3,000,000"]
vals = [E(c) for c in LINE]; assert len(set(vals)) == 16
order = [c for v, c in sorted(zip(vals, LINE))]
line_html = "".join(f'<div class="c"><span class="tag">Card {i}</span><div class="fc">{t}</div></div>' for i, t in enumerate(LINE, 1))
line_key = " < ".join(str(LINE.index(c) + 1) for c in order)
# Index Dominoes: 20 clues, all answers different numbers
DOMS = [("2⁵", "32"), ("3³", "27"), ("10⁴", "10,000"), ("(−2)⁴", "16"), ("−5²", "−25"), ("√144", "12"), ("√(3² + 4²)", "5"),
        ("2 + 3² × 2", "20"), ("(2 + 4)² ÷ 4", "9"), ("2⁷ ÷ 2⁴", "8"), ("3² × 3²", "81"), ("(2³)²", "64"), ("10⁶ ÷ 10³", "1,000"),
        ("5⁴ ÷ 5²", "25"), ("4 × 3²", "36"), ("1⁹ + 9¹", "10"), ("6² − 2⁵", "4"), ("10⁴ ÷ 10²", "100"), ("√81 × 2", "18"), ("7² + 1", "50")]
for q, a in DOMS: same(q, a)
ANS = [a for q, a in DOMS]; assert len(set(ANS)) == 20, sorted(ANS)
random.seed(1717); chain = DOMS[:]; random.shuffle(chain)
dom = [("START" if k == 0 else chain[k - 1][1], "Work out " + c[0]) for k, c in enumerate(chain)] + [(chain[-1][1], "FINISH")]
dom_print = dom[:]; random.shuffle(dom_print)
dom_html = "".join(f'<div class="dom"><div class="h l">{l}</div><div class="h r">{r}</div></div>' for l, r in dom_print)
chain_key = "".join(f"<li>{q} → <b>{a}</b></li>" for q, a in chain)

ERR = [("2⁴", "2⁴ = 2 × 4 = 8", "The index counts how many 2s are multiplied: 2 × 2 × 2 × 2 = <b>16</b>", "16", "8"),
       ("x³ × x⁵", "x³ × x⁵ = x¹⁵", "Multiplying: ADD the indices: <b>x⁸</b>", "x⁸", "x¹⁵"),
       ("3² × 3⁴", "3² × 3⁴ = 9⁶", "The base stays 3: <b>3⁶</b> (= 729)", "3⁶", "9⁶"),
       ("−4²", "−4² = 16", "The index belongs to the 4 only: −(4 × 4) = <b>−16</b>", "−16", "16"),
       ("4,700,000 in standard form", "47 × 10⁵", "47 is not between 1 and 10: <b>4.7 × 10⁶</b>", "4.7 × 10⁶", None),
       ("(2 × 10³) × (6 × 10⁴)", "12 × 10¹²", "Add the indices (3 + 4 = 7), then tidy: 12 × 10⁷ = <b>1.2 × 10⁸</b>", "1.2 × 10⁸", "12 × 10¹²")]
for q, w, r, good, bad in ERR:
    qq = "4700000" if "standard form" in q else q
    assert T.eq(E(qq), E(good)), q
    if bad: assert not T.eq(E(qq), E(bad)), q
assert T.is_sf("4.7 × 10⁶") and not T.is_sf("47 × 10⁵") and T.is_sf("1.2 × 10⁸")
W = [("Write as a single power, then work out the value: (3⁵ × 3⁴) ÷ 3⁶.", "3⁵⁺⁴⁻⁶ = <b>3³ = 27</b>"),
     ("Simplify (a) 4a³ × 5a⁶ (b) 18b⁸ ÷ 6b³ (c) (y⁵)³ ÷ y⁷.", "(a) <b>20a⁹</b> (b) <b>3b⁵</b> (c) y¹⁵ ÷ y⁷ = <b>y⁸</b>"),
     ("Find n if (a) 5ⁿ × 5³ = 5¹⁰ (b) 2ⁿ = 128.", "(a) <b>n = 7</b> (b) <b>n = 7</b> (2⁷ = 128)"),
     ("A hard drive holds 2 × 10¹² bytes. A film uses 4 × 10⁹ bytes. (a) How many films fit on the drive? (b) Write 4 × 10⁹ as an ordinary number.",
      "(a) (2 × 10¹²) ÷ (4 × 10⁹) = 0.5 × 10³ = <b>500 films</b> (b) <b>4,000,000,000</b>"),
     (f"<b>Higher Level.</b> (a) Work out {fi(8, '2/3')} and 4⁻². (b) Solve 2ˣ = 1/32. (c) Simplify (2x⁴)³ × x⁻⁵.",
      "(a) (cube root of 8)² = <b>4</b>; 1/4² = <b>1/16</b> (b) 1/32 = 2⁻⁵, so <b>x = −5</b> (c) 8x¹² × x⁻⁵ = <b>8x⁷</b>")]
assert E("(3⁵ × 3⁴) ÷ 3⁶") == 27 and T.eq(E("4a³ × 5a⁶"), E("20a⁹")) and T.eq(E("18n⁸ ÷ 6n³"), E("3n⁵")) and T.eq(E("(y⁵)³ ÷ y⁷"), E("y⁸"))
assert 5 ** 7 * 5 ** 3 == 5 ** 10 and 2 ** 7 == 128 and E("(2 × 10¹²) ÷ (4 × 10⁹)") == 500 and E("4 × 10⁹") == 4000000000
assert E("8^(2/3)") == 4 and E("4⁻²") == sp.Rational(1, 16) and sp.Rational(1, 32) == sp.Integer(2) ** -5 and T.eq(E("(2x⁴)³ × x⁻⁵"), E("8x⁷"))
EXIT = [same("(2⁶ × 2²) ÷ 2⁵", "8"), sf("52000", "5.2 × 10⁴")]

pack_style = open(os.path.join(SRC, "build_ratio_pdfs.py"), encoding="utf-8").read()
pack_style = pack_style[pack_style.index("<style>", pack_style.index('pack = f"""')) + 7:pack_style.index("</style>", pack_style.index('pack = f"""'))]
pack_style = pack_style.replace("{{", "{").replace("}}", "}").replace("{LO}", LO)
pack_style += (".fym .c{height:19mm}.fym .fc{font-size:19pt}.line4 .c{height:20mm}sup.fx{font-size:.62em}"
               ".laws3{display:grid;grid-template-columns:1fr;gap:4mm}.laws3 div{border-radius:14px;padding:5mm;text-align:center;font-size:14pt;line-height:1.45}.laws3 b{display:block;font-size:28pt;font-weight:800}")
pack = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Indices and Standard Form Teacher Pack | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{pack_style}</style></head><body>

<div class="page p1">
  <div class="band"><div><div class="k">Junior Cycle Maths · Teacher pack</div><h1>Indices &amp; standard form</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2018 specification): {LO} (zero, negative and fractional indices, (ab)ʳ and small numbers in standard form are Higher Level; surds come later, N.1b)</p>
  <div class="two">
    <div><h3>Aims</h3><p>By the end of the lesson students move between whole numbers and index form; use the laws of indices for multiplying, dividing and powers of powers (with numbers in front); apply BIMDAS with indices and roots; and write numbers in and out of standard form, comparing and calculating with them.</p></div>
    <div><h3>In this pack</h3><p>p.1 Teacher notes · p.2 Index Law Match cards + Standard Form Line-Up cards · p.3 Index Dominoes (cut-up) · p.4 Wall poster · p.5 Worksheet: Error Hunt + exam-style questions · p.6 Answers. Level: 2nd year (Higher and Ordinary), or 3rd-year revision. Time: about 60 minutes. All questions are original.</p></div>
  </div>
  <h2 style="margin-top:8px">Procedure</h2>
  <table class="proc"><tbody>
    <tr><td>5 min</td><td><b>Lead-in: fold it.</b> "A sheet of paper is folded in half again and again. How many layers after 1, 2, 3 … 10 folds?" Build the table 2, 4, 8 … and write the answers as 2¹, 2², 2³ … 2¹⁰ = 1,024. Base, index, and why 2⁵ ≠ 10.</td></tr>
    <tr><td>8 min</td><td><b>Guided discovery.</b> Pairs write out 2³ × 2⁴, 3² × 3⁵, x⁴ × x² and 2⁶ ÷ 2² in full (as on the poster) and count. What happens to the indices? Then (2³)²: what is it as one power? Pairs state the three laws in their own words before you name them.</td></tr>
    <tr><td>10 min</td><td><b>Index Law Match</b> (p.2, 24 cards = 12 pairs; one card each). Question cards find the person holding their simplified answer. Pairs then explain which law they used. Feedback on 2⁵ × 2³ (the base stays 2) and (x⁴)² ÷ x⁵.</td></tr>
    <tr><td>10 min</td><td><b>Standard Form Line-Up</b> (p.2, 16 cards). Students with a card line up across the room from smallest to biggest without talking, then each says their number in standard form. Discuss: why is 1.05 × 10⁵ bigger than 9.9 × 10³? (Look at the power of 10 first.)</td></tr>
    <tr><td>10 min</td><td><b>Index Dominoes</b> (p.3), groups of 3–4: start with START, work out the clue, find the domino with that answer on its left and build the chain to FINISH. No calculators.</td></tr>
    <tr><td>14 min</td><td><b>Worksheet</b> (p.5). Error Hunt in pairs (find the mistake, name the rule, fix it), then the exam-style questions alone. Higher Level groups do question 5.</td></tr>
    <tr><td>3 min</td><td><b>Exit ticket.</b> Work out (2⁶ × 2²) ÷ 2⁵ as a number; write 52,000 in standard form ({EXIT[0]}; {EXIT[1]}). Homework: play <b>Power Up</b> at leim.ie/power-up.html (Index laws and Standard form rounds) and copy three lines from the "Go back over these" list.</td></tr>
  </tbody></table>
  <div class="note"><b>Index Law Match key</b> (question card ↔ answer card): {match_key}.<br>
  <b>Standard Form Line-Up key</b> (card numbers, smallest first): {line_key}.<br>
  <b>Errors to look for:</b> 2⁵ = 10 · x³ × x⁵ = x¹⁵ · 3² × 3⁴ = 9⁶ · −4² = 16 · BIMDAS: 2 × 3² = 36 · 47 × 10⁵ left as the answer · 12 × 10⁷ not tidied up. <b>Support:</b> write powers out in full until the pattern is secure; a laws card on the desk. <b>Fast finishers:</b> which is bigger, 2¹⁰ or 10³? 2¹⁰⁰ or 10³⁰?</div>
  <p class="small"><b>Domino answer chain</b> (START → FINISH):</p>
  <ol class="small" style="columns:3;column-gap:12px;font-size:7.8pt;line-height:1.3;margin:0;padding-left:16px">{chain_key}</ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">One card per student · cut along the dashed lines</div><h1>Index Law Match + Line-Up cards</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.5pt;margin:0"><b>Index Law Match.</b> Cut out the 24 cards and give one to each student. Question card? Find the person holding its simplified answer. (Fewer students? Take out whole pairs.)</p>
  <div class="fym">{match_html}</div>
  <p style="font-size:9.5pt;margin:4mm 0 0"><b>Standard Form Line-Up.</b> 16 cards: line up from smallest to biggest without talking, then say your number in standard form.</p>
  <div class="fym line4">{line_html}</div>
</div>

<div class="page">
  <div class="band"><div><div class="k">Groups of 3–4 · cut along the dashed lines</div><h1>Index Dominoes</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.5pt">Start with START. Work out the clue on the right, then find the domino with that answer on its left. Keep going until you reach FINISH. No calculators!</p>
  <div class="doms">{dom_html}</div>
</div>

<div class="page">
  <div class="poster">
    <h1>The laws of indices</h1>
    <p style="text-align:center;font-size:15pt!important;margin:0">2³ × 2⁴ = (2 × 2 × 2) × (2 × 2 × 2 × 2) = 2⁷</p>
    <div class="laws3">
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>aᵖ × a<sup>q</sup> = a<sup>p+q</sup></b>Multiply: <b style="display:inline;font-size:inherit">add</b> the indices · x³ × x⁵ = x⁸</div>
      <div style="background:var(--green-soft)"><b>aᵖ ÷ a<sup>q</sup> = a<sup>p−q</sup></b>Divide: <b style="display:inline;font-size:inherit">subtract</b> the indices · 5⁹ ÷ 5³ = 5⁶</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>(aᵖ)<sup>q</sup> = a<sup>pq</sup></b>Power of a power: <b style="display:inline;font-size:inherit">multiply</b> · (2³)⁴ = 2¹²</div>
    </div>
    <div class="ops">
      <div style="background:var(--green-soft)"><b>Standard form</b>a × 10ⁿ, 1 ≤ a &lt; 10<br>45,000 = 4.5 × 10⁴</div>
      <div style="background:var(--green-soft)"><b>Higher Level</b>a⁰ = 1 · a⁻ⁿ = 1/aⁿ<br>27{fi('', '2/3')} = 3² = 9</div>
    </div>
    <p style="text-align:center;font-size:13pt;margin:0"><b>BIMDAS:</b> Brackets · Indices · ÷ × · + −</p>
    <p style="text-align:center;font-size:10pt;color:var(--muted)">Léim · leim.ie · Play Power Up: leim.ie/power-up.html</p>
  </div>
</div>

<div class="page ws">
  <div class="band"><div><div class="k">Worksheet</div><h1>Error Hunt + exam-style questions</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Error Hunt</h2>
  <p>Each answer has one mistake. Find it, say which rule was broken, and write the right answer.</p>
  <table class="eh"><thead><tr><th>Question</th><th>Student's working</th><th>The mistake and the right answer</th></tr></thead><tbody>
  {"".join(f"<tr><td>{q}</td><td>{w}</td><td><span class='gap'></span><span class='gap'></span></td></tr>" for q, w, r, g, b in ERR)}
  </tbody></table>
  <h2>B. Exam-style questions (show all your work)</h2>
  <ol class="q">{"".join(f"<li>{q}<span class='long'></span><span class='long'></span>{'<span class=long></span>' if len(q) > 60 else ''}</li>" for q, w in W)}</ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">For the teacher</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>Index Law Match</h2>
  <p style="font-size:9.6pt">{" · ".join(f"{q} = <b>{a}</b>" for q, a in MATCH)}</p>
  <h2>Standard Form Line-Up (smallest first)</h2>
  <p style="font-size:9.6pt">{" &lt; ".join(order)}</p>
  <h2>A. Error Hunt</h2>
  <table><tbody>{"".join(f"<tr><td style='width:34%'><b>{q}</b>: {w}</td><td>{r}</td></tr>" for q, w, r, g, b in ERR)}</tbody></table>
  <h2>B. Exam-style questions</h2>
  <ol class="q">{"".join(f"<li>{w}</li>" for q, w in W)}</ol>
  <h2>Marking tip</h2>
  <p>As in the exam, give credit for showing the law (3⁵⁺⁴⁻⁶) even if the final value slips, and expect answers in the form asked for: a value of 12 × 10⁷ is correct but not in standard form.</p>
</div>
</body></html>"""

cover = """<!doctype html><html><head><meta charset="utf-8"><style>
body{margin:0;width:1200px;height:1200px;background:#1B2430;font-family:Inter,sans-serif;color:#fff;display:flex;flex-direction:column;justify-content:space-between;padding:90px;box-sizing:border-box}
.k{display:inline-block;background:#2E7D57;border-radius:99px;padding:12px 26px;font-weight:700;font-size:28px;letter-spacing:.06em;text-transform:uppercase}
h1{font-size:108px;font-weight:800;line-height:1.12;letter-spacing:-.03em;margin:40px 0 0}
h1 span{background:#F6CF5A;color:#1B2430;padding:0 14px;box-decoration-break:clone;-webkit-box-decoration-break:clone}
.sub{font-size:38px;color:#C9D1DA;margin-top:36px;line-height:1.35}
.em{font-size:50px;margin-top:30px;font-weight:800;letter-spacing:.01em;color:#F6CF5A}
.foot{display:flex;justify-content:space-between;align-items:center;font-size:34px;font-weight:700}
.price{background:#F6CF5A;color:#1B2430;border-radius:16px;padding:14px 28px}
</style></head><body>
<div><span class="k">Junior Cycle Maths · Teacher pack</span>
<h1><span>Indices &amp;</span><br><span>Standard Form</span></h1>
<div class="sub">Index Law Match · Standard Form Line-Up<br>Index Dominoes · Poster · Worksheet + answers</div>
<div class="em">2³ × 2⁴ = 2⁷ &nbsp;·&nbsp; 45,000 = 4.5 × 10⁴</div></div>
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
    pdf("teacher-pack", os.path.join(OUT, "Indices-and-Standard-Form-Teacher-Pack-Leim.pdf"))
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--hide-scrollbars", "--window-size=1200,1200",
                    f"--screenshot={os.path.join(OUT, f'{SLUG}-cover.png')}", f"{SLUG}-cover.html"], cwd=SRC, check=True, capture_output=True)
    print("domino chain:", chain)
