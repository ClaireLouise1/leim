#!/usr/bin/env python3
"""Independent checker for Persuasion Power (JC English Order 18, persuasive writing & speeches).
It does not trust the game's answers: it re-derives each one with its own rules (no spaCy needed).
  - techniques  rq    = the line ends with "?"
                three = a list of three: "X, Y and Z" (up to 4 words per item)
                stat  = a number, "per cent" or "half"
                emo   = a word from EMO (innocent, heartbreaking, lonely, abandoned …)
                you   = you / your / yourself
                rep   = a content word (4+ letters, not in STOP) used twice
                a technique line must hit exactly ONE of these
  - back it up  the best reason shares a content word with the claim (simple stem), has evidence (EVID: a number,
                for example / for instance / such as / which means / so that) and no RUDE word; every wrong option
                fails one of those three tests
  - answer back the best reply starts with a counter word (However / But / Yet / On the other hand …), shares a
                content word with the other side's view and has no RUDE word; every wrong option fails one of them
                (an AGREE opener, a RUDE word, or no shared word)
  - call to action  starts with an order verb from IMP (or "Let's") and shares a content word with the topic;
                wrong options are WEAK endings or another topic's call that shares no word with this topic
Usage: N=400 node src/test_persuasion_power.js persuasion-power.html > /tmp/pp.jsonl && python3 src/test_persuasion_power.py /tmp/pp.jsonl persuasion-power.html
       python3 src/test_persuasion_power.py - <page or json>   (data pass only)"""
import sys, json, re

TECH = {"rq": "❓ Rhetorical question", "three": "3️⃣ Rule of three", "stat": "📊 Statistic",
        "emo": "💔 Emotive language", "you": "👉 Direct address", "rep": "🔁 Repetition"}
STOP = set("that with this they their them were very from have after every would before there been also what when where which while about into than then your just only some more most many much such like will should could".split())
EMO = r"\b(innocent|heartbreaking|heartbroken|lonely|abandoned|helpless|frightened|terrified|disgusting|cruel|tragic|devastating|desperate|starving|suffering|shocking|disgraceful|heartless|choked)\b"
W = r"[\w'-]+(?: [\w'-]+){0,3}"
def tech(s):
    k = []
    if s.rstrip().endswith("?"): k.append("rq")
    if re.search(rf"{W}, {W},? and [\w'-]+", s): k.append("three")
    if re.search(r"\d|per cent|\bhalf\b", s, re.I): k.append("stat")
    if re.search(EMO, s, re.I): k.append("emo")
    if re.search(r"\b(you|your|yours|yourself|you're)\b", s, re.I): k.append("you")
    ws = [w for w in re.findall(r"[a-z']+", s.lower()) if len(w) >= 4 and w not in STOP]
    if len(ws) != len(set(ws)): k.append("rep")
    return k

def stem(w):
    w = w.lower().replace("'s", "")
    for suf in ("ing", "ed", "es", "s"):
        if w.endswith(suf) and len(w) - len(suf) >= 3: w = w[:-len(suf)]; break
    return w[:-1] if w.endswith("e") and len(w) > 3 else w
def content(s): return {stem(w) for w in re.findall(r"[A-Za-z']+", s) if len(w) >= 4 and w.lower() not in STOP and w.lower() not in ("some", "people", "argue", "think", "say", "says")}
def shares(a, b): return bool(content(a) & content(b))

EVID = r"\d|€|for example|for instance|such as|which means|that means|so that"
RUDE = r"\b(lazy|idiots?|stupid|clueless|fool|losers?|hopeless|pigs?|boring|weird|pathetic|selfish|waste of space)\b"
COUNTER = r"^(However|But|Yet|On the other hand|Even so|While that may be true)\b"
AGREE = r"^(They are right|That is true|I agree)\b"
IMP = r"^(Let's|Sign|Dust|Leave|Visit|Vote|Join|Pick|Put|Bring|Come|Grab|Fill|Write|Email|Ask|Help|Start|Tell|Switch|Support|Walk)\b"
WEAK = r"(that's all|anyway|I suppose|I guess|don't really know|so yeah)"
def evid(s): return bool(re.search(EVID, s, re.I))
def rude(s): return bool(re.search(RUDE, s, re.I))
def good_reason(claim, s): return shares(claim, s) and evid(s) and not rude(s)
def good_reply(view, s): return bool(re.search(COUNTER, s)) and shares(view, s) and not rude(s)
def good_cta(topic, s): return bool(re.search(IMP, s)) and shares(topic, s) and not re.search(WEAK, s, re.I)

def load(path):
    s = open(path, encoding="utf-8").read()
    if path.endswith(".json"): return json.loads(s)
    return json.loads(s[s.index("/*DATA*/") + 8:s.index("/*END*/")])

def data_pass(D):
    e = []
    for s, k in D["tech"]:
        if tech(s) != [k]: e.append(f"tech: {s!r} hits {tech(s)}, tagged {k}")
    for c, b, w in D["back"]:
        if not good_reason(c, b): e.append(f"back: best reason fails {b!r} (share={shares(c,b)} evid={evid(b)} rude={rude(b)})")
        for x in w:
            if good_reason(c, x): e.append(f"back: wrong option passes {x!r}")
        if not any(rude(x) for x in w) or not any(not shares(c, x) for x in w): e.append(f"back: needs a rude and an off-topic option {c!r}")
    for v, b, w in D["counter"]:
        if not good_reply(v, b): e.append(f"counter: best reply fails {b!r}")
        for x in w:
            if good_reply(v, x): e.append(f"counter: wrong option passes {x!r}")
        if not re.search(AGREE, w[0]) or not rude(w[1]) or shares(v, w[2]): e.append(f"counter: options should be agree / rude / off-topic {v!r}")
    for t, c in D["cta"]:
        if not good_cta(t, c): e.append(f"cta: {c!r} fails for {t!r}")
    return e

def check(q, D):
    t, a, w, d = q["data"]["t"], q["answer"], q["wrong"], q["data"]
    e = []
    if len(w) != q["nw"] or len(set(w)) != len(w) or a in w: e.append("option count/duplicates")
    if t == "tech":
        k = tech(d["s"])
        if len(k) != 1 or TECH[k[0]] != a: e.append(f"technique {k}")
        for x in w:
            if x not in TECH.values(): e.append(f"bad label {x!r}")
        if d["s"] not in q["html"]: e.append("line not shown")
    elif t == "back":
        if not good_reason(d["s"], a): e.append("answer is not a good reason")
        for x in w:
            if good_reason(d["s"], x): e.append(f"wrong option is a good reason {x!r}")
    elif t == "counter":
        if not good_reply(d["s"], a): e.append("answer is not a good reply")
        for x in w:
            if good_reply(d["s"], x): e.append(f"wrong option is a good reply {x!r}")
    elif t == "cta":
        if not good_cta(d["s"], a): e.append("answer is not a call to action for this topic")
        for x in w:
            if good_cta(d["s"], x): e.append(f"wrong option is a call to action for this topic {x!r}")
            if not re.search(WEAK, x, re.I) and not re.search(IMP, x): e.append(f"odd wrong option {x!r}")
    else: e.append("unknown type")
    if t != "tech" and d["s"] not in q["html"]: e.append("prompt not shown")
    return e

if __name__ == "__main__":
    src = sys.argv[2] if len(sys.argv) > 2 else "persuasion-power.html"
    D = load(src); errs = data_pass(D)
    for x in errs: print("DATA", x)
    n = bad = 0; seen = {}; longest = [0, 0]
    if sys.argv[1] != "-":
        for line in open(sys.argv[1], encoding="utf-8"):
            q = json.loads(line); n += 1; e = check(q, D)
            seen[q["data"]["t"]] = seen.get(q["data"]["t"], 0) + 1
            if q["data"]["t"] in ("back", "counter", "cta"):
                longest[1] += 1; longest[0] += len(q["answer"]) > max(len(x) for x in q["wrong"])
            if e:
                bad += 1
                if bad <= 15: print("BAD", q["mode"], q["data"].get("s"), q["answer"], e)
    print(f"data problems: {len(errs)} · questions: {n} · problems: {bad} · types: {seen}" + (f" · answer longest {100*longest[0]//max(1,longest[1])}%" if longest[1] else ""))
    sys.exit(1 if errs or bad or (sys.argv[1] != "-" and n < 100) else 0)
