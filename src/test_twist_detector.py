#!/usr/bin/env python3
"""Independent checker for Twist Detector (JC English Order 11, short stories). It re-derives every answer with its own rules + spaCy:
- story part: its own lexicons — climax = opens with a sudden-moment phrase, ending = opens with an ending phrase,
  problem = a trouble word, setting = a time word; every line must hit exactly ONE of the four
- order: lines 2-4 sorted by that part (problem → climax → ending)
- twist: an ending is a twist when it has a reveal phrase (turned out / realised / all along / was really / had been),
  is not a dream, and shares a content lemma (spaCy noun/verb/adjective, not a name) with exactly ONE line of the story;
  the "random" ending reveals but links to no line; the plain ending has no reveal phrase
- clue line: the one story line the twist links to
- opening: weak openers by its own WEAK list; hook kind = dialogue (opens with a quote) / mystery (mystery words, ?) / action (action verbs) — exactly one
- setting: its own clue-word lexicon per place; a line must hit exactly one place and no wrong option may be hit
Usage: N=400 node src/test_twist_detector.js twist-detector.html > /tmp/td.jsonl && python3 src/test_twist_detector.py /tmp/td.jsonl twist-detector.html
       python3 src/test_twist_detector.py - <page or data.json>   (data pass only)"""
import sys, json, re, html as H
import spacy
nlp = spacy.load("en_core_web_sm")
_memo = {}
def doc(s):
    if s not in _memo: _memo[s] = nlp(s)
    return _memo[s]

TIMEW = re.compile(r"\b(morning|afternoon|evening|night|dawn|dusk|midnight|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday|"
                   r"January|February|March|April|June|July|August|September|October|November|December|summer|winter|autumn|spring|Christmas|Halloween|Easter)\b")
PROB = re.compile(r"\b(lost|missing|gone|locked|stuck|broke|broken|couldn't|wouldn't|no sign of|forg[oe]t\w*|ruined|trapped|losing|injured|missed|stealing)\b", re.I)
CLIM = re.compile(r"^(Suddenly|Just then|At that moment|All at once|Without warning|Out of nowhere)\b")
ENDO = re.compile(r"^(In the end|At last|Finally|From that day on|Ever since|By the time)\b")
def parts(s):
    h = []
    if CLIM.search(s): h.append("cl")
    if ENDO.search(s): h.append("en")
    if PROB.search(s): h.append("pr")
    if TIMEW.search(s): h.append("se")
    return h
def part(s):
    h = parts(s); return h[0] if len(h) == 1 else None
LAB = {"se": "🏠 Setting", "pr": "⚔️ Problem", "cl": "💥 Climax", "en": "🏁 Ending"}

REVEAL = re.compile(r"\b(turned out|realised|all along|was really|had been)\b", re.I)
DREAM = re.compile(r"\bdream\b", re.I)
SKIP = {"be", "have", "do", "get", "make", "go", "come", "say", "keep", "take", "turn", "realise", "one", "thing", "way", "time"}
def content(s):
    return {t.lemma_.lower() for t in doc(s) if t.pos_ in ("NOUN", "VERB", "ADJ") and not t.is_stop and t.is_alpha and not t.is_title and t.lemma_.lower() not in SKIP}  # title-case = names (Aisling, Dad) — never a clue
def linked(end, lines):
    c = content(end); return [i for i, l in enumerate(lines) if c & content(l)]
def kind(end, lines):
    if DREAM.search(end): return "dream"
    if not REVEAL.search(end): return "plain"
    L = linked(end, lines)
    return "twist" if len(L) == 1 else "random" if not L else "unclear"

WEAK = re.compile(r"^(This is a story about|My story is about|Once upon a time|Hi, I'm going to tell you)\b")
MYST = re.compile(r"(\?|\b(nobody|no one|never|strange|secret|mystery|vanished|why)\b)", re.I)
ACT = re.compile(r"\b(dived|slammed|grabbed|crashed|ran|leapt|sprinted|raced|jumped|kicked|smashed|burst|threw|scrambled|pedalled)\b")
def hook(s):
    h = []
    if s.startswith("“"): h.append("d")
    else:
        if MYST.search(s): h.append("m")
        if ACT.search(s): h.append("a")
    return h[0] if len(h) == 1 else None
OLAB = {"d": "💬 Dialogue", "a": "🏃 Action", "m": "❓ Mystery"}

PLACEW = {
 "be": r"sand|waves?|seaweed|tide|gulls?|seagulls?|sandcastles?|shells?|towel",
 "sc": r"bell|corridor|lockers?|classroom|homework|teachers?|uniform|whiteboard|canteen|principal",
 "fo": r"trees|leaves|branches|pine|moss|owls?|twigs|mushrooms",
 "ho": r"nurses?|ward|bandages?|doctors?|stretcher|ambulance|beeping machine|plaster",
 "pi": r"crowd|referee|whistle|goalposts|jersey|stands|scoreboard|pitch|cheer",
 "ki": r"oven|kettle|frying pan|toast|fridge|sink|sizzl\w*|cooker|baking",
 "fa": r"tractor|cows?|hay|mud|sheep|barn|wellies|milking|hens",
 "ci": r"traffic|buses|taxis|skyscrapers|crowded street|horns|footpath"}
PLACEW = {k: re.compile(r"\b(" + v + r")\b", re.I) for k, v in PLACEW.items()}
PLAB = {"be": "🏖️ Beach", "sc": "🏫 School", "fo": "🌲 Forest", "ho": "🏥 Hospital", "pi": "🏟️ Match", "ki": "🍳 Kitchen", "fa": "🐄 Farm", "ci": "🏙️ City"}
def places(s): return [k for k, r in PLACEW.items() if r.search(s)]
INV = lambda d: {v: k for k, v in d.items()}

def load(path):
    t = open(path, encoding="utf-8").read()
    if "/*DATA*/" in t: t = t[t.index("/*DATA*/") + 8:t.index("/*END*/")]
    return json.loads(t)

def data_pass(D):
    errs = []
    for T in D["twists"]:
        L = T["lines"]
        if kind(T["twist"], L) != "twist": errs.append(("twist not a twist", T["k"], kind(T["twist"], L), linked(T["twist"], L)))
        elif linked(T["twist"], L)[0] != T["clue"] - 1: errs.append(("clue line", T["k"], linked(T["twist"], L), T["clue"]))
        if kind(T["plain"], L) != "plain": errs.append(("plain", T["k"], T["plain"]))
        if kind(T["random"], L) != "random": errs.append(("random", T["k"], T["random"], linked(T["random"], L)))
    for S in D["stories"]:
        got = [part(l) for l in S["lines"]]
        if got != ["se", "pr", "cl", "en"]: errs.append(("story parts", S["k"], got, [parts(l) for l in S["lines"]]))
    for a, e, s, k in D["open"]:
        if hook(s) != k: errs.append(("hook", s, hook(s), k))
        if WEAK.search(s): errs.append(("hook weak", s))
    for s, k in D["place"]:
        if places(s) != [k]: errs.append(("place", s, places(s), k))
    return errs

def strip(h): return H.unescape(re.sub(r"<[^>]+>", " ", h))
def card_lines(h): return [H.unescape(x) for x in re.findall(r"<p><b>\d</b>(.*?)</p>", h)]

def check(q, D):
    t, a, w = q["data"]["t"], q["answer"], q["wrong"]
    opts = [a] + w
    if len(set(opts)) != len(opts): return "duplicate options"
    if len(w) != q["nw"]: return "wrong count"
    if t == "twist":
        L = card_lines(q["html"])
        ks = {o: kind(o, L) for o in opts}
        tw = [o for o in opts if ks[o] == "twist"]
        if tw != [a]: return f"twist: {ks}"
        if not any(ks[o] == "dream" for o in w): return "no dream option"
    elif t == "clue":
        L = card_lines(q["html"]); end = H.unescape(re.search(r'<i>🎁 The ending</i>(.*?)</p>', q["html"]).group(1))
        ln = linked(end, L)
        if len(ln) != 1 or a != f"Line {ln[0]+1}": return f"clue {ln} {a}"
        if any(o == a for o in w) or not all(re.fullmatch(r"Line [123]", o) for o in opts): return "clue options"
    elif t == "part":
        s = q["data"]["s"]
        if part(s) is None or LAB[part(s)] != a: return f"part {parts(s)}"
        if s not in strip(q["html"]): return "part card"
    elif t == "order":
        lets = re.findall(r'<p class="td-l"><b>([ABC])</b>(.*?)</p>', q["html"])
        rk = {"pr": 1, "cl": 2, "en": 3}
        try: order = sorted(lets, key=lambda x: rk[part(H.unescape(x[1]))])
        except KeyError: return "order unparsed"
        if " → ".join(l for l, _ in order) != a: return "order"
        top = re.search(r'<p class="td-t">🏠 (.*?)</p>', q["html"]).group(1)
        if part(H.unescape(top)) != "se": return "order top"
    elif t == "open":
        good = [o for o in opts if not WEAK.search(o)]
        if good != [a] or hook(a) is None: return "open"
        if q["data"]["about"] not in " ".join(w): return "open weak topic"
    elif t == "hook":
        s = q["data"]["s"]
        if hook(s) is None or OLAB[hook(s)] != a: return f"hook {hook(s)}"
    elif t == "place":
        s = q["data"]["s"]; P = places(s)
        if len(P) != 1 or PLAB[P[0]] != a: return f"place {P}"
        inv = INV(PLAB)
        if any(inv[o] in P for o in w): return "place wrong hit"
    else: return "unknown type " + t
    return None

if __name__ == "__main__":
    if sys.argv[1] == "-":
        e = data_pass(load(sys.argv[2])); [print(x) for x in e]; print("data errors:", len(e)); sys.exit(1 if e else 0)
    D = load(sys.argv[2]); errs = data_pass(D)
    for x in errs: print("DATA", x)
    n = bad = 0; seen = {}
    for line in open(sys.argv[1], encoding="utf-8"):
        q = json.loads(line); n += 1; seen[q["data"]["t"]] = seen.get(q["data"]["t"], 0) + 1
        r = check(q, D)
        if r:
            bad += 1
            if bad <= 15: print("BAD", r, "|", q["answer"], q["wrong"], q["data"])
    print("questions:", n, "types:", seen, "problems:", bad, "data errors:", len(errs))
    sys.exit(1 if bad or errs else 0)
