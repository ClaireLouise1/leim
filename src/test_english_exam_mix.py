#!/usr/bin/env python3
"""Independent checker for English Exam Mix (Order 32, exam technique). It never trusts the game's answers:
 - timing questions: reads the paper (hours, marks) and the question's marks / minutes from the drawn fact card and
   recomputes with Fractions (time follows the marks: 120 min / 180 marks);
 - command-word questions: reads the question from the card and sorts it by its OWN list of opening command words;
   no other command verb may appear anywhere in it;
 - form questions: finds the form word (article, speech/talk, letter, email, diary, story, review, report) in the task: exactly one;
 - reader questions: the answer must be written in the task, and no wrong option may be.
Usage: N=400 node src/test_english_exam_mix.js english-exam-mix.html > /tmp/xm.jsonl && python3 src/test_english_exam_mix.py /tmp/xm.jsonl english-exam-mix.html
       python3 src/test_english_exam_mix.py - <page>   (data pass only). No spaCy needed."""
import json, re, sys, html as H
from fractions import Fraction as F
from collections import Counter

LAB = {"find": "🔎 Find it in the text", "desc": "📝 Say what it is like", "expl": "💡 Say why or how",
       "comp": "⚖️ Alike and different", "opin": "🙋 Your view + reasons", "sum": "✂️ Main points, short"}
START = [("find", r"(Identify|Name|List|Write down|Pick out|Find)\b"), ("desc", r"Describe\b"), ("expl", r"Explain\b"),
         ("comp", r"(Compare|Contrast)\b"), ("opin", r"(Do you agree|Do you think|Would you|Which\b.*\bdo you think|In your opinion)\b"),
         ("sum", r"(Summarise|Sum up)\b")]
OTHER = r"\b(identify|name|list|write down|pick out|describe|explain|compare|contrast|summarise|sum up|discuss|why)\b"
FORMW = {"article": r"\barticle\b", "speech": r"\b(speech|talk)\b", "letter": r"\bletter\b", "email": r"\be-?mail\b",
         "diary": r"\bdiary\b", "story": r"\bstory\b", "review": r"\breview\b", "report": r"\breport\b"}
FLAB = {"article": "📰 Article", "speech": "🎤 Speech or talk", "letter": "✉️ Letter", "email": "📧 Email",
        "diary": "📔 Diary entry", "story": "📖 Story", "review": "⭐ Review", "report": "📋 Report"}

def text(h): return re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", " ", h))).strip()

def command(q):
    """→ key, or a problem string"""
    hits = [k for k, rx in START if re.match(rx, q)]
    if len(hits) != 1: return None, "opening command words: %s" % hits
    k = hits[0]; m = re.match(dict(START)[k], q)
    rest = q[m.end():]
    o = [w for w in re.findall(OTHER, rest, re.I) if not (k == "expl" and w.lower() == "why")]   # "Explain why" is still explain
    if o: return None, "another command word later: %s" % o
    return k, ""

def form(t):
    hits = [k for k, rx in FORMW.items() if re.search(rx, t, re.I)]
    return hits[0] if len(hits) == 1 else None

def load(path):
    s = open(path, encoding="utf-8").read()
    if path.endswith(".json"): return json.loads(s)
    return json.loads(s[s.index("/*DATA*/") + 8:s.index("/*END*/")])

def data_pass(D):
    P = []
    if D["paper"] != {"min": 120, "marks": 180}: P.append("paper facts changed: %s" % D["paper"])
    seen = set()
    for q, k in D["cmd"]:
        got, why = command(q)
        if got != k: P.append("cmd %r: game says %s, checker %s %s" % (q, k, got, why))
        if q in seen: P.append("cmd twice: " + q)
        seen.add(q)
    c = Counter(k for _, k in D["cmd"])
    if min(c.values()) < 4 or len(c) != 6: P.append("cmd counts %s" % c)
    readers = [r for _, _, r in D["task"] if r]
    for t, k, r in D["task"]:
        if form(t) != k: P.append("task %r: game says %s, checker %s" % (t, k, form(t)))
        if r and r not in t: P.append("reader %r not in task %r" % (r, t))
        for o in readers:
            if o != r and o in t and r: P.append("another reader %r also in task %r" % (o, t))
    if len(set(readers)) != len(readers): P.append("readers repeat")
    return P

def check(q, D):
    P = []; h = text(q["html"]); d = q["data"]; t = d.get("t")
    if len(q["wrong"]) != 3: P.append("wrong count %d" % len(q["wrong"]))
    if q["answer"] in q["wrong"] or len(set(q["wrong"])) != len(q["wrong"]): P.append("answer among wrong / repeats")
    m = re.search(r"Paper: (\d+) hours · (\d+) marks", h)
    if t in ("time", "marks"):
        if not m: return ["no paper line"]
        mins, marks = int(m.group(1)) * 60, int(m.group(2))
        if (mins, marks) != (120, 180): P.append("paper line %s" % m.group(0))
        if t == "time":
            M = int(re.search(r"This question: (\d+) marks", h).group(1)); ans = F(M * mins, marks)
            if ans.denominator != 1: P.append("not whole minutes")
            want = "%d min" % ans; rx = r"^\d+ min$"
        else:
            T = int(re.search(r"spent (\d+) minutes", h).group(1)); ans = F(T * marks, mins)
            if ans.denominator != 1: P.append("not whole marks")
            want = "%d marks" % ans; rx = r"^\d+ marks$"
        if q["answer"] != want: P.append("answer %s, checker %s" % (q["answer"], want))
        for w in q["wrong"]:
            if not re.match(rx, w) or int(w.split()[0]) <= 0: P.append("odd option " + w)
    elif t == "cmd":
        k, why = command(h)
        if not k: P.append(why)
        elif q["answer"] != LAB[k]: P.append("answer %s, checker %s for %r" % (q["answer"], LAB[k], h))
        if any(w not in LAB.values() for w in q["wrong"]): P.append("odd wrong option")
    elif t == "form":
        task = h.replace("✍️ WRITING TASK", "").strip(); k = form(task)
        if not k: P.append("no single form word: " + task)
        elif q["answer"] != FLAB[k]: P.append("answer %s, checker %s" % (q["answer"], FLAB[k]))
        if any(w not in FLAB.values() for w in q["wrong"]): P.append("odd wrong option")
    elif t == "reader":
        task = h.replace("✍️ WRITING TASK", "").strip()
        readers = [r for _, _, r in D["task"] if r]
        if q["answer"] not in task: P.append("answer not in task")
        for w in q["wrong"]:
            if w in task: P.append("wrong option %r is in the task" % w)
            if w not in readers: P.append("odd wrong option " + w)
    else:
        P.append("unknown type %s" % t)
    return P

if __name__ == "__main__":
    D = load(sys.argv[2])
    DP = data_pass(D)
    for p in DP: print("DATA PROBLEM", p)
    if sys.argv[1] == "-":
        print("data pass:", len(DP), "problems"); sys.exit(1 if DP else 0)
    n = bad = 0; types = Counter()
    for line in open(sys.argv[1], encoding="utf-8"):
        q = json.loads(line); n += 1; types[q["data"].get("t")] += 1
        P = check(q, D)
        if P:
            bad += 1
            if bad < 15: print("PROBLEM", q["en"], "|", text(q["html"])[:90], "|", P)
    exp = {"time", "marks", "cmd", "form", "reader"}
    if set(types) != exp: print("PROBLEM types", dict(types)); bad += 1
    print("data problems: %d · questions: %d · problems: %d · types: %s" % (len(DP), n, bad, dict(types)))
    sys.exit(1 if bad or DP or n < 50 else 0)
