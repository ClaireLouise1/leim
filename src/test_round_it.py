"""Recompute every Round It answer with Python's Decimal (independent of the game code)."""
import json, sys, re
from decimal import Decimal as D, ROUND_HALF_UP as H, ROUND_FLOOR
from fractions import Fraction as F
qs = json.load(open(sys.argv[1])); probs = 0
def val(s): return D(re.sub(r"[€ ]", "", s))
def rdp(x, d): return x.quantize(D(1).scaleb(-d), H) if d >= 0 else (x / D(10) ** -d).quantize(D(1), H) * D(10) ** -d
def sig(x, s): e = x.adjusted(); return rdp(x, s - 1 - e)
def calc(expr):
    a, op, b = re.fullmatch(r"([\d.]+) ([+−×÷]) ([\d.]+)", expr).groups(); a, b = D(a), D(b)
    return {"+": a + b, "−": a - b, "×": a * b, "÷": a / b}[op]
def est(expr):
    a, op, b = re.fullmatch(r"([\d.]+) ([×÷]) ([\d.]+)", expr).groups(); a, b = sig(D(a), 1), sig(D(b), 1)
    return a * b if op == "×" else a / b
seen = {}
for q in qs:
    d = q["data"]; t = d.get("t"); a = q["answer"]; ok = True; msg = ""
    try:
        if len(q["wrong"]) != 3 or len(set(q["wrong"] + [a])) != 4: ok, msg = False, "options"
        if any(w in ("", "undefined") or "NaN" in w or "undefined" in w for w in q["wrong"] + [a]) or "undefined" in q["en"] + q["why"] + q["review"]: ok, msg = False, "undefined"
        if t in ("dp", "place", "sf", "line", "op", "money", "est", "estw", "early"):
            if t == "dp": exp = rdp(D(d["x"]), d["d"]); assert q["frame"] == d["x"]
            elif t == "place": exp = rdp(D(d["x"]), -d["p"])
            elif t == "sf": exp = sig(D(d["x"]), d["s"])
            elif t == "line":
                # read the arrow from the SVG, not from data
                m = re.search(r'data-a="([\d.]+)" data-k="(\d)" data-j="(\d)"', q["html"]); A, k, j = D(m[1]), int(m[2]), int(m[3])
                x = A + D(j) * D(10) ** -(k + 1); exp = rdp(x, k)
                assert f"{x}" not in ("",)
            elif t == "op": exp = calc(q["frame"])
            elif t == "money": exp = D(d["T"]) - d["q"] * D(d["p1"]) - D(d["p2"]); assert a.startswith("€") and len(a.split(".")[1]) == 2
            elif t == "est": exp = est(q["frame"])
            elif t == "estw": exp = sig(D(d["p"]), 1) * sig(D(d["x"]), 1)
            elif t == "early": exp = rdp(calc(q["frame"]), 1)
            if val(a) != exp: ok, msg = False, f"answer {a} expected {exp}"
            if t in ("dp", "sf", "place", "early", "line"):
                # the answer string must show exactly the asked precision
                if t == "dp" and len(a.split(".")[1] if "." in a else "") != d["d"]: ok, msg = False, "dp shown"
                if t == "sf" and val(a) != sig(val(a), d["s"]): ok, msg = False, "sf shown"
            for w in q["wrong"]:
                if val(w) == val(a): ok, msg = False, f"wrong {w} equals answer"
            if t == "op" and "÷" not in q["frame"]:
                pass
        elif t == "digit":
            x = d["x"]; pos = x.split(".")[1].index(str(d["dg"])) + 1; exp = D(d["dg"]) * D(10) ** -pos
            if val(a) != exp: ok, msg = False, f"digit {a} vs {exp}"
            if any(val(w) == exp for w in q["wrong"]): ok, msg = False, "digit wrong equal"
        elif t == "order":
            vs = sorted(d["list"], key=D); exp = vs[-1] if d["big"] else vs[0]
            if a != exp or len(set(map(D, d["list"]))) != 4: ok, msg = False, f"order {a} vs {exp}"
        elif t in ("fd", "df"):
            f = F(d["f"]); assert F(D(d["dec"])) == f and f.denominator == F(d["f"]).denominator
            if t == "fd":
                if val(a) != D(d["dec"]) or any(val(w) == D(d["dec"]) for w in q["wrong"]): ok, msg = False, "fd"
            else:
                if F(a) != F(D(d["dec"])) or any(F(w) == F(D(d["dec"])) for w in q["wrong"]): ok, msg = False, "df"
        else: ok, msg = False, "no check for " + str(t)
    except Exception as e:
        ok, msg = False, "error " + repr(e)
    seen[q["mk"]] = seen.get(q["mk"], 0) + 1
    if not ok:
        probs += 1
        if probs < 30: print(q["mk"], msg, q["en"], q["frame"], a, q["wrong"])
print(len(qs), "questions,", probs, "problems; makers:", seen)
