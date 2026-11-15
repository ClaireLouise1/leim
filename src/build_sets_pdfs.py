#!/usr/bin/env python3
"""Sets & Venn diagrams (JC Maths topic 5): free sheet + teacher pack + Payhip cover.
Run from the repo root: python3 src/build_sets_pdfs.py OUTDIR
Writes src/sets-venn-diagrams-*.html; PDFs/cover PNG go to OUTDIR (free sheet also to printables/).
Every answer is computed with Python sets and asserted."""
import os, sys, random, subprocess, re
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC)
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/sets"; os.makedirs(OUT, exist_ok=True)
SLUG = "sets-venn-diagrams"
LO = "N.5, U.4"

def L(s):
    s = sorted(s, key=lambda x: (isinstance(x, str), x)); return "{" + ", ".join(map(str, s)) + "}" if s else "∅"
def is_prime(n): return n > 1 and all(n % d for d in range(2, int(n ** .5) + 1))
def U_(n): return set(range(1, n + 1))

# ---------- Venn pictures (inline SVG) ----------
INK, YEL, GREEN = "#1B2430", "#F6CF5A", "#2E7D57"
C2, R2 = [(110, 105), (190, 105)], 64
C3, R3 = [(118, 98), (182, 98), (150, 155)], 58
P2 = {1: (80, 110), 3: (150, 110), 2: (220, 110), 0: (262, 192)}
P3 = {1: (92, 84), 2: (208, 84), 3: (150, 70), 4: (150, 192), 5: (115, 139), 6: (185, 139), 7: (150, 116), 0: (268, 244)}
_uid = [0]
def venn(n, labels, vals=None, shade=(), h="44mm", fs=None):
    H = 210 if n == 2 else 262; c, r = (C2, R2) if n == 2 else (C3, R3); P = P2 if n == 2 else P3
    _uid[0] += 1; idp = f"s{_uid[0]}"
    o = [f'<svg viewBox="0 0 300 {H}" style="height:{h};width:auto;display:block;margin:0 auto" xmlns="http://www.w3.org/2000/svg">',
         f'<rect x="4" y="4" width="292" height="{H-8}" rx="10" fill="#fff" stroke="{INK}" stroke-width="2"/>']
    if shade:
        d = "<defs>" + "".join(f'<clipPath id="{idp}c{i}"><circle cx="{c[i][0]}" cy="{c[i][1]}" r="{r}"/></clipPath>' for i in range(n))
        body = ""
        for g in shade:
            d += f'<mask id="{idp}m{g}"><rect x="0" y="0" width="300" height="{H}" fill="#fff"/>' + "".join(
                f'<circle cx="{c[i][0]}" cy="{c[i][1]}" r="{r}" fill="#000"/>' for i in range(n) if not g >> i & 1) + "</mask>"
            s = f'<rect x="4" y="4" width="292" height="{H-8}" fill="{YEL}" mask="url(#{idp}m{g})"/>'
            for i in range(n):
                if g >> i & 1: s = f'<g clip-path="url(#{idp}c{i})">{s}</g>'
            body += s
        o.append(d + "</defs>" + body)
    for i in range(n): o.append(f'<circle cx="{c[i][0]}" cy="{c[i][1]}" r="{r}" fill="none" stroke="{INK}" stroke-width="2.5"/>')
    o.append(f'<text x="18" y="28" font-size="17" font-weight="800" fill="{INK}" font-family="Inter,sans-serif">U</text>')
    lp = [(52, 40), (248, 40)] if n == 2 else [(70, 30), (230, 30), (150, 250)]
    for i in range(n):
        o.append(f'<text x="{lp[i][0]}" y="{lp[i][1]}" font-size="{14 if len(labels[i]) > 2 else 18}" font-weight="800" text-anchor="middle" fill="{GREEN}" font-family="Inter,sans-serif">{labels[i]}</text>')
    for g, v in (vals or {}).items():
        v = str(v); size = fs or (13 if len(v) > 4 else 16 if n == 3 else 18)
        o.append(f'<text x="{P[g][0]}" y="{P[g][1]+6}" font-size="{size}" font-weight="800" text-anchor="middle" fill="{INK}" font-family="Inter,sans-serif">{v}</text>')
    return "".join(o) + "</svg>"
def region_sets(n, sets, U):
    out = {g: set() for g in range(1 << n)}
    for x in U: out[sum(1 << i for i in range(n) if x in sets[i])].add(x)
    return out

# ---------- free sheet ----------
U12 = U_(12); A = {2, 3, 5, 7, 11}; B = {1, 3, 5, 7, 9}
SA = [("List the elements of the set: the factors of 18.", L({x for x in range(1, 19) if 18 % x == 0})),
      ("A = {2, 3, 5, 7, 11}. True or false: 9 ∈ A?", "False" if 9 not in A else "True"),
      ("B = {1, 3, 5, 7, 9}. Write down #B.", str(len(B))),
      ("Is {3, 5} ⊂ B? Explain.", "Yes: 3 ∈ B and 5 ∈ B" if {3, 5} <= B else "No"),
      ("List the even numbers in A = {2, 3, 5, 7, 11}.", L({x for x in A if x % 2 == 0})),
      ("List the set of letters in the word VENN.", L(set("VENN")))]
assert [a for q, a in SA] == ["{1, 2, 3, 6, 9, 18}", "False", "5", "Yes: 3 ∈ B and 5 ∈ B", "{2}", "{E, N, V}"], [a for q, a in SA]
SB = [("A ∩ B", A & B), ("A ∪ B", A | B), ("A \\ B", A - B), ("B \\ A", B - A), ("A′", U12 - A), ("B′", U12 - B), ("(A ∪ B)′", U12 - (A | B)), ("#(A ∪ B)", len(A | B))]
assert len(A | B) == len(A) + len(B) - len(A & B) == 7 and A & B == {3, 5, 7} and U12 - (A | B) == {4, 6, 8, 10, 12}
def show(v): return L(v) if isinstance(v, set) else str(v)
# C: read a Venn diagram of elements
CU = U_(10); CA = {1, 2, 4, 6}; CB = {2, 6, 8, 10}
rs = region_sets(2, [CA, CB], CU)
cvals = {g: ", ".join(map(str, sorted(rs[g]))) for g in rs}
SC = [("List A.", CA), ("List B.", CB), ("List A ∩ B.", CA & CB), ("List A ∪ B.", CA | CB), ("List A \\ B.", CA - CB), ("List B′.", CU - CB), ("List (A ∪ B)′.", CU - (CA | CB)), ("Write down #A.", len(CA))]
assert rs[0] == {3, 5, 7, 9} and rs[3] == {2, 6}
SD = [("in A and in B", "A ∩ B"), ("in A or in B (or both)", "A ∪ B"), ("in A but not in B", "A \\ B"), ("not in A", "A′"),
      ("in all three of A, B and C", "A ∩ B ∩ C"), ("in none of A, B and C", "(A ∪ B ∪ C)′")]
d1a, d1b = {1, 2, 3}, {3, 4}
assert d1a - d1b == {1, 2} and d1b - d1a == {4}
e1, e2, e3 = {1, 2}, {2, 3}, {3, 4}
assert (e1 | e2) | e3 == e1 | (e2 | e3) == {1, 2, 3, 4}
# E: exam style
x31 = 17 + 14 + 4 - 30; assert x31 == 5 and (17 - x31) + x31 + (14 - x31) + 4 == 30
n32 = 120 - (70 + 45 - 20); one32 = (70 - 20) + (45 - 20); assert n32 == 25 and one32 == 75
c3 = {7: 2}; c3[3] = 5 - 2; c3[6] = 6 - 2; c3[5] = 7 - 2
c3[1] = 18 - c3[3] - c3[5] - 2; c3[2] = 15 - c3[3] - c3[6] - 2; c3[4] = 20 - c3[5] - c3[6] - 2
inside33 = sum(c3.values()); none33 = 40 - inside33; two33 = c3[3] + c3[5] + c3[6]
assert (c3[1], c3[2], c3[4], inside33, none33, two33) == (8, 6, 9, 37, 3, 12), (c3, inside33)
U20 = U_(20); P = {x for x in U20 if is_prime(x)}; E = {x for x in U20 if x % 2 == 0}; T = {x for x in U20 if x % 3 == 0}
a34 = [P & E, E & T, P & T, P & E & T, len(E | T)]
assert a34 == [{2}, {6, 12, 18}, {3}, set(), 13] and len(E | T) == len(E) + len(T) - len(E & T)
EX = [(f"30 students were asked if they play rugby (R) or soccer (S). 17 play rugby, 14 play soccer and 4 play neither. x play both. (a) Draw a Venn diagram. (b) Find x. (c) How many play rugby only?",
       f"(17 − x) + x + (14 − x) + 4 = 30, so 35 − x = 30, <b>x = {x31}</b>; rugby only <b>{17 - x31}</b>"),
      ("120 people were asked how they read the news. 70 read it online, 45 read a paper and 20 do both. (a) How many do neither? (b) How many use exactly one?",
       f"(a) 70 + 45 − 20 = 95, so <b>{n32}</b> (b) 50 + 25 = <b>{one32}</b>"),
      ("40 students were asked which languages they study: French (F), German (G), Spanish (S). 2 study all three; 5 study French and German, 6 German and Spanish, 7 French and Spanish; 18 study French, 15 German and 20 Spanish. (a) Draw the Venn diagram. (b) How many study none? (c) How many study exactly two?",
       f"Centre 2; two only 3, 4, 5; one only F {c3[1]}, G {c3[2]}, S {c3[4]}. (b) 40 − {inside33} = <b>{none33}</b> (c) 3 + 4 + 5 = <b>{two33}</b>"),
      ("U = {1, 2, …, 20}. P = the prime numbers, E = the even numbers, T = the multiples of 3. List (a) P ∩ E (b) E ∩ T (c) P ∩ T (d) P ∩ E ∩ T. (e) Find #(E ∪ T).",
       f"(a) <b>{L(a34[0])}</b> (b) <b>{L(a34[1])}</b> (c) <b>{L(a34[2])}</b> (d) <b>∅</b> (e) 10 + 6 − 3 = <b>{a34[4]}</b>")]

def qs(items, w="120px"): return "".join(f"<li>{q} <span class='line' style='min-width:{w}'></span></li>" for q, a in items)

sheet = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Sets and Venn diagrams: rules and practice | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>@page{{@bottom-left{{content:"Léim · leim.ie · Free to print for home or class · JC Maths LOs (2018 spec): {LO}"}}}}
.tight{{font-size:10pt;line-height:1.42}}.tight td:first-child{{white-space:nowrap}}.tight td,.tight th{{padding:3px 6px}}.tight h2{{margin:9px 0 5px;font-size:13.5pt}}.tight .note,.tight .tip{{padding:6px 10px;margin:6px 0}}
ol.q{{padding-left:30px}}ol.q li{{margin:6px 0}}.cols{{columns:2;column-gap:12mm}}.cols li{{break-inside:avoid}}
.ans td{{padding:3px 6px;font-size:9.2pt}}
</style></head><body>
<div class="page tight">
  <div class="band"><div><div class="k">Junior Cycle Maths · Free revision sheet</div><h1>Sets &amp; Venn diagrams</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2018 specification): {LO}. Play the game: <b>leim.ie/venn-sorter.html</b></p>
  <div class="two">
   <div><h2>1. The language of sets</h2>
    <p>A <b>set</b> is a well-defined collection of <b>elements</b>. <b>List</b> it, A = {{2, 4, 6, 8}}, or give a <b>rule</b>: the even numbers from 1 to 9.</p>
    <table><tbody>
     <tr><td><b>∈ / ∉</b></td><td>is / is not an element of: 4 ∈ A, 5 ∉ A</td></tr>
     <tr><td><b>#A</b></td><td>the number of elements: #A = 4</td></tr>
     <tr><td><b>⊂</b></td><td>subset (every element is also in A): {{2, 8}} ⊂ A</td></tr>
     <tr><td><b>∅</b> or {{ }}</td><td>the empty (null) set</td></tr>
     <tr><td><b>U</b></td><td>the universal set: everything in the question (the box)</td></tr></tbody></table>
    <h2>2. The four operations</h2>
    <p>U = {{1, …, 8}}, A = {{1, 2, 3, 4, 6}}, B = {{2, 4, 6, 8}}</p>
    <table><tbody>
     <tr><td><b>A ∩ B</b></td><td>in A <b>and</b> B</td><td>{{2, 4, 6}}</td></tr>
     <tr><td><b>A ∪ B</b></td><td>in A <b>or</b> B (or both)</td><td>{{1, 2, 3, 4, 6, 8}}</td></tr>
     <tr><td><b>A \\ B</b></td><td>in A <b>but not</b> B</td><td>{{1, 3}}</td></tr>
     <tr><td><b>A′</b></td><td><b>not</b> in A</td><td>{{5, 7, 8}}</td></tr></tbody></table>
    <div class="note"><b>Order:</b> A ∩ B = B ∩ A and A ∪ B = B ∪ A (commutative); (A ∩ B) ∩ C = A ∩ (B ∩ C), same for ∪ (associative). But A \\ B ≠ B \\ A.</div></div>
   <div><h2>3. Venn diagrams</h2>
    {venn(2, ["A", "B"], {1: "A \\ B", 3: "A ∩ B", 2: "B \\ A", 0: "(A ∪ B)′"}, h="48mm", fs=13)}
    <h2>4. Counting</h2>
    <p><b>#(A ∪ B) = #A + #B − #(A ∩ B)</b>: adding #A and #B counts the overlap twice.</p>
    <h2>5. Survey questions</h2>
    <p>Fill the <b>middle first</b> (call it <b>x</b> if unknown). Then each circle "only" = total − overlap (15 − x). "Neither" goes <b>outside</b> the circles, inside the box. All regions add up to the total: solve for x.</p>
    <p><b>3 sets:</b> centre → the three "two only" parts → the "one only" parts → outside. "Exactly two" leaves out the centre; "at least two" includes it.</p></div>
  </div>
  <div class="tip"><b>Exam tip:</b> draw the box for U and label every circle. List each element once, in set brackets {{ }}. An empty answer is ∅, not 0. Read "only", "neither", "exactly" and "at least" carefully, and show the equation when you find x.</div>
</div>

<div class="page tight">
  <div class="band"><div><div class="k">Practice · 34 questions</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <div class="two"><div><h2>A. Set language</h2><ol class="q">{qs(SA, "60px")}</ol></div>
  <div><h2>B. U = {{1, 2, …, 12}}, A = {{2, 3, 5, 7, 11}}, B = {{1, 3, 5, 7, 9}}</h2><ol class="q" start="7">{"".join(f"<li>{q} = <span class='line'></span></li>" for q, v in SB)}</ol></div></div>
  <h2>C. Use the Venn diagram</h2>
  <div class="two" style="align-items:center"><div>{venn(2, ["A", "B"], cvals, h="40mm")}</div><div><ol class="q" start="15">{qs(SC, "80px")}</ol></div></div>
  <h2>D. Write in set notation: the elements that are…</h2><ol class="q cols" start="23">{qs(SD, "70px")}</ol>
  <ol class="q" start="29"><li>A = {{1, 2, 3}} and B = {{3, 4}}. List A \\ B and B \\ A. Are they equal? <span class='line'></span></li>
   <li>A = {{1, 2}}, B = {{2, 3}}, C = {{3, 4}}. Show that (A ∪ B) ∪ C = A ∪ (B ∪ C). <span class='line'></span></li></ol>
  <p class="small" style="margin-top:6px">Questions 31–34 are on the next page.</p>
</div>

<div class="page tight">
  <div class="band"><div><div class="k">Exam-style · then check</div><h1>Exam corner + answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>E. Exam-style questions (show your work)</h2>
  <ol class="q" start="31">{"".join(f"<li>{q}<span class='long'></span><span class='long'></span></li>" for q, a in EX)}</ol>
  <h2 style="margin-top:12px">Answers</h2>
  <table class="ans"><tbody>
   <tr><td><b>A</b></td><td>{" · ".join(f"{i}. {a}" for i, (q, a) in enumerate(SA, 1))}</td></tr>
   <tr><td><b>B</b></td><td>{" · ".join(f"{i}. {show(v)}" for i, (q, v) in enumerate(SB, 7))}</td></tr>
   <tr><td><b>C</b></td><td>{" · ".join(f"{i}. {show(v)}" for i, (q, v) in enumerate(SC, 15))}</td></tr>
   <tr><td><b>D</b></td><td>{" · ".join(f"{i}. {a}" for i, (q, a) in enumerate(SD, 23))} · 29. A \\ B = {L(d1a - d1b)}, B \\ A = {L(d1b - d1a)}: not equal · 30. both = {L((e1 | e2) | e3)}</td></tr>
   <tr><td><b>E</b></td><td>{" · ".join(f"{i}. {a}" for i, (q, a) in enumerate(EX, 31))}</td></tr>
  </tbody></table>
  <div class="note"><b>Got one wrong?</b> Check: did you list each element once? Did you take the overlap away for "only"? Did you put "neither" outside the circles? Then play <b>Venn Sorter</b> at leim.ie/venn-sorter.html: the "Go back over these" list at the end shows the rule for each mistake.</div>
  <p class="small">All questions written by Léim. Léim is independent and not connected with the State Examinations Commission or the NCCA.</p>
</div>
</body></html>"""

# ---------- teacher pack ----------
ROUNDS = [("A = even numbers", "B = multiples of 3", lambda x: x % 2 == 0, lambda x: x % 3 == 0),
          ("A = factors of 16", "B = odd numbers", lambda x: 16 % x == 0, lambda x: x % 2 == 1),
          ("A = prime numbers", "B = numbers less than 8", is_prime, lambda x: x < 8),
          ("A = square numbers", "B = multiples of 4", lambda x: int(round(x ** .5)) ** 2 == x, lambda x: x % 4 == 0)]
U16 = U_(16); round_keys = []
for a, b, fa, fb in ROUNDS:
    rs = region_sets(2, [{x for x in U16 if fa(x)}, {x for x in U16 if fb(x)}], U16)
    assert all(rs[g] for g in rs), a
    round_keys.append((a, b, rs))
assert round_keys[1][2][3] == {1} and round_keys[2][2][3] == {2, 3, 5, 7}
cards_html = "".join(f'<div class="c"><span class="tag">Card {i}</span><div class="fc">{i}</div></div>' for i in range(1, 17))

# Venn Dominoes: U = {1..10}, A, B, C fixed; 20 clues, 20 different answers
DU = U_(10); DA = {1, 2, 3, 4, 5, 6}; DB = {4, 5, 6, 7, 8}; DC = {2, 4, 6, 8, 10}
CL = [("A ∩ B", DA & DB), ("A ∪ B", DA | DB), ("A \\ B", DA - DB), ("B \\ A", DB - DA), ("B′", DU - DB), ("(A ∪ B)′", DU - (DA | DB)),
      ("A ∩ C", DA & DC), ("C \\ A", DC - DA), ("B ∩ C", DB & DC), ("C \\ B", DC - DB), ("A ∩ B ∩ C", DA & DB & DC), ("(A ∪ C)′", DU - (DA | DC)),
      ("#(A ∪ B)", len(DA | DB)), ("#A", len(DA)), ("#(A ∩ C)", len(DA & DC)), ("#(B ∪ C)", len(DB | DC)), ("#C′", len(DU - DC)), ("(A ∩ B) \\ C", (DA & DB) - DC),
      ("A \\ (B ∪ C)", DA - (DB | DC)), ("#(A ∪ B ∪ C)", len(DA | DB | DC))]
ans_str = [show(v) for k, v in CL]
assert len(set(ans_str)) == 20, sorted(ans_str)
random.seed(55); chain = CL[:]; random.shuffle(chain)
dom = [("START" if k == 0 else show(chain[k - 1][1]), x[0]) for k, x in enumerate(chain)] + [(show(chain[-1][1]), "FINISH")]
dom_print = dom[:]; random.shuffle(dom_print)
dom_html = "".join(f'<div class="dom"><div class="h l">{l}</div><div class="h r">{r}</div></div>' for l, r in dom_print)
chain_key = "".join(f"<li>{x} = <b>{show(v)}</b></li>" for x, v in chain)

ea, eb = {1, 2, 3}, {3, 4}
ERR = [("A = {1, 2, 3}, B = {3, 4}. A ∪ B", "= {1, 2, 3, 3, 4}", f"Each element is listed once: <b>{L(ea | eb)}</b>"),
       ("A = {2, 4}, B = {1, 3}. A ∩ B", "= 0", f"No elements in common gives the empty set: <b>{L({2, 4} & {1, 3})}</b>, not the number 0"),
       ("15 play hurling, 6 play both. How many play hurling only?", "= 15", f"The 15 includes the 6 who play both: 15 − 6 = <b>{15 - 6}</b>"),
       ("#A = 8, #B = 6, #(A ∩ B) = 3. Find #(A ∪ B).", "= 14", f"The overlap was counted twice: 8 + 6 − 3 = <b>{8 + 6 - 3}</b>"),
       ("A = {1, 2}, B = {2, 3}. A \\ B", "= {3}", f"That's B \\ A. In A but not in B: <b>{L({1, 2} - {2, 3})}</b>"),
       ("3 sets: the \"two only\" regions hold 3, 4 and 5; the centre holds 2. How many are in at least two?", "= 12", f"\"At least two\" includes the centre: 3 + 4 + 5 + 2 = <b>{3 + 4 + 5 + 2}</b>")]
assert ea | eb == {1, 2, 3, 4}
W1U = U_(10); W1A = {x for x in W1U if 10 % x == 0}; W1B = {x for x in W1U if x % 2}
w1 = [W1A & W1B, W1A | W1B, W1U - (W1A | W1B), W1B - W1A]
assert W1A == {1, 2, 5, 10} and w1 == [{1, 5}, {1, 2, 3, 5, 7, 9, 10}, {4, 6, 8}, {3, 7, 9}]
# dog/cat: (16 − x) + x + (11 − x) + 2x = 31
x2 = 31 - 27; assert (16 - x2) + x2 + (11 - x2) + 2 * x2 == 31 and x2 == 4
v3 = {7: 5, 3: 8, 6: 4, 5: 3, 1: 20, 2: 6, 4: 7}; none3 = 60 - sum(v3.values()); tea3 = v3[1] + v3[3] + v3[5] + v3[7]
two3 = v3[3] + v3[5] + v3[6]; sc3 = v3[2] + v3[3] + v3[6] + v3[7]
assert (none3, tea3, two3, sc3) == (7, 36, 15, 23)
cafe = venn(3, ["Tea", "Scone", "Cake"], {**v3, 0: "?"}, h="46mm")
w4A, w4B, w4C = {1, 2, 3, 4}, {2, 4, 6}, {4, 5, 6}
ai1, ai2 = (w4A & w4B) & w4C, w4A & (w4B & w4C); ad1, ad2 = (w4A - w4B) - w4C, w4A - (w4B - w4C)
assert ai1 == ai2 == {4} and ad1 == {1, 3} and ad2 == {1, 3, 4} and ad1 != ad2

def shaded(label, regs): return f'<div>{venn(2, ["A", "B"], shade=regs, h="34mm")}<b>{label}</b></div>'
pack = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Sets &amp; Venn Diagrams Teacher Pack | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>
@page{{@bottom-left{{content:"Léim · leim.ie · Single-teacher licence · JC Maths LOs (2018 spec): {LO}";font-size:7pt}}}}
.proc td{{font-size:8.9pt;padding:3px 6px;line-height:1.32}}.proc td:first-child{{white-space:nowrap;font-weight:700;color:var(--green)}}
.p1 .note{{font-size:8.7pt;padding:6px 10px;line-height:1.35}}.p1 p{{font-size:9.5pt}}
.fym{{display:grid;grid-template-columns:repeat(4,1fr);margin-top:2mm}}
.fym .c{{border:2px dashed #9AA3AE;margin:-1px 0 0 -1px;height:30mm;position:relative;display:flex;align-items:center;justify-content:center}}
.fym .fc{{font-size:40pt;font-weight:800;text-align:center}}
.fym .tag{{position:absolute;top:1.5mm;left:3mm;font-size:6.8pt;color:var(--green);font-weight:800;text-transform:uppercase;letter-spacing:.04em}}
.rules td{{font-size:9.5pt;padding:4px 7px}}
.doms{{display:grid;grid-template-columns:1fr 1fr;gap:2mm 6mm}}
.dom{{display:grid;grid-template-columns:1.4fr 1fr;border:2px dashed #9AA3AE;height:16.6mm}}
.dom .h{{display:flex;align-items:center;justify-content:center;text-align:center;padding:2mm;font-size:12.5pt;font-weight:800}}
.dom .r{{font-size:15pt}}
.dom .l{{background:var(--mist);border-right:2px solid var(--ink)}}
.poster{{height:255mm;border:6px solid var(--night);border-radius:18px;padding:9mm;display:flex;flex-direction:column;justify-content:space-between}}
.poster h1{{font-size:44pt;text-align:center}}
.sh{{display:grid;grid-template-columns:1fr 1fr;gap:4mm 6mm;text-align:center}}.sh b{{font-size:20pt;display:block;margin-top:1mm}}
.ops{{display:grid;grid-template-columns:1fr 1fr;gap:4mm}}.ops div{{border-radius:14px;padding:5mm 4mm;text-align:center;font-size:12.5pt;line-height:1.45}}.ops b{{display:block;font-size:18pt;font-weight:800;margin-bottom:1mm}}
.ws{{font-size:9.8pt;line-height:1.4}}.ws ol.q li{{margin:5px 0}}.ws .long{{height:20px}}
.eh td{{padding:4px 8px;font-size:9.4pt}}.eh td:first-child{{font-weight:700;width:38%}}.eh .gap{{display:block;border-bottom:1px solid #9AA3AE;height:15px}}
.key td{{font-size:8.8pt;padding:3px 6px}}
</style></head><body>

<div class="page p1">
  <div class="band"><div><div class="k">Junior Cycle Maths · Teacher pack</div><h1>Sets &amp; Venn diagrams</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2018 specification): {LO} (sets usually come up as a survey question with a Venn diagram)</p>
  <div class="two">
    <div><h3>Aims</h3><p>By the end of the lesson students can describe a set by listing or by a rule, use the notation ∈, ∉, ⊂, #, ∅ and U, find A ∩ B, A ∪ B, A \\ B and A′ for 2 and 3 sets, show sets on a Venn diagram, solve survey problems (including with x), and check whether the operations are commutative or associative.</p></div>
    <div><h3>In this pack</h3><p>p.1 Teacher notes · p.2 Human Venn Diagram cards + rounds · p.3 Venn Dominoes (cut-up) · p.4 Wall poster · p.5 Worksheet: Error Hunt + exam-style questions · p.6 Answers. Level: 1st year (Higher and Ordinary), or 3rd-year revision. Time: about 60 minutes. You need two skipping ropes or hoops (or chalk/tape circles). All questions are original.</p></div>
  </div>
  <h2 style="margin-top:8px">Procedure</h2>
  <table class="proc"><tbody>
    <tr><td>5 min</td><td><b>Lead-in: Stand up if…</b> "Stand up if you have a brother." Sit. "Stand up if you have a sister." Ask: who stood up both times? Who never stood up? How many students are in the room? Can we show all of that in one picture? Elicit two overlapping circles in a box.</td></tr>
    <tr><td>12 min</td><td><b>Human Venn Diagram</b> (p.2). Lay two overlapping rope circles on the floor and label them A and B. Give out the 16 number cards. Read a round's rules; students walk to the right region (or stand outside the circles, inside the "room" = U). Each region explains why they're there. After round 2, ask: what is A ∩ B? A ∪ B? Who is in A′? Introduce the symbols on the board as students say them.</td></tr>
    <tr><td>8 min</td><td><b>Guided discovery: counting.</b> Board #A, #B, #(A ∩ B) and #(A ∪ B) for rounds 1–3 (from the key on p.6). Pairs look for the rule. Elicit #(A ∪ B) = #A + #B − #(A ∩ B) and why (the overlap is counted twice).</td></tr>
    <tr><td>12 min</td><td><b>Venn Dominoes</b> (p.3), groups of 3–4. Start with START, work out the clue using the sets at the top of the page, find the domino with that answer on its left and build the chain to FINISH. Answer chain below.</td></tr>
    <tr><td>8 min</td><td><b>Class survey with x.</b> Each pair asks 8 classmates two yes/no questions they choose (sport? instrument?), then fills a 2-set Venn diagram. Pairs swap totals only (how many asked, yes to Q1, yes to Q2, neither) and the other pair finds the overlap with x.</td></tr>
    <tr><td>12 min</td><td><b>Worksheet</b> (p.5). Error Hunt in pairs (find the mistake, name the rule, fix it), then the exam-style questions alone. Feedback on question 3: why fill the middle first?</td></tr>
    <tr><td>3 min</td><td><b>Exit ticket.</b> A = {{1, 2, 3, 4}}, B = {{3, 4, 5}}: list A \\ B and B \\ A ({{1, 2}}; {{5}}). Homework: play <b>Venn Sorter</b> at leim.ie/venn-sorter.html (Survey sums round) and copy three lines from the "Go back over these" list.</td></tr>
  </tbody></table>
  <div class="note"><b>Errors to look for:</b> listing an element twice in A ∪ B · writing 0 for the empty set · forgetting to take the overlap away ("hurling only" = 15 instead of 15 − x) · putting "neither" inside a circle or leaving it out of the total · mixing up A \\ B and B \\ A · counting the centre as "exactly two". <b>Support:</b> colour each circle in a different colour. <b>Fast finishers:</b> is \\ associative? Try (A \\ B) \\ C and A \\ (B \\ C) with A = {{1, 2, 3, 4}}, B = {{2, 4, 6}}, C = {{4, 5, 6}}.</div>
  <p class="small"><b>Domino answer chain</b> (START → FINISH):</p>
  <ol class="small" style="columns:3;column-gap:12px;font-size:7.8pt;line-height:1.35;margin:0;padding-left:16px">{chain_key}</ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">Cut up the cards · one per student</div><h1>Human Venn Diagram</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.5pt;margin:0">Two overlapping circles on the floor, A and B. The room is U = {{1, 2, …, 16}}. Read a round; each student walks to the region where their number belongs. (Big class? Print twice and run two diagrams, or give out letters as well.)</p>
  <div class="fym">{cards_html}</div>
  <h2 style="margin-top:5mm">The rounds</h2>
  <table class="rules"><thead><tr><th>Round</th><th>Circle A</th><th>Circle B</th><th>Then ask</th></tr></thead><tbody>
  {"".join(f"<tr><td>{i}</td><td><b>{a[4:]}</b></td><td><b>{b[4:]}</b></td><td>{q}</td></tr>" for i, ((a, b, rs), q) in enumerate(zip(round_keys, ["Who is in A ∩ B? Why is 6 there?", "Why is only one card in the middle?", "What is #(A ∪ B)? Who is in (A ∪ B)′?", "Who is in A \\ B? Is it the same as B \\ A?"]), 1))}
  </tbody></table>
  <p style="font-size:9.5pt">Answer key on page 6.</p>
</div>

<div class="page">
  <div class="band"><div><div class="k">Groups of 3–4 · cut along the dashed lines</div><h1>Venn Dominoes</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:10.5pt"><b>U = {{1, 2, …, 10}} · A = {L(DA)} · B = {L(DB)} · C = {L(DC)}</b></p>
  <p style="font-size:9.5pt">Start with START. Work out the clue on the right, then find the domino with that answer on its left. Keep going until you reach FINISH. Sketch a Venn diagram to help!</p>
  <div class="doms">{dom_html}</div>
</div>

<div class="page">
  <div class="poster">
    <h1>Sets &amp; Venn diagrams</h1>
    <div class="sh">{shaded("A ∩ B · and", [3])}{shaded("A ∪ B · or", [1, 2, 3])}{shaded("A \\ B · but not", [1])}{shaded("A′ · not", [0, 2])}</div>
    <div class="ops">
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Symbols</b>∈ is in · ∉ is not in<br>⊂ subset · # how many<br>∅ empty set · U the box</div>
      <div style="background:var(--green-soft)"><b>Counting</b>#(A ∪ B) =<br>#A + #B − #(A ∩ B)</div>
      <div style="background:var(--green-soft)"><b>Surveys</b>Middle first (x)<br>"only" = total − overlap<br>"neither" outside the circles</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Order</b>A ∩ B = B ∩ A · A ∪ B = B ∪ A<br>but A \\ B ≠ B \\ A</div>
    </div>
    <p style="text-align:center;font-size:10pt;color:var(--muted)">Léim · leim.ie · Play Venn Sorter: leim.ie/venn-sorter.html</p>
  </div>
</div>

<div class="page ws">
  <div class="band"><div><div class="k">Worksheet</div><h1>Error Hunt + exam-style questions</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Error Hunt</h2>
  <p>Each answer has one mistake. Find it, say which rule was broken, and write the right answer.</p>
  <table class="eh"><thead><tr><th>Question</th><th>Student's answer</th><th>The mistake and the right answer</th></tr></thead><tbody>
  {"".join(f"<tr><td>{q}</td><td>{w}</td><td><span class='gap'></span><span class='gap'></span></td></tr>" for q, w, r in ERR)}
  </tbody></table>
  <h2>B. Exam-style questions (show all your work)</h2>
  <ol class="q">
    <li>U = {{1, 2, …, 10}}, A = the factors of 10, B = the odd numbers in U. Draw a Venn diagram. List A ∩ B, A ∪ B, (A ∪ B)′ and B \\ A.<span class="long"></span><span class="long"></span></li>
    <li>31 students were asked about pets. 16 have a dog, 11 have a cat and x have both. Twice as many students have neither as have both. Draw a Venn diagram and find x.<span class="long"></span><span class="long"></span></li>
    <li style="break-inside:avoid">60 café customers were asked what they ordered. (a) How many ordered none of the three? (b) How many ordered tea? (c) How many ordered exactly two? (d) Find #Scone.
      {cafe}</li>
    <li>A = {{1, 2, 3, 4}}, B = {{2, 4, 6}}, C = {{4, 5, 6}}. (a) Is (A ∩ B) ∩ C = A ∩ (B ∩ C)? (b) Is (A \\ B) \\ C = A \\ (B \\ C)? Show your work.<span class="long"></span></li>
  </ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">For the teacher</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>Human Venn Diagram key</h2>
  <table class="key"><thead><tr><th>Round</th><th>A only</th><th>A ∩ B</th><th>B only</th><th>Outside</th></tr></thead><tbody>
  {"".join(f"<tr><td>{i}</td><td>{L(rs[1])}</td><td>{L(rs[3])}</td><td>{L(rs[2])}</td><td>{L(rs[0])}</td></tr>" for i, (a, b, rs) in enumerate(round_keys, 1))}
  </tbody></table>
  <h2>A. Error Hunt</h2>
  <table><tbody>{"".join(f"<tr><td style='width:40%'><b>{q}</b></td><td>{r}</td></tr>" for q, w, r in ERR)}</tbody></table>
  <h2>B. Exam-style questions</h2>
  <ol class="q">
    <li>A = {L(W1A)}, B = {L(W1B)}. A ∩ B = <b>{L(w1[0])}</b>, A ∪ B = <b>{L(w1[1])}</b>, (A ∪ B)′ = <b>{L(w1[2])}</b>, B \\ A = <b>{L(w1[3])}</b>.</li>
    <li>Dog only 16 − x, both x, cat only 11 − x, neither 2x. (16 − x) + x + (11 − x) + 2x = 31, so 27 + x = 31 and <b>x = {x2}</b> ({2 * x2} have neither).</li>
    <li>(a) 60 − {sum(v3.values())} = <b>{none3}</b> (b) 20 + 8 + 3 + 5 = <b>{tea3}</b> (c) 8 + 3 + 4 = <b>{two3}</b> (d) 6 + 8 + 4 + 5 = <b>{sc3}</b></li>
    <li>(a) A ∩ B = {{2, 4}}, ∩ C = <b>{{4}}</b>; B ∩ C = {{4, 6}}, A ∩ {{4, 6}} = <b>{{4}}</b>: <b>yes</b>. (b) A \\ B = {{1, 3}}, \\ C = <b>{L(ad1)}</b>; B \\ C = {{2}}, A \\ {{2}} = <b>{L(ad2)}</b>: <b>no</b>, set difference is not associative.</li>
  </ol>
  <h2>Marking tip</h2>
  <p>Give credit for each step, as the exam does: a correct Venn diagram with x in the right places earns marks even if the equation slips. Insist on set brackets and on ∅ for an empty set.</p>
</div>
</body></html>"""

cover = """<!doctype html><html><head><meta charset="utf-8"><style>
body{margin:0;width:1200px;height:1200px;background:#1B2430;font-family:Inter,sans-serif;color:#fff;display:flex;flex-direction:column;justify-content:space-between;padding:90px;box-sizing:border-box}
.k{display:inline-block;background:#2E7D57;border-radius:99px;padding:12px 26px;font-weight:700;font-size:28px;letter-spacing:.06em;text-transform:uppercase}
h1{font-size:112px;font-weight:800;line-height:1.08;letter-spacing:-.03em;margin:40px 0 0}
h1 span{background:#F6CF5A;color:#1B2430;padding:0 14px}
.sub{font-size:38px;color:#C9D1DA;margin-top:36px;line-height:1.35}
.em{font-size:52px;margin-top:30px;font-weight:800;letter-spacing:.01em;color:#F6CF5A}
.foot{display:flex;justify-content:space-between;align-items:center;font-size:34px;font-weight:700}
.price{background:#F6CF5A;color:#1B2430;border-radius:16px;padding:14px 28px}
</style></head><body>
<div><span class="k">Junior Cycle Maths · Teacher pack</span>
<h1><span>Sets &amp; Venn</span><br><span>Diagrams</span></h1>
<div class="sub">Human Venn Diagram · Class Survey<br>Venn Dominoes · Poster · Worksheet + answers</div>
<div class="em">A ∩ B · A ∪ B · A \\ B · A′</div></div>
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
    pdf("teacher-pack", os.path.join(OUT, "Sets-and-Venn-Diagrams-Teacher-Pack-Leim.pdf"))
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--hide-scrollbars", "--window-size=1200,1200",
                    f"--screenshot={os.path.join(OUT, f'{SLUG}-cover.png')}", f"{SLUG}-cover.html"], cwd=SRC, check=True, capture_output=True)
    print("domino chain:", [(x, show(v)) for x, v in chain])
