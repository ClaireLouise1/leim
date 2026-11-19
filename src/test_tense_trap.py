#!/usr/bin/env python3
"""Independent checker for Tense Trap (JC English Order 17, Grammar 2: tenses, agreement & pronouns).
It does not trust the game's answers: it re-derives each one with its own rules.
  - tense   the time cue in the sentence (CUES: yesterday / last / ago → past; every / always / usually / often / never →
            present; tomorrow / next / later / soon → future) decides the tense; each option is put into the gap and
            classified by spaCy (VBD past, VBZ/VBP present, will + verb future, have/has + VBN present perfect).
            The answer must match the cue; no wrong option may. Present answers must agree with the subject
            (he / she / it / a singular noun → -s form).
  - slip    every {verb} is tagged by spaCy in the plain sentence: exactly one present-tense verb (the answer), the rest past
  - agree   its own number rules for the subject: "There ___ X" → the number of X; "and" → plural;
            each / every / everyone / everybody / nobody / somebody / one → singular; "X of Y" → X;
            otherwise spaCy's NN / NNS tag of the head word. Singular verbs end in -s (is, was, has, plays).
  - irr     its own table of irregular verbs (IRR); a have / has / had / be-form within the 3 words before the gap
            → past participle, otherwise past simple; spaCy must tag the filled sentence VBN or VBD to agree
  - pron    the gap is filled with "Sam" and parsed: following "conj" links up, nsubj → subject form (I, he, she, we, they),
            dobj / pobj / dative → object form (me, him, her, us, them)
Usage: N=400 node src/test_tense_trap.js tense-trap.html > /tmp/tt.jsonl && python3 src/test_tense_trap.py /tmp/tt.jsonl tense-trap.html
       python3 src/test_tense_trap.py - <page or json>   (data pass only)"""
import sys, json, re
import spacy
NLP = spacy.load("en_core_web_sm")
_cache = {}
def nlp(s):
    if s not in _cache: _cache[s] = NLP(s)
    return _cache[s]

CUES = {"pa": r"\b(yesterday|last|ago)\b", "pr": r"\b(every|always|usually|often|never)\b", "fu": r"\b(tomorrow|next|later|soon)\b"}
def cue(s):
    k = [t for t, p in CUES.items() if re.search(p, s, re.I)]
    return k[0] if len(k) == 1 else None

def gap_tokens(s, opt):
    """Fill the gap, parse, return (doc, tokens of the option)."""
    i = s.index("___"); filled = s[:i] + opt + s[i + 3:]
    d = nlp(filled); a, b = i, i + len(opt)
    return d, [t for t in d if t.idx >= a and t.idx < b]

def tense_of(s, opt):
    d, toks = gap_tokens(s, opt)
    w = [t.lower_ for t in toks]
    if not toks: return None, d, toks
    if w[0] == "will" and len(toks) == 2 and toks[1].tag_ == "VB": return "fu", d, toks
    if w[0] in ("have", "has") and len(toks) == 2 and toks[1].tag_ == "VBN": return "pp", d, toks
    if len(toks) == 1:
        tg = toks[0].tag_
        if tg == "VBD": return "pa", d, toks
        if tg in ("VBZ", "VBP"): return "pr", d, toks
    return None, d, toks

def third_sing(d, verb):
    subj = [c for c in verb.children if c.dep_ == "nsubj"]
    if not subj: return None
    s = subj[0]
    if s.lower_ in ("he", "she", "it"): return True
    if s.lower_ in ("i", "you", "we", "they"): return False
    if s.tag_ in ("NN", "NNP"): return not any(c.dep_ == "conj" for c in s.children)
    if s.tag_ in ("NNS", "NNPS"): return False
    return None

# ---------- slip ----------
def slip(s):
    """[(verb, spaCy tag, marked-by-the-game?)] for every {verb}; the game marks its answer {*verb}."""
    plain = re.sub(r"[{}*]", "", s); d = nlp(plain); out = []; shift = 0
    for m in re.finditer(r"\{(\*?)([^}]+)\}", s):
        start = m.start() - shift; shift += 2 + len(m.group(1))
        tok = [t for t in d if t.idx == start]
        out.append((m.group(2), tok[0].tag_ if tok else None, bool(m.group(1))))
    return out

# ---------- agree ----------
SING_START = r"^(Each|Every|Everyone|Everybody|Nobody|Somebody|Someone|One|No one|Anybody|Anyone)\b"
def number(s):
    i = s.index("___"); before = s[:i].strip()
    if before == "There":
        d = nlp(s.replace("___", "is"))
        for t in d:
            if t.idx > i and t.pos_ in ("NOUN", "PROPN"): return "s" if t.tag_ in ("NN", "NNP") else "p"
        return None
    if re.search(r"\band\b", before): return "p"
    if re.search(SING_START, before): return "s"
    head = re.split(r"\s+(of|in|on|at)\s+", before)[0]
    d = nlp(head); last = [t for t in d if t.is_alpha][-1]
    if last.lower_ in ("he", "she", "it"): return "s"
    if last.lower_ in ("i", "you", "we", "they"): return "p"
    return "s" if last.tag_ in ("NN", "NNP") else "p" if last.tag_ in ("NNS", "NNPS") else None

# ---------- irregular ----------
IRR = {"go": ("went", "gone"), "see": ("saw", "seen"), "do": ("did", "done"), "come": ("came", "come"),
       "run": ("ran", "run"), "begin": ("began", "begun"), "write": ("wrote", "written"), "eat": ("ate", "eaten"),
       "take": ("took", "taken"), "give": ("gave", "given"), "break": ("broke", "broken"), "drink": ("drank", "drunk"),
       "swim": ("swam", "swum"), "sing": ("sang", "sung"), "ring": ("rang", "rung"), "throw": ("threw", "thrown"),
       "choose": ("chose", "chosen"), "freeze": ("froze", "frozen"), "fall": ("fell", "fallen"), "steal": ("stole", "stolen"),
       "ride": ("rode", "ridden"), "speak": ("spoke", "spoken"), "forget": ("forgot", "forgotten")}
AUX = {"have", "has", "had", "having", "was", "were", "is", "are", "am", "be", "been"}
def irr_form(s, base):
    before = re.findall(r"[A-Za-z'-]+", s[:s.index("___")])[-3:]
    need_pp = any(w.lower() in AUX for w in before)
    ans = IRR[base][1] if need_pp else IRR[base][0]
    d, toks = gap_tokens(s, ans)
    tag = toks[0].tag_ if len(toks) == 1 else None
    return ans, need_pp, tag

# ---------- pronouns ----------
SUBJ = {"i": "I", "he": "he", "she": "she", "we": "we", "they": "they"}
OBJ = {"i": "me", "he": "him", "she": "her", "we": "us", "they": "them"}
def role(s):
    d, toks = gap_tokens(s, "Sam")
    t = toks[0]
    while t.dep_ == "conj": t = t.head
    if t.dep_ in ("nsubj", "nsubjpass"): return "subj"
    if t.dep_ in ("dobj", "pobj", "dative", "iobj", "obj"): return "obj"
    return t.dep_

def load(path):
    s = open(path, encoding="utf-8").read()
    if path.endswith(".json"): return json.loads(s)
    return json.loads(s[s.index("/*DATA*/") + 8:s.index("/*END*/")])

def tense_item(s, ans, wrong):
    e = []; k = cue(s)
    if not k: e.append(f"tense: no single time cue: {s!r}"); return e
    t, d, toks = tense_of(s, ans)
    if t != k: e.append(f"tense: answer {ans!r} reads {t}, cue says {k}: {s!r}")
    if k == "pr" and t == "pr":
        ts = third_sing(d, toks[0])
        if ts is None or ts != ans.endswith("s"): e.append(f"tense: {ans!r} doesn't agree with the subject: {s!r}")
    for w in wrong:
        tw, _, _ = tense_of(s, w)
        if tw is None or tw == k: e.append(f"tense: wrong option {w!r} reads {tw}: {s!r}")
    if len(set([ans] + wrong)) != 3: e.append(f"tense: options not 3 distinct: {s!r}")
    return e

def data_pass(D):
    e = []
    for s, a, w in D["tense"]: e += tense_item(s, a, w)
    for s in D["slip"]:
        v = slip(s)
        pres = [x for x, tg, _ in v if tg in ("VBZ", "VBP")]; past = [x for x, tg, _ in v if tg == "VBD"]
        if len(v) != 4 or len(pres) != 1 or len(past) != 3 or len({x for x, _, _ in v}) != 4: e.append(f"slip: {v}: {s!r}")
        if [x for x, _, m in v if m] != pres: e.append(f"slip: marked {[x for x, _, m in v if m]}, spaCy says {pres}: {s!r}")
    for s, a, w in D["agree"]:
        n = number(s)
        if n is None or (n == "s") != a.endswith("s") or a.endswith("s") == w.endswith("s"): e.append(f"agree: number {n}, answer {a!r}: {s!r}")
    for s, b in D["irr"]:
        if b not in IRR: e.append(f"irr: unknown verb {b!r}"); continue
        ans, pp, tag = irr_form(s, b)
        if tag != ("VBN" if pp else "VBD"): e.append(f"irr: spaCy tags {ans!r} {tag}, rule says {'VBN' if pp else 'VBD'}: {s!r}")
    for s, k, a in D["pron"]:
        r = role(s)
        if r not in ("subj", "obj") or (SUBJ if r == "subj" else OBJ)[k] != a: e.append(f"pron: role {r}, answer {a!r}: {s!r}")
    return e

def check(q, D):
    e = []; d = q["data"]; t = d.get("t"); a = q["answer"]; w = q["wrong"]
    if a in w or len(set(w)) != len(w): e.append("answer among wrong / duplicates")
    if len(w) != q["nw"]: e.append("wrong count")
    if t == "tense":
        e += tense_item(d["s"], a, w)
        if d["s"].split()[0] not in re.sub(r"<[^>]+>", "", q["html"]): e.append("sentence not shown")
    elif t == "slip":
        v = slip(d["s"]); pres = [x for x, tg, _ in v if tg in ("VBZ", "VBP")]
        if pres != [a]: e.append(f"slip answer {a!r}, checker {pres}")
        if set([a] + w) != {x for x, _, _ in v}: e.append("slip options are not the 4 verbs")
        if "{" in q["html"] or "*" in q["html"]: e.append("braces shown")
    elif t == "agree":
        n = number(d["s"])
        if (n == "s") != a.endswith("s"): e.append(f"agree: number {n}, answer {a!r}")
        if len(w) != 1 or w[0].endswith("s") == a.endswith("s"): e.append("agree wrong option")
    elif t == "irr":
        b = d["b"]; ans, pp, tag = irr_form(d["s"], b)
        if a != ans: e.append(f"irr: answer {a!r}, checker {ans!r}")
        if set(w) != {b, *IRR[b]} - {a}: e.append(f"irr: wrong {w}")
    elif t == "pron":
        r = role(d["s"]); k = d["k"]
        if (SUBJ if r == "subj" else OBJ).get(k) != a: e.append(f"pron: role {r}, answer {a!r}")
        if w != [(OBJ if r == "subj" else SUBJ)[k]]: e.append("pron wrong option")
    else: e.append("unknown type")
    return e

if __name__ == "__main__":
    src = sys.argv[2] if len(sys.argv) > 2 else "tense-trap.html"
    D = load(src); errs = data_pass(D)
    for x in errs: print("DATA", x)
    n = bad = 0; seen = {}
    if sys.argv[1] != "-":
        for line in open(sys.argv[1], encoding="utf-8"):
            q = json.loads(line); n += 1; e = check(q, D)
            seen[q["data"].get("t")] = seen.get(q["data"].get("t"), 0) + 1
            if e:
                bad += 1
                if bad <= 15: print("BAD", q["mode"], q["data"].get("s"), q["answer"], e)
    print(f"data problems: {len(errs)} · questions: {n} · problems: {bad} · types: {seen}")
    sys.exit(1 if errs or bad or (sys.argv[1] != "-" and n < 100) else 0)
