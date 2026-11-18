# Independent checker for Root Rush (quadratic equations). Reads the question TEXT and HTML only.
# node src/test_root_rush.js > /tmp/rr.json ; python3 src/test_root_rush.py /tmp/rr.json
import json, re, sys, html as H
from collections import Counter
from fractions import Fraction
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
X, K, T = sp.symbols('x k t')
TR = standard_transformations + (implicit_multiplication_application,)
def P(s):
    s = s.replace('−', '-').replace('²', '**2').replace('×', '*')
    return parse_expr(s, local_dict={'x': X, 'k': K, 't': T, 'h': sp.Symbol('h')}, transformations=TR)
def eqn(s):
    l, r = s.split('=')
    return sp.expand(P(l) - P(r))
def prop(a, b):
    """same equation up to a nonzero factor"""
    if a == 0 or b == 0: return a == b
    q = sp.simplify(a / b)
    return q.is_number and q != 0
def roots_of(e, v=X):
    return set(sp.nsimplify(r) for r in sp.solve(sp.Eq(e, 0), v))
def val(s):
    s = s.replace('−', '-').strip()
    return Fraction(s)
def rset(opt):
    """'x = −5 or x = 3' → set of Fractions"""
    parts = opt.split(' or ')
    out = []
    for p in parts:
        m = re.fullmatch(r'x = (−?\d+(?:/\d+)?)', p.strip())
        if not m: raise ValueError('bad roots option ' + opt)
        out.append(val(m.group(1)))
    if len(set(out)) != len(out): raise ValueError('repeated value ' + opt)
    if out != sorted(out): raise ValueError('not in order ' + opt)
    return set(out)
def fr(r): return Fraction(int(sp.numer(r)), int(sp.denom(r)))
def eqbox(h):
    return [H.unescape(re.sub('<[^>]+>', '', m)).strip() for m in re.findall(r'<p class="e"[^>]*>(.*?)</p>', h)]
def steps(h):
    return [H.unescape(re.sub('<[^>]+>', '', m)).split(':', 1)[1].strip() for m in re.findall(r'<p data-line="\d">(.*?)</p>', h)]
def d2(x):
    v = round(x * 100) / 100
    if abs(v) < 0.005: v = 0
    return ('−' if v < 0 else '') + f'{abs(v):.2f}'

bad = []
def flag(q, msg): bad.append((q['mk'], msg, q['en'], q['answer'], q['wrong']))
TEXT_BAD = [(r'(?<![\w(])1x', '1x'), (r'\+ −', '+ −'), (r'−0(?![.\d])', '−0'), (r'(?<![\d.])0x', '0x'), (r'\b(\w+) \1\b', 'doubled word'), (r'(?<=[\s(])-\d', 'ASCII minus')]

def check(q):
    t = q['data'].get('t'); en = q['en']; A = q['answer']; W = q['wrong']; h = q['html']
    for vis in [en, A, q['why']] + W + eqbox(h) + steps(h):
        for pat, name in TEXT_BAD:
            if re.search(pat, vis): flag(q, 'text: ' + name)
    if len(W) != 3 or len(set(W + [A])) != 4: flag(q, 'options'); return
    hl = bool(q['data'].get('hl'))
    if en.startswith('Higher Level: ') != hl: flag(q, 'HL label')
    if t in ('isroot', 'facroots', 'solve', 'other', 'findk', 'formula', 'value', 'rearr', 'slip'):
        box = eqbox(h)[0]
    if t == 'isroot':
        R = {fr(r) for r in roots_of(eqn(box))}
        if val(A) not in R: flag(q, 'answer not a root')
        for w in W:
            if val(w) in R: flag(q, 'wrong option is a root')
    elif t in ('facroots', 'solve'):
        e = eqn(box)
        if sp.degree(e, X) != 2: flag(q, 'not quadratic')
        R = {fr(r) for r in roots_of(e)}
        if any(not sp.Rational(r).is_rational for r in R): flag(q, 'irrational')
        if rset(A) != R: flag(q, 'wrong roots')
        for w in W:
            if rset(w) == R: flag(q, 'wrong option equal')
        a = sp.Poly(e, X).all_coeffs()[0]
        if not hl and any(r.denominator != 1 for r in R): flag(q, 'fraction root at OL')
        if hl and t == 'solve' and all(r.denominator == 1 for r in R): flag(q, 'HL without fraction')
    elif t == 'formula':
        e = eqn(box); rr = sorted(float(r) for r in sp.solve(e, X))
        exp = f'x = {d2(rr[0])} or x = {d2(rr[1])}'
        if A != exp: flag(q, f'formula {exp}')
        if any(w == exp for w in W): flag(q, 'wrong equals formula')
        disc = sp.discriminant(e, X)
        if sp.sqrt(disc).is_rational: flag(q, 'formula with rational roots')
    elif t == 'value':
        k = int(re.search(r'x = (−?\d+)', en).group(1).replace('−', '-'))
        v = P(box).subs(X, k)
        if val(A) != v: flag(q, 'value')
    elif t == 'rearr':
        st = eqn(box); ans = eqn(A)
        if not prop(st, ans) or not A.endswith('= 0'): flag(q, 'rearr answer')
        for w in W:
            if prop(st, eqn(w)): flag(q, 'rearr wrong equivalent')
    elif t == 'slip':
        st = eqn(box); L = steps(h)
        ok1 = prop(st, eqn(L[0]))
        ok2 = sp.expand(eqn(L[1]) - eqn(L[0])) == 0
        ok3 = rset(L[2]) == {fr(r) for r in roots_of(eqn(L[1]))}
        first = 'No mistake' if ok1 and ok2 and ok3 else 'Line 1' if not ok1 else 'Line 2' if not ok2 else 'Line 3'
        if first != A: flag(q, f'slip says {A}, checker {first}')
        if A == 'No mistake' and rset(L[2]) != {fr(r) for r in roots_of(st)}: flag(q, 'final roots')
    elif t in ('formeq', 'formfac'):
        m = re.search(r'Roots: (−?\d+) and (−?\d+)', eqbox(h)[0]); R = {val(m.group(1)), val(m.group(2))}
        def rts(s):
            e = eqn(s); return {r for r in roots_of(e)}, e
        R = {sp.Rational(z.numerator, z.denominator) for z in R}
        ra, ea = rts(A)
        if ra != R or sp.Poly(ea, X).degree() != 2: flag(q, 'form answer')
        if t == 'formfac' and not re.fullmatch(r'(x|\(x [−+] \d+\))(\(x [−+] \d+\)) = 0', A): flag(q, 'form shape')
        for w in W:
            if rts(w)[0] == R: flag(q, 'form wrong has the roots')
    elif t == 'other':
        r = val(re.search(r'x = (−?\d+) is one root', en).group(1))
        R = {fr(z) for z in roots_of(eqn(box))}
        if r not in R or R - {r} != {val(A)}: flag(q, 'other root')
    elif t == 'findk':
        r = int(re.search(r'x = (−?\d+) is a root', en).group(1).replace('−', '-'))
        e = eqn(box).subs(X, r); ks = sp.solve(e, K)
        if len(ks) != 1 or val(A) != ks[0]: flag(q, 'k')
    elif t in ('rect', 'formword'):
        top = re.search(r'data-top="([^"]+)"', h).group(1); side = re.search(r'data-side="([^"]+)"', h).group(1)
        area = int(re.search(r'data-area="(\d+) cm²"', h).group(1))
        e = sp.expand(P(top) * P(side) - area)
        pos = [fr(r) for r in roots_of(e) if r > 0]
        if t == 'rect':
            if len(pos) != 1 or val(A) != pos[0] or int(re.search(r'area is (\d+)', en).group(1)) != area: flag(q, 'rect')
        else:
            if not prop(e, eqn(A)): flag(q, 'formword answer')
            for w in W:
                if prop(e, eqn(w)): flag(q, 'formword wrong equivalent')
    elif t == 'num':
        m = re.search(r'number, (plus|minus) (?:(\d+) times )?the number, is (\d+)', en)
        k = int(m.group(2) or 1) * (1 if m.group(1) == 'plus' else -1); N = int(m.group(3))
        pos = [fr(r) for r in roots_of(X**2 + k*X - N) if r > 0]
        if len(pos) != 1 or val(A) != pos[0] or pos[0].denominator != 1: flag(q, 'num')
    elif t == 'consec':
        Pn = int(re.search(r'multiply to (\d+)', en).group(1))
        pos = [fr(r) for r in roots_of(X*(X+1) - Pn) if r > 0]
        if len(pos) != 1 or val(A) != pos[0]: flag(q, 'consec')
    elif t in ('land', 'height'):
        e = eqbox(h)[0]; hh = P(e.split('=')[1])
        target = 0 if t == 'land' else int(re.search(r'When is the ball (\d+) m high', en).group(1))
        ts = sorted(fr(r) for r in roots_of(hh - target, T) if r > 0)
        def tset(o): return [Fraction(z) for z in re.findall(r't = (\d+) s', o)] or [Fraction(re.fullmatch(r'(\d+) s', o).group(1))]
        if tset(A) != ts: flag(q, f'{t} {ts}')
        for w in W:
            if tset(w) == ts: flag(q, 'ball wrong equal')
    else:
        flag(q, 'unknown type ' + str(t))

d = json.load(open(sys.argv[1]))
for q in d:
    try: check(q)
    except Exception as e: flag(q, 'crash ' + repr(e))
print(len(d), 'questions,', len(bad), 'problems')
c = Counter((b[0], b[1]) for b in bad)
for k, v in c.most_common(30): print(v, k)
for b in bad[:12]: print(b)
