#!/usr/bin/env python3
"""Persuasive writing & speeches (JC English Order 18): free sheet (-> printables/), 6-page teacher pack + 1200x1200 cover (-> OUTDIR).
Usage: python3 src/build_persuasive_pdfs.py /tmp/persuasive
Items come from the game's data block (persuasion-power.html). Every answer is re-derived with the checker's own rules
(src/test_persuasion_power.py: tech, good_reason, good_reply, good_cta) and asserted; the checker's data pass runs first.
Styles are read from src/build_money1_pdfs.py."""
import os, sys, random, subprocess, re
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC); sys.path.insert(0, SRC)
from test_persuasion_power import content, tech, good_reason, good_reply, good_cta, load, data_pass, rude, evid
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/persuasive"; os.makedirs(OUT, exist_ok=True)
SLUG = "persuasive-writing-speeches"
LO = "W3, OL5, OL7, OL10, R8"
GAME = "leim.ie/persuasion-power.html"
D = load(os.path.join(ROOT, "persuasion-power.html")); assert not data_pass(D), data_pass(D)
TN = {"rq": "Rhetorical question", "three": "Rule of three", "stat": "Statistic", "emo": "Emotive language", "you": "Direct address", "rep": "Repetition"}
L = "abcd"
def strip_emoji(s): return re.sub(r"^\S+ ", "", s)

# ---------- free sheet ----------
random.seed(1818)
A_items = [x for k in TN for x in random.sample([y for y in D["tech"] if y[1] == k], 2)]; random.shuffle(A_items)
for s, k in A_items: assert tech(s) == [k]
def mc(items, ok):
    out = []
    for p, best, wrong in items:
        opts = [best] + list(wrong); random.shuffle(opts)
        right = [i for i, o in enumerate(opts) if ok(p, o)]; assert len(right) == 1, (p, opts)
        out.append((p, opts, L[right[0]]))
    return out
B_items = mc(random.sample(D["back"], 3), good_reason)
C_items = mc(random.sample(D["counter"], 3), good_reply)
D_items = random.sample(D["cta"], 4)
for t, c in D_items: assert good_cta(t, c)
NQ = len(A_items) + len(B_items) + len(C_items) + len(D_items) + 2; assert NQ == 24, NQ
nA = 1; nB = nA + len(A_items); nC = nB + len(B_items); nD = nC + len(C_items); nE = nD + len(D_items)

def style(var):
    return re.search(var + r' = f"""<!doctype.*?<style>(.*?)</style>', open(os.path.join(SRC, "build_money1_pdfs.py"), encoding="utf-8").read(), re.S).group(1).replace("{LO}", LO).replace("{{", "{").replace("}}", "}").replace("JC Maths LOs (2018 spec)", "JC English LOs (2015 spec)")
SHEET_STYLE = style("sheet"); PACK_STYLE = style("pack")
assert "JC English LOs (2015 spec)" in SHEET_STYLE and "Single-teacher licence" in PACK_STYLE and "JC English LOs (2015 spec)" in PACK_STYLE
EXTRA = """.wk{line-height:1.45;border:1.5px solid var(--line);border-radius:8px;padding:2px 7px;margin:3px 0;font-size:9.4pt}.wk b.h{display:block}
table.st{border-collapse:collapse;margin:3px 0;font-size:9.2pt;width:100%}table.st td,table.st th{border:1px solid #C9D1DA;padding:2px 6px;text-align:left}
.pass{border-left:4px solid var(--green);background:var(--mist);padding:5px 10px;margin:4px 0;font-style:italic}
.opts{list-style:none;padding-left:0;margin:1px 0 3px}.opts li{margin:0!important;font-size:8.8pt}"""

half = len(A_items) // 2
def a_li(i, s): return f"<li value='{i}'><i>{s}</i><br><span class='line' style='min-width:34mm'></span></li>"
A1 = "".join(a_li(i, s) for i, (s, k) in enumerate(A_items[:half], nA)); A2 = "".join(a_li(i, s) for i, (s, k) in enumerate(A_items[half:], nA + half))
def mc_html(items, n0, lab):
    return "".join(f"<li value='{i}'><b>{lab}</b> <i>{p}</i><ul class='opts'>{''.join(f'<li>({L[j]}) {o}</li>' for j, o in enumerate(opts))}</ul></li>" for i, (p, opts, a) in enumerate(items, n0))
B_html = mc_html(B_items, nB, "Point:"); C_html = mc_html(C_items, nC, "The other side says:")
D_html = "".join(f"<li value='{i}'>Speech: <b>{strip_emoji(t)}</b><span class='long'></span></li>" for i, (t, c) in enumerate(D_items, nD))

E1 = "Our school should have a water fountain on every corridor."
E2 = ("Who wants to eat lunch standing up? Every day, 120 students queue for 30 tables. "
      "The canteen is crowded, noisy and too small. You deserve somewhere to sit.")
assert "rq" in tech("Who wants to eat lunch standing up?") and tech("Every day, 120 students queue for 30 tables.") == ["stat"]
assert tech("The canteen is crowded, noisy and too small.") == ["three"] and tech("You deserve somewhere to sit.") == ["you"]

sheet = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Persuasive writing and speeches, rules and practice | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{SHEET_STYLE}
{EXTRA}
.p2 ol.q li{{margin-bottom:1px;font-size:9pt}}.p2 h2{{margin:4px 0 2px}}.p2 .two{{gap:5mm}}
</style></head><body>
<div class="page tight">
  <div class="band"><div><div class="k">Junior Cycle English · Free revision sheet</div><h1>Persuasive writing and speeches</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2015 specification): {LO}. Play the game: <b>{GAME}</b></p>
  <div class="two">
   <div><h2>1. Six techniques</h2>
    <table class="st"><tbody>
     <tr><td><b>Rhetorical question</b></td><td>Who wants a town with nowhere safe to play?</td></tr>
     <tr><td><b>Rule of three</b></td><td>Sport teaches teamwork, patience and respect.</td></tr>
     <tr><td><b>Statistic</b></td><td>Our survey found that 8 in 10 students skip breakfast.</td></tr>
     <tr><td><b>Emotive language</b></td><td>Innocent animals are left cold and frightened.</td></tr>
     <tr><td><b>Direct address</b></td><td>Your vote can change this town.</td></tr>
     <tr><td><b>Repetition</b></td><td>We need action. We need it now.</td></tr></tbody></table>
    <p style="font-size:9pt">Use real facts, or say where a number comes from ("our class survey"). Never make up a fact and pretend it is official.</p>
    <h2>2. Back it up</h2>
    <div class="wk"><b class="h">Weak</b><i>We should get a skate park because it would be good.</i></div>
    <div class="wk"><b class="h">Strong</b><i>A skate park would give teenagers a safe place to meet, so that fewer would skate on busy roads.</i></div>
    <p style="font-size:9pt">Evidence = a number, an example ("for example…", "such as…") or a result ("which means…"). Insults win no one over.</p></div>
   <div><h2>3. Build a speech</h2>
    <table class="st"><tbody>
     <tr><td><b>1 Hook</b></td><td>a question, a fact or a short story</td></tr>
     <tr><td><b>2 Points</b></td><td>one per paragraph, each backed up</td></tr>
     <tr><td><b>3 Answer back</b></td><td>Some people say… However…</td></tr>
     <tr><td><b>4 Call to action</b></td><td>tell them exactly what to do</td></tr></tbody></table>
    <h2>4. Answer the other side</h2>
    <div class="wk"><i>Some people say phones help students stay safe. <b>However</b>, students can stay safe with a phone kept in a locker until home time.</i></div>
    <p style="font-size:9pt">State their point fairly, use However / But / Yet, and deal with <b>their</b> point. Stay polite.</p>
    <h2>5. End with a call to action</h2>
    <div class="wk"><b class="h">Weak</b><i>That's all I have to say. Thanks.</i></div>
    <div class="wk"><b class="h">Strong</b><i>Sign our petition today and help us plant fifty new trees.</i></div>
    <p style="font-size:9pt">Start with a doing word: Sign… Join… Vote… Bring… Write to…</p></div>
  </div>
  <div class="tip"><b>Exam tip:</b> for "How does the writer try to persuade?" questions: <b>name</b> the technique, <b>quote</b> it and <b>explain</b> its effect on the reader. For writing tasks, check who the audience is: a speech to the council is formal, polite but firm.</div>
</div>

<div class="page p2">
  <div class="band"><div><div class="k">Practice · {NQ} questions</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Name the technique in each line</h2>
  <div class="two"><div><ol class="q">{A1}</ol></div><div><ol class="q">{A2}</ol></div></div>
  <div class="two"><div><h2>B. Which reason backs up the point best? Circle a letter</h2><ol class="q">{B_html}</ol></div>
  <div><h2>C. Which is the best answer to the other side? Circle a letter</h2><ol class="q">{C_html}</ol></div></div>
</div>

<div class="page">
  <div class="band"><div><div class="k">Write it + answers</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <h2>D. Write a call to action to end each speech</h2><ol class="q">{D_html}</ol>
  <h2>E. Exam-style</h2>
  <ol class="q">
   <li value="{nE}">Write the opening of a speech to your school: "{E1}" Use a rhetorical question and the rule of three.<span class="long"></span><span class="long"></span></li>
   <li value="{nE + 1}">Name <b>three</b> techniques in this extract and explain how one works: <i>"{E2}"</i><span class="long"></span><span class="long"></span></li>
  </ol>
  <h2>Answers</h2>
  <table class="ans"><tbody>
   <tr><td><b>A</b></td><td>{" · ".join(f"{i}. {TN[tech(s)[0]]}" for i, (s, k) in enumerate(A_items, nA))}</td></tr>
   <tr><td><b>B</b></td><td>{" · ".join(f"{i}. ({a})" for i, (p, o, a) in enumerate(B_items, nB))}: the right reason sticks to the point and gives evidence. The others insult, go off the topic or go round in circles.</td></tr>
   <tr><td><b>C</b></td><td>{" · ".join(f"{i}. ({a})" for i, (p, o, a) in enumerate(C_items, nC))}: the best answer starts with However / But / Yet, deals with their point and stays polite.</td></tr>
   <tr><td><b>D</b></td><td>Sample answers: {" · ".join(f"{i}. <i>{c}</i>" for i, (t, c) in enumerate(D_items, nD))}<br>(Any line that tells the audience exactly what to do is fine.)</td></tr>
   <tr><td><b>E</b></td><td>{nE}. Sample: <i>Good morning, everyone. How many of you have sat through double PE with nothing to drink? A fountain on every corridor would be cheap, healthy and good for the planet.</i><br>
     {nE + 1}. Rhetorical question ("Who wants to eat lunch standing up?"), statistic ("120 students queue for 30 tables"), rule of three ("crowded, noisy and too small"), direct address ("You deserve…"). The statistic makes the problem sound real: 120 students for 30 tables is hard to argue with.</td></tr>
  </tbody></table>
  <div class="note"><b>Got one wrong?</b> Go back to page 1, then play <b>Persuasion Power</b> at {GAME}: the "Go back over these" list at the end explains each mistake.</div>
  <p class="small">All sentences written by Léim; names, places and survey numbers are made up. Léim is independent and not connected with the State Examinations Commission or the NCCA.</p>
</div>
</body></html>"""
assert "rq" in tech("How many of you have sat through double PE with nothing to drink?") and "three" in tech("A fountain on every corridor would be cheap, healthy and good for the planet.")

# ---------- teacher pack ----------
random.seed(1819)
TS = [x for k in TN for x in random.sample([y for y in D["tech"] if y[1] == k], 4)]; random.shuffle(TS)
assert len(TS) == 24
for s, k in TS: assert tech(s) == [k]
ts_html = "".join(f'<div class="c"><span class="tag">Card {i}</span><div class="fc sm">{s}</div></div>' for i, (s, k) in enumerate(TS, 1))
ts_key = " · ".join(f"<b>{TN[k]}</b>: {', '.join(str(i) for i, (s, kk) in enumerate(TS, 1) if kk == k)}" for k in TN)

CA = D["counter"][0:6]; CB = D["counter"][6:12]
def swap_card(who, mine, theirs, seed):
    ans = [b for v, b, w in theirs]; random.seed(seed); random.shuffle(ans)
    return f"""<div class="idc"><h3>Student {who} · Debate Swap</h3>
    <p style="font-size:8.8pt;margin:0 0 1mm"><b>1. Read</b> each point from the other side to your partner, one at a time. Your partner finds the best answer on their card and reads it back. Tick it if it deals with the point.</p>
    <table class="st" style="font-size:9pt"><tbody>{"".join(f"<tr><td style='width:6%'><b>{i}</b></td><td>{v}</td><td style='width:8%'>☐</td></tr>" for i, (v, b, w) in enumerate(mine, 1))}</tbody></table>
    <p style="font-size:8.8pt;margin:1mm 0"><b>2. Listen</b> to your partner's points. Find the answer below that deals with each one and read it out. Write their point number in the box.</p>
    <table class="st" style="font-size:9pt"><tbody>{"".join(f"<tr><td>{a}</td><td style='width:10%'></td></tr>" for a in ans)}</tbody></table>
    <p style="font-size:8.8pt;margin:1mm 0 0"><b>3. Together:</b> underline the word in each answer that links back to the other side's point.</p></div>"""
for v, b, w in CA + CB: assert good_reply(v, b)
def link(v, b):
    return [x for x in re.findall(r"[A-Za-z'-]+", b) if len(x) >= 4 and (content(x) & content(v))][0]

FIX = [("Today I'm going to talk about why we need a new library.", "Weak hook (it just announces the topic): <b>Where in this town can you study in peace? Nowhere.</b>"),
       ("We should get a pool because it would be good.", "No evidence: <b>A pool would let every first year learn to swim, which means safer summers at the beach.</b>"),
       ("Anyone who disagrees with me is an idiot.", "An insult wins nobody over: <b>Some people may disagree, so let me explain why I think they should think again.</b>"),
       ("Loads of kids, like, really want it!!", "Slang in a formal speech: <b>Many students have told us that they want it.</b>"),
       ("Some people say it costs too much. They are right.", "Agrees with the other side: <b>Some people say it costs too much. However, local businesses could help to pay for it.</b>"),
       ("That's all I have to say. Thanks.", "Weak ending: <b>Please sign our petition today and help us make it happen. Thank you for listening.</b>")]
assert rude("Anyone who disagrees with me is an idiot.") and evid("A pool would let every first year learn to swim, which means safer summers at the beach.")
assert good_cta("a petition to make it happen", "Sign our petition today and help us make it happen.")

SPEECH = ("A Bike Shed for Kilbrook Community School",
          ["Good morning, everyone.", "How many of you cycled to school today?",
           "In our class survey, only 4 of 28 students did, and most of the others said there is nowhere safe to lock a bike.",
           "A covered bike shed would be cheap, simple and safe.",
           "Some people say bikes would be stolen anyway.", "However, bikes locked in a shed beside the office would be in full view of staff all day.",
           "Think of the traffic at the gate every morning. Think of your own fitness.",
           "Please sign our petition at lunchtime and help us build the shed before spring.", "Thank you for listening."])
S = SPEECH[1]
assert "rq" in tech(S[1]) and "stat" in tech(S[2]) and tech(S[3]) == ["three"] and "rep" in tech(S[6])
assert good_reply(S[4], S[5]) and good_cta("bike shed", S[7].replace("Please s", "S"))

pack = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Persuasive Writing and Speeches Teacher Pack | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{PACK_STYLE}
{EXTRA}
.fym .c{{height:28mm}}.fym .fc.sm{{font-size:9.4pt;line-height:1.25;margin-top:2mm;font-weight:500}}.idc{{padding:2mm 4mm;margin-bottom:3mm}}.idc h3{{margin:0 0 1mm}}
.idc .st td{{padding:1px 6px}}.p1 .proc td{{font-size:8.6pt;padding:2px 6px}}.ops div{{font-size:12pt;padding:5mm 3mm}}.ops b{{font-size:19pt}}
.ws .eh td{{font-size:8.6pt;padding:2px 6px}}.ws .eh .gap{{height:13px}}.ws ol.q li{{margin-bottom:1px}}.ws .pass{{font-size:9pt}}
</style></head><body>

<div class="page p1">
  <div class="band"><div><div class="k">Junior Cycle English · Teacher pack</div><h1>Persuasive writing and speeches</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2015 specification): {LO}</p>
  <div class="two">
    <div><h3>Aims</h3><p>By the end of the lesson students can name and explain six persuasive techniques, back up a point with evidence, answer the other side politely, and end a speech with a clear call to action.</p></div>
    <div><h3>In this pack</h3><p>p.1 Teacher notes · p.2 Technique Sort cards (cut-up) · p.3 Debate Swap A/B (speaking) · p.4 Wall poster · p.5 Worksheet: Fix the Speech + exam-style questions · p.6 Answers. Level: 2nd year. Time: about 60 minutes. All texts are original; names, places and survey numbers are made up.</p></div>
  </div>
  <h2 style="margin-top:8px">Procedure</h2>
  <table class="proc"><tbody>
    <tr><td>5 min</td><td><b>Lead-in.</b> Read two openings for a skate-park speech: "Today I'm going to talk about the skate park. It would be good." and "Where can a teenager go in this town on a Saturday?…" (the game's "Spot the pattern"). Which would make the council listen? Why?</td></tr>
    <tr><td>8 min</td><td><b>Guided discovery.</b> Students find three things the strong opening does. Elicit and name: rhetorical question, statistic, direct address. Add rule of three, emotive language, repetition with one example each.</td></tr>
    <tr><td>12 min</td><td><b>Technique Sort</b> (p.2, groups of 3, one set of 24 cards). Sort the lines into six groups of four. Then each group picks its favourite line and explains the effect.</td></tr>
    <tr><td>12 min</td><td><b>Debate Swap</b> (p.3, pairs). A reads a point from the other side; B finds and reads the answer that deals with it; then swap. Together they underline the linking word.</td></tr>
    <tr><td>18 min</td><td><b>Worksheet</b> (p.5). Fix the Speech in pairs, then the exam-style questions on the bike-shed speech alone.</td></tr>
    <tr><td>5 min</td><td><b>Exit ticket.</b> Write a one-line call to action for a speech asking for a longer lunch break. Homework: play <b>Persuasion Power</b> at {GAME}.</td></tr>
  </tbody></table>
  <div class="note"><b>Errors to look for:</b> opinions with no reason ("it would be good") · made-up facts presented as official · insulting the other side · agreeing with the other side by mistake · a flat ending ("That's all, thanks") · naming a technique with no quote or explanation. <b>Support:</b> the poster (p.4) on the desk. <b>Fast finishers:</b> write the other side's speech against the bike shed.</div>
</div>

<div class="page">
  <div class="band"><div><div class="k">Groups of 3 · cut up the 24 cards</div><h1>Technique Sort</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.4pt;margin:0 0 2mm">Sort the 24 lines into six groups of four: <b>rhetorical question · rule of three · statistic · emotive language · direct address · repetition</b>.</p>
  <div class="fym">{ts_html}</div>
</div>

<div class="page">
  <div class="band"><div><div class="k">Pairs · cut along the dashed line</div><h1>Debate Swap A/B</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.4pt">Every point from the other side has an answer on your partner's card. Can you find it by listening?</p>
  {swap_card("A", CA, CB, 1820)}
  {swap_card("B", CB, CA, 1821)}
</div>

<div class="page">
  <div class="poster">
    <h1>Win them over</h1>
    <div class="ops">
      <div style="background:var(--green-soft)"><b>1 Hook</b>a question, a fact<br>or a short story</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>2 Back it up</b>a number · an example<br>a result</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>3 Answer back</b>Some people say…<br>However…</div>
      <div style="background:var(--green-soft)"><b>4 Call to action</b>Sign… Join…<br>Vote…</div>
    </div>
    <p style="text-align:center;font-size:20pt!important;font-weight:800;margin:4mm 0">No point without proof.</p>
    <p style="text-align:center;font-size:10pt;color:var(--muted)">Léim · leim.ie · Play Persuasion Power: {GAME}</p>
  </div>
</div>

<div class="page ws">
  <div class="band"><div><div class="k">Worksheet · exam-style questions</div><h1>Fix the Speech</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Fix the Speech</h2>
  <p>Each line is from a speech to the school assembly. Say what's wrong and write a better line.</p>
  <table class="eh"><thead><tr><th>Line</th><th>What's wrong and the fix</th></tr></thead><tbody>
  {"".join(f"<tr><td style='font-weight:500'>{s}</td><td><span class='gap'></span><span class='gap'></span></td></tr>" for s, r in FIX)}
  </tbody></table>
  <h2>B. Exam-style questions: "{SPEECH[0]}"</h2>
  <div class="pass">{" ".join(S)}</div>
  <ol class="q">
    <li>Who is the audience for this speech, and what is its purpose?<span class="long"></span></li>
    <li>Find a rhetorical question and a statistic in the speech.<span class="long"></span></li>
    <li>Quote the rule of three and explain why it works.<span class="long"></span></li>
    <li>How does the speaker deal with the other side's point?<span class="long"></span></li>
    <li>Is the ending effective? Explain your answer.<span class="long"></span><span class="long"></span></li>
  </ol>
</div>

<div class="page an">
  <div class="band"><div><div class="k">For the teacher</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>Technique Sort (card numbers)</h2>
  <p>{ts_key}</p>
  <h2>Debate Swap</h2>
  <p>Each point and the answer that deals with it (the linking word in brackets): {" · ".join(f"<b>{w}{i}</b> {' '.join(b.split()[:5])}… ({link(v, b)})" for w, LL in (("A", CA), ("B", CB)) for i, (v, b, x) in enumerate(LL, 1))}</p>
  <h2>A. Fix the Speech</h2>
  <table><tbody>{"".join(f"<tr><td style='width:36%'>{s}</td><td>{r}</td></tr>" for s, r in FIX)}</tbody></table>
  <h2>B. Exam-style questions</h2>
  <ol class="q">
    <li>Students (and staff) at the school assembly; to persuade them to support a covered bike shed and sign the petition.</li>
    <li>Rhetorical question: "How many of you cycled to school today?" Statistic: "only 4 of 28 students".</li>
    <li>"cheap, simple and safe": three short words sound complete and easy to remember, and they answer the main worries (cost, effort, safety).</li>
    <li>It states the other side fairly ("Some people say bikes would be stolen anyway"), then answers it with "However" and a reason (bikes locked beside the office would be in view of staff all day).</li>
    <li>Yes: it is a clear call to action (sign the petition, when and where) with a goal ("before spring"), and it thanks the audience politely. Repetition just before it ("Think of…") builds up to it.</li>
  </ol>
  <h2>Marking tip</h2>
  <p>Reward a technique named + quoted + explained over a list of names. In writing, reward evidence for each point and a fair answer to the other side. Our guide, not an official marking scheme.</p>
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
<h1><span>Persuasive writing</span><br><span>&amp; speeches</span></h1>
<div class="sub">Technique Sort cards · Debate Swap A/B<br>Poster · Worksheet + answers</div>
<div class="em">hook · back it up · answer back<br>call to action</div></div>
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
    pdf("teacher-pack", os.path.join(OUT, "Persuasive-Writing-Speeches-Teacher-Pack-Leim.pdf"))
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--hide-scrollbars", "--window-size=1200,1200",
                    f"--screenshot={os.path.join(OUT, f'{SLUG}-cover.png')}", f"{SLUG}-cover.html"], cwd=SRC, check=True, capture_output=True)
