#!/usr/bin/env python3
"""Algebraic fractions, long division & changing the subject (JC Maths topic 35): free sheet + teacher pack + Payhip cover.
Run from the repo root: python3 src/build_algfrac_pdfs.py OUTDIR
Writes src/algebraic-fractions-changing-the-subject-*.html; PDFs/cover PNG go to OUTDIR (free sheet also to printables/).
Every answer is checked with test_rearrange_race.py's sympy checker (rearr_ok, zero, P) and sympy division.
Styles are read from src/build_money1_pdfs.py."""
import os, sys, random, subprocess, re, itertools
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC)
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/algfrac"; os.makedirs(OUT, exist_ok=True)
SLUG = "algebraic-fractions-changing-the-subject"
LO = "AF.3a, AF.3c, AF.6"
GAME = "leim.ie/rearrange-race.html"

# ---------- the checker's own maths ----------
_ns = {}; exec(open(os.path.join(SRC, "test_rearrange_race.py"), encoding="utf-8").read().split("if __name__")[0], _ns)
P, rearr_ok, zero, LET, sp = (_ns[k] for k in ("P", "rearr_ok", "zero", "LET", "sp"))
LET["k"] = sp.Symbol("k", positive=True)
def is_expr(q, a): return zero(P(a) - P(q))                     # "x/2 + x/3" equals "5x/6"
def is_div(top, dv, a):
    qt, rm = sp.div(P(top), P(dv), LET["x"]); return rm == 0 and sp.expand(qt - P(a)) == 0
def is_re(F, s, a): return rearr_ok(F, s, a)
def value(F, sub, vals):                                        # solve F for sub with numbers put in
    l, r = [P(z) for z in F.split(" = ")]; v = {LET[k]: sp.nsimplify(x) for k, x in vals.items()}
    S = sp.solve(sp.Eq(l.subs(v), r.subs(v)), LET[sub]); assert len(S) == 1, (F, S); return sp.nsimplify(S[0])
assert is_expr("x/2 + x/3", "5x/6") and not is_expr("x/2 + x/3", "2x/5")
assert is_div("x² + 5x + 6", "x + 2", "x + 3") and is_re("v = u + at", "t", "t = (v − u)/a")

# ---------- free sheet ----------
A = [("x/2 + x/5", "7x/10"), ("x/3 − x/4", "x/12"), ("(x + 1)/2 + (x + 3)/4", "(3x + 5)/4"), ("(x + 2)/3 + (x − 1)/2", "(5x + 1)/6"),
     ("(2x + 1)/5 + (x − 3)/2", "(9x − 13)/10"), ("(x + 4)/3 − (x − 2)/5", "(2x + 26)/15"), ("(3x − 1)/4 − (x + 2)/6", "(7x − 7)/12"), ("(6x + 9)/3", "2x + 3")]
for q, a in A: assert is_expr(q, a), q
B = [("x² + 7x + 12", "x + 3", "x + 4"), ("x² + 2x − 15", "x + 5", "x − 3"), ("x² − 9x + 14", "x − 2", "x − 7"),
     ("2x² + 7x + 6", "x + 2", "2x + 3"), ("3x² − 10x − 8", "x − 4", "3x + 2"), ("6x² + x − 2", "2x − 1", "3x + 2")]
for t, d, a in B: assert is_div(t, d, a), t
CQ = [("y = x + 7", "x", "x = y − 7"), ("y = 4x − 3", "x", "x = (y + 3)/4"), ("y = (x − 5)/2", "x", "x = 2y + 5"), ("P = 4s", "s", "s = P/4"),
      ("v = u + at", "u", "u = v − at"), ("A = ½bh", "b", "b = 2A/h"), ("y = mx + c", "m", "m = (y − c)/x")]
for F, s, a in CQ: assert is_re(F, s, a), F
C8 = value("F = 1.8C + 32", "C", {"F": 77}); assert C8 == 25 and is_re("F = 1.8C + 32", "C", "C = (F − 32)/1.8")
D = [("Higher Level: 3/(x + 1) + 2/(x − 4)", "(5x − 10)/((x + 1)(x − 4))", "e"), ("Higher Level: 5/(x − 2) − 3/(x + 3)", "(2x + 21)/((x − 2)(x + 3))", "e"),
     ("Higher Level: (x³ + 2x² − 5x − 6) ÷ (x + 1)", "x² + x − 6", "d"), ("Higher Level: (x³ − 27) ÷ (x − 3)", "x² + 3x + 9", "d"),
     ("Higher Level: A = πr². Make r the subject.", "r = √(A/π)", "r"), ("Higher Level: y = (x + 4)/(x − 2). Make x the subject.", "x = (2y + 4)/(y − 1)", "r")]
for q, a, k in D:
    body = q.replace("Higher Level: ", "")
    if k == "e": assert is_expr(body, a), q
    elif k == "d": t, d = body.split(" ÷ "); assert is_div(t[1:-1], d[1:-1], a), q
    else: F, s = re.match(r"(.+)\. Make (\w) the subject\.", body).groups(); assert is_re(F, s, a), q
# exam-style
assert is_expr("(x + 3)/2 + (x − 2)/3", "(5x + 5)/6") and value("w = (5x + 5)/6", "x", {"w": 5}) == 5
assert is_div("x² + 3x − 28", "x − 4", "x + 7")
assert is_re("C = 3.5 + 2k", "k", "k = (C − 3.5)/2") and value("C = 3.5 + 2k", "k", {"C": 15.5}) == 6
assert is_re("E = ½mv²", "v", "v = √(2E/m)") and value("v = √(2E/m)", "v", {"E": 400, "m": 8}) == 10
Eq = [("<b>One fraction, then solve.</b> (a) Write (x + 3)/2 + (x − 2)/3 as a single fraction. (b) Hence solve (x + 3)/2 + (x − 2)/3 = 5.",
       "(a) (3(x + 3) + 2(x − 2))/6 = <b>(5x + 5)/6</b> (b) 5x + 5 = 30 → <b>x = 5</b>"),
      ("<b>Divide, then solve.</b> (a) Divide x² + 3x − 28 by x − 4. (b) Use your answer to solve x² + 3x − 28 = 0.",
       "(a) <b>x + 7</b> (b) (x − 4)(x + 7) = 0 → <b>x = 4 or x = −7</b>"),
      ("<b>The taxi.</b> A taxi fare is C = 3.5 + 2k euro for k km. (a) Make k the subject. (b) A fare is €15.50. How far was the trip?",
       "(a) <b>k = (C − 3.5)/2</b> (b) (15.5 − 3.5)/2 = <b>6 km</b>"),
      ("<b>Higher Level.</b> E = ½mv². (a) Make v the subject. (b) Find v when E = 400 and m = 8.",
       "(a) 2E = mv² → <b>v = √(2E/m)</b> (b) √(800/8) = √100 = <b>10</b>")]

def qs(items): return "".join(f"<li>{q} <span class='line'></span></li>" for q in items)
def style(var):
    return re.search(var + r' = f"""<!doctype.*?<style>(.*?)</style>', open(os.path.join(SRC, "build_money1_pdfs.py"), encoding="utf-8").read(), re.S).group(1).replace("{LO}", LO).replace("{{", "{").replace("}}", "}")
SHEET_STYLE = style("sheet"); PACK_STYLE = style("pack")
assert "@bottom-left" in SHEET_STYLE and "Single-teacher licence" in PACK_STYLE
EXTRA = """.wk{font-variant-numeric:tabular-nums;line-height:1.95;border:1.5px solid var(--line);border-radius:8px;padding:2px 7px;margin:3px 0;font-size:9.2pt}.wk b.h{display:block}
.fr{display:inline-flex;flex-direction:column;vertical-align:middle;text-align:center;margin:0 2px;line-height:1.1}.fr>span:first-child{border-bottom:1.3px solid currentColor;padding:0 3px}
pre.ld{font:600 9.6pt/1.3 "DejaVu Sans Mono",Menlo,monospace;border:1.5px solid var(--line);border-radius:8px;padding:3px 8px;margin:3px 0}
.flow{display:flex;align-items:center;gap:4px;font-weight:800;font-size:10pt;margin:2px 0}.flow span{border:1.5px solid var(--line);border-radius:6px;padding:0 6px}"""
def fr(t, b): return f'<span class="fr"><span>{t}</span><span>{b}</span></span>'
LD = """              x + 3
      ┌─────────────
x + 2 │ x² + 5x + 6
      −(x² + 2x)
        ───────
             3x + 6
           −(3x + 6)
             ──────
                  0"""

sheet = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Algebraic fractions, long division and changing the subject: rules and practice | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{SHEET_STYLE}
{EXTRA}
</style></head><body>
<div class="page tight">
  <div class="band"><div><div class="k">Junior Cycle Maths · Free revision sheet</div><h1>Algebraic fractions &amp; changing the subject</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2018 specification): {LO}. Play the game: <b>{GAME}</b></p>
  <div class="two">
   <div><h2>1. Adding and subtracting fractions</h2>
    <p>Just like number fractions: same bottom first, then add the tops. {fr(1,2)} + {fr(1,3)} = {fr(3,6)} + {fr(2,6)} = {fr(5,6)}</p>
    <div class="wk"><b class="h">{fr("x + 3",4)} − {fr("x − 2",6)}</b>= {fr("3(x + 3) − 2(x − 2)",12)} = {fr("3x + 9 − 2x + 4",12)} = <b>{fr("x + 13",12)}</b></div>
    <p>Put each top in a <b>bracket</b>. The minus sign multiplies the <b>whole</b> bracket: −2 × −2 = +4. Never add the bottoms.</p>
    <h2>2. Long division</h2>
    <p>Divide, multiply, subtract, bring down. Same as 156 ÷ 12.</p>
    <pre class="ld">{LD}</pre>
    <p>x² ÷ x = <b>x</b> · x(x + 2) = x² + 2x · subtract: 3x · 3x ÷ x = <b>3</b> · 3(x + 2) = 3x + 6 · remainder 0.<br><b>Check:</b> (x + 3)(x + 2) = x² + 5x + 6 ✓</p></div>
   <div><h2>3. Changing the subject</h2>
    <p>Undo the steps in <b>reverse order</b>. y = 3x + 5:</p>
    <div class="flow"><span>x</span>→<span>× 3</span>→<span>+ 5</span>→<span>y</span></div>
    <div class="flow"><span>y</span>→<span>− 5</span>→<span>÷ 3</span>→<span>x</span> &nbsp; so x = {fr("y − 5",3)}</div>
    <div class="wk"><b class="h">v = u + at → make t the subject</b>v − u = at → t = {fr("v − u","a")}</div>
    <div class="wk"><b class="h">y = (x + 4)/3 → make x the subject</b>A fraction? Multiply it away first: 3y = x + 4 → x = 3y − 4</div>
    <h2>4. Higher Level</h2>
    <div class="wk"><b class="h">{fr(3,"x + 2")} − {fr(1,"x − 1")}</b>= {fr("3(x − 1) − 1(x + 2)","(x + 2)(x − 1)")} = {fr("2x − 5","(x + 2)(x − 1)")}</div>
    <div class="wk"><b class="h">A = πr² → r</b>r² = A/π → r = √(A/π) (square root last)</div>
    <div class="wk"><b class="h">Subject twice: y = (x + 2)/(x − 3)</b>xy − 3y = x + 2 → xy − x = 3y + 2 → x(y − 1) = 3y + 2 → x = {fr("3y + 2","y − 1")}</div>
    <div class="wk"><b class="h">(x³ − 8) ÷ (x − 2)</b>Write x³ + 0x² + 0x − 8 so nothing gets lost → x² + 2x + 4</div>
    <div class="note"><b>Classic mistakes:</b> adding the bottoms · not changing the sign of the second term after a minus · moving a number before multiplying away the fraction · dividing only one term · π outside the square root.</div></div>
  </div>
  <div class="tip"><b>Exam tip:</b> one step per line. After long division, multiply back to check. After rearranging, put in easy numbers to check both formulas agree.</div>
</div>

<div class="page p2">
  <div class="band"><div><div class="k">Practice · 32 questions</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Write as a single fraction (Q8: simplify)</h2>
  <ol class="q" style="columns:2;column-gap:8mm">{qs(q for q, a in A)}</ol>
  <h2>B. Divide</h2><ol class="q" start="9" style="columns:2;column-gap:8mm">{qs(f"({t}) ÷ ({d})" for t, d, a in B)}</ol>
  <h2>C. Change the subject</h2><ol class="q" start="15" style="columns:2;column-gap:8mm">{qs(f"{F}. Make {s} the subject." for F, s, a in CQ)}<li>F = 1.8C + 32. Make C the subject, then find C when F = 77. <span class='line'></span></li></ol>
  <h2>D. Higher Level</h2><ol class="q" start="23" style="columns:2;column-gap:8mm">{qs(q for q, a, k in D)}</ol>
  <p class="small" style="margin-top:4px">Questions 29–32 are on the next page.</p>
</div>

<div class="page">
  <div class="band"><div><div class="k">Exam-style · then check</div><h1>Exam corner + answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>E. Exam-style questions (show your work)</h2>
  <ol class="q e3" start="29">{"".join(f"<li>{q}<span class='long'></span><span class='long'></span></li>" for q, a in Eq)}</ol>
  <h2 style="margin-top:10px">Answers</h2>
  <table class="ans"><tbody>
   <tr><td><b>A</b></td><td>{" · ".join(f"{i}. {a}" for i, (q, a) in enumerate(A, 1))}</td></tr>
   <tr><td><b>B</b></td><td>{" · ".join(f"{i}. {a}" for i, (t, d, a) in enumerate(B, 9))}</td></tr>
   <tr><td><b>C</b></td><td>{" · ".join(f"{i}. {a}" for i, (F, s, a) in enumerate(CQ, 15))} · 22. C = (F − 32)/1.8; C = {C8}</td></tr>
   <tr><td><b>D</b></td><td>{" · ".join(f"{i}. {a}" for i, (q, a, k) in enumerate(D, 23))}</td></tr>
   <tr><td><b>E</b></td><td>{" · ".join(f"{i}. {a}" for i, (q, a) in enumerate(Eq, 29))}</td></tr>
  </tbody></table>
  <div class="note"><b>Got one wrong?</b> Did you put each top in a bracket? Did the minus change BOTH signs? Did you multiply back to check your division? Did you undo the steps in reverse order? Then play <b>Rearrange Race</b> at {GAME}: the "Go back over these" list at the end shows the rule for each mistake.</div>
  <p class="small">All questions written by Léim. Léim is independent and not connected with the State Examinations Commission or the NCCA.</p>
</div>
</body></html>"""
NQ = len(A) + len(B) + len(CQ) + 1 + len(D) + len(Eq)
assert NQ == 32, NQ

# ---------- teacher pack ----------
MATCH = [("y = 3x + 2", "x", "x = (y − 2)/3"), ("y = 3x − 2", "x", "x = (y + 2)/3"), ("y = (x + 2)/3", "x", "x = 3y − 2"),
         ("y = x/3 + 2", "x", "x = 3(y − 2)"), ("y = 2 − 3x", "x", "x = (2 − y)/3"), ("A = lw", "l", "l = A/w"),
         ("P = 2l + 2w", "w", "w = (P − 2l)/2"), ("v = u + at", "t", "t = (v − u)/a"), ("s = d/t", "t", "t = d/s"),
         ("C = 2πr", "r", "r = C/(2π)"), ("E = mgh", "h", "h = E/(mg)"), ("A = πr² (Higher Level)", "r", "r = √(A/π)")]
mf = [re.sub(r" \(Higher Level\)", "", F) for F, s, a in MATCH]
for i in range(12):   # each answer card fits its own formula card and no other
    fit = [j for j in range(12) if MATCH[j][1] == MATCH[i][1] and is_re(mf[j], MATCH[j][1], MATCH[i][2])]
    assert fit == [i], (i, fit)
random.seed(35); order = list(range(24)); random.shuffle(order)
cards = [("q", i) for i in range(12)] + [("a", i) for i in range(12)]
match_print = [cards[k] for k in order]
def card_html(c):
    kind, i = c
    if kind == "a": return f'<div class="fc{" sm" if len(MATCH[i][2]) > 13 else ""}">{MATCH[i][2]}</div>'
    hl = "Higher Level: " if "Higher" in MATCH[i][0] else ""
    return f'<div class="fc">{mf[i]}<br><span style="font-size:7.5pt;font-weight:600">{hl}make {MATCH[i][1]} the subject</span></div>'
match_html = "".join(f'<div class="c"><span class="tag">Card {k}</span>{card_html(c)}</div>' for k, c in enumerate(match_print, 1))
match_key = " · ".join(f"{match_print.index(('q', i)) + 1} → {match_print.index(('a', i)) + 1}" for i in range(12))

# Formula Swap: each fact on exactly ONE card
SW1 = [("Formula", "C = f + rm", "AB"), ("Monthly fee f", "€12", "A"), ("Cost per minute r", "€0.05", "B"), ("This month's bill C", "€20", "A"),
       ("Rearranged formula", "", None), ("Minutes used m", "", None)]
assert is_re("C = f + rm", "m", "m = (C − f)/r") and value("C = f + rm", "m", {"C": 20, "f": 12, "r": 0.05}) == 160
SW2 = [("Formula", "P = 2l + 2w", "AB"), ("Width w", "4.5 m", "B"), ("Perimeter P", "31 m", "A"),
       ("Rearranged formula", "", None), ("Length l", "", None)]
assert is_re("P = 2l + 2w", "l", "l = (P − 2w)/2") and value("P = 2l + 2w", "l", {"P": 31, "w": 4.5}) == 11
for rows in (SW1, SW2): assert sum(w == "A" for *_, w in rows) >= 1 and sum(w == "B" for *_, w in rows) >= 1
def swap_card(who):
    def tab(title, rows):
        return f'<table class="ss"><thead><tr><th colspan="2">{title}</th></tr></thead><tbody>' + "".join(
            f"<tr><td>{k}</td><td><b>{v if w and who in w else ''}</b></td></tr>" for k, v, w in rows) + "</tbody></table>"
    return f'<div class="idc"><h3>Student {who} · Formula Swap</h3><div class="two">{tab("The phone bill", SW1)}{tab("The garden", SW2)}</div></div>'

# Rearranging Dominoes: 20 clues, 20 different answers
DOMS = [("y = x + 9 → x", "x = y − 9", ("r", "y = x + 9", "x")), ("y = 5x → x", "x = y/5", ("r", "y = 5x", "x")),
        ("y = 2x + 6 → x", "x = (y − 6)/2", ("r", "y = 2x + 6", "x")), ("y = 3x − 1 → x", "x = (y + 1)/3", ("r", "y = 3x − 1", "x")),
        ("y = x/4 → x", "x = 4y", ("r", "y = x/4", "x")), ("y = (x + 1)/2 → x", "x = 2y − 1", ("r", "y = (x + 1)/2", "x")),
        ("y = 7 − x → x", "x = 7 − y", ("r", "y = 7 − x", "x")), ("s = d/t → d", "d = st", ("r", "s = d/t", "d")),
        ("V = lwh → w", "w = V/(lh)", ("r", "V = lwh", "w")), ("C = πd → d", "d = C/π", ("r", "C = πd", "d")),
        ("x/3 + x/6", "x/2", ("e", "x/3 + x/6")), ("x/2 − x/5", "3x/10", ("e", "x/2 − x/5")),
        ("(x + 1)/3 + (x + 2)/3", "(2x + 3)/3", ("e", "(x + 1)/3 + (x + 2)/3")), ("(x + 4)/2 + x/4", "(3x + 8)/4", ("e", "(x + 4)/2 + x/4")),
        ("(x² + 6x + 8) ÷ (x + 2)", "x + 4", ("d", "x² + 6x + 8", "x + 2")), ("(x² − 4x − 12) ÷ (x − 6)", "x + 2", ("d", "x² − 4x − 12", "x − 6")),
        ("(2x² + 5x + 3) ÷ (x + 1)", "2x + 3", ("d", "2x² + 5x + 3", "x + 1")),
        ("Higher Level: A = πr² → r", "r = √(A/π)", ("r", "A = πr²", "r")), ("Higher Level: 2/x + 3/(x + 1)", "(5x + 2)/(x(x + 1))", ("e", "2/x + 3/(x + 1)")),
        ("Higher Level: (x³ − 1) ÷ (x − 1)", "x² + x + 1", ("d", "x³ − 1", "x − 1"))]
for clue, a, chk in DOMS:
    if chk[0] == "r": assert is_re(chk[1], chk[2], a), clue
    elif chk[0] == "e": assert is_expr(chk[1], a), clue
    else: assert is_div(chk[1], chk[2], a), clue
DANS = [a for c, a, k in DOMS]; assert len(set(DANS)) == 20
for a, b in itertools.combinations(DANS, 2):          # no two answers are the same thing written differently
    if "=" in a or "=" in b:
        if a.split(" = ")[0] == b.split(" = ")[0]: assert not zero(P(a.split(" = ")[1]) - P(b.split(" = ")[1])), (a, b)
    else: assert not zero(P(a) - P(b)), (a, b)
random.seed(3535); chain = DOMS[:]; random.shuffle(chain)
dom = [("START" if k == 0 else chain[k - 1][1], x[0]) for k, x in enumerate(chain)] + [(chain[-1][1], "FINISH")]
dom_print = dom[:]; random.shuffle(dom_print)
dom_html = "".join(f'<div class="dom"><div class="h l{" sm" if len(l) > 11 else ""}">{l}</div><div class="h r">{r}</div></div>' for l, r in dom_print)
chain_key = "".join(f"<li>{x} = <b>{a}</b></li>" for x, a, k in chain)

ERR = [("x/2 + x/3", "2x/5", "Added the bottoms. Common bottom 6: <b>5x/6</b>"),
       ("(x + 3)/2 − (x − 1)/4 = (2x + 6 − x − 1)/4", "(x + 5)/4", "−(x − 1) = −x <b>+ 1</b>: <b>(x + 7)/4</b>"),
       ("y = 4x + 8. Make x the subject.", "x = y/4 − 8", "Divided only y by 4. Subtract 8 first: <b>x = (y − 8)/4</b>"),
       ("y = (x − 2)/5. Make x the subject.", "x = y/5 + 2", "Multiply by 5, don't divide: 5y = x − 2, <b>x = 5y + 2</b>"),
       ("(x² + 7x + 10) ÷ (x + 2). Line 1: x² ÷ x = x", "x + 7", "After x(x + 2), subtract: 7x − 2x = 5x, so <b>x + 5</b>"),
       ("Higher Level: A = πr². Make r the subject.", "r = √A/π", "π must be inside the root: <b>r = √(A/π)</b>")]
assert is_expr("x/2 + x/3", "5x/6") and is_expr("(x + 3)/2 − (x − 1)/4", "(x + 7)/4") and not is_expr("(x + 3)/2 − (x − 1)/4", "(x + 5)/4")
assert is_re("y = 4x + 8", "x", "x = (y − 8)/4") and not is_re("y = 4x + 8", "x", "x = y/4 − 8")
assert is_re("y = (x − 2)/5", "x", "x = 5y + 2") and not is_re("y = (x − 2)/5", "x", "x = y/5 + 2")
assert is_div("x² + 7x + 10", "x + 2", "x + 5") and is_re("A = πr²", "r", "r = √(A/π)") and not is_re("A = πr²", "r", "r = √A/π")
# worksheet exam-style
assert is_expr("(2x − 1)/3 + (x + 4)/2", "(7x + 10)/6") and is_div("3x² + 11x − 4", "x + 4", "3x − 1")
assert is_re("C = 6 + 4h", "h", "h = (C − 6)/4") and value("C = 6 + 4h", "h", {"C": 30}) == 6
assert is_re("v² = u² + 2sa", "s", "s = (v² − u²)/(2a)") and value("v² = u² + 2sa", "s", {"v": 20, "u": 10, "a": 5}) == 30
assert is_expr("4/(x − 3) − 1/(x + 2)", "(3x + 11)/((x − 3)(x + 2))") and is_re("y = (2x + 1)/(x − 3)", "x", "x = (3y + 1)/(y − 2)")

pack = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Algebraic Fractions &amp; Changing the Subject Teacher Pack | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{PACK_STYLE}
{EXTRA}
.ss td:nth-child(2){{width:34%}}.ss td,.ss th{{padding:2px 5px;font-size:8.8pt;line-height:1.3}}.fym{{grid-template-columns:repeat(3,1fr)}}.fym .c{{height:13mm}}.fym .fc{{font-size:11.5pt;line-height:1.1}}.fym .fc.sm{{font-size:10.5pt}}.idc{{padding:1mm 4mm}}.idc h3{{margin:0 0 1mm}}.p1 .proc td{{font-size:8.5pt;padding:2px 6px}}
.dom .r{{font-size:9pt}}.dom .l{{font-size:11pt}}.dom .l.sm{{font-size:9pt}}.ops div{{font-size:12pt}}
</style></head><body>

<div class="page p1">
  <div class="band"><div><div class="k">Junior Cycle Maths · Teacher pack</div><h1>Algebraic fractions &amp; changing the subject</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2018 specification): {LO}</p>
  <div class="two">
    <div><h3>Aims</h3><p>By the end of the lesson students can add and subtract algebraic fractions with number denominators, divide a quadratic by a linear expression (long division), and change the subject of a formula, then use the new formula. Higher Level: fractions with x in the denominator, cubic ÷ linear, formulas with squares and square roots, and the subject appearing twice.</p></div>
    <div><h3>In this pack</h3><p>p.1 Teacher notes · p.2 Rearrange Match mingle cards + Formula Swap A/B cards · p.3 Rearranging Dominoes (cut-up) · p.4 Wall poster · p.5 Worksheet: Error Hunt + exam-style questions · p.6 Answers. Level: 3rd year (Higher and Ordinary). Time: about 60 minutes. All questions are original.</p></div>
  </div>
  <h2 style="margin-top:8px">Procedure</h2>
  <table class="proc"><tbody>
    <tr><td>5 min</td><td><b>Lead-in: think of a number.</b> "I thought of a number, multiplied by 3 and added 5. I got 26. What was it?" Students undo it: − 5, ÷ 3. Write y = 3x + 5 and the reverse flow y → − 5 → ÷ 3 → x on the board: that's changing the subject.</td></tr>
    <tr><td>8 min</td><td><b>Guided discovery.</b> Pairs do ½ + ⅓, then x/2 + x/3, then (x + 1)/2 + (x + 4)/3 the same way. Elicit: same bottom first, every top in a bracket. Then 156 ÷ 12 by long division next to (x² + 5x + 6) ÷ (x + 2): same four steps.</td></tr>
    <tr><td>10 min</td><td><b>Rearrange Match mingle</b> (p.2, 24 cards = 12 formula cards + 12 answer cards; one card each). Formula card? Rearrange it, then find the card with your answer. Answer card? Find your formula. Pairs check by putting in easy numbers.</td></tr>
    <tr><td>12 min</td><td><b>Formula Swap</b> (p.2, pairs, don't show your card). Each number is on only ONE card. Ask your partner for what you're missing, rearrange the formula together, then put the numbers in. Feedback: phone bill → <b>160 minutes</b>; garden → <b>11 m</b>.</td></tr>
    <tr><td>10 min</td><td><b>Rearranging Dominoes</b> (p.3), groups of 3–4. Start with START, work out the clue, find the domino with that answer on its left, and build the chain to FINISH.</td></tr>
    <tr><td>12 min</td><td><b>Worksheet</b> (p.5). Error Hunt in pairs (find the mistake, name it, fix it), then the exam-style questions alone. Question 5 is Higher Level.</td></tr>
    <tr><td>3 min</td><td><b>Exit ticket.</b> Make x the subject of y = 2x − 7, then write x/4 + x/6 as one fraction. (x = (y + 7)/2; 5x/12.) Homework: play <b>Rearrange Race</b> at {GAME}.</td></tr>
  </tbody></table>
  <div class="note"><b>Mingle key</b> (formula card → answer card): {match_key}.<br>
  <b>Errors to look for:</b> adding the bottoms · not changing both signs after a minus · moving a term before multiplying away a fraction · dividing only one term · subtracting wrongly in long division · π outside the square root. <b>Support:</b> "What was done to x first? Undo that last." <b>Fast finishers:</b> make up a formula whose rearranged form is x = (y + 4)/5 in two different ways.</div>
  <p class="small"><b>Domino answer chain</b> (START → FINISH):</p>
  <ol class="small" style="columns:2;column-gap:12px;font-size:7.2pt;line-height:1.22;margin:0;padding-left:16px">{chain_key}</ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">Cut up the cards · one Formula Swap card per student</div><h1>Rearrange Match + Formula Swap</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:8.8pt;margin:0"><b>Rearrange Match mingle.</b> Cut out the 24 cards and give one to each student. Formula card? Rearrange it, then find your answer card. Answer card? Find your formula. (Fewer students? Take out whole pairs.)</p>
  <div class="fym">{match_html}</div>
  <p style="font-size:8.8pt;margin:3mm 0 0"><b>Formula Swap.</b> Don't show your card. Each number is on only one of the two cards: ask your partner for what you're missing, rearrange the formula together, then fill in every blank.</p>
  {swap_card("A")}
  {swap_card("B")}
</div>

<div class="page">
  <div class="band"><div><div class="k">Groups of 3–4 · cut along the dashed lines</div><h1>Rearranging Dominoes</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.4pt">Start with START. Work out the clue on the right ("→ x" means make x the subject), then find the domino with that answer on its left. Keep going until you reach FINISH. The last three clues are Higher Level (Ordinary Level groups can be given those answers).</p>
  <div class="doms">{dom_html}</div>
</div>

<div class="page">
  <div class="poster">
    <h1>Fractions · Division · Rearranging</h1>
    <div class="ops">
      <div style="background:var(--green-soft)"><b>Fractions</b>same bottom first<br>every top in a bracket<br>minus → change both signs</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Long division</b>divide · multiply<br>subtract · bring down<br>multiply back to check</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Change the subject</b>undo in reverse order<br>fraction? multiply first<br>y = 3x + 5 → x = (y − 5)/3</div>
      <div style="background:var(--green-soft)"><b>Higher Level</b>square → square root last<br>subject twice: collect,<br>then take it out as a factor</div>
    </div>
    <pre class="ld" style="font-size:15pt;width:max-content;margin:4mm auto">{LD}</pre>
    <p style="text-align:center;font-size:10pt;color:var(--muted)">Léim · leim.ie · Play Rearrange Race: {GAME}</p>
  </div>
</div>

<div class="page ws">
  <div class="band"><div><div class="k">Worksheet</div><h1>Error Hunt + exam-style questions</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Error Hunt</h2>
  <p>Each student's working has one mistake. Find it, say what went wrong, and write the right answer.</p>
  <table class="eh"><thead><tr><th>Question and working</th><th>Student's answer</th><th>The mistake and the right answer</th></tr></thead><tbody>
  {"".join(f"<tr><td>{q}</td><td>{w}</td><td><span class='gap'></span><span class='gap'></span></td></tr>" for q, w, r in ERR)}
  </tbody></table>
  <h2>B. Exam-style questions (show all your work)</h2>
  <ol class="q">
    <li>Write (2x − 1)/3 + (x + 4)/2 as a single fraction.<span class="long"></span></li>
    <li>Divide 3x² + 11x − 4 by x + 4. Check your answer by multiplying.<span class="long"></span></li>
    <li>Hiring a bike costs C = 6 + 4h euro for h hours. (a) Make h the subject. (b) Sinéad paid €30. For how many hours did she hire the bike?<span class="long"></span></li>
    <li>v² = u² + 2as. (a) Make s the subject. (b) Find s when v = 20, u = 10 and a = 5.<span class="long"></span></li>
    <li>Higher Level: (a) Write 4/(x − 3) − 1/(x + 2) as a single fraction. (b) Make x the subject of y = (2x + 1)/(x − 3).<span class="long"></span></li>
  </ol>
</div>

<div class="page an">
  <div class="band"><div><div class="k">For the teacher</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>Formula Swap</h2>
  <div class="two"><table><tbody>
   <tr><td>Rearranged formula</td><td><b>m = (C − f)/r</b></td></tr><tr><td>Working</td><td>(20 − 12) ÷ 0.05 = 8 ÷ 0.05</td></tr>
   <tr><td>Minutes used</td><td><b>160 minutes</b></td></tr></tbody></table>
  <table><tbody>
   <tr><td>Rearranged formula</td><td><b>l = (P − 2w)/2</b></td></tr><tr><td>Working</td><td>(31 − 9) ÷ 2 = 22 ÷ 2</td></tr>
   <tr><td>Length</td><td><b>11 m</b></td></tr></tbody></table></div>
  <h2>A. Error Hunt</h2>
  <table><tbody>{"".join(f"<tr><td style='width:42%'><b>{q}</b></td><td>{r}</td></tr>" for q, w, r in ERR)}</tbody></table>
  <h2>B. Exam-style questions</h2>
  <ol class="q">
    <li>(2(2x − 1) + 3(x + 4))/6 = (4x − 2 + 3x + 12)/6 = <b>(7x + 10)/6</b></li>
    <li>3x² ÷ x = 3x; 3x(x + 4) = 3x² + 12x; subtract: −x − 4; −x ÷ x = −1. Answer <b>3x − 1</b>. Check: (3x − 1)(x + 4) = 3x² + 11x − 4 ✓</li>
    <li>(a) C − 6 = 4h → <b>h = (C − 6)/4</b> (b) (30 − 6)/4 = <b>6 hours</b></li>
    <li>(a) v² − u² = 2as → <b>s = (v² − u²)/(2a)</b> (b) (400 − 100)/10 = <b>30</b></li>
    <li>(a) (4(x + 2) − (x − 3))/((x − 3)(x + 2)) = <b>(3x + 11)/((x − 3)(x + 2))</b> (b) xy − 3y = 2x + 1 → xy − 2x = 3y + 1 → x(y − 2) = 3y + 1 → <b>x = (3y + 1)/(y − 2)</b></li>
  </ol>
  <h2>Marking tip</h2>
  <p>Give credit for each step, as the exam does: the common denominator, the expanded top, the simplified answer. In long division look for like terms lined up and a check by multiplying. When rearranging, one operation per line; in "use the formula" parts accept a correct substitution into a correctly rearranged formula.</p>
</div>
</body></html>"""

cover = """<!doctype html><html><head><meta charset="utf-8"><style>
body{margin:0;width:1200px;height:1200px;background:#1B2430;font-family:Inter,sans-serif;color:#fff;display:flex;flex-direction:column;justify-content:space-between;padding:90px;box-sizing:border-box}
.k{display:inline-block;background:#2E7D57;border-radius:99px;padding:12px 26px;font-weight:700;font-size:28px;letter-spacing:.06em;text-transform:uppercase}
h1{font-size:92px;font-weight:800;line-height:1.16;letter-spacing:-.03em;margin:40px 0 0}
h1 span{background:#F6CF5A;color:#1B2430;padding:0 14px;box-decoration-break:clone;-webkit-box-decoration-break:clone}
.sub{font-size:38px;color:#C9D1DA;margin-top:36px;line-height:1.35}
.em{font-size:50px;margin-top:30px;font-weight:800;letter-spacing:.01em;color:#F6CF5A}
.foot{display:flex;justify-content:space-between;align-items:center;font-size:34px;font-weight:700}
.price{background:#F6CF5A;color:#1B2430;border-radius:16px;padding:14px 28px}
</style></head><body>
<div><span class="k">Junior Cycle Maths · Teacher pack</span>
<h1><span>Algebraic Fractions</span><br><span>&amp; Changing the Subject</span></h1>
<div class="sub">Rearrange Match mingle · Formula Swap A/B<br>Dominoes · Poster · Worksheet + answers</div>
<div class="em">v = u + at → t = (v − u)/a</div></div>
<div class="foot"><span>↗ Léim · leim.ie</span><span class="price">Ready to teach · 60 min</span></div>
</body></html>"""

if __name__ == "__main__":
    for name, txt in [("rules-and-practice", sheet), ("teacher-pack", pack), ("cover", cover)]:
        plain = re.sub(r"<[^>]+>", " ", re.sub(r"<style>.*?</style>|<svg.*?</svg>", "", txt, flags=re.S))
        assert not re.search(r"[\dxy)]\s*-\s*[\dxy(]|[=(]\s*-\d|(?<![\w])-\d", plain), (name, re.findall(r".{20}[\dxy)]\s*-\s*[\dxy(].{10}|.{10}[=(]\s*-\d.{10}", plain)[:3])
        open(os.path.join(SRC, f"{SLUG}-{name}.html"), "w", encoding="utf-8").write(txt)
    def pdf(name, out):
        subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--no-pdf-header-footer", f"--print-to-pdf={out}",
                        f"{SLUG}-{name}.html"], cwd=SRC, check=True, capture_output=True)
        d = open(out, "rb").read(); print(name, len(re.findall(rb"/Type\s*/Page[^s]", d)), "pages")
    pdf("rules-and-practice", os.path.join(ROOT, "printables", f"{SLUG}-rules-and-practice.pdf"))
    pdf("teacher-pack", os.path.join(OUT, "Algebraic-Fractions-Changing-the-Subject-Teacher-Pack-Leim.pdf"))
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--hide-scrollbars", "--window-size=1200,1200",
                    f"--screenshot={os.path.join(OUT, f'{SLUG}-cover.png')}", f"{SLUG}-cover.html"], cwd=SRC, check=True, capture_output=True)
    print("domino chain:", [(x, a) for x, a, k in chain])
