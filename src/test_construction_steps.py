"""Check every Construction Steps question independently.
Diagrams: every finished construction is re-checked with GEOMETRY read from the SVG (arc centres and radii, crossing points,
lines, labels): e.g. the bisector really halves the angle, the perpendicular really is at 90° through the midpoint, the
triangle's sides and angles really match its labels and the task. "Which construction is this?" questions: Léim's own
validators for all 15 constructions are run on the drawing and EXACTLY ONE must pass, and it must be the answer.
"Next step" questions: the answer must match this file's own list of the steps (written separately from the game), no wrong
option may also be the right next step, and the picture must show exactly the steps done so far.
Numbers and facts are recomputed from the question text.
node src/test_construction_steps.js > /tmp/cs.json ; python3 src/test_construction_steps.py /tmp/cs.json"""
import json, sys, re, math
from collections import Counter
probs = []
def bad(q, msg): probs.append((q.get("mk"), msg, q.get("en", "")[:90], q.get("answer", "")[:70], [w[:40] for w in q.get("wrong", [])]))
def P(s): x, y = s.split(","); return (float(x), float(y))
def dist(a, b): return math.hypot(a[0] - b[0], a[1] - b[1])
def sub(a, b): return (a[0] - b[0], a[1] - b[1])
def dot(a, b): return a[0] * b[0] + a[1] * b[1]
def crs(a, b): return a[0] * b[1] - a[1] * b[0]
def angd(v, p): return math.degrees(math.atan2(p[1] - v[1], p[0] - v[0])) % 360
def angle_at(v, a, b):
    x = abs(angd(v, a) - angd(v, b)) % 360; return min(x, 360 - x)
def line_dist(p, a, b): return abs(crs(sub(b, a), sub(p, a))) / dist(a, b)
def seg_dist(p, a, b):
    ab = sub(b, a); t = max(0, min(1, dot(sub(p, a), ab) / dot(ab, ab))); c = (a[0] + t * ab[0], a[1] + t * ab[1]); return dist(p, c)
TOL = 0.9

class Fail(Exception): pass
def need(c, msg):
    if not c: raise Fail(msg)

def parse(svg):
    g = {"u": float(re.search(r'data-u="([\d.]+)"', svg).group(1)) if 'data-u="' in svg else 22.0}
    g["segs"] = [dict(s=int(s), a=P(a), b=P(b)) for s, a, b in re.findall(r'<line class="sg[^"]*" data-s="(\d+)"(?: pathLength="1")? data-a="([^"]+)" data-b="([^"]+)"', svg)]
    g["arcs"] = [dict(s=int(s), c=P(c), r=float(r), a1=float(a1), a2=float(a2)) for s, c, r, a1, a2 in
                 re.findall(r'<path class="arc[^"]*" data-s="(\d+)"(?: pathLength="1")? data-c="([^"]+)" data-r="([^"]+)" data-a1="([^"]+)" data-a2="([^"]+)"', svg)]
    g["pts"] = {}
    for s, p, n in re.findall(r'<g class="pn[^"]*" data-s="(\d+)" data-p="([^"]+)" data-n="([^"]+)"', svg):
        if n in g["pts"]: raise Fail("point named twice: " + n)
        g["pts"][n] = P(p)
    g["names_s"] = {n: int(s) for s, p, n in re.findall(r'<g class="pn[^"]*" data-s="(\d+)" data-p="([^"]+)" data-n="([^"]+)"', svg)}
    g["dots"] = [P(p) for s, p in re.findall(r'<circle class="dt[^"]*" data-s="(\d+)" data-p="([^"]+)"', svg)]
    g["marks"] = [dict(v=P(v), a1=float(a1), sw=float(sw), l=l) for s, v, a1, sw, l in re.findall(r'<g class="am[^"]*" data-s="(\d+)" data-v="([^"]+)" data-a1="([^"]+)" data-sw="([^"]+)" data-l="([^"]*)"', svg)]
    g["rts"] = [dict(v=P(v), a1=float(a1)) for s, v, a1 in re.findall(r'<path class="rt[^"]*" data-s="(\d+)" data-v="([^"]+)" data-a1="([^"]+)"', svg)]
    g["lens"] = [dict(a=P(a), b=P(b), t=t) for s, a, b, t in re.findall(r'<text class="len[^"]*" data-s="(\d+)" data-a="([^"]+)" data-b="([^"]+)"[^>]*>([^<]*)</text>', svg)]
    g["cws"] = [dict(a=P(a), b=P(b), t=t) for s, a, b, t in re.findall(r'<g class="cw[^"]*" data-s="(\d+)" data-a="([^"]+)" data-b="([^"]+)">.*?<text[^>]*>([^<]*)</text></g>', svg)]
    g["pros"] = [dict(c=P(c), r=float(r), a0=float(a0)) for s, c, r, a0 in re.findall(r'<g class="pro[^"]*" data-s="(\d+)" data-c="([^"]+)" data-r="([^"]+)" data-a0="([^"]+)"', svg)]
    g["steps"] = [int(x) for x in re.findall(r'data-s="(\d+)"', svg)]
    g["new"] = [int(x) for x in re.findall(r'class="[a-z]+ new[t]?" data-s="(\d+)"', svg)]
    return g

def pt(g, n):
    need(n in g["pts"], "no point " + n); return g["pts"][n]
def on_arc(p, a, tol=TOL):
    if abs(dist(p, a["c"]) - a["r"]) > tol: return False
    t = angd(a["c"], p); x = (t - a["a1"]) % 360; return x <= (a["a2"] - a["a1"]) + 0.3
def arc_through(g, c, p):  # a drawn arc centred at c that passes through p
    for a in g["arcs"]:
        if dist(a["c"], c) < TOL and on_arc(p, a): return a
    raise Fail(f"no arc centred {c} through {p}")
def on_seg(g, p):
    return any(seg_dist(p, s["a"], s["b"]) < TOL for s in g["segs"])
def seg_through(g, p, q):  # a drawn segment that contains both p and q
    for s in g["segs"]:
        if seg_dist(p, s["a"], s["b"]) < TOL and seg_dist(q, s["a"], s["b"]) < TOL: return s
    raise Fail(f"no line through {p} and {q}")
def has_rt(g, v, d1, d2):
    for r in g["rts"]:
        if dist(r["v"], v) < TOL:
            a = r["a1"]
            def cd(x, y): return min((x - y) % 360, (y - x) % 360)
            # the square's two sides must lie along the two lines (either way round)
            if (cd(a, d1) < 1 and cd(a + 90, d2) < 1) or (cd(a, d2) < 1 and cd(a + 90, d1) < 1) or (cd(a, d1) < 1 and cd(a - 90, d2) < 1) or (cd(a, d2) < 1 and cd(a - 90, d1) < 1): return True
    return False
def num_in(t):
    m = re.fullmatch(r"([\d.]+) cm", t.strip()); need(m, "bad length label " + t); return float(m.group(1))
def len_label(g, p, q):
    for l in g["lens"]:
        if (dist(l["a"], p) < TOL and dist(l["b"], q) < TOL) or (dist(l["a"], q) < TOL and dist(l["b"], p) < TOL): return num_in(l["t"])
    raise Fail("no length label")
def mark_at(g, v):
    for m in g["marks"]:
        if dist(m["v"], v) < TOL: return m
    raise Fail("no angle mark")
def mark_val(m):
    x = re.fullmatch(r"(\d+)°", m["l"]); need(x, "bad angle label"); return int(x.group(1))
def perp(u, w): return abs(dot(u, w)) / (math.hypot(*u) * math.hypot(*w)) < 0.003
def para(u, w): return abs(crs(u, w)) / (math.hypot(*u) * math.hypot(*w)) < 0.003

# ---------- the 15 validators (each raises Fail unless the drawing IS that construction, correctly done) ----------
def v1(g, q):
    B, A, C, D, E, F = (pt(g, n) for n in "BACDEF")
    need(len(g["pts"]) == 6, "extra points")
    seg_through(g, B, A); seg_through(g, B, C)
    aB = arc_through(g, B, D); need(on_arc(E, aB), "E not on the arc from B")
    need(seg_dist(D, B, A) < TOL and seg_dist(E, B, C) < TOL, "D, E not on the arms")
    a1, a2 = arc_through(g, D, F), arc_through(g, E, F); need(abs(a1["r"] - a2["r"]) < TOL, "different widths from D and E")
    s = seg_through(g, B, F)
    need(abs(angle_at(B, A, F) - angle_at(B, F, C)) < 0.2, "the line doesn't halve the angle")
    need(abs(angle_at(B, A, F) + angle_at(B, F, C) - angle_at(B, A, C)) < 0.2, "F not inside the angle")
def v2(g, q):
    A, B, C, D, M = (pt(g, n) for n in "ABCDM")
    need(len(g["pts"]) == 5 and "P" not in g["pts"], "extra points")
    seg_through(g, A, B)
    r = [arc_through(g, A, C)["r"], arc_through(g, A, D)["r"], arc_through(g, B, C)["r"], arc_through(g, B, D)["r"]]
    need(max(r) - min(r) < TOL and r[0] > dist(A, B) / 2, "arcs not equal or not more than half")
    need(g["cws"] and abs(dist(g["cws"][0]["a"], g["cws"][0]["b"]) - r[0]) < TOL, "compass width bar doesn't match the arcs")
    seg_through(g, C, D); need(perp(sub(D, C), sub(B, A)), "CD not perpendicular to AB")
    mid = ((A[0] + B[0]) / 2, (A[1] + B[1]) / 2); need(dist(M, mid) < TOL and line_dist(mid, C, D) < TOL, "not through the midpoint")
    need(has_rt(g, M, angd(M, B), angd(M, C)), "no right-angle mark at M")
def find_l(g):
    s = max(g["segs"], key=lambda s: dist(s["a"], s["b"])); need("l" in g["pts"], "no line l"); return s
def v3(g, q):
    l = find_l(g); Pp, A, B, Q = (pt(g, n) for n in "PABQ")
    need(line_dist(Pp, l["a"], l["b"]) > 20, "P is on l")
    for X in (A, B): need(seg_dist(X, l["a"], l["b"]) < TOL, "A/B not on l")
    aP = arc_through(g, Pp, A); need(on_arc(B, aP), "B not on the arc from P")
    need(abs(arc_through(g, A, Q)["r"] - arc_through(g, B, Q)["r"]) < TOL, "different widths from A and B")
    need(crs(sub(l["b"], l["a"]), sub(Pp, l["a"])) * crs(sub(l["b"], l["a"]), sub(Q, l["a"])) < 0, "Q on the same side as P")
    seg_through(g, Pp, Q); need(perp(sub(Q, Pp), sub(l["b"], l["a"])), "PQ not perpendicular to l")
def v4(g, q):
    l = find_l(g); Pp, A, B, Q = (pt(g, n) for n in "PABQ")
    need(seg_dist(Pp, l["a"], l["b"]) < TOL, "P not on l")
    for X in (A, B): need(seg_dist(X, l["a"], l["b"]) < TOL, "A/B not on l")
    need(abs(arc_through(g, Pp, A)["r"] - arc_through(g, Pp, B)["r"]) < TOL and dot(sub(A, Pp), sub(B, Pp)) < 0, "A, B not equal distances either side of P")
    r1, r2 = arc_through(g, A, Q)["r"], arc_through(g, B, Q)["r"]
    need(abs(r1 - r2) < TOL and r1 > dist(Pp, A) + 2, "second arcs not equal or not wider")
    seg_through(g, Pp, Q); need(perp(sub(Q, Pp), sub(l["b"], l["a"])), "PQ not perpendicular to l"); need(has_rt(g, Pp, angd(Pp, Q), angd(Pp, B)), "no right-angle mark")
def v5(g, q):
    l = find_l(g); Pp, Q, R, S, T, Uu = (pt(g, n) for n in "PQRSTU")
    need(seg_dist(Q, l["a"], l["b"]) < TOL and seg_dist(R, l["a"], l["b"]) < TOL, "Q/R not on l")
    tr = seg_through(g, Q, Pp); need(seg_dist(S, tr["a"], tr["b"]) < TOL and seg_dist(T, tr["a"], tr["b"]) < TOL, "S/T not on QP")
    a = arc_through(g, Q, R); need(on_arc(S, a), "S not on the arc from Q")
    b = arc_through(g, Pp, T); need(abs(a["r"] - b["r"]) < TOL and on_arc(Uu, b), "arc from P wrong width or U not on it")
    c = arc_through(g, T, Uu); need(abs(c["r"] - dist(R, S)) < TOL, "arc from T not |RS|")
    need(dot(sub(T, Pp), sub(S, Q)) > 0, "T on the wrong side of P")
    s = seg_through(g, Pp, Uu); need(para(sub(Uu, Pp), sub(l["b"], l["a"])), "PU not parallel to l")
def vdiv(g, q, k):
    A, B = pt(g, "A"), pt(g, "B"); subs = "₁₂₃₄₅₆₇"
    Cs = []; i = 0
    while "C" + subs[i] in g["pts"]: Cs.append(g["pts"]["C" + subs[i]]); i += 1
    n = len(Cs); need(n >= 2, "no marks")
    need((k == 6 and n <= 3) or (k == 7 and n >= 4), "wrong number of parts for this construction")
    ray = seg_through(g, A, Cs[-1]); need(angle_at(A, B, Cs[-1]) < 89, "ray not at an acute angle")
    prev = A
    for c in Cs: arc_through(g, prev, c); need(abs(dist(prev, c) - dist(A, Cs[0])) < TOL, "steps not equal"); prev = c
    seg_through(g, Cs[-1], B)
    for j, c in enumerate(Cs[:-1], 1):
        X = (A[0] + (B[0] - A[0]) * j / n, A[1] + (B[1] - A[1]) * j / n)
        s = seg_through(g, c, X); need(para(sub(s["b"], s["a"]), sub(B, Cs[-1])), "line not parallel to the last join")
        need(any(dist(d, X) < TOL for d in g["dots"]), "division point not marked")
    return n
def v6(g, q): vdiv(g, q, 6)
def v7(g, q): vdiv(g, q, 7)
def v8(g, q):
    A, B = pt(g, "A"), pt(g, "B"); need(len(g["pts"]) == 2, "extra points")
    ray = max(g["segs"], key=lambda s: dist(s["a"], s["b"])); need(dist(ray["a"], A) < TOL and seg_dist(B, ray["a"], ray["b"]) < TOL, "B not on the ray from A")
    arc_through(g, A, B); L = len_label(g, A, B); need(abs(dist(A, B) - L * g["u"]) < TOL, "|AB| doesn't match the label")
    need(g["cws"] and abs(num_in(g["cws"][0]["t"]) - L) < 1e-9 and abs(dist(g["cws"][0]["a"], g["cws"][0]["b"]) - L * g["u"]) < TOL, "compass setting wrong")
def v9(g, q):
    A, B = pt(g, "A"), pt(g, "B"); need(len(g["pts"]) == 2 and g["pros"], "not a protractor drawing")
    pr = g["pros"][0]; need(dist(pr["c"], A) < TOL and abs(pr["a0"] - angd(A, B)) < 0.5, "protractor not centred on A along AB")
    need(len(g["dots"]) == 1, "no dot"); d = g["dots"][0]; need(abs(dist(d, A) - pr["r"]) < TOL, "dot not on the scale")
    seg_through(g, A, d); m = mark_at(g, A); need(abs(angle_at(A, B, d) - mark_val(m)) < 0.3 and abs(m["sw"] - mark_val(m)) < 0.3, "angle doesn't match its label")
def tri(g): return pt(g, "A"), pt(g, "B"), pt(g, "C")
def v10(g, q):
    A, B, Cp = tri(g); need(not g["marks"] and not g["rts"], "angles marked")
    for X, Y in ((A, B), (A, Cp), (B, Cp)): seg_through(g, X, Y); need(abs(dist(X, Y) - len_label(g, X, Y) * g["u"]) < TOL, "side doesn't match its label")
    arc_through(g, A, Cp); arc_through(g, B, Cp)
def v11(g, q):
    A, B, Cp = tri(g); need(not g["rts"] and len(g["marks"]) == 1, "wrong marks")
    for X, Y in ((A, B), (A, Cp)): need(abs(dist(X, Y) - len_label(g, X, Y) * g["u"]) < TOL, "side doesn't match its label")
    seg_through(g, Cp, B); m = mark_at(g, A); need(abs(angle_at(A, B, Cp) - mark_val(m)) < 0.3, "∠A doesn't match"); arc_through(g, A, Cp)
def v12(g, q):
    A, B, Cp = tri(g); need(not g["rts"] and len(g["marks"]) == 2, "wrong marks")
    need(abs(dist(A, B) - len_label(g, A, B) * g["u"]) < TOL, "AB doesn't match"); seg_through(g, A, Cp); seg_through(g, B, Cp)
    need(abs(angle_at(A, B, Cp) - mark_val(mark_at(g, A))) < 0.3 and abs(angle_at(B, A, Cp) - mark_val(mark_at(g, B))) < 0.3, "angles don't match")
def v13(g, q):
    A, B, Cp = tri(g); need(not g["marks"] and has_rt(g, A, angd(A, B), angd(A, Cp)), "no right angle at A")
    need(abs(angle_at(A, B, Cp) - 90) < 0.2, "∠A not 90")
    need(abs(dist(A, B) - len_label(g, A, B) * g["u"]) < TOL and abs(dist(B, Cp) - len_label(g, B, Cp) * g["u"]) < TOL, "sides don't match")
    need(abs(arc_through(g, B, Cp)["r"] - dist(B, Cp)) < TOL, "no hypotenuse arc"); seg_through(g, B, Cp)
def v14(g, q):
    A, B, Cp = tri(g); need(len(g["marks"]) == 1 and has_rt(g, A, angd(A, B), angd(A, Cp)), "no right angle at A")
    need(abs(angle_at(A, B, Cp) - 90) < 0.2 and abs(angle_at(B, A, Cp) - mark_val(mark_at(g, B))) < 0.3, "angles don't match")
    need(abs(dist(A, B) - len_label(g, A, B) * g["u"]) < TOL, "AB doesn't match"); seg_through(g, B, Cp)
def v15(g, q):
    A, B, Cp, D = (pt(g, n) for n in "ABCD")
    need(abs(angle_at(A, B, D) - 90) < 0.2 and abs(angle_at(B, A, Cp) - 90) < 0.2, "not right angles at A and B")
    need(has_rt(g, A, angd(A, B), angd(A, D)) and has_rt(g, B, angd(B, A), angd(B, Cp)), "right-angle marks missing")
    w, h = len_label(g, A, B), len_label(g, B, Cp)
    need(abs(dist(A, B) - w * g["u"]) < TOL and abs(dist(A, D) - h * g["u"]) < TOL and abs(dist(B, Cp) - h * g["u"]) < TOL, "sides don't match")
    arc_through(g, A, D); arc_through(g, B, Cp); seg_through(g, D, Cp)
V = {1: v1, 2: v2, 3: v3, 4: v4, 5: v5, 6: v6, 7: v7, 8: v8, 9: v9, 10: v10, 11: v11, 12: v12, 13: v13, 14: v14, 15: v15}
MYNAMES = {1: "Bisector of an angle", 2: "Perpendicular bisector of a line segment", 3: "Perpendicular to a line, from a point not on it",
           4: "Perpendicular to a line, at a point on it", 5: "Line parallel to a line, through a point", 6: "Dividing a line segment into 2 or 3 equal parts",
           7: "Dividing a line segment into any number of equal parts", 8: "Line segment of a given length on a ray", 9: "Angle of a given size on a ray",
           10: "Triangle: three sides (SSS)", 11: "Triangle: two sides and the angle between them (SAS)", 12: "Triangle: two angles and the side between them (ASA)",
           13: "Right-angled triangle: the hypotenuse and one other side", 14: "Right-angled triangle: one side and one acute angle", 15: "Rectangle: given the side lengths"}
def which(g, q):
    ok = []
    for k, f in V.items():
        try: f(g, q); ok.append(k)
        except (Fail, KeyError, ZeroDivisionError, ValueError, IndexError, AttributeError): pass
    return ok
def why_fail(g, q, k):
    try: V[k](g, q); return None
    except Fail as e: return str(e)

# ---------- the steps, written separately from the game ----------
CANON = {1: [r"compass point on B.*arc.*both arms", r"on D, then on E.*same compass width", r"line from B through F"],
         2: [r"^Open the compass to more than half", r"point on A, and then on B.*above and below", r"line through C and D"],
         3: [r"compass point on P.*cuts l in two", r"on A, and then on B.*other side of l", r"line through P and Q"],
         4: [r"compass point on P.*each side of P", r"^Open the compass wider.*on A, and then on B", r"line through P and Q"],
         5: [r"^Draw a line through P that crosses l", r"compass point on Q.*crosses l at R", r"same compass width.*point on P", r"distance from R to S.*point on T", r"line through P and U.*parallel"],
         6: [r"^Draw a ray from A at an acute angle", r"step off (\d) equal marks", r"^Join the last mark", r"^Through each of the other marks.*parallel"],
         8: [r"^Open the compass to ([\d.]+) cm", r"compass point on A and draw an arc that crosses the ray", r"^Label the segment"],
         9: [r"centre of the protractor on A", r"starts at 0° on \[AB, and mark a dot at (\d+)°", r"ray from A through the dot"],
         10: [r"^Draw \[AB\], (\d+) cm", r"compass to (\d+) cm and draw an arc from A\. Then set it to (\d+) cm and draw an arc from B", r"^Join C to A and C to B"],
         11: [r"^Draw \[AB\], (\d+) cm", r"^At A, use a protractor to draw an angle of (\d+)°", r"compass to (\d+) cm\. Put the point on A", r"^Join C to B"],
         12: [r"^Draw \[AB\], (\d+) cm", r"protractor, draw an angle of (\d+)° at A and an angle of (\d+)° at B, on the same side", r"two new arms cross at C"],
         13: [r"^Draw \[AB\], (\d+) cm", r"^At A, construct a line perpendicular to \[AB\] \(a right angle\)", r"compass to (\d+) cm\. Put the point on B", r"^Join B to C"],
         14: [r"^Draw \[AB\], (\d+) cm", r"^At A, construct a line perpendicular to \[AB\]\. At B, use a protractor to draw an angle of (\d+)°", r"two new lines cross at C"],
         15: [r"^Draw \[AB\], (\d+) cm", r"perpendicular to \[AB\] at A, and another at B", r"compass to (\d+) cm\. From A and from B", r"^Join D to C"]}
CANON[7] = CANON[6]
def nums(t): return [float(x) for x in re.findall(r"(\d+(?:\.\d+)?)", t)]
def title_numbers(k, en):
    """What the task asks for, read from the question text."""
    if k == 10: m = re.search(r"\|AB\| = (\d+) cm, \|AC\| = (\d+) cm and \|BC\| = (\d+) cm", en); return dict(ab=int(m[1]), ac=int(m[2]), bc=int(m[3]))
    if k == 11: m = re.search(r"\|AB\| = (\d+) cm, ∠BAC = (\d+)° and \|AC\| = (\d+) cm", en); return dict(ab=int(m[1]), al=int(m[2]), ac=int(m[3]))
    if k == 12: m = re.search(r"\|AB\| = (\d+) cm, ∠CAB = (\d+)° and ∠ABC = (\d+)°", en); return dict(ab=int(m[1]), al=int(m[2]), be=int(m[3]))
    if k == 13: m = re.search(r"\|AB\| = (\d+) cm and the hypotenuse \|BC\| = (\d+) cm", en); return dict(s=int(m[1]), h=int(m[2]))
    if k == 14: m = re.search(r"\|AB\| = (\d+) cm and ∠ABC = (\d+)°", en); return dict(s=int(m[1]), be=int(m[2]))
    if k == 15: m = re.search(r"\|AB\| = (\d+) cm and \|BC\| = (\d+) cm", en); return dict(w=int(m[1]), h=int(m[2]))
    if k == 8: return dict(L=float(re.search(r"length ([\d.]+) cm", en)[1]))
    if k == 9: return dict(d=int(re.search(r"angle of (\d+)°", en)[1]))
    if k in (6, 7): return dict(n=int(re.search(r"into (\d+) equal parts", en)[1]))
    return {}
def task_matches_drawing(k, T, g):
    """The finished drawing must be the one the task asked for (numbers from the question text)."""
    u = g["u"]
    if k == 10:
        A, B, Cp = tri(g); need(abs(dist(A, B) - T["ab"] * u) < TOL and abs(dist(A, Cp) - T["ac"] * u) < TOL and abs(dist(B, Cp) - T["bc"] * u) < TOL, "sides ≠ task")
    if k == 11:
        A, B, Cp = tri(g); need(abs(dist(A, B) - T["ab"] * u) < TOL and abs(dist(A, Cp) - T["ac"] * u) < TOL and abs(angle_at(A, B, Cp) - T["al"]) < 0.3, "≠ task")
    if k == 12:
        A, B, Cp = tri(g); need(abs(dist(A, B) - T["ab"] * u) < TOL and abs(angle_at(A, B, Cp) - T["al"]) < 0.3 and abs(angle_at(B, A, Cp) - T["be"]) < 0.3, "≠ task")
    if k == 13:
        A, B, Cp = tri(g); need(abs(dist(A, B) - T["s"] * u) < TOL and abs(dist(B, Cp) - T["h"] * u) < TOL, "≠ task")
    if k == 14:
        A, B, Cp = tri(g); need(abs(dist(A, B) - T["s"] * u) < TOL and abs(angle_at(B, A, Cp) - T["be"]) < 0.3, "≠ task")
    if k == 15:
        A, B, Cp = tri(g); need(abs(dist(A, B) - T["w"] * u) < TOL and abs(dist(B, Cp) - T["h"] * u) < TOL, "≠ task")
    if k == 8: need(abs(dist(pt(g, "A"), pt(g, "B")) - T["L"] * u) < TOL, "≠ task")
    if k == 9: need(abs(angle_at(pt(g, "A"), pt(g, "B"), g["dots"][0]) - T["d"]) < 0.3, "≠ task")
    if k in (6, 7): need(vdiv(g, None, k) == T["n"], "≠ task")
def step_numbers_ok(k, j, ans, T):
    m = re.search(CANON[k][j], ans)
    if k == 10 and j == 0: return int(m[1]) == T["ab"]
    if k == 10 and j == 1: return int(m[1]) == T["ac"] and int(m[2]) == T["bc"]
    if k in (11, 12, 13, 14, 15) and j == 0: return int(m[1]) == (T.get("ab") or T.get("s") or T.get("w"))
    if k == 11 and j == 1: return int(m[1]) == T["al"]
    if k == 11 and j == 2: return int(m[1]) == T["ac"]
    if k == 12 and j == 1: return int(m[1]) == T["al"] and int(m[2]) == T["be"]
    if k == 13 and j == 2: return int(m[1]) == T["h"]
    if k == 14 and j == 1: return int(m[1]) == T["be"]
    if k == 15 and j == 2: return int(m[1]) == T["h"]
    if k == 8 and j == 0: return float(m[1]) == T["L"]
    if k == 9 and j == 1: return int(m[1]) == T["d"]
    if k in (6, 7) and j == 1: return int(m[1]) == T["n"]
    return True
def k_from_title(en):
    for pat, k in [(r"bisector of ∠ABC", 1), (r"perpendicular bisector of \[AB\]", 2), (r"perpendicular to l\. \(Higher", 3), (r"perpendicular to l\.$", 4),
                   (r"parallel to l", 5), (r"into [23] equal parts without measuring it\.$", 6), (r"into [4-9] equal parts without measuring it\. \(Higher", 7),
                   (r"segment \[AB\] of length", 8), (r"Construct an angle of", 9), (r"\|AC\| = \d+ cm and \|BC\|", 10), (r"∠BAC = \d+° and \|AC\|", 11),
                   (r"∠CAB = \d+° and ∠ABC", 12), (r"hypotenuse \|BC\|", 13), (r"right angle at A, \|AB\| = \d+ cm and ∠ABC", 14), (r"rectangle ABCD", 15)]:
        if re.search(pat, en): return k
    return None

def check_step(q):
    k = k_from_title(q["en"]); need(k, "can't tell the construction from the task")
    T = title_numbers(k, q["en"]); steps = CANON[k]
    hits = [j for j, pat in enumerate(steps) if re.search(pat, q["answer"])]
    need(len(hits) == 1, f"answer matches steps {hits}"); j = hits[0]
    need(step_numbers_ok(k, j, q["answer"], T), "numbers in the step don't match the task")
    for w in q["wrong"]:
        if re.search(steps[j], w) and step_numbers_ok(k, j, w, T): raise Fail("a wrong option is also the right next step: " + w)
    # the picture: exactly steps 1..j done, the newest in red
    if q["html"]:
        g = parse(q["html"]); need(max(g["steps"]) == j, f"picture shows {max(g['steps'])} steps, expected {j}")
        need(all(s == j for s in g["new"]) and (bool(g["new"]) == (j > 0)), "wrong elements shown as new")
    else: need(j == 0, "no picture after some steps")
    want = "What's the first step?" if j == 0 else "next step"
    need(want in q["frame"], "frame wording")
    # the finished construction (from the same random build) must be correct and match the task
    gf = parse(q["data"]["full"]); w = which(gf, q); need(w == [k], f"finished drawing validates as {w}, task is {k}: " + str(why_fail(gf, q, k)))
    task_matches_drawing(k, T, gf)

def check_name(q):
    g = parse(q["html"]); w = which(g, q)
    need(len(w) == 1, f"drawing validates as {w}" + (": " + str(why_fail(g, q, q['data']['k'])) if not w else ""))
    need(q["answer"] == MYNAMES[w[0]], "answer isn't the construction drawn")
    for x in q["wrong"]: need(x in MYNAMES.values() and x != q["answer"], "odd wrong option")
    if w[0] in (6, 7): need(MYNAMES[13 - w[0]] not in q["wrong"], "6/7 both offered")

DESC_KEYS = [(r"angle exactly in half", {1}), (r"segment in half, at right angles", {2}), (r"P is not on l", {3}), (r"P that is on l", {4}),
             (r"never meets", {5}), (r"into 3 equal parts", {6, 7}), (r"into 7 equal parts", {7}), (r"exactly 6 cm long", {8}), (r"angle of 40°", {9}),
             (r"all three sides", {10}), (r"two sides and the angle between", {11}), (r"two angles and the side between", {12}),
             (r"hypotenuse and one other side", {13}), (r"one side and an acute angle", {14}), (r"rectangle", {15})]
def check_desc(q):
    hits = [s for pat, s in DESC_KEYS if re.search(pat, q["frame"])]; need(len(hits) == 1, "description not recognised")
    good = {MYNAMES[k] for k in hits[0]}; need(q["answer"] in good, "wrong construction for the description")
    for w in q["wrong"]: need(w not in good and w in MYNAMES.values(), "a wrong option also fits")

TOOL_KEY = [(r"bisector of an angle \(construction 1\)", "compass and a straight edge only"), (r"perpendicular bisector of a line segment \(construction 2\)", "compass and a straight edge only"),
            (r"construction arcs", "leave them showing"), (r"how wide must the compass", "more than half"), (r"Higher level course only", "3 and 7"),
            (r"two sides of a triangle and the angle between", "^SAS$"), (r"all three sides of a triangle", "^SSS$"), (r"two angles of a triangle and the side between", "^ASA$"),
            (r"right angle, the hypotenuse", "^RHS$"), (r"Every point on the perpendicular bisector", "same distance from a as from b"),
            (r"What does the bisector of an angle do", "two equal angles"), (r"same compass width\?", "same distance from d and e"), (r"which scale do you read", "starts at 0°"),
            (r'What does "bisect" mean', "two equal parts"), (r"meets \[AB\] at what angle", "^90°$"), (r"SAS triangle construction, which angle", "between the two given sides"),
            (r"5 equal parts without measuring, what do you do first", "ray from a"), (r"lines through the marks must be", "parallel to the line from the last mark to b"),
            (r"In construction 4", "wider"), (r"What is the hypotenuse", "opposite the right angle")]
def check_tool(q):
    hits = [a for pat, a in TOOL_KEY if re.search(pat, q["en"])]; need(len(hits) == 1, "tool question not recognised")
    need(re.search(hits[0], q["answer"].lower() if not hits[0].startswith("^") else q["answer"]), "wrong answer")
    for w in q["wrong"]: need(not re.search(hits[0], w.lower() if not hits[0].startswith("^") else w), "a wrong option also fits")

def val(s, unit):
    m = re.fullmatch(r"(\d+(?:\.\d+)?)" + (r"°" if unit == "°" else r" cm"), s); need(m, "bad option " + s); return float(m[1])
def check_number(q, t, en):
    ex = None; unit = "cm"
    if t == "bisect": ex, unit = int(re.search(r"angle of (\d+)°", en)[1]) / 2, "°"
    elif t == "bisectback": ex, unit = 2 * int(re.search(r"angle of (\d+)° with the arm", en)[1]), "°"
    elif t == "half": ex = float(re.search(r"\|AB\| = ([\d.]+) cm", en)[1]) / 2
    elif t == "equi": ex = float(re.search(r"\|CA\| = ([\d.]+) cm", en)[1])
    elif t == "parts": m = re.search(r"segment of ([\d.]+) cm into (\d+) equal parts", en); ex = float(m[1]) / int(m[2])
    elif t == "third3": m = re.search(r"∠CAB = (\d+)° and ∠ABC = (\d+)°", en); ex, unit = 180 - int(m[1]) - int(m[2]), "°"
    elif t == "scale": ex, unit = 180 - int(re.search(r"wants an angle of (\d+)° but reads the wrong scale", en)[1]), "°"
    elif t == "hyp": ex = int(re.search(r"hypotenuse of (\d+) cm", en)[1])
    elif t == "rect": m = re.search(r"\|AB\| = (\d+) cm and \|BC\| = (\d+) cm\. What is its perimeter", en); ex = 2 * (int(m[1]) + int(m[2]))
    elif t == "perp": ex, unit = 90, "°"
    if ex is not None:
        need(abs(val(q["answer"], unit) - ex) < 1e-9, f"answer {q['answer']} but should be {ex}")
        for w in q["wrong"]: need(abs(val(w, unit) - ex) > 1e-9 and val(w, unit) > 0, "wrong option equals the answer")
        return
    if t == "marks":
        n = int(re.search(r"into (\d+) equal parts", en)[1]); need(q["answer"] == str(n), "marks")
    elif t == "width":
        L = int(re.search(r"\|AB\| = (\d+) cm", en)[1]); opts = [q["answer"]] + q["wrong"]
        good = [o for o in opts if val(o, "cm") > L / 2]; need(good == [q["answer"]], "exactly one width must work")
    elif t == "can":
        s = sorted(int(x) for x in re.findall(r"(\d+) cm", en)); ok = s[0] + s[1] > s[2]
        need(q["answer"] == ("Yes" if ok else "No"), "triangle inequality")
    elif t == "third":
        a, b = (int(x) for x in re.search(r"are (\d+) cm and (\d+) cm", en).groups())
        def fits(x): return abs(a - b) < x < a + b
        need(not fits(val(q["answer"], "cm")), "answer could be the third side")
        for w in q["wrong"]: need(fits(val(w, "cm")), "a wrong option can't be the third side either")
    else: raise Fail("unknown number type " + t)

def check(q):
    texts = [q["en"], q["frame"], q["answer"], q["why"], q["review"]] + q["wrong"]
    for t in texts:
        if re.search(r"undefined|NaN|null|\[object", t): raise Fail("bad text: " + t)
    need(len(q["wrong"]) == 3 and len(set(q["wrong"])) == 3 and q["answer"] not in q["wrong"], "options")
    t = q["data"].get("t")
    if t == "step": check_step(q)
    elif t == "name": check_name(q)
    elif t == "desc": check_desc(q)
    elif t == "tool": check_tool(q)
    else: check_number(q, t, q["en"])

if __name__ == "__main__":
    qs = json.load(open(sys.argv[1])); kinds = Counter()
    for q in qs:
        kinds[(q["data"].get("t"), q["data"].get("k"))] += 1
        try: check(q)
        except Fail as e: bad(q, str(e))
        except Exception as e: bad(q, "CRASH " + type(e).__name__ + " " + str(e))
    print(len(qs), "questions checked;", len(probs), "problems")
    for p in Counter((p[0], p[1]) for p in probs).most_common(25): print(p)
    for p in probs[:6]: print(p)
    print("coverage:", sorted((k for k in kinds if k[0] in ("step", "name")), key=str))
    sys.exit(1 if probs else 0)
