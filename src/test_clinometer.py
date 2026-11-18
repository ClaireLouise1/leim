#!/usr/bin/env python3
"""Independent checker for Clinometer Challenge (JC Maths topic 32, trigonometry).
node src/test_clinometer.js > /tmp/cc.json ; python3 src/test_clinometer.py /tmp/cc.json   (env TL=<file> tests a mutated copy, N=<count> per maker)
It MEASURES every diagram: the shaded right-angled triangle, the right-angle mark (90°), the marked angle
(measured against its label; an angle of depression is measured from the horizontal), every labelled length
against the drawing's scale data-s. It then solves the triangle itself from the LABELS (its own sin/cos/tan
choice, half-up rounding), parses every text question with its own regexes and evaluates every option of the
"which calculation / which ratio" questions, requiring exactly one to be right."""
import json, re, sys, math, collections
from fractions import Fraction as Fr
from decimal import Decimal, ROUND_HALF_UP

def attrs(tag): return dict(re.findall(r'([\w-]+)="([^"]*)"', tag))
def P(s): return tuple(float(v) for v in s.split(","))
def f(p): return (p[0], -p[1])
def read_svg(html):
    m = re.search(r'<svg class="pf"[^>]*>', html or "")
    if not m: return None
    D = {"s": float(attrs(m.group(0)).get("data-s", 0) or 0), "lines": [], "marks": [], "lens": [], "polys": [], "names": {}}
    for t in re.findall(r'<line class="ln"[^>]*/>', html):
        a = attrs(t); D["lines"].append(((float(a["x1"]), -float(a["y1"])), (float(a["x2"]), -float(a["y2"]))))
    for g in re.findall(r'<g class="am"[^>]*>', html):
        a = attrs(g); D["marks"].append({"v": f(P(a["data-v"])), "p": f(P(a["data-p"])), "q": f(P(a["data-q"])), "l": a["data-l"]})
    for t, txt in re.findall(r'(<text class="ll"[^>]*>)([^<]*)</text>', html):
        a = attrs(t); D["lens"].append({"a": f(P(a["data-a"])), "b": f(P(a["data-b"])), "t": txt})
    for t in re.findall(r'<polygon class="tri"[^>]*/>', html):
        D["polys"].append([f(P(x)) for x in attrs(t)["data-pts"].split()])
    for t, txt in re.findall(r'(<text class="vn"[^>]*>)([^<]*)</text>', html):
        D["names"][txt] = f(P(attrs(t)["data-p"]))
    return D
def dist(a, b): return math.hypot(a[0] - b[0], a[1] - b[1])
def angle(v, p, q):
    x = abs(math.degrees(math.atan2(p[1] - v[1], p[0] - v[0]) - math.atan2(q[1] - v[1], q[0] - v[0]))) % 360
    return 360 - x if x > 180 else x
def same(p, q, t=0.6): return dist(p, q) <= t

class Bad(Exception): pass
def need(c, msg):
    if not c: raise Bad(msg)
def val(s):
    m = re.fullmatch(r'(\d+(?:\.\d+)?)(?: (mm|cm|m|km))?', s.strip())
    return (Fr(m.group(1)), m.group(2) or "") if m else (None, None)
def half_up(x, dp):
    q = Decimal(1).scaleb(-dp)
    return Decimal(repr(x)).quantize(q, rounding=ROUND_HALF_UP)
def not_edge(x, dp):
    t = x * 10 ** dp - math.floor(x * 10 ** dp)
    need(abs(t - 0.5) > 0.004, "too close to a rounding boundary: %r" % x)
S_ = lambda a: math.sin(math.radians(a)); C_ = lambda a: math.cos(math.radians(a)); T_ = lambda a: math.tan(math.radians(a))

def triangle(D):
    """returns dict: R (right-angle vertex), V (marked vertex), W (third), alpha (angle at V, or None if unknown θ),
    edges {'o','a','h'} as (p,q) relative to V, known {'o':val}, unk (which edge is x, or None), unit, extra labels"""
    need(D and D["s"] > 0, "no scaled figure"); need(len(D["polys"]) == 1, "need one triangle")
    tri = D["polys"][0]; need(len(tri) == 3, "triangle has 3 vertices")
    rts = [m for m in D["marks"] if m["l"] == "rt"]; need(len(rts) == 1, "one right-angle mark")
    R = rts[0]["v"]; need(any(same(R, p) for p in tri), "right angle not at a vertex")
    need(abs(angle(R, rts[0]["p"], rts[0]["q"]) - 90) < 0.3, "right-angle mark isn't 90°")
    others = [p for p in tri if not same(p, R)]; need(abs(angle(R, others[0], others[1]) - 90) < 0.3, "triangle not right-angled")
    am = [m for m in D["marks"] if m["l"] != "rt"]; need(len(am) == 1, "one angle mark")
    m = am[0]; V = m["v"]; need(any(same(V, p) for p in others), "angle mark not at a non-right vertex")
    W = others[1] if same(V, others[0]) else others[0]
    inner = angle(V, R, W); markm = angle(V, m["p"], m["q"])
    if m["l"] == "θ":
        need(abs(markm - inner) < 0.6, "θ mark isn't the triangle's angle"); alpha, label = None, None
    else:
        need(re.fullmatch(r'\d+', m["l"]), "odd angle label " + m["l"]); label = int(m["l"])
        need(abs(markm - label) < 0.6, "angle labelled %s but drawn %.2f" % (label, markm))
        if abs(markm - inner) < 0.6: alpha = label
        else:   # angle of depression: measured from the horizontal, which is perpendicular to the edge V–R
            need(abs(markm + inner - 90) < 0.6, "marked angle is neither the angle nor its complement")
            ray = m["p"] if angle(V, m["p"], W) < angle(V, m["q"], W) and abs(angle(V, m["p"], R) - 90) < 0.6 else m["q"]
            hz = [x for x in (m["p"], m["q"]) if abs(angle(V, x, R) - 90) < 0.6]
            need(hz, "depression mark has no horizontal ray"); alpha = 90 - label
    edges = {"o": (R, W), "a": (V, R), "h": (V, W)}
    known, unk, unit, extra = {}, None, set(), []
    for l in D["lens"]:
        drawn = dist(l["a"], l["b"]) / D["s"]
        k = [e for e, (p, q) in edges.items() if (same(p, l["a"]) and same(q, l["b"])) or (same(p, l["b"]) and same(q, l["a"]))]
        need(any((same(a, l["a"]) and same(b, l["b"])) or (same(a, l["b"]) and same(b, l["a"])) for a, b in D["lines"]), "label on no line")
        if l["t"] in ("x", "?"):
            need(len(k) == 1 and unk is None, "unknown label"); unk = k[0]; continue
        v, u = val(l["t"]); need(v is not None, "odd label " + l["t"]); unit.add(u)
        need(abs(float(v) - drawn) < 0.003 * float(v) + 0.01, "label %s drawn %.3f" % (l["t"], drawn))
        if k: known[k[0]] = v
        else: extra.append(v)
    # the drawing itself must be a right-angled triangle with angle alpha at V
    if alpha is not None:
        dO, dA, dH = (dist(*edges[e]) for e in "oah")
        need(abs(math.degrees(math.atan2(dO, dA)) - alpha) < 0.3, "drawn angle at V isn't %s" % alpha)
    return {"alpha": alpha, "known": known, "unk": unk, "unit": unit, "extra": extra, "edges": edges, "D": D, "V": V, "R": R, "W": W}

def solve(T):
    """all three sides from the angle and one known side (independent formulas)"""
    a = T["alpha"]; need(a is not None, "no angle"); k = T["known"]; need(len(k) == 1, "need exactly one known side, have %s" % list(k))
    (e, v), = k.items(); v = float(v)
    h = {"h": v, "o": v / S_(a), "a": v / C_(a)}[e]
    return {"h": h, "o": h * S_(a), "a": h * C_(a)}
def solve_angle(T):
    k = {e: float(v) for e, v in T["known"].items()}; need(len(k) == 2 and T["unk"] is None, "angle question needs 2 sides")
    if "o" in k and "h" in k: need(k["o"] < k["h"], "opp ≥ hyp"); return math.degrees(math.asin(k["o"] / k["h"]))
    if "a" in k and "h" in k: need(k["a"] < k["h"], "adj ≥ hyp"); return math.degrees(math.acos(k["a"] / k["h"]))
    return math.degrees(math.atan(k["o"] / k["a"]))

def opts_len(q, exp, unit):
    vals = []
    for o in [q["answer"]] + q["wrong"]:
        m = re.fullmatch(r'(\d+\.\d) (cm|m)', o); need(m, "not 1 d.p. with a unit: " + o)
        need(m.group(2) == unit, "unit differs: " + o); vals.append(Decimal(m.group(1)))
    need(len(set(vals)) == 4, "options equal in value"); need(all(v > 0 for v in vals), "option ≤ 0")
    need(vals[0] == exp, "answer %s expected %s" % (q["answer"], exp))
def opts_deg(q, exp):
    vals = []
    for o in [q["answer"]] + q["wrong"]:
        m = re.fullmatch(r'(\d+)°', o); need(m, "not whole degrees: " + o); v = int(m.group(1)); need(0 < v < 90, "angle out of range " + o); vals.append(v)
    need(len(set(vals)) == 4, "options equal"); need(vals[0] == exp, "answer %s expected %s°" % (q["answer"], exp))

def check_fig(q):
    T = triangle(read_svg(q["html"])); need(len(T["unit"]) == 1, "units"); unit = T["unit"].pop()
    if T["alpha"] is None:
        th = solve_angle(T); need("(to the nearest degree)" in q["en"], "no rounding instruction"); not_edge(th, 0)
        opts_deg(q, int(half_up(th, 0))); return
    need(T["unk"] is not None and T["unk"] != "?", "no x"); x = solve(T)[T["unk"]]
    need("(to 1 d.p.)" in q["en"], "no rounding instruction"); not_edge(x, 1)
    need(not T["extra"], "extra labels"); opts_len(q, half_up(x, 1), unit)
    need(q["answer"].split()[0] in q["why"], "why doesn't show the answer")

def check_eye(q):
    T = triangle(read_svg(q["html"])); m = re.search(r"'s eyes are (\d+(?:\.\d+)?) m above the ground\. How tall is the (tree|building|tower|flagpole)\? \(to 1 d\.p\.\)$", q["en"]); need(m, "parse eye")
    e = Fr(m.group(1)); need(T["extra"] == [e], "eye height not drawn"); need(T["unk"] is None, "no x expected")
    S = solve(T); x = S["o"] + float(e); not_edge(x, 1); opts_len(q, half_up(x, 1), "m")

def check_name(q):
    T = triangle(read_svg(q["html"])); need(q["en"] == "Name the side marked ?", "text")
    D = T["D"]; qs = [l for l in D["lens"] if l["t"] == "?"]; need(len(qs) == 1 and not T["known"], "one ? label")
    exp = {"o": "Opposite", "a": "Adjacent", "h": "Hypotenuse"}[T["unk"]]
    need(q["answer"] == exp, "name %s expected %s" % (q["answer"], exp))
    need(sorted(q["wrong"]) == sorted({"Opposite", "Adjacent", "Hypotenuse"} - {exp}), "options")

RATIO = {frozenset("oh"): "sin", frozenset("ah"): "cos", frozenset("oa"): "tan"}
def check_whichratio(q):
    T = triangle(read_svg(q["html"])); need(T["alpha"] is None and len(T["known"]) == 2, "two sides")
    k = T["known"]; S = solve_angle(T)   # also checks the sides are consistent with each other
    exp = RATIO[frozenset(k)]; need(q["answer"] == exp and sorted(q["wrong"]) == sorted({"sin", "cos", "tan"} - {exp}), "ratio %s expected %s" % (q["answer"], exp))

def check_frac(q):
    T = triangle(read_svg(q["html"])); m = re.fullmatch(r'(sin|cos|tan) θ = \?', q["en"]); need(m, "parse frac")
    k = T["known"]; need(len(k) == 3, "three sides"); need(k["o"] ** 2 + k["a"] ** 2 == k["h"] ** 2, "sides not Pythagorean")
    fn = m.group(1); top, bot = {"sin": ("o", "h"), "cos": ("a", "h"), "tan": ("o", "a")}[fn]
    exp = k[top] / k[bot]
    def fv(o):
        mm = re.fullmatch(r'(\d+)/(\d+)', o); need(mm, "not a fraction " + o)
        need(Fr(mm.group(1)) in k.values() and Fr(mm.group(2)) in k.values(), "fraction not from the sides " + o); return Fr(int(mm.group(1)), int(mm.group(2)))
    vs = [fv(o) for o in [q["answer"]] + q["wrong"]]
    need(vs[0] == exp and exp not in vs[1:], "frac answer"); need(len(set(vs)) == 4, "equal values")
    need(q["answer"] == "%s/%s" % (k[top], k[bot]), "fraction not written from the sides")

SOHKEY = {"sin θ = ?": "Opposite ÷ Hypotenuse", "cos θ = ?": "Adjacent ÷ Hypotenuse", "tan θ = ?": "Opposite ÷ Adjacent"}
def check_soh(q): need(SOHKEY[q["en"]] == q["answer"] and SOHKEY[q["en"]] not in q["wrong"], "soh")

def d4(x): return str(half_up(x, 4)).replace("-", "−")
def check_calc(q):
    m = re.fullmatch(r'🧮 (sin|cos|tan) (\d+)° = \? \(to 4 d\.p\.\)', q["en"]); need(m, "parse calc")
    fn, a = m.group(1), int(m.group(2)); v = {"sin": S_, "cos": C_, "tan": T_}[fn](a); not_edge(abs(v), 4)
    need(q["answer"] == d4(v), "calc %s expected %s" % (q["answer"], d4(v)))
    for w in q["wrong"]: need(re.fullmatch(r'−?\d\.\d{4}|−?\d+\.\d{4}', w) and w != q["answer"], "wrong calc option " + w)

def ev_side(o):
    m = re.fullmatch(r'(\d+(?:\.\d+)?) ([×÷]) (sin|cos|tan) (\d+)°', o); need(m, "odd calc " + o)
    r = {"sin": S_, "cos": C_, "tan": T_}[m.group(3)](int(m.group(4))); v = float(m.group(1))
    return v * r if m.group(2) == "×" else v / r, m
def check_calcfig(q):
    T = triangle(read_svg(q["html"])); x = solve(T)[T["unk"]]; ok = []
    for o in [q["answer"]] + q["wrong"]:
        v, m = ev_side(o); need(Fr(m.group(1)) in T["known"].values() and int(m.group(4)) == T["alpha"], "calc uses other numbers " + o); ok.append(abs(v - x) < 1e-9)
    need(ok[0] and sum(ok) == 1, "calc options %s" % ok)

def ev_inv(o):
    m = re.fullmatch(r'(sin|cos|tan)⁻¹\((\d+(?:\.\d+)?) ÷ (\d+(?:\.\d+)?)\)', o); need(m, "odd inverse " + o)
    r = float(m.group(2)) / float(m.group(3))
    if m.group(1) != "tan" and r > 1: return None, m
    return math.degrees({"sin": math.asin, "cos": math.acos, "tan": math.atan}[m.group(1)](r)), m
def check_anglecalc(q):
    T = triangle(read_svg(q["html"])); th = solve_angle(T); ok = []
    for o in [q["answer"]] + q["wrong"]:
        v, m = ev_inv(o); ok.append(v is not None and abs(v - th) < 1e-9)
        if v is not None: need(round(v) != round(th) or ok[-1], "a wrong option gives the same whole-degree answer " + o)
    need(ok[0] and sum(ok) == 1, "anglecalc %s" % ok)

def check_inv(q):
    m = re.fullmatch(r'🧮 (sin|cos|tan)⁻¹\((\d+(?:\.\d+)?)\) = \? \(to the nearest degree\)', q["en"]); need(m, "parse inv")
    v = float(m.group(2)); need(m.group(1) == "tan" or v < 1, "ratio > 1")
    th = math.degrees({"sin": math.asin, "cos": math.acos, "tan": math.atan}[m.group(1)](v)); not_edge(th, 0); opts_deg(q, int(half_up(th, 0)))

WORDKEY = {"The angle of elevation is measured…": "Up from the horizontal", "The angle of depression is measured…": "Down from the horizontal",
    "From a boat, the angle of elevation of a cliff top is 20°. The angle of depression from the cliff top to the boat is…": "20°",
    "Your calculator must be in…": "DEG (degrees) mode", "Sin, cos and tan work in…": "Right-angled triangles only",
    "sin⁻¹ gives you…": "An angle", "To find an angle you need…": "Two sides", "A clinometer measures…": "Angles of elevation"}
def check_words(q): need(WORDKEY.get(q["en"]) == q["answer"] and q["answer"] not in q["wrong"], "words key")

def check_flag(q):
    D = read_svg(q["html"]); m = re.fullmatch(r'🚩 Higher Level: the angle to the top is (\d+)°\. How tall is the flagpole, x\? \(to 1 d\.p\.\)', q["en"]); need(m, "parse flag")
    a2 = int(m.group(1)); marks = [k for k in D["marks"] if k["l"] not in ("rt",)]
    num_ = [k for k in marks if re.fullmatch(r'\d+', k["l"])]; arc = [k for k in marks if k["l"] == "=1"]; need(len(num_) == 1 and len(arc) == 1, "flag marks")
    O = num_[0]["v"]; a1 = int(num_[0]["l"]); need(abs(angle(O, num_[0]["p"], num_[0]["q"]) - a1) < 0.6, "a1 drawn")
    need(same(arc[0]["v"], O), "second angle at the same point")
    tot = angle(O, num_[0]["p"], num_[0]["q"]) + angle(O, arc[0]["p"], arc[0]["q"]); need(abs(tot - a2) < 0.6, "angle to the top drawn %.2f" % tot)
    labs = [(l, val(l["t"])) for l in D["lens"]]; dl = [v for l, (v, u) in labs if v is not None]; need(len(dl) == 1, "one distance")
    d = float(dl[0]); need(abs(dist(*[(l["a"], l["b"]) for l, (v, u) in labs if v is not None][0]) / D["s"] - d) < 0.01, "distance drawn")
    x = d * (T_(a2) - T_(a1)); not_edge(x, 1)
    xl = [l for l, (v, u) in labs if l["t"] == "x"][0]; need(abs(dist(xl["a"], xl["b"]) / D["s"] - x) < 0.01, "flagpole drawn")
    opts_len(q, half_up(x, 1), "m")

def check_ratiohl(q):
    m = re.fullmatch(r'Higher Level: (sin|cos|tan) A = (\d+)/(\d+) \(0° < A < 90°\)\. (sin|cos|tan) A = \?', q["en"]); need(m, "parse ratiohl")
    g, p, r, w = m.group(1), int(m.group(2)), int(m.group(3)), m.group(4); need(g != w, "same ratio")
    if g == "tan": o, a = p, r; h2 = o * o + a * a; h = math.isqrt(h2); need(h * h == h2, "not whole"); sides = (o, a, h)
    else:
        h, s = r, p; t2 = h * h - s * s; t = math.isqrt(t2); need(t * t == t2 and t > 0, "not whole")
        sides = (s, t, h) if g == "sin" else (t, s, h)
    o, a, h = sides; exp = {"sin": Fr(o, h), "cos": Fr(a, h), "tan": Fr(o, a)}[w]
    vals = []
    for opt in [q["answer"]] + q["wrong"]:
        mm = re.fullmatch(r'(\d+)/(\d+)', opt); need(mm, "fraction " + opt); vals.append(Fr(int(mm.group(1)), int(mm.group(2))))
    need(vals[0] == exp and exp not in vals[1:] and len(set(vals)) == 4, "ratiohl %s expected %s" % (q["answer"], exp))

CHK = {"fig": check_fig, "eye": check_eye, "name": check_name, "whichratio": check_whichratio, "frac": check_frac, "soh": check_soh,
       "calc": check_calc, "calcfig": check_calcfig, "anglecalc": check_anglecalc, "inv": check_inv, "words": check_words, "flag": check_flag, "ratiohl": check_ratiohl}
def check(q):
    blob = json.dumps(q, ensure_ascii=False)
    need("NaN" not in blob and "undefined" not in blob and "Infinity" not in blob, "NaN/undefined")
    for s in [q["en"], q["answer"], q["why"]] + q["wrong"]:
        need(not re.search(r'(?<![\w])-\d', s), "ASCII minus: " + s)
        need(not re.search(r'\b(\w+) \1\b', s), "doubled word: " + s)
    n = 2 if q["data"].get("n3") else 3
    need(len(q["wrong"]) == n and q["answer"] not in q["wrong"] and len(set(q["wrong"])) == n, "options")
    need(len(q["en"]) <= 120, "question text too long (%d)" % len(q["en"]))
    CHK[q["data"]["t"]](q)

if __name__ == "__main__":
    data = json.load(open(sys.argv[1])); probs = collections.Counter(); ex = {}
    for q in data:
        try: check(q)
        except (Bad, AttributeError, TypeError, ValueError, IndexError, KeyError) as e:
            k = q["mk"] + ": " + str(e)[:60]; k = re.sub(r'[\d.]+', '#', k); probs[k] += 1; ex.setdefault(k, (q["en"][:160], q["answer"], q["wrong"], str(e)))
    print(len(data), "questions,", sum(probs.values()), "problems")
    for k, n in probs.most_common(): print(n, k, ex[k])
