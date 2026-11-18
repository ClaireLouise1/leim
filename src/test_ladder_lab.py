#!/usr/bin/env python3
"""Independent checker for Ladder Lab (JC Maths topic 25, Pythagoras).
node src/test_ladder_lab.js > /tmp/ll.json ; python3 src/test_ladder_lab.py /tmp/ll.json   (env LL=<file> tests a mutated copy)
It MEASURES every diagram (right-angle marks, every labelled length against data-s), finds the right-angled
triangle that contains x in the drawing and works x out from the LABELS itself (exact arithmetic, half-up
rounding), parses every text question with its own regexes, evaluates every option of "which calculation /
which triangle / what mistake" questions and requires exactly one to be right."""
import json, re, sys, math, collections
from fractions import Fraction as Fr
from decimal import Decimal, getcontext, ROUND_HALF_UP
getcontext().prec = 50

def attrs(tag): return dict(re.findall(r'([\w-]+)="([^"]*)"', tag))
def P(s): return tuple(float(v) for v in s.split(","))
def read_svg(html):
    m = re.search(r'<svg class="pf"[^>]*>', html or "")
    if not m: return None
    s = float(attrs(m.group(0)).get("data-s", 0) or 0)
    D = {"s": s, "lines": [], "marks": [], "lens": [], "names": {}, "polys": [], "ticks": []}
    for t in re.findall(r'<line class="ln"[^>]*/>', html):
        a = attrs(t); D["lines"].append(((float(a["x1"]), -float(a["y1"])), (float(a["x2"]), -float(a["y2"]))))
    for g in re.findall(r'<g class="am"[^>]*>', html):
        a = attrs(g); D["marks"].append({"v": f(P(a["data-v"])), "p": f(P(a["data-p"])), "q": f(P(a["data-q"])), "l": a["data-l"]})
    for t, txt in re.findall(r'(<text class="ll"[^>]*>)([^<]*)</text>', html):
        a = attrs(t); D["lens"].append({"a": f(P(a["data-a"])), "b": f(P(a["data-b"])), "t": txt, "x": float(a["x"]), "y": -float(a["y"])})
    for t, txt in re.findall(r'(<text class="vn"[^>]*>)([^<]*)</text>', html):
        D["names"][txt] = f(P(attrs(t)["data-p"]))
    for t in re.findall(r'<polygon class="tri"[^>]*/>', html):
        D["polys"].append([f(P(x)) for x in attrs(t)["data-pts"].split()])
    D["ticks"] = re.findall(r'<line class="tick"[^>]*/>', html)
    return D
def f(p): return (p[0], -p[1])   # data-* attributes are written in screen y (down); flip back to maths y (up)
def dist(a, b): return math.hypot(a[0] - b[0], a[1] - b[1])
def angle(v, p, q):
    a1 = math.atan2(p[1] - v[1], p[0] - v[0]); a2 = math.atan2(q[1] - v[1], q[0] - v[0])
    x = abs(math.degrees(a1 - a2)) % 360
    return 360 - x if x > 180 else x
def same(p, q, t=0.6): return dist(p, q) <= t
def on_seg(p, a, b): return abs(dist(a, p) + dist(p, b) - dist(a, b)) < 0.6

UNIT = r'(mm|cm|m|km)'
def val(s):
    s = s.replace("−", "-").strip()
    m = re.fullmatch(r'(-?\d+(?:\.\d+)?)( (?:mm|cm|m|km)²?)?', s)
    return (Fr(m.group(1)), (m.group(2) or "").strip()) if m else (None, None)
def sqrt_exact(F):
    """exact sqrt if F is a perfect square of a fraction, else None"""
    n, d = F.numerator, F.denominator
    rn, rd = math.isqrt(n), math.isqrt(d)
    return Fr(rn, rd) if rn * rn == n and rd * rd == d else None
def dsqrt(F): return (Decimal(F.numerator) / Decimal(F.denominator)).sqrt()
def r1(x):
    x = x if isinstance(x, Decimal) else Decimal(x.numerator) / Decimal(x.denominator)
    return Fr(str(x.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)))
def dp_of(s):
    m = re.search(r'\.(\d+)', s); return len(m.group(1)) if m else 0

class Bad(Exception): pass
def need(c, msg):
    if not c: raise Bad(msg)

def expect_root(F2, q, label="answer"):
    """F2 = x² (exact). Returns the expected answer value and checks the rounding instruction."""
    ex = sqrt_exact(F2)
    rounding = "1 decimal place" in q["en"]
    if ex is not None and ex.denominator in (1, 2, 5, 10):
        need(not rounding, "asks for 1 d.p. but the answer is exact: " + str(ex)); return ex, False
    need(rounding, "answer isn't exact but there's no rounding instruction (x² = %s)" % F2)
    return r1(dsqrt(F2)), True

def check_option_format(q, rounding):
    vals = []
    for o in [q["answer"]] + q["wrong"]:
        v, u = val(o); need(v is not None, "option not a number: " + o)
        need(v > 0, "option not positive: " + o)
        if rounding: need(dp_of(o) == 1, "not written to 1 d.p.: " + o)
        else: need(dp_of(o) <= 1, "more than 1 d.p.: " + o)
        vals.append((v, u))
    need(len(set(v for v, u in vals)) == 4, "options equal in value")
    need(len(set(u for v, u in vals)) == 1, "units differ")
    return vals

def fig_lengths(D):
    need(D and D["s"] > 0, "no scaled figure")
    for m in D["marks"]:
        need(m["l"] == "rt", "unexpected mark " + m["l"])
        need(abs(angle(m["v"], m["p"], m["q"]) - 90) < 0.3, "right-angle mark isn't 90°")
    known, unk = [], []
    for l in D["lens"]:
        v, u = val(l["t"])
        meas = dist(l["a"], l["b"]) / D["s"]
        if v is None:
            need(l["t"] in ("x",), "odd label " + l["t"]); unk.append(l)
        else:
            need(abs(float(v) - meas) < 0.02, "label %s but drawn %.3f" % (l["t"], meas)); known.append((l, v, u))
        # every labelled segment is a drawn line
        need(any((same(a, l["a"]) and same(b, l["b"])) or (same(a, l["b"]) and same(b, l["a"])) for a, b in D["lines"]), "label on no line")
    return known, unk

def length_of(p, q, known):
    for l, v, u in known:
        if (same(l["a"], p) and same(l["b"], q)) or (same(l["a"], q) and same(l["b"], p)): return v
    for l, v, u in known:   # half of a labelled segment (foot of the height at its midpoint)
        m = ((l["a"][0] + l["b"][0]) / 2, (l["a"][1] + l["b"][1]) / 2)
        for e in (l["a"], l["b"]):
            if (same(p, m) and same(q, e)) or (same(q, m) and same(p, e)): return v / 2
    return None

def endpoints(D):
    pts = []
    for a, b in D["lines"]:
        for p in (a, b):
            if not any(same(p, r) for r in pts): pts.append(p)
    return pts
def joined(D, p, q): return any((same(a, p) and same(b, q)) or (same(a, q) and same(b, p)) for a, b in D["lines"]) or any(on_seg(p, a, b) and on_seg(q, a, b) for a, b in D["lines"])

def solve_x(D, known, xl):
    """find the right-angled triangle containing segment x and return x² from the LABELS"""
    P_, Q_ = xl["a"], xl["b"]; sols = set(); pts = endpoints(D)
    for m in D["marks"]:
        V = m["v"]
        if not (same(V, P_) or same(V, Q_)):
            if joined(D, V, P_) and joined(D, V, Q_) and abs(angle(V, P_, Q_) - 90) < 0.3:
                a, b = length_of(V, P_, known), length_of(V, Q_, known)
                if a is not None and b is not None: sols.add(a * a + b * b)
        else:
            O = Q_ if same(V, P_) else P_
            for R in pts:
                if same(R, V) or same(R, O) or not joined(D, V, R) or not joined(D, O, R): continue
                if abs(angle(V, O, R) - 90) > 0.3: continue
                h, a = length_of(O, R, known), length_of(V, R, known)
                if h is not None and a is not None: sols.add(h * h - a * a)
    need(len(sols) == 1, "x not determined exactly once: %s" % sols)
    return sols.pop()

def text_numbers_in_labels(q, known):
    labs = set(v for l, v, u in known)
    for n in re.findall(r'(\d+(?:\.\d+)?) (?:cm|m|km)\b', q["en"]):
        if Fr(n) not in labs and Fr(n) * 2 not in labs and Fr(n) / 2 not in labs:
            need(False, "text number %s not in the drawing" % n)

def check_fig(q):
    D = read_svg(q["html"]); known, unk = fig_lengths(D)
    need(len(unk) == 1, "need exactly one x label"); xl = unk[0]
    X2 = solve_x(D, known, xl)
    need(X2 > 0, "x² ≤ 0")
    exp, rounding = expect_root(X2, q)
    meas = dist(xl["a"], xl["b"]) / D["s"]
    need(abs(meas - math.sqrt(X2)) < 0.02, "x drawn %.3f but should be %.3f" % (meas, math.sqrt(X2)))
    vals = check_option_format(q, rounding)
    need(vals[0][0] == exp, "answer %s, expected %s" % (q["answer"], exp))
    units = set(u for l, v, u in known); need(vals[0][1] in units, "answer unit not the drawing's")
    text_numbers_in_labels(q, known)
    return exp

def check_isoarea(q):
    D = read_svg(q["html"]); known, unk = fig_lengths(D); need(not unk, "no x expected")
    m = re.search(r'base of (\d+(?:\.\d+)?) (cm|m) and two sides of (\d+(?:\.\d+)?) \2', q["en"]); need(m, "parse")
    b, e, u = Fr(m.group(1)), Fr(m.group(3)), m.group(2)
    need(sorted(v for l, v, uu in known) == sorted([b, e]), "labels don't match the text")
    need(len(D["ticks"]) == 2, "equal sides not marked")
    h = sqrt_exact(e * e - b * b / 4); need(h is not None, "height not exact")
    # the height in the drawing
    rt = D["marks"]; need(len(rt) == 1, "one right angle")
    A = b * h / 2
    vals = check_option_format(q, False); need(vals[0][0] == A and vals[0][1] == u + "²", "area %s expected %s" % (q["answer"], A))

def check_whichhyp(q):
    D = read_svg(q["html"]); need(len(D["marks"]) == 1, "one right angle")
    V = D["marks"][0]["v"]; nm = {k: p for k, p in D["names"].items()}
    vk = [k for k, p in nm.items() if same(p, V)]; need(len(vk) == 1, "right-angle vertex unnamed")
    others = sorted(k for k in nm if k != vk[0])
    ans = q["answer"]; need(re.fullmatch(r'\[[A-Z]{2}\]', ans) and sorted(ans[1:3]) == others, "hypotenuse wrong: " + ans)
    for w in q["wrong"]:
        if re.fullmatch(r'\[[A-Z]{2}\]', w): need(sorted(w[1:3]) != others, "a wrong option is the hypotenuse")

def check_eq(q):
    D = read_svg(q["html"]); V = D["marks"][0]["v"]; vk = [k for k, p in D["names"].items() if same(p, V)][0]
    good = []
    for o in [q["answer"]] + q["wrong"]:
        m = re.fullmatch(r'\|([A-Z]{2})\|² = \|([A-Z]{2})\|² \+ \|([A-Z]{2})\|²', o)
        good.append(bool(m) and vk not in m.group(1) and vk in m.group(2) and vk in m.group(3) and len({m.group(1), m.group(2), m.group(3)}) == 3)
    need(good[0] and sum(good) == 1, "eq options")

def check_root(q):
    m = re.fullmatch(r'√(\d+) lies between which two whole numbers\?', q["en"]); need(m, "parse")
    n = int(m.group(1)); k = math.isqrt(n); need(k * k != n, "perfect square")
    def ok(o):
        mm = re.fullmatch(r'(\d+) and (\d+)', o); a, b = int(mm.group(1)), int(mm.group(2)); return b == a + 1 and a * a < n < b * b
    need(ok(q["answer"]) and not any(ok(w) for w in q["wrong"]), "root")

def ev(expr):
    e = expr.replace("−", "-").replace("²", "**2").replace("√", "sqrt")
    need(re.fullmatch(r'[\d.+\-*/ ()sqrt]+', e), "odd calc " + expr)
    return eval(e, {"sqrt": math.sqrt})
def check_calc(q):
    D = read_svg(q["html"]); known, unk = fig_lengths(D); X2 = solve_x(D, known, unk[0]); x = math.sqrt(X2)
    res = [abs(ev(o) - x) < 1e-9 for o in [q["answer"]] + q["wrong"]]
    need(res[0] and sum(res) == 1, "calc options %s" % res)

def check_slip(q):
    en = q["en"]
    mh = re.search(r'the hypotenuse x of a right-angled triangle whose other two sides are (\d+(?:\.\d+)?) (cm|m) and (\d+(?:\.\d+)?) \2\.', en)
    ml = re.search(r'the side x of a right-angled triangle whose hypotenuse is (\d+(?:\.\d+)?) (cm|m) and whose other side is (\d+(?:\.\d+)?) \2\.', en)
    need(mh or ml, "parse slip")
    w = re.search(r'writes: (.*) = (\d+(?:\.\d+)?) (cm|m)\. What mistake', en); need(w, "parse working")
    her = Fr(w.group(2))
    if mh:
        a, b = sorted([Fr(mh.group(1)), Fr(mh.group(3))])
        cand = {"No mistake": (a * a + b * b, True), "added the sides without squaring": (a + b, False), "forgot to take the square root": (a * a + b * b, False), "subtracted the squares instead of adding": (b * b - a * a, True)}
    else:
        c, a = Fr(ml.group(1)), Fr(ml.group(3))
        cand = {"No mistake": (c * c - a * a, True), "subtracted the sides without squaring": (c - a, False), "forgot to take the square root": (c * c - a * a, False), "added the squares instead of subtracting": (c * c + a * a, True)}
    def value(k):
        v, root = cand[k]; return (r1(dsqrt(v)) if sqrt_exact(v) is None else sqrt_exact(v)) if root else v
    hits = [k for k in cand if value(k) == her]
    need(len(hits) == 1, "her answer fits %s" % hits)
    opts = [q["answer"]] + q["wrong"]
    match = [o for o in opts if hits[0] in o]
    need(len(match) == 1 and match[0] == q["answer"], "slip answer %s, expected %s" % (q["answer"], hits[0]))
    for o in opts: need(any(k in o for k in cand), "unknown option " + o)
    pron = re.search(r'\. (He|She) writes', en).group(1)
    need(all(o.startswith(pron) or o.startswith("No mistake") for o in opts), "pronoun")

def sides(o):
    nums = [Fr(x) for x in re.findall(r'(\d+(?:\.\d+)?)(?: (?:cm|m))?', o)]
    need(len(nums) == 3, "3 sides: " + o); return sorted(nums)
def is_right(t): return t[0] ** 2 + t[1] ** 2 == t[2] ** 2
def check_whichright(q, whole=False):
    opts = [q["answer"]] + q["wrong"]; res = []
    for o in opts:
        t = sides(o); need(t[0] + t[1] > t[2], "not a triangle " + o)
        if whole: need(all(x.denominator == 1 for x in t), "not whole")
        res.append(is_right(t))
    need(res[0] and sum(res) == 1, "which right %s" % res)

def check_whichangle(q):
    m = re.fullmatch(r'Triangle ([A-Z]{3}) has (.*)\. Which angle is a right angle\?', q["en"]); need(m, "parse")
    S = dict((k, Fr(v)) for k, v in re.findall(r'\|([A-Z]{2})\| = (\d+(?:\.\d+)?) (?:cm|m)', m.group(2))); need(len(S) == 3, "3 sides")
    lng = max(S, key=lambda k: S[k]); others = sorted(v for k, v in S.items() if k != lng)
    right = others[0] ** 2 + others[1] ** 2 == S[lng] ** 2
    if right:
        vtx = [c for c in m.group(1) if c not in lng][0]
        a = q["answer"]; need(re.fullmatch(r'∠[A-Z]{3}', a) and a[2] == vtx and set(a[1:]) == set(m.group(1)), "angle answer " + a)
        for w in q["wrong"]: need(not (w.startswith("∠") and w[2] == vtx), "wrong option is the right angle")
    else:
        need(q["answer"].startswith("None"), "should be none")

def check_isright(q):
    m = re.fullmatch(r'A triangle has sides (.*)\. Is it right-angled\?', q["en"]); t = sides(m.group(1)); right = is_right(t)
    need(q["answer"].startswith("Yes" if right else "No"), "isright conclusion")
    need(all(not w.startswith("Yes" if right else "No") for w in q["wrong"]), "a wrong option has the right conclusion")
    a = q["answer"].replace("−", "-")
    if right:
        mm = re.fullmatch(r'Yes: ([\d.]+)² \+ ([\d.]+)² = ([\d.]+) = ([\d.]+)²', a); need(mm, "parse yes")
        x, y, s, z = map(Fr, mm.groups()); need(x * x + y * y == s == z * z and sorted([x, y, z]) == t, "yes statement false")
    else:
        mm = re.fullmatch(r'No: ([\d.]+)² \+ ([\d.]+)² = ([\d.]+), but ([\d.]+)² = ([\d.]+)', a); need(mm, "parse no")
        x, y, s, z, s2 = map(Fr, mm.groups()); need(x * x + y * y == s and z * z == s2 and s != s2 and z == t[2], "no statement false")

def check_builder(q):
    m = re.search(r'marks (\d+(?:\.\d+)?) (cm|m) along one wall and (\d+(?:\.\d+)?) \2 along the other, then measures (\d+(?:\.\d+)?) \2', q["en"]); need(m, "parse")
    a, b, d = Fr(m.group(1)), Fr(m.group(3)), Fr(m.group(4)); s = a * a + b * b
    exp = "Yes" if d * d == s else ("bigger" if d * d > s else "less")
    need(exp in q["answer"], "builder %s %s" % (exp, q["answer"]))

WORDKEY = {"What is the hypotenuse?": "The side opposite the right angle",
    "Which side of a right-angled triangle is always the longest?": "The hypotenuse",
    "What does Pythagoras' theorem (Theorem 14) say?": "In a right-angled triangle, the square of the hypotenuse is the sum of the squares of the other two sides",
    "What does the converse of Pythagoras' theorem (Theorem 15) say?": "If the square of one side equals the sum of the squares of the other two, the angle opposite that side is a right angle",
    "A Pythagorean triple is…": "Three whole numbers with a² + b² = c²",
    "If 3, 4, 5 is a Pythagorean triple, which of these is also one?": "6, 8, 10",
    "To find a SHORTER side of a right-angled triangle, you…": "Subtract the squares, then take the square root",
    "√(a² + b²) is the same as a + b…": "Never, when a and b are both positive"}
def check_words(q):
    need(WORDKEY.get(q["en"]) == q["answer"], "words key")
    if q["en"].startswith("If 3, 4, 5"):
        need(sum(is_right(sides(o)) for o in [q["answer"]] + q["wrong"]) == 1, "multiple triples")

def text_answer(q, F2_or_val, is_sq=True):
    if is_sq: exp, rounding = expect_root(F2_or_val, q)
    else:
        v = F2_or_val
        if isinstance(v, Decimal):
            need("1 decimal place" in q["en"], "needs rounding instruction"); exp, rounding = r1(v), True
        else: need("1 decimal place" not in q["en"], "exact but asks for 1 d.p."); exp, rounding = v, False
    vals = check_option_format(q, rounding); need(vals[0][0] == exp, "answer %s expected %s" % (q["answer"], exp))

def check_shortcut(q):
    m = re.search(r'field is (\d+) m wide and (\d+) m long', q["en"]); w, l = Fr(m.group(1)), Fr(m.group(2))
    ex = sqrt_exact(w * w + l * l)
    text_answer(q, (w + l - ex) if ex is not None else Decimal(int(w + l)) - dsqrt(w * w + l * l), False)
def check_travel(q):
    m = re.search(r'goes (\d+(?:\.\d+)?) km (\w+) and then (\d+(?:\.\d+)?) km (\w+)\. How far is it from where it started', q["en"])
    if m:
        need({m.group(2), m.group(4)} in ({"north", "east"}, {"south", "west"}, {"east", "south"}, {"west", "north"}), "directions not at right angles")
        a, b = Fr(m.group(1)), Fr(m.group(3)); text_answer(q, a * a + b * b); return
    m = re.search(r'goes (\d+(?:\.\d+)?) km (\w+), then turns and goes (\w+)\. The finish is (\d+(?:\.\d+)?) km from the start in a straight line\. How far (\w+) did it go\?', q["en"]); need(m, "parse travel")
    need(m.group(3) == m.group(5), "direction mismatch")
    a, c = Fr(m.group(1)), Fr(m.group(4)); text_answer(q, c * c - a * a)
def check_slide(q):
    m = re.search(r'A (\d+(?:\.\d+)?) m ladder reaches (\d+(?:\.\d+)?) m up a wall\. Its top slides down (\d+(?:\.\d+)?) m\.', q["en"]); need(m, "parse slide")
    L, h, dh = map(Fr, m.groups()); need(h < L, "ladder shorter than height"); text_answer(q, L * L - (h - dh) ** 2)

TEXTFIG = {"fig": check_fig}
def check(q):
    t = q["data"].get("t")
    blob = json.dumps(q, ensure_ascii=False)
    need("NaN" not in blob and "undefined" not in blob and "Infinity" not in blob, "NaN/undefined")
    for s in [q["en"], q["answer"], q["why"]] + q["wrong"]:
        need(not re.search(r'(?<![\w])-\d', s), "ASCII minus: " + s)
        need(not re.search(r'\b(\w+) \1\b', s), "doubled word: " + s)
    need(len(q["wrong"]) == 3 and q["answer"] not in q["wrong"] and len(set(q["wrong"])) == 3, "options")
    if t == "fig":
        check_fig(q)
        if q["mk"] in ("qLadderL", "qLadderH"):
            m = re.findall(r'(\d+(?:\.\d+)?) m', q["en"]); need(len(m) == 2, "ladder text")
    elif t == "isoarea": check_isoarea(q)
    elif t == "whichhyp": check_whichhyp(q)
    elif t == "eq": check_eq(q)
    elif t == "root": check_root(q)
    elif t == "calc": check_calc(q)
    elif t == "slip": check_slip(q)
    elif t == "whichright": check_whichright(q)
    elif t == "triple": check_whichright(q, whole=True)
    elif t == "whichangle": check_whichangle(q)
    elif t == "isright": check_isright(q)
    elif t == "builder": check_builder(q)
    elif t == "words": check_words(q)
    elif t == "shortcut": check_shortcut(q)
    elif t == "travel": check_travel(q)
    elif t == "slide": check_slide(q)
    else: need(False, "unknown type " + str(t))
    # the explanation shows the answer (number questions)
    v, u = val(q["answer"])
    if v is not None: need(q["answer"].replace(" " + u, "") in q["why"], "why doesn't show the answer")

if __name__ == "__main__":
    data = json.load(open(sys.argv[1])); probs = collections.Counter(); ex = {}
    for q in data:
        try: check(q)
        except (Bad, AttributeError, TypeError, ValueError, IndexError, KeyError) as e:
            k = q["mk"] + ": " + str(e).split(":")[0][:60]; probs[k] += 1; ex.setdefault(k, (q["en"][:160], q["answer"], q["wrong"], str(e)))
    print(len(data), "questions,", sum(probs.values()), "problems")
    for k, n in probs.most_common(): print(n, k, ex[k])
