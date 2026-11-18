#!/usr/bin/env python3
"""Independent checker for Floor Planner (area, perimeter & scale drawings, JC Maths topic 21).
Reads every question's TEXT and its DRAWING (polygon points, edge labels, dashed heights, circle radii,
squared-paper grids), works the answer out again with exact Fractions (and math.pi for "use the π button")
and checks the game's answer and every wrong option.
Usage: N=400 node src/test_floor_planner.js > /tmp/fp.json ; python3 src/test_floor_planner.py /tmp/fp.json"""
import json, re, sys, math
from fractions import Fraction as F
from math import floor, ceil
from collections import Counter

problems = Counter(); examples = {}; count = Counter()
def bad(q, msg):
    problems[msg] += 1
    examples.setdefault(msg, (q["mk"], q["en"], q["answer"], q["wrong"]))

def N(s): return F(s.replace(",", ""))
def half_up(x, dp):
    u = F(1, 10 ** dp); return F(floor(F(x) / u + F(1, 2))) * u
def pi_val(mode):
    return {"314": F(314, 100), "227": F(22, 7)}.get(mode)

# ---------- drawing reader ----------
def attrs(tag):
    return dict(re.findall(r'([\w-]+)="([^"]*)"', tag))
def pt(s): return tuple(F(v) for v in s.split(","))
def read_fig(q):
    h = q["html"] or ""
    m = re.search(r"<svg[^>]*class=\"fig\"[^>]*>", h)
    if not m: return None
    sv = attrs(m.group(0)); fig = {"kind": sv["data-kind"], "svg": sv, "labels": []}
    s, ox, oy = float(sv["data-s"]), float(sv["data-ox"]), float(sv["data-oy"])
    pm = re.search(r"<polygon ([^>]*)/>", h)
    if pm:
        a = attrs(pm.group(1)); P = [pt(x) for x in a["data-pts"].split()]
        scr = [tuple(map(float, x.split(","))) for x in a["points"].split()]
        fig["P"] = P; fig["scr"] = scr
        if fig["kind"] != "grid":
            for (x, y), (X, Y) in zip(P, scr):
                if abs(ox + float(x) * s - X) > 0.02 or abs(oy - float(y) * s - Y) > 0.02:
                    fig["drawn_wrong"] = True
    for tm in re.finditer(r"<text ([^>]*)>([^<]*)</text>", h):
        a = attrs(tm.group(1))
        if "data-k" not in a: continue
        A, B = pt(a["data-a"]), pt(a["data-b"]); t = tm.group(2)
        L2 = (A[0] - B[0]) ** 2 + (A[1] - B[1]) ** 2
        lab = {"k": a["data-k"], "a": A, "b": B, "t": t, "L2": L2}
        if t != "?":
            mm = re.fullmatch(r"(\d+(?:\.\d+)?) (m|cm)", t)
            if not mm: fig["badlabel"] = t
            else:
                lab["v"] = N(mm[1]); lab["u"] = mm[2]
                if lab["v"] ** 2 != L2: fig["label_mismatch"] = t
        fig["labels"].append(lab)
    if "P" in fig:
        P = fig["P"]; n = len(P)
        for lab in fig["labels"]:
            if lab["k"] in ("e", "q"):
                ok = any(P[i] == lab["a"] and P[(i + 1) % n] == lab["b"] for i in range(n))
                if not ok: fig["label_not_edge"] = lab["t"]
            if lab["k"] == "h":
                if lab["a"] not in P or lab["b"][1] != 0 or lab["a"][0] != lab["b"][0]: fig["bad_height"] = True
    if "data-r" in sv:
        r = F(sv["data-r"]); fig["r"] = r
        for lab in fig["labels"]:
            if lab["k"] == "r" and lab.get("v") != r: fig["r_mismatch"] = True
            if lab["k"] == "d" and fig["kind"] != "track" and lab.get("v") != 2 * r: fig["r_mismatch"] = True
    if fig["kind"] == "grid":
        xs = sorted({float(a["x1"]) for a in map(attrs, re.findall(r'<line class="gl" ([^>]*)/>', h)) if a["x1"] == a["x2"]})
        gap = (xs[-1] - xs[0]) / (len(xs) - 1)
        if any(abs((xs[i + 1] - xs[i]) - gap) > 0.02 for i in range(len(xs) - 1)): fig["grid_uneven"] = True
        ys = sorted({float(a["y1"]) for a in map(attrs, re.findall(r'<line class="gl" ([^>]*)/>', h)) if a["y1"] == a["y2"]})
        if abs((ys[1] - ys[0]) - gap) > 0.02: fig["grid_uneven"] = True
        G = [(round((X - xs[0]) / gap, 4), round((Y - ys[0]) / gap, 4)) for X, Y in fig["scr"]]
        if any(abs(c - round(c)) > 1e-3 for p in G for c in p): fig["off_grid"] = True
        fig["G"] = [(F(round(x)), F(round(y))) for x, y in G]
    return fig

def shoelace(P):
    n = len(P); return abs(sum(P[i][0] * P[(i + 1) % n][1] - P[(i + 1) % n][0] * P[i][1] for i in range(n))) / 2
def perim(P):
    n = len(P); tot = F(0)
    for i in range(n):
        a, b = P[i], P[(i + 1) % n]; d2 = (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2
        r = F(math.isqrt(d2.numerator), math.isqrt(d2.denominator))
        assert r * r == d2, "edge not a whole length"; tot += r
    return tot
def lab(fig, k):
    return [l for l in fig["labels"] if l["k"] == k]

# ---------- option readers ----------
def reader(unit):
    def f(o):
        if unit == "€":
            m = re.fullmatch(r"€(\d{1,3}(?:,\d{3})*\.\d\d)", o); assert m, "bad money"; return N(m[1])
        m = re.fullmatch(r"(\d{1,3}(?:,\d{3})*(?:\.\d+)?) " + re.escape(unit), o); assert m, "bad option format"
        assert not re.search(r"\.\d*0$", m[1]), "trailing zero"; return N(m[1])
    return f
def pireader(unit):
    def f(o):
        m = re.fullmatch(r"(\d{1,3}(?:,\d{3})*(?:\.\d+)?)?π " + re.escape(unit), o); assert m, "bad π option"
        return N(m[1]) if m[1] else F(1)
    return f

def check(q, true, rd, dp=None, why=True):
    """dp=None: options must be EXACT; dp=k: the true value rounded half up to k places."""
    try:
        a = rd(q["answer"]); ws = [rd(w) for w in q["wrong"]]
    except AssertionError as e:
        return bad(q, str(e))
    want = true if dp is None else half_up(true, dp)
    if a != want: bad(q, "WRONG ANSWER")
    if dp is not None:
        dec = re.search(r"\.(\d+)", q["answer"].split(" ")[0])
        if dec and len(dec[1]) > dp: bad(q, "too many decimal places")
    if len(q["wrong"]) != 3: bad(q, "not 3 wrong options")
    if any(w == want for w in ws): bad(q, "a wrong option equals the answer")
    if len(set(q["wrong"] + [q["answer"]])) != 4: bad(q, "duplicate option text")
    if any(w <= 0 for w in ws): bad(q, "option ≤ 0")
    if why and q["answer"] not in (q["why"] or ""): bad(q, "explanation doesn't show the answer")

def pimode(en):
    if "Use π = 3.14" in en: return "314"
    if "Use π = 22/7" in en: return "227"
    if "in terms of π" in en: return "inpi"
    if "π button" in en: return "calc"
    return None
def pi_check(q, coef, unit, extra=F(0)):
    """value = coef·π (+ extra). inpi: answer is the coefficient (extra must be 0)."""
    mode = pimode(q["en"])
    if mode is None: return bad(q, "no π instruction")
    if mode == "inpi":
        assert extra == 0; return check(q, coef, pireader(unit))
    if mode == "calc":
        true = F(coef * F(math.pi)) + extra
        # stay clear of rounding knife-edges
        return check(q, true, reader(unit), dp=1)
    return check(q, coef * pi_val(mode) + extra, reader(unit))

# ---------- main ----------
data = json.load(open(sys.argv[1]))
for q in data:
    t = q["data"].get("t"); count[q["mk"]] += 1; en = q["en"]
    for s in [en, q["answer"], q["why"] or ""] + q["wrong"]:
        if re.search(r"NaN|undefined|Infinity|\[object", s): bad(q, "NaN/undefined in text")
    fig = read_fig(q)
    if fig:
        for k in ("drawn_wrong", "badlabel", "label_mismatch", "label_not_edge", "bad_height", "r_mismatch", "grid_uneven", "off_grid"):
            if fig.get(k): bad(q, "drawing: " + k)
    try:
        if t in ("rarea", "larea", "gable"):
            check(q, shoelace(fig["P"]), reader("m²"))
        elif t in ("rper", "lper"):
            check(q, perim(fig["P"]), reader("m"))
        elif t == "lmiss":
            ql = lab(fig, "q"); assert len(ql) == 1
            check(q, F(math.isqrt(ql[0]["L2"].numerator), math.isqrt(ql[0]["L2"].denominator)), reader("m"))
            if len(lab(fig, "e")) != 5: bad(q, "lmiss: not 5 other sides shown")
        elif t == "price":
            p = N(re.search(r"costs €([\d,.]+) per m²", en)[1]); check(q, shoelace(fig["P"]) * p, reader("€"))
        elif t == "packs":
            c = N(re.search(r"covers ([\d.]+) m²", en)[1]); A = shoelace(fig["P"])
            check(q, F(ceil(A / c)), reader("packs"))
        elif t == "skirt":
            d = N(re.search(r"which is ([\d.]+) m wide", en)[1]); check(q, perim(fig["P"]) - d, reader("m"))
        elif t == "tiles":
            m = re.search(r"A floor is ([\d.]+) m by ([\d.]+) m\. Square tiles (\d+) cm by \3 cm", en)
            W, H, tl = N(m[1]) * 100, N(m[2]) * 100, N(m[3])
            assert (W / tl).denominator == 1 and (H / tl).denominator == 1, "tiles don't fit exactly"
            check(q, W / tl * H / tl, reader("tiles"))
        elif t in ("tri", "para", "rtarea"):
            if t != "rtarea":   # area from the drawing must equal base × the LABELLED perpendicular height
                hs = lab(fig, "h"); base = [l for l in lab(fig, "e") if l["a"][1] == 0 and l["b"][1] == 0]
                assert len(hs) == 1 and len(base) == 1
                k = F(1, 2) if t == "tri" else 1
                if k * base[0]["v"] * hs[0]["v"] != shoelace(fig["P"]): bad(q, "height label doesn't fit the drawing")
            check(q, shoelace(fig["P"]), reader("cm²"))
        elif t in ("rtper", "paraper"):
            check(q, perim(fig["P"]), reader("cm"))
        elif t == "whichtri":
            A = shoelace(fig["P"]); good = 0
            for o in [q["answer"]] + q["wrong"]:
                e = o.replace("½", "1/2").replace("×", "*").replace(" ", "")
                v = eval("+".join("*".join("F('%s')" % x for x in term.split("*")) for term in e.split("+")))
                if v == A: good += 1; ok = o
            if good != 1 or ok != q["answer"]: bad(q, "whichtri: not exactly one right calculation")
            if len(q["wrong"]) != 3: bad(q, "not 3 wrong options")
        elif t in ("findht", "findhp"):
            m = re.search(r"area of ([\d,.]+) cm² and a base of ([\d.]+) cm", en); A, b = N(m[1]), N(m[2])
            check(q, 2 * A / b if t == "findht" else A / b, reader("cm"))
        elif t in ("circ", "carea"):
            if fig: r = fig["r"]
            else:
                m = re.search(r"a (radius|diameter) of ([\d.]+) cm", en); r = N(m[2]) / (2 if m[1] == "diameter" else 1)
            if t == "circ": pi_check(q, 2 * r, "cm")
            else: pi_check(q, r * r, "cm²")
        elif t in ("semiarea", "quarea"):
            r = fig["r"]; pi_check(q, r * r / (2 if t == "semiarea" else 4), "m²")
        elif t == "semiper":
            r = fig["r"]; pi_check(q, r, "m", extra=2 * r)
        elif t == "quper":
            r = fig["r"]; pi_check(q, r / 2, "m", extra=2 * r)
        elif t in ("winarea", "winper"):
            w = lab(fig, "w")[0]["v"]; h = lab(fig, "h")[0]["v"]; r = w / 2
            if t == "winarea": pi_check(q, r * r / 2, "m²", extra=w * h)
            else: pi_check(q, r, "m", extra=w + 2 * h)
        elif t in ("trackper", "trackarea"):
            L = lab(fig, "l")[0]["v"]; d = lab(fig, "d")[0]["v"]; r = d / 2
            if t == "trackper": pi_check(q, d, "m", extra=2 * L)
            else: pi_check(q, r * r, "m²", extra=L * d)
        elif t == "rad":
            k = q["data"]["kind"]
            if k == "cpi": m = re.search(r"circumference of a circle is ([\d.]+)π cm", en); r = N(m[1]) / 2
            elif k == "api": m = re.search(r"area of a circle is ([\d.]+)π cm²", en); r2 = N(m[1]); r = F(math.isqrt(r2.numerator), math.isqrt(r2.denominator)); assert r * r == r2
            elif k == "c314": m = re.search(r"circumference of a circle is ([\d.]+) cm\. Use π = 3\.14", en); r = N(m[1]) / F(314, 100) / 2
            else:
                m = re.search(r"area of a circle is ([\d.]+) cm²\. Use π = 3\.14", en); r2 = N(m[1]) / F(314, 100)
                r = F(math.isqrt(r2.numerator), math.isqrt(r2.denominator)); assert r * r == r2
            check(q, r, reader("cm"))
        elif t == "wheel":
            m = re.search(r"diameter of (\d+) cm\. \w+'s wheel turns (\d+) times", en); d, n = N(m[1]), N(m[2])
            if "22/7" in en: check(q, F(22, 7) * d * n / 100, reader("m"))
            else:
                assert "nearest metre" in en; check(q, F(math.pi) * d * n / 100, reader("m"), dp=0)
        elif t == "turns":
            m = re.search(r"diameter of (\d+) cm\. How many COMPLETE turns does it make in (\d+) m", en); d, L = N(m[1]), N(m[2])
            check(q, F(floor(F(L * 100) / (F(math.pi) * d))), reader("turns"), why=False)
            if q["answer"].split()[0] not in q["why"]: bad(q, "explanation doesn't show the answer")
        elif t == "planreal":
            m = re.search(r"scale of 1 : (\d+)\. A wall is ([\d.]+) cm long on the plan", en); n, p = N(m[1]), N(m[2])
            check(q, p * n / 100, reader("m"))
        elif t == "cmrep":
            m = re.search(r"1 cm represents ([\d.]+) m\. A room is ([\d.]+) cm long", en); check(q, N(m[1]) * N(m[2]), reader("m"))
        elif t == "realplan":
            m = re.search(r"scale of 1 : (\d+)\. A real wall is ([\d.]+) m long", en); n, R = N(m[1]), N(m[2])
            check(q, R * 100 / n, reader("cm"))
        elif t == "findscale":
            m = re.search(r"really ([\d.]+) m long is drawn ([\d.]+) cm long", en); n = N(m[1]) * 100 / N(m[2])
            opts = [N(o.replace("1 : ", "")) for o in [q["answer"]] + q["wrong"]]
            if opts[0] != n or opts.count(n) != 1: bad(q, "WRONG ANSWER")
            if len(q["wrong"]) != 3: bad(q, "not 3 wrong options")
        elif t == "planarea":
            n = N(re.search(r"scale of 1 : (\d+)", en)[1]); ls = [l["v"] for l in lab(fig, "e")]
            assert all(l["u"] == "cm" for l in lab(fig, "e"))
            check(q, shoelace(fig["P"]) * n * n / 10000, reader("m²"))
        elif t in ("map", "mapback"):
            n = N(re.search(r"scale of 1 : ([\d,]+)", en)[1])
            if t == "map": d = N(re.search(r"([\d.]+) cm apart on the map", en)[1]); check(q, d * n / 100000, reader("km"))
            else: D = N(re.search(r"A walk is ([\d.]+) km long", en)[1]); check(q, D * 100000 / n, reader("cm"))
        elif t in ("gridarea", "gridper"):
            sq = N(re.search(r"Each square stands for ([\d.]+) m by \1 m", en)[1]); G = fig["G"]
            if t == "gridarea": check(q, shoelace(G) * sq * sq, reader("m²"))
            else: check(q, perim(G) * sq, reader("m"))
        else:
            bad(q, "unknown type " + str(t))
    except Exception as e:
        bad(q, "checker could not read: " + type(e).__name__ + " " + str(e)[:60])

print(f"{len(data)} questions, {len(count)} makers")
if not problems: print("0 problems")
for k, v in problems.most_common():
    print(f"{v:6}  {k}\n        e.g. {examples[k]}")
