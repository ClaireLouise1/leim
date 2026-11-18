#!/usr/bin/env python3
"""Independent checker for Proof Builder (JC Maths topic 24).
node src/test_proof_builder.js > /tmp/pb.json ; python3 src/test_proof_builder.py /tmp/pb.json
It MEASURES every diagram (angles at marks, lengths of labelled segments with data-s, circles, parallel lines),
classifies congruence cases from the labels it finds on each triangle, uses its own answer key for proofs,
and its own truth tables for the word questions."""
import json, re, sys, math, itertools
from fractions import Fraction as Fr

TOL_A = 0.35   # degrees
TOL_L = 0.03   # cm

def P(s): return tuple(float(v) for v in s.split(","))
def attrs(tag):
    return dict(re.findall(r'([\w-]+)="([^"]*)"', tag))

def read_svg(html):
    m = re.search(r'<svg class="pf"[^>]*>', html)
    if not m: return None
    top = attrs(m.group(0)); s = float(top.get("data-s", 0) or 0)
    D = {"s": s, "lines": [], "polys": [], "circs": [], "marks": [], "lens": [], "names": {}, "dots": [], "pars": 0}
    for t in re.findall(r'<line class="ln"[^>]*/>', html):
        a = attrs(t); D["lines"].append(((float(a["x1"]), float(a["y1"])), (float(a["x2"]), float(a["y2"])), int(a.get("data-g", 0))))
    for t in re.findall(r'<polygon class="tri"[^>]*/>', html):
        D["polys"].append([P(x) for x in attrs(t)["data-pts"].split()])
    for t in re.findall(r'<circle class="cir"[^>]*/>', html):
        a = attrs(t); D["circs"].append((P(a["data-c"]), float(a["data-r"])))
    for t in re.findall(r'<circle class="dot"[^>]*/>', html):
        D["dots"].append(P(attrs(t)["data-p"]))
    for g in re.findall(r'<g class="am"[^>]*>', html):
        a = attrs(g); D["marks"].append({"v": P(a["data-v"]), "p": P(a["data-p"]), "q": P(a["data-q"]), "l": a["data-l"]})
    for t, txt in re.findall(r'(<text class="ll"[^>]*>)([^<]*)</text>', html):
        a = attrs(t); D["lens"].append({"a": P(a["data-a"]), "b": P(a["data-b"]), "t": txt})
    for t, txt in re.findall(r'(<text class="vn"[^>]*>)([^<]*)</text>', html):
        D["names"][txt] = P(attrs(t)["data-p"])
    D["pars"] = html.count('class="par"')
    return D

def d(a, b): return math.hypot(a[0] - b[0], a[1] - b[1])
def angle(v, p, q):
    a1 = math.atan2(p[1] - v[1], p[0] - v[0]); a2 = math.atan2(q[1] - v[1], q[0] - v[0])
    x = abs(math.degrees(a1 - a2)) % 360
    return 360 - x if x > 180 else x
def mang(m): return angle(m["v"], m["p"], m["q"])
def close(a, b, t=TOL_A): return abs(a - b) <= t
def same(p, q, t=0.6): return d(p, q) <= t
def numval(s):
    s = s.replace("−", "-").replace(" cm", "").replace(" m", "").replace("°", "").strip()
    return float(s)
def cross(a, b, c, e):  # direction cross product of ab and ce
    return (b[0] - a[0]) * (e[1] - c[1]) - (b[1] - a[1]) * (e[0] - c[0])
def parallel(a, b, c, e): return abs(cross(a, b, c, e)) / (d(a, b) * d(c, e)) < 0.004
def on_seg(p, a, b): return abs(d(a, p) + d(p, b) - d(a, b)) < 0.6

def is_para(Q):
    A, B, C, D_ = Q
    return same((A[0] + C[0], A[1] + C[1]), (B[0] + D_[0], B[1] + D_[1]), 1.0)

def lin(expr):
    """'3x + 5' or '2x − 7' → (m, c)"""
    e = expr.replace("−", "-").replace(" ", "")
    m_ = re.fullmatch(r"(\d*)x([+-]\d+)?", e)
    assert m_, expr
    return int(m_.group(1) or 1), int(m_.group(2) or 0)

problems = []
def bad(q, msg):
    problems.append((q.get("mk"), msg, q["en"][:110], q["answer"], q["wrong"]))

def opts(q): return [q["answer"]] + q["wrong"]
def deg(s): return int(s.rstrip("°"))

# ---------- my own answer key for the proofs ----------
G = "Given"; ALT = "Alternate angles"; COR = "Corresponding angles"; STR = "Angles on a straight line add to 180°"; TRI = "Angles in a triangle add to 180°"
COI = "Co-interior angles add to 180°"; ISO = "Isosceles triangle: base angles are equal"; COM = "Common side"; RAD = "Radii of the same circle"
MATCH = "Matching parts of congruent triangles are equal"
KEY = {
    "T9": [("∠BAC = ∠ACD", {ALT}, []), ("∠BCA = ∠CAD", {ALT}, []), ("|AC| = |CA|", {COM}, []), ("△ABC ≡ △CDA", {"ASA"}, [0, 1, 2]), ("So |AB| = |CD| and |BC| = |DA|", {MATCH}, [3])],
    "T10": [("∠EAB = ∠ECD", {ALT}, []), ("∠EBA = ∠EDC", {ALT}, []), ("|AB| = |CD|", {"Opposite sides of a parallelogram are equal"}, []), ("△ABE ≡ △CDE", {"ASA"}, [0, 1, 2]), ("So |AE| = |CE| and |BE| = |DE|", {MATCH}, [3])],
    "ISO": [("|AB| = |AC|", {G}, []), ("|BD| = |DC|", {"D is the midpoint of [BC]", G}, []), ("|AD| = |AD|", {COM}, []), ("△ABD ≡ △ACD", {"SSS"}, [0, 1, 2]), ("So ∠ABD = ∠ACD", {MATCH}, [3])],
    "SEMI": [("|OA| = |OB| = |OC|", {RAD}, []), ("∠OBA = ∠OAB: call them x", {ISO}, [0]), ("∠OCA = ∠OAC: call them y", {ISO}, [0]), ("x + y + (x + y) = 180°", {TRI}, [1, 2]), ("So ∠BAC = x + y = 90°", {"Divide both sides by 2"}, [3])],
    "OPP": [("∠A + ∠B = 180°", {COI}, []), ("∠B + ∠C = 180°", {COI}, []), ("So ∠A = ∠C", {"Both equal 180° − ∠B"}, [0, 1])],
    "T4": [("∠DAB = ∠ABC", {ALT}, []), ("∠EAC = ∠ACB", {ALT}, []), ("∠DAB + ∠BAC + ∠EAC = 180°", {STR}, []), ("So ∠ABC + ∠BAC + ∠ACB = 180°", {"Put in the equal angles from lines 1 and 2"}, [0, 1, 2])],
    "T1": [("a + b = 180°", {STR}, []), ("b + c = 180°", {STR}, []), ("So a = c", {"Both equal 180° − b"}, [0, 1])],
    "SIM": [("∠ADE = ∠ABC", {COR}, []), ("∠AED = ∠ACB", {COR}, []), ("∠DAE = ∠BAC", {"Common angle"}, []), ("△ADE and △ABC are similar", {"Equiangular triangles are similar"}, [0, 1, 2]), ("So |AD| : |AB| = |DE| : |BC|", {"Similar triangles: sides in proportion"}, [3])],
    "KITE": [("|AB| = |AD|", {G}, []), ("|CB| = |CD|", {G}, []), ("|AC| = |AC|", {COM}, []), ("△ABC ≡ △ADC", {"SSS"}, [0, 1, 2]), ("So ∠ABC = ∠ADC", {MATCH}, [3])],
}
ALL_REASONS = {G, ALT, COR, STR, TRI, COI, ISO, COM, RAD, MATCH, "Vertically opposite angles", "Angles at a point add to 360°", "Common angle", "D is the midpoint of [BC]",
               "Opposite sides of a parallelogram are equal", "SSS", "SAS", "ASA", "RHS", "Equiangular triangles are similar", "Similar triangles: sides in proportion",
               "Divide both sides by 2", "Both equal 180° − ∠B", "Both equal 180° − b", "Put in the equal angles from lines 1 and 2"}
def steps(html):
    return re.findall(r'<p data-line="([A-F\d])"><b>[A-F\d]\.</b> (.*?) <span class="rs( gap)?">\((.*?)\)</span></p>', html)
def valid_order(key, idx):
    pos = {i: n for n, i in enumerate(idx)}
    return all(pos[dd] < pos[i] for i in idx for dd in key[i][2])

def check_proof(q):
    t = q["data"]["t"]; pid = q["data"]["id"]; key = KEY[pid]; st = steps(q["html"])
    if t == "gap":
        assert len(st) == len(key), pid
        for n, (lab, s, g, r) in enumerate(st):
            if s != key[n][0]: bad(q, f"line {n+1} statement differs from my key: {s}")
            if not g and r not in key[n][1]: bad(q, f"shown reason not in my key: {s} ({r})")
        gl = [n for n, x in enumerate(st) if x[2]]
        if len(gl) != 1 or st[gl[0]][3] != "?": bad(q, "gap not shown once"); return
        n = gl[0]
        if q["answer"] not in key[n][1]: bad(q, f"answer {q['answer']} not acceptable for {key[n][0]}")
        for w in q["wrong"]:
            if w in key[n][1]: bad(q, f"wrong option is acceptable: {w}")
            if w not in ALL_REASONS: bad(q, f"unknown reason {w}")
    else:
        lines = {lab: s for lab, s, g, r in st}
        stmts = [k[0] for k in key]
        for lab, s, g, r in st:
            i = stmts.index(s)
            if r not in key[i][1]: bad(q, f"order: shown reason wrong {s} ({r})")
        def idx_of(o): return [stmts.index(lines[x.strip()]) for x in o.split(",")]
        if not valid_order(key, idx_of(q["answer"])): bad(q, "order answer is not a valid proof order")
        for w in q["wrong"]:
            ix = idx_of(w)
            if sorted(ix) != list(range(len(key))): bad(q, "order option is not a permutation")
            if valid_order(key, ix): bad(q, f"wrong order is valid: {w}")

# ---------- word keys (my own) ----------
TERMS = {"accepted without proof": "Axiom", "has been proved": "Theorem", "chain of logical steps": "Proof", "follows quickly": "Corollary", "swapping": "Converse", "⇒": "Implies"}
TRUE_FACTS = {"In every parallelogram, the diagonals bisect each other.": True, "In every parallelogram, opposite sides are equal in length.": True,
    "In every parallelogram, opposite angles are equal.": True, "In every parallelogram, neighbouring angles add to 180°.": True,
    "A diagonal cuts a parallelogram into two congruent triangles.": True, "Every angle in a semicircle is 90°.": True,
    "In every parallelogram, the diagonals are equal in length.": False, "In every parallelogram, the diagonals meet at 90°.": False,
    "In every parallelogram, all four angles are equal.": False, "In every parallelogram, all four sides are equal.": False,
    "In every parallelogram, opposite angles add to 180°.": False, "Every angle in a semicircle is 180°.": False, "Two triangles with equal angles must be congruent.": False}

def conv_ok(stmt, cand):
    m = re.fullmatch(r"If (.*), then (.*)\.", stmt); n = re.fullmatch(r"If (.*), then (.*)\.", cand)
    if not (m and n): return False
    # my own swap test: the hypothesis of the candidate must talk about the original conclusion and vice versa
    def keyw(s): return set(w for w in re.findall(r"[a-z\[\]A-Z°0-9]+", s.lower()) if len(w) > 3 and w not in {"then", "that", "quadrilateral's", "quadrilateral", "triangle", "angles", "lines", "line", "circle"})
    a, b = keyw(m.group(1)), keyw(m.group(2)); c, e = keyw(n.group(1)), keyw(n.group(2))
    neg = re.search(r"\bnot\b|n't", n.group(1))
    return not neg and (b & c) and (a & e) and not (a <= c and not (b & c - a))

# ---------- main ----------
def main(path):
    Qs = json.load(open(path, encoding="utf-8"))
    counts = {}
    for q in Qs:
        t = q["data"]["t"]; counts[t] = counts.get(t, 0) + 1
        o = opts(q)
        if len(q["wrong"]) != 3 or len(set(o)) != 4: bad(q, "need 4 different options")
        blob = json.dumps(q, ensure_ascii=False)
        if "undefined" in blob or "NaN" in blob or "Infinity" in blob: bad(q, "undefined/NaN")
        if re.search(r"(?<![\w-])-\d", q["en"] + q["answer"] + " ".join(q["wrong"]) + q["why"]): bad(q, "ASCII minus")
        if re.search(r"\b1x\b|\+ −|  ", q["en"] + q["why"]): bad(q, "1x / + − / double space")
        if re.search(r"\b(\w+) \1\b", q["en"] + " " + q["why"]): bad(q, "doubled word")
        if q["data"].get("hl") and not q["en"].startswith("Higher Level: "): bad(q, "HL label missing")
        try:
            check(q, t)
        except Exception as e:
            bad(q, f"checker error {type(e).__name__}: {e}")
    print(len(Qs), "questions,", len(problems), "problems")
    print(counts)
    seen = set()
    for p in problems:
        if p[1] in seen: continue
        seen.add(p[1]); print(p)
    return len(problems)

def unk_mark(D):
    xs = [m for m in D["marks"] if re.search(r"[a-z]", m["l"])]
    assert len(xs) == 1, [m["l"] for m in D["marks"]]
    return xs[0]
def num_marks_ok(q, D):
    for m in D["marks"]:
        if re.fullmatch(r"\d+", m["l"]) and not close(mang(m), int(m["l"])): bad(q, f"label {m['l']}° but drawn {mang(m):.2f}°")
        if m["l"] == "rt" and not close(mang(m), 90): bad(q, "right-angle mark not 90°")
def lens_ok(q, D):
    if not D["s"]: return
    for l in D["lens"]:
        if "cm" in l["t"]:
            if abs(numval(l["t"]) - d(l["a"], l["b"]) / D["s"]) > TOL_L: bad(q, f"label {l['t']} but drawn {d(l['a'], l['b']) / D['s']:.3f}")
def ans_num(q): return numval(q["answer"])
def wrong_nums(q): return [numval(w) for w in q["wrong"]]
def num_options_ok(q, unit):
    for x in opts(q):
        if not re.fullmatch(r"\d+(\.\d)?" + re.escape(unit), x): bad(q, f"option format {x!r}")
    a = ans_num(q)
    for w in wrong_nums(q):
        if abs(w - a) < 1e-9: bad(q, "wrong option equal in value")
def ang_options_ok(q):
    for x in opts(q):
        if not re.fullmatch(r"\d+°", x) or not 0 < deg(x) < 360: bad(q, f"angle option {x!r}")
def on_circle(D, p): return any(abs(d(c, p) - r) < 0.6 for c, r in D["circs"])

def check(q, t):
    if t in ("gap", "order"): return check_proof(q)
    D = read_svg(q["html"]) if q["html"] else None
    if D: num_marks_ok(q, D); lens_ok(q, D)
    if t == "paraang":
        assert len(D["polys"]) == 1 and is_para(D["polys"][0]), "not a parallelogram"
        assert D["pars"] >= 4
        x = unk_mark(D); ang_options_ok(q)
        if not close(mang(x), deg(q["answer"])): bad(q, f"x drawn {mang(x):.2f}")
        if str(deg(q["answer"])) not in q["why"]: bad(q, "why lacks answer")
    elif t == "paraalg":
        assert is_para(D["polys"][0])
        x = unk_mark(D); m_, c_ = lin(x["l"]); val = (round(mang(x)) - c_) / m_
        if not close(mang(x), round(mang(x)), 0.3): bad(q, "expression angle not whole")
        if abs(val - ans_num(q)) > 1e-9: bad(q, f"x should be {val}")
        num_options_ok(q, "")
    elif t in ("paraside", "paraper", "paraback"):
        Q = D["polys"][0]; assert is_para(Q)
        per = sum(d(Q[i], Q[(i + 1) % 4]) for i in range(4)) / D["s"]
        if t == "paraper":
            if abs(per - ans_num(q)) > TOL_L: bad(q, f"perimeter drawn {per:.3f}")
            num_options_ok(q, " cm")
        else:
            xs = [l for l in D["lens"] if l["t"] == "x"]; assert len(xs) == 1
            v = d(xs[0]["a"], xs[0]["b"]) / D["s"]
            if abs(v - ans_num(q)) > TOL_L: bad(q, f"x drawn {v:.3f}")
            if t == "paraback":
                pp = int(re.search(r"perimeter of (\d+) cm", q["en"]).group(1))
                if abs(pp - per) > TOL_L: bad(q, "stated perimeter isn't the drawn one")
                # x must be found from labels: p/2 - other
                other = [numval(l["t"]) for l in D["lens"] if l["t"] != "x"]
                if abs(pp / 2 - other[0] - ans_num(q)) > 1e-9: bad(q, "paraback algebra")
            num_options_ok(q, " cm")
    elif t in ("diaghalf", "diagwhole", "diagalg"):
        Q = D["polys"][0]; assert is_para(Q)
        E = D["dots"][0]
        if not same(E, ((Q[0][0] + Q[2][0]) / 2, (Q[0][1] + Q[2][1]) / 2)) or not same(E, ((Q[1][0] + Q[3][0]) / 2, (Q[1][1] + Q[3][1]) / 2)): bad(q, "O not the midpoint of both diagonals")
        if t == "diaghalf":
            x = [l for l in D["lens"] if l["t"] == "x"][0]; v = d(x["a"], x["b"]) / D["s"]
            if abs(v - ans_num(q)) > TOL_L: bad(q, f"x drawn {v:.3f}")
            num_options_ok(q, " cm")
        elif t == "diagwhole":
            seg = re.search(r"Find \|(\w)(\w)\|", q["en"]); a, b = D["names"][seg.group(1)], D["names"][seg.group(2)]
            v = d(a, b) / D["s"]
            if abs(v - ans_num(q)) > TOL_L: bad(q, f"|{seg.group(0)}| drawn {v:.3f}")
            num_options_ok(q, " cm")
        else:
            ex = [l for l in D["lens"] if "x" in l["t"]][0]; m_, c_ = lin(ex["t"]); v = d(ex["a"], ex["b"]) / D["s"]
            if abs((v - c_) / m_ - ans_num(q)) > TOL_L: bad(q, "diag algebra")
            num_options_ok(q, "")
    elif t in ("semi", "semi90"):
        (Oc, r), = D["circs"]; x = unk_mark(D); ang_options_ok(q)
        # find the diameter: a drawn line through the centre with both ends on the circle
        dia = [l for l in D["lines"] if on_seg(Oc, l[0], l[1]) and abs(d(l[0], l[1]) - 2 * r) < 1]
        if len(dia) != 1: bad(q, "no diameter")
        if not on_circle(D, x["v"]): bad(q, "x vertex not on circle")
        if not close(mang(x), deg(q["answer"])): bad(q, f"x drawn {mang(x):.2f}")
    elif t in ("centre", "samearc", "cyclic"):
        x = unk_mark(D); ang_options_ok(q)
        if not close(mang(x), deg(q["answer"])): bad(q, f"x drawn {mang(x):.2f}")
        for m in D["marks"]:
            if not on_circle(D, m["v"]) and not (D["dots"] and same(m["v"], D["dots"][0])): bad(q, "mark vertex not on circle / centre")
        # Theorem checks from the drawing itself
        if t == "cyclic":
            if len(D["polys"]) and len(D["polys"][0]) != 4: bad(q, "cyclic poly")
    elif t == "case": check_case(q, D)
    elif t == "simpair": check_simpair(q, D)
    elif t == "nest": check_nest(q, D)
    elif t == "ratio":
        r, tt, AC = q["data"]["r"], q["data"]["tt"], q["data"]["AC"]
        rr = re.search(r"\|AD\| : \|DB\| = (\d+) : (\d+)", q["en"]); r2, t2 = int(rr.group(1)), int(rr.group(2))
        ac = numval([l for l in D["lens"]][0]["t"])
        N = D["names"]
        if abs(d(N["A"], N["D"]) / d(N["A"], N["B"]) - r2 / (r2 + t2)) > 0.003: bad(q, "D not at the stated ratio")
        if abs(d(N["A"], N["E"]) / d(N["A"], N["C"]) - r2 / (r2 + t2)) > 0.003: bad(q, "E not at the same ratio")
        want = Fr(int(ac)) * (r2 if "|AE|" in q["en"] else t2) / (r2 + t2)
        if abs(float(want) - ans_num(q)) > 1e-9: bad(q, f"ratio answer should be {want}")
        num_options_ok(q, " cm")
    elif t == "three":
        b = int(re.search(r"first segment is (\d+) cm", q["en"]).group(1))
        if ans_num(q) != b: bad(q, "theorem 11")
        num_options_ok(q, " cm")
    elif t == "shadow":
        m_ = re.search(r"([\d.]+) m tall casts a shadow ([\d.]+) m long, and a \w+( post)? casts a shadow ([\d.]+) m long", q["en"])
        p, sh, T = float(m_.group(1)), float(m_.group(2)), float(m_.group(4))
        if abs(p * T / sh - ans_num(q)) > 1e-9: bad(q, "shadow")
        num_options_ok(q, " m")
    elif t == "issim":
        m_ = re.search(r"Triangle 1 has sides (.*?) cm\. Triangle 2 has sides (.*?) cm\.", q["en"])
        A = sorted(Fr(x.strip()) for x in m_.group(1).split(" cm,")); B = sorted(Fr(x.strip()) for x in m_.group(2).split(" cm,"))
        ok = len({b / a for a, b in zip(A, B)}) == 1
        if q["answer"].startswith("Yes") != ok: bad(q, "issim verdict")
        if ok and f"× {float(B[0] / A[0]):g}" not in q["answer"]: bad(q, "issim factor")
        for w in q["wrong"]:
            if ok and w.startswith("Yes: every side is ×"): bad(q, "issim wrong yes")
            if not ok and w.startswith("No"): bad(q, "issim wrong no")
    elif t == "simang":
        m_ = re.findall(r"angles (\d+)° and (\d+)°", q["en"]); a1, b1 = map(int, m_[0]); a2, b2 = map(int, m_[1])
        ok = sorted([a1, b1, 180 - a1 - b1]) == sorted([a2, b2, 180 - a2 - b2])
        if q["answer"].startswith("Yes") != ok: bad(q, "simang verdict")
        if 180 - a2 - b2 <= 0: bad(q, "simang impossible triangle")
        for w in q["wrong"]:
            if ok and w.startswith("Yes"): bad(q, "simang wrong yes")
    elif t == "ispara":
        en = q["en"]
        if "diagonals" in en: v, kind = True, "diagonals"
        else:
            vals = [int(x) for x in re.findall(r"(\d+)(?:°| cm)", en)]
            kind = "angles" if "°" in en else "sides"
            v = vals[0] == vals[2] and vals[1] == vals[3]
        if q["answer"].startswith("Yes") != v: bad(q, "ispara verdict")
        word = {"angles": "angles", "sides": "sides", "diagonals": "diagonals"}[kind]
        if word not in q["answer"]: bad(q, "ispara reason doesn't match the data given")
        for w in q["wrong"]:
            if w.startswith("Yes") == v and word in w and "90°" not in w: bad(q, f"ispara wrong option also right: {w}")
    elif t == "diam":
        a = int(re.search(r"∠BAC = (\d+)°", q["en"]).group(1))
        if q["answer"].startswith("Yes") != (a == 90): bad(q, "diam")
        if any(w.startswith("Yes: the angle") for w in q["wrong"]) and a == 90: bad(q, "diam wrong")
    elif t == "true":
        if not TRUE_FACTS[q["answer"]]: bad(q, "true answer is false")
        for w in q["wrong"]:
            if TRUE_FACTS[w]: bad(q, f"true: wrong option is true: {w}")
    elif t in ("match", "matchang"):
        m_ = re.search(r"△(\w{3}) ≡ △(\w{3})", q["en"]); A, B = m_.group(1), m_.group(2); mp = dict(zip(A, B))
        if t == "match":
            s = re.search(r"equal to \[(\w)(\w)\]", q["en"]); want = {mp[s.group(1)], mp[s.group(2)]}
            def seg(x): return set(x.strip("[]"))
            if seg(q["answer"]) != want: bad(q, "match side")
            for w in q["wrong"]:
                if seg(w) == want: bad(q, "match wrong is right")
        else:
            s = re.search(r"equal to ∠(\w)(\w)(\w)", q["en"]); want = mp[s.group(2)]
            def vtx(x): return x[2] if x.startswith("∠") else None
            if vtx(q["answer"]) != want: bad(q, "matchang")
            for w in q["wrong"]:
                if vtx(w) == want: bad(q, "matchang wrong is right")
    elif t == "congfind":
        m_ = re.search(r"△ABC ≡ △(\w{3})\. \|AB\| = (\d+) cm, \|BC\| = (\d+) cm and ∠ABC = (\d+)°\. Find (.*?)\.$", q["en"]); B = m_.group(1)
        mp = dict(zip("ABC", B)); inv = {v: k for k, v in mp.items()}
        tgt = m_.group(5)
        if tgt.startswith("|"):
            ends = {inv[tgt[1]], inv[tgt[2]]}
            want = int(m_.group(2)) if ends == {"A", "B"} else int(m_.group(3)) if ends == {"B", "C"} else None
            if want is None or ans_num(q) != want: bad(q, "congfind side")
            num_options_ok(q, " cm")
        else:
            if inv[tgt[2]] != "B" or deg(q["answer"]) != int(m_.group(4)): bad(q, "congfind angle")
            ang_options_ok(q)
    elif t == "congword":
        en = q["en"]
        if "NOT a test" in en:
            for w in q["wrong"]:
                if w not in ("SSS", "SAS", "ASA", "RHS"): bad(q, "congword NOT")
            if q["answer"] in ("SSS", "SAS", "ASA", "RHS"): bad(q, "congword NOT answer")
        elif "RHS stand" in en:
            if q["answer"] != "Right angle, Hypotenuse, Side": bad(q, "RHS")
        elif "In SAS" in en:
            if "Between" not in q["answer"]: bad(q, "SAS")
        elif "congruent?" in en:
            if "same size" not in q["answer"] or any("same shape and the same size" in w for w in q["wrong"]): bad(q, "congruent meaning")
        elif "hypotenuse" in en:
            if "opposite the right angle" not in q["answer"]: bad(q, "hyp")
        else: bad(q, "unknown congword")
    elif t == "term":
        want = [v for k, v in TERMS.items() if k in q["frame"]]
        if want != [q["answer"]]: bad(q, f"term {want}")
    elif t == "conv":
        if not conv_ok(q["frame"], q["answer"]): bad(q, "converse answer fails my swap test")
        for w in q["wrong"]:
            if conv_ok(q["frame"], w): bad(q, f"converse wrong option passes: {w}")
    else:
        bad(q, "unknown type " + t)

# ---------- congruent triangles ----------
def tri_info(D, T):
    """labels that belong to triangle T: sides (frozenset of vertex indices) and angles (vertex index)"""
    def vi(p):
        for i, v in enumerate(T):
            if same(p, v, 0.8): return i
        return None
    sides, angs = {}, {}
    for l in D["lens"]:
        a, b = vi(l["a"]), vi(l["b"])
        if a is not None and b is not None: sides[frozenset((a, b))] = numval(l["t"])
    for m in D["marks"]:
        v = vi(m["v"])
        if v is not None:
            # the mark must be the interior angle at v
            if not close(mang(m), angle(T[v], T[(v + 1) % 3], T[(v + 2) % 3])): continue
            angs[v] = 90 if m["l"] == "rt" else int(m["l"])
    return sides, angs
def classify(sides, angs):
    if len(sides) == 3: return "SSS"
    rt = [v for v, a in angs.items() if a == 90]
    if rt and len(sides) == 2:
        hyp = frozenset(i for i in range(3) if i != rt[0])
        if hyp in sides: return "RHS"
    if len(sides) == 2 and len(angs) == 1:
        v = next(iter(angs)); s1, s2 = list(sides)
        if v in s1 and v in s2: return "SAS"
        return "no"
    if len(angs) == 2 and len(sides) == 1:
        s = next(iter(sides))
        return "ASA" if set(angs) == set(s) else "AAS"
    if len(angs) == 3 and not sides: return "no"
    return "?"
def sorted_sides(T): return sorted(d(T[i], T[(i + 1) % 3]) for i in range(3))
def check_case(q, D):
    assert len(D["polys"]) == 2
    res = []
    for T in D["polys"]:
        s, a = tri_info(D, T); res.append((classify(s, a), sorted(s.values()), sorted(a.values())))
    if res[0] != res[1]: bad(q, f"the two triangles show different information {res}")
    kind = res[0][0]
    if kind in ("?", "AAS"): bad(q, f"unclear case {kind}")
    want = {"SSS": "SSS", "SAS": "SAS", "ASA": "ASA", "RHS": "RHS", "no": "Not enough information"}[kind]
    if not q["answer"].startswith(want): bad(q, f"case should be {want}")
    for w in q["wrong"]:
        if w.startswith(want): bad(q, "case wrong option right")
    S0, S1 = sorted_sides(D["polys"][0]), sorted_sides(D["polys"][1])
    congruent = all(abs(a - b) < 0.8 for a, b in zip(S0, S1))
    if (kind != "no") != congruent: bad(q, f"drawn triangles congruent={congruent} but case {kind}")

# ---------- similar triangles ----------
def check_simpair(q, D):
    assert len(D["polys"]) == 2
    T1, T2 = D["polys"]
    def marks_of(T):
        out = {}
        for m in D["marks"]:
            for i, v in enumerate(T):
                if same(m["v"], v, 0.8): out[m["l"]] = (i, mang(m))
        return out
    M1, M2 = marks_of(T1), marks_of(T2)
    if set(M1) != {"=1", "=2", "=3"} or set(M2) != set(M1): bad(q, "angle marks missing"); return
    for k in M1:
        if not close(M1[k][1], M2[k][1], 0.5): bad(q, f"marked angles {k} differ: {M1[k][1]:.2f} v {M2[k][1]:.2f}")
    corr = {M1[k][0]: M2[k][0] for k in M1}
    def lab(T):
        out = {}
        for l in D["lens"]:
            ii = [i for i, v in enumerate(T) if same(l["a"], v, 0.8) or same(l["b"], v, 0.8)]
            if len(ii) == 2: out[frozenset(ii)] = l["t"]
        return out
    L1, L2 = lab(T1), lab(T2)
    known = [s for s, v in L2.items() if v != "x"]; xs = [s for s, v in L2.items() if v == "x"]
    assert len(known) == 1 and len(xs) == 1
    inv = {v: k for k, v in corr.items()}
    k1 = frozenset(inv[i] for i in known[0]); x1 = frozenset(inv[i] for i in xs[0])
    ratio = Fr(str(numval(L2[known[0]]))) / Fr(str(numval(L1[k1])))
    want = Fr(str(numval(L1[x1]))) * ratio
    if abs(float(want) - ans_num(q)) > 1e-9: bad(q, f"simpair should be {want}")
    i, j = list(xs[0]); meas = d(T2[i], T2[j]) / D["s"]
    if abs(meas - ans_num(q)) > TOL_L: bad(q, f"simpair x drawn {meas:.3f}")
    num_options_ok(q, " cm")

def check_nest(q, D):
    N = D["names"]; A, B, C, Dd, E = (N[k] for k in "ABCDE")
    if not on_seg(Dd, A, B) or not on_seg(E, A, C): bad(q, "D/E not on the sides")
    if not parallel(Dd, E, B, C): bad(q, "DE not parallel to BC")
    if D["pars"] < 2: bad(q, "no parallel arrows")
    lab = {}
    for l in D["lens"]:
        nm = "".join(sorted(k for k in "ABCDE" if same(l["a"], N[k], 0.8) or same(l["b"], N[k], 0.8)))
        lab[nm] = l["t"]
    vals = {k: (None if v == "x" else Fr(str(numval(v)))) for k, v in lab.items()}
    # my own solve: AD/AB = DE/BC with AB = AD + DB
    AD = vals.get("AD"); DB = vals.get("BD"); AB = vals.get("AB"); DE = vals.get("DE"); BC = vals.get("BC")
    if AB is None and AD is not None and DB is not None: AB = AD + DB
    xk = [k for k, v in lab.items() if v == "x"][0]
    if xk == "BC": want = DE * AB / AD
    elif xk == "DE": want = BC * AD / AB
    elif xk == "BD": want = AD * BC / DE - AD
    elif xk == "AB": want = AD * BC / DE
    else: raise ValueError(xk)
    if abs(float(want) - ans_num(q)) > 1e-9: bad(q, f"nest should be {want}")
    i = xk
    a, b = N[i[0]], N[i[1]]
    if abs(d(a, b) / D["s"] - ans_num(q)) > TOL_L: bad(q, f"nest x drawn {d(a, b) / D['s']:.3f}")
    num_options_ok(q, " cm")

if __name__ == "__main__":
    sys.exit(1 if main(sys.argv[1]) else 0)
