#!/usr/bin/env python3
"""Independent checker for Power Up (indices, roots & standard form).
node src/test_power_up.js > /tmp/pu.json ; python3 src/test_power_up.py /tmp/pu.json
Reads every question from its TEXT (superscripts, √, fractional indices in <sup>, standard form),
works the answer out itself with sympy, and checks the marked answer is the only right option."""
import json, re, sys
import sympy as sp
from sympy.parsing.sympy_parser import (parse_expr, standard_transformations,
                                        implicit_multiplication_application, rationalize)

SYM = {c: sp.Symbol(c, positive=True) for c in "xaynpk"}
TR = standard_transformations + (implicit_multiplication_application, rationalize)
SUP = {"⁰": "0", "¹": "1", "²": "2", "³": "3", "⁴": "4", "⁵": "5", "⁶": "6", "⁷": "7", "⁸": "8", "⁹": "9",
       "⁻": "-", "ⁿ": "n", "ˣ": "x"}
SUPRE = "[" + "".join(SUP) + "]+"


def tok(s):
    s = re.sub(r'<span class="ix">([^<]+)<sup>([^<]+)</sup></span>', r"(\1)^(\2)", s)
    s = re.sub(r"÷ ([^\s(]+)", r"÷ (\1)", s)   # "÷ 6n⁴" divides by the whole term
    s = s.replace("−", "-").replace("×", "*").replace("÷", "/")
    s = re.sub(r"(?<=\d),(?=\d{3})", "", s)
    s = re.sub(SUPRE, lambda m: "^(" + "".join(SUP[c] for c in m.group(0)) + ")", s)
    s = s.replace("^", "**")
    s = re.sub(r"√\(", "sqrt(", s)
    s = re.sub(r"√(\d+)", r"sqrt(\1)", s)
    return s


def E(s):
    return parse_expr(tok(s), local_dict=SYM, transformations=TR)


def eq(a, b):
    d = a - b
    return d == 0 or sp.expand(sp.powsimp(d, force=True)) == 0


SFRE = re.compile(r"^(\d(?:\.\d+)?) × 10(" + SUPRE + r")$")


def is_sf(s):
    m = SFRE.match(s)
    if not m:
        return False
    a = sp.Rational(m.group(1))
    return 1 <= a < 10 and not ("." in m.group(1) and m.group(1).endswith("0"))


PROBLEMS = []


def bad(q, msg):
    PROBLEMS.append((msg, q["mk"], q["en"], q["frame"], q["html"][:60], q["answer"], q["wrong"]))


def expr_of(q):
    return E(q["html"] if q["html"] and not q["frame"] else q["frame"])


SINGLE = re.compile(r"^(−?\d*(?:[a-z](?:" + SUPRE + r")?)+|\d+(?:" + SUPRE + r")?)$")


def check(q):
    t = q["data"].get("t")
    opts = [q["answer"]] + q["wrong"]
    texts = [q["en"], q["frame"] or "", q["why"] or ""] + opts
    for s in texts:
        if re.search(r"NaN|undefined|Infinity|\+ −|−−", s):
            bad(q, "bad text " + s)
        if re.search(r"(?<![\w\d.^])-\d", s) or re.search(r"\d - \d", s):
            bad(q, "ASCII minus " + s)
    if len(q["wrong"]) != 3 or len(set(opts)) != 4:
        bad(q, "options")
    if any(re.search(r"(?<![\d.,/])1[a-z]", o) for o in opts):
        bad(q, "1x in option")
    if t in ("eval", "simp"):
        v = expr_of(q)
        a = E(q["answer"])
        if not eq(v, a):
            bad(q, "answer wrong %s v %s" % (v, a))
        for w in q["wrong"]:
            if eq(v, E(w)):
                bad(q, "wrong option is right: " + w)
        if t == "simp" and not SINGLE.match(q["answer"]):
            bad(q, "answer not one term")
    elif t == "pow":
        m = re.search(r"Write (1/)?([\d,]+) as a power of (\d+)", q["en"], re.I)
        N = sp.Rational(1, int(m.group(2).replace(",", ""))) if m.group(1) else sp.Integer(int(m.group(2).replace(",", "")))
        b = m.group(3)
        if not re.match("^" + b + SUPRE + "$", q["answer"]) or E(q["answer"]) != N:
            bad(q, "pow answer")
        for w in q["wrong"]:
            if E(w) == N:
                bad(q, "pow wrong equals")
    elif t in ("big", "small"):
        vals = [E(o) for o in opts]
        if len(set(vals)) != 4:
            bad(q, "equal values")
        best = max(vals) if t == "big" else min(vals)
        if vals[0] != best or vals.count(best) != 1:
            bad(q, "not the " + t)
    elif t == "between":
        N = int(re.search(r"√(\d+)", q["en"]).group(1))
        lo, hi = map(int, q["answer"].split(" and "))
        if not (hi == lo + 1 and lo * lo < N < hi * hi):
            bad(q, "between")
        for w in q["wrong"]:
            l2, h2 = map(int, w.split(" and "))
            if l2 * l2 < N < h2 * h2:
                bad(q, "between wrong ok")
    elif t == "claim":
        tr = []
        for o in opts:
            L, R = o.split(" = ")
            tr.append(eq(E(L), E(R)))
        if tr != [True, False, False, False]:
            bad(q, "claims %s" % tr)
    elif t == "equiv":
        x = E(re.search(r"equals (.+)\?", q["en"]).group(1))
        if [eq(x, E(o)) for o in opts] != [True, False, False, False]:
            bad(q, "equiv")
    elif t == "findn":
        L, R = q["frame"].split(" = ")
        n = SYM["n"]
        s = [r for r in sp.solve(sp.Eq(E(L), E(R)), n) if r.is_real]
        if len(s) != 1 or s[0] != E(q["answer"]):
            bad(q, "findn %s" % s)
        for w in q["wrong"]:
            if E(w) == s[0]:
                bad(q, "findn wrong")
    elif t == "solvex":
        L, R = q["frame"].split(" = ")
        b = int(L.replace("ˣ", ""))
        v = E(R)
        xv = sp.nsimplify(sp.log(v) / sp.log(b))
        if not xv.is_Rational or b ** xv != v or E(q["answer"]) != xv:
            bad(q, "solvex %s" % xv)
        for w in q["wrong"]:
            if E(w) == xv:
                bad(q, "solvex wrong")
    elif t in ("sf", "sfcalc"):
        if q["frame"]:
            v = E(q["frame"])
        else:
            v = sp.Integer(int(re.search(r"(\d[\d,]{3,})", q["en"]).group(1).replace(",", "")))
        if not is_sf(q["answer"]) or not eq(E(q["answer"]), v):
            bad(q, "sf answer")
        for w in q["wrong"]:
            if is_sf(w) and eq(E(w), v):
                bad(q, "sf wrong is right")
    elif t == "fromsf":
        v = E(q["frame"])
        if "×" in q["answer"] or E(q["answer"]) != v:
            bad(q, "fromsf")
        if re.search(r"\.\d*0$|^\.", q["answer"]):
            bad(q, "decimal format")
        for w in q["wrong"]:
            if E(w) == v:
                bad(q, "fromsf wrong")
    elif t == "issf":
        if [is_sf(o) for o in opts] != [True, False, False, False]:
            bad(q, "issf %s" % [is_sf(o) for o in opts])
    else:
        bad(q, "unknown type %s" % t)


if __name__ == "__main__":
    data = json.load(open(sys.argv[1]))
    for q in data:
        try:
            check(q)
        except Exception as e:
            bad(q, "crash %r" % e)
    from collections import Counter
    print(len(data), "questions,", len(PROBLEMS), "problems")
    print(Counter(p[0][:30] for p in PROBLEMS).most_common(12))
    for p in PROBLEMS[:25]:
        print(p)
