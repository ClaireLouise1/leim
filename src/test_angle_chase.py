"""Check every Angle Chase question independently.
Diagrams: every angle mark is MEASURED from the SVG coordinates (labels must match the drawing), every mark must sit on
drawn lines, and x is found by Léim's own angle-fact solver, which reads the facts straight off the picture
(lines through a point, triangles, equal-side dashes, parallel arrows) — not from the game's own data.
"Which fact" questions: exactly one option is a fact that gives x in ONE step from the given angles.
Word questions are re-classified with separate rules.
node src/test_angle_chase.js > /tmp/ac.json ; python3 src/test_angle_chase.py /tmp/ac.json"""
import json, sys, re, math
from collections import Counter
probs = []; DEBUG = False
def bad(q, msg): probs.append((q["mk"], msg, q["en"], q["frame"][:80], q["answer"], q["wrong"]))
def P(s): x, y = s.split(","); return (float(x), -float(y))          # back to y-up
def sub(a, b): return (a[0] - b[0], a[1] - b[1])
def norm(a): l = math.hypot(*a); return (a[0] / l, a[1] / l)
def dot(a, b): return a[0] * b[0] + a[1] * b[1]
def crs(a, b): return a[0] * b[1] - a[1] * b[0]
def angd(v, p): return math.degrees(math.atan2(p[1] - v[1], p[0] - v[0])) % 360
def same(a, b, t=0.8): return math.hypot(a[0] - b[0], a[1] - b[1]) < t
def para(u, w): return dot(u, w) > 0.9995
def seg_dist(p, a, b):
    ab = sub(b, a); t = max(0, min(1, dot(sub(p, a), ab) / dot(ab, ab))); c = (a[0] + t * ab[0], a[1] + t * ab[1]); return math.hypot(p[0] - c[0], p[1] - c[1])
def line_dist(p, a, b): return abs(crs(sub(b, a), sub(p, a))) / math.hypot(*sub(b, a))

def parse(svg):
    lines = [(P(a + "," + b), P(c + "," + d), int(g or 0)) for g, a, b, c, d in
             re.findall(r'<line class="ln"(?: data-g="(\d)")? x1="([-\d.]+)" y1="([-\d.]+)" x2="([-\d.]+)" y2="([-\d.]+)"', svg)]
    ticks = [(P(a), P(b), int(n)) for a, b, n in re.findall(r'class="tick" data-a="([^"]+)" data-b="([^"]+)" data-n="(\d)"', svg)]
    tris = [[P(s) for s in pts.split()] for pts in re.findall(r'class="tri" data-pts="([^"]+)"', svg)]
    marks = [dict(v=P(v), p=P(p), q=P(q), r=int(r), l=l) for v, p, q, r, l in
             re.findall(r'class="am" data-v="([^"]+)" data-p="([^"]+)" data-q="([^"]+)" data-r="(\d)" data-l="([^"]*)"', svg)]
    return lines, ticks, tris, marks

def on_line(lines, v, d):  # a drawn line passes through v and carries on from v in direction d
    for a, b, g in lines:
        if seg_dist(v, a, b) < 0.7 and abs(crs(norm(sub(b, a)), d)) < 0.01:
            if max(dot(sub(a, v), d), dot(sub(b, v), d)) > 8: return (a, b, g)
    return None

def solve(q, lines, ticks, tris, marks):
    """Returns (value of x or None, set of fact kinds that give x in one step, values dict)."""
    n = len(marks); var = {}; known = {}
    for i, m in enumerate(marks):
        m["sw"] = (angd(m["v"], m["q"]) - angd(m["v"], m["p"])) % 360
        m["dp"], m["dq"] = norm(sub(m["p"], m["v"])), norm(sub(m["q"], m["v"]))
        if (m["sw"] > 180) != bool(m["r"]): bad(q, "reflex flag wrong")
        for d in (m["dp"], m["dq"]):
            if not on_line(lines, m["v"], d): bad(q, "angle mark not on a drawn line")
        if re.fullmatch(r"\d+", m["l"]):
            known[i] = int(m["l"])
            if abs(m["sw"] - known[i]) > 0.6: bad(q, f"label {m['l']} but the drawing measures {m['sw']:.2f}")
        elif m["l"] == "rt":
            known[i] = 90
            if abs(m["sw"] - 90) > 0.6: bad(q, "right-angle mark not 90")
    rels = []  # (kind, type, ids, const)
    # angles at one point: vertically opposite, chains along a straight line, all the way round
    for i in range(n):
        for j in range(n):
            if i < j and same(marks[i]["v"], marks[j]["v"]) and para(marks[i]["dp"], tuple(-c for c in marks[j]["dp"])) and para(marks[i]["dq"], tuple(-c for c in marks[j]["dq"])):
                rels.append(("vo", "eq", (i, j), 0))
    def chains(i, path, tot):
        m = marks[path[-1]]
        if abs(tot - 180) < 0.6: rels.append(("str", "sum", tuple(sorted(path)), 180))
        if abs(tot - 360) < 0.6: rels.append(("pt", "sum", tuple(sorted(path)), 360)); return
        if tot > 360: return
        for k in range(n):
            if k not in path and same(marks[k]["v"], m["v"]) and para(marks[k]["dp"], m["dq"]): chains(i, path + [k], tot + marks[k]["sw"])
    for i in range(n): chains(i, [i], marks[i]["sw"])
    # triangles: interior angles (a drawn mark, or a hidden unknown), exterior angles, equal sides
    for ti, T in enumerate(tris):
        inner = []
        for k in range(3):
            v, a, b = T[k], T[(k + 1) % 3], T[(k + 2) % 3]
            da, db = norm(sub(a, v)), norm(sub(b, v)); hit = None
            for i, m in enumerate(marks):
                if same(m["v"], v) and ((para(m["dp"], da) and para(m["dq"], db)) or (para(m["dp"], db) and para(m["dq"], da))): hit = i
            inner.append(hit if hit is not None else ("hidden", ti, k))
        rels.append(("tri", "sum", tuple(inner), 180))
        for k in range(3):
            v = T[k]
            for j, o in ((1, 2), (2, 1)):
                toj, away = norm(sub(T[(k + j) % 3], v)), norm(sub(v, T[(k + o) % 3]))
                for i, m in enumerate(marks):
                    if same(m["v"], v) and ((para(m["dp"], toj) and para(m["dq"], away)) or (para(m["dp"], away) and para(m["dq"], toj))):
                        rels.append(("ext", "ext", (i, inner[(k + 1) % 3], inner[(k + 2) % 3]), 0))
                        rels.append(("str", "sum", tuple(sorted([i, inner[k]], key=str)), 180))
        sides = {}
        for k in range(3):
            a, b = T[k], T[(k + 1) % 3]
            for ta, tb, tn in ticks:
                if (same(ta, a) and same(tb, b)) or (same(ta, b) and same(tb, a)): sides[k] = tn
        for k in range(3):   # side k joins T[k], T[k+1]; the angle opposite it is at T[k+2]
            for k2 in range(k + 1, 3):
                if k in sides and k2 in sides and sides[k] == sides[k2]:
                    rels.append(("iso" if len(sides) < 3 else "equi", "eq", (inner[(k + 2) % 3], inner[(k2 + 2) % 3]), 0))
    # parallel lines and a transversal
    groups = {}
    for a, b, g in lines:
        if g: groups.setdefault(g, []).append((a, b))
    for g, ls in groups.items():
        for a, b in ls:
            if not para(norm(sub(b, a)), norm(sub(ls[0][1], ls[0][0]))) and not para(norm(sub(b, a)), norm(sub(ls[0][0], ls[0][1]))): bad(q, "arrowed lines not parallel")
    for i in range(n):
        for j in range(n):
            if i >= j or same(marks[i]["v"], marks[j]["v"]): continue
            v1, v2 = marks[i]["v"], marks[j]["v"]; u = norm(sub(v2, v1))
            if not any(a_ and seg_dist(v1, *l[:2]) < 0.7 and seg_dist(v2, *l[:2]) < 0.7 and not l[2] for l in lines for a_ in [1]): continue
            def split(m, w):
                rays = [m["dp"], m["dq"]]; t = [r for r in rays if abs(crs(r, w)) < 0.01]; o = [r for r in rays if abs(crs(r, w)) >= 0.01]
                if len(t) != 1 or len(o) != 1: return None
                l = on_line(lines, m["v"], o[0])
                return (t[0], o[0], l) if l and l[2] else None
            s1, s2 = split(marks[i], u), split(marks[j], u)
            if not s1 or not s2 or s1[2] == s2[2] or s1[2][2] != s2[2][2]: continue
            t1, p1, _ = s1; t2, p2, _ = s2
            if para(t1, t2) and para(p1, p2): rels.append(("cor", "eq", (i, j), 0))
            elif dot(t1, u) > 0 and dot(t2, u) < 0 and para(p1, tuple(-c for c in p2)): rels.append(("alt", "eq", (i, j), 0))
            elif dot(t1, u) > 0 and dot(t2, u) < 0 and para(p1, p2): rels.append(("coi", "sum", (i, j), 180))
    # one-step facts for x
    xi = [i for i, m in enumerate(marks) if m["l"] == "x"]
    direct = set()
    if xi:
        x = xi[0]
        for kind, typ, ids, c in rels:
            if x in ids and all(isinstance(k, int) for k in ids) and all(k in known for k in ids if k != x): direct.add(kind)
    if DEBUG: print(rels)
    # solve: equal angles are merged first (union-find), then any fact with one unknown left is solved
    par_ = {}
    def F(k):
        while par_.get(k, k) != k: k = par_[k]
        return k
    for kind, typ, ids, c in rels:
        if typ == "eq": par_[F(ids[0])] = F(ids[1])
    cv = {}
    for k, v in known.items():
        if F(k) in cv and cv[F(k)] != v: bad(q, "given angles that should be equal are not")
        cv[F(k)] = v
    eqs = []
    for kind, typ, ids, c in rels:
        if typ == "sum": co = Counter(F(k) for k in ids); eqs.append((co, c))
        elif typ == "ext": co = Counter({F(ids[0]): 1}); co[F(ids[1])] -= 1; co[F(ids[2])] -= 1; eqs.append((co, 0))
    changed = True
    while changed:
        changed = False
        for co, c in eqs:
            unk = [k for k, v in co.items() if v and k not in cv]
            if len(unk) != 1: continue
            u_ = unk[0]; rest = c - sum(v * cv[k] for k, v in co.items() if v and k != u_)
            cv[u_] = rest / co[u_]; changed = True
    allv = set(known) | {k for _, _, ids, _ in rels for k in ids} | set(range(n))
    vals = {k: cv[F(k)] for k in allv if F(k) in cv}
    # every solved value must agree with every relation and with the drawing
    for kind, typ, ids, c in rels:
        if all(k in vals for k in ids):
            ok = (vals[ids[0]] == vals[ids[1]]) if typ == "eq" else (sum(vals[k] for k in ids) == c) if typ == "sum" else (vals[ids[0]] == vals[ids[1]] + vals[ids[2]])
            if not ok: bad(q, f"facts disagree ({kind})")
    for i, m in enumerate(marks):
        if i in vals and abs(vals[i] - m["sw"]) > 0.6: bad(q, f"solved {vals[i]} but the drawing measures {m['sw']:.2f}")
    xv = vals.get(xi[0]) if xi else None
    if xv is not None and xv != int(xv): bad(q, "x not a whole number")
    return (int(xv) if xv is not None else None), direct, vals, marks

KIND = {"angles on a straight line": "str", "angles at a point": "pt", "vertically opposite": "vo", "angles in a triangle": "tri",
        "base angles of an isosceles": "iso", "exterior angle": "ext", "alternate angles": "alt", "corresponding angles": "cor", "co-interior": "coi"}
def kind_of(text):
    k = [v for key, v in KIND.items() if key in text.lower()]
    return k[0] if len(k) == 1 else None
def deg(s):
    m = re.fullmatch(r"(\d+)°", s); return int(m.group(1)) if m else None
def classify_angle(n): return "Acute" if n < 90 else "Right angle" if n == 90 else "Obtuse" if n < 180 else "Straight angle" if n == 180 else "Reflex"
TERMS = {"never meet": "Parallel lines", "meet at a right angle": "Perpendicular lines", "cuts across": "Transversal", "end point at each end": "Line segment",
         "forever in one direction": "Ray", "two arms": "Vertex", "more than 180": "Reflex", "less than 90": "Acute", "between 90": "Obtuse", "exactly 90": "Right angle",
         "all three sides different": "Scalene triangle", "all three sides the same": "Equilateral triangle", "two sides the same": "Isosceles triangle",
         "one angle of 90": "Right-angled triangle", "opposite each other where two lines cross": "Vertically opposite angles", "\"Z\"": "Alternate angles",
         "\"F\"": "Corresponding angles", "next side extended": "Exterior angle"}
FACT = {"full turn": 360, "straight angle": 180, "right angle": 90, "add up to": 180, "equilateral": 60}

if __name__ == "__main__":
    qs = json.load(open(sys.argv[1]))
    for q in qs:
        opts = [q["answer"]] + q["wrong"]
        if len(q["wrong"]) != 3 or len(set(opts)) != 4: bad(q, "not 4 different options")
        blob = json.dumps(q, ensure_ascii=False)
        if re.search(r"NaN|undefined|Infinity|null°|\+ −|−−", blob): bad(q, "junk text")
        t = q["data"].get("t")
        if q["html"].startswith("<svg") and t not in ("type",):
            lines, ticks, tris, marks = parse(q["html"])
            x, direct, vals, marks = solve(q, lines, ticks, tris, marks)
            if x is None: bad(q, "x can't be found from the facts in the picture"); continue
            if t in ("reason",):
                if direct != {kind_of(q["answer"])}: bad(q, f"one-step facts {direct} but answer {q['answer']}")
                for w in q["wrong"]:
                    if kind_of(w) in direct or kind_of(w) is None: bad(q, "wrong option is also right / unreadable: " + w)
                if not q["en"].startswith(f"x = {x}°"): bad(q, f"stem says {q['en'][:12]} but x = {x}")
            elif t == "both":
                good = []
                for o in opts:
                    m = re.fullmatch(r"(\d+)° \((.+)\)", o)
                    if m and int(m.group(1)) == x and kind_of(m.group(2)) in direct: good.append(o)
                if good != [q["answer"]]: bad(q, f"right options {good}, x={x}, direct {direct}")
            else:
                if deg(q["answer"]) != x: bad(q, f"answer {q['answer']} but x = {x}")
                if any(deg(w) is None or deg(w) == x for w in q["wrong"]): bad(q, "bad wrong option")
                for nm in re.findall(r"Find (y|z) first|Find y and z", q["en"]):
                    for lab in ("y", "z") if "and z" in q["en"] else ("y",):
                        ids = [i for i, m in enumerate(marks) if m["l"] == lab]
                        if not ids or ids[0] not in vals: bad(q, f"{lab} can't be found")
                        elif vals[ids[0]] in (None,): bad(q, "y missing")
                if t in ("par2", "isoext", "twoext", "partri") and direct: bad(q, f"meant to be two steps but one fact gives x: {direct}")
        elif t == "type":
            lines, ticks, tris, marks = parse(q["html"])
            m = marks[0]; sw = (angd(m["v"], m["q"]) - angd(m["v"], m["p"])) % 360
            if q["answer"] != classify_angle(round(sw)): bad(q, f"measured {sw:.1f} → {classify_angle(round(sw))}")
        elif t == "trikind":
            a = [int(n) for n in re.findall(r"(\d+)°", q["en"])]
            if sum(a) != 180 or min(a) <= 0: bad(q, "angles don't make a triangle")
            k = "Right-angled triangle" if max(a) == 90 else "Obtuse-angled triangle" if max(a) > 90 else "Acute-angled triangle"
            if q["answer"] != k: bad(q, "wrong kind " + k)
        elif t == "trisides":
            s = sorted(int(n) for n in re.findall(r"(\d+) cm", q["en"]))
            if s[0] + s[1] <= s[2]: bad(q, "sides can't make a triangle")
            k = "Equilateral" if s[0] == s[2] else "Isosceles" if len(set(s)) == 2 else "Scalene"
            if q["answer"] != k: bad(q, "wrong type " + k)
            if "Right-angled" in q["wrong"] and s[0] ** 2 + s[1] ** 2 == s[2] ** 2: bad(q, "it IS right-angled")
            if (k == "Equilateral" and "Isosceles" in opts) or (k == "Isosceles" and "Equilateral" in opts and False): bad(q, "isosceles/equilateral overlap")
        elif t == "could":
            ok = [o for o in opts if (lambda n: sum(n) == 180 and min(n) > 0 and len(n) == 3)([int(v) for v in re.findall(r"\d+", o)])]
            if ok != [q["answer"]]: bad(q, f"triangle sets {ok}")
        elif t == "word":
            k = [v for key, v in TERMS.items() if key in q["frame"]]
            if k != [q["answer"]]: bad(q, f"definition → {k}")
            if q["answer"] == "Isosceles triangle" and "Equilateral triangle" in q["wrong"]: bad(q, "equilateral is also isosceles")
            if q["answer"] == "Equilateral triangle" and "Isosceles triangle" in q["wrong"]: bad(q, "equilateral is also isosceles")
        elif t == "vertex":
            nm = re.search(r"∠([A-Z])([A-Z])([A-Z])", q["en"])
            if not nm or q["answer"] != nm.group(2): bad(q, "vertex wrong")
        elif t == "fact":
            k = [v for key, v in FACT.items() if key in q["en"]]
            if len(k) != 1 or str(k[0]) != q["answer"]: bad(q, f"fact {k}")
        else: bad(q, "unchecked question type " + str(t))

    print(len(qs), "questions;", dict(Counter(q["mk"] for q in qs)))
    print(len(probs), "problems")
    for p in Counter((p[0], p[1]) for p in probs).most_common(20): print(p)
    for p in probs[:6]: print(p)
