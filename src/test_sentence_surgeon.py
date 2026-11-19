#!/usr/bin/env python3
"""Independent checker for Sentence Surgeon: re-parses every sentence with spaCy (src/sentence_check.py) and checks each question.
Setup (new session): pip install --break-system-packages spacy + the en_core_web_sm 3.8.0 wheel from github.com/explosion/spacy-models/releases.
Usage: N=400 node src/test_sentence_surgeon.js sentence-surgeon.html > /tmp/ss.jsonl && python3 src/test_sentence_surgeon.py /tmp/ss.jsonl sentence-surgeon.html"""
import sys, json, re, html as H, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sentence_check import kind, structure, stype
LAB = {"✅ Sentence": "sentence", "🧩 Fragment": "fragment", "🚧 Run-on": "runon", "💬 Statement": "st", "❓ Question": "qu", "📢 Command": "cm",
       "😲 Exclamation": "ex", "1️⃣ Simple": "si", "➕ Compound": "co", "🔀 Complex": "cx"}
GROUP = {"surgeon": {"sentence", "fragment", "runon"}, "types": {"st", "qu", "cm", "ex"}, "build": {"si", "co", "cx"}}
COORD = {"but", "so", "or", "and"}
memo = {}
def M(f, s):
    if (f.__name__, s) not in memo: memo[(f.__name__, s)] = f(s)
    return memo[(f.__name__, s)]
def text(h): return H.unescape(re.sub("<[^>]+>", "", h)).strip()
def halves_ok(a, b):
    """both halves of a run-on are complete sentences on their own"""
    return M(kind, a + ".") == "sentence" and M(kind, b[0].upper() + b[1:]) == "sentence"
bad = n = 0; seen = set()
for line in open(sys.argv[1]):
    q = json.loads(line); n += 1; d = q["data"]; t = d["t"]; opts = [q["answer"]] + q["wrong"]
    def fail(msg):
        global bad; bad += 1
        if bad < 30: print("FAIL", msg, "|", q["en"], "|", text(q["html"]), "|", opts)
    need = 2 if t in ("surgeon", "build") else 3
    if len(q["wrong"]) != need: fail("wrong option count")
    if len(set(opts)) != len(opts): fail("duplicate option")
    if any(re.search(r"undefined|NaN|null", o) for o in opts + [q["en"], q["why"], text(q["html"])]): fail("bad text")
    shown = text(q["html"])
    if t in GROUP:
        if {LAB[o] for o in opts} != GROUP[t]: fail("options aren't the full label set")
        want = LAB[q["answer"]]
        if t == "surgeon":
            if want == "runon":
                a, b = d["run"].split("|")
                if shown != a + d["join"] + b: fail("shown text isn't the run-on")
                if not halves_ok(a, b): fail("a half of the run-on isn't a sentence")
                if d["join"] == ", " and M(kind, shown) != "runon": fail("parser doesn't see a run-on")
            else:
                got = M(kind, shown)
                if got != want: fail(f"parser says {got}")
        elif t == "types":
            if M(stype, shown) != want: fail(f"parser says {M(stype, shown)}")
        elif t == "build":
            if M(kind, shown) != "sentence": fail("not a sentence")
            if M(structure, shown) != want: fail(f"parser says {M(structure, shown)}")
        seen.add((t, shown))
    elif t == "fix":
        a, b = d["run"].split("|"); la = a.split()[-1]; fb = b.split()[0]
        if not halves_ok(a, b): fail("half isn't a sentence")
        if q["answer"] != f"{la}. {fb[0].upper()}{fb[1:]}": fail("answer isn't full stop + capital")
        for w in q["wrong"]:
            if re.fullmatch(re.escape(la) + r"\. [A-Z]\S*", w): fail("wrong option is also full stop + capital")
        if (la + ". " + fb) == q["answer"]: fail("lowercase option equals answer")
        if la not in shown or fb not in shown: fail("join words not shown")
        seen.add((t, d["run"]))
    elif t == "join":
        s = d["sent"]
        if "___" not in s: fail("no gap")
        filled = s.replace("___", q["answer"])
        if M(kind, filled) != "sentence": fail("answer doesn't make a sentence: " + filled)
        st = M(structure, filled)
        if q["answer"] in COORD and st not in ("co",) and not s.split()[0].istitle(): pass
        if q["answer"] in COORD and st == "cx": fail("coordinating word but parser sees complex")
        if q["answer"] not in COORD and st == "co": fail("subordinating word but parser sees compound")
        if q["answer"] in COORD and ", " + q["answer"] + " " not in d["rv"]: fail("no comma before " + q["answer"])
        if q["answer"] not in q["why"]: fail("why doesn't name the answer")
        seen.add((t, s))
print(f"{n} questions, {bad} problems, {len(seen)} different items")
if len(sys.argv) > 2:   # full pass over the data block (catches items the random sample missed)
    D = json.loads(open(sys.argv[2], encoding="utf-8").read().split("/*DATA*/")[1].split("/*END*/")[0])
    errs = []
    for s in D["sent"]:
        if M(kind, s) != "sentence": errs.append(("sent", s))
    for s, k in D["frag"]:
        if M(kind, s) != "fragment": errs.append(("frag", s))
    for r in D["run"]:
        a, b = r.split("|")
        if not halves_ok(a, b) or M(kind, a + ", " + b) != "runon" or not b[0].islower(): errs.append(("run", r))
    for k, L in D["types"].items():
        errs += [("type " + k, s) for s in L if M(stype, s) != k]
    for k, L in D["struct"].items():
        errs += [("struct " + k, s) for s in L if M(kind, s) != "sentence" or M(structure, s) != k]
    for s, a, w in D["join"]:
        if a in w or len(set(w)) != 3: errs.append(("join options", s))
        if M(kind, s.replace("___", a)) != "sentence": errs.append(("join", s))
    allt = D["sent"] + [f for f, k in D["frag"]] + [r.replace("|", " ") for r in D["run"]] + sum(D["types"].values(), []) + sum(D["struct"].values(), [])
    if len(set(allt)) != len(allt): errs.append(("duplicate item", ""))
    print("data block:", len(errs), "problems", errs[:10])
    bad += len(errs)
sys.exit(1 if bad else 0)
