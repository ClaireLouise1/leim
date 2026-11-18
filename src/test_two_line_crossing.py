#!/usr/bin/env python3
"""Independent checker for Two-Line Crossing (Order 29, simultaneous equations).
node src/test_two_line_crossing.js > /tmp/tl.json ; python3 src/test_two_line_crossing.py /tmp/tl.json
(env TL=<file> tests a mutated copy, N=<count> per maker)

Works every answer out again from the question TEXT (the two equations, the steps, the word
problem's numbers) and from the PICTURE (lines read back from the SVG via test_line_lab.read_plane),
with sympy and exact fractions. Checks the answer is right and that no wrong option is also right."""
import json, re, sys, os
from fractions import Fraction as Fr
from collections import Counter
import sympy as sp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from test_line_lab import read_plane

MINUS = "−"
X, Y = sp.symbols("x y")

def ex(s):
    t = s.replace(MINUS, "-").strip()
    t = re.sub(r"(\d|\))\s*([xy(])", r"\1*\2", t)
    assert re.fullmatch(r"[\dxy+\-*/(). ]+", t), s
    return sp.sympify(t)
def eqn(s):
    """'2x + 3(y − 1) = 7' → sympy expression lhs − rhs"""
    assert s.count(" = ") == 1, s
    l, r = s.split(" = ")
    return sp.expand(ex(l) - ex(r))
def same(a, b):
    """two linear equations (as lhs − rhs) describe the same line / statement"""
    if a == 0 or b == 0: return a == b
    q = sp.simplify(a / b)
    return q.free_symbols == set() and q != 0
def frac(s): return Fr(s.replace(MINUS, "-"))
def pair(s):
    m = re.fullmatch(r"x = (\S+), y = (\S+)", s)
    assert m, "pair format " + s
    return (frac(m.group(1)), frac(m.group(2)))
def fits(e, P): return sp.simplify(e.subs({X: sp.Rational(P[0].numerator, P[0].denominator), Y: sp.Rational(P[1].numerator, P[1].denominator)})) == 0
def eqs_of(html):
    out = []
    for raw in re.findall(r'<p class="e" data-e="\d">(.*?)</p>', html):
        t = re.sub(r"<b[^>]*>[^<]*</b>\s*", "", raw)
        t = re.sub(r"^[①②]\s*", "", t)
        out.append(t)
    return out
def solve2(e1, e2):
    s = sp.solve([e1, e2], [X, Y], dict=True)
    assert len(s) == 1 and len(s[0]) == 2, "no unique solution"
    return (Fr(str(s[0][X])), Fr(str(s[0][Y])))
def combo(s):
    m = re.fullmatch(r"(?:(\d) × )?① ([+−]) (?:(\d) × )?②", s)
    assert m, "combo format " + s
    p = int(m.group(1) or 1); q = int(m.group(3) or 1) * (1 if m.group(2) == "+" else -1)
    return p, q

def check(q):
    p = []
    t = q["data"].get("t"); html = q["html"]; en = q["en"]; A = q["answer"]; W = q["wrong"]
    opts = [A] + W
    if len(W) != 3 or len(set(opts)) != 4: p.append("needs 4 different options")
    text = " ".join([en, re.sub(r"<svg.*?</svg>", "", html, flags=re.S)] + opts)
    plain = re.sub(r"<[^>]+>", " ", text)
    if "-" in plain.replace("Two-Line", "") : p.append("ASCII minus")
    for bad, why in [(r"(?<![\d.])1[xy]", "1x"), (r"−1[xy]", "−1x"), (r"\+ −", "+ −"), (r"−0(?![.\d])", "−0"), (r"(?<![\d.])0[xy]", "0x"), (r"−−", "−−"), (r"\b([A-Za-z]+) \1\b", "doubled word"), (r"NaN|undefined|Infinity|null", "bad value")]:
        if re.search(bad, plain): p.append("text: " + why)
    hl = en.startswith("Higher Level: ")
    if hl != bool(q["data"].get("hl")): p.append("Higher Level label")
    E = [eqn(s) for s in eqs_of(html)]
    if t in ("pair", "solve", "graph"):
        assert len(E) == 2
        S = solve2(*E)
        if pair(A) != S: p.append(f"answer {A} but solution is {S}")
        for w in W:
            if fits(E[0], pair(w)) and fits(E[1], pair(w)): p.append("wrong option also solves both: " + w)
        if not hl and (S[0].denominator != 1 or S[1].denominator != 1): p.append("fraction answer outside Higher Level")
        if hl and t == "solve":
            has_frac = any("/" in s for s in eqs_of(html)) or S[0].denominator != 1 or S[1].denominator != 1
            if not has_frac: p.append("HL question with nothing Higher Level in it")
        if t == "graph":
            pl = read_plane(html)
            lines = pl["lines"]
            if set(lines) != {"l", "k"}: p.append("graph needs lines l and k")
            for name, e in zip(["l", "k"], E):
                m, c = lines[name]
                # the drawn line must be the equation's line: two points of it must fit
                for xv in (Fr(0), Fr(1)):
                    if not fits(e, (xv, m * xv + c)): p.append(f"line {name} drawn is not its equation"); break
            if abs(S[0]) > pl["R"] - 1 or abs(S[1]) > pl["R"] - 1: p.append("crossing too near the edge")
    elif t == "issol":
        T = pair(re.search(r"Does (x = \S+, y = \S+) fit", en).group(1).rstrip(","))
        o1, o2 = fits(E[0], T), fits(E[1], T)
        truth = "Yes, both" if o1 and o2 else "Only ①" if o1 else "Only ②" if o2 else "Neither"
        if A != truth: p.append(f"issol answer {A}, truth {truth}")
        if set(opts) != {"Yes, both", "Only ①", "Only ②", "Neither"}: p.append("issol options")
    elif t == "findy":
        assert len(E) == 1
        xv = int(re.search(r"x = (\S+)\.", en).group(1).replace(MINUS, "-"))
        s = sp.solve(E[0].subs(X, xv), Y); yv = Fr(str(s[0]))
        if frac(A) != yv: p.append(f"findy answer {A}, truth {yv}")
        if yv.denominator != 1: p.append("findy not whole")
        if any(frac(w) == yv for w in W): p.append("findy wrong = answer")
    elif t == "step":
        v = {"x": X, "y": Y}[re.search(r"gets rid of ([xy])\?", en).group(1)]
        o = {X: Y, Y: X}[v]
        def res(c):
            a, b = combo(c); r = sp.expand(a * E[0] + b * E[1]); return r.coeff(v), r.coeff(o)
        cv, co = res(A)
        if cv != 0 or co == 0: p.append("step answer doesn't eliminate")
        for w in W:
            if res(w)[0] == 0: p.append("wrong step also eliminates: " + w)
    elif t == "after":
        add = en.startswith("Add ① and ②")
        assert add or en.startswith("Take ② away from ①")
        R = sp.expand(E[0] + E[1] if add else E[0] - E[1])
        if R.coeff(Y) != 0: p.append("after: y not gone")
        if sp.expand(eqn(A) - R) != 0: p.append(f"after answer {A} is not the result")
        for w in W:
            if same(eqn(w), R): p.append("after wrong option equivalent: " + w)
    elif t == "slip":
        L = re.findall(r'<p data-line="(\d)"><b>Line \d:</b> (.*?)</p>', html)
        assert [a for a, _ in L] == ["1", "2", "3", "4"]
        L = [re.sub(r"<[^>]+>", "", s) for _, s in L]
        first = None
        m = re.fullmatch(r"① ([+−]) ②: (.+)", L[0]); sg = 1 if m.group(1) == "+" else -1
        e1 = eqn(m.group(2))
        if sp.expand(e1 - (E[0] + sg * E[1])) != 0: first = first or 1
        if e1.coeff(Y) != 0: p.append("slip: line 1 still has y")
        x2 = frac(re.fullmatch(r"x = (\S+)", L[1]).group(1))
        if first is None:
            xs = sp.solve(e1, X)
            if len(xs) != 1 or Fr(str(xs[0])) != x2: first = 2
        m3 = re.fullmatch(r"Put x = (\S+) in ①: (.+)", L[2]); x3 = frac(m3.group(1)); e3 = eqn(m3.group(2))
        if x3 != x2: p.append("slip: line 3 uses a different x")
        if first is None:
            # line 3 must be ① with x put in, written as a number + by = c
            if sp.expand(e3 - E[0].subs(X, sp.Rational(x3.numerator, x3.denominator))) != 0: first = 3
        y4 = frac(re.fullmatch(r"y = (\S+)", L[3]).group(1))
        if first is None:
            ys = sp.solve(e3, Y)
            if len(ys) != 1 or Fr(str(ys[0])) != y4: first = 4
        truth = "No mistake" if first is None else f"Line {first}"
        if A != truth: p.append(f"slip answer {A}, truth {truth}")
        if first is None:
            S = solve2(*E)
            if (x2, y4) != S: p.append("slip: 'no mistake' working gives the wrong solution")
        for s in L:
            for v in re.findall(r"[−\d/]+", s):
                if "/" in v: p.append("slip: fraction in working")
    elif t == "subst":
        m = re.fullmatch(r"y = (.+)", eqs_of(html)[0]); rhs = ex(m.group(1))
        want = sp.expand(E[1].subs(Y, rhs))
        if sp.expand(eqn(A) - want) != 0: p.append(f"subst answer {A} wrong")
        if Y in eqn(A).free_symbols: p.append("subst answer still has y")
        for w in W:
            e = eqn(w)
            if Y not in e.free_symbols and same(e, want): p.append("subst wrong option equivalent: " + w)
    elif t == "tix":
        m = re.fullmatch(r".+ sold (\d+) tickets: (\w+) €(\d+), (\w+) €(\d+)\. Takings: €(\d+)\. How many (\w+) tickets\?", en)
        n, pa, pb, T = int(m.group(1)), int(m.group(3)), int(m.group(5)), int(m.group(6))
        a, b = sp.symbols("a b"); s = sp.solve([a + b - n, pa * a + pb * b - T], [a, b])
        ask = m.group(7); first = m.group(2).startswith(ask[:3])
        truth = s[a] if first else s[b]
        if not (s[a] > 0 and s[b] > 0 and s[a].is_integer and s[b].is_integer): p.append("tix not whole/positive")
        if frac(A) != truth: p.append(f"tix answer {A}, truth {truth}")
        if any(frac(w) == truth for w in W): p.append("tix wrong = answer")
    elif t == "price":
        m = re.fullmatch(r"(\d+) (.+?) and (\d+) (.+?) cost €(\d+)\. (\d+) (.+?) and (\d+) (.+?) cost €(\d+)\. How much is one (.+)\?", en)
        g = m.groups(); a1, b1, T1, a2, b2, T2 = int(g[0]), int(g[2]), int(g[4]), int(g[5]), int(g[7]), int(g[9])
        for k in (1, 6):
            if g[k][:3] != g[1][:3]: p.append("price: item order differs")
        u, v = sp.symbols("u v"); s = sp.solve([a1 * u + b1 * v - T1, a2 * u + b2 * v - T2], [u, v])
        ask = g[10]; truth = s[u] if ask[:3] == g[1][:3] else s[v]
        if ask[:3] not in (g[1][:3], g[3][:3]): p.append("price: unknown item")
        for k in (0, 2, 5, 7):
            n_ = int(g[k]); w0 = g[k + 1].split()[0]
            if (n_ == 1) == w0.endswith("s"): p.append("price: plural " + str(n_) + " " + g[k + 1])
        if not (s[u] > 0 and s[v] > 0 and s[u].is_integer and s[v].is_integer): p.append("price not whole/positive")
        if A != f"€{truth}": p.append(f"price answer {A}, truth {truth}")
        if f"€{truth}" in W: p.append("price wrong = answer")
    elif t == "two":
        m = re.fullmatch(r"Two numbers add up to (\d+)\. Their difference is (\d+)\. What is the (bigger|smaller) number\?", en)
        s_, d_ = int(m.group(1)), int(m.group(2)); big = (s_ + d_) / 2; sm = (s_ - d_) / 2
        truth = big if m.group(3) == "bigger" else sm
        if not (sm > 0 and big == int(big)): p.append("two: not whole/positive")
        if float(frac(A)) != truth: p.append("two answer")
        if any(float(frac(w)) == truth for w in W): p.append("two wrong = answer")
    elif t == "form":
        m = re.fullmatch(r".+ sold (\d+) tickets: (\w+) €(\d+), (\w+) €(\d+)\. Takings: €(\d+)\. x = (\w+), y = (\w+)\. Which equations fit\?", en)
        n, pa, pb, T = int(m.group(1)), int(m.group(3)), int(m.group(5)), int(m.group(6))
        if m.group(7) != m.group(2) or m.group(8) != m.group(4): p.append("form: x, y names")
        true = [sp.expand(X + Y - n), sp.expand(pa * X + pb * Y - T)]
        def ok(s):
            e = [eqn(z) for z in s.split(" and ")]
            return len(e) == 2 and any(same(e[0], true[i]) and same(e[1], true[1 - i]) for i in (0, 1))
        if not ok(A): p.append("form answer wrong")
        for w in W:
            if ok(w): p.append("form wrong option right: " + w)
    else:
        p.append("unknown type " + str(t))
    return p

if __name__ == "__main__":
    data = json.load(open(sys.argv[1]))
    probs = Counter(); ex_ = {}
    for q in data:
        try: r = check(q)
        except Exception as e: r = ["crash: " + repr(e)[:120]]
        for x in r:
            k = q["mk"] + ": " + x.split(":")[0] if "crash" not in x else q["mk"] + ": " + x
            probs[k] += 1; ex_.setdefault(k, (q["en"], re.sub(r"<svg.*?</svg>", "[svg]", q["html"], flags=re.S)[:300], q["answer"], q["wrong"], x))
    print(len(data), "questions,", sum(probs.values()), "problems")
    for k, v in probs.most_common(40): print(v, k, "\n    ", ex_[k])
