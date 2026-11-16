"""Check every Data Detective question independently from the question TEXT and the pictures.
Data types, leading questions, samples, methods and stages are re-classified with Léim's own keyword rules
(written separately from the game's lists), and exactly ONE option must fit. Tables and tally marks are read from the HTML.
node src/test_data_detective.js > /tmp/dd.json ; python3 src/test_data_detective.py /tmp/dd.json"""
import json, sys, re
from fractions import Fraction as Fr
qs = json.load(open(sys.argv[1])); probs = []
def bad(q, msg): probs.append((q["mk"], msg, q["en"], q["frame"], q["answer"], q["wrong"]))
NOM, ORD, DIS, CON = "Categorical nominal", "Categorical ordinal", "Numerical discrete", "Numerical continuous"
def kind(v):  # classify a variable description
    s = v.lower()
    if s.startswith("the number of"): return DIS
    if re.search(r"\b(height|mass|time each|length|temperature|arm span|amount of rain|distance|how far)\b", s): return CON
    if re.search(r"t-shirt size|grade|agrees|star rating|finishing position|year each|spicy|how often|size of coffee", s): return ORD
    return NOM
ORDW = [{"Small", "Medium", "Large"}, {"Mild", "Medium", "Hot"}, {"Never", "Sometimes", "Often", "Always"},
        {"Strongly agree", "Agree", "Disagree", "Strongly disagree"}, {"Distinction", "Higher Merit", "Merit", "Achieved"}]
def kind_vals(vals):
    if all(re.fullmatch(r"\d+", v) for v in vals): return DIS
    if all(re.fullmatch(r"\d+\.\d+ (m|kg|s|°C|cm)", v) for v in vals): return CON
    if any(set(vals) <= w for w in ORDW): return ORD
    if all(re.fullmatch(r"[A-Z][a-z ]+", v) for v in vals): return NOM
    return None
def leading(s): return bool(re.search(r"Don't you|Wouldn't|Isn't|Surely|Everyone knows|Most students love|boring|How much do you love|agree that", s))
def random_sample(s): return bool(re.search(r"random|every 10th|out of a hat with every", s, re.I))
STATM = ["students in my class get", "among 1st years", "students in my year", "families on my road", "students in my class?", "2nd years in my school"]
def stat(s): return any(m in s for m in STATM)
def secondary(s): return bool(re.search(r"Met Éireann|CSO|website|newspaper", s))
def method(s):
    if re.search(r"whether|catch a falling", s): return 2
    if re.search(r"last 10 years|population of each|last 5 years", s): return 3
    if re.search(r"how many cars pass|take the stairs|colours of the cars", s): return 1
    return 0
METH = ["A survey (questionnaire)", "Observation (watch and count)", "An experiment", "Existing data (a website or database)"]
STEPS = ["Pose a question", "Collect the data", "Analyse the data", "Interpret the results"]
def stage(s):
    if re.search(r"decides to find out|writes the question|wonders", s): return 0
    if re.search(r"hands out|times \d+|counts the cars", s): return 1
    if re.search(r"draws a", s): return 2
    if re.search(r"writes: \"Most|says his results", s): return 3
    return None
def table(html):
    rows = re.findall(r"<tr><td[^>]*>(.*?)</td><td[^>]*>(.*?)</td></tr>", html)
    return [(c, None if f == "?" else int(f)) for c, f in rows]
def ranges(opt):
    out = []
    for p in opt.split(" · "):
        m = re.fullmatch(r"(\d+)–(\d+)", p)
        if m: out.append((int(m[1]), int(m[2]))); continue
        m = re.fullmatch(r"(\d+) or more", p)
        if m: out.append((int(m[1]), 10 ** 6)); continue
        return None
    return out
def good_boxes(opt):
    r = ranges(opt)
    return r is not None and all(sum(a <= x <= b for a, b in r) == 1 for x in range(0, 300))
def one(q, pred, label):
    opts = [q["answer"]] + q["wrong"]; fit = [o for o in opts if pred(o)]
    if fit != [q["answer"]]: bad(q, f"{label}: fitting options {fit}")

for q in qs:
    t = q["data"].get("t"); en, fr, a, w = q["en"], q["frame"] or "", q["answer"], q["wrong"]
    blob = " ".join([en, fr, q["why"] or "", q["review"], a] + w)
    if len(w) != 3 or len(set(w)) != 3 or a in w: bad(q, "options"); continue
    if re.search(r"undefined|NaN|null|\[object", blob): bad(q, "junk text")
    if "  " in en or en != en.strip(): bad(q, "spacing")
    if t == "type":
        if set([a] + w) != {NOM, ORD, DIS, CON}: bad(q, "type options")
        if kind(fr.rstrip(".")) != a: bad(q, f"type: mine {kind(fr)}")
    elif t == "which":
        m = re.search(r"gives (.+) data\?", en)[1]
        target = {"NUMERICAL": {DIS, CON}, "CATEGORICAL": {NOM, ORD}}.get(m) or {x for x in (NOM, ORD, DIS, CON) if x.upper() == m}
        if not target: bad(q, "which target"); continue
        one(q, lambda o: kind(o) in target, "which")
    elif t == "values":
        if kind_vals(fr.split(", ")) != a: bad(q, f"values: mine {kind_vals(fr.split(', '))}")
    elif t == "lead":
        want = q["data"]["want"]; one(q, (lambda o: leading(o)) if want == "biased" else (lambda o: not leading(o)), "lead")
        if ("BIASED" in en) != (want == "biased"): bad(q, "lead text")
    elif t == "sample": one(q, random_sample, "sample")
    elif t == "pop":
        N, n = map(int, re.match(r".*? asks (\d+) of the (\d+) ", en).groups()[::-1])
        popQ = "POPULATION" in en
        if popQ and not a.startswith(f"All {N} "): bad(q, "population")
        if not popQ and not (a.startswith(f"The {n} ") and a.endswith("asked")): bad(q, "sample")
        if not N > n: bad(q, "N > n")
    elif t == "statq": one(q, stat, "statq")
    elif t == "source":
        sec = "SECONDARY" in en; one(q, (lambda o: secondary(o)) if sec else (lambda o: not secondary(o)), "source")
    elif t == "census": one(q, lambda o: o.startswith("Asking every one of"), "census")
    elif t == "count":
        c = re.search(r"How many \S+ (?:years )?(?:said|were) (.+)\?$", en)[1]
        if int(a) != fr.split(", ").count(c): bad(q, "count")
        n = int(re.search(r"results for (\d+) ", en)[1])
        if len(fr.split(", ")) != n: bad(q, "count n")
    elif t == "tally":
        if int(a) != len(re.findall(r'class="tk"', q["html"])): bad(q, "tally")
    elif t in ("total", "more", "missing", "frac", "popular"):
        tb = table(q["html"]); fs = [f for c, f in tb]
        if t == "total":
            if int(a) != sum(fs): bad(q, "total")
        elif t == "more":
            m = re.search(r"How many more \S+ (?:years )?(?:said|were) (.+) than (.+)\?$", en); d = dict(tb)
            if int(a) != d[m[1]] - d[m[2]] or int(a) <= 0: bad(q, "more")
        elif t == "missing":
            N = int(re.search(r": (\d+) \w", en)[1])
            if fs.count(None) != 1 or int(a) != N - sum(f for f in fs if f is not None) or int(a) < 1: bad(q, "missing")
        elif t == "frac":
            c = re.search(r"(?:said|were) (.+)\? \(Simplest", en)[1]; p = Fr(dict(tb)[c], sum(fs))
            if a != f"{p.numerator}/{p.denominator}": bad(q, "frac")
            for x in w:
                v = Fr(x)
                if v == p or not 0 < v < 1: bad(q, "frac wrong option")
        else:
            least = "LEAST" in en; target = min(fs) if least else max(fs)
            if fs.count(target) != 1 or dict(tb)[a] != target: bad(q, "popular")
            if sorted([a] + w) != sorted(c for c, f in tb)[:4] and len(tb) == 4: bad(q, "popular options")
    elif t == "class":
        x = int(re.search(r"Which class does (\d+) go in", en)[1])
        one(q, lambda o: (lambda m: int(m[1]) <= x <= int(m[2]))(re.fullmatch(r"(\d+)–(\d+)", o)), "class")
    elif t == "classcount":
        lo, hi = map(int, re.search(r"in the class (\d+)–(\d+)\?", en).groups())
        if int(a) != sum(lo <= int(v) <= hi for v in fr.split(", ")): bad(q, "classcount")
    elif t == "stage":
        s = stage(fr)
        if s is None or STEPS[s] != a: bad(q, f"stage: mine {s}")
    elif t == "next":
        if "FIRST" in en: ok = a == STEPS[0]
        else:
            prev = re.search(r'straight after "(.+)"\?', en)[1]; ok = a == STEPS[STEPS.index(prev) + 1]
        if not ok or set([a] + w) - set(STEPS): bad(q, "next")
    elif t == "method":
        topic = re.search(r"collect data on (.+)\?$", en)[1]
        if METH[method(topic)] != a: bad(q, f"method: mine {METH[method(topic)]}")
    elif t == "boxes": one(q, good_boxes, "boxes")
    else: bad(q, "unknown type " + str(t))

from collections import Counter
print(len(qs), "questions;", dict(Counter(q["mk"] for q in qs)))
print(len(probs), "problems")
for p in probs[:25]: print(p)
sys.exit(1 if probs else 0)
