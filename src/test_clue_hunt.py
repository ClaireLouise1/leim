#!/usr/bin/env python3
"""Independent checker for Clue Hunt (JC English Order 4, reading for meaning).
It does not trust the game's answers: it re-derives each one from the TEXT with its own rules.
  - Which line proves it?  the clue words must sit in the answer line and in no other line; the claim must not just copy a line.
  - Scan it                the answer must appear in exactly one line, that line must share a content word with the question,
                           and no wrong option may appear in that line.
  - Best title             spaCy lemmas: the answer must link to 2+ lines, every wrong title to at most 1, and fewer than the answer.
  - Feelings               its own clue-word lexicon (below): the answer feeling must be found in the named lines,
                           no other feeling may be found there, and look-alike feelings are never offered as wrong.
  - Fact or opinion        its own list of judgement words: opinions need one, facts must have none.
Setup (new session): pip install --break-system-packages spacy + the en_core_web_sm 3.8.0 wheel.
Usage: N=400 node src/test_clue_hunt.js clue-hunt.html > /tmp/ch.jsonl && python3 src/test_clue_hunt.py /tmp/ch.jsonl clue-hunt.html"""
import sys, json, re, html as H
import spacy
nlp = spacy.load("en_core_web_sm")

FEELING = {   # label -> clue words / phrases that show it (longest match wins; a matched span is used once)
    "😊 Happy": ["grinning", "cried with relief", "jumped on her", "smiled", "cheered", "delighted", "laughed", "made me laugh", "can't wait"],
    "😨 Scared": ["shaking", "trembled", "froze", "heart pounded", "terrified"],
    "😬 Nervous": ["stomach was in knots", "butterflies", "couldn't eat", "bit her nails"],
    "😠 Angry": ["complain", "furious", "slammed", "shouted"],
    "😢 Sad": ["cried", "tears", "sobbed", "heartbroken"],
    "😴 Bored": ["nothing to do", "sighing", "yawned", "ticked slowly"],
    "😳 Embarrassed": ["face went red", "blushed", "wanted the ground to swallow"],
}
CLOSE = {"😨 Scared": {"😬 Nervous"}, "😬 Nervous": {"😨 Scared"}}
JUDGE = ["best", "worst", "boring", "exciting", "should", "ugly", "delicious", "easier", "harder", "amazing", "nicest", "too ",
         "better", "annoying", "lovely", "fun", "i think", "unfair", "brilliant", "awful", "terrible", "beautiful", "great",
         "brave", "stupid", "favourite"]
STOP = {"the", "a", "an", "and", "of", "to", "in", "on", "for", "at", "is", "be", "do", "how", "what", "when", "who", "which",
        "with", "her", "his", "their", "they", "it", "she", "he", "i", "my", "new", "old", "about", "from", "there", "that", "this",
        "long", "often", "many", "much", "until", "get"}
SYN = {"cost": "€", "age": "aged", "date": None}   # question word -> word to look for in the line

def stem(w): return w[:5]
lem_memo = {}
def lemmas(s):
    if s not in lem_memo:
        lem_memo[s] = {stem(t.lemma_.lower()) for t in nlp(s) if t.is_alpha and t.lemma_.lower() not in STOP and not t.is_stop}
    return lem_memo[s]
def feelings(s):
    s = s.lower(); found = set()
    phrases = sorted(((p, f) for f, L in FEELING.items() for p in L), key=lambda x: -len(x[0]))
    for p, f in phrases:
        if p in s: found.add(f); s = s.replace(p, "#")
    return found
def is_opinion(s): return any(j in s.lower() for j in JUDGE)
def text(h): return H.unescape(re.sub("<[^>]+>", " ", h))

D = json.loads(open(sys.argv[2], encoding="utf-8").read().split("/*DATA*/")[1].split("/*END*/")[0]) if len(sys.argv) > 2 else None
FEELMAP = {"happy": "😊 Happy", "scared": "😨 Scared", "nervous": "😬 Nervous", "angry": "😠 Angry", "sad": "😢 Sad",
           "bored": "😴 Bored", "embarrassed": "😳 Embarrassed"}

def check_proof(T, claim, ln, clue):
    e = []
    hits = [i + 1 for i, l in enumerate(T["lines"]) if clue.lower() in l.lower()]
    if hits != [ln]: e.append(f"clue “{clue}” found in lines {hits}, not only line {ln}")
    if any(claim.lower().rstrip(".") in l.lower() for l in T["lines"]): e.append("claim copies a line")
    return e
def fact_line(T, ans):
    return [i + 1 for i, l in enumerate(T["lines"]) if re.search(r"(?<![\w€])" + re.escape(ans.lower()) + r"(?!\w)", l.lower())]
def check_fact(T, q, ans, wrong, ln):
    e = []
    hits = fact_line(T, ans)
    if hits != [ln]: e.append(f"answer “{ans}” in lines {hits}, not only line {ln}"); return e
    line = T["lines"][ln - 1]
    qw = lemmas(re.sub(r"[^\w\s']", " ", q))
    extra = any(SYN.get(w) and SYN[w] in line for w in qw)
    if not (qw & lemmas(line)) and not extra and not re.search(r"how many|how long|how often|when|what time|colour", q.lower()):
        e.append("question shares no word with the answer line")
    for w in wrong:
        if w.lower() == ans.lower(): e.append("wrong = answer")
        if re.search(r"(?<!\w)" + re.escape(w.lower()) + r"(?!\w)", line.lower()): e.append(f"wrong option “{w}” is in the answer line")
    return e
def coverage(T, title): return [i + 1 for i, l in enumerate(T["lines"]) if lemmas(title) & lemmas(l)]
def check_main(T, ans, wrong):
    e = []; a = len(coverage(T, ans))
    if a < 2: e.append(f"best title links to {a} line(s)")
    for w in wrong:
        c = len(coverage(T, w))
        if c > 1 or c >= a: e.append(f"wrong title “{w}” links to {c} lines (answer {a})")
    return e
def check_feel(T, ans, wrong, lines):
    e = []; seg = " ".join(T["lines"][i - 1] for i in lines); f = feelings(seg)
    if ans not in f: e.append(f"lexicon finds {f}, not {ans}")
    for w in wrong:
        if w in f: e.append(f"wrong feeling {w} is also shown")
        if w in CLOSE.get(ans, ()): e.append(f"look-alike {w} offered as wrong")
    return e

bad = n = 0; seen = set()
for raw in open(sys.argv[1]):
    q = json.loads(raw); n += 1; d = q["data"]; t = d["t"]; opts = [q["answer"]] + q["wrong"]
    def fail(msg):
        global bad; bad += 1
        if bad < 30: print("FAIL", t, msg, "|", q["en"], "|", opts)
    if len(q["wrong"]) != (1 if t == "fo" else 3): fail("wrong option count")
    if len(set(o.lower() for o in opts)) != len(opts): fail("duplicate option")
    if any(re.search(r"undefined|NaN|null", o) for o in opts + [q["en"], q["why"], text(q["html"])]): fail("bad text")
    if t == "fo":
        want = "💭 Opinion" if is_opinion(d["s"]) else "📏 Fact"
        if q["answer"] != want: fail(f"rule says {want}")
        if d["s"] not in text(q["html"]): fail("sentence not shown")
        seen.add(d["s"]); continue
    T = D["texts"][d["x"]]
    shown = text(q["html"])
    if not all(l in H.unescape(shown) for l in T["lines"]): fail("text card doesn't show every line")
    if t == "proof":
        if sorted(opts) != ["Line 1", "Line 2", "Line 3", "Line 4"]: fail("options aren't Line 1–4")
        p = [p for p in T["proofs"] if p[0] == d["claim"]][0]
        ln = int(q["answer"].split()[1])
        for m in check_proof(T, d["claim"], ln, p[2]): fail(m)
        if p[2].lower() not in q["why"].lower(): fail("why doesn't quote the clue")
    elif t == "scan":
        f = [f for f in T["facts"] if f[0] == d["q"]][0]
        hits = fact_line(T, q["answer"])
        if len(hits) != 1: fail(f"answer in lines {hits}")
        else:
            for m in check_fact(T, d["q"], q["answer"], q["wrong"], hits[0]): fail(m)
    elif t == "main":
        for m in check_main(T, q["answer"], q["wrong"]): fail(m)
    elif t == "feel":
        f = [f for f in T["feel"] if f[0] == d["q"]][0]
        for m in check_feel(T, q["answer"], q["wrong"], f[3]): fail(m)
    seen.add((t, d["x"], d.get("claim") or d.get("q") or ""))
print(f"{n} questions, {bad} problems, {len(seen)} different items")

if D:   # full pass over the data block
    errs = []
    for x, T in enumerate(D["texts"]):
        if len(T["lines"]) != 4: errs.append((x, "not 4 lines"))
        if len(set(T["main"])) != 4: errs.append((x, "titles repeat"))
        errs += [(x, m) for m in check_main(T, T["main"][0], T["main"][1:])]
        for qq, a, w, ln in T["facts"]:
            if len(set(w)) != 3: errs.append((x, "fact options"))
            errs += [(x, m) for m in check_fact(T, qq, a, w, ln)]
        if len(T["proofs"]) < 2: errs.append((x, "fewer than 2 proofs"))
        for c, ln, clue in T["proofs"]: errs += [(x, m) for m in check_proof(T, c, ln, clue)]
        for qq, k, clues, lines in T["feel"]:
            ans = FEELMAP[k]
            others = [v for v in FEELMAP.values() if v != ans and v not in CLOSE.get(ans, ())]
            errs += [(x, m) for m in check_feel(T, ans, others, lines)]
            for c in clues:
                if not any(c.lower() in T["lines"][i - 1].lower() for i in lines): errs.append((x, f"feel clue “{c}” not in its lines"))
        if not (T["facts"] or T["feel"]): errs.append((x, "nothing to scan"))
    for s in D["fo"]["f"]:
        if is_opinion(s): errs.append(("fact", s))
    for s in D["fo"]["o"]:
        if not is_opinion(s): errs.append(("opinion", s))
    allfo = D["fo"]["f"] + D["fo"]["o"]
    if len(set(allfo)) != len(allfo): errs.append(("duplicate fact/opinion", ""))
    print("data block:", len(errs), "problems", errs[:12])
    bad += len(errs)
sys.exit(1 if bad else 0)
