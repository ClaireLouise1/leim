# Independent checker for Graph Match (functions & graphs). Reads the question TEXT and HTML only:
# graphs are MEASURED from the SVG polylines, mapping diagrams from the arrow positions, tables from the cells.
# node src/test_graph_match.js > /tmp/gm.json ; python3 src/test_graph_match.py /tmp/gm.json
import json, re, sys, html as H, math
from collections import Counter
from fractions import Fraction as Fr
import numpy as np
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
X, K = sp.symbols('x k')
TR = standard_transformations + (implicit_multiplication_application,)
MINUS = '−'
def P(s):
    s = s.replace('−', '-').replace('²', '**2').replace('×', '*')
    s = re.sub(r'(\d)ˣ', r'(\1**x)', s)
    return parse_expr(s, local_dict={'x': X, 'k': K}, transformations=TR)
def num(s): return Fr(s.replace('−', '-').strip())
def attrs(tag): return dict(re.findall(r'([\w-]+)="([^"]*)"', tag))
def txt(s): return H.unescape(re.sub('<[^>]+>', '', s)).strip()
def eqbox(h): return [txt(m) for m in re.findall(r'<p class="e"[^>]*>(.*?)</p>', h)]
def rhs(box):  # "f(x) = 3x − 2" → sympy expr
    m = re.fullmatch(r'\w\(x\) = (.+)', box); assert m, box; return P(m.group(1))
def xset(opt):
    out = []
    for p in opt.split(' or '):
        m = re.fullmatch(r'x = (−?\d+)', p.strip())
        if not m: raise ValueError('bad x option ' + opt)
        out.append(num(m.group(1)))
    if len(set(out)) != len(out) or out != sorted(out): raise ValueError('order/repeat ' + opt)
    return set(out)
def ptv(opt):
    m = re.fullmatch(r'\((−?\d+), (−?\d+)\)', opt); assert m, opt; return (num(m.group(1)), num(m.group(2)))
def val(e, x): return Fr(str(sp.nsimplify(e.subs(X, x))))

# ---------- graph reader ----------
def read_graphs(h):
    out = []
    for m in re.finditer(r'<svg class="tg"([^>]*)>(.*?)</svg>', h, re.S):
        a = attrs(m.group(1)); body = m.group(2)
        x0, x1, y0, y1 = (float(a[k]) for k in ('data-x0', 'data-x1', 'data-y0', 'data-y1'))
        sx, sy, pl, pt = (float(a[k]) for k in ('data-sx', 'data-sy', 'data-pl', 'data-pt'))
        GX = lambda p: x0 + (p - pl) / sx; GY = lambda p: y1 - (p - pt) / sy
        for v, xp in re.findall(r'<text class="tk" data-v="(-?[\d.]+)" x="([\d.]+)"', body): assert abs(GX(float(xp)) - float(v)) < .02, 'x tick'
        for v, yp in re.findall(r'<text class="tk" data-w="(-?[\d.]+)" x="[\d.]+" y="([\d.]+)"', body): assert abs(GY(float(yp) - 3.5) - float(v)) < .02, 'y tick'
        labs = [txt(t) for t in re.findall(r'<text class="axl"[^>]*>(.*?)</text>', body)]
        g = {'box': (x0, x1, y0, y1), 'xl': labs[0], 'yl': labs[1], 'curves': {}, 'gly': sorted(set(round(GY(float(y)), 6) for y in re.findall(r'<line class="gl" x1="[\d.]+" y1="([\d.]+)" x2="[\d.]+" y2="\1"', body)))}
        for tag in re.findall(r'<polyline class="cv[^"]*"[^>]*>', body):
            t = attrs(tag); pts = [tuple(map(float, q.split(','))) for q in t['points'].split()]
            P2 = [(GX(p), GY(q)) for p, q in pts]; vis = [(x, y) for x, y in P2 if y0 - 1e-6 <= y <= y1 + 1e-6 and x0 - 1e-6 <= x <= x1 + 1e-6]
            assert len(vis) >= 10, 'curve hardly visible'
            n = t['data-n']
            if n: assert re.search(r'<text class="lnl[^"]*"[^>]*>' + re.escape(n) + '</text>', body), 'label missing'
            g['curves'][n] = fit(vis)
        out.append(g)
    return out
def fit(vis):
    xs = np.array([p[0] for p in vis]); ys = np.array([p[1] for p in vis])
    best = None
    for deg in (1, 2):
        c = np.polyfit(xs, ys, deg); r = np.max(np.abs(np.polyval(c, xs) - ys))
        if r < 0.01:
            cs = [Fr(v).limit_denominator(4) for v in c]
            e = sum(sp.Rational(cf.numerator, cf.denominator) * X ** (deg - i) for i, cf in enumerate(cs))
            assert max(abs(float(e.subs(X, x)) - y) for x, y in vis) < 0.01
            return ('linear' if deg == 1 or cs[0] == 0 else 'quadratic', sp.expand(e))
    assert all(ys > 0), 'not a polynomial and not positive'
    c = np.polyfit(xs, np.log(ys), 1); b = Fr(math.exp(c[0])).limit_denominator(4); a = Fr(math.exp(c[1])).limit_denominator(4)
    e = sp.Rational(a.numerator, a.denominator) * sp.Rational(b.numerator, b.denominator) ** X
    assert max(abs(float(e.subs(X, x)) - y) for x, y in vis) < 0.01, 'exp fit'
    return ('exponential', e)
def iroots(e, c=0):
    r = sp.solve(sp.Eq(e, c), X); assert all(v.is_real for v in r), 'complex'
    for v in r: assert v.is_integer, 'root off the grid ' + str(r)
    return set(Fr(int(v)) for v in r)

# ---------- mapping diagrams ----------
def read_maps(h):
    out = []
    for m in re.finditer(r'<svg class="mp"([^>]*)>(.*?)</svg>', h, re.S):
        a = attrs(m.group(1)); b = m.group(2)
        ins = [(float(y) - 5, int(v.replace('−', '-'))) for y, v in re.findall(r'<text class="mi" x="38" y="([\d.]+)"[^>]*>(−?\d+)</text>', b)]
        outs = [(float(y) - 5, int(v.replace('−', '-'))) for y, v in re.findall(r'<text class="mo" x="112" y="([\d.]+)"[^>]*>(−?\d+)</text>', b)]
        pairs = []
        for tag in re.findall(r'<line class="ar"[^>]*>', b):
            t = attrs(tag); ya, yb = float(t['y1']), float(t['y2'])
            i = [v for y, v in ins if abs(y - ya) < .3]; o = [v for y, v in outs if abs(y - yb) < .3]
            assert len(i) == 1 and len(o) == 1, 'arrow not on a number'; pairs.append((i[0], o[0]))
        assert len(set(v for _, v in ins)) == len(ins) and len(set(v for _, v in outs)) == len(outs), 'repeated number'
        out.append((a.get('data-l', ''), [v for _, v in ins], pairs))
    return out
def is_fn(ins, pairs): return all(len(set(o for i, o in pairs if i == v)) == 1 for v in ins)

# ---------- sketches ----------
def shape_of(svgbody):
    t = re.search(r'<polyline class="cv[^"]*" points="([^"]+)"', svgbody).group(1)
    P2 = [tuple(map(float, q.split(','))) for q in t.split()]
    v = [-q for _, q in P2]; d = [b - a for a, b in zip(v, v[1:])]; dd = [b - a for a, b in zip(d, d[1:])]
    if all(abs(x) < 1e-6 for x in d): return 'flat'
    if all(x > 0 for x in d): return 'up' if all(abs(x) < .02 for x in dd) else ('exp' if all(x > -.02 for x in dd) else '?')
    if all(x < 0 for x in d): return 'down' if all(abs(x) < .02 for x in dd) else '?'
    i = v.index(max(v)); j = v.index(min(v))
    if 0 < i < len(v) - 1 and all(x > -1e-9 for x in d[:i]) and all(x < 1e-9 for x in d[i:]): return 'hill'
    if 0 < j < len(v) - 1 and all(x < 1e-9 for x in d[:j]) and all(x > -1e-9 for x in d[j:]): return 'valley'
    return '?'
def read_sk(h): return [(attrs(m.group(1)).get('data-l', ''), shape_of(m.group(2))) for m in re.finditer(r'<svg class="sk"([^>]*)>(.*?)</svg>', h, re.S)]
# the checker's own idea of what each story looks like (by emoji)
STORY = {'🚕': 'up', '🛁': 'up', '🔋': 'down', '🕯': 'down', '⛽': 'down', '🅿': 'flat', '🚗': 'flat', '⚽': 'hill', '🐬': 'hill', '🤿': 'valley', '🛩': 'valley', '🦠': 'exp', '📲': 'exp'}
def story_shape(s):
    k = [v for e, v in STORY.items() if s.startswith(e)]; assert len(k) == 1, 'story ' + s; return k[0]

def read_table(h):
    rows = re.findall(r'<tr>(.*?)</tr>', re.search(r'<table class="ft">(.*?)</table>', h, re.S).group(1))
    cells = [[txt(c) for c in re.findall(r'<td>(.*?)</td>', r)] for r in rows]
    return [num(c) for c in cells[0]], [num(c) for c in cells[1]]
def classify_table(xs, ys):
    d = [b - a for a, b in zip(ys, ys[1:])]; dd = [b - a for a, b in zip(d, d[1:])]
    if len(set(d)) == 1: return 'Linear'
    if len(set(dd)) == 1: return 'Quadratic'
    if 0 not in ys and len(set(b / a for a, b in zip(ys, ys[1:]))) == 1: return 'Exponential'
    return '?'
def classify_expr(e):
    if X in e.free_symbols and any(X in a.free_symbols for a in e.atoms(sp.Pow) if a.exp.has(X)): return 'Exponential'
    d = sp.degree(sp.expand(e), X); return {1: 'Linear', 2: 'Quadratic'}.get(d, '?')
def fopt(s):
    m = re.fullmatch(r'f\(x\) = (.+)', s); assert m, s; return P(m.group(1))

bad = []
def flag(q, msg): bad.append((q['mk'], msg, q['en'], q['answer'], q['wrong']))
TEXT_BAD = [(r'(?<![\w(])1x', '1x'), (r'\+ −', '+ −'), (r'−0(?![.\d])', '−0'), (r'(?<![\d.])0x', '0x'), (r'\b(\w+) \1\b', 'doubled word'), (r'(?<=[\s(])-\d', 'ASCII minus'), (r'\bNaN|undefined', 'NaN')]
def unit(s, u):
    m = re.fullmatch(r'(−?\d+(?:\.\d+)?) ' + u, s); assert m, (s, u); return num(m.group(1))

def check(q):
    t = q['data'].get('t'); en = q['en']; A = q['answer']; W = q['wrong']; h = q['html']
    for vis in [en, A, q['why']] + W + eqbox(h):
        for pat, name in TEXT_BAD:
            if re.search(pat, vis): flag(q, 'text: ' + name)
    n3 = bool(q['data'].get('n3'))
    if len(W) != (2 if n3 else 3) or len(set(W + [A])) != len(W) + 1: flag(q, 'options'); return
    if en.startswith('Higher Level: ') != bool(q['data'].get('hl')): flag(q, 'HL label')
    O = [A] + W
    if t in ('eval', 'evalexp'):
        e = rhs(eqbox(h)[0]); k = num(re.fullmatch(r'(?:Higher Level: )?Find \w\((−?\d+)\)\.', en).group(1))
        v = val(e, k); assert num(A) == v, 'eval'; assert all(num(w) != v for w in W)
        if t == 'evalexp': assert classify_expr(e) == 'Exponential'
    elif t == 'solvef':
        e = rhs(eqbox(h)[0]); k = num(re.fullmatch(r'f\(x\) = (−?\d+)\. Find x\.', en).group(1))
        s = sp.solve(sp.Eq(e, k), X); assert len(s) == 1 and Fr(str(s[0])) == num(A), 'solvef'
        assert all(val(e, num(w)) != k for w in W)
    elif t == 'ongraph':
        e = rhs(eqbox(h)[0]); x, y = ptv(A); assert val(e, x) == y
        for w in W: x, y = ptv(w); assert val(e, x) != y, 'wrong point on graph'
    elif t == 'notfn':
        D = read_maps(h); assert len(D) == 4 and [d[0] for d in D] == list('ABCD')
        for l, ins, pairs in D: assert set(i for i, _ in pairs) == set(ins), 'input with no arrow'
        nf = [l for l, ins, pairs in D if not is_fn(ins, pairs)]; assert nf == [A], 'notfn ' + str(nf)
    elif t == 'maprule':
        (l, ins, pairs), = read_maps(h); assert is_fn(ins, pairs) and len(pairs) == len(ins)
        assert all(val(fopt(A), i) == o for i, o in pairs), 'rule'
        for w in W: assert not all(val(fopt(w), i) == o for i, o in pairs), 'wrong rule fits'
    elif t == 'findk':
        e = rhs(eqbox(h)[0]); m = re.fullmatch(r'Higher Level: f\((−?\d+)\) = (−?\d+)\. Find k\.', en)
        s = sp.solve(sp.Eq(e.subs(X, int(num(m.group(1)))), int(num(m.group(2)))), K); assert len(s) == 1 and num(A) == Fr(str(s[0]))
        assert all(num(w) != Fr(str(s[0])) for w in W)
    elif t in ('roots', 'turn', 'readval', 'solvek', 'whichf', 'meet', 'classg'):
        g, = read_graphs(h); x0, x1, y0, y1 = g['box']
        if t == 'meet':
            (kf, f), (kg, gg) = g['curves']['f'], g['curves']['g']; assert kf == 'quadratic' and kg == 'linear'
            S = iroots(f - gg); assert S == xset(A), 'meet'
            for x in S: assert y0 < float(f.subs(X, x)) < y1, 'meeting point off the grid'
            assert all(xset(w) != S for w in W); return
        kind, f = g['curves']['f']
        if t == 'classg': assert A == kind.capitalize(), ('classg', kind); return
        assert kind == 'quadratic'
        if t in ('roots', 'whichf'):
            S = iroots(f); assert len(S) == 2 and all(x0 < x < x1 for x in S)
            if t == 'roots': assert xset(A) == S and all(xset(w) != S for w in W)
            else:
                assert sp.expand(fopt(A) - f) == 0, 'whichf'
                for w in W: assert sp.expand(fopt(w) - f) != 0
        elif t == 'turn':
            a = sp.Poly(f, X).all_coeffs()[0]; hx = sp.solve(sp.diff(f, X), X)[0]; ky = f.subs(X, hx)
            assert hx.is_integer and ky.is_integer and x0 < hx < x1 and y0 < ky < y1
            assert ('maximum' in en) == (a < 0) and ('minimum' in en) == (a > 0)
            assert ptv(A) == (Fr(int(hx)), Fr(int(ky))) and all(ptv(w) != ptv(A) for w in W)
        elif t == 'readval':
            x = num(re.search(r'find f\((−?\d+)\)', en).group(1)); v = val(f, x); assert num(A) == v and y0 < v < y1
            assert all(num(w) != v for w in W)
        elif t == 'solvek':
            c = num(re.search(r'solve f\(x\) = (−?\d+)\.', en).group(1)); S = iroots(f, c)
            assert all(x0 < x < x1 for x in S) and xset(A) == S and all(xset(w) != S for w in W) and y0 < c < y1
    elif t in ('ballmax', 'balltop', 'balland', 'ballh'):
        g, = read_graphs(h); assert g['xl'] == 't (s)' and g['yl'] == 'h (m)'
        kind, f = g['curves']['']; assert kind == 'quadratic'
        a = sp.Poly(f, X).all_coeffs()[0]; assert a < 0 and f.subs(X, 0) == 0
        tt = sp.solve(sp.diff(f, X), X)[0]; Hm = f.subs(X, tt); land = max(sp.solve(f, X))
        assert Fr(str(Hm)) in [Fr(v).limit_denominator(100) for v in g['gly']], 'max height not on a gridline'
        if t == 'ballmax': ans = Fr(str(Hm)); assert unit(A, 'm') == ans and all(not w.endswith(' m') or unit(w, 'm') != ans for w in W)
        if t == 'balltop': assert unit(A, 's') == Fr(str(tt)) and all(unit(w, 's') != Fr(str(tt)) for w in W)
        if t == 'balland': assert unit(A, 's') == Fr(str(land)) and all(unit(w, 's') != Fr(str(land)) for w in W)
        if t == 'ballh':
            hh = num(re.search(r'ball (\d+) m high', en).group(1)); S = sorted(Fr(str(v)) for v in sp.solve(sp.Eq(f, hh), X))
            assert len(S) == 2 and all(v.denominator == 1 for v in S) and hh in [Fr(v).limit_denominator(100) for v in g['gly']]
            assert A == f'{S[0]} s and {S[1]} s', 'ballh'
            assert all(w != A for w in W)
    elif t.startswith('taxi'):
        g, = read_graphs(h); assert g['xl'] == 'km' and g['yl'] == '€'
        kind, f = g['curves']['']; assert kind == 'linear'
        m = sp.Poly(f, X).all_coeffs(); m, c = (m + [0])[:2] if len(m) == 2 else (0, m[0])
        euro = lambda s: num(re.fullmatch(r'€(\d+)', s).group(1))
        if t == 'taxifix': assert euro(A) == c and all(euro(w) != c for w in W)
        if t == 'taxirate': assert euro(A) == m and all(euro(w) != m for w in W)
        if t == 'taxicost':
            d = num(re.search(r'What does (\d+) km cost', en).group(1)); v = val(f, d); assert euro(A) == v and all(euro(w) != v for w in W)
            assert v in [Fr(x).limit_denominator(100) for x in g['gly']], 'cost not on a gridline'
        if t == 'taxidist':
            cc = num(re.search(r'for €(\d+)\?', en).group(1)); s = sp.solve(sp.Eq(f, cc), X)[0]; assert unit(A, 'km') == Fr(str(s))
            assert all(unit(w, 'km') != Fr(str(s)) and unit(w, 'km') > 0 for w in W) and cc in [Fr(x).limit_denominator(100) for x in g['gly']]
    elif t == 'storyg':
        st = eqbox(h)[0]; want = story_shape(st); S = read_sk(h); assert [l for l, _ in S] == list('ABCD')
        sh = [s for _, s in S]; assert '?' not in sh and len(set(sh)) == 4, sh
        assert dict(S)[A] == want, ('storyg', S, st)
    elif t == 'gstory':
        (l, s), = read_sk(h); assert s != '?'
        assert story_shape(A) == s and all(story_shape(w) != s for w in W)
        assert len(set(story_shape(w) for w in W)) == 3
    elif t == 'classtab':
        xs, ys = read_table(h); assert classify_table(xs, ys) == A, (xs, ys, A)
    elif t == 'classf':
        assert classify_expr(rhs(eqbox(h)[0])) == A
    elif t == 'tablerule':
        xs, ys = read_table(h); assert all(val(fopt(A), x) == y for x, y in zip(xs, ys)), 'rule'
        for w in W: assert not all(val(fopt(w), x) == y for x, y in zip(xs, ys)), 'wrong rule fits'
    else: flag(q, 'unknown type ' + str(t))

def main():
    Q = json.load(open(sys.argv[1])); types = Counter()
    for q in Q:
        try: check(q)
        except Exception as e: flag(q, 'ERROR ' + repr(e)[:160])
        types[q['data'].get('t')] += 1
    print(len(Q), 'questions;', dict(types))
    c = Counter(b[0] + ': ' + b[1][:60] for b in bad)
    for k, v in c.most_common(30): print(v, k)
    for b in bad[:8]: print(b)
    print('PROBLEMS:', len(bad))
main()
