#!/usr/bin/env python3
"""Independent checker for Story Spine (JC English Order 12, narrative writing). It re-derives every answer with its own rules + spaCy:
- links: two lines are linked when they share a content lemma (spaCy noun / proper noun / verb / adjective, not a stop word,
  not a light verb in SKIP, after the spine phrase is stripped) — names count, so a hero links a story together
- story spine: each spine is 5 lines that open with the 5 spine phrases in order (Once upon a time / Every day / But one day /
  Because of that / Until finally); every line after the first links to another line of its spine; the right option for a gap
  links to the lines shown, and no wrong option links to any of them (the data pass checks this for EVERY pair of spines)
- cut it: the off-track event links to no other line of the plan; every on-track event links to another on-track event
- who's telling: first person = the line has a first-person word (I, me, my, we, us, our …); otherwise third person
- keep it steady: tense from spaCy (the root verb, or its first auxiliary: VBD/VBN = past, VBZ/VBP = present) + person as above;
  the right next line matches the first line in BOTH, and the three wrong ones break tense only / person only / both
- pay it off: the ending that works links to the problem line (line 2); the from-nowhere ending links to no line; the dream ending
  says "dream"; another story's ending (offered as wrong) links to no line of this story (the data pass checks every pair)
Usage: N=400 node src/test_story_spine.js story-spine.html > /tmp/sp.jsonl && python3 src/test_story_spine.py /tmp/sp.jsonl story-spine.html
       python3 src/test_story_spine.py - <page or data.json>   (data pass only)"""
import sys, json, re, html as H
import spacy
nlp = spacy.load("en_core_web_sm")
_memo = {}
def doc(s):
    if s not in _memo: _memo[s] = nlp(s)
    return _memo[s]

STEPS = ["Once upon a time,", "Every day,", "But one day,", "Because of that,", "Until finally,"]
STEP_RE = re.compile(r"^(Once upon a time|Every day|But one day|Because of that|Until finally|In the end),\s*")
SKIP = {"be", "have", "do", "get", "make", "go", "come", "say", "keep", "take", "turn", "one", "thing", "way", "time", "day",
        "end", "lot", "set", "start", "look", "put", "give", "let", "want", "try", "need", "find", "call", "first", "next", "new"}
def body(s): return STEP_RE.sub("", s)
def content(s):
    return {t.lemma_.lower() for t in doc(body(s)) if t.pos_ in ("NOUN", "PROPN", "VERB", "ADJ") and not t.is_stop and t.is_alpha
            and t.lemma_.lower() not in SKIP}
def links(a, b): return bool(content(a) & content(b))
def linked(s, lines): return [i for i, l in enumerate(lines) if links(s, l)]

FIRST = re.compile(r"\b(I|me|my|mine|myself|we|us|our|ours|ourselves)\b", re.I)
def person(s): return 1 if FIRST.search(s) else 3
def tense(s):
    d = doc(s); root = [t for t in d if t.dep_ == "ROOT"][0]
    aux = [c for c in root.children if c.dep_ in ("aux", "auxpass") and c.tag_ in ("VBD", "VBZ", "VBP")]
    tag = aux[0].tag_ if aux else root.tag_
    return "past" if tag in ("VBD", "VBN") else "present" if tag in ("VBZ", "VBP") else None
POVLAB = {1: "🙋 First person (I)", 3: "👀 Third person (he / she)"}
DREAM = re.compile(r"\bdream\b", re.I)

def load(path):
    t = open(path, encoding="utf-8").read()
    if "/*DATA*/" in t: t = t[t.index("/*DATA*/") + 8:t.index("/*END*/")]
    return json.loads(t)

def data_pass(D):
    errs = []
    S = D["spines"]
    for sp in S:
        L = sp["lines"]
        if len(L) != 5 or any(not l.startswith(STEPS[i]) for i, l in enumerate(L)): errs.append(("spine phrases", sp["k"]))
        for i in range(1, 5):
            if not [j for j in range(5) if j != i and links(L[i], L[j])]: errs.append(("spine line unlinked", sp["k"], i + 1, L[i]))
    for a in S:
        for b in S:
            if a is b: continue
            for i in range(1, 5):
                shown = [l for j, l in enumerate(a["lines"]) if j != i]
                if linked(b["lines"][i], shown): errs.append(("spine wrong option links", a["k"], b["k"], i + 1, sorted(content(b["lines"][i]) & set().union(*map(content, shown)))))
    for p in D["plans"]:
        L = p["lines"]
        if linked(p["odd"], L): errs.append(("plan odd links", p["k"], p["odd"], [sorted(content(p["odd"]) & content(l)) for l in L]))
        for i in range(4):
            if not [j for j in range(4) if j != i and links(L[i], L[j])]: errs.append(("plan line unlinked", p["k"], L[i]))
    for s, k in D["pov"]:
        if person(s) != k: errs.append(("pov", s, person(s), k))
    for it in D["steady"]:
        f, r, wt, wp, wb = it
        T, P = tense(f), person(f)
        if None in (T, tense(r), tense(wt), tense(wp), tense(wb)): errs.append(("steady tense unparsed", it, [tense(x) for x in it])); continue
        if (tense(r), person(r)) != (T, P): errs.append(("steady right", f, r))
        if not (tense(wt) != T and person(wt) == P): errs.append(("steady tense-only", f, wt))
        if not (tense(wp) == T and person(wp) != P): errs.append(("steady person-only", f, wp))
        if not (tense(wb) != T and person(wb) != P): errs.append(("steady both", f, wb))
    E = D["ends"]
    for e in E:
        L = e["lines"]
        if not links(e["end"], L[1]): errs.append(("end doesn't link to the problem", e["k"], e["end"]))
        if linked(e["random"], L): errs.append(("random links", e["k"], e["random"]))
        if DREAM.search(e["end"] + e["random"]): errs.append(("dream word", e["k"]))
        for o in E:
            if o is not e and linked(o["end"], L): errs.append(("other end links", e["k"], o["k"], sorted(content(o["end"]) & set().union(*map(content, L)))))
    return errs

def card_lines(h): return [H.unescape(x) for x in re.findall(r"<p><b>[\d?]</b>(.*?)</p>", h)]
def gap(h):
    m = re.search(r'<p class="sp-gap"><b>\?</b>(.*?)</p>', h); return H.unescape(m.group(1)) if m else None

def check(q, D):
    t, a, w = q["data"]["t"], q["answer"], q["wrong"]
    opts = [a] + w
    if len(set(opts)) != len(opts): return "duplicate options"
    if len(w) != q["nw"]: return "wrong count"
    if t == "spine":
        L = card_lines(q["html"]); g = gap(q["html"])
        if len(L) != 4 or g is None: return "spine card"
        step = STEPS.index(g.split(" …")[0].strip() + ",") if (g.split(" …")[0].strip() + ",") in STEPS else None
        if step is None: return "gap step"
        full = {o: STEPS[step] + " " + o.lstrip("…").strip() for o in opts}
        allsteps = {l for sp in D["spines"] for l in sp["lines"] if l.startswith(STEPS[step])}
        if any(full[o] not in allsteps for o in opts): return "option not a line of this step"
        good = [o for o in opts if linked(full[o], L)]
        if good != [a]: return f"spine good={good}"
    elif t == "cut":
        L = card_lines(q["html"])
        if len(L) != 5: return "cut card"
        off = [i for i, l in enumerate(L) if not linked(l, L[:i] + L[i + 1:])]
        if len(off) != 1 or a != f"Line {off[0] + 1}" or off[0] == 0: return f"cut off={off}"
        if not all(re.fullmatch(r"Line [2-5]", o) for o in opts): return "cut options"
    elif t == "pov":
        s = q["data"]["s"]
        if POVLAB[person(s)] != a or set(opts) != set(POVLAB.values()): return "pov"
    elif t == "steady":
        f = q["data"]["s"]; T, P = tense(f), person(f)
        good = [o for o in opts if (tense(o), person(o)) == (T, P)]
        if good != [a]: return f"steady good={good}"
        kinds = sorted(("t" if tense(o) != T else "") + ("p" if person(o) != P else "") for o in w)
        if kinds != ["p", "t", "tp"]: return f"steady kinds {kinds}"
    elif t == "end":
        L = card_lines(q["html"])
        if len(L) != 2: return "end card"
        good = [o for o in opts if not DREAM.search(o) and links(o, L[1])]
        if good != [a]: return f"end good={good}"
        if any(linked(o, L) for o in w): return "end wrong links"
        if not any(DREAM.search(o) for o in w): return "no dream"
    else: return "unknown type " + t
    return None

if __name__ == "__main__":
    if sys.argv[1] == "-":
        e = data_pass(load(sys.argv[2])); [print(x) for x in e]; print("data errors:", len(e)); sys.exit(1 if e else 0)
    D = load(sys.argv[2]); errs = data_pass(D)
    for x in errs: print("DATA", x)
    n = bad = 0; seen = {}; longest = {}
    for line in open(sys.argv[1], encoding="utf-8"):
        q = json.loads(line); n += 1; t = q["data"]["t"]; seen[t] = seen.get(t, 0) + 1
        if t in ("spine", "end", "steady"):
            longest[t] = longest.get(t, 0) + (len(q["answer"]) > max(len(x) for x in q["wrong"]))
        r = check(q, D)
        if r:
            bad += 1
            if bad <= 15: print("BAD", r, "|", q["answer"], q["wrong"], q["data"])
    print("questions:", n, "types:", seen, "answer is the longest option:", {k: f"{v / seen[k]:.0%}" for k, v in longest.items()}, "problems:", bad, "data errors:", len(errs))
    sys.exit(1 if bad or errs else 0)
