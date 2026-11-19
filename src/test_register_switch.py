#!/usr/bin/env python3
"""Independent checker for Register Switch (JC English Order 16, register & tone).
It does not trust the game's answers: it re-derives each one with its own rules.
  - register  Format Fixer's markers (src/test_format_fixer.py inf / form) plus a few extra ones (EXTRA_INF, EXTRA_FORM):
              formal = a formal marker and no informal one; informal = the other way round
  - reader    its own reader lists: FORMAL_R (principal, manager, editor, council …) → formal; INFORMAL_R (friend, Gran,
              brother, chat …) → informal; a situation must hit exactly one list
  - polite    POL markers (please, could you, would you mind, excuse me, sorry, thank you …) vs BLUNT markers
              (an order verb first, "I want", "now", "!", "What?"): polite = POL and no BLUNT; blunt = BLUNT and no POL
  - tone      word lists per tone (cheerful / sad / angry / worried): a line must hit exactly one list
  - slang     the {word} must be an informal marker; no other word of the sentence may be one
Usage: N=400 node src/test_register_switch.js register-switch.html > /tmp/rs.jsonl && python3 src/test_register_switch.py /tmp/rs.jsonl register-switch.html
       python3 src/test_register_switch.py - <page or json>   (data pass only)"""
import sys, os, json, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from test_format_fixer import inf as ff_inf, form as ff_form

REG = {"f": "📨 Formal", "i": "😊 Informal"}
POLL = {"p": "😊 Polite", "b": "🙄 Blunt"}
TONEL = {"ch": "😄 Cheerful", "sa": "😢 Sad", "an": "😠 Angry", "wo": "😟 Worried"}

EXTRA_INF = r"\b(awesome|dodgy|epic|savage|buzzing|gutted|lads|nah|kinda|gotta|dunno|cos|omg|oops|mins|eejit|wanna|gonna)\b"
EXTRA_FORM = [r"\bWould it be possible\b", r"^May I\b", r"\bI am (afraid|sorry|unable|delighted|pleased)\b",
              r"^Good (morning|afternoon|evening)\b", r"\bWe regret\b", r"\bI regret\b"]
def inf(s): return ff_inf(s) + ([EXTRA_INF] if re.search(EXTRA_INF, s, re.I) else [])
def form(s): return ff_form(s) + [p for p in EXTRA_FORM if re.search(p, s)]
def register(s):
    a, b = bool(inf(s)), bool(form(s))
    return "i" if a and not b else "f" if b and not a else None

FORMAL_R = r"\b(principal|manager|editor|council|receptionist|listeners|teacher|librarian|company|assembly|judges)\b"
INFORMAL_R = r"\b(friend|Gran|brother|sister|cousin|chat|mate)\b"
def reader(sit):
    a, b = bool(re.search(FORMAL_R, sit, re.I)), bool(re.search(INFORMAL_R, sit, re.I))
    return "f" if a and not b else "i" if b and not a else None

POL = r"\b(please|could you|could I|would you|would you mind|excuse me|sorry|thank you|do you think|I wonder if|if you don't mind|grateful)\b"
BLUNT = [r"^(Give|Move|Stop|Turn|Get|Hand|Shut|Hurry|Tell|Send|Put|Bring|Take|Pass|Open|Close|Answer|Lend|Sit|Say)\b",
         r"\bI want\b", r"\bnow\b", r"!", r"^What\?"]
def pol(s): return bool(re.search(POL, s, re.I))
def blunt(s): return [p for p in BLUNT if re.search(p, s)]
def manner(s):
    a, b = pol(s), bool(blunt(s))
    return "p" if a and not b else "b" if b and not a else None

TONES = {"ch": r"\b(brilliant|wonderful|delighted|thrilled|fantastic|lovely|hooray|yay|can't wait|best day|so happy|amazing|great news)\b",
         "sa": r"\b(miss|missed|missing|lonely|tears|cried|crying|heartbroken|empty|goodbye|never see|sadly|alone)\b",
         "an": r"\b(furious|sick of|fed up|unacceptable|how dare|ridiculous|disgrace|livid|slammed|never again|outrageous)\b",
         "wo": r"\b(worried|what if|afraid|nervous|anxious|scared|hope nothing|keep thinking|unsure)\b"}
def tones(s): return [k for k, p in TONES.items() if re.search(p, s, re.I)]

def slang_word(s):
    m = re.findall(r"\{(\w+)\}", s); return m[0] if len(m) == 1 else None
def words(s): return re.findall(r"[A-Za-z']+", s.replace("{", "").replace("}", ""))

def load(path):
    s = open(path, encoding="utf-8").read()
    if path.endswith(".json"): return json.loads(s)
    return json.loads(s[s.index("/*DATA*/") + 8:s.index("/*END*/")])

def data_pass(D):
    e = []
    for fs, isit, fl, il in D["switch"]:
        if reader(fs) != "f": e.append(f"switch: formal situation reads {reader(fs)}: {fs!r}")
        if reader(isit) != "i": e.append(f"switch: informal situation reads {reader(isit)}: {isit!r}")
        if register(fl) != "f": e.append(f"switch: formal line reads {register(fl)}: {fl!r} inf={inf(fl)} form={form(fl)}")
        if register(il) != "i": e.append(f"switch: informal line reads {register(il)}: {il!r} inf={inf(il)} form={form(il)}")
    for s, k in D["pol"]:
        if manner(s) != k: e.append(f"pol: {s!r} reads {manner(s)}, tagged {k} (pol={pol(s)}, blunt={blunt(s)})")
    for b, a, w in D["mkpol"]:
        if manner(b) != "b": e.append(f"mkpol: prompt not blunt {b!r}")
        if manner(a) != "p": e.append(f"mkpol: answer not polite {a!r} (blunt={blunt(a)})")
        for x in w:
            if not blunt(x): e.append(f"mkpol: wrong option not blunt {x!r}")
        if len(set(w + [a])) != 4: e.append(f"mkpol: duplicates {b!r}")
    for s, k in D["tone"]:
        if tones(s) != [k]: e.append(f"tone: {s!r} hits {tones(s)}, tagged {k}")
    for s in D["slang"]:
        w = slang_word(s)
        if not w or not inf(w): e.append(f"slang: {s!r} word {w!r} is not slang")
        rest = s.replace("{" + str(w) + "}", "")
        if inf(rest): e.append(f"slang: other informal marker in {s!r}: {inf(rest)}")
        if len([x for x in words(rest) if len(x) >= 4]) < 3: e.append(f"slang: too few other words {s!r}")
    return e

def check(q, D):
    t, a, w, d = q["data"]["t"], q["answer"], q["wrong"], q["data"]
    e = []
    if len(w) != q["nw"] or len(set(w)) != len(w) or a in w: e.append("option count/duplicates")
    if t == "switch":
        need = reader(d["s"])
        if need is None: e.append("reader unclear")
        if register(a) != need: e.append(f"answer register {register(a)} for a {need} reader")
        for x in w:
            if register(x) not in ("f", "i") or register(x) == need: e.append(f"wrong option {x!r} fits the reader")
        if d["s"] not in q["html"]: e.append("situation not shown")
        it = [x for x in D["switch"] if d["s"] in (x[0], x[1])]
        if len(it) != 1 or {a} | set(w) != {it[0][2], it[0][3]}: e.append("options are not the same message in two registers")
    elif t == "pol":
        k = manner(d["s"])
        if POLL.get(k) != a: e.append(f"manner {k}")
        if set(w) != set(POLL.values()) - {a}: e.append("wrong set")
    elif t == "mkpol":
        if manner(d["s"]) != "b": e.append("prompt not blunt")
        if manner(a) != "p": e.append("answer not polite")
        for x in w:
            if not blunt(x): e.append(f"wrong option polite {x!r}")
    elif t == "tone":
        k = tones(d["s"])
        if len(k) != 1 or TONEL[k[0]] != a: e.append(f"tone {k}")
        if set(w) != set(TONEL.values()) - {a}: e.append("wrong set")
    elif t == "slang":
        ws = words(d["s"])
        for x in [a] + w:
            if x not in ws: e.append(f"option {x!r} not in the sentence")
        if not inf(a): e.append(f"answer {a!r} not slang")
        for x in w:
            if inf(x): e.append(f"wrong option {x!r} is slang")
        if "{" in q["html"] or a not in q["html"]: e.append("sentence card")
    else: e.append("unknown type")
    return e

if __name__ == "__main__":
    src = sys.argv[2] if len(sys.argv) > 2 else "register-switch.html"
    D = load(src); errs = data_pass(D)
    for x in errs: print("DATA", x)
    n = bad = 0; seen = {}; longest = [0, 0]
    if sys.argv[1] != "-":
        for line in open(sys.argv[1], encoding="utf-8"):
            q = json.loads(line); n += 1; e = check(q, D)
            seen[q["data"]["t"]] = seen.get(q["data"]["t"], 0) + 1
            if q["data"]["t"] in ("switch", "mkpol"):
                longest[1] += 1; longest[0] += len(q["answer"]) > max(len(x) for x in q["wrong"])
            if e:
                bad += 1
                if bad <= 15: print("BAD", q["mode"], q["data"].get("s"), q["answer"], e)
    print(f"data problems: {len(errs)} · questions: {n} · problems: {bad} · types: {seen}" + (f" · answer longest {100*longest[0]//max(1,longest[1])}%" if longest[1] else ""))
    sys.exit(1 if errs or bad or (sys.argv[1] != "-" and n < 100) else 0)
