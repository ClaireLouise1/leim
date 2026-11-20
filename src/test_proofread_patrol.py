#!/usr/bin/env python3
"""Independent checker for Proofread Patrol (JC English Order 26, Editing & redrafting: proofreading your own work).
It does not trust the game's answers: every planted slip {wrong>right} is judged again with rules from outside the game.
  judge()  works out what kind of slip a pair is and whether the fix is right in THIS sentence:
    cw  both words in one of Spell Strike's mix-up groups (there/their/they're, to/too, of/have, then/than …):
        Spell Strike checker's own context rule (spaCy) must pick the fix
    gr  irregular verbs (saw/seen, did/done, went/gone …): Tense Trap checker's irr_form (have/has/had before the gap → participle)
        agreement (is/are, was/were, has/have): Tense Trap checker's number() of the subject
        pronouns (I/me, he/him …): Tense Trap checker's role() (subject or object)
        fewer/less: spaCy tags the noun after the gap: NNS (can count) → fewer, NN → less
        who/whom: after a preposition → whom; else the word after the gap: a verb → who, a pronoun / name / noun → whom
    sp  anything else: the fix must be a dictionary word (pyspellchecker), the slip must NOT be one, edit distance 1-3
  The corrected sentence / passage must then pass a spell check (every lower-case word in the dictionary).
  patrol  answer = the slip; the 3 other buttons are other words of the same sentence; the slip appears once only
  count   answer = the number of {…} marks in the passage ("None" for 0)
  few / who  the rules above
  brk     an option is right only if ONE pair of brackets, or ONE pair of dashes, holds exactly the extra information
          and taking it out leaves the sentence; the answer must pass, every wrong option must fail
Usage: N=400 node src/test_proofread_patrol.js proofread-patrol.html > /tmp/pp.jsonl && python3 src/test_proofread_patrol.py /tmp/pp.jsonl proofread-patrol.html
       python3 src/test_proofread_patrol.py - <page or json>   (data pass only)"""
import sys, os, json, re
SRC = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, SRC)
import test_tense_trap as TT
# Spell Strike's checker runs its checks at import time, so take only its rule section (everything before "adding endings")
_ss = open(os.path.join(SRC, "test_spell_strike.py"), encoding="utf-8").read()
_ss = _ss[_ss.index("import sys"):_ss.index("# ---------- adding endings")]
SS = {}; exec(_ss, SS)
known, dist, GROUPS, rule = SS["known"], SS["dist"], SS["GROUPS"], SS["rule"]
nlp = TT.nlp

AGREE = [("is", "are"), ("was", "were"), ("has", "have")]          # singular first
SUBJF, OBJF = set(TT.SUBJ.values()), set(TT.OBJ.values())
PAIRS = {TT.SUBJ[k]: TT.OBJ[k] for k in TT.SUBJ}; PAIRS.update({v: k for k, v in PAIRS.items()})
# mix-up groups whose words have no other everyday job (have / were / to / no / are have many), so the rule can judge a decoy
DECOY_GROUPS = {"there", "your", "then", "quiet", "lose", "accept", "affect", "effects", "weather"}
PREP = {"to", "with", "for", "from", "of", "by", "about", "beside", "behind"}

def gap_doc(s, w):
    i = s.index("___"); d = nlp(s[:i] + w + s[i + 3:])
    return d, [t for t in d if t.idx >= i + len(w)], [t for t in d if t.idx + len(t.text) <= i]

def fewer_less(s):
    d, after, _ = gap_doc(s, "fewer")
    for t in after:
        if t.pos_ == "NOUN": return "fewer" if t.tag_ == "NNS" else "less" if t.tag_ == "NN" else None
    return None

def who_whom(s):
    d, after, before = gap_doc(s, "who")
    if before and before[-1].lower_ in PREP: return "whom"
    if not after: return None
    t = after[0]
    if t.pos_ in ("VERB", "AUX"): return "who"
    if t.pos_ in ("PRON", "PROPN", "DET", "NOUN"): return "whom"
    return None

def judge(s, wrong, right):
    """s has ___ where the slip is. Returns (kind, error message or None)."""
    w, r = wrong.lower(), right.lower()
    if w == r: return "?", "slip and fix are the same word"
    for g, ws in GROUPS.items():
        if w in ws and r in ws:
            want = rule(g, s)
            return "cw", None if want == r else f"mix-up rule says {want!r}, not {r!r}"
    for base, forms in TT.IRR.items():
        fs = set(forms) | {base}
        if w in fs and r in fs:
            ans = TT.irr_form(s, base)[0]
            return "gr", None if ans == r else f"irregular verb rule says {ans!r}"
    for sg, pl in AGREE:
        if {w, r} == {sg, pl}:
            n = TT.number(s)
            want = sg if n == "s" else pl if n == "p" else None
            return "gr", None if want == r else f"agreement rule says {want!r}"
    if PAIRS.get(right) == wrong or PAIRS.get(r) == w:
        ro = TT.role(s); want_subj = right in SUBJF or r == "i"
        ok = (ro == "subj") == want_subj and ro in ("subj", "obj")
        return "gr", None if ok else f"pronoun role is {ro!r}"
    if {w, r} == {"fewer", "less"}:
        want = fewer_less(s); return "gr", None if want == r else f"fewer/less rule says {want!r}"
    if {w, r} == {"who", "whom"}:
        want = who_whom(s); return "gr", None if want == r else f"who/whom rule says {want!r}"
    if not known(r): return "sp", f"fix {right!r} isn't a dictionary word"
    if known(w): return "sp", f"slip {wrong!r} is a real word and no rule covers the pair"
    if not 1 <= dist(w, r) <= 3: return "sp", f"{wrong!r} isn't a near miss of {right!r}"
    return "sp", None

MARK = re.compile(r"\{([^>{}]+)>([^{}]+)\}")
def fixed(t): return MARK.sub(lambda m: m.group(2), t)
def shown(t): return MARK.sub(lambda m: m.group(1), t)
def words(t): return re.findall(r"[A-Za-z][A-Za-z']*", t)
def spell_errors(t):
    return [x for x in words(t) if x[0].islower() and not known(x) and not known(x.replace("'", ""))
            and not (x.endswith("'s") and known(x[:-2])) and not (x.endswith("n't") and known(x[:-3]))]

def sentences(t): return [x for x in re.split(r"(?<=[.?!])\s+", t) if x]
def marks_in(t):
    """[(sentence with ___ at the mark and every other mark fixed, wrong, right)]"""
    out = []
    for sn in sentences(t):
        for m in MARK.finditer(sn):
            g = fixed(sn[:m.start()]) + "___" + fixed(sn[m.end():])
            out.append((g, m.group(1), m.group(2)))
    return out

def brk_parts(s):
    m = re.search(r" \[([^\]]+)\]", s); return s[:m.start()] + s[m.end():], m.group(1)
def brk_ok(opt, s):
    base, extra = brk_parts(s)
    if opt.count("(") == 1 and opt.count(")") == 1 and "–" not in opt:
        a, b = opt.index("("), opt.index(")")
        if b < a: return False
        inside, out = opt[a + 1:b], (opt[:a].rstrip() + " " + opt[b + 1:].lstrip()).strip()
    elif opt.count(" – ") == 2 and "(" not in opt and ")" not in opt:
        p = opt.split(" – "); inside, out = p[1], p[0] + " " + p[2]
    elif opt.count(", ") == 2 and not re.search(r"[()–]", opt):     # a pair of commas does the same job: never offer it as wrong
        p = opt.split(", "); inside, out = p[1], p[0] + " " + p[2]
    else: return False
    return inside == extra and out == base

def data_pass(D):
    e = []
    for s, k, tip in D["spot"]:
        ms = list(MARK.finditer(s))
        if len(ms) != 1: e.append(f"spot: needs exactly one slip: {s!r}"); continue
        (g, w, r), = marks_in(s)
        kind, err = judge(g, w, r)
        if err: e.append(f"spot: {w}>{r}: {err}: {s!r}")
        if kind != k: e.append(f"spot: kind is {kind}, data says {k}: {s!r}")
        se = spell_errors(fixed(s))
        if se: e.append(f"spot: spelling in the fixed sentence {se}: {s!r}")
        ws = words(shown(s))
        if ws.count(w) != 1: e.append(f"spot: slip {w!r} appears {ws.count(w)} times: {s!r}")
        if s.startswith("{"): e.append(f"spot: slip can't be the first word: {s!r}")
        if len(set(x for x in ws[1:] if x.lower() not in ("a", "an", "the") and x != w)) < 3: e.append(f"spot: too few other words: {s!r}")
        if not tip: e.append(f"spot: no tip: {s!r}")
    for k, t in D["pass"]:
        for g, w, r in marks_in(t):
            kind, err = judge(g, w, r)
            if err: e.append(f"pass {k}: {w}>{r}: {err}")
        se = spell_errors(fixed(t))
        if se: e.append(f"pass {k}: spelling in the fixed passage {se}")
        if len(MARK.findall(t)) > 3: e.append(f"pass {k}: more than 3 slips")
    for s, a in D["few"]:
        if fewer_less(s) != a: e.append(f"few: rule says {fewer_less(s)!r}, data {a!r}: {s!r}")
    for s, a in D["who"]:
        if who_whom(s) != a: e.append(f"who: rule says {who_whom(s)!r}, data {a!r}: {s!r}")
    for s in D["brk"]:
        base, extra = brk_parts(s)
        se = spell_errors(base + " " + extra)
        if se: e.append(f"brk: spelling {se}: {s!r}")
        if s.index("[") < 4 or s.endswith("].") : e.append(f"brk: extra info must sit mid-sentence: {s!r}")
    return e

def load(path):
    s = open(path, encoding="utf-8").read()
    if path.endswith(".json"): return json.loads(s)
    return json.loads(s[s.index("/*DATA*/") + 8:s.index("/*END*/")])

def strip(h): return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", h).replace("&nbsp;", " ").replace("&amp;", "&")).strip()
COUNT = {0: "None", 1: "1 slip", 2: "2 slips", 3: "3 slips"}

def check(q, D):
    e = []; d = q["data"]; t = d.get("t"); a = q["answer"]; W = q["wrong"]; nw = q.get("nw") or 3
    if len(W) != nw or len(set(W)) != nw: e.append("wrong-option count")
    if a in W: e.append("answer among wrong options")
    if not q.get("why"): e.append("no why")
    if t == "patrol":
        s = d["s"]; (g, w, r), = marks_in(s)
        if a != w: e.append(f"answer {a!r} isn't the slip {w!r}")
        if shown(s) not in strip(q["html"]): e.append("card doesn't show the sentence with the slip")
        ws = words(shown(s))
        for x in W:
            if x not in ws[1:]: e.append(f"option {x!r} isn't a later word of the sentence")
            if x == w: e.append("slip offered twice")
            for gname, gw in GROUPS.items():      # a mix-up word offered as a decoy must be RIGHT where it stands
                if gname in DECOY_GROUPS and x.lower() in gw:
                    fx = fixed(s); i = re.search(r"\b%s\b" % re.escape(x), fx).start()
                    if rule(gname, fx[:i] + "___" + fx[i + len(x):]) != x.lower(): e.append(f"decoy {x!r} is itself a slip")
        if r not in q["why"]: e.append("why doesn't name the fix")
    elif t == "count":
        txt = d["text"]; n = len(MARK.findall(txt))
        if a != COUNT[n]: e.append(f"answer {a!r}, passage has {n} slips")
        if shown(txt) not in strip(q["html"]): e.append("card doesn't show the passage with its slips")
        if sorted([a] + W) != sorted(COUNT.values()): e.append("options aren't None / 1 / 2 / 3")
    elif t == "few":
        s = d["s"]; want = fewer_less(s)
        if a != want: e.append(f"fewer/less: answer {a!r}, rule says {want!r}")
        if W != [{"fewer": "less", "less": "fewer"}.get(a)]: e.append("fewer/less options")
    elif t == "who":
        s = d["s"]; want = who_whom(s)
        if a.lower() != want: e.append(f"who/whom: answer {a!r}, rule says {want!r}")
        if [x.lower() for x in W] != [{"who": "whom", "whom": "who"}.get(a.lower())]: e.append("who/whom options")
    elif t == "brk":
        s = d["s"]
        if not brk_ok(a, s): e.append(f"brackets: answer isn't right: {a!r}")
        for x in W:
            if brk_ok(x, s): e.append(f"brackets: wrong option is right too: {x!r}")
            if words(x) != words(s):
                e.append(f"brackets: wrong option changes the words: {x!r}")
    else: e.append(f"unknown type {t}")
    return e

if __name__ == "__main__":
    if sys.argv[1] == "-":
        errs = data_pass(load(sys.argv[2]))
        for x in errs: print("PROBLEM:", x)
        print("data pass:", len(errs), "problems"); sys.exit(1 if errs else 0)
    D = load(sys.argv[2]); errs = data_pass(D); n = 0; bad = 0; longest = [0, 0]
    for x in errs: print("PROBLEM:", x)
    for line in open(sys.argv[1], encoding="utf-8"):
        q = json.loads(line); n += 1
        for x in check(q, D):
            bad += 1
            if bad <= 40: print("PROBLEM:", x, "·", q["data"])
        if q["data"].get("t") == "brk":
            longest[1] += 1; longest[0] += len(q["answer"]) >= max(len(w) for w in q["wrong"])
    print(f"{n} questions, {bad} problems; data pass {len(errs)} problems; brackets answer longest {longest[0]}/{longest[1]}")
    sys.exit(1 if bad or errs else 0)
