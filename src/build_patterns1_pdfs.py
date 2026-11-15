#!/usr/bin/env python3
"""Patterns 1: linear patterns & sequences (JC Maths topic 9): free sheet + teacher pack + Payhip cover.
Run from the repo root: python3 src/build_patterns1_pdfs.py OUTDIR
Writes src/linear-patterns-sequences-*.html; PDFs/cover PNG go to OUTDIR (free sheet also to printables/).
Every answer is computed from the pattern and asserted; picture patterns are drawn from a stick list and counted."""
import os, sys, random, subprocess, re
from fractions import Fraction
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC)
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/patterns1"; os.makedirs(OUT, exist_ok=True)
SLUG = "linear-patterns-sequences"
LO = "N.4, AF.1a, AF.1b, U.4, U.11"

def n(x): return ("−" + str(-x)) if x < 0 else str(x)
def S(a, d, k=4): return [a + i * d for i in range(k)]
def ss(l, more=True): return ", ".join(n(x) for x in l) + (", …" if more else "")
def R(d, b, v="n"):
    """rule d·v + b written like the game: positive term first (34 − 4n)."""
    t = ("" if abs(d) == 1 else str(abs(d))) + v
    if d > 0: return t + ("" if b == 0 else (" + " + str(b) if b > 0 else " − " + str(-b)))
    return str(b) + " − " + t if b > 0 else "−" + t + ("" if b == 0 else " − " + str(-b))
def rule_of(l):
    """general term (d, b) of a linear list, asserting it is linear."""
    d = l[1] - l[0]; assert all(y - x == d for x, y in zip(l, l[1:])), l
    return d, l[0] - d
def T(d, b, k): return d * k + b
def which(l, X):
    d, b = rule_of(l); k = Fraction(X - b, d); return int(k) if k.denominator == 1 and k >= 1 else None
assert R(3, 1) == "3n + 1" and R(-4, 34) == "34 − 4n" and R(2, -1) == "2n − 1" and R(1, 4) == "n + 4"

# ---------- matchstick pictures (same drawing rules as the game) ----------
def edges(kind, k):
    E, out = set(), []
    def add(p, q):
        key = tuple(sorted([p, q]))
        if key not in E: E.add(key); out.append((p, q))
    for i in range(k):
        if kind in ("squares", "houses"):
            add((i, 0), (i + 1, 0)); add((i + 1, 0), (i + 1, 1)); add((i + 1, 1), (i, 1)); add((i, 1), (i, 0))
            if kind == "houses": add((i, 1), (i + .5, 1.7)); add((i + 1, 1), (i + .5, 1.7))
        elif kind == "double":
            for r in (0, 1): add((i, r), (i + 1, r)); add((i + 1, r), (i + 1, r + 1)); add((i + 1, r + 1), (i, r + 1)); add((i, r + 1), (i, r))
        else:
            j = i // 2
            if i % 2 == 0: add((j, 0), (j + 1, 0)); add((j, 0), (j + .5, .87)); add((j + 1, 0), (j + .5, .87))
            else: add((j + .5, .87), (j + 1.5, .87)); add((j + 1, 0), (j + 1.5, .87))
    return out
def count(kind, k): return len(edges(kind, k))
STICK = {kind: rule_of([count(kind, k) for k in (1, 2, 3, 4, 5)]) for kind in ("squares", "triangles", "houses", "double")}
assert STICK == {"squares": (3, 1), "triangles": (2, 1), "houses": (5, 1), "double": (5, 2)}, STICK
def sticks(kind, stages=(1, 2, 3), h="13mm", labels=True):
    u, x0, H = 24, 6, {"houses": 1.7, "double": 2}.get(kind, 1); base = 8 + H * u; o = ""
    for k in stages:
        aw = (k + 1) // 2 + (.5 if k % 2 == 0 else 0) if kind == "triangles" else k; w = max(1.8, aw); ox = x0 + (w - aw) * u / 2
        for (a, b), (c, d) in edges(kind, k):
            o += f'<line x1="{ox + a * u:.1f}" y1="{base - b * u:.1f}" x2="{ox + c * u:.1f}" y2="{base - d * u:.1f}" stroke="#C0392B" stroke-width="3.5" stroke-linecap="round"/>'
        if labels: o += f'<text x="{x0 + w * u / 2:.1f}" y="{base + 18}" font-size="12" font-weight="700" text-anchor="middle" font-family="Inter,sans-serif" fill="#1B2430">Stage {k}</text>'
        x0 += w * u + 26
    return f'<svg viewBox="0 0 {x0 - 18:.0f} {base + (24 if labels else 6):.0f}" style="height:{h};width:auto;max-width:100%">{o}</svg>'
def graph(pts, xlab, ylab, h="40mm"):
    W, H, L, B, Tp, Rt = 300, 200, 40, 168, 12, 286; xmax = pts[-1][0] + 1; ymax = max(y for x, y in pts)
    step = 2 if ymax <= 12 else 5 if ymax <= 30 else 10; ymax = -(-(ymax + 1) // step) * step
    X = lambda x: L + (Rt - L) * x / xmax; Y = lambda y: B - (B - Tp) * y / ymax; o = ""
    for y in range(0, ymax + 1, step): o += f'<line x1="{L}" y1="{Y(y):.1f}" x2="{Rt}" y2="{Y(y):.1f}" stroke="#E5E7EB"/><text x="{L - 6}" y="{Y(y) + 4:.1f}" font-size="11" text-anchor="end" fill="#5B6470">{y}</text>'
    for x in range(xmax): o += f'<text x="{X(x):.1f}" y="{B + 15}" font-size="11" text-anchor="middle" fill="#5B6470">{x}</text>'
    o += f'<line x1="{L}" y1="{B}" x2="{Rt}" y2="{B}" stroke="#1B2430" stroke-width="2"/><line x1="{L}" y1="{B}" x2="{L}" y2="{Tp}" stroke="#1B2430" stroke-width="2"/>'
    o += f'<text x="{(L + Rt) / 2}" y="{H - 2}" font-size="12" font-weight="700" text-anchor="middle">{xlab}</text><text x="12" y="{(Tp + B) / 2}" font-size="12" font-weight="700" text-anchor="middle" transform="rotate(-90 12 {(Tp + B) / 2})">{ylab}</text>'
    for x, y in pts: o += f'<circle cx="{X(x):.1f}" cy="{Y(y):.1f}" r="5" fill="#C0392B"/>'
    o += f'<line x1="{X(pts[0][0]):.1f}" y1="{Y(pts[0][1]):.1f}" x2="{X(pts[-1][0]):.1f}" y2="{Y(pts[-1][1]):.1f}" stroke="#C0392B" stroke-dasharray="4 4"/>'
    return f'<svg viewBox="0 0 {W} {H}" style="height:{h};width:auto" font-family="Inter,sans-serif" fill="#1B2430">{o}</svg>'

# ---------- free sheet ----------
A = [(S(4, 5), 2), (S(30, -3), 2), (S(-7, 4), 2), (S(11, 9), 2)]
Aq = [(f"Write the next two terms: {ss(l)}", f"{n(T(*rule_of(l), 5))}, {n(T(*rule_of(l), 6))}") for l, _ in A]
miss = [([6, None, 20, 27], 13), ([45, 39, None, 27], 33), ([None, 2, 9, 16], -5)]
for l, a in miss:
    known = [(i, v) for i, v in enumerate(l) if v is not None]; d = (known[1][1] - known[0][1]) // (known[1][0] - known[0][0])
    assert a == known[0][1] + (l.index(None) - known[0][0]) * d and all(v == known[0][1] + (i - known[0][0]) * d for i, v in known)
Aq += [(f"Fill in the gap: {', '.join('__' if v is None else n(v) for v in l)}", n(a)) for l, a in miss]
Aq += [(f"What is the common difference of {ss(S(52, -7))}?", n(rule_of(S(52, -7))[0]))]
assert len(Aq) == 8
Bl = [S(5, 3), S(9, 4), S(1, 6), S(2, 5), S(20, -2), S(-3, 3)]
Bq = [(f"Find Tₙ for {ss(l)}", R(*rule_of(l))) for l in Bl]
tabB = [12, 19, 26, 33]; Bq.append((f"Find the rule for this table: n = 1, 2, 3, 4 → {', '.join(map(str, tabB))}", R(*rule_of(tabB))))
Bq.append(("Write the first four terms of Tₙ = 6n − 4", ss([T(6, -4, k) for k in (1, 2, 3, 4)], False)))
assert [a for q, a in Bq] == ["3n + 2", "4n + 5", "6n − 5", "5n − 3", "22 − 2n", "3n − 6", "7n + 5", "2, 8, 14, 20"], [a for q, a in Bq]
Cl = S(3, 4)
Cq = [(f"Find the 20th term of {ss(Cl)}", n(T(*rule_of(Cl), 20))), (f"Find the 100th term of {ss(Cl)}", n(T(*rule_of(Cl), 100))),
      (f"Which term of {ss(Cl)} is 83?", str(which(Cl, 83))), (f"Is 100 a term of {ss(Cl)}? Explain.", "No: (100 − 3) ÷ 4 = 24.25, not a whole number"),
      (f"Find the 50th term of {ss(S(90, -2))}", n(T(*rule_of(S(90, -2)), 50))), (f"Which term of {ss(S(7, 6))} is 157?", str(which(S(7, 6), 157))),
      (f"Is 95 a term of {ss(S(5, 9))}? If so, which?", f"Yes: term {which(S(5, 9), 95)}"),
      ("Tₙ = 8n − 3. Which term is 117?", str(which([T(8, -3, k) for k in (1, 2, 3)], 117)))]
assert which(Cl, 100) is None and [a for q, a in Cq] == ["79", "399", "21", Cq[3][1], "−8", "26", "Yes: term 11", "15"], [a for q, a in Cq]
d_t, b_t = STICK["triangles"]
Dq = [("The matchstick triangles at the top of page 1: how many matchsticks in stage 4?", str(T(d_t, b_t, 4))),
      ("…and in stage 20?", str(T(d_t, b_t, 20))), ("…write the rule for stage n.", R(d_t, b_t)),
      ("Ella has €40 and saves €12 a week. Write a formula for her savings S after w weeks.", "S = " + R(12, 40, "w")),
      ("…how much will she have after 8 weeks?", "€" + str(T(12, 40, 8))), ("…after how many weeks will she have €220?", str(Fraction(220 - 40, 12)))]
assert [a for q, a in Dq] == ["9", "41", "2n + 1", "S = 12w + 40", "€136", "15"], [a for q, a in Dq]
assert count("triangles", 4) == 9 and count("triangles", 20) == 41
# exam-style
e1 = [T(3, 2, k) for k in (1, 2, 3, 4, 5)]; assert e1[:3] == [5, 8, 11] and rule_of(e1) == (3, 2)
e1c, e1d = T(3, 2, 30), which(e1, 125); assert (e1c, e1d) == (92, 41)
e2 = S(50, -4); d2, b2 = rule_of(e2); e2b = T(d2, b2, 10); e2c = min(k for k in range(1, 100) if T(d2, b2, k) < 0)
assert (R(d2, b2), e2b, e2c, T(d2, b2, e2c)) == ("54 − 4n", 14, 14, -2)
e3 = (R(3, 8, "w"), T(3, 8, 10), Fraction(50 - 8, 3)); assert e3 == ("3w + 8", 38, 14)
gA = [10 + 2 * g for g in range(7)]; gB = [4 * g for g in range(7)]; eqg = [g for g in range(7) if gA[g] == gB[g]]; assert eqg == [5] and gA[5] == 20
E4 = [("Tiles: stage 1 has 5 tiles, stage 2 has 8, stage 3 has 11. (a) Make a table for stages 1 to 5. (b) Find a formula for the number of tiles in stage n. (c) How many tiles are in stage 30? (d) Which stage uses 125 tiles?",
       f"(a) {ss(e1, False)} (b) <b>3n + 2</b> (c) 3(30) + 2 = <b>{e1c}</b> (d) (125 − 2) ÷ 3 = <b>stage {e1d}</b>"),
      ("The sequence 50, 46, 42, 38, … (a) Find Tₙ. (b) Find T₁₀. (c) Which is the first term that is less than zero? Explain.",
       f"(a) <b>54 − 4n</b> (b) 54 − 40 = <b>{e2b}</b> (c) T₁₃ = 2 and T₁₄ = −2, so <b>T₁₄ = −2</b>"),
      ("Hannah's plant is 8 cm tall and grows 3 cm a week. (a) Write a formula for its height h after w weeks. (b) Find the height after 10 weeks. (c) After how many weeks will it be 50 cm? (d) On a graph of h against w, what are the start value and the rate of change?",
       f"(a) <b>h = 3w + 8</b> (b) <b>{e3[1]} cm</b> (c) (50 − 8) ÷ 3 = <b>{e3[2]} weeks</b> (d) start value <b>8 cm</b>, rate of change <b>3 cm per week</b>"),
      ("Data plans: Plan A costs €10 plus €2 per GB. Plan B costs €4 per GB. (a) Make a table of the cost of each plan for 0 to 6 GB. (b) For how many GB do the plans cost the same? (c) Which plan is cheaper for 8 GB?",
       f"(a) A: {ss(gA, False)}; B: {ss(gB, False)} (b) <b>5 GB</b> (both €20) (c) A: €{10 + 2 * 8}, B: €{4 * 8}, so <b>Plan A</b>")]
assert 10 + 2 * 8 < 4 * 8

def qs(items, cls=""): return "".join(f"<li>{q} <span class='line'></span></li>" for q, a in items)
sheet = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Linear patterns and sequences, rules and practice | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>@page{{@bottom-left{{content:"Léim · leim.ie · Free to print for home or class · JC Maths LOs (2018 spec): {LO}"}}}}
.tight{{font-size:9.9pt;line-height:1.4}}.tight td,.tight th{{padding:3px 6px}}.tight h2{{margin:8px 0 4px;font-size:13.5pt}}.tight .note,.tight .tip{{padding:6px 10px;margin:6px 0}}
ol.q{{padding-left:30px}}ol.q li{{margin:7px 0}}
.ans td{{padding:3px 6px;font-size:9pt}}
.p2{{font-size:9.5pt;line-height:1.36}}.p2 ol.q li{{margin:4px 0}}.p2 h2{{margin:8px 0 4px;font-size:13pt}}.p2 .line{{min-width:60px}}
.pic{{text-align:center;margin:4px 0}}
</style></head><body>
<div class="page tight">
  <div class="band"><div><div class="k">Junior Cycle Maths · Free revision sheet</div><h1>Linear patterns &amp; sequences</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2018 specification): {LO}. Play the game: <b>leim.ie/pattern-builder.html</b></p>
  <div class="two">
   <div><h2>1. The words</h2>
    <p>A <b>sequence</b> is a list of numbers in order: 5, 8, 11, 14, … Each number is a <b>term</b>: T₁ = 5, T₂ = 8. <b>Tₙ</b> is the nth term.</p>
    <p>In a <b>linear</b> pattern you add (or take away) the <b>same amount</b> every time: the <b>common difference</b>. 5, 8, 11, … goes up by <b>3</b>; 20, 16, 12, … by <b>−4</b>.</p>
    <h2>2. Finding Tₙ (the general term)</h2>
    <p>1. Find the common difference d: the rule starts <b>dn</b>.<br>2. Compare dn with T₁, then add or take away.<br>3. <b>Check</b> with T₂.</p>
    <p>5, 8, 11, …: d = 3, so 3n. 3(1) = 3, but T₁ = 5: add 2. <b>Tₙ = 3n + 2</b>. Check: 3(2) + 2 = 8 ✓<br>30, 26, 22, …: d = −4. −4(1) = −4, T₁ = 30: add 34. <b>Tₙ = 34 − 4n</b>.</p>
    <p class="small">Not "n + 3": that only says how to get from one term to the next. Test it: n = 1 gives 4, not 5.</p>
    <h2>3. Picture patterns</h2>
    <div class="pic">{sticks("triangles", h="15mm")}</div>
    <p>Each new stage adds <b>2</b> matchsticks, and stage 1 has 3 = 2 + <b>1</b>, so stage n has <b>2n + 1</b>. Stage 10 has 21, <b>not</b> 10 × 3 = 30.</p></div>
   <div><h2>4. Far-away terms, working backwards</h2>
    <p><b>50th term</b> of 5, 8, 11, …: 3(50) + 2 = <b>152</b> (or 5 + <b>49</b> jumps of 3).</p>
    <p><b>Which term is 65?</b> (65 − 5) ÷ 3 = 20 jumps after T₁, so it's <b>T₂₁</b>. Check: 3(21) + 2 = 65 ✓</p>
    <p><b>Is 100 a term?</b> (100 − 5) ÷ 3 = 31.66…, not whole, so <b>no</b>.</p>
    <h2>5. Tables and graphs</h2>
    <table><tbody><tr><td><b>n</b></td><td>1</td><td>2</td><td>3</td><td>4</td></tr><tr><td><b>Tₙ</b></td><td>5</td><td>8</td><td>11</td><td>14</td></tr></tbody></table>
    <p>Plot the points (n, Tₙ): a linear pattern makes a <b>straight line</b>.</p>
    <h2>6. Real life</h2>
    <div class="pic">{graph([(w, 35 + 15 * w) for w in range(5)], "Weeks (w)", "Savings (€)", h="33mm")}</div>
    <p>€35 saved, plus €15 a week. <b>Start value</b> = 35 (week 0, where the line meets the axis). <b>Rate of change</b> = 15 per week. <b>S = 15w + 35</b>.</p></div>
  </div>
  <div class="tip"><b>Exam tip:</b> fill in tables carefully (later parts use them), check every rule with two terms, and show your working for "which stage?" questions: (100 − 1) ÷ 3 = 33.</div>
</div>

<div class="page p2">
  <div class="band"><div><div class="k">Practice · 34 questions</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <div class="two"><div><h2>A. Continue the pattern</h2><ol class="q">{qs(Aq)}</ol></div>
  <div><h2>B. Find the rule</h2><ol class="q" start="9">{qs(Bq)}</ol></div></div>
  <h2>C. Far-away terms and working backwards</h2><ol class="q" start="17">{qs(Cq)}</ol>
  <h2>D. Pictures and real life</h2><ol class="q" start="25">{qs(Dq)}</ol>
  <p class="small" style="margin-top:6px">Questions 31–34 are on the next page.</p>
</div>

<div class="page">
  <div class="band"><div><div class="k">Exam-style · then check</div><h1>Exam corner + answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>E. Exam-style questions (show your work)</h2>
  <ol class="q" start="31">{"".join(f"<li>{q}<span class='long'></span><span class='long'></span></li>" for q,a in E4)}</ol>
  <h2 style="margin-top:12px">Answers</h2>
  <table class="ans"><tbody>
   <tr><td><b>A</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(Aq,1))}</td></tr>
   <tr><td><b>B</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(Bq,9))}</td></tr>
   <tr><td><b>C</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(Cq,17))}</td></tr>
   <tr><td><b>D</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(Dq,25))}</td></tr>
   <tr><td><b>E</b></td><td>{" · ".join(f"{i}. {a}" for i,(q,a) in enumerate(E4,31))}</td></tr>
  </tbody></table>
  <div class="note"><b>Got one wrong?</b> Check: did you count the jumps (the 20th term is 19 jumps after the 1st)? Did you put the common difference in front of the n? Did you check your rule with the second term? Did you work backwards before dividing? Then play <b>Pattern Builder</b> at leim.ie/pattern-builder.html: the "Go back over these" list at the end shows the rule for each mistake.</div>
  <p class="small">All questions written by Léim. Léim is independent and not connected with the State Examinations Commission or the NCCA.</p>
</div>
</body></html>"""

# ---------- teacher pack ----------
# Pattern Detectives: 12 patterns (pictures, lists, a table, a story) ↔ 12 different rules
MATCH = []
for kind in ("squares", "triangles", "houses", "double"):
    MATCH.append((sticks(kind, h="11mm", labels=False), R(*STICK[kind]), kind))
for l in (S(5, 4), S(2, 6), S(10, -2), S(7, 3), S(1, 5), S(9, 2)):
    MATCH.append((ss(l), R(*rule_of(l)), "seq"))
MATCH.append(("n: 1, 2, 3, 4<br>Tₙ: 3, 10, 17, 24", R(*rule_of([3, 10, 17, 24])), "table"))
MATCH.append(("€25 saved, plus €5 a week: savings after n weeks", R(5, 25), "story"))
rules = [a for q, a, k in MATCH]; assert len(set(rules)) == 12, rules
assert rules == ["3n + 1", "2n + 1", "5n + 1", "5n + 2", "4n + 1", "6n − 4", "12 − 2n", "3n + 4", "5n − 4", "2n + 7", "7n − 4", "5n + 25"], rules
cards = [q for q, a, k in MATCH] + [a for q, a, k in MATCH]
random.seed(9); match_print = cards[:]; random.shuffle(match_print)
def fc(x): return x if x.startswith("<svg") else f'<div class="fc{" sm" if len(x) > 12 else ""}">{x}</div>'
match_html = "".join(f'<div class="c"><span class="tag">Card {i}</span>{fc(x)}</div>' for i, x in enumerate(match_print, 1))
NAMES = {"squares": "row of squares", "triangles": "row of triangles", "houses": "row of houses", "double": "double row of squares"}
match_key = " · ".join(f"{NAMES.get(k, q.replace('<br>', '; '))} → <b>{a}</b>" for q, a, k in MATCH)

def dom_t(l, k): return n(T(*rule_of(l), k))
DOMS = [("Next term: 3, 7, 11, 15, …", dom_t(S(3, 4), 5)), ("Common difference of 40, 34, 28, …", n(rule_of(S(40, -6))[0])),
        ("10th term of 2, 5, 8, …", dom_t(S(2, 3), 10)), ("T₅ when Tₙ = 4n − 3", n(T(4, -3, 5))), ("Tₙ for 6, 11, 16, …", R(*rule_of(S(6, 5)))),
        ("Tₙ for 1, 3, 5, …", R(*rule_of(S(1, 2)))), ("Matchstick squares: sticks in stage 5", str(count("squares", 5))),
        ("Which term of 4, 7, 10, … is 40?", str(which(S(4, 3), 40))), ("Missing term: 12, __, 30, 39", "21"),
        ("Start value: €20 saved, plus €6 a week", "20"), ("Rate of change: a 30 cm candle burns 2 cm an hour", "−2"),
        ("T₃ when Tₙ = 7n + 2", n(T(7, 2, 3))), ("S = 15w + 10. Find S when w = 4", n(T(15, 10, 4))), ("Tₙ for 20, 17, 14, …", R(*rule_of(S(20, -3)))),
        ("20th term of 5, 10, 15, …", dom_t(S(5, 5), 20)), ("Matchstick triangles: sticks in stage 12", str(count("triangles", 12))),
        ("Rule for the table n: 1, 2, 3 → 9, 13, 17", R(*rule_of([9, 13, 17]))), ("Next term: 50, 45, 40, …", dom_t(S(50, -5), 4)),
        ("Which term of 3, 8, 13, … is 88?", str(which(S(3, 5), 88))), ("First term of Tₙ = 6n − 1", n(T(6, -1, 1)))]
assert rule_of([12, 21, 30, 39]) == (9, 3)
ANS = [a for k, a in DOMS]
assert ANS == ["19", "−6", "29", "17", "5n + 1", "2n − 1", "16", "13", "21", "20", "−2", "23", "70", "23 − 3n", "100", "25", "4n + 5", "35", "18", "5"], ANS
assert len(set(ANS)) == 20
random.seed(99); chain = DOMS[:]; random.shuffle(chain)
dom = [("START" if k == 0 else chain[k - 1][1], x[0]) for k, x in enumerate(chain)] + [(chain[-1][1], "FINISH")]
dom_print = dom[:]; random.shuffle(dom_print)
dom_html = "".join(f'<div class="dom"><div class="h l">{l}</div><div class="h r">{r}</div></div>' for l, r in dom_print)
chain_key = "".join(f"<li>{x} = <b>{a}</b></li>" for x, a in chain)

ERR = [("Next term of 5, 9, 13, …", "= 18", f"It goes up by 4, not 5: <b>{dom_t(S(5, 4), 4)}</b>"),
       ("Tₙ for 4, 7, 10, …", "= n + 3", f"The jump goes in front of n: <b>{R(*rule_of(S(4, 3)))}</b> (n + 3 gives 4, 5, 6, …)"),
       ("10th term of 2, 6, 10, …", "= 2 + 10 × 4 = 42", f"Only 9 jumps from T₁ to T₁₀: 2 + 9 × 4 = <b>{dom_t(S(2, 4), 10)}</b>"),
       ("Squares: stage 1 uses 4 sticks. Stage 10?", "= 10 × 4 = 40", f"The squares share sides: 3(10) + 1 = <b>{count('squares', 10)}</b>"),
       ("Common difference of 20, 15, 10, …", "= 5", f"It goes down, so it's <b>{n(rule_of(S(20, -5))[0])}</b>"),
       ("Is 50 a term of 3, 7, 11, …?", "Yes, (50 − 3) ÷ 4 = 11.75", "11.75 is not a whole number, so <b>no</b> (T₁₂ = 47, T₁₃ = 51)")]
assert which(S(3, 4), 50) is None and T(4, -1, 12) == 47 and T(4, -1, 13) == 51 and dom_t(S(5, 4), 4) == "17"
w1 = S(3, 7); assert (R(*rule_of(w1)), T(*rule_of(w1), 15), which(w1, 150)) == ("7n − 4", 101, 22)
w2 = (R(*STICK["houses"]), T(*STICK["houses"], 20), (200 - 1) // 5, T(*STICK["houses"], (200 - 1) // 5)); assert w2 == ("5n + 1", 101, 39, 196) and count("houses", 20) == 101
w3 = (R(25, 40, "m"), T(25, 40, 6), Fraction(315 - 40, 25)); assert w3 == ("25m + 40", 190, 11)
w5 = [(x, 6 + 3 * x) for x in range(4)]; assert rule_of([y for x, y in w5])[0] == 3 and w5[0] == (0, 6) and T(3, 6, 10) == 36

pack_style = open(os.path.join(SRC, "build_ratio_pdfs.py"), encoding="utf-8").read()
pack_style = pack_style[pack_style.index("<style>", pack_style.index('pack = f"""')) + 7:pack_style.index("</style>", pack_style.index('pack = f"""'))]
pack_style = pack_style.replace("{{", "{").replace("}}", "}").replace("{LO}", LO)
pack_style += ".fym .c{height:21mm}.fym svg{margin-top:2mm}.trk{border:2px dashed #9AA3AE;padding:3mm 4mm;margin-top:3mm;font-size:9.4pt}.trk table td{padding:2px 6px;text-align:center;border:1px solid #D1D5DB;height:7mm}"
pack = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Linear Patterns and Sequences Teacher Pack | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{pack_style}</style></head><body>

<div class="page p1">
  <div class="band"><div><div class="k">Junior Cycle Maths · Teacher pack</div><h1>Linear patterns &amp; sequences</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2018 specification): {LO} (quadratic and doubling patterns come later, AF.1c; function notation and graphs of functions in Functions, AF.7)</p>
  <div class="two">
    <div><h3>Aims</h3><p>By the end of the lesson students can continue a linear pattern from a list, a picture or a table; find the common difference and the general term Tₙ; find far-away terms; work backwards to find which term a value is (and whether it's in the pattern); and link tables, graphs and formulas using start value and rate of change.</p></div>
    <div><h3>In this pack</h3><p>p.1 Teacher notes · p.2 Build It task + Pattern Detectives cards · p.3 Pattern Dominoes (cut-up) · p.4 Wall poster · p.5 Worksheet: Error Hunt + exam-style questions · p.6 Answers. Level: 1st year (Higher and Ordinary), or 3rd-year revision. Time: about 60 minutes. All questions are original.</p></div>
  </div>
  <h2 style="margin-top:8px">Procedure</h2>
  <table class="proc"><tbody>
    <tr><td>5 min</td><td><b>Lead-in.</b> Draw stages 1–3 of the matchstick squares on the board. "How many matchsticks for stage 4? For stage 100?" Collect guesses for stage 100 (expect 400). Don't judge yet.</td></tr>
    <tr><td>12 min</td><td><b>Build It</b> (p.2), groups of 3: build (or draw) stages 1–4 of the group's pattern with matchsticks, lollipop sticks or pencils, fill in the table, and explain in words why it goes up by the same amount each time. Find stage 10 and stage 100 and justify. Groups explain "where the + 1 comes from" (guided discovery: the first stick, counted once).</td></tr>
    <tr><td>8 min</td><td><b>Pull it together.</b> Board: common difference → dn → fix with T₁ → check T₂. Show the classic mistake ("n + 3") and test it with n = 1. Then working backwards: which stage uses 100 matchsticks?</td></tr>
    <tr><td>10 min</td><td><b>Pattern Detectives</b> (p.2, 24 cards = 12 pairs; one card each). Pictures, lists, a table and a story find their rule. Pairs check each other with two terms and sit together.</td></tr>
    <tr><td>12 min</td><td><b>Pattern Dominoes</b> (p.3), groups of 3–4: start with START, work out the clue, find the domino with that answer on its left and build the chain to FINISH.</td></tr>
    <tr><td>10 min</td><td><b>Worksheet</b> (p.5). Error Hunt in pairs (find the mistake, name the rule, fix it), then the exam-style questions alone.</td></tr>
    <tr><td>3 min</td><td><b>Exit ticket.</b> Find Tₙ for 8, 13, 18, … and say whether 100 is a term (5n + 3; no: 97 ÷ 5 = 19.4). Homework: play <b>Pattern Builder</b> at leim.ie/pattern-builder.html (Find the rule round) and copy three lines from the "Go back over these" list.</td></tr>
  </tbody></table>
  <div class="note"><b>Pattern Detectives key:</b> {match_key}.<br>
  <b>Errors to look for:</b> Tₙ = n + d (the jump added, not multiplied) · stage 10 = 10 × stage 1 · 10th term = T₁ + 10d · a positive common difference for a falling pattern · "is 50 a term?" answered from a rounded division · reading the graph's start value at x = 1. <b>Support:</b> build and count. <b>Fast finishers:</b> design a picture pattern with rule 4n + 3.</div>
  <p class="small"><b>Domino answer chain</b> (START → FINISH):</p>
  <ol class="small" style="columns:2;column-gap:14px;font-size:7.6pt;line-height:1.33;margin:0;padding-left:16px">{chain_key}</ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">One task card per group · one match card per student</div><h1>Build It + Pattern Detectives</h1></div><div class="logo">↗ Léim</div></div>
  <div class="trk"><b>Build It.</b> Your group's pattern (circle one): row of squares · row of triangles · row of houses · double row of squares. Build stages 1 to 4, count and fill in the table.
    <table style="width:auto;margin:2mm 0"><tbody><tr><td><b>Stage</b></td><td>1</td><td>2</td><td>3</td><td>4</td><td>10</td><td>100</td><td>n</td></tr><tr><td><b>Matchsticks</b></td><td></td><td></td><td></td><td></td><td></td><td></td><td style="width:22mm"></td></tr></tbody></table>
    How much does it go up each time? Why? Where does the extra bit come from? Which stage would use exactly 100 matchsticks (or explain why none can)?</div>
  <p style="font-size:9.5pt;margin:4mm 0 0"><b>Pattern Detectives.</b> Cut out the 24 cards and give one to each student. Pattern card (picture, list, table or story)? Find the person with your rule. Rule card? Find your pattern. Check with two terms before you sit down. (Fewer students? Take out whole pairs.)</p>
  <div class="fym">{match_html}</div>
</div>

<div class="page">
  <div class="band"><div><div class="k">Groups of 3–4 · cut along the dashed lines</div><h1>Pattern Dominoes</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.5pt">Start with START. Work out the clue on the right, then find the domino with that answer on its left. Keep going until you reach FINISH. No calculators!</p>
  <div class="doms">{dom_html}</div>
</div>

<div class="page">
  <div class="poster">
    <h1>Linear patterns</h1>
    <div class="big3"><div>5, 8, 11, 14<span>sequence</span></div><div>+3<span>common difference</span></div><div>3n + 2<span>general term Tₙ</span></div></div>
    <div style="text-align:center">{sticks("squares", h="24mm")}<p style="font-size:13pt;margin:2mm 0 0"><b>3n + 1</b>: 3 more each stage, 1 extra stick at the start</p></div>
    <div class="ops">
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Find Tₙ</b>jump d → dn<br>fix it with T₁<br>check with T₂</div>
      <div style="background:var(--green-soft)"><b>Far terms</b>T₅₀ = 3(50) + 2<br>T₁ + 49 jumps<br>(not 50!)</div>
      <div style="background:var(--green-soft)"><b>Backwards</b>which term is 65?<br>(65 − 5) ÷ 3 = 20 jumps<br>→ T₂₁</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Real life</b>start value = at 0<br>rate of change = jump<br>S = 15w + 35</div>
    </div>
    <p style="text-align:center;font-size:10pt;color:var(--muted)">Léim · leim.ie · Play Pattern Builder: leim.ie/pattern-builder.html</p>
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
    <li>The sequence 3, 10, 17, 24, … (a) Find Tₙ. (b) Find T₁₅. (c) Is 150 a term? Explain.<span class="long"></span><span class="long"></span></li>
    <li>A row of matchstick houses: 1 house uses 6 matchsticks, 2 houses use 11, 3 houses use 16. (a) Write a rule for n houses. (b) How many matchsticks for 20 houses? (c) Tom has 200 matchsticks. How many houses can he make in one row, and how many matchsticks are left over?<span class="long"></span><span class="long"></span></li>
    <li>A gym charges a €40 joining fee plus €25 a month. (a) Write a formula for the total cost after m months. (b) Find the cost for 6 months. (c) After how many months will the total be €315?<span class="long"></span><span class="long"></span></li>
    <li>Ciara says the general term of 3, 7, 11, 15, … is n + 4. Explain her mistake and give the right rule.<span class="long"></span></li>
    <li>The points (0, 6), (1, 9), (2, 12) and (3, 15) lie on a straight line. (a) Write down the start value and the rate of change. (b) Write a formula for y in terms of x. (c) Find y when x = 10.<span class="long"></span><span class="long"></span></li>
  </ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">For the teacher</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>Build It</h2>
  <table><tbody>{"".join(f"<tr><td style='width:34%'><b>{NAMES[k]}</b></td><td>{', '.join(str(count(k, s)) for s in (1, 2, 3, 4))} · stage 10: {count(k, 10)} · stage 100: {count(k, 100)} · rule <b>{R(*STICK[k])}</b> · 100 matchsticks: {('stage ' + str(which([count(k, s) for s in (1, 2, 3)], 100))) if which([count(k, s) for s in (1, 2, 3)], 100) else 'no stage'}</td></tr>" for k in ("squares", "triangles", "houses", "double"))}</tbody></table>
  <h2>A. Error Hunt</h2>
  <table><tbody>{"".join(f"<tr><td style='width:34%'><b>{q}</b> {w}</td><td>{r}</td></tr>" for q,w,r in ERR)}</tbody></table>
  <h2>B. Exam-style questions</h2>
  <ol class="q">
    <li>(a) <b>{w1 and R(*rule_of(w1))}</b> (b) 7(15) − 4 = <b>{T(*rule_of(w1), 15)}</b> (c) (150 + 4) ÷ 7 = 22, a whole number, so <b>yes: T₂₂ = 150</b></li>
    <li>(a) <b>{w2[0]}</b> (b) 5(20) + 1 = <b>{w2[1]}</b> (c) (200 − 1) ÷ 5 = 39.8, so <b>{w2[2]} houses</b>, using {w2[3]} matchsticks: <b>{200 - w2[3]} left over</b></li>
    <li>(a) <b>C = {w3[0]}</b> (b) 25(6) + 40 = <b>€{w3[1]}</b> (c) (315 − 40) ÷ 25 = <b>{w3[2]} months</b></li>
    <li>n + 4 only says "add 4 to get the next term"; it gives 5, 6, 7, … The jump 4 goes in front of n: 4n gives 4 for n = 1, so take away 1: <b>Tₙ = 4n − 1</b>. Check: 4(2) − 1 = 7 ✓</li>
    <li>(a) start value <b>6</b>, rate of change <b>3</b> (b) <b>y = 3x + 6</b> (c) 3(10) + 6 = <b>36</b></li>
  </ol>
  <h2>Marking tip</h2>
  <p>Give credit for each step, as the exam does: a correct table or a correct common difference earns marks even if the rule slips. Accept equivalent forms of the rule (34 − 4n = −4n + 34) and any clear "working backwards" method.</p>
</div>
</body></html>"""
assert T(4, -1, 1) == 3 and T(4, -1, 2) == 7 and which(S(3, 4), 50) is None
for k in STICK:
    assert [count(k, s) for s in (10, 100)] == [T(*STICK[k], 10), T(*STICK[k], 100)]

cover = """<!doctype html><html><head><meta charset="utf-8"><style>
body{margin:0;width:1200px;height:1200px;background:#1B2430;font-family:Inter,sans-serif;color:#fff;display:flex;flex-direction:column;justify-content:space-between;padding:90px;box-sizing:border-box}
.k{display:inline-block;background:#2E7D57;border-radius:99px;padding:12px 26px;font-weight:700;font-size:28px;letter-spacing:.06em;text-transform:uppercase}
h1{font-size:104px;font-weight:800;line-height:1.12;letter-spacing:-.03em;margin:40px 0 0}
h1 span{background:#F6CF5A;color:#1B2430;padding:0 14px;box-decoration-break:clone;-webkit-box-decoration-break:clone}
.sub{font-size:38px;color:#C9D1DA;margin-top:36px;line-height:1.35}
.em{font-size:50px;margin-top:30px;font-weight:800;letter-spacing:.01em;color:#F6CF5A}
.foot{display:flex;justify-content:space-between;align-items:center;font-size:34px;font-weight:700}
.price{background:#F6CF5A;color:#1B2430;border-radius:16px;padding:14px 28px}
</style></head><body>
<div><span class="k">Junior Cycle Maths · Teacher pack</span>
<h1><span>Linear Patterns</span><br><span>&amp; Sequences</span></h1>
<div class="sub">Build It · Pattern Detectives<br>Pattern Dominoes · Poster · Worksheet + answers</div>
<div class="em">5, 8, 11, 14, … &nbsp;→&nbsp; Tₙ = 3n + 2</div></div>
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
    pdf("teacher-pack", os.path.join(OUT, "Linear-Patterns-Teacher-Pack-Leim.pdf"))
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--hide-scrollbars", "--window-size=1200,1200",
                    f"--screenshot={os.path.join(OUT, f'{SLUG}-cover.png')}", f"{SLUG}-cover.html"], cwd=SRC, check=True, capture_output=True)
    print("domino chain:", [(x, a) for x, a in chain])
