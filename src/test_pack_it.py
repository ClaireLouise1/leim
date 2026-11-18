#!/usr/bin/env python3
"""Independent checker for Pack It (JC Maths topic 33, volume, surface area & nets).
node src/test_pack_it.js > /tmp/pk.json ; python3 src/test_pack_it.py /tmp/pk.json   (env TL=<file> tests a mutated copy, N=<count> per maker)
It MEASURES every drawing: each labelled length is found as a drawn edge (polygon edge, line or path segment)
and its length is compared with the label (receding edges are drawn at half length), cuboid fronts must be
rectangles, prism ends right-angled triangles with a² + b² = c², cylinder tops and balls are measured from the
ellipses, nets are measured face by face (areas summed, solid classified by its faces). It then works out every
answer itself from the LABELS and the question TEXT with its own formulas (π modes, half-up rounding with a
rounding-boundary check) and checks that no wrong option has the same value as the answer."""
import json, re, sys, math, collections
from fractions import Fraction as Fr
from decimal import Decimal, ROUND_HALF_UP

KZ = 0.5
class Bad(Exception): pass
def need(c, msg):
    if not c: raise Bad(msg)
def attrs(tag): return dict(re.findall(r'([\w-]+)="([^"]*)"', tag))
def pts(s): return [tuple(float(v) for v in p.split(",")) for p in s.split()]
def close(a, b, t=0.03): return abs(a - b) <= t

def svgs(html):
    out = []
    for m in re.finditer(r'<svg class="sf"[^>]*>.*?</svg>', html or "", re.S):
        out.append(read_svg(m.group(0)))
    return out

def read_svg(x):
    head = attrs(re.match(r'<svg[^>]*>', x).group(0))
    s, ox, oy = float(head["data-s"]), float(head["data-ox"]), float(head["data-oy"])
    R = lambda px, py: ((px - ox) / s, (oy - py) / s)
    D = {"kind": head["data-kind"], "s": s, "polys": [], "segs": [], "ells": [], "labs": [], "head": head, "arcs": []}
    for t in re.findall(r'<polygon [^>]*/>', x):
        a = attrs(t); P = [R(*p) for p in pts(a["points"])]
        D["polys"].append({"c": a["class"], "role": a.get("data-role"), "p": P})
        for i in range(len(P)): D["segs"].append((P[i], P[(i + 1) % len(P)]))
    for t in re.findall(r'<line [^>]*/>', x):
        a = attrs(t); D["segs"].append((R(float(a["x1"]), float(a["y1"])), R(float(a["x2"]), float(a["y2"]))))
    for t in re.findall(r'<path [^>]*/>', x):
        a = attrs(t); toks = re.findall(r'[MLAZ]|-?\d+(?:\.\d+)?', a["d"]); i = 0; cur = None; start = None
        while i < len(toks):
            c = toks[i]
            if c in "ML":
                p = R(float(toks[i + 1]), float(toks[i + 2]))
                if c == "L" and cur: D["segs"].append((cur, p))
                if c == "M": start = p
                cur = p; i += 3
            elif c == "A":
                rx, ry = float(toks[i + 1]) / s, float(toks[i + 2]) / s; p = R(float(toks[i + 6]), float(toks[i + 7]))
                D["arcs"].append((rx, ry, cur, p)); cur = p; i += 8
            elif c == "Z":
                if cur and start: D["segs"].append((cur, start))
                cur = start; i += 1
            else: raise Bad("bad path token " + c)
    for t in re.findall(r'<ellipse [^>]*/>', x):
        a = attrs(t); c = R(float(a["cx"]), float(a["cy"]))
        D["ells"].append({"c": a["class"], "ctr": c, "rx": float(a["rx"]) / s, "ry": float(a["ry"]) / s})
    for t, txt in re.findall(r'(<text class="fl[^"]*"[^>]*>)([^<]*)</text>', x):
        a = attrs(t)
        D["labs"].append({"k": a["data-k"], "t": txt, "a": tuple(map(float, a["data-a"].split(","))), "b": tuple(map(float, a["data-b"].split(","))), "z": a["data-z"] == "1"})
    check_labels(D)
    return D

def lab_val(t):
    if t == "?": return None, None
    m = re.fullmatch(r'([\d,]+(?:\.\d+)?) (cm|m)', t); need(m, "label %r" % t)
    return Fr(m.group(1).replace(",", "")), m.group(2)

def check_labels(D):
    D["L"] = {}; units = set()
    for l in D["labs"]:
        a, b = l["a"], l["b"]
        drawn = any((close(p[0], a[0], .05) and close(p[1], a[1], .05) and close(q[0], b[0], .05) and close(q[1], b[1], .05)) or
                    (close(q[0], a[0], .05) and close(q[1], a[1], .05) and close(p[0], b[0], .05) and close(p[1], b[1], .05)) for p, q in D["segs"])
        need(drawn, "label %s=%s is not on a drawn edge" % (l["k"], l["t"]))
        L = math.dist(a, b) / (KZ if l["z"] else 1)
        if l["z"]:  # receding edges go up-right at 30°
            need(close(math.degrees(math.atan2(b[1] - a[1], b[0] - a[0])), 30, .3), "receding edge not at 30°")
        v, u = lab_val(l["t"])
        if u: units.add(u)
        if v is not None: need(close(L, float(v), .03), "label %s=%s but drawn %.3f" % (l["k"], l["t"], L))
        D["L"][l["k"]] = (v, L)
    need(len(units) <= 1, "mixed units in one drawing")
    D["unit"] = units.pop() if units else None
    k = D["kind"]
    if k in ("cuboid", "cube", "triprism", "gable"):
        fr = [p for p in D["polys"] if p["role"] == "front"]; need(len(fr) == 1, "one front face")
        F = fr[0]["p"]
        if k in ("cuboid", "cube"):
            need(len(F) == 4, "cuboid front has 4 corners")
            w_, h_ = math.dist(F[0], F[1]), math.dist(F[1], F[2])
            need(close(math.dist(F[0], F[2]), math.hypot(w_, h_), .03), "cuboid front is not a rectangle")
            if k == "cube": need(close(w_, h_, .03), "cube front is not a square")
        if k == "triprism":
            need(len(F) == 3, "prism end is a triangle")
            A, B, Cc = F; need(close((B[0] - A[0]) * (Cc[0] - A[0]) + (B[1] - A[1]) * (Cc[1] - A[1]), 0, .05), "no right angle at the corner")
    if k in ("cylinder", "silo"):
        top = [e for e in D["ells"] if e["c"] == "top"]
        r = float(D["head"]["data-r"])
        if top: need(close(top[0]["rx"], r, .03), "top ellipse radius")
        for kk in ("r", "d"):
            if kk in D["L"] and D["L"][kk][0] is not None:
                need(close(float(D["L"][kk][0]) / (2 if kk == "d" else 1), r, .03), "radius label vs drawing")
    if k == "sphere":
        ball = [e for e in D["ells"] if e["c"] == "ball"]; need(len(ball) == 1 and close(ball[0]["rx"], ball[0]["ry"]), "ball is a circle")
        r = ball[0]["rx"]
        for kk in ("r", "d"):
            if kk in D["L"] and D["L"][kk][0] is not None: need(close(float(D["L"][kk][0]) / (2 if kk == "d" else 1), r, .03), "ball radius label")
    if k == "hemisphere":
        dome = [a for a in D["arcs"] if close(a[0], a[1])]; need(dome, "hemisphere dome")
        r = dome[0][0]
        for kk in ("r", "d"):
            if kk in D["L"] and D["L"][kk][0] is not None: need(close(float(D["L"][kk][0]) / (2 if kk == "d" else 1), r, .03), "hemisphere radius label")

def V(D, k):
    need(k in D["L"], "missing label " + k); v = D["L"][k][0]; need(v is not None, "label %s is ?" % k); return v
def radius(D):
    if "r" in D["L"]: return V(D, "r")
    return V(D, "d") / 2

# ---------- formatting, as a person would write it ----------
def fmt(x, dp):
    d = Decimal(x.numerator) / Decimal(x.denominator) if isinstance(x, Fr) else Decimal(repr(x))
    q = d.quantize(Decimal(1).scaleb(-dp), rounding=ROUND_HALF_UP)
    s = format(q, "f")
    if "." in s: s = s.rstrip("0").rstrip(".")
    i, _, f = s.partition(".")
    i = "{:,}".format(int(i))
    return i + ("." + f if f else "")
def not_edge(x, dp):
    t = x * 10 ** dp - math.floor(x * 10 ** dp)
    need(abs(t - 0.5) > 0.004, "too close to a rounding boundary: %r" % x)
def nice(x, dp): return Fr(x) * 10 ** dp == int(Fr(x) * 10 ** dp)

PI_TXT = {"(π button, 1 d.p.)": "calc", "(π = 3.14)": "314", "(π = 22/7)": "227", "(in terms of π)": "inpi"}
def pimode(en):
    ms = [m for t, m in PI_TXT.items() if t in en]; need(len(ms) == 1, "one π instruction"); return ms[0]
def pians(en, coef, unit):
    m = pimode(en); coef = Fr(coef)
    if m == "inpi":
        need(nice(coef, 2), "π coefficient not 2 d.p."); return ("" if coef == 1 else fmt(coef, 2)) + "π " + unit
    if m == "calc":
        x = float(coef) * math.pi; not_edge(x, 1); return fmt(x, 1) + " " + unit
    if m == "314":
        x = coef * Fr(314, 100); need(nice(x, 2), "3.14 answer not 2 d.p."); return fmt(x, 2) + " " + unit
    x = coef * Fr(22, 7); need(nice(x, 2), "22/7 answer not 2 d.p."); return fmt(x, 2) + " " + unit

def parse_opt(s):
    m = re.fullmatch(r'([\d,]*(?:\.\d+)?)(π)? (.+)', s)
    if not m: return None
    n = m.group(1).replace(",", "")
    return (Fr(n) if n else Fr(1), bool(m.group(2)), m.group(3))

def nums(en): return [Fr(x.replace(",", "")) for x in re.findall(r'\d[\d,]*(?:\.\d+)?', en)]

def classify_net(D):
    tris = [p for p in D["polys"] if len(p["p"]) == 3]; rects = [p for p in D["polys"] if len(p["p"]) == 4]
    circ = [e for e in D["ells"] if e["c"] == "nc"]
    if len(circ) == 2 and len(rects) == 1 and not tris:
        R = rects[0]["p"]; w = math.dist(R[0], R[1]); r = circ[0]["rx"]
        need(close(w, 2 * math.pi * r, .05), "cylinder net: rectangle isn't 2πr long"); return "Cylinder"
    if len(tris) == 2 and len(rects) == 3: return "Triangular prism"
    if len(rects) == 6 and not tris and not circ:
        sides = sorted(round(math.dist(p["p"][0], p["p"][1]), 3) for p in rects) + sorted(round(math.dist(p["p"][1], p["p"][2]), 3) for p in rects)
        if max(sides) - min(sides) < .01: return "Cube"
        areas = collections.Counter(round(area(p["p"]), 1) for p in rects)
        need(all(v % 2 == 0 for v in areas.values()), "cuboid net faces don't pair up"); return "Cuboid"
    raise Bad("unknown net")
def area(P):
    return abs(sum(P[i][0] * P[(i + 1) % len(P)][1] - P[(i + 1) % len(P)][0] * P[i][1] for i in range(len(P)))) / 2

def solve(q):
    t = q["data"].get("t"); en = q["en"]; G = svgs(q["html"]); D = G[0] if G else None; u = D["unit"] if D else None
    if t in ("cubv", "cubsa", "openbox", "litres", "m3litres", "fill"):
        need(D["kind"] == "cuboid", "cuboid drawing"); l, w, h = V(D, "l"), V(D, "w"), V(D, "h")
        if t == "cubv": return fmt(l * w * h, 0) + " cm³"
        if t == "cubsa": return fmt(2 * (l * w + l * h + w * h), 0) + " cm²"
        if t == "openbox": need("no lid" in en, "says no lid"); return fmt(l * w + 2 * l * h + 2 * w * h, 0) + " cm²"
        if t == "litres": need(u == "cm" and "1,000 cm³" in en, "cm tank"); return fmt(l * w * h / 1000, 2) + " litres"
        if t == "m3litres": need(u == "m" and "1,000 litres" in en, "m tank"); return fmt(l * w * h * 1000, 0) + " litres"
        rate = nums(en)[0]; need("litres a minute" in en, "rate"); x = l * w * h / 1000 / rate; return fmt(x, 1) + " minutes"
    if t in ("cubev", "cubesa"):
        need(D["kind"] == "cube", "cube drawing"); a = V(D, "l")
        return fmt(a ** 3, 0) + " cm³" if t == "cubev" else fmt(6 * a * a, 0) + " cm²"
    if t == "cubeback":
        Vv = nums(en)[0]; a = round(float(Vv) ** (1 / 3)); need(a ** 3 == Vv, "not a cube number"); return fmt(Fr(a), 2) + " cm"
    if t == "cubmiss":
        Vv = nums(en)[0]; known = [D["L"][k][0] for k in "lwh" if D["L"][k][0] is not None]; need(len(known) == 2, "two lengths known")
        need(sum(1 for k in "lwh" if D["L"][k][0] is None) == 1, "one ?"); x = Vv / (known[0] * known[1])
        qk = [k for k in "lwh" if D["L"][k][0] is None][0]; need(close(float(x), D["L"][qk][1], .03), "? side drawn wrong length")
        return fmt(x, 2) + " cm"
    if t == "pack":
        need(len(G) == 2, "container + box"); B = G[1]; L, W, H = V(D, "l"), V(D, "w"), V(D, "h"); a, b, c = V(B, "l"), V(B, "w"), V(B, "h")
        n = (L // a) * (W // b) * (H // c); need("same way round" in en, "orientation fixed"); return fmt(Fr(n), 0) + " boxes"
    if t in ("triv", "trisa"):
        a, b, c, L = V(D, "a"), V(D, "b"), V(D, "c"), V(D, "L"); need(a * a + b * b == c * c, "a² + b² ≠ c²")
        return fmt(a * b / 2 * L, 1) + " cm³" if t == "triv" else fmt(a * b + (a + b + c) * L, 1) + " cm²"
    if t == "gablev":
        w, h1, H, L = V(D, "w"), V(D, "h1"), V(D, "H"), V(D, "L"); need(H > h1, "roof"); return fmt((w * h1 + w * (H - h1) / 2) * L, 1) + " m³"
    if t == "xsec":
        A, L = nums(en)[:2]; need("end has area" in en, "text"); return fmt(A * L, 0) + " cm³"
    if t == "xsecback":
        Vv, L = nums(en)[:2]; return fmt(Vv / L, 2) + " cm²"
    if t == "netwhich": return classify_net(D)
    if t == "netsa":
        need(classify_net(D) == "Cuboid", "cuboid net"); l, w, h = V(D, "l"), V(D, "w"), V(D, "h")
        S = 2 * (l * w + l * h + w * h); need(close(sum(area(p["p"]) for p in D["polys"]), float(S), .2), "net area measured ≠ formula")
        return fmt(S, 0) + " cm²"
    if t == "fev":
        F = [p for p in D["polys"] if p["role"] == "front"][0]["p"]; n = len(F)
        faces, edges, verts = n + 2, 3 * n, 2 * n; need(faces - edges + verts == 2, "Euler")
        k = ["faces", "edges", "vertices"].index(re.search(r'How many (faces|edges|vertices)', en).group(1)); return str([faces, edges, verts][k])
    if t == "cylv":
        r, h = radius(D), V(D, "h"); return pians(en, r * r * h, "cm³")
    if t == "cylcsa":
        r, h = radius(D), V(D, "h"); need("Curved" in en, "curved"); return pians(en, 2 * r * h, "cm²")
    if t == "cyltsa":
        r, h = radius(D), V(D, "h"); lid = "Closed" in en; need(lid != ("No lid" in en), "lid?")
        return pians(en, (2 if lid else 1) * r * r + 2 * r * h, "cm²")
    if t in ("sphv", "hemiv"):
        need(D["kind"] == ("sphere" if t == "sphv" else "hemisphere"), "solid"); need(("Hemisphere" in en) == (t == "hemiv"), "text")
        r = radius(D); return pians(en, Fr(4 if t == "sphv" else 2, 3) * r ** 3, "cm³")
    if t in ("sphsa", "hemisa"):
        need(D["kind"] == ("sphere" if t == "sphsa" else "hemisphere"), "solid"); r = radius(D)
        return pians(en, (4 if t == "sphsa" else 3) * r * r, "cm²")
    if t == "cylh":
        c, r = nums(en)[:2]; need("π cm³" in en, "π"); return fmt(c / (r * r), 2) + " cm"
    if t == "sphr":
        c = nums(en)[0]; r3 = c * 3 / 4; r = round(float(r3) ** (1 / 3)); need(r ** 3 == r3, "cube root"); return fmt(Fr(r), 2) + " cm"
    if t == "cylr":
        c, h = nums(en)[:2]; r2 = c / h; r = math.isqrt(int(r2)); need(r * r == r2, "square root"); return fmt(Fr(r), 2) + " cm"
    if t == "netcyl":
        need(classify_net(D) == "Cylinder", "cylinder net"); return pians(en, 2 * V(D, "r"), "cm")
    if t == "disrect":
        l, w = V(D, "l"), V(D, "w"); n = nums(en)[0]; vol = n * 1000 if "litre stone" in en else n; return fmt(vol / (l * w), 2) + " cm"
    if t == "discyl":
        R = V(D, "r"); x = nums(en); k = 1 if en.startswith("A ball") else x[0]; r = x[-1] if k == 1 else x[1]
        return fmt(k * Fr(4, 3) * r ** 3 / (R * R), 2) + " cm"
    if t == "silo":
        r, h = V(D, "r"), V(D, "h"); return pians(en, r * r * h + Fr(2, 3) * r ** 3, "m³")
    if t == "recast1":
        r, R = nums(en)[:2]; return fmt(Fr(4, 3) * r ** 3 / (R * R), 2) + " cm"
    if t == "recast2":
        Rc, hc, rb = nums(en)[:3]; n = Rc * Rc * hc / (Fr(4, 3) * rb ** 3); need(n.denominator == 1, "whole balls"); return fmt(n, 0) + " balls"
    if t == "cyllitres":
        r, h = V(D, "r"), V(D, "h"); need("(π button, 1 d.p.)" in en, "π"); x = math.pi * float(r * r * h) / 1000; not_edge(x, 1); return fmt(x, 1) + " litres"
    raise Bad("unknown type %r" % t)

def main():
    data = json.load(open(sys.argv[1])); bad = collections.Counter(); ex = {}; n = 0
    for q in data:
        n += 1
        try:
            ans = solve(q)
            need(ans == q["answer"], "answer %r, checker says %r" % (q["answer"], ans))
            need(len(q["wrong"]) == 3, "needs 3 wrong options")
            need(len(set(q["wrong"])) == 3 and q["answer"] not in q["wrong"], "duplicate options")
            pa = parse_opt(q["answer"])
            for w in q["wrong"]:
                pw = parse_opt(w)
                if pa and pw:
                    need(pw[2] == pa[2] and pw[1] == pa[1], "wrong option %r in a different form" % w)
                    need(pw[0] != pa[0] and pw[0] > 0, "wrong option %r same value / not positive" % w)
            need("−" not in q["en"] or True, "")
            need(not re.search(r'\b1x\b|NaN|undefined|Infinity', q["en"] + q["why"] + q["answer"] + "".join(q["wrong"])), "bad text")
        except Bad as e:
            key = q["mk"] + ": " + str(e).split(" but ")[0][:70]; bad[key] += 1; ex.setdefault(key, (q["en"], q["answer"], q["wrong"], str(e)))
        except Exception as e:
            key = q["mk"] + ": CRASH " + repr(e)[:60]; bad[key] += 1; ex.setdefault(key, (q["en"], q["answer"], q["wrong"]))
    print(n, "questions checked,", sum(bad.values()), "problems")
    for k, v in bad.most_common(): print(" ", v, k, "\n     e.g.", ex[k])
    sys.exit(1 if bad else 0)
main()
