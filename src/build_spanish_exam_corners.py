#!/usr/bin/env python3
"""Put an Exam corner on JC Spanish game pages (data: src/spanish_exam_corner_data.py).

  python3 src/build_spanish_exam_corners.py            # every slug in CORNERS
  python3 src/build_spanish_exam_corners.py <slug>...  # just these

Safe to re-run: the corner sits between <!--sec--> and <!--/sec--> just before the
rules panel's "Back to the game" buttons; styles and the audio player sit between
<!--secjs--> markers before </body>. Listening tasks are read aloud with the player
from src/build_oral_cba.py (copied from that file's source, not imported, because
importing it rebuilds the oral pages). Runs free_first at the end.
"""
import ast, html, json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from spanish_exam_corner_data import CORNERS
import came_up_data as D

ROOT = os.path.join(os.path.dirname(__file__), '..')
# Spanish tracker row - 1 = the order number used in came_up_data.py
ORDER = {'meet-and-greet': 1}   # add each new slug: its Spanish tracker row minus 1


def _player():
    src = open(os.path.join(os.path.dirname(__file__), 'build_oral_cba.py'), encoding='utf-8').read()
    out = {}
    for node in ast.parse(src).body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and getattr(node.targets[0], 'id', '') in ('PLAYER_CSS', 'PLAYER_JS', 'SETTINGS'):
            out[node.targets[0].id] = ast.literal_eval(node.value)
    return out['PLAYER_CSS'], out['PLAYER_JS'], out['SETTINGS']


CSS = ('.exam{margin-top:30px;border:2px solid var(--night);border-radius:14px;padding:22px}'
       '.exam h3{margin-top:18px}.eq li{margin:14px 0;font-size:16px}'
       '.eq details{margin-top:8px;background:var(--green-soft);border-radius:8px;padding:8px 12px;border:0}'
       '.eq details summary{font-size:15px;color:var(--green-dark);cursor:pointer;font-weight:700}'
       '.eq details p{color:var(--ink);margin-top:6px}'
       '.pass{background:#fff;border-left:4px solid var(--night);padding:10px 14px;border-radius:8px;margin:8px 0}'
       '.pass .sp{display:block;margin:4px 0}.exq{margin:6px 0 0 22px}.exq li{margin:4px 0!important;font-size:16px}')


def corner(slug, c):
    t = []
    t.append('<!--sec--><div class="exam" id="exam" style="scroll-margin-top:90px">')
    t.append('<span class="pill" style="background:var(--night);color:#fff">Exam corner</span>')
    t.append('<h3 style="font-size:21px;margin:12px 0 8px">Where this shows up in the exam</h3>')
    t.append('<p>%s</p>' % c['where'])
    t.append('<h3 style="font-size:19px;margin:18px 0 8px">How marks are won and lost</h3><ul>%s</ul>' % ''.join('<li>%s</li>' % x for x in c['tips']))
    t.append('<h3 style="font-size:19px;margin:18px 0 8px">Try these exam-style questions</h3>')
    t.append('<p style="color:var(--muted);font-size:15px">Written by Léim in the style of the exam (not taken from past papers). '
             'The people, places and texts are made up. Press ▶ Play to hear the listening (your browser reads the Spanish; play it twice, like the exam). '
             '"Where the marks would go" is our guide, not an official marking scheme.</p>')
    t.append('<ol class="eq">')
    for i, k in enumerate(c['tasks']):
        t.append('<li><b>%s.</b> %s' % (k['title'], k['q']))
        if k['kind'] == 'listen':
            n = len(k['audio']['lines'])
            t.append('<div class="au" data-au="%s-%d" data-n="%d"><div class="meta">%s</div></div>' % (slug, i, n, ' and '.join(k['audio']['who'])))
        elif k['kind'] == 'read':
            t.append('<div class="pass" lang="es">%s</div>' % k['text'])
        if k['qs']:
            t.append('<ol type="a" class="exq">%s</ol>' % ''.join('<li>%s</li>' % q for q in k['qs']))
        t.append('<details><summary>Show a model answer</summary><p>%s<br><i>Where the marks would go:</i> %s</p></details></li>' % (k['model'], k['marks']))
    t.append('</ol>')
    line = D.came_line('spanish', ORDER[slug]) if slug in ORDER else None
    if line:
        t.append('<p class="came" style="font-size:14px;color:var(--muted);margin-top:10px"><b>Came up in:</b> %s (%s) See the '
                 '<a href="%s" target="_blank" rel="noopener">past papers ↗</a>.</p>' % (html.escape(line, quote=False), D.KEYS['spanish'], D.ARCHIVE))
    t.append('</div><!--/sec-->')
    return '\n'.join(t)


def audio_data(slug, c):
    return {'%s-%d' % (slug, i): {'who': k['audio']['who'], 'lines': k['audio']['lines']}
            for i, k in enumerate(c['tasks']) if k['kind'] == 'listen'}


def build(slug):
    c = CORNERS[slug]
    p = os.path.join(ROOT, slug + '.html')
    s = open(p, encoding='utf-8').read()
    s = re.sub(r'<!--sec-->.*?<!--/sec-->\n?', '', s, flags=re.S)
    s = re.sub(r'<!--secjs-->.*?<!--/secjs-->\n?', '', s, flags=re.S)
    m = re.search(r'id="revise".*?(\n\s*<div class="actions"><a class="btn" href="#game">)', s, flags=re.S)
    assert m, slug + ': no rules panel actions row'
    pcss, pjs, settings = _player()
    data = audio_data(slug, c)
    for it in data.values():
        for L in it['lines']:
            assert '<' not in L[1] and L[0] < len(it['who']), (slug, L)
    block = corner(slug, c)
    if data:
        block = block.replace('<ol class="eq">', settings + '\n<ol class="eq">', 1)
    s = s[:m.start(1)] + '\n' + block + s[m.start(1):]
    js = '<!--secjs--><style>%s%s</style>' % (CSS, pcss.replace('\n', ''))
    if data:
        js += pjs.replace('__DATA__', json.dumps(data, ensure_ascii=False))
    js += '<!--/secjs-->\n'
    i = s.rfind('</body>')
    s = s[:i] + js + s[i:]
    open(p, 'w', encoding='utf-8').write(s)
    print('exam corner:', slug, '(%d tasks, %d with audio)' % (len(c['tasks']), len(data)))


if __name__ == '__main__':
    for slug in (sys.argv[1:] or list(CORNERS)):
        build(slug)
    import free_first
    free_first.hide_all()
