#!/usr/bin/env python3
"""Independent checker for the Exam Mix "Problem solver" questions.
Reads the JSON lines from src/test_exam_mix.js and recomputes every answer from the
question TEXT (the fact card), with exact Fractions. Usage:
  TL=exam-mix.html N=400 node src/test_exam_mix.js > /tmp/em.jsonl && python3 src/test_exam_mix.py /tmp/em.jsonl"""
import sys, json, re, math
from fractions import Fraction as F

def nums(s):
    return [F(x) for x in re.findall(r"\d+(?:\.\d+)?", s.replace("−", "-"))]

def money(x, sym="€"):
    x = F(x)
    c = round(x * 100)
    assert abs(x * 100 - c) < F(1, 10**9), ("money not whole cents", x)
    return sym + (str(c // 100) if c % 100 == 0 else "%d.%02d" % (c // 100, c % 100))

def val(opt):
    """numeric value of an option for 'unequal' checks"""
    m = re.search(r"-?\d+(?:\.\d+)?", opt.replace(":", ""))
    return opt

FRAC = {"½": 2, "⅓": 3, "¼": 4, "⅕": 5}

def hm(m):
    m %= 1440
    return "%02d:%02d" % (m // 60, m % 60)

def solve(q):
    f, t = q["facts"], q["t"]
    if t == "fence":
        l, w = nums(f[0]); p, = nums(f[1]); return money(2 * (l + w) * p)
    if t == "paint":
        l, h = nums(f[0]); coats = nums(f[1])[0]; cov = nums(f[2])[-1]
        # "1 tin covers 5 m²" -> numbers 1, 5, 2 (the ² is not a digit)
        cov = nums(f[2])[1]
        A = l * h * coats
        assert A % cov != 0, "paint: must need rounding"
        return "%d tins" % math.ceil(A / cov)
    if t == "plan":
        a, b = nums(f[0]); T, = nums(f[1]); g = (T - a) / b
        assert g.denominator == 1 and g > 0; return "%d GB" % g
    if t == "sale":
        P, = nums(f[0]); x, = nums(f[1]); y, = nums(f[2])
        return money(P * (100 - x) / 100 * (100 - y) / 100)
    if t == "share":
        T, a, b = nums(f[0]); assert a < b
        d = FRAC[re.search(r"[½⅓¼⅕]", f[2]).group(0)]
        s = T * a / (a + b); return money(s - s / d)
    if t == "trip":
        d, v = nums(f[0]); hh, mm = map(int, re.search(r"(\d\d):(\d\d)", f[1]).groups())
        tm = d / v * 60; assert tm.denominator == 1
        return hm(hh * 60 + mm + int(tm))
    if t == "path":
        a, b = nums(f[0]); c = math.isqrt(int(a * a + b * b)); assert c * c == a * a + b * b
        return "%d m" % (a + b - c)
    if t == "mean":
        s = nums(f[0]); m = nums(f[1])[0]; n = nums(f[1])[1]; assert n == len(s) + 1
        need = m * n - sum(s); assert 0 <= need <= 100; return str(need)
    if t == "bag":
        r, b = nums(f[0]); return str(b - r)
    if t == "tank":
        l, w, h = nums(f[0]); rate, = nums(f[1]); mins = l * w * h / 1000 / rate
        assert mins.denominator == 1; return "%d min" % mins
    if t == "wage":
        r, h = nums(f[0]); o, = nums(f[1]); return money(r * h + r * F(3, 2) * o)
    if t == "tiles":
        a, b = nums(f[0]); N, = nums(f[1])
        n = 0
        while a * (n + 1) + b <= N: n += 1
        return "Stage %d" % n
    if t == "cash":
        E, = nums(f[0]); one, r = nums(f[1]); assert one == 1; sp, = nums(f[2])
        return money(E * r - sp, "$")
    if t == "rect":
        P, = nums(f[0]); d, = nums(f[1]); w = (P / 2 - d) / 2; assert w.denominator == 1 and w > 0
        return "%d cm²" % (w * (w + d))
    if t == "vat":
        base, = nums(f[0]); v, = nums(f[1]); parts, = nums(f[2]); return money(base * (1 + v / 100) / parts)
    raise ValueError(t)

def main():
    n = bad = 0; seen = {}
    for line in open(sys.argv[1], encoding="utf-8"):
        q = json.loads(line); n += 1; seen[q["t"]] = seen.get(q["t"], 0) + 1
        try:
            a = solve(q)
            assert a == q["answer"], ("answer", a, q["answer"])
            assert len(q["wrong"]) == 3, "need 3 wrong options"
            assert a not in q["wrong"], "answer among wrong"
            assert len(set(q["wrong"])) == 3
            for w in q["wrong"]:
                assert not re.search(r"NaN|undefined|Infinity|-", w), w
            assert a in q["why"] or q["t"] in ("tiles",) or a.replace(" tins", "") in q["why"] or a.split()[0] in q["why"] or a.replace("Stage ", "") in q["why"], ("why lacks answer", q["why"])
        except AssertionError as e:
            bad += 1
            if bad < 15: print("BAD", q["t"], e, q["facts"], q["answer"], q["wrong"])
    print(n, "questions,", bad, "problems;", seen)
    sys.exit(1 if bad else 0)

if __name__ == "__main__":
    main()
