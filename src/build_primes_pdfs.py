#!/usr/bin/env python3
"""Factors, multiples & primes (JC Maths topic 2): free sheet + teacher pack + Payhip cover.
Run from the repo root: python3 src/build_primes_pdfs.py OUTDIR
Writes src/factors-multiples-primes-*.html; PDFs/cover PNG go to OUTDIR (free sheet also to printables/).
Every answer is computed and asserted."""
import os, sys, random, subprocess, re
from math import gcd
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC)
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/primes"; os.makedirs(OUT, exist_ok=True)
SLUG = "factors-multiples-primes"
LO = "N.1d"
SUP = {2: "²", 3: "³", 4: "⁴", 5: "⁵", 6: "⁶"}
def isP(n): return n > 1 and all(n % i for i in range(2, int(n ** .5) + 1))
def lcm(a, b): return a * b // gcd(a, b)
def divs(n): return [i for i in range(1, n + 1) if n % i == 0]
def pf(n):
    o, d = {}, 2
    while n > 1:
        while n % d == 0: o[d] = o.get(d, 0) + 1; n //= d
        d += 1
    return o
def idx(n): return " × ".join(f"{p}{SUP.get(k, '') if k > 1 else ''}" for p, k in sorted(pf(n).items()))
def longf(n): return " × ".join(str(p) for p, k in sorted(pf(n).items()) for _ in range(k))
def j(xs): return ", ".join(str(x) for x in xs)

# ---------- free sheet ----------
circ = [2, 9, 17, 21, 29, 33, 41, 51]
A = [(f"Circle the primes: {j(circ)}", j([x for x in circ if isP(x)])),
     ("Why is 1 not a prime number?", "it has only one factor (a prime has exactly two)"),
     ("Is 87 prime? Explain.", "No: 8 + 7 = 15, so 87 divides by 3 (87 = 3 × 29)"),
     ("List the primes between 50 and 70.", j([x for x in range(51, 70) if isP(x)])),
     ("Which is the only even prime number?", "2"),
     ("Is 91 prime? Explain.", "No: 91 = 7 × 13")]
assert A[0][1] == "2, 17, 29, 41" and A[3][1] == "53, 59, 61, 67" and 87 == 3 * 29 and 91 == 7 * 13
B = [("List all the factors of 24.", j(divs(24))), ("List all the factors of 45.", j(divs(45))),
     ("List all the factors of 64.", j(divs(64))), ("Write the first five multiples of 7.", j([7 * i for i in range(1, 6)])),
     ("Is 84 a multiple of 6? How do you know?", f"Yes: 6 × 14 = 84"), ("How many factors does 100 have?", str(len(divs(100)))),
     ("Which multiple of 8 is between 50 and 60?", j([x for x in range(51, 60) if x % 8 == 0])),
     ("Write down a common factor of 18 and 30 (not 1).", "2, 3 or 6")]
assert 84 % 6 == 0 and 84 // 6 == 14 and B[6][1] == "56" and B[5][1] == "9"
Cn = [36, 48, 75, 84, 120, 200, 252, 300]
Dp = [("HCF", 18, 24), ("LCM", 18, 24), ("HCF", 20, 32), ("LCM", 20, 32), ("HCF", 45, 60), ("LCM", 6, 8), ("HCF", 56, 70), ("LCM", 15, 25)]
def hl(t, a, b): return gcd(a, b) if t == "HCF" else lcm(a, b)
assert [hl(*x) for x in Dp] == [6, 72, 4, 160, 15, 24, 14, 75]
E = [("The 46 bus stops outside the school every 15 minutes and the 47 every 20 minutes. Both stop there at 3:30 p.m. When will they next both stop there together?",
      f"LCM of 15 and 20 = {lcm(15,20)} minutes, so 4:30 p.m."),
     ("Saoirse has 36 red beads and 54 blue beads. She makes identical bracelets using all the beads. What is the greatest number of bracelets, and how many of each colour are on each?",
      f"HCF = {gcd(36,54)} bracelets, each with {36//gcd(36,54)} red and {54//gcd(36,54)} blue"),
     ("A floor is 240 cm by 180 cm. It is covered with square tiles, all the same size, with no cutting. What is the largest tile that can be used, and how many tiles are needed?",
      f"HCF = {gcd(240,180)} cm; {240//gcd(240,180)} × {180//gcd(240,180)} = {(240//gcd(240,180))*(180//gcd(240,180))} tiles"),
     ("a = 2³ × 3 × 5 and b = 2² × 3² × 7. Find the HCF and the LCM of a and b. Leave your answers in index form.",
      "HCF = 2² × 3 (= 12) · LCM = 2³ × 3² × 5 × 7 (= 2520)")]
a_, b_ = 8 * 3 * 5, 4 * 9 * 7
assert lcm(15, 20) == 60 and gcd(a_, b_) == 12 and lcm(a_, b_) == 2520 and idx(12) == "2² × 3" and idx(2520) == "2³ × 3² × 5 × 7"
assert gcd(36, 54) == 18 and gcd(240, 180) == 60

def qs(items, start):
    return "".join(f"<li>{q} <span class='line'></span></li>" for q, a in items)

sheet = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Factors, multiples and primes: rules and practice | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>@page{{@bottom-left{{content:"Léim · leim.ie · Free to print for home or class · JC Maths LO (2018 spec): {LO}"}}}}
.tight{{font-size:10.6pt;line-height:1.48}}.tight td{{padding:3px 6px}}.tight h2{{margin:12px 0 6px;font-size:14pt}}.tight .note,.tight .tip{{padding:6px 10px;margin:6px 0}}
ol.q li{{margin:7px 0}}.cols{{columns:2;column-gap:12mm}}.cols li{{break-inside:avoid}}
.ans td{{padding:3px 6px;font-size:9.4pt}}
</style></head><body>
<div class="page tight">
  <div class="band"><div><div class="k">Junior Cycle Maths · Free revision sheet</div><h1>Factors, multiples &amp; primes</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcome (2018 specification): {LO}. Play the game: <b>leim.ie/prime-smash.html</b></p>
  <div class="two">
   <div><h2>1. Factors and multiples</h2>
    <p>A <b>factor</b> divides in exactly: the factors of 12 are 1, 2, 3, 4, 6, 12. A <b>multiple</b> is in the times table: multiples of 6 are 6, 12, 18, 24 …</p>
    <p><b>Find factors in pairs:</b> 36 = 1 × 36 = 2 × 18 = 3 × 12 = 4 × 9 = 6 × 6, so 36 has 9 factors.</p>
    <h2>2. Prime numbers</h2>
    <p>A <b>prime</b> has exactly two factors: 1 and itself. Primes up to 50: <b>2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47</b>.</p>
    <div class="note"><b>1 is not prime</b> (one factor only). <b>2</b> is the only even prime. Watch out for 51 = 3 × 17, 57 = 3 × 19, 91 = 7 × 13.</div>
    <p><b>Quick tests:</b> ÷3 if the digits add to a multiple of 3 · ÷5 if it ends in 0 or 5 · to test a number, try primes up to its square root.</p></div>
   <div><h2>3. Factor trees</h2>
    <p>Split into any two factors and keep going until every branch is prime.</p>
    <table><tbody>
     <tr><td>360 = 10 × 36</td></tr><tr><td>10 = 2 × 5 · 36 = 4 × 9 = 2 × 2 × 3 × 3</td></tr>
     <tr><td>360 = 2 × 2 × 2 × 3 × 3 × 5 = <b>2³ × 3² × 5</b></td></tr>
    </tbody></table>
    <div class="note"><b>Finish the job:</b> 2² × 15 isn't a product of primes (15 = 3 × 5). And 2³ = 2 × 2 × 2 = 8, not 6.</div>
    <h2>4. HCF and LCM</h2>
    <table><tbody>
     <tr><td><b>HCF</b></td><td>biggest number that goes into both · HCF(12, 18) = 6</td></tr>
     <tr><td><b>LCM</b></td><td>smallest number both go into · LCM(12, 18) = 36</td></tr>
    </tbody></table></div>
  </div>
  <h2>5. HCF and LCM with primes</h2>
  <p>84 = 2² × 3 × 7 and 90 = 2 × 3² × 5. <b>HCF:</b> shared primes, smaller power → 2 × 3 = <b>6</b>. <b>LCM:</b> every prime, bigger power → 2² × 3² × 5 × 7 = <b>1260</b>. Check: HCF × LCM = 84 × 90 = 7560 ✓</p>
  <div class="tip"><b>Which one?</b> "Together again", "at the same time" → <b>LCM</b>. "Biggest equal groups", "largest size", "nothing left over" → <b>HCF</b>. <b>Exam tip:</b> show your factor tree (part marks), give the answer in the form asked (index form, a time of day), and multiply back to check.</div>
</div>

<div class="page">
  <div class="band"><div><div class="k">Practice · 34 questions</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <div class="two"><div><h2>A. Primes</h2><ol class="q">{qs(A,1)}</ol></div>
  <div><h2>B. Factors and multiples</h2><ol class="q" start="7">{qs(B,7)}</ol></div></div>
  <h2>C. Write as a product of primes in index form (show the tree)</h2><ol class="q cols" start="15">{"".join(f"<li>{n} = <span class='line' style='min-width:110px'></span></li>" for n in Cn)}</ol>
  <h2>D. HCF and LCM</h2><ol class="q cols" start="23">{"".join(f"<li>The {t} of {a} and {b} = <span class='line' style='min-width:60px'></span></li>" for t,a,b in Dp)}</ol>
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
   <tr><td><b>C</b></td><td>{" · ".join(f"{i}. {idx(n)}" for i,n in enumerate(Cn,15))}</td></tr>
   <tr><td><b>D</b></td><td>{" · ".join(f"{i}. {hl(t,a,b)}" for i,(t,a,b) in enumerate(Dp,23))}</td></tr>
   <tr><td><b>E</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(E,31))}</td></tr>
  </tbody></table>
  <div class="note"><b>Got one wrong?</b> Check: is every factor in your answer prime? Did you mix up HCF (small, goes into both) and LCM (big, both go into it)? Then play <b>Prime Smash</b> at leim.ie/prime-smash.html: the "Go back over these" list at the end shows the rule for each mistake.</div>
  <p class="small">All questions written by Léim. Léim is independent and not connected with the State Examinations Commission or the NCCA.</p>
</div>
</body></html>"""

# ---------- teacher pack ----------
# Number Detective: each clue must have exactly one answer in 1..200 (brute-force checked)
DET = [("I am prime. I am between 20 and 30. My digits add up to 11.", lambda n: isP(n) and 20 < n < 30 and sum(map(int, str(n))) == 11),
       ("I am the HCF of 24 and 36.", lambda n: n == gcd(24, 36)),
       ("I am the LCM of 6 and 8.", lambda n: n == lcm(6, 8)),
       ("I am a factor of 56 and a multiple of 7. I have two digits and I am less than 20.", lambda n: 56 % n == 0 and n % 7 == 0 and 10 <= n < 20),
       ("I have exactly 3 factors. I am between 20 and 30.", lambda n: len(divs(n)) == 3 and 20 < n < 30),
       ("I am the smallest number that 2, 3 and 5 all go into.", lambda n: n == lcm(lcm(2, 3), 5)),
       ("I am 2³ × 3².", lambda n: n == 8 * 9),
       ("I am the only even prime.", lambda n: isP(n) and n % 2 == 0),
       ("I am a prime between 90 and 100.", lambda n: isP(n) and 90 < n < 100),
       ("I am odd and not prime. I am the product of two different primes that add up to 10.", lambda n: n % 2 == 1 and any(isP(p) and isP(q) and p != q and p + q == 10 and p * q == n for p in range(2, 10) for q in range(2, 10))),
       ("I am a multiple of 9 and a factor of 108. I am between 30 and 40.", lambda n: n % 9 == 0 and 108 % n == 0 and 30 < n < 40),
       ("I am a square number with exactly 5 factors. I am less than 50.", lambda n: int(n ** .5) ** 2 == n and len(divs(n)) == 5 and n < 50)]
DETANS = []
for t, fn in DET:
    sols = [n for n in range(1, 201) if fn(n)]; assert len(sols) == 1, (t, sols); DETANS.append(sols[0])
assert DETANS == [29, 12, 24, 14, 25, 30, 72, 2, 97, 21, 36, 16], DETANS
det_html = "".join(f'<div class="c"><span class="tag">Detective card {"ABCDEFGHIJKL"[k]}</span>{t}<span class="me">I am ______</span></div>' for k, (t, fn) in enumerate(DET))
det_key = " · ".join(f"{'ABCDEFGHIJKL'[k]} {DETANS[k]}" for k in range(12))
line_key = " → ".join(f"{a} ({'ABCDEFGHIJKL'[k]})" for k, a in sorted(enumerate(DETANS), key=lambda x: x[1]))

# Sieve grid 1-100
sieve = "".join(f"<div>{n}</div>" for n in range(1, 101))
PR100 = [n for n in range(2, 101) if isP(n)]; assert len(PR100) == 25

# Dominoes: 20 clues with distinct answers, chained START → FINISH
DOMS = [("HCF of 12 and 18", gcd(12, 18)), ("LCM of 4 and 10", lcm(4, 10)), ("HCF of 28 and 42", gcd(28, 42)), ("LCM of 6 and 9", lcm(6, 9)),
        ("HCF of 45 and 75", gcd(45, 75)), ("LCM of 8 and 12", lcm(8, 12)), ("HCF of 36 and 48", gcd(36, 48)), ("LCM of 5 and 7", lcm(5, 7)),
        ("HCF of 40 and 64", gcd(40, 64)), ("LCM of 3 and 10", lcm(3, 10)), ("2³ × 5", 40), ("3² × 5", 45),
        ("the 7th prime", [n for n in range(2, 100) if isP(n)][6]), ("the number of factors of 36", len(divs(36))), ("2 × 3 × 7", 42), ("LCM of 10 and 25", lcm(10, 25)),
        ("HCF of 26 and 39", gcd(26, 39)), ("the first prime after 20", next(n for n in range(21, 50) if isP(n))), ("HCF of 16 and 28", gcd(16, 28)), ("LCM of 9 and 12", lcm(9, 12))]
dv = [v for x, v in DOMS]; assert len(set(dv)) == 20, sorted(dv)
assert dict(DOMS)["2³ × 5"] == 2 ** 3 * 5 and dict(DOMS)["3² × 5"] == 9 * 5 and dict(DOMS)["2 × 3 × 7"] == 42
random.seed(2)
chain = DOMS[:]; random.shuffle(chain)
dom = [("START" if k == 0 else str(chain[k - 1][1]), x) for k, (x, v) in enumerate(chain)] + [(str(chain[-1][1]), "FINISH")]
dom_print = dom[:]; random.shuffle(dom_print)
dom_html = "".join(f'<div class="dom"><div class="h l">{l}</div><div class="h r">{r}</div></div>' for l, r in dom_print)
chain_key = "".join(f"<li>{x} = <b>{v}</b></li>" for x, v in chain)

# Error hunt
ERR = [("Is 51 prime?", "Yes: it's odd and it isn't in the 5 times table.", "No: 5 + 1 = 6, so it divides by 3. <b>51 = 3 × 17</b>"),
       ("60 as a product of primes", "60 = 2² × 15", "15 isn't prime: <b>60 = 2² × 3 × 5</b>"),
       ("HCF of 12 and 18", "36", "36 is the LCM. The HCF (biggest number into both) is <b>6</b>"),
       ("LCM of 6 and 8", "48", "48 is a common multiple, but not the lowest: <b>24</b>"),
       ("2³ × 5", "= 6 × 5 = 30", "2³ = 2 × 2 × 2 = 8, so <b>40</b>"),
       ("All the factors of 18", "2, 3, 6, 9", "Missed 1 and 18 itself: <b>1, 2, 3, 6, 9, 18</b>")]
assert gcd(12, 18) == 6 and lcm(12, 18) == 36 and lcm(6, 8) == 24 and divs(18) == [1, 2, 3, 6, 9, 18] and 51 == 3 * 17
assert idx(180) == "2² × 3² × 5" and idx(168) == "2³ × 3 × 7" and gcd(180, 168) == 12 and lcm(180, 168) == 2520
assert lcm(15, 25) == 75 and 600 // 75 == 8 and gcd(360, 210) == 30 and (360 // 30) * (210 // 30) == 84
assert [n for n in range(101, 120) if n % 21 == 0] == [105]

TREE = """<svg viewBox="0 0 300 200" style="height:52mm;width:auto" xmlns="http://www.w3.org/2000/svg" font-family="Inter,sans-serif" font-weight="800" text-anchor="middle">
<g stroke="#1B2430" stroke-width="2"><line x1="150" y1="30" x2="85" y2="68"/><line x1="150" y1="30" x2="215" y2="68"/><line x1="85" y1="90" x2="55" y2="128"/><line x1="85" y1="90" x2="115" y2="128"/><line x1="215" y1="90" x2="175" y2="128"/><line x1="215" y1="90" x2="255" y2="128"/><line x1="175" y1="150" x2="155" y2="172"/><line x1="175" y1="150" x2="195" y2="172"/><line x1="255" y1="150" x2="235" y2="172"/><line x1="255" y1="150" x2="275" y2="172"/></g>
<text x="150" y="24" font-size="22">360</text><text x="85" y="86" font-size="20">10</text><text x="215" y="86" font-size="20">36</text>
<g fill="#E7F3EC" stroke="#2E7D57" stroke-width="2.5"><circle cx="55" cy="140" r="15"/><circle cx="115" cy="140" r="15"/><circle cx="155" cy="185" r="13"/><circle cx="195" cy="185" r="13"/><circle cx="235" cy="185" r="13"/><circle cx="275" cy="185" r="13"/></g>
<g font-size="17"><text x="55" y="146">2</text><text x="115" y="146">5</text><text x="155" y="191">2</text><text x="195" y="191">2</text><text x="235" y="191">3</text><text x="275" y="191">3</text></g>
<text x="175" y="146" font-size="18">4</text><text x="255" y="146" font-size="18">9</text></svg>"""
VENN = """<svg viewBox="0 0 320 190" style="height:52mm;width:auto" xmlns="http://www.w3.org/2000/svg" font-family="Inter,sans-serif" text-anchor="middle">
<circle cx="115" cy="100" r="80" fill="#F6CF5A" fill-opacity=".35" stroke="#1B2430" stroke-width="2.5"/><circle cx="205" cy="100" r="80" fill="#2E7D57" fill-opacity=".22" stroke="#1B2430" stroke-width="2.5"/>
<text x="80" y="14" font-size="15" font-weight="800">84</text><text x="240" y="14" font-size="15" font-weight="800">90</text>
<g font-size="22" font-weight="800"><text x="80" y="95">2</text><text x="80" y="125">7</text><text x="160" y="95">2</text><text x="160" y="125">3</text><text x="240" y="95">3</text><text x="240" y="125">5</text></g></svg>"""

pack = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Factors, Multiples & Primes Teacher Pack | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>
@page{{@bottom-left{{content:"Léim · leim.ie · Single-teacher licence · JC Maths LO (2018 spec): {LO}";font-size:7pt}}}}
.proc td{{font-size:8.9pt;padding:3px 6px;line-height:1.32}}.proc td:first-child{{white-space:nowrap;font-weight:700;color:var(--green)}}
.p1 .note{{font-size:8.7pt;padding:6px 10px;line-height:1.35}}.p1 p{{font-size:9.5pt}}
.sieve{{display:grid;grid-template-columns:repeat(10,1fr);width:132mm;margin:3mm auto 0}}
.sieve div{{border:1px solid #9AA3AE;margin:-1px 0 0 -1px;height:11.5mm;display:flex;align-items:center;justify-content:center;font-size:13pt;font-weight:700}}
.fym{{display:grid;grid-template-columns:repeat(4,1fr);margin-top:3mm}}
.fym .c{{border:2px dashed #9AA3AE;margin:-1px 0 0 -1px;height:30mm;position:relative;padding:6mm 3mm 3mm;font-size:8.6pt;line-height:1.3;font-weight:600}}
.fym .tag{{position:absolute;top:1.5mm;left:3mm;font-size:6.8pt;color:var(--green);font-weight:800;text-transform:uppercase;letter-spacing:.04em}}
.fym .me{{position:absolute;bottom:2mm;left:3mm;font-size:8pt;color:var(--muted)}}
.doms{{display:grid;grid-template-columns:1fr 1fr;gap:2mm 6mm}}
.dom{{display:grid;grid-template-columns:1fr 1.9fr;border:2px dashed #9AA3AE;height:18.5mm}}
.dom .h{{display:flex;align-items:center;justify-content:center;text-align:center;padding:2mm;font-size:15pt;font-weight:800}}
.dom .r{{font-size:11.5pt;line-height:1.2}}
.dom .l{{background:var(--mist);border-right:2px solid var(--ink)}}
.poster{{height:255mm;border:6px solid var(--night);border-radius:18px;padding:10mm;display:flex;flex-direction:column;justify-content:space-between}}
.poster h1{{font-size:34pt;text-align:center}}
.pgrid{{display:grid;grid-template-columns:repeat(9,1fr);gap:2mm}}.pgrid div{{background:var(--night);color:#F6CF5A;border-radius:8px;text-align:center;font-size:15pt;font-weight:800;padding:1.5mm 0}}
.pp{{display:grid;grid-template-columns:1fr 1fr;gap:5mm;align-items:center}}.pp>div{{text-align:center;font-size:11.5pt;line-height:1.35}}
.hl2{{display:grid;grid-template-columns:1fr 1fr;gap:4mm}}.hl2 div{{border-radius:14px;padding:4mm;text-align:center;font-size:11.5pt;line-height:1.35}}.hl2 b{{display:block;font-size:22pt;font-weight:800}}
.ws{{font-size:10pt;line-height:1.42}}.ws ol.q li{{margin:6px 0}}.ws .long{{height:22px}}
.eh td{{padding:5px 8px;font-size:9.8pt}}.eh td:first-child{{font-weight:700;width:24%}}.eh .gap{{display:block;border-bottom:1px solid #9AA3AE;height:16px}}
</style></head><body>

<div class="page p1">
  <div class="band"><div><div class="k">Junior Cycle Maths · Teacher pack</div><h1>Factors, multiples &amp; primes</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcome (2018 specification): {LO} (also used in N.1a fractions and AF.3 factorising)</p>
  <div class="two">
    <div><h3>Aims</h3><p>By the end of the lesson students can find all the factors of a number in pairs, list multiples, explain what a prime is (and why 1 isn't one), write a number as a product of primes in index form using a factor tree, find the HCF and LCM of two numbers, and decide which one a word problem needs.</p></div>
    <div><h3>In this pack</h3><p>p.1 Teacher notes · p.2 Sieve of Eratosthenes + Number Detective cards · p.3 HCF &amp; LCM Dominoes (cut-up) · p.4 Wall poster · p.5 Worksheet: Error Hunt + exam-style questions · p.6 Answers. Level: 1st year (Higher and Ordinary), or 3rd-year revision. Time: about 60 minutes. All questions are original.</p></div>
  </div>
  <h2 style="margin-top:8px">Procedure</h2>
  <table class="proc"><tbody>
    <tr><td>5 min</td><td><b>Lead-in: Rectangles.</b> Pairs use 12 counters (or squares on grid paper) to make every possible rectangle: 1 × 12, 2 × 6, 3 × 4. Now try 7, then 9. Which numbers make only one rectangle? Those are the primes. Elicit <i>factor</i>, <i>factor pair</i>, <i>prime</i>.</td></tr>
    <tr><td>10 min</td><td><b>Guided discovery: the Sieve</b> (p.2, one per student). Cross out 1. Circle 2 and cross out every other multiple of 2; circle 3 and cross out its multiples; then 5, then 7. Everything left is prime (25 primes). Ask: why can we stop at 7? (11 × 11 = 121 &gt; 100.) Why is 2 the only even prime?</td></tr>
    <tr><td>12 min</td><td><b>Number Detective line-up</b> (p.2, cut up). One card per student (or one per pair). Each works out their mystery number, checks it with a neighbour, then the class lines up in order of the numbers. The class reads the clues out in order to check. Model the factor tree for 360 and HCF/LCM with the Venn diagram on the poster (p.4) before the next step.</td></tr>
    <tr><td>12 min</td><td><b>HCF &amp; LCM Dominoes</b> (p.3), groups of 3–4. Start with START, work out the clue, find the domino with that answer on its left and build the chain to FINISH. Answer chain below.</td></tr>
    <tr><td>15 min</td><td><b>Worksheet</b> (p.5). Error Hunt in pairs (find the mistake, name the rule, fix it), then the exam-style questions alone. Feedback: which questions needed the HCF and which the LCM, and how could you tell?</td></tr>
    <tr><td>5 min</td><td><b>Exit ticket.</b> Write 72 as a product of primes in index form and find the HCF of 72 and 60 (2³ × 3²; 12). Homework: play <b>Prime Smash</b> at leim.ie/prime-smash.html (HCF &amp; LCM round) and copy three lines from the "Go back over these" list.</td></tr>
  </tbody></table>
  <div class="note"><b>Number Detective key:</b> {det_key}. <b>Line-up order:</b> {line_key}.<br>
  <b>Errors to look for:</b> calling 1 prime · thinking every odd number is prime (51, 57, 87, 91) · leaving a composite in the "product of primes" (2² × 15) · 2³ = 6 · mixing up HCF and LCM, or giving a common multiple that isn't the lowest (48 for 6 and 8) · missing 1 and the number itself from a factor list · in word problems, giving "60" when the question asks for a time. <b>Support:</b> multiplication square on the desk. <b>Fast finishers:</b> find two primes that differ by 2 (twin primes) above 50; or find every number below 100 with exactly 3 factors (4, 9, 25, 49: squares of primes). Why does that work?</div>
  <p class="small"><b>Domino answer chain</b> (START → FINISH):</p>
  <ol class="small" style="columns:3;column-gap:12px;font-size:7.8pt;line-height:1.35;margin:0;padding-left:16px">{chain_key}</ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">Each student · then cut up the cards</div><h1>Sieve of Eratosthenes + Number Detective</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.5pt"><b>The Sieve.</b> Cross out 1. Circle 2, then cross out every multiple of 2. Circle 3 and cross out its multiples. Do the same for 5 and 7. Circle every number that's left: those are the primes up to 100. How many are there?</p>
  <div class="sieve">{sieve}</div>
  <p style="font-size:9.5pt;margin-top:4mm"><b>Number Detective.</b> Cut out the cards. Work out your mystery number, check it with a partner, then line up in order.</p>
  <div class="fym">{det_html}</div>
</div>

<div class="page">
  <div class="band"><div><div class="k">Groups of 3–4 · cut along the dashed lines</div><h1>HCF &amp; LCM Dominoes</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.5pt">Start with START. Work out the clue on the right, then find the domino with that answer on its left. Keep going until you reach FINISH. No calculators!</p>
  <div class="doms">{dom_html}</div>
</div>

<div class="page">
  <div class="poster">
    <h1>Primes, HCF &amp; LCM</h1>
    <div><p style="text-align:center;font-size:12pt;margin-bottom:3mm"><b>A prime has exactly two factors.</b> 1 is not prime · 2 is the only even prime</p>
    <div class="pgrid">{"".join(f"<div>{p}</div>" for p in PR100)}</div></div>
    <div class="pp">
      <div>{TREE}<br><b>360 = 2³ × 3² × 5</b><br>Keep splitting until every branch is prime.</div>
      <div>{VENN}<br>84 = 2² × 3 × 7 · 90 = 2 × 3² × 5<br><b>HCF</b> = middle = 2 × 3 = 6<br><b>LCM</b> = all of it = 2² × 3² × 5 × 7 = 1260</div>
    </div>
    <div class="hl2">
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>HCF</b>Highest Common Factor<br>"biggest equal groups", "largest size", "nothing left over"</div>
      <div style="background:var(--green-soft)"><b>LCM</b>Lowest Common Multiple<br>"together again", "at the same time", "the next time both…"</div>
    </div>
    <p style="text-align:center;font-size:10pt;color:var(--muted)">Léim · leim.ie · Play Prime Smash: leim.ie/prime-smash.html</p>
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
    <li>(a) Write 180 and 168 as products of primes in index form. (b) Find the HCF of 180 and 168. (c) Find the LCM of 180 and 168.<span class="long"></span><span class="long"></span></li>
    <li>Two lighthouses flash together at 9 p.m. One flashes every 15 seconds and the other every 25 seconds. (a) After how many seconds do they next flash together? (b) How many more times will they flash together in the next 10 minutes?<span class="long"></span><span class="long"></span></li>
    <li>A patio is 360 cm long and 210 cm wide. It will be covered with identical square slabs, with no cutting. Find the largest slab that can be used, and how many slabs are needed.<span class="long"></span><span class="long"></span></li>
    <li>Ciarán says, "Every prime number is odd." Is he right? Give a reason.<span class="long"></span></li>
    <li>Find the number between 100 and 120 that has both 3 and 7 as factors.<span class="long"></span></li>
  </ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">For the teacher</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>Sieve of Eratosthenes</h2>
  <p>The 25 primes up to 100: {j(PR100)}.</p>
  <h2>A. Error Hunt</h2>
  <table><tbody>{"".join(f"<tr><td style='width:28%'><b>{q}</b></td><td>{r}</td></tr>" for q,w,r in ERR)}</tbody></table>
  <h2>B. Exam-style questions</h2>
  <ol class="q">
    <li>(a) 180 = <b>{idx(180)}</b> and 168 = <b>{idx(168)}</b>. (b) HCF = 2² × 3 = <b>{gcd(180,168)}</b>. (c) LCM = 2³ × 3² × 5 × 7 = <b>{lcm(180,168)}</b>. Check: 12 × 2520 = 30 240 = 180 × 168.</li>
    <li>(a) LCM of 15 and 25 = <b>{lcm(15,25)} seconds</b>. (b) 10 minutes = 600 seconds; 600 ÷ 75 = <b>{600//lcm(15,25)} times</b>.</li>
    <li>HCF of 360 and 210 = <b>{gcd(360,210)} cm</b> slabs; {360//gcd(360,210)} × {210//gcd(360,210)} = <b>{(360//gcd(360,210))*(210//gcd(360,210))} slabs</b>.</li>
    <li><b>No:</b> 2 is prime (factors 1 and 2) and it is even.</li>
    <li>It must be a multiple of 3 × 7 = 21: 21, 42, 63, 84, <b>105</b>.</li>
  </ol>
  <h2>Marking tip</h2>
  <p>Give credit for each correct step, as the exam does: a correct factor tree with one slip should still earn most of the marks. In word problems, ask students to write "HCF" or "LCM" and why before they calculate.</p>
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
<h1>Factors, multiples &amp; <span>primes</span></h1>
<div class="sub">Sieve of Eratosthenes + Number Detective<br>HCF &amp; LCM Dominoes · Poster · Worksheet + answers</div>
<div class="em">360 = 2³ × 3² × 5 · HCF · LCM</div></div>
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
    pdf("teacher-pack", os.path.join(OUT, "Factors-Multiples-and-Primes-Teacher-Pack-Leim.pdf"))
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--hide-scrollbars", "--window-size=1200,1200",
                    f"--screenshot={os.path.join(OUT, f'{SLUG}-cover.png')}", f"{SLUG}-cover.html"], cwd=SRC, check=True, capture_output=True)
    print("domino chain:", chain)
