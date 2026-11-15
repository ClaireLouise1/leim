# Builds junior-cycle-maths-exam-centre.html and exam-centre.html.
# Data: SEC Junior Cycle 2026 Mathematics papers + marking schemes (Higher and Ordinary),
# read 15 Nov 2026 (marks, scale values and suggested times only; no questions or solutions).
import re
src=open('junior-cycle-spanish-exam-centre.html').read()
head=src.split('<main id="main">')[0]
foot='</main>'+src.split('</main>',1)[1]
def mkhead(title,desc):
    h=re.sub(r'<title>.*?</title>',f'<title>{title}</title>',head)
    h=re.sub(r'<meta name="description" content=".*?">',f'<meta name="description" content="{desc}">',h)
    h=h.replace('<a href="exam-centre.html" aria-current="page">Exam Centre</a>','<a href="exam-centre.html">Exam Centre</a>')
    h=h.replace('<a href="exam-centre.html">Exam Centre</a>','<a href="exam-centre.html" aria-current="page">Exam Centre</a>')
    assert 'href="exam-centre.html" aria-current' in h
    return h
extra_css='''<style>
.qt td,.qt th{white-space:normal}
.qt .num{text-align:center;white-space:nowrap}
.split{display:flex;flex-wrap:wrap;gap:4px}
.split span{background:var(--mist);border:1px solid var(--line);border-radius:6px;padding:1px 7px;font-size:14px;font-weight:600;white-space:nowrap}
.scale{display:flex;flex-wrap:wrap;gap:6px;margin:4px 0 10px}
.scale span{background:var(--mist);border:1px solid var(--line);border-radius:8px;padding:4px 10px;font-weight:700;font-size:15px}
.scale span.f{background:var(--green);color:#fff;border-color:var(--green)}
.sl{font-size:15px;color:var(--muted);margin:10px 0 0}
.warn{background:#FFF6D6;border:1px solid #F0D27A;border-radius:12px;padding:16px 18px;margin:16px 0}
.lvl{display:flex;gap:8px;margin:14px 0 6px}
.lvl button{font:inherit;font-weight:700;font-size:16px;padding:9px 18px;border-radius:999px;border:2px solid var(--green);background:#fff;color:var(--green);cursor:pointer}
.lvl button[aria-pressed="true"]{background:var(--green);color:#fff}
.js .lv[hidden]{display:none}
</style>
</head>'''
HL=[(1,15,'5C 10D',5),(2,25,'10D 5C 10C',10),(3,30,'15D 10D 5C',10),(4,20,'5B 5C 5D 5C',10),(5,15,'5C 10C',5),(6,10,'5C 5B',5),
    (7,30,'5B 10C 5D 10D',10),(8,25,'10D 5D 5B 5C',10),(9,20,'5C 5C 10D',10),(10,25,'10C 5C 10D',10),(11,20,'5C 5C 10D',10),(12,20,'10C 10C',10),(13,15,'15D',5)]
OL=[(1,15,'10C 5D',5),(2,20,'10D 10D',10),(3,20,'10D 5D 5D',10),(4,20,'5C 5C 5B 5C',10),(5,30,'10D 10C 10D',10),(6,30,'10D 10D 10D',10),
    (7,25,'5D 10D 5C 5B',10),(8,20,'5C 5C 5C 5C',10),(9,15,'15D',5),(10,20,'10D 10D',5),(11,20,'10C 10D',10),(12,15,'10D 5C',10),(13,20,'10C 10C',5)]
SC={'H':{'5B':'0,3,5','5C':'0,2,3,5','5D':'0,2,3,4,5','10C':'0,3,6,10','10D':'0,3,5,7,10','15D':'0,4,8,12,15'},
    'O':{'5B':'0,3,5','5C':'0,2,3,5','5D':'0,2,3,4,5','10C':'0,3,7,10','10D':'0,4,6,8,10','15D':'0,4,8,12,15'}}
for L in (HL,OL):
    assert sum(q[1] for q in L)==270 and sum(q[3] for q in L)==110 and len(L)==13
    for n,t,p,m in L: assert sum(int(x[:-1]) for x in p.split())==t,(n,p,t)
def table(L):
    rows=''.join(f'<tr><td><strong>Q{n}</strong></td><td class="num">{t}</td><td><div class="split">{"".join(f"<span>{x}</span>" for x in p.split())}</div></td><td class="num">{m} min</td></tr>' for n,t,p,m in L)
    return f'''<div class="table-wrap"><table class="qt">
    <thead><tr><th>Q</th><th>Marks</th><th>How the marks split</th><th>Time*</th></tr></thead>
    <tbody>{rows}
      <tr><td><strong>Total</strong></td><td class="num"><strong>270</strong></td><td></td><td class="num"><strong>110 min</strong></td></tr>
    </tbody></table></div>'''
def chips(v): v=v.split(','); return '<div class="scale">'+''.join(f'<span{" class=\"f\"" if i==len(v)-1 else ""}>{x}</span>' for i,x in enumerate(v))+'</div>'
def scales(k):
    order=['5B','5C','5D','10C','10D','15D']
    return ''.join(f'<p class="sl"><strong>{s}</strong> ({s[-1]} scale, {s[:-1]} marks)</p>{chips(SC[k][s])}' for s in order)
used={'H':set(' '.join(q[2] for q in HL).split()),'O':set(' '.join(q[2] for q in OL).split())}
assert used['H']<=set(SC['H']) and used['O']<=set(SC['O'])

main=f'''<main id="main">

<section class="hero">
  <div class="wrap">
    <div class="hero-copy">
      <span class="pill">Junior Cycle Maths · Higher &amp; Ordinary level</span>
      <h1>The Maths <span class="hl">Exam Centre</span></h1>
      <p class="lede">How the June paper works, how every mark is given, and what to do when a question goes wrong. Based on the State Examinations Commission's published 2026 papers and marking schemes.</p>
      <nav class="toc" aria-label="On this page">
        <a href="#paper">The paper</a><a href="#marks">Marks per question</a><a href="#marking">How it's marked</a><a href="#wrong">If you go wrong</a><a href="#strategies">Strategies</a><a href="#grades">Grades</a><a href="#parents">For parents</a>
      </nav>
    </div>
  </div>
</section>

<div class="block"><div class="wrap ec">

<section id="paper">
  <h2>The paper explained</h2>
  <p>Junior Cycle Maths is <strong>one written paper</strong> in June of 3rd year, at <strong>Higher</strong> or <strong>Ordinary</strong> level. In 2026 both levels looked the same from the outside:</p>
  <ul>
    <li><strong>2 hours</strong> and <strong>270 marks</strong></li>
    <li><strong>13 questions</strong>, and <strong>every question must be answered</strong>: there is no choice, so every topic on the course matters</li>
    <li>You write your answers in the exam booklet, and you get a <strong>Formulae and Tables booklet</strong> in the exam</li>
  </ul>
  <p>The difference is in the questions: Higher level asks harder questions and covers some extra topics.</p>
</section>

<section id="marks">
  <h2>Marks per question</h2>
  <p>Pick your level. Each grey box is one part (or a few short parts marked together), with its marks and its marking scale (B, C or D, explained <a href="#marking">below</a>).</p>
  <div class="lvl" role="group" aria-label="Choose a level"><button type="button" data-lv="H" aria-pressed="true">Higher</button><button type="button" data-lv="O" aria-pressed="false">Ordinary</button></div>
  <div class="lv" data-lv="H">
    <h3>Higher level, 2026</h3>
    {table(HL)}
    <p class="big"><strong>The big message:</strong> the questions are not equal. Questions 3 and 7 were worth 30 marks each, three times as much as Question 6.</p>
  </div>
  <div class="lv" data-lv="O">
    <h3>Ordinary level, 2026</h3>
    {table(OL)}
    <p class="big"><strong>The big message:</strong> the questions are not equal. Questions 5 and 6 were worth 30 marks each, twice as much as Questions 1, 9 and 12.</p>
  </div>
  <p class="small" style="color:var(--muted)">*Time = the suggested maximum time printed on the paper for each question. They add up to 110 minutes, which leaves about 10 minutes to check. The split changes every year (2025 was different), so use this to understand how the paper works, not to predict next June's paper.</p>
</section>

<section id="marking">
  <h2>How it's marked</h2>
  <p>Maths is <strong>not</strong> marked one mark per step. The examiner reads your answer to a part and decides which level it reaches. Each level is worth a fixed number of marks.</p>
  <h3>The levels</h3>
  <ul>
    <li><strong>No credit:</strong> nothing of real value.</li>
    <li><strong>Low partial credit:</strong> some useful work, for example a correct first step or the right formula.</li>
    <li><strong>Mid partial credit</strong> (D scales only): about half right.</li>
    <li><strong>High partial credit:</strong> almost there.</li>
    <li><strong>Full credit:</strong> correct.</li>
  </ul>
  <p>A <strong>B scale</strong> has 3 levels (no credit, partial, full), a <strong>C scale</strong> has 4 and a <strong>D scale</strong> has 5.</p>
  <h3>What each scale was worth in 2026</h3>
  <div class="lv" data-lv="H"><p><strong>Higher level</strong></p>{scales('H')}</div>
  <div class="lv" data-lv="O"><p><strong>Ordinary level</strong></p>{scales('O')}</div>
  <p>The green box is full marks. The examiner can only give a mark on the scale, or one mark below full (see below), so there are no half marks.</p>
  <div class="warn"><strong>One line of work is worth marks.</strong> Even low partial credit is 2 marks on a 5-mark part, 3 or 4 marks on a 10-mark part and 4 marks on a 15-mark part. A blank is always 0.</div>
</section>

<section id="wrong">
  <h2>If you go wrong</h2>
  <h3>A small slip costs 1 mark at most</h3>
  <p>The marking scheme calls these <strong>slips</strong>:</p>
  <ul>
    <li>rounding wrongly, or not rounding when asked</li>
    <li>leaving out the units (cm, €, m²…), when the question says units are needed</li>
    <li>a small arithmetic slip that doesn't make the question easier</li>
    <li>misreading a number, as long as it doesn't make the question easier</li>
  </ul>
  <p>If everything else is right, one slip gives you <strong>full marks minus 1</strong> (for example 9 out of 10). If your answer wasn't getting full marks anyway, one slip costs nothing. But <strong>two or more slips</strong> in the same part count as an error.</p>
  <h3>An error drops you one level</h3>
  <p>A real mistake (an <strong>error</strong>) usually drops your answer one level on the scale, and two errors drop it two levels. But if you've shown enough good work, you still keep at least low partial credit. Some parts are marked in <strong>steps</strong> instead: then a mistake in one step doesn't stop you getting credit for the other steps.</p>
  <h3>A wrong answer in part (a) doesn't ruin part (b)</h3>
  <p>If you got (a) wrong, <strong>use your wrong answer in (b) and carry on</strong>. Examiners accept work carried forward from an earlier part, as long as your mistake hasn't made the later part easier. You can still get full marks for (b).</p>
  <h3>Crossed it out? Had two goes?</h3>
  <ul>
    <li><strong>For a worked answer</strong> (a calculation or a method), the examiner marks <strong>every attempt, even crossed-out ones</strong>, and gives you the best one. So don't scribble out work: put a single line through it and keep going.</li>
    <li><strong>For a "choose" answer</strong> (pick an option, tick a box, name one thing), if you leave two different answers, you get the mark for the <strong>worse</strong> one. Cross out the one you don't want.</li>
    <li><strong>Extra work after the answer</strong> generally isn't penalised, except when you're asked to explain or justify in words: then your whole answer counts, so don't add things that contradict it.</li>
  </ul>
  <h3>Always show your work</h3>
  <p>A right answer with no work can still lose marks: in recent marking schemes, an answer without enough supporting work usually gets only the lowest mark above zero, unless that part says otherwise. Show every step.</p>
  <h3>Ran out of space?</h3>
  <p>Write all your answers in the exam booklet, inside the answer areas. There's extra space at the back: if you use it, <strong>label it with the question number and part</strong> (for example "Q7(b)"). Work written outside the answer areas might not be seen.</p>
</section>

<section id="strategies">
  <h2>Exam strategies</h2>
  <ol>
    <li><strong>Check the time on each question.</strong> Each question shows a suggested maximum time. If you go over, move on and come back at the end.</li>
    <li><strong>Collect the easy marks first.</strong> Every question is compulsory, but you can do them in any order. Do your strong ones first to build up marks and confidence.</li>
    <li><strong>Read the last line twice.</strong> "Give your answer correct to 2 decimal places", "in cm²", "as a fraction": these are the instructions that cost a mark when missed.</li>
    <li><strong>Round only at the end.</strong> Keep full calculator values until the final answer.</li>
    <li><strong>Check your calculator is in degrees</strong> before any trigonometry question.</li>
    <li><strong>Use the Formulae and Tables booklet.</strong> You get one in the exam (you can't bring your own), so practise with it all year.</li>
    <li><strong>Never leave a part blank.</strong> Write the formula, put in the numbers, draw a labelled diagram: one line can be worth marks.</li>
  </ol>
  <a class="card cardlink" href="junior-cycle-maths.html#games"><h3 style="margin:0">Practise topic by topic: free Maths games</h3><p>60-second games for each topic, each with the rules, a free printable sheet and an Exam corner of exam-style questions with worked answers.</p><p style="color:var(--green);font-weight:700">Play the Maths games →</p></a>
</section>

<section id="grades">
  <h2>Grades</h2>
  <p>Your marks out of 270 become a percentage, and the percentage gives the grade. These are the new grade bands used since the 2025 exams, the same at both levels. The marks below are rounded.</p>
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
  <p>That means 27 marks is about 10%. One unanswered 15-mark part can be the difference between two grades.</p>
</section>

<section id="parents">
  <h2>For parents</h2>
  <ul>
    <li><strong>The June exam gives the grade.</strong> It's set and marked by the State Examinations Commission, at Higher or Ordinary level.</li>
    <li><strong>The CBA is separate.</strong> Students do at least one Classroom-Based Assessment in class (most schools do one) (a Mathematical or a Statistical Investigation). It appears on the Junior Cycle Profile of Achievement, not in the exam grade. <a href="junior-cycle-cbas.html#maths">See CBAs explained, with example investigations</a>.</li>
    <li><strong>Ask to see the working.</strong> When your child shows you homework, look for the steps, not just the answer. That habit is worth marks in June.</li>
    <li><strong>Try one question against the clock.</strong> Past papers and marking schemes are free on the <a href="https://www.examinations.ie/exammaterialarchive/" target="_blank" rel="noopener">SEC's exam archive ↗</a>. Let your child do one question in its suggested time, then check it against the marking scheme together.</li>
  </ul>
  <p class="small" style="color:var(--muted)">Based on the SEC's Junior Cycle 2026 Higher and Ordinary level Mathematics papers and marking schemes. The SEC says marking details can change from year to year, so check the latest scheme on examinations.ie. Léim is not affiliated with the State Examinations Commission or the NCCA.</p>
</section>

</div></div>

<script>
(function(){{document.documentElement.classList.add('js');
var bs=document.querySelectorAll('.lvl button'),ps=document.querySelectorAll('.lv');
function set(l){{bs.forEach(function(b){{b.setAttribute('aria-pressed',b.dataset.lv===l?'true':'false')}});ps.forEach(function(p){{p.hidden=p.dataset.lv!==l}});try{{localStorage.setItem('leim-maths-level',l)}}catch(e){{}}}}
bs.forEach(function(b){{b.addEventListener('click',function(){{set(b.dataset.lv)}})}});
var s='H';try{{s=localStorage.getItem('leim-maths-level')||'H'}}catch(e){{}}set(s);}})();
</script>
'''
h=mkhead("Junior Cycle Maths Exam Centre: Higher and Ordinary papers, how they're marked, what to do if you go wrong | Léim",
 "How the Junior Cycle Maths paper is marked at Higher and Ordinary level: 270 marks, 13 compulsory questions, marks per question, partial credit scales, slips and errors, crossed-out work, strategies and the new grade bands.")
h=h.replace('</style>\n</head>', '</style>\n'+extra_css,1)
assert extra_css in h
open('junior-cycle-maths-exam-centre.html','w').write(h+main+foot)
hub=open('exam-centre.html').read()
hub=hub.replace('<p>The Higher paper (270 marks, 13 questions), marks for every question and part, how partial credit works, and what to do if you go wrong.</p>','<p>Higher and Ordinary papers (270 marks, 13 questions), marks for every question, how partial credit works, and what to do if you go wrong.</p>')
open('exam-centre.html','w').write(hub)
