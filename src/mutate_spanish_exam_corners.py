#!/usr/bin/env python3
"""Mutation check for src/test_spanish_exam_corners.py: plant one mistake at a time
(in a copy of the data / page, nothing is written) and make sure the checker catches it."""
import copy, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from spanish_exam_corner_data import CORNERS
from test_spanish_exam_corners import check, ROOT

pages = {s: open(os.path.join(ROOT, s + '.html'), encoding='utf-8').read() for s in CORNERS}
slug = next(iter(CORNERS))


def first(kind):
    return next(i for i, k in enumerate(CORNERS[slug]['tasks']) if k['kind'] == kind)


def m_data(f):
    def run():
        c = copy.deepcopy(CORNERS); f(c[slug]); return check(c, pages)
    return run


def m_page(f):
    def run():
        p = dict(pages); p[slug] = f(p[slug]); return check(CORNERS, p)
    return run


L, R, W = first('listen'), first('read'), first('write')
def set_line(c, txt): c['tasks'][L]['audio']['lines'][0][1] = txt
MUTANTS = {
    'missing accent in audio (habitacion)': m_data(lambda c: set_line(c, 'Su habitacion es la número catorce.')),
    'typo in audio (reserba)': m_data(lambda c: set_line(c, 'Tengo una reserba para tres noches.')),
    'wrong verb form (venieron)': m_data(lambda c: set_line(c, 'Mis amigos venieron ayer.')),
    'typo in reading text (profesorra)': m_data(lambda c: c['tasks'][R].__setitem__('text', c['tasks'][R]['text'].replace('profesora', 'profesorra'))),
    'missing ñ in model (pequeno)': m_data(lambda c: c['tasks'][W].__setitem__('model', c['tasks'][W]['model'].replace('Soy simpático', 'Soy pequeno'))),
    'HTML in audio line': m_data(lambda c: set_line(c, 'Hola, <b>Javier</b>.')),
    'speaker index out of range': m_data(lambda c: c['tasks'][L]['audio']['lines'].append([5, 'Hola.'])),
    'answer (d) missing from model': m_data(lambda c: c['tasks'][L].__setitem__('model', c['tasks'][L]['model'].replace('(d)', ''))),
    'extra question with no answer': m_data(lambda c: c['tasks'][R]['qs'].append('Extra?')),
    'no marks guide': m_data(lambda c: c['tasks'][R].__setitem__('marks', '')),
    'answer number not in audio (14 → catorce removed)': m_data(lambda c: [x.__setitem__(1, x[1].replace('catorce', 'doce')) for x in c['tasks'][L]['audio']['lines']]),
    'corner twice on page': m_page(lambda s: s.replace('<!--sec-->', '<!--sec--><div id="exam"></div><!--sec-->', 1)),
    'audio box with no player data': m_page(lambda s: s.replace('data-au="%s-%d"' % (slug, L), 'data-au="nope"')),
    'Payhip link in corner': m_page(lambda s: s.replace('</ol>\n</div><!--/sec-->', '</ol><a href="https://payhip.com/b/x">x</a>\n</div><!--/sec-->')),
    'unclosed tag in corner': m_page(lambda s: s.replace('<!--/sec-->', '<div><!--/sec-->', 1)),
    'speed control missing': m_page(lambda s: s.replace('id="auRate"', 'id="auRateX"')),
}

caught = 0
for name, run in MUTANTS.items():
    p = run()
    ok = bool(p)
    caught += ok
    print(('✓ caught: ' if ok else '✗ MISSED: ') + name + ('' if not ok else '  → ' + p[0][:90]))
print(f'{caught}/{len(MUTANTS)} caught')
sys.exit(0 if caught == len(MUTANTS) else 1)
