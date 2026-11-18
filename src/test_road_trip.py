#!/usr/bin/env python3
"""Independent checker for Road Trip (speed, distance, time & currency, JC Maths topic 20).
Reads every question's TEXT (and the distance-time graph SVG / trip list), works the answer out again
with exact Fractions and checks the game's answer and every wrong option.
Usage: N=400 node src/test_road_trip.js > /tmp/rt.json ; python3 src/test_road_trip.py /tmp/rt.json"""
import json, re, sys
from fractions import Fraction as F
from math import floor
from collections import Counter

problems = Counter(); examples = {}; count = Counter()
def bad(q, msg):
    problems[msg] += 1
    examples.setdefault(msg, (q["mk"], q["en"], q["answer"], q["wrong"]))

def N(s): return F(s.replace(",", ""))
TM = r"((?:\d+ h \d+ min)|(?:\d+ h)|(?:\d+ min))"
def tmin(s):
    m = re.fullmatch(r"(?:(\d+) h)?\s?(?:(\d+) min)?", s.strip())
    assert m and (m[1] or m[2]), "bad time " + s
    return int(m[1] or 0) * 60 + int(m[2] or 0)
def half_up(x, unit=F(1, 100)): return F(floor(x / unit + F(1, 2))) * unit

# option readers (each also checks the format)
def r_kmh(o):
    m = re.fullmatch(r"(\d{1,3}(?:,\d{3})*(?:\.\d)?) km/h", o); assert m, "bad km/h " + o; return N(m[1])
def r_km(o):
    m = re.fullmatch(r"(\d{1,3}(?:,\d{3})*(?:\.\d)?) km", o); assert m, "bad km " + o; return N(m[1])
def r_m(o):
    m = re.fullmatch(r"(\d{1,3}(?:,\d{3})*(?:\.\d)?) m", o); assert m, "bad m " + o; return N(m[1])
def r_ms(o):
    m = re.fullmatch(r"(\d{1,3}(?:,\d{3})*(?:\.\d\d?)?) m/s", o); assert m, "bad m/s " + o; return N(m[1])
def r_hours(o):
    m = re.fullmatch(r"(\d+(?:\.\d{1,3})?) hours", o); assert m, "bad hours " + o; return N(m[1])
def r_hm(o):
    assert re.fullmatch(TM, o), "bad h/min " + o
    t = tmin(o); m = re.search(r"(\d+) min", o)
    assert not m or 0 < int(m[1]) < 60, "minutes ≥ 60 " + o
    return t
def r_clk(o):
    m = re.fullmatch(r"([01]\d|2[0-3]):([0-5]\d)", o); assert m, "bad clock " + o; return int(m[1]) * 60 + int(m[2])
SYM = {"£": "GBP", "$": "USD", "CHF ": "CHF", "€": "EUR"}
def r_money(sym):
    def f(o):
        m = re.fullmatch(re.escape(sym) + r"(\d{1,3}(?:,\d{3})*\.\d\d)", o); assert m, "bad money " + o; return N(m[1])
    return f

def numeric(q, true, reader):
    try:
        a = reader(q["answer"]); ws = [reader(w) for w in q["wrong"]]
    except AssertionError as e:
        return bad(q, str(e).split(" ")[0] + " " + str(e).split(" ")[1])
    if a != true: bad(q, "WRONG ANSWER")
    if len(q["wrong"]) != 3: bad(q, "not 3 wrong options")
    vals = [a] + ws
    if len(set(vals)) != len(vals): bad(q, "duplicate value among options")
    if any(w <= 0 for w in ws): bad(q, "wrong option ≤ 0")
    if q["answer"] not in (q["why"] or ""): bad(q, "explanation doesn't show the answer")

def choice(q, is_true):
    opts = [q["answer"]] + q["wrong"]
    t = [o for o in opts if is_true(o)]
    if t != [q["answer"]]: bad(q, "CHOICE: not exactly the answer is right")
    if len(q["wrong"]) < 3: bad(q, "too few wrong options")
    if len(set(opts)) != len(opts): bad(q, "duplicate option")

def ev(expr):
    m = re.fullmatch(r"([\d.]+) ([÷×−+]) ([\d.]+)", expr); assert m, expr
    a, op, b = F(m[1]), m[2], F(m[3])
    return a / b if op == "÷" else a * b if op == "×" else a - b if op == "−" else a + b

# ---------- distance-time graph reader ----------
def graph(q):
    s = q["html"]
    start = int(re.search(r'data-start="(\d+)"', s)[1])
    x0, xs, y0, ys = (F(re.search(rf'data-{k}="([\d.e-]+)"', s)[1]) for k in ("x0", "xs", "y0", "ys"))
    pts = []
    for c in re.finditer(r'<circle class="gp" cx="([\d.]+)" cy="([\d.]+)" r="[\d.]+" data-t="(\d+)" data-d="(\d+)" data-n="(\w)"/>', s):
        cx, cy, t, d, n = float(c[1]), float(c[2]), int(c[3]), int(c[4]), c[5]
        if abs(cx - float(x0 + xs * t)) > 0.01 or abs(cy - float(y0 - ys * d)) > 0.01: bad(q, "graph point not where its data says")
        pts.append((t, d, n))
    # every point must sit on the drawn line, and the axis labels must match the scale
    poly = re.search(r'<polyline class="jl" points="([^"]+)"', s)[1].split()
    if len(poly) != len(pts): bad(q, "line and points differ")
    for lab in re.finditer(r'<text x="([\d.]+)" y="([\d.]+)" class="ax" text-anchor="middle">(\d\d):(\d\d)</text>', s):
        t = int(lab[3]) * 60 + int(lab[4]) - start
        if abs(float(lab[1]) - float(x0 + xs * t)) > 0.01: bad(q, "time label in the wrong place")
    for lab in re.finditer(r'<text x="[\d.]+" y="([\d.]+)" class="ax" text-anchor="end">(\d+)</text>', s):
        if abs(float(lab[1]) - 4 - float(y0 - ys * int(lab[2]))) > 0.01: bad(q, "distance label in the wrong place")
    if [p[2] for p in pts] != list("OABCDE"[:len(pts)]): bad(q, "point names")
    if pts[0][:2] != (0, 0): bad(q, "graph doesn't start at home")
    return start, pts

def at(pts, t):
    for (t1, d1, _), (t2, d2, _) in zip(pts, pts[1:]):
        if t1 <= t <= t2: return F(d1) + F(d2 - d1) * (t - t1) / (t2 - t1)
    raise AssertionError("time not on graph")

def check(q):
    en, html = q["en"], q["html"] or ""
    txt = en + " " + q["answer"] + " " + " ".join(q["wrong"]) + " " + (q["why"] or "")
    for junk in ("NaN", "undefined", "Infinity", "null", "+ −", "−−", " 0 min", "60 min"):
        if junk in txt: bad(q, "junk text " + junk.strip())
    t = q["data"].get("t")
    count[t] += 1

    if t == "speed":
        r = re.fullmatch(r"A \w+ travels ([\d,]+) km in " + TM + r"\. What is its average speed\?", en)
        return numeric(q, N(r[1]) * 60 / tmin(r[2]), r_kmh) if r else bad(q, "unparsed speed")
    if t == "dist":
        r = re.fullmatch(r"A \w+ travels for " + TM + r" at an average speed of ([\d,]+) km/h\. How far does it go\?", en)
        return numeric(q, N(r[2]) * tmin(r[1]) / 60, r_km) if r else bad(q, "unparsed dist")
    if t == "time":
        r = re.fullmatch(r"How long does it take to travel ([\d,]+) km at an average speed of ([\d,]+) km/h\?", en)
        return numeric(q, N(r[1]) / N(r[2]) * 60, r_hm) if r else bad(q, "unparsed time")
    if t == "tohrs":
        r = re.fullmatch(r"Write " + TM + r" in hours, as a decimal\.", en)
        return numeric(q, F(tmin(r[1]), 60), r_hours) if r else bad(q, "unparsed tohrs")
    if t == "tohm":
        r = re.fullmatch(r"A journey takes ([\d.]+) hours\. How long is that in hours and minutes\?", en)
        return numeric(q, F(r[1]) * 60, r_hm) if r else bad(q, "unparsed tohm")
    if t == "arrive":
        r = re.fullmatch(r"(\S+) leaves at (\d\d:\d\d) and drives ([\d,]+) km at an average speed of ([\d,]+) km/h\. At what time does \1 arrive\?", en)
        return numeric(q, r_clk(r[2]) + N(r[3]) / N(r[4]) * 60, r_clk) if r else bad(q, "unparsed arrive")
    if t == "whichcalc":
        r = (re.fullmatch(r"A train goes ([\d,]+) km in " + TM + r"\. Which calculation gives its average speed in km/h\?", en) or
             re.fullmatch(r"A car drives for " + TM + r" at ([\d,]+) km/h\. Which calculation gives the distance in km\?", en) or
             re.fullmatch(r"A coach must travel ([\d,]+) km at ([\d,]+) km/h\. Which calculation gives the time in hours\?", en))
        if not r: return bad(q, "unparsed whichcalc")
        k = q["data"]["kind"]
        true = N(r[1]) * 60 / tmin(r[2]) if k == "speed" else N(r[2]) * tmin(r[1]) / 60 if k == "dist" else N(r[1]) / N(r[2])
        return choice(q, lambda o: ev(o) == true)
    if t == "avg2":
        r = re.fullmatch(r"(\S+) drives ([\d,]+) km in " + TM + r", then ([\d,]+) km in " + TM + r"\. What is \1's average speed for the whole journey\?", en)
        return numeric(q, (N(r[2]) + N(r[4])) * 60 / (tmin(r[3]) + tmin(r[5])), r_kmh) if r else bad(q, "unparsed avg2")
    if t == "avgspeeds":
        r = re.fullmatch(r"A lorry travels for " + TM + r" at ([\d,]+) km/h, then for " + TM + r" at ([\d,]+) km/h\. What is its average speed for the whole trip\?", en)
        if not r: return bad(q, "unparsed avgspeeds")
        t1, t2 = tmin(r[1]), tmin(r[3]); return numeric(q, (N(r[2]) * t1 + N(r[4]) * t2) / (t1 + t2), r_kmh)
    if t == "stop":
        r = re.fullmatch(r"(\S+) drives ([\d,]+) km in " + TM + r", stops for (\d+) minutes, then drives ([\d,]+) km in " + TM + r"\. What is the average speed for the whole journey, including the stop\?", en)
        return numeric(q, (N(r[2]) + N(r[5])) * 60 / (tmin(r[3]) + int(r[4]) + tmin(r[6])), r_kmh) if r else bad(q, "unparsed stop")
    if t == "round":
        r = re.fullmatch(r"(\S+) (?:cycles|drives) ([\d,]+) km to the lake at ([\d,]+) km/h and comes straight back at ([\d,]+) km/h\. What is the average speed for the round trip\?", en)
        if not r: return bad(q, "unparsed round")
        L, a, b = N(r[2]), N(r[3]), N(r[4]); return numeric(q, 2 * L / (L / a + L / b), r_kmh)
    if t == "tomps":
        r = re.fullmatch(r"Change ([\d,.]+) km/h into metres per second\.", en)
        return numeric(q, N(r[1]) * 1000 / 3600, r_ms) if r else bad(q, "unparsed tomps")
    if t == "tokmh":
        r = re.fullmatch(r"Change ([\d,.]+) m/s into kilometres per hour\.", en)
        return numeric(q, N(r[1]) * 3600 / 1000, r_kmh) if r else bad(q, "unparsed tokmh")
    if t == "run":
        r = re.fullmatch(r"(\S+) runs ([\d,]+) m in ([\d,]+) seconds\. What is \1's average speed\?", en)
        return numeric(q, N(r[2]) / N(r[3]), r_ms) if r else bad(q, "unparsed run")
    if t == "rundist":
        r = re.fullmatch(r"(\S+) runs at an average speed of ([\d.]+) m/s for (\d+) seconds\. How far does \1 run\?", en)
        return numeric(q, N(r[2]) * int(r[3]), r_m) if r else bad(q, "unparsed rundist")
    if t == "fastest":
        trips = {m[1]: (N(m[2]), tmin(m[3])) for m in re.finditer(r"<b>(\S+):</b> ([\d,]+) km in " + TM + "</li>", html)}
        if len(trips) != 4: return bad(q, "trip list")
        sp = {k: d * 60 / t for k, (d, t) in trips.items()}
        if len(set(sp.values())) != 4: bad(q, "two trips with the same speed")
        best = max(sp, key=sp.get)
        if sorted([q["answer"]] + q["wrong"]) != sorted(trips): bad(q, "options aren't the four names")
        return choice(q, lambda o: o == best)

    if t and t.startswith("g"):
        start, pts = graph(q)
        segs = list(zip(pts, pts[1:]))
        if t == "gread":
            r = re.search(r"How far from home was \S+ at (\d\d:\d\d)\?$", en)
            return numeric(q, at(pts, r_clk(r[1]) - start), r_km)
        if t == "gstop":
            flat = [(b[0] - a[0]) for a, b in segs if a[1] == b[1]]
            if len(flat) != 1: return bad(q, "not exactly one stop")
            return numeric(q, flat[0], r_hm)
        if t == "gspeed":
            r = re.search(r"speed between (\w) and (\w)\?$", en)
            a, b = [p for p in pts if p[2] == r[1]][0], [p for p in pts if p[2] == r[2]][0]
            if pts.index(b) != pts.index(a) + 1: bad(q, "not next to each other")
            if a[1] == b[1]: bad(q, "asked the speed of a stop")
            return numeric(q, F(abs(b[1] - a[1]) * 60, b[0] - a[0]), r_kmh)
        if t == "gavg":
            tot = sum(abs(b[1] - a[1]) for a, b in segs)
            return numeric(q, F(tot * 60, pts[-1][0]), r_kmh)
        if t == "gwhat":
            r = re.search(r"between (\w) and (\w)\?$", en)
            a, b = [p for p in pts if p[2] == r[1]][0], [p for p in pts if p[2] == r[2]][0]
            kind = "Moving away" if b[1] > a[1] else "Coming back" if b[1] < a[1] else "Stopped"
            return choice(q, lambda o: o.startswith(kind))
        if t == "gfast":
            sp = {f"{a[2]} to {b[2]}": F(abs(b[1] - a[1]), b[0] - a[0]) for a, b in segs}
            m = max(sp.values())
            if list(sp.values()).count(m) != 1: bad(q, "two fastest parts")
            if sorted([q["answer"]] + q["wrong"]) != sorted(sp): bad(q, "options aren't the parts")
            return choice(q, lambda o: sp[o] == m)

    if t in ("tof", "toe", "fee", "rate", "whichcur", "compare"):
        rr = re.search(r"€1 = (£|\$|CHF )(\d\.\d{2,3})", en)
        if t != "rate":
            if not rr: return bad(q, "no rate")
            sym, R = rr[1], F(rr[2])
        if t == "tof":
            r = re.search(r"(\S+) changes €([\d,]+) into (sterling|US dollars|Swiss francs)\. How much does \1 get\?$", en)
            if {"sterling": "£", "US dollars": "$", "Swiss francs": "CHF "}[r[3]] != sym: bad(q, "currency name ≠ symbol")
            return numeric(q, half_up(N(r[2]) * R), r_money(sym))
        if t == "toe":
            r = re.search(r"changes " + re.escape(sym) + r"([\d,]+) back into euro\. How many euro does \S+ get \(to the nearest cent\)\?$", en)
            return numeric(q, half_up(N(r[1]) / R), r_money("€"))
        if t == "fee":
            r = re.fullmatch(r"A bank takes ([\d.]+)% commission from the euro before changing it\. (\S+) changes €([\d,]+) into (sterling|US dollars|Swiss francs) at €1 = .*\. How much does \2 get\?", en)
            return numeric(q, half_up(N(r[3]) * (1 - F(r[1]) / 100) * R), r_money(sym))
        if t == "rate":
            r = re.fullmatch(r"(\S+) changes €([\d,]+) and gets (£|\$|CHF )([\d,]+\.\d\d)\. What is the exchange rate\?", en)
            true = N(r[4]) / N(r[2])
            def rd(o):
                m = re.fullmatch(r"€1 = " + re.escape(r[3]) + r"(\d+\.\d{1,3})", o); assert m, "bad rate " + o; return F(m[1])
            return numeric(q, true, rd)
        if t == "whichcur":
            r = re.search(r"Which calculation changes (?:€(\d+) into \S.*|" + re.escape(sym) + r"(\d+) into euro)\?$", en)
            true = N(r[1]) * R if r[1] else N(r[2]) / R
            return choice(q, lambda o: ev(o) == true)
        if t == "compare":
            r = re.fullmatch(r"A [a-z ]+ costs €([\d,]+\.\d\d) in Cork and £([\d,]+\.\d\d) in Belfast\. The rate is €1 = £[\d.]+\. Which is true\?", en)
            eu, pe = N(r[1]), half_up(N(r[2]) / R)
            def ok(o):
                if o == "They cost the same": return eu == pe
                m = re.fullmatch(r"(Belfast|Cork) is cheaper by €([\d,]+\.\d\d)", o); assert m, o
                place = "Belfast" if pe < eu else "Cork"
                return m[1] == place and N(m[2]) == abs(eu - pe)
            return choice(q, ok)
    bad(q, "unknown type " + str(t))

qs = json.load(open(sys.argv[1]))
for q in qs:
    try: check(q)
    except Exception as e: bad(q, "CRASH " + type(e).__name__ + " " + str(e)[:50])
print(len(qs), "questions;", dict(count))
if problems:
    for k, v in problems.most_common():
        print(f"  {v:5d}  {k}\n         e.g. {examples[k]}")
    sys.exit(1)
print("0 problems")
