#!/usr/bin/env python3
"""Independent checker for Number-Line Shade (inequalities).
node src/test_number_line_shade.js > /tmp/nls.json ; python3 src/test_number_line_shade.py /tmp/nls.json
Every answer is worked out again from the question TEXT / the drawn SVG (not from the game's data),
and every wrong option must give a different solution set."""
import json, re, sys, html as H
from fractions import Fraction as F

def clean(s): return H.unescape(re.sub(r"<[^>]+>", " ", s or "")).replace("−", "-").strip()

# ---------- linear expressions: returns (coef, const) in variable v ----------
def lin(s, v="x"):
    s = s.replace(" ", "").replace("−", "-")
    m = re.fullmatch(r"\((.+)\)/(\d+)", s)
    if m:
        a, b = lin(m.group(1), v); d = int(m.group(2)); return (a / d, b / d)
    m = re.fullmatch(r"(-?\d*)\((.+)\)", s)
    if m and "(" not in m.group(2):
        k = m.group(1); k = 1 if k in ("", "+") else (-1 if k == "-" else int(k))
        a, b = lin(m.group(2), v); return (a * k, b * k)
    a = F(0); b = F(0)
    for t in re.findall(r"[+-]?[^+-]+", s):
        if v in t:
            t2 = t.replace(v, "")
            m2 = re.fullmatch(r"([+-]?)(\d*)/(\d+)", t2)
            if m2:
                c = F(int(m2.group(2) or 1), int(m2.group(3))); a += -c if m2.group(1) == "-" else c; continue
            c = 1 if t2 in ("", "+") else (-1 if t2 == "-" else int(t2)); a += c
        else:
            b += F(t)
    return (a, b)

OPS = {"<": "<", ">": ">", "≤": "<=", "≥": ">="}
FLIP = {"<": ">", ">": "<", "<=": ">=", ">=": "<="}

class Iv:  # interval on the real line; lo/hi None = no end
    def __init__(s, lo=None, loIn=False, hi=None, hiIn=False): s.lo, s.loIn, s.hi, s.hiIn = lo, loIn, hi, hiIn
    def has(s, x): return (s.lo is None or (x >= s.lo if s.loIn else x > s.lo)) and (s.hi is None or (x <= s.hi if s.hiIn else x < s.hi))
    def key(s): return (s.lo, s.loIn if s.lo is not None else None, s.hi, s.hiIn if s.hi is not None else None)
    def __and__(s, o):
        r = Iv(s.lo, s.loIn, s.hi, s.hiIn)
        if o.lo is not None and (r.lo is None or o.lo > r.lo or (o.lo == r.lo and not o.loIn)): r.lo, r.loIn = o.lo, o.loIn
        if o.hi is not None and (r.hi is None or o.hi < r.hi or (o.hi == r.hi and not o.hiIn)): r.hi, r.hiIn = o.hi, o.hiIn
        return r

def solve1(a, b, op):  # a x + b OP 0
    assert a != 0
    v = -b / a
    if a < 0: op = FLIP[op]
    return Iv(v, op == ">=", None, False) if op in (">", ">=") else Iv(None, False, v, op == "<=")

def parse_ineq(s, v="x"):
    """'2x + 3 < 11', '-1 < x - 2 <= 5', 'x >= 3' (optionally ', x ∈ ℤ') -> (Iv, set)"""
    s = s.replace("−", "-"); st = "R"
    m = re.search(r",\s*" + v + r"\s*∈\s*([ℕℤℝ])\s*$", s)
    if m: st = {"ℕ": "N", "ℤ": "Z", "ℝ": "R"}[m.group(1)]; s = s[:m.start()]
    parts = re.split(r"\s*([<>≤≥])\s*", s.strip())
    if len(parts) == 3:
        (a1, b1), (a2, b2) = lin(parts[0], v), lin(parts[2], v)
        return solve1(a1 - a2, b1 - b2, OPS[parts[1]]), st
    if len(parts) == 5:
        k1, op1, mid, op2, k2 = parts
        A, B = lin(mid, v); k1 = lin(k1, v); k2 = lin(k2, v); assert k1[0] == 0 and k2[0] == 0
        left = solve1(-A, k1[1] - B, OPS[op1])   # k1 OP1 A x + B  ->  k1 - (Ax+B) OP1 0
        right = solve1(A, B - k2[1], OPS[op2])
        return left & right, st
    raise ValueError("can't parse " + s)

def int_list(iv, st, lo=-80, hi=80):
    return [x for x in range(lo, hi + 1) if (st != "N" or x >= 1) and iv.has(x)]
def same(i1, s1, i2, s2):
    if s1 == "R" or s2 == "R": return s1 == s2 and i1.key() == i2.key()
    return int_list(i1, s1) == int_list(i2, s2)

def parse_set(s):
    s = s.replace("−", "-").strip()
    assert s[0] == "{" and s[-1] == "}", s
    body = s[1:-1].strip()
    if not body: return [], False
    items = [t.strip() for t in body.split(",")]
    more = items[-1] == "…"
    if more: items = items[:-1]
    return [int(t) for t in items], more

def attrs(tag): return dict(re.findall(r'([\w-]+)="([^"]*)"', tag))

def read_nl(svg):
    """measure the number line: returns (kind, data)."""
    top = attrs(re.search(r"<svg[^>]*>", svg).group(0)); st = top["data-set"]; L, R = int(top["data-l"]), int(top["data-r"])
    ticks = {int(a["data-v"]): float(a["x"]) for a in map(attrs, re.findall(r'<text class="tk"[^>]*>', svg))}
    assert sorted(ticks) == list(range(L, R + 1)), "ticks"
    u = (ticks[R] - ticks[L]) / (R - L)
    for t, x in ticks.items(): assert abs(x - (ticks[L] + (t - L) * u)) < 0.05, "uneven ticks"
    val = lambda px: (px - ticks[L]) / u + L
    if st == "R":
        sh = attrs(re.search(r'<line class="sh"[^>]*>', svg).group(0))
        eps = [attrs(e) for e in re.findall(r'<circle class="ep"[^>]*>', svg)]
        x1, x2 = sorted([float(sh["x1"]), float(sh["x2"])])
        lo = hi = None; loIn = hiIn = False
        for e in eps:
            cx = float(e["cx"]); v = val(cx); assert abs(v - round(v)) < 0.01, "dot off a tick"; v = round(v)
            closed = e["fill"] != "#fff"
            if abs(cx - x1) < 0.5: lo, loIn = F(v), closed
            elif abs(cx - x2) < 0.5: hi, hiIn = F(v), closed
            else: raise AssertionError("end dot not at the end of the shading")
        if lo is None: assert x1 < ticks[L], "left end must run off the line"
        if hi is None: assert x2 > ticks[R], "right end must run off the line"
        has_arrow_l = bool(re.search(r'<path d="M4 ', svg)); has_arrow_r = bool(re.search(r'<path d="M33\d ', svg))
        assert has_arrow_l == (lo is None) and has_arrow_r == (hi is None), "arrows"
        return "R", Iv(lo, loIn, hi, hiIn)
    dots = sorted(round(val(float(a["cx"]))) for a in map(attrs, re.findall(r'<circle class="dt"[^>]*>', svg)))
    more = {a["data-d"] for a in map(attrs, re.findall(r'<text class="more"[^>]*>', svg))}
    return "dots", (dots, "l" in more, "r" in more, L, R)

def matches_picture(pic, iv, st):
    kind, d = pic
    if kind == "R": return st == "R" and iv.key() == d.key()
    if st == "R": return False
    dots, ml, mr, L, R = d
    il = int_list(iv, st)
    inside = [x for x in il if L <= x <= R]
    return inside == dots and (any(x < L for x in il)) == ml and (any(x > R for x in il)) == mr

WORDS = {"at least": ">=", "at most": "<=", "more than": ">", "less than": "<", "no more than": "<=", "no less than": ">=", "over": ">", "under": "<"}

def ceil(f): return -((-f.numerator) // f.denominator)
def floor(f): return f.numerator // f.denominator

def check(q):
    en, ans, wrong = q["en"], q["answer"], q["wrong"]
    opts = [ans] + wrong
    assert len(wrong) == 3 and len(set(opts)) == 4, "need 4 different options"
    for o in opts: assert "NaN" not in o and "undefined" not in o and "-" not in o, "bad text " + o
    hq = q["html"] or ""
    m = re.search(r'<div class="iq">(.*?)</div>', hq); qtext = clean(m.group(1)) if m else None
    t = None
    if "<svg class=\"nl\"" in hq:
        pic = read_nl(hq)
        ok = [o for o in opts if matches_picture(pic, *parse_ineq(o))]
        assert ok == [ans], "picture matches %s" % ok; return "read"
    if "<svg class=\"gr\"" in hq:
        top = attrs(re.search(r"<svg[^>]*>", hq).group(0)); xa, ya = int(top["data-xa"]), int(top["data-ya"]); sx, sy = F(top["data-sx"]), F(top["data-sy"]); p, Hh = int(top["data-p"]), int(top["data-h"])
        X = lambda px: (F(px) - p) / sx + xa; Y = lambda py: (Hh - p - F(py)) / sy + ya
        fn = attrs(re.search(r'<line class="fn"[^>]*>', hq).group(0)); kl = attrs(re.search(r'<line class="kl"[^>]*>', hq).group(0))
        x1, y1, x2, y2 = X(fn["x1"]), Y(fn["y1"]), X(fn["x2"]), Y(fn["y2"]); k = Y(kl["y1"])
        assert abs(k - round(k)) < F(1, 50), "y = k not on a gridline"; k = round(k)
        lab = re.search(r">y = ([^<]+)</text>", hq).group(1).replace("−", "-"); assert int(lab) == k, "label"
        m_ = (y2 - y1) / (x2 - x1); x0 = x1 + (k - y1) / m_
        assert abs(x0 - round(x0)) < F(1, 50), "crossing not on a gridline"; x0 = round(x0)
        assert xa < x0 < 6, "crossing inside the grid"
        op = OPS[re.search(r"y ([<>≤≥]) ", en).group(1)]
        # y = m x + c  OP k  ->  m (x - x0) OP 0
        sol = solve1(F(1) if m_ > 0 else F(-1), F(-x0) if m_ > 0 else F(x0), op)
        ok = [o for o in opts if same(sol, "R", *parse_ineq(o))]
        assert ok == [ans], "graph %s" % ok; return "graph"
    mw = re.fullmatch(r"x is (.+) (−?\d+)\.", en)
    if mw:
        v = int(mw.group(2).replace("−", "-")); sol = parse_ineq("x %s %d" % ({"<": "<", ">": ">", "<=": "≤", ">=": "≥"}[WORDS[mw.group(1)]], v))[0]
        ok = [o for o in opts if same(sol, "R", *parse_ineq(o))]; assert ok == [ans], "words %s" % ok; return "words"
    if en == "Solve.":
        sol, st = parse_ineq(qtext)
        ok = [o for o in opts if same(sol, st, *parse_ineq(o))]; assert ok == [ans], "solve %s" % ok
        assert sol.lo is None or sol.lo.denominator == 1; assert sol.hi is None or sol.hi.denominator == 1
        return "solve"
    if en == "Which value of x fits?":
        sol, st = parse_ineq(qtext)
        ok = [o for o in opts if sol.has(int(o.replace("−", "-")))]; assert ok == [ans], "which %s" % ok; return "which"
    if en == "List the values.":
        sol, st = parse_ineq(qtext); assert st in "NZ"
        il = int_list(sol, st); assert il and len(il) < 40
        def eq(o):
            L, more = parse_set(o)
            return (not more) and L == il
        ok = [o for o in opts if eq(o)]; assert ok == [ans], "list %s" % ok; return "list"
    if en in ("Biggest value of x?", "Smallest value of x?", "How many values?"):
        sol, st = parse_ineq(qtext); il = int_list(sol, st, -200, 200)
        v = max(il) if en.startswith("Big") else min(il) if en.startswith("Small") else len(il)
        assert ans.replace("−", "-") == str(v), "%s want %s" % (ans, v)
        return "num"
    nums = [int(n) for n in re.findall(r"\d+", en)]
    if en.startswith("🚕"):
        f, p_, B = nums; v = floor(F(B - f, p_)); assert ans == str(v) and v >= 1; return "ctx"
    if en.startswith("🛗") and en.endswith("Most boxes?"):
        L, mm, w = nums; v = floor(F(L - mm, w)); assert ans == str(v) and v >= 1; return "ctx"
    if en.startswith("🐷"):
        s0, w, T = nums; v = ceil(F(T - s0, w)); assert ans == str(v) and v >= 1; return "ctx"
    if en.startswith("🎟️"):
        p_, f, B = nums; v = floor(F(B - f, p_)); assert ans == str(v) and v >= 1; return "ctx"
    if en.startswith("🛗") and en.endswith("Which one?"):
        L, mm, w = nums  # m + w b <= L over the reals
        want = solve1(F(w), F(mm - L), "<=")
        ok = [o for o in opts if parse_ineq(o, "b")[0].key() == want.key()]; assert ok == [ans], "form %s" % ok; return "form"
    raise AssertionError("unknown question: " + en)

if __name__ == "__main__":
    data = json.load(open(sys.argv[1])); bad = 0; kinds = {}
    for q in data:
        try:
            k = check(q); kinds[k] = kinds.get(k, 0) + 1
        except Exception as e:
            bad += 1
            if bad <= 12: print("PROBLEM", q.get("mk"), "|", q["en"], "|", clean(q["html"])[:80], "|", q["answer"], q["wrong"], "|", repr(e))
    print(len(data), "questions,", bad, "problems", kinds)
    sys.exit(1 if bad else 0)
