#!/usr/bin/env python3
"""Independent checker for Coin & Dice Lab (JC Maths Order 26).
node src/test_coin_dice_lab.js > /tmp/cdl.json ; python3 src/test_coin_dice_lab.py /tmp/cdl.json
Every answer is worked out again from the question TEXT (and the table / chart / graph read from the HTML),
with exact Fractions. Written separately from the game's code."""
import sys, json, re, math, html as H
from fractions import Fraction as Fr
from math import prod, factorial

def n(s): return int(s.replace(",", ""))
NUM = r"(\d[\d,]*)"
def fmt_dec(x):
    x = Fr(x)
    for k in range(4):
        v = x * 10 ** k
        if v.denominator == 1:
            v = int(v); s = str(v).rjust(k + 1, "0")
            return s if k == 0 else s[:-k] + "." + s[-k:]
    return None
def parse_val(s, form):
    s = s.strip()
    if form == "pct":
        assert s.endswith("%"), s; return Fr(s[:-1]) / 100
    if form == "frac":
        assert re.fullmatch(r"\d+/\d+|0|1", s), s
        v = Fr(s); assert "/" not in s or (Fr(s).numerator == int(s.split("/")[0])), ("not simplest", s); return v
    assert re.fullmatch(r"\d+(\.\d{1,3})?", s), s; return Fr(s)
def whole(s):
    assert re.fullmatch(r"\d{1,3}(,\d{3})*", s), ("bad whole", s); return n(s)
def form_of(t):
    return "dec" if "as a decimal" in t else "pct" if "as a percentage" in t else "frac" if "fraction in its simplest form" in t else None

EXP = [r"dropped " + NUM + r" times\. It lands point up " + NUM + " times", r"thrown in the air " + NUM + r" times\. It lands on its side " + NUM + " times",
       r"flips a water bottle " + NUM + r" times\. It lands standing up " + NUM + " times", r"takes " + NUM + r" penalties in training and scores " + NUM + " of them",
       r"plants " + NUM + r" sunflower seeds and " + NUM + " of them grow", r"next " + NUM + r" cars to pass the school finds that " + NUM + " of them are red",
       r"makes " + NUM + r" phone cases and " + NUM + " of them have a fault"]
def exp_nk(t):
    for p in EXP:
        m = re.search(p, t)
        if m: return n(m.group(1)), n(m.group(2))
    raise AssertionError("no experiment in " + t)

def table(h):
    heads = re.findall(r'<th[^>]*data-o="([^"]+)"[^>]*>([^<]*)</th>', h)
    cells = re.findall(r'<td[^>]*data-f="([^"]+)"[^>]*>([^<]*)</td>', h)
    assert len(heads) == len(cells) and heads
    out = []
    for (o, ot), (f, ft) in zip(heads, cells):
        assert o == ot
        if f == "?": assert ft == "?"; out.append((o, None))
        else: assert n(ft) == int(f); out.append((o, int(f)))
    return out

def attrs(tag): return dict(re.findall(r'([\w-]+)="([^"]*)"', tag))
def read_bars(svg):
    ticks = [(float(a['data-v']), float(a['y']) - 4) for a in map(attrs, re.findall(r'<text class="yt"[^>]*>', svg))]
    ticks.sort(); v0, y0 = ticks[0]; v1, y1 = ticks[-1]
    assert v0 == 0 and abs(y0 - 180) < .11
    step = ticks[1][0] - ticks[0][0]
    for i, (v, y) in enumerate(ticks): assert v == i * step and abs(y - (180 - (y0 - y1) * v / v1)) < .11, "uneven ticks"
    labs = [(float(a['x']), t) for a, t in ((attrs(m.group(1)), m.group(2)) for m in re.finditer(r'(<text class="xl"[^>]*>)([^<]*)</text>', svg))]
    bars = {}
    for t in re.findall(r'<rect class="bar"[^>]*>', svg):
        a = attrs(t); top = float(a['y']); assert abs(top + float(a['height']) - 180) < .11
        val = (180 - top) / (y0 - y1) * v1; vr = round(val / step) * step
        assert abs(val - vr) * (y0 - y1) / v1 < .11, "bar between gridlines"
        cx = float(a['x']) + float(a['width']) / 2; lab = min(labs, key=lambda l: abs(l[0] - cx)); assert abs(lab[0] - cx) < .2
        assert lab[1] == a['data-c']; bars[lab[1]] = int(round(vr))
    return bars
def read_rf(svg):
    pts = []
    for t in re.findall(r'<circle class="rp"[^>]*>', svg):
        a = attrs(t); nn, k = int(a['data-n']), int(a['data-k']); assert 0 <= k <= nn
        assert abs(float(a['cy']) - (190 - 160 * k / nn)) < .06, "point not where its data says"
        pts.append((nn, k))
    assert [p[0] for p in pts] == [10, 20, 50, 100, 200, 500, 1000]
    poly = re.search(r'<polyline[^>]*points="([^"]+)"', svg).group(1).split()
    assert len(poly) == 7
    return pts

def fair_setup(t):
    """returns (P, trials M or None) from the description of a fair experiment"""
    m = re.search(r"fair die is rolled", t)
    evs = {"an even number": lambda x: x % 2 == 0, "a 6": lambda x: x == 6, "a prime number": lambda x: x in (2, 3, 5), "a multiple of 3": lambda x: x % 3 == 0,
           "a number greater than 4": lambda x: x > 4, "a 1 or a 2": lambda x: x <= 2, "a number less than 6": lambda x: x < 6}
    if m:
        ev = next(e for e in sorted(evs, key=len, reverse=True) if re.search(r"(expect|EXPECT) " + re.escape(e) + r"\b", t))
        return Fr(sum(1 for x in range(1, 7) if evs[ev](x)), 6)
    if "fair coin is tossed" in t: assert "heads" in t; return Fr(1, 2)
    m = re.search(r"spinner has (\d+) equal sectors and (\d+) of them are red", t)
    if m: return Fr(int(m.group(2)), int(m.group(1)))
    m = re.search(r"bag has (\d+) red and (\d+) blue counters", t)
    if m: assert "red counter" in t; return Fr(int(m.group(1)), int(m.group(1)) + int(m.group(2)))
    m = re.search(r"Cards (?:are )?numbered 1 to (\d+)", t)
    if m:
        top = int(m.group(1)); ce = {"a multiple of 5": lambda x: x % 5 == 0, "an even number": lambda x: x % 2 == 0, "a number greater than 7": lambda x: x > 7}
        ev = next(e for e in ce if re.search(r"(expect|EXPECT) " + re.escape(e), t))
        return Fr(sum(1 for x in range(1, top + 1) if ce[ev](x)), top)
    raise AssertionError("unknown setup " + t)

TRUE_KEYS = ["more times you repeat an experiment, the better", "Expected frequency = probability × number of trials", "will usually get different results",
             "always between 0 and 1", "expect about 100 sixes"]
FALSE_KEYS = ["more likely to be tails", "you will get exactly 10 sixes", "just as reliable", "it is impossible", "exactly 50 times in 100", "bigger than 1 if"]
def truth(s):
    t = any(k in s for k in TRUE_KEYS); f = any(k in s for k in FALSE_KEYS); assert t != f, s; return t

def check(q):
    t, en, ans, W, h = q['data']['t'], q['en'], q['answer'], q['wrong'], q['html'] or ""
    full = en + " " + (q['frame'] or "")
    opts = [ans] + W
    assert len(W) == 3 and len(set(opts)) == 4, "options"
    for s in [en, q['frame'] or "", q['why'] or "", ans] + W:
        assert "undefined" not in s and "NaN" not in s and "null" not in s, s
        assert not re.search(r"\b(\w+) \1\b", re.sub(r"\d", "", s)), ("doubled word", s)
        assert not re.search(r"(?<![\w.])-\d", s), ("ASCII minus", s)
        assert not re.search(r"(?<![\d.,])1 (times|counters|seeds|tops|bases|toppings|drinks|starters|desserts|sizes|colours)\b", s), ("1 plural", s)
    form = form_of(en)
    # ---------- expected value of the answer ----------
    if t == "rf":
        N, k = exp_nk(en); want = Fr(k, N)
    elif t == "rftable":
        tb = table(h); N = n(re.search(r"rolls a die " + NUM + " times", en).group(1)); assert sum(f for o, f in tb) == N
        ev = re.search(r"relative frequency of (a \d|an even number|an odd number|a number greater than \d|a number less than \d)\?", en).group(1)
        fn = {"an even number": lambda x: x % 2 == 0, "an odd number": lambda x: x % 2 == 1}.get(ev)
        if not fn:
            m = re.match(r"a number (greater|less) than (\d)", ev)
            fn = (lambda x: x > int(m.group(2))) if m and m.group(1) == "greater" else (lambda x: x < int(m.group(2))) if m else (lambda x: x == int(ev[2:]))
        want = Fr(sum(f for o, f in tb if fn(int(o))), N)
    elif t == "missf":
        tb = table(h); N = n(re.search(r"rolls a die " + NUM + " times", en).group(1)); face = re.search(r"roll a (\d)\?", en).group(1)
        miss = [o for o, f in tb if f is None]; assert miss == [face]
        want = N - sum(f for o, f in tb if f is not None); assert want > 0
    elif t == "combine":
        m = re.findall(r"(\d+) times and it lands [a-z ]+? (\d+) times", en); assert len(m) == 2
        (n1, k1), (n2, k2) = [(int(a), int(b)) for a, b in m]; want = Fr(k1 + k2, n1 + n2)
        assert parse_val(ans, form) != (Fr(k1, n1) + Fr(k2, n2)) / 2 or Fr(k1, n1) == Fr(k2, n2)
    elif t in ("chartrf", "chartexp"):
        bars = read_bars(h); N = n(re.search(r"spun " + NUM + " times", en).group(1)); assert sum(bars.values()) == N
        assert re.search(r"Results of " + str(N) + " spins", h)
        col = re.search(r"(?:relative frequency of|land on) (red|blue|green|yellow)", en).group(1).capitalize()
        if t == "chartrf": want = Fr(bars[col], N)
        else:
            M = n(re.search(r"in " + NUM + " spins", en).group(1)); want = Fr(bars[col], N) * M
    elif t == "best":
        rows = re.findall(r"<li[^>]*>(\w+): (\d+) trials, [a-z ]+ (\d+) times</li>", h); assert len(rows) == 4
        mx = max(int(r[1]) for r in rows); assert sum(int(r[1]) == mx for r in rows) == 1
        assert all(int(r[2]) < int(r[1]) for r in rows)
        want = next(r[0] for r in rows if int(r[1]) == mx); assert set(opts) == {r[0] for r in rows} and ans == want; return
    elif t == "expfair":
        P = fair_setup(en); M = n(re.search(NUM + r" times\. How many", en).group(1)); want = P * M
    elif t == "exprf":
        N, k = exp_nk(en); M = n(re.search(NUM, en[en.rindex("How many"):]).group(1))
        want = Fr(k, N) * M
    elif t == "trials":
        P = fair_setup(en.replace("would you expect", "EXPECT")); T = n(re.search(r"on " + NUM + " of them", en).group(1)); want = T / P
    elif t == "bagest":
        m = re.search(r"bag has (\d+) counters.*?puts it back, " + NUM + r" times\. A red counter comes up " + NUM + " times", en)
        want = Fr(n(m.group(3)), n(m.group(2))) * int(m.group(1))
    elif t == "expdec":
        m = re.search(r" is (0\.\d+|\d+%)\.", en); p = Fr(m.group(1)[:-1]) / 100 if m.group(1).endswith("%") else Fr(m.group(1))
        M = n(re.findall(NUM, en.split(". ", 1)[1])[0]); want = p * M
    elif t == "theory":
        P = fair_setup(en); M = n(re.search(NUM + r" times\. ", en).group(1)); want = P * M
    elif t == "menu":
        nums = [n(x) for x in re.findall(r"(\d+) (?:starters|main courses|desserts|sandwiches|drinks)", en)]; assert len(nums) in (2, 3); want = prod(nums)
    elif t == "outfit":
        m = re.search(r"packs (\d+) tops, (\d+) pairs of trousers and (\d+) pairs of runners", en); want = prod(map(int, m.groups()))
    elif t == "hoodie":
        m = re.search(r"(\d+) colours and (\d+) sizes, with or without", en); want = int(m.group(1)) * int(m.group(2)) * 2
    elif t == "code":
        if "dials, each numbered 0 to 9" in en: want = 10 ** int(re.search(r"has (\d) dials", en).group(1))
        elif "one letter (A to Z) followed by one digit" in en: want = 26 * 10
        elif "each digit is from 1 to" in en:
            m = re.search(r"code has (\d) digits and each digit is from 1 to (\d)", en); want = int(m.group(2)) ** int(m.group(1))
        elif "game code" in en:
            lets = {"A, B or C": 3, "A, B, C or D": 4, "A to E": 5}; m = re.search(r"letter from (.+?) followed by (\d) digits", en); want = lets[m.group(1)] * 10 ** int(m.group(2))
        else: assert "red die, a blue die and a green die" in en; want = 6 ** 3
    elif t == "arrange":
        want = factorial(int(re.search(r"can (\d) friends stand in a row", en).group(1)))
    elif t == "medals":
        r = int(re.search(r"(\d+) runners", en).group(1)); want = r * (r - 1) * (r - 2)
    elif t == "letters":
        w = re.search(r"word ([A-Z]+) ", en).group(1); assert len(set(w)) == len(w); want = factorial(len(w))
    elif t == "norep":
        k = int(re.search(r"digits 1 to (\d)", en).group(1))
        want = k ** 3 if "CAN be used more than once" in en else k * (k - 1) * (k - 2); assert ("CAN be used" in en) != ("No digit can be used twice" in en)
    elif t == "misschoice":
        m = re.search(r"offers (\d+) bases and some toppings.*?There are (\d+) different pizzas", en)
        if m: want = Fr(int(m.group(2)), int(m.group(1)))
        else:
            m = re.search(r"make (\d+) different outfits from (\d+) tops, (\d+) pairs of trousers", en); want = Fr(int(m.group(1)), int(m.group(2)) * int(m.group(3)))
        assert want.denominator == 1 and want > 1
    elif t == "whichcalc":
        nums = [int(x) for x in re.findall(r"(\d+) (?:starters|main courses|desserts|colours|sizes|logos|bread types|fillings|sauces)", en)]; assert len(nums) == 3
        target = prod(nums)
        good = [o for o in opts if re.fullmatch(r"\d+( [×+] \d+)+", o) and eval(o.replace("×", "*")) == target]
        assert good == [ans], (good, ans); assert ans == " × ".join(map(str, nums))
        return
    elif t == "lockp":
        d = int(re.search(r"has (\d) dials", en).group(1)); code = re.search(r"code is ([\d ]+?)\?", en).group(1).split(); assert len(code) == d; want = Fr(1, 10 ** d)
    elif t == "mealp":
        m = re.search(r"has (\d+) starters \(one is soup\), (\d+) main courses \(one is pasta\) and (\d+) desserts", en); a, b, c = map(int, m.groups()); want = Fr(c, a * b * c)
    elif t == "rowp":
        k = int(re.match(r"(\d) friends", en).group(1)); want = Fr(factorial(k - 1), factorial(k))
    elif t == "fair":
        tb = table(h); N = n(re.search(r"(?:rolled|spun) " + NUM + " times", en).group(1)); assert sum(f for o, f in tb) == N
        E = Fr(N, len(tb)); assert E.denominator == 1 and re.search(r"expected about " + format(int(E), ",") + " times", en)
        dev = [abs(f - E) / E for o, f in tb]; mx = max(dev)
        top = max(tb, key=lambda x: x[1])
        if mx <= Fr(1, 10): want = "Probably fair: every result is close to " + format(int(E), ",")
        else:
            assert mx >= Fr(1, 2) and top[1] > E, "unclear"; nm = ("a " + top[0]) if top[0].isdigit() else top[0]
            assert sum(1 for o, f in tb if abs(f - E) / E >= Fr(1, 2) and f > E) == 1
            want = "Probably biased: " + nm + " came up far more often than " + format(int(E), ",")
        assert ans == want, (ans, want); return
    elif t in ("true", "false"):
        assert ("TRUE" in en) == (t == "true")
        good = [o for o in opts if truth(o) == (t == "true")]; assert good == [ans], (good, ans); return
    elif t == "better":
        assert "many more" in ans and not any("more times" in w or "many more" in w for w in W); return
    elif t == "rfgraph":
        pts = read_rf(h); last = [Fr(k, nn) for nn, k in pts[-3:]]
        v = Fr(ans); assert all(abs(x - v) <= Fr(3, 100) for x in last), (last, v)
        for w in W: assert abs(Fr(w) - v) >= Fr(1, 10) and 0 < Fr(w) < 1
        assert abs(Fr(pts[0][1], 10) - v) >= Fr(15, 100); return
    else:
        raise AssertionError("unknown type " + t)
    # ---------- compare ----------
    if isinstance(want, Fr) and form:
        assert 0 <= want <= 1
        got = parse_val(ans, form); assert got == want, (ans, want)
        vals = [parse_val(w, form) for w in W]
        assert all(0 <= v <= 1 for v in vals) and want not in vals and len(set(vals)) == 3, ("wrong options", W)
    else:
        want = Fr(want); assert want.denominator == 1 and want >= 0, ("not whole", want)
        assert whole(ans) == want, (ans, want)
        vals = [whole(w) for w in W]; assert want not in vals and len(set(vals)) == 3
    assert ans in (q['why'] or ""), ("why lacks answer", ans, q['why'])

if __name__ == "__main__":
    data = json.load(open(sys.argv[1])); bad = 0; seen = {}
    for q in data:
        try: check(q)
        except Exception as e:
            bad += 1
            if seen.get(q['data']['t'], 0) < 3:
                seen[q['data']['t']] = seen.get(q['data']['t'], 0) + 1; print("FAIL", q['mk'], q['data']['t'], repr(e)[:300], "|", q['en'][:200], "|", q['answer'], q['wrong'])
    print(len(data), "questions,", bad, "problems")
    sys.exit(1 if bad else 0)
