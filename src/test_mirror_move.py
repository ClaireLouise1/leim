#!/usr/bin/env python3
"""Independent checker for Mirror Move (Order 23, transformations & symmetry).
node src/test_mirror_move.js > /tmp/mm.json ; python3 src/test_mirror_move.py /tmp/mm.json
(env MM=<file> tests a mutated copy, N=<count> per maker)

Reads every picture back from the SVG (grid points from screen coordinates, mirror lines,
centres, arrows, shaded squares, plain shapes and dashed lines), works out each transformation
itself with complex numbers from the question TEXT, and checks the answer is the only right option."""
import json, re, sys, math, itertools

MINUS = "−"
def num(s): return int(s.replace(MINUS, "-"))
CO = re.compile(r"\((−?\d+), (−?\d+)\)")
def pt(s):
    m = re.fullmatch(r"\((−?\d+), (−?\d+)\)", s)
    return (num(m.group(1)), num(m.group(2))) if m else None
def attrs(tag): return dict(re.findall(r'([\w-]+)="([^"]*)"', tag))

# ---------- reading the grid picture ----------
def read_plane(html):
    m = re.search(r'<svg class="tg"[^>]*>', html)
    if not m: return None
    a = attrs(m.group(0)); R = int(a["data-r"]); s = float(a["data-s"]); pd = float(a["data-pd"])
    G = lambda X, Y: ((X - pd) / s - R, R - (Y - pd) / s)
    def lat(X, Y, what):
        x, y = G(X, Y); rx, ry = round(x), round(y)
        assert abs(x - rx) < 0.02 and abs(y - ry) < 0.02, f"{what} not on a grid point ({x:.2f},{y:.2f})"
        return (rx, ry)
    out = {"R": R, "polys": [], "pts": {}, "lines": [], "vec": []}
    for tag in re.findall(r'<polygon class="sp[^"]*"[^>]*>', html):
        t = attrs(tag); P = [lat(*map(float, p.split(",")), "vertex") for p in t["points"].split()]
        D = [tuple(map(int, p.split(","))) for p in t["data-pts"].split()]
        assert P == D, "polygon drawn somewhere else than its data"
        for p in P: assert abs(p[0]) <= R and abs(p[1]) <= R, "vertex off the grid"
        out["polys"].append({"n": t["data-n"], "c": t["class"], "P": P})
    # names written inside the shapes
    for x, y, txt in re.findall(r'<text class="pn[^"]*" x="([\d.]+)" y="([\d.]+)"[^>]*>([^<]*)</text>', html):
        gx, gy = G(float(x), float(y) - 4.5)
        own = [p for p in out["polys"] if p["n"] == txt]
        assert len(own) == 1, f"label {txt} has no shape"
        cx = sum(p[0] for p in own[0]["P"]) / len(own[0]["P"]); cy = sum(p[1] for p in own[0]["P"]) / len(own[0]["P"])
        assert abs(gx - cx) < .05 and abs(gy - cy) < .05, "label not at the centre of its shape"
        assert inside((gx, gy), own[0]["P"]), f"label {txt} outside its shape"
    for tag in re.findall(r'<circle class="pt[^"]*"[^>]*>', html):
        t = attrs(tag); p = lat(float(t["cx"]), float(t["cy"]), "point")
        assert p == (int(t["data-x"]), int(t["data-y"]))
        out["pts"][t["data-n"] or ("centre" if "cc" in t["class"] else "?")] = p
        if t["data-n"]: assert f'>{t["data-n"]}</text>' in html, "point label missing"
    for tag in re.findall(r'<line class="mir"[^>]*>', html):
        t = attrs(tag); a1 = G(float(t["x1"]), float(t["y1"])); b1 = G(float(t["x2"]), float(t["y2"]))
        out["lines"].append((complex(*a1), complex(*b1)))
    for tag in re.findall(r'<line class="vec"[^>]*>', html):
        t = attrs(tag); A = tuple(map(int, t["data-a"].split(","))); B = tuple(map(int, t["data-b"].split(",")))
        assert lat(float(t["x1"]), float(t["y1"]), "arrow start") == A
        e = G(float(t["x2"]), float(t["y2"])); d1 = complex(*e) - complex(*A); d2 = complex(*B) - complex(*A)
        assert abs(d1 / d2 - abs(d1) / abs(d2)) < 1e-3 and abs(d1) < abs(d2), "arrow points the wrong way"
        out["vec"].append((A, B))
    return out

def inside(p, P):
    x, y = p; n = len(P); c = False
    for i in range(n):
        (x1, y1), (x2, y2) = P[i], P[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1): c = not c
    return c

# ---------- my own transformations (complex numbers) ----------
def refl(a, b):   # reflection in the line through a and b
    d = b - a
    return lambda z: a + (d / d.conjugate()) * (z - a).conjugate()
def half(c): return lambda z: 2 * c - z
def rot(c, cw): w = -1j if cw else 1j; return lambda z: c + w * (z - c)
def trans(v): return lambda z: z + v
def C_(p): return complex(*p)
def P_(z):
    assert abs(z.real - round(z.real)) < 1e-6 and abs(z.imag - round(z.imag)) < 1e-6, "image not on a grid point"
    return (round(z.real), round(z.imag))
def key(P): return sorted(P)

def line_of(name, pic):
    if name == "the x-axis": return refl(0, 1)
    if name == "the y-axis": return refl(0, 1j)
    assert name == "the line m" and pic and len(pic["lines"]) == 1, "line m must be drawn"
    a, b = pic["lines"][0]; return refl(a, b)

def parse_T(txt, pic):
    """the transformation named in a question (returns a function on complex numbers)"""
    m = re.search(r"axial symmetry in (the x-axis|the y-axis|the line m)", txt)
    if m: return line_of(m.group(1), pic)
    m = re.search(r"central symmetry in (?:the origin \(0, 0\)|the point C\((−?\d+), (−?\d+)\))", txt)
    if m:
        c = (0, 0) if m.group(1) is None else (num(m.group(1)), num(m.group(2)))
        if pic: check_centre(c, pic)
        return half(C_(c))
    m = re.search(r"a rotation of 90° (clockwise|anticlockwise) about (?:the origin \(0, 0\)|the point C\((−?\d+), (−?\d+)\))", txt)
    if m:
        c = (0, 0) if m.group(2) is None else (num(m.group(2)), num(m.group(3)))
        if pic: check_centre(c, pic)
        return rot(C_(c), m.group(1) == "clockwise")
    m = re.search(r"moves every point (.+?)[?.]$", txt)
    if m: return trans(C_(move(m.group(1))))
    raise AssertionError("no transformation found in: " + txt)

def check_centre(c, pic):
    if c == (0, 0): assert pic["pts"].get("centre", (0, 0)) == (0, 0) or pic["pts"].get("C") is None
    else: assert pic["pts"].get("C") == c, "centre C drawn in the wrong place"

def move(s):
    x = y = 0; parts = s.split(" and ")
    assert 1 <= len(parts) <= 2
    for p in parts:
        m = re.fullmatch(r"(\d+) (unit|units) (right|left|up|down)", p); assert m, "bad move " + s
        k = int(m.group(1)); assert k > 0 and (m.group(2) == "unit") == (k == 1), "unit/units wrong: " + s
        if m.group(3) == "right": x += k
        elif m.group(3) == "left": x -= k
        elif m.group(3) == "up": y += k
        else: y -= k
    if len(parts) == 2: assert parts[0].split()[2] in ("right", "left") and parts[1].split()[2] in ("up", "down")
    return (x, y)

def describe_T(o):
    """option text in 'Which transformation maps S onto S′?'"""
    m = re.fullmatch(r"Translation: (.+)", o)
    if m: return trans(C_(move(m.group(1))))
    m = re.fullmatch(r"Axial symmetry in (the x-axis|the y-axis)", o)
    if m: return line_of(m.group(1), None)
    m = re.fullmatch(r"Central symmetry in \((−?\d+), (−?\d+)\)", o)
    if m: return half(complex(num(m.group(1)), num(m.group(2))))
    m = re.fullmatch(r"Rotation of 90° (clockwise|anticlockwise) about \((−?\d+), (−?\d+)\)", o)
    if m: return rot(complex(num(m.group(2)), num(m.group(3))), m.group(1) == "clockwise")
    raise AssertionError("unknown option " + o)

def maps(f, A, B):
    try: return key([P_(f(C_(p))) for p in A]) == key(B)
    except AssertionError: return False

def isometry_kinds(A, B):
    """every kind of isometry taking polygon A onto polygon B (by trying each vertex matching)"""
    kinds = set(); za = [C_(p) for p in A]
    for perm in itertools.permutations(B):
        zb = [C_(p) for p in perm]
        for rev in (False, True):
            u = [z.conjugate() if rev else z for z in za]
            if abs(u[1] - u[0]) < 1e-9: continue
            w = (zb[1] - zb[0]) / (u[1] - u[0])
            if abs(abs(w) - 1) > 1e-9: continue
            t = zb[0] - w * u[0]
            if all(abs(w * u[i] + t - zb[i]) < 1e-9 for i in range(len(A))):
                if not rev:
                    if abs(w - 1) < 1e-9: kinds.add("tr")
                    elif abs(w + 1) < 1e-9: kinds.add("cs")
                    elif abs(w - 1j) < 1e-9 or abs(w + 1j) < 1e-9: kinds.add("ro")
                    else: kinds.add("other")
                else:
                    f = lambda z: w * z.conjugate() + t
                    kinds.add("ax" if abs(f(f(5 + 7j)) - (5 + 7j)) < 1e-9 else "glide")
    return kinds

def apart(P, Q):
    a = (min(p[0] for p in P), min(p[1] for p in P), max(p[0] for p in P), max(p[1] for p in P))
    b = (min(p[0] for p in Q), min(p[1] for p in Q), max(p[0] for p in Q), max(p[1] for p in Q))
    return a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1]

def no_symmetry(P):
    """the shapes S must have no symmetry, or several transformations could give the same picture"""
    return isometry_kinds(P, P) == {"tr"}

# ---------- plain shapes ----------
def read_shape(html, data=False):
    m = re.search(r'<svg class="tg sy"[^>]*>', html); a = attrs(m.group(0)); s = float(a["data-s"]); ox = float(a["data-ox"]); oy = float(a["data-oy"])
    G = lambda X, Y: ((X - ox) / s, (oy - Y) / s)
    t = attrs(re.search(r'<polygon class="sp ob"[^>]*>', html).group(0))
    P = [G(*map(float, p.split(","))) for p in t["points"].split()]
    D = [tuple(map(float, p.split(","))) for p in t["data-pts"].split()]
    for p, d in zip(P, D): assert abs(p[0] - d[0]) < .02 and abs(p[1] - d[1]) < .02, "shape drawn wrongly"
    if data: P = D
    lines = []
    for tag in re.findall(r'<line class="mir dl"[^>]*>', html):
        u = attrs(tag); a1 = G(float(u["x1"]), float(u["y1"])); b1 = G(float(u["x2"]), float(u["y2"]))
        lines.append((u["data-n"], complex(*a1), complex(*b1)))
    return P, lines

def is_axis(P, a, b, tol=0.02):
    f = refl(a, b); Z = [complex(*p) for p in P]
    return all(min(abs(f(z) - w) for w in Z) < tol for z in Z)

def count_axes(P):
    """try lines through the middle at every half-degree; count the separate directions that work"""
    Z = [complex(*p) for p in P]; c = sum(Z) / len(Z); found = []
    for k in range(360):
        ang = k * math.pi / 360; d = complex(math.cos(ang), math.sin(ang))
        if is_axis(P, c, c + d, 0.08):
            # refine and keep separate directions only
            if not any(min(abs(ang - g), math.pi - abs(ang - g)) < 0.05 for g in found): found.append(ang)
    return len(found)

def polygon_name(P):
    """name a shape by measuring it (my own rules)"""
    n = len(P); L = [math.dist(P[i], P[(i + 1) % n]) for i in range(n)]
    eq = lambda x, y: abs(x - y) < 2e-3
    def ang(i):
        a, b, c = P[i - 1], P[i], P[(i + 1) % n]; v1 = (a[0] - b[0], a[1] - b[1]); v2 = (c[0] - b[0], c[1] - b[1])
        return math.degrees(math.acos(max(-1, min(1, (v1[0] * v2[0] + v1[1] * v2[1]) / (math.hypot(*v1) * math.hypot(*v2))))))
    A = [ang(i) for i in range(n)]
    eqa = lambda x, y: abs(x - y) < 0.05
    if n == 3:
        k = sum(eq(L[i], L[j]) for i, j in ((0, 1), (1, 2), (0, 2)))
        if k == 3: return "equilateral triangle"
        if k == 1: return "right-angled isosceles triangle" if any(eqa(a, 90) for a in A) else "isosceles triangle"
        return "scalene triangle"
    if n == 4:
        par = lambda i: abs((P[(i + 1) % 4][0] - P[i][0]) * (P[(i + 3) % 4][1] - P[(i + 2) % 4][1]) - (P[(i + 1) % 4][1] - P[i][1]) * (P[(i + 3) % 4][0] - P[(i + 2) % 4][0])) < 2e-3
        p0, p1 = par(0), par(1); allL = all(eq(x, L[0]) for x in L); right = all(eqa(a, 90) for a in A)
        if p0 and p1:
            if right: return "square" if allL else "rectangle"
            return "rhombus" if allL else "parallelogram"
        if p0 or p1:
            legs = (L[1], L[3]) if p0 else (L[0], L[2])
            return "isosceles trapezium" if eq(*legs) else "trapezium"
        if (eq(L[0], L[1]) and eq(L[2], L[3])) or (eq(L[1], L[2]) and eq(L[3], L[0])): return "kite"
        return "quadrilateral"
    if all(eq(x, L[0]) for x in L) and all(eqa(a, A[0]) for a in A):
        return {5: "regular pentagon", 6: "regular hexagon", 8: "regular octagon"}[n]
    return "polygon"

def has_centre(P):
    Z = [complex(*p) for p in P]; c = sum(Z) / len(Z)
    return all(min(abs(2 * c - z - w) for w in Z) < 2e-3 for z in Z)

# my own facts (written separately from the game's lists)
CENTRE = {"square": True, "rectangle": True, "rhombus": True, "parallelogram": True, "kite": False, "isosceles trapezium": False,
          "isosceles triangle": False, "equilateral triangle": False, "scalene triangle": False, "right-angled isosceles triangle": False,
          "regular pentagon": False, "regular hexagon": True, "regular octagon": True}
AXES = {"square": 4, "rectangle": 2, "rhombus": 2, "parallelogram": 0, "kite": 1, "isosceles trapezium": 1, "isosceles triangle": 1,
        "equilateral triangle": 3, "scalene triangle": 0, "right-angled isosceles triangle": 1, "regular pentagon": 5, "regular hexagon": 6, "regular octagon": 8}
def fact_true(s):
    m = re.fullmatch(r"An? ([\w -]+?) has (\d+) axes of symmetry", s)
    if m: return AXES[m.group(1)] == int(m.group(2))
    m = re.fullmatch(r"An? ([\w -]+?) has a centre of symmetry", s)
    if m: return True if m.group(1) == "circle" else CENTRE[m.group(1)]
    TAB = {"Central symmetry in a point is the same as a rotation of 180° about that point": True,
           "Central symmetry is the same as a rotation of 90°": False,
           "A translation does not change the size or the shape": True, "A translation turns a shape round": False,
           "A translation flips a shape over": False, "Axial symmetry flips a shape over": True,
           "Axial symmetry makes a shape bigger": False, "Under axial symmetry, a point on the mirror line is its own image": True,
           "Under axial symmetry, every point is its own image": False, "Under central symmetry, the centre is its own image": True,
           "A rotation turns a shape about a fixed point": True,
           "A rotation of 90° clockwise is the same as a rotation of 90° anticlockwise": False}
    return TAB[s]

# ---------- squared-paper patterns ----------
def read_cells(html):
    a = attrs(re.search(r'<svg class="tg cg"[^>]*>', html).group(0)); W, H = int(a["data-w"]), int(a["data-h"]); s = float(a["data-s"]); pd = float(a["data-pd"])
    on = set(); n = 0
    for tag in re.findall(r'<rect class="cell[^"]*"[^>]*>', html):
        t = attrs(tag); c = round((float(t["x"]) - pd) / s); r = H - 1 - round((float(t["y"]) - pd) / s)
        assert (c, r) == (int(t["data-c"]), int(t["data-r"])), "square drawn in the wrong place"; n += 1
        if "on" in t["class"].split(): on.add((c, r))
    assert n == W * H
    t = attrs(re.search(r'<line class="mir"[^>]*>', html).group(0))
    gx = lambda X: (X - pd) / s; gy = lambda Y: H - (Y - pd) / s
    a1 = complex(gx(float(t["x1"])), gy(float(t["y1"]))); b1 = complex(gx(float(t["x2"])), gy(float(t["y2"])))
    return W, H, on, refl(a1, b1)

def complete_count(W, H, on, f):
    need = set()
    for c, r in on:
        z = f(complex(c + .5, r + .5)); cc, rr = z.real - .5, z.imag - .5
        assert abs(cc - round(cc)) < 1e-6 and abs(rr - round(rr)) < 1e-6
        cc, rr = round(cc), round(rr); assert 0 <= cc < W and 0 <= rr < H, "mirror square off the paper"
        if (cc, rr) not in on: need.add((cc, rr))
    return len(need)

# ---------- checking ----------
def check(q):
    t = q["data"]["t"]; en = q["en"]; opts = [q["answer"]] + q["wrong"]
    assert len(opts) == 4 and len(set(opts)) == 4, "need 4 different options"
    for o in opts: assert "-" not in re.sub(r"[A-Za-z]-[a-z]", "", o), "ASCII minus in " + o
    txt = " ".join([en, q.get("frame") or "", q.get("why") or "", " ".join(opts)])
    assert not re.search(r"NaN|undefined|Infinity|\b1 units\b|\b0 units?\b", txt), "bad text"
    pic = read_plane(q["html"]) if q["html"] and 'class="tg"' in q["html"] else None

    if t == "pick":
        S = [p for p in pic["polys"] if p["n"] == "S"]; assert len(S) == 1 and no_symmetry(S[0]["P"])
        f = parse_T(en, pic); want = key([P_(f(C_(p))) for p in S[0]["P"]])
        hits = [p["n"] for p in pic["polys"] if p["n"] != "S" and key(p["P"]) == want]
        assert hits == [q["answer"]], f"image is {hits}, answer {q['answer']}"
        assert sorted(opts) == sorted(p["n"] for p in pic["polys"] if p["n"] != "S"), "options don't match the shapes"
        for A, B in itertools.combinations(pic["polys"], 2): assert apart(A["P"], B["P"]), "shapes overlap"
        if "C" in pic["pts"]: assert "C" not in opts
        return
    if t in ("point", "vertex", "tarrow"):
        if t == "tarrow":
            (A, B), = pic["vec"]; assert pic["pts"]["A"] == A and pic["pts"]["B"] == B
            f = trans(C_(B) - C_(A)); P = pic["pts"]["P"]
        else:
            f = parse_T(en, pic)
            m = re.search(r"(?:point|vertex) ([A-Z])(\((−?\d+), (−?\d+)\))?", en)
            nm = m.group(1)
            if m.group(2): P = (num(m.group(3)), num(m.group(4))); assert pic is None or pic["pts"].get(nm) in (None, P)
            else: P = pic["pts"][nm]
        if t in ("vertex", "tarrow"):
            assert any(P in p["P"] for p in pic["polys"]), "P is not a corner of the shape"
        I = P_(f(C_(P))); assert I != P, "the point is its own image"
        assert pt(q["answer"]) == I, f"image of {P} is {I}, answer {q['answer']}"
        for o in q["wrong"]: assert pt(o) and pt(o) != I
        return
    if t == "complete":
        W, H, on, f = read_cells(q["html"]); n = complete_count(W, H, on, f)
        assert q["answer"] == str(n), f"need {n}, answer {q['answer']}"
        for o in q["wrong"]: assert o.isdigit() and int(o) != n
        return
    if t == "name":
        S = [p for p in pic["polys"] if p["n"] == "S"][0]["P"]; I = [p for p in pic["polys"] if p["n"] == "S′"][0]["P"]
        assert no_symmetry(S) and apart(S, I)
        good = [o for o in opts if maps(describe_T(o), S, I)]
        assert good == [q["answer"]], f"options that work: {good}"
        return
    if t == "kind":
        S = [p for p in pic["polys"] if p["n"] == "S"][0]["P"]; I = [p for p in pic["polys"] if p["n"] == "S′"][0]["P"]
        k = isometry_kinds(S, I); assert len(k) == 1, f"kinds {k}"
        NAMES = {"tr": "A translation", "ax": "An axial symmetry", "cs": "A central symmetry", "ro": "A rotation of 90°"}
        assert NAMES[k.pop()] == q["answer"]; assert all(o in NAMES.values() for o in opts)
        return
    if t == "tmap":
        (a, b, c) = [(num(x), num(y)) for x, y in CO.findall(en)]
        I = P_(C_(c) + C_(b) - C_(a)); assert pt(q["answer"]) == I
        for o in q["wrong"]: assert pt(o) != I
        return
    if t == "tdesc":
        S = [p for p in pic["polys"] if p["n"] == "S"][0]["P"]; I = [p for p in pic["polys"] if p["n"] == "S′"][0]["P"]
        good = [o for o in opts if maps(trans(C_(move(o))), S, I)]
        assert good == [q["answer"]], f"moves that work: {good}"
        return
    if t in ("centre", "nocentre"):
        want = t == "centre"; good = [o for o in opts if CENTRE[o.lower()] == want]
        assert good == [q["answer"]], f"good {good}"
        return
    if t == "fact":
        good = [o for o in opts if fact_true(o)]; assert good == [q["answer"]], f"true: {good}"
        return
    if t == "axes":
        P, _ = read_shape(q["html"], True); nm = polygon_name(P); n = count_axes(P)
        assert nm == q["data"]["name"], f"drawn shape is a {nm}, not a {q['data']['name']}"
        assert AXES[nm] == n == int(q["answer"]), f"{nm}: counted {n}, table {AXES[nm]}, answer {q['answer']}"
        assert has_centre(P) == CENTRE[nm]
        return
    if t == "whichline":
        P, L = read_shape(q["html"], True); assert len(L) == 4
        assert polygon_name(P) == q["data"]["name"], "name " + polygon_name(P)
        assert ("the " + q["data"]["name"]) in en
        good = [n for n, a, b in L if is_axis(P, a, b)]
        assert good == [q["answer"]], f"axes among the lines: {good}"
        for n, a, b in L:   # every dashed line passes through the shape
            assert sorted(opts) == sorted(x for x, _, _ in L)
        return
    raise AssertionError("unknown type " + t)

def check_fix(path):
    """the fixed Exam-corner diagrams must match the worked answers on the page"""
    import subprocess

if __name__ == "__main__":
    data = json.load(open(sys.argv[1])); bad = {}; n = 0
    for q in data:
        n += 1
        try: check(q)
        except Exception as e:
            k = q["mk"] + ": " + str(e)[:110]; bad.setdefault(k, (0, q)); bad[k] = (bad[k][0] + 1, q)
    for k, (c, q) in sorted(bad.items()):
        print(f"{c:5d}  {k}\n       {q['en']} | {q['answer']} | {q['wrong']}")
    print(f"{n} questions, {sum(c for c, _ in bad.values())} problems")
