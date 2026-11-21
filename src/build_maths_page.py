#!/usr/bin/env python3
"""Builds junior-cycle-maths-guide.html (the long parents/teachers course guide; since 21 Nov 2026 the student page junior-cycle-maths.html is built by build_subject_hub.py — after running this, run build_subject_hub.py too) from the Spanish page's header/sign-up/footer + checklist_data.MATHS.
Run from the repo root after changing checklist_data.py: python3 src/build_maths_page.py"""
import os, re, sys, html
sys.path.insert(0, os.path.dirname(__file__))
from checklist_data import MATHS
e = html.escape
T = open("junior-cycle-spanish-guide.html", encoding="utf-8").read()
head = T[:T.index('<main id="main">')]
head = re.sub(r"<title>.*?</title>", "<title>Junior Cycle Maths: course guide for parents &amp; teachers | Léim</title>", head)
head = re.sub(r'<meta name="description" content=".*?">', '<meta name="description" content="Free Junior Cycle Maths revision games mapped to the 2018 specification: integers, BIMDAS and more, with rules, free printable sheets, an exam corner for every topic and a topic checklist for 1st to 3rd year.">', head)
head = head.replace(' aria-current="page"', "").replace('<a href="junior-cycle-maths.html">', '<a href="junior-cycle-maths.html" aria-current="page">')
# (Subjects tab removed 21 Nov 2026)
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
        "clock-dash.html": "the 24-hour clock, reading clock faces, time differences by counting on, metric units of length, mass and capacity, hours and minutes as decimals, and Cork bus timetables, with an Exam corner of exam-style questions.",
        "spin-and-predict.html": "the probability scale, equally likely outcomes with dice, cards, counters and spinners, P(not A), listing sample spaces, two-way tables and tree diagrams, with an Exam corner of exam-style questions.",
        "data-detective.html": "nominal, ordinal, discrete or continuous data, statistical questions, population v sample, biased samples and leading questions, tally marks and frequency tables, and the four stages of an investigation (CBA 2), with an Exam corner of exam-style questions.",
        "angle-chase.html": "find the missing angle and name the reason: straight lines, angles at a point, vertically opposite angles, triangles, isosceles triangles, exterior angles and parallel lines (alternate, corresponding, co-interior), with two-step chases and an Exam corner of exam-style questions.",
        "construction-steps.html": "watch each of the 15 constructions drawn step by step and pick the next step: bisectors, perpendiculars, parallel lines, equal parts, angles and SSS, SAS, ASA and RHS triangles, plus the right tools and an Exam corner of exam-style constructions.",
        "bracket-blaster.html": "multiplying terms, expanding one bracket (with minus signs and letters outside), expand and simplify, double brackets with the area model, squaring a bracket, the difference of two squares and spot-the-slip, with an Exam corner of exam-style questions.",
        "balance-it.html": "balance-scale pictures, one- and two-step equations, letters on both sides, brackets, fractions, forming equations from words and spot-the-slip, with an Exam corner of exam-style questions.",
        "power-up.html": "powers and square roots, (−3)² v −3², BIMDAS with indices, the laws of indices (with numbers in front), find n, standard form both ways, comparing and calculating in standard form, and a Higher Level round on zero, negative and fractional indices, with an Exam corner of exam-style questions.",
        "shop-keeper.html": "add up receipts and give change, electricity bills from meter readings, phone plans and call-out charges, add VAT and find the price before VAT, sale prices, profit and loss and % profit on the cost price, value for money and best buys, and Higher Level mark-up and margin, with an Exam corner of exam-style questions.",
        "payslip-puzzle.html": "gross pay and overtime, payslips with a missing line, income tax with a tax credit, net pay, compound interest on savings and loans for up to 3 years with year-by-year tables, spot-the-slip working, and Higher Level cut-off points and working backwards, with an Exam corner of exam-style questions.",
        "road-trip.html": "speed, distance and time, minutes as decimals of an hour, arrival times, average speed for journeys with stops and the round-trip trap, km/h and m/s, distance–time graphs, and changing euro into sterling, dollars and Swiss francs (and back), with commission and price comparisons, with an Exam corner of exam-style questions.",
        "floor-planner.html": "the area and perimeter of rectangles, L-shaped rooms, triangles, parallelograms and circles, π (calculator, 3.14, 22/7 and in terms of π), semicircles and quarter circles, pricing a floor, packs and tiles, scale drawings, plans and maps, with an Exam corner of exam-style questions.",
        "average-ace.html": "mean, median, mode and range from lists and frequency tables, the missing value and the new mean, grouped data, bar charts, pie chart angles, line plots, histograms, ordered and back-to-back stem-and-leaf plots, the best display and average, misleading charts and what a sample can show, with an Exam corner of exam-style questions.",
        "mirror-move.html": "axial symmetry in the x-axis, the y-axis and other lines, translations, central symmetry in the origin and other points, rotations of 90° clockwise and anticlockwise, naming the transformation that maps S onto S′, completing symmetric patterns, and axes and centres of symmetry of shapes, with an Exam corner of exam-style questions.",
        "proof-builder.html": "fill the missing reason in real geometry proofs and put the steps in order, parallelograms (opposite sides and angles, diagonals), the angle in a semicircle, congruent triangles (SSS, SAS, ASA, RHS), similar triangles and scale factors, plus Higher Level circle theorems, with an Exam corner of exam-style questions.",
        "ladder-lab.html": "find the hypotenuse and the shorter sides of right-angled triangles, square roots, \"which calculation?\" and spot the mistake, the converse of Pythagoras' theorem and Pythagorean triples, ladders, screens, isosceles triangles, shortcuts and journeys, with an Exam corner of exam-style questions.",
        "coin-dice-lab.html": "relative frequency from experiments, tables and bar charts, putting results together, expected frequency, fair or biased dice and spinners, the relative-frequency graph, and the fundamental principle of counting for menus, outfits, codes and medals, with a coin-and-dice lab and an Exam corner of exam-style questions.",
        "factor-match.html": "take out the highest common factor, factorise four terms by grouping, x² + bx + c with the area model backwards, the difference of two squares and \"which is FULLY factorised?\", plus Higher Level ax² + bx + c, with an Exam corner of exam-style questions.",
        "line-lab.html": "slope from two points and from a graph, slope as a rate of change, midpoints, distances, y = mx + c, finding the equation of a line, points on a line, parallel lines and where lines meet, plus Higher Level perpendicular lines and ax + by + c = 0, with an Exam corner of exam-style questions.",
        "two-line-crossing.html": "checking a solution, solving simultaneous equations by elimination and substitution, reading where two lines cross, spotting the first mistake in someone's working, and ticket, price and number word problems, plus Higher Level fractions, with an Exam corner of exam-style questions.",
        "root-rush.html": "finding the roots of a quadratic, solving quadratic equations by factorising (including x² + bx = 0 and x² = k), spotting the first mistake in someone's working, writing the equation from its roots, and area, number and ball word problems, plus Higher Level 2x², the formula and finding k, with an Exam corner of exam-style questions.",
        "graph-match.html": "what a function is, f(x) notation and mapping diagrams, reading roots, turning points and solutions of f(x) = k from quadratic graphs, matching graphs to real-life stories, and telling linear, quadratic and exponential functions apart, plus Higher Level f(x) = g(x) and exponential functions, with an Exam corner of exam-style questions.",
        "clinometer-challenge.html": "sin, cos and tan with SOH CAH TOA: naming the opposite, adjacent and hypotenuse, finding a side, finding an angle with sin⁻¹, cos⁻¹ and tan⁻¹, and angles of elevation and depression for trees, kites, ladders, ramps and cliffs, plus Higher Level two-step problems, with an Exam corner of exam-style questions.",
        "pack-it.html": "volume and surface area of cuboids, cubes, triangular prisms, cylinders, spheres and hemispheres, nets, how many boxes fit, litres, water rising and silos, with π, plus Higher Level working backwards and melting, with an Exam corner of exam-style questions.",
        "number-line-shade.html": "reading and drawing inequalities on a number line (open and closed dots, ℕ, ℤ and ℝ), solving linear inequalities, listing, counting and finding the biggest or smallest whole-number answer, taxi, lift and savings problems and reading a solution from a graph, plus Higher Level flips, double inequalities and fractions, with an Exam corner of exam-style questions.",
        "rearrange-race.html": "changing the subject of a formula (v = u + at, A = ½bh, F = 1.8C + 32), using the rearranged formula, adding and subtracting algebraic fractions, long division of a quadratic by a bracket and spotting the first mistake in someone's working, plus Higher Level fractions with x on the bottom, square-root formulas, the subject appearing twice and cubics",
        "growth-spotter.html": "telling linear, quadratic and exponential patterns apart, 1st and 2nd differences, next and missing terms, growing tile patterns, doubling and tripling, plus Higher Level general terms Tₙ = an² + bn + c",
        "surd-simplify.html": "simplifying surds like √72 = 6√2, adding like surds, multiplying, dividing and squaring surds, plus Higher Level brackets with surds",
        "exam-mix.html": "questions from every Maths topic mixed like the real paper, plus two-step problems that join topics: area and cost, speed and arrival time, mean working backwards"}
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
    <p style="color:#C9D1DA;margin-top:14px;font-size:15px">Want two full mock papers (Higher and Ordinary) with worked solutions and where the marks would go? <a href="https://payhip.com/b/e9F6G" target="_blank" rel="noopener" style="color:#fff;font-weight:700">Get the Junior Cycle Maths Exam Pack (€12) ↗</a></p>
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
      <a class="card" href="https://payhip.com/b/BEKe8" target="_blank" rel="noopener" style="text-decoration:none;color:inherit"><h3>Units, Time &amp; Timetables Teacher Pack · €5</h3><p>Unit Line-Up cards, Timetable Swap A/B, Time Dominoes, poster, worksheet + answers. About 60 minutes of class time.</p><p style="margin-top:10px;color:var(--green);font-weight:700">Get the pack on Payhip ↗</p></a>
      <a class="card" href="https://payhip.com/b/JEfN5" target="_blank" rel="noopener" style="text-decoration:none;color:inherit"><h3>Probability Teacher Pack · €5</h3><p>Probability Line-Up cards, Fair Game? two-dice cards, Probability Dominoes, poster, worksheet + answers. About 60 minutes of class time.</p><p style="margin-top:10px;color:var(--green);font-weight:700">Get the pack on Payhip ↗</p></a>
      <a class="card" href="https://payhip.com/b/zR8y6" target="_blank" rel="noopener" style="text-decoration:none;color:inherit"><h3>Statistics Teacher Pack · €5</h3><p>Data Sort cards, Fix the Survey, Data Dominoes, poster, worksheet + answers. About 60 minutes of class time.</p><p style="margin-top:10px;color:var(--green);font-weight:700">Get the pack on Payhip ↗</p></a>
      <a class="card" href="https://payhip.com/b/IvGhA" target="_blank" rel="noopener" style="text-decoration:none;color:inherit"><h3>Lines, Angles &amp; Triangles Teacher Pack · €5</h3><p>Angle Sort cards, Angle Dominoes, poster, worksheet + answers. About 60 minutes of class time.</p><p style="margin-top:10px;color:var(--green);font-weight:700">Get the pack on Payhip ↗</p></a>
      <a class="card" href="https://payhip.com/b/MBIZE" target="_blank" rel="noopener" style="text-decoration:none;color:inherit"><h3>Constructions Teacher Pack · €5</h3><p>Step Sort cards, Construction Dominoes, poster of all 15, worksheet + answers. About 60 minutes of class time.</p><p style="margin-top:10px;color:var(--green);font-weight:700">Get the pack on Payhip ↗</p></a>
      <a class="card" href="https://payhip.com/b/9Kp26" target="_blank" rel="noopener" style="text-decoration:none;color:inherit"><h3>Expanding &amp; Simplifying Teacher Pack · €5</h3><p>Bracket Relay, Area Model Match cards, Expanding Dominoes, poster, worksheet + answers. About 60 minutes of class time.</p><p style="margin-top:10px;color:var(--green);font-weight:700">Get the pack on Payhip ↗</p></a>
      <a class="card" href="https://payhip.com/b/BVXpM" target="_blank" rel="noopener" style="text-decoration:none;color:inherit"><h3>Linear Equations Teacher Pack · €5</h3><p>Equation Relay, Word-to-Equation Match cards, Equation Dominoes, poster, worksheet + answers. About 60 minutes of class time.</p><p style="margin-top:10px;color:var(--green);font-weight:700">Get the pack on Payhip ↗</p></a>
      <a class="card" href="https://payhip.com/b/hfkvt" target="_blank" rel="noopener" style="text-decoration:none;color:inherit"><h3>Indices &amp; Standard Form Teacher Pack · €5</h3><p>Index Law Match cards, Standard Form Line-Up, Index Dominoes, poster, worksheet + answers. About 60 minutes of class time.</p><p style="margin-top:10px;color:var(--green);font-weight:700">Get the pack on Payhip ↗</p></a>
      <a class="card" href="https://payhip.com/b/vbKBH" target="_blank" rel="noopener" style="text-decoration:none;color:inherit"><h3>Money: Bills, VAT, Profit &amp; Loss Teacher Pack · €5</h3><p>Market Day mingle cards, Bill Swap A/B cards, Money Dominoes, poster, worksheet + answers. About 60 minutes of class time.</p><p style="margin-top:10px;color:var(--green);font-weight:700">Get the pack on Payhip ↗</p></a>
      <a class="card" href="https://payhip.com/b/lc8Em" target="_blank" rel="noopener" style="text-decoration:none;color:inherit"><h3>Money: Income Tax, Net Pay &amp; Compound Interest Teacher Pack · €5</h3><p>Payday mingle cards, Payslip Swap A/B cards, Money Dominoes, poster, worksheet + answers. About 60 minutes of class time.</p><p style="margin-top:10px;color:var(--green);font-weight:700">Get the pack on Payhip ↗</p></a>
      <a class="card" href="https://payhip.com/b/ZXw9C" target="_blank" rel="noopener" style="text-decoration:none;color:inherit"><h3>Speed, Distance, Time &amp; Currency Teacher Pack · €5</h3><p>Road Trip mingle cards, Journey Swap A/B cards, Travel Dominoes, poster, worksheet + answers. About 60 minutes of class time.</p><p style="margin-top:10px;color:var(--green);font-weight:700">Get the pack on Payhip ↗</p></a>
      <a class="card" href="https://payhip.com/b/RM9rT" target="_blank" rel="noopener" style="text-decoration:none;color:inherit"><h3>Area, Perimeter &amp; Scale Drawings Teacher Pack · €5</h3><p>Floor Planner mingle cards, Plan Swap A/B cards, Area Dominoes, poster, worksheet + answers. About 60 minutes of class time.</p><p style="margin-top:10px;color:var(--green);font-weight:700">Get the pack on Payhip ↗</p></a>
      <a class="card" href="https://payhip.com/b/d9CQP" target="_blank" rel="noopener" style="text-decoration:none;color:inherit"><h3>Graphs &amp; Averages Teacher Pack · €5</h3><p>Average Ace mingle cards, Class Data Swap A/B cards, Statistics Dominoes, poster, worksheet + answers. About 60 minutes of class time.</p><p style="margin-top:10px;color:var(--green);font-weight:700">Get the pack on Payhip ↗</p></a>
      <a class="card" href="https://payhip.com/b/FU23r" target="_blank" rel="noopener" style="text-decoration:none;color:inherit"><h3>Transformations &amp; Symmetry Teacher Pack · €5</h3><p>Mirror Move mingle cards, Grid Swap A/B cards, Transformation Dominoes, poster, worksheet + answers. About 60 minutes of class time.</p><p style="margin-top:10px;color:var(--green);font-weight:700">Get the pack on Payhip ↗</p></a>
      <a class="card" href="https://payhip.com/b/iFC6S" target="_blank" rel="noopener" style="text-decoration:none;color:inherit"><h3>Theorems, Congruent &amp; Similar Triangles Teacher Pack · €5</h3><p>Proof Builder mingle cards, Proof Sort strips, Geometry Dominoes, poster, worksheet + answers. About 60 minutes of class time.</p><p style="margin-top:10px;color:var(--green);font-weight:700">Get the pack on Payhip ↗</p></a>
      <a class="card" href="https://payhip.com/b/VeTa4" target="_blank" rel="noopener" style="text-decoration:none;color:inherit"><h3>Pythagoras' Theorem Teacher Pack · €5</h3><p>Ladder Lab mingle cards, Triangle Swap A/B cards, Pythagoras Dominoes, poster, worksheet + answers. About 60 minutes of class time.</p><p style="margin-top:10px;color:var(--green);font-weight:700">Get the pack on Payhip ↗</p></a>
      <a class="card" href="https://payhip.com/b/Ec1Kr" target="_blank" rel="noopener" style="text-decoration:none;color:inherit"><h3>Relative Frequency &amp; Counting Teacher Pack · €5</h3><p>Class Experiment sheet, Coin &amp; Dice Lab mingle cards, Probability Dominoes, poster, worksheet + answers. About 60 minutes of class time.</p><p style="margin-top:10px;color:var(--green);font-weight:700">Get the pack on Payhip ↗</p></a>
      <a class="card" href="https://payhip.com/b/ENKsD" target="_blank" rel="noopener" style="text-decoration:none;color:inherit"><h3>Factorising Teacher Pack · €5</h3><p>Factor Relay, Factor Match mingle cards, Factorising Dominoes, poster, worksheet + answers. About 60 minutes of class time.</p><p style="margin-top:10px;color:var(--green);font-weight:700">Get the pack on Payhip ↗</p></a>
      <a class="card" href="https://payhip.com/b/urHTo" target="_blank" rel="noopener" style="text-decoration:none;color:inherit"><h3>Coordinate Geometry of the Line Teacher Pack · €5</h3><p>Line Lab mingle cards, Line Swap A/B cards, Line Dominoes, poster, worksheet + answers. About 60 minutes of class time.</p><p style="margin-top:10px;color:var(--green);font-weight:700">Get the pack on Payhip ↗</p></a>
      <a class="card" href="https://payhip.com/b/g8CDp" target="_blank" rel="noopener" style="text-decoration:none;color:inherit"><h3>Simultaneous Equations Teacher Pack · €5</h3><p>Crossing Point mingle cards, Ticket Swap A/B cards, Simultaneous Dominoes, poster, worksheet + answers. About 60 minutes of class time.</p><p style="margin-top:10px;color:var(--green);font-weight:700">Get the pack on Payhip ↗</p></a>
      <a class="card" href="https://payhip.com/b/UzcIf" target="_blank" rel="noopener" style="text-decoration:none;color:inherit"><h3>Quadratic Equations Teacher Pack · €5</h3><p>Root Match mingle cards, Garden Swap A/B cards, Quadratic Dominoes, poster, worksheet + answers. About 60 minutes of class time.</p><p style="margin-top:10px;color:var(--green);font-weight:700">Get the pack on Payhip ↗</p></a>
      <a class="card" href="https://payhip.com/b/Z1VJ9" target="_blank" rel="noopener" style="text-decoration:none;color:inherit"><h3>Functions &amp; Graphs Teacher Pack · €5</h3><p>Function Match mingle cards, Story Graph Swap A/B cards, Function Dominoes, poster, worksheet + answers. About 60 minutes of class time.</p><p style="margin-top:10px;color:var(--green);font-weight:700">Get the pack on Payhip ↗</p></a>
      <a class="card" href="https://payhip.com/b/ashv5" target="_blank" rel="noopener" style="text-decoration:none;color:inherit"><h3>Trigonometry Teacher Pack · €5</h3><p>Clinometer mingle cards, Height Swap A/B cards, Trigonometry Dominoes, poster, worksheet + answers. About 60 minutes of class time.</p><p style="margin-top:10px;color:var(--green);font-weight:700">Get the pack on Payhip ↗</p></a>
      <a class="card" href="https://payhip.com/b/NUr1Q" target="_blank" rel="noopener" style="text-decoration:none;color:inherit"><h3>Volume, Surface Area &amp; Nets Teacher Pack · €5</h3><p>Pack It mingle cards, Tank Swap A/B cards, Volume Dominoes, poster, worksheet + answers. About 60 minutes of class time.</p><p style="margin-top:10px;color:var(--green);font-weight:700">Get the pack on Payhip ↗</p></a>
      <a class="card" href="https://payhip.com/b/qMXR1" target="_blank" rel="noopener" style="text-decoration:none;color:inherit"><h3>Inequalities Teacher Pack · €5</h3><p>Shade Match mingle cards, Budget Swap A/B cards, Inequality Dominoes, poster, worksheet + answers. About 60 minutes of class time.</p><p style="margin-top:10px;color:var(--green);font-weight:700">Get the pack on Payhip ↗</p></a>
      <a class="card" href="https://payhip.com/b/qdWNU" target="_blank" rel="noopener" style="text-decoration:none;color:inherit"><h3>Algebraic Fractions &amp; Changing the Subject Teacher Pack · €5</h3><p>Rearrange Match mingle cards, Formula Swap A/B cards, Rearranging Dominoes, poster, worksheet + answers. About 60 minutes of class time.</p><p style="margin-top:10px;color:var(--green);font-weight:700">Get the pack on Payhip ↗</p></a>
      <a class="card" href="https://payhip.com/b/SMsFL" target="_blank" rel="noopener" style="text-decoration:none;color:inherit"><h3>Quadratic &amp; Exponential Patterns Teacher Pack · €5</h3><p>Growth Match mingle cards, Pattern Swap A/B cards, Pattern Dominoes, poster, worksheet + answers. About 60 minutes of class time.</p><p style="margin-top:10px;color:var(--green);font-weight:700">Get the pack on Payhip ↗</p></a>
      <a class="card" href="https://payhip.com/b/HJiI7" target="_blank" rel="noopener" style="text-decoration:none;color:inherit"><h3>Surds Teacher Pack · €5</h3><p>Surd Match mingle cards, Surd Swap A/B cards, Surd Dominoes, poster, worksheet + answers. About 60 minutes of class time.</p><p style="margin-top:10px;color:var(--green);font-weight:700">Get the pack on Payhip ↗</p></a>
      <a class="card" href="https://payhip.com/b/fk96q" target="_blank" rel="noopener" style="text-decoration:none;color:inherit"><h3>Problem Solving &amp; Exam Mix Teacher Pack · €5</h3><p>Two-Step Match mingle cards, Problem Swap A/B cards, Mixed Dominoes, poster, worksheet + answers. About 60 minutes of class time.</p><p style="margin-top:10px;color:var(--green);font-weight:700">Get the pack on Payhip ↗</p></a>
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
open("junior-cycle-maths-guide.html", "w", encoding="utf-8").write(head + main + foot)
print("ok")

# Free first (21 Nov 2026): keep every buy link hidden until launch — see src/free_first.py
if __name__ == "__main__":
    import sys as _ffs, os as _ffo
    _ffs.path.insert(0, _ffo.path.dirname(_ffo.path.abspath(__file__)))
    import free_first
    free_first.hide_all(quiet=False)
