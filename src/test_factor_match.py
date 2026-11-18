#!/usr/bin/env python3
"""Independent checker for Factor Match (Order 27, factorising).
node src/test_factor_match.js > /tmp/fm.json ; python3 src/test_factor_match.py /tmp/fm.json   (env FM=<file> / N=<count> on the .js)
Works every answer out again from the question TEXT and the pictures with sympy (pip install --break-system-packages sympy).
A factorised answer must (1) multiply back to the question and (2) be FULLY factorised: every bracket has at least two terms,
no common factor inside (content 1, no letter in every term) and cannot be factorised again over the rationals."""
import json, re, sys
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
TR = standard_transformations + (implicit_multiplication_application,)
SUP = {"²": "**2", "³": "**3", "⁴": "**4", "⁵": "**5"}
LET = {c: sp.Symbol(c) for c in "abcdefghjkmnpqrstuvwxyz"}
Bx = sp.Symbol("B")
from functools import lru_cache
@lru_cache(maxsize=None)
def E(s, expand=True):
    s = s.replace("−", "-").replace("×", "*").replace("□", "B")
    s = re.sub(r"([a-zA-Z0-9)])([²³⁴⁵])", lambda m: m[1] + SUP[m[2]], s)
    s = re.sub(r"([a-zB])(?=[a-zB(])", r"\1*", s)
    s = re.sub(r"\)\(", ")*(", s)
    s = re.sub(r"(\d)\(", r"\1*(", s)
    e = parse_expr(s, transformations=TR, local_dict=dict(LET, B=Bx))
    return sp.expand(e) if expand else e
def N(s): return int(s.replace("−", "-").replace(",", ""))
def split_f(s):
    m = re.fullmatch(r"([^()]*)((?:\([^()]+\))+)", s)
    if not m: return None
    return m[1], re.findall(r"\(([^()]+)\)", m[2])
@lru_cache(maxsize=None)
def is_full(s):
    """is s a fully factorised form (outside monomial + irreducible primitive brackets)?"""
    sf = split_f(s)
    if sf is None: return False
    out, brs = sf
    if out not in ("", "−") and not re.fullmatch(r"−?\d*[a-z]*(²|³)?[a-z]?(²)?", out): return False
    for b in brs:
        e = E(b)
        if len(sp.Add.make_args(e)) < 2: return False
        P = sp.Poly(e, *sorted(e.free_symbols, key=str))
        if sp.gcd_list([int(c) for c in P.coeffs()]) != 1: return False
        c, fl = sp.factor_list(e)
        if sum(m for f, m in fl) != 1 or abs(c) != 1: return False
    return True
d = json.load(open(sys.argv[1]))
for q in d:
    for k in ("en","frame","why","answer"): q[k] = (q[k] or "").replace("\u00a0", " ")
    q["wrong"] = [w.replace("\u00a0", " ") for w in q["wrong"]]
probs = []
def bad(q, msg): probs.append((q["mk"], msg, q["en"], q["frame"], q["answer"], q["wrong"]))
def fac_q(q, true):
    true = sp.expand(true)
    if sp.expand(E(q["answer"]) - true) != 0: bad(q, "answer doesn't multiply back"); return
    if not is_full(q["answer"]): bad(q, "answer not fully factorised")
    full = "fully" in q["en"].lower()
    vals = []
    for w in q["wrong"]:
        if split_f(w) is None: bad(q, "wrong option not in factorised form: " + w)
        eq = sp.expand(E(w) - true) == 0
        if eq and (not full or is_full(w)): bad(q, "wrong option %s is also right" % w)
        if not eq:
            if any(sp.expand(E(w) - v) == 0 for v in vals): bad(q, "two wrong options equal")
            vals.append(E(w))
def expr_q(q, true):
    if sp.expand(E(q["answer"]) - true) != 0: bad(q, "answer %s should be %s" % (q["answer"], true))
    for w in q["wrong"]:
        if sp.expand(E(w) - true) == 0: bad(q, "wrong option equal")
def num_q(q, true):
    if N(q["answer"]) != true: bad(q, "answer %s should be %s" % (q["answer"], true))
    if any(N(w) == true for w in q["wrong"]): bad(q, "wrong option equals answer")
def one_right(q, valid):
    ok = [o for o in [q["answer"]] + q["wrong"] if valid(o)]
    if ok != [q["answer"]]: bad(q, "valid options: %s" % ok)
def solve_box(frame):
    L, R = frame.split(" = ")
    diff = sp.expand(E(L) - E(R))
    sol = sp.solve(diff, Bx)
    return sol
def is_dots(s):
    m = re.fullmatch(r"(\d*)([a-z])(²|³) − (\d+)", s)
    if not m: return False
    a = int(m[1] or 1); b = int(m[4])
    return m[3] == "²" and sp.sqrt(a).is_integer and sp.sqrt(b).is_integer
HL = {"qTriHL", "qDotsHL"}
for q in d:
    t = q["data"].get("t"); en = q["en"]; fr = q["frame"] or ""; h = q["html"] or ""
    allopts = [q["answer"]] + q["wrong"]
    if len(q["wrong"]) != 3 or q["answer"] in q["wrong"] or len(set(q["wrong"])) != 3: bad(q, "options"); continue
    if any(re.search(r"NaN|undefined|Infinity|null|\+ −|− −|\+ \+|− \+|(?<![\d.,])1[a-z]|(?<![a-z(])-\d|\b(\w+) \1\b", x) for x in [en, fr, q["why"]] + allopts): bad(q, "bad text")
    if any(re.search(r"([a-z])\1|\(\)", x) for x in allopts + [fr]): bad(q, "bad term")
    if (q["mk"] in HL) != en.startswith("Higher Level: "): bad(q, "Higher Level label")
    try:
      if "✓" in q["why"] and "Check" in q["why"]:
        m = re.search(r"Check by multiplying out: (.+?) = ([^,]+?)(?:,| ✓)", q["why"])
        if m and sp.expand(E(m[1]) - E(m[2])) != 0: bad(q, "check line wrong")
    except Exception as ex: bad(q, "check line unreadable " + repr(ex))
    try:
        if t == "hcf":
            ts = q["data"]["terms"]
            if fr != " and ".join(ts): bad(q, "frame")
            g = sp.gcd(E(ts[0]), E(ts[1]))
            if g.as_coeff_Mul()[0] < 0: g = -g
            expr_q(q, g)
        elif t == "fac":
            if not re.match(r"(?i)(Higher Level: )?(Factorise|Factorise fully|Factorise by grouping|Finish factorising):$", en): bad(q, "fac text")
            fac_q(q, E(fr))
        elif t == "fully":
            if not en.startswith("Which is the FULLY factorised form of"): bad(q, "text")
            fac_q(q, E(fr))
            ok = [o for o in allopts if is_full(o) and sp.expand(E(o) - E(fr)) == 0]
            if ok != [q["answer"]]: bad(q, "fully valid %s" % ok)
            if not any(sp.expand(E(w) - E(fr)) == 0 for w in q["wrong"]): bad(q, "no partial distractor")
        elif t == "box":
            sol = solve_box(fr)
            if len(sol) != 1: bad(q, "box not unique"); continue
            expr_q(q, sp.expand(sol[0]))
        elif t == "boxn":
            sol = solve_box(fr)
            if len(sol) != 1 or not sol[0].is_integer: bad(q, "box %s" % sol); continue
            num_q(q, int(sol[0]))
            # the left side must also be the expansion of what's written on the right with the box filled
        elif t == "rect":
            sides = re.findall(r'data-side="(\d)"[^>]*>([^<]+)<', h); area = re.search(r'data-area="([^"]+)"', h)[1]
            known = [s for i, s in sides if s != "?"]; unk = [i for i, s in sides if s == "?"]
            if len(known) != 1 or len(unk) != 1: bad(q, "sides"); continue
            if ("length" in en) != (unk[0] == "0") or ("width" in en) != (unk[0] == "1"): bad(q, "which side")
            other = sp.cancel(E(area) / E(known[0]))
            if sp.fraction(other)[1] != 1: bad(q, "not exact")
            expr_q(q, sp.expand(other))
        elif t == "pair":
            c, b = q["data"]["c"], q["data"]["b"]
            m = re.fullmatch(r"Which two numbers multiply to give (−?\d+) and add to give (−?\d+)\?", en)
            c, b = N(m[1]), N(m[2])
            def ok(o):
                u, v = [N(x) for x in o.split(" and ")]
                return u * v == c and u + v == b
            one_right(q, ok)
            # the pair must really factorise the trinomial
            u, v = [N(x) for x in q["answer"].split(" and ")]
            x = LET["x"]
            if sp.expand((x + u) * (x + v) - (x**2 + b * x + c)) != 0: bad(q, "pair")
        elif t == "tarea":
            m = re.search(r"add up to (.+)\. Which brackets", en); true = E(m[1])
            cells = [E(c[3]) for c in re.finditer(r'class="cell" data-i="(\d)" data-j="(\d)"[^>]*>([^<]+)<', h)]
            if len(cells) != 4 or sp.expand(sum(cells) - true) != 0: bad(q, "cells don't add up"); continue
            if re.findall(r'class="(?:rh|ch)" data-t="([^"]+)"', h) != ["?"] * 4: bad(q, "sides shown")
            fac_q(q, true)
            _, brs = split_f(q["answer"])
            A, B = [sp.Add.make_args(E(b)) for b in brs]
            prods = sorted(str(sp.expand(a * b)) for a in A for b in B)
            if prods != sorted(str(c) for c in cells): bad(q, "cells don't match the brackets")
        elif t == "isdots":
            one_right(q, is_dots)
        elif t == "dnum":
            m = re.fullmatch(r"(\d+)² − (\d+)²", fr)
            num_q(q, int(m[1])**2 - int(m[2])**2)
            if "factorising" not in en: bad(q, "text")
        elif t == "claim":
            m = re.search(r"writes: (.+) = (.+)\. Is (she|he) right\?", en); L, R = E(m[1]), E(m[2])
            right = sp.expand(L - R) == 0
            if not is_full(m[2]) and right: bad(q, "claim is equal but not fully factorised")
            def valid(o):
                if o == "Right": return right
                mm = re.fullmatch(r"Wrong: it should be (.+)", o)
                return (not right) and sp.expand(E(mm[1]) - L) == 0 and is_full(mm[1])
            one_right(q, valid)
        else: bad(q, "unknown type " + str(t))
    except Exception as ex:
        bad(q, "error " + repr(ex))
print(len(d), "questions checked,", len(probs), "problems")
seen = set()
for p in probs:
    if p[:2] in seen: continue
    seen.add(p[:2]); print(p)
