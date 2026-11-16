"""Recompute every Spin & Predict answer independently from the question TEXT (Python Fraction);
counters, spinner sectors, scale letters, table cells and tree outcomes are read from the picture.
node src/test_spin_and_predict.js > /tmp/sp.json ; python3 src/test_spin_and_predict.py /tmp/sp.json"""
import json, sys, re
from fractions import Fraction as Fr
qs = json.load(open(sys.argv[1])); probs = []
def bad(q, msg): probs.append((q["mk"], msg, q["en"], q["frame"], q["answer"], q["wrong"]))
def isp(n): return n > 1 and all(n % d for d in range(2, int(n ** .5) + 1))
def event(phrase):
    p = phrase
    if p == "an even number": return lambda n: n % 2 == 0
    if p == "an odd number": return lambda n: n % 2 == 1
    if p == "a prime number": return isp
    if p == "a square number": return lambda n: int(round(n ** .5)) ** 2 == n
    m = re.fullmatch(r"a multiple of (\d+)", p)
    if m: k = int(m[1]); return lambda n: n % k == 0
    m = re.fullmatch(r"a number greater than (\d+)", p)
    if m: k = int(m[1]); return lambda n: n > k
    m = re.fullmatch(r"a number less than (\d+)", p)
    if m: k = int(m[1]); return lambda n: n < k
    m = re.fullmatch(r"a factor of (\d+)", p)
    if m: k = int(m[1]); return lambda n: k % n == 0
    m = re.fullmatch(r"an? (\d+)", p)
    if m: k = int(m[1]); return lambda n: n == k
    if p == "a whole number from 1 to 6": return lambda n: 1 <= n <= 6
    raise ValueError(p)
def val(s):
    s = s.replace("−", "-")
    if s.endswith("%"): return Fr(s[:-1]) / 100
    return Fr(s)
def bag(text):
    m = re.search(r"bag (?:has|of) (.+?) counters", text); parts = re.split(r", | and ", m[1]); c = {}
    for x in parts:
        n, col = x.split(" "); c[col] = int(n)
    return c
def event_prob(e):
    m = re.fullmatch(r"getting (heads|tails) when you toss a fair coin", e)
    if m: return Fr(1, 2)
    m = re.fullmatch(r"rolling (.+) on a fair six-sided die", e)
    if m: f = event(m[1]); return Fr(sum(f(n) for n in range(1, 7)), 6)
    m = re.fullmatch(r"picking (.+) from cards numbered 1 to (\d+)", e)
    if m: f = event(m[1]); N = int(m[2]); return Fr(sum(f(n) for n in range(1, N + 1)), N)
    m = re.fullmatch(r"picking a (.+?) counter from a bag of (.+) counters", e)
    if m:
        c = bag("bag of " + m[2] + " counters"); N = sum(c.values())
        want = m[1].split(" or "); return Fr(sum(c.get(w, 0) for w in want), N)
    raise ValueError(e)
def words(p): return "Impossible" if p == 0 else "Certain" if p == 1 else "Even chance" if p == Fr(1, 2) else "Unlikely" if p < Fr(1, 2) else "Likely"
THING = {"toss a coin": ["H", "T"], "roll a die": list("123456"), "spin a spinner with 3 equal sectors (R, B, G)": list("RBG"),
         "spin a spinner numbered 1 to 4": list("1234"), "spin a spinner with 2 equal sectors (R, B)": list("RB"), "spin a spinner numbered 1 to 3": list("123")}
def table(html):
    op = re.search(r'data-op="([^"]+)"', html)[1]
    rows = re.findall(r"<tr>(.*?)</tr>", html); cols = [int(x) for x in re.findall(r"<th[^>]*>(\d+)</th>", rows[0])]
    cells = {}
    for r in rows[1:]:
        a = int(re.search(r"<th[^>]*>(\d+)</th>", r)[1]); tds = re.findall(r"<td[^>]*>([^<]+)</td>", r)
        assert len(tds) == len(cols)
        for b, t in zip(cols, tds):
            true = a + b if op == "+" else a * b
            if t != "?": assert int(t) == true, ("cell", a, b, t)
            cells[(a, b)] = (true, t == "?")
    return op, cells
TREE = {"you toss a fair coin twice": ("HT", "HT"), "you toss a fair coin, then spin a fair spinner with 3 equal sectors (R, B, G)": ("HT", "RBG"),
        "you spin a fair spinner with 3 equal sectors (R, B, G), then toss a fair coin": ("RBG", "HT"),
        "you toss a fair coin, then spin a fair spinner numbered 1 to 4": ("HT", "1234"),
        "you spin spinner A (2 equal sectors: R, B), then spinner B (3 equal sectors: 1, 2, 3)": ("RB", "123")}
for q in qs:
    en, fr, a, w, h, mk = q["en"], q["frame"], q["answer"], q["wrong"], q["html"], q["mk"]
    alltxt = " ".join([en, fr, a, q["why"], q["review"]] + w)
    if re.search(r"NaN|undefined|Infinity|null", alltxt): bad(q, "bad text")
    if len(w) != 3 or len(set(w + [a])) != 4: bad(q, "options"); continue
    try:
        exp = None
        if mk == "qWord":
            exp = words(event_prob(fr[0].lower() + fr[1:-1]))
        elif mk == "qLetter":
            e = re.fullmatch(r"Which letter on the scale shows the probability of (.+)\?", en)[1]; p = event_prob(e)
            lets = {l: (float(x) - 30) / 260 for x, l in re.findall(r'class="lt" data-x="([\d.]+)"[^>]*>([A-D])<', h)}
            near = [l for l, v in lets.items() if abs(v - float(p)) < 0.01]
            assert len(near) == 1, lets; exp = near[0]
            xs = sorted(lets.values()); assert all(xs[i + 1] - xs[i] >= 0.11 for i in range(3)), "letters too close"
        elif mk == "qCant":
            outs = [o for o in [a] + w if not (0 <= val(o) <= 1)]; assert outs == [a], outs; continue
        elif mk == "qMost":
            most = "MOST" in en; vs = {o: val(o) for o in [a] + w}; assert len(set(vs.values())) == 4
            exp = (max if most else min)(vs, key=vs.get)
        elif mk == "qCoinSpin":
            sec = re.findall(r'<path data-c="(\w+)"', h); n = int(re.search(r"has (\d+) equal sectors", en)[1]); assert len(sec) == n
            m = re.search(r"lands on (a colour that is NOT )?(\w+)\?", en); k = sec.count(m[2])
            exp = Fr(n - k if m[1] else k, n)
        elif mk == "qDie":
            m = re.fullmatch(r"You roll a fair six-sided die\. What is the probability of (NOT )?rolling (.+)\?", en)
            k = sum(event(m[2])(n) for n in range(1, 7)); exp = Fr(6 - k if m[1] else k, 6)
        elif mk == "qCards":
            m = re.fullmatch(r"Cards numbered 1 to (\d+) are shuffled and one is picked at random\. What is the probability that it shows (.+)\?", en)
            N = int(m[1]); exp = Fr(sum(event(m[2])(n) for n in range(1, N + 1)), N)
        elif mk == "qBag":
            c = bag(en); pic = re.findall(r'<circle data-c="(\w+)"', h)
            assert {k.lower(): pic.count(k) for k in set(pic)} == c, ("picture", c)
            N = sum(c.values()); m = re.search(r"probability that it is (NOT )?(\w+)(?: or (\w+))?\?", en)
            k = c[m[2]] + (c[m[3]] if m[3] else 0); exp = Fr(N - k if m[1] else k, N)
        elif mk == "qLetters":
            m = re.search(r"word (\w+) is written.*shows (a vowel|the letter (\w))", en); wd = m[1]
            k = sum(ch in "AEIOU" for ch in wd) if m[2] == "a vowel" else wd.count(m[3]); exp = Fr(k, len(wd))
        elif mk == "qHowMany":
            m = re.search(r"has (\d+) counters\. The probability of picking a \w+ one is (\d+)/(\d+)", en)
            exp = int(m[1]) * Fr(int(m[2]), int(m[3])); assert exp.denominator == 1
        elif mk == "qNot":
            m = re.search(r"is (\d+/\d+|[\d.]+)\. What is the probability", en); exp = 1 - val(m[1])
            if "/" not in m[1]:
                for o in [a] + w: assert 0 < val(o) < 1
        elif mk == "qCount":
            if "coins" in en: k = 2 if "two coins" in en else 3; exp = 2 ** k
            elif "two dice" in en: exp = 36
            else:
                m = re.fullmatch(r"You (.+) and (.+)\. How many outcomes are in the sample space\?", en); exp = len(THING[m[1]]) * len(THING[m[2]])
        elif mk == "qFull":
            if "two coins" in en: S = {"HH", "HT", "TH", "TT"}
            else:
                m = re.fullmatch(r"You (.+), then (.+)\. Which is the full sample space\?", en); S = {x + y for x in THING[m[1]] for y in THING[m[2]]}
            ok = [o for o in [a] + w if set(o.strip("{}").split(", ")) == S and len(o.strip("{}").split(", ")) == len(S)]
            assert ok == [a], ok; continue
        elif mk == "qMissing":
            m = re.match(r"You (.+), then (.+)\. \w+ lists", en); S = {x + y for x in THING[m[1]] for y in THING[m[2]]}
            listed = fr.split(", "); assert len(set(listed)) == len(listed) and set(listed) < S
            miss = S - set(listed); assert len(miss) == 1; exp = miss.pop()
        elif mk in ("qFill", "qWays", "qTableP"):
            op, cells = table(h); vals = [v for v, _ in cells.values()]
            assert ("added" in en) == (op == "+")
            if "two dice" in en: assert len(cells) == 36
            else: n = int(re.search(r"numbered 1 to (\d)", en)[1]); assert len(cells) == n * 6
            if mk == "qFill": hid = [v for v, hh in cells.values() if hh]; assert len(hid) == 1; exp = hid[0]
            elif mk == "qWays": exp = vals.count(int(re.search(r" (\d+)\?$", en)[1]))
            else:
                m = re.search(r"probability that (.+)\?$", en)[1]; N = len(vals)
                if m == "both dice show the same number": k = sum(1 for (x, y) in cells if x == y)
                elif m.endswith("an even number"): k = sum(v % 2 == 0 for v in vals)
                else:
                    mm = re.fullmatch(r"the (total|product) is (greater than |less than )?(\d+)", m); t = int(mm[3])
                    k = sum((v > t) if mm[2] == "greater than " else (v < t) if mm[2] == "less than " else (v == t) for v in vals)
                exp = Fr(k, N)
        elif mk == "qTree":
            m = re.match(r"The tree diagram shows what can happen when (.+?)\. (.+)$", en); A, B = TREE[m[1]]
            S = [x + y for x in A for y in B]; oc = re.findall(r'class="oc"[^>]*>(\w+)<', h); assert oc == S, (oc, S)
            rest = m[2]
            if rest == "How many outcomes are there?": exp = len(S)
            else:
                mm = re.fullmatch(r"What is the probability of getting (\w\w)\?", rest)
                if mm: exp = Fr(S.count(mm[1]), len(S))
                else:
                    mm = re.fullmatch(r"What is the probability of getting (at least one head|exactly one head|no heads)\?", rest)
                    if mm: f = {"at least one head": lambda s: s.count("H") >= 1, "exactly one head": lambda s: s.count("H") == 1, "no heads": lambda s: "H" not in s}[mm[1]]; exp = Fr(sum(map(f, S)), len(S))
                    else:
                        mm = re.fullmatch(r"What is the probability that .+ (?:shows|lands on) (\w)\?", rest); exp = Fr(sum(s[-1] == mm[1] for s in S), len(S))
        else:
            bad(q, "no checker"); continue
        if isinstance(exp, Fr):
            assert 0 <= exp <= 1 or mk == "qHowMany"
            if mk == "qHowMany": assert a == str(exp.numerator)
            else:
                sa = "0" if exp == 0 else "1" if exp == 1 else f"{exp.numerator}/{exp.denominator}"
                if mk == "qNot" and "/" not in en.split("is ")[1]: assert val(a) == exp, (a, exp)
                else: assert a == sa, (a, sa)
                for o in w:
                    assert val(o) != exp, ("wrong equals answer", o)
                    assert 0 <= val(o) <= 1, ("out of range", o)
        elif isinstance(exp, int): assert a == str(exp), (a, exp); assert all(int(o) != exp and int(o) >= 0 for o in w)
        else: assert a == exp, (a, exp); assert exp not in w
    except Exception as ex:
        bad(q, repr(ex))
from collections import Counter
print(len(qs), "questions,", len(probs), "problems")
print(Counter(p[0] for p in probs))
for p in probs[:12]: print(p)
