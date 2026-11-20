#!/usr/bin/env python3
"""Functional writing: reports, reviews, articles & blogs (JC English Order 22): free sheet (-> printables/),
6-page teacher pack + 1200x1200 cover (-> OUTDIR).
Usage: python3 src/build_functional_writing_pdfs.py /tmp/fw
Items come from the game's data block (format-sort.html). Every answer is re-derived with the checker's own rules
(src/test_format_sort.py: types, rparts, vparts, shares) and asserted; the checker's data pass runs first.
Styles are read from src/build_money1_pdfs.py."""
import os, sys, random, subprocess, re
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC); sys.path.insert(0, SRC)
from test_format_sort import types, rparts, vparts, shares, load, data_pass
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/fw"; os.makedirs(OUT, exist_ok=True)
SLUG = "functional-writing"
LO = "W4, W3, R13"
GAME = "leim.ie/format-sort.html"
D = load(os.path.join(ROOT, "format-sort.html")); assert not data_pass(D), data_pass(D)
TN = {"rep": "Report", "rev": "Review", "art": "Article", "blo": "Blog", "spe": "Speech"}
RN = {"ti": "Title", "in": "Introduction", "fi": "Findings", "re": "Recommendation", "si": "Sign-off"}
VN = {"de": "Details", "pr": "Praise", "cr": "Criticism", "ve": "Verdict"}
L = "abcdefgh"

# ---------- free sheet ----------
random.seed(2221)
A_items = [x for k in TN for x in random.sample([y for y in D["type"] if y[1] == k], 2)]; random.shuffle(A_items)
for s, k in A_items: assert types(s) == [k]
H_items = random.sample(D["heads"], 4)
H_box = [h for _, h in H_items] + random.sample([h for t, h in D["heads"] if [t, h] not in H_items], 1) + random.sample(D["vague"], 1)
random.shuffle(H_box)
for t, h in H_items:
    assert [x for x in H_box if shares(t, x)] == [h], (t, h)
C_items = [x for k in RN for x in random.sample([y for y in D["rep"] if y[1] == k], 1)] + random.sample([y for y in D["rep"] if y[1] in ("fi", "re")], 3)
C_items = list(dict.fromkeys(map(tuple, C_items)))
while len(C_items) < 8: C_items = list(dict.fromkeys(C_items + [tuple(random.choice(D["rep"]))]))
random.shuffle(C_items)
for s, k in C_items: assert rparts(s) == [k]
E_items = [x for k in VN for x in random.sample([y for y in D["rev"] if y[1] == k], 2)]; random.shuffle(E_items)
for s, k in E_items: assert vparts(s) == [k]
NQ = len(A_items) + len(H_items) + len(C_items) + len(E_items) + 3; assert NQ == 33, NQ
nA = 1; nB = nA + len(A_items); nC = nB + len(H_items); nE = nC + len(C_items); nF = nE + len(E_items)

def style(var):
    return re.search(var + r' = f"""<!doctype.*?<style>(.*?)</style>', open(os.path.join(SRC, "build_money1_pdfs.py"), encoding="utf-8").read(), re.S).group(1).replace("{LO}", LO).replace("{{", "{").replace("}}", "}").replace("JC Maths LOs (2018 spec)", "JC English LOs (2015 spec)")
SHEET_STYLE = style("sheet"); PACK_STYLE = style("pack")
assert "JC English LOs (2015 spec)" in SHEET_STYLE and "Single-teacher licence" in PACK_STYLE and "JC English LOs (2015 spec)" in PACK_STYLE
EXTRA = """.wk{line-height:1.45;border:1.5px solid var(--line);border-radius:8px;padding:2px 7px;margin:3px 0;font-size:9.4pt}.wk b.h{display:block}
table.st{border-collapse:collapse;margin:3px 0;font-size:9.2pt;width:100%}table.st td,table.st th{border:1px solid #C9D1DA;padding:2px 6px;text-align:left}
.pass{border-left:4px solid var(--green);background:var(--mist);padding:5px 10px;margin:4px 0;font-family:Georgia,serif;font-size:9.4pt;line-height:1.45}
.pass i{color:#4A5562}.box{border:1.5px dashed #9AA6B2;border-radius:8px;padding:3px 8px;margin:2px 0 4px;font-size:9pt}"""

def two(items_html, cut):
    return f"<div class='two'><div><ol class='q'>{''.join(items_html[:cut])}</ol></div><div><ol class='q'>{''.join(items_html[cut:])}</ol></div></div>"
A_html = [f"<li value='{i}'>{s} <span class='line' style='min-width:18mm'></span></li>" for i, (s, k) in enumerate(A_items, nA)]
B_html = "".join(f"<li value='{i}'>{t} <span class='line' style='min-width:10mm'></span></li>" for i, (t, h) in enumerate(H_items, nB))
B_box = "<div class='box'><b>Headlines:</b> " + " · ".join(f"({L[i]}) {h}" for i, h in enumerate(H_box)) + "</div>"
C_html = [f"<li value='{i}'>{s} <span class='line' style='min-width:18mm'></span></li>" for i, (s, k) in enumerate(C_items, nC)]
E_html = [f"<li value='{i}'>{s} <span class='line' style='min-width:16mm'></span></li>" for i, (s, k) in enumerate(E_items, nE)]

FACTS = ("THE FACTS: BALLYDUFF COMMUNITY GARDEN",
  ["The old tennis court behind Ballyduff Community School has become a vegetable garden.",
   "40 students and 12 neighbours helped to build it over the summer.",
   "It opens to the public on Saturday 6 June at 11 a.m.",
   "Of the 90 students surveyed, 71 said they would like to work in the garden at lunchtime.",
   "Ms Daly, the science teacher: \"The students have done something amazing.\""])
assert types(FACTS[1][3]) == ["rep"] and rparts(FACTS[1][3]) == ["fi"]

sheet = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Functional writing: reports, reviews, articles and blogs, rules and practice | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{SHEET_STYLE}
{EXTRA}
.p2 ol.q li{{margin-bottom:1px;font-size:9pt}}.p2 h2{{margin:4px 0 2px}}.p2 .two{{gap:5mm}}
</style></head><body>
<div class="page tight">
  <div class="band"><div><div class="k">Junior Cycle English · Free revision sheet</div><h1>Functional writing</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2015 specification): {LO}. Play the game: <b>{GAME}</b></p>
  <p>Functional writing does a job for a real reader. Before you write, ask: <b>What type of text is it? Who is reading it? What does it need to do?</b> The answers decide your layout, your opening and your tone.</p>
  <div class="two">
   <div><h2>1. Five text types</h2>
    <table class="st"><thead><tr><th>Type</th><th>Look for</th></tr></thead><tbody>
     <tr><td><b>Report</b></td><td>"Report on ..." title, terms of reference, findings (numbers), recommendations, signed and dated. Formal.</td></tr>
     <tr><td><b>Review</b></td><td>details (title, director or author, price), praise, criticism, a verdict or star rating. No spoilers.</td></tr>
     <tr><td><b>Article</b></td><td>headline, byline (By ...), who / what / where / when in the first paragraph, quotes, subheadings.</td></tr>
     <tr><td><b>Blog</b></td><td>title and date, first person, chatty, talks to readers, asks for comments, hashtags.</td></tr>
     <tr><td><b>Speech</b></td><td>greets the audience, signposts, rhetorical questions, "Thank you for listening."</td></tr></tbody></table>
    <h2>2. Headlines</h2>
    <p style="font-size:9pt">Short (under eight words), the <b>main fact</b>, present tense, little words dropped: <b>Bees Close Bray Playground</b>. "Big News Today" tells the reader nothing.</p>
    <h2>3. Same news, four ways</h2>
    <div class="wk"><b>Report:</b> Of the 120 students surveyed, 85% said they would use a skate park.<br><b>Article:</b> By Ellen Daly: Students in Carrick will skate at school from Friday, according to the principal.<br><b>Blog:</b> Hi everyone! Our skate park opens on Friday. Comment below if you're coming!<br><b>Speech:</b> Good morning, everyone. Fellow students, on Friday our skate park opens.</div></div>
   <div><h2>4. How a report is laid out</h2>
    <div class="pass"><b>Report on Lunchtime Litter at St Brigid's College</b><br><b>Introduction:</b> This report was requested by the principal, Ms Byrne, to find out why the yard is full of litter.<br><b>Findings:</b> Of the 150 students surveyed, 90 said there are not enough bins.<br><b>Recommendations:</b> I recommend that four more bins are placed in the yard.<br><b>Signed:</b> Aoife Byrne, Student Council Secretary, 12 May 2026</div>
    <h2>5. How a review works</h2>
    <table class="st"><tbody>
     <tr><td><b>Details</b></td><td>title, director / author, length, price</td></tr>
     <tr><td><b>Praise</b></td><td>what's good, with a reason</td></tr>
     <tr><td><b>Criticism</b></td><td>what's weak, fairly</td></tr>
     <tr><td><b>Verdict</b></td><td>stars or a score; who would enjoy it</td></tr></tbody></table>
    <h2>6. Tone for the reader</h2>
    <p style="font-size:9pt"><b>Formal</b> for a principal, a board or a council (report, letter to a paper). <b>Lively</b> for a school magazine review. <b>Chatty</b> for a blog. A speech talks <b>to</b> the audience: "you", "we", "our".</p></div>
  </div>
  <div class="tip"><b>Exam tip:</b> show the format from the <b>first line</b> (a report title, a headline + byline, a greeting) and use the features the task names: if it asks for two recommendations, give two.</div>
</div>

<div class="page p2">
  <div class="band"><div><div class="k">Practice · {NQ} questions</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Which text type? (report / review / article / blog / speech)</h2>
  {two(A_html, 5)}
  <h2>B. Pick the best headline for each story: write a letter</h2>
  {B_box}
  <ol class="q">{B_html}</ol>
  <h2>C. Which part of the report? (title / introduction / findings / recommendation / sign-off)</h2>
  {two(C_html, 4)}
  <h2>D. Which part of the review? (details / praise / criticism / verdict)</h2>
  {two(E_html, 4)}
</div>

<div class="page">
  <div class="band"><div><div class="k">Exam-style · answers</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <h2>E. Exam-style</h2>
  <div class="pass"><b>{FACTS[0]}</b><br>{"<br>".join(FACTS[1])}</div>
  <ol class="q">
   <li value="{nF}">Write a headline and the first paragraph of an article about the garden for the local newspaper.<span class="long"></span><span class="long"></span></li>
   <li value="{nF + 1}">The board of management wants a report. Write the title, the terms of reference and one recommendation.<span class="long"></span><span class="long"></span></li>
   <li value="{nF + 2}">Write the opening of a blog post about the garden for the school website. Name two blog features you used.<span class="long"></span></li>
  </ol>
  <h2>Answers</h2>
  <table class="ans"><tbody>
   <tr><td><b>A</b></td><td>{" · ".join(f"{i}. {TN[types(s)[0]]}" for i, (s, k) in enumerate(A_items, nA))}</td></tr>
   <tr><td><b>B</b></td><td>{" · ".join(f"{i}. ({L[H_box.index(h)]})" for i, (t, h) in enumerate(H_items, nB))}</td></tr>
   <tr><td><b>C</b></td><td>{" · ".join(f"{i}. {RN[rparts(s)[0]]}" for i, (s, k) in enumerate(C_items, nC))}</td></tr>
   <tr><td><b>D</b></td><td>{" · ".join(f"{i}. {VN[vparts(s)[0]]}" for i, (s, k) in enumerate(E_items, nE))}</td></tr>
   <tr><td><b>E</b></td><td>{nF}. E.g. <b>Students Turn Tennis Court into Garden</b>. By (name): A vegetable garden built by 40 students and 12 neighbours on an old tennis court in Ballyduff opens to the public on Saturday 6 June. {nF + 1}. <b>Report on the Ballyduff Community Garden</b>; This report was requested by the board of management to find out how students would use the garden. I recommend that the garden opens at lunchtime, as 71 of the 90 students surveyed want to work in it. {nF + 2}. E.g. "Hi everyone! You will not believe what we did this summer ..." Features: first person, chatty tone, talks to readers, invites comments.</td></tr>
  </tbody></table>
  <div class="note"><b>Got one wrong?</b> Go back to page 1, then play <b>Format Sort</b> at {GAME}: the "Go back over these" list at the end explains each mistake.</div>
  <p class="small">All stories, films, books, games, names and places are made up by Léim. Léim is independent and not connected with the State Examinations Commission or the NCCA.</p>
</div>
</body></html>"""

# ---------- teacher pack ----------
random.seed(2222)
FS = [x for k in TN for x in random.sample([y for y in D["type"] if y[1] == k], 4)]; random.shuffle(FS)
assert len(FS) == 20
for s, k in FS: assert types(s) == [k]
fs_html = "".join(f'<div class="c"><span class="tag">Card {i}</span><div class="fc sm">{s}</div></div>' for i, (s, k) in enumerate(FS, 1))
fs_key = " · ".join(f"<b>{TN[k]}</b>: {', '.join(str(i) for i, (s, kk) in enumerate(FS, 1) if kk == k)}" for k in TN)

# Headline Swap: A reads 4 stories, B picks from 6 headlines (A's 4 + 1 other story + 1 vague), and vice versa
HS = random.sample(D["heads"], 8); HA, HB = HS[:4], HS[4:]
others = [x for x in D["heads"] if x not in HS]
def hbox(stories):
    box = [h for _, h in stories] + [random.choice(others)[1], random.choice(D["vague"])]; random.shuffle(box)
    for t, h in stories: assert [x for x in box if shares(t, x)] == [h], (t, h)
    return box
BOX_B, BOX_A = hbox(HA), hbox(HB)  # B listens to A's stories with BOX_B
# Report Swap: each reads 5 jumbled report lines (one per part); the partner labels each line
RA = [random.choice([y for y in D["rep"] if y[1] == k]) for k in RN]; random.shuffle(RA)
RB = [random.choice([y for y in D["rep"] if y[1] == k and y not in RA]) for k in RN]; random.shuffle(RB)
for s, k in RA + RB: assert rparts(s) == [k]
def swap_card(who, mine, box, reps):
    return f"""<div class="idc"><h3>Student {who} · Headline &amp; Report Swap</h3>
    <p style="font-size:8.8pt;margin:0 0 1mm"><b>1. Read</b> each news story to your partner. They choose its headline from their box. Tick if they're right.</p>
    <table class="st" style="font-size:8.8pt"><tbody>{"".join(f"<tr><td style='width:4%'><b>{i}</b></td><td>{t}</td><td style='width:5%'>☐</td></tr>" for i, (t, h) in enumerate(mine, 1))}</tbody></table>
    <p style="font-size:8.8pt;margin:1mm 0"><b>2. Listen</b> to your partner's four stories. Write the letter of the best headline. <b>Box:</b> {" · ".join(f"({L[i]}) {h}" for i, h in enumerate(box))}</p>
    <table class="st" style="font-size:8.8pt"><tbody><tr>{"".join(f"<td><b>{i}</b> ___</td>" for i in range(1, 5))}</tr></tbody></table>
    <p style="font-size:8.8pt;margin:1mm 0"><b>3. Report jumble.</b> Read these report lines aloud in this order. Your partner says which part each one is (title / introduction / findings / recommendation / sign-off) and the right order.</p>
    <table class="st" style="font-size:8.8pt"><tbody>{"".join(f"<tr><td style='width:4%'><b>{i}</b></td><td>{s}</td><td style='width:5%'>☐</td></tr>" for i, (s, k) in enumerate(reps, 1))}</tbody></table></div>"""

FIX = [("Report: Hi everyone, I'm going to tell you all about the canteen!", "Wrong tone and no format. Start with a title and terms of reference: <b>Report on the School Canteen. This report was requested by the student council to ...</b>"),
       ("Headline: There was a really big storm in our town last night and lots of trees fell down", "Far too long, and a full sentence. Keep the main fact: <b>Storm Brings Down Trees in Kilkee</b>"),
       ("Review: The film is good. I liked it.", "No details, no reasons, no verdict: <b>Storm Island (12A, 98 minutes) is a gripping thriller. The acting is superb ... Four stars out of five.</b>"),
       ("Review: In the end, it turns out the teacher was the thief all along!", "A spoiler. Hint at the twist without giving it away: <b>The ending will take you completely by surprise.</b>"),
       ("Article: I think the new pool is brilliant and everyone should go.", "A news article reports facts and quotes people: <b>The new pool opened on Monday. \"We had 300 swimmers on the first day,\" said manager Ann Ryan.</b>"),
       ("Report: The yard is a disgrace and someone should do something!!", "A report is calm and specific: <b>Findings: the bins are full by 11 a.m. Recommendation: I recommend that four more bins are placed in the yard.</b>")]

pack = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Functional Writing Teacher Pack | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{PACK_STYLE}
{EXTRA}
.fym .c{{height:36mm}}.fym .fc.sm{{font-size:10.4pt;line-height:1.3;margin-top:2mm;font-weight:500}}.idc{{padding:2mm 4mm;margin-bottom:3mm}}.idc h3{{margin:0 0 1mm}}
.idc .st td{{padding:1px 5px}}.p1 .proc td{{font-size:8.6pt;padding:2px 6px}}.ops div{{font-size:12pt;padding:5mm 3mm}}.ops b{{font-size:19pt}}
.ws .eh td{{font-size:8.6pt;padding:2px 6px}}.ws .eh .gap{{height:13px}}.ws ol.q li{{margin-bottom:1px}}.ws .pass{{font-size:9pt}}
</style></head><body>

<div class="page p1">
  <div class="band"><div><div class="k">Junior Cycle English · Teacher pack</div><h1>Functional writing</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2015 specification): {LO}</p>
  <div class="two">
    <div><h3>Aims</h3><p>By the end of the lesson students can tell a report, review, article, blog and speech apart by their features, lay out a report (title, terms of reference, findings, recommendations, sign-off), name the parts of a review, write a short headline that names the main fact, and match their tone to the reader.</p></div>
    <div><h3>In this pack</h3><p>p.1 Teacher notes · p.2 Format Sort cards (cut-up) · p.3 Headline &amp; Report Swap A/B (speaking) · p.4 Wall poster · p.5 Worksheet: Fix the Answer + exam-style questions · p.6 Answers. Level: 2nd year. Time: about 60 minutes. All stories and titles are made up.</p></div>
  </div>
  <h2 style="margin-top:8px">Procedure</h2>
  <table class="proc"><tbody>
    <tr><td>5 min</td><td><b>Lead-in.</b> Read the skate-park news four ways (free sheet, box 3). Which is the report, article, blog and speech? What gave each one away? List the clues on the board.</td></tr>
    <tr><td>8 min</td><td><b>Guided discovery.</b> Label the St Brigid's report (free sheet, box 4): title, introduction, findings, recommendations, sign-off. Then build a feature table for the five text types together.</td></tr>
    <tr><td>12 min</td><td><b>Format Sort</b> (p.2, groups of 3, one set of 20 cards). Sort the lines into report, review, article, blog and speech, and underline the word or phrase that gave each one away.</td></tr>
    <tr><td>12 min</td><td><b>Headline &amp; Report Swap</b> (p.3, pairs). A reads four news stories; B picks each headline from a box with two decoys. Then A reads five jumbled report lines; B names each part and puts them in order. Swap.</td></tr>
    <tr><td>18 min</td><td><b>Worksheet</b> (p.5). Fix the Answer in pairs, then the exam-style questions on the Kilmore Youth Café alone.</td></tr>
    <tr><td>5 min</td><td><b>Exit ticket.</b> Write one headline and one report recommendation about something in your school. Homework: play <b>Format Sort</b> at {GAME}.</td></tr>
  </tbody></table>
  <div class="note"><b>Errors to look for:</b> writing a story when the task asks for a report or article · a chatty tone in a report · headlines that are full sentences · reviews with no verdict or with spoilers · articles full of the writer's opinions and no facts or quotes · forgetting the sign-off and date. <b>Support:</b> the poster (p.4) on the desk. <b>Fast finishers:</b> rewrite one Format Sort card as a different text type.</div>
</div>

<div class="page">
  <div class="band"><div><div class="k">Groups of 3 · cut up the 20 cards</div><h1>Format Sort</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.4pt;margin:0 0 2mm">Sort the 20 lines into five piles: <b>report · review · article · blog · speech</b>. Underline the clue in each one.</p>
  <div class="fym">{fs_html}</div>
</div>

<div class="page">
  <div class="band"><div><div class="k">Pairs · cut along the dashed line</div><h1>Headline &amp; Report Swap A/B</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.4pt">Read, listen, choose, then sort out a jumbled report.</p>
  {swap_card("A", HA, BOX_A, RA)}
  {swap_card("B", HB, BOX_B, RB)}
</div>

<div class="page">
  <div class="poster">
    <h1>Know your format</h1>
    <div class="ops">
      <div style="background:var(--green-soft)"><b>Report</b>Title · findings<br>recommendations · signed</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Review</b>Details · praise<br>criticism · verdict</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Article</b>Headline · byline<br>facts · quotes</div>
      <div style="background:var(--green-soft)"><b>Blog</b>Title · date<br>chatty · comments</div>
    </div>
    <p style="text-align:center;font-size:20pt!important;font-weight:800;margin:4mm 0">Who is reading? What must it do?</p>
    <p style="text-align:center;font-size:10pt;color:var(--muted)">Léim · leim.ie · Play Format Sort: {GAME}</p>
  </div>
</div>

<div class="page ws">
  <div class="band"><div><div class="k">Worksheet · exam-style questions</div><h1>Fix the Answer</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Fix the Answer</h2>
  <p>Each line is the start of a student's answer. Say what's wrong and write a better version.</p>
  <table class="eh"><thead><tr><th>Answer</th><th>What's wrong and the fix</th></tr></thead><tbody>
  {"".join(f"<tr><td style='font-weight:500'>{s}</td><td><span class='gap'></span><span class='gap'></span></td></tr>" for s, r in FIX)}
  </tbody></table>
  <h2>B. Exam-style questions: Kilmore Youth Café</h2>
  <div class="pass"><b>THE FACTS</b><br>The old library in Kilmore has reopened as a youth café for 12 to 18-year-olds.<br>It is open Tuesday to Saturday, 4 p.m. to 9 p.m., with board games, a music room and free Wi-Fi.<br>Of the 200 teenagers surveyed by the council, 150 said they had nowhere to go in the evenings.<br>Youth worker Cathal Byrne: "This is their space, and they designed it."</div>
  <ol class="q">
    <li>Write a headline for a local newspaper article about the café. Explain why it works.<span class="long"></span></li>
    <li>Write the first paragraph of the article. Include who, what, where, when and a quote.<span class="long"></span><span class="long"></span></li>
    <li>The council asks for a report. Write the terms of reference and one finding.<span class="long"></span></li>
    <li>Write two recommendations for the report.<span class="long"></span></li>
    <li>You visit the café. Write a short review for your school magazine, with a verdict.<span class="long"></span><span class="long"></span></li>
  </ol>
</div>

<div class="page an">
  <div class="band"><div><div class="k">For the teacher</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>Format Sort (card numbers)</h2>
  <p>{fs_key}</p>
  <h2>Headline &amp; Report Swap</h2>
  <p>Headlines: {" · ".join(f"<b>{w}{i}</b> ({L[box.index(h)]}) {h}" for w, LL, box in (("A", HA, BOX_B), ("B", HB, BOX_A)) for i, (t, h) in enumerate(LL, 1))}. (A's stories are matched from B's box, and B's from A's.)</p>
  <p>Report jumble: {" · ".join(f"<b>{w}{i}</b> {RN[rparts(s)[0]]}" for w, LL in (("A", RA), ("B", RB)) for i, (s, k) in enumerate(LL, 1))}. Right order: title, introduction, findings, recommendation, sign-off.</p>
  <h2>A. Fix the Answer</h2>
  <table><tbody>{"".join(f"<tr><td style='width:34%'>{s}</td><td>{r}</td></tr>" for s, r in FIX)}</tbody></table>
  <h2>B. Exam-style questions</h2>
  <ol class="q">
    <li>E.g. <b>Old Library Reborn as Youth Café</b>: short, present tense, names the main fact and the place.</li>
    <li>E.g. Teenagers in Kilmore finally have somewhere to go in the evenings: the old library has reopened as a youth café for 12 to 18-year-olds, open Tuesday to Saturday from 4 p.m. "This is their space, and they designed it," said youth worker Cathal Byrne.</li>
    <li>This report was requested by the council to find out whether young people use the new youth café. Finding: of the 200 teenagers surveyed, 150 said they had nowhere to go in the evenings.</li>
    <li>E.g. I recommend that the café opens on Sundays. It is recommended that a homework room is added.</li>
    <li>Details (place, opening hours), praise and criticism with reasons, a verdict or star rating, a lively tone for students.</li>
  </ol>
  <h2>Marking tip</h2>
  <p>Reward answers that show the format from the first line, use the features the task asks for and match the tone to the reader. Our guide, not an official marking scheme.</p>
</div>
</body></html>"""

cover = """<!doctype html><html><head><meta charset="utf-8"><style>
body{margin:0;width:1200px;height:1200px;background:#1B2430;font-family:Inter,sans-serif;color:#fff;display:flex;flex-direction:column;justify-content:space-between;padding:90px;box-sizing:border-box}
.k{display:inline-block;background:#2E7D57;border-radius:99px;padding:12px 26px;font-weight:700;font-size:28px;letter-spacing:.06em;text-transform:uppercase}
h1{font-size:100px;font-weight:800;line-height:1.25;letter-spacing:-.02em;margin:60px 0 20px}
h1 span{background:#F6CF5A;color:#1B2430;padding:0 18px;border-radius:14px}
.sub{font-size:40px;line-height:1.4;color:#DDE3EA}
.em{font-size:46px;margin-top:30px;font-weight:800;letter-spacing:.01em;color:#F6CF5A}
.foot{display:flex;justify-content:space-between;align-items:center;font-size:34px;font-weight:700}
.price{background:#F6CF5A;color:#1B2430;border-radius:16px;padding:14px 28px}
</style></head><body>
<div><span class="k">Junior Cycle English · Teacher pack</span>
<h1><span>Functional</span><br><span>writing</span></h1>
<div class="sub">Format Sort cards · Headline &amp; Report Swap A/B<br>Poster · Worksheet + answers</div>
<div class="em">reports · reviews · articles<br>blogs · headlines</div></div>
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
    pdf("teacher-pack", os.path.join(OUT, "Functional-Writing-Teacher-Pack-Leim.pdf"))
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--hide-scrollbars", "--window-size=1200,1200",
                    f"--screenshot={os.path.join(OUT, f'{SLUG}-cover.png')}", f"{SLUG}-cover.html"], cwd=SRC, check=True, capture_output=True)
