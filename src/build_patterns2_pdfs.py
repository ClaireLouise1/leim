#!/usr/bin/env python3
"""Patterns 2: quadratic & exponential (JC Maths topic 36): free sheet + teacher pack + Payhip cover.
Run from the repo root: python3 src/build_patterns2_pdfs.py OUTDIR
Writes src/quadratic-exponential-patterns-*.html; PDFs/cover PNG go to OUTDIR (free sheet also to printables/).
Every answer is checked with test_growth_spotter.py's own maths (kind, extend, rule, ev, tiles, diffs).
Styles are read from src/build_money1_pdfs.py."""
import os, sys, random, subprocess, re
from fractions import Fraction as Fr
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC)
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/patterns2"; os.makedirs(OUT, exist_ok=True)
SLUG = "quadratic-exponential-patterns"
LO = "AF.1a, AF.1b, AF.1c, N.4"
GAME = "leim.ie/growth-spotter.html"

# ---------- the checker's own maths ----------
_ns = {}; exec(open(os.path.join(SRC, "test_growth_spotter.py"), encoding="utf-8").read().split("def main")[0], _ns)
kind, extend, rule, ev, tiles, diffs, seq = (_ns[k] for k in ("kind", "extend", "rule", "ev", "tiles", "diffs", "seq"))
def S(s): return [Fr(x) for x in seq(s)]
def nxt(s, k=1): a = S(s); return [extend(a, len(a) + i) for i in range(1, k + 1)]
def fits(r, s): return all(ev(rule(r), i + 1) == v for i, v in enumerate(S(s)))
def which(r, X):
    import sympy as sp
    sols = [v for v in sp.solve(sp.Eq(rule(r), X), _ns["n"]) if v.is_integer and v > 0]; assert len(sols) == 1, (r, X, sols); return int(sols[0])
def missing(s):
    import sympy as sp
    x = sp.Symbol("x"); b = [x if t == "?" else sp.Integer(int(t)) for t in s.split(", ")]
    dd = diffs(diffs(b)); sol = sp.solve(sp.Eq(dd[0], dd[1]), x); assert len(sol) == 1
    assert all(sp.simplify(e.subs(x, sol[0]) - dd[0].subs(x, sol[0])) == 0 for e in dd); return int(sol[0])
def I(v): assert v == int(v); return str(int(v))
def mn(s): return str(s).replace("-", "−")

# ---------- tile pictures (same drawing as the game; tiles counted back by the checker) ----------
COL = {"g": "#9BD3AE", "y": "#F6CF5A", "b": "#A9C4E8"}
def cells(kind_, n, e=0, r=2, c=1):
    if kind_ == "sqk": return [(i, j, "g") for i in range(n) for j in range(n)] + [(n + .3, i, "y") for i in range(e)]
    if kind_ == "rect": return [(i, j, "b") for i in range(n + 1) for j in range(n)]
    if kind_ == "big": return [(i, j, "g") for i in range(n + 1) for j in range(n + 1)]
    N = c * r ** (n - 1); cols = 1
    while cols * cols < N: cols += 1
    return [(i % cols, i // cols, "b") for i in range(N)]
def pic(kind_, stages, u=13, **kw):
    S_, H, x0, o = [], 0, 6, ""
    for n in stages:
        cs = cells(kind_, n, **kw); w = max(t[0] for t in cs) + 1; h = max(t[1] for t in cs) + 1
        S_.append((n, cs, w, h)); H = max(H, h)
    base = 8 + H * u
    for n, cs, w, h in S_:
        w2 = max(w, 2.6); ox = x0 + (w2 - w) * u / 2; o += f'<g data-stage="{n}">'
        for t in cs: o += f'<rect class="t" x="{ox + t[0] * u:.1f}" y="{base - (t[1] + 1) * u:.1f}" width="{u - 1}" height="{u - 1}" fill="{COL[t[2]]}" stroke="#1B2430" stroke-width=".8"/>'
        o += f'</g><text x="{x0 + w2 * u / 2:.1f}" y="{base + 14}" font-size="10" font-weight="700" text-anchor="middle" fill="#1B2430" font-family="Inter,sans-serif">Stage {n}</text>'
        x0 += w2 * u + 18
    return f'<svg class="tp" viewBox="0 0 {x0 - 12:.0f} {base + 20}" width="{(x0 - 12) * 1.1:.0f}">{o}</svg>'
def counts(svg): return [Fr(c) for s, c in tiles(svg)]

FIG_SQ = pic("sqk", [1, 2, 3], e=2)
FIG_BIG = pic("big", [1, 2, 3])
FIG_TRI = pic("dbl", [1, 2, 3], r=3, c=1)
FIG_RECT = pic("rect", [1, 2, 3])
assert counts(FIG_SQ) == [3, 6, 11] and counts(FIG_BIG) == [4, 9, 16] and counts(FIG_TRI) == [1, 3, 9] and counts(FIG_RECT) == [2, 6, 12]

# ---------- free sheet ----------
A = ["4, 9, 14, 19, 24", "2, 6, 18, 54, 162", "1, 5, 11, 19, 29", "7, 14, 28, 56, 112", "10, 13, 18, 25, 34", "40, 35, 30, 25, 20"]
A_ans = [kind(S(s)) for s in A]; assert A_ans == ["Linear", "Exponential", "Quadratic", "Exponential", "Quadratic", "Linear"]
B = ["4, 7, 12, 19", "1, 2, 4, 8", "2, 8, 18, 32", "5, 15, 45, 135", "3, 8, 15, 24", "6, 11, 18, 27"]
B_ans = [", ".join(I(v) for v in nxt(s, 2)) for s in B]
assert B_ans == ["28, 39", "16, 32", "50, 72", "405, 1215", "35, 48", "38, 51"], B_ans
c13 = S("2, 7, 16, 29, 46"); d1 = diffs(c13); d2 = diffs(d1); assert kind(c13) == "Quadratic"
C_ans = ["1st: " + ", ".join(I(v) for v in d1) + "; 2nd: " + ", ".join(I(v) for v in d2),
         I(missing("3, 7, ?, 21, 31")), I(missing("2, ?, 12, 20, 30")), I(ev(rule("Tₙ = n² + 7"), 5)), I(ev(rule("Tₙ = 2ⁿ"), 8))]
assert C_ans[1:] == ["13", "6", "32", "256"]
D_big = [extend(counts(FIG_BIG), 4), extend(counts(FIG_BIG), 10)]; assert D_big == [25, 121]
assert kind(counts(FIG_BIG) + [Fr(25)]) == "Quadratic"
D_tri = [extend(counts(FIG_TRI), 4), extend(counts(FIG_TRI), 6)]; assert D_tri == [27, 243]
D23 = 30 * 2 ** 5; assert D23 == 960
E = [("3, 6, 11, 18", "Tₙ = n² + 2"), ("4, 10, 18, 28", "Tₙ = n² + 3n"), ("5, 11, 21, 35", "Tₙ = 2n² + 3"), ("0, 5, 14, 27", "Tₙ = 2n² − n − 1")]
for s, r in E: assert fits(r, s) and kind(S(s)) == "Quadratic", (s, r)
E28 = which("Tₙ = n² + 3n", 130); assert E28 == 10
# exam-style F
F29 = [extend(counts(FIG_RECT), 4), extend(counts(FIG_RECT), 10)]; assert F29 == [20, 110]
wk = next(n for n in range(1, 50) if 2 ** (n - 1) > 50 * n); assert wk == 10 and 2 ** 8 < 50 * 9
fold = next(k for k in range(1, 30) if 2 ** k > 500); assert fold == 9 and 2 ** 6 == 64
assert fits("Tₙ = 2n² + 3n + 1", "6, 15, 28, 45") and which("Tₙ = 2n² + 3n + 1", 231) == 10

def qs(items): return "".join(f"<li>{q} <span class='line'></span></li>" for q in items)
def style(var):
    return re.search(var + r' = f"""<!doctype.*?<style>(.*?)</style>', open(os.path.join(SRC, "build_money1_pdfs.py"), encoding="utf-8").read(), re.S).group(1).replace("{LO}", LO).replace("{{", "{").replace("}}", "}")
SHEET_STYLE = style("sheet"); PACK_STYLE = style("pack")
assert "@bottom-left" in SHEET_STYLE and "Single-teacher licence" in PACK_STYLE
EXTRA = """.wk{font-variant-numeric:tabular-nums;line-height:1.5;border:1.5px solid var(--line);border-radius:8px;padding:2px 7px;margin:3px 0;font-size:9.2pt}.wk b.h{display:block}
svg.tp{display:block;margin:2px auto;max-width:100%;height:auto}
pre.dt{font:700 10pt/1.35 "DejaVu Sans Mono",Menlo,monospace;border:1.5px solid var(--line);border-radius:8px;padding:3px 8px;margin:3px 0}
table.st{border-collapse:collapse;margin:3px 0;font-size:9pt}table.st td,table.st th{border:1px solid #C9D1DA;padding:1px 6px;text-align:center}table.st th{text-align:left}
.ef{float:right;margin:0 0 2px 8px}"""
DT = """1    4    9    16    25
   3    5    7     9      ← 1st differences
     2    2    2          ← 2nd differences"""
HLT = '<table class="st"><tr><th>n</th><td>1</td><td>2</td><td>3</td><td>4</td></tr><tr><th>Tₙ</th><td>4</td><td>11</td><td>22</td><td>37</td></tr><tr><th>2n²</th><td>2</td><td>8</td><td>18</td><td>32</td></tr><tr><th>Tₙ − 2n²</th><td>2</td><td>3</td><td>4</td><td>5</td></tr></table>'
assert fits("Tₙ = 2n² + n + 1", "4, 11, 22, 37") and which("Tₙ = 2n² + n + 1", 211) == 10

Fq = [(f'<b>Tiles.</b> <span class="ef">{FIG_RECT}</span>The pattern has 2, 6, 12 tiles in stages 1, 2, 3. (a) How many tiles in stage 4? (b) Linear, quadratic or exponential? Give a reason. (c) How many tiles in stage 10?',
       "(a) jumps 4, 6 → 8: <b>20</b> (b) 2nd differences 2, 2: <b>quadratic</b> (c) n(n + 1) = 10 × 11 = <b>110</b>"),
      ("<b>Two plans.</b> Plan A pays €50 a week (50, 100, 150, …). Plan B pays €1 in week 1 and doubles every week (1, 2, 4, …). In which week is Plan B first bigger than Plan A?",
       "Week 9: 256 &lt; 450. Week 10: 512 &gt; 500. <b>Week 10</b>"),
      ("<b>Folding paper.</b> Each fold doubles the layers: 1 fold → 2 layers. (a) Layers after 6 folds? (b) Fewest folds for more than 500 layers?",
       "(a) 2⁶ = <b>64</b> (b) 2⁸ = 256, 2⁹ = 512: <b>9 folds</b>"),
      ("<b>Higher Level.</b> 6, 15, 28, 45, … is quadratic. (a) Find Tₙ = an² + bn + c. (b) Which term is 231?",
       "(a) 2nd difference 4, a = 2; Tₙ − 2n² = 4, 7, 10, 13 = 3n + 1: <b>Tₙ = 2n² + 3n + 1</b> (b) 2n² + 3n + 1 = 231 → (2n + 23)(n − 10) = 0 → <b>n = 10</b>")]

sheet = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Quadratic and exponential patterns: rules and practice | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{SHEET_STYLE}
{EXTRA}
</style></head><body>
<div class="page tight">
  <div class="band"><div><div class="k">Junior Cycle Maths · Free revision sheet</div><h1>Quadratic &amp; exponential patterns</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2018 specification): {LO}. Play the game: <b>{GAME}</b></p>
  <div class="two">
   <div><h2>1. Three kinds of pattern</h2>
    <div class="wk"><b class="h">Linear: 5, 8, 11, 14</b>Same jump every time (+3). Graph: a straight line.</div>
    <div class="wk"><b class="h">Quadratic: 3, 6, 11, 18</b>Jumps 3, 5, 7 change by the same amount: same <b>2nd difference</b> (+2). Graph: a curve.</div>
    <div class="wk"><b class="h">Exponential: 3, 6, 12, 24</b>Same <b>multiplier</b>: × 2 (doubling) or × 3 (tripling). Graph: flat, then shoots up.</div>
    <h2>2. Differences</h2>
    <pre class="dt">{DT}</pre>
    <p><b>Next term of a quadratic:</b> 3, 6, 11, 18, ? Jumps 3, 5, 7, so the next jump is 9: 18 + 9 = <b>27</b>.</p>
    <h2>3. Growing tile patterns</h2>
    {FIG_SQ}
    <p>Stage n = an n × n square + 2 yellow tiles: <b>n² + 2</b>. Stage 10 = 10 × 10 + 2 = <b>102</b>. (Not 10 × stage 1.)</p></div>
   <div><h2>4. Doubling and tripling</h2>
    <p>1, 2, 4, 8, … × 2 each time. 1, 3, 9, 27, … × 3 each time.</p>
    <div class="wk"><b class="h">Start 50, doubles every hour. After 3 hours?</b>50 × 2 × 2 × 2 = 50 × 2³ = <b>400</b></div>
    <p>Rules: 2, 4, 8, 16 → <b>Tₙ = 2ⁿ</b>. 3, 9, 27, 81 → <b>Tₙ = 3ⁿ</b>.<br>Don't mix up 2n (2, 4, 6, 8), n² (1, 4, 9, 16) and 2ⁿ (2, 4, 8, 16).</p>
    <h2>5. Higher Level: Tₙ = an² + bn + c</h2>
    <p>4, 11, 22, 37: 1st differences 7, 11, 15; 2nd differences 4, 4. <b>a = half the 2nd difference = 2.</b></p>
    {HLT}
    <p>The last row is n + 1, so <b>Tₙ = 2n² + n + 1</b>. Check n = 2: 8 + 2 + 1 = 11 ✓<br>Which term is 211? 2n² + n + 1 = 211 → n = 10.</p>
    <div class="note"><b>Classic mistakes:</b> adding the same jump again in a quadratic · stage 10 = 10 × stage 1 · doubling as + 2 instead of × 2 · a = the 2nd difference (it's half) · 2n, n² and 2ⁿ mixed up.</div></div>
  </div>
  <div class="tip"><b>Exam tip:</b> always give a reason: write the differences (or the × number). Check any rule with two terms from the table.</div>
</div>

<div class="page p2">
  <div class="band"><div><div class="k">Practice · 32 questions</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Linear, quadratic or exponential? Give a reason.</h2>
  <ol class="q" style="columns:2;column-gap:8mm">{qs(f"{s}, …" for s in A)}</ol>
  <h2>B. Write the next two terms</h2><ol class="q" start="7" style="columns:2;column-gap:8mm">{qs(f"{s}, …" for s in B)}</ol>
  <h2>C. Differences and terms</h2><ol class="q" start="13" style="columns:2;column-gap:8mm">{qs(["Write the 1st and 2nd differences of 2, 7, 16, 29, 46.", "Find the missing term: 3, 7, ?, 21, 31 (quadratic)", "Find the missing term: 2, ?, 12, 20, 30 (quadratic)", "Tₙ = n² + 7. Find T₅.", "Tₙ = 2ⁿ. Find T₈."])}</ol>
  <h2>D. Growing pictures and doubling</h2>
  <div class="two"><div>{FIG_BIG}<ol class="q" start="18">{qs(["How many tiles in stage 4?", "Linear, quadratic or exponential? Why?", "How many tiles in stage 10?"])}</ol></div>
  <div>{FIG_TRI}<ol class="q" start="21">{qs(["How many tiles in stage 4?", "How many tiles in stage 6?", "Bacteria double every hour. Start: 30. How many after 5 hours?"])}</ol></div></div>
  <h2>E. Higher Level: find Tₙ = an² + bn + c</h2><ol class="q" start="24" style="columns:2;column-gap:8mm">{qs([f"{s}, …" for s, r in E] + ["Tₙ = n² + 3n. Which term is 130?"])}</ol>
  <p class="small" style="margin-top:4px">Questions 29–32 are on the next page.</p>
</div>

<div class="page">
  <div class="band"><div><div class="k">Exam-style · then check</div><h1>Exam corner + answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>F. Exam-style questions (show your work)</h2>
  <ol class="q e3" start="29">{"".join(f"<li>{q}<span class='long'></span><span class='long'></span></li>" for q, a in Fq)}</ol>
  <h2 style="margin-top:10px;clear:both">Answers</h2>
  <table class="ans"><tbody>
   <tr><td><b>A</b></td><td>{" · ".join(f"{i}. {a}" for i, a in enumerate(A_ans, 1))} (same jump / same 2nd difference / same × number)</td></tr>
   <tr><td><b>B</b></td><td>{" · ".join(f"{i}. {a}" for i, a in enumerate(B_ans, 7))}</td></tr>
   <tr><td><b>C</b></td><td>{" · ".join(f"{i}. {a}" for i, a in enumerate(C_ans, 13))}</td></tr>
   <tr><td><b>D</b></td><td>18. {I(D_big[0])} · 19. quadratic (jumps 5, 7, 9; 2nd difference 2) · 20. {I(D_big[1])} (11 × 11) · 21. {I(D_tri[0])} · 22. {I(D_tri[1])} · 23. {D23}</td></tr>
   <tr><td><b>E</b></td><td>{" · ".join(f"{i}. {r}" for i, (s, r) in enumerate(E, 24))} · 28. n = {E28}</td></tr>
   <tr><td><b>F</b></td><td>{" · ".join(f"{i}. {a}" for i, (q, a) in enumerate(Fq, 29))}</td></tr>
  </tbody></table>
  <div class="note"><b>Got one wrong?</b> Did you write out the differences? Did you multiply (not add) for doubling? Did you use the rule for far-away stages? Then play <b>Growth Spotter</b> at {GAME}: the "Go back over these" list at the end shows the rule for each mistake.</div>
  <p class="small">All questions written by Léim. Léim is independent and not connected with the State Examinations Commission or the NCCA.</p>
</div>
</body></html>"""
NQ = len(A) + len(B) + 5 + 6 + len(E) + 1 + len(Fq); assert NQ == 32, NQ

# ---------- teacher pack ----------
MATCH = [("2, 5, 10, 17", "Tₙ = n² + 1"), ("5, 8, 13, 20", "Tₙ = n² + 4"), ("0, 3, 8, 15", "Tₙ = n² − 1"), ("2, 8, 18, 32", "Tₙ = 2n²"),
         ("2, 6, 12, 20", "Tₙ = n² + n"), ("4, 9, 16, 25", "Tₙ = (n + 1)²"), ("2, 4, 8, 16", "Tₙ = 2ⁿ"), ("3, 9, 27, 81", "Tₙ = 3ⁿ"),
         ("6, 12, 24, 48", "Tₙ = 3 × 2ⁿ"), ("6, 18, 54, 162", "Tₙ = 2 × 3ⁿ"), ("4, 7, 10, 13", "Tₙ = 3n + 1"), ("5, 10, 15, 20", "Tₙ = 5n")]
for i, (s, r) in enumerate(MATCH):   # each rule card fits its own pattern card and no other
    assert [j for j in range(12) if fits(r, MATCH[j][0])] == [i], (i, r)
random.seed(36); order = list(range(24)); random.shuffle(order)
cards = [("q", i) for i in range(12)] + [("a", i) for i in range(12)]
match_print = [cards[k] for k in order]
def card_html(c):
    k, i = c
    return f'<div class="fc">{MATCH[i][1] if k == "a" else MATCH[i][0] + ", …"}</div>'
match_html = "".join(f'<div class="c"><span class="tag">Card {k}</span>{card_html(c)}</div>' for k, c in enumerate(match_print, 1))
match_key = " · ".join(f"{match_print.index(('q', i)) + 1} → {match_print.index(('a', i)) + 1}" for i in range(12))

# Pattern Swap: each fact on exactly ONE card
SW1 = [("Stage 1 tiles", "3", "A"), ("Stage 2 tiles", "6", "B"), ("Stage 3 tiles", "11", "A"), ("Stage 4 tiles", "18", "B"),
       ("Kind of pattern", "", None), ("Rule (tiles in stage n)", "", None), ("Stage 10 tiles", "", None)]
t1 = S("3, 6, 11, 18"); assert kind(t1) == "Quadratic" and fits("Tₙ = n² + 2", "3, 6, 11, 18") and extend(t1, 10) == 102
SW2 = [("Bacteria at the start", "25", "A"), ("After 1 hour", "50", "B"), ("After 2 hours", "100", "A"),
       ("Multiplier each hour", "", None), ("After 6 hours", "", None), ("First hour over 10 000", "", None)]
assert 25 * 2 ** 6 == 1600 and next(k for k in range(30) if 25 * 2 ** k > 10000) == 9
for rows in (SW1, SW2): assert sum(w == "A" for *_, w in rows) >= 1 and sum(w == "B" for *_, w in rows) >= 1
def swap_card(who):
    def tab(title, rows):
        return f'<table class="ss"><thead><tr><th colspan="2">{title}</th></tr></thead><tbody>' + "".join(
            f"<tr><td>{k}</td><td><b>{v if w and who in w else ''}</b></td></tr>" for k, v, w in rows) + "</tbody></table>"
    return f'<div class="idc"><h3>Student {who} · Pattern Swap</h3><div class="two">{tab("The tile pattern", SW1)}{tab("The bacteria (double every hour)", SW2)}</div></div>'

# Pattern Dominoes: 20 clues, 20 different answers (each worked out by the checker)
DOMS = [("Next: 2, 5, 10, 17, …", nxt("2, 5, 10, 17")[0]), ("Next: 3, 6, 12, 24, …", nxt("3, 6, 12, 24")[0]), ("Next: 1, 3, 9, 27, …", nxt("1, 3, 9, 27")[0]),
        ("Next: 4, 7, 12, 19, …", nxt("4, 7, 12, 19")[0]), ("Next: 0, 3, 8, 15, …", nxt("0, 3, 8, 15")[0]), ("2nd difference of 2, 9, 22, 41, …", diffs(diffs(S("2, 9, 22, 41")))[0]),
        ("Tₙ = n² + 5. T₄?", ev(rule("Tₙ = n² + 5"), 4)), ("Tₙ = n² − n. T₆?", ev(rule("Tₙ = n² − n"), 6)), ("Tₙ = 2ⁿ. T₆?", ev(rule("Tₙ = 2ⁿ"), 6)),
        ("Tₙ = 3ⁿ. T₃?", ev(rule("Tₙ = 3ⁿ"), 3)), ("Missing: 5, 8, ?, 20, 29", missing("5, 8, ?, 20, 29")), ("Tiles n² + 2. Stage 10?", ev(rule("Tₙ = n² + 2"), 10)),
        ("Start 10, doubles 4 times", Fr(10 * 2 ** 4)), ("Start 2, triples 3 times", Fr(2 * 3 ** 3)), ("1st difference after 9 in 1, 4, 9, 16", diffs(S("1, 4, 9, 16"))[2]),
        ("Next: 6, 12, 20, 30, …", nxt("6, 12, 20, 30")[0]), ("Next: 5, 10, 20, 40, …", nxt("5, 10, 20, 40")[0]),
        ("Higher Level: a in an² + bn + c for 3, 10, 21, 36", diffs(diffs(S("3, 10, 21, 36")))[0] / 2),
        ("Higher Level: which term of n² + 3 is 84?", Fr(which("Tₙ = n² + 3", 84))), ("Higher Level: which term of 2n² + 1 is 201?", Fr(which("Tₙ = 2n² + 1", 201)))]
DOMS = [(c, I(a)) for c, a in DOMS]
assert [a for c, a in DOMS] == ["26", "48", "81", "28", "24", "6", "21", "30", "64", "27", "13", "102", "160", "54", "7", "42", "80", "2", "9", "10"]
DANS = [a for c, a in DOMS]; assert len(set(DANS)) == 20
random.seed(3636); chain = DOMS[:]; random.shuffle(chain)
dom = [("START" if k == 0 else chain[k - 1][1], x[0]) for k, x in enumerate(chain)] + [(chain[-1][1], "FINISH")]
dom_print = dom[:]; random.shuffle(dom_print)
dom_html = "".join(f'<div class="dom"><div class="h l">{l}</div><div class="h r">{r}</div></div>' for l, r in dom_print)
chain_key = "".join(f"<li>{x} = <b>{a}</b></li>" for x, a in chain)

ERR = [("Next term of 3, 6, 11, 18, …", "25", "Added 7 again. Jumps grow by 2: 18 + 9 = <b>27</b>"),
       ("Stage 10 of the tiles 3, 6, 11, … (n² + 2)", "30", "10 × stage 1 is wrong. 10² + 2 = <b>102</b>"),
       ("Start 20, doubles every hour. After 3 hours?", "120", "Doubling is × 2 each hour: 20 × 2 × 2 × 2 = <b>160</b>"),
       ("2, 4, 8, 16: \"quadratic, the 2nd differences are 2, 2\"", "Quadratic", "1st differences 2, 4, 8; 2nd 2, 4 (not equal). × 2 each time: <b>exponential</b>"),
       ("Tₙ = 2ⁿ. Find T₅.", "10", "2ⁿ is not 2 × n: 2⁵ = <b>32</b>"),
       ("Higher Level: find Tₙ for 3, 9, 19, 33, …", "Tₙ = 4n² − 1", "a = half the 2nd difference (4) = 2: <b>Tₙ = 2n² + 1</b>")]
assert nxt("3, 6, 11, 18")[0] == 27 and ev(rule("Tₙ = n² + 2"), 10) == 102 and ev(rule("Tₙ = 2ⁿ"), 5) == 32
assert kind(S("2, 4, 8, 16")) == "Exponential" and fits("Tₙ = 2n² + 1", "3, 9, 19, 33") and not fits("Tₙ = 4n² − 1", "3, 9, 19, 33")
# worksheet exam-style
fold = [2 ** k for k in (3, 4, 5)]; assert fold == [8, 16, 32] and next(k for k in range(30) if 2 ** k > 1000) == 10
assert 4 * 3 ** 4 == 324 and next(k for k in range(30) if 4 * 3 ** k > 2000) == 6
tri = S("1, 3, 6, 10, 15"); assert [I(v) for v in nxt("1, 3, 6, 10, 15", 2)] == ["21", "28"] and diffs(diffs(tri))[0] == 1
assert fits("Tₙ = 2n² + n + 2", "5, 12, 23, 38") and which("Tₙ = 2n² + n + 2", 107) == 7

pack = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Quadratic &amp; Exponential Patterns Teacher Pack | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{PACK_STYLE}
{EXTRA}
.ss td:nth-child(2){{width:28%}}.ss td,.ss th{{padding:2px 5px;font-size:8.8pt;line-height:1.3}}.fym{{grid-template-columns:repeat(3,1fr)}}.fym .c{{height:13mm}}.fym .fc{{font-size:12.5pt;line-height:1.1}}.idc{{padding:1mm 4mm}}.idc h3{{margin:0 0 1mm}}.p1 .proc td{{font-size:8.5pt;padding:2px 6px}}
.dom .r{{font-size:9.6pt}}.dom .l{{font-size:15pt}}.ops div{{font-size:12pt}}
</style></head><body>

<div class="page p1">
  <div class="band"><div><div class="k">Junior Cycle Maths · Teacher pack</div><h1>Quadratic &amp; exponential patterns</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2018 specification): {LO}</p>
  <div class="two">
    <div><h3>Aims</h3><p>By the end of the lesson students can tell linear, quadratic and exponential patterns apart (same jump, same 2nd difference, same multiplier), continue them, find far-away terms of growing tile patterns and solve doubling and tripling problems. Higher Level: find Tₙ = an² + bn + c and say which term has a given value.</p></div>
    <div><h3>In this pack</h3><p>p.1 Teacher notes · p.2 Growth Match mingle cards + Pattern Swap A/B cards · p.3 Pattern Dominoes (cut-up) · p.4 Wall poster · p.5 Worksheet: Error Hunt + exam-style questions · p.6 Answers. Level: 3rd year (Higher and Ordinary). Time: about 60 minutes. All questions are original.</p></div>
  </div>
  <h2 style="margin-top:8px">Procedure</h2>
  <table class="proc"><tbody>
    <tr><td>5 min</td><td><b>Lead-in: the rice and the chessboard.</b> 1 grain on square 1, 2 on square 2, 4 on square 3 … Students guess square 10, then work it out (512). Compare with "add 100 each square". Which wins in the end?</td></tr>
    <tr><td>8 min</td><td><b>Guided discovery.</b> Write 1, 4, 9, 16, 25. Pairs find the jumps, then the jumps of the jumps. Then 2, 5, 10, 17 and 3, 6, 12, 24 the same way. Elicit the three kinds: same jump (linear), same 2nd difference (quadratic), same multiplier (exponential).</td></tr>
    <tr><td>10 min</td><td><b>Growth Match mingle</b> (p.2, 24 cards = 12 pattern cards + 12 rule cards; one card each). Find your partner: the rule must fit all four terms. Pairs then say what kind of pattern they have.</td></tr>
    <tr><td>12 min</td><td><b>Pattern Swap</b> (p.2, pairs, don't show your card). Each number is on only ONE card. Ask for what you're missing, then fill in the blanks together. Feedback: tiles → <b>quadratic, n² + 2, 102</b>; bacteria → <b>× 2, 1600, hour 9</b>.</td></tr>
    <tr><td>10 min</td><td><b>Pattern Dominoes</b> (p.3), groups of 3–4. Start with START, work out the clue, find the domino with that answer on its left, and build the chain to FINISH.</td></tr>
    <tr><td>12 min</td><td><b>Worksheet</b> (p.5). Error Hunt in pairs (find the mistake, name it, fix it), then the exam-style questions alone. Question 5 is Higher Level.</td></tr>
    <tr><td>3 min</td><td><b>Exit ticket.</b> Linear, quadratic or exponential: 2, 6, 12, 20 and 2, 6, 18, 54? Next term of each? (Quadratic, 30; exponential, 162.) Homework: play <b>Growth Spotter</b> at {GAME}.</td></tr>
  </tbody></table>
  <div class="note"><b>Mingle key</b> (pattern card → rule card): {match_key}.<br>
  <b>Errors to look for:</b> adding the same jump again · stage 10 = 10 × stage 1 · + 2 instead of × 2 · a = the 2nd difference (it's half) · 2n, n² and 2ⁿ mixed up. <b>Support:</b> "Write the jumps under the terms." <b>Fast finishers:</b> invent a tile pattern with the rule n² + n + 1 and draw stages 1–3.</div>
  <p class="small"><b>Domino answer chain</b> (START → FINISH):</p>
  <ol class="small" style="columns:2;column-gap:12px;font-size:7.2pt;line-height:1.22;margin:0;padding-left:16px">{chain_key}</ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">Cut up the cards · one Pattern Swap card per student</div><h1>Growth Match + Pattern Swap</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:8.8pt;margin:0"><b>Growth Match mingle.</b> Cut out the 24 cards and give one to each student. Pattern card? Find the rule that fits all four terms. Rule card? Find your pattern. (Fewer students? Take out whole pairs.)</p>
  <div class="fym">{match_html}</div>
  <p style="font-size:8.8pt;margin:3mm 0 0"><b>Pattern Swap.</b> Don't show your card. Each number is on only one of the two cards: ask your partner for what you're missing, then fill in every blank together.</p>
  {swap_card("A")}
  {swap_card("B")}
</div>

<div class="page">
  <div class="band"><div><div class="k">Groups of 3–4 · cut along the dashed lines</div><h1>Pattern Dominoes</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.4pt">Start with START. Work out the clue on the right, then find the domino with that answer on its left. Keep going until you reach FINISH. Three clues are marked Higher Level (Ordinary Level groups can be given those answers).</p>
  <div class="doms">{dom_html}</div>
</div>

<div class="page">
  <div class="poster">
    <h1>How does it grow?</h1>
    <div class="ops">
      <div style="background:var(--green-soft)"><b>Linear</b>same jump<br>5, 8, 11, 14<br>+3 +3 +3</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Quadratic</b>same 2nd difference<br>3, 6, 11, 18<br>jumps 3, 5, 7 (+2)</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Exponential</b>same multiplier<br>3, 6, 12, 24<br>× 2 × 2 × 2</div>
      <div style="background:var(--green-soft)"><b>Higher Level</b>Tₙ = an² + bn + c<br>a = half the 2nd difference<br>then take away an²</div>
    </div>
    <pre class="dt" style="font-size:17pt;width:max-content;margin:4mm auto">{DT}</pre>
    <p style="text-align:center;font-size:10pt;color:var(--muted)">Léim · leim.ie · Play Growth Spotter: {GAME}</p>
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
    <li>Fold a sheet of paper in half again and again. 1 fold → 2 layers. (a) How many layers after 3, 4 and 5 folds? (b) Write a rule for the layers after n folds. (c) How many folds until there are more than 1000 layers?<span class="long"></span></li>
    <li>Weeds in a garden triple every week. At the start there are 4. (a) How many after 4 weeks? (b) In which week are there first more than 2000?<span class="long"></span></li>
    <li>1, 3, 6, 10, 15, … (a) Write the next two terms. (b) Linear, quadratic or exponential? Give a reason.<span class="long"></span></li>
    <li>A tile pattern has 3, 6, 11, 18 tiles in stages 1 to 4. Ciara says stage 8 has 6 × 8 = 48 tiles because stage 2 has 6. Is she right? Explain.<span class="long"></span></li>
    <li>Higher Level: 5, 12, 23, 38, … is quadratic. (a) Find Tₙ = an² + bn + c. (b) Which term is 107?<span class="long"></span></li>
  </ol>
</div>

<div class="page an">
  <div class="band"><div><div class="k">For the teacher</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>Pattern Swap</h2>
  <div class="two"><table><tbody>
   <tr><td>Kind of pattern</td><td><b>Quadratic</b> (jumps 3, 5, 7; 2nd difference 2)</td></tr><tr><td>Rule</td><td><b>n² + 2</b></td></tr>
   <tr><td>Stage 10</td><td>10² + 2 = <b>102</b></td></tr></tbody></table>
  <table><tbody>
   <tr><td>Multiplier</td><td><b>× 2</b></td></tr><tr><td>After 6 hours</td><td>25 × 2⁶ = <b>1600</b></td></tr>
   <tr><td>First over 10 000</td><td>hour 8: 6400; <b>hour 9: 12 800</b></td></tr></tbody></table></div>
  <h2>A. Error Hunt</h2>
  <table><tbody>{"".join(f"<tr><td style='width:42%'><b>{q}</b></td><td>{r}</td></tr>" for q, w, r in ERR)}</tbody></table>
  <h2>B. Exam-style questions</h2>
  <ol class="q">
    <li>(a) <b>8, 16, 32</b> (b) <b>Tₙ = 2ⁿ</b> (c) 2⁹ = 512, 2¹⁰ = 1024: <b>10 folds</b></li>
    <li>(a) 4 × 3⁴ = <b>324</b> (b) 4, 12, 36, 108, 324, 972, 2916: <b>week 6</b></li>
    <li>(a) <b>21, 28</b> (b) jumps 2, 3, 4, 5; 2nd difference 1 (the same): <b>quadratic</b></li>
    <li><b>No.</b> The jumps grow (3, 5, 7), so it's quadratic, not × 3 each stage. Rule n² + 2: stage 8 = 64 + 2 = <b>66</b>.</li>
    <li>(a) 2nd difference 4, a = 2; Tₙ − 2n² = 3, 4, 5, 6 = n + 2: <b>Tₙ = 2n² + n + 2</b> (b) 2n² + n + 2 = 107 → 2n² + n − 105 = 0 → (2n + 15)(n − 7) = 0 → <b>term 7</b></li>
  </ol>
  <h2>Marking tip</h2>
  <p>Give credit for each step, as the exam does: the differences written out, the kind of pattern with a reason, the rule, the checked answer. "It goes up" or "it gets bigger" is not a reason: look for the jumps or the multiplier.</p>
</div>
</body></html>"""
assert ev(rule("Tₙ = n² + 2"), 8) == 66 and 2 ** 10 == 1024

cover = """<!doctype html><html><head><meta charset="utf-8"><style>
body{margin:0;width:1200px;height:1200px;background:#1B2430;font-family:Inter,sans-serif;color:#fff;display:flex;flex-direction:column;justify-content:space-between;padding:90px;box-sizing:border-box}
.k{display:inline-block;background:#2E7D57;border-radius:99px;padding:12px 26px;font-weight:700;font-size:28px;letter-spacing:.06em;text-transform:uppercase}
h1{font-size:100px;font-weight:800;line-height:1.16;letter-spacing:-.03em;margin:40px 0 0}
h1 span{background:#F6CF5A;color:#1B2430;padding:0 14px;box-decoration-break:clone;-webkit-box-decoration-break:clone}
.sub{font-size:38px;color:#C9D1DA;margin-top:36px;line-height:1.35}
.em{font-size:50px;margin-top:30px;font-weight:800;letter-spacing:.01em;color:#F6CF5A}
.foot{display:flex;justify-content:space-between;align-items:center;font-size:34px;font-weight:700}
.price{background:#F6CF5A;color:#1B2430;border-radius:16px;padding:14px 28px}
</style></head><body>
<div><span class="k">Junior Cycle Maths · Teacher pack</span>
<h1><span>Quadratic &amp;</span><br><span>Exponential Patterns</span></h1>
<div class="sub">Growth Match mingle · Pattern Swap A/B<br>Dominoes · Poster · Worksheet + answers</div>
<div class="em">3, 6, 11, 18 … &nbsp;·&nbsp; 3, 6, 12, 24 …</div></div>
<div class="foot"><span>↗ Léim · leim.ie</span><span class="price">Ready to teach · 60 min</span></div>
</body></html>"""

if __name__ == "__main__":
    for name, txt in [("rules-and-practice", sheet), ("teacher-pack", pack), ("cover", cover)]:
        plain = re.sub(r"<[^>]+>", " ", re.sub(r"<style>.*?</style>|<svg.*?</svg>", "", txt, flags=re.S))
        assert not re.search(r"[\dn)]\s*-\s*[\dn(]|[=(]\s*-\d|(?<![\w])-\d", plain), (name, re.findall(r".{20}[\dn)]\s*-\s*[\dn(].{10}", plain)[:3])
        open(os.path.join(SRC, f"{SLUG}-{name}.html"), "w", encoding="utf-8").write(txt)
    def pdf(name, out):
        subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--no-pdf-header-footer", f"--print-to-pdf={out}",
                        f"{SLUG}-{name}.html"], cwd=SRC, check=True, capture_output=True)
        d = open(out, "rb").read(); print(name, len(re.findall(rb"/Type\s*/Page[^s]", d)), "pages")
    pdf("rules-and-practice", os.path.join(ROOT, "printables", f"{SLUG}-rules-and-practice.pdf"))
    pdf("teacher-pack", os.path.join(OUT, "Quadratic-Exponential-Patterns-Teacher-Pack-Leim.pdf"))
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--hide-scrollbars", "--window-size=1200,1200",
                    f"--screenshot={os.path.join(OUT, f'{SLUG}-cover.png')}", f"{SLUG}-cover.html"], cwd=SRC, check=True, capture_output=True)
    print("domino chain:", chain)
