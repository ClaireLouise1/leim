#!/usr/bin/env python3
"""Speaking & listening: talking to a group (JC English Order 10): free sheet (-> printables/), 6-page teacher pack + 1200x1200 cover (-> OUTDIR).
Usage: python3 src/build_speaking_pdfs.py /tmp/speaking
Items come from the game's data block (talk-tips.html). Every answer is re-derived with the checker's own rules
(src/test_talk_tips.py: tip, hook_types, weak_marks, sign, good_reply, disc) and asserted.
Styles are read from src/build_money1_pdfs.py."""
import os, sys, random, subprocess, re
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC); sys.path.insert(0, SRC)
from test_talk_tips import tip, hook_types, weak_marks, sign, good_reply, disc, shares, load
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/speaking"; os.makedirs(OUT, exist_ok=True)
SLUG = "speaking-listening"
LO = "OL1, OL2, OL3, OL4, OL5, OL6, OL7"
GAME = "leim.ie/talk-tips.html"
D = load(os.path.join(ROOT, "talk-tips.html"))
HN = {"q": "Question", "f": "Fact", "s": "Story"}; SN = {"s": "Start", "m": "Next point", "e": "End"}
DN = {"ag": "Agree", "di": "Disagree politely", "jo": "Join in", "as": "Ask for more"}
def one(f, s):
    r = f(s); assert len(r) == 1, (s, r); return list(r)[0]

# ---------- free sheet ----------
random.seed(1010)
A_items = random.sample([x for x in D["tips"] if x[0] == "do"], 3) + random.sample([x for x in D["tips"] if x[0] == "avoid"], 3)
random.shuffle(A_items)
for k, s in A_items: assert one(tip, s) == k
B_items = []
for k in ("q", "f", "s", "f"):
    B_items.append(random.choice([o for o in D["open"] if one(hook_types, o[2]) == k and o not in B_items]))
random.shuffle(B_items)
C_items = random.sample(D["sign"], 5)
for s, k in C_items: assert one(sign, s) == k
D_items = random.sample(D["listen"], 3); D_opts = []
for f, g, bad in D_items:
    o = [g] + bad; random.shuffle(o); D_opts.append(o)
    assert [x for x in o if good_reply(f, x)] == [g]
E_items = []
for k in ("as", "di", "jo", "ag", "di"):
    E_items.append(random.choice([x for x in D["discuss"] if x[1] == k and x not in E_items]))
for s, k in E_items: assert one(disc, s) == k
NQ = len(A_items) + len(B_items) + len(C_items) + len(D_items) + len(E_items) + 2; assert NQ == 25, NQ
nA = 1; nB = nA + len(A_items); nC = nB + len(B_items); nE = nC + len(C_items); nD = nE + len(E_items); nF = nD + len(D_items)  # D on the sheet = discussion (E_items), E = listening (D_items)

def style(var):
    return re.search(var + r' = f"""<!doctype.*?<style>(.*?)</style>', open(os.path.join(SRC, "build_money1_pdfs.py"), encoding="utf-8").read(), re.S).group(1).replace("{LO}", LO).replace("{{", "{").replace("}}", "}").replace("JC Maths LOs (2018 spec)", "JC English LOs (2015 spec)")
SHEET_STYLE = style("sheet"); PACK_STYLE = style("pack")
assert "JC English LOs (2015 spec)" in SHEET_STYLE and "Single-teacher licence" in PACK_STYLE and "JC English LOs (2015 spec)" in PACK_STYLE
EXTRA = """.wk{line-height:1.45;border:1.5px solid var(--line);border-radius:8px;padding:2px 7px;margin:3px 0;font-size:9.4pt}.wk b.h{display:block}
table.st{border-collapse:collapse;margin:3px 0;font-size:9.2pt;width:100%}table.st td,table.st th{border:1px solid #C9D1DA;padding:2px 6px;text-align:left}
.bank{border:1.5px solid var(--line);border-radius:8px;padding:4px 10px;margin:4px 0;text-align:center;font-weight:700;word-spacing:4px}
.pass{border-left:4px solid var(--green);background:var(--mist);padding:5px 10px;margin:4px 0;font-style:italic}"""
A_html = "".join(f"<li value='{i}'>{s} &nbsp; <b>Do it / Avoid it</b></li>" for i, (k, s) in enumerate(A_items, nA))
B_html = "".join(f"<li value='{i}'><i>{h}</i> <span class='line' style='min-width:18mm'></span></li>" for i, (t, e, h) in enumerate(B_items, nB))
C_html = "".join(f"<li value='{i}'><i>{s}</i> &nbsp; <b>Start / Next / End</b></li>" for i, (s, k) in enumerate(C_items, nC))
D_html = "".join(f"<li value='{i}'>Your friend says: <i>“{f}”</i><br>{' &nbsp;/&nbsp; '.join(o)}</li>" for i, ((f, g, b), o) in enumerate(zip(D_items, D_opts), nD))
E_html = "".join(f"<li value='{i}'><i>“{s}”</i> <span class='line' style='min-width:22mm'></span></li>" for i, (s, k) in enumerate(E_items, nE))
EX_TOPIC = "a person I admire"

sheet = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Speaking and listening, rules and practice | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{SHEET_STYLE}
{EXTRA}
.p2 ol.q li{{margin-bottom:1px;font-size:9pt}}.p2 h2{{margin:4px 0 2px}}.p2 .two{{gap:5mm}}
</style></head><body>
<div class="page tight">
  <div class="band"><div><div class="k">Junior Cycle English · Free revision sheet</div><h1>Speaking and listening</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2015 specification): {LO}. Play the game: <b>{GAME}</b></p>
  <div class="two">
   <div><h2>1. Talking to a group</h2>
    <table class="st"><thead><tr><th></th><th>Do it</th><th>Avoid it</th></tr></thead><tbody>
     <tr><td><b>Eyes</b></td><td>look up, around the room</td><td>stare at the floor or the page</td></tr>
     <tr><td><b>Voice</b></td><td>loud enough for the back row; stress key words</td><td>mumble; one flat voice</td></tr>
     <tr><td><b>Pace</b></td><td>slow down; pause</td><td>rush; "em" and "like"</td></tr>
     <tr><td><b>Body</b></td><td>stand straight, feet still</td><td>fidget, sway, turn your back</td></tr>
     <tr><td><b>Notes</b></td><td>cue cards with key words</td><td>read every word</td></tr></tbody></table>
    <h2>2. Plan your talk</h2>
    <div class="wk"><b>Hook</b> (first line): a <b>question</b> to the audience, a surprising <b>fact</b> or number, or a short <b>story</b> from your life. Never "Today I'm going to talk about…".<br>
    <b>Plan:</b> tell them how many points (<i>three reasons…</i>). <b>End strongly:</b> sum up and leave one last thought.</div>
    <table class="st"><tbody>
     <tr><td><b>Start</b></td><td>First of all · To begin with · Firstly</td></tr>
     <tr><td><b>Next point</b></td><td>Moving on · Secondly · Another reason · On top of that</td></tr>
     <tr><td><b>End</b></td><td>To sum up · In conclusion · To finish · All in all</td></tr></tbody></table></div>
   <div><h2>3. Listening well</h2>
    <div class="wk">Nod, let them finish, then reply to what <b>they</b> said: ask a question about it.<br>
    <i>“I went to Paris.”</i> → <b>What was your favourite part of Paris?</b><br>
    Not: changing the subject · talking about yourself · putting them down.</div>
    <h2>4. Discussing in a group</h2>
    <table class="st"><tbody>
     <tr><td><b>Agree</b></td><td>That's a great point. · I agree with…</td></tr>
     <tr><td><b>Disagree politely</b></td><td>I see what you mean, but… · With respect, I disagree.</td></tr>
     <tr><td><b>Join in</b></td><td>Can I come in here? · Could I say something?</td></tr>
     <tr><td><b>Ask for more</b></td><td>Can you give us an example? · Why do you think that?</td></tr></tbody></table>
    <div class="note"><b>Classic mistakes:</b> reading a script word for word · no hook · no signposts, so listeners get lost · "That's it, thanks" as an ending · interrupting · "That's stupid" instead of a polite disagreement.</div></div>
  </div>
  <div class="tip"><b>Exam tip:</b> in the written paper you may have to <b>write a talk</b>. Use the same tools: a hook, "you" and "we" to speak to the audience, signposts for each point, and a strong ending.</div>
</div>

<div class="page p2">
  <div class="band"><div><div class="k">Practice · {NQ} questions</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <div class="two"><div><h2>A. Good habit? Circle Do it or Avoid it</h2><ol class="q">{A_html}</ol>
  <h2>B. Which kind of hook? (question, fact, story)</h2><ol class="q">{B_html}</ol></div>
  <div><h2>C. Where in the talk? Circle one</h2><ol class="q">{C_html}</ol>
  <h2>D. What is it for?</h2><div class="bank" style="font-size:8.4pt">{" · ".join(DN.values())}</div><ol class="q">{E_html}</ol></div></div>
  <h2>E. Listen well: circle the best reply</h2><ol class="q">{D_html}</ol>
  <h2>F. Exam-style</h2>
  <ol class="q">
   <li value="{nF}">Write the opening two sentences of a talk to your class on <b>"{EX_TOPIC}"</b>. Start with a hook.<span class="long"></span><span class="long"></span></li>
   <li value="{nF + 1}">In a class discussion, someone says: <b>"Phones should be allowed in class."</b> Disagree politely and give one reason.<span class="long"></span><span class="long"></span></li>
  </ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">Check your work</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <table class="ans"><tbody>
   <tr><td><b>A</b></td><td>{" · ".join(f"{i}. {'Do it' if k == 'do' else 'Avoid it'}" for i, (k, s) in enumerate(A_items, nA))}</td></tr>
   <tr><td><b>B</b></td><td>{" · ".join(f"{i}. {HN[one(hook_types, h)]}" for i, (t, e, h) in enumerate(B_items, nB))}</td></tr>
   <tr><td><b>C</b></td><td>{" · ".join(f"{i}. {SN[k]}" for i, (s, k) in enumerate(C_items, nC))}</td></tr>
   <tr><td><b>D</b></td><td>{" · ".join(f"{i}. {DN[k]}" for i, (s, k) in enumerate(E_items, nE))}</td></tr>
   <tr><td><b>E</b></td><td>{" · ".join(f"{i}. {g}" for i, (f, g, b) in enumerate(D_items, nD))}<br>(Each one asks about what your friend just said.)</td></tr>
   <tr><td><b>F</b></td><td>{nF}. Sample: <i>When I was eight, my grandad taught me to fish off the pier in Kinsale, and he never once lost his temper. Today I'll tell you three reasons why he is the person I admire most.</i> (A story hook, then a plan.)<br>
     {nF + 1}. Sample: <i>I see what you mean, because phones can be useful for looking things up, but I'm not so sure. They make it very hard to concentrate when messages keep coming in.</i></td></tr>
  </tbody></table>
  <h2>Worked examples</h2>
  <div class="two">
   <div class="wk"><b class="h">Writing a hook</b>Topic: recycling. Question: <i>What happens to your crisp packet after the bin?</i> Fact: <i>A plastic bottle can take hundreds of years to break down.</i> Story: <i>Last summer, I found a plastic bag on Inch beach.</i></div>
   <div class="wk"><b class="h">Planning with signposts</b>Hook → "three reasons" → <b>First of all</b> … → <b>Moving on</b> … → <b>Another reason</b> … → <b>To sum up</b> … → one last thought.</div>
   <div class="wk"><b class="h">A good listening reply</b>Pick a word they used and ask about it: <i>“My team won the final.”</i> → <i>Who scored in the <b>final</b>?</i></div>
   <div class="wk"><b class="h">Disagreeing politely</b>Show you heard them (<i>I see what you mean…</i>), then <i>but</i> + your reason. Never "That's stupid".</div>
  </div>
  <div class="note"><b>Got one wrong?</b> Go back to page 1, then play <b>Talk Tips</b> at {GAME}: the "Go back over these" list at the end explains each mistake.</div>
  <p class="small">All sentences and passages written by Léim. Léim is independent and not connected with the State Examinations Commission or the NCCA.</p>
</div>
</body></html>"""

# ---------- teacher pack ----------
EXTRA_DISC = [("I agree completely.", "ag"), ("You're right, that's true.", "ag"), ("That's true, but I think it's too late.", "di"),
              ("I'm not so sure about that.", "di"), ("Could I just add something?", "jo"), ("Can I say one thing here?", "jo"),
              ("What makes you think that?", "as")]
SORT = []
for k in DN:
    L = [x for x in D["discuss"] + EXTRA_DISC if x[1] == k]; random.seed(1000 + len(SORT)); SORT += random.sample(L, 6)
for s, k in SORT: assert one(disc, s) == k
assert len(SORT) == 24 and len({s for s, k in SORT}) == 24
random.seed(1011); random.shuffle(SORT)
sort_html = "".join(f'<div class="c"><span class="tag">Card {i}</span><div class="fc sm">{s}</div></div>' for i, (s, k) in enumerate(SORT, 1))
sort_key = " · ".join(f"<b>{DN[k]}</b>: " + ", ".join(str(i) for i, x in enumerate(SORT, 1) if x[1] == k) for k in DN)

TALK_A = ("Why every teenager should learn to cook", [
    "Who here can cook a proper dinner?", "Today I'll give you three reasons to learn.",
    "First of all, cooking saves money: a homemade pizza costs far less than a takeaway.",
    "Secondly, it's healthier, because you know exactly what goes in.",
    "Another reason is that it's a skill for life, because one day you'll live on your own.",
    "To sum up, grab an apron and ask to help with dinner this week."])
TALK_B = ("Why dogs make the best pets", [
    "Dogs have been living with people for over 15,000 years.", "Today I'll tell you three reasons why they make the best pets.",
    "To begin with, a dog is loyal and is always happy to see you.",
    "Moving on, a dog gets you outside for a walk every single day.",
    "On top of that, looking after a dog teaches you to be responsible.",
    "To sum up, if you want a friend for life, get a dog."])
TALK_KEY = {}
for name, L in (TALK_A, TALK_B):
    h = one(hook_types, L[0]); assert not weak_marks(" ".join(L))
    seq = [one(sign, s) for s in L[2:]]; assert seq == ["s", "m", "m", "e"], (name, seq)
    assert not sign(L[0]) and not sign(L[1])
    TALK_KEY[name] = (h, [s.split(",")[0] for s in L[2:]])
assert TALK_KEY[TALK_A[0]][0] == "q" and TALK_KEY[TALK_B[0]][0] == "f"
def swap_card(who, mine, theirs):
    name, L = mine
    return f"""<div class="idc"><h3>Student {who} · Talk Swap</h3>
    <p style="font-size:8.6pt;margin:0 0 1mm"><b>1. Give your one-minute talk.</b> Read it through twice to yourself, then say it to your partner. Look up at least once per sentence.</p>
    <div class="pass" style="font-size:10pt"><b style="font-style:normal">"{name}"</b><br>{" ".join(L)}</div>
    <p style="font-size:8.6pt;margin:1mm 0"><b>2. Then listen</b> to "{theirs[0]}" without looking at the text. Fill in the grid:</p>
    <table class="st" style="font-size:8.6pt"><tbody>{"".join(f"<tr><td style='width:34%'><b>{n}</b></td><td></td></tr>" for n in ["Hook: question, fact or story?", "Start signpost", "Next-point signposts", "End signpost", "The three points", "One question to ask the speaker"])}</tbody></table>
    <p style="font-size:8.6pt;margin:1mm 0 0"><b>3. Ask your question.</b> Then give one tip: eyes, voice, pace or body.</p></div>"""

FIX = [("“Today I'm going to talk about sharks.”", "No hook. Start with a fact or a question: <b>Sharks were here before the dinosaurs.</b>"),
       ("“Em, so, like, sharks are, like, fish.”", "Fillers. Pause instead of “em” and “like”."),
       ("Reads the whole talk from a page, head down.", "No eye contact. Use cue cards with key words and look up."),
       ("“That's it. Thanks.”", "Weak ending. Sum up and leave one last thought: <b>To sum up, sharks need our protection, not our fear.</b>"),
       ("Friend: “I got a puppy!” Reply: “I want a new phone.”", "Changes the subject. Ask about it: <b>What did you call your puppy?</b>"),
       ("“That's a stupid idea.”", "Rude. Disagree politely: <b>I see what you mean, but I'm not so sure.</b>")]
assert weak_marks("Today I'm going to talk about sharks.") and weak_marks("Em, so, like, sharks are, like, fish.")
assert good_reply("I got a puppy!", "What did you call your puppy?") and not good_reply("I got a puppy!", "I want a new phone.")
assert one(disc, "I see what you mean, but I'm not so sure.") == "di" and one(sign, "To sum up, sharks need our protection, not our fear.") == "e"

SKATE = ["Last summer, my friends and I were moved on from the shopping centre car park three times in one week.",
         "We weren't doing anything wrong: we just had nowhere to skate.",
         "Today I want to convince you that our town needs a skate park.",
         "First of all, a skate park would give young people a safe place to meet.",
         "Secondly, skating is exercise, and it gets us off our screens.",
         "On top of that, we would look after a place that is ours.",
         "In conclusion, you were all young once. Please give us a space to be young in."]
assert one(hook_types, SKATE[0]) == "s" and [one(sign, s) for s in SKATE[3:]] == ["s", "m", "m", "e"] and not weak_marks(" ".join(SKATE))

pack = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Speaking and Listening Teacher Pack | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{PACK_STYLE}
{EXTRA}
.fym .c{{height:24mm}}.fym .fc.sm{{font-size:10.4pt;line-height:1.28;margin-top:2mm;font-weight:600}}.idc{{padding:2mm 4mm;margin-bottom:3mm}}.idc h3{{margin:0 0 1mm}}
.idc .st td{{height:5mm;padding:1px 6px}}.p1 .proc td{{font-size:8.6pt;padding:2px 6px}}.ops div{{font-size:12pt;padding:5mm 3mm}}.ops b{{font-size:19pt}}
.ws .eh td{{font-size:8.6pt;padding:2px 6px}}.ws .eh .gap{{height:13px}}.ws ol.q li{{margin-bottom:1px}}
</style></head><body>

<div class="page p1">
  <div class="band"><div><div class="k">Junior Cycle English · Teacher pack</div><h1>Speaking and listening</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2015 specification): {LO}</p>
  <div class="two">
    <div><h3>Aims</h3><p>By the end of the lesson students can open a short talk with a hook, use signpost words so listeners can follow, keep eye contact and a clear voice, reply to a speaker with a follow-up question, and agree, disagree, join in and ask for more politely in a group.</p></div>
    <div><h3>In this pack</h3><p>p.1 Teacher notes · p.2 Discussion Sort cards (cut-up) · p.3 Talk Swap A/B (speaking + listening) · p.4 Wall poster · p.5 Worksheet: Fix the Talk + exam-style questions · p.6 Answers. Level: 1st year (good prep for the 2nd-year Oral Communication CBA). Time: about 60 minutes. All texts are original.</p></div>
  </div>
  <h2 style="margin-top:8px">Procedure</h2>
  <table class="proc"><tbody>
    <tr><td>5 min</td><td><b>Lead-in.</b> Give two openings to the same talk: <i>“Em, so, today I'm going to talk about sharks.”</i> / <i>“Sharks were swimming in the sea long before the dinosaurs.”</i> Which one makes you want to listen? Why?</td></tr>
    <tr><td>8 min</td><td><b>Guided discovery.</b> Elicit the three kinds of hook (question, fact, story) and the signposts for start, next point and end. Model bad habits for 20 seconds (head down, mumbling, swaying); students name each one and the fix.</td></tr>
    <tr><td>10 min</td><td><b>Discussion Sort</b> (p.2, groups of 4, one set of 24 cards). Sort into agree / disagree politely / join in / ask for more (6 each). Then deal the cards out and discuss <i>“Should homework be banned?”</i>: each student must use their cards, laying each one down as they say it.</td></tr>
    <tr><td>15 min</td><td><b>Talk Swap</b> (p.3, pairs). A gives the one-minute talk; B listens without the text and fills the grid, then asks their follow-up question and gives one delivery tip. Swap.</td></tr>
    <tr><td>17 min</td><td><b>Worksheet</b> (p.5). Fix the Talk in pairs, then the exam-style questions on "A Place to Skate" alone.</td></tr>
    <tr><td>5 min</td><td><b>Exit ticket.</b> Write a hook for a talk on your favourite place, and one question you would ask a classmate about theirs. Homework: play <b>Talk Tips</b> at {GAME}.</td></tr>
  </tbody></table>
  <div class="note"><b>Errors to look for:</b> announcing the topic instead of a hook · reading word for word · no signposts · "That's it" endings · follow-up questions that change the subject · disagreeing with "No, that's wrong". <b>Support:</b> the poster (p.4) on the desk; let weaker students hold their Talk Swap text and look up at each full stop. <b>Fast finishers:</b> rewrite the Talk Swap opening with a different kind of hook.</div>
  <p class="small"><b>Discussion Sort key:</b> {sort_key}</p>
</div>

<div class="page">
  <div class="band"><div><div class="k">Groups of 4 · cut up the 24 cards</div><h1>Discussion Sort</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.4pt;margin:0 0 2mm">Sort the cards into four jobs: <b>agree, disagree politely, join in, ask for more</b> (6 cards each). Then use them in a real discussion: lay a card down each time you say it.</p>
  <div class="fym">{sort_html}</div>
</div>

<div class="page">
  <div class="band"><div><div class="k">Pairs · cut along the dashed line</div><h1>Talk Swap A/B</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.4pt">Each talk has a hook, three points with signposts and a strong ending. Can your partner catch them all without seeing the text?</p>
  {swap_card("A", TALK_A, TALK_B)}
  {swap_card("B", TALK_B, TALK_A)}
</div>

<div class="page">
  <div class="poster">
    <h1>Hook. Signpost. Finish strong.</h1>
    <div class="ops">
      <div style="background:var(--green-soft)"><b>Hook</b>a question · a fact<br>a short story</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Signposts</b>First of all · Moving on<br>To sum up</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Delivery</b>look up · slow down<br>loud enough · no "em"</div>
      <div style="background:var(--green-soft)"><b>Listen</b>nod · let them finish<br>ask about what they said</div>
    </div>
    <p style="text-align:center;font-size:20pt!important;font-weight:800;margin:4mm 0">Not "Today I'm going to talk about…"</p>
    <p style="text-align:center;font-size:10pt;color:var(--muted)">Léim · leim.ie · Play Talk Tips: {GAME}</p>
  </div>
</div>

<div class="page ws">
  <div class="band"><div><div class="k">Worksheet · exam-style questions</div><h1>Fix the Talk</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Fix the Talk</h2>
  <p>Each one has a problem. Say what's wrong and write or describe a better version.</p>
  <table class="eh"><thead><tr><th>What the speaker does</th><th>What's wrong and the fix</th></tr></thead><tbody>
  {"".join(f"<tr><td style='font-weight:500'>{s}</td><td><span class='gap'></span><span class='gap'></span></td></tr>" for s, r in FIX)}
  </tbody></table>
  <h2>B. Exam-style questions: "A Place to Skate" (a talk to the town council)</h2>
  <div class="pass">{" ".join(SKATE)}</div>
  <ol class="q">
    <li>What kind of hook does the speaker use? Why does it work?<span class="long"></span></li>
    <li>List the four signpost words or phrases.<span class="long"></span></li>
    <li>Find two places where the speaker talks directly to the audience.<span class="long"></span></li>
    <li>Is the ending effective? Explain your answer.<span class="long"></span></li>
    <li>Write the opening of a talk on a change you would like in your school. Use a different kind of hook.<span class="long"></span><span class="long"></span></li>
  </ol>
</div>

<div class="page an">
  <div class="band"><div><div class="k">For the teacher</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>Discussion Sort</h2>
  <p>{sort_key}</p>
  <h2>Talk Swap</h2>
  {"".join(f"<p><b>{n}:</b> Hook: {HN[TALK_KEY[n][0]].lower()} · Signposts: <i>{' → '.join(TALK_KEY[n][1])}</i> · Points: " + "; ".join(L[i].split(", ", 1)[1].rstrip('.') for i in (2, 3, 4)) + "</p>" for n, L in (TALK_A, TALK_B))}
  <p>Accept any follow-up question about the talk's topic (e.g. <i>What's the easiest dinner to start with?</i> / <i>What breed of dog would you pick?</i>).</p>
  <h2>A. Fix the Talk</h2>
  <table><tbody>{"".join(f"<tr><td style='width:40%'>{s}</td><td>{r}</td></tr>" for s, r in FIX)}</tbody></table>
  <h2>B. Exam-style questions</h2>
  <ol class="q">
    <li>A story: being moved on from the car park three times. It is personal and real, so listeners feel the problem before the speaker argues.</li>
    <li>First of all · Secondly · On top of that · In conclusion.</li>
    <li>"Today I want to convince you" · "you were all young once" · "Please give us a space" (any two).</li>
    <li>Yes: it sums up and speaks straight to the council with a memorable last line ("a space to be young in"), not "That's it".</li>
    <li>Credit a question or fact hook (since the model uses a story), a clear point of view and a plan.</li>
  </ol>
  <h2>Marking tip</h2>
  <p>For a written talk, reward a hook, audience awareness (you, we, a question), signposted points and a strong ending, more than length. Our guide, not an official marking scheme.</p>
</div>
</body></html>"""

cover = """<!doctype html><html><head><meta charset="utf-8"><style>
body{margin:0;width:1200px;height:1200px;background:#1B2430;font-family:Inter,sans-serif;color:#fff;display:flex;flex-direction:column;justify-content:space-between;padding:90px;box-sizing:border-box}
.k{display:inline-block;background:#2E7D57;border-radius:99px;padding:12px 26px;font-weight:700;font-size:28px;letter-spacing:.06em;text-transform:uppercase}
h1{font-size:96px;font-weight:800;line-height:1.25;letter-spacing:-.02em;margin:60px 0 20px}
h1 span{background:#F6CF5A;color:#1B2430;padding:0 18px;border-radius:14px}
.sub{font-size:40px;line-height:1.4;color:#DDE3EA}
.em{font-size:48px;margin-top:30px;font-weight:800;letter-spacing:.01em;color:#F6CF5A}
.foot{display:flex;justify-content:space-between;align-items:center;font-size:34px;font-weight:700}
.price{background:#F6CF5A;color:#1B2430;border-radius:16px;padding:14px 28px}
</style></head><body>
<div><span class="k">Junior Cycle English · Teacher pack</span>
<h1><span>Speaking &amp;</span><br><span>listening</span></h1>
<div class="sub">Discussion Sort cards · Talk Swap A/B<br>Poster · Worksheet + answers</div>
<div class="em">hooks · signposts · eye contact<br>listening replies · discussion</div></div>
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
    pdf("teacher-pack", os.path.join(OUT, "Speaking-Listening-Teacher-Pack-Leim.pdf"))
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--hide-scrollbars", "--window-size=1200,1200",
                    f"--screenshot={os.path.join(OUT, f'{SLUG}-cover.png')}", f"{SLUG}-cover.html"], cwd=SRC, check=True, capture_output=True)
