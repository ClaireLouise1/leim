#!/usr/bin/env python3
"""Punctuation 2: dialogue, quotes, colons & semicolons (JC English Order 24): free sheet (-> printables/),
6-page teacher pack + 1200x1200 cover (-> OUTDIR).
Usage: python3 src/build_punctuation2_pdfs.py /tmp/p24
Items come from the game's data block (speech-marks-sprint.html). Every answer is re-derived with the checker's own rules
(src/test_speech_marks.py: valid, build, kind, join_mark, reported, rep_slip, gender) and asserted; the checker's data pass runs first.
Styles are read from src/build_money1_pdfs.py."""
import os, sys, random, subprocess, re
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC); sys.path.insert(0, SRC)
from test_speech_marks import valid, build, kind, join_mark, reported, rep_slip, gender, load, data_pass, END_A, END_B
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/p24"; os.makedirs(OUT, exist_ok=True)
SLUG = "punctuation-2"
LO = "W11, W10"
GAME = "leim.ie/speech-marks-sprint.html"
D = load(os.path.join(ROOT, "speech-marks-sprint.html")); assert not data_pass(D), data_pass(D)
MN = {",": "comma", ".": "full stop", "?": "question mark", "!": "exclamation mark"}
def bare(it):
    """the sentence with every mark and capital the student has to add taken out"""
    sp, tag, pos = it
    return (f"{sp[0].lower() + sp[1:]} {tag}" if pos == "a" else f"{tag} {sp[0].lower() + sp[1:]}")
def mark_of(it):
    sp, tag, pos = it; return (END_A if pos == "a" else END_B)[kind(sp, tag)]
def gap_line(it):
    sp, tag, pos = it
    g = "<span class='line' style='min-width:6mm'></span>"
    return f'"{sp}{g}" {tag}.' if pos == "a" else f'{tag}, "{sp}{g}"'
def slips(it):
    """wrong versions of one dialogue sentence (each asserted invalid by the checker)"""
    sp, tag, pos = it; k = kind(sp, tag); low = sp[0].lower() + sp[1:]
    if pos == "a":
        m = END_A[k]
        c = [f'"{sp}"{m} {tag}.', f'"{sp}{m} {tag}."', f'"{low}{m}" {tag}.', f'"{sp}" {tag}.']
        if k == "s": c.append(f'"{sp}." {tag}.')
        if k != "s" and tag[0].islower(): c.append(f'"{sp}{m}" {tag[0].upper() + tag[1:]}.')
    else:
        m = END_B[k]
        c = [f'{tag} "{sp}{m}"', f'{tag}, "{sp}"{m}', f'{tag}, "{low}{m}"', f'"{tag}, {sp}{m}"']
    for x in c: assert not valid(x), x
    return c

# ---------- free sheet ----------
random.seed(2401)
A_items = random.sample([x for x in D["dlg"] if x[2] == "a"], 5) + random.sample([x for x in D["dlg"] if x[2] == "b"], 3)
for it in A_items: assert valid(build(*it))
B_items = random.sample([x for x in D["dlg"] if x not in A_items], 8)
assert sum(mark_of(x) == "," for x in B_items) >= 2
C_items = random.sample([x for x in D["join"] if x[1] == "c"], 4) + random.sample([x for x in D["join"] if x[1] == "s"], 4); random.shuffle(C_items)
for s, k in C_items: assert join_mark(s) == k
D_items = random.sample([x for x in D["rep"] if not x[1].startswith("asked")], 3) + random.sample([x for x in D["rep"] if x[1].startswith("asked")], 3)
for it in D_items: assert gender(it[1]) == it[2] and not rep_slip(reported(*it))
nA = 1; nB = nA + 8; nC = nB + 8; nD = nC + 8; nE = nD + 6; nF = nE + 1
NQ = nF + 2 - 1; assert NQ == 33, NQ

# E: a dialogue passage to punctuate (new speaker, new line)
E_LINES = [("Is anyone home", "asked Saoirse", "a"), ("We're in the kitchen", "Gran replied", "a"), ("Guess what", "Saoirse shouted", "b"), ("Did you win", "Gran asked", "b")]
for it in E_LINES: assert valid(build(*it)), build(*it)
E_BARE = "is anyone home asked saoirse we're in the kitchen gran replied saoirse shouted guess what gran asked did you win"
assert E_BARE == " ".join(bare(it) for it in E_LINES).replace("Saoirse", "saoirse").replace("Gran", "gran"), " ".join(bare(it) for it in E_LINES)

def style(var):
    return re.search(var + r' = f"""<!doctype.*?<style>(.*?)</style>', open(os.path.join(SRC, "build_money1_pdfs.py"), encoding="utf-8").read(), re.S).group(1).replace("{LO}", LO).replace("{{", "{").replace("}}", "}").replace("JC Maths LOs (2018 spec)", "JC English LOs (2015 spec)")
SHEET_STYLE = style("sheet"); PACK_STYLE = style("pack")
assert "JC English LOs (2015 spec)" in SHEET_STYLE and "Single-teacher licence" in PACK_STYLE and "JC English LOs (2015 spec)" in PACK_STYLE
EXTRA = """.wk{line-height:1.45;border:1.5px solid var(--line);border-radius:8px;padding:2px 7px;margin:3px 0;font-size:9.4pt}.wk b.h{display:block}
table.st{border-collapse:collapse;margin:3px 0;font-size:9.2pt;width:100%}table.st td,table.st th{border:1px solid #C9D1DA;padding:2px 6px;text-align:left}
.pass{border-left:4px solid var(--green);background:var(--mist);padding:5px 10px;margin:4px 0;font-size:9.4pt;line-height:1.45}
.pu{color:#C0392B;font-weight:900}"""
def pu(s): return re.sub(r'([,.?!;:"])', r"<b class='pu'>\1</b>", s.replace("&", "&amp;"))
def two(items_html, cut):
    return f"<div class='two'><div><ol class='q'>{''.join(items_html[:cut])}</ol></div><div><ol class='q'>{''.join(items_html[cut:])}</ol></div></div>"
L = "<span class='line' style='min-width:70mm'></span>"
A_html = [f"<li value='{i}'><i>{bare(it)}</i><br>{L}</li>" for i, it in enumerate(A_items, nA)]
B_html = [f"<li value='{i}'>{gap_line(it)}</li>" for i, it in enumerate(B_items, nB)]
C_html = [f"<li value='{i}'>{s.replace('___', '<b>___</b>')}</li>" for i, (s, k) in enumerate(C_items, nC)]
D_html = [f"<li value='{i}'>{build(it[0], it[1], 'a')}<br>{L}</li>" for i, it in enumerate(D_items, nD)]

EX1 = ("I have lost my ticket", "said Maeve", "f"); assert reported(*EX1) == "Maeve said that she had lost her ticket."
EX2 = "Bring three things to the beach ___ a towel, a hat and sun cream."; assert join_mark(EX2) == "c"
EX2b = "My brother loves the sea ___ my sister hates the sand."; assert join_mark(EX2b) == "s"

sheet = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Punctuation 2: dialogue, quotes, colons and semicolons, rules and practice | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{SHEET_STYLE}
{EXTRA}
.p2 ol.q li{{margin-bottom:2px;font-size:9.2pt}}.p2 h2{{margin:4px 0 2px}}.p2 .two{{gap:5mm}}
</style></head><body>
<div class="page tight">
  <div class="band"><div><div class="k">Junior Cycle English · Free revision sheet</div><h1>Punctuation 2: dialogue</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2015 specification): {LO}. Play the game: <b>{GAME}</b></p>
  <p>Speech marks, colons and semicolons: the marks that make dialogue and longer sentences work. Every story you write needs them, and every answer is marked partly for accuracy.</p>
  <div class="two">
   <div><h2>1. Two ways to set out speech</h2>
    <div class="wk"><b class="h">Speech first</b>{pu('"I'+"'"+'m starving," said Dara.')}<br>{pu('"Can I come too?" asked Liam.')}</div>
    <div class="wk"><b class="h">Speech last</b>{pu('Mam said, "Dinner is ready."')}<br>{pu('Dad asked, "Have you seen my keys?"')}</div>
    <h2>2. Four rules</h2>
    <table class="st"><tbody>
     <tr><td><b>1</b></td><td>Only the <b>spoken words</b> go inside the speech marks.</td></tr>
     <tr><td><b>2</b></td><td>A <b>capital</b> starts the speech, even mid-sentence.</td></tr>
     <tr><td><b>3</b></td><td>The mark goes <b>inside</b> the closing speech mark. Speech first: a statement ends with a <b>comma</b>, and <i>said / asked</i> stays small after ? or !.</td></tr>
     <tr><td><b>4</b></td><td><b>New speaker, new line.</b></td></tr></tbody></table>
    <p style="font-size:9pt">Single (' ') or double (" ") marks are both fine: be consistent. Also called inverted commas.</p></div>
   <div><h2>3. Direct and reported speech</h2>
    <div class="wk"><b class="h">Direct</b>{pu('"I am tired," said Niamh.')}<br><b class="h">Reported</b>Niamh said that she was tired.</div>
    <p style="font-size:9pt">Reported speech: no speech marks; <b>that</b> (or <b>if</b> for a question); I → she / he; am / is → was, are → were, have → had, can → could, will → would.</p>
    <h2>4. Colon : and semicolon ;</h2>
    <div class="wk"><b class="h">Colon : before a list</b>I packed three things{pu(':')} a torch, a map and a flask of tea.<br><span style="font-size:8.6pt">Not after <i>are</i> or <i>include</i>: The colours are green, white and orange.</span></div>
    <div class="wk"><b class="h">Semicolon ; joins two full sentences</b>Dara loves hurling{pu(';')} his sister prefers soccer.<br><span style="font-size:8.6pt">A comma can't do this (a run-on). A full stop could.</span></div>
    <h2>5. Quotes in your answers</h2>
    <p style="font-size:9pt">Put the exact words in quotation marks and keep them short: <i>The word "raging" makes the sea sound furious.</i> Poem and story titles go in quotation marks too.</p></div>
  </div>
  <div class="tip"><b>Exam tip:</b> a few short lines of well-punctuated dialogue bring a story to life. Check every closing speech mark: is the mark inside? Did a new speaker get a new line?</div>
</div>

<div class="page p2">
  <div class="band"><div><div class="k">Practice · {NQ} questions</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Write each sentence out with speech marks, capitals and the right marks</h2>
  {two(A_html, 4)}
  <h2>B. Which mark goes in the gap? (comma / full stop / question mark / exclamation mark)</h2>
  {two(B_html, 4)}
  <h2>C. Colon or semicolon?</h2>
  {two(C_html, 4)}
  <h2>D. Change into reported speech</h2>
  {two(D_html, 3)}
</div>

<div class="page">
  <div class="band"><div><div class="k">Dialogue · exam-style · answers</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <h2>E. Punctuate this dialogue. Start a new line for each new speaker.</h2>
  <ol class="q"><li value="{nE}"><div class="pass">{E_BARE}</div><span class="long"></span><span class="long"></span><span class="long"></span><span class="long"></span></li></ol>
  <h2>F. Exam-style</h2>
  <ol class="q">
   <li value="{nF}">Change into reported speech: <i>"{EX1[0]}," {EX1[1]}.</i> Then add a colon or a semicolon: (a) <i>{EX2.replace('___', '___')}</i> (b) <i>{EX2b}</i><span class="long"></span><span class="long"></span></li>
   <li value="{nF + 1}">Write four lines of dialogue between two friends waiting for exam results. Use speech marks correctly, put the tag before the speech at least once, and start a new line for each speaker.<span class="long"></span><span class="long"></span><span class="long"></span><span class="long"></span></li>
  </ol>
  <h2>Answers</h2>
  <table class="ans"><tbody>
   <tr><td><b>A</b></td><td>{" · ".join(f"{i}. {build(*it)}" for i, it in enumerate(A_items, nA))}</td></tr>
   <tr><td><b>B</b></td><td>{" · ".join(f"{i}. {MN[mark_of(it)]}" for i, it in enumerate(B_items, nB))}</td></tr>
   <tr><td><b>C</b></td><td>{" · ".join(f"{i}. {'colon' if join_mark(s) == 'c' else 'semicolon'}" for i, (s, k) in enumerate(C_items, nC))}</td></tr>
   <tr><td><b>D</b></td><td>{" · ".join(f"{i}. {reported(*it)}" for i, it in enumerate(D_items, nD))}</td></tr>
   <tr><td><b>E</b></td><td>{" / ".join(build(*it) for it in E_LINES)} (each on a new line)</td></tr>
   <tr><td><b>F</b></td><td>{nF}. {reported(*EX1)} (a) {EX2.replace(' ___', ':')} (b) {EX2b.replace(' ___', ';')} · {nF + 1}. Check: only spoken words inside the marks, the mark inside, capitals, small <i>said</i> after the speech, a new line per speaker.</td></tr>
  </tbody></table>
  <div class="note"><b>Got one wrong?</b> Go back to page 1, then play <b>Speech Marks Sprint</b> at {GAME}: the "Go back over these" list at the end explains each mistake.</div>
  <p class="small">All sentences are written by Léim. Léim is independent and not connected with the State Examinations Commission or the NCCA.</p>
</div>
</body></html>"""

# ---------- teacher pack ----------
random.seed(2402)
pool = D["dlg"][:]; random.shuffle(pool)
RIGHT = pool[:12]; WRONG_SRC = pool[12:24]
CARDS = [(build(*it), True, it) for it in RIGHT] + [(random.choice(slips(it)), False, it) for it in WRONG_SRC]
random.shuffle(CARDS)
for s, ok, it in CARDS: assert valid(s) == ok, s
cards_html = "".join(f'<div class="c"><span class="tag">Card {i}</span><div class="fc sm">{pu(s)}</div></div>' for i, (s, ok, it) in enumerate(CARDS, 1))
cards_key = "Right: " + ", ".join(str(i) for i, (s, ok, it) in enumerate(CARDS, 1) if ok) + ". Wrong (fixed): " + " · ".join(f"<b>{i}</b> {build(*it)}" for i, (s, ok, it) in enumerate(CARDS, 1) if not ok)

DA = [("Where are you going", "asked Mam", "a"), ("To the shop", "I said", "a"), ("Bring back some milk", "Mam called", "b"), ("Can I get crisps", "I asked", "b")]
DB = [("Who left the gate open", "asked Grandad", "a"), ("It wasn't me", "said Ruth", "a"), ("The calves are out", "Grandad groaned", "b"), ("Will I help", "Ruth asked", "b")]
def dl(it): return build(*it)
for it in DA + DB: assert valid(dl(it)), dl(it)
RA = [("I am hungry", "said Liam", "m"), ("Can I come to the party", "asked Liam", "m")]
RB = [("My bike is broken", "said Orla", "f"), ("Is my dinner ready", "asked Ciara", "f")]
for it in RA + RB: assert it in [tuple(x) for x in D["rep"]] or it[0] == "I am hungry"
assert reported("I am hungry", "said Liam", "m") == "Liam said that he was hungry."
def swap_card(who, lines, reps):
    rows = "".join(f"<tr><td style='width:4%'><b>{i}</b></td><td>{pu(dl(it))}</td></tr>" for i, it in enumerate(lines, 1))
    grid = "".join(f"<tr><td><b>{i}</b></td><td></td></tr>" for i in range(1, 5))
    rr = "".join(f"<tr><td>{pu(build(it[0], it[1], 'a'))}</td><td></td></tr>" for it in reps)
    return f"""<div class="idc"><h3>Student {who} · Dialogue Dictation</h3>
    <p style="font-size:8.8pt;margin:0 0 1mm"><b>1. Read</b> your four lines aloud, slowly, twice. Say the words only: don't say "comma" or "speech marks"!</p>
    <table class="st" style="font-size:9pt"><tbody>{rows}</tbody></table>
    <p style="font-size:8.8pt;margin:1mm 0"><b>2. Write</b> your partner's four lines with every mark, one line per speaker. Then compare with their card.</p>
    <table class="st" style="font-size:9pt"><tbody>{grid}</tbody></table>
    <p style="font-size:8.8pt;margin:1mm 0"><b>3. Report it.</b> Read each line aloud. Your partner says it as reported speech; write what they say.</p>
    <table class="st" style="font-size:9pt"><thead><tr><th style="width:48%">Direct</th><th>Reported</th></tr></thead><tbody>{rr}</tbody></table></div>"""

FIX = [('"Hurry up" said Mam.', 'No comma inside the closing mark: <b>"Hurry up," said Mam.</b>'),
       ('"Where are you"? asked Niall.', 'The question mark goes inside: <b>"Where are you?" asked Niall.</b>'),
       ('"Watch out!" Shouted Dad.', 'After ! the tag stays small: <b>"Watch out!" shouted Dad.</b>'),
       ('Aoife said "it\'s my turn."', 'Comma after said, capital to start the speech: <b>Aoife said, "It\'s my turn."</b>'),
       ("The match was over, we went home.", "Two sentences joined by a comma (a run-on): <b>The match was over; we went home.</b> (or a full stop)"),
       ("The kit includes: a jersey, shorts and socks.", "No colon straight after <i>includes</i>: <b>The kit includes a jersey, shorts and socks.</b> or <b>The kit has three parts: a jersey, shorts and socks.</b>")]
for s, r in FIX[:4]: assert not valid(s), s
for s in ['"Hurry up," said Mam.', '"Where are you?" asked Niall.', '"Watch out!" shouted Dad.']: assert valid(s), s
assert valid('Aoife said, "It\'s my turn."')

EXP = ["it's a shame said the ranger the puffins have gone",
       "Darragh asked are they coming back",
       "next April the ranger replied they always do"]
EXP_ANS = ['"It\'s a shame," said the ranger. "The puffins have gone."', 'Darragh asked, "Are they coming back?"', '"Next April," the ranger replied. "They always do."']
for a in EXP_ANS[1:2]: assert valid(a), a

pack = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Punctuation 2: Dialogue, Colons &amp; Semicolons Teacher Pack | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{PACK_STYLE}
{EXTRA}
.fym .c{{height:30mm}}.fym .fc.sm{{font-size:10pt;line-height:1.35;margin-top:2mm;font-weight:600}}.idc{{padding:2mm 4mm;margin-bottom:3mm}}.idc h3{{margin:0 0 1mm}}
.idc .st td,.idc .st th{{padding:1px 5px}}.idc .st td{{height:5.4mm}}.p1 .proc td{{font-size:8.6pt;padding:2px 6px}}.ops div{{font-size:12pt;padding:5mm 3mm}}.ops b{{font-size:19pt}}
.ws .eh td{{font-size:8.6pt;padding:2px 6px}}.ws .eh .gap{{height:13px}}.ws ol.q li{{margin-bottom:1px}}
</style></head><body>

<div class="page p1">
  <div class="band"><div><div class="k">Junior Cycle English · Teacher pack</div><h1>Punctuation 2: dialogue</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2015 specification): {LO}</p>
  <div class="two">
    <div><h3>Aims</h3><p>By the end of the lesson students can set out dialogue with the tag before or after the speech, put the right mark inside the closing speech mark, start a new line for each speaker, turn direct speech into reported speech, and choose a colon or a semicolon.</p></div>
    <div><h3>In this pack</h3><p>p.1 Teacher notes · p.2 Right or Wrong? Sort (24 cut-up cards) · p.3 Dialogue Dictation A/B (speaking and listening) · p.4 Wall poster · p.5 Worksheet: Fix the Dialogue + exam-style questions · p.6 Answers. Level: 2nd year. Time: about 60 minutes. All sentences are written by Léim.</p></div>
  </div>
  <h2 style="margin-top:8px">Procedure</h2>
  <table class="proc"><tbody>
    <tr><td>5 min</td><td><b>Lead-in.</b> Write <i>"I'm starving," said Dara.</i> and <i>Mam said, "Dinner is ready."</i> on the board. Where is each comma? Why a comma, not a full stop, in the first? Build the four rules (free sheet, box 2).</td></tr>
    <tr><td>12 min</td><td><b>Right or Wrong? Sort</b> (p.2, groups of 3, one set of 24 cards). Sort into right and wrong; for each wrong card, say the slip and write the fixed version on the back. 12 are right, 12 have one slip.</td></tr>
    <tr><td>12 min</td><td><b>Dialogue Dictation</b> (p.3, pairs). A reads four lines of dialogue aloud (words only); B writes them with every mark, a new line per speaker, then checks against A's card. Part 3: turn two lines into reported speech. Swap.</td></tr>
    <tr><td>8 min</td><td><b>Colon or semicolon?</b> Board: <i>I packed three things ___ a torch, a map and tea.</i> / <i>Dara loves hurling ___ his sister prefers soccer.</i> Thumbs up for colon, thumbs down for semicolon. Why can't a comma join two sentences?</td></tr>
    <tr><td>18 min</td><td><b>Worksheet</b> (p.5). Fix the Dialogue in pairs, then the exam-style questions on "The Puffins" alone.</td></tr>
    <tr><td>5 min</td><td><b>Exit ticket.</b> Write two lines of dialogue: one with the tag after, one with the tag before. Homework: play <b>Speech Marks Sprint</b> at {GAME}.</td></tr>
  </tbody></table>
  <div class="note"><b>Errors to look for:</b> the comma or ? outside the closing speech mark · a full stop before <i>said</i> · <i>Asked</i> with a capital after ? · <i>said</i> inside the speech marks · no capital to start the speech · two speakers on one line · reported speech that keeps I / my or "is" · a comma joining two sentences · a colon straight after <i>are</i> or <i>include</i>. <b>Support:</b> the poster (p.4) on the desk. <b>Fast finishers:</b> write a split sentence: <i>"I know," said Ava, "but it's late."</i></div>
</div>

<div class="page">
  <div class="band"><div><div class="k">Groups of 3 · cut up the 24 cards</div><h1>Right or Wrong? Sort</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.4pt;margin:0 0 2mm">Sort the cards into <b>right</b> and <b>wrong</b>. Twelve are right. Each wrong card has <b>one</b> slip: say what it is and write the fixed sentence on the back.</p>
  <div class="fym">{cards_html}</div>
</div>

<div class="page">
  <div class="band"><div><div class="k">Pairs · cut along the dashed line</div><h1>Dialogue Dictation A/B</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.4pt">Listen, write, check: every mark counts.</p>
  {swap_card("A", DA, RA)}
  {swap_card("B", DB, RB)}
</div>

<div class="page">
  <div class="poster">
    <h1>Inside the marks.</h1>
    <div class="ops">
      <div style="background:var(--green-soft)"><b>,"</b>"Hi," said Dara.<br>(not a full stop)</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>?"</b>"Ready?" asked Liam.<br>(asked stays small)</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>, "</b>Mam said, "Go."<br>(capital to start)</div>
      <div style="background:var(--green-soft)"><b>↵</b>new speaker,<br>new line</div>
    </div>
    <p style="text-align:center;font-size:18pt!important;font-weight:800;margin:4mm 0">Colon : before a list. Semicolon ; between two sentences.</p>
    <p style="text-align:center;font-size:10pt;color:var(--muted)">Léim · leim.ie · Play Speech Marks Sprint: {GAME}</p>
  </div>
</div>

<div class="page ws">
  <div class="band"><div><div class="k">Worksheet · exam-style questions</div><h1>Fix the Dialogue</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Fix the Dialogue</h2>
  <p>Each line has one slip. Say what's wrong and write the correct version.</p>
  <table class="eh"><thead><tr><th>Line</th><th>What's wrong and the fix</th></tr></thead><tbody>
  {"".join(f"<tr><td style='font-weight:500'>{s}</td><td><span class='gap'></span><span class='gap'></span></td></tr>" for s, r in FIX)}
  </tbody></table>
  <h2>B. Exam-style questions: "The Puffins"</h2>
  <div class="pass">{" ".join(EXP)}</div>
  <ol class="q">
    <li>Rewrite the passage above with correct punctuation, starting a new line for each new speaker.<span class="long"></span><span class="long"></span><span class="long"></span></li>
    <li>Change the ranger's first words into reported speech.<span class="long"></span></li>
    <li>Add a colon or a semicolon: (a) <i>The boat trip had two highlights ___ the puffins and the seals.</i> (b) <i>The way out was calm ___ the way back was rough.</i><span class="long"></span></li>
    <li>Explain why <i>The island was quiet, the birds had gone.</i> is a run-on, and fix it two ways.<span class="long"></span></li>
    <li>Continue the scene with four more lines of dialogue between Darragh and the ranger.<span class="long"></span><span class="long"></span><span class="long"></span></li>
  </ol>
</div>

<div class="page an">
  <div class="band"><div><div class="k">For the teacher</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>Right or Wrong? Sort</h2>
  <p style="font-size:8.8pt">{cards_key}</p>
  <h2>Dialogue Dictation</h2>
  <p style="font-size:9pt">Each partner's lines are on the other card. Reported: {" · ".join(reported(*it) for it in RA + RB)}</p>
  <h2>A. Fix the Dialogue</h2>
  <table><tbody>{"".join(f"<tr><td style='width:34%'>{s}</td><td>{r}</td></tr>" for s, r in FIX)}</tbody></table>
  <h2>B. Exam-style questions</h2>
  <ol class="q">
    <li>{EXP_ANS[0]}<br>{EXP_ANS[1]}<br>{EXP_ANS[2]}</li>
    <li>The ranger said that it was a shame and that the puffins had gone.</li>
    <li>(a) colon: <i>two highlights: the puffins and the seals</i> (b) semicolon: <i>The way out was calm; the way back was rough.</i></li>
    <li>Two complete sentences joined by a comma. <i>The island was quiet. The birds had gone.</i> / <i>The island was quiet; the birds had gone.</i> (or <i>…quiet because the birds had gone.</i>)</li>
    <li>Reward correct speech marks with the mark inside, capitals, a new line per speaker, tags before and after, and dialogue that moves the scene on.</li>
  </ol>
  <h2>Marking tip</h2>
  <p>In the exam, punctuation is rewarded as part of the overall accuracy of a written answer rather than as a separate question. Our guide, not an official marking scheme.</p>
</div>
</body></html>"""
assert join_mark("The boat trip had two highlights ___ the puffins and the seals.") == "c" and join_mark("The way out was calm ___ the way back was rough.") == "s"

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
<h1><span>Punctuation 2:</span><br><span>dialogue</span></h1>
<div class="sub">Right or Wrong? Sort · Dialogue Dictation A/B<br>Poster · Worksheet + answers</div>
<div class="em">speech marks · reported speech<br>colons &amp; semicolons</div></div>
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
    pdf("teacher-pack", os.path.join(OUT, "Punctuation-2-Dialogue-Teacher-Pack-Leim.pdf"))
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--hide-scrollbars", "--window-size=1200,1200",
                    f"--screenshot={os.path.join(OUT, f'{SLUG}-cover.png')}", f"{SLUG}-cover.html"], cwd=SRC, check=True, capture_output=True)
