#!/usr/bin/env python3
"""Factorising (JC Maths topic 27, AF.3d): free sheet + teacher pack + Payhip cover.
Run from the repo root: python3 src/build_factorising_pdfs.py OUTDIR   (needs: pip install --break-system-packages sympy)
Writes src/factorising-*.html; PDFs/cover PNG go to OUTDIR (free sheet also to printables/).
Every answer is asserted with the game checker's own tests (src/test_factor_match.py): it must multiply back to the
question AND be fully factorised."""
import os, sys, random, subprocess, re
import sympy as sp
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC)
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/factorising"; os.makedirs(OUT, exist_ok=True)
SLUG = "factorising"
LO = "AF.3d"
_t = open(os.path.join(SRC, "test_factor_match.py"), encoding="utf-8").read()
exec(_t[:_t.index("d = json.load")])          # E(), is_full(), split_f(), is_dots()
def eq(a, b): return sp.expand(E(a) - E(b)) == 0
def fac(q, a):
    """a must multiply back to q AND be fully factorised."""
    assert eq(q, a), (q, a)
    assert is_full(a), ("not fully factorised", a)
    return a
def notfull(q, a):
    assert eq(q, a) and not is_full(a), (q, a)
def n(x): return ("−" + str(-x)) if x < 0 else str(x)

# ---------- free sheet ----------
A = [("8x + 12", "4(2x + 3)"), ("15a − 10", "5(3a − 2)"), ("x² + 7x", "x(x + 7)"), ("6x² − 9x", "3x(2x − 3)"),
     ("4ab + 6ac", "2a(2b + 3c)"), ("10xy − 15yz", "5y(2x − 3z)"), ("3p² + p", "p(3p + 1)"), ("6ab + 9ac − 3a", "3a(2b + 3c − 1)")]
A = [(q, fac(q, a)) for q, a in A]
B = [("ax + ay + bx + by", "(x + y)(a + b)"), ("xy + 2x + 5y + 10", "(y + 2)(x + 5)"), ("ab − 3a + 4b − 12", "(b − 3)(a + 4)"),
     ("pq + 6p − 2q − 12", "(q + 6)(p − 2)"), ("3xy − 6x + y − 2", "(y − 2)(3x + 1)"), ("ax − ay − bx + by", "(x − y)(a − b)")]
B = [(q, fac(q, a)) for q, a in B]
C = [("x² + 7x + 12", "(x + 3)(x + 4)"), ("x² + 8x + 15", "(x + 3)(x + 5)"), ("x² − 9x + 20", "(x − 4)(x − 5)"), ("x² + 3x − 10", "(x + 5)(x − 2)"),
     ("x² − 2x − 24", "(x + 4)(x − 6)"), ("x² − 11x + 18", "(x − 2)(x − 9)"), ("<i>HL</i> 2x² + 7x + 3", "(2x + 1)(x + 3)"), ("<i>HL</i> 3x² − 10x − 8", "(3x + 2)(x − 4)")]
C = [(q, fac(re.sub(r"<i>HL</i> ", "", q), a)) for q, a in C]
D = [("x² − 36", "(x − 6)(x + 6)"), ("y² − 1", "(y − 1)(y + 1)"), ("<i>HL</i> 9x² − 25", "(3x − 5)(3x + 5)"), ("<i>HL</i> 4a² − 49b²", "(2a − 7b)(2a + 7b)"),
     ("Factorise fully: 3x² − 12", "3(x − 2)(x + 2)"), ("Factorise fully: 2x² + 10x + 12", "2(x + 2)(x + 3)")]
D = [(q, fac(re.sub(r"^(<i>HL</i> |Factorise fully: )", "", q), a)) for q, a in D]
assert 65**2 - 35**2 == 30 * 100 == 3000
notfull("5x² + 10x", "5(x² + 2x)"); fac("5x² + 10x", "5x(x + 2)")
D += [("Use factorising to work out 65² − 35² without a calculator.", "(65 − 35)(65 + 35) = 30 × 100 = 3,000"),
      ("Seán says 5x² + 10x = 5(x² + 2x) is fully factorised. Is he right?", "No: x² + 2x still has x in both terms. 5x(x + 2)")]
# exam-style
fac("6x² − 15x", "3x(2x − 5)"); fac("xy + 4x − 3y − 12", "(y + 4)(x − 3)"); fac("x² − 64", "(x − 8)(x + 8)")
fac("x² − 2x − 35", "(x + 5)(x − 7)"); assert (12 + 5) * (12 - 7) == 12**2 - 2 * 12 - 35 == 85
fac("x² + 6x + 9", "(x + 3)(x + 3)"); assert eq("(x + 3)²", "x² + 6x + 9")
fac("4x² − 100", "4(x − 5)(x + 5)"); fac("2x² − 3x − 5", "(2x − 5)(x + 1)")
E4 = [("Factorise (a) 6x² − 15x (b) xy + 4x − 3y − 12 (c) x² − 64.", "(a) <b>3x(2x − 5)</b> (b) x(y + 4) − 3(y + 4) = <b>(y + 4)(x − 3)</b> (c) <b>(x − 8)(x + 8)</b>"),
      ("A rectangle has area x² − 2x − 35 cm². Its length is x + 5 cm. (a) Find its width. (b) Find the length, the width and the area when x = 12 and check.",
       "(a) (x + 5)(x − 7), so width <b>x − 7</b> cm (b) 17 cm × 5 cm = 85 cm²; 144 − 24 − 35 = <b>85</b> ✓"),
      ("(a) Factorise x² + 6x + 9. (b) What shape has area x² + 6x + 9? Give its side length.", "(a) <b>(x + 3)(x + 3)</b> = (x + 3)² (b) a <b>square</b> with sides x + 3"),
      ("(a) Factorise fully 4x² − 100. (b) <i>Higher Level.</i> Factorise 2x² − 3x − 5 and check with x = 2.", "(a) 4(x² − 25) = <b>4(x − 5)(x + 5)</b> (b) <b>(2x − 5)(x + 1)</b>; x = 2: 8 − 6 − 5 = −3 and (−1)(3) = −3 ✓")]
assert 2 * 4 - 6 - 5 == -3 == (4 - 5) * (2 + 1)

def qs(items, cls=""): return "".join(f"<li>{q} <span class='line'></span></li>" for q, a in items)
sheet = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Factorising, rules and practice | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>@page{{@bottom-left{{content:"Léim · leim.ie · Free to print for home or class · JC Maths LO (2018 spec): {LO}"}}}}
.tight{{font-size:10.6pt;line-height:1.45}}.tight td,.tight th{{padding:3px 6px}}.tight h2{{margin:10px 0 4px;font-size:13.5pt}}.tight .note,.tight .tip{{padding:6px 10px;margin:6px 0}}.tight p{{margin:3px 0}}
ol.q{{padding-left:30px}}ol.q li{{margin:7px 0}}
.ans td{{padding:3px 6px;font-size:9.2pt}}
.p2{{font-size:9.6pt;line-height:1.4}}.p2 ol.q li{{margin:6px 0}}.p2 h2{{margin:8px 0 4px;font-size:13pt}}.p2 .line{{min-width:70px}}
.fp4{{display:grid;grid-template-columns:1fr 1fr;gap:2mm;margin:2mm 0}}.fp4 div{{border:1.5px solid var(--line);border-radius:6px;padding:1.5mm 2mm;text-align:center;font-weight:700}}.fp4 .y{{background:var(--cream)}}
</style></head><body>
<div class="page tight">
  <div class="band"><div><div class="k">Junior Cycle Maths · Free revision sheet</div><h1>Factorising</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcome (2018 specification): {LO}. Play the game: <b>leim.ie/factor-match.html</b></p>
  <p>Factorising is expanding <b>backwards</b>: put the brackets back. <b>Always check by multiplying out.</b></p>
  <div class="two">
   <div><h2>1. Highest common factor (HCF)</h2>
    <p>Find the biggest number and the letters in <b>every</b> term (smallest power). Put it outside; divide each term by it.</p>
    <table><tbody><tr><td>6x + 9</td><td><b>3(2x + 3)</b></td></tr><tr><td>4x² − 10x</td><td><b>2x(2x − 5)</b></td></tr>
    <tr><td>6ab + 9ac − 3a</td><td><b>3a(2b + 3c − 1)</b> (keep the 1)</td></tr><tr><td>HCF of 12x²y, 18xy²</td><td><b>6xy</b></td></tr></tbody></table>
    <p><b>Fully</b> factorised: nothing more can come out. 2(2x² − 5x) is <b>not</b> fully factorised.</p>
    <h2>2. Grouping (four terms)</h2>
    <p>xy − 3x + 2y − 6<br>= x(y − 3) + 2(y − 3)<br>= <b>(y − 3)(x + 2)</b></p>
    <p>A minus in front of the second pair: 2ab + 8a − 3b − 12 = 2a(b + 4) <b>− 3</b>(b + 4) = <b>(b + 4)(2a − 3)</b>.</p>
    <h2>4. Difference of two squares</h2>
    <p><b>a² − b² = (a − b)(a + b)</b><br>x² − 49 = <b>(x − 7)(x + 7)</b><br>2x² − 18 = 2(x² − 9) = <b>2(x − 3)(x + 3)</b><br><i>HL:</i> 9x² − 4y² = <b>(3x − 2y)(3x + 2y)</b><br>53² − 47² = 6 × 100 = <b>600</b></p></div>
   <div><h2>3. x² + bx + c</h2>
    <p>Find two numbers that <b>multiply</b> to c and <b>add</b> to b. x² + 8x + 12: pairs for 12:</p>
    <div class="fp4"><div>1, 12 → 13</div><div class="y">2, 6 → 8 ✓</div><div>3, 4 → 7</div><div>−2, −6 → −8</div></div>
    <p>So x² + 8x + 12 = <b>(x + 2)(x + 6)</b>.</p>
    <p><b>Signs:</b> c positive → both numbers have the sign of b. c negative → one +, one −.<br>x² − 9x + 14 = <b>(x − 2)(x − 7)</b><br>x² + 2x − 15 = <b>(x + 5)(x − 3)</b></p>
    <p><b>Common factor first:</b> 3x² + 15x + 18 = 3(x² + 5x + 6) = <b>3(x + 2)(x + 3)</b></p>
    <p><b>Higher Level: ax² + bx + c.</b> Try brackets that give the first and last terms; check the middle. 2x² + 7x + 3 → (2x + 1)(x + 3): middle 6x + x = 7x ✓. (2x + 3)(x + 1) gives 5x ✗.</p>
    <h2>Which method?</h2>
    <p>1. Common factor first, always. 2. Two terms, a minus, both squares → difference of two squares. 3. Three terms → x² + bx + c. 4. Four terms → grouping. Then <b>check by multiplying out</b>.</p></div>
  </div>
  <div class="tip"><b>Exam tip:</b> show the middle line in grouping, watch the signs (x² − x − 12 = (x + 3)(x − 4)), and check with x = 1: the question and your answer must give the same number.</div>
</div>

<div class="page p2">
  <div class="band"><div><div class="k">Practice · 34 questions</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <div class="two"><div><h2>A. Common factor: factorise</h2><ol class="q">{qs(A)}</ol></div>
  <div><h2>B. Grouping: factorise</h2><ol class="q" start="9">{qs(B)}</ol></div></div>
  <div class="two"><div><h2>C. x² + bx + c: factorise</h2><ol class="q" start="15">{qs(C)}</ol></div>
  <div><h2>D. Squares and "fully"</h2><ol class="q" start="23">{qs(D)}</ol></div></div>
  <p class="small" style="margin-top:6px"><i>HL</i> = Higher Level. Questions 31–34 are on the next page.</p>
</div>

<div class="page">
  <div class="band"><div><div class="k">Exam-style · then check</div><h1>Exam corner + answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>E. Exam-style questions (show your work)</h2>
  <ol class="q" start="31">{"".join(f"<li>{q}<span class='long'></span><span class='long'></span></li>" for q,a in E4)}</ol>
  <h2 style="margin-top:12px">Answers</h2>
  <table class="ans"><tbody>
   <tr><td><b>A</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(A,1))}</td></tr>
   <tr><td><b>B</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(B,9))}</td></tr>
   <tr><td><b>C</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(C,15))}</td></tr>
   <tr><td><b>D</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(D,23))}</td></tr>
   <tr><td><b>E</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(E4,31))}</td></tr>
  </tbody></table>
  <div class="note"><b>Got one wrong?</b> Multiply your answer out: does it give the question back? Did you take out the <b>highest</b> common factor? Did you lose a 1? Are the signs right (multiply to c, add to b)? Then play <b>Factor Match</b> at leim.ie/factor-match.html: the "Go back over these" list at the end shows the rule for each mistake.</div>
  <p class="small">All questions written by Léim. Léim is independent and not connected with the State Examinations Commission or the NCCA.</p>
</div>
</body></html>"""

# ---------- teacher pack ----------
# Factor Relay: each runner works on the previous runner's answer
def relay_check():
    fac("2x² + 6x", "2x(x + 3)"); assert eq("(x + 3)²", "x² + 6x + 9"); fac("x² + 6x + 9 − 25", "(x + 8)(x − 2)"); assert (12 + 8) * (12 - 2) == 200
    fac("x² − 16", "(x − 4)(x + 4)"); assert eq("(x + 4)(x + 2)", "x² + 6x + 8"); fac("3x² + 18x + 24", "3(x + 2)(x + 4)"); assert 3 * 8 * 10 == 240
relay_check()
RELAY = {
 "A": [("Factorise fully 2x² + 6x.", "2x(x + 3)"),
       ("Take the bracket from your answer, square it and expand: (bracket)².", "x² + 6x + 9"),
       ("Subtract 25 from your answer, then factorise.", "(x + 8)(x − 2)"),
       ("Find the value of your answer when x = 12.", "200")],
 "B": [("Factorise x² − 16.", "(x − 4)(x + 4)"),
       ("Take the bracket with the + sign, multiply it by (x + 2) and expand.", "x² + 6x + 8"),
       ("Multiply your answer by 3, then factorise fully.", "3(x + 2)(x + 4)"),
       ("Find the value of your answer when x = 6.", "240")]}
# Factor Match mingle: 12 pairs
MATCH = [("x² + 5x + 6", "(x + 2)(x + 3)"), ("x² + 7x + 6", "(x + 1)(x + 6)"), ("x² − 5x + 6", "(x − 2)(x − 3)"), ("x² + x − 6", "(x + 3)(x − 2)"),
         ("x² − x − 6", "(x − 3)(x + 2)"), ("x² − 9", "(x − 3)(x + 3)"), ("x² + 3x", "x(x + 3)"), ("3x² − 9x", "3x(x − 3)"),
         ("xy + 3x + 2y + 6", "(y + 3)(x + 2)"), ("2x² + 7x + 6", "(2x + 3)(x + 2)"), ("2x² − 18", "2(x − 3)(x + 3)"), ("4x² − 9", "(2x − 3)(2x + 3)")]
for q, a in MATCH: fac(q, a)
for q, a in MATCH: assert sum(eq(q, b) for _, b in MATCH) == 1, q
assert len(set(str(E(a)) for _, a in MATCH)) == 12
cards = [q for q, a in MATCH] + [a for q, a in MATCH]
random.seed(27); match_print = cards[:]; random.shuffle(match_print)
match_html = "".join(f'<div class="c"><span class="tag">Card {i}</span><div class="fc{" md" if len(x) > 14 else ""}">{x}</div></div>' for i, x in enumerate(match_print, 1))
idx = {x: i for i, x in enumerate(match_print, 1)}
match_key = " · ".join(f"{idx[q]}↔{idx[a]}" for q, a in MATCH)

DOMS = [("Factorise 5x + 20", "5(x + 4)"), ("Factorise x² − 8x", "x(x − 8)"), ("Factorise 6x² + 4x", "2x(3x + 2)"), ("HCF of 8a²b and 12ab²", "4ab"),
        ("Factorise x² + 9x + 20", "(x + 4)(x + 5)"), ("Factorise x² − 7x + 10", "(x − 2)(x − 5)"), ("Factorise x² + 4x − 21", "(x + 7)(x − 3)"), ("Factorise x² − 3x − 28", "(x − 7)(x + 4)"),
        ("Factorise x² − 25", "(x − 5)(x + 5)"), ("Factorise x² − 100", "(x − 10)(x + 10)"), ("Factorise ab + 2a + 3b + 6", "(b + 2)(a + 3)"), ("Factorise xy − 4x + y − 4", "(y − 4)(x + 1)"),
        ("Factorise fully 4x² − 36", "4(x − 3)(x + 3)"), ("Factorise fully 3x² + 3x − 6", "3(x + 2)(x − 1)"), ("41² − 39² = ?", "160"), ("Two numbers: × to 24, + to −11", "−3 and −8"),
        ("(x + 6)(x + □) = x² + 4x − 12", "−2"), ("Factorise 9x² − 1", "(3x − 1)(3x + 1)"), ("HL: factorise 2x² + 5x + 2", "(2x + 1)(x + 2)"), ("Factorise 7p² − p", "p(7p − 1)")]
for q, a in DOMS:
    if q.startswith("HCF"): assert sp.gcd(E("8a²b"), E("12ab²")) == E(a)
    elif q.startswith("41²"): assert 41**2 - 39**2 == 160
    elif q.startswith("Two numbers"): assert -3 * -8 == 24 and -3 + -8 == -11
    elif q.startswith("(x + 6)"): assert sp.solve(E("(x + 6)(x + □)") - E("x² + 4x − 12"), Bx) == [-2]
    else: fac(re.sub(r"^(HL: factorise|Factorise fully|Factorise) ", "", q), a)
ANS = [a for q, a in DOMS]; assert len(set(ANS)) == 20
random.seed(2727); chain = DOMS[:]; random.shuffle(chain)
dom = [("START" if k == 0 else chain[k - 1][1], x[0]) for k, x in enumerate(chain)] + [(chain[-1][1], "FINISH")]
dom_print = dom[:]; random.shuffle(dom_print)
dom_html = "".join(f'<div class="dom"><div class="h l{" sm" if len(l) > 13 else ""}">{l}</div><div class="h r{" sm" if len(r) > 26 else ""}">{r}</div></div>' for l, r in dom_print)
chain_key = "".join(f"<li>{x} = <b>{a}</b></li>" for x, a in chain)

ERR = [("Factorise 6ab + 9ac − 3a", "= 3a(2b + 3c)", "3a ÷ 3a = 1, not 0: <b>3a(2b + 3c − 1)</b>"),
       ("Factorise fully 8x² + 12x", "= 4(2x² + 3x)", "x is still in both terms: <b>4x(2x + 3)</b>"),
       ("Factorise x² − 5x + 6", "= (x + 2)(x + 3)", "they add to +5, not −5: <b>(x − 2)(x − 3)</b>"),
       ("Factorise x² − 16", "= (x − 4)(x − 4)", "that gives x² − 8x + 16: <b>(x − 4)(x + 4)</b>"),
       ("Factorise x² + x − 12", "= (x + 3)(x − 4)", "3 + −4 = −1, not +1: <b>(x − 3)(x + 4)</b>"),
       ("Factorise xy − 2x − 3y + 6", "= x(y − 2) − 3(y + 2)", "−3 × −2 = +6: x(y − 2) − 3(y − 2) = <b>(y − 2)(x − 3)</b>")]
for q, w, r in ERR:
    qq = re.sub(r"^Factorise (fully )?", "", q); wrong = w.replace("= ", ""); right = re.findall(r"<b>(.+?)</b>", r)[-1]
    assert (not eq(qq, wrong)) or (not is_full(wrong)), q
    fac(qq, right)
w1 = fac("10x² − 15x", "5x(2x − 3)"); w2 = fac("ab − 5a + 2b − 10", "(b − 5)(a + 2)"); w3 = fac("x² + x − 30", "(x + 6)(x − 5)")
assert 97**2 - 3**2 == 94 * 100 == 9400; w4b = fac("6x² − 54", "6(x − 3)(x + 3)")
w5 = fac("3x² + 11x − 4", "(3x − 1)(x + 4)"); assert 3 + 11 - 4 == 10 == (3 - 1) * (1 + 4)
assert 3 * 2**2 + 11 * 2 - 4 == 30 == (3 * 2 - 1) * (2 + 4)

pack_style = open(os.path.join(SRC, "build_ratio_pdfs.py"), encoding="utf-8").read()
pack_style = pack_style[pack_style.index("<style>", pack_style.index('pack = f"""')) + 7:pack_style.index("</style>", pack_style.index('pack = f"""'))]
pack_style = pack_style.replace("{{", "{").replace("}}", "}").replace("{LO}", LO)
pack_style += (".fym .c{height:15mm}.fym .fc{font-size:14pt}.fym .fc.md{font-size:12pt}.trk{border:2px dashed #9AA3AE;padding:2.5mm 4mm;margin-top:2mm;font-size:9.6pt}.trk ol{margin:1mm 0 0;padding-left:18px}.trk li{margin:1.8mm 0}"
               ".relays{display:grid;grid-template-columns:1fr 1fr;gap:3mm}.dom .l{font-size:11.5pt}.dom .l.sm{font-size:9.6pt;line-height:1.2}.dom .r.sm{font-size:9.6pt}")
pack = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Factorising Teacher Pack | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{pack_style}</style></head><body>

<div class="page p1">
  <div class="band"><div><div class="k">Junior Cycle Maths · Teacher pack</div><h1>Factorising</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcome (2018 specification): {LO} (expanding was Algebra 2, AF.3b; solving quadratics by factorising comes in Quadratic equations, AF.4)</p>
  <div class="two">
    <div><h3>Aims</h3><p>By the end of the lesson students can find the HCF of terms and take it out; factorise four terms by grouping; factorise x² + bx + c; recognise and factorise a difference of two squares; factorise fully; and check every answer by multiplying out. Higher Level: ax² + bx + c and a²x² − b²y².</p></div>
    <div><h3>In this pack</h3><p>p.1 Teacher notes · p.2 Factor Relay + Factor Match mingle cards · p.3 Factorising Dominoes (cut-up) · p.4 Wall poster · p.5 Worksheet: Error Hunt + exam-style questions · p.6 Answers. Level: 3rd year (Higher and Ordinary). Time: about 60 minutes. All questions are original.</p></div>
  </div>
  <h2 style="margin-top:8px">Procedure</h2>
  <table class="proc"><tbody>
    <tr><td>6 min</td><td><b>Lead-in: "undo it".</b> Write 3(x + 4), x(x − 5), (x + 2)(x + 3) on the board and have pairs expand them. Then rub out the questions and leave only 3x + 12, x² − 5x, x² + 5x + 6: "Put the brackets back." Factorising is expanding backwards.</td></tr>
    <tr><td>8 min</td><td><b>Guided discovery.</b> Pairs expand (x + 2)(x + 3), (x + 1)(x + 6), (x − 2)(x − 3), (x + 6)(x − 1). What do the bracket numbers do to make the middle and last numbers? (Add; multiply.) Then they factorise x² + 8x + 12 by listing the pairs that multiply to 12.</td></tr>
    <tr><td>10 min</td><td><b>Factor Match mingle</b> (p.2, 24 cards = 12 pairs; one card each). Expression cards find their factorised form and vice versa. Pairs prove the match by multiplying out. Feedback: the three cards with 6 at the end, and why (x − 3)(x + 3) is only two terms.</td></tr>
    <tr><td>10 min</td><td><b>Factor Relay</b> (p.2), teams of 4 in a line. Runner 1 does step 1 and passes the answer (not the card) to runner 2, and so on. The last runner brings the final number to you: if it's wrong, the team finds the broken step.</td></tr>
    <tr><td>10 min</td><td><b>Factorising Dominoes</b> (p.3), groups of 3–4: start with START, work out the clue, find the domino with that answer on its left and build the chain to FINISH.</td></tr>
    <tr><td>13 min</td><td><b>Worksheet</b> (p.5). Error Hunt in pairs (find the mistake, name the rule, fix it), then the exam-style questions alone.</td></tr>
    <tr><td>3 min</td><td><b>Exit ticket.</b> Factorise fully 5x² − 20x; factorise x² − x − 20 (5x(x − 4); (x − 5)(x + 4)). Homework: play <b>Factor Match</b> at leim.ie/factor-match.html (Squares &amp; checks round) and copy three lines from the "Go back over these" list.</td></tr>
  </tbody></table>
  <div class="note"><b>Factor Match key (card numbers):</b> {match_key}.<br>
  <b>Errors to look for:</b> losing the 1 (3a(2b + 3c)) · not fully factorised (2(2x² − 5x)) · signs in x² − 5x + 6 · (x − 4)(x − 4) for x² − 16 · the second pair in grouping taken out with the wrong sign · x² + 9 "factorised" as (x + 3)(x + 3). <b>Support:</b> list the factor pairs in a table; draw the area model backwards; multiply out every answer. <b>Fast finishers:</b> 12x² − 27, x⁴ − 16, or explain why x² + 4 can't be factorised.</div>
  <p class="small"><b>Factor Relay answers:</b> A: {" → ".join(a for q, a in RELAY["A"])} · B: {" → ".join(a for q, a in RELAY["B"])}. <b>Domino answer chain</b> (START → FINISH):</p>
  <ol class="small" style="columns:2;column-gap:12px;font-size:7.6pt;line-height:1.3;margin:0;padding-left:16px">{chain_key}</ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">One relay per team of 4 · one match card per student</div><h1>Factor Relay + Factor Match</h1></div><div class="logo">↗ Léim</div></div>
  <div class="relays">{"".join(f'<div class="trk"><b>Factor Relay {k}.</b> Cut into 4 strips. Each runner uses the answer passed to them.<ol>' + "".join(f"<li><b>Runner {i}:</b> {q}</li>" for i, (q, a) in enumerate(st, 1)) + "</ol></div>" for k, st in RELAY.items())}</div>
  <p style="font-size:9.5pt;margin:3mm 0 0"><b>Factor Match.</b> Cut out the 24 cards and give one to each student. Expression card? Find the person with its factorised form. Brackets card? Find your expression. Prove it by multiplying out. (Fewer students? Take out whole pairs.)</p>
  <div class="fym">{match_html}</div>
</div>

<div class="page">
  <div class="band"><div><div class="k">Groups of 3–4 · cut along the dashed lines</div><h1>Factorising Dominoes</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.5pt">Start with START. Work out the clue on the right, then find the domino with that answer on its left. Keep going until you reach FINISH. No calculators!</p>
  <div class="doms">{dom_html}</div>
</div>

<div class="page">
  <div class="poster">
    <h1>Factorising</h1>
    <div class="big3"><div>6x + 9<span>= 3(2x + 3)</span></div><div>x² + 5x + 6<span>= (x + 2)(x + 3)</span></div><div>x² − 49<span>= (x − 7)(x + 7)</span></div></div>
    <div class="ops">
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>1. Common factor</b>always first<br>4x² − 10x = 2x(2x − 5)</div>
      <div style="background:var(--green-soft)"><b>2. Four terms: grouping</b>xy − 3x + 2y − 6<br>= x(y − 3) + 2(y − 3) = (y − 3)(x + 2)</div>
      <div style="background:var(--green-soft)"><b>3. Three terms</b>× to c, + to b<br>x² − x − 12 = (x + 3)(x − 4)</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>4. Two squares, a minus</b>a² − b² = (a − b)(a + b)<br>9x² − 4 = (3x − 2)(3x + 2)</div>
    </div>
    <p style="text-align:center;font-size:13pt;margin:0"><b>Check: multiply your answer out. You must get the question back.</b></p>
    <p style="text-align:center;font-size:10pt;color:var(--muted)">Léim · leim.ie · Play Factor Match: leim.ie/factor-match.html</p>
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
    <li>Factorise fully 10x² − 15x.<span class="long"></span></li>
    <li>Factorise ab − 5a + 2b − 10.<span class="long"></span></li>
    <li>A rectangle has area x² + x − 30 m². (a) Factorise x² + x − 30. (b) The width is x − 5 m. Write the length.<span class="long"></span><span class="long"></span></li>
    <li>(a) Use factorising to work out 97² − 3² without a calculator. (b) Factorise fully 6x² − 54.<span class="long"></span><span class="long"></span></li>
    <li><i>Higher Level.</i> Factorise 3x² + 11x − 4, and check your answer with x = 2.<span class="long"></span></li>
  </ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">For the teacher</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>Factor Relay</h2>
  <ol class="q">
    <li><b>Relay A:</b> {" → ".join(a for q, a in RELAY["A"])} (x² + 6x + 9 − 25 = x² + 6x − 16; (12 + 8)(12 − 2) = 20 × 10)</li>
    <li><b>Relay B:</b> {" → ".join(a for q, a in RELAY["B"])} (3x² + 18x + 24 = 3(x² + 6x + 8); 3 × 8 × 10)</li>
  </ol>
  <h2>A. Error Hunt</h2>
  <table><tbody>{"".join(f"<tr><td style='width:38%'><b>{q}</b> {w}</td><td>{r}</td></tr>" for q,w,r in ERR)}</tbody></table>
  <h2>B. Exam-style questions</h2>
  <ol class="q">
    <li>HCF = 5x: <b>{w1}</b></li>
    <li>a(b − 5) + 2(b − 5) = <b>{w2}</b></li>
    <li>(a) × to −30, + to 1: 6 and −5, <b>{w3}</b> (b) length <b>x + 6</b> m</li>
    <li>(a) (97 − 3)(97 + 3) = 94 × 100 = <b>9,400</b> (b) 6(x² − 9) = <b>{w4b}</b></li>
    <li>× to −12, check the middle: (3x − 1)(x + 4) gives 12x − x = 11x ✓. <b>{w5}</b>. Check with x = 2: 12 + 22 − 4 = 30 and (6 − 1)(2 + 4) = 5 × 6 = 30 ✓</li>
  </ol>
  <h2>Marking tip</h2>
  <p>Give credit for each step, as the exam does: the middle line in grouping and a correct factor pair earn marks even if the final brackets slip. Accept the brackets in either order and (x + 3)² for (x + 3)(x + 3). "Factorise fully" needs the highest common factor out first.</p>
</div>
</body></html>"""

cover = """<!doctype html><html><head><meta charset="utf-8"><style>
body{margin:0;width:1200px;height:1200px;background:#1B2430;font-family:Inter,sans-serif;color:#fff;display:flex;flex-direction:column;justify-content:space-between;padding:90px;box-sizing:border-box}
.k{display:inline-block;background:#2E7D57;border-radius:99px;padding:12px 26px;font-weight:700;font-size:28px;letter-spacing:.06em;text-transform:uppercase}
h1{font-size:120px;font-weight:800;line-height:1.12;letter-spacing:-.03em;margin:40px 0 0}
h1 span{background:#F6CF5A;color:#1B2430;padding:0 14px;box-decoration-break:clone;-webkit-box-decoration-break:clone}
.sub{font-size:38px;color:#C9D1DA;margin-top:36px;line-height:1.35}
.em{font-size:50px;margin-top:30px;font-weight:800;letter-spacing:.01em;color:#F6CF5A}
.foot{display:flex;justify-content:space-between;align-items:center;font-size:34px;font-weight:700}
.price{background:#F6CF5A;color:#1B2430;border-radius:16px;padding:14px 28px}
</style></head><body>
<div><span class="k">Junior Cycle Maths · Teacher pack</span>
<h1><span>Factorising</span></h1>
<div class="sub">Factor Relay · Factor Match mingle cards<br>Factorising Dominoes · Poster · Worksheet + answers</div>
<div class="em">x² + 5x + 6 = (x + 2)(x + 3)</div></div>
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
    pdf("teacher-pack", os.path.join(OUT, "Factorising-Teacher-Pack-Leim.pdf"))
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--hide-scrollbars", "--window-size=1200,1200",
                    f"--screenshot={os.path.join(OUT, f'{SLUG}-cover.png')}", f"{SLUG}-cover.html"], cwd=SRC, check=True, capture_output=True)
    print("domino chain:", [(x, a) for x, a in chain])
