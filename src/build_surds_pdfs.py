#!/usr/bin/env python3
"""Surds (JC Maths topic 37): free sheet + teacher pack + Payhip cover.
Run from the repo root: python3 src/build_surds_pdfs.py OUTDIR
Writes src/surds-*.html; PDFs/cover PNG go to OUTDIR (free sheet also to printables/).
Every answer is checked with test_surd_simplify.py's own maths (val = exact value, simplest = simplest form).
Styles are read from src/build_money1_pdfs.py."""
import os, sys, random, subprocess, re
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC)
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/surds"; os.makedirs(OUT, exist_ok=True)
SLUG = "surds"
LO = "N.1b, U.13"
GAME = "leim.ie/surd-simplify.html"

_ns = {}; exec(open(os.path.join(SRC, "test_surd_simplify.py"), encoding="utf-8").read().split("def main")[0], _ns)
val, simplest = _ns["val"], _ns["simplest"]
import sympy as sp
def same(a, b): return sp.simplify(val(a) - val(b)) == 0
def ok(q, a):
    """a is the simplest-form value of q"""
    assert same(q, a), (q, a, val(q)); assert simplest(a), ("not simplest", a); return a
def root(n): return "√" + str(n)

# ---------- free sheet ----------
A = [("√8", "2√2"), ("√12", "2√3"), ("√18", "3√2"), ("√20", "2√5"), ("√27", "3√3"), ("√45", "3√5"), ("√50", "5√2"), ("√75", "5√3")]
B = [("√32", "4√2"), ("√48", "4√3"), ("√72", "6√2"), ("√98", "7√2")]
for q, a in A + B: ok(q, a)
Cq = [("2√3", "√12"), ("3√2", "√18"), ("5√2", "√50")]
for q, a in Cq: assert same(q, a)
D = [("4√3 + 2√3", "6√3"), ("7√5 − 3√5", "4√5"), ("√8 + √18", "5√2"), ("√12 + √27", "5√3"), ("√50 − √8", "3√2")]
for q, a in D: ok(q, a)
D_cant = "√2 + √3"; assert val(D_cant) == sp.sqrt(2) + sp.sqrt(3)
E = [("√3 × √12", "6"), ("√2 × √5", "√10"), ("2√3 × 4√2", "8√6"), ("(3√5)²", "45"), ("√60 ÷ √5", "2√3"), ("6√10 ÷ 2√2", "3√5")]
for q, a in E: ok(q, a)
Fh = [("√2(3 + √2)", "2 + 3√2"), ("(4 + √3)(4 − √3)", "13"), ("(2 + √5)²", "9 + 4√5")]
for q, a in Fh: ok(q, a)
G1 = ok("√(9 + 36)".replace("√(9 + 36)", "√45"), "3√5"); assert 3 ** 2 + 6 ** 2 == 45
G2a = ok("√8 × √18", "12"); G2b = ok("2√8 + 2√18", "10√2")

def qs(items): return "".join(f"<li>{q} <span class='line'></span></li>" for q in items)
def style(var):
    return re.search(var + r' = f"""<!doctype.*?<style>(.*?)</style>', open(os.path.join(SRC, "build_money1_pdfs.py"), encoding="utf-8").read(), re.S).group(1).replace("{LO}", LO).replace("{{", "{").replace("}}", "}")
SHEET_STYLE = style("sheet"); PACK_STYLE = style("pack")
assert "@bottom-left" in SHEET_STYLE and "Single-teacher licence" in PACK_STYLE
EXTRA = """.wk{font-variant-numeric:tabular-nums;line-height:1.5;border:1.5px solid var(--line);border-radius:8px;padding:2px 7px;margin:3px 0;font-size:9.4pt}.wk b.h{display:block}
table.st{border-collapse:collapse;margin:3px 0;font-size:9.4pt}table.st td,table.st th{border:1px solid #C9D1DA;padding:2px 7px;text-align:center}"""
SPOT = '<table class="st"><tr><td>√4 × √9 = 2 × 3 = 6</td><td>√36 = 6</td></tr><tr><td>√4 × √25 = 2 × 5 = 10</td><td>√100 = 10</td></tr><tr><td>√9 + √16 = 3 + 4 = 7</td><td>√25 = 5 (not 7!)</td></tr></table>'
assert same("√4 × √9", "√36") and same("√4 × √25", "√100") and not same("√9 + √16", "√25")

sheet = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Surds: rules and practice | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{SHEET_STYLE}
{EXTRA}
</style></head><body>
<div class="page tight">
  <div class="band"><div><div class="k">Junior Cycle Maths · Free revision sheet</div><h1>Surds</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2018 specification): {LO}. Play the game: <b>{GAME}</b></p>
  <div class="two">
   <div><h2>1. What is a surd?</h2>
    <p>A square root that never comes out exact: √2, √3, √5, √12 … &nbsp;√9 = 3 and √25 = 5 are <b>not</b> surds. Leave answers "in surd form" (exact): √2, not 1.41.</p>
    <h2>2. Spot the pattern</h2>
    {SPOT}
    <p><b>√a × √b = √(ab)</b>, but <b>√a + √b ≠ √(a + b)</b>.</p>
    <h2>3. The rules</h2>
    <div class="wk"><b class="h">Multiply: √a × √b = √(ab)</b>√2 × √8 = √16 = 4</div>
    <div class="wk"><b class="h">Divide: √a ÷ √b = √(a ÷ b)</b>√50 ÷ √2 = √25 = 5</div>
    <div class="wk"><b class="h">Square: (√a)² = a</b>(√7)² = 7 &nbsp;·&nbsp; (3√2)² = 9 × 2 = 18</div>
    <h2>4. Simplifying</h2>
    <p>Find the <b>biggest square number</b> that goes in: 4, 9, 16, 25, 36, 49, 64 …</p>
    <div class="wk">√72 = √(36 × 2) = √36 × √2 = <b>6√2</b><br>√48 = √(16 × 3) = <b>4√3</b> (2√12 is not finished)<br>Backwards: 3√5 = √9 × √5 = <b>√45</b></div></div>
   <div><h2>5. Adding and subtracting</h2>
    <p>Only <b>like surds</b> (same number under the root). Treat √2 like x: 3√2 + 5√2 = 8√2.</p>
    <div class="wk">√8 + √18 = 2√2 + 3√2 = <b>5√2</b> (simplify first)<br>√50 − √8 = 5√2 − 2√2 = <b>3√2</b><br>√2 + √3 <b>can't be simplified</b> (it is not √5)</div>
    <p><b>Multiply</b> numbers and roots separately: 2√3 × 5√2 = 10√6.</p>
    <h2>6. Higher Level: brackets</h2>
    <p>Expand like algebra. √3 × √3 = 3.</p>
    <div class="wk">√3(4 + √3) = 4√3 + 3 = <b>3 + 4√3</b><br>(5 + √2)(5 − √2) = 25 − 2 = <b>23</b> (middle terms cancel)<br>(1 + √2)² = 1 + √2 + √2 + 2 = <b>3 + 2√2</b></div>
    <div class="note"><b>Classic mistakes:</b> not using the biggest square (2√12) · √2 + √8 = √10 · 3√5 × 2√5 = 6√5 (it's 6 × 5 = 30) · (√6)² = 36 (it's 6) · (1 + √2)² = 1 + 2 (forgot the middle).</div></div>
  </div>
  <div class="tip"><b>Exam tip:</b> show the square you used: √72 = √36 × √2 = 6√2. "In the form a√b" means b must have no square factor left.</div>
</div>

<div class="page p2">
  <div class="band"><div><div class="k">Practice · 32 questions</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Simplify</h2><ol class="q" style="columns:4;column-gap:6mm">{qs(q for q, a in A)}</ol>
  <h2>B. Simplify (bigger squares)</h2><ol class="q" start="9" style="columns:4;column-gap:6mm">{qs(q for q, a in B)}</ol>
  <h2>C. Write as one square root</h2><ol class="q" start="13" style="columns:3;column-gap:6mm">{qs(q for q, a in Cq)}</ol>
  <h2>D. Add and subtract (or write "can't be simplified")</h2><ol class="q" start="16" style="columns:3;column-gap:6mm">{qs([q for q, a in D] + [D_cant])}</ol>
  <h2>E. Multiply and divide</h2><ol class="q" start="22" style="columns:3;column-gap:6mm">{qs(q for q, a in E)}</ol>
  <h2>F. Higher Level: expand and simplify</h2><ol class="q" start="28" style="columns:3;column-gap:6mm">{qs(q for q, a in Fh)}</ol>
  <h2>G. Exam-style (show your work)</h2>
  <ol class="q" start="31">
   <li>A right-angled triangle has shorter sides 3 cm and 6 cm. Find the longest side in the form a√b.<span class="long"></span><span class="long"></span></li>
   <li>A rectangle is √8 cm long and √18 cm wide. (a) Find its area. (b) Find its perimeter in the form a√b.<span class="long"></span><span class="long"></span></li>
  </ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">Check your work</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <table class="ans"><tbody>
   <tr><td><b>A</b></td><td>{" · ".join(f"{i}. {a}" for i, (q, a) in enumerate(A, 1))}</td></tr>
   <tr><td><b>B</b></td><td>{" · ".join(f"{i}. {a}" for i, (q, a) in enumerate(B, 9))} (16, 16, 36, 49 are the squares)</td></tr>
   <tr><td><b>C</b></td><td>{" · ".join(f"{i}. {a}" for i, (q, a) in enumerate(Cq, 13))}</td></tr>
   <tr><td><b>D</b></td><td>{" · ".join(f"{i}. {a}" for i, (q, a) in enumerate(D, 16))} · 21. can't be simplified (not like surds)</td></tr>
   <tr><td><b>E</b></td><td>{" · ".join(f"{i}. {a}" for i, (q, a) in enumerate(E, 22))}</td></tr>
   <tr><td><b>F</b></td><td>{" · ".join(f"{i}. {a}" for i, (q, a) in enumerate(Fh, 28))}</td></tr>
   <tr><td><b>G</b></td><td>31. c² = 9 + 36 = 45, c = √9 × √5 = <b>{G1} cm</b> · 32. (a) √8 × √18 = √144 = <b>{G2a} cm²</b> (b) 2√2 + 3√2 + 2√2 + 3√2 = <b>{G2b} cm</b></td></tr>
  </tbody></table>
  <h2>Worked examples</h2>
  <div class="two">
   <div class="wk"><b class="h">10. √48</b>Biggest square in 48: 16. √48 = √16 × √3 = 4√3.<br>(4 × 12 gives 2√12, then 2 × 2√3 = 4√3: same answer, more work.)</div>
   <div class="wk"><b class="h">18. √8 + √18</b>√8 = 2√2, √18 = 3√2. Now they are like surds: 2√2 + 3√2 = 5√2.</div>
   <div class="wk"><b class="h">24. 2√3 × 4√2</b>Numbers: 2 × 4 = 8. Roots: √3 × √2 = √6. Answer 8√6.</div>
   <div class="wk"><b class="h">30. (2 + √5)²</b>(2 + √5)(2 + √5) = 4 + 2√5 + 2√5 + 5 = 9 + 4√5.</div>
  </div>
  <div class="note"><b>Got one wrong?</b> Did you use the biggest square? Did you simplify before adding? Did you multiply the numbers in front separately? Then play <b>Surd Simplify</b> at {GAME}: the "Go back over these" list at the end shows the rule for each mistake.</div>
  <p class="small">All questions written by Léim. Léim is independent and not connected with the State Examinations Commission or the NCCA.</p>
</div>
</body></html>"""
NQ = len(A) + len(B) + len(Cq) + len(D) + 1 + len(E) + len(Fh) + 2; assert NQ == 32, NQ
assert same("√48", "4√3") and same("2 × 2√3", "4√3") and same("2√3 × 4√2", "8√6") and same("(2 + √5)(2 + √5)", "9 + 4√5")

# ---------- teacher pack ----------
MATCH = [("√8", "2√2"), ("√12", "2√3"), ("√18", "3√2"), ("√20", "2√5"), ("√27", "3√3"), ("√45", "3√5"),
         ("√50", "5√2"), ("√48", "4√3"), ("√72", "6√2"), ("√75", "5√3"), ("√2 × √8", "4"), ("(√7)²", "7")]
for i, (q, a) in enumerate(MATCH):   # each answer card fits its own question card and no other
    ok(q, a); assert [j for j in range(12) if same(MATCH[j][0], a)] == [i], (i, a)
random.seed(37); order = list(range(24)); random.shuffle(order)
cards = [("q", i) for i in range(12)] + [("a", i) for i in range(12)]
match_print = [cards[k] for k in order]
match_html = "".join(f'<div class="c"><span class="tag">Card {k}</span><div class="fc">{MATCH[i][1] if t == "a" else MATCH[i][0]}</div></div>' for k, (t, i) in enumerate(match_print, 1))
match_key = " · ".join(f"{match_print.index(('q', i)) + 1} → {match_print.index(('a', i)) + 1}" for i in range(12))

# Surd Swap: each fact on exactly ONE card
SW1 = [("Length", "√50 m", "A"), ("Width", "√8 m", "B"), ("Length as a√b", "", None), ("Width as a√b", "", None), ("Perimeter", "", None), ("Area", "", None)]
SW1_ans = [ok("√50", "5√2"), ok("√8", "2√2"), ok("2√50 + 2√8", "14√2"), ok("√50 × √8", "20")]
SW2 = [("Shorter side 1", "3 cm", "A"), ("Shorter side 2", "6 cm", "B"), ("Longest side (a√b)", "", None), ("Area", "", None)]
SW2_ans = [ok("√45", "3√5"), "9"]; assert 3 * 3 + 6 * 6 == 45 and 3 * 6 / 2 == 9
for rows in (SW1, SW2): assert sum(w == "A" for *_, w in rows) == 1 and sum(w == "B" for *_, w in rows) == 1
def swap_card(who):
    def tab(title, rows):
        return f'<table class="ss"><thead><tr><th colspan="2">{title}</th></tr></thead><tbody>' + "".join(
            f"<tr><td>{k}</td><td><b>{v if w and who in w else ''}</b></td></tr>" for k, v, w in rows) + "</tbody></table>"
    return f'<div class="idc"><h3>Student {who} · Surd Swap</h3><div class="two">{tab("The garden (a rectangle)", SW1)}{tab("The ramp (a right-angled triangle)", SW2)}</div></div>'

# Surd Dominoes: 20 clues, 20 different answers (all checked)
DOMS = [("√8", "2√2"), ("√12", "2√3"), ("√18", "3√2"), ("√20", "2√5"), ("√27", "3√3"), ("√50", "5√2"), ("√48", "4√3"), ("√72", "6√2"),
        ("√2 × √8", "4"), ("√3 × √27", "9"), ("(√11)²", "11"), ("√2 × √3", "√6"), ("√5 + √20", "3√5"), ("√63 − √7", "2√7"),
        ("√90 ÷ √10", "3"), ("2√3 × 3√3", "18"), ("√42 ÷ √6", "√7"),
        ("Higher Level: (3 + √2)(3 − √2)", "7"), ("Higher Level: (1 + √3)²", "4 + 2√3"), ("Higher Level: √2(√2 + 5)", "2 + 5√2")]
for c, a in DOMS: ok(c.replace("Higher Level: ", ""), a)
DV = [val(a) for c, a in DOMS]; assert len(DOMS) == 20 and all(sp.simplify(DV[i] - DV[j]) != 0 for i in range(20) for j in range(i))
random.seed(3737); chain = DOMS[:]; random.shuffle(chain)
dom = [("START" if k == 0 else chain[k - 1][1], x[0]) for k, x in enumerate(chain)] + [(chain[-1][1], "FINISH")]
dom_print = dom[:]; random.shuffle(dom_print)
dom_html = "".join(f'<div class="dom"><div class="h l{" sm" if len(l) > 6 else ""}">{l}</div><div class="h r">{r}</div></div>' for l, r in dom_print)
chain_key = "".join(f"<li>{x} = <b>{a}</b></li>" for x, a in chain)

ERR = [("Simplify √72", "2√18", "18 still has a square in it. Use 36: √36 × √2 = <b>6√2</b>"),
       ("Simplify √2 + √8", "√10", "√a + √b ≠ √(a + b). √8 = 2√2, so √2 + 2√2 = <b>3√2</b>"),
       ("Work out 3√5 × 2√5", "6√5", "√5 × √5 = 5, so 6 × 5 = <b>30</b>"),
       ("Work out (√6)²", "36", "Squaring a root removes it: <b>6</b>"),
       ("Simplify √50 − √2", "√48", "Simplify first: 5√2 − √2 = <b>4√2</b>"),
       ("Higher Level: expand (2 + √3)²", "7", "Forgot the middle: 4 + 2√3 + 2√3 + 3 = <b>7 + 4√3</b>")]
for (q, w, r), good in zip(ERR, ["6√2", "3√2", "30", "6", "4√2", "7 + 4√3"]):
    e = re.sub(r"^(Higher Level: expand |Simplify |Work out )", "", q)
    ok(e, good); assert not same(e, w) or not simplest(w), (q, w)
# worksheet exam-style
WS = [ok("√50", "5√2"), ok("4 × 5√2", "20√2"), ok("√12 + √27 + √75", "10√3"), ok("2√3 + 3√3 + 5√3", "10√3"),
      ok("(2√3 + 1)(2√3 − 1)", "11"), ok("(√5 + 2)²", "9 + 4√5")]
assert val("4√3") ** 2 == 48 and val("3√5") ** 2 == 45 and 5 + 11 == 16

pack = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Surds Teacher Pack | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{PACK_STYLE}
{EXTRA}
.ss td:nth-child(2){{width:30%}}.ss td,.ss th{{padding:2px 5px;font-size:9pt;line-height:1.35}}.fym{{grid-template-columns:repeat(4,1fr)}}.fym .c{{height:14mm}}.fym .fc{{font-size:15pt}}.idc{{padding:1mm 4mm}}.idc h3{{margin:0 0 1mm}}.p1 .proc td{{font-size:8.6pt;padding:2px 6px}}
.dom .r{{font-size:11pt}}.dom .l{{font-size:15pt}}.dom .l.sm{{font-size:12pt}}.ops div{{font-size:13pt}}
</style></head><body>

<div class="page p1">
  <div class="band"><div><div class="k">Junior Cycle Maths · Teacher pack</div><h1>Surds</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2018 specification): {LO}</p>
  <div class="two">
    <div><h3>Aims</h3><p>By the end of the lesson students can say what a surd is, simplify surds using the biggest square factor, add and subtract like surds, and multiply, divide and square surds. Higher Level: expand brackets with surds, including (a + √b)(a − √b) and (a + √b)².</p></div>
    <div><h3>In this pack</h3><p>p.1 Teacher notes · p.2 Surd Match mingle cards + Surd Swap A/B cards · p.3 Surd Dominoes (cut-up) · p.4 Wall poster · p.5 Worksheet: Error Hunt + exam-style questions · p.6 Answers. Level: 3rd year (mostly Higher Level). Time: about 60 minutes. All questions are original.</p></div>
  </div>
  <h2 style="margin-top:8px">Procedure</h2>
  <table class="proc"><tbody>
    <tr><td>5 min</td><td><b>Lead-in: which is bigger?</b> Write 3√2 and 2√3 on the board. Students guess, then square both (18 and 12). Ask: why do calculators show √2 as 1.414213…? Elicit "it never ends": a surd.</td></tr>
    <tr><td>8 min</td><td><b>Guided discovery.</b> Pairs work out √4 × √9 and √36, √4 × √25 and √100, then √9 + √16 and √25. Elicit √a × √b = √(ab), but √a + √b ≠ √(a + b). Then use it backwards: √72 = √36 × √2 = 6√2.</td></tr>
    <tr><td>10 min</td><td><b>Surd Match mingle</b> (p.2, 24 cards = 12 question cards + 12 answer cards; one card each). Find your partner. Pairs then explain which square number they used.</td></tr>
    <tr><td>12 min</td><td><b>Surd Swap</b> (p.2, pairs, don't show your card). Each measurement is on only ONE card. Ask for what you're missing, then fill in the blanks together. Feedback: garden → <b>5√2, 2√2, 14√2 m, 20 m²</b>; ramp → <b>3√5 cm, 9 cm²</b>.</td></tr>
    <tr><td>10 min</td><td><b>Surd Dominoes</b> (p.3), groups of 3–4. Start with START, work out the clue, find the domino with that answer on its left, and build the chain to FINISH.</td></tr>
    <tr><td>12 min</td><td><b>Worksheet</b> (p.5). Error Hunt in pairs (find the mistake, name it, fix it), then the exam-style questions alone. Question 5 is Higher Level.</td></tr>
    <tr><td>3 min</td><td><b>Exit ticket.</b> Simplify √98 and √12 + √75. (7√2; 7√3.) Homework: play <b>Surd Simplify</b> at {GAME}.</td></tr>
  </tbody></table>
  <div class="note"><b>Mingle key</b> (question card → answer card): {match_key}.<br>
  <b>Errors to look for:</b> not the biggest square (2√12) · √a + √b = √(a + b) · 3√5 × 2√5 = 6√5 · (√6)² = 36 · forgetting the middle terms of (a + √b)². <b>Support:</b> a list of square numbers 4 to 100 on the desk. <b>Fast finishers:</b> which is bigger, 5√2 or 4√3? Explain without a calculator.</div>
  <p class="small"><b>Domino answer chain</b> (START → FINISH):</p>
  <ol class="small" style="columns:2;column-gap:12px;font-size:7.4pt;line-height:1.22;margin:0;padding-left:16px">{chain_key}</ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">Cut up the cards · one Surd Swap card per student</div><h1>Surd Match + Surd Swap</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:8.8pt;margin:0"><b>Surd Match mingle.</b> Cut out the 24 cards and give one to each student. Question card? Find its simplest form. Answer card? Find your question. (Fewer students? Take out whole pairs.)</p>
  <div class="fym">{match_html}</div>
  <p style="font-size:8.8pt;margin:3mm 0 0"><b>Surd Swap.</b> Don't show your card. Each measurement is on only one of the two cards: ask your partner for what you're missing, then fill in every blank together. Give answers in surd form.</p>
  {swap_card("A")}
  {swap_card("B")}
</div>

<div class="page">
  <div class="band"><div><div class="k">Groups of 3–4 · cut along the dashed lines</div><h1>Surd Dominoes</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.4pt">Start with START. Work out the clue on the right in its simplest form, then find the domino with that answer on its left. Keep going until you reach FINISH. Three clues are marked Higher Level (Ordinary Level groups can be given those answers).</p>
  <div class="doms">{dom_html}</div>
</div>

<div class="page">
  <div class="poster">
    <h1>Surd rules</h1>
    <div class="ops">
      <div style="background:var(--green-soft)"><b>Simplify</b>biggest square<br>√72 = √36 × √2<br>= 6√2</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Multiply</b>√a × √b = √(ab)<br>√2 × √8 = √16 = 4<br>(√a)² = a</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Add</b>like surds only<br>√8 + √18<br>= 2√2 + 3√2 = 5√2</div>
      <div style="background:var(--green-soft)"><b>Higher Level</b>expand like algebra<br>(5 + √2)(5 − √2)<br>= 25 − 2 = 23</div>
    </div>
    <p style="text-align:center;font-size:22pt!important;font-weight:800;margin:4mm 0">√a + √b ≠ √(a + b)</p>
    <p style="text-align:center;font-size:10pt;color:var(--muted)">Léim · leim.ie · Play Surd Simplify: {GAME}</p>
  </div>
</div>

<div class="page ws">
  <div class="band"><div><div class="k">Worksheet</div><h1>Error Hunt + exam-style questions</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Error Hunt</h2>
  <p>Each student's answer has one mistake. Find it, say what went wrong, and write the right answer.</p>
  <table class="eh"><thead><tr><th>Question</th><th>Student's answer</th><th>The mistake and the right answer</th></tr></thead><tbody>
  {"".join(f"<tr><td>{q}</td><td>{w}</td><td><span class='gap'></span><span class='gap'></span></td></tr>" for q, w, r in ERR)}
  </tbody></table>
  <h2>B. Exam-style questions (show all your work)</h2>
  <ol class="q">
    <li>A square has an area of 50 cm². (a) Find the length of a side in the form a√b. (b) Find its perimeter.<span class="long"></span></li>
    <li>Show that √12 + √27 + √75 = 10√3.<span class="long"></span></li>
    <li>Which is bigger, 4√3 or 3√5? Explain without a calculator.<span class="long"></span></li>
    <li>A right-angled triangle has shorter sides √5 cm and √11 cm. Show that the longest side is a whole number.<span class="long"></span></li>
    <li>Higher Level: expand and simplify (a) (2√3 + 1)(2√3 − 1) (b) (√5 + 2)².<span class="long"></span></li>
  </ol>
</div>

<div class="page an">
  <div class="band"><div><div class="k">For the teacher</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>Surd Swap</h2>
  <div class="two"><table><tbody>
   <tr><td>Length</td><td>√25 × √2 = <b>{SW1_ans[0]} m</b></td></tr><tr><td>Width</td><td>√4 × √2 = <b>{SW1_ans[1]} m</b></td></tr>
   <tr><td>Perimeter</td><td>5√2 + 2√2 + 5√2 + 2√2 = <b>{SW1_ans[2]} m</b></td></tr><tr><td>Area</td><td>√50 × √8 = √400 = <b>{SW1_ans[3]} m²</b></td></tr></tbody></table>
  <table><tbody>
   <tr><td>Longest side</td><td>c² = 9 + 36 = 45, c = <b>{SW2_ans[0]} cm</b></td></tr><tr><td>Area</td><td>½ × 3 × 6 = <b>{SW2_ans[1]} cm²</b></td></tr></tbody></table></div>
  <h2>A. Error Hunt</h2>
  <table><tbody>{"".join(f"<tr><td style='width:40%'><b>{q}</b></td><td>{r}</td></tr>" for q, w, r in ERR)}</tbody></table>
  <h2>B. Exam-style questions</h2>
  <ol class="q">
    <li>(a) side = √50 = √25 × √2 = <b>{WS[0]} cm</b> (b) 4 × 5√2 = <b>{WS[1]} cm</b></li>
    <li>2√3 + 3√3 + 5√3 = <b>{WS[3]}</b> ✓</li>
    <li>4√3 = √48 and 3√5 = √45. 48 &gt; 45, so <b>4√3 is bigger</b>.</li>
    <li>c² = (√5)² + (√11)² = 5 + 11 = 16, so c = <b>4 cm</b>, a whole number.</li>
    <li>(a) (2√3)² − 1² = 12 − 1 = <b>{WS[4]}</b> (b) 5 + 2√5 + 2√5 + 4 = <b>{WS[5]}</b></li>
  </ol>
  <h2>Marking tip</h2>
  <p>Give credit for each step, as the exam does: the square factor shown (√36 × √2), the surds simplified before adding, the final answer in the form asked for. An answer like 8.49 instead of 6√2 is not exact: ask for surd form.</p>
</div>
</body></html>"""

cover = """<!doctype html><html><head><meta charset="utf-8"><style>
body{margin:0;width:1200px;height:1200px;background:#1B2430;font-family:Inter,sans-serif;color:#fff;display:flex;flex-direction:column;justify-content:space-between;padding:90px;box-sizing:border-box}
.k{display:inline-block;background:#2E7D57;border-radius:99px;padding:12px 26px;font-weight:700;font-size:28px;letter-spacing:.06em;text-transform:uppercase}
h1{font-size:150px;font-weight:800;line-height:1.1;letter-spacing:-.02em;margin:60px 0 20px}
h1 span{background:#F6CF5A;color:#1B2430;padding:0 18px;border-radius:14px}
.sub{font-size:40px;line-height:1.4;color:#DDE3EA}
.em{font-size:56px;margin-top:30px;font-weight:800;letter-spacing:.01em;color:#F6CF5A}
.foot{display:flex;justify-content:space-between;align-items:center;font-size:34px;font-weight:700}
.price{background:#F6CF5A;color:#1B2430;border-radius:16px;padding:14px 28px}
</style></head><body>
<div><span class="k">Junior Cycle Maths · Teacher pack</span>
<h1><span>Surds</span></h1>
<div class="sub">Surd Match mingle · Surd Swap A/B<br>Dominoes · Poster · Worksheet + answers</div>
<div class="em">√72 = 6√2 &nbsp;·&nbsp; √8 + √18 = 5√2</div></div>
<div class="foot"><span>↗ Léim · leim.ie</span><span class="price">Ready to teach · 60 min</span></div>
</body></html>"""

if __name__ == "__main__":
    for name, txt in [("rules-and-practice", sheet), ("teacher-pack", pack), ("cover", cover)]:
        plain = re.sub(r"<[^>]+>", " ", re.sub(r"<style>.*?</style>|<svg.*?</svg>", "", txt, flags=re.S))
        assert not re.search(r"[\d)]\s*-\s*[\d(√]|[=(]\s*-\d|(?<![\w])-\d", plain), (name, re.findall(r".{20}[\d)]\s*-\s*[\d(].{10}", plain)[:3])
        open(os.path.join(SRC, f"{SLUG}-{name}.html"), "w", encoding="utf-8").write(txt)
    def pdf(name, out):
        subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--no-pdf-header-footer", f"--print-to-pdf={out}",
                        f"{SLUG}-{name}.html"], cwd=SRC, check=True, capture_output=True)
        d = open(out, "rb").read(); print(name, len(re.findall(rb"/Type\s*/Page[^s]", d)), "pages")
    pdf("rules-and-practice", os.path.join(ROOT, "printables", f"{SLUG}-rules-and-practice.pdf"))
    pdf("teacher-pack", os.path.join(OUT, "Surds-Teacher-Pack-Leim.pdf"))
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--hide-scrollbars", "--window-size=1200,1200",
                    f"--screenshot={os.path.join(OUT, f'{SLUG}-cover.png')}", f"{SLUG}-cover.html"], cwd=SRC, check=True, capture_output=True)
    print("domino chain:", chain)
