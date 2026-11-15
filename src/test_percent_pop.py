#!/usr/bin/env python3
"""Independent checker for Percent Pop. node src/test_percent_pop.js > /tmp/pp.json ; python3 src/test_percent_pop.py /tmp/pp.json
Re-derives every answer from the question TEXT (and the SVG picture) with exact fractions."""
import json, re, sys
from fractions import Fraction as F
d = json.load(open(sys.argv[1]))
def val(s):
    s = s.replace('€', '').replace(',', '').strip(); pc = s.endswith('%'); s = s.rstrip('%')
    x = F(int(s.split('/')[0]), int(s.split('/')[1])) if '/' in s else F(s)
    return x / 100 if pc else x
def money(x):  # exact €x.xx
    return '€%d.%02d' % (int(x), round((x - int(x)) * 100)) if (x * 100).denominator == 1 else None
probs = []
def bad(q, msg): probs.append((q['mk'], msg, q['en'], q['frame'], q['answer'], q['wrong']))
def numeric(q, true, simplest=False, is_money=False):
    a = val(q['answer'])
    if a != true: bad(q, 'answer %s should be %s' % (a, true)); return
    if is_money and money(true) != q['answer']: bad(q, 'money format')
    if simplest and '/' in q['answer']:
        t, b = map(int, q['answer'].split('/'))
        if F(t, b).numerator != t: bad(q, 'not simplest')
    vs = [val(w) for w in q['wrong']]
    if len(set(vs)) < 3 or true in vs or any(v <= 0 for v in vs): bad(q, 'wrong options clash')
    if is_money and any(not re.fullmatch(r'€\d+\.\d\d', w) for w in q['wrong']): bad(q, 'wrong money format')
for q in d:
    t = q['data'].get('t'); txt = q['en'] + ' ' + (q['frame'] or ''); fr = q['frame'] or ''
    if len(q['wrong']) != 3 or q['answer'] in q['wrong']: bad(q, 'options'); continue
    if t == 'f2p': numeric(q, val(fr)) if q['answer'].endswith('%') else bad(q, 'not %')
    elif t == 'd2p': numeric(q, val(fr)) if q['answer'].endswith('%') else bad(q, 'not %')
    elif t == 'p2d': numeric(q, val(fr)) if re.fullmatch(r'\d*\.?\d+', q['answer']) else bad(q, 'not decimal')
    elif t == 'p2f':
        if '/' not in q['answer']: bad(q, 'not fraction')
        numeric(q, val(fr), simplest=True)
    elif t == 'grid':
        n = len(re.findall(r'fill="#F6CF5A"', q['html']))
        if 'percentage' in q['en'] and not q['answer'].endswith('%'): bad(q, 'grid kind')
        if 'decimal' in q['en'] and not re.fullmatch(r'0\.\d+', q['answer']): bad(q, 'grid kind')
        numeric(q, F(n, 100), simplest='simplest' in q['en'])
    elif t == 'order':
        opts = [o for o in re.split(r'\s{3}', fr) if o]
        vals = [val(o) for o in opts]
        if len(set(vals)) != 4 or sorted(opts) != sorted([q['answer']] + q['wrong']): bad(q, 'order opts'); continue
        want = opts[vals.index(max(vals) if 'biggest' in q['en'] else min(vals))]
        if want != q['answer']: bad(q, 'order answer')
    elif t == 'of':
        m = re.fullmatch(r'(\d+)% of (€?)(\d+)', fr); true = F(int(m[1]) * int(m[3]), 100)
        numeric(q, true, is_money=bool(m[2]))
    elif t == 'build':
        m = re.match(r'10% of (\d+) is ([\d.]+)\. Use that to find (\d+)% of (\d+)\.', q['en'])
        if F(m[2]) != F(int(m[1]), 10) or m[1] != m[4]: bad(q, 'build stem')
        numeric(q, F(int(m[3]) * int(m[4]), 100))
    elif t == 'aspct':
        a, b = map(int, re.findall(r'\d+', q['en'])[:2]); numeric(q, F(a, b))
    elif t == 'swap':
        A, B = re.split(r'\s+or\s+', fr)
        ev = lambda e: F(int(re.match(r'(\d+)% of (\d+)', e)[1]) * int(re.match(r'(\d+)% of (\d+)', e)[2]), 100)
        want = "They're the same" if ev(A) == ev(B) else (A if ev(A) > ev(B) else B)
        if want != q['answer']: bad(q, 'swap')
    elif t == 'sale':
        texts = re.findall(r'>([^<]+)</text>', q['html'])
        P = F(next(x for x in texts if x.startswith('€'))[1:]); dd = int(re.match(r'(\d+)% OFF', next(x for x in texts if 'OFF' in x))[1])
        numeric(q, P * (100 - dd) / 100, is_money=True)
    elif t == 'inc':
        m = re.search(r'€(\d+).*?by (\d+)%', q['en']); numeric(q, int(m[1]) * F(100 + int(m[2]), 100), is_money=True)
    elif t == 'mult':
        m = re.search(r'(increase|decrease) an amount by (\d+)%', q['en']); k = int(m[2])
        numeric(q, F(100 + k if m[1] == 'increase' else 100 - k, 100))
    elif t == 'chg':
        m = re.search(r'from €(\d+) to €(\d+)\. What is the percentage (increase|decrease)', q['en'])
        o, n = int(m[1]), int(m[2])
        if (n > o) != (m[3] == 'increase'): bad(q, 'direction')
        numeric(q, F(abs(n - o), o))
    elif t == 'best':
        def fin(s):
            m = re.fullmatch(r'(\d+)% off €(\d+)', s)
            if m: return int(m[2]) * F(100 - int(m[1]), 100)
            m = re.fullmatch(r'€(\d+) off €(\d+)', s)
            if m: return F(int(m[2]) - int(m[1]))
            return F(int(re.fullmatch(r'€(\d+) \(no sale\)', s)[1]))
        opts = [q['answer']] + q['wrong']; fs = [fin(o) for o in opts]
        if len(set(fs)) != 4 or fs[0] != min(fs) or min(fs) <= 0: bad(q, 'best')
    elif t == 'revdown':
        m = re.match(r'After (\d+)% off, .* costs €([\d.]+)\.', q['en']); numeric(q, F(m[2]) / F(100 - int(m[1]), 100), is_money=True)
    elif t == 'revup':
        m = re.match(r'After a (\d+)% increase, .* costs €([\d.]+)\.', q['en']); numeric(q, F(m[2]) / F(100 + int(m[1]), 100), is_money=True)
    elif t == 'part':
        p = int(re.search(r'(\d+)%', q['en'])[1]); x = int(re.search(r'(?<![\d.])(\d+)(?![\d%])', q['en'])[1])
        true = F(x * 100, p)
        if true.denominator != 1: bad(q, 'part not whole')
        numeric(q, true)
    elif t == 'which':
        m = re.match(r'A price (was cut|went up) by (\d+)% and it\'s now €([\d.]+)\.', q['en'])
        orig = F(m[3]) / (F(100 - int(m[2]), 100) if m[1] == 'was cut' else F(100 + int(m[2]), 100))
        def ev(e):
            a, op, b = e.split(' '); a, b = F(a), F(b)
            return {'÷': a / b, '×': a * b, '+': a + b, '−': a - b}[op]
        good = [o for o in [q['answer']] + q['wrong'] if ev(o) == orig]
        if good != [q['answer']]: bad(q, 'which')
    else: bad(q, 'unknown type')
print(len(d), 'questions checked,', len(probs), 'problems')
for p in probs[:15]: print(p)
sys.exit(1 if probs else 0)
