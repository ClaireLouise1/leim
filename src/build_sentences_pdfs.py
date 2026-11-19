#!/usr/bin/env python3
"""Sentences (JC English Order 2): free sheet (-> printables/), 6-page teacher pack + 1200x1200 cover (-> OUTDIR).
Usage: python3 src/build_sentences_pdfs.py /tmp/sent
Items come from the game's data block (sentence-surgeon.html) and every sentence / fragment / run-on / type / structure answer is re-checked
with spaCy via src/sentence_check.py (same checks as src/test_sentence_surgeon.py). Styles are read from src/build_money1_pdfs.py."""
import os, sys, random, subprocess, re, json
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC); sys.path.insert(0, SRC)
from sentence_check import kind, structure, stype
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/sent"; os.makedirs(OUT, exist_ok=True)
SLUG = "sentences"
LO = "W10, W11, W12"
GAME = "leim.ie/sentence-surgeon.html"
D = json.loads(open(os.path.join(ROOT, "sentence-surgeon.html"), encoding="utf-8").read().split("/*DATA*/")[1].split("/*END*/")[0])
NAME = {"sentence": "sentence", "fragment": "fragment", "runon": "run-on", "st": "statement", "qu": "question", "cm": "command", "ex": "exclamation",
        "si": "simple", "co": "compound", "cx": "complex"}
COORD = {"but", "so", "or", "and"}
def run_text(r, j=", "): a, b = r.split("|"); return a + j + b
def run_fixed(r): a, b = r.split("|"); return a + ". " + b[0].upper() + b[1:]
def is_run(r):
    a, b = r.split("|")
    return kind(a + ".") == "sentence" and kind(b[0].upper() + b[1:]) == "sentence" and kind(a + ", " + b) == "runon"
def join_full(s, w): return s.replace(" ___ ", (", " if w in COORD else " ") + w + " ")

# ---------- free sheet ----------
FRAGS = {f: k for f, k in D["frag"]}
A_items = [("The bus was late again.", "sentence"), ("Because the bus was late.", "fragment"), (run_text("It was raining|we stayed indoors."), "runon"),
           ("Running down the corridor.", "fragment"), ("When the bell rang, everyone rushed outside.", "sentence"), (run_text("The test was hard|we all passed it."), "runon"),
           ("The girl who won the race.", "fragment"), ("Nobody answered the phone.", "sentence"), (run_text("The sea was rough|the ferry was cancelled.", " "), "runon"),
           ("Although she was nervous, Aisling sang beautifully.", "sentence"), ("A huge crowd outside the stadium.", "fragment"), (run_text("We waited for hours|nobody came."), "runon")]
for s, k in A_items:
    if k == "runon":
        r = next(x for x in D["run"] if run_text(x) == s or run_text(x, " ") == s); assert is_run(r), s
    else:
        assert kind(s) == k, (s, kind(s)); assert s in D["sent"] or s in FRAGS, s
assert [k for s, k in A_items].count("runon") == 4 and [k for s, k in A_items].count("fragment") == 4
B_items = [(s, k) for k in ("st", "qu", "cm", "ex") for s in D["types"][k][:2]]
random.seed(22); random.shuffle(B_items)
for s, k in B_items: assert stype(s) == k, (s, k)
C_runs = ["Niamh missed the bus|she walked to school.", "Pizza is my favourite|my sister hates it.", "My phone died|nobody could ring me.",
          "The water was freezing|we swam anyway.", "The power went off|we lit candles.", "Dad burnt the toast|the smoke alarm went off."]
for r in C_runs: assert r in D["run"] and is_run(r), r
JB = [j for j in D["join"] if j[1] in ("but", "so", "because", "until", "if", "although")]
D_items = []
for w in ("but", "so", "because", "until", "if", "although"):
    it = next(j for j in JB if j[1] == w); D_items.append(it); assert kind(join_full(it[0], w)) == "sentence"
E_items = [("Ciara and Jack walked to school.", "si"), ("We knocked, but nobody answered.", "co"), ("If you hurry, you'll catch the train.", "cx"),
           ("The children laughed and shouted.", "si"), ("She smiled when she saw the cake.", "cx"), ("The wind howled, and the windows rattled.", "co")]
for s, k in E_items: assert s in D["struct"][k] and structure(s) == k and kind(s) == "sentence", s
F_items = ["After we left the cinema.", "Waiting for the bus in the rain.", "My best friend from primary school.", "The phone that I lost last week."]
F_models = ["After we left the cinema, we went for chips.", "We were waiting for the bus in the rain.", "My best friend from primary school moved to Cork.",
            "The phone that I lost last week turned up under my bed."]
for f, m in zip(F_items, F_models): assert kind(f) == "fragment" and kind(m) == "sentence", (f, m)
G1 = "The match started at three it was freezing. Our team scored first, the crowd went wild. Then the rain came."
G1_fix = ["The match started at three.", "It was freezing.", "Our team scored first.", "The crowd went wild.", "Then the rain came."]
for s in G1_fix: assert kind(s) == "sentence", s
assert kind("Our team scored first, the crowd went wild.") == "runon"
G2 = ["The bus broke down.", "We were late.", "We missed the show."]
G2_model = "Because the bus broke down, we were late and missed the show."
assert kind(G2_model) == "sentence" and structure(G2_model) == "cx"
NQ = len(A_items) + len(B_items) + len(C_runs) + len(D_items) + len(E_items) + len(F_items) + 2; assert NQ == 44, NQ
nA, nB, nC, nD, nE, nF = 1, 13, 21, 27, 33, 39

def qs(items): return "".join(f"<li>{q} <span class='line'></span></li>" for q in items)
def style(var):
    return re.search(var + r' = f"""<!doctype.*?<style>(.*?)</style>', open(os.path.join(SRC, "build_money1_pdfs.py"), encoding="utf-8").read(), re.S).group(1).replace("{LO}", LO).replace("{{", "{").replace("}}", "}").replace("JC Maths LOs (2018 spec)", "JC English LOs (2015 spec)")
SHEET_STYLE = style("sheet"); PACK_STYLE = style("pack")
assert "JC English LOs (2015 spec)" in SHEET_STYLE and "Single-teacher licence" in PACK_STYLE and "JC English LOs (2015 spec)" in PACK_STYLE
EXTRA = """.wk{line-height:1.45;border:1.5px solid var(--line);border-radius:8px;padding:2px 7px;margin:3px 0;font-size:9.4pt}.wk b.h{display:block}
table.st{border-collapse:collapse;margin:3px 0;font-size:9.4pt;width:100%}table.st td,table.st th{border:1px solid #C9D1DA;padding:2px 6px;text-align:left}
.bank{border:1.5px solid var(--line);border-radius:8px;padding:4px 10px;margin:4px 0;text-align:center;font-weight:700;word-spacing:9px}
.pass{border-left:4px solid var(--green);background:var(--mist);padding:5px 10px;margin:4px 0;font-style:italic}"""

sheet = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Sentences: rules and practice | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{SHEET_STYLE}
{EXTRA}
</style></head><body>
<div class="page tight">
  <div class="band"><div><div class="k">Junior Cycle English · Free revision sheet</div><h1>Sentences, fragments and run-ons</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2015 specification): {LO}. Play the game: <b>{GAME}</b></p>
  <div class="two">
   <div><h2>1. What a sentence needs</h2>
    <table class="st"><tbody>
     <tr><td><b>Who or what</b></td><td>the subject: <i>The bus, Ciara, We</i></td></tr>
     <tr><td><b>A verb</b></td><td>doing or being: <i>was, laughed, missed</i></td></tr>
     <tr><td><b>A complete thought</b></td><td>makes sense on its own; capital letter at the start, end mark at the end</td></tr></tbody></table>
    <h2>2. Fragments: half a sentence</h2>
    <div class="wk">Because the bus was late. → <b>Because the bus was late, we missed the film.</b><br>Running down the corridor. → <b>I was</b> running down the corridor.<br>The boy with the red scarf. → The boy with the red scarf <b>waved</b>.</div>
    <h2>3. Run-ons: two sentences jammed together</h2>
    <div class="wk">It was raining, we stayed in. ✗ (a comma can't hold two sentences)<br>→ It was raining<b>. W</b>e stayed in.<br>→ It was raining<b>, so</b> we stayed in.</div>
    <h2>4. Four types of sentence</h2>
    <table class="st"><tbody>
     <tr><td><b>Statement</b></td><td>gives information: <i>The shop opens at nine.</i></td></tr>
     <tr><td><b>Question</b></td><td>asks something: <i>Where is my jumper?</i></td></tr>
     <tr><td><b>Command</b></td><td>tells someone to do something: <i>Close the door.</i></td></tr>
     <tr><td><b>Exclamation</b></td><td>strong feeling: <i>What a goal! How cold it is!</i></td></tr></tbody></table></div>
   <div><h2>5. Simple, compound, complex</h2>
    <table class="st"><tbody>
     <tr><td><b>Simple</b></td><td>one clause: <i>Rain fell all night.</i> (Two names or two verbs can still be simple: <i>Ciara and Jack walked to school.</i>)</td></tr>
     <tr><td><b>Compound</b></td><td>two main clauses + and / but / so / or: <i>We knocked, but nobody answered.</i></td></tr>
     <tr><td><b>Complex</b></td><td>main clause + a because / when / if / although / until … clause: <i>We stayed in because it was raining.</i></td></tr></tbody></table>
    <h2>6. Joining words</h2>
    <div class="wk"><b>but</b> contrast · <b>so</b> result · <b>or</b> choice · <b>because</b> reason · <b>when / until / before / while</b> time · <b>if</b> condition · <b>although</b> surprise</div>
    <h2>7. Commas with joining words</h2>
    <div class="wk">Comma <b>before</b> and / but / so / or when they join two sentences: <i>I was tired, but I kept running.</i><br>"Because / when / if…" part first? Comma after it: <i>If you hurry, you'll catch the train.</i></div>
    <h2>8. Sentences for effect</h2>
    <p>Mix short and long sentences. A very short sentence after longer ones creates tension or shock: <i>Then the lights went out.</i> Writers sometimes use a fragment on purpose (<i>Too silent.</i>), but in your own answers use full sentences.</p>
    <div class="note"><b>Classic mistakes:</b> a comma between two sentences (comma splice) · starting a sentence with "Because…" and never finishing it · forgetting the question mark · a small letter after a full stop.</div></div>
  </div>
  <div class="tip"><b>Exam tip:</b> read your answer back in your head. Where your voice drops and you pause, you need a full stop, not a comma.</div>
</div>

<div class="page p2">
  <div class="band"><div><div class="k">Practice · {NQ} questions</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Sentence, fragment or run-on?</h2><ol class="q" style="columns:2;column-gap:8mm">{qs(s for s, k in A_items)}</ol>
  <h2>B. Statement, question, command or exclamation? Add the end mark.</h2><ol class="q" start="{nB}" style="columns:2;column-gap:8mm">{qs(s[:-1] for s, k in B_items)}</ol>
  <h2>C. Fix each run-on: write it as two sentences</h2><ol class="q" start="{nC}" style="columns:2;column-gap:8mm">{qs(run_text(r) for r in C_runs)}</ol>
  <h2>D. Fill the gap with a joining word</h2>
  <div class="bank">although &nbsp; because &nbsp; but &nbsp; if &nbsp; so &nbsp; until</div>
  <ol class="q" start="{nD}" style="columns:2;column-gap:8mm">{qs(s.replace("___", "_______") for s, a, w in D_items)}</ol>
  <h2>E. Simple, compound or complex?</h2><ol class="q" start="{nE}" style="columns:2;column-gap:8mm">{qs(s for s, k in E_items)}</ol>
  <h2>F. Turn each fragment into a full sentence</h2><ol class="q" start="{nF}" style="columns:2;column-gap:8mm">{qs(F_items)}</ol>
  <h2>G. Exam-style</h2>
  <ol class="q" start="{NQ - 1}">
   <li>Correct the punctuation: "{G1}"<span class="long"></span><span class="long"></span></li>
   <li>Join into one good sentence: "{' '.join(G2)}"<span class="long"></span></li>
  </ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">Check your work</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <table class="ans"><tbody>
   <tr><td><b>A</b></td><td>{" · ".join(f"{i}. {NAME[k]}" for i, (s, k) in enumerate(A_items, nA))}</td></tr>
   <tr><td><b>B</b></td><td>{" · ".join(f"{i}. {NAME[k]} {s[-1]}" for i, (s, k) in enumerate(B_items, nB))}</td></tr>
   <tr><td><b>C</b></td><td>{" · ".join(f"{i}. {run_fixed(r)}" for i, r in enumerate(C_runs, nC))}<br>(A comma + and / but / so is also right, e.g. Niamh missed the bus, so she walked to school.)</td></tr>
   <tr><td><b>D</b></td><td>{" · ".join(f"{i}. {a}" for i, (s, a, w) in enumerate(D_items, nD))}</td></tr>
   <tr><td><b>E</b></td><td>{" · ".join(f"{i}. {NAME[k]}" for i, (s, k) in enumerate(E_items, nE))}</td></tr>
   <tr><td><b>F</b></td><td>Any full sentence that finishes the thought, e.g. {" · ".join(f"{i}. {m}" for i, m in enumerate(F_models, nF))}</td></tr>
   <tr><td><b>G</b></td><td>{NQ - 1}. {" ".join(G1_fix)} (Or: Our team scored first, <b>and</b> the crowd went wild.)<br>{NQ}. e.g. {G2_model}</td></tr>
  </tbody></table>
  <h2>Worked examples</h2>
  <div class="two">
   <div class="wk"><b class="h">2. Because the bus was late.</b>Because… then what happened? There's no main part, so it's a <b>fragment</b>. Fix: Because the bus was late, we missed the film.</div>
   <div class="wk"><b class="h">5. When the bell rang, everyone rushed outside.</b>"When the bell rang" can't stand alone, but it's joined to a main part (everyone rushed outside), so it's a <b>sentence</b>.</div>
   <div class="wk"><b class="h">{nE + 3}. The children laughed and shouted.</b>Two verbs, but one subject doing both: one clause, so <b>simple</b>.</div>
   <div class="wk"><b class="h">{nE + 1}. We knocked, but nobody answered.</b>Two main clauses (we knocked / nobody answered) joined by "but": <b>compound</b>.</div>
  </div>
  <div class="note"><b>Got one wrong?</b> Ask: who did what? Is the thought finished? Then play <b>Sentence Surgeon</b> at {GAME}: the "Go back over these" list at the end shows the reason for each mistake.</div>
  <p class="small">All sentences written by Léim. Léim is independent and not connected with the State Examinations Commission or the NCCA.</p>
</div>
</body></html>"""
assert E_items[3][0].startswith("The children") and E_items[1][1] == "co" and A_items[1][1] == "fragment" and A_items[4][1] == "sentence"

# ---------- teacher pack ----------
SORT = [s for s in ["Ciara laughed.", "We missed the start of the match.", "Because it was raining, we stayed indoors.", "My granny grows tomatoes in her greenhouse.",
        "After the concert, we walked home.", "The kettle is boiling.", "Oisín forgot his lunch, so he borrowed a sandwich.", "Seán and Maeve built a sandcastle."]]
SORT_F = ["When the match finished.", "If you finish your homework.", "Lots of rain and wind.", "The boy with the red scarf.", "Laughing at the joke.",
          "Sitting by the fire with a book.", "While Dad was cooking dinner.", "A cold, wet Monday morning."]
SORT_R = ["The film was long|we enjoyed it.", "The shop was closed|we went home.", "Tom studied all week|he still felt nervous.", "The dog loves walks|the cat hates them.",
          "It was very late|the shops were still open.", "Emma practised every day|she won the competition.", "The whistle blew|the players shook hands.", "Mam lost her key|we climbed in the window."]
for s in SORT: assert s in D["sent"] and kind(s) == "sentence", s
for s in SORT_F: assert s in FRAGS and kind(s) == "fragment", s
for r in SORT_R: assert r in D["run"] and is_run(r), r
cards = [(s, "S") for s in SORT] + [(s, "F") for s in SORT_F] + [(run_text(r, ", " if i % 2 == 0 else " "), "R") for i, r in enumerate(SORT_R)]
random.seed(2002); random.shuffle(cards)
sort_html = "".join(f'<div class="c"><span class="tag">Card {k}</span><div class="fc">{s}</div></div>' for k, (s, t) in enumerate(cards, 1))
sort_key = {t: ", ".join(str(k) for k, (s, x) in enumerate(cards, 1) if x == t) for t in "SFR"}

# Fix the Story relay: 6 cards, 2 mistakes each (run-on / fragment / end mark). Fixed sentences are all parser-checked.
STORY = [("My birthday started badly. I woke up late, my alarm hadn't gone off. Rushing down the stairs.",
          ["My birthday started badly.", "I woke up late.", "My alarm hadn't gone off.", "I came rushing down the stairs."], "run-on (late, my) · fragment (Rushing…)"),
         ("Mam was in the kitchen she was making pancakes. Because it was my birthday.",
          ["Mam was in the kitchen.", "She was making pancakes because it was my birthday."], "run-on (kitchen she) · fragment (Because…)"),
         ("After breakfast, I looked for my phone. It wasn't in my room, it wasn't in my bag. The phone that Gran gave me.",
          ["After breakfast, I looked for my phone.", "It wasn't in my room.", "It wasn't in my bag.", "I had lost the phone that Gran gave me."], "run-on (room, it) · fragment (The phone that…)"),
         ("I searched the whole house nobody had seen it. My little brother grinning in the corner.",
          ["I searched the whole house.", "Nobody had seen it.", "My little brother was grinning in the corner."], "run-on (house nobody) · fragment (…grinning)"),
         ("“Where is it.” I asked him. He just laughed, he pointed at the fridge.",
          ["“Where is it?” I asked him.", "He just laughed.", "He pointed at the fridge."], "end mark (it? not it.) · run-on (laughed, he)"),
         ("My phone was in the fridge, next to the butter. What a strange birthday. Although it ended well.",
          ["My phone was in the fridge, next to the butter.", "What a strange birthday!", "It was a strange birthday, although it ended well."], "end mark (birthday!) · fragment (Although…)")]
for wrong, fixed, note in STORY:
    for s in fixed:
        if s.startswith("“"): continue
        if s.endswith("!"): assert stype(s) == "ex", s; continue
        assert kind(s) == "sentence", s
assert kind("I woke up late, my alarm hadn't gone off.") == "runon" and kind("Rushing down the stairs.") == "fragment"
assert kind("Because it was my birthday.") == "fragment" and kind("The phone that Gran gave me.") == "fragment"
assert kind("My little brother grinning in the corner.") == "fragment" and kind("He just laughed, he pointed at the fridge.") == "runon"
assert kind("Although it ended well.") == "fragment" and stype("What a strange birthday!") == "ex" and kind("It wasn't in my room, it wasn't in my bag.") == "runon"
relay_html = "".join(f'<div class="idc"><h3>Card {k} of 6 · "The Lost Phone"</h3><p style="font-size:11pt;line-height:1.55;margin:1mm 0">{w}</p><p style="font-size:8.4pt;color:var(--muted);margin:0">Find 2 mistakes. Write the fixed version on your group\'s sheet, then pass the card on.</p></div>' for k, (w, f, n) in enumerate(STORY, 1))
relay_key = "".join(f"<li>{' '.join(f)} <span style='color:var(--muted)'>({n})</span></li>" for w, f, n in STORY)

ERR = [("It was late, we went home.", "Comma splice (run-on): It was late<b>. W</b>e went home. / It was late<b>, so</b> we went home."),
       ("Because I was tired.", "Fragment: add a main part. I went to bed early <b>because I was tired.</b>"),
       ("Are you coming to the party.", "It's a question: Are you coming to the party<b>?</b>"),
       ("The rain stopped. we went outside.", "Capital letter after a full stop: <b>We</b> went outside."),
       ("My brother plays the drums he is very loud.", "Run-on: My brother plays the drums<b>. H</b>e is very loud."),
       ("Sitting on the bus for two hours.", "Fragment (no helper verb): <b>We were</b> sitting on the bus for two hours.")]
assert kind("It was late, we went home.") == "runon" and kind("Because I was tired.") == "fragment" and stype("Are you coming to the party?") == "qu"
assert kind("My brother plays the drums. ") == "sentence" and kind("He is very loud.") == "sentence" and kind("Sitting on the bus for two hours.") == "fragment"
assert kind("We were sitting on the bus for two hours.") == "sentence" and kind("I went to bed early because I was tired.") == "sentence"
WS_PASS = "Night fell. The wind rose, rattling the windows and howling down the chimney as if it wanted to get in. Ellen lay awake. Something was moving downstairs."
WS_J = "The referee blew the final whistle. The fans ran onto the pitch."
WS_J_MODEL = "When the referee blew the final whistle, the fans ran onto the pitch."
assert structure(WS_J_MODEL) == "cx" and kind(WS_J_MODEL) == "sentence" and structure("Ciara and Jack walked to school.") == "si"
for s in ["Night fell.", "Ellen lay awake.", "Something was moving downstairs."]: assert kind(s) == "sentence", s

pack = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Sentences Teacher Pack | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{PACK_STYLE}
{EXTRA}
.fym .c{{height:24mm}}.fym .fc{{font-size:10.4pt;line-height:1.28;margin-top:2.5mm}}.idc{{padding:2mm 4mm;margin-bottom:2.5mm}}.idc h3{{margin:0 0 1mm}}
.p1 .proc td{{font-size:8.6pt;padding:2px 6px}}.ops div{{font-size:12pt;padding:4mm 3mm}}.ops b{{font-size:18pt}}.pass{{font-size:10pt}}
</style></head><body>

<div class="page p1">
  <div class="band"><div><div class="k">Junior Cycle English · Teacher pack</div><h1>Sentences, fragments and run-ons</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2015 specification): {LO}</p>
  <div class="two">
    <div><h3>Aims</h3><p>By the end of the lesson students can tell a complete sentence from a fragment or a run-on, fix comma splices and fragments in their own writing, name the four sentence types, join ideas with the right joining word, and say whether a sentence is simple, compound or complex.</p></div>
    <div><h3>In this pack</h3><p>p.1 Teacher notes · p.2 Sentence Sort cards (cut-up) · p.3 Fix the Story relay cards · p.4 Wall poster · p.5 Worksheet: Error Hunt + exam-style questions · p.6 Answers. Level: 1st year (useful revision in 2nd and 3rd). Time: about 60 minutes. All sentences are original.</p></div>
  </div>
  <h2 style="margin-top:8px">Procedure</h2>
  <table class="proc"><tbody>
    <tr><td>5 min</td><td><b>Lead-in.</b> Read aloud: "The bus was late." / "Because the bus was late." / "The bus was late we missed the film." Which one sounds finished? Elicit: who + verb + a complete thought.</td></tr>
    <tr><td>8 min</td><td><b>Guided discovery.</b> Pairs: what's missing from the second? What's too much in the third? Board the words <b>fragment</b> and <b>run-on</b> and the two fixes (full stop + capital, or comma + and / but / so). Then the four sentence types.</td></tr>
    <tr><td>12 min</td><td><b>Sentence Sort</b> (p.2, groups of 3–4, one set of 24 cards). Sort into three piles: sentence, fragment, run-on. Then each group fixes two fragments and two run-ons on mini-whiteboards. Feedback: why is card "Because it was raining, we stayed indoors." a sentence?</td></tr>
    <tr><td>15 min</td><td><b>Fix the Story relay</b> (p.3, groups). Each group gets one card, finds the 2 mistakes and writes the fixed lines on a group sheet, then passes the card on (2 min per card). At the end, groups read the whole story in order and compare fixes.</td></tr>
    <tr><td>15 min</td><td><b>Worksheet</b> (p.5). Error Hunt in pairs (find it, say what's wrong, fix it), then the exam-style questions alone.</td></tr>
    <tr><td>5 min</td><td><b>Exit ticket.</b> Write one sentence of each type about your weekend, and one complex sentence starting with "When". Homework: play <b>Sentence Surgeon</b> at {GAME}.</td></tr>
  </tbody></table>
  <div class="note"><b>Sort key:</b> sentences: cards {sort_key["S"]} · fragments: cards {sort_key["F"]} · run-ons: cards {sort_key["R"]}.<br>
  <b>Errors to look for:</b> comma splices ("It was late, we went home") · "Because…" sentences that never finish · thinking a long sentence must be a run-on (length isn't the test: two sentences with no joining word is) · thinking "Ciara and Jack walked to school" is compound (two names, one clause: simple). <b>Support:</b> the poster (p.4) on the desk. <b>Fast finishers:</b> rewrite the Lost Phone story with one short sentence for effect.</div>
  <p class="small"><b>Relay answers</b> (any correct fix is fine; a comma + and / but / so also fixes a run-on):</p>
  <ol class="small" style="font-size:7.6pt;line-height:1.25;margin:0;padding-left:16px">{relay_key}</ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">Groups of 3–4 · cut up the 24 cards</div><h1>Sentence Sort</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.4pt;margin:0 0 2mm">Sort the cards into three piles: <b>sentence</b> (complete), <b>fragment</b> (half a sentence) and <b>run-on</b> (two sentences jammed together). Then fix two fragments and two run-ons.</p>
  <div class="fym">{sort_html}</div>
</div>

<div class="page">
  <div class="band"><div><div class="k">Groups · one card each, then pass it on</div><h1>Fix the Story relay</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.4pt">Each card is one part of the story "The Lost Phone". Each card has <b>2 mistakes</b>: a run-on, a fragment or a wrong end mark. Find them, write the fixed version, then pass the card on. Finished? Read the whole story in order (cards 1–6).</p>
  {relay_html}
</div>

<div class="page">
  <div class="poster">
    <h1>Is it a sentence?</h1>
    <div class="ops">
      <div style="background:var(--green-soft)"><b>Sentence</b>who + verb + complete thought<br><i>The bus was late.</i></div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Fragment</b>half a sentence<br><i>Because the bus was late.</i></div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Run-on</b>two jammed together<br><i>It was late, we left.</i></div>
      <div style="background:var(--green-soft)"><b>Fix a run-on</b>full stop + capital<br>or , and / but / so</div>
      <div style="background:var(--green-soft)"><b>4 types</b>statement . · question ?<br>command . · exclamation !</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Join it</b>but · so · because<br>when · if · although</div>
    </div>
    <p style="text-align:center;font-size:20pt!important;font-weight:800;margin:4mm 0">A comma can't hold two sentences.</p>
    <p style="text-align:center;font-size:10pt;color:var(--muted)">Léim · leim.ie · Play Sentence Surgeon: {GAME}</p>
  </div>
</div>

<div class="page ws">
  <div class="band"><div><div class="k">Worksheet</div><h1>Error Hunt + exam-style questions</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Error Hunt</h2>
  <p>Each line has one mistake. Say what's wrong and write it correctly.</p>
  <table class="eh"><thead><tr><th>Sentence</th><th>What's wrong and the fix</th></tr></thead><tbody>
  {"".join(f"<tr><td>{s}</td><td><span class='gap'></span><span class='gap'></span></td></tr>" for s, r in ERR)}
  </tbody></table>
  <h2>B. Exam-style questions</h2>
  <div class="pass">{WS_PASS}</div>
  <ol class="q">
    <li>How does the writer use sentence length to build tension? Refer to the text.<span class="long"></span><span class="long"></span></li>
    <li>Write one statement, one question, one command and one exclamation about a school tour.<span class="long"></span><span class="long"></span></li>
    <li>Join into one complex sentence starting with "When": "{WS_J}"<span class="long"></span></li>
    <li>"Ciara and Jack walked to school." Simple or compound? Explain.<span class="long"></span></li>
    <li>Write a short paragraph (3–4 sentences) about a storm. Use at least one very short sentence for effect.<span class="long"></span><span class="long"></span></li>
  </ol>
</div>

<div class="page an">
  <div class="band"><div><div class="k">For the teacher</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>Sentence Sort</h2>
  <p>Sentences: cards {sort_key["S"]} · Fragments: cards {sort_key["F"]} · Run-ons: cards {sort_key["R"]}. Watch for "Because it was raining, we stayed indoors." and "Oisín forgot his lunch, so he borrowed a sandwich.": both are complete sentences.</p>
  <h2>Fix the Story relay</h2>
  <ol class="q" style="font-size:9pt">{relay_key}</ol>
  <h2>A. Error Hunt</h2>
  <table><tbody>{"".join(f"<tr><td style='width:38%'>{s}</td><td>{r}</td></tr>" for s, r in ERR)}</tbody></table>
  <h2>B. Exam-style questions</h2>
  <ol class="q">
    <li>e.g. Very short sentences ("Night fell." "Ellen lay awake.") slow us down and feel tense. The long middle sentence lets the wind build up. The last short sentence, "Something was moving downstairs.", is a shock that leaves us waiting. (Credit: point about length + quote + effect.)</li>
    <li>e.g. The bus leaves at eight. Where are we stopping for lunch? Bring a packed lunch. What a brilliant day!</li>
    <li>{WS_J_MODEL}</li>
    <li>Simple: there are two names, but one clause (one verb: walked).</li>
    <li>Any paragraph of correct sentences with at least one short sentence used for tension or surprise.</li>
  </ol>
  <h2>Marking tip</h2>
  <p>In students' own writing, comma splices and fragments are the most common accuracy slips. In questions on a writer's style, credit a clear point about sentence length or type, a short quote and the effect on the reader.</p>
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
<h1><span>Sentences</span></h1>
<div class="sub">Sentence Sort cards · Fix the Story relay<br>Poster · Worksheet + answers</div>
<div class="em">fragments · run-ons · 4 types</div></div>
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
    pdf("teacher-pack", os.path.join(OUT, "Sentences-Teacher-Pack-Leim.pdf"))
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--hide-scrollbars", "--window-size=1200,1200",
                    f"--screenshot={os.path.join(OUT, f'{SLUG}-cover.png')}", f"{SLUG}-cover.html"], cwd=SRC, check=True, capture_output=True)
