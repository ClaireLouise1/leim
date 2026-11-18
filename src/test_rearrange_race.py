# Independent checker for Rearrange Race (algebraic fractions, long division, changing the subject).
# Reads the question TEXT only (the data-e attribute of the question box and the visible options).
# node src/test_rearrange_race.js > /tmp/rr.json ; python3 src/test_rearrange_race.py /tmp/rr.json
import json, re, sys, html as H, random
from fractions import Fraction
from math import gcd
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
TR = standard_transformations + (implicit_multiplication_application,)
LET = {c: sp.Symbol(c, positive=True) for c in 'abcdefghlmnrstuvwyzACEFHIPRSTV'}
LET['x'] = sp.Symbol('x', positive=True)
LET['π'] = sp.Symbol('π', positive=True)
def P(s):
    s = s.strip().replace('−', '-').replace('²', '**2').replace('³', '**3').replace('½', '(1/2)').replace('×', '*')
    s = re.sub(r'(?<=[\w)])√', '*√', s)
    s = re.sub(r'√(\w)', r'sqrt(\1)', s).replace('√', 'sqrt')
    return parse_expr(s, local_dict=dict(LET), transformations=TR)
def side(s):
    l, r = s.split(' = ')
    return P(l), P(r)
def zero(e):
    se = sp.simplify(e)
    if se.has(sp.nan, sp.zoo): return False
    if se == 0: return True
    # numeric fallback (several random positive points)
    syms = list(e.free_symbols)
    for _ in range(6):
        v = {k: random.uniform(1.5, 9) for k in syms}
        z = complex(e.subs(v).evalf())
        if z != z or abs(z) > 1e-9: return False
    return True
def eqbox(h):
    return [H.unescape(m) for m in re.findall(r'<p class="e" data-e="([^"]*)"', h)]
def extra(h):
    m = re.search(r'<p class="e2">(.*?)</p>', h)
    return H.unescape(m.group(1)) if m else None
def steps(h):
    return [H.unescape(m) for m in re.findall(r'<p data-line="\d" data-s="([^"]*)"', h)]
def num(s): return Fraction(s.replace('−', '-'))

bad = []
def flag(q, msg): bad.append((q['mk'], msg, q['en'], q['answer'], q['wrong'], q['data'].get('rv')))
TEXT_BAD = [(r'(?<![\w(./])1[a-zπ]', '1x'), (r'\+ −', '+ −'), (r'−0(?![.\d])', '−0'), (r'(?<![\d.])0[xy]', '0x'), (r'\b(\w+) \1\b', 'doubled word'), (r'(?<=[\s(])-\d', 'ASCII minus'), (r'\(\)', 'empty brackets'), (r'NaN|undefined', 'NaN')]

def rearr_ok(F, sub, opt):
    m = re.fullmatch(r'(\w) = (.+)', opt)
    if not m or m.group(1) != sub: raise ValueError('bad option ' + opt)
    l, r = side(F); s = LET[sub]
    e = P(m.group(2))
    if s in e.free_symbols: raise ValueError('subject on both sides ' + opt)
    return zero((l - r).subs(s, e))

def check(q):
    t = q['data'].get('t'); en = q['en']; A = q['answer']; W = q['wrong']; h = q['html']
    for vis in [en, A, q['why']] + W + eqbox(h) + steps(h):
        for pat, name in TEXT_BAD:
            if re.search(pat, vis): flag(q, 'text: ' + name + ' in ' + vis)
    if len(W) != 3 or len(set(W + [A])) != 4: flag(q, 'options'); return
    if en.startswith('Higher Level: ') != bool(q['data'].get('hl')): flag(q, 'HL label')
    box = eqbox(h)[0]
    if t == 'rearr':
        sub = re.search(r'Make (\w) the subject', en).group(1)
        if not rearr_ok(box, sub, A): flag(q, 'answer wrong')
        for w in W:
            if rearr_ok(box, sub, w): flag(q, 'wrong option is right: ' + w)
    elif t == 'use':
        sub = re.fullmatch(r'Find (\w)\.', en).group(1)
        vals = {}
        for part in extra(h).split(', '):
            k, v = part.split(' = '); vals[LET[k]] = sp.Rational(str(num(v)))
        l, r = side(box)
        sol = sp.solve(sp.Eq(l.subs(vals), r.subs(vals)), LET[sub] if sub != 'C' else LET['C'])
        # C is declared positive; Celsius can be negative, so solve with a plain symbol
        if sub == 'C':
            c = sp.Symbol('c_any'); sol = sp.solve(sp.Eq(l.subs(vals).subs(LET['C'], c), r.subs(vals).subs(LET['C'], c)), c)
        if len(sol) != 1: flag(q, 'no unique solution'); return
        true = Fraction(str(sol[0]))
        if true.denominator != 1: flag(q, 'answer not whole')
        if num(A) != true: flag(q, 'answer wrong')
        for w in W:
            if num(w) == true: flag(q, 'wrong option is right')
    elif t in ('add', 'simp'):
        e = P(box)
        if not zero(P(A) - e): flag(q, 'answer wrong')
        for w in W:
            if zero(P(w) - e): flag(q, 'wrong option is right: ' + w)
        # fully simplified: denominator of the answer = denominator of the sum
        nd = sp.fraction(sp.cancel(sp.together(e)))
        m = re.fullmatch(r'\((.+)\)/(\d+)|(−?\d*x)/(\d+)|(−?\d+)/(\d+)', A)
        if m and not q['data'].get('hl'):
            L = int(m.group(2) or m.group(4) or m.group(6))
            topx = sp.Poly(P(m.group(1) or m.group(3) or m.group(5)), LET['x'])
            g = L
            for c in topx.all_coeffs(): g = gcd(g, int(c))
            if g != 1: flag(q, 'not simplified')
        if q['data'].get('hl'):
            mm = re.fullmatch(r'(.+)/\((\(x [+−] \d\)\(x [+−] \d\))\)', A)
            if not mm: flag(q, 'HL answer format')
    elif t == 'lcd':
        ds = [int(d) for d in re.findall(r'/(\d+)', box)]
        L = ds[0] * ds[1] // gcd(ds[0], ds[1])
        if num(A) != L: flag(q, 'lcd wrong')
        for w in W:
            if num(w) == L: flag(q, 'wrong option is right')
    elif t == 'div':
        top, dv = [P(z.strip()[1:-1]) for z in box.split(' ÷ ')]
        x = LET['x']
        qt, rm = sp.div(sp.Poly(top, x), sp.Poly(dv, x))
        if rm.as_expr() != 0: flag(q, 'remainder')
        if sp.expand(P(A) - qt.as_expr()) != 0: flag(q, 'answer wrong')
        for w in W:
            if sp.expand(P(w) - qt.as_expr()) == 0: flag(q, 'wrong option is right')
    elif t in ('slipexpr', 'slipeq'):
        L = steps(h); first = 0
        if t == 'slipexpr':
            e0 = P(box)
            for i, z in enumerate(L):
                if not zero(P(z) - e0): first = i + 1; break
        else:
            sub = q['data']['sub']; s = LET[sub]
            l, r = side(box)
            sol = sp.solve(sp.Eq(l, r), s)
            if len(sol) != 1: flag(q, 'start not linear'); return
            for i, z in enumerate(L):
                l2, r2 = side(z)
                if not zero((l2 - r2).subs(s, sol[0])): first = i + 1; break
            if not re.fullmatch(sub + r' = .+', L[-1]) or s in P(L[-1].split(' = ')[1]).free_symbols: flag(q, 'last line not solved')
            if not en.startswith('Make ' + sub + ' the subject.'): flag(q, 'subject not named')
        exp = 'No mistake' if first == 0 else 'Line %d' % first
        if A != exp: flag(q, 'slip: expected ' + exp)
    else:
        flag(q, 'unknown type ' + str(t))

if __name__ == '__main__':
    data = json.load(open(sys.argv[1]))
    from collections import Counter
    for q in data:
        try: check(q)
        except Exception as ex: flag(q, 'crash: %r' % ex)
    c = Counter(b[0] + ': ' + b[1].split(':')[0] for b in bad)
    print(len(data), 'questions,', len(bad), 'problems')
    for k, v in c.most_common(): print(' ', v, k)
    seen = set()
    for b in bad:
        if (b[0], b[1][:20]) in seen: continue
        seen.add((b[0], b[1][:20])); print(b)
