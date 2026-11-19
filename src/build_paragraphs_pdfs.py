#!/usr/bin/env python3
"""Paragraphs & topic sentences (JC English Order 7): free sheet (-> printables/), 6-page teacher pack + 1200x1200 cover (-> OUTDIR).
Usage: python3 src/build_paragraphs_pdfs.py /tmp/para
Items come from the game's data block (paragraph-builder.html). Every answer is re-derived with the checker's own rules
(src/test_paragraph_builder.py: topic_line, odd_line, rank, tip, link_group) and asserted. Styles are read from src/build_money1_pdfs.py."""
import os, sys, random, subprocess, re, json
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC); sys.path.insert(0, SRC)
from test_paragraph_builder import topic_line, odd_line, rank, tip, link_group, links, GOF, load
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/para"; os.makedirs(OUT, exist_ok=True)
SLUG = "paragraphs"
LO = "W1, W10, W3"
GAME = "leim.ie/paragraph-builder.html"
D = load(os.path.join(ROOT, "paragraph-builder.html"))
P = {x["k"].split(" ", 1)[1]: x for x in D["paras"]}
TIPN = {"ti": "Time", "pl": "Place", "to": "Topic", "pe": "Person"}
LET = "ABC"

# ---------- free sheet ----------
random.seed(77)
A_items = []
for name in ("Breakfast", "Plastic"):
    x = P[name]; L = [x["topic"]] + x["sup"]; random.shuffle(L)
    while L[0] == x["topic"]: random.shuffle(L)
    assert topic_line(L) == L.index(x["topic"]); A_items.append((L, L.index(x["topic"]) + 1, x["topic"]))
B_items = []
for name in ("Hurling", "Music"):
    x = P[name]; L = [x["topic"]] + x["sup"]; pos = random.randint(1, 4); L.insert(pos, x["odd"])
    assert odd_line(L) == pos; B_items.append((L, pos + 1, x["odd"]))
C_items = []
for i in (0, 11):
    S = D["seq"][i]; idx = [1, 2, 3]; random.shuffle(idx)
    while idx == [1, 2, 3]: random.shuffle(idx)
    ans = " ".join(LET[idx.index(n)] for n in (1, 2, 3))
    assert sorted(LET[j] for j in range(3)) == sorted(ans.split()) and [rank(S[n]) for n in idx] != [1, 2, 3]
    assert " ".join(l for l, s in sorted(zip(LET, [S[n] for n in idx]), key=lambda z: rank(z[1]))) == ans
    C_items.append((S[0], [S[n] for n in idx], ans))
D_items = []
for k in ("ti", "pl", "to", "pe"):
    D_items += [t for t in D["tip"] if t[2] == k][1:2]
random.shuffle(D_items)
assert {k for b, a, k in D_items} == {"ti", "pl", "to", "pe"}
for b, a, k in D_items: assert tip(b, a) == [k], (a, tip(b, a))
BANK = ["However", "For example", "As a result", "In addition", "On the other hand", "Because of this"]
E_items = []
for w in BANK:
    it = next(l for l in D["link"] if l[2] == w); E_items.append(it); assert link_group(it[0], it[1]) == GOF[w], it
random.shuffle(E_items)
F_items = [(["The museum has a dinosaur skeleton.", "Visitors can try on a suit of armour.", "Entry is free on Sundays."], "Our local museum is a brilliant day out."),
           (["We sang songs the whole way there on the bus.", "Every student in our class won a medal.", "The rain held off until we got home."], "Our school tour was a day to remember."),
           ]
SNOW = ["We woke up to a white world.", "Snow covered every car and every roof on our road.", "School was closed, so we raced outside in our pyjamas.",
        "An hour later, our fingers were frozen.", "We had built a snowman taller than Dad.", "Granny phoned to say she was snowed in.",
        "So we made her a tray of hot scones and carried them through the snow."]
SNOW_BREAKS = {3: "ti", 5: "pe"}
for i in range(1, len(SNOW)):
    got = tip(SNOW[i - 1], SNOW[i]); assert got == ([SNOW_BREAKS[i]] if i in SNOW_BREAKS else []), (SNOW[i], got)
NQ = len(A_items) + len(B_items) + len(C_items) + len(D_items) + len(E_items) + len(F_items) + 2; assert NQ == 20, NQ
nA, nB, nC, nD, nE, nF = 1, 3, 5, 7, 11, 17

def numlines(L): return "".join(f"<span class='n'>{i}</span> {s} " for i, s in enumerate(L, 1))
def style(var):
    return re.search(var + r' = f"""<!doctype.*?<style>(.*?)</style>', open(os.path.join(SRC, "build_money1_pdfs.py"), encoding="utf-8").read(), re.S).group(1).replace("{LO}", LO).replace("{{", "{").replace("}}", "}").replace("JC Maths LOs (2018 spec)", "JC English LOs (2015 spec)")
SHEET_STYLE = style("sheet"); PACK_STYLE = style("pack")
assert "JC English LOs (2015 spec)" in SHEET_STYLE and "Single-teacher licence" in PACK_STYLE and "JC English LOs (2015 spec)" in PACK_STYLE
EXTRA = """.wk{line-height:1.45;border:1.5px solid var(--line);border-radius:8px;padding:2px 7px;margin:3px 0;font-size:9.4pt}.wk b.h{display:block}
table.st{border-collapse:collapse;margin:3px 0;font-size:9.4pt;width:100%}table.st td,table.st th{border:1px solid #C9D1DA;padding:2px 6px;text-align:left}
.bank{border:1.5px solid var(--line);border-radius:8px;padding:4px 10px;margin:4px 0;text-align:center;font-weight:700;word-spacing:4px}
.pass{border-left:4px solid var(--green);background:var(--mist);padding:5px 10px;margin:4px 0}
.pg{border:1.5px solid var(--line);border-radius:8px;padding:3px 7px;margin:2px 0 3px;font-size:9pt;line-height:1.38}
.pg .n{display:inline-block;min-width:13px;height:13px;border-radius:50%;background:#1B2430;color:#fff;font-size:7pt;font-weight:800;text-align:center;line-height:13px;margin-right:1px}
.pg .l{display:inline-block;min-width:13px;height:13px;border-radius:50%;background:#F6CF5A;color:#1B2430;font-size:7pt;font-weight:800;text-align:center;line-height:13px;margin-right:1px}"""

def pgq(i, html, ask): return f"<li value='{i}'><div class='pg'>{html} <b>{ask}</b> <span class='line' style='min-width:12mm'></span></div></li>"
A_html = "".join(pgq(i, numlines(L), "→ Topic sentence:") for i, (L, a, t) in enumerate(A_items, nA))
B_html = "".join(pgq(i, numlines(L), "→ Doesn't belong:") for i, (L, a, t) in enumerate(B_items, nB))
C_html = "".join(pgq(i, f"<b>{t}</b> " + "".join(f"<span class='l'>{LET[j]}</span> {s} " for j, s in enumerate(L)), "→ Order:") for i, (t, L, a) in enumerate(C_items, nC))
D_html = "".join(f"<li value='{i}'>… {b} <b>//</b> {a} <span class='line' style='min-width:16mm'></span></li>" for i, (b, a, k) in enumerate(D_items, nD))
E_html = "".join(f"<li value='{i}'>{a} _____________, {b}</li>" for i, (a, b, w) in enumerate(E_items, nE))
F_html = "".join(f"<li value='{i}'>{' '.join(d)}<span class='long'></span></li>" for i, (d, m) in enumerate(F_items, nF))

sheet = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Paragraphs: rules and practice | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{SHEET_STYLE}
{EXTRA}
.p2 ol.q li{{margin-bottom:1px}}.p2 .pg{{font-size:8.3pt;line-height:1.3;margin:1px 0}}.p2 .two{{gap:4mm}}.p2 h2{{margin:4px 0 2px}}
.p2 .dd li,.p2 ol.q li{{font-size:8.6pt}}.p2 .long{{height:13px}}.p2 .pass{{font-size:8.6pt;padding:3px 8px;margin:2px 0}}
</style></head><body>
<div class="page tight">
  <div class="band"><div><div class="k">Junior Cycle English · Free revision sheet</div><h1>Paragraphs and topic sentences</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2015 specification): {LO}. Play the game: <b>{GAME}</b></p>
  <div class="two">
   <div><h2>1. What is a paragraph?</h2>
    <p>A group of sentences about <b>one main idea</b>. One paragraph = one idea. A sentence about something else doesn't belong: move it or cut it.</p>
    <h2>2. How a paragraph is built</h2>
    <table class="st"><tbody>
     <tr><td><b>Topic sentence</b></td><td>the main idea, usually first: <i>Dogs are loyal and loving pets.</i></td></tr>
     <tr><td><b>Supporting sentences</b></td><td>details, facts, examples, reasons: <i>A dog will often wait by the door for its owner to come home.</i></td></tr>
     <tr><td><b>Link</b></td><td>a last line that sums up or leads into the next paragraph</td></tr></tbody></table>
    <h2>3. Spot the topic sentence</h2>
    <div class="wk">It could be a <b>title</b> for all the other sentences, and every other sentence <b>links back</b> to it: <i>Puffins are some of the most unusual birds in Ireland.</i> → puffins arrive every spring · these birds dig burrows · their beaks look unusual.</div>
    <h2>4. When to start a new paragraph: TiPToP</h2>
    <table class="st"><tbody>
     <tr><td><b>Ti</b>me</td><td>time moves on: <i>The next morning, … · Two hours later, …</i></td></tr>
     <tr><td><b>P</b>lace</td><td>a new place: <i>Back at home, … · Inside the stadium, …</i></td></tr>
     <tr><td><b>To</b>pic</td><td>a new point or idea: <i>Another reason … · On the other hand, …</i></td></tr>
     <tr><td><b>P</b>erson</td><td>a new person comes in or speaks: <i>Mr Byrne stood up.</i></td></tr></tbody></table></div>
   <div><h2>5. Linking words</h2>
    <table class="st"><tbody>
     <tr><td><b>Order</b></td><td>First, At first, Next, Then, After that, Finally, In the end</td></tr>
     <tr><td><b>Adding</b></td><td>In addition, Also, What's more</td></tr>
     <tr><td><b>Contrast</b></td><td>However, On the other hand</td></tr>
     <tr><td><b>Example</b></td><td>For example, For instance</td></tr>
     <tr><td><b>Result</b></td><td>As a result, Because of this</td></tr></tbody></table>
    <p>Put a comma after a linking word at the start of a sentence: <i>However, the rooms were not clean.</i> One or two per paragraph is plenty.</p>
    <h2>6. A paragraph that argues a point</h2>
    <div class="wk"><b>Point:</b> School uniforms save families money.<br><b>Support:</b> A uniform costs less than the clothes students would want every week. <b>For example,</b> a jumper and two shirts can last a whole year.<br><b>Link:</b> <b>For these reasons,</b> uniforms should stay.</div>
    <h2>7. Showing paragraphs</h2>
    <p>In handwriting, leave a line between paragraphs or start the first line further in (indent). Be consistent.</p>
    <div class="note"><b>Classic mistakes:</b> one long block with no paragraphs · a new paragraph for every sentence · a topic sentence with nothing after it · a sentence that wanders off the point · "However" where there's no contrast.</div></div>
  </div>
  <div class="tip"><b>Exam tip:</b> before you write, jot down one word for each paragraph's main idea. Then each paragraph starts with a topic sentence about that word.</div>
</div>

<div class="page p2">
  <div class="band"><div><div class="k">Practice · {NQ} questions</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <div class="two"><div><h2>A. Which is the topic sentence?</h2><ol class="q">{A_html}</ol></div>
  <div><h2>B. Which sentence doesn't belong?</h2><ol class="q">{B_html}</ol></div></div>
  <h2>C. Put A, B and C in the right order after the topic sentence</h2><ol class="q">{C_html}</ol>
  <h2>D. A new paragraph starts at // . Why? Write Time, Place, Topic or Person.</h2><ol class="q dd">{D_html}</ol>
  <h2>E. Fill each gap with a linking word (use each once)</h2>
  <div class="bank">{" · ".join(sorted(BANK))}</div><ol class="q" style="columns:2;column-gap:8mm">{E_html}</ol>
  <h2>F. Write a topic sentence for these details</h2><ol class="q ff">{F_html}</ol>
  <h2>G. Exam-style</h2>
  <ol class="q">
   <li value="{NQ - 1}">This should be three paragraphs. Write the first two words of each new paragraph, and the TiPToP reason. <div class="pass">{" ".join(SNOW)}</div></li>
   <li value="{NQ}">Write one paragraph: "Every town should have a skate park." Use a topic sentence, two supporting sentences and a linking word.<span class="long"></span><span class="long"></span></li>
  </ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">Check your work</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <table class="ans"><tbody>
   <tr><td><b>A</b></td><td>{" · ".join(f"{i}. sentence {a} ({t})" for i, (L, a, t) in enumerate(A_items, nA))}</td></tr>
   <tr><td><b>B</b></td><td>{" · ".join(f"{i}. sentence {a} ({t})" for i, (L, a, t) in enumerate(B_items, nB))}</td></tr>
   <tr><td><b>C</b></td><td>{" · ".join(f"{i}. {a}" for i, (t, L, a) in enumerate(C_items, nC))}</td></tr>
   <tr><td><b>D</b></td><td>{" · ".join(f"{i}. {TIPN[k]}" for i, (b, a, k) in enumerate(D_items, nD))}</td></tr>
   <tr><td><b>E</b></td><td>{" · ".join(f"{i}. {w}" for i, (a, b, w) in enumerate(E_items, nE))}<br>(However / On the other hand and As a result / Because of this are in the same family, so either is right in those gaps. For instance / What's more also work for For example / In addition.)</td></tr>
   <tr><td><b>F</b></td><td>Any sentence that sums up all three details, e.g. {" · ".join(f"{i}. {m}" for i, (d, m) in enumerate(F_items, nF))}</td></tr>
   <tr><td><b>G</b></td><td>{NQ - 1}. New paragraphs start at "An hour" (Time) and "Granny phoned" (Person).<br>{NQ}. e.g. <b>Every town should have a skate park.</b> Teenagers need somewhere safe to meet in the evenings. For example, the skate park in Clonakilty is busy every night. As a result, our council should build one this year.</td></tr>
  </tbody></table>
  <h2>Worked examples</h2>
  <div class="two">
   <div class="wk"><b class="h">{nA}. Which is the topic sentence?</b>Sentence {A_items[0][1]} ("{A_items[0][2]}") could be a title for the others. Each other sentence gives a detail that links back to it.</div>
   <div class="wk"><b class="h">{nB}. Which doesn't belong?</b>"{B_items[0][2]}" has nothing to do with hurling. One paragraph = one main idea.</div>
   <div class="wk"><b class="h">{nC}. Order</b>Look for the order words: First → Next → Finally.</div>
   <div class="wk"><b class="h">{nE}–{nE + 5}. Linking words</b>Ask what the second sentence does: the opposite (However), an example (For example), a result (As a result) or one more point (In addition).</div>
  </div>
  <div class="note"><b>Got one wrong?</b> Ask: what is this paragraph about? Then play <b>Paragraph Builder</b> at {GAME}: the "Go back over these" list at the end shows the reason for each mistake.</div>
  <p class="small">All sentences written by Léim. Léim is independent and not connected with the State Examinations Commission or the NCCA.</p>
</div>
</body></html>"""

# ---------- teacher pack ----------
JIG = [D["seq"][i] for i in (1, 2, 3, 5, 8, 9)]
for S in JIG: assert [rank(s) for s in S[1:]] == [1, 2, 3] and rank(S[0]) is None
cards = [(s, pi, j) for pi, S in enumerate(JIG) for j, s in enumerate(S)]
random.seed(707); random.shuffle(cards)
jig_html = "".join(f'<div class="c"><span class="tag">Card {k}</span><div class="fc sm">{s}</div></div>' for k, (s, pi, j) in enumerate(cards, 1))
jig_key = "".join(f"<li><b>{S[0]}</b> Cards {' → '.join(str(next(k for k, (s, a, b) in enumerate(cards, 1) if a == pi and b == j)) for j in range(4))}</li>" for pi, S in enumerate(JIG))

STORY_A = ("The Sleepover", ["Ciara's sleepover was supposed to be the best night of the year.", "Six of us squeezed into her bedroom with sleeping bags and snacks.",
            "We watched two films and ate far too many crisps.", "At midnight, the lights suddenly went out.", "Somebody screamed, and the popcorn went everywhere.",
            "Down in the kitchen, we found a torch in a drawer.", "The whole street outside was dark.", "Ciara's dad appeared at the back door with a lantern.",
            "He told us the storm had knocked down a power line.", "We spent the rest of the night telling ghost stories by lantern light."], {3: "ti", 5: "pl", 7: "pe"})
STORY_B = ("The Breakfast Club", ["Our school should start a breakfast club.", "Many students arrive in the morning without eating anything.",
            "It is hard to concentrate in class on an empty stomach.", "Another reason is that a breakfast club helps students make friends.",
            "Students from different years would sit together and chat.", "On the other hand, some people say it would cost too much.",
            "The canteen already has a toaster and a kettle.", "Parents could donate cereal and fruit.",
            "In addition, students who arrive early would have somewhere warm to wait.", "The breakfast club deserves a try."], {3: "to", 5: "to", 8: "to"})
for name, L, br in (STORY_A, STORY_B):
    for i in range(1, len(L)):
        got = tip(L[i - 1], L[i]); assert got == ([br[i]] if i in br else []), (name, L[i], got)
def story_card(who, mine, theirs):
    name, L, br = mine
    txt = "".join((" <b>//</b> " if i in br else " ") + s + (f" <span style='color:var(--green);font-weight:800'>[{TIPN[br[i]]}]</span>" if i in br else "") for i, s in enumerate(L))
    return f"""<div class="idc"><h3>Student {who} · Paragraph Swap</h3>
    <p style="font-size:8.6pt;margin:0 0 1mm"><b>1. Read your story aloud</b> slowly, one sentence at a time. Your partner listens with their book closed and says <b>"New paragraph!"</b> + the reason (Time, Place, Topic or Person) when they hear one. Check against the <b>//</b> marks.</p>
    <p style="font-size:9.6pt;line-height:1.45;margin:0 0 1mm"><b>"{name}"</b>{txt}</p>
    <p style="font-size:8.6pt;margin:0"><b>2. Then listen</b> to your partner's story, "{theirs[0]}". Say "New paragraph!" + the reason each time you hear one. How many did you get out of {len(theirs[2])}?</p></div>"""

FIX = [("The sliotar can travel at 150 km an hour. Hurling players need quick hands. Teams race from end to end in seconds.",
        "No topic sentence. Add one first: <b>Hurling is one of the fastest field games in the world.</b>"),
       ("Breakfast gives you energy for the morning. Students who eat breakfast concentrate better. My cousin lives in Sligo. Porridge is a cheap, filling breakfast choice.",
        "Off-topic sentence: cut <b>My cousin lives in Sligo.</b>"),
       ("Dogs are loyal pets. They wait by the door for you. Cats prefer to be left alone and sleep all day.",
        "Two ideas: start a new paragraph (new <b>topic</b>) at <b>Cats prefer…</b>, with its own topic sentence and details."),
       ("The test seemed easy at first. As a result, nobody finished the last question.",
        "Wrong linking word: it's a contrast, not a result. <b>However,</b> nobody finished the last question."),
       ("Phones are a big distraction in class.",
        "A topic sentence on its own isn't a paragraph. Add details or examples: <b>A single buzz can pull attention away from the lesson…</b>"),
       ("We went to bed at ten. The next morning, the garden was covered in snow.",
        "Time moves on: start a new paragraph at <b>The next morning,</b> (TiPToP: Time).")]
assert link_group("The test seemed easy at first.", "nobody finished the last question.") == "contrast"
assert odd_line(["Breakfast gives you energy for the morning.", "Students who eat breakfast concentrate better.", "My cousin lives in Sligo.", "Porridge is a cheap, filling breakfast choice."]) == 2
assert tip("We went to bed at ten.", "The next morning, the garden was covered in snow.") == ["ti"]
assert topic_line(["Hurling is one of the fastest field games in the world.", "The sliotar can travel at 150 km an hour, so the game never slows down.", "Hurling players need quick hands.", "Teams race from one end of the field to the other in seconds."]) == 0
RIVER = ["Rain had been falling on Bandon for three days.", "By Friday, the river was brown and roaring.", "We kept checking the weather warnings on the radio.",
         "That night, the water crept over the riverbank.", "As a result, the road outside our house disappeared under the flood.",
         "Upstairs in my bedroom, I watched the water rise.", "Our car floated slowly away down the street.",
         "Mrs Daly from next door rowed up to our window in a little red boat.", "She was laughing and waving a flask of tea.", "I was too worried about our car to laugh."]
RIVER_BR = {3: "ti", 5: "pl", 7: "pe"}
for i in range(1, len(RIVER)):
    got = tip(RIVER[i - 1], RIVER[i]); assert got == ([RIVER_BR[i]] if i in RIVER_BR else []), (RIVER[i], got)
assert link_group("That night, the water crept over the riverbank.", "the road outside our house disappeared under the flood.") == "result"

pack = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Paragraphs Teacher Pack | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{PACK_STYLE}
{EXTRA}
.fym .c{{height:30mm}}.fym .fc.sm{{font-size:9.6pt;line-height:1.28;margin-top:2mm;font-weight:600}}.idc{{padding:2mm 4mm;margin-bottom:3mm}}.idc h3{{margin:0 0 1mm}}
.p1 .proc td{{font-size:8.6pt;padding:2px 6px}}.ops div{{font-size:12pt;padding:4mm 3mm}}.ops b{{font-size:18pt}}.pass{{font-size:9pt;line-height:1.38}}.ws .eh td{{font-size:8.6pt;padding:2px 6px}}.ws .eh .gap{{height:13px}}.ws ol.q li{{margin-bottom:1px}}
</style></head><body>

<div class="page p1">
  <div class="band"><div><div class="k">Junior Cycle English · Teacher pack</div><h1>Paragraphs and topic sentences</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2015 specification): {LO}</p>
  <div class="two">
    <div><h3>Aims</h3><p>By the end of the lesson students can find and write a topic sentence, support it with details, cut a sentence that doesn't belong, put a paragraph in a logical order, know when to start a new paragraph (TiPToP: time, place, topic, person) and choose the right linking word.</p></div>
    <div><h3>In this pack</h3><p>p.1 Teacher notes · p.2 Paragraph Jigsaw cards (cut-up) · p.3 Paragraph Swap A/B (speaking + listening) · p.4 Wall poster · p.5 Worksheet: Fix the Paragraph + exam-style questions · p.6 Answers. Level: 1st year (useful revision in 2nd and 3rd). Time: about 60 minutes. All texts are original.</p></div>
  </div>
  <h2 style="margin-top:8px">Procedure</h2>
  <table class="proc"><tbody>
    <tr><td>5 min</td><td><b>Lead-in.</b> Read out four jumbled sentences about puffins. Which one could be the title for the others? Elicit: the <b>topic sentence</b> gives the main idea; the others give details and link back to it.</td></tr>
    <tr><td>8 min</td><td><b>Guided discovery.</b> Show a paragraph with one off-topic sentence. Pairs find it and say why. Board: one paragraph = one main idea; topic sentence + supporting sentences + link. Then TiPToP and the linking-word families.</td></tr>
    <tr><td>15 min</td><td><b>Paragraph Jigsaw</b> (p.2, groups of 3–4, one set of 24 cards). Sort the cards into 6 paragraphs, put the topic sentence first and the rest in order. Fast groups: write a 7th paragraph of their own on blank cards.</td></tr>
    <tr><td>12 min</td><td><b>Paragraph Swap</b> (p.3, pairs). A reads "The Sleepover" aloud; B listens with the book closed and calls "New paragraph!" + the TiPToP reason. A checks against the // marks. Swap for "The Breakfast Club".</td></tr>
    <tr><td>15 min</td><td><b>Worksheet</b> (p.5). Fix the Paragraph in pairs, then the exam-style questions on "The Day the River Rose" alone.</td></tr>
    <tr><td>5 min</td><td><b>Exit ticket.</b> Write a topic sentence for a paragraph about your favourite place, and one supporting sentence that starts "For example,". Homework: play <b>Paragraph Builder</b> at {GAME}.</td></tr>
  </tbody></table>
  <div class="note"><b>Errors to look for:</b> picking the most interesting detail as the topic sentence (it must sum up all the others) · a new paragraph for every sentence · one huge block · "However" with no contrast · starting every sentence with a linking word. <b>Support:</b> the poster (p.4) on the desk; give weaker groups the topic sentences of the jigsaw first. <b>Fast finishers:</b> rewrite "The Sleepover" with a fourth paragraph that starts with a new place.</div>
  <p class="small"><b>Jigsaw key</b> (topic sentence first, then in order):</p>
  <ol class="small" style="font-size:7.8pt;line-height:1.3;margin:0;padding-left:16px">{jig_key}</ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">Groups of 3–4 · cut up the 24 cards</div><h1>Paragraph Jigsaw</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.4pt;margin:0 0 2mm">The cards make <b>6 paragraphs</b> of 4 sentences. Find each paragraph's <b>topic sentence</b>, put it first, then put the other three in order. Clue: look for First / Then / Finally.</p>
  <div class="fym">{jig_html}</div>
</div>

<div class="page">
  <div class="band"><div><div class="k">Pairs · cut along the dashed line</div><h1>Paragraph Swap A/B</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.4pt">Each story is written with no paragraph breaks. Only the reader can see where they go (//). Listen for <b>TiPToP</b>: a new <b>Ti</b>me, <b>P</b>lace, <b>To</b>pic or <b>P</b>erson.</p>
  {story_card("A", STORY_A, STORY_B)}
  {story_card("B", STORY_B, STORY_A)}
</div>

<div class="page">
  <div class="poster">
    <h1>One paragraph, one idea</h1>
    <div class="ops">
      <div style="background:var(--green-soft)"><b>Topic sentence</b>the main idea<br>usually first</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Support</b>details · facts<br>examples · reasons</div>
      <div style="background:var(--green-soft)"><b>Link</b>sum up or lead<br>into the next one</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>TiPToP</b>new Time · Place<br>Topic · Person</div>
      <div style="background:var(--green-soft)"><b>Linking words</b>However · For example<br>As a result · In addition</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Show it</b>leave a line<br>or indent</div>
    </div>
    <p style="text-align:center;font-size:20pt!important;font-weight:800;margin:4mm 0">New Time, Place, Topic or Person? New paragraph.</p>
    <p style="text-align:center;font-size:10pt;color:var(--muted)">Léim · leim.ie · Play Paragraph Builder: {GAME}</p>
  </div>
</div>

<div class="page ws">
  <div class="band"><div><div class="k">Worksheet · exam-style questions</div><h1>Fix the Paragraph</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Fix the Paragraph</h2>
  <p>Each paragraph has one problem. Say what's wrong and how to fix it.</p>
  <table class="eh"><thead><tr><th>Paragraph</th><th>What's wrong and the fix</th></tr></thead><tbody>
  {"".join(f"<tr><td style='font-weight:500'>{s}</td><td><span class='gap'></span><span class='gap'></span></td></tr>" for s, r in FIX)}
  </tbody></table>
  <h2>B. Exam-style questions: "The Day the River Rose"</h2>
  <div class="pass">{" ".join(RIVER)}</div>
  <ol class="q">
    <li>This text should be four paragraphs. Write the first two words of each new paragraph and the TiPToP reason.<span class="long"></span><span class="long"></span></li>
    <li>Write a topic sentence that could start the whole story.<span class="long"></span></li>
    <li>Find a linking word in the text. What job does it do?<span class="long"></span></li>
    <li>Write the next paragraph. Start it with a new time.<span class="long"></span><span class="long"></span></li>
    <li>Write one paragraph arguing that every town needs a library. Use a topic sentence, support and a linking word.<span class="long"></span><span class="long"></span></li>
  </ol>
</div>

<div class="page an">
  <div class="band"><div><div class="k">For the teacher</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>Paragraph Jigsaw</h2>
  <ol class="q" style="font-size:9pt">{jig_key}</ol>
  <h2>Paragraph Swap</h2>
  <p>"{STORY_A[0]}": new paragraphs at "At midnight" (Time), "Down in the kitchen" (Place), "Ciara's dad" (Person). "{STORY_B[0]}": "Another reason", "On the other hand", "In addition" (all Topic: a new point).</p>
  <h2>A. Fix the Paragraph</h2>
  <table><tbody>{"".join(f"<tr><td style='width:42%'>{s}</td><td>{r}</td></tr>" for s, r in FIX)}</tbody></table>
  <h2>B. Exam-style questions</h2>
  <ol class="q">
    <li>"That night," (Time) · "Upstairs in" (Place) · "Mrs Daly" (Person).</li>
    <li>e.g. The summer our town flooded was the scariest week of my life.</li>
    <li>"As a result": it shows what happened because the water came over the bank (a result).</li>
    <li>Any paragraph that opens with a time phrase (e.g. "By morning, …" / "Two days later, …") and stays on one main idea.</li>
    <li>e.g. Every town needs a library. It gives everyone free books, films and computers. For example, students can print school projects there. As a result, it helps families who can't afford these things at home.</li>
  </ol>
  <h2>Marking tip</h2>
  <p>In students' own writing, credit a clear topic sentence, support that stays on the point and paragraphs that change at a sensible place. One idea per paragraph matters more than length.</p>
</div>
</body></html>"""

cover = """<!doctype html><html><head><meta charset="utf-8"><style>
body{margin:0;width:1200px;height:1200px;background:#1B2430;font-family:Inter,sans-serif;color:#fff;display:flex;flex-direction:column;justify-content:space-between;padding:90px;box-sizing:border-box}
.k{display:inline-block;background:#2E7D57;border-radius:99px;padding:12px 26px;font-weight:700;font-size:28px;letter-spacing:.06em;text-transform:uppercase}
h1{font-size:120px;font-weight:800;line-height:1.15;letter-spacing:-.02em;margin:60px 0 20px}
h1 span{background:#F6CF5A;color:#1B2430;padding:0 18px;border-radius:14px}
.sub{font-size:40px;line-height:1.4;color:#DDE3EA}
.em{font-size:52px;margin-top:30px;font-weight:800;letter-spacing:.01em;color:#F6CF5A}
.foot{display:flex;justify-content:space-between;align-items:center;font-size:34px;font-weight:700}
.price{background:#F6CF5A;color:#1B2430;border-radius:16px;padding:14px 28px}
</style></head><body>
<div><span class="k">Junior Cycle English · Teacher pack</span>
<h1><span>Paragraphs</span></h1>
<div class="sub">Paragraph Jigsaw cards · Paragraph Swap A/B<br>Poster · Worksheet + answers</div>
<div class="em">topic sentences · TiPToP<br>linking words</div></div>
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
    pdf("teacher-pack", os.path.join(OUT, "Paragraphs-Teacher-Pack-Leim.pdf"))
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--hide-scrollbars", "--window-size=1200,1200",
                    f"--screenshot={os.path.join(OUT, f'{SLUG}-cover.png')}", f"{SLUG}-cover.html"], cwd=SRC, check=True, capture_output=True)
