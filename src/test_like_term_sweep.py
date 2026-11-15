#!/usr/bin/env python3
"""Independent checker for Like-Term Sweep. node src/test_like_term_sweep.js > /tmp/lts.json ; python3 src/test_like_term_sweep.py /tmp/lts.json
Re-derives every answer from the question TEXT (and the SVG pictures) with sympy (pip install sympy)."""
import json, re, sys
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
TR = standard_transformations + (implicit_multiplication_application,)
SUP = {"²": "**2", "³": "**3", "⁴": "**4"}
def E(s):
    s = s.replace("−", "-").replace("×", "*").replace("÷", "/").replace("“", "").replace("”", "")
    s = re.sub(r"([a-z0-9)])([²³⁴])", lambda m: m[1] + SUP[m[2]], s)
    s = re.sub(r"([a-z])(?=[a-z])", r"\1*", s)          # ab → a*b (single-letter variables only)
    return sp.expand(parse_expr(s, transformations=TR, local_dict={c: sp.Symbol(c) for c in "abcdkmnpqtxyhgCD"}))
def N(s): return int(s.replace("−", "-"))
d = json.load(open(sys.argv[1]))
probs = []
def bad(q, msg): probs.append((q["mk"], msg, q["en"], q["frame"], q["answer"], q["wrong"]))
def expr_q(q, true):
    if E(q["answer"]) != sp.expand(true): bad(q, "answer %s should be %s" % (q["answer"], true)); return
    for w in q["wrong"]:
        if sp.expand(E(w) - true) == 0: bad(q, "wrong option %s is equal to the answer" % w)
def num_q(q, true):
    if N(q["answer"]) != true: bad(q, "answer %s should be %s" % (q["answer"], true))
    if any(N(w) == true for w in q["wrong"]): bad(q, "wrong option equals answer")
def one_right(q, valid):
    ok = [o for o in [q["answer"]] + q["wrong"] if valid(o)]
    if ok != [q["answer"]]: bad(q, "valid options: %s" % ok)
WORDS = [(r"(\d+) more than (\d+) times (\w)", lambda a, b, v: f"{b}{v}+{a}"),
         (r"(\d+) less than (\d+) times (\w)", lambda a, b, v: f"{b}{v}-{a}"),
         (r"(\d+) times (\w), taken away from (\d+)", lambda a, v, b: f"{b}-{a}{v}"),
         (r"(\d+) less than (\w), then multiplied by (\d+)", lambda a, v, b: f"{b}*({v}-{a})"),
         (r"(\d+) more than (\w)", lambda a, v: f"{v}+{a}"), (r"(\d+) less than (\w)", lambda a, v: f"{v}-{a}"),
         (r"(\w) multiplied by (\d+)", lambda v, a: f"{a}*{v}"), (r"(\d+) times (\w), then add (\d+)", lambda a, v, b: f"{a}*{v}+{b}"),
         (r"double (\w), then subtract (\d+)", lambda v, a: f"2*{v}-{a}"), (r"(\w) squared, plus (\d+)", lambda v, a: f"{v}**2+{a}"),
         (r"subtract (\w) from (\d+)", lambda v, a: f"{a}-{v}"), (r"(\w) cubed", lambda v: f"{v}**3"),
         (r"(half|a third|a quarter) of (\w), then add (\d+)", lambda f, v, a: f"{v}/{ {'half': 2, 'a third': 3, 'a quarter': 4}[f]}+{a}"),
         (r"(half|a third|a quarter) of (\w)", lambda f, v: f"{v}/{ {'half': 2, 'a third': 3, 'a quarter': 4}[f]}")]
def words(s):
    for pat, f in WORDS:
        m = re.fullmatch(pat, s)
        if m: return E(f(*m.groups()))
    raise ValueError("no grammar for " + s)
for q in d:
    t = q["data"].get("t"); en = q["en"]; fr = q["frame"] or ""; h = q["html"] or ""
    allopts = [q["answer"]] + q["wrong"]
    if len(q["wrong"]) != 3 or q["answer"] in q["wrong"] or len(set(q["wrong"])) != 3: bad(q, "options"); continue
    if any(re.search(r"NaN|undefined|Infinity|null|\+ −|− −|\+ \+|− \+|(?<![\d.])1[a-z]|(?<![a-z(])-\d", x) for x in [en, fr, q["why"]] + allopts): bad(q, "bad text")
    try:
        if t == "simp" or t == "equiv":
            expr_q(q, E(fr))
            if t == "simp" and len(sp.Add.make_args(E(q["answer"]))) != len(re.split(r" [+−] ", q["answer"])): bad(q, "answer not simplest")
        elif t == "like":
            tgt = E(q["data"]["target"])
            def like(o):
                e = E(o); r = sp.simplify(e / tgt); return r.is_number and r != 0
            one_right(q, like)
        elif t in ("coef", "const", "count"):
            e = E(fr); syms = sorted(e.free_symbols, key=str)
            if t == "coef":
                v = sp.Symbol(q["data"]["v"]); true = sp.Poly(e, *syms).coeff_monomial(v)
                if not re.search(r"what is the coefficient of %s\b" % q["data"]["v"], en, re.I): bad(q, "coef text")
            elif t == "const": true = sp.Poly(e, *syms).coeff_monomial(1)
            else: true = len(sp.Add.make_args(e))
            num_q(q, int(true))
        elif t == "tiles":
            n2, nx, n1 = h.count('class="t2"'), h.count('class="tx"'), h.count('class="t1"'); x = sp.Symbol("x")
            expr_q(q, n2 * x ** 2 + nx * x + n1)
        elif t == "words" or t == "half":
            expr_q(q, words(fr.strip("“”")))
        elif t == "read":
            e = E(fr); one_right(q, lambda o: sp.expand(words(o) - e) == 0)
        elif t == "cost":
            ints = [int(z) for z in re.findall(r"\d+", en)]
            if q["data"]["c"] == "cinema": p, f = ints; true = p * sp.Symbol("n") + f
            elif q["data"]["c"] == "taxi": f, p = ints; true = p * sp.Symbol("d") + f
            elif q["data"]["c"] == "ages": k, m = ints; x = sp.Symbol("x"); true = x + (x + k) + m * x
            else: k, m = ints; true = sp.Symbol("n") - k + m
            expr_q(q, true)
        elif t == "perim":
            sides = [E(s) for s in re.findall(r'data-side="\d"[^>]*>([^<]+)<', h)]
            kind = re.search(r'data-shape="(\w+)"', h)[1]
            true = 2 * sum(sides) if kind == "rect" else sum(sides)
            if len(sides) != (2 if kind == "rect" else 3) or (kind == "rect") != ("rectangle" in en): bad(q, "shape")
            expr_q(q, true)
        elif t == "sub":
            vals = dict((m[1], N(m[2])) for m in re.finditer(r"(\w) = (−?\d+)", en))
            reels = dict((m[1], int(m[2])) for m in re.finditer(r'data-v="(\w)" data-n="(-?\d+)"', h))
            if vals != reels: bad(q, "reels %s v text %s" % (reels, vals))
            num_q(q, int(E(fr).subs({sp.Symbol(k): v for k, v in vals.items()})))
        elif t == "formula":
            m = re.search(r"\b([A-Z]) = (−?[\w ²+−]+?)(?:,| euro| metres|\.)", en); f = E(m[2])
            w = re.search(r"Find \w when (\w) = (−?\d+)\.", en)
            if m[1] not in en.split("Find")[1]: bad(q, "formula letter")
            reels = re.search(r'data-v="(\w)" data-n="(-?\d+)"', h)
            if (reels[1], int(reels[2])) != (w[1], N(w[2])): bad(q, "reel")
            num_q(q, int(f.subs(sp.Symbol(w[1]), N(w[2]))))
        elif t == "notation":
            expr_q(q, E(fr))
        elif t == "claim":
            m = re.search(r"writes: (.+) = (.+)\. Is (she|he) right\?", en); L, R = E(m[1]), E(m[2])
            right = sp.expand(L - R) == 0
            unlike = len(sp.Add.make_args(L)) == len(re.split(r" [+−] ", m[1]))
            def valid(o):
                if o == "Right": return right
                if o == "Wrong: the order matters": return False
                if o == "Wrong: it can't be simplified": return (not right) and unlike
                mm = re.fullmatch(r"Wrong: it should be (.+)", o)
                return (not right) and sp.expand(E(mm[1]) - L) == 0
            one_right(q, valid)
        else: bad(q, "unknown type " + str(t))
    except Exception as ex:
        bad(q, "error " + repr(ex))
print(len(d), "questions checked,", len(probs), "problems")
seen = set()
for p in probs:
    if p[:2] in seen: continue
    seen.add(p[:2]); print(p)
