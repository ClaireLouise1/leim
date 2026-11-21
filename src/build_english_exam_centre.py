# Builds the JC English Exam Centre and the two English CBA guides (job E5, Orders 19 and 25, 21 Nov 2026):
#   junior-cycle-english-exam-centre.html   the paper, timing by marks, command words, original model answers,
#                                           what came up (src/build_came_up.py), CBAs, grades, parents
#   junior-cycle-english-oral-cba.html      CBA 1 Oral Communication: a step-by-step guide for students (Order 19)
#   junior-cycle-english-texts-cba.html     CBA 2 The Collection of the Student's Texts: a guide for students (Order 25)
# and points exam-centre.html's English card, the English topics page chip and checklist rows 19 and 25 at them.
#
# FACTS (checked 21 Nov 2026):
#  - CBA rules + Features of Quality: NCCA "Junior Cycle English: Guidelines for the Classroom-Based Assessments
#    and Assessment Task" (curriculumonline.ie), paraphrased in our own words. Never copy its wording at length.
#  - 2026/27 arrangements (at least one CBA per subject; AT not examined): Circular 0062/2026, as on junior-cycle-cbas.html.
#  - Paper: one 2-hour paper, 180 marks, Higher and Ordinary, built around a theme (SEC papers 2022-2026, facts only).
#  - Grade bands since 2025: 85 / 70 / 55 / 40 / 20 (Department of Education, April 2025).
# Every text, question and model answer here is original (Léim). Never copy or adapt SEC questions or texts.
# Run: python3 src/build_english_exam_centre.py   (free_first.py runs at the end)
import re, os, sys, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
os.chdir(ROOT)
sys.path.insert(0, HERE)

src = open('junior-cycle-spanish-exam-centre.html', encoding='utf-8').read()
HEAD = src.split('<main id="main">')[0]
FOOT = '</main>' + src.split('</main>', 1)[1]


def mkhead(title, desc, url):
    h = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', HEAD)
    h = re.sub(r'<meta name="description" content=".*?">', f'<meta name="description" content="{desc}">', h)
    h = re.sub(r'(<meta property="og:title" content=")[^"]*', r'\g<1>' + title.replace('\\', ''), h)
    h = re.sub(r'(<meta property="og:description" content=")[^"]*', r'\g<1>' + desc, h)
    h = re.sub(r'https://leim\.ie/junior-cycle-spanish-exam-centre\.html', 'https://leim.ie/' + url, h)
    h = h.replace('<a href="exam-centre.html" aria-current="page">Exam Centre</a>', '<a href="exam-centre.html">Exam Centre</a>')
    h = h.replace('<a href="exam-centre.html">Exam Centre</a>', '<a href="exam-centre.html" aria-current="page">Exam Centre</a>')
    return h.replace('</style>\n</head>', '</style>\n' + CSS, 1)


CSS = '''<style>
.ec h3{margin-top:18px}
.warn{background:#FFF6D6;border:1px solid #F0D27A;border-radius:12px;padding:16px 18px;margin:16px 0}
.tip{background:var(--green-soft,#E6F2EC);border-radius:12px;padding:14px 16px;margin:14px 0}
.model-q{border:1px solid var(--line);border-radius:14px;padding:16px 18px;margin:14px 0;background:#fff}
.model-q h3{margin:2px 0 6px;font-size:19px}
.model-q details{border:0;padding:8px 0 0}
.model-q details summary{font-size:16px;color:var(--green);cursor:pointer;font-weight:700}
.mq-s{font-size:13px;font-weight:700;text-transform:uppercase;letter-spacing:.04em;color:var(--green);margin:0}
.txt{background:var(--mist);border-left:4px solid var(--green);border-radius:8px;padding:12px 16px;margin:10px 0;font-family:Georgia,serif;line-height:1.55}
.txt p{margin:0 0 8px}.txt p:last-child{margin:0}
.poem{white-space:pre-line}
.ans{border:1px dashed var(--line);border-radius:10px;padding:12px 14px;margin:10px 0;line-height:1.55}
.why li{margin:4px 0}
.ex-links{display:flex;flex-wrap:wrap;gap:6px;margin:6px 0 14px}
.ex-links a{background:var(--mist);border:1px solid var(--line);border-radius:999px;padding:5px 12px;font-size:15px;font-weight:600;text-decoration:none;color:var(--ink)}
.ex-links a:hover{border-color:var(--green);color:var(--green)}
.steps{counter-reset:s;list-style:none;padding:0}
.steps>li{counter-increment:s;position:relative;padding:0 0 14px 46px;margin:0}
.steps>li::before{content:counter(s);position:absolute;left:0;top:-2px;width:32px;height:32px;border-radius:50%;background:var(--sun,#F6CF5A);font-weight:800;display:grid;place-items:center}
.steps>li b{display:block;font-size:17px}
.lvls td:first-child{font-weight:700;white-space:nowrap}
.cue{display:grid;gap:8px;margin:10px 0}
.cue div{border:2px solid var(--line);border-radius:10px;padding:10px 12px;background:#fff}
.cue b{color:var(--green)}
.cue .t{float:right;font-size:13px;color:var(--muted);font-weight:700}
.fill td{height:34px}
.two{display:grid;gap:12px}@media(min-width:760px){.two{grid-template-columns:1fr 1fr}}
.cardgrid{display:grid;gap:12px;margin:12px 0}@media(min-width:760px){.cardgrid{grid-template-columns:1fr 1fr}}
.backbar{margin:0 0 6px;font-size:15px}.backbar a{color:var(--muted)}
</style>
</head>'''


def hero(pill, title_html, lede, toc, crumb=''):
    links = ''.join(f'<a href="#{a}">{b}</a>' for a, b in toc)
    cr = f'<p class="backbar">{crumb}</p>' if crumb else ''
    return f'''<section class="hero">
  <div class="wrap">
    <div class="hero-copy">
      {cr}<span class="pill">{pill}</span>
      <h1>{title_html}</h1>
      <p class="lede">{lede}</p>
      <nav class="toc" aria-label="On this page">{links}</nav>
    </div>
  </div>
</section>
'''


def model(kind, title, task, text, answer, why, text_cls='txt'):
    t = f'<div class="{text_cls}">{text}</div>' if text else ''
    w = ''.join(f'<li>{x}</li>' for x in why)
    return f'''<div class="model-q">
    <p class="mq-s">{kind}</p>
    <h3>{title}</h3>
    {t}
    <p><strong>{task}</strong></p>
    <details><summary>Show the model answer</summary>
      <div class="ans">{answer}</div>
      <p><strong>Why it works</strong></p>
      <ul class="why">{w}</ul>
    </details>
  </div>'''


def card(href, h, p, go):
    return f'<a class="card cardlink" href="{href}"><h3 style="margin:0">{h}</h3><p>{p}</p><p style="color:var(--green);font-weight:700">{go}</p></a>'


LEVELS_NOTE = ('<p class="small" style="color:var(--muted)">Your teacher reads the whole piece and decides which level fits best, '
               'starting at the lowest and moving up (an "on balance" judgement), so one weak moment doesn\'t sink it. '
               'The level words are the NCCA\'s; the descriptions are ours, in plain English.</p>')

THIS_YEAR = ('<div class="warn"><strong>This year\'s rule (exams in 2027 and 2028):</strong> every student does <strong>at least one</strong> '
             'English CBA, and the school decides whether it\'s one or both. Ask your teacher which one your class is doing, and when. '
             'The written Assessment Task is not examined, so the June exam is 100% of the English grade. '
             '<a href="junior-cycle-cbas.html">Dates and rules for this school year →</a></div>')

# ---------------------------------------------------------------- English games, grouped (from the subject hub)
from slim_game_pages import subjects  # noqa: E402  (reads SUBJECTS from build_subject_hub.py without building)
EN = subjects()['english']


def game_name(slug):
    h = open(slug + '.html', encoding='utf-8').read()
    m = re.search(r'<div class="gtop">.*?<h1>(.*?)</h1>', h, re.S)
    return m.group(1) if m else slug


def strand_links():
    out = ''
    for icon, name, slugs in EN['strands']:
        out += f'<p class="sl" style="margin:10px 0 0"><strong>{icon} {name}</strong></p><div class="ex-links">' + ''.join(
            f'<a href="english-practice-test.html?t={s}">{game_name(s)}</a>' for s in slugs) + '</div>'
    return out


def links(pairs):
    return '<div class="ex-links">' + ''.join(f'<a href="{h}">{t}</a>' for h, t in pairs) + '</div>'


# ================================================================ 1. ENGLISH EXAM CENTRE
TIMES = [(10, 7), (15, 10), (20, 13), (25, 17), (30, 20), (40, 27), (60, 40)]
for mk, mn in TIMES:
    assert abs(mk * 120 / 180 - mn) < 0.7, (mk, mn)   # 2 hours for 180 marks = 2/3 of a minute a mark
GRADES = [('Distinction', 85, 100), ('Higher Merit', 70, 84), ('Merit', 55, 69), ('Achieved', 40, 54), ('Partially Achieved', 20, 39), ('Not Graded', 0, 19)]
import math  # noqa: E402


def g_marks(lo, hi):
    a = math.ceil(lo * 180 / 100)
    b = math.ceil((hi + 1) * 180 / 100) - 1 if hi < 100 else 180
    return a, b


assert g_marks(85, 100) == (153, 180) and g_marks(70, 84) == (126, 152) and g_marks(0, 19) == (0, 35)
GRADE_ROWS = ''.join(f'<tr><td>{n}</td><td>{lo}–{hi}%</td><td class="num">{a}–{b}</td></tr>' for n, lo, hi in GRADES for a, b in [g_marks(lo, hi)])

POEM = '''Rain drums the roof like a hundred fingers,
the windows sweat, the radiators tick.
Someone's crisp packet crackles like a fire
and thirty voices climb, louder, quick,
till the door swings open. Silence. Click.'''
PROSE = ('<p>Gran never sat down. Even while the kettle was boiling she was wiping a counter that was already clean, '
         'or straightening the photographs on the dresser. When I came in soaked from the match, she tutted, threw a towel '
         'at my head and had a plate of toast in front of me before I\'d taken off my boots.</p>'
         '<p>"You\'ll catch your death," she said. But she was smiling.</p>')
# the model answers quote only these Léim texts; check every quote really is in its text
A1 = ('The poet fills the poem with sound to show how loud and restless a wet break is. In the first line the rain '
      '"<em>drums the roof like a hundred fingers</em>". This simile makes the rain sound constant and impatient, as if it is '
      'tapping to be let in, so the poem is noisy from the very start. The poet also uses onomatopoeia: the radiators '
      '"<em>tick</em>" and a crisp packet "<em>crackles like a fire</em>". These small, sharp sounds let me hear the room, and '
      'comparing a crisp packet to a fire is funny, because it shows how bored and jumpy everyone is. The noise builds when '
      '"<em>thirty voices climb, louder, quick</em>", and the short words and commas make the line itself speed up. Then the '
      'poet stops everything with two one-word sentences: "<em>Silence. Click.</em>" After so much noise, the sudden quiet tells '
      'us someone, probably a teacher, has come in, and the full stops make the reader stop too.')
A2 = ('<p><strong>1. Gran is hard-working, maybe restless.</strong> The writer says she "<em>never sat down</em>" and was wiping a '
      'counter "<em>that was already clean</em>". This shows she always has to be busy, even when there is nothing left to do.</p>'
      '<p><strong>2. Gran is caring, even though she hides it.</strong> She "<em>tutted</em>" and "<em>threw a towel</em>" at the '
      'narrator, which sounds cross, but she had toast ready "<em>before I\'d taken off my boots</em>". Her words are a telling-off, '
      'but "<em>she was smiling</em>", so we know she is really glad to look after her grandchild.</p>')
for q in re.findall(r'<em>(.*?)</em>', A1):
    assert q in POEM.replace('\n', ' '), q
for q in re.findall(r'<em>(.*?)</em>', A2):
    assert q in PROSE.replace("\\'", "'"), q
A3 = ('<p>Good morning, everyone. Quick question: hands up if you could cook a dinner for four people tonight, without a packet, '
      'a microwave or a video telling you what to do.</p>'
      '<p>Be honest.</p>'
      '<p>When I asked our class last week, six hands went up. Six, out of twenty-eight. In a few years most of us will be living '
      'away from home, in college, in a job or in a flat with people we barely know. And right now, most of us couldn\'t boil an '
      'egg without looking it up.</p>'
      '<p>So today I want to convince you of one thing: learning to cook isn\'t a hobby. It\'s a life skill, like swimming or '
      'reading a bus timetable, and every student in this school should learn it before they leave. I\'ve got three reasons, and '
      'the first one is money.</p>')

MODELS = ''.join([
    model('Unseen poem · Higher level style', 'Sound in a poem',
          'How does the poet use sound to bring the wet break to life? Support your answer with reference to the poem.',
          '<p><strong>"Wet Break"</strong> (written by Léim)</p><p class="poem">' + POEM + '</p>', A1,
          ['It answers the question in the first sentence: sound, and what it shows.',
           'Every point has a short quote (a few words, not whole lines) and then explains what the quote <em>does</em>.',
           'It names techniques (simile, onomatopoeia) but always says why they matter. Naming a technique on its own earns little.',
           'It follows the poem from start to finish, so the answer has a shape: noise builds, then stops.']),
    model('Unseen prose · Ordinary level style', 'What is a character like?',
          'What kind of person is Gran? Give two qualities and support each one with evidence from the extract.',
          PROSE, A2,
          ['Two clear qualities, one per paragraph, each in bold, so the examiner can see both straight away.',
           'Point, quote, explain: the quote is short and the explanation says what it shows about her.',
           'The second point notices a contrast (cross words, kind actions). Spotting that is what lifts an answer.']),
    model('Writing · Higher or Ordinary', 'The opening of a talk',
          'Write the text of a talk for your class on why every student should learn to cook before they leave school. (The opening is shown.)',
          '', A3,
          ['It\'s written as a <strong>talk</strong>: it greets the audience, asks them to do something and speaks to "you".',
           'The hook is a question the audience can answer, then a fact from the speaker\'s own class survey.',
           'The opinion is clear by the end of the opening, and "three reasons, the first one is money" tells the listener what\'s coming.',
           'Short sentences ("Be honest.") are used on purpose, for effect, the way a speaker would pause.']),
])

import build_came_up as _CU  # noqa: E402
CAMEUP = _CU.english_section()

EC = f'''<main id="main">
{hero('Junior Cycle English · Higher &amp; Ordinary level', 'The English <span class="hl">Exam Centre</span>',
      'How the June paper works, how long to spend on each question, what the questions are really asking, and model answers that show what a good answer looks like. Plus free guides to both CBAs.',
      [('paper', 'The paper'), ('timing', 'Timing'), ('words', 'Question words'), ('answers', 'Good answers'), ('models', 'Model answers'),
       ('texts', 'Studied texts'), ('practice', 'Practise'), ('came-up', 'What came up'), ('cba', 'CBAs'), ('grades', 'Grades'), ('parents', 'For parents')])}
<div class="block"><div class="wrap ec">

<section id="paper">
  <h2>The paper explained</h2>
  <p>Junior Cycle English is <strong>one written paper</strong> in June of 3rd year, at <strong>Higher</strong> or <strong>Ordinary</strong> level, set and marked by the State Examinations Commission.</p>
  <ul>
    <li><strong>2 hours</strong> and <strong>180 marks</strong></li>
    <li>The whole paper is built around <strong>one theme</strong> (for example "Perception" or "Journeys and Adventure"), and every text and question links to it</li>
    <li>It mixes <strong>unseen texts</strong> (a poem, a story extract, an article, a poster…), questions on <strong>texts you studied</strong> (your novel, poems, play or film) and <strong>writing tasks</strong> (a story, a speech, a letter, a review…)</li>
    <li>The <strong>sections and marks change every year</strong>, so you can't learn the layout off. What doesn't change is the skills it tests</li>
  </ul>
  <p>You write in an answer booklet, in the spaces under each question. The marks for each question are printed beside it: use them (see <a href="#timing">Timing</a>).</p>
</section>

<section id="timing">
  <h2>Timing: let the marks decide</h2>
  <p>2 hours for 180 marks works out at <strong>⅔ of a minute (40 seconds) a mark</strong>. So the marks beside a question tell you how long it deserves:</p>
  <div class="table-wrap"><table><thead><tr><th>Marks</th><th>About this long</th></tr></thead><tbody>
  {''.join(f'<tr><td>{mk} marks</td><td>{mn} minutes</td></tr>' for mk, mn in TIMES)}
  </tbody></table></div>
  <div class="tip"><strong>The trap:</strong> spending 25 minutes on a 10-mark question you love, then rushing a 40-mark writing task. When your time for a question is up, finish the sentence and move on. You can come back.</div>
  <p>Practise this with the <strong>Exam technique</strong> round in <a href="english-exam-mix.html">English Exam Mix</a>: it asks you "minutes for this question?" against the clock.</p>
</section>

<section id="words">
  <h2>What is the question really asking?</h2>
  <p>The first word or two of a question tell you what kind of answer gets the marks.</p>
  <div class="table-wrap"><table><thead><tr><th>If it says…</th><th>Do this</th></tr></thead><tbody>
    <tr><td>Identify, name, list, pick out, find</td><td>A short answer with the exact detail or words from the text. No long explaining.</td></tr>
    <tr><td>Describe</td><td>Say what it's like, with details from the text.</td></tr>
    <tr><td>Explain, how, why</td><td>Say why or how. Use "because", and back it up with the text.</td></tr>
    <tr><td>Compare, contrast</td><td>Say how the two are alike <em>and</em> how they're different. Mention both, every time.</td></tr>
    <tr><td>Do you agree, in your opinion, which do you prefer</td><td>Say clearly what you think, then give reasons from the text.</td></tr>
    <tr><td>Summarise, sum up</td><td>The main points only, short, in your own words.</td></tr>
  </tbody></table></div>
  <p>For a <strong>writing task</strong>, find three things before you write a word: the <strong>form</strong> (article, speech, letter, diary, review…), the <strong>reader</strong> (your principal, your class, a magazine's readers) and the <strong>purpose</strong> (to persuade, describe, inform, entertain). A brilliant story written when the task asked for a speech will lose marks.</p>
</section>

<section id="answers">
  <h2>What makes a good answer</h2>
  <p>This is our guide, based on how English answers are usually judged; it's not the official marking scheme. Good answers:</p>
  <ol>
    <li><strong>Answer the exact question</strong>, in the first sentence. Use its words.</li>
    <li><strong>Make a point, back it with a short quote, then explain it</strong> (point, quote, explain). A quote of 2–6 words, in quotation marks, is better than a copied-out paragraph.</li>
    <li><strong>Explain more than you retell.</strong> "This shows…", "This makes the reader feel…", "The writer does this because…" are where the marks are.</li>
    <li><strong>Match the marks.</strong> A 10-mark question usually wants two or three well-made points; a 30-mark one wants more, and more development.</li>
    <li><strong>Get the form right in writing tasks</strong>, and write in clear paragraphs with careful spelling and punctuation. Leave two minutes to read it back.</li>
  </ol>
  <p>The SEC publishes every marking scheme free, so you can see exactly how a past question was marked (see <a href="#parents">For parents</a>).</p>
</section>

<section id="models">
  <h2>Model answers</h2>
  <p>Three exam-style questions on texts written by Léim. Try each one first (write it or say it out loud), then open the model answer.</p>
  {MODELS}
</section>

<section id="texts">
  <h2>Studied texts: get ready</h2>
  <p>Questions on your studied novel, poems, play and film almost always ask you to talk about a <strong>key moment</strong> or a <strong>character</strong>, and to back it up. For each text, have ready:</p>
  <ul>
    <li><strong>2–3 key moments</strong> you can describe in a few lines: what happens, and why it matters</li>
    <li><strong>The main characters</strong>: what they're like, how they change, and a short quote or detail for each</li>
    <li><strong>The theme(s)</strong>, in a sentence each, so you can link any text to the paper's theme</li>
    <li>For a film: <strong>two or three techniques</strong> (a shot, the music, lighting) in one key scene</li>
    <li>Higher level: Shakespeare came up every year from 2023 to 2026 (see <a href="#came-up">What came up</a>)</li>
  </ul>
  {links([('character-clues.html', 'Character Clues'), ('plot-line.html', 'Plot Line'), ('technique-spotter.html', 'Technique Spotter'), ('mood-match.html', 'Mood Match'),
          ('stage-it.html', 'Stage It'), ('who-said-it.html', 'Who Said It? (Shakespeare)'), ('shot-spotter.html', 'Shot Spotter'), ('pqe-builder.html', 'PQE Builder'), ('compare-cards.html', 'Compare Cards')])}
</section>

<section id="practice">
  <h2>Practise</h2>
  <div class="cardgrid">
    {card('english-exam-mix.html', 'English Exam Mix', 'Every topic mixed like the real paper, plus an Exam technique round: timing by marks, question words, form and reader.', 'Play Exam Mix →')}
    {card('junior-cycle-english.html', 'All 29 English topics', 'A 60-second game for each topic, then a 10-question practice test, a printable sample test and the years it came up.', 'Choose a topic →')}
  </div>
  <h3>Practice test for each topic</h3>
  <p>10 questions, no timer, the answer explained after each one.</p>
  {strand_links()}
</section>

{CAMEUP}

<section id="cba">
  <h2>CBAs (Classroom-Based Assessments)</h2>
  <p>English CBAs are done in class, judged by your teacher, and reported on your Junior Cycle Profile of Achievement, separately from the June grade.</p>
  <div class="cardgrid">
    {card('junior-cycle-english-oral-cba.html', 'CBA 1: Oral Communication', 'A talk of about 3 minutes, alone or in a group. Choosing a topic, a 3-week plan, cue cards, how it\'s judged and the reflection note.', 'Read the guide →')}
    {card('junior-cycle-english-texts-cba.html', 'CBA 2: Collection of Texts', 'At least four pieces of your writing in four genres; you pick two. Genres, redrafting, how it\'s judged and the reflection note.', 'Read the guide →')}
  </div>
  {THIS_YEAR}
</section>

<section id="grades">
  <h2>Grades</h2>
  <p>Your marks out of 180 become a percentage, and the percentage gives the grade. These are the grade bands used since the 2025 exams, the same at both levels. The marks are rounded.</p>
  <div class="table-wrap"><table>
    <thead><tr><th>Grade</th><th>Percentage</th><th>About this many marks out of 180</th></tr></thead>
    <tbody>{GRADE_ROWS}</tbody>
  </table></div>
  <p>That means 18 marks is 10%: one 20-mark question left half-done can be the difference between two grades.</p>
</section>

<section id="parents">
  <h2>For parents</h2>
  <ul>
    <li><strong>The June exam gives the grade.</strong> It's one 2-hour paper, at Higher or Ordinary level, set and marked by the State Examinations Commission.</li>
    <li><strong>The CBAs are separate.</strong> They're judged by the class teacher and appear on the Junior Cycle Profile of Achievement. <a href="junior-cycle-cbas.html#english">CBAs explained, with example work</a>.</li>
    <li><strong>Talk about the texts.</strong> Asking "what was the best moment in your novel, and why?" over dinner is real revision: it's exactly what the paper asks.</li>
    <li><strong>Try one question against the clock.</strong> Past papers and marking schemes are free on the <a href="https://www.examinations.ie/exammaterialarchive/" target="_blank" rel="noopener">SEC's exam archive ↗</a> (tick the box to accept their terms, then choose Exam Papers, the year, Junior Cycle and English). Use the marks to set the time, then check the answer against the marking scheme together.</li>
  </ul>
  <p class="small" style="color:var(--muted)">Based on the SEC's Junior Cycle English papers 2022–2026 (facts only: length, marks, themes, which topics came up) and the NCCA's assessment guidelines. All texts, questions and model answers on this page are written by Léim. Léim is not affiliated with the State Examinations Commission or the NCCA.</p>
</section>

</div></div>
'''

# ================================================================ 2. ORAL COMMUNICATION CBA GUIDE (Order 19)
ORAL = f'''<main id="main">
{hero('Junior Cycle English · CBA 1', 'Oral Communication: <span class="hl">a step-by-step guide</span>',
      'Everything you need for the English oral CBA: what it is, picking a topic, a 3-week plan, how to shape a talk that holds the room, how it\'s judged, and the reflection note.',
      [('what', 'What it is'), ('topic', 'Pick a topic'), ('plan', '3-week plan'), ('shape', 'Shape it'), ('example', 'Example'),
       ('judged', 'How it\'s judged'), ('note', 'Reflection note'), ('mistakes', 'Mistakes'), ('practise', 'Practise')],
      '<a href="junior-cycle-english-exam-centre.html#cba">‹ English Exam Centre</a>')}
<div class="block"><div class="wrap ec">

<section id="what">
  <h2>What it is</h2>
  <ul>
    <li><strong>About 3 minutes</strong>, and that includes the time you spend engaging your audience (questions, a show of hands). Your teacher may ask you questions too.</li>
    <li><strong>Alone or in a group.</strong> In a group, everyone needs a real part, and you're judged on <em>your</em> part.</li>
    <li><strong>Usually near the end of 2nd year</strong>, with about <strong>3 school weeks</strong> to prepare it in class.</li>
    <li><strong>Any format that suits you:</strong> a <strong>presentation</strong> (notes are fine, and so is reading from a script you wrote), a <strong>performance</strong> (a scene, a sketch, a poem), an <strong>interview</strong> (being interviewed, or doing the interviewing) or a <strong>response to something</strong> (a picture, a song, a poem, a clip). A debate, a radio show, a sports commentary or a mock interview all count.</li>
    <li>Afterwards you write a short <strong>Student Reflection Note</strong> (see <a href="#note">below</a>).</li>
  </ul>
  {THIS_YEAR}
</section>

<section id="topic">
  <h2>Pick a topic</h2>
  <p>Choose something you actually care about. It doesn't have to come from English class. Then turn it into <strong>one key question</strong>: it keeps your research and your talk on track.</p>
  <div class="table-wrap"><table><thead><tr><th>Interest</th><th>Key question</th></tr></thead><tbody>
    <tr><td>Sport</td><td>Why do so many teenage girls give up sport, and what would keep them playing?</td></tr>
    <tr><td>Your family</td><td>How was my grandmother's school different from mine? (an interview)</td></tr>
    <tr><td>Games</td><td>Can a video game tell a story as well as a novel?</td></tr>
    <tr><td>Your town</td><td>What was our main street like 100 years ago?</td></tr>
    <tr><td>Music</td><td>Why do some songs get stuck in your head?</td></tr>
    <tr><td>School life</td><td>Should our school start at 9.30?</td></tr>
    <tr><td>A book or film</td><td>Is the villain in my favourite book actually the hero?</td></tr>
    <tr><td>A skill</td><td>Can anyone learn to draw? (with a live demonstration)</td></tr>
    <tr><td>A local business</td><td>How did the café on our square start? (interview the owner)</td></tr>
    <tr><td>Health</td><td>What really happens to your brain when you don't sleep?</td></tr>
  </tbody></table></div>
  <div class="tip"><strong>Check before you commit:</strong> can you find at least two sources for it, and can you get it ready in three weeks? A topic that needs you to travel or wait for replies is risky.</div>
</section>

<section id="plan">
  <h2>Your 3-week plan</h2>
  <ol class="steps">
    <li><b>Week 1: Research</b>Write your key question at the top of a page. Use <strong>more than one source</strong> so you can check one against another, and note where each fact came from. Original research is great: a class survey, an interview, an email to an expert. Note it all; you'll need it for your reflection note.</li>
    <li><b>Week 2: Shape it</b>Pick your <strong>best three points</strong> and drop the rest. Write a hook, an ending and the bridges between points (see <a href="#shape">Shape it</a>). Make <strong>cue cards</strong>: one card per part, a few words each, big writing. Plan how you'll involve the audience, and what you'd show (a picture, an object, one slide).</li>
    <li><b>Week 3: Practise</b>Say it out loud, timed, at least five times. <strong>Record yourself</strong> on a school device or practise on a friend or family member, and ask them one thing to fix. Practise answering two or three questions people might ask you.</li>
  </ol>
</section>

<section id="shape">
  <h2>Shape it: a talk that holds the room</h2>
  <div class="two">
    <div>
      <h3>Start strong (first 20 seconds)</h3>
      <ul>
        <li>A question to the audience: "Hands up if…"</li>
        <li>A surprising fact or number from your research</li>
        <li>A 3-line story: "Last summer, my grandad handed me a photo…"</li>
        <li>An object: hold it up and say nothing for two seconds</li>
      </ul>
    </div>
    <div>
      <h3>End strong (last 20 seconds)</h3>
      <ul>
        <li>Go back to your hook ("So, hands up now if…")</li>
        <li>Give the audience a challenge or one thing to remember</li>
        <li>Answer your key question in one sentence</li>
        <li>Then: "Thank you. Does anyone have a question?"</li>
      </ul>
    </div>
  </div>
  <h3>In the middle</h3>
  <ul>
    <li><strong>Three points, signposted:</strong> "First…", "The second thing surprised me…", "Finally…". Listeners can't flick back a page, so tell them where you are.</li>
    <li><strong>One example or story per point.</strong> People remember stories, not lists.</li>
    <li><strong>Talk to the audience, not your cards:</strong> "you", "we", eye contact, pauses after a big fact.</li>
    <li><strong>If you're persuading,</strong> answer the other side: "Some people say… but…".</li>
  </ul>
</section>

<section id="example">
  <h2>Example: cue cards for a 3-minute talk</h2>
  <p>Key question: <strong>"How was my grandmother's school different from mine?"</strong> A presentation built on an interview with her. (An example written by Léim. For a full example talk, see the <a href="junior-cycle-cbas.html#english">CBA guide for parents</a>.)</p>
  <div class="cue">
    <div><span class="t">0:00–0:25</span><b>1 Hook</b> Hold up her 1968 school photo. "Find the girl who looks like me." (pause) "That's my nan, aged 12."</div>
    <div><span class="t">0:25–1:00</span><b>2 Getting there</b> Walked 3 miles · no school bus · "wet socks all day" · Show of hands: who walks to school?</div>
    <div><span class="t">1:00–1:40</span><b>3 The classroom</b> 42 in one room · tables chanted out loud · ink pens, no calculators · I have a laptop and 26 classmates</div>
    <div><span class="t">1:40–2:20</span><b>4 What surprised me</b> She loved it! · teacher read stories aloud on Fridays · "we had less, but we listened more"</div>
    <div><span class="t">2:20–3:00</span><b>5 Answer + end</b> Different tools, same worries: friends, tests, being picked for teams · Back to photo: "Same face. Different world." · Questions?</div>
  </div>
  <p><strong>Why it works:</strong> it opens with an object and a question, every card is a few words (so she talks, not reads), it uses original research (the interview), it compares then and now point by point, and it ends by answering the key question and going back to the hook.</p>
</section>

<section id="judged">
  <h2>How it's judged</h2>
  <p>Your teacher looks at three things: <strong>how well you know and control your material</strong>, <strong>how clearly it's shaped for a purpose</strong>, and <strong>how well you engage your audience</strong>. The four levels:</p>
  <div class="table-wrap"><table class="lvls"><thead><tr><th>Level</th><th>What it looks like</th></tr></thead><tbody>
    <tr><td>Exceptional</td><td>Fluent and fully in control of the material; shaped imaginatively for a very clear purpose; the audience is hooked the whole way.</td></tr>
    <tr><td>Above Expectations</td><td>Clear and convincing, with very well-chosen material; fully shaped for its purpose; very effective with the audience.</td></tr>
    <tr><td>In Line with Expectations</td><td>Clear and convincing most of the time, showing you know your topic; shaped for a purpose; keeps the audience with you reasonably well.</td></tr>
    <tr><td>Yet to Meet Expectations</td><td>Shows some knowledge but isn't convincing; the purpose is often unclear; the audience is engaged only now and then.</td></tr>
  </tbody></table></div>
  {LEVELS_NOTE}
  <div class="tip"><strong>What this means for you:</strong> a talk with a clear purpose that keeps the audience involved scores better than a talk crammed with facts. Know your material well enough to look up from your cards.</div>
</section>

<section id="note">
  <h2>The Student Reflection Note</h2>
  <p>Everyone writes their own, even in a group, and hands it to the teacher. It has three parts:</p>
  <ol>
    <li><strong>A title</strong></li>
    <li><strong>Your role and your sources</strong>: what you did (and, in a group, which part was yours), and the materials or sources you used</li>
    <li><strong>A short reflection</strong>: one important thing you learned, and what you'd change or improve next time</li>
  </ol>
  <h3>Example (for the cue cards above)</h3>
  <div class="txt">
    <p><strong>Title:</strong> Then and now: my nan's school and mine</p>
    <p><strong>My role and sources:</strong> I did this on my own. I interviewed my nan for 40 minutes and recorded it (with her permission), used her school photo and copybook, and checked the facts about school transport in the 1960s on a local history website and in a book from the library.</p>
    <p><strong>What I learned:</strong> a real person's story holds an audience better than facts. Everyone leaned in when I held up the photo.</p>
    <p><strong>Next time:</strong> I'd practise in front of people sooner. My first try at home was over 4 minutes, so I cut a whole card about uniforms.</p>
  </div>
</section>

<section id="mistakes">
  <h2>Common mistakes</h2>
  <ul>
    <li><strong>Reading a wall of text</strong> with your head down. Reading your own script is allowed, but look up, slow down and talk to people.</li>
    <li><strong>Too much information.</strong> Three points told well beat ten facts rushed.</li>
    <li><strong>Forgetting it's for an audience:</strong> no hook, no questions, no "you".</li>
    <li><strong>Copying from a website.</strong> Use sources, but put it in your own words and say where it came from.</li>
    <li><strong>Not timing it.</strong> Most first tries run long. Time it, then cut.</li>
    <li><strong>A group where one person does everything.</strong> Each person is judged on their own part.</li>
  </ul>
</section>

<section id="practise">
  <h2>Practise the skills</h2>
  {links([('talk-tips.html', '🎤 Talk Tips'), ('english-practice-test.html?t=talk-tips', '📝 Talk Tips practice test'), ('persuasion-power.html', 'Persuasion Power'), ('register-switch.html', 'Register Switch'), ('fact-or-opinion.html', 'Fact or Opinion')])}
  <p><a href="junior-cycle-cbas.html#english">CBAs explained for parents, with a full example talk →</a></p>
  <p class="small" style="color:var(--muted)">Based on the NCCA's Junior Cycle English assessment guidelines, in our own words, and this year's arrangements (Circular 0062/2026). Your school sets the exact dates and may add its own instructions: follow your teacher's. Léim is not affiliated with the NCCA or the State Examinations Commission.</p>
</section>

</div></div>
'''

# ================================================================ 3. COLLECTION OF THE STUDENT'S TEXTS GUIDE (Order 25)
GENRES = [
    ('Opinion piece', 'an article or speech arguing a point', 'persuasion-power', 'Persuasion Power'),
    ('Descriptive piece', 'a place, a person or a moment, through the senses', 'show-dont-tell', "Show, Don't Tell"),
    ('Functional writing', 'a letter, email, report or set of instructions', 'format-fixer', 'Format Fixer'),
    ('Autobiography', 'a true moment from your own life', 'paragraph-builder', 'Paragraph Builder'),
    ('Humorous piece', 'a funny story, column or sketch', 'register-switch', 'Register Switch'),
    ('Media piece', 'a news report, advert, podcast script or blog', 'ad-breaker', 'Ad Breaker'),
    ('Critique', 'a review of a book, film, game or event', 'compare-cards', 'Compare Cards'),
    ('Narrative', 'a short story', 'story-spine', 'Story Spine'),
    ('Expressive piece', 'a poem, a diary entry, a letter you\'ll never send', 'technique-spotter', 'Technique Spotter'),
    ('Drama or film script', 'a scene with stage directions or shots', 'stage-it', 'Stage It'),
]
for _g in GENRES:
    assert os.path.exists(_g[2] + '.html'), _g
REVIEW = ('<p><strong>Review: "The Wizard of Oz", our school musical</strong></p>'
          '<p>Three nights, one tornado and 140 nervous students: our school\'s "Wizard of Oz" was ambitious, and for most of the night it worked.</p>'
          '<p>The star was the set. The art department turned the hall into Kansas with grey sheets and a wind machine, then pulled them down in seconds to reveal Oz in every colour they could find. The whole audience gasped, and so did I.</p>'
          '<p>Aoife Byrne, as Dorothy, carried the show. Her "Over the Rainbow" was quiet and simple, and the hall went completely still. The Tin Man got the biggest laughs, mostly because his costume squeaked whenever he moved.</p>'
          '<p>It wasn\'t perfect. The second half dragged, and the flying monkeys were hard to hear over the band. Twenty minutes shorter would have been ten times better.</p>'
          '<p>Still, it\'s the best thing our school has put on in years. Four stars out of five. Bring tissues for the ending, and earplugs for the monkeys.</p>')
TEXTS = f'''<main id="main">
{hero('Junior Cycle English · CBA 2', 'The Collection of Texts: <span class="hl">a guide for students</span>',
      'How to build your collection of writing over 2nd and 3rd year, the genres to choose from, how to redraft, how the two pieces you pick are judged, and the reflection note.',
      [('what', 'What it is'), ('genres', 'Genres'), ('build', 'Build it'), ('redraft', 'Redrafting'), ('choose', 'Pick your two'),
       ('judged', 'How it\'s judged'), ('note', 'Reflection note'), ('example', 'Example'), ('practise', 'Practise')],
      '<a href="junior-cycle-english-exam-centre.html#cba">‹ English Exam Centre</a>')}
<div class="block"><div class="wrap ec">

<section id="what">
  <h2>What it is</h2>
  <ul>
    <li>Over <strong>2nd and 3rd year</strong> you keep a collection of your own writing: <strong>at least four texts, in at least four different genres</strong>.</li>
    <li>Most pieces come from <strong>normal class work</strong>: write a report in the report-writing unit, and it can go in. A stronger piece can replace a weaker one later.</li>
    <li>Your <strong>drafts stay in the collection</strong> too. They show how the piece grew, but they aren't graded.</li>
    <li>A "text" can be handwritten, typed, digital or multimodal (words with images, audio or video).</li>
    <li>In <strong>3rd year you choose two texts</strong> to be assessed (your best, or with your teacher's advice), and write a <strong>Student Reflection Note</strong> for each.</li>
  </ul>
  {THIS_YEAR}
</section>

<section id="genres">
  <h2>The genres</h2>
  <p>These are the kinds of writing suggested for the collection. It isn't a closed list, and genres can overlap. Each one has a Léim game for the skills behind it.</p>
  <div class="table-wrap"><table><thead><tr><th>Genre</th><th>For example</th><th>Practise</th></tr></thead><tbody>
  {''.join(f'<tr><td><strong>{g}</strong></td><td>{d}</td><td><a href="{s}.html">{n}</a></td></tr>' for g, d, s, n in GENRES)}
  </tbody></table></div>
</section>

<section id="build">
  <h2>Build your collection</h2>
  <p>Keep a simple tracker at the front of your folder (copy this one). Aim to have four genres covered by the end of 2nd year, so 3rd year is about improving, not starting.</p>
  <div class="table-wrap"><table class="fill"><thead><tr><th>Genre</th><th>Title</th><th>Written in</th><th>Drafts</th><th>Ready to pick?</th></tr></thead><tbody>
    <tr><td>Descriptive piece</td><td><em>The Last Bus</em></td><td>2nd year, Oct</td><td>2</td><td>Nearly</td></tr>
    <tr><td></td><td></td><td></td><td></td><td></td></tr>
    <tr><td></td><td></td><td></td><td></td><td></td></tr>
    <tr><td></td><td></td><td></td><td></td><td></td></tr>
  </tbody></table></div>
  <div class="tip"><strong>Keep everything:</strong> plans, first drafts, your teacher's comments. You'll need them for your reflection notes, and they show how much you improved.</div>
</section>

<section id="redraft">
  <h2>Redrafting: where the improvement happens</h2>
  <ol class="steps">
    <li><b>Plan</b>Who's it for, and what should they think or feel at the end? Note your ideas, then put them in order.</li>
    <li><b>Draft</b>Get it all down. Don't fix as you go.</li>
    <li><b>Get feedback</b>From your teacher or a classmate: one thing that works, one thing to improve.</li>
    <li><b>Redraft</b>Change the big things first: the opening, the order, a weak ending, a dull paragraph. Swap "telling" for "showing".</li>
    <li><b>Edit and proofread</b>Then the small things: spelling, punctuation, repeated words, paragraphing. Read it out loud: you'll hear the mistakes.</li>
  </ol>
  <h3>A redraft in action</h3>
  <div class="two">
    <div class="txt"><p><strong>First draft</strong></p><p>The bus was cold and late. There was a man sleeping and two girls listening to music. It smelled bad. Then we got to the town.</p></div>
    <div class="txt"><p><strong>Redraft</strong></p><p>The 10.40 was always late, and always cold. A man in a high-vis jacket slept with his forehead on the glass, while two girls shared one set of earphones and laughed at something only they could hear.</p></div>
  </div>
  <p>The redraft swaps a list of facts for <strong>specific details</strong> the reader can see. That's the kind of change that moves a piece up a level. (The full piece is on the <a href="junior-cycle-cbas.html#english">CBA guide for parents</a>.)</p>
</section>

<section id="choose">
  <h2>Pick your two</h2>
  <ul>
    <li><strong>Pick your two strongest</strong>, and ask your teacher if you're unsure.</li>
    <li><strong>Both have to be strong.</strong> If your two pieces get different levels, the <strong>lower one</strong> is reported. One brilliant piece and one rushed piece gives you the rushed piece's level.</li>
    <li><strong>Show range.</strong> Two different genres (say, a story and an opinion piece) show more of what you can do than two of the same kind.</li>
    <li><strong>Pick pieces you can write about.</strong> You'll need to explain why you chose the genre and what you learned, so choose ones with a story behind them.</li>
  </ul>
</section>

<section id="judged">
  <h2>How it's judged</h2>
  <p>Each of your two texts is judged on <strong>how well you handle its genre</strong>, <strong>the quality of the writing and word choice</strong>, and <strong>how well it's shaped for its audience</strong>. The four levels:</p>
  <div class="table-wrap"><table class="lvls"><thead><tr><th>Level</th><th>What it looks like</th></tr></thead><tbody>
    <tr><td>Exceptional</td><td>Creative and in full command of the genre; highly skilled writing with original ideas and imaginative word choices that fit the purpose perfectly; fully shaped for its reader.</td></tr>
    <tr><td>Above Expectations</td><td>Very good control of the genre; consistently skilled writing with effective word choices for the purpose; clearly written with the reader in mind.</td></tr>
    <tr><td>In Line with Expectations</td><td>Good awareness of the genre; generally skilled writing with word choices that suit the purpose; the reader is kept in mind throughout.</td></tr>
    <tr><td>Yet to Meet Expectations</td><td>Little awareness of the genre; the writing isn't yet skilled and word choices may not suit the purpose; little sense of who it's for.</td></tr>
  </tbody></table></div>
  {LEVELS_NOTE}
</section>

<section id="note">
  <h2>The Student Reflection Note (one per text)</h2>
  <ol>
    <li><strong>The title and the genre</strong></li>
    <li><strong>Why you chose that genre</strong>, briefly</li>
    <li><strong>A reflection on the piece</strong>: what you were trying to do, what you learned writing it, and what you'd do differently next time</li>
  </ol>
  <p>Your drafts help here: look at what changed between them.</p>
</section>

<section id="example">
  <h2>Example: a critique, with its reflection note</h2>
  <p>Written by Léim, as an example of the length and style of a strong piece. (The school show in it is made up.)</p>
  <div class="txt">{REVIEW}</div>
  <h3>Its reflection note</h3>
  <div class="txt">
    <p><strong>Title and genre:</strong> Review: "The Wizard of Oz", our school musical. Critique (a review).</p>
    <p><strong>Why this genre:</strong> I'd only ever written stories, and I wanted to try writing an opinion that's fair: praising what worked and being honest about what didn't.</p>
    <p><strong>What I was trying to do:</strong> make readers who missed the show feel they'd seen it, and help them judge it for themselves.</p>
    <p><strong>What I learned:</strong> my first draft just retold the story of the musical. In my redraft I cut the plot to one line and gave every paragraph one judgement with an example (the set, Dorothy, the problems).</p>
    <p><strong>Next time:</strong> I'd interview someone in the cast, to add a quote and another point of view.</p>
  </div>
  <p><strong>Why the review works:</strong> it opens with a hook and an overall verdict, every paragraph makes one judgement backed by a specific detail, it's honest about the weak points, and the ending gives a clear rating and a joke that sounds like a real reviewer.</p>
</section>

<section id="practise">
  <h2>Practise the skills</h2>
  {links([('story-spine.html', 'Story Spine'), ('show-dont-tell.html', "Show, Don't Tell"), ('paragraph-builder.html', 'Paragraph Builder'), ('format-fixer.html', 'Format Fixer'),
          ('format-sort.html', 'Format Sort'), ('register-switch.html', 'Register Switch'), ('persuasion-power.html', 'Persuasion Power'), ('proofread-patrol.html', 'Proofread Patrol')])}
  <p><a href="junior-cycle-cbas.html#english">CBAs explained for parents, with a full example descriptive piece →</a></p>
  <p class="small" style="color:var(--muted)">Based on the NCCA's Junior Cycle English assessment guidelines, in our own words, and this year's arrangements (Circular 0062/2026). Your school sets the exact dates and may add its own instructions: follow your teacher's. Léim is not affiliated with the NCCA or the State Examinations Commission.</p>
</section>

</div></div>
'''

PAGES = [
    ('junior-cycle-english-exam-centre.html', EC,
     "Junior Cycle English Exam Centre: the paper, timing, question words and model answers | Léim",
     "How the Junior Cycle English paper works at Higher and Ordinary level: one 2-hour, 180-mark paper built around a theme, timing by marks, question words, original model answers, what came up 2022-2026, CBA guides and grades."),
    ('junior-cycle-english-oral-cba.html', ORAL,
     "Junior Cycle English Oral Communication CBA: a step-by-step guide for students | Léim",
     "The English oral CBA explained for students: about 3 minutes, alone or in a group, topic ideas, a 3-week plan, cue cards, how it's judged and an example reflection note."),
    ('junior-cycle-english-texts-cba.html', TEXTS,
     "Junior Cycle English CBA 2, the Collection of the Student's Texts: a guide for students | Léim",
     "The English Collection of Texts CBA explained: at least four texts in four genres, redrafting, choosing your two, how they're judged and an example reflection note."),
]
for fn, body, title, desc in PAGES:
    open(fn, 'w', encoding='utf-8').write(mkhead(title, desc, fn) + body + FOOT)
    print('built', fn)

# ---------------------------------------------------------------- links into the new pages
hub = open('exam-centre.html', encoding='utf-8').read()
old = re.search(r'<a class="card[^"]*" href="junior-cycle-english\.html#exam"[^>]*>.*?</a>', hub, re.S)
if old:
    new = ('<a class="card cardlink" href="junior-cycle-english-exam-centre.html"><h3 style="margin:0">English</h3>'
           '<p>The 2-hour, 180-mark paper built around a theme, timing by marks, question words, model answers, and guides to both CBAs.</p>'
           '<p style="color:var(--green);font-weight:700">Open the English Exam Centre →</p></a>')
    hub = hub[:old.start()] + new + hub[old.end():]
    open('exam-centre.html', 'w', encoding='utf-8').write(hub)
assert 'junior-cycle-english-exam-centre.html' in open('exam-centre.html', encoding='utf-8').read()

for p in ('sitemap.xml',):
    s = open(p, encoding='utf-8').read()
    for fn, *_ in PAGES:
        if fn not in s:
            s = s.replace('</urlset>', f'  <url><loc>https://leim.ie/{fn}</loc><lastmod>2026-11-21</lastmod></url>\n</urlset>')
    open(p, 'w', encoding='utf-8').write(s)
s = open('llms.txt', encoding='utf-8').read()
add = ''.join(f'- [{t.replace(" | Léim", "")}](https://leim.ie/{fn}): {d}\n' for fn, _, t, d in PAGES if fn not in s)
if add:
    anchor = re.search(r'- \[Junior Cycle Maths Exam Centre[^\n]*\n', s)
    s = s[:anchor.end()] + add + s[anchor.end():] if anchor else s + add
    open('llms.txt', 'w', encoding='utf-8').write(s)

if __name__ == '__main__':
    subprocess.run(['python3', os.path.join(HERE, 'free_first.py')], check=False, stdout=subprocess.DEVNULL)
