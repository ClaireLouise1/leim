#!/usr/bin/env python3
"""Independent checker for Pattern Builder. node src/test_pattern_builder.js > /tmp/pb.json ; python3 src/test_pattern_builder.py /tmp/pb.json
Re-derives every answer from the question TEXT, the tables and the SVG pictures (counts matchsticks/tiles, reads graph points).
Needs sympy (pip install --break-system-packages sympy)."""
import json, re, sys
from fractions import Fraction
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
TR = standard_transformations + (implicit_multiplication_application,)
def E(s):
    s = s.replace("−", "-").replace("Tₙ =", "")
    return sp.expand(parse_expr(s, transformations=TR, local_dict={c: sp.Symbol(c) for c in "nwmthdv"}))
def N(s): return int(s.replace("−", "-"))
def SEQ(s): return [N(x) for x in s.replace(", …", "").split(", ")]
def diffs(l): return [b - a for a, b in zip(l, l[1:])]
def const_d(l):
    ds = diffs(l); return ds[0] if len(set(ds)) == 1 else None
d = json.load(open(sys.argv[1]))
probs = []
def bad(q, msg): probs.append((q["mk"], msg, q["en"], q["frame"], q["answer"], q["wrong"]))
def num_q(q, true):
    if N(q["answer"]) != true: bad(q, "answer %s should be %s" % (q["answer"], true))
    if any(N(w) == true for w in q["wrong"]): bad(q, "wrong option equals answer")
def expr_q(q, true):
    if E(q["answer"]) != sp.expand(true): bad(q, "answer %s should be %s" % (q["answer"], true)); return
    for w in q["wrong"]:
        if sp.expand(E(w) - true) == 0: bad(q, "wrong option %s is equal to the answer" % w)
def one_right(q, valid):
    ok = [o for o in [q["answer"]] + q["wrong"] if valid(o)]
    if ok != [q["answer"]]: bad(q, "valid options: %s" % ok)
def stage_counts(h):
    out = {}
    for m in re.finditer(r'<g data-stage="(\d+)">(.*?)</g>', h, re.S):
        out[int(m[1])] = len(re.findall(r'<line class="m"', m[2])) + len(re.findall(r'<rect class="tile"', m[2]))
    return out
def pic_rule(q):
    c = stage_counts(q["html"]); l = [c[1], c[2], c[3]]; dd = const_d(l)
    if dd is None: raise ValueError("picture not linear %s" % l)
    return dd, l[0] - dd
def table(h):
    rows = {}
    for m in re.finditer(r'<tr data-row="(\w)">(.*?)</tr>', h, re.S):
        rows[m[1]] = [re.sub(r"<.*?>", "", c) for c in re.findall(r"<td[^>]*>(.*?)</td>", m[2])]
    return [int(x) for x in rows["n"]], rows["v"]
def points(h): return [(int(a), int(b)) for a, b in re.findall(r'<circle class="pt" data-x="(\d+)" data-y="(\d+)"', h)]
def rule_from(en):
    m = re.search(r"Tₙ = ([^.?]*?)(?: to fill| are plotted|\?)", en); return E(m[1])
n = sp.Symbol("n")
LIFE = [(r"has €(\d+) saved and adds €(\d+) every week", 1), (r"is (\d+) cm tall when \w+ plants it\. It grows (\d+) cm", 1),
        (r"€(\d+) joining fee plus €(\d+) a month", 1), (r"holds (\d+) litres of water\. A hose adds (\d+) litres", 1),
        (r"candle is (\d+) cm tall\. It burns down (\d+) cm", -1), (r"has €(\d+) of phone credit and uses €(\d+)", -1)]
for q in d:
    t = q["data"].get("t"); en = q["en"]; fr = q["frame"] or ""; h = q["html"] or ""
    opts = [q["answer"]] + q["wrong"]
    if len(q["wrong"]) != 3 or q["answer"] in q["wrong"] or len(set(q["wrong"])) != 3: bad(q, "options"); continue
    if any(re.search(r"NaN|undefined|Infinity|null|\+ −|− −|\+ \+|− \+|(?<![\d.,(])1[a-zA-Z]|(?<![\w(])-\d|\b1 (tiles|matchsticks|weeks|days|hours)\b|are 1 extra", x) for x in [en, fr, q["why"]] + opts):
        bad(q, "bad text")
    if any(re.search(r"[+−] 0\b", o) for o in opts): bad(q, "+ 0 in an option")
    try:
        if t == "next":
            l = fr.split(", "); i = l.index("?"); known = [(j, N(x)) for j, x in enumerate(l) if x != "?"]
            (j0, v0), (j1, v1) = known[0], known[1]; dd = (v1 - v0) // (j1 - j0)
            assert all(v == v0 + (j - j0) * dd for j, v in known); num_q(q, v0 + (i - j0) * dd)
        elif t == "jump":
            dd = const_d(SEQ(fr)); assert dd is not None; num_q(q, dd)
        elif t == "termk":
            k = int(re.search(r"the (\d+)th term", en)[1]); l = SEQ(fr); dd = const_d(l); num_q(q, l[0] + (k - 1) * dd)
        elif t in ("picnext", "picfar"):
            k = int(re.search(r"stage (\d+) need", en)[1]); dd, b = pic_rule(q); num_q(q, dd * k + b)
        elif t == "rulepic":
            dd, b = pic_rule(q); expr_q(q, dd * n + b)
        elif t == "ruleseq":
            l = SEQ(fr); dd = const_d(l); expr_q(q, dd * n + l[0] - dd)
        elif t == "ruletable":
            ns, vs = table(h); vs = [N(v) for v in vs]; dd = (vs[1] - vs[0]) // (ns[1] - ns[0])
            assert all(v == vs[0] + (x - ns[0]) * dd for x, v in zip(ns, vs)); expr_q(q, dd * n + vs[0] - dd * ns[0])
        elif t == "rulecheck":
            r = rule_from(en); true = [int(r.subs(n, i)) for i in (1, 2, 3, 4)]
            one_right(q, lambda o: SEQ(o) == true)
        elif t == "claim":
            m = re.search(r"general term of (.*?, …) is Tₙ = (.*?)\. Is", en); l = SEQ(m[1]); dd = const_d(l)
            true = dd * n + l[0] - dd; claim = E(m[2])
            def valid(o):
                if o == "Right": return sp.expand(claim - true) == 0
                return sp.expand(claim - true) != 0 and sp.expand(E(o.replace("Wrong: it should be ", "")) - true) == 0
            one_right(q, valid)
        elif t == "tablefill":
            r = rule_from(en); ns, vs = table(h)
            for x, v in zip(ns, vs):
                if v != "?" and N(v) != r.subs(n, x): bad(q, "table value wrong")
            num_q(q, int(r.subs(n, ns[vs.index("?")])))
        elif t in ("gstart", "grate", "gvalue", "grule"):
            p = points(h); dd = const_d([y for _, y in p]); assert dd is not None and [x for x, _ in p] == list(range(len(p))) and p[0][0] == 0
            b = p[0][1]
            if t == "gstart": num_q(q, b)
            elif t == "grate": num_q(q, dd)
            elif t == "gvalue": k = int(re.search(r"after (\d+) ", en)[1]); num_q(q, b + dd * k)
            else: v = sp.Symbol(re.search(r"value after (\w) ", en)[1]); expr_q(q, dd * v + b)
        elif t == "pointon":
            r = rule_from(en)
            def valid(o):
                x, y = [N(s) for s in o.strip("()").split(", ")]; return r.subs(n, x) == y
            one_right(q, valid)
        elif t == "linear":
            one_right(q, lambda o: const_d(SEQ(o)) is not None)
        elif t and t.startswith("life"):
            for pat, sg in LIFE:
                m = re.search(pat, en)
                if m: S, r = int(m[1]), sg * int(m[2]); break
            else: raise ValueError("no context")
            if t == "lifevalue": k = int(re.search(r"after (\d+) ", en)[1]); num_q(q, S + r * k)
            elif t == "lifestart": num_q(q, S)
            elif t == "liferate": num_q(q, r)
            elif t == "lifeformula": v = sp.Symbol(re.search(r"after (\w) \w+s\?", en)[1]); expr_q(q, r * v + S)
            elif t == "lifewhen":
                T = int(re.search(r"be €?(\d+)(?: cm| litres)?\?", en)[1]); k = Fraction(T - S, r); assert k.denominator == 1 and k > 0; num_q(q, int(k))
        elif t == "whichterm":
            m = re.search(r"pattern (.*?, …) is (\d+)\?", en); l = SEQ(m[1]); dd = const_d(l); k = Fraction(int(m[2]) - l[0], dd) + 1
            assert k.denominator == 1; num_q(q, int(k))
        elif t == "inpat":
            m = re.search(r"Is (\d+) a term of the pattern (.*?, …)\?", en); X = int(m[1]); l = SEQ(m[2]); dd = const_d(l)
            k = Fraction(X - l[0], dd) + 1; yes = k.denominator == 1 and k >= 1
            def valid(o):
                if o.startswith("No"): return not yes
                return yes and int(re.search(r"term (\d+)", o)[1]) == k
            one_right(q, valid)
        else: bad(q, "unknown type %s" % t)
    except Exception as e:
        bad(q, "error %r" % e)
for p in probs[:40]: print(p)
print(len(d), "questions,", len(probs), "problems")
