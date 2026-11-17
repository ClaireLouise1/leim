#!/usr/bin/env python3
"""Independent checker for Balance It (linear equations).
node src/test_balance_it.js > /tmp/bi.json ; python3 src/test_balance_it.py /tmp/bi.json
Solves every equation itself with sympy, counts bags/counters in the balance pictures,
re-does the 'both sides' operations, reads the word problems with its own grammar
(reverse operations, no sympy), and finds the first wrong line in worked solutions."""
import json, re, sys
from fractions import Fraction
from math import gcd
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

x = sp.Symbol("x")
TR = standard_transformations + (implicit_multiplication_application,)

def E(s):
    s = s.replace("−", "-").replace("×", "*").replace("€", "").strip()
    return parse_expr(s, local_dict={"x": x}, transformations=TR)

def EQ(s):
    l, r = s.split(" = ")
    return E(l), E(r)

def sol(s):
    l, r = EQ(s)
    v = sp.solve(sp.Eq(l, r), x)
    assert len(v) == 1, ("not one solution", s, v)
    return sp.Rational(v[0])

def numv(s):
    return sp.Rational(s.replace("−", "-").replace("€", ""))

def lcm(a, b):
    return a * b // gcd(a, b)

def think(en):
    """own grammar: reverse the operations"""
    m = re.search(r"I multiply it by (\d+) and add (\d+)\. The answer is (\d+)\.", en)
    if m and "same answer" not in en:
        a, b, c = map(int, m.groups()); return Fraction(c - b, a)
    m = re.search(r"I multiply it by (\d+) and subtract (\d+)\. The answer is (\d+)\.", en)
    if m:
        a, b, c = map(int, m.groups()); return Fraction(c + b, a)
    m = re.search(r"I add (\d+), then multiply the result by (\d+)\. The answer is (\d+)\.", en)
    if m:
        b, a, c = map(int, m.groups()); return Fraction(c, a) - b
    m = re.search(r"If I multiply it by (\d+) and add (\d+), I get the same answer as when I multiply it by (\d+) and add (\d+)\.", en)
    if m:
        a, b, c, d = map(int, m.groups()); return Fraction(d - b, a - c)
    m = re.search(r"I divide it by (\d+), then add (\d+)\. The answer is (\d+)\.", en)
    if m:
        a, b, c = map(int, m.groups()); return Fraction(c - b) * a
    raise AssertionError("think: no template " + en)

def ctx(en, html):
    m = re.search(r"A rectangle is \(x \+ (\d+)\) cm long and x cm wide\. Its perimeter is (\d+) cm\.", en)
    if m:
        a, P = map(int, m.groups())
        labels = re.findall(r'data-side="\d"[^>]*>([^<]+)<', html)
        assert labels == ["x + %d" % a, "x"], ("rect labels", labels)
        # try every whole number: the perimeter must match
        hits = [w for w in range(1, 200) if 2 * (w + a) + 2 * w == P]
        assert len(hits) == 1; return Fraction(hits[0])
    m = re.search(r"angles of a triangle are x°, (\d+)x° and \(x \+ (\d+)\)°", en)
    if m:
        k, a = map(int, m.groups()); return Fraction(180 - a, k + 2)
    m = re.search(r"Three consecutive whole numbers add up to (\d+)\. What is the smallest", en)
    if m:
        S = int(m.group(1)); hits = [n for n in range(-100, 200) if n + (n + 1) + (n + 2) == S]
        assert len(hits) == 1; return Fraction(hits[0])
    m = re.search(r"(\w+) is (\d+) years older than her brother (\w+)\. Their ages add up to (\d+)\. How old is (\w+)\?", en)
    if m:
        g, a, b, S, b2 = m.groups(); assert b == b2; return Fraction(int(S) - int(a), 2)
    m = re.search(r"(\d+) cinema tickets and a €(\d+) popcorn cost €(\d+) altogether", en)
    if m:
        n, a, S = map(int, m.groups()); return Fraction(S - a, n)
    m = re.search(r"(\w+) has (\d+) times as many stickers as (\w+)\. Together they have (\d+)\. How many has (\w+)\?", en)
    if m:
        g, k, b, S, b2 = m.groups(); assert b == b2; return Fraction(int(S), int(k) + 1)
    raise AssertionError("ctx: no template " + en)

def apply_op(op, l, r):
    m = re.match(r"(Subtract|Add) (.+?) (?:from|to) both sides\.$", op)
    if m:
        t = E(m.group(2)); s = -1 if m.group(1) == "Subtract" else 1
        return sp.expand(l + s * t), sp.expand(r + s * t)
    m = re.match(r"(Divide|Multiply) both sides by (\d+)\.$", op)
    if m:
        k = int(m.group(2)); f = sp.Rational(1, k) if m.group(1) == "Divide" else k
        return sp.expand(l * f), sp.expand(r * f)
    raise AssertionError("op? " + op)

BAD = [r"NaN", r"undefined", r"Infinity", r"\+ −", r"− −", r"(?<![0-9])1x", r"−0(?![0-9.])", r"(?<![0-9])0x", r"\+ 0(?![0-9])", r"(?<![\w(])-\d", r"\[object"]

def check(q):
    t = q["data"]["t"]; ans = q["answer"]; wr = q["wrong"]
    assert len(wr) == 3 and ans not in wr and len(set(wr)) == 3, "options"
    for fld in ("en", "frame", "answer", "why") + tuple():
        for b in BAD:
            assert not re.search(b, q[fld] or ""), ("bad text", b, fld, q[fld])
    for w in wr:
        for b in BAD:
            assert not re.search(b, w), ("bad option", b, w)
    for m in re.finditer(r"(\d+) \(the LCM of (\d+) and (\d+)\)", q["why"]):
        assert int(m.group(1)) == lcm(int(m.group(2)), int(m.group(3))), ("LCM in why", m.group(0))
    for m in re.finditer(r"lowest common multiple of the bottom numbers (\d+) and (\d+): (\d+)\.", q["why"]):
        assert int(m.group(3)) == lcm(int(m.group(1)), int(m.group(2))), ("LCM in why", m.group(0))
    if t in ("solve", "bal", "ctx", "think"):
        assert re.search(r"(?<![\d.])" + re.escape(ans) + r"(?![\d])", q["why"]), ("answer not in why", ans, q["why"])
    if t in ("solve", "bal"):
        s = sol(q["frame"])
        assert s.q == 1, ("not whole", q["frame"], s)
        assert numv(ans) == s, ("wrong answer", q["frame"], ans, s)
        for w in wr: assert numv(w) != s, ("wrong option is right", w)
        if t == "bal":
            items = re.findall(r'<g class="(bag|one)" data-side="(L|R)"', q["html"])
            c = {(k, sd): items.count((k, sd)) for k in ("bag", "one") for sd in "LR"}
            pl = c[("bag", "L")] * x + c[("one", "L")]; prr = c[("bag", "R")] * x + c[("one", "R")]
            l, r = EQ(q["frame"])
            assert sp.expand((l - r) - (pl - prr)) == 0, ("picture != equation", q["frame"], c)
            assert s > 0, "a bag can't hold a negative number"
    elif t == "op":
        l, r = EQ(q["frame"]); nl, nr = apply_op(q["data"]["op"], l, r)
        def is_result(e):
            a, b = EQ(e); return sp.expand(a - nl) == 0 and sp.expand(b - nr) == 0
        assert is_result(ans), ("op result", q["frame"], q["data"]["op"], ans, nl, nr)
        for w in wr: assert not is_result(w), ("wrong option is the result", w)
        assert q["en"].startswith(q["data"]["op"])
    elif t == "lcd":
        ds = [int(d) for d in re.findall(r"/(\d+)", q["frame"])]
        L = 1
        for d in ds: L = lcm(L, d)
        assert int(numv(ans)) == L, ("lcd", q["frame"], ans, L)
        for w in wr: assert numv(w) != L
    elif t == "think":
        v = think(q["en"]); assert v.denominator == 1 and v > 0
        assert numv(ans) == v, ("think", q["en"], ans, v)
        for w in wr: assert numv(w) != v
    elif t == "form":
        v = think(q["en"])
        good = [o for o in [ans] + wr if sol(o) == v]
        assert good == [ans], ("form: options with the right solution", q["en"], good)
    elif t == "ctx":
        v = ctx(q["en"], q["html"]); assert v.denominator == 1 and v > 0, (q["en"], v)
        assert numv(ans) == v, ("ctx", q["en"], ans, v)
        for w in wr: assert numv(w) != v
    elif t == "claim":
        m = re.search(r"says the solution of (.+) is x = (\S+)\. Is (?:he|she) right\?$", q["en"])
        assert m, q["en"]
        s = sol(m.group(1)); v = numv(m.group(2))
        right = "Right" if v == s else "Wrong: x = " + (str(s).replace("-", "−"))
        assert ans == right, ("claim", q["en"], ans, right)
        nm = q["en"].split(" ")[0]
        assert q["en"].endswith(("she right?" if nm in GIRLS else "he right?")), ("pronoun", q["en"])
    elif t == "line":
        lines = re.findall(r'<p data-line="(\d)"><b>Line \d:</b> (.+?)</p>', q["html"])
        assert len(lines) == 4
        s0 = sol(q["frame"]); first = "No mistake"
        for i, ln in lines:
            if sol(ln) != s0: first = "Line " + i; break
        assert ans == first, ("line", q["frame"], lines, ans, first)
        assert lines[3][1].startswith("x = ")
        for i, ln in lines:
            for b in BAD: assert not re.search(b, ln), ("bad line", b, ln)
    else:
        raise AssertionError("unknown type " + t)

GIRLS = {"Ciara", "Aoife", "Zara", "Emma", "Niamh", "Áine", "Ella", "Saoirse"}

if __name__ == "__main__":
    data = json.load(open(sys.argv[1]))
    bad = 0; per = {}
    for q in data:
        per[q["mk"]] = per.get(q["mk"], 0) + 1
        try:
            check(q)
        except Exception as e:
            bad += 1
            if bad <= 12: print("FAIL", q["mk"], repr(e)[:400])
    print(len(data), "questions,", bad, "problems")
    print(per)
    sys.exit(1 if bad else 0)
