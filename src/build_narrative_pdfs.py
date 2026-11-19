#!/usr/bin/env python3
"""Narrative writing (JC English Order 12): free sheet (-> printables/), 6-page teacher pack + 1200x1200 cover (-> OUTDIR).
Usage: python3 src/build_narrative_pdfs.py /tmp/narrative
Items come from the game's data block (story-spine.html). Every answer is re-derived with the checker's own rules
(src/test_story_spine.py: links, linked, content, person, tense, STEPS) and asserted.
Styles are read from src/build_money1_pdfs.py."""
import os, sys, random, subprocess, re
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC); sys.path.insert(0, SRC)
from test_story_spine import links, linked, content, person, tense, load, STEPS, DREAM
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/narrative"; os.makedirs(OUT, exist_ok=True)
SLUG = "narrative-writing"
LO = "W1, W3, W7, W9"
GAME = "leim.ie/story-spine.html"
D = load(os.path.join(ROOT, "story-spine.html"))
PV = {1: "First", 3: "Third"}
DREAM_END = "Then I woke up. It was all a dream."
def step_body(l, i): return l[len(STEPS[i]):].strip()

# ---------- free sheet ----------
random.seed(1212)
sp = random.sample(D["spines"], 3)
# A1: order a shuffled spine (spine phrases removed would be too hard: keep them, shuffled)
S0 = sp[0]; ordr = list(range(5)); random.shuffle(ordr)
while ordr == sorted(ordr): random.shuffle(ordr)
A_order = (S0, ordr, " → ".join("ABCDE"[ordr.index(i)] for i in range(5)))
# A2-3: gap with 3 options
A_gaps = []
for S, g in ((sp[1], 2), (sp[2], 4)):
    shown = [l for i, l in enumerate(S["lines"]) if i != g]
    others = [x["lines"][g] for x in D["spines"] if x is not S]
    random.shuffle(others); opts = [S["lines"][g]] + others[:2]; random.shuffle(opts)
    assert [o for o in opts if linked(o, shown)] == [S["lines"][g]]
    A_gaps.append((S, g, opts))
# B: cut it
B_items = []
for P in random.sample(D["plans"], 2):
    pos = random.randint(1, 4); L = P["lines"][:]; L.insert(pos, P["odd"])
    off = [i for i, l in enumerate(L) if not linked(l, L[:i] + L[i + 1:])]
    assert off == [pos], (P["k"], off)
    B_items.append((P, L, pos))
# C: who's telling
C_items = random.sample(D["pov"], 8)
while sum(k == 1 for s, k in C_items) != 4: C_items = random.sample(D["pov"], 8)
for s, k in C_items: assert person(s) == k
# D: keep it steady
D_items = []
for it in random.sample(D["steady"], 3):
    o = it[1:]; o = o[:]; random.shuffle(o)
    good = [x for x in o if (tense(x), person(x)) == (tense(it[0]), person(it[0]))]
    assert good == [it[1]]
    D_items.append((it, o))
# E: pay it off
E_items = []
for E in random.sample(D["ends"], 2):
    other = random.choice([x for x in D["ends"] if x is not E])
    o = [E["end"], E["random"], DREAM_END, other["end"]]; random.shuffle(o)
    assert [x for x in o if not DREAM.search(x) and links(x, E["lines"][1])] == [E["end"]]
    assert not any(linked(x, E["lines"]) for x in o if x != E["end"])
    E_items.append((E, o))
EX_TENSE = "I opened the gate and the dog runs straight past me. She chases it down the lane, and I shouted at her to stop."
EX_FIX = "I opened the gate and the dog ran straight past me. I chased it down the lane and shouted at it to stop."
assert tense(EX_FIX.split(". ")[0] + ".") == "past" and person(EX_FIX) == 1
NQ = 3 + len(B_items) + len(C_items) + len(D_items) + len(E_items) + 2; assert NQ == 20, NQ
nA = 1; nB = nA + 3; nC = nB + len(B_items); nD = nC + len(C_items); nE = nD + len(D_items); nF = nE + len(E_items)
def style(var):
    return re.search(var + r' = f"""<!doctype.*?<style>(.*?)</style>', open(os.path.join(SRC, "build_money1_pdfs.py"), encoding="utf-8").read(), re.S).group(1).replace("{LO}", LO).replace("{{", "{").replace("}}", "}").replace("JC Maths LOs (2018 spec)", "JC English LOs (2015 spec)")
SHEET_STYLE = style("sheet"); PACK_STYLE = style("pack")
assert "JC English LOs (2015 spec)" in SHEET_STYLE and "Single-teacher licence" in PACK_STYLE and "JC English LOs (2015 spec)" in PACK_STYLE
EXTRA = """.wk{line-height:1.45;border:1.5px solid var(--line);border-radius:8px;padding:2px 7px;margin:3px 0;font-size:9.4pt}.wk b.h{display:block}
table.st{border-collapse:collapse;margin:3px 0;font-size:9.2pt;width:100%}table.st td,table.st th{border:1px solid #C9D1DA;padding:2px 6px;text-align:left}
.bank{border:1.5px solid var(--line);border-radius:8px;padding:4px 10px;margin:4px 0;text-align:center;font-weight:700;word-spacing:4px}
.pass{border-left:4px solid var(--green);background:var(--mist);padding:5px 10px;margin:4px 0;font-style:italic}
.sty{border:1.5px solid var(--line);border-radius:8px;padding:2px 7px;margin:2px 0 3px;font-size:8.8pt}.sty p{margin:0 0 1px}"""
EXTRA = """.wk{line-height:1.45;border:1.5px solid var(--line);border-radius:8px;padding:2px 7px;margin:3px 0;font-size:9.4pt}.wk b.h{display:block}
table.st{border-collapse:collapse;margin:3px 0;font-size:9.2pt;width:100%}table.st td,table.st th{border:1px solid #C9D1DA;padding:2px 6px;text-align:left}
.bank{border:1.5px solid var(--line);border-radius:8px;padding:4px 10px;margin:4px 0;text-align:center;font-weight:700;word-spacing:4px}
.pass{border-left:4px solid var(--green);background:var(--mist);padding:5px 10px;margin:4px 0;font-style:italic}
.sty{border:1.5px solid var(--line);border-radius:8px;padding:2px 7px;margin:2px 0 3px;font-size:8.8pt}.sty p{margin:0 0 1px}"""
def sty(lines, labels):
    return "<div class='sty'>" + "".join(f"<p><b>{lab}</b> {l}</p>" for lab, l in zip(labels, lines)) + "</div>"
A_html = (f"<li value='{nA}'>Put this story spine in order. <span class='line' style='min-width:30mm'></span>" +
          sty([S0["lines"][i] for i in ordr], "ABCDE") + "</li>")
for j, (S, g, opts) in enumerate(A_gaps):
    lines = [("<b>?</b> " + STEPS[i] + " …") if i == g else l for i, l in enumerate(S["lines"])]
    A_html += (f"<li value='{nA + 1 + j}'>Circle the line that fills the gap." + sty(lines, "12345") +
               "<br>".join(f"&nbsp; {'abc'[k]}) {o}" for k, o in enumerate(opts)) + "</li>")
B_html = "".join(f"<li value='{i}'><b>{P['k'][2:].strip()}</b>: which event doesn't belong? <span class='line' style='min-width:14mm'></span>" + sty(L, "12345") + "</li>" for i, (P, L, pos) in enumerate(B_items, nB))
C_html = "".join(f"<li value='{i}'><i>{s}</i> <span class='line' style='min-width:14mm'></span></li>" for i, (s, k) in enumerate(C_items, nC))
D_html = "".join(f"<li value='{i}'><i>{it[0]}</i><br>" + " &nbsp; ".join(f"{'abcd'[k]}) {x}" for k, x in enumerate(o)) + "</li>" for i, (it, o) in enumerate(D_items, nD))
E_html = "".join(f"<li value='{i}'><b>{E['k'][2:].strip()}</b>: <i>{' '.join(E['lines'])}</i><br>" + "<br>".join(f"&nbsp; {'abcd'[k]}) {x}" for k, x in enumerate(o)) + "</li>" for i, (E, o) in enumerate(E_items, nE))

sheet = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Narrative writing, rules and practice | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{SHEET_STYLE}
{EXTRA}
.p2 ol.q li{{margin-bottom:1px;font-size:8.7pt}}.p2 h2{{margin:3px 0 1px}}.p2 .two{{gap:5mm}}.p2 .sty{{font-size:8.2pt;padding:1px 6px}}
</style></head><body>
<div class="page tight">
  <div class="band"><div><div class="k">Junior Cycle English · Free revision sheet</div><h1>Narrative writing</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2015 specification): {LO}. Play the game: <b>{GAME}</b></p>
  <div class="two">
   <div><h2>1. Plan in five minutes: the story spine</h2>
    <table class="st"><thead><tr><th>Step</th><th>What it does</th></tr></thead><tbody>
     <tr><td><b>Once upon a time…</b></td><td>who, where, and what they want or fear</td></tr>
     <tr><td><b>Every day…</b></td><td>normal life, before anything happens</td></tr>
     <tr><td><b>But one day…</b></td><td>one problem or event changes everything</td></tr>
     <tr><td><b>Because of that…</b></td><td>what it leads to: the tension builds (can repeat)</td></tr>
     <tr><td><b>Until finally…</b></td><td>the ending: the problem is solved</td></tr></tbody></table>
    <div class="wk"><i>Once upon a time, Fionn was afraid of the ball. Every day, he hid at the back of the pitch. But one day, the goalkeeper was sick. Because of that, Fionn had to play in goal in the final. Until finally, Fionn saved a penalty.</i><br>
    When you write, the spine words disappear and each step grows into a paragraph.</div>
    <h2>2. One problem</h2>
    <div class="wk">A short story has room for <b>one problem</b> and two or three characters. If an event has nothing to do with the problem, <b>cut it</b>.</div></div>
   <div><h2>3. Who's telling the story?</h2>
    <table class="st"><tbody>
     <tr><td><b>First person</b></td><td>the narrator is in the story: <i>I, me, my, we, us, our</i><br><i>My heart thumped as I opened the envelope.</i></td></tr>
     <tr><td><b>Third person</b></td><td>the narrator tells us about others: <i>he, she, they</i>, a name<br><i>Tom's heart thumped as he opened the envelope.</i></td></tr></tbody></table>
    <h2>4. Keep it steady</h2>
    <div class="wk">Choose <b>past</b> (<i>I ran</i>) or <b>present</b> (<i>I run</i>) tense, and <b>first</b> or <b>third</b> person, and keep them all the way through.<br>
    Not: <i>I <u>opened</u> the door and I <u>see</u> a fox. <u>She</u> grabs the brush.</i></div>
    <h2>5. Pay it off</h2>
    <div class="wk">The ending <b>solves the problem</b> you set up. Plan it before you start. Avoid <i>It was all a dream</i> and endings that come from nowhere.</div>
    <div class="note"><b>Classic mistakes:</b> no plan, so the story runs out of steam · too many events · switching tense · switching from I to she · an ending that has nothing to do with the problem.</div></div>
  </div>
  <div class="tip"><b>Exam tip:</b> spend five minutes on a spine before you write, and five minutes at the end reading it over for tense and narrator slips.</div>
</div>

<div class="page p2">
  <div class="band"><div><div class="k">Practice · {NQ} questions</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <div class="two"><div><h2>A. Story spine</h2><ol class="q">{A_html}</ol></div>
  <div><h2>B. Cut it</h2><ol class="q">{B_html}</ol>
  <h2>C. Who's telling? Write First or Third.</h2><ol class="q">{C_html}</ol></div></div>
</div>

<div class="page p2">
  <div class="band"><div><div class="k">Practice · continued</div><h1>Keep it steady + endings</h1></div><div class="logo">↗ Léim</div></div>
  <h2>D. Keep it steady: circle the best next line (same tense, same narrator)</h2><ol class="q">{D_html}</ol>
  <h2>E. Pay it off: circle the ending that works</h2><ol class="q">{E_html}</ol>
  <h2>F. Exam-style</h2>
  <ol class="q">
   <li value="{nF}">Rewrite in the past tense and the first person: <i>{EX_TENSE}</i><span class="long"></span><span class="long"></span></li>
   <li value="{nF + 1}">Plan a story called <b>"The Missing Key"</b> with the five steps of a story spine.<span class="long"></span><span class="long"></span><span class="long"></span><span class="long"></span></li>
  </ol>
  <h2>Answers</h2>
  <table class="ans"><tbody>
   <tr><td><b>A</b></td><td>{nA}. {A_order[2]} · {" · ".join(f"{nA + 1 + j}. {'abc'[opts.index(S['lines'][g])]}" for j, (S, g, opts) in enumerate(A_gaps))} (the right line is about the same people and problem)</td></tr>
   <tr><td><b>B</b></td><td>{" · ".join(f"{i}. line {pos + 1}: <i>{P['odd']}</i>" for i, (P, L, pos) in enumerate(B_items, nB))}</td></tr>
   <tr><td><b>C</b></td><td>{" · ".join(f"{i}. {PV[k]}" for i, (s, k) in enumerate(C_items, nC))}</td></tr>
   <tr><td><b>D</b></td><td>{" · ".join(f"{i}. {'abcd'[o.index(it[1])]}" for i, (it, o) in enumerate(D_items, nD))}</td></tr>
   <tr><td><b>E</b></td><td>{" · ".join(f"{i}. {'abcd'[o.index(E['end'])]}" for i, (E, o) in enumerate(E_items, nE))}</td></tr>
   <tr><td><b>F</b></td><td>{nF}. <i>{EX_FIX}</i><br>{nF + 1}. Sample: <i>Once upon a time, Aoife was the only one home with her dog Rua. Every day, she let herself in with the key under the flowerpot. But one day, the key was gone. Because of that, she had to search the garden in the rain while Rua barked inside. Until finally, she found the key in Rua's basket: he had carried it in from the garden.</i></td></tr>
  </tbody></table>
  <div class="note"><b>Got one wrong?</b> Go back to page 1, then play <b>Story Spine</b> at {GAME}: the "Go back over these" list at the end explains each mistake.</div>
  <p class="small">All sentences and stories written by Léim. Léim is independent and not connected with the State Examinations Commission or the NCCA.</p>
</div>
</body></html>"""

# ---------- teacher pack ----------
random.seed(1213)
JIG = random.sample(D["spines"], 4)
ODD = random.sample([P["odd"] for P in D["plans"] if not any(linked(P["odd"], S["lines"]) for S in JIG)], 4)
for o in ODD:
    for S in JIG: assert not linked(o, S["lines"]), (o, S["k"])
cards = [(l, pi, j) for pi, S in enumerate(JIG) for j, l in enumerate(S["lines"])] + [(o, -1, -1) for o in ODD]
assert len({c[0] for c in cards}) == 24
random.seed(1214); random.shuffle(cards)
jig_html = "".join(f'<div class="c"><span class="tag">Card {k}</span><div class="fc sm">{s}</div></div>' for k, (s, pi, j) in enumerate(cards, 1))
num = lambda pi, j: next(k for k, (s, a, b) in enumerate(cards, 1) if a == pi and b == j)
jig_key = "".join(f"<li><b>{S['k'][2:].strip()}</b>: {' → '.join(str(num(pi, j)) for j in range(5))}</li>" for pi, S in enumerate(JIG))
odd_key = ", ".join(str(k) for k, (s, a, b) in enumerate(cards, 1) if a == -1)

SWAP_A = ("The Sponsored Swim", [
    "Once upon a time, I was the only girl in my class who couldn't swim.",
    "Every day, I sat on the bench at the pool in Tralee and watched the others swim.",
    "But one day, our teacher announced a sponsored swim for the local hospice.",
    "Because of that, I went to the pool every morning before school with my aunt.",
    "Until finally, I managed ten lengths and raised two hundred euro for the hospice."])
SWAP_B = ("The Grumpy Farmer", [
    "Once upon a time, a boy called Eoin lived next door to a grumpy old farmer.",
    "Every day, the farmer shouted at Eoin for kicking his football into the field.",
    "But one day, a cow got stuck in the ditch beside the field.",
    "Because of that, Eoin ran for help, and he and the farmer pulled the cow out together.",
    "Until finally, the farmer built Eoin a goal at the end of the field."])
SWAP_INFO = {}
for name, L in (SWAP_A, SWAP_B):
    assert all(l.startswith(STEPS[i]) for i, l in enumerate(L)), name
    assert all([j for j in range(5) if j != i and links(L[i], L[j])] for i in range(5)), name
    P = {person(l) for l in L}; T = {tense(l) for l in L}
    assert len(P) == 1 and len(T) == 1, (name, [person(l) for l in L], [tense(l) for l in L])
    SWAP_INFO[name] = (PV[P.pop()], T.pop())
assert SWAP_INFO["The Sponsored Swim"] == ("First", "past") and SWAP_INFO["The Grumpy Farmer"] == ("Third", "past")
GRID = ["Who and where? (Once upon a time…)", "Normal life (Every day…)", "What changes? (But one day…)", "What it leads to (Because of that…)", "The ending (Until finally…)", "Narrator: first or third person?", "Tense: past or present?"]
def swap_card(who, mine, theirs):
    name, L = mine
    return f"""<div class="idc"><h3>Student {who} · Spine Swap</h3>
    <p style="font-size:8.6pt;margin:0 0 1mm"><b>1. Read your story spine aloud twice</b>, slowly. Don't show it to your partner.</p>
    <div class="pass" style="font-size:9.6pt"><b style="font-style:normal">"{name}"</b><br>{"<br>".join(L)}</div>
    <p style="font-size:8.6pt;margin:1mm 0"><b>2. Then listen</b> to "{theirs[0]}" and fill in the grid:</p>
    <table class="st" style="font-size:8.4pt"><tbody>{"".join(f"<tr><td style='width:40%'><b>{n}</b></td><td></td></tr>" for n in GRID)}</tbody></table>
    <p style="font-size:8.6pt;margin:1mm 0 0"><b>3. Together:</b> add one more "Because of that…" step to each story. Does the ending still work?</p></div>"""

FIX = [("“I started writing straight away and ran out of ideas after a page.”", "No plan. Spend five minutes on a story spine first: then you know where the story is going."),
       ("A story with a robbery, a football match, a birthday party and a trip to Spain.", "Too many events. Pick one problem and cut everything that isn't about it."),
       ("“I run to the door and I opened it.”", "Tense switch. Keep the past: <b>I ran to the door and opened it.</b>"),
       ("“I grabbed my coat. Then she ran outside.” (the narrator is the same girl)", "Narrator switch. Keep first person: <b>Then I ran outside.</b>"),
       ("“…and then I woke up. It was all a dream.”", "A cheat ending: nothing was at stake. Plan a real ending before you start."),
       ("The problem is a lost dog, but the ending is about winning a medal.", "The ending doesn't solve the problem. Go back to the spine: the ending must answer “But one day…”.")]
assert tense("I ran to the door and opened it.") == "past" and person("Then I ran outside.") == 1 and DREAM.search(FIX[4][0])

GATE = ["Every Saturday, I walked Gran's dog, Bonnie, along the river in Fermoy.",
        "We always went through the green gate at the end of Gran's road.",
        "But that Saturday, the gate was locked with a shiny new padlock.",
        "Bonnie pulled at the lead and whined.",
        "Through the bars, I saw a small rowing boat drifting in the middle of the river, and a boy waving from the far bank."]
assert person(" ".join(GATE)) == 1 and all(tense(l) == "past" for l in GATE), [tense(l) for l in GATE]
REWRITE = "Through the bars, she saw a small rowing boat drifting in the middle of the river, and a boy waving from the far bank."
assert person(REWRITE) == 3 and tense(REWRITE) == "past"

pack = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Narrative Writing Teacher Pack | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{PACK_STYLE}
{EXTRA}
.fym .c{{height:30mm}}.fym .fc.sm{{font-size:9.6pt;line-height:1.28;margin-top:2mm;font-weight:600}}.idc{{padding:2mm 4mm;margin-bottom:3mm}}.idc h3{{margin:0 0 1mm}}
.idc .st td{{height:4.6mm;padding:1px 6px}}.p1 .proc td{{font-size:8.6pt;padding:2px 6px}}.ops div{{font-size:12pt;padding:5mm 3mm}}.ops b{{font-size:19pt}}
.ws .eh td{{font-size:8.6pt;padding:2px 6px}}.ws .eh .gap{{height:13px}}.ws ol.q li{{margin-bottom:1px}}
</style></head><body>

<div class="page p1">
  <div class="band"><div><div class="k">Junior Cycle English · Teacher pack</div><h1>Narrative writing</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2015 specification): {LO}</p>
  <div class="two">
    <div><h3>Aims</h3><p>By the end of the lesson students can plan a story in five minutes with a story spine, keep a story to one problem, recognise first- and third-person narrators, keep the tense and narrator steady, and choose an ending that solves the problem they set up.</p></div>
    <div><h3>In this pack</h3><p>p.1 Teacher notes · p.2 Spine Jigsaw cards (cut-up) · p.3 Spine Swap A/B (speaking + listening) · p.4 Wall poster · p.5 Worksheet: Fix the Story + exam-style questions · p.6 Answers. Level: 1st year (useful all through Junior Cycle). Time: about 60 minutes. All stories are original.</p></div>
  </div>
  <h2 style="margin-top:8px">Procedure</h2>
  <table class="proc"><tbody>
    <tr><td>5 min</td><td><b>Lead-in.</b> Ask: why do stories in exams run out of steam, or end with “I woke up”? Elicit: no plan. Write the five spine words on the board: <i>Once upon a time · Every day · But one day · Because of that · Until finally</i>.</td></tr>
    <tr><td>8 min</td><td><b>Guided discovery.</b> Read one line at a time: <i>Once upon a time, Fionn was afraid of the ball. Every day, he hid at the back of the pitch. But one day, the goalkeeper was sick. Because of that, Fionn had to play in goal in the final. Until finally, Fionn saved a penalty.</i> What job does each line do? Could two lines swap? Which line solves the problem from line 1?</td></tr>
    <tr><td>12 min</td><td><b>Spine Jigsaw</b> (p.2, groups of 3–4, one set of 24 cards). Rebuild 4 story spines in order. 4 cards belong to no story: find them and say why they'd be cut.</td></tr>
    <tr><td>15 min</td><td><b>Spine Swap</b> (p.3, pairs). A reads a spine aloud; B fills the grid, including the narrator and the tense. Swap. Then each pair adds a “Because of that…” step to both stories.</td></tr>
    <tr><td>15 min</td><td><b>Worksheet</b> (p.5). Fix the Story in pairs, then the exam-style questions on "The Green Gate" alone.</td></tr>
    <tr><td>5 min</td><td><b>Exit ticket.</b> A five-line spine for a story called "The Storm". Homework: turn it into a story, or play <b>Story Spine</b> at {GAME}.</td></tr>
  </tbody></table>
  <div class="note"><b>Errors to look for:</b> spines with two problems · “Because of that” steps that don't follow from the step before · endings unrelated to the problem · I/she and past/present switches in students' own writing. <b>Support:</b> give weaker groups the 4 “Once upon a time” cards first. <b>Fast finishers:</b> retell one jigsaw spine in the first person, or in the present tense.</div>
  <p class="small"><b>Spine Jigsaw key</b> (cards in order):</p><ul class="small" style="columns:2;margin:0">{jig_key}</ul><p class="small">Cards that belong to no story: {odd_key}.</p>
</div>

<div class="page">
  <div class="band"><div><div class="k">Groups of 3–4 · cut up the 24 cards</div><h1>Spine Jigsaw</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.4pt;margin:0 0 2mm">The cards make <b>4 story spines</b> of 5 steps each. Rebuild each one in order. <b>4 cards belong to no story</b>: find them and cut them.</p>
  <div class="fym">{jig_html}</div>
</div>

<div class="page">
  <div class="band"><div><div class="k">Pairs · cut along the dashed line</div><h1>Spine Swap A/B</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.4pt">Each of you has a story spine. Listen carefully: can you catch every step, the narrator and the tense?</p>
  {swap_card("A", SWAP_A, SWAP_B)}
  {swap_card("B", SWAP_B, SWAP_A)}
</div>

<div class="page">
  <div class="poster">
    <h1>Plan it. Stick to it. Pay it off.</h1>
    <div class="ops">
      <div style="background:var(--green-soft)"><b>Once upon a time…</b>who, where, what they want</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Every day…</b>normal life</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>But one day…</b>one problem</div>
      <div style="background:var(--green-soft)"><b>Because of that…</b>the tension builds</div>
      <div style="background:var(--green-soft)"><b>Until finally…</b>solve the problem</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Keep it steady</b>same tense · same narrator</div>
    </div>
    <p style="text-align:center;font-size:20pt!important;font-weight:800;margin:4mm 0">Five minutes planning. No "I woke up".</p>
    <p style="text-align:center;font-size:10pt;color:var(--muted)">Léim · leim.ie · Play Story Spine: {GAME}</p>
  </div>
</div>

<div class="page ws">
  <div class="band"><div><div class="k">Worksheet · exam-style questions</div><h1>Fix the Story</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Fix the Story</h2>
  <p>Each one has a problem. Say what's wrong and write or describe a better version.</p>
  <table class="eh"><thead><tr><th>What the writer did</th><th>What's wrong and the fix</th></tr></thead><tbody>
  {"".join(f"<tr><td style='font-weight:500'>{s}</td><td><span class='gap'></span><span class='gap'></span></td></tr>" for s, r in FIX)}
  </tbody></table>
  <h2>B. Exam-style questions: "The Green Gate"</h2>
  <div class="pass">{" ".join(GATE)}</div>
  <ol class="q">
    <li>Is this story told in the first or the third person? Quote two words that show it.<span class="long"></span></li>
    <li>Which tense is it told in? Give two verbs from the text that show it.<span class="long"></span></li>
    <li>Fill in the first three steps of a story spine for this opening (Once upon a time… / Every day… / But one day…).<span class="long"></span><span class="long"></span></li>
    <li>Write the last two steps (Because of that… / Until finally…) so the ending solves the problem.<span class="long"></span><span class="long"></span></li>
    <li>Rewrite the last sentence in the third person (the narrator is a girl).<span class="long"></span></li>
  </ol>
</div>

<div class="page an">
  <div class="band"><div><div class="k">For the teacher</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>Spine Jigsaw</h2>
  <ul style="columns:2;margin:0">{jig_key}</ul>
  <p>Cards that belong to no story: {odd_key} ({"; ".join(ODD)}).</p>
  <h2>Spine Swap</h2>
  {"".join(f"<p><b>{n}:</b> {' / '.join(step_body(l, i) for i, l in enumerate(L))} · Narrator: {SWAP_INFO[n][0]} person · Tense: {SWAP_INFO[n][1]}</p>" for n, L in (SWAP_A, SWAP_B))}
  <h2>A. Fix the Story</h2>
  <table><tbody>{"".join(f"<tr><td style='width:40%'>{s}</td><td>{r}</td></tr>" for s, r in FIX)}</tbody></table>
  <h2>B. Exam-style questions</h2>
  <ol class="q">
    <li>First person: "I walked", "I saw" (also "We always went").</li>
    <li>Past tense: walked, went, was, pulled, whined, saw (any two).</li>
    <li>Once upon a time, a girl walked her gran's dog Bonnie by the river in Fermoy. Every day (Saturday), they went through the green gate. But one day, the gate was locked with a new padlock.</li>
    <li>Credit two steps that follow on: e.g. Because of that, she climbed the wall and ran along the bank to the boy. Until finally, she helped him pull the boat in with Bonnie's lead. The ending must link to the locked gate or the boat.</li>
    <li>{REWRITE}</li>
  </ol>
  <h2>Marking tip</h2>
  <p>In students' own stories, reward a clear shape (one problem, an ending that solves it) and control (steady tense and narrator) more than length. Our guide, not an official marking scheme.</p>
</div>
</body></html>"""

cover = """<!doctype html><html><head><meta charset="utf-8"><style>
body{margin:0;width:1200px;height:1200px;background:#1B2430;font-family:Inter,sans-serif;color:#fff;display:flex;flex-direction:column;justify-content:space-between;padding:90px;box-sizing:border-box}
.k{display:inline-block;background:#2E7D57;border-radius:99px;padding:12px 26px;font-weight:700;font-size:28px;letter-spacing:.06em;text-transform:uppercase}
h1{font-size:104px;font-weight:800;line-height:1.25;letter-spacing:-.02em;margin:60px 0 20px}
h1 span{background:#F6CF5A;color:#1B2430;padding:0 18px;border-radius:14px}
.sub{font-size:40px;line-height:1.4;color:#DDE3EA}
.em{font-size:48px;margin-top:30px;font-weight:800;letter-spacing:.01em;color:#F6CF5A}
.foot{display:flex;justify-content:space-between;align-items:center;font-size:34px;font-weight:700}
.price{background:#F6CF5A;color:#1B2430;border-radius:16px;padding:14px 28px}
</style></head><body>
<div><span class="k">Junior Cycle English · Teacher pack</span>
<h1><span>Narrative</span><br><span>writing</span></h1>
<div class="sub">Spine Jigsaw cards · Spine Swap A/B<br>Poster · Worksheet + answers</div>
<div class="em">plan a story · one problem<br>tense &amp; narrator · endings</div></div>
<div class="foot"><span>↗ Léim · leim.ie</span><span class="price">Ready to teach · 60 min</span></div>
</body></html>"""

if __name__ == "__main__":
    for name, txt in [("rules-and-practice", sheet), ("teacher-pack", pack), ("cover", cover)]:
        open(os.path.join(SRC, f"{SLUG}-{name}.html"), "w", encoding="utf-8").write(txt)
    def pdf(name, out):
        subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--no-pdf-header-footer", f"--print-to-pdf={out}",
                        f"{SLUG}-{name}.html"], cwd=SRC, check=True, capture_output=True)
        print(name, subprocess.run(["pdfinfo", out], capture_output=True, text=True).stdout.split("Pages:")[1].split()[0], "pages")
    pdf("rules-and-practice", os.path.join(ROOT, "printables", f"{SLUG}-rules-and-practice.pdf"))
    pdf("teacher-pack", os.path.join(OUT, "Narrative-Writing-Teacher-Pack-Leim.pdf"))
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--hide-scrollbars", "--window-size=1200,1200",
                    f"--screenshot={os.path.join(OUT, f'{SLUG}-cover.png')}", f"{SLUG}-cover.html"], cwd=SRC, check=True, capture_output=True)
