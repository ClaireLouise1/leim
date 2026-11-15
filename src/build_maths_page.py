#!/usr/bin/env python3
"""Builds junior-cycle-maths.html from the Spanish page's header/sign-up/footer + checklist_data.MATHS.
Run from the repo root after changing checklist_data.py: python3 src/build_maths_page.py"""
import os, re, sys, html
sys.path.insert(0, os.path.dirname(__file__))
from checklist_data import MATHS
e = html.escape
T = open("junior-cycle-spanish.html", encoding="utf-8").read()
head = T[:T.index('<main id="main">')]
head = re.sub(r"<title>.*?</title>", "<title>Junior Cycle Maths revision | Léim</title>", head)
head = re.sub(r'<meta name="description" content=".*?">', '<meta name="description" content="Free Junior Cycle Maths revision games mapped to the 2018 specification: integers, BIMDAS and more, with rules, free printable sheets, an exam corner for every topic and a topic checklist for 1st to 3rd year.">', head)
head = head.replace(' aria-current="page"', "").replace('<a href="junior-cycle-maths.html">', '<a href="junior-cycle-maths.html" aria-current="page">')
head = head.replace('<a href="subjects.html">Subjects</a>', '<a href="subjects.html" aria-current="page">Subjects</a>', 1)  # new tab bar (15 Nov)
signup = T[T.index('<div class="signup" id="join">'):T.index('</section>', T.index('<div class="signup" id="join">'))]
foot = T[T.index("</main>"):]

DESC = {"integer-rush.html": "negative numbers, the signs rules, BIMDAS and the number line, with an Exam corner of exam-style questions.",
        "prime-smash.html": "spot the primes, factor trees, products of primes, HCF and LCM, with an Exam corner of exam-style questions.",
        "fraction-match.html": "fraction pictures, simplest form, mixed numbers, +, −, × and ÷ with fractions and fractions of amounts, with an Exam corner of exam-style questions.",
        "round-it.html": "place value, comparing decimals, decimal sums, rounding to decimal places and significant figures, and estimating to check an answer, with an Exam corner of exam-style questions.",
        "venn-sorter.html": "sorting into Venn diagrams, set notation (∩, ∪, \\, ′, ∈, ⊂, #), naming shaded regions and survey questions with x, with an Exam corner of exam-style questions.",
        "percent-pop.html": "fractions ↔ decimals ↔ percentages, percentage of an amount, sale prices and multipliers, percentage change and finding the price before the sale, with an Exam corner of exam-style questions.",
        "share-it-out.html": "sharing money in a ratio (bar models), simplifying ratios, recipes and the unitary method, map scales, best buys and absolute v relative comparison, with an Exam corner of exam-style questions.",
        "like-term-sweep.html": "collecting like terms (with x² and minus signs), algebra tiles, writing expressions from words, substituting negative numbers and spotting equal expressions, with an Exam corner of exam-style questions.",
        "pattern-builder.html": "matchstick and tile patterns, the common difference, the general term Tₙ, far-away terms, tables and graphs, start value and rate of change, with an Exam corner of exam-style questions.",
        "clock-dash.html": "the 24-hour clock, reading clock faces, time differences by counting on, metric units of length, mass and capacity, hours and minutes as decimals, and Cork bus timetables, with an Exam corner of exam-style questions."}
live = [r for r in MATHS if r[5]]
cards = "\n".join(f'      <a class="card" href="{r[5]}" style="text-decoration:none;color:inherit"><h3>{e(r[4])}</h3><p>{e(r[2])}: {DESC.get(r[5], "")}</p><p style="margin-top:10px;color:var(--green);font-weight:700">Play {e(r[4])} →</p></a>' for r in live)
nxt = [r for r in MATHS if not r[5]][:3]
cards += "\n" + "\n".join(f'      <div class="card" style="opacity:.75"><span class="pill" style="background:var(--mist);color:var(--muted)">Coming next</span><h3>{e(r[4])}</h3><p>{e(r[2])}</p></div>' for r in nxt)

tabs = ""
for i, yr in enumerate(["1st year", "2nd year", "3rd year"], 1):
    rows = "".join(
        f'<tr><td class="num">{n}</td><td><b>{e(r[2])}</b>{"" if r[5] else " <em>(coming soon)</em>"}</td><td>{e(r[1])}</td><td>{e(r[3])}</td><td>{f"<a href={chr(34)}{r[5]}{chr(34)}>{e(r[4])}</a>" if r[5] else e(r[4])}</td></tr>'
        for n, r in enumerate(MATHS, 1) if r[0].startswith(yr[:3]))
    tabs += f'    <div id="y{i}" role="tabpanel" aria-label="{yr}"{"" if i == 1 else " hidden"}>\n<div class="table-wrap"><table><thead><tr><th>#</th><th>Topic</th><th>Term</th><th>Learning outcomes</th><th>Game</th></tr></thead><tbody>{rows}</tbody></table></div>\n    </div>\n'

main = f'''<main id="main">

<section class="hero">
  <div class="wrap">
    <div class="hero-copy">
      <span class="pill">Junior Cycle Maths · Higher &amp; Ordinary</span>
      <h1>Leap up a grade in <span class="hl">Maths</span>.</h1>
      <p class="lede">Free 60-second games for every Junior Cycle Maths topic, each with the rules, a printable practice sheet and an Exam corner showing where the marks are. Mapped to the official specification, 1st to 3rd year.</p>
      <div class="hero-actions">
        <a class="btn" href="integer-rush.html">Play Integer Rush</a>
        <a class="btn ghost" href="junior-cycle-maths-checklist.html">My topic checklist</a>
      </div>
    </div>
    {signup}</section>

<section class="block night">
  <div class="wrap">
    <div class="sec-head">
      <h2>How the exam works</h2>
      <p>One written paper in June, at Higher or Ordinary level, set and marked by the State Examinations Commission.</p>
    </div>
    <div class="stats">
      <div class="stat"><b>2 hours</b><span>for the Higher and the Ordinary paper (2026)</span></div>
      <div class="stat"><b>270</b><span>marks at both levels (2026)</span></div>
      <div class="stat"><b>13</b><span>questions, and every one must be answered: there is no choice</span></div>
      <div class="stat"><b>1+ CBA</b><span>at least one in class (a Mathematical or a Statistical Investigation; most schools do one), reported separately on the JCPA</span></div>
    </div>
    <p style="color:#C9D1DA;margin-top:24px;font-size:15px">Because every question is compulsory, every topic matters. See exactly how the Higher and Ordinary papers are marked, question by question, in the Maths Exam Centre.</p>
    <p style="margin-top:16px"><a class="btn" href="junior-cycle-maths-exam-centre.html">Open the Maths Exam Centre →</a></p>
  </div>
</section>

<section class="block mist" id="games" style="scroll-margin-top:90px">
  <div class="wrap">
    <div class="sec-head">
      <h2>Free Maths games</h2>
      <p>60-second games, each with the rules, an Exam corner and a free printable practice sheet underneath. No login needed. New topics are added in the order schools teach them.</p>
    </div>
    <div class="grid">
{cards}
    </div>
  </div>
</section>

<section class="block"><div class="wrap"><div class="note" style="display:flex;flex-wrap:wrap;gap:12px;align-items:center;justify-content:space-between"><div><strong>My Maths topic checklist.</strong> All {len(MATHS)} topics from 1st to 3rd year in one list: tick off the game, the rules and the revision sheet, and rate how confident you feel. Free, no login, and there's a printable copy for the fridge.</div><a class="btn" href="junior-cycle-maths-checklist.html">Open the checklist →</a></div></div></section>

<section class="block" id="teacher-packs" style="scroll-margin-top:90px">
  <div class="wrap">
    <div class="sec-head">
      <h2>For teachers: ready-to-teach packs</h2>
      <p>Print, cut and go. Each pack has teacher notes, a whole-class activity, a card game, a wall poster and a worksheet with answers, mapped to the 2018 Junior Cycle Mathematics specification.</p>
    </div>
    <div class="grid">
      <a class="card" href="https://payhip.com/b/UEp6b" target="_blank" rel="noopener" style="text-decoration:none;color:inherit"><h3>Integers &amp; Order of Operations Teacher Pack · €5</h3><p>Human Number Line, Find Your Match mingle, Integer Dominoes, BIMDAS poster, worksheet + answers. About 60 minutes of class time.</p><p style="margin-top:10px;color:var(--green);font-weight:700">Get the pack on Payhip ↗</p></a>
      <a class="card" href="https://payhip.com/b/w72tX" target="_blank" rel="noopener" style="text-decoration:none;color:inherit"><h3>Factors, Multiples &amp; Primes Teacher Pack · €5</h3><p>Sieve of Eratosthenes, Number Detective line-up, HCF &amp; LCM Dominoes, poster, worksheet + answers. About 60 minutes of class time.</p><p style="margin-top:10px;color:var(--green);font-weight:700">Get the pack on Payhip ↗</p></a>
      <a class="card" href="https://payhip.com/b/KBrk8" target="_blank" rel="noopener" style="text-decoration:none;color:inherit"><h3>Fractions Teacher Pack · €5</h3><p>Fraction Wall, Find Your Match cards, Fraction Dominoes, poster, worksheet + answers. About 60 minutes of class time.</p><p style="margin-top:10px;color:var(--green);font-weight:700">Get the pack on Payhip ↗</p></a>
      <a class="card" href="https://payhip.com/b/DkYZR" target="_blank" rel="noopener" style="text-decoration:none;color:inherit"><h3>Decimals &amp; Rounding Teacher Pack · €5</h3><p>Human Number Line, Estimation Auction, Rounding Dominoes, poster, worksheet + answers. About 60 minutes of class time.</p><p style="margin-top:10px;color:var(--green);font-weight:700">Get the pack on Payhip ↗</p></a>
      <a class="card" href="https://payhip.com/b/XT1Jl" target="_blank" rel="noopener" style="text-decoration:none;color:inherit"><h3>Sets &amp; Venn Diagrams Teacher Pack · €5</h3><p>Human Venn Diagram, Class Survey with x, Venn Dominoes, poster, worksheet + answers. About 60 minutes of class time.</p><p style="margin-top:10px;color:var(--green);font-weight:700">Get the pack on Payhip ↗</p></a>
      <a class="card" href="https://payhip.com/b/zNCQ4" target="_blank" rel="noopener" style="text-decoration:none;color:inherit"><h3>Percentages Teacher Pack · €5</h3><p>Percent Trios, Sale Shop role-play, Percentage Dominoes, poster, worksheet + answers. About 60 minutes of class time.</p><p style="margin-top:10px;color:var(--green);font-weight:700">Get the pack on Payhip ↗</p></a>
      <a class="card" href="https://payhip.com/b/E1WXq" target="_blank" rel="noopener" style="text-decoration:none;color:inherit"><h3>Ratio &amp; Proportion Teacher Pack · €5</h3><p>Share It Out mingle, Recipe Swap A/B cards, Ratio Dominoes, poster, worksheet + answers. About 60 minutes of class time.</p><p style="margin-top:10px;color:var(--green);font-weight:700">Get the pack on Payhip ↗</p></a>
      <a class="card" href="https://payhip.com/b/JjUGh" target="_blank" rel="noopener" style="text-decoration:none;color:inherit"><h3>Variables &amp; Expressions Teacher Pack · €5</h3><p>Think of a Number, Algebra Tiles Match cards, Algebra Dominoes, poster, worksheet + answers. About 60 minutes of class time.</p><p style="margin-top:10px;color:var(--green);font-weight:700">Get the pack on Payhip ↗</p></a>
      <a class="card" href="https://payhip.com/b/TqQer" target="_blank" rel="noopener" style="text-decoration:none;color:inherit"><h3>Linear Patterns &amp; Sequences Teacher Pack · €5</h3><p>Build It matchstick task, Pattern Detectives cards, Pattern Dominoes, poster, worksheet + answers. About 60 minutes of class time.</p><p style="margin-top:10px;color:var(--green);font-weight:700">Get the pack on Payhip ↗</p></a>
    </div>
  </div>
</section>

<section class="block mist" id="units">
  <div class="wrap">
    <div class="sec-head">
      <h2>{len(MATHS)} topics across three years</h2>
      <p>The whole course in the order most schools teach it, with the learning outcome codes from the 2018 specification. Some topics have extra Higher level parts.</p>
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
    <details><summary>Which specification do you follow?</summary><p>The Junior Cycle Mathematics specification (2018), which all current 1st, 2nd and 3rd years follow. Every game, sheet and pack is tagged with its learning outcome codes (for example N.1a), so you can match it to your child's school work.</p></details>
    <details><summary>Higher or Ordinary level?</summary><p>The games and sheets work for both levels. Where a topic has extra Higher level parts, we say so on the topic page.</p></details>
    <details><summary>Do students need an account?</summary><p>No. Students just play. Parents and teachers can sign up for the free parent guide and news of new topics.</p></details>
    <details><summary>Are you connected to the SEC or the NCCA?</summary><p>No. Léim is an independent revision service. All questions are written by us in the style of the exam; we never copy past papers.</p></details>
  </div>
</section>

<section class="night cta">
  <div class="wrap">
    <div>
      <h2>Get the free parent guide</h2>
      <p><em>How to Get Your Child into College</em>: CAO points, the 25 bonus points for Higher Maths, entry requirements and every other route in.</p>
    </div>
    <a class="btn" href="#join">Send me the guide</a>
  </div>
</section>

'''
open("junior-cycle-maths.html", "w", encoding="utf-8").write(head + main + foot)
print("ok")
