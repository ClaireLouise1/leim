#!/usr/bin/env python3
"""Exam technique & exam mix (JC English Order 32): free sheet (-> printables/), 6-page teacher pack + 1200x1200 cover (-> OUTDIR).
Usage: python3 src/build_exam_technique_pdfs.py /tmp/p32
Reads the game's data block (english-exam-mix.html) and re-checks every answer with the checker's own functions
(src/test_english_exam_mix.py: command, form, data_pass); every time and mark is computed with Fractions and asserted.
Styles are read from src/build_money1_pdfs.py."""
import os, sys, random, subprocess, re
from fractions import Fraction as Fr
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC); sys.path.insert(0, SRC)
from test_english_exam_mix import load, data_pass, command, form, LAB, FLAB
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/p32"; os.makedirs(OUT, exist_ok=True)
SLUG = "exam-technique-exam-mix"
LO = "R3, R7, W1, W3, W4, W11"
GAME = "leim.ie/english-exam-mix.html"
D = load(os.path.join(ROOT, "english-exam-mix.html")); assert not data_pass(D)
MIN, MARKS = D["paper"]["min"], D["paper"]["marks"]; assert (MIN, MARKS) == (120, 180)
def mins(m):
    t = Fr(m * MIN, MARKS); assert t.denominator == 1, m; return int(t)
JOB = {k: re.sub(r"^\S+ ", "", v) for k, v in LAB.items()}          # labels without the emoji (no emoji in PDFs)
FORMN = {k: re.sub(r"^\S+ ", "", v) for k, v in FLAB.items()}
KEYS = ["find", "desc", "expl", "comp", "opin", "sum"]; LET = "abcdef"
JOBLONG = {"find": "find it in the text: short and exact", "desc": "say what it is like, with details", "expl": "say why or how, and back it up",
           "comp": "show how they are alike AND different", "opin": "give your view clearly, then reasons", "sum": "give the main points only, short"}

def style(var):
    return re.search(var + r' = f"""<!doctype.*?<style>(.*?)</style>', open(os.path.join(SRC, "build_money1_pdfs.py"), encoding="utf-8").read(), re.S).group(1).replace("{LO}", LO).replace("{{", "{").replace("}}", "}").replace("JC Maths LOs (2018 spec)", "JC English LOs (2015 spec)")
SHEET_STYLE = style("sheet"); PACK_STYLE = style("pack")
assert "JC English LOs (2015 spec)" in SHEET_STYLE and "Single-teacher licence" in PACK_STYLE and "JC English LOs (2015 spec)" in PACK_STYLE
EXTRA = """.wk{line-height:1.4;border:1.5px solid var(--line);border-radius:8px;padding:2px 7px;margin:3px 0;font-size:9.2pt}.wk b.h{display:block}
table.st{border-collapse:collapse;margin:3px 0;font-size:9pt;width:100%}table.st td,table.st th{border:1px solid #C9D1DA;padding:2px 6px;text-align:left;vertical-align:top}
.pass{border-left:4px solid var(--green);background:var(--mist);padding:5px 10px;margin:4px 0;font-size:9.3pt;line-height:1.5}
.pass .sp{display:block;margin:1px 0}.qt{font-family:Georgia,serif;font-style:italic}.tc{border:1.5px solid var(--line);border-radius:8px;padding:3px 8px;margin:3px 0;font-size:9.2pt;line-height:1.45}.tc .k{font-size:8pt;font-weight:700;color:var(--muted)}"""
L = "<span class='line' style='min-width:22mm'></span>"
def li(i, s): return f"<li value='{i}'>{s}</li>"
def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;")
def cw(q):
    """underline the opening command word(s), as found by the checker"""
    k, why = command(q); assert k, (q, why)
    m = re.match(r"(Identify|Name|List|Write down|Pick out|Find|Describe|Explain|Compare|Contrast|Do you agree|Do you think|Would you|Which|In your opinion|Summarise|Sum up)", q)
    return f"<u>{esc(m.group(0))}</u>{esc(q[m.end():])}", k
TIME_TAB = [15, 21, 30, 45, 60, 90]

# ---------- free sheet ----------
rng = random.Random(3201)
A_marks = rng.sample([6, 9, 12, 18, 24, 27, 36, 45, 60], 6)
A_items = [(m, mins(m)) for m in A_marks]
by = {k: [q for q, kk in D["cmd"] if kk == k] for k in KEYS}
B_items = []
for k in rng.sample(KEYS, 6) + rng.sample(KEYS, 2):
    q = rng.choice([x for x in by[k] if x not in [b[0] for b in B_items]]); B_items.append((q, k))
rng.shuffle(B_items)
for q, k in B_items: assert command(q)[0] == k
C_items = rng.sample([t for t in D["task"] if t[2]], 4)
for t, k, r in C_items: assert form(t) == k and r in t
nA = 1; nB = nA + 6; nC = nB + 8; nD = nC + 4; nE = nD + 2; NQ = nE + 1; assert NQ == 22, NQ
WEAK = [("How does Seán feel at the end of the extract? (10 marks)", "Seán goes home and talks to his mam. Then he goes to bed.",
         "It retells the story. It never names a feeling and never uses the text.",
         "At the end, Seán feels relieved: he “let out a long breath” when his mam hugged him, which shows the worry has gone."),
        ("Compare the openings of the two stories. (15 marks)", "The first story opens on a beach. It is very exciting and the writer uses short sentences.",
         "It only talks about ONE story. A comparison needs both, in every point.",
         "Both stories open with a mystery, but the first one is set on a busy beach while the second starts alone in a dark house, so it feels more tense.")]
SEC = [("A", "Reading", 30), ("A", "Reading", 30), ("B", "Studied texts", 45), ("C", "Writing", 75)]
assert sum(m for *_, m in SEC) == MARKS
ESEC = [(n, mins(m)) for n, (_, _, m) in enumerate(SEC)]

sheet = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Exam technique and exam mix, tips and practice | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{SHEET_STYLE}
{EXTRA}
.p2 ol.q li{{margin-bottom:2px;font-size:9pt}}.p2 h2{{margin:4px 0 2px}}.p2 .two{{gap:6mm}}.p2 .tc{{font-size:8.6pt;line-height:1.33;margin:2px 0}}
</style></head><body>
<div class="page tight">
  <div class="band"><div><div class="k">Junior Cycle English · Free revision sheet</div><h1>Exam technique</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2015 specification): {LO}. Play the game: <b>{GAME}</b></p>
  <p>The Junior Cycle English exam is <b>one paper, 2 hours, 180 marks</b>, at Higher and at Ordinary level. Every question links to the paper's <b>theme</b>, and the sections and marks change from year to year. You can't learn the paper off, but you can learn <b>how to read a question</b> and <b>how to use your time</b>.</p>
  <div class="two">
   <div><h2>1. Command words: the first word is the job</h2>
    <table class="st"><thead><tr><th></th><th>The question says…</th><th>So you…</th></tr></thead><tbody>
     <tr><td>a</td><td>Identify, name, list, write down, pick out, find</td><td>{JOBLONG['find']}</td></tr>
     <tr><td>b</td><td>Describe</td><td>{JOBLONG['desc']}</td></tr>
     <tr><td>c</td><td>Explain, why, how</td><td>{JOBLONG['expl']}</td></tr>
     <tr><td>d</td><td>Compare, contrast</td><td>{JOBLONG['comp']}</td></tr>
     <tr><td>e</td><td>Do you agree, do you think, in your opinion</td><td>{JOBLONG['opin']}</td></tr>
     <tr><td>f</td><td>Summarise, sum up</td><td>{JOBLONG['sum']}</td></tr></tbody></table>
    <h2>2. Read the question twice</h2>
    <ul style="font-size:9.2pt;margin:2px 0 2px 14px;padding:0"><li><b>Underline</b> the command word.</li><li><b>Circle how many</b>: two reasons, three details.</li>
     <li><b>Box the focus</b>: which character, paragraph or feeling.</li><li>“With reference to the text” = <b>point, quote, explain</b>.</li></ul></div>
   <div><h2>3. Time it by the marks</h2>
    <p style="font-size:9.2pt;margin:2px 0">120 minutes ÷ 180 marks = <b>⅔ of a minute (40 seconds) a mark</b>.</p>
    <table class="st"><thead><tr><th>Marks</th>{''.join(f"<th>{m}</th>" for m in TIME_TAB)}</tr></thead><tbody><tr><td><b>Minutes</b></td>{''.join(f"<td>{mins(m)}</td>" for m in TIME_TAB)}</tr></tbody></table>
    <p style="font-size:9.2pt;margin:2px 0">When the time is up, finish your sentence and move on. Use the marks printed on <i>your</i> paper.</p>
    <h2>4. Writing tasks: form, reader, purpose</h2>
    <div class="wk"><b class="h">Write the text of a talk for your class about a place you love.</b>Form: a talk (speak to them, “Thank you for listening”). Reader: your class (friendly, no slang). Purpose: to describe and share.</div>
    <h2>5. Read it back</h2>
    <p style="font-size:9.2pt;margin:2px 0">Keep the last few minutes for missing words, spelling, full stops and capitals.</p></div>
  </div>
  <div class="tip"><b>Exam tip:</b> use the question's own words in your first sentence. It keeps you on the question, and the examiner sees it straight away.</div>
</div>

<div class="page p2">
  <div class="band"><div><div class="k">Practice · {NQ} questions</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. The paper is 2 hours, 180 marks. About how many minutes should you spend on a question worth…</h2>
  <div class="two"><ol class="q">{''.join(li(i, f"{m} marks? {L} minutes") for i, (m, t) in enumerate(A_items[:3], nA))}</ol><ol class="q">{''.join(li(i, f"{m} marks? {L} minutes") for i, (m, t) in enumerate(A_items[3:], nA + 3))}</ol></div>
  <h2>B. What does each question want? Write the letter (a–f) from the table on page 1.</h2>
  <ol class="q">{''.join(li(i, f"{esc(q)} ____") for i, (q, k) in enumerate(B_items, nB))}</ol>
  <h2>C. Writing tasks. Write the form and the reader for each.</h2>
  <ol class="q">{''.join(li(i, f"{esc(t)}<br>Form: {L} Reader: {L}") for i, (t, k, r) in enumerate(C_items, nC))}</ol>
  <h2>D. Why would each answer lose marks? Write a better one.</h2>
  <ol class="q">{''.join(li(i, f"<b>{esc(q)}</b><br>Answer: <span class='qt'>“{esc(a)}”</span><span class='long'></span><span class='long'></span>") for i, (q, a, w, b) in enumerate(WEAK, nD))}</ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">Exam-style · answers</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <h2>E. Exam-style: plan the paper</h2>
  <div class="pass"><b>A made-up paper (2 hours, 180 marks)</b>{''.join(f"<span class='sp'>Question {n + 1} ({s}: {p}): {m} marks</span>" for n, (s, p, m) in enumerate(SEC))}</div>
  <ol class="q">
   <li value="{nE}">Make a time plan: how many minutes for each question? Show how you worked it out.<span class="long"></span><span class="long"></span></li>
   <li value="{nE + 1}">Read this question and say exactly what it asks you to do: <span class="qt">“Explain two ways the writer makes the opening of the story exciting. Support your answer with reference to the text.”</span><span class="long"></span><span class="long"></span><span class="long"></span></li>
  </ol>
  <h2>Answers</h2>
  <table class="ans"><tbody>
   <tr><td><b>A</b></td><td>{" · ".join(f"{i}. {t} min" for i, (m, t) in enumerate(A_items, nA))} (marks × ⅔)</td></tr>
   <tr><td><b>B</b></td><td>{" · ".join(f"{i}. {LET[KEYS.index(k)]}" for i, (q, k) in enumerate(B_items, nB))}</td></tr>
   <tr><td><b>C</b></td><td>{" · ".join(f"{i}. {FORMN[k].lower()}, {esc(r)}" for i, (t, k, r) in enumerate(C_items, nC))}</td></tr>
   <tr><td><b>D</b></td><td>{" ".join(f"{i}. {esc(w)} <i>Better:</i> {esc(b)}" for i, (q, a, w, b) in enumerate(WEAK, nD))}</td></tr>
   <tr><td><b>E</b></td><td>{nE}. {" · ".join(f"Q{n + 1}: {SEC[n][2]} × ⅔ = {t} min" for n, t in ESEC)} (total {sum(t for n, t in ESEC)} min). In the real exam, keep a few of those minutes at the end to read back.
     {nE + 1}. Command word: <b>explain</b>, so say how, not just what happens. How many: <b>two</b> ways, so two paragraphs. Focus: the <b>opening</b> only, and <b>exciting</b>. Reference: a short <b>quote</b> for each way, then what it does.</td></tr>
  </tbody></table>
  <div class="note"><b>Got one wrong?</b> Go back to page 1, then play <b>English Exam Mix</b> at {GAME}: the “Go back over these” list at the end explains each one.</div>
  <p class="small">All questions are written by Léim in the style of the exam, not taken from past papers. Léim is independent and not connected with the State Examinations Commission or the NCCA.</p>
</div>
</body></html>"""
assert sum(t for n, t in ESEC) == MIN

# ---------- teacher pack ----------
rng = random.Random(3202)
cards = []
for k in KEYS:
    cards += [(q, k) for q in rng.sample(by[k], 4)]
rng.shuffle(cards)
for q, k in cards: assert command(q)[0] == k
cards_html = "".join(f'<div class="c"><span class="tag">{i}</span><div class="fc sm">{cw(q)[0]}</div></div>' for i, (q, k) in enumerate(cards, 1))
ckey = " · ".join(f"{JOB[k]}: " + ", ".join(str(i) for i, (q, kk) in enumerate(cards, 1) if kk == k) for k in KEYS)

# Exam Planner Swap: two made-up papers (180 marks each); each student reads theirs out, the partner fills the time plan
PA = ("Theme: Bridges", [("Reading: an article about a new bridge", 30), ("Reading: a poster", 15), ("Studied poem", 30), ("Studied novel", 45), ("Writing: a speech", 60)])
PB = ("Theme: Night", [("Reading: a short story extract", 45), ("Studied drama", 30), ("Studied film", 30), ("Functional writing: a letter", 30), ("Writing: a story", 45)])
for t, qs in (PA, PB): assert sum(m for _, m in qs) == MARKS and sum(mins(m) for _, m in qs) == MIN
def swap_card(who, mine):
    return f"""<div class="idc"><h3>Student {who} · Exam Planner Swap</h3>
    <div class="two" style="gap:4mm"><div><p style="font-size:8.8pt;margin:0 0 1mm"><b>1. Your paper (keep it hidden).</b> Read it out: “{esc(mine[0])}. Question 1: {esc(mine[1][0][0])}, {mine[1][0][1]} marks …”</p>
    <table class="st"><tbody>{''.join(f"<tr><td>Q{i}</td><td>{esc(p)}</td><td>{m} marks</td></tr>" for i, (p, m) in enumerate(mine[1], 1))}</tbody></table>
    <p style="font-size:8.8pt;margin:1mm 0"><b>3. Then check</b> your partner's plan for your paper: does it add up to 120 minutes?</p></div>
    <div><p style="font-size:8.8pt;margin:0 0 1mm"><b>2. Plan your partner's paper</b> as they read it out (2 hours, 180 marks: ⅔ of a minute a mark).</p>
    <table class="st"><thead><tr><th>Q</th><th>Marks</th><th>Minutes</th></tr></thead><tbody>{''.join(f"<tr><td>{i}</td><td style='height:5.2mm'></td><td></td></tr>" for i in range(1, 6))}<tr><td><b>Total</b></td><td>180</td><td></td></tr></tbody></table>
    <p style="font-size:8.8pt;margin:1mm 0">Which question would you do first, and why?</p></div></div></div>"""
CARD_A = swap_card("A", PA); CARD_B = swap_card("B", PB)
def plan(P): return f"{esc(P[0])}: " + ", ".join(f"Q{i} {m} → {mins(m)} min" for i, (p, m) in enumerate(P[1], 1)) + " (= 120)"

FIX = [("Q: Explain why the girl hides the letter. A: She hides it under her bed.", "says what, not why: “She hides it because she is afraid her mother will read it, as she “glanced at the door” first.”"),
       ("Q: Compare the two poems. A: The first poem is about winter and uses lots of similes.", "only one poem: every point needs both (“Both are about winter, but…”)"),
       ("Q: Identify two facts from the leaflet. (6 marks) A: a whole page about why the leaflet is good", "a 6-mark question gets about 4 minutes: two short facts, then move on"),
       ("Q: Do you agree that the ending is happy? A: The ending is when they go home.", "no view and no reason: “I agree, because…” + evidence"),
       ("Q: Describe the setting. A: It is nice.", "no detail: name the place, time and mood, with words from the text"),
       ("Q: Write a letter to your principal… A: Hey Sir, guess what!!", "wrong register for the reader: “Dear Mr Byrne, I am writing to…”")]
WX = ("A made-up section of a paper", ["Question 1 (20 marks): Name two things the narrator sees on the beach and explain how she feels.",
      "Question 2 (40 marks): Compare the openings of the two stories you have read.",
      "Question 3 (60 marks): Write a speech for your school assembly on why every student should learn to swim."])
assert [int(re.search(r"\((\d+) marks", s).group(1)) for s in WX[1]] == [20, 40, 60]
WT = [round(m * MIN / MARKS) for m in (20, 40, 60)]; assert WT == [13, 27, 40] and Fr(20 * MIN, MARKS) == Fr(40, 3)
assert command("Name two things the narrator sees on the beach.")[0] == "find" and form(WX[1][2]) == "speech"

pack = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Exam Technique Teacher Pack | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{PACK_STYLE}
{EXTRA}
.fym{{grid-template-columns:repeat(4,1fr)}}.fym .c{{height:30mm}}.fym .fc.sm{{font-size:9.4pt;font-weight:600;line-height:1.3}}
.idc{{padding:2mm 4mm;margin-bottom:3mm}}.idc h3{{margin:0 0 1mm}}.p1 .proc td{{font-size:8.6pt;padding:2px 6px}}
.ws .eh td{{font-size:8.6pt;padding:2px 6px}}.ws .eh .gap{{height:11px}}.ws .pass{{font-size:8.6pt;line-height:1.35}}.ws ol.q li{{margin-bottom:1px}}
.prow{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:4mm}}.prow div{{border-radius:14px;padding:5mm 3mm;text-align:center;font-size:12pt;line-height:1.45}}.prow b{{display:block;font-size:20pt}}
.pex{{border:3px solid var(--night);border-radius:14px;padding:5mm 7mm;font-size:13pt;line-height:1.5}}
</style></head><body>

<div class="page p1">
  <div class="band"><div><div class="k">Junior Cycle English · Teacher pack</div><h1>Exam Technique</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2015 specification): {LO}</p>
  <div class="two">
    <div><h3>Aims</h3><p>By the end of the lesson students can say what each command word asks for, plan their time on a 2-hour, 180-mark paper from the marks, pick out the form, reader and purpose of a writing task, and fix answers that lose marks by missing the question.</p></div>
    <div><h3>In this pack</h3><p>p.1 Teacher notes · p.2 Command Word Sort (24 cards) · p.3 Exam Planner Swap A/B (pair listening task) · p.4 Wall poster · p.5 Worksheet: Fix the Answer + exam-style questions · p.6 Answers. Level: 3rd year (works from 2nd year). Time: about 60 minutes.</p></div>
  </div>
  <h2 style="margin-top:8px">Procedure</h2>
  <table class="proc"><tbody>
    <tr><td>5 min</td><td><b>Lead-in.</b> Write “Identify”, “Explain”, “Compare” on the board. Students say what a full answer to each would look like. Which is shortest? Which needs two texts?</td></tr>
    <tr><td>12 min</td><td><b>Command Word Sort</b> (p.2, groups of 3–4). Sort the 24 question cards into six piles by the job they ask for. Then each group picks one card and plans a full answer in three bullet points.</td></tr>
    <tr><td>15 min</td><td><b>Exam Planner Swap</b> (p.3, pairs). Each reads their made-up paper aloud; the partner plans the minutes for each question (⅔ of a minute a mark). Swap and check that each plan adds up to 120 minutes.</td></tr>
    <tr><td>5 min</td><td><b>Poster</b> (p.4). Read it. Time it. Answer it. Ask: what do you do when the time for a question runs out?</td></tr>
    <tr><td>18 min</td><td><b>Worksheet</b> (p.5). Fix the Answer in pairs, then the exam-style questions alone.</td></tr>
    <tr><td>5 min</td><td><b>Exit ticket.</b> One question from an old class test: underline the command word, circle how many, box the focus. Homework: play <b>English Exam Mix</b> at {GAME}.</td></tr>
  </tbody></table>
  <div class="note"><b>Errors to look for:</b> answering “what” when the question asks “why” · comparing one text only · long answers to small questions and no time left for the big one · retelling the story · a writing task in the wrong form or register for its reader. <b>Note:</b> the sections and marks of the real paper change each year; the papers in this pack are made up. Our guide, not an official marking scheme.</div>
</div>

<div class="page">
  <div class="band"><div><div class="k">Groups · cut up the cards</div><h1>Command Word Sort</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.4pt;margin:0 0 2mm">Sort the 24 questions into six piles: <b>{' · '.join(JOB[k] for k in KEYS)}</b>. The underlined words are the clue. Then plan a full answer to one card.</p>
  <div class="fym">{cards_html}</div>
</div>

<div class="page">
  <div class="band"><div><div class="k">Pairs · cut along the dashed line</div><h1>Exam Planner Swap A/B</h1></div><div class="logo">↗ Léim</div></div>
  {CARD_A}
  {CARD_B}
</div>

<div class="page">
  <div class="poster">
    <h1>Read it. Time it. Answer it.</h1>
    <div class="prow">
      <div style="background:var(--green-soft)"><b>Read it</b>Underline the command word<br>Circle how many<br>Box the focus</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Time it</b>2 hours · 180 marks<br>⅔ of a minute a mark<br>30 marks = 20 minutes</div>
      <div style="background:var(--green-soft)"><b>Answer it</b>Use the question's words<br>Point · quote · explain<br>Read it back</div>
    </div>
    <div class="pex"><b>Identify</b> = find it · <b>Describe</b> = what it's like · <b>Explain</b> = why or how · <b>Compare</b> = alike and different · <b>Do you agree?</b> = your view + reasons · <b>Summarise</b> = main points</div>
    <p style="text-align:center;font-size:18pt!important;font-weight:800;margin:4mm 0">Answer the question that was asked.</p>
    <p style="text-align:center;font-size:10pt;color:var(--muted)">Léim · leim.ie · Play English Exam Mix: {GAME}</p>
  </div>
</div>

<div class="page ws">
  <div class="band"><div><div class="k">Worksheet · exam-style questions</div><h1>Fix the Answer</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Fix the Answer</h2>
  <p>Each answer misses what the question asked. Say what's wrong and write a better version.</p>
  <table class="eh"><thead><tr><th>Question and weak answer</th><th>What's wrong and a better version</th></tr></thead><tbody>
  {"".join(f"<tr><td style='font-weight:500'>{esc(s)}</td><td><span class='gap'></span><span class='gap'></span></td></tr>" for s, r in FIX)}
  </tbody></table>
  <h2>B. Exam-style questions</h2>
  <div class="pass"><b>{WX[0]}</b>{''.join(f"<span class='sp'>{esc(l)}</span>" for l in WX[1])}</div>
  <ol class="q">
    <li>The whole paper is 2 hours, 180 marks. About how many minutes should you give each of these three questions?<span class="long"></span></li>
    <li>Question 1 has two command words. What are they, and what does each ask you to do?<span class="long"></span></li>
    <li>What must a good answer to Question 2 do in every point?<span class="long"></span></li>
    <li>For Question 3, write down the form, the reader and the purpose.<span class="long"></span></li>
    <li>Write the opening two sentences of the speech in Question 3.<span class="long"></span><span class="long"></span></li>
  </ol>
</div>

<div class="page an">
  <div class="band"><div><div class="k">For the teacher</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>Command Word Sort</h2>
  <p style="font-size:9pt">{ckey}</p>
  <h2>Exam Planner Swap</h2>
  <p style="font-size:9pt">A's paper: {plan(PA)}<br>B's paper: {plan(PB)}</p>
  <h2>A. Fix the Answer</h2>
  <table><tbody>{"".join(f"<tr><td style='width:42%'>{esc(s)}</td><td>{esc(r)}</td></tr>" for s, r in FIX)}</tbody></table>
  <h2>B. Exam-style questions</h2>
  <ol class="q">
    <li>About {WT[0]}, {WT[1]} and {WT[2]} minutes (20 × ⅔ = 13⅓, 40 × ⅔ = 26⅔, 60 × ⅔ = 40).</li>
    <li><b>Name</b> (find two things: short) and <b>explain</b> (say how she feels and why, with a quote).</li>
    <li>Talk about both stories in every point: how the openings are alike and how they are different.</li>
    <li>Form: a speech. Reader: the students at your school assembly. Purpose: to persuade.</li>
    <li>Sample: “Good morning, everyone. Hands up if you could swim fifty metres right now, in cold water, in your clothes?” (talks to the audience, hooks them with a question).</li>
  </ol>
  <h2>Marking tip</h2>
  <p>Answers are rewarded for doing what the question asks: the right job for the command word, the right number of points, and evidence from the text. Our guide, not an official marking scheme.</p>
</div>
</body></html>"""

cover = """<!doctype html><html><head><meta charset="utf-8"><style>
body{margin:0;width:1200px;height:1200px;background:#1B2430;font-family:Inter,sans-serif;color:#fff;display:flex;flex-direction:column;justify-content:space-between;padding:90px;box-sizing:border-box}
.k{display:inline-block;background:#2E7D57;border-radius:99px;padding:12px 26px;font-weight:700;font-size:28px;letter-spacing:.06em;text-transform:uppercase}
h1{font-size:104px;font-weight:800;line-height:1.3;letter-spacing:-.02em;margin:60px 0 20px}
h1 span{background:#F6CF5A;color:#1B2430;padding:0 18px;border-radius:14px}
.sub{font-size:40px;line-height:1.4;color:#DDE3EA}
.em{font-size:46px;margin-top:30px;font-weight:800;letter-spacing:.01em;color:#F6CF5A}
.foot{display:flex;justify-content:space-between;align-items:center;font-size:34px;font-weight:700}
.price{background:#F6CF5A;color:#1B2430;border-radius:16px;padding:14px 28px}
</style></head><body>
<div><span class="k">JC English · Teacher pack</span>
<h1><span>Exam</span><br><span>Technique</span></h1>
<div class="sub">Command Word Sort · Exam Planner Swap A/B<br>Poster · Worksheet + answers</div>
<div class="em">read it, time it, answer it</div></div>
<div class="foot"><span>↗ Léim · leim.ie</span><span class="price">Ready to teach · 60 min</span></div>
</body></html>"""

if __name__ == "__main__":
    for name, txt in [("rules-and-practice", sheet), ("teacher-pack", pack), ("cover", cover)]:
        open(os.path.join(SRC, f"{SLUG}-{name}.html"), "w", encoding="utf-8").write(txt)
    def pdf(name, out):
        subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--no-pdf-header-footer", f"--print-to-pdf={out}",
                        f"{SLUG}-{name}.html"], cwd=SRC, check=True, capture_output=True)
        n = subprocess.run(["pdfinfo", out], capture_output=True, text=True).stdout.split("Pages:")[1].split()[0]
        print(name, n, "pages"); return int(n)
    a = pdf("rules-and-practice", os.path.join(ROOT, "printables", f"{SLUG}-rules-and-practice.pdf"))
    b = pdf("teacher-pack", os.path.join(OUT, "Exam-Technique-Teacher-Pack-Leim.pdf"))
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--hide-scrollbars", "--window-size=1200,1200",
                    f"--screenshot={os.path.join(OUT, f'{SLUG}-cover.png')}", f"{SLUG}-cover.html"], cwd=SRC, check=True, capture_output=True)
    assert a == 3 and b == 6, (a, b)
