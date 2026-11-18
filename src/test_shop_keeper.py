#!/usr/bin/env python3
"""Independent checker for Shop Keeper (Money 1). Reads every question's TEXT (and the receipt /
meter / sale-tag pictures), works the answer out again with exact Fractions and checks the game's
answer and wrong options.
Usage: N=400 node src/test_shop_keeper.js > /tmp/sk.json ; python3 src/test_shop_keeper.py /tmp/sk.json"""
import json, re, sys
from fractions import Fraction as F
from collections import Counter

M = r"€([\d,]+\.\d\d)"
def m(s):  # "€1,234.50" -> Fraction euros
    s = s.replace("−", "-").replace("€", "").replace(",", "")
    return F(s)
def money_opt(o):
    assert re.fullmatch(r"€\d{1,3}(,\d{3})*\.\d\d", o), "bad money format: " + o
    return m(o)
def pct_opt(o):
    assert re.fullmatch(r"\d+(\.\d)?%", o), "bad % format: " + o
    return F(o[:-1])
def n(s): return F(s.replace(",", ""))
def cent(x): return F(round(x * 100), 100)  # nearest cent (game never needs rounding for answers)

problems = Counter(); examples = {}; count = Counter()
def bad(q, msg):
    problems[msg] += 1
    examples.setdefault(msg, (q["mk"], q["en"], q["answer"], q["wrong"]))

def numeric(q, true, kind):
    """answer must equal `true`; wrong options must differ in value, be positive, no duplicates"""
    conv = money_opt if kind == "money" else pct_opt
    try:
        a = conv(q["answer"]); ws = [conv(w) for w in q["wrong"]]
    except AssertionError as e:
        return bad(q, str(e)[:40])
    if kind == "pct":
        ok = abs(a - true) < F(1, 20)  # % options shown to 1 dp
    else:
        ok = a == true
    if not ok: bad(q, "WRONG ANSWER")
    if len(q["wrong"]) != 3: bad(q, "not 3 wrong options")
    vals = [a] + ws
    if len(set(vals)) != len(vals): bad(q, "duplicate value among options")
    if any(w <= 0 for w in ws): bad(q, "wrong option ≤ 0")
    if kind == "pct" and any(abs(w - true) < F(1, 20) for w in ws): bad(q, "wrong % option equals answer")

def choice(q, opts_true, need=3):
    """opts_true: function option-text -> bool; exactly one option (the answer) must be true"""
    opts = [q["answer"]] + q["wrong"]
    t = [o for o in opts if opts_true(o)]
    if t != [q["answer"]]: bad(q, "CHOICE: not exactly the answer is right")
    if len(q["wrong"]) < need: bad(q, "too few wrong options")
    if len(set(opts)) != len(opts): bad(q, "duplicate option")

def check(q):
    en = q["en"]; html = q["html"] or ""
    txt = en + " " + q["answer"] + " " + " ".join(q["wrong"]) + " " + (q["why"] or "")
    for junk in ("NaN", "undefined", "Infinity", "null", "€-", "+ −"):
        if junk in txt: bad(q, "junk text " + junk)
    if re.search(r"€[\d,]+\.\d{3,}|€[\d,]+\.\d(?!\d)", txt): bad(q, "money not to 2 decimal places")

    if en.startswith("Here is a receipt"):
        rows = re.findall(r'<td>(\d+) × ([^<]+)</td><td>@ ' + M + '</td>', html)
        if not 3 <= len(rows) <= 4: bad(q, "receipt rows")
        tot = sum(int(a) * m(c) for a, _, c in rows)
        if "change" in en:
            note = n(re.search(r"with a €(\d+) note", en).group(1))
            if note <= tot: bad(q, "note too small")
            count["change"] += 1; return numeric(q, note - tot, "money")
        count["receipt"] += 1; return numeric(q, tot, "money")
    r = re.fullmatch(r"Electricity: previous meter reading (\d+), present reading (\d+)\. Each unit costs (\d+)c and the standing charge is " + M + r"\. What is the bill before VAT\?", en)
    if r:
        prev, pres, c, sc = int(r[1]), int(r[2]), int(r[3]), m(r[4])
        digs = re.findall(r'data-row="(\w+)"[^>]*>(\d)<', html)
        rp = "".join(d for w, d in digs if w == "Previous"); rn = "".join(d for w, d in digs if w == "Present")
        if int(rp) != prev or int(rn) != pres: bad(q, "meter picture doesn't match text")
        count["meter"] += 1; return numeric(q, (pres - prev) * F(c, 100) + sc, "money")
    r = re.fullmatch(r"A phone plan costs " + M + r" a month and includes (\d+) (minutes|texts|GB of data)\. Each extra (minute|text|GB) costs (?:" + M + r"|(\d+)c)\. Ríona uses (\d+) (minutes|texts|GB of data) this month\. What is her bill\?", en)
    if r:
        fee, inc, c, used = m(r[1]), int(r[2]), (m(r[5]) if r[5] else F(int(r[6]), 100)), int(r[7])
        if r[3] != r[8] or not r[3].startswith(r[4]): bad(q, "phone units mismatch")
        count["phone"] += 1; return numeric(q, fee + max(0, used - inc) * c, "money")
    r = re.fullmatch(r"(?:A|An) [a-z ]+ charges a (?:call-out|fixed) charge of " + M + r" plus " + M + r" an hour\. The job takes ([\d.]+) hours\. What is the bill( including VAT at 13\.5%\?| \(no VAT\)\?)", en)
    if r:
        b = m(r[1]) + m(r[2]) * F(r[3])
        if "13.5" in r[4]: b = b * F(1135, 1000)
        if b != cent(b): bad(q, "hourly not whole cents")
        count["hourly"] += 1; return numeric(q, b, "money")
    r = re.fullmatch(r"(.+?) " + M + r" before VAT\. VAT is charged at ([\d.]+)%\. (How much is the VAT\?|What is the price including VAT\?)", en)
    if r:
        P, rt = m(r[2]), F(r[3]); v = P * rt / 100
        count["addvat"] += 1; return numeric(q, v if "How much" in r[4] else P + v, "money")
    r = re.fullmatch(r"(.+?) " + M + r" including VAT at ([\d.]+)%\. (How much of that is VAT\?|What was the price before VAT\?)", en)
    if r:
        T, rt = m(r[2]), F(r[3]); P = T / (1 + rt / 100)
        if P != cent(P): bad(q, "backvat not whole cents")
        count["backvat"] += 1; return numeric(q, T - P if "How much" in r[4] else P, "money")
    if en in ("What is the sale price?", "How much do you save in this sale?"):
        r = re.search(r'data-price="' + M + r'" data-pct="(\d+)%"', html)
        r2 = re.search(r'>' + M + r'</text>.*?>(\d+)% OFF<', html)
        if not r or not r2 or r[1] != r2[1] or r[2] != r2[2]: bad(q, "sale tag unreadable")
        P, d = m(r[1]), F(r[2]); off = P * d / 100
        count["sale"] += 1; return numeric(q, P - off if "sale price" in en else off, "money")
    r = re.fullmatch(r"In a sale, a \w+ costs " + M + r" after (\d+)% off\. What was the price before the sale\?", en)
    if r:
        N, d = m(r[1]), F(r[2]); P = N / (1 - d / 100)
        count["was"] += 1; return numeric(q, P, "money")
    r = re.fullmatch(r"Which calculation (adds VAT at ([\d.]+)% to|takes (\d+)% off) a price\?", en)
    if r:
        rt = F(r[2] or r[3]); k = 1 + rt / 100 if r[2] else 1 - rt / 100
        def right(o):
            mm = re.fullmatch(r"([×+−]) ([\d.]+)", o)
            if not mm: bad(q, "unreadable calc option"); return False
            x = F(mm[2]); ok = True
            for P in (F(37), F(100), F(259)):
                got = P * x if mm[1] == "×" else (P + x if mm[1] == "+" else P - x)
                ok = ok and got == P * k
            return ok
        count["which"] += 1; return choice(q, right)
    r = re.fullmatch(r"A shop buys [a-zA-Z -]+ for " + M + r" each and sells them for " + M + r" each\. Profit or loss on each one\?", en)
    if r:
        c, s = m(r[1]), m(r[2])
        def right(o):
            mm = re.fullmatch(r"(Profit|Loss) of " + M, o)
            return bool(mm) and ((mm[1] == "Profit" and s > c and m(mm[2]) == s - c) or (mm[1] == "Loss" and c > s and m(mm[2]) == c - s))
        count["pl"] += 1; return choice(q, right)
    r = re.fullmatch(r"A trader buys [a-zA-Z -]+ for " + M + r" and sells them for " + M + r"\. What is the percentage (profit|loss) on the cost price\?", en)
    if r:
        c, s = m(r[1]), m(r[2])
        if (r[3] == "profit") != (s > c): bad(q, "profit/loss word wrong")
        count["pctpl"] += 1; return numeric(q, abs(s - c) / c * 100, "pct")
    r = re.fullmatch(r"Aidan buys a [a-z -]+ for " + M + r" and sells it at a (profit|loss) of (\d+)% on the cost price\. What does he sell it for\?", en)
    if r:
        c, p = m(r[1]), F(r[3]); s = c * (1 + p / 100) if r[2] == "profit" else c * (1 - p / 100)
        count["sell"] += 1; return numeric(q, s, "money")
    r = re.fullmatch(r"A shop sells [a-zA-Z -]+ for " + M + r" each, making a profit of (\d+)% on the cost price\. What is the cost price\?", en)
    if r:
        s, p = m(r[1]), F(r[2]); c = s / (1 + p / 100)
        if c != cent(c): bad(q, "costback not whole cents")
        count["costback"] += 1; return numeric(q, c, "money")
    r = re.fullmatch(r"Higher Level: A shop buys [a-zA-Z -]+ for " + M + r" and sells them for " + M + r"\. Find the (mark-up|margin)\.", en)
    if r:
        c, s = m(r[1]), m(r[2])
        count["markup"] += 1; return numeric(q, (s - c) / (c if r[3] == "mark-up" else s) * 100, "pct")
    r = re.fullmatch(r"Higher Level: A shop buys [a-zA-Z -]+ for " + M + r" each\. It wants a margin of (\d+)% \(profit as a percentage of the SELLING price\)\. What should the selling price be\?", en)
    if r:
        c, g = m(r[1]), F(r[2]); s = c / (1 - g / 100)
        if (s - c) / s * 100 != g: bad(q, "margin check")
        count["marginback"] += 1; return numeric(q, s, "money")
    def size(t):  # "500 g" / "1.5 litres" / "2 kg" -> grams/ml
        mm = re.fullmatch(r"([\d.]+) (g|ml|kg|litre|litres)", t)
        x = F(mm[1]); return x * 1000 if mm[2] in ("kg", "litre", "litres") else x
    r = re.fullmatch(r"Which pack of ([a-z -]+) is the best value\?", en)
    if r:
        def unit(o):
            mm = re.fullmatch(r"(.+) for " + M, o)
            if mm[1].startswith("1 ") and mm[1].endswith("s"): bad(q, "1 litres")
            return m(mm[2]) / size(mm[1])
        opts = [q["answer"]] + q["wrong"]; us = [unit(o) for o in opts]
        lo = min(us)
        count["best"] += 1; return choice(q, lambda o: unit(o) == lo, need=2)
    r = re.fullmatch(r"A ([\d.]+ (?:g|ml|kg|litres?)) pack of [a-z -]+ costs " + M + r"\. What is the cost of 100 (g|ml)\?", en)
    if r:
        count["per100"] += 1; return numeric(q, m(r[2]) / size(r[1]) * 100, "money")
    r = re.fullmatch(r"You need 3 [a-z ]+ that cost " + M + r' each\. Shop A: "3 for the price of 2"\. Shop B: "(\d+)% off each"\. Which is cheaper\?', en)
    if r:
        P, d = m(r[1]), F(r[2]); A, B = 2 * P, 3 * P * (1 - d / 100)
        def right(o):
            return (o == "3 for the price of 2" and A < B) or (o == f"{r[2]}% off each" and B < A) or (o == "They cost the same" and A == B)
        count["deal"] += 1; return choice(q, right, need=2)
    r = re.fullmatch(r"A ([\d.]+ (?:g|ml|kg|litres?)) pack of [a-z ]+ costs " + M + r" and a ([\d.]+ (?:g|ml|kg|litres?)) pack costs " + M + r"\. How much do you save by buying one big pack instead of (\d+) small packs\?", en)
    if r:
        s1, p1, s2, p2, k = size(r[1]), m(r[2]), size(r[3]), m(r[4]), int(r[5])
        if s2 != k * s1: bad(q, "big pack isn't k small packs")
        count["save"] += 1; return numeric(q, k * p1 - p2, "money")
    r = re.fullmatch(r"(Gym A|Pool A) costs " + M + r" a month for unlimited (?:visits|swims)\. (Gym B|Pool B) costs " + M + r" a month plus " + M + r" per (?:visit|swim)\. Méabh goes (\d+) times a month\. Which is cheaper for her\?", en)
    if r:
        A, B = m(r[2]), m(r[4]) + int(r[6]) * m(r[5])
        def right(o):
            return (o == r[1] and A < B) or (o == r[3] and B < A) or (o == "They cost the same" and A == B)
        count["plans"] += 1; return choice(q, right, need=2)
    bad(q, "UNPARSED question")

data = json.load(open(sys.argv[1]))
for q in data: check(q)
print(len(data), "questions;", dict(count))
if problems:
    for k, v in problems.most_common():
        print(f"{v:5d}  {k}\n       e.g. {examples[k]}")
    sys.exit(1)
print("0 problems")
