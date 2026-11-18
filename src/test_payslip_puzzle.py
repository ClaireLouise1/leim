#!/usr/bin/env python3
"""Independent checker for Payslip Puzzle (Money 2: income tax, net pay & compound interest).
Reads every question's TEXT (and the payslip / interest-table / working-steps pictures), works the
answer out again with exact Fractions and checks the game's answer and wrong options.
Usage: N=400 node src/test_payslip_puzzle.js > /tmp/pp.json ; python3 src/test_payslip_puzzle.py /tmp/pp.json"""
import json, re, sys
from fractions import Fraction as F
from collections import Counter

M = r"€([\d,]+\.\d\d)"
def m(s):
    return F(s.replace("−", "-").replace("€", "").replace(",", ""))
def money_opt(o):
    assert re.fullmatch(r"€\d{1,3}(,\d{3})*\.\d\d", o), "bad money format: " + o
    return m(o)
def pct_opt(o):
    assert re.fullmatch(r"\d+(\.\d{1,2})?%", o), "bad % format: " + o
    return F(o[:-1])
def P(s): return F(s)  # a rate like "2.5"
def cent(x): return F(round(x * 100), 100)

problems = Counter(); examples = {}; count = Counter()
def bad(q, msg):
    problems[msg] += 1
    examples.setdefault(msg, (q["mk"], q["en"], q["answer"], q["wrong"]))

def numeric(q, true, kind="money"):
    conv = money_opt if kind == "money" else pct_opt
    try:
        a = conv(q["answer"]); ws = [conv(w) for w in q["wrong"]]
    except AssertionError as e:
        return bad(q, str(e)[:40])
    if a != true: bad(q, "WRONG ANSWER")
    if len(q["wrong"]) != 3: bad(q, "not 3 wrong options")
    vals = [a] + ws
    if len(set(vals)) != len(vals): bad(q, "duplicate value among options")
    if any(w <= 0 for w in ws): bad(q, "wrong option ≤ 0")

def choice(q, is_true):
    opts = [q["answer"]] + q["wrong"]
    t = [o for o in opts if is_true(o)]
    if t != [q["answer"]]: bad(q, "CHOICE: not exactly the answer is right")
    if len(q["wrong"]) < 3: bad(q, "too few wrong options")
    if len(set(opts)) != len(opts): bad(q, "duplicate option")

def grow(a, r): return a * (100 + r) / 100

def check(q):
    en = q["en"]; html = q["html"] or ""
    txt = en + " " + q["answer"] + " " + " ".join(q["wrong"]) + " " + (q["why"] or "")
    for junk in ("NaN", "undefined", "Infinity", "null", "€-", "+ −", "−−"):
        if junk in txt: bad(q, "junk text " + junk)
    if re.search(r"€[\d,]+\.\d{3,}|€[\d,]+\.\d(?!\d)", txt): bad(q, "money not to 2 decimal places")

    r = re.fullmatch(r"(\S+) works as a [a-z ]+ for ([\d.]+) hours a week at " + M + r" an hour\. What is \1's gross pay for the week\?", en)
    if r: count["hours"] += 1; return numeric(q, F(r[2]) * m(r[3]))
    r = re.fullmatch(r"(\S+) earns " + M + r" an hour for a basic (\d+)-hour week, and (time-and-a-half|double time) for overtime\. This week \1 works (\d+) hours\. What is the gross pay\?", en)
    if r:
        rate, b, h = m(r[2]), int(r[3]), int(r[5]); k = F(3, 2) if r[4] == "time-and-a-half" else 2
        if h <= b: bad(q, "no overtime")
        count["overtime"] += 1; return numeric(q, b * rate + (h - b) * rate * k)
    r = re.fullmatch(r"\S+ earns " + M + r" gross a (week|month|year)[^.]*\. What is (the gross pay for the year(?: \(52 weeks\))?|that a month|that a week \(52 weeks\))\?", en)
    if r:
        a, per, ask = m(r[1]), r[2], r[3]
        if per == "week" and "year" in ask: t = a * 52
        elif per == "month" and "year" in ask: t = a * 12
        elif per == "year" and "month" in ask: t = a / 12
        elif per == "year" and "week" in ask: t = a / 52
        else: return bad(q, "year question not understood")
        if t != cent(t): bad(q, "year answer not whole cents")
        count["year"] += 1; return numeric(q, t)
    if en.startswith("Here is ") and "payslip" in en:
        rows = re.findall(r'<tr[^>]*data-k="([^"]+)"[^>]*><td>[^<]+</td><td[^>]*>(?:− )?(\?|' + M + r')</td></tr>', html)
        if len(rows) < 5 or rows[0][0] != "Gross pay" or rows[-1][0] != "Net pay": return bad(q, "payslip rows")
        vals = [None if v == "?" else m(v[1:] if False else v) for _, v, _x in rows]
        if vals.count(None) != 1: return bad(q, "payslip: not exactly one ?")
        i = vals.index(None)
        g, net, ded = vals[0], vals[-1], vals[1:-1]
        if i == len(vals) - 1:
            if "net pay" not in en: bad(q, "payslip ask mismatch")
            t = g - sum(ded)
        else:
            if rows[i][0] not in en: bad(q, "payslip: asks for a different line")
            t = g - net - sum(d for d in ded if d is not None)
        count["payslip"] += 1; return numeric(q, t)
    r = re.fullmatch(r"(\S+)'s gross income is " + M + r" a year\. \1 pays " + M + r" income tax, " + M + r" USC and " + M + r" PRSI\. What is \1's net income\?", en)
    if r: count["netspec"] += 1; return numeric(q, m(r[2]) - m(r[3]) - m(r[4]) - m(r[5]))
    r = re.fullmatch(r"\S+ has a gross income of " + M + r" a year\. The standard rate of income tax is 20%\. How much is the gross tax\?", en)
    if r: count["grosstax"] += 1; return numeric(q, m(r[1]) * F(20, 100))
    r = re.fullmatch(r"(\S+) earns " + M + r" a year and has a tax credit of " + M + r"\. Income tax is charged at the standard rate of 20%\. How much income tax does \1 pay\?", en)
    if r:
        t = m(r[2]) / 5 - m(r[3])
        if t <= 0: bad(q, "tax ≤ 0")
        count["taxpay"] += 1; return numeric(q, t)
    r = re.fullmatch(r"(\S+) earns " + M + r" a year, with a tax credit of " + M + r" and income tax at 20%\. There are no other deductions\. What is \1's take-home \(net\) pay for the year\?", en)
    if r: count["nettax"] += 1; return numeric(q, m(r[2]) - (m(r[2]) / 5 - m(r[3])))
    if en.startswith("Which of these gives the income tax"):
        count["whichtax"] += 1
        return choice(q, lambda o: o == "20% of the gross income, then take away the tax credit")
    r = re.fullmatch(r"(\S+) pays " + M + r" income tax for the year\. The tax credit is " + M + r" and the standard rate is 20%\. What is \1's gross income\?", en)
    if r: count["backtax"] += 1; return numeric(q, (m(r[2]) + m(r[3])) * 5)
    r = re.fullmatch(r"Higher Level: (\S+) earns " + M + r" a year\. The standard rate cut-off point is " + M + r", the standard rate is 20% and the higher rate is 40%\. \1's tax credits are " + M + r"\. How much income tax does \1 pay\?", en)
    if r:
        G, Cc, T = m(r[2]), m(r[3]), m(r[4])
        if G <= Cc: bad(q, "income below cut-off")
        count["tworates"] += 1; return numeric(q, Cc / 5 + (G - Cc) * F(2, 5) - T)
    r = re.fullmatch(r"Higher Level: (\S+)'s gross pay is " + M + r" a week\. Tax payable is " + M + r" and USC is " + M + r"\. PRSI is ([\d.]+)% of gross pay(?: and (\d+)% of gross pay goes into a pension)?\. What is the net pay\?", en)
    if r:
        g = m(r[2]); t = g - m(r[3]) - m(r[4]) - g * F(r[5]) / 100 - (g * int(r[6]) / 100 if r[6] else 0)
        count["netpct"] += 1; return numeric(q, t)
    r = re.fullmatch(r"(\S+) (?:puts|invests|saves) " + M + r" in a savings account paying ([\d.]+)% compound interest a year\. What is it worth after (\d) years\?", en)
    if r:
        a = m(r[2])
        for _ in range(int(r[4])): a = grow(a, F(r[3]))
        count["ciamount"] += 1; return numeric(q, a)
    r = re.fullmatch(r"(\S+) (?:puts|invests|saves) " + M + r" for (\d) years at ([\d.]+)% compound interest a year\. How much interest does \1 earn altogether\?", en)
    if r:
        a0 = a = m(r[2])
        for _ in range(int(r[3])): a = grow(a, F(r[4]))
        count["ciinterest"] += 1; return numeric(q, a - a0)
    if en.startswith("This table shows"):
        rows = re.findall(r'<tr data-y="(\d)" data-r="([\d.]+)"><td>\d \([\d.]+%\)</td>(.*?)</tr>', html)
        if len(rows) not in (2, 3): return bad(q, "ci table rows")
        grid = [re.findall(r'<td data-k="\d"(?: class="q">\?|>' + M + ')</td>', rw[2]) for rw in rows]
        cells = [[None if c == "" else m(c) for c in g] for g in grid]
        flat = [c for g in cells for c in g]
        if flat.count(None) != 1: return bad(q, "ci table: not exactly one ?")
        # rebuild the table from the first visible start value
        start = cells[0][0]
        if start is None: return bad(q, "ci table hides the principal")
        a = start; true = None
        for (y, rr, _), g in zip(rows, cells):
            I = a * F(rr) / 100; want = [a, I, a + I]
            for j in range(3):
                if g[j] is None: true = want[j]
                elif g[j] != want[j]: bad(q, "ci table visible cell wrong")
            a = a + I
        count["citable"] += 1; return numeric(q, true)
    r = re.fullmatch(r"\S+ invests " + M + r"\. The interest rate is (.+) \(compound\)\. What is the investment worth at the end of year (\d)\?", en)
    if r:
        rs = re.findall(r"([\d.]+)% in year (\d)", r[2])
        if [int(y) for _, y in rs] != list(range(1, int(r[3]) + 1)): bad(q, "rates/years mismatch")
        a = m(r[1])
        for rr, _ in rs: a = grow(a, F(rr))
        count["cirates"] += 1; return numeric(q, a)
    r = re.fullmatch(r"(\S+) borrows " + M + r" at ([\d.]+)% compound interest a year\. At the end of year 1, \1 repays " + M + r"\. How much is owed at the end of year 2\?", en)
    if r:
        rr = F(r[3]); a = grow(m(r[2]), rr) - m(r[4])
        if a <= 0: bad(q, "loan repaid too much")
        count["loan"] += 1; return numeric(q, grow(a, rr))
    r = re.fullmatch(r"Which calculation gives the value of €([\d,]+) after (\d) years at (\d+)% compound interest a year\?", en)
    if r:
        Pv, n, rr = F(r[1].replace(",", "")), int(r[2]), F(r[3])
        true = Pv * ((100 + rr) / 100) ** n
        def ev(o):
            s = o.replace("€", "").replace(",", "")
            mm = re.fullmatch(r"(\d+) × ([\d.]+)([²³]?)(?: × (\d+))?", s)
            if not mm: bad(q, "whichci option unreadable"); return False
            v = F(mm[1]) * F(mm[2]) ** {"": 1, "²": 2, "³": 3}[mm[3]] * (int(mm[4]) if mm[4] else 1)
            return v == true
        count["whichci"] += 1; return choice(q, ev)
    r = re.fullmatch(r"Higher Level: (\S+) invested some money at (\d+)% compound interest a year\. After 2 years it is worth " + M + r"\. How much did \1 invest\?", en)
    if r:
        t = m(r[3]) / ((100 + F(r[2])) / 100) ** 2
        if t != cent(t): bad(q, "principal not whole cents")
        count["backp"] += 1; return numeric(q, t)
    r = re.fullmatch(r"Higher Level: " + M + r" grows to " + M + r" in 2 years at the same compound rate each year\. What is the rate\?", en)
    if r:
        ratio = m(r[2]) / m(r[1]); found = None
        for k in range(1, 10001):  # rates to 0.01%
            rr = F(k, 100)
            if ((100 + rr) / 100) ** 2 == ratio: found = rr; break
        if found is None: return bad(q, "rate not exact")
        count["findrate"] += 1; return numeric(q, found, "pct")
    if "Which line has the first mistake?" in en:
        lines = re.findall(r'<p data-line="(\d)"><b>Line \d:</b> (.*?)</p>', html)
        if len(lines) != 4: return bad(q, "steps lines")
        first = None
        r = re.fullmatch(r"(\S+) earns " + M + r" a year, has a tax credit of " + M + r", pays USC of " + M + r" and income tax at 20%\. Here is .*", en)
        if r:
            G, T, U = m(r[2]), m(r[3]), m(r[4]); prev = None; ok = []
            pats = [r"Gross tax = 20% of " + M + r" = " + M, r"Tax payable = " + M + r" (−|\+) " + M + r" = " + M,
                    r"Deductions = " + M + r" \+ " + M + r" = " + M, r"Net pay = " + M + r" − " + M + r" = " + M]
            vals = []
            for (n_, l), pt in zip(lines, pats):
                mm = re.fullmatch(pt, l)
                if not mm: return bad(q, "tax line unreadable: " + l[:30])
                vals.append(mm)
            g1 = vals[0]; ok.append(m(g1[1]) == G and m(g1[2]) == G / 5)
            g2 = vals[1]; ok.append(m(g2[1]) == m(g1[2]) and g2[2] == "−" and m(g2[3]) == T and m(g2[4]) == m(g2[1]) - T)
            g3 = vals[2]; ok.append(m(g3[1]) == m(g2[4]) and m(g3[2]) == U and m(g3[3]) == m(g3[1]) + U)
            g4 = vals[3]; ok.append(m(g4[1]) == G and m(g4[2]) == m(g3[3]) and m(g4[3]) == G - m(g4[2]))
        else:
            r = re.fullmatch(r"\S+ invests " + M + r" for 3 years at ([\d.]+)% compound interest a year\. Here is .*", en)
            if not r: return bad(q, "line question not understood")
            Pv, rr = m(r[1]), F(r[2]); ok = []; prev = Pv
            for k, (n_, l) in enumerate(lines[:3]):
                mm = re.fullmatch(r"Year " + str(k + 1) + r": " + M + r" × ([\d.]+) = " + M, l)
                if not mm: return bad(q, "ci line unreadable: " + l[:30])
                ok.append(m(mm[1]) == prev and F(mm[2]) == (100 + rr) / 100 and m(mm[3]) == m(mm[1]) * F(mm[2]))
                prev = m(mm[3])
            mm = re.fullmatch(r"Interest = " + M + r" − " + M + r" = " + M, lines[3][1])
            if not mm: return bad(q, "interest line unreadable")
            ok.append(m(mm[1]) == prev and m(mm[2]) == Pv and m(mm[3]) == m(mm[1]) - Pv)
        first = "No mistake" if all(ok) else "Line %d" % (ok.index(False) + 1)
        count["line"] += 1
        return choice(q, lambda o: o == first)
    r = re.fullmatch(r"(\S+) earns " + M + r" a year with a tax credit of " + M + r"\. Income tax is 20%\. \1 says the tax payable is " + M + r"\. What mistake did \1 make\?", en)
    if r:
        G, T, said = m(r[2]), m(r[3]), m(r[4])
        tests = {"Took the tax credit off the income instead of off the tax": (G - T) / 5,
                 "Added the tax credit instead of taking it away": G / 5 + T,
                 "Forgot to take away the tax credit": G / 5}
        count["whywrong-tax"] += 1
        return choice(q, lambda o: tests.get(o) == said)
    r = re.fullmatch(r"(\S+) invests " + M + r" for 3 years at ([\d.]+)% compound interest a year\. \1 says it will be worth " + M + r"\. What mistake did \1 make\?", en)
    if r:
        Pv, rr, said = m(r[2]), F(r[3]), m(r[4])
        a = [Pv]
        for _ in range(3): a.append(grow(a[-1], rr))
        tests = {"Worked out the interest on the first amount every year (simple interest)": Pv + 3 * Pv * rr / 100,
                 "Did one year too few": a[2], "Gave the interest, not the final value": a[3] - Pv}
        if rr == 5: tests["Used the wrong multiplier (5% is × 1.05, not × 1.5)"] = cent(Pv * F(3, 2) ** 3)
        if said == a[3]: bad(q, "the 'mistake' is right")
        count["whywrong-ci"] += 1
        return choice(q, lambda o: tests.get(o) == said)
    bad(q, "UNRECOGNISED QUESTION")

data = json.load(open(sys.argv[1]))
for q in data: check(q)
print(len(data), "questions;", dict(count))
if problems:
    for k, v in problems.most_common():
        print("PROBLEM", v, "×", k, "e.g.", examples[k])
    sys.exit(1)
print("0 problems")
