#!/usr/bin/env python3
"""Independent checker for Bracket Blaster (Order 15, Algebra 2).
node src/test_bracket_blaster.js > /tmp/bb.json ; python3 src/test_bracket_blaster.py /tmp/bb.json
Re-derives every answer from the question TEXT and the SVG pictures with sympy (pip install --break-system-packages sympy)."""
import json, re, sys
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
TR = standard_transformations + (implicit_multiplication_application,)
SUP = {"²": "**2", "³": "**3", "⁴": "**4", "⁵": "**5"}
LET = {c: sp.Symbol(c) for c in "abcdkmnpqtxy"}
def E(s):
    s = s.replace("−", "-").replace("×", "*").replace("□", "B")
    s = re.sub(r"([a-z0-9)])([²³⁴⁵])", lambda m: m[1] + SUP[m[2]], s)
    s = re.sub(r"([a-z])(?=[a-z(])", r"\1*", s)          # ab → a*b, x(… → x*(…
    s = re.sub(r"\)\(", ")*(", s)
    s = re.sub(r"(\d)\(", r"\1*(", s)
    return sp.expand(parse_expr(s, transformations=TR, local_dict=dict(LET, B=sp.Symbol("B"))))
def N(s): return int(s.replace("−", "-"))
def nterms(s): return len(re.split(r"(?<=\S) [+−] ", s))
d = json.load(open(sys.argv[1]))
probs = []
def bad(q, msg): probs.append((q["mk"], msg, q["en"], q["frame"], q["answer"], q["wrong"]))
def expr_q(q, true, simplest=True):
    true = sp.expand(true)
    if sp.expand(E(q["answer"]) - true) != 0: bad(q, "answer %s should be %s" % (q["answer"], true)); return
    if simplest and ("(" in q["answer"] or nterms(q["answer"]) != len(sp.Add.make_args(true))): bad(q, "answer not expanded/simplified")
    for w in q["wrong"]:
        if sp.expand(E(w) - true) == 0: bad(q, "wrong option %s is equal to the answer" % w)
def num_q(q, true):
    if N(q["answer"]) != true: bad(q, "answer %s should be %s" % (q["answer"], true))
    if any(N(w) == true for w in q["wrong"]): bad(q, "wrong option equals answer")
def one_right(q, valid):
    ok = [o for o in [q["answer"]] + q["wrong"] if valid(o)]
    if ok != [q["answer"]]: bad(q, "valid options: %s" % ok)
def heads(h, cls): return [E(m) for m in re.findall(r'class="%s" data-t="([^"]+)"' % cls, h)]
for q in d:
    t = q["data"].get("t"); en = q["en"]; fr = q["frame"] or ""; h = q["html"] or ""
    allopts = [q["answer"]] + q["wrong"]
    if len(q["wrong"]) != 3 or q["answer"] in q["wrong"] or len(set(q["wrong"])) != 3: bad(q, "options"); continue
    if any(re.search(r"NaN|undefined|Infinity|null|\+ −|− −|\+ \+|− \+|(?<![\d.])1[a-z]|(?<![a-z(])-\d", x) for x in [en, fr, q["why"]] + allopts) or any(re.search(r"[a-z][²³⁴][a-z]|([a-z])\1", x) for x in allopts + [fr]): bad(q, "bad text")
    try:
        if t == "exp":
            if not re.match(r"(Higher Level: )?(Expand|Expand and simplify|Multiply):$", en, re.I): bad(q, "exp text")
            expr_q(q, E(fr))
        elif t == "area":
            rows, cols = heads(h, "rh"), heads(h, "ch")
            shown = E(fr)
            true = sp.expand(sum(rows) * sum(cols))
            if sp.expand(shown - true) != 0: bad(q, "picture %s doesn't match %s" % (true, m[1]))
            for c in re.finditer(r'class="cell" data-i="(\d)" data-j="(\d)"[^>]*>([^<]+)<', h):
                if c[3] != "?" and sp.expand(E(c[3]) - rows[int(c[1])] * cols[int(c[2])]) != 0: bad(q, "cell wrong")
            expr_q(q, true)
        elif t == "cell":
            rows, cols = heads(h, "rh"), heads(h, "ch")
            if sp.expand(E(fr) - sum(rows) * sum(cols)) != 0: bad(q, "picture doesn't match text")
            ys = [(int(c[1]), int(c[2])) for c in re.finditer(r'class="cell" data-i="(\d)" data-j="(\d)"[^>]*>\?<', h)]
            if len(ys) != 1: bad(q, "yellow cells %s" % ys); continue
            for c in re.finditer(r'class="cell" data-i="(\d)" data-j="(\d)"[^>]*>([^<?]+)<', h):
                if sp.expand(E(c[3]) - rows[int(c[1])] * cols[int(c[2])]) != 0: bad(q, "shown cell wrong")
            i, j = ys[0]; expr_q(q, rows[i] * cols[j])
        elif t == "middle":
            L, R = fr.split(" = "); x = LET["x"]; B = sp.Symbol("B")
            e = E(L); r = E(R)
            # the box must make both sides equal for every x
            sol = sp.solve(sp.Poly(e - r, x).all_coeffs(), B, dict=True)
            if len(sol) != 1: bad(q, "box not unique"); continue
            num_q(q, int(sol[0][B]))
        elif t == "rect":
            sides = [E(s) for s in re.findall(r'data-side="\d"[^>]*>([^<]+)<', h)]
            if len(sides) != 2 or "area" not in en: bad(q, "shape"); continue
            expr_q(q, sides[0] * sides[1])
        elif t == "equal":
            tgt = E(q["data"]["target"])
            if q["data"]["target"] not in en: bad(q, "target text")
            one_right(q, lambda o: sp.expand(E(o) - tgt) == 0)
        elif t == "claim":
            m = re.search(r"writes: (.+) = (.+)\. Is (she|he) right\?", en); L, R = E(m[1]), E(m[2])
            right = sp.expand(L - R) == 0
            def valid(o):
                if o == "Right": return right
                mm = re.fullmatch(r"Wrong: it should be (.+)", o)
                return (not right) and sp.expand(E(mm[1]) - L) == 0
            one_right(q, valid)
        elif t == "line":
            prev = E(fr)
            lines = re.findall(r'data-line="(\d)"><b>Line \d:</b> ([^<]+)<', h)
            if len(lines) != 3: bad(q, "lines"); continue
            first = "No mistake"
            for n, s in lines:
                if "(" in s: bad(q, "bracket left in a line")
                e = E(s)
                if sp.expand(e - prev) != 0: first = "Line " + n; break
                prev = e
            if lines[2][1].count("x") > 1: bad(q, "line 3 not collected")
            if q["answer"] != first: bad(q, "first mistake is %s, game says %s" % (first, q["answer"]))
        elif t == "sub":
            w = re.fullmatch(r"Find the value when (\w) = (−?\d+):", en)
            num_q(q, int(E(fr).subs(LET[w[1]], N(w[2]))))
        else: bad(q, "unknown type " + str(t))
    except Exception as ex:
        bad(q, "error " + repr(ex))
print(len(d), "questions checked,", len(probs), "problems")
seen = set()
for p in probs:
    if p[:2] in seen: continue
    seen.add(p[:2]); print(p)
