#!/usr/bin/env python3
"""Builds junior-cycle-english.html from the Spanish page's header/sign-up/footer + checklist_data.ENGLISH (job E2, 18 Nov 2026).
Run from the repo root after changing checklist_data.py: python3 src/build_english_page.py
Facts come from the English tracker's "Exam & CBAs" tab (checked 18 Nov 2026)."""
import os, re, sys, html
sys.path.insert(0, os.path.dirname(__file__))
from checklist_data import ENGLISH
e = html.escape
T = open("junior-cycle-spanish.html", encoding="utf-8").read()
head = T[:T.index('<main id="main">')]
head = re.sub(r"<title>.*?</title>", "<title>Junior Cycle English revision | Léim</title>", head)
head = re.sub(r'<meta name="description" content=".*?">', '<meta name="description" content="Junior Cycle English revision mapped to the 2015 specification: how the 2-hour, 180-mark theme-based paper works, the two CBAs, the text-list rules and all 32 topics from 1st to 3rd year, with a free topic checklist and free games, starting with Word Sort (parts of speech).">', head)
head = head.replace(' aria-current="page"', "")
head = head.replace('<a href="subjects.html">Subjects</a>', '<a href="subjects.html" aria-current="page">Subjects</a>', 1)
signup = T[T.index('<div class="signup" id="join">'):T.index('</section>', T.index('<div class="signup" id="join">'))]
foot = T[T.index("</main>"):]

# Short "what you'll practise" line per topic (from the tracker's "What students learn" column, cut down).
DESC = {
  "Word Sort": "nouns, verbs, adjectives, adverbs, pronouns, prepositions and conjunctions, and picking stronger words.",
  "Sentence Surgeon": "statements, questions and commands, simple, compound and complex sentences, and fixing fragments and run-ons.",
  "Comma Catch": "capital letters, full stops, commas in lists and after openers, and apostrophes (its or it's?).",
  "Clue Hunt": "skimming, scanning, the main idea, reading between the lines and finding the line that proves your answer.",
  "Character Clues": "how writers show a character through actions, speech, thoughts and how others react.",
  "Spell Strike": "spelling rules and the words everyone mixes up: there / their / they're, your / you're, to / too / two.",
}
cards = []
for r in ENGLISH[:6]:
    if r[5]:   # live: a link card (like build_maths_page.py)
        cards.append(f'      <a class="card" href="{r[5]}" style="text-decoration:none;color:inherit"><span class="pill">Free game</span><h3>{e(r[4])}</h3><p style="font-size:14px;color:var(--muted);margin:0 0 6px">{e(r[2].split(":")[0])}</p><p>{e(DESC[r[4]][0].upper() + DESC[r[4]][1:])}</p><p style="margin-top:10px;color:var(--green);font-weight:700">Play {e(r[4])} →</p></a>')
        continue
    cards.append(f'      <div class="card" style="opacity:.85"><span class="pill" style="background:var(--mist);color:var(--muted)">Coming soon</span><h3>{e(r[4])}</h3><p style="font-size:14px;color:var(--muted);margin:0 0 6px">{e(r[2].split(":")[0])}</p><p>{e(DESC[r[4]][0].upper() + DESC[r[4]][1:])}</p></div>')
cards = "\n".join(cards)

tabs = ""
for i, yr in enumerate(["1st year", "2nd year", "3rd year"], 1):
    rows = ""
    for n, r in enumerate(ENGLISH, 1):
        if not r[0].startswith(yr[:3]):
            continue
        cba = r[4] == "CBA guide"
        game = ("Free CBA guide" if cba else e(r[4]))
        if r[5]:
            game = f'<a href="{r[5]}">{game}</a>'
        soon = "" if r[5] else " <em>(coming soon)</em>"
        tag = ' <span class="pill" style="font-size:11px;padding:2px 8px;vertical-align:2px">CBA</span>' if cba else ""
        rows += f'<tr><td class="num">{n}</td><td><b>{e(r[2])}</b>{tag}{soon}</td><td>{e(r[1])}</td><td>{e(r[3])}</td><td>{game}</td></tr>'
    tabs += f'    <div id="y{i}" role="tabpanel" aria-label="{yr}"{"" if i == 1 else " hidden"}>\n<div class="table-wrap"><table><thead><tr><th>#</th><th>Topic</th><th>Term</th><th>Learning outcomes</th><th>Game</th></tr></thead><tbody>{rows}</tbody></table></div>\n    </div>\n'

main = f'''<main id="main">

<section class="hero">
  <div class="wrap">
    <div class="hero-copy">
      <span class="pill">Junior Cycle English · Higher &amp; Ordinary</span>
      <h1>Leap up a grade in <span class="hl">English</span>.</h1>
      <p class="lede">Short, text-light games for every Junior Cycle English skill, from commas to comparing poems, each with the rules, a printable practice sheet and an Exam corner. Built around skills, so it works whatever novel, play or film your class is studying. Mapped to the official specification, 1st to 3rd year.</p>
      <div class="hero-actions">
        <a class="btn" href="junior-cycle-english-checklist.html">My topic checklist</a>
        <a class="btn ghost" href="#exam">How the exam works</a>
      </div>
      <p style="margin-top:14px;font-size:15px;color:#C9D1DA">The first English games, <a href="word-sort.html" style="color:#F6CF5A">Word Sort</a> and <a href="sentence-surgeon.html" style="color:#F6CF5A">Sentence Surgeon</a>, are live. More are on the way: sign up and we'll tell you when they're ready.</p>
    </div>
    {signup}</section>

<section class="block night" id="exam" style="scroll-margin-top:90px">
  <div class="wrap">
    <div class="sec-head">
      <h2>How the exam works</h2>
      <p>One written paper in June of 3rd year, at Higher or Ordinary level, set and marked by the State Examinations Commission.</p>
    </div>
    <div class="stats">
      <div class="stat"><b>2 hours</b><span>one paper at each level</span></div>
      <div class="stat"><b>180</b><span>marks for the paper</span></div>
      <div class="stat"><b>1 theme</b><span>every question links to the paper's theme, and the sections and their marks change from year to year</span></div>
      <div class="stat"><b>2 CBAs</b><span>Oral Communication (2nd year) and the Collection of the Student's Texts (3rd year); students sitting in 2027 and 2028 do only one</span></div>
    </div>
    <p style="color:#C9D1DA;margin-top:24px;font-size:15px">Because the layout changes every year, you can't learn the paper off by heart. What you can learn are the skills it always tests: reading closely, answering the exact question, backing up a point with a short quote, and writing clearly for a reader. That's what every Léim English topic practises.</p>
  </div>
</section>

<section class="block" id="texts" style="scroll-margin-top:90px">
  <div class="wrap">
    <div class="sec-head">
      <h2>What you study</h2>
      <p>Over 2nd and 3rd year your teacher picks the texts from the Department of Education's lists.</p>
    </div>
    <div class="grid">
      <div class="card"><h3>From the prescribed lists</h3><p>2 novels, 2 drama texts (an extract or extracts can count as one) and 1 film.</p></div>
      <div class="card"><h3>Poems, stories and more</h3><p>At least 16 poems, a number of short stories, and a range of non-literary texts such as articles, ads, speeches and web pages, including spoken ones.</p></div>
      <div class="card"><h3>Higher Level only</h3><p>One full Shakespeare play.</p></div>
      <div class="card"><h3>Which list is yours?</h3><p>Sitting the exam in <b>2027</b>: Circular 0051/2024 (the same list as 2024–2026). Sitting in <b>2028, 2029 or 2030</b>: the new list in Circular 0038/2025. Your teacher will know which texts your class is doing.</p></div>
    </div>
    <div class="note" style="margin-top:22px"><b>Does Léim cover my novel?</b> Our English topics teach the skills the exam asks for (character, setting, theme, key scenes, point–quote–explain) using short original texts written by us. You then use the same skills on whichever novel, play or film your class studied.</div>
  </div>
</section>

<section class="block mist" id="cba" style="scroll-margin-top:90px">
  <div class="wrap">
    <div class="sec-head">
      <h2>The two CBAs</h2>
      <p>Classroom-Based Assessments are done in class, judged by your teacher and reported on the Junior Cycle Profile of Achievement (JCPA), separately from the exam.</p>
    </div>
    <div class="grid">
      <div class="card"><span class="pill">CBA 1 · 2nd year</span><h3>Oral Communication</h3><p>You pick a topic and a format (on your own or in a group), research and prepare it, then present it to the class. You also write a short Student Reflection Note. Your teacher judges it against four descriptors.</p></div>
      <div class="card"><span class="pill">CBA 2 · 3rd year</span><h3>Collection of the Student's Texts</h3><p>Over 2nd and 3rd year you build a collection of your own writing in different genres, choose pieces and redraft them, and write a Student Reflection Note. Judged against four descriptors.</p></div>
    </div>
    <p style="margin-top:18px;font-size:15px;color:var(--muted)">Students sitting Junior Cycle in 2027 and 2028 complete only one CBA per subject, so ask the teacher which one your class is doing. The written Assessment Task linked to CBA 2 has not been required in recent years. Free guides for both CBAs are on the way.</p>
    <p style="margin-top:12px"><a class="btn ghost" href="junior-cycle-cbas.html#english" style="color:var(--ink);border-color:var(--line)">CBAs explained for parents →</a></p>
  </div>
</section>

<section class="block" id="games" style="scroll-margin-top:90px">
  <div class="wrap">
    <div class="sec-head">
      <h2>English games</h2>
      <p>Quick games with very little text on screen, each with the rules, an Exam corner and a free printable practice sheet underneath. No login needed. Topics are added in the order schools teach them.</p>
    </div>
    <div class="grid">
{cards}
    </div>
  </div>
</section>

<section class="block mist" id="teacher-packs" style="scroll-margin-top:90px">
  <div class="wrap">
    <div class="sec-head">
      <h2>For teachers</h2>
      <p>Print, cut and go. Each pack has teacher notes, a speaking activity, a card game, a wall poster and a worksheet with answers, mapped to the 2015 Junior Cycle English specification.</p>
    </div>
    <div class="grid">
      <a class="card" href="https://payhip.com/b/f97Ip" target="_blank" rel="noopener" style="text-decoration:none;color:inherit"><h3>Parts of Speech Teacher Pack · €5</h3><p>Upgrade Match mingle cards, Story Swap A/B cards, Word Class Dominoes, poster, worksheet + answers. About 60 minutes of class time.</p><p style="margin-top:10px;color:var(--green);font-weight:700">Get the pack on Payhip ↗</p></a>
    </div>
  </div>
</section>

<section class="block"><div class="wrap"><div class="note" style="display:flex;flex-wrap:wrap;gap:12px;align-items:center;justify-content:space-between"><div><strong>My English topic checklist.</strong> All {len(ENGLISH)} topics from 1st to 3rd year in one list, so you can see the whole course: tick off each step, rate how confident you feel, and print a copy for the fridge or school folder. Free, no login.</div><div style="display:flex;gap:10px;flex-wrap:wrap"><a class="btn" href="junior-cycle-english-checklist.html">Open the checklist</a><a class="btn ghost" href="printables/junior-cycle-english-topic-checklist.pdf" target="_blank" rel="noopener" style="color:var(--ink);border-color:var(--line)">Print it (PDF)</a></div></div></div></section>

<section class="block mist" id="units">
  <div class="wrap">
    <div class="sec-head">
      <h2>{len(ENGLISH)} topics across three years</h2>
      <p>The whole course in the order most schools teach it, with the learning outcome codes from the 2015 specification (OL = Oral language, R = Reading, W = Writing). Shakespeare is Higher Level only.</p>
    </div>
    <div class="years" role="tablist" aria-label="Choose a year">
      <button role="tab" aria-selected="true" aria-controls="y1">1st year</button>
      <button role="tab" aria-selected="false" aria-controls="y2">2nd year</button>
      <button role="tab" aria-selected="false" aria-controls="y3">3rd year</button>
    </div>
{tabs}  </div>
</section>

<section class="block">
  <div class="wrap">
    <div class="sec-head"><h2>Questions</h2></div>
    <details><summary>Which specification do you follow?</summary><p>The Junior Cycle English specification (2015, with small changes in 2018), which all current 1st, 2nd and 3rd years follow. Every game, sheet and pack is tagged with its learning outcome codes (for example W11), so you can match it to your child's school work.</p></details>
    <details><summary>Higher or Ordinary level?</summary><p>The games and sheets work for both levels. Shakespeare is Higher Level only, and where a topic goes further at Higher Level we say so on the topic page.</p></details>
    <details><summary>Why aren't there games about my novel or play?</summary><p>Schools choose different texts from the lists, and the exam asks about skills, not one set book. So each topic uses short texts written by us to practise a skill (for example how a writer shows character), and students then use that skill on their own texts.</p></details>
    <details><summary>Do students need an account?</summary><p>No. Students just play. Parents and teachers can sign up for the free parent guide and news of new topics.</p></details>
    <details><summary>Are you connected to the SEC or the NCCA?</summary><p>No. Léim is an independent revision service. All questions and texts are written by us in the style of the exam; we never copy past papers.</p></details>
  </div>
</section>

<section class="night cta">
  <div class="wrap">
    <div>
      <h2>Get the free parent guide</h2>
      <p><em>How to Get Your Child into College</em>: CAO points, entry requirements and every other route in, plus news when the English games go live.</p>
    </div>
    <a class="btn" href="#join">Send me the guide</a>
  </div>
</section>

'''
open("junior-cycle-english.html", "w", encoding="utf-8").write(head + main + foot)
print("ok")
