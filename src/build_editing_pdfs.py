#!/usr/bin/env python3
"""Editing & redrafting: proofreading your own work (JC English Order 26): free sheet (-> printables/),
6-page teacher pack + 1200x1200 cover (-> OUTDIR).
Usage: python3 src/build_editing_pdfs.py /tmp/p26
Items come from the game's data block (proofread-patrol.html). Every planted slip {slip>fix} is judged again with the checker's
own rules (src/test_proofread_patrol.py: judge, marks_in, spell_errors, fewer_less, who_whom, brk_ok) and asserted;
the checker's data pass runs first. Styles are read from src/build_money1_pdfs.py."""
import os, sys, random, subprocess, re
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC); sys.path.insert(0, SRC)
from test_proofread_patrol import judge, marks_in, spell_errors, fewer_less, who_whom, brk_ok, brk_parts, fixed, shown, load, data_pass, MARK
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/p26"; os.makedirs(OUT, exist_ok=True)
SLUG = "editing-redrafting"
LO = "W1, W6, W13, W2"
GAME = "leim.ie/proofread-patrol.html"
D = load(os.path.join(ROOT, "proofread-patrol.html")); assert not data_pass(D), data_pass(D)
KN = {"sp": "spelling", "cw": "mix-up word", "gr": "grammar"}

def checked(t, n=None):
    """assert every planted slip in t is a real slip with the right fix, and the fixed text spells clean"""
    ms = marks_in(t)
    for g, w, r in ms:
        k, err = judge(g, w, r); assert err is None, (t, w, r, err)
    assert not spell_errors(fixed(t)), (t, spell_errors(fixed(t)))
    if n is not None: assert len(ms) == n, (t, len(ms))
    return t
def slips_of(t): return [(w, r, judge(g, w, r)[0]) for g, w, r in marks_in(t)]
def fixlist(t): return ", ".join(f"<i>{w}</i> → <b>{r}</b>" for w, r, k in slips_of(t))

# ---------- free sheet ----------
random.seed(2601)
by = {k: [x for x in D["spot"] if x[1] == k] for k in KN}
A_items = random.sample(by["sp"], 3) + random.sample(by["cw"], 3) + random.sample(by["gr"], 2); random.shuffle(A_items)
for s, k, tip in A_items: checked(s, 1); assert judge(*marks_in(s)[0])[0] == k
B_items = [p for p in D["pass"] if len(MARK.findall(p[1])) in (2, 3)]
B_items = random.sample(B_items, 2)
for k, t in B_items: checked(t)
C_items = random.sample([x for x in D["few"] if x[1] == "fewer"], 3) + random.sample([x for x in D["few"] if x[1] == "less"], 3); random.shuffle(C_items)
for s, a in C_items: assert fewer_less(s) == a
D_items = random.sample([x for x in D["who"] if x[1] == "who"], 3) + random.sample([x for x in D["who"] if x[1] == "whom"], 3); random.shuffle(D_items)
for s, a in D_items: assert who_whom(s) == a
E_items = random.sample(D["brk"], 4)
def brk_bare(s): return s.replace("[", "").replace("]", "")
def brk_ans(s): return s.replace("[", "(").replace("]", ")")
for s in E_items: assert brk_ok(brk_ans(s), s) and not brk_ok(brk_bare(s), s)
nA = 1; nB = nA + 8; nC = nB + 2; nD = nC + 6; nE = nD + 6; nF = nE + 4
NQ = nF + 2 - 1; assert NQ == 28, NQ

EXAM = checked("On Sunday we went to the open day at the coastguard station in Kilmore. My brother and {me>I} climbed into the rescue boat. The crew showed us how they {done>did} a rescue at sea. There {was>were} three helicopters on the pad, and we got to sit in {one>one} of them. I {definately>definitely} want to join the coastguard when I'm older.".replace("{one>one}", "one"), 4)
EXAM_REDRAFT = "The day was good. We saw the boat and it was good. The helicopter was good too and the crew were nice."

def style(var):
    return re.search(var + r' = f"""<!doctype.*?<style>(.*?)</style>', open(os.path.join(SRC, "build_money1_pdfs.py"), encoding="utf-8").read(), re.S).group(1).replace("{LO}", LO).replace("{{", "{").replace("}}", "}").replace("JC Maths LOs (2018 spec)", "JC English LOs (2015 spec)")
SHEET_STYLE = style("sheet"); PACK_STYLE = style("pack")
assert "JC English LOs (2015 spec)" in SHEET_STYLE and "Single-teacher licence" in PACK_STYLE and "JC English LOs (2015 spec)" in PACK_STYLE
EXTRA = """.wk{line-height:1.45;border:1.5px solid var(--line);border-radius:8px;padding:2px 7px;margin:3px 0;font-size:9.4pt}.wk b.h{display:block}
table.st{border-collapse:collapse;margin:3px 0;font-size:9.2pt;width:100%}table.st td,table.st th{border:1px solid #C9D1DA;padding:2px 6px;text-align:left}
.pass{border-left:4px solid var(--green);background:var(--mist);padding:5px 10px;margin:4px 0;font-size:9.4pt;line-height:1.5}
.slip{text-decoration:line-through;color:#C0392B}.fx{font-weight:800;color:#1E6B45}"""
def two(items_html, cut):
    return f"<div class='two'><div><ol class='q'>{''.join(items_html[:cut])}</ol></div><div><ol class='q'>{''.join(items_html[cut:])}</ol></div></div>"
L = "<span class='line' style='min-width:60mm'></span>"
A_html = [f"<li value='{i}'>{shown(s)}<br>{L}</li>" for i, (s, k, t) in enumerate(A_items, nA)]
B_html = [f"<li value='{i}'><b>{k[2:].strip()}</b>: {shown(t)}<br>Slips: ____ {L}</li>" for i, (k, t) in enumerate(B_items, nB)]
C_html = [f"<li value='{i}'>{s.replace('___', '<b>_______</b>')}</li>" for i, (s, a) in enumerate(C_items, nC)]
D_html = [f"<li value='{i}'>{s.replace('___', '<b>_______</b>')}</li>" for i, (s, a) in enumerate(D_items, nD)]
E_html = [f"<li value='{i}'>{brk_bare(s)}</li>" for i, s in enumerate(E_items, nE)]

sheet = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Editing and redrafting: proofreading your own work, rules and practice | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{SHEET_STYLE}
{EXTRA}
.p2 ol.q li{{margin-bottom:2px;font-size:9.2pt}}.p2 h2{{margin:4px 0 2px}}.p2 .two{{gap:5mm}}
</style></head><body>
<div class="page tight">
  <div class="band"><div><div class="k">Junior Cycle English · Free revision sheet</div><h1>Editing &amp; redrafting</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2015 specification): {LO}. Play the game: <b>{GAME}</b></p>
  <p>Proofreading means reading your own work again to catch the slips. Redrafting means making it <b>better</b>. Every written answer is marked partly for accuracy, so both win marks.</p>
  <div class="two">
   <div><h2>1. Four passes</h2>
    <table class="st"><tbody>
     <tr><td><b>1. Spelling</b></td><td>your own tricky words: definitely, separate, beginning, until</td></tr>
     <tr><td><b>2. Mix-ups</b></td><td>there / their / they're, to / too, then / than, should <b>have</b> (not of)</td></tr>
     <tr><td><b>3. Grammar</b></td><td>one tense all the way; each of them <b>has</b>; my friend and <b>I</b> went; I <b>saw</b> / I have <b>seen</b></td></tr>
     <tr><td><b>4. Punctuation</b></td><td>capitals, full stops (no run-ons), apostrophes, speech marks</td></tr></tbody></table>
    <div class="wk"><b class="h">Spot the slips</b>My brother and <span class="slip">me</span> <span class="fx">I</span> went to the beach. <span class="slip">Their</span> <span class="fx">There</span> was nobody there. We should <span class="slip">of</span> <span class="fx">have</span> brought a coat.<br><span style="font-size:8.6pt">A spell checker would miss all three: they're real words in the wrong place.</span></div>
    <h2>2. Tips</h2>
    <p style="font-size:9pt">Read it in your head as if aloud. Check your <b>own</b> usual slips first. Cross out with one neat line and write the fix above. Leave two minutes at the end of every answer.</p></div>
   <div><h2>3. Fewer or less? Who or whom?</h2>
    <div class="wk"><b class="h">fewer / less</b><b>fewer</b> for things you can count: fewer cars, fewer goals.<br><b>less</b> for things you can't: less milk, less time.</div>
    <div class="wk"><b class="h">who / whom</b><b>who</b> does the action: the girl who won (she won).<br><b>whom</b> has it done to them: the man whom we met (we met <b>him</b>), and after to / with / for.<br><span style="font-size:8.6pt">Trick: him and whom both end in m.</span></div>
    <h2>4. Brackets and dashes</h2>
    <div class="wk">Our dog (a very lazy spaniel) slept through the storm.<br>Our dog – a very lazy spaniel – slept through the storm.<br><span style="font-size:8.6pt">Always in pairs. Take the extra part out and the sentence still works.</span></div>
    <h2>5. Redrafting</h2>
    <p style="font-size:9pt">Cut repeated words · swap weak words (nice, good, got) for exact ones · start sentences in different ways · one main idea per paragraph · keep your drafts for the Collection of Texts (CBA 2).</p></div>
  </div>
  <div class="tip"><b>Exam tip:</b> the students who keep their accuracy marks are the ones who read their answers back. Plan your time so you can.</div>
</div>

<div class="page p2">
  <div class="band"><div><div class="k">Practice · {NQ} questions</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Each sentence has one slip. Underline it and write the fix.</h2>
  {two(A_html, 4)}
  <h2>B. How many slips? Write the number, then the fixes.</h2>
  <ol class="q">{''.join(B_html)}</ol>
  <div class="two"><div><h2>C. fewer or less?</h2><ol class="q">{''.join(C_html)}</ol></div>
  <div><h2>D. who or whom?</h2><ol class="q">{''.join(D_html)}</ol></div></div>
  <h2>E. Add brackets (or a pair of dashes) round the extra information.</h2>
  {two(E_html, 2)}
</div>

<div class="page">
  <div class="band"><div><div class="k">Exam-style · answers</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <h2>F. Exam-style</h2>
  <ol class="q">
   <li value="{nF}">This paragraph from a student's diary has four slips. Find each one and write the correction.<div class="pass">{shown(EXAM)}</div><span class="long"></span><span class="long"></span></li>
   <li value="{nF + 1}">Redraft this paragraph to make it better. Keep the same day out.<div class="pass">{EXAM_REDRAFT}</div><span class="long"></span><span class="long"></span><span class="long"></span><span class="long"></span></li>
  </ol>
  <h2>Answers</h2>
  <table class="ans"><tbody>
   <tr><td><b>A</b></td><td>{" · ".join(f"{i}. {fixlist(s)}" for i, (s, k, t) in enumerate(A_items, nA))}</td></tr>
   <tr><td><b>B</b></td><td>{" · ".join(f"{i}. {len(slips_of(t))}: {fixlist(t)}" for i, (k, t) in enumerate(B_items, nB))}</td></tr>
   <tr><td><b>C</b></td><td>{" · ".join(f"{i}. {a}" for i, (s, a) in enumerate(C_items, nC))}</td></tr>
   <tr><td><b>D</b></td><td>{" · ".join(f"{i}. {a}" for i, (s, a) in enumerate(D_items, nD))}</td></tr>
   <tr><td><b>E</b></td><td>{" · ".join(f"{i}. {brk_ans(s)}" for i, s in enumerate(E_items, nE))} (or dashes)</td></tr>
   <tr><td><b>F</b></td><td>{nF}. {fixlist(EXAM)} · {nF + 1}. For example: <i>The open day was the best trip of the year. We clambered into the orange rescue boat, then sat in a real helicopter while the friendly crew explained every switch.</i> Reward: no repeated "good", exact words, detail, varied sentence starts.</td></tr>
  </tbody></table>
  <div class="note"><b>Got one wrong?</b> Go back to page 1, then play <b>Proofread Patrol</b> at {GAME}: the "Go back over these" list at the end explains each slip.</div>
  <p class="small">All sentences are written by Léim. Léim is independent and not connected with the State Examinations Commission or the NCCA.</p>
</div>
</body></html>"""

# ---------- teacher pack ----------
random.seed(2602)
CARDS = random.sample(by["sp"], 8) + random.sample(by["cw"], 8) + random.sample(by["gr"], 8); random.shuffle(CARDS)
for s, k, t in CARDS: checked(s, 1); assert judge(*marks_in(s)[0])[0] == k
cards_html = "".join(f'<div class="c"><span class="tag">Card {i}</span><div class="fc sm">{shown(s)}</div></div>' for i, (s, k, t) in enumerate(CARDS, 1))
cards_key = " · ".join(f"<b>{i}</b> {KN[k][0].upper()} {fixlist(s)}" for i, (s, k, t) in enumerate(CARDS, 1))

PA = checked("Last summer my cousin Ruth came to stay with us in Clare. We went {swiming>swimming} at Lahinch every day. Ruth surfed better {then>than} me. One day the waves were {to>too} big, so we built a sandcastle instead. Ruth and {me>I} called it Castle Clare.", 4)
PB = checked("Our school held a cake sale for the hospice in Ennis. Every class {have>has} to bake something. My friend and I made {fourty>forty} cupcakes with green icing. We sold them all before lunch, and {their>there} was a queue at the door. We raised more {then>than} last year.", 4)
def swap_card(who, mine, theirs):
    return f"""<div class="idc"><h3>Student {who} · Editor's Desk</h3>
    <p style="font-size:8.8pt;margin:0 0 1mm"><b>1. Proofread</b> your paragraph. It has <b>four</b> slips. Circle each one and write the fix above it.</p>
    <div class="pass">{shown(mine)}</div>
    <p style="font-size:8.8pt;margin:1mm 0"><b>2. Swap jobs.</b> Your partner reads out the four fixes they made. Check them against the corrected version of <b>their</b> paragraph below. Tick each one they found; for any they missed, give a clue (which sentence?), not the answer.</p>
    <div class="pass" style="background:#fff">{fixed(theirs)}</div>
    <p style="font-size:8.8pt;margin:1mm 0"><b>3. Redraft</b> one sentence of your paragraph to make it better. Read both versions to your partner: which is better, and why?</p>
    <span class="line" style="min-width:150mm"></span></div>"""

FIX = [("We should of booked the tickets online.", "should <b>have</b> booked (it only sounds like of)", "We should {of>have} booked the tickets online."),
       ("Each of the girls have a locker.", "each = one, so <b>has</b>", "Each of the girls {have>has} a locker."),
       ("I seen the new film on Friday.", "<b>saw</b> stands alone; seen needs have", "I {seen>saw} the new film on Friday."),
       ("There was less people at Mass this week.", "you can count people: <b>fewer</b> (and <b>were</b>)", None),
       ("My friend and me are going to Cork.", "take away \"my friend\": <b>I</b> am going", "My friend and {me>I} are going to Cork."),
       ("The match was brilliant, we won by a goal.", "a comma can't join two sentences: <b>brilliant. We won…</b> or <b>brilliant; we won…</b>", None)]
for s, r, m in FIX:
    if m: checked(m, 1); assert shown(m) == s
assert fewer_less("There were ___ people at Mass this week.") == "fewer"

EXP = checked("The Coastguard Open Day was held in Kilmore Quay on Saturday. Hundreds of people came, despite the {wheather>weather}. The crew showed visitors the rescue boat and {there>their} new drone. Each of the volunteers {were>was} wearing a bright orange jacket. The children, {whom>who} had never seen a lifeboat up close, loved every minute. Next year the crew hope to have {less>fewer} cancellations because of storms.", 5)

pack = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Editing &amp; Redrafting: Proofreading Teacher Pack | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{PACK_STYLE}
{EXTRA}
.fym .c{{height:30mm}}.fym .fc.sm{{font-size:10pt;line-height:1.35;margin-top:2mm;font-weight:600}}.idc{{padding:2mm 4mm;margin-bottom:3mm}}.idc h3{{margin:0 0 1mm}}
.idc .pass{{font-size:9.2pt}}.p1 .proc td{{font-size:8.6pt;padding:2px 6px}}.ops div{{font-size:12pt;padding:5mm 3mm}}.ops b{{font-size:19pt}}
.ws .eh td{{font-size:8.6pt;padding:2px 6px}}.ws .eh .gap{{height:13px}}.ws ol.q li{{margin-bottom:1px}}
</style></head><body>

<div class="page p1">
  <div class="band"><div><div class="k">Junior Cycle English · Teacher pack</div><h1>Editing &amp; redrafting</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2015 specification): {LO}</p>
  <div class="two">
    <div><h3>Aims</h3><p>By the end of the lesson students can proofread their own writing in four passes (spelling, mix-up words, grammar, punctuation), explain each slip they fix, choose fewer / less and who / whom, use brackets and dashes in pairs, and redraft a sentence to make it better.</p></div>
    <div><h3>In this pack</h3><p>p.1 Teacher notes · p.2 Slip Sort (24 cut-up cards) · p.3 Editor's Desk A/B (pair proofreading) · p.4 Wall poster · p.5 Worksheet: Error Hunt + exam-style questions · p.6 Answers. Level: 3rd year. Time: about 60 minutes. All sentences are written by Léim.</p></div>
  </div>
  <h2 style="margin-top:8px">Procedure</h2>
  <table class="proc"><tbody>
    <tr><td>5 min</td><td><b>Lead-in.</b> Board: <i>My brother and me went to the beach. Their was nobody there. We should of brought a coat.</i> How many slips? Would a spell checker find them? Introduce the four passes (poster, p.4).</td></tr>
    <tr><td>12 min</td><td><b>Slip Sort</b> (p.2, groups of 3, one set of 24 cards). Each card has one slip. Sort into three piles: <b>spelling</b>, <b>mix-up word</b>, <b>grammar</b>; write the fix on the back. 8 cards in each pile.</td></tr>
    <tr><td>15 min</td><td><b>Editor's Desk</b> (p.3, pairs). Each student proofreads their own paragraph (4 slips), then the partner checks the fixes against the corrected version on their card, giving clues, not answers. Finish by redrafting one sentence.</td></tr>
    <tr><td>5 min</td><td><b>fewer / less, who / whom.</b> Quick-fire on the board: <i>___ goals / ___ time / the girl ___ won / the man ___ we met</i>. Teach the him / whom trick.</td></tr>
    <tr><td>18 min</td><td><b>Worksheet</b> (p.5). Error Hunt in pairs, then the exam-style questions on the Coastguard report alone.</td></tr>
    <tr><td>5 min</td><td><b>Exit ticket.</b> Students write their own top three slips on a sticky note to check in every answer. Homework: play <b>Proofread Patrol</b> at {GAME}.</td></tr>
  </tbody></table>
  <div class="note"><b>Errors to look for:</b> trusting the spell checker · reading too fast (read word by word, as if aloud) · <i>should of</i> · <i>each of them have</i> · <i>me and him went</i> · <i>I seen / I done</i> · <i>less people</i> · one bracket or one dash on its own · redrafting that only fixes slips without improving the writing. <b>Support:</b> give the number of slips per sentence. <b>Fast finishers:</b> write a paragraph with three hidden slips for a partner.</div>
</div>

<div class="page">
  <div class="band"><div><div class="k">Groups of 3 · cut up the 24 cards</div><h1>Slip Sort</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.4pt;margin:0 0 2mm">Each card has <b>one</b> slip. Find it, then sort the cards into three piles: <b>spelling</b>, <b>mix-up word</b> (a real word in the wrong place), <b>grammar</b>. Write the fix on the back.</p>
  <div class="fym">{cards_html}</div>
</div>

<div class="page">
  <div class="band"><div><div class="k">Pairs · cut along the dashed line</div><h1>Editor's Desk A/B</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.4pt">Proofread, check, redraft.</p>
  {swap_card("A", PA, PB)}
  {swap_card("B", PB, PA)}
</div>

<div class="page">
  <div class="poster">
    <h1>Read it twice.</h1>
    <div class="ops">
      <div style="background:var(--green-soft)"><b>abc</b>Spelling<br>definitely, until</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>⇄</b>Mix-ups<br>there / their, should have</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>✓</b>Grammar<br>each has, I saw</div>
      <div style="background:var(--green-soft)"><b>.,'</b>Punctuation<br>full stops, capitals</div>
    </div>
    <p style="text-align:center;font-size:18pt!important;font-weight:800;margin:4mm 0">Once for sense. Once for slips.</p>
    <p style="text-align:center;font-size:10pt;color:var(--muted)">Léim · leim.ie · Play Proofread Patrol: {GAME}</p>
  </div>
</div>

<div class="page ws">
  <div class="band"><div><div class="k">Worksheet · exam-style questions</div><h1>Error Hunt</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Error Hunt</h2>
  <p>Each line has one slip. Say what's wrong and write the correct version.</p>
  <table class="eh"><thead><tr><th>Line</th><th>What's wrong and the fix</th></tr></thead><tbody>
  {"".join(f"<tr><td style='font-weight:500'>{s}</td><td><span class='gap'></span><span class='gap'></span></td></tr>" for s, r, m in FIX)}
  </tbody></table>
  <h2>B. Exam-style questions: a report for the local paper</h2>
  <div class="pass">{shown(EXP)}</div>
  <ol class="q">
    <li>The report has five slips. Find each one and write the correction.<span class="long"></span><span class="long"></span></li>
    <li>For two of your corrections, explain the rule in one sentence.<span class="long"></span><span class="long"></span></li>
    <li>Add a pair of brackets to this sentence: <i>The rescue boat a gift from a local family was launched in 2019.</i><span class="long"></span></li>
    <li>Rewrite the second sentence so that it starts in a different way and gives more detail.<span class="long"></span></li>
    <li>The report ends flatly. Redraft the last sentence into a stronger ending of two sentences.<span class="long"></span><span class="long"></span></li>
  </ol>
</div>

<div class="page an">
  <div class="band"><div><div class="k">For the teacher</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>Slip Sort (S = spelling, M = mix-up word, G = grammar)</h2>
  <p style="font-size:8.6pt">{cards_key}</p>
  <h2>Editor's Desk</h2>
  <p style="font-size:9pt"><b>A:</b> {fixlist(PA)}. <b>B:</b> {fixlist(PB)}.</p>
  <h2>A. Error Hunt</h2>
  <table><tbody>{"".join(f"<tr><td style='width:38%'>{s}</td><td>{r}</td></tr>" for s, r, m in FIX)}</tbody></table>
  <h2>B. Exam-style questions</h2>
  <ol class="q">
    <li>{fixlist(EXP)}.</li>
    <li>For example: <i>each</i> means one, so the verb is singular (<i>was</i>); people can be counted, so <i>fewer</i>.</li>
    <li><i>The rescue boat (a gift from a local family) was launched in 2019.</i></li>
    <li>For example: <i>Despite grey skies and a stiff breeze, hundreds of families queued along the pier.</i></li>
    <li>Reward a clear, confident close that looks forward or echoes the opening, e.g. <i>The crew hope next year will bring calmer seas. Either way, the doors of Kilmore Quay will be open.</i></li>
  </ol>
  <h2>Marking tip</h2>
  <p>In the exam, spelling, grammar and punctuation are rewarded as part of the overall accuracy of each written answer rather than as a separate question. Our guide, not an official marking scheme.</p>
</div>
</body></html>"""
assert brk_ok("The rescue boat (a gift from a local family) was launched in 2019.", "The rescue boat [a gift from a local family] was launched in 2019.")

cover = """<!doctype html><html><head><meta charset="utf-8"><style>
body{margin:0;width:1200px;height:1200px;background:#1B2430;font-family:Inter,sans-serif;color:#fff;display:flex;flex-direction:column;justify-content:space-between;padding:90px;box-sizing:border-box}
.k{display:inline-block;background:#2E7D57;border-radius:99px;padding:12px 26px;font-weight:700;font-size:28px;letter-spacing:.06em;text-transform:uppercase}
h1{font-size:96px;font-weight:800;line-height:1.25;letter-spacing:-.02em;margin:60px 0 20px}
h1 span{background:#F6CF5A;color:#1B2430;padding:0 18px;border-radius:14px}
.sub{font-size:40px;line-height:1.4;color:#DDE3EA}
.em{font-size:46px;margin-top:30px;font-weight:800;letter-spacing:.01em;color:#F6CF5A}
.foot{display:flex;justify-content:space-between;align-items:center;font-size:34px;font-weight:700}
.price{background:#F6CF5A;color:#1B2430;border-radius:16px;padding:14px 28px}
</style></head><body>
<div><span class="k">Junior Cycle English · Teacher pack</span>
<h1><span>Editing &amp;</span><br><span>redrafting</span></h1>
<div class="sub">Slip Sort · Editor's Desk A/B<br>Poster · Worksheet + answers</div>
<div class="em">proofreading your own work<br>fewer / less · who / whom</div></div>
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
    pdf("teacher-pack", os.path.join(OUT, "Editing-Redrafting-Teacher-Pack-Leim.pdf"))
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--hide-scrollbars", "--window-size=1200,1200",
                    f"--screenshot={os.path.join(OUT, f'{SLUG}-cover.png')}", f"{SLUG}-cover.html"], cwd=SRC, check=True, capture_output=True)
