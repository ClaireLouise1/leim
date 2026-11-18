#!/usr/bin/env python3
"""Independent checker for Line Lab (Order 28, coordinate geometry of the line).
node src/test_line_lab.js > /tmp/ll.json ; python3 src/test_line_lab.py /tmp/ll.json
(env LL=<file> tests a mutated copy, N=<count> per maker)

Works every answer out again from the question TEXT (points, equations, contexts) and from the
PICTURE (lines, segments and points read back from the SVG's screen coordinates), with exact
fractions and sympy. Checks the answer is right and that no wrong option is also right."""
import json, re, sys, math
from fractions import Fraction as Fr
from functools import lru_cache
import sympy as sp

MINUS = "−"
X, Y = sp.symbols("x y")
UNI = {"½": "(1/2)", "⅓": "(1/3)", "⅔": "(2/3)", "¼": "(1/4)", "¾": "(3/4)"}

def num(s):
    s = s.strip().replace(MINUS, "-")
    return Fr(s)
PT = r"\((−?[\d.]+), (−?[\d.]+)\)"
def pts(s): return [(num(a), num(b)) for a, b in re.findall(PT, s)]
def pt(s):
    m = re.fullmatch(PT, s.strip())
    return (num(m.group(1)), num(m.group(2))) if m else None

@lru_cache(maxsize=None)
def E(s):
    """parse an expression like '⅔x − 1', '−(3/2)x + 4', '7 − 2x', '3x + 3y + 2' into sympy"""
    t = s.replace(MINUS, "-")
    for k, v in UNI.items(): t = t.replace(k, v)
    t = re.sub(r"(\d|\))\s*([xy])", r"\1*\2", t)
    assert re.fullmatch(r"[\dxy+\-*/(). ]+", t), s
    return sp.nsimplify(sp.sympify(t))

def line_of(s):
    """'y = …' or '… = 0' → (slope, intercept) as Fractions (vertical lines not used)"""
    l, r = s.split(" = ")
    if l == "y":
        e = sp.expand(E(r)); assert e.free_symbols <= {X}, s
        P = sp.Poly(e, X); assert P.degree() <= 1
        m = P.coeff_monomial(X); c = P.coeff_monomial(1)
    else:
        assert r == "0"; e = sp.expand(E(l)); a = e.coeff(X); b = e.coeff(Y); d = e.subs({X: 0, Y: 0})
        assert b != 0; m = -a / b; c = -d / b
    return (Fr(str(m)), Fr(str(c)))

def F(v): return Fr(v).limit_denominator(12)

# ---------- reading the grid picture ----------
def attrs(tag): return dict(re.findall(r'([\w-]+)="([^"]*)"', tag))
def read_plane(html):
    m = re.search(r'<svg class="tg"[^>]*>', html)
    if not m: return None
    a = attrs(m.group(0)); R = int(a["data-r"]); s = float(a["data-s"]); pd = float(a["data-pd"])
    G = lambda Xp, Yp: ((float(Xp) - pd) / s - R, R - (float(Yp) - pd) / s)
    out = {"R": R, "lines": {}, "segs": [], "pts": {}}
    # tick labels where they should be
    for tag in re.findall(r'<text class="tk" data-v="(-?\d+)" x="([\d.]+)"', html):
        v, xp = int(tag[0]), float(tag[1]); assert abs(G(xp, 0)[0] - v) < 0.02, "x tick in the wrong place"
    for tag in re.findall(r'<line class="ln[^"]*"[^>]*>', html):
        t = attrs(tag); p = G(t["x1"], t["y1"]); q = G(t["x2"], t["y2"])
        for e in (p, q): assert abs(abs(e[0]) - R) < 0.03 or abs(abs(e[1]) - R) < 0.03, "line stops inside the grid"
        assert abs(q[0] - p[0]) > 0.5, "vertical line"
        mm = F((q[1] - p[1]) / (q[0] - p[0])); cc = F(p[1] - float(mm) * p[0])
        for e in (p, q): assert abs(float(mm) * e[0] + float(cc) - e[1]) < 0.03, "line not straight through its ends"
        n = t["data-n"]; assert n not in out["lines"]
        if n: assert re.search(r'<text class="lnl[^"]*"[^>]*>' + re.escape(n) + "</text>", html), "line label missing"
        out["lines"][n] = (mm, cc)
    for tag in re.findall(r'<line class="sg"[^>]*>', html):
        t = attrs(tag); p = G(t["x1"], t["y1"]); q = G(t["x2"], t["y2"])
        A = tuple(map(int, t["data-a"].split(","))); B = tuple(map(int, t["data-b"].split(",")))
        assert abs(p[0] - A[0]) < .02 and abs(p[1] - A[1]) < .02 and abs(q[0] - B[0]) < .02 and abs(q[1] - B[1]) < .02, "segment data"
        out["segs"].append((A, B))
    for tag in re.findall(r'<circle class="pt[^"]*"[^>]*>', html):
        t = attrs(tag); p = G(t["cx"], t["cy"])
        assert abs(p[0] - float(t["data-x"])) < .02 and abs(p[1] - float(t["data-y"])) < .02, "point data"
        assert abs(p[0]) <= R and abs(p[1]) <= R
        out["pts"][t["data-n"] or f"?{len(out['pts'])}"] = (F(p[0]), F(p[1]))
        if t["data-n"]: assert f'>{t["data-n"]}</text>' in html, "point label missing"
    return out

def lattice_on(L, R):
    m, c = L
    return [(x, m * x + c) for x in range(-R, R + 1) if (m * x + c).denominator == 1 and abs(m * x + c) <= R]

def on(L, p): return L[0] * p[0] + L[1] == p[1]
def fs(f):
    f = Fr(f); s = (MINUS if f < 0 else "") + str(abs(f.numerator)) + ("" if f.denominator == 1 else "/" + str(f.denominator)); return s

# ---------- per question ----------
def check(q):
    en, ans, W, t = q["en"], q["answer"], q["wrong"], q["data"].get("t")
    opts = [ans] + W
    assert len(W) == 3, "fewer than 3 wrong options"
    assert len(set(opts)) == 4, "repeated option"
    pic = read_plane(q["html"]) if q["html"] else None
    hl = en.startswith("Higher Level: ")
    assert hl == (t in ("genslope", "genform", "perp", "perpeq", "pairperp")), "Higher Level label"
    def frac_opts(right):
        a = num(ans); assert a == right, f"answer {ans} should be {fs(right)}"
        for w in W: assert num(w) != right, f"wrong option {w} is also right"
    def pt_opts(right):
        assert pt(ans) == right, f"answer {ans} should be {right}"
        for w in W: assert pt(w) != right, f"wrong option {w} is the answer"
    def eq_opts(right):
        assert line_of(ans) == right, f"answer {ans} should be {right}"
        for w in W: assert line_of(w) != right, f"wrong option {w} is the same line"
    if t == "slope2":
        (A, B) = pts(en); frac_opts(Fr(B[1] - A[1]) / (B[0] - A[0]))
    elif t == "sgraph":
        L = pic["lines"]["l"]; A, B = pic["pts"]["A"], pic["pts"]["B"]
        assert on(L, A) and on(L, B), "A, B not on l"
        assert all(v.denominator == 1 for v in A + B), "A or B not on a grid point"
        assert Fr(B[1] - A[1]) / (B[0] - A[0]) == L[0]
        frac_opts(L[0])
    elif t == "sign":
        m = pic["lines"]["l"][0]; right = "Positive" if m > 0 else "Negative" if m < 0 else "Zero"
        assert ans == right, f"{ans} v {right}"
        assert len(lattice_on(pic["lines"]["l"], pic["R"])) >= 2
    elif t == "rate":
        (P0, P1) = pts(en); assert P0[0] == 0
        m = (P1[1] - P0[1]) / (P1[0] - P0[0]); c = P0[1]
        def val(o): return Fr(re.search(r"(\d+)", o).group(1))
        def is_rate(o): return " per " in o
        if q["data"]["q"] == "slope":
            assert "slope" in en and is_rate(ans) and val(ans) == m, ans
            for w in W: assert not (is_rate(w) and val(w) == m), w
        else:
            assert "y-axis" in en and not is_rate(ans) and val(ans) == c, ans
            for w in W: assert is_rate(w) or val(w) != c, w
        unit = re.search(r"with x in (\w+) and y in (\w+)", en).groups()
        per = {"hours": "per hour", "km": "per km", "minutes": "per minute", "months": "per month"}[unit[0]]
        for o in opts:
            if is_rate(o): assert per in o, "wrong unit"
            if unit[1] == "euro": assert "€" in o
            if unit[1] == "litres": assert "litres" in o
    elif t == "missk":
        m_ = re.fullmatch(r"The line through A\((−?\d+), k\) and B\((−?\d+), (−?\d+)\) has slope (−?\d+)\. Find k\.", en)
        x1, x2, y2, m = map(num, m_.groups()); frac_opts(y2 - m * (x2 - x1))
    elif t == "mid":
        A, B = pts(en); pt_opts(((A[0] + B[0]) / 2, (A[1] + B[1]) / 2))
    elif t == "midgraph":
        (A, B), = pic["segs"]; assert pic["pts"]["A"] == A and pic["pts"]["B"] == B
        pt_opts((Fr(A[0] + B[0], 2), Fr(A[1] + B[1], 2)))
    elif t == "end":
        M, A = pts(en); assert en.startswith("M(") and "A is" in en
        pt_opts((2 * M[0] - A[0], 2 * M[1] - A[1]))
    elif t in ("dist", "dist1", "distgraph"):
        if t == "distgraph":
            (A, B), = pic["segs"]; assert pic["pts"]["A"] == A and pic["pts"]["B"] == B
        else: A, B = pts(en)
        s2 = (B[0] - A[0]) ** 2 + (B[1] - A[1]) ** 2; d = math.sqrt(s2)
        if t == "dist":
            assert int(d) ** 2 == s2 and "decimal" not in en; frac_opts(Fr(int(d)))
        else:
            assert "to 1 decimal place" in en and round(d) ** 2 != s2
            for o in opts: assert re.fullmatch(r"\d+\.\d", o), f"not 1 d.p.: {o}"
            right = f"{d:.1f}"; assert abs(d * 10 - math.floor(d * 10) - 0.5) > 0.05, "rounding too close to call"
            assert ans == right, f"{ans} v {right}"
            for w in W: assert w != right
    elif t == "readm":
        L = line_of(re.fullmatch(r"What is the slope of the line (.*)\?", en).group(1)); frac_opts(L[0])
    elif t == "readc":
        L = line_of(re.fullmatch(r"Where does the line (.*) cross the y-axis\?", en).group(1)); pt_opts((0, L[1]))
    elif t == "whicheq":
        L = pic["lines"]["l"]; assert len(lattice_on(L, pic["R"])) >= 2, "line hard to read"
        assert L[1].denominator == 1 and abs(L[1]) <= pic["R"]
        eq_opts(L)
    elif t == "eqps":
        m_ = re.fullmatch(r"Find the equation of the line through \((−?\d+), (−?\d+)\) with slope (−?[\d/]+)\. Write it in the form y = mx \+ c\.", en)
        x1, y1, m = map(num, m_.groups()); eq_opts((m, y1 - m * x1))
    elif t == "eq2":
        A, B = pts(en); m = (B[1] - A[1]) / (B[0] - A[0]); eq_opts((m, A[1] - m * A[0]))
    elif t == "online":
        L = line_of(re.fullmatch(r"Which point is on the line (.*)\?", en).group(1))
        assert on(L, pt(ans)), ans
        for w in W: assert not on(L, pt(w)), f"{w} is also on the line"
    elif t == "findk":
        m_ = re.fullmatch(r"The point \((k|−?\d+), (k|−?\d+)\) is on the line (.*)\. Find k\.", en)
        a, b, e = m_.groups(); L = line_of(e)
        right = L[0] * num(a) + L[1] if b == "k" else (num(b) - L[1]) / L[0]
        assert (a == "k") != (b == "k"); frac_opts(right)
    elif t == "genslope":
        L = line_of(re.fullmatch(r"Higher Level: Find the slope of the line (.*)\.", en).group(1)); frac_opts(L[0])
    elif t == "genform":
        L = line_of(re.fullmatch(r"Higher Level: Write the line (.*) in the form y = mx \+ c\.", en).group(1)); eq_opts(L)
    elif t == "par":
        L = line_of(re.fullmatch(r"The line k is parallel to the line (.*)\. What is the slope of k\?", en).group(1)); frac_opts(L[0])
    elif t == "perp":
        L = line_of(re.fullmatch(r"Higher Level: The line k is perpendicular to the line (.*)\. What is the slope of k\?", en).group(1)); frac_opts(-1 / L[0])
    elif t in ("pareq", "perpeq"):
        m_ = re.fullmatch(r"(?:Higher Level: )?Find the equation of the line through P\((−?\d+), (−?\d+)\) that is (parallel|perpendicular) to (.*)\.", en)
        x1, y1, kind, e = m_.groups(); x1, y1 = num(x1), num(y1); L = line_of(e)
        m = L[0] if kind == "parallel" else -1 / L[0]
        assert (kind == "parallel") == (t == "pareq")
        if kind == "parallel": assert not on(L, (x1, y1)), "P is on the given line"
        eq_opts((m, y1 - m * x1))
    elif t in ("pairpar", "pairperp"):
        def ok(o):
            a, b = o.split(" and "); A, B = line_of(a), line_of(b)
            return (A[0] == B[0] and A[1] != B[1]) if t == "pairpar" else A[0] * B[0] == -1
        assert ok(ans), ans
        for w in W: assert not ok(w), f"{w} also works"
    elif t == "meetgraph":
        L1, L2 = pic["lines"]["l"], pic["lines"]["k"]; assert L1[0] != L2[0]
        x = (L2[1] - L1[1]) / (L1[0] - L2[0]); P = (x, L1[0] * x + L1[1])
        assert P[0].denominator == 1 and P[1].denominator == 1 and abs(P[0]) <= 4 and abs(P[1]) <= 4, "meeting point not readable"
        pt_opts(P)
    elif t == "both":
        a, b = re.fullmatch(r"Which point is on BOTH lines (.*) and (.*)\?", en).groups(); A, B = line_of(a), line_of(b)
        assert on(A, pt(ans)) and on(B, pt(ans)), ans
        for w in W: assert not (on(A, pt(w)) and on(B, pt(w))), w
    elif t == "xcross":
        L = line_of(re.fullmatch(r"Where does the line (.*) cross the x-axis\?", en).group(1)); pt_opts((-L[1] / L[0], 0))
    else:
        raise AssertionError("unknown type " + str(t))
    # wording checks on everything shown
    for txt in [en, q["why"]] + opts:
        assert "-" not in re.sub(r"(y-axis|x-axis|y-intercept|call-out|right-angled|x-coordinate|y-coordinate|straight-line)", "", txt), f"ASCII minus in: {txt}"
        assert not re.search(r"(?<![\d.])1x|−1y|\(\d+\)x|\+ −|− −(?!\d)|−0(?![.\d])|\b(\w+) \1\b", txt), f"wording: {txt}"
    for o in opts: assert "NaN" not in o and "undefined" not in o and "Infinity" not in o

if __name__ == "__main__":
    d = json.load(open(sys.argv[1]))
    bad = {}; n = 0
    for q in d:
        n += 1
        try: check(q)
        except Exception as e:
            k = (q["mk"], str(e)[:90]); bad.setdefault(k, q)
    for (mk, e), q in list(bad.items())[:40]:
        print(f"[{mk}] {e}\n   {q['en']} → {q['answer']} | {q['wrong']}")
    print(f"{n} questions, {len(bad)} kinds of problem")
