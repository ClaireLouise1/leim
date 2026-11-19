# -*- coding: utf-8 -*-
"""Léim Oral CBA Prep Pack (Junior Cycle Spanish): pack PDF + cover + free Speaking page + audio page.
Usage: python3 src/build_oral_cba.py OUTDIR   (pack PDF and cover PNG go to OUTDIR; site pages written in the repo)"""
import sys, os, re, json, html, subprocess
sys.path.insert(0, os.path.dirname(__file__))
from oral_cba_data import *

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
S = R + 'src/'
OUT = sys.argv[1] if len(sys.argv) > 1 else '/tmp/oral'
os.makedirs(OUT, exist_ok=True)
AUDIO_URL = "leim.ie/oral"
E = lambda s: s  # texts already contain safe inline HTML (<i>) and no bare &

def strip(s): return re.sub(r'<[^>]+>', '', s)

# ---------- picture card ----------
def market_svg(w="100%"):
    oranges = ''.join('<circle cx="%d" cy="%d" r="9" fill="#F28C28" stroke="#C96A10" stroke-width="1.2"/>' % (62 + 19 * (i % 4) + (9 if i // 4 % 2 else 0), 200 - 15 * (i // 4)) for i in range(11))
    apples = ''.join('<circle cx="%d" cy="%d" r="9" fill="#D7383B" stroke="#A82326" stroke-width="1.2"/>' % (172 + 19 * (i % 4) + (9 if i // 4 % 2 else 0), 200 - 15 * (i // 4)) for i in range(11))
    bananas = ''.join('<path d="M%d %d q14 16 34 0 q-18 6 -34 0z" fill="#F4D03F" stroke="#B7950B" stroke-width="1.2"/>' % (282 + 6 * (i % 3), 196 - 11 * i) for i in range(5))
    def person(x, body, h=1.0, bag=False, apron=False, hair="#5B3A1E", dy=0):
        y0 = 150 + (1 - h) * 60 + dy
        s = '<circle cx="%d" cy="%d" r="%d" fill="#F1C9A5" stroke="#1B2430" stroke-width="1.5"/>' % (x, y0, 13 * h)
        s += '<path d="M%d %d a%d %d 0 0 1 %d 0z" fill="%s"/>' % (x - 13 * h, y0 - 2, 13 * h, 11 * h, 26 * h, hair)
        s += '<rect x="%d" y="%d" width="%d" height="%d" rx="9" fill="%s" stroke="#1B2430" stroke-width="1.5"/>' % (x - 17 * h, y0 + 15 * h, 34 * h, 62 * h, body)
        if apron: s += '<rect x="%d" y="%d" width="%d" height="%d" rx="4" fill="#2E7D57"/>' % (x - 11, y0 + 24, 22, 46)
        s += '<path d="M%d %d a4 3 0 0 0 8 0" fill="none" stroke="#1B2430" stroke-width="1.4"/>' % (x - 4, y0 + 3 * h)
        if bag: s += '<rect x="%d" y="%d" width="20" height="22" rx="3" fill="#F6CF5A" stroke="#1B2430" stroke-width="1.5"/><path d="M%d %d q6 -12 12 0" fill="none" stroke="#1B2430" stroke-width="1.5"/>' % (x + 14, y0 + 48, x + 18, y0 + 48)
        return s
    sign = lambda x, t1, t2: '<rect x="%d" y="214" width="76" height="30" rx="4" fill="#fff" stroke="#1B2430" stroke-width="1.5"/><text x="%d" y="227" font-size="10.5" font-weight="700" text-anchor="middle">%s</text><text x="%d" y="240" font-size="10" text-anchor="middle">%s</text>' % (x, x + 38, t1, x + 38, t2)
    stripes = ''.join('<rect x="%d" y="60" width="30" height="34" fill="%s"/>' % (30 + 30 * i, '#D7383B' if i % 2 == 0 else '#fff') for i in range(10))
    return ('<svg viewBox="0 0 470 300" width="%s" xmlns="http://www.w3.org/2000/svg" font-family="Inter,sans-serif">' % w +
        '<rect width="470" height="300" fill="#E8F3FA"/><circle cx="420" cy="42" r="22" fill="#F6CF5A"/>'
        '<rect x="0" y="262" width="470" height="38" fill="#D9D3C7"/>'
        '<rect x="30" y="94" width="300" height="8" fill="#8B5A2B"/><rect x="34" y="102" width="6" height="110" fill="#8B5A2B"/><rect x="320" y="102" width="6" height="110" fill="#8B5A2B"/>'
        + stripes + '<rect x="30" y="60" width="300" height="34" fill="none" stroke="#1B2430" stroke-width="1.5"/>'
        '<text x="180" y="83" font-size="15" font-weight="800" text-anchor="middle" fill="#1B2430">FRUTAS MARI</text>'
        + person(110, "#F7F7F7", apron=True, hair="#1B2430", dy=-34) +
        '<rect x="30" y="205" width="300" height="57" fill="#B07A45" stroke="#1B2430" stroke-width="1.5"/>'
        '<rect x="50" y="172" width="96" height="38" fill="#C9965E" stroke="#1B2430" stroke-width="1.2"/>'
        '<rect x="160" y="172" width="96" height="38" fill="#C9965E" stroke="#1B2430" stroke-width="1.2"/>'
        '<rect x="270" y="172" width="54" height="38" fill="#C9965E" stroke="#1B2430" stroke-width="1.2"/>'
        + oranges + apples + bananas +
        sign(58, "Naranjas", "1,50 €/kg") + sign(168, "Manzanas", "2,00 €/kg") + sign(254, "Plátanos", "1,80 €/kg") +
        person(370, "#3A6EA5", h=0.95, hair="#C68A3C") + person(425, "#C2185B", h=0.9, bag=True, hair="#5B3A1E") +
        '</svg>')

# ---------- pack HTML ----------
FOOT = "Léim · Oral CBA Prep Pack · JC Spanish · LOs (2017 spec) %s · One household or one teacher" % LO17
CSS = '''
@page{@bottom-left{content:"%s";font-size:6.8pt}}
@page:first{margin:0;@bottom-left{content:none}@bottom-right{content:none}}
body{font-size:10pt;line-height:1.42}
.cover{width:210mm;height:297mm;background:#1B2430;color:#fff;padding:26mm 22mm 22mm;display:flex;flex-direction:column;justify-content:space-between;page-break-after:always}
.cover .pill{display:inline-block;background:#2E7D57;border-radius:99px;padding:5px 14px;font-weight:700;font-size:9.5pt;letter-spacing:.06em;text-transform:uppercase}
.cover h1{font-size:50pt;line-height:1.02;letter-spacing:-.03em;margin:16mm 0 0;color:#fff}
.cover h1 span{background:#F6CF5A;color:#1B2430;padding:0 6px}
.cover .sub{font-size:15pt;color:#C9D1DA;margin-top:10mm;line-height:1.4;max-width:160mm}
.cover ul{list-style:none;padding:0;margin:11mm 0 0;font-size:12.3pt;line-height:1.85}
.cover ul li:before{content:"✓";color:#F6CF5A;font-weight:800;margin-right:10px}
.cover .foot{display:flex;justify-content:space-between;align-items:flex-end;font-size:11pt;font-weight:700}
.cover .foot .small{color:#C9D1DA;font-weight:500;font-size:9pt;max-width:125mm;line-height:1.45}
.cover .logo{font-size:20pt}
.band{padding:11px 16px;margin-bottom:9px}
.band h1{font-size:18pt}
h2{font-size:13pt;margin:10px 0 5px}
h3{font-size:11pt;margin:8px 0 3px}
.setup{background:var(--cream);border:1px solid var(--cream-line);border-radius:8px;padding:6px 11px;margin:6px 0;font-size:9.6pt}
.model{border-left:4px solid var(--green);background:#FAFBFC;padding:7px 12px;margin:6px 0;font-size:10.5pt;line-height:1.5}
.model p{margin:4px 0}
.qa{width:100%%;border-collapse:collapse;margin:6px 0}
.qa td{border-bottom:1px solid var(--line);padding:4px 6px;vertical-align:top;font-size:9.8pt}
.qa td.q{width:42%%;font-weight:700;color:var(--green)}
.why{margin:3px 0;padding-left:18px}.why li{margin:2px 0}
.yt{background:var(--green-soft);border-radius:8px;padding:7px 11px;margin:7px 0}
.yt b{color:var(--green)}
.dl{margin:6px 0}
.dl p{margin:3px 0;font-size:10.2pt;line-height:1.45}
.dl .sp{font-weight:800;color:var(--green)}
.dl .sp.t{color:#8a5a00}
.tn{font-size:8.8pt;color:var(--muted);margin:3px 0}
.foq td{font-size:8.9pt;padding:4px 6px;vertical-align:top;line-height:1.35}
.foq th{font-size:8.8pt;padding:4px 6px}
.foq td:first-child{font-weight:800;width:23mm}
.two{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.qb{columns:2;column-gap:12px}
.qb .t{break-inside:avoid;margin-bottom:9px}
.qb h3{font-size:10.4pt;margin:0 0 2px;background:var(--green);color:#fff;border-radius:5px;padding:2px 7px}
.qb p{margin:2.5px 0;font-size:9.6pt;line-height:1.38}
.qb p i{color:var(--muted)}
.lad td{font-size:9.4pt;padding:4px 6px;vertical-align:top}
.lad td:first-child{width:16mm;font-weight:800}
.box{display:inline-block;width:9px;height:9px;border:1.3px solid var(--ink);border-radius:2px;margin-right:7px;vertical-align:-1px}
ul.ck{list-style:none;padding-left:0;margin:3px 0}ul.ck li{margin:4px 0}
.write{border:1.5px solid var(--line);border-radius:8px;padding:6px 10px;margin:6px 0}
.write .h{font-weight:800;font-size:9.6pt;color:var(--green)}
.lines span{display:block;border-bottom:1px solid #B5BCC5;height:19px}
.cue{border:2px dashed var(--muted);border-radius:10px;padding:8px 12px;height:58mm;position:relative}
.pic{border:1.5px solid var(--line);border-radius:10px;padding:6px;margin:6px 0;text-align:center}
.pic svg{height:62mm;width:auto}
.plan td{font-size:9.6pt;padding:5px 7px;vertical-align:top}.plan td:first-child{font-weight:800;width:17mm;white-space:nowrap}
.ideas td{font-size:9.3pt;padding:4px 7px;vertical-align:top}.ideas td:first-child{font-weight:800;width:25mm}
.log td,.log th{font-size:9pt;padding:6px 7px;height:9mm}
.small{font-size:9pt}
''' % FOOT

def band(k, t): return '<div class="band"><div><div class="k">%s</div><h1>%s</h1></div><div class="logo">↗ Léim</div></div>' % (k, t)
def qa_table(qa, title="Questions your teacher might ask afterwards, with good answers"):
    if not qa: return ''
    return '<h3>%s</h3><table class="qa">%s</table>' % (title, ''.join('<tr><td class="q" lang="es">%s</td><td lang="es">%s</td></tr>' % (q, a) for q, a in qa))
def dialogue(m):
    out = []
    for who, t in m['lines']:
        out.append('<p lang="es"><span class="sp%s">%s:</span> %s</p>' % ('' if who == 0 else ' t', m['who'][who], t))
    return '<div class="dl model">%s</div>' % ''.join(out)
def why(m): return '<h3>Why it works</h3><ul class="why">%s</ul>' % ''.join('<li>%s</li>' % w for w in m['why'])
def listen(m): return '<p class="tn">Hear it read aloud: <b>%s</b> → %s.</p>' % (AUDIO_URL, strip(m['title']))

M = {m['id']: m for m in MODELS}
pages = []
# 1 cover
pages.append('''<div class="cover"><div><span class="pill">Junior Cycle Spanish · Oral CBA</span>
<h1>The Oral <span>CBA</span><br>Prep Pack</h1>
<div class="sub">Everything a 2nd year needs to prepare the Spanish speaking CBA: how it works, what the teacher listens for, and models of all four formats.</div>
<ul><li>How the oral CBA works, in plain English</li><li>What gets you each descriptor, and how to move up</li><li>6 full models: presentations, interview, role-plays, picture</li><li>48-question bank with answer starters</li><li>Survival phrases, answer ladders, pronunciation</li><li>3-week plan, planning sheet, self-check, reflection help</li><li>Every model read aloud at leim.ie/oral</li></ul></div>
<div class="foot"><div class="small">Original Léim material for the 2017 Junior Cycle Modern Foreign Languages specification (CBA 1, Oral Communication). Not official material: Léim is independent and not connected to the NCCA or the State Examinations Commission. Spotted a mistake? Email hello@leim.ie</div><div class="logo">↗ Léim</div></div></div>''')
# 2 how it works
pages.append('<div class="page">' + band("Start here", "How the oral CBA works") + '''
<p>The Oral Communication CBA is a short speaking task done in class and judged by your Spanish teacher. There are <b>no marks</b>: you get a <b>descriptor</b>, printed on your Junior Cycle Profile of Achievement (JCPA). It does not change your exam grade.</p>
<table><tr><th style="width:34mm">Question</th><th>Answer</th></tr>
<tr><td><b>When?</b></td><td>2017 specification (exams in 2027 and 2028): <b>CBA 1</b>, finished by the <b>end of 2nd year</b>, in a set window on the national CBA calendar. Students sitting the exam in 2027 and 2028 do one CBA in Spanish, and it must be this oral one.<br><span class="small">1st years from September 2026 follow the 2025 specification: the oral becomes CBA 2, the Oral Communication Task, in 3rd year. The advice in this pack still applies.</span></td></tr>
<tr><td><b>How long to prepare?</b></td><td>Up to <b>three weeks</b> of class time. You choose your topic, stimulus or role-play at the start, and it must be one you <b>haven't already practised or prepared</b>.</td></tr>
<tr><td><b>How long is it?</b></td><td>About <b>3–4 minutes</b>, including the teacher's questions, pauses and any corrections.</td></tr>
<tr><td><b>Alone or with others?</b></td><td>Alone, in a pair or in a small group (your teacher agrees it). In a pair or group, each person must have enough time to speak.</td></tr>
<tr><td><b>In which language?</b></td><td>Spanish, all the way through.</td></tr>
<tr><td><b>Questions?</b></td><td>Yes. In every format the teacher asks questions you haven't seen, to check you understand and can answer. Prepare for them (page 11).</td></tr>
<tr><td><b>Notes and props?</b></td><td>A presentation can use slides, pictures or props. Rules on notes and cue cards vary from school to school: <b>ask your teacher</b> before you make one.</td></tr>
<tr><td><b>Afterwards?</b></td><td>You write a short <b>Student Reflection Note</b> (help on page 15).</td></tr>
<tr><td><b>Descriptors</b></td><td>Exceptional · Above expectations · In line with expectations · Yet to meet expectations</td></tr></table>
<h2>The four formats: you choose one</h2>
<div class="two"><div><p><b>1. Presentation</b> on a topic, with pictures, slides or props, then the teacher's questions. <i>Models: pages 5–6.</i></p>
<p><b>2. Interview</b>: you answer the teacher's questions (in a pair or group, you also ask each other). <i>Model: page 7.</i></p></div>
<div><p><b>3. Role-play</b>: a real-life situation such as a hotel or a host family, then questions. <i>Models: pages 8–9.</i></p>
<p><b>4. Conversation about a stimulus</b>: a picture, text, video or object starts the conversation. <i>Model: page 10.</i></p></div></div>
<div class="yt"><b>The golden rule.</b> Your CBA topic must be new, so <b>don't learn these models off</b>. Use them to see how a good answer is built, borrow the phrases, and make your own on a different topic.</div>
</div>''')
# 3 FoQ
pages.append('<div class="page">' + band("What gets the grade", "What your teacher listens for") + '''
<p>Your teacher judges three things, using the official <b>Features of Quality</b>. Here they are in plain English (our summary; your teacher has the official wording, so ask to see it).</p>
<table class="foq"><tr><th></th><th>Speaking (production)</th><th>Answering questions (interaction)</th><th>How Spanish works (language awareness)</th></tr>
<tr><td>Exceptional</td><td>Very clear; flows very well; very accurate; a wide range of words.</td><td>Understands and answers the questions easily.</td><td>Uses the patterns very well (verb endings, agreement) and fixes slips.</td></tr>
<tr><td>Above expectations</td><td>Clear; flows well; good accuracy and range.</td><td>Understands well; answers make sense when the teacher speaks slowly and clearly.</td><td>Good use of the patterns; may fix slips.</td></tr>
<tr><td>In line with expectations</td><td>Clear enough to understand; some hesitation, mistakes and repeated words.</td><td>Understands some questions; answers mostly make sense.</td><td>Some awareness of the patterns.</td></tr>
<tr><td>Yet to meet expectations</td><td>Often unclear; only very basic words and phrases.</td><td>Understands and answers very little.</td><td>Little or no awareness of the patterns.</td></tr></table>
<p class="tn">The level is aimed at beginners: roughly A1–A2 on the European language scale. Nobody expects you to sound like a Spanish person.</p>
<h2>How to move up a level</h2>
<div class="two"><div>
<h3>Speaking</h3><ul class="why"><li><b>Speak, don't read.</b> Key words, not a script.</li><li><b>Short, correct sentences</b> beat long, broken ones.</li><li><b>Range:</b> three time frames, opinions with reasons, linking words (page 12).</li><li><b>Pronunciation:</b> clear vowels, the tricky letters (page 13).</li></ul>
<h3>Answering questions</h3><ul class="why"><li>Answer in <b>full sentences</b> and add one more thing: a reason, a detail or an example.</li><li>Didn't catch it? Ask: <i lang="es">¿Puede repetir, por favor?</i> That counts as interaction.</li><li>Practise with questions in a <b>random order</b>.</li></ul>
</div><div>
<h3>Language awareness</h3><ul class="why"><li>Check <b>verb endings</b>: <i lang="es">yo juego, fui, voy a ir</i>.</li><li>Make adjectives <b>agree</b>: <i lang="es">una casa bonita, unos amigos simpáticos</i>.</li><li><b>Fix your own slips</b>: <i lang="es">Fui… perdón, fuimos</i>. Self-correction is a good sign.</li><li>Know the classic traps (page 13).</li></ul>
<div class="yt"><b>Remember:</b> the teacher hears you once, live. Calm, clear and confident beats fast and complicated.</div>
</div></div></div>''')
# 4 choose + plan
ideas = ''.join('<tr><td>%s</td><td>%s</td></tr>' % (k, ' · '.join(v)) for k, v in IDEAS.items())
plan = ''.join('<tr><td>%s</td><td>%s</td></tr>' % (a, b) for a, b in PLAN3)
pages.append('<div class="page">' + band("Plan it", "Choose your format, plan your three weeks") + '''
<h2>Which format suits you?</h2>
<div class="two"><div><p><b>Presentation</b> if you like preparing and want to show off a topic you love. Lots of control, but the questions afterwards matter.</p><p><b>Interview</b> if you're good at chatting and want to talk about your own life.</p></div>
<div><p><b>Role-play</b> if you like acting and working with a partner. Great for polite phrases and questions.</p><p><b>Picture conversation</b> if you're good at describing and thinking on your feet.</p></div></div>
<h2>Topic ideas</h2><table class="ideas">''' + ideas + '''</table>
<p class="tn">Pick something you genuinely care about: it's easier to talk about, and easier to answer questions on.</p>
<h2>Your three weeks</h2><table class="plan">''' + plan + '''</table></div>''')
# 5-6 presentations
for mid, pg in (("pres1", "Format 1 · Presentation · Model A"), ("pres2", "Format 1 · Presentation · Model B")):
    m = M[mid]
    pages.append('<div class="page">' + band(pg, m['title']) + '<div class="setup"><b>Setting:</b> %s</div>' % m['setup'] +
        '<div class="model" lang="es">%s</div>' % ''.join('<p>%s</p>' % p for p in m['talk']) + qa_table(m['qa']) + why(m) + listen(m) + '</div>')
# 7 interview
m = M['int1']
pages.append('<div class="page">' + band("Format 2 · Interview", m['title']) + '<div class="setup"><b>Setting:</b> %s</div>' % m['setup'] +
    qa_table(m['qa'], "Twelve questions, twelve good answers") + why(m) +
    '<div class="yt"><b>Your turn:</b> cover the answers and answer each question about <b>yourself</b>, with two sentences each. Then ask a friend to read the questions in a random order.</div>' + listen(m) + '</div>')
# 8-9 role-plays
for mid, pg in (("rp1", "Format 3 · Role-play · Model A"), ("rp2", "Format 3 · Role-play · Model B")):
    m = M[mid]
    pages.append('<div class="page">' + band(pg, m['title']) + '<div class="setup"><b>Setting:</b> %s</div>' % m['setup'] + dialogue(m) +
        qa_table(m['qa'], "Then the teacher steps out of the role and asks you") + why(m) + listen(m) + '</div>')
# 10 picture
m = M['stim1']
pages.append('<div class="page">' + band("Format 4 · Conversation about a picture", m['title']) + '<div class="setup"><b>Setting:</b> %s</div>' % m['setup'] +
    '<div class="pic">%s</div>' % market_svg() + dialogue(m) + why(m) +
    '<p class="small"><b>Picture toolkit:</b> <i lang="es">En la foto hay… · A la izquierda / a la derecha · En el centro · Al fondo · Lleva… · Creo que… porque… · Parece…</i></p>' + listen(m) + '</div>')
# 11 question bank
qb = ''.join('<div class="t"><h3 lang="es">%s</h3>%s</div>' % (t, ''.join('<p lang="es"><b>%s</b> <i>%s</i></p>' % (q, a) for q, a in qs)) for t, qs in QBANK)
pages.append('<div class="page">' + band("Be ready for anything", "48 questions teachers often ask") + '''
<p class="small">The teacher's questions are unscripted, but most come from these topics. Each question has a way to start your answer (in grey). <b>Aim for two sentences per answer</b>, one with a reason.</p>
<div class="qb">''' + qb + '</div></div>')
assert sum(len(q) for _, q in QBANK) == 48
# 12 keep it going
surv = ''.join('<tr><td lang="es"><b>%s</b></td><td>%s</td></tr>' % (a, b) for a, b in SURVIVAL)
lad = ''.join('<h3 lang="es">%s</h3><table class="lad"><tr><td>Basic</td><td lang="es">%s</td></tr><tr><td>Good</td><td lang="es">%s</td></tr><tr><td>Great</td><td lang="es">%s</td></tr></table>' % L for L in LADDERS)
pages.append('<div class="page">' + band("Keep the conversation going", "Survival phrases and answer ladders") + '''
<div class="two"><div><h2>When you're stuck</h2><table>''' + surv + '''</table>
<p class="small">Asking for help in Spanish is <b>good</b> interaction, not a failure.</p></div>
<div><h2>Buy time, join up, give opinions</h2>
<p><b>Thinking words:</b> <i lang="es">''' + FILLERS + '''</i></p>
<p><b>Linking words:</b> <i lang="es">''' + LINKS + '''</i></p>
<p><b>Opinions:</b> <i lang="es">''' + OPINIONS + '''</i></p>
<p><b>Time frames:</b> <i lang="es">''' + TENSES + '''</i></p></div></div>
<h2>Climb the answer ladder</h2><p class="small">The same question answered three ways. Great answers add <b>a detail, a reason, the past and the future</b>.</p>''' + lad + '</div>')
# 13 pronunciation + mistakes
pr = ''.join('<tr><td><b>%s</b></td><td>%s</td></tr>' % p for p in PRON)
mk = ''.join('<tr><td lang="es">✗ %s</td><td lang="es"><b>%s</b></td></tr>' % p for p in MISTAKES).replace('✗', '')
pages.append('<div class="page">' + band("Sound good", "Pronunciation and classic mistakes") + '''
<h2>Pronunciation: the sounds that matter</h2><table>''' + pr + '''</table>
<p class="small"><b>Practise:</b> record yourself reading your plan, then listen to the Léim audio at <b>''' + AUDIO_URL + '''</b> and copy the rhythm. Slow and clear is better than fast.</p>
<h2>Classic mistakes, and the fix</h2><table><tr><th>Not this</th><th>This</th></tr>''' + mk + '</table></div>')
# 14 planning sheet
pages.append('<div class="page">' + band("Your plan", "My oral CBA planning sheet") + '''
<div class="two"><div class="write"><div class="h">My format</div><div class="lines"><span></span></div></div><div class="write"><div class="h">My topic / situation</div><div class="lines"><span></span></div></div></div>
<div class="write"><div class="h">My plan (start · 3–4 parts · end)</div><div class="lines">''' + '<span></span>' * 6 + '''</div></div>
<div class="two"><div class="write"><div class="h">Key words I need (Spanish = English)</div><div class="lines">''' + '<span></span>' * 7 + '''</div></div>
<div class="write"><div class="h">My sources (websites, videos, books)</div><div class="lines">''' + '<span></span>' * 7 + '''</div></div></div>
<div class="write"><div class="h">10 questions my teacher might ask me, and my first sentence for each</div><div class="lines">''' + '<span></span>' * 10 + '''</div></div>
<h3>Cue card (only if your teacher allows one): key words, never full sentences</h3><div class="cue"></div></div>''')
# 15 self-check + log + reflection
ck = ''.join('<li><span class="box"></span>%s</li>' % s for s in SELFCHECK)
rf = ''.join('<li>%s</li>' % s for s in REFLECT)
pages.append('<div class="page">' + band("Nearly there", "Self-check, practice log and reflection") + '''
<h2>Self-check: tick when it's true</h2><ul class="ck">''' + ck + '''</ul>
<h2>Practice log</h2><table class="log"><tr><th style="width:24mm">Date</th><th>Who I practised with</th><th style="width:22mm">Time</th><th>One thing to fix</th></tr>''' + '<tr><td></td><td></td><td></td><td></td></tr>' * 5 + '''</table>
<h2>Your Student Reflection Note</h2>
<p>After the CBA you write a short reflection about how it went. Write it <b>yourself</b>: there's no right answer, and your teacher wants your own thoughts. Use these questions to get started:</p>
<ol class="why">''' + rf + '''</ol>
<p class="tn">Jot ideas down straight after the CBA, while you still remember how it felt.</p></div>''')
# 16 back page
pages.append('<div class="page">' + band("Before you go", "Hear it, play it, ask") + '''
<h2>Hear every model read aloud</h2>
<p>Go to <b>''' + AUDIO_URL + '''</b> on a phone, tablet or computer. Press play and your device reads each model in Spanish, with a different voice for the teacher. You can slow it down, and pause after each line to repeat it.</p>
<h2>Practise for free on leim.ie</h2>
<ul class="why"><li><b>Meet &amp; Greet</b>: greetings, introductions, <i lang="es">tú</i> and <i lang="es">usted</i>.</li>
<li><b>Question Quick-Fire</b>: question words and quick answers.</li>
<li><b>Sound Match</b>: Spanish sounds and spelling, with a Listening mode.</li>
<li><b>Fiesta Quiz</b>: festivals, food and places for a culture presentation.</li>
<li><b>The Speaking page</b>: leim.ie/junior-cycle-spanish-speaking.html</li></ul>
<h2>For parents: how to help (no Spanish needed)</h2>
<ul class="why"><li><b>Be the audience.</b> Let your child give the talk to you, then ask two questions from page 11 (read them out as best you can).</li>
<li><b>Time it.</b> About 3–4 minutes including questions.</li>
<li><b>Don't write it for them.</b> The CBA must be their own work, and teachers can tell.</li>
<li><b>Keep it calm.</b> It's one line on the JCPA and it doesn't change the exam grade.</li></ul>
<div class="yt"><b>About this pack.</b> All texts, models and questions were written by Léim for the Junior Cycle Spanish Oral Communication CBA (2017 specification). It is not official material. Léim is independent and not connected to the NCCA, the Department of Education or the State Examinations Commission. Always follow your teacher's instructions and your school's CBA calendar. Spotted a mistake? Email <b>hello@leim.ie</b>.</div>
<p class="tn">© Léim 2026 · leim.ie · Licence: one household, or one teacher for their own classes.</p></div>''')

doc = '<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Oral CBA Prep Pack | Léim</title><link rel="stylesheet" href="pdf.css"><style>%s</style></head><body>%s</body></html>' % (CSS, '\n'.join(pages))
open(S + 'oral-cba-prep-pack.html', 'w', encoding='utf-8').write(doc)
cover = open(S + 'jc-spanish-exam-pack-cover.html', encoding='utf-8').read()
for a, b in [('Junior Cycle Spanish · Exams 2027 &amp; 2028', 'Junior Cycle Spanish · Oral CBA'),
             ('The Spanish <span>Exam Pack</span>', 'The Oral <span>CBA</span> Prep Pack'),
             ('8 model answers · 4 reading sets · 4 listening sets<br>Full 2-hour mock paper + marking guide', 'All 4 formats · 6 full models with audio<br>48-question bank · 3-week plan · self-check'),
             ('32 pages · answers included', '16 pages · for 2nd years')]:
    assert cover.count(a) == 1, a; cover = cover.replace(a, b)
open(S + 'oral-cba-prep-pack-cover.html', 'w', encoding='utf-8').write(cover)

if '--nopdf' not in sys.argv:
    pdf = OUT + '/Oral-CBA-Prep-Pack-Spanish-Leim.pdf'
    subprocess.run(['google-chrome', '--headless=new', '--no-sandbox', '--no-pdf-header-footer', '--print-to-pdf=' + pdf, 'oral-cba-prep-pack.html'], cwd=S, check=True, capture_output=True)
    subprocess.run(['google-chrome', '--headless=new', '--no-sandbox', '--hide-scrollbars', '--screenshot=' + OUT + '/oral-cba-prep-pack-cover.png', '--window-size=1200,1200', 'oral-cba-prep-pack-cover.html'], cwd=S, check=True, capture_output=True)
    n = int(re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout).group(1))
    print('pages', n); assert n == 16, n

# ---------- data for the site pages ----------
def audio_items():
    items = []
    for m in MODELS:
        lines = []
        if 'talk' in m: lines += [[0, p] for p in m['talk']]
        if 'lines' in m: lines += [[w, t] for w, t in m['lines']]
        for q, a in m['qa']: lines += [[1, q], [0, a]]
        items.append({'id': m['id'], 'title': strip(m['title']), 'fmt': m['fmt'], 'who': m['who'], 'lines': [[w, html.unescape(strip(t))] for w, t in lines]})
    return items
json.dump(audio_items(), open('/tmp/oral_audio.json', 'w'), ensure_ascii=False)
print('ok')

# ================= site pages =================
tpl = open(R + 'junior-cycle-spanish-no-spanish-at-school.html', encoding='utf-8').read()
FOOTER = tpl[tpl.index('</main>') + len('</main>'):]
def head(title, desc, noindex=False, extra=''):
    h = tpl[:tpl.index('<main id="main">')]
    h = re.sub(r'<title>.*?</title>', '<title>%s</title>' % title, h)
    h = re.sub(r'<meta name="description" content=".*?">', '<meta name="description" content="%s">%s' % (desc, '\n<meta name="robots" content="noindex">' if noindex else ''), h)
    return h.replace('</style>', PLAYER_CSS + extra + '</style>')

PLAYER_CSS = '''
.au{background:#fff;border:1px solid var(--line);border-radius:14px;padding:16px 18px;margin:14px 0}
.au.playing{border-color:var(--green);box-shadow:0 0 0 3px rgba(46,125,87,.15)}
.au h3{margin:0 0 4px!important;font-size:20px}
.au .meta{font-size:15px;color:var(--ink-2);margin-bottom:10px}
.au-row{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:8px 0}
.au-btn{font:inherit;font-weight:700;font-size:15px;border-radius:999px;padding:9px 16px;border:2px solid var(--green);background:var(--green);color:#fff;cursor:pointer}
.au-btn.ghost{background:#fff;color:var(--green)}
.au-st{font-size:15px;font-weight:600;color:var(--green);min-height:22px;margin-top:4px}
.au-txt{display:none;background:var(--cream);border:1px solid var(--cream-line);border-radius:10px;padding:10px 14px;margin-top:10px}
.au-txt.open{display:block}
.au-txt p{margin:0 0 6px!important;font-size:16px!important;line-height:1.5}
.au-txt p.on{background:#FFE58A;border-radius:6px}
.au-txt b{color:var(--green)}.au-txt b.t{color:#8a5a00}
.au-set{display:flex;flex-wrap:wrap;gap:14px;align-items:center;background:var(--cream);border:1px solid var(--cream-line);border-radius:12px;padding:12px 16px;margin:16px 0;font-size:16px}
.au-set select{font:inherit;padding:6px 8px;border-radius:8px;border:1px solid var(--line)}
.au-warn{display:none;background:#fdecea;border:1px solid #f3b8b0;border-radius:12px;padding:14px 16px;margin:14px 0;font-size:16px}
.au-warn.show{display:block}
.qa2{margin:10px 0}.qa2 p{margin:0 0 4px!important}
.say{font:inherit;font-size:14px;font-weight:700;border:1.5px solid var(--green);color:var(--green);background:#fff;border-radius:999px;padding:2px 10px;margin-left:6px;cursor:pointer;vertical-align:1px}
'''
SETTINGS = '''<div id="auWarn" class="au-warn"><b>No Spanish voice found on this device.</b> Try Chrome, Safari or Edge, or a phone or tablet. On a computer you may need to add a Spanish voice in the system settings. The texts are under each item (press <b>Show the text</b>).</div>
<div class="au-set"><label>Speed: <select id="auRate"><option value="0.75">Slow</option><option value="0.9" selected>Normal for learners</option><option value="1">Natural</option></select></label>
<label><input type="checkbox" id="auRep"> Pause after each line so I can repeat it</label></div>'''
PLAYER_JS = r'''<script>
(function(){
var DATA=__DATA__;
var $=function(id){return document.getElementById(id);};
var synth=window.speechSynthesis,voices=[],run=0,cur=null;
function esc(s){return s.replace(/[&<>]/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;"}[c];});}
function findVoices(){
  if(!synth){$("auWarn").classList.add("show");return;}
  var v=synth.getVoices()||[];
  var bad=/eddy|flo\b|grandma|grandpa|reed|rocko|sandy|shelley|bells|bubbles|jester|organ|superstar|trinoids|whisper|wobble|zarvox|albert|bad news|good news|boing|cellos|fred|junior|kathy|ralph/i;
  var good=/m[oó]nica|jorge|marisol|google|microsoft|elvira|[aá]lvaro|helena|pablo|laura|lucia|luc[ií]a|enrique|conchita|dar[ií]o|paulina|juan|diego|isabela/i;
  function score(x){return (/^es[-_]ES/i.test(x.lang)?4:0)+(good.test(x.name)?2:0)-(bad.test(x.name)?10:0);}
  var es=v.filter(function(x){return /^es/i.test(x.lang);}).sort(function(a,b){return score(b)-score(a);});
  var ok=es.filter(function(x){return !bad.test(x.name);});if(ok.length)es=ok;
  voices=es.slice(0,2);
  $("auWarn").classList.toggle("show",!voices.length&&v.length>0);
}
if(synth){findVoices();synth.onvoiceschanged=findVoices;setTimeout(function(){findVoices();if(!voices.length)$("auWarn").classList.add("show");},1500);}else findVoices();
function sentences(t){return (t.match(/[^.!?…]+[.!?…]+[»"]?|[^.!?…]+$/g)||[t]).map(function(s){return s.trim();}).filter(Boolean);}
function say(text,who,my){return new Promise(function(res){
  if(my!==run||!synth||!voices.length)return res();
  var u=new SpeechSynthesisUtterance(text);var v=voices[who%voices.length];
  u.voice=v;u.lang=v?v.lang:"es-ES";u.rate=parseFloat($("auRate").value);
  u.pitch=(voices.length<2&&who===1)?1.3:1;
  var done=false;function fin(){if(!done){done=true;res();}}
  u.onend=fin;u.onerror=fin;synth.speak(u);
  setTimeout(fin,Math.max(8000,text.length*230));
});}
function sleep(ms,my){return new Promise(function(r){setTimeout(r,my===run?ms:0);});}
function stop(){run++;if(synth)synth.cancel();if(cur){cur.el.classList.remove("playing");cur.st.textContent="";cur.el.querySelectorAll(".au-txt p").forEach(function(p){p.classList.remove("on");});cur=null;}}
async function play(it,el,st,from,to){
  stop();if(!voices.length){$("auWarn").classList.add("show");return;}
  var my=++run;cur={el:el,st:st};el.classList.add("playing");
  var ps=el.querySelectorAll(".au-txt p"),rep=$("auRep").checked;
  for(var i=from;i<to;i++){
    if(my!==run)return;
    ps.forEach(function(p){p.classList.remove("on");});if(ps[i])ps[i].classList.add("on");
    st.textContent="▶ "+(it.who[it.lines[i][0]]||"");
    var ss=sentences(it.lines[i][1]);
    for(var j=0;j<ss.length;j++){if(my!==run)return;await say(ss[j],it.lines[i][0],my);}
    if(rep&&my===run){st.textContent="Your turn: say it out loud…";await sleep(1500+it.lines[i][1].length*70,my);}
    else await sleep(350,my);
  }
  if(my!==run)return;
  st.textContent="✓ Finished.";el.classList.remove("playing");ps.forEach(function(p){p.classList.remove("on");});cur=null;
}
document.querySelectorAll("[data-au]").forEach(function(box){
  var it=DATA[box.getAttribute("data-au")];if(!it)return;
  var lim=parseInt(box.getAttribute("data-n")||"0",10)||it.lines.length;
  var h='<div class="au-row"><button class="au-btn" type="button" data-a="play">▶ Play</button><button class="au-btn ghost" type="button" data-a="stop">■ Stop</button><button class="au-btn ghost" type="button" data-a="txt">Show the text</button></div><div class="au-st" aria-live="polite"></div><div class="au-txt" lang="es">';
  for(var i=0;i<lim;i++){var L=it.lines[i];h+='<p data-i="'+i+'"><b class="'+(L[0]?"t":"")+'">'+esc(it.who[L[0]])+':</b> '+esc(L[1])+' <button class="say" type="button" data-a="one" data-i="'+i+'" aria-label="Play this line">▶</button></p>';}
  h+='</div>';box.insertAdjacentHTML("beforeend",h);
  var st=box.querySelector(".au-st");
  box.addEventListener("click",function(e){var b=e.target.closest("button");if(!b)return;var a=b.getAttribute("data-a");
    if(a==="play")play(it,box,st,0,lim);else if(a==="stop")stop();
    else if(a==="txt"){box.querySelector(".au-txt").classList.toggle("open");b.textContent=box.querySelector(".au-txt").classList.contains("open")?"Hide the text":"Show the text";}
    else if(a==="one"){var i=parseInt(b.getAttribute("data-i"),10);play(it,box,st,i,i+1);}});
});
})();
</script>
'''
items = {i['id']: i for i in audio_items()}
items['surv'] = {'id': 'surv', 'title': 'Survival phrases', 'fmt': '', 'who': ['Tú'], 'lines': [[0, a] for a, _ in SURVIVAL]}
items['lad'] = {'id': 'lad', 'title': 'Answer ladder', 'fmt': '', 'who': ['Básico', 'Bien', 'Muy bien', 'Pregunta'],
                'lines': [[3, LADDERS[0][0]], [0, LADDERS[0][1]], [1, LADDERS[0][2]], [2, LADDERS[0][3]]]}
# keep all spoken text free of HTML and of guillemet-dots
for it in items.values():
    for L in it['lines']: assert '<' not in L[1], L
def player_js(keys): return PLAYER_JS.replace('__DATA__', json.dumps({k: items[k] for k in keys}, ensure_ascii=False))

# ---------- audio page for the pack (noindex) ----------
cards = ''
for m in MODELS:
    cards += '<div class="au" id="%s" data-au="%s"><h3>%s</h3><div class="meta">%s · %s%s</div></div>\n' % (
        m['id'], m['id'], html.escape(strip(m['title'])), m['fmt'], ' and '.join(m['who']),
        ' · then the teacher\'s questions' if m['qa'] and m['fmt'] != 'Interview' else '')
audio_main = '''<main id="main">

<section class="hero">
  <div class="wrap">
    <div class="hero-copy">
      <span class="pill">Junior Cycle Spanish · Oral CBA Prep Pack</span>
      <h1>Hear the <span class="hl">oral CBA</span> models</h1>
      <p class="lede">Every model in the Léim Oral CBA Prep Pack, read aloud in Spanish with a different voice for the teacher. Listen, then press <b>Pause after each line</b> and say it yourself.</p>
    </div>
  </div>
</section>

<div class="block"><div class="wrap ec">
''' + SETTINGS + '\n' + cards + '''
<div class="note" style="margin-top:20px"><b>Remember:</b> your CBA topic must be one you haven't prepared before, so don't learn these off. Copy the rhythm and borrow the phrases. <a href="junior-cycle-spanish-speaking.html">More speaking help</a>.</div>
<p class="small" style="color:var(--muted);margin-top:16px">The voices come from your device. All texts are original Léim material, not official CBA material. Léim is independent and not connected to the NCCA or the State Examinations Commission.</p>
</div></div>

</main>'''
page = head('Oral CBA models: hear them in Spanish | Léim', 'Audio for the Léim Junior Cycle Spanish Oral CBA Prep Pack: every model presentation, interview, role-play and picture conversation read aloud in Spanish.', noindex=True) + audio_main + FOOTER
page = page.replace('<script src="site.js"></script>', '<script src="site.js"></script>\n' + player_js([m['id'] for m in MODELS]))
assert player_js([]) and page.count('__DATA__') == 0
open(R + 'junior-cycle-spanish-oral-cba-audio.html', 'w', encoding='utf-8').write(page)
os.makedirs(R + 'oral', exist_ok=True)
open(R + 'oral/index.html', 'w', encoding='utf-8').write('''<!doctype html>
<html lang="en-IE"><head><meta charset="utf-8"><title>Oral CBA models | Léim</title>
<meta name="robots" content="noindex">
<link rel="canonical" href="https://leim.ie/junior-cycle-spanish-oral-cba-audio.html">
<meta http-equiv="refresh" content="0; url=/junior-cycle-spanish-oral-cba-audio.html">
<script>location.replace("/junior-cycle-spanish-oral-cba-audio.html"+location.hash);</script>
</head><body><p><a href="/junior-cycle-spanish-oral-cba-audio.html">Go to the Oral CBA models</a></p></body></html>
''')


# ---------- free Speaking page ----------
sv = ''.join('<tr><td lang="es"><b>%s</b></td><td>%s</td></tr>' % (a, b) for a, b in SURVIVAL)
pl = ''.join('<li><b>%s:</b> %s</li>' % (a, re.sub(r'\s*\(page \d+\)', '', b)) for a, b in PLAN3).replace('use the models in this pack to learn HOW', 'use models like the one below to learn HOW')
ck = ''.join('<li>%s</li>' % re.sub(r'\s*\(page \d+\)', '', x) for x in SELFCHECK)
pr = ''.join('<li><b>%s</b> %s</li>' % p for p in PRON[:7])
LO_TAG = 'Junior Cycle Spanish learning outcomes: %s (2017 spec, exams 2027–2028)' % LO17
free_main = '''<main id="main">

<section class="hero">
  <div class="wrap">
    <div class="hero-copy">
      <span class="pill">Junior Cycle Spanish · Speaking · Oral CBA</span>
      <h1>Speaking and the <span class="hl">oral CBA</span></h1>
      <p class="lede">The June exam has no speaking part. Speaking is assessed in class, in the Oral Communication CBA. Here's how it works, what your teacher listens for, and how to prepare, with Spanish you can listen to.</p>
      <nav class="toc" aria-label="On this page">
        <a href="#how">How it works</a><a href="#listens">What the teacher listens for</a><a href="#formats">The 4 formats</a><a href="#plan">3-week plan</a><a href="#model">Hear a model</a><a href="#stuck">When you're stuck</a><a href="#ladder">Better answers</a><a href="#check">Self-check</a><a href="#parents">Parents</a>
      </nav>
    </div>
  </div>
</section>

<div class="block"><div class="wrap ec">
<p><span class="lo">''' + LO_TAG + '''</span></p>

<section id="how">
  <h2>How the oral CBA works</h2>
  <div class="table-wrap"><table><thead><tr><th>Question</th><th>Answer</th></tr></thead><tbody>
  <tr><td><b>When?</b></td><td>2017 specification (exams in 2027 and 2028): <b>CBA 1</b>, finished by the <b>end of 2nd year</b> in a set window. Students sitting the exam in 2027 and 2028 do one CBA in Spanish, and it must be this oral one. 1st years from September 2026 (2025 specification) do it as <b>CBA 2</b>, the Oral Communication Task, in 3rd year.</td></tr>
  <tr><td><b>Preparation</b></td><td>Up to <b>three weeks</b> in class. You pick your topic, stimulus or role-play at the start, and it must be one you <b>haven't already practised or prepared</b>.</td></tr>
  <tr><td><b>How long?</b></td><td>About <b>3–4 minutes</b>, including the teacher's questions.</td></tr>
  <tr><td><b>Who with?</b></td><td>Alone, in a pair or in a small group, as your teacher agrees.</td></tr>
  <tr><td><b>Questions?</b></td><td>Yes, in every format: unscripted questions to check you understand and can answer.</td></tr>
  <tr><td><b>Notes?</b></td><td>Presentations can use pictures, slides or props. Rules on notes and cue cards vary: ask your teacher.</td></tr>
  <tr><td><b>Afterwards</b></td><td>You write a short <b>Student Reflection Note</b> about how you prepared and what you learned.</td></tr>
  <tr><td><b>Result</b></td><td>No marks. One descriptor on the Junior Cycle Profile of Achievement: Exceptional, Above expectations, In line with expectations or Yet to meet expectations. It does not change the exam grade.</td></tr>
  </tbody></table></div>
  <p class="small" style="color:var(--muted)">Source: the NCCA's <a href="https://www.curriculumonline.ie/getmedia/e21d9e9d-cede-4b50-8377-9268f8cb7166/MFL_Assessment_Guidelines.pdf" target="_blank" rel="noopener">Junior Cycle MFL assessment guidelines ↗</a>. Always follow your teacher and your school's CBA calendar. More on CBAs: <a href="junior-cycle-cbas.html#spanish">CBAs explained</a>.</p>
</section>

<section id="listens">
  <h2>What your teacher listens for</h2>
  <p>Teachers use the official <b>Features of Quality</b>, which look at three things. In plain English:</p>
  <ol>
    <li><b>Speaking:</b> how clear you are, how well it flows, how accurate it is and how many different words and structures you use.</li>
    <li><b>Answering questions:</b> whether you understand the teacher's questions and give answers that make sense.</li>
    <li><b>How Spanish works:</b> verb endings, agreement, word order, and fixing your own slips.</li>
  </ol>
  <p><b>To move up a level:</b> speak from key words, not a script · use the present, past and future · give opinions with reasons (<em lang="es">porque…</em>) · answer in full sentences and add one detail · fix slips out loud (<em lang="es">fui… perdón, fuimos</em>) · ask for help in Spanish if you don't understand.</p>
</section>

<section id="formats">
  <h2>The four formats</h2>
  <ul>
    <li><b>Presentation</b> on a topic, with pictures, slides or props, then the teacher's questions. Ideas: your sport or hobby, a festival in a Spanish-speaking country compared with Ireland, a city you'd love to visit.</li>
    <li><b>Interview:</b> the teacher asks about you, your family, school, free time, holidays and plans. In pairs, you also ask each other.</li>
    <li><b>Role-play:</b> a real-life situation such as a hotel, a host family, a shop or a café, then questions.</li>
    <li><b>Conversation about a stimulus:</b> a picture, short text, video clip or object starts the conversation.</li>
  </ul>
  <p>Pick something you care about: it's easier to talk about, and easier to answer questions on.</p>
</section>

<section id="plan">
  <h2>A 3-week plan</h2>
  <ol>''' + pl + '''</ol>
</section>

<section id="model">
  <h2>Hear a model: an interview</h2>
  <p>Róisín, a 2nd year, answers her teacher's questions. Notice how every answer adds one more thing: a detail, a reason or a second sentence. Press <b>Play</b>, or tick the box to pause after each line and repeat it.</p>
  ''' + SETTINGS + '''
  <div class="au" id="interview" data-au="int1" data-n="16"><h3>Entrevista: mi vida (8 of the 12 questions)</h3><div class="meta">Róisín and her teacher</div></div>
  <p class="small" style="color:var(--muted)">Don't learn it off: your CBA topic has to be new. Answer the same questions about <b>yourself</b>.</p>
</section>

<section id="stuck">
  <h2>When you're stuck</h2>
  <p>Asking for help in Spanish is good interaction, not a failure.</p>
  <div class="table-wrap"><table><thead><tr><th>Say</th><th>It means</th></tr></thead><tbody>''' + sv + '''</tbody></table></div>
  <div class="au" data-au="surv"><h3>Hear the survival phrases</h3><div class="meta">Six phrases, said slowly</div></div>
  <p><b>Thinking words:</b> <em lang="es">''' + FILLERS + '''</em><br><b>Linking words:</b> <em lang="es">''' + LINKS + '''</em><br><b>Opinions:</b> <em lang="es">''' + OPINIONS + '''</em></p>
</section>

<section id="ladder">
  <h2>Climb the answer ladder</h2>
  <p>The same question answered three ways. Great answers add a detail, a reason, the past and the future.</p>
  <div class="au" data-au="lad"><h3 lang="es">''' + LADDERS[0][0] + '''</h3><div class="meta">Basic → good → great</div></div>
  <h3>Sounds to get right</h3>
  <ul>''' + pr + '''</ul>
  <p>Practise the sounds with <a href="sound-match.html">Sound Match</a>, and questions with <a href="question-quick-fire.html">Question Quick-Fire</a> and <a href="meet-and-greet.html">Meet &amp; Greet</a>. For a culture presentation, try <a href="fiesta-quiz.html">Fiesta Quiz</a>.</p>
</section>

<section id="check">
  <h2>Self-check before the day</h2>
  <ul>''' + ck + '''</ul>
  <p class="big"><b>The Léim Oral CBA Prep Pack (€6).</b> 16 printable pages: all four formats with six full models (two presentations, an interview, two role-plays and a picture conversation), the teacher's likely questions with good answers, a 48-question bank, answer ladders, pronunciation, a planning sheet and reflection help, with every model read aloud online.</p>
  <p style="margin-top:14px"><a class="btn" href="https://payhip.com/b/2K5MU" target="_blank" rel="noopener">Get the Oral CBA Prep Pack ↗</a></p>
</section>

<section id="parents">
  <h2>For parents: how to help (no Spanish needed)</h2>
  <ul>
    <li><b>Be the audience.</b> Let your child give the talk or do the interview with you, then ask two questions (read them from their notes as best you can).</li>
    <li><b>Time it:</b> about 3–4 minutes including questions.</li>
    <li><b>Help them plan the weeks:</b> research, a plan, then a practice run each day in week 3.</li>
    <li><b>Don't write it for them, and don't let AI write it.</b> It must be their own work, and teachers can tell.</li>
    <li><b>Keep it calm.</b> It's one line on the JCPA and it doesn't change the exam grade.</li>
  </ul>
  <p class="small" style="color:var(--muted)">All Spanish on this page is original Léim material, not official CBA material. Léim is independent and not connected to the NCCA or the State Examinations Commission. <a href="junior-cycle-spanish-exam-centre.html">Back to the Spanish Exam Centre</a>.</p>
</section>

</div></div>

</main>'''
fp = head('Junior Cycle Spanish speaking: the oral CBA explained, with models | Léim',
          'How the Junior Cycle Spanish oral CBA works: timing, the four formats, what the teacher listens for, a 3-week plan, survival phrases and a model interview you can listen to.') + free_main + FOOTER
fp = fp.replace('<script src="site.js"></script>', '<script src="site.js"></script>\n' + player_js(['int1', 'surv', 'lad']))
open(R + 'junior-cycle-spanish-speaking.html', 'w', encoding='utf-8').write(fp)
print('site pages ok')
