"""Recompute every Venn Sorter answer independently (Python sets; shaded regions read from the SVG).
node src/test_venn_sorter.js > /tmp/vs.json ; python3 src/test_venn_sorter.py /tmp/vs.json"""
import json, sys, re, itertools
qs = json.load(open(sys.argv[1])); probs = 0
def is_prime(n): return n > 1 and all(n % d for d in range(2, int(n ** .5) + 1))
RULE = {"even numbers": lambda n: n % 2 == 0, "odd numbers": lambda n: n % 2 == 1, "multiples of 3": lambda n: n % 3 == 0,
        "multiples of 4": lambda n: n % 4 == 0, "multiples of 5": lambda n: n % 5 == 0, "prime numbers": is_prime,
        "square numbers": lambda n: int(round(n ** .5)) ** 2 == n, "factors of 24": lambda n: 24 % n == 0,
        "factors of 30": lambda n: 30 % n == 0, "factors of 36": lambda n: 36 % n == 0}
def listing(s):
    if s == "∅": return []
    m = re.fullmatch(r"\{([\d, ]*)\}", s); assert m, s
    return [int(x) for x in m[1].split(", ")] if m[1] else []
def L(xs): xs = sorted(set(xs)); return "{" + ", ".join(map(str, xs)) + "}" if xs else "∅"
# --- set expression parser over abstract regions ---
def regions(n): return list(itertools.product([0, 1], repeat=n))
def parse(s, n):
    toks = re.findall(r"[ABC]|[∩∪\\()′]", s); i = 0
    allr = frozenset(regions(n))
    def atom():
        nonlocal i
        t = toks[i]; i += 1
        if t == "(": v = expr(); assert toks[i] == ")"; i += 1
        else: k = "ABC".index(t); assert k < n; v = frozenset(r for r in allr if r[k])
        while i < len(toks) and toks[i] == "′": v = allr - v; i += 1
        return v
    def expr():
        nonlocal i
        v = atom(); ops = set()
        while i < len(toks) and toks[i] in "∩∪\\":
            op = toks[i]; i += 1; ops.add(op); w = atom()
            v = v & w if op == "∩" else v | w if op == "∪" else v - w
        assert len(ops) <= 1 and not (ops == {"\\"} and False), s  # mixed operators must be bracketed
        return v
    v = expr(); assert i == len(toks), s; return v
def reg_of_bits(g, n): return tuple((g >> k) & 1 for k in range(n))
NAME2 = {"A only": 1, "B only": 2, "A and B (A ∩ B)": 3, "Outside both": 0}
NAME3 = {n: g for g, n in enumerate(["Outside all three", "A only", "B only", "A and B only", "C only", "A and C only", "B and C only", "A, B and C"])}
def nums(html):
    return {int(g): (int(v) if v.isdigit() else v) for g, v in re.findall(r'<text data-r="(\d)"[^>]*>([^<]+)</text>', html)}
for q in qs:
    d = q["data"]; t = d["t"]; a = q["answer"]; w = q["wrong"]; ok = True; msg = ""
    try:
        if len(w) != 3 or len(set(w + [a])) != 4: raise AssertionError("options")
        if any("undefined" in x or "NaN" in x or x == "" for x in w + [a]) or "undefined" in q["en"] + q["why"] + q["review"] + q["frame"]: raise AssertionError("undefined")
        if t in ("sort", "sort3"):
            rules = re.findall(r"[ABC] = the ([a-z0-9 ]+?)[,.]", q["en"]); x = int(re.search(r"Where does (\d+) go", q["en"])[1])
            top = int(re.search(r"…, (\d+)\}", q["en"])[1]); assert 1 <= x <= top
            g = sum(1 << k for k, r in enumerate(rules) if RULE[r](x))
            names = NAME2 if t == "sort" else NAME3
            assert names[a] == g, (a, g); assert all(names[o] != g for o in w)
        elif t == "sortw":
            A, B, x = re.search(r"A = the letters in (\w+), B = the letters in (\w+)\. Where does the letter (\w) go", q["en"]).groups()
            g = (x in A) + 2 * (x in B); assert NAME2[a] == g and all(NAME2[o] != g for o in w)
        elif t == "op":
            A = listing(re.search(r"A = (\{[^}]*\})", q["en"])[1]); bm = re.search(r"B = (\{[^}]*\})", q["en"]); B = listing(bm[1]) if bm else []
            tm = re.search(r"…, (\d+)\}", q["en"]); U = set(range(1, int(tm[1]) + 1)) if tm else None
            op = q["frame"]; A, B = set(A), set(B)
            exp = {"A ∩ B": A & B, "A ∪ B": A | B, "A \\ B": A - B, "B \\ A": B - A, "A′": (U - A) if U else None, "(A ∪ B)′": (U - (A | B)) if U else None}[op]
            assert listing(a) == sorted(exp), (op, a); assert all(set(listing(o)) != exp for o in w)
        elif t == "state":
            A = set(listing(re.search(r"A = (\{[^}]*\})", q["en"])[1])); B = set(listing(re.search(r"B = (\{[^}]*\})", q["en"])[1]))
            S = {"A": A, "B": B}
            def truth(st):
                if m := re.fullmatch(r"(\d+) ∈ ([AB])", st): return int(m[1]) in S[m[2]]
                if m := re.fullmatch(r"(\d+) ∉ ([AB])", st): return int(m[1]) not in S[m[2]]
                if m := re.fullmatch(r"(\{[\d, ]+\}) ⊂ ([AB])", st): return set(listing(m[1])) <= S[m[2]]
                if m := re.fullmatch(r"#\(A ([∪∩]) B\) = (\d+)", st): return len(A | B if m[1] == "∪" else A & B) == int(m[2])
                raise AssertionError("statement " + st)
            assert truth(a) and not any(truth(o) for o in w)
        elif t == "list":
            r = q["frame"]
            if m := re.fullmatch(r"factors of (\d+)", r): n = int(m[1]); exp = [x for x in range(1, n + 1) if n % x == 0]
            elif m := re.fullmatch(r"prime numbers less than (\d+)", r): exp = [x for x in range(int(m[1])) if is_prime(x)]
            elif m := re.fullmatch(r"multiples of (\d+) less than (\d+)", r): exp = [x for x in range(1, int(m[2])) if x % int(m[1]) == 0]
            elif m := re.fullmatch(r"square numbers less than (\d+)", r): exp = [x for x in range(1, int(m[1])) if int(round(x ** .5)) ** 2 == x]
            assert listing(a) == exp, (r, a); assert all(listing(o) != exp for o in w)
        elif t == "shade":
            n = d["n"]; shaded = {reg_of_bits(int(g), n) for g in re.findall(r'<g data-r="(\d)">', q["html"])}
            assert parse(a, n) == shaded, (a, shaded); assert all(parse(o, n) != shaded for o in w)
            assert q["html"].count("<circle") >= n
        elif t == "where":
            names = {"A and B (A ∩ B)": (1, 1), "A only": (1, 0), "B only": (0, 1), "Outside both": (0, 0)}
            v = parse(q["frame"], 2); assert v == {names[a]}; assert all(v != {names[o]} for o in w)
        elif t == "law":
            n = 3; v = parse(q["frame"], n); assert parse(a, n) == v; assert all(parse(o, n) != v for o in w)
        elif t == "read2":
            v = nums(q["html"]); A = v[1] + v[3]; B = v[2] + v[3]; T = sum(v.values()); e = q["en"]
            exp = (v[1] if "only?" in e else A if "(#A)" in e else A + v[2] if "#(A ∪ B)" in e else v[0] if "neither" in e
                   else v[1] + v[2] if "exactly one" in e else T if "in total" in e else v[2] if "#(B \\ A)" in e else None)
            assert exp is not None and int(a) == exp, (e, a, exp)
        elif t == "read3":
            v = nums(q["html"]); bits = lambda g: bin(g).count("1"); e = q["en"]
            exp = (v[4] if "only?" in e else sum(v[g] for g in v if bits(g) == 2) if "exactly two" in e else sum(v[g] for g in v if bits(g) >= 2) if "at least two" in e
                   else v[3] if "but not" in e else sum(v[g] for g in v if g & 2) if "(#B)" in e else v[0] if "none of the three" in e else None)
            assert exp is not None and int(a) == exp, (e, a, exp)
            labels = re.findall(r'fill="#2E7D57"[^>]*>([^<]+)<', q["html"]); assert e.startswith(f"A = {labels[0]}, B = {labels[1]}, C = {labels[2]}.")
        elif t == "x":
            T, A, B, N = map(int, re.search(r"There are (\d+) students in a class\. (\d+) .*?, (\d+) .*? and (\d+) do neither", q["en"]).groups())
            x = A + B + N - T; assert int(a) == x and 0 < x < min(A, B)
            v = nums(q["html"]); assert v[3] == "x" and v[1] == f"{A}−x" and v[2] == f"{B}−x" and int(v[0]) == N, v
        elif t == "word":
            e = q["en"]
            if "How many do both" in e:
                T, A, B, N = map(int, re.search(r"survey of (\d+) people, (\d+) .*? and (\d+) .*?\. (\d+) do neither", e).groups()); exp = A + B - (T - N)
            else:
                T, A, B, BO = map(int, re.search(r"class of (\d+), (\d+) .*?, (\d+) .*? and (\d+) do both", e).groups()); exp = T - (A + B - BO)
            assert int(a) == exp and exp >= 0, (e, a, exp)
        else: raise AssertionError("unknown type " + t)
        if t in ("read2", "read3", "x", "word"): assert all(int(o) >= 0 for o in w) and all(o.isdigit() for o in w + [a])
    except Exception as ex:
        probs += 1
        if probs <= 15: print("PROBLEM", t, repr(ex)[:200], "|", q["en"][:140], q["frame"], "→", a, w)
print(len(qs), "questions checked,", probs, "problems")
