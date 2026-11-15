import re
src=open('junior-cycle-spanish-exam-centre.html').read()
head=src.split('<main id="main">')[0]
foot='</main>'+src.split('</main>',1)[1]
def mkhead(title,desc):
    h=re.sub(r'<title>.*?</title>',f'<title>{title}</title>',head)
    h=re.sub(r'<meta name="description" content=".*?">',f'<meta name="description" content="{desc}">',h)
    h=h.replace('<a href="junior-cycle-spanish-exam-centre.html" aria-current="page">Exam Centre</a>','<a href="exam-centre.html" aria-current="page">Exam Centre</a>')
    assert 'href="exam-centre.html" aria-current' in h
    return h
extra_css='''<style>
.qt td,.qt th{white-space:normal}
.qt td:nth-child(3){white-space:nowrap}
.qt .num{text-align:center}
.scale{display:flex;flex-wrap:wrap;gap:6px;margin:6px 0 2px}
.scale span{background:var(--mist);border:1px solid var(--line);border-radius:8px;padding:4px 10px;font-weight:700;font-size:15px}
.scale span.f{background:var(--green);color:#fff;border-color:var(--green)}
.warn{background:#FFF6D6;border:1px solid #F0D27A;border-radius:12px;padding:16px 18px;margin:16px 0}
</style>
</head>'''
# ---------- Maths Exam Centre ----------
Q=[(1,10,'(a) 5C · (b) 5C',5),(2,15,'(a) 5D · (b) 10D',10),(3,15,'(a) 10D · (b)+(c) 5C',5),
(4,30,'(a) 10D · (b) 10B · (c) 5B · (d)+(e) 5C',10),(5,20,'(a)+(b) 10C · (c)+(d) 10D',5),
(6,30,'(a) 15C · (b)(i) 5D · (b)(ii) 5B · (c) 5D',10),(7,60,'(a)(i) 5B · (a)(ii) 10C · (b) 5C · (c) 15C · (d) 5C · (e) 20C',15),
(8,15,'(a) 5B · (b) 10C',5),(9,25,'(a)+(b) 5C · (c)+(d) 5D · (e) 10B · (f) 5B',15),(10,10,'(a) 5D · (b) 5B',5),
(11,15,'(a) 5C · (b) 10D',5),(12,15,'(a) 10D · (b) 5D',10),(13,10,'(a)+(b) 5D · (c) 5C',10)]
assert sum(q[1] for q in Q)==270 and sum(q[3] for q in Q)==110
# check parts sum
for n,t,p,_ in Q:
    s=sum(int(m) for m in re.findall(r'(\d+)[ABCD]',p)); assert s==t,(n,s,t)
rows=''.join(f'<tr><td><strong>Q{n}</strong></td><td class="num">{t}</td><td>{p.replace(" · ","<br>")}</td><td class="num">{m} min</td></tr>' for n,t,p,m in Q)
def sc(vals): 
    v=vals.split(',');return '<div class="scale">'+''.join(f'<span{" class=\"f\"" if i==len(v)-1 else ""}>{x.strip()}</span>' for i,x in enumerate(v))+'</div>'
main=f'''<main id="main">

<section class="hero">
  <div class="wrap">
    <div class="hero-copy">
      <span class="pill">Junior Cycle Maths · Higher level</span>
      <h1>The Maths <span class="hl">Exam Centre</span></h1>
      <p class="lede">How the Higher paper works, how every mark is given, and what to do when a question goes wrong. Based on the State Examinations Commission's published 2025 paper and marking scheme.</p>
      <nav class="toc" aria-label="On this page">
        <a href="#paper">The paper</a><a href="#marking">How it's marked</a><a href="#wrong">If you go wrong</a><a href="#strategies">Strategies</a><a href="#grades">Grades</a><a href="#parents">For parents</a>
      </nav>
    </div>
  </div>
</section>

<div class="block"><div class="wrap ec">

<section id="paper">
  <h2>The paper explained</h2>
  <p>Junior Cycle Higher level Maths is <strong>one written paper</strong> in June of 3rd year: <strong>2 hours</strong>, <strong>270 marks</strong>, <strong>13 questions</strong>. <strong>Every question must be answered.</strong> There is no choice, so every topic on the course matters.</p>
  <p>Here is how the marks were split on the 2025 paper. The letter after each mark (B, C, D) is the marking scale, explained in the next section. "+" means two parts were marked together.</p>
  <div class="table-wrap"><table class="qt">
    <thead><tr><th>Question</th><th>Marks</th><th>Parts and scales</th><th>Time*</th></tr></thead>
    <tbody>{rows}
      <tr><td><strong>Total</strong></td><td class="num"><strong>270</strong></td><td></td><td class="num"><strong>110 min</strong></td></tr>
    </tbody>
  </table></div>
  <p class="small" style="color:var(--muted)">*Time = the suggested maximum time printed on the paper for each question.</p>
  <p class="big"><strong>The big message:</strong> the questions are not equal. In 2025, Question 7 alone was worth 60 marks, more than a fifth of the paper. The suggested times add up to 110 minutes, which leaves about 10 minutes to check.</p>
  <p class="small" style="color:var(--muted)">The split changes every year. Use this to understand how the paper works, not to predict next June's paper.</p>
</section>

<section id="marking">
  <h2>How it's marked</h2>
  <p>Maths is <strong>not</strong> marked one mark per step. The examiner reads your whole answer to a part and decides which level it reaches. Each level is worth a fixed number of marks.</p>
  <h3>The levels</h3>
  <ul>
    <li><strong>No credit:</strong> nothing of real value.</li>
    <li><strong>Low partial credit:</strong> some useful work, for example a correct first step or the right formula.</li>
    <li><strong>Mid partial credit</strong> (D scales only): about half right.</li>
    <li><strong>High partial credit:</strong> almost there, for example the full method with a slip near the end.</li>
    <li><strong>Full credit:</strong> correct.</li>
  </ul>
  <h3>What each scale is worth</h3>
  <p><strong>B scale</strong> (no credit / partial / full)</p>
  <p class="small">5 marks:</p>{sc("0,3,5")}<p class="small">10 marks:</p>{sc("0,5,10")}
  <p style="margin-top:14px"><strong>C scale</strong> (no credit / low / high / full)</p>
  <p class="small">5 marks:</p>{sc("0,2,3,5")}<p class="small">10 marks:</p>{sc("0,4,6,10")}<p class="small">15 marks:</p>{sc("0,4,6,15")}<p class="small">20 marks:</p>{sc("0,4,7,20")}
  <p style="margin-top:14px"><strong>D scale</strong> (no credit / low / mid / high / full)</p>
  <p class="small">5 marks:</p>{sc("0,2,3,4,5")}<p class="small">10 marks:</p>{sc("0,4,5,6,10")}
  <div class="warn"><strong>Look at the 15 and 20-mark parts.</strong> Some good work gets you 4 marks. Almost right gets you 6 or 7. Only a <em>finished, correct</em> answer gets 15 or 20. On the big parts, finishing the question is worth more than everything before it put together.</div>
  <p>The examiner can only give a mark that is on the scale, or one mark below full (see below). So there are no "half marks".</p>
</section>

<section id="wrong">
  <h2>If you go wrong</h2>
  <h3>A small slip only costs 1 mark</h3>
  <p>If your answer is right apart from a small slip, you get <strong>full marks minus 1</strong> (for example 9 out of 10). This covers things like:</p>
  <ul>
    <li>rounding wrongly, or not rounding when asked</li>
    <li>leaving out the units (cm, €, m²…)</li>
    <li>a small arithmetic slip that doesn't make the question easier</li>
    <li>misreading a number, as long as it doesn't make the question easier</li>
  </ul>
  <p>You only lose the rounding mark once per part and the units mark once per question. If the question already gives the unit, you aren't penalised for leaving it out, and a missing € sign usually costs nothing.</p>
  <h3>A wrong answer in part (a) doesn't ruin part (b)</h3>
  <p>If you got (a) wrong, <strong>use your wrong answer in (b) and carry on</strong>. Examiners can accept work carried forward from an earlier part, as long as your mistake hasn't made the later part easier. You can still get full marks for (b).</p>
  <h3>Stuck? Write something down</h3>
  <ul>
    <li><strong>One line can be worth marks.</strong> Writing the right formula, putting numbers into it, or drawing a labelled diagram can lift you from 0 to low partial credit. That's 2 marks on a 5-mark part and 4 marks on a 10, 15 or 20-mark part.</li>
    <li><strong>Never leave a part blank.</strong> A blank always gets 0.</li>
    <li><strong>Any correct method counts.</strong> You don't have to use the method your teacher showed you, as long as it's correct.</li>
  </ul>
  <h3>Always show your work</h3>
  <p>An answer with no work behind it usually only gets the lowest mark above zero, even if it's right. Some parts do accept a correct answer on its own, but you can't know which in advance. Show every step.</p>
  <h3>Ran out of space?</h3>
  <p>Write all your answers in the exam booklet, inside the answer areas. There's extra space at the back: if you use it, <strong>label it with the question number and part</strong> (for example "Q7(c)"). Work written outside the answer areas might not be seen.</p>
</section>

<section id="strategies">
  <h2>Exam strategies</h2>
  <ol>
    <li><strong>Check the time on each question.</strong> Each question shows a suggested maximum time. If you go over, move on and come back at the end.</li>
    <li><strong>Collect the easy marks first.</strong> Every question is compulsory, but you can do them in any order. Do your strong ones first to build up marks and confidence.</li>
    <li><strong>Read the last line twice.</strong> "Give your answer correct to 2 decimal places", "in cm²", "as a fraction": these are the instructions that cost 1 mark when missed.</li>
    <li><strong>Round only at the end.</strong> Keep full calculator values until the final answer. Rounding too early can cost you marks.</li>
    <li><strong>Check your calculator is in degrees</strong> before any trigonometry question.</li>
    <li><strong>Use the Formulae and Tables booklet.</strong> You get one in the exam (you can't bring your own), so practise with it all year.</li>
    <li><strong>Finish the big parts.</strong> On a 15 or 20-mark part, the jump from "almost" to "correct" is worth 8 to 13 marks. Use your last 10 minutes on those.</li>
  </ol>
  <a class="card cardlink" href="junior-cycle-maths.html#games"><h3 style="margin:0">Practise topic by topic: free Maths games</h3><p>60-second games for each topic, each with the rules, a free printable sheet and an Exam corner of exam-style questions with worked answers.</p><p style="color:var(--green);font-weight:700">Play the Maths games →</p></a>
</section>

<section id="grades">
  <h2>Grades</h2>
  <p>Your marks out of 270 become a percentage, and the percentage gives the grade. These are the new grade bands used since the 2025 exams. The marks below are rounded.</p>
  <div class="table-wrap"><table>
    <thead><tr><th>Grade</th><th>Percentage</th><th>About this many marks out of 270</th></tr></thead>
    <tbody>
      <tr><td>Distinction</td><td>85–100%</td><td class="num">230+</td></tr>
      <tr><td>Higher Merit</td><td>70–84%</td><td class="num">189–229</td></tr>
      <tr><td>Merit</td><td>55–69%</td><td class="num">149–188</td></tr>
      <tr><td>Achieved</td><td>40–54%</td><td class="num">108–148</td></tr>
      <tr><td>Partially Achieved</td><td>20–39%</td><td class="num">54–107</td></tr>
      <tr><td>Not Graded</td><td>0–19%</td><td class="num">0–53</td></tr>
    </tbody>
  </table></div>
  <p>That means 27 marks is about 10%. One unfinished 20-mark part can be the difference between two grades.</p>
</section>

<section id="parents">
  <h2>For parents</h2>
  <ul>
    <li><strong>The June exam gives the grade.</strong> It's set and marked by the State Examinations Commission, at Higher or Ordinary level.</li>
    <li><strong>The CBA is separate.</strong> Students do one Classroom-Based Assessment in class (a Mathematical or a Statistical Investigation). It appears on the Junior Cycle Profile of Achievement, not in the exam grade.</li>
    <li><strong>Ask to see the working.</strong> When your child shows you homework, look for the steps, not just the answer. That habit is worth marks in June.</li>
    <li><strong>Try one question against the clock.</strong> Past papers and marking schemes are free on the <a href="https://www.examinations.ie/exammaterialarchive/" target="_blank" rel="noopener">SEC's exam archive ↗</a>. Let your child do one question in its suggested time, then check it against the marking scheme together.</li>
  </ul>
  <p class="small" style="color:var(--muted)">Based on the SEC's Junior Cycle 2025 Higher level Mathematics paper and marking scheme. The SEC says marking details can change from year to year, so check the latest scheme on examinations.ie. Ordinary level details are coming soon. Léim is not affiliated with the State Examinations Commission or the NCCA.</p>
</section>

</div></div>

'''
h=mkhead('Junior Cycle Maths Exam Centre: the paper, how it\'s marked, what to do if you go wrong | Léim',
 'How the Junior Cycle Higher Maths paper is marked: 270 marks, 13 compulsory questions, marks per question and part, partial credit scales, the one-mark slip rule, carrying errors forward, strategies and grades.')
h=h.replace('</style>\n</head>', '</style>\n'+extra_css,1)
assert extra_css in h
open('junior-cycle-maths-exam-centre.html','w').write(h+main+foot)

# ---------- hub ----------
hub='''<main id="main">

<section class="hero">
  <div class="wrap">
    <div class="hero-copy">
      <span class="pill">Junior Cycle</span>
      <h1>The <span class="hl">Exam Centre</span></h1>
      <p class="lede">Each paper explained: where the marks are, how it's marked, and the strategies that win marks. Pick a subject.</p>
    </div>
  </div>
</section>

<div class="block"><div class="wrap ec">
  <a class="card cardlink" href="junior-cycle-spanish-exam-centre.html"><h3 style="margin:0">Spanish</h3><p>The paper (360 marks: Listening, Reading, Writing), grade bands, strategies, a model answer and a guide for parents.</p><p style="color:var(--green);font-weight:700">Open the Spanish Exam Centre →</p></a>
  <a class="card cardlink" href="junior-cycle-maths-exam-centre.html"><h3 style="margin:0">Maths</h3><p>The Higher paper (270 marks, 13 questions), marks for every question and part, how partial credit works, and what to do if you go wrong.</p><p style="color:var(--green);font-weight:700">Open the Maths Exam Centre →</p></a>
  <div class="card" style="opacity:.75;margin:14px 0"><span class="pill" style="background:var(--mist);color:var(--muted)">Coming soon</span><h3>English and Irish</h3></div>
</div></div>

'''
h=mkhead('Junior Cycle Exam Centre: Spanish and Maths | Léim','Léim Exam Centre: the Junior Cycle Spanish and Maths papers explained, how they are marked, and strategies to win marks.')
open('exam-centre.html','w').write(h+hub+foot)
