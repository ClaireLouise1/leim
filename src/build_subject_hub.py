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
   strands=[
    ('🔢','Number',['integer-rush','prime-smash','fraction-match','round-it','venn-sorter','percent-pop','share-it-out','power-up','surd-simplify','clock-dash','shop-keeper','payslip-puzzle','road-trip']),
    ('🧮','Algebra &amp; Functions',['like-term-sweep','bracket-blaster','factor-match','balance-it','two-line-crossing','root-rush','number-line-shade','rearrange-race','pattern-builder','growth-spotter','graph-match']),
    ('📐','Geometry &amp; Trigonometry',['angle-chase','construction-steps','proof-builder','mirror-move','floor-planner','pack-it','ladder-lab','line-lab','clinometer-challenge']),
    ('📊','Statistics &amp; Probability',['data-detective','average-ace','spin-and-predict','coin-dice-lab']),
   ]),
}
SHORT = {'Integers &amp; order of operations':'Integers &amp; BIMDAS','Factors, multiples &amp; primes (HCF, LCM)':'Factors, multiples &amp; primes','Decimals, rounding &amp; estimation':'Decimals &amp; rounding','Units of measure, time &amp; timetables':'Units, time &amp; timetables','Money 1':'Bills, VAT &amp; profit','Money 2':'Tax, pay &amp; interest','Speed, distance, time &amp; currency':'Speed &amp; currency','Algebra 1':'Expressions','Algebra 2':'Expanding brackets','Algebraic fractions, long division &amp; changing the subject':'Changing the subject','Patterns 1':'Linear patterns','Patterns 2':'Quadratic patterns','Geometry 1':'Angles &amp; triangles','Geometry 2':'Theorems &amp; proofs','Transformations &amp; symmetry':'Transformations','Area, perimeter &amp; scale drawings':'Area &amp; perimeter','Volume &amp; surface area (3D solids &amp; nets)':'Volume &amp; surface area','Pythagoras &amp; right-angled triangles':'Pythagoras','Coordinate geometry of the line':'The line','Statistics 1':'Collecting data','Statistics 2':'Graphs &amp; averages','Probability 1':'Chance','Probability 2':'Relative frequency'}

STYLES = open(os.path.join(os.path.dirname(__file__), 'subject_hub.css'), encoding='utf-8').read()

def build(key, cfg):
    idx = open('index.html', encoding='utf-8').read()
    guide = open(cfg['guide'], encoding='utf-8').read()
    cards = dict((s,(g,d)) for s,g,d in re.findall(r'<a class="card" href="([a-z0-9-]+)\.html"[^>]*><h3>(.*?)</h3><p>(.*?)</p>', guide))
    head = idx.split('<style>')[0]
    url = f'https://leim.ie/junior-cycle-{key}.html'
    t = f'Junior Cycle {cfg["title"]} revision games | Léim'
    head = re.sub(r'<title>.*?</title>', f'<title>{t}</title>', head)
    head = head.replace('href="https://leim.ie/"', f'href="{url}"').replace('content="https://leim.ie/"', f'content="{url}"')
    head = re.sub(r'(<meta property="og:title" content=")[^"]*', r'\g<1>'+t, head)
    hdr = idx.split('<body>')[1].split('<main id="main">')[0]
    foot = '</main>' + idx.split('</main>')[1]
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
            rows.append(f'<a class="topic" href="{s}.html"><span class="n">{n}</span><div><div class="t">{topic}</div><div class="m"><span class="g">🎮 {g}</span>{came}</div></div><span class="go">›</span></a>')
        sid = ' id="games"' if i == 0 else ''
        out.append(f'<section class="strand"{sid}><h2>{icon} {name} <small>{len(slugs)} topics</small></h2><div class="tlist">{"".join(rows)}</div></section>')
    chips = ''.join(f'<a class="chip {c}" href="{h}">{l}</a>' for c,l,h in cfg['chips'])
    mh, mt, ms = cfg['mix']
    main = f'''<main id="main">
<div class="home">
<p class="crumbs"><a href="index.html">Home</a> › <a href="index.html#jc">Junior Cycle</a> › {cfg["title"]}</p>
<h1 class="home-title">Junior Cycle <span class="acc">{cfg["title"]}</span></h1>
<p style="margin:0 0 10px;font-weight:600">{n} topics · tap one to play · 📅 = how many of the last 5 exams it came up in</p>
<div class="btnrow">{chips}</div>
{''.join(out)}
<a class="mix" href="{mh}"><span class="n">🔀</span><div><b>{mt}</b><div style="opacity:.8;font-size:.9rem">{ms}</div></div></a>
<p style="margin-top:20px;font-size:.9rem;color:var(--muted)">📝 Practice tests for each topic: coming soon. Parents and teachers: see the <a href="{cfg["guide"]}">course guide</a>.</p>
</div>
'''
    open(f'junior-cycle-{key}.html','w',encoding='utf-8').write(head+'<style>'+STYLES+'</style>\n</head>\n<body>'+hdr+main+foot)
    print('built', key, n, 'topics')

for k,c in SUBJECTS.items(): build(k,c)
subprocess.run(['python3', os.path.join(os.path.dirname(__file__),'free_first.py')], check=False, stdout=subprocess.DEVNULL)
