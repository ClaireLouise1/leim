# Independent checker for Growth Spotter (quadratic & exponential patterns, Order 36).
# Reads the question TEXT only: the question line, the sequence in the question box,
# the table cells, or the tiles counted in each stage of the picture; then recomputes the answer.
# node src/test_growth_spotter.js > /tmp/gs.json ; python3 src/test_growth_spotter.py /tmp/gs.json
import json, re, sys, html as H
from fractions import Fraction
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
TR = standard_transformations + (implicit_multiplication_application,)
n = sp.Symbol('n', positive=True, integer=True)
SUBS = '₀₁₂₃₄₅₆₇₈₉'

def num(s): return Fraction(s.replace('−', '-'))
def rule(s):
    assert s.startswith('Tₙ = '), s
    e = s[5:].replace('−', '-').replace('ⁿ', '**n').replace('²', '**2').replace('³', '**3').replace('½', '(1/2)').replace('×', '*')
    return parse_expr(e, local_dict={'n': n}, transformations=TR)
def ev(r, k): return Fraction(str(sp.nsimplify(r.subs(n, k))))
def eqbox(h):
    m = re.findall(r'<p class="e" data-e="1">(.*?)</p>', h)
    return H.unescape(m[0]) if m else None
def seq(s):
    s = s.replace(', …', '')
    return [None if t == '?' else num(t) for t in s.split(', ')]
def tiles(h):
    out = []
    for g in re.findall(r'<g data-stage="(\d+)">(.*?)</g>', h):
        out.append((int(g[0]), g[1].count('<rect class="t"')))
    return out
def table(h):
    rows = re.findall(r'<tr>(.*?)</tr>', h)
    cells = [re.findall(r'<td>(.*?)</td>', r) for r in rows]
    return [int(x) for x in cells[0]], [num(x) for x in cells[1]]
def diffs(a): return [a[i+1] - a[i] for i in range(len(a) - 1)]
def kind(a):
    d = diffs(a)
    if len(set(d)) == 1: return 'Linear'
    if 0 not in a and len(set(a[i+1] / a[i] for i in range(len(a)-1))) == 1: return 'Exponential'
    if len(set(diffs(d))) == 1: return 'Quadratic'
    return None
def extend(a, k):
    """value of term k (1-based) of the pattern whose terms 1..len(a) are a"""
    t = kind(a)
    assert t, a
    if t == 'Exponential': return a[0] * (a[1] / a[0]) ** (k - 1)
    deg = 1 if t == 'Linear' else 2
    poly = sp.interpolate([(i + 1, sp.Rational(v.numerator, v.denominator)) for i, v in enumerate(a[:deg+1])], n)
    for i, v in enumerate(a): assert Fraction(str(poly.subs(n, i + 1))) == v
    return Fraction(str(poly.subs(n, k)))

def answer(q):
    en, h = q['en'], q['html']
    box = eqbox(h) if h else None
    if en == 'Linear, quadratic or exponential?':
        if box: return kind(seq(box))
        c = tiles(h); assert [s for s, _ in c] == [1, 2, 3, 4]
        return kind([Fraction(x) for _, x in c])
    if en in ('Next term?', 'Missing term?'):
        a = seq(box); g = a.index(None)
        if g == len(a) - 1: return extend(a[:-1], len(a))
        x = sp.Symbol('x'); b = [x if v is None else sp.Rational(v.numerator, v.denominator) for v in a]
        dd = diffs(diffs(b)); sol = sp.solve(sp.Eq(dd[0], dd[1]), x)
        assert len(sol) == 1 and all(sp.simplify(e.subs(x, sol[0]) - dd[0].subs(x, sol[0])) == 0 for e in dd)
        return Fraction(str(sol[0]))
    if en == '2nd difference?':
        dd = diffs(diffs(seq(box))); assert len(set(dd)) == 1; return dd[0]
    if en == '1st differences?':
        return ', '.join(str(d).replace('-', '−') for d in diffs(seq(box)))
    if en == 'Tₙ = an² + bn + c. Find a.':
        dd = diffs(diffs(seq(box))); assert len(set(dd)) == 1; return dd[0] / 2
    m = re.fullmatch(r'Find T([₀-₉]+)\.', en)
    if m:
        k = int(''.join(str(SUBS.index(c)) for c in m.group(1))); return ev(rule(box), k)
    m = re.fullmatch(r'Which term is (\d+)\?', en)
    if m:
        X = int(m.group(1)); r = rule(box)
        sols = [s for s in sp.solve(sp.Eq(r, X), n) if s.is_integer and s > 0]
        assert len(sols) == 1, (en, box, sols); return Fraction(int(sols[0]))
    m = re.fullmatch(r'Tiles in stage (\d+)\?', en)
    if m:
        c = tiles(h); assert [s for s, _ in c] == [1, 2, 3, 4]
        return extend([Fraction(x) for _, x in c], int(m.group(1)))
    m = re.fullmatch(r'\S+ \w+ (double|triple) every (\w+)\. Start: (\d+)\. After (\d+) (\w+)s\?', en)
    if m:
        assert m.group(2) == m.group(5)
        return Fraction(int(m.group(3)) * (2 if m.group(1) == 'double' else 3) ** int(m.group(4)))
    m = re.fullmatch(r'\S+ \w+ (double|triple) every (\w+)\. Start: (\d+)\. First (\w+) over (\d+)\?', en)
    if m:
        r = 2 if m.group(1) == 'double' else 3; v = int(m.group(3)); k = 0
        while v <= int(m.group(5)): v *= r; k += 1
        return Fraction(k)
    if en == 'Which rule?':
        if '<table' in h:
            ks, vs = table(h); return ('table', list(zip(ks, vs)))
        if box: return ('table', [(i + 1, v) for i, v in enumerate(seq(box))])
        c = tiles(h); return ('table', [(s, Fraction(x)) for s, x in c])
    raise Exception('unknown question: ' + en)

def main():
    Q = json.load(open(sys.argv[1]))
    bad = 0; per = {}
    for q in Q:
        per[q['mk']] = per.get(q['mk'], 0) + 1
        opts = [q['answer']] + q['wrong']
        try:
            assert len(q['wrong']) == (2 if q['en'] == 'Linear, quadratic or exponential?' else 3), 'only %d wrong options' % len(q['wrong'])
            assert len(set(opts)) == len(opts), 'duplicate options'
            for o in opts: assert '-' not in o and 'NaN' not in o and 'undefined' not in o, 'bad option ' + o
            a = answer(q)
            if isinstance(a, tuple):
                pts = a[1]; assert len(pts) >= 4
                fits = [o for o in opts if all(ev(rule(o), k) == v for k, v in pts)]
                assert fits == [q['answer']], ('rule fits', fits)
            elif isinstance(a, str):
                assert q['answer'] == a, (a, q['answer'])
            else:
                assert num(q['answer']) == a, ('answer', a, q['answer'])
                for w in q['wrong']: assert num(w) != a, 'wrong equals answer'
            if q['en'] == '1st differences?':
                for w in q['wrong']: assert w != a
        except Exception as e:
            bad += 1
            if bad <= 12: print('PROBLEM', q['mode'], q['mk'], q['en'], eqbox(q['html']) if q['html'] else '', q['answer'], q['wrong'], repr(e)[:300])
    print(len(Q), 'questions,', bad, 'problems;', per)
    sys.exit(1 if bad else 0)
main()
