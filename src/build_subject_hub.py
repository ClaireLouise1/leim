"""Builds the student-facing subject pages in the new home-page layout (21 Nov 2026,
she chose it): Exam -> Subject -> Topics (cards grouped by strand) -> game.
Text-light on purpose. The long version of each page (exam info, teacher packs,
FAQ) lives in junior-cycle-<subject>-guide.html (built by build_<subject>_page.py).

Run: python3 src/build_subject_hub.py   (then free_first.py runs at the end)
To add a new topic/game: add its slug to the right strand in SUBJECTS below
(and a short name in SHORT if the topic name is long), then re-run.
Game names come from the guide page's cards; the 📅 count comes from each
game page's "Came up in" line (src/build_came_up.py)."""
import re, os, subprocess, html
ROOT = os.path.join(os.path.dirname(__file__), '..')
os.chdir(ROOT)

SUBJECTS = {
 'maths': dict(
   title='Maths', guide='junior-cycle-maths-guide.html',
   chips=[('y','🎯 Exam Centre','junior-cycle-maths-exam-centre.html'),('','✅ Checklist','junior-cycle-maths-checklist.html'),('','🔀 Exam Mix','exam-mix.html'),('','📖 Course guide','junior-cycle-maths-guide.html')],
   mix=('exam-mix.html','Exam Mix','Every topic, mixed like the real paper'),
   tests=['number','algebra','geometry','stats'],
   strands=[
    ('🔢','Number',['integer-rush','prime-smash','fraction-match','round-it','venn-sorter','percent-pop','share-it-out','power-up','surd-simplify','clock-dash','shop-keeper','payslip-puzzle','road-trip']),
    ('🧮','Algebra &amp; Functions',['like-term-sweep','bracket-blaster','factor-match','balance-it','two-line-crossing','root-rush','number-line-shade','rearrange-race','pattern-builder','growth-spotter','graph-match']),
    ('📐','Geometry &amp; Trigonometry',['angle-chase','construction-steps','proof-builder','mirror-move','floor-planner','pack-it','ladder-lab','line-lab','clinometer-challenge']),
    ('📊','Statistics &amp; Probability',['data-detective','average-ace','spin-and-predict','coin-dice-lab']),
   ]),
  'english': dict(
   title='English', guide='junior-cycle-english-guide.html',
   chips=[('y','🎯 Exam Centre','exam-centre.html'),('','✅ Checklist','junior-cycle-english-checklist.html'),('','🔀 Exam Mix','english-exam-mix.html'),('','📖 Course guide','junior-cycle-english-guide.html')],
   mix=('english-exam-mix.html','English Exam Mix','Every topic, mixed like the real paper'),
   tests='english',   # bundle section per game comes from SECTIONS in build_english_exam_mix.py
   strands=[
    ('✏️','Grammar, spelling &amp; punctuation',['word-sort','sentence-surgeon','comma-catch','speech-marks-sprint','spell-strike','word-ladder','tense-trap','proofread-patrol']),
    ('📚','Novel, poetry, drama &amp; film',['character-clues','plot-line','twist-detector','technique-spotter','mood-match','stage-it','who-said-it','shot-spotter','ad-breaker']),
    ('📝','Writing',['paragraph-builder','show-dont-tell','story-spine','format-fixer','format-sort','register-switch','persuasion-power']),
    ('🎯','Reading, speaking &amp; exam skills',['clue-hunt','fact-or-opinion','pqe-builder','compare-cards','talk-tips']),
   ]),
  'spanish': dict(
   title='Spanish', guide='junior-cycle-spanish-guide.html',
   chips=[('y','🎯 Exam Centre','junior-cycle-spanish-exam-centre.html'),('','✅ Checklist','junior-cycle-spanish-checklist.html'),('','🗣️ Speaking','junior-cycle-spanish-speaking.html'),('','📖 Course guide','junior-cycle-spanish-guide.html')],
   mix=None,
   strands=[
    ('🙋','Me &amp; my world',['meet-and-greet','sound-match','number-rush','family-tree-detective','agreement-snap','opinion-dash','hobby-bingo','timetable-scramble','room-raider','que-te-duele','dream-job-match']),
    ('✈️','Out &amp; about',['cafe-order-rush','price-check','map-dash','postcard-builder','forecast-match','fiesta-quiz']),
    ('🧱','Grammar',['verb-sprint','time-machine','plan-it','routine-order-up','verb-swipe','gender-sort','question-quick-fire','connector-chain']),
    ('🎯','Exam skills',['gist-or-detail','fix-the-email']),
   ]),
}
SHORT = {'Integers &amp; order of operations':'Integers &amp; BIMDAS','Factors, multiples &amp; primes (HCF, LCM)':'Factors, multiples &amp; primes','Decimals, rounding &amp; estimation':'Decimals &amp; rounding','Units of measure, time &amp; timetables':'Units, time &amp; timetables','Money 1':'Bills, VAT &amp; profit','Money 2':'Tax, pay &amp; interest','Speed, distance, time &amp; currency':'Speed &amp; currency','Algebra 1':'Expressions','Algebra 2':'Expanding brackets','Algebraic fractions, long division &amp; changing the subject':'Changing the subject','Patterns 1':'Linear patterns','Patterns 2':'Quadratic patterns','Geometry 1':'Angles &amp; triangles','Geometry 2':'Theorems &amp; proofs','Transformations &amp; symmetry':'Transformations','Area, perimeter &amp; scale drawings':'Area &amp; perimeter','Volume &amp; surface area (3D solids &amp; nets)':'Volume &amp; surface area','Pythagoras &amp; right-angled triangles':'Pythagoras','Coordinate geometry of the line':'The line','Statistics 1':'Collecting data','Statistics 2':'Graphs &amp; averages','Probability 1':'Chance','Probability 2':'Relative frequency',
 'Punctuation 1':'Capitals, commas &amp; full stops','Punctuation 2':'Speech marks, colons &amp; semicolons','The novel 1':'The novel: characters','The novel 2':'The novel: plot','Poetry 1':'Poetry: imagery &amp; sound','Poetry 2':'Poetry: theme &amp; mood','Grammar 2':'Tenses &amp; agreement','Media 1':'Advertising','Drama 1':'Drama','Shakespeare (Higher Level only)':'Shakespeare (Higher Level)',
 'Numbers, age, birthdays, dates and the time':'Numbers, dates &amp; time','Greetings, introductions and classroom Spanish':'Greetings &amp; introductions','Exam skills for Listening and Reading':'Listening &amp; reading skills','Jobs, future plans and me gustaría':'Jobs &amp; future plans','Spain and the Spanish-speaking world':'Spain &amp; Latin America','Food, drink and eating out':'Food &amp; eating out','Free time, hobbies and sport':'Hobbies &amp; sport','Where I live, house and town':'House &amp; town','The near future and making plans':'The near future','Daily routine and reflexive verbs':'Daily routine','Shopping, clothes and prices':'Shopping &amp; clothes','Messages, emails and forms':'Emails &amp; messages','Linking and extending sentences':'Linking words','Alphabet, sounds and spelling':'Sounds &amp; spelling','Directions and getting around':'Directions','The past tense (preterite)':'The past tense','Likes, dislikes and opinions':'Likes &amp; opinions','Ser, estar and hay':'Ser, estar &amp; hay','Nouns and articles':'Nouns &amp; articles','Me and my family':'Me &amp; my family','Weather and seasons':'Weather &amp; seasons','Health and the body':'Health &amp; the body','Numbers, age, birthdays, dates and the time, with a Listening mode that reads the Spanish aloud.':'Numbers, dates &amp; time','Holidays and travel':'Holidays &amp; travel','Spelling &amp; commonly confused words':'Spelling','Vocabulary &amp; dictionary skills':'Vocabulary','Paragraphs &amp; topic sentences':'Paragraphs','Persuasive writing &amp; speeches':'Persuasive writing'}

STYLES = open(os.path.join(os.path.dirname(__file__), 'subject_hub.css'), encoding='utf-8').read()

def build(key, cfg):
    idx = open('index.html', encoding='utf-8').read()
    guide = open(cfg['guide'], encoding='utf-8').read()
    cards = {}
    for s_,g,tp,d in re.findall(r'<a class="card" href="([a-z0-9-]+)\.html"[^>]*>(?:<span class="pill">[^<]*</span>)?<h3>(.*?)</h3>(?:<p style="[^"]*">([^<]*)</p>)?<p>(.*?)</p>', guide):
        cards[s_] = (g, (tp + ':') if tp else d)
    head = idx.split('<style>')[0]
    url = f'https://leim.ie/junior-cycle-{key}.html'
    t = f'Junior Cycle {cfg["title"]} revision games | Léim'
    head = re.sub(r'<title>.*?</title>', f'<title>{t}</title>', head)
    head = head.replace('href="https://leim.ie/"', f'href="{url}"').replace('content="https://leim.ie/"', f'content="{url}"')
    head = re.sub(r'(<meta property="og:title" content=")[^"]*', r'\g<1>'+t, head)
    hdr = idx.split('<body>')[1].split('<main id="main">')[0]
    foot = '</main>' + idx.split('</main>')[1]
    hdr, foot = (x.replace('href="#join"', 'href="index.html#join"') for x in (hdr, foot))   # the sign-up form is on the home page
    out, n = [], 0
    for i,(icon,name,slugs) in enumerate(cfg['strands']):
        rows = []
        for s in slugs:
            n += 1
            g, d = cards[s]
            topic = d.split(':')[0]; topic = topic[0].upper()+topic[1:]
            topic = SHORT.get(topic, topic)
            m = re.search(r'class="came"[^>]*><b>Came up in:</b>(.*?)</p>', open(s+'.html', encoding='utf-8').read(), re.S)
            y = len(set(re.findall(r'\b(20\d\d) \(', m.group(1)))) if m else 0
            came = f' · 📅 {y}/5' if y else ''
            if cfg.get('tests'):
                bundle = EN_SECTION[s] if cfg['tests'] == 'english' else cfg['tests'][i]
                # past-paper refs for the test page's "In the real exam" box: [[year, "H5, O3"], ...]
                came_l = re.findall(r'\b(20\d\d) \(([^)]*)\)', m.group(1)) if m else []
                TESTS.setdefault(key, {})[s] = {'topic': html.unescape(topic), 'game': html.unescape(g), 'bundle': bundle, 'came': [list(x) for x in came_l]}
                rows.append(f'<div class="topic hasT"><a class="tl" href="{s}.html"><span class="n">{n}</span><div><div class="t">{topic}</div><div class="m"><span class="g">🎮 {g}</span>{came}</div></div></a><a class="tb" href="{PT_PAGE[key]}?t={s}" data-pt="{s}" aria-label="Practice test: {topic}">📝<span>Test</span></a></div>')
            else:
                rows.append(f'<a class="topic" href="{s}.html"><span class="n">{n}</span><div><div class="t">{topic}</div><div class="m"><span class="g">🎮 {g}</span>{came}</div></div><span class="go">›</span></a>')
        sid = ' id="games"' if i == 0 else ''
        out.append(f'<section class="strand"{sid}><h2>{icon} {name} <small>{len(slugs)} topics</small></h2><div class="tlist">{"".join(rows)}</div></section>')
    chips = ''.join(f'<a class="chip {c}" href="{h}">{l}</a>' for c,l,h in cfg['chips'])
    mixhtml = ''
    if cfg['mix']:
        mh, mt, ms = cfg['mix']
        mixhtml = f'<a class="mix" href="{mh}"><span class="n">🔀</span><div><b>{mt}</b><div style="opacity:.8;font-size:.9rem">{ms}</div></div></a>'
    anycame = '📅' in ''.join(out)
    explain = ' · 📅 = how many of the last 5 exams it came up in' if anycame else ''
    main = f'''<main id="main">
<div class="home">
<p class="crumbs"><a href="index.html">Home</a> › <a href="index.html#jc">Junior Cycle</a> › {cfg["title"]}</p>
<h1 class="home-title">Junior Cycle <span class="acc">{cfg["title"]}</span></h1>
<p style="margin:0 0 10px;font-weight:600">{n} topics · tap one to play{explain}</p>
<div class="btnrow">{chips}</div>
{''.join(out)}
{mixhtml}
<p style="margin-top:20px;font-size:.9rem;color:var(--muted)">{'📝 Tap <b>Test</b> on any topic for a 10-question practice test.' if cfg.get('tests') else '📝 Practice tests for each topic: coming soon.'} Parents and teachers: see the <a href="{cfg["guide"]}">course guide</a>.</p>
</div>
'''
    if cfg.get('tests'):
        foot = foot.replace('</body>', '<script>try{document.querySelectorAll("[data-pt]").forEach(function(a){var b=+localStorage.getItem("leim-pt-"+a.getAttribute("data-pt"));if(b){a.querySelector("span").textContent=b+"/10";a.classList.add("done");}});}catch(e){}</script>\n</body>')
    open(f'junior-cycle-{key}.html','w',encoding='utf-8').write(head+'<style>'+STYLES+'</style>\n</head>\n<body>'+hdr+main+foot)
    print('built', key, n, 'topics')

TESTS = {}
PT_PAGE = {'maths': 'practice-test.html', 'english': 'english-practice-test.html'}
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_english_exam_mix import SECTIONS as _SEC
EN_SECTION = {g: sec for sec, gs in _SEC.items() for g in gs}
for k,c in SUBJECTS.items(): build(k,c)
import importlib.util as _u
_spec=_u.spec_from_file_location('bpt', os.path.join(os.path.dirname(os.path.abspath(__file__)),'build_practice_test.py')); _m=_u.module_from_spec(_spec); _spec.loader.exec_module(_m); 
for _k,_t in TESTS.items(): _m.build(_t, _k)
subprocess.run(['python3', os.path.join(os.path.dirname(__file__),'free_first.py')], check=False, stdout=subprocess.DEVNULL)
