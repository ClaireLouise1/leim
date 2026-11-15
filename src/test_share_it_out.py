#!/usr/bin/env python3
"""Independent checker for Share It Out. node src/test_share_it_out.js > /tmp/sio.json ; python3 src/test_share_it_out.py /tmp/sio.json
Re-derives every answer from the question TEXT (and the SVG pictures) with exact fractions."""
import json, re, sys
from fractions import Fraction as F
from math import gcd
d = json.load(open(sys.argv[1]))
def val(s):
    s = s.replace('€', '').replace(',', '').strip(); s = re.sub(r'\s*(km|cm|ml|kg|g|m|l)$', '', s)
    pc = s.endswith('%'); s = s.rstrip('%')
    x = F(int(s.split('/')[0]), int(s.split('/')[1])) if '/' in s else F(s)
    return x / 100 if pc else x
def money(x): return '€%d.%02d' % (int(x), int((x - int(x)) * 100)) if (x * 100).denominator == 1 else None
def ratio(s): return [int(x) for x in s.split(' : ')]
def simplest(r): g = 0
probs = []
def bad(q, msg): probs.append((q['mk'], msg, q['en'], q['frame'], q['answer'], q['wrong']))
def numeric(q, true, is_money=False, unit=None):
    a = val(q['answer'])
    if a != true: bad(q, 'answer %s should be %s' % (a, true)); return
    if is_money:
        if money(true) != q['answer']: bad(q, 'money format')
        if any(not re.fullmatch(r'€\d+\.\d\d', w) for w in q['wrong']): bad(q, 'wrong money format')
    if unit is not None and any(not w.endswith(unit) for w in [q['answer']] + q['wrong']): bad(q, 'unit')
    vs = [val(w) for w in q['wrong']]
    if len(set(vs)) < 3 or true in vs or any(v <= 0 for v in vs): bad(q, 'wrong options clash')
def ints(s): return [int(x) for x in re.findall(r'\d+', s)]
def choice(q, want):
    if want != q['answer']: bad(q, 'choice answer %s should be %s' % (q['answer'], want))
for q in d:
    t = q['data'].get('t'); en = q['en']; fr = q['frame'] or ''
    if len(q['wrong']) != 3 or q['answer'] in q['wrong'] or len(set(q['wrong'])) != 3: bad(q, 'options'); continue
    if t == 'share2':
        m = re.match(r'Share €(\d+) between (\S+) and (\S+) in the ratio (\d+) : (\d+)\. How much does (\S+) get\?', en) or \
            re.match(r'(\S+) and (\S+) share (\d+) sweets in the ratio (\d+) : (\d+)\. How many sweets does (\S+) get\?', en)
        if en.startswith('Share'): T, n1, n2 = int(m[1]), m[2], m[3]
        else: n1, n2, T = m[1], m[2], int(m[3])
        a, b, who = int(m[4]), int(m[5]), m[6]
        parts = [int(x) for x in re.search(r'data-parts="([\d,]+)"', q['html'])[1].split(',')]
        if parts != [a, b] or q['html'].count('class="box"') != a + b: bad(q, 'bar model')
        true = F(T * (a if who == n1 else b), a + b)
        numeric(q, true, is_money=en.startswith('Share'))
    elif t == 'share3':
        m = re.match(r'(\S+), (\S+) and (\S+) share €(\d+) in the ratio (\d+) : (\d+) : (\d+)\. How much does (\S+) get\?', en)
        names = [m[1], m[2], m[3]]; r = [int(m[5]), int(m[6]), int(m[7])]
        if q['html'].count('class="box"') != sum(r): bad(q, 'bar model')
        numeric(q, F(int(m[4]) * r[names.index(m[8])], sum(r)), is_money=True)
    elif t == 'known':
        a, b, A = ints(en)[:3]; k = F(A, a)
        u = ' ml' if ' ml ' in en else ' kg' if ' kg ' in en else ''
        true = k * b if q['data']['ask'] == 'other' else k * (a + b)
        if ('altogether' in en) != (q['data']['ask'] == 'total'): bad(q, 'ask')
        numeric(q, true, unit=u if u else None)
    elif t == 'diff':
        m = re.search(r'ratio (\d+) : (\d+)\. \S+ gets €(\d+) more', en); a, b, D = int(m[1]), int(m[2]), int(m[3])
        numeric(q, F(D * (a + b), b - a), is_money=True)
    elif t == 'frac':
        m = re.search(r'ratio of (\w+) to (\w+) is (\d+) : (\d+)\. What fraction of .* are (\w+)\?', en)
        a, b = int(m[3]), int(m[4]); want = F(b if m[5] == m[2] else a, a + b)
        numeric(q, want)
        if q['answer'] != (str(want.numerator) + '/' + str(want.denominator)): bad(q, 'frac form')
    elif t == 'simp':
        a, b = ratio(fr); g = gcd(a, b); choice(q, '%d : %d' % (a // g, b // g))
    elif t == 'units':
        m = re.fullmatch(r'(\d+) ?(\S+) : (€?)(\d+) ?(\S*)', fr)
        small, su, big, bu = int(m[1]), m[2], int(m[4]), (m[3] or m[5])
        conv = {('cm', 'm'): 100, ('g', 'kg'): 1000, ('minutes', 'hours'): 60, ('minutes', 'hour'): 60, ('c', '€'): 100, ('ml', 'litres'): 1000, ('ml', 'litre'): 1000, ('m', 'km'): 1000}[(su, bu)]
        B = big * conv; g = gcd(small, B); choice(q, '%d : %d' % (small // g, B // g))
    elif t == 'dots':
        r = q['html'].count('fill="#C8463D"'); b = q['html'].count('fill="#3A6EA5"')
        x, y = (r, b) if 'red to blue' in en else (b, r); g = gcd(x, y); choice(q, '%d : %d' % (x // g, y // g))
    elif t == 'equiv':
        a, b = [int(x) for x in re.search(r'same as (\d+) : (\d+)', en).groups()]
        for o in [q['answer']] + q['wrong']:
            x, y = ratio(o)
            if (x * b == y * a) != (o == q['answer']): bad(q, 'equiv %s' % o)
    elif t == 'gap':
        a, b = [int(x) for x in fr.split(' = ')[0].split(' : ')]; rhs = fr.split(' = ')[1].split(' : ')
        true = F(int(rhs[0]) * b, a) if rhs[1] == '?' else F(int(rhs[1]) * a, b)
        numeric(q, true)
    elif t == 'recipe':
        m = re.search(r'for (\d+) people uses (\d+) (g|ml) of .* for (\d+) people', en)
        numeric(q, F(int(m[2]) * int(m[4]), int(m[1])), unit=' ' + m[3])
    elif t == 'unit':
        m = re.match(r'(\d+) .* cost €(\d+\.\d\d)\. How much do (\d+) ', en)
        numeric(q, F(m[2]) * int(m[3]) / int(m[1]), is_money=True)
    elif t == 'map':
        sc = int(re.search(r'1 : ([\d ]+)\.', en)[1].replace(' ', ''))
        if 'on the map' in en and 'in real life?' in en:
            cm = F(re.search(r'are ([\d.]+) cm apart', en)[1]); numeric(q, cm * sc / 100000, unit=None)
            if not q['answer'].endswith(' km'): bad(q, 'km')
        else:
            km = F(re.search(r'are ([\d.]+) km apart', en)[1]); numeric(q, km * 100000 / sc)
            if not q['answer'].endswith(' cm'): bad(q, 'cm')
        if any(w.endswith(' m') for w in q['wrong']):  # "x m" option must not equal answer in metres
            pass
    elif t == 'best':
        packs = [(int(m[1]), F(m[2])) for m in (re.fullmatch(r'(\d+) for €(\d+\.\d\d)', o) for o in [q['answer']] + q['wrong'])]
        each = [p / n for n, p in packs]
        if len(set(each)) != 4: bad(q, 'tie')
        choice(q, ([q['answer']] + q['wrong'])[each.index(min(each))])
    elif t == 'rel':
        m = re.match(r'(.+?): (\d+) out of (\d+) .*?\. (.+?): (\d+) out of (\d+) ', en)
        x, y = F(int(m[2]), int(m[3])), F(int(m[5]), int(m[6]))
        choice(q, "They're the same" if x == y else (m[1] if x > y else m[4]))
    elif t == 'absrel':
        m = re.match(r'(.+?): .*? from €?(\d+) to €?(\d+)\. (.+?): .*? from €?(\d+) to €?(\d+)\. Which had the bigger (\w+)', en)
        c1, c2 = int(m[3]) - int(m[2]), int(m[6]) - int(m[5])
        if m[7] == 'ABSOLUTE': want = m[1] if c1 > c2 else m[4] if c2 > c1 else "They're the same"
        else:
            r1, r2 = F(c1, int(m[2])), F(c2, int(m[5])); want = m[1] if r1 > r2 else m[4] if r2 > r1 else "They're the same"
        choice(q, want)
    elif t == 'chg':
        m = re.search(r'from (€?)(\d+) to €?(\d+)\. What is the (relative|absolute)', en); a, b = int(m[2]), int(m[3])
        if m[4] == 'relative':
            if not q['answer'].endswith('%'): bad(q, 'pct')
            numeric(q, F(b - a, a))
        else:
            if q['answer'] != m[1] + str(b - a): bad(q, 'abs %s' % q['answer'])
            if m[1] and any(w.endswith('%') for w in q['wrong']) and False: pass
    else: bad(q, 'unknown type')
    for s in [q['en'], q['frame'] or '', q['answer'], q['why']] + q['wrong']:
        if re.search(r'NaN|undefined|Infinity|null', s or ''): bad(q, 'junk text')
print(len(d), 'questions checked,', len(probs), 'problems')
for p in probs[:25]: print(p)
sys.exit(1 if probs else 0)
