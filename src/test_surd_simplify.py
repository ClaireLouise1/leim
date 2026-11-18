# Independent checker for Surd Simplify (surds, Order 37).
# Reads the question TEXT only (the question line and the expression in the question box),
# works the answer out exactly with sympy, and checks every option.
# node src/test_surd_simplify.js > /tmp/ss.json ; python3 src/test_surd_simplify.py /tmp/ss.json
import json, re, sys, html as H
import sympy as sp

def eqbox(h):
    m = re.findall(r'<p class="e" data-e="1">(.*?)</p>', h)
    return H.unescape(m[0]) if m else None

def val(s):
    """exact value of a surd expression written like the site: 3√2, √3(4 + 2√3), (2 + √5)², 6√18 ÷ 2√2"""
    e = s.replace('−', '-').replace('×', '*').replace('÷', '/').replace('²', '**2')
    e = re.sub(r'√(\d+)', r'sqrt(\1)', e)
    e = re.sub(r'(\d|\))(?=sqrt|\()', r'\1*', e)
    # "a ÷ b" where b is a product like 2*sqrt(2): divide by the whole term
    if '/' in e:
        l, r = e.split('/')
        return sp.nsimplify(sp.sympify(l) / sp.sympify(r))
    return sp.expand(sp.sympify(e))

def simplest(s):
    """an answer is in simplest form: a whole number, or c ± a√b, with b square-free and > 1"""
    t = s.replace(' ', '').replace('−', '-')
    m = re.fullmatch(r'-?\d+', t)
    if m: return True
    m = re.fullmatch(r'(?:(-?\d+)([+-]))?(-?\d*)√(\d+)(?:([+-])(\d+))?', t)
    if not m: return False
    b = int(m.group(4))
    return b > 1 and all(b % (k * k) for k in range(2, b + 1) if k * k <= b) and m.group(3) not in ('1', '-1')

def sqfree_part(n):
    s, t = 1, n
    k = 2
    while k * k <= t:
        while t % (k * k) == 0: t //= k * k; s *= k
        k += 1
    return s, t

def check(q):
    en, box = q['en'], eqbox(q['html']) if q['html'] else None
    opts = [q['answer']] + q['wrong']
    if en in ('Simplify.', 'Work out.', 'Expand.'):
        v = val(box)
        if q['answer'] == "Can't simplify":
            terms = re.findall(r'√(\d+)', box)
            assert len(terms) == 2 and '−' not in box
            parts = [sqfree_part(int(t)) for t in terms]
            assert all(p[0] == 1 for p in parts) and parts[0][1] != parts[1][1], 'it CAN be simplified'
        else:
            assert sp.simplify(val(q['answer']) - v) == 0, ('answer value', v)
            assert simplest(q['answer']), 'answer not in simplest form'
            if "Can't simplify" in opts:
                assert len(set(sqfree_part(int(t))[1] for t in re.findall(r'√(\d+)', box))) == 1
        for w in q['wrong']:
            if w == "Can't simplify": continue
            assert sp.simplify(val(w) - v) != 0, 'wrong option equals answer: ' + w
        return
    if en == 'Write as one square root.':
        v = val(box)
        m = re.fullmatch(r'√(\d+)', q['answer']); assert m
        assert int(m.group(1)) == v ** 2
        for w in q['wrong']: assert sp.simplify(val(w) - v) != 0, w
        return
    if en in ('Which one is a surd?', 'Which one is NOT a surd?'):
        irr = [o for o in opts if not sp.sqrt(int(o[1:])).is_rational]
        if en == 'Which one is a surd?': assert irr == [q['answer']], irr
        else:
            rat = [o for o in opts if o not in irr]
            assert rat == [q['answer']], rat
        return
    if en == 'Between which two whole numbers?':
        n = int(box[1:])
        def inside(o):
            a, b = map(int, o.split(' and ')); assert b == a + 1
            return a * a < n < b * b
        assert inside(q['answer'])
        for w in q['wrong']: assert not inside(w), w
        return
    raise AssertionError('unknown question ' + en)

def main():
    Q = json.load(open(sys.argv[1]))
    bad = 0; per = {}
    for q in Q:
        per[q['mk']] = per.get(q['mk'], 0) + 1
        opts = [q['answer']] + q['wrong']
        try:
            assert len(q['wrong']) == 3, 'only %d wrong options' % len(q['wrong'])
            assert len(set(opts)) == len(opts), 'duplicate options'
            for o in opts: assert '-' not in o and 'NaN' not in o and 'undefined' not in o and not re.search(r'√1(?!\d)', o), 'bad option ' + o
            for o in opts: assert not re.search(r'(^|[^\d])1√', o) and not re.search(r'√0', o), 'bad option ' + o
            check(q)
        except Exception as e:
            bad += 1
            if bad <= 12: print('PROBLEM', q['mode'], q['mk'], q['en'], eqbox(q['html']) if q['html'] else '', q['answer'], q['wrong'], repr(e)[:300])
    print(len(Q), 'questions,', bad, 'problems;', per)
    sys.exit(1 if bad else 0)

if __name__ == '__main__':
    main()
