#!/usr/bin/env python3
"""Independent checker for Speech Marks Sprint (JC English Order 24, Punctuation 2: dialogue, quotes, colons & semicolons).
It does not trust the game's answers: it re-derives each one with its own rules (no spaCy needed).
  - speech kind   from the reporting verb in the tag (asked / wondered -> question; shouted, yelled, screamed, cried,
                  roared -> exclamation; anything else -> statement) AND from the spoken words (a question must open
                  with a question word or helping verb, nothing else may) - the two must agree
  - valid(s)      reads a whole dialogue sentence with its own grammar of the two school layouts:
                    "Speech," said X.  /  "Question?" asked X.  /  "Shout!" yelled X.   (tag starts lower case unless
                    it starts with a name)
                    X said, "Speech."  /  X asked, "Question?"  /  X yelled, "Shout!"
                  every answer must be valid and EVERY wrong option invalid
  - inside mark   the mark inside the closing speech mark, from the kind and the layout; the ambiguous marks
                  (a comma for a shout, a full stop for a shout at the end) are never offered
  - colon/semi    colon = a list announced by a number word / "the following" / "these" / "everything" / "the basics"
                  before the gap, with a list (comma or "and") after it; semicolon = two complete sentences: no
                  announcing word, no comma after the gap, and the second part does not open with a joining word
                  (and / but / so / because), so a comma is never right
  - reported      the checker builds the reported version itself: I -> he/she, my -> his/her, we -> they, our -> their,
                  am/is -> was, are -> were, have/has -> had, can -> could, will -> would, don't -> didn't,
                  can't -> couldn't; questions -> "X asked if <subject> <verb> ..."; the answer must equal it, and every
                  wrong option must differ and show a real slip (I / my kept, a present verb kept, speech marks or a
                  question mark kept)
Usage: N=400 node src/test_speech_marks.js speech-marks-sprint.html > /tmp/sm.jsonl && python3 src/test_speech_marks.py /tmp/sm.jsonl speech-marks-sprint.html
       python3 src/test_speech_marks.py - <page or json>   (data pass only)"""
import sys, json, re, html as H

QV = {"asked", "wondered"}
EV = {"shouted", "yelled", "screamed", "cried", "roared"}
SV = {"said", "whispered", "explained", "replied", "muttered", "admitted", "announced", "told", "grumbled", "called", "groaned"}
VERBS = QV | EV | SV
QSTART = set("Who What Where When Why How Which Can Could Is Are Am Was Were Do Does Did Have Has Will Would Should Shall".split())
PRON = {"He", "She", "They", "It", "We", "I", "You"}
MARK_NAME = {",": "Comma ,", ".": "Full stop .", "?": "Question mark ?", "!": "Exclamation mark !"}

def tag_kind(tag):
    vs = [w for w in re.findall(r"[a-z]+", tag) if w in VERBS]
    if len(vs) != 1: return None
    v = vs[0]
    return "q" if v in QV else "e" if v in EV else "s"
def words_kind(sp):
    return "q" if sp.split()[0] in QSTART else "x"
def kind(sp, tag):
    k = tag_kind(tag)
    if k is None: return None
    if (k == "q") != (words_kind(sp) == "q"): return None
    return k
END_A = {"s": ",", "q": "?", "e": "!"}
END_B = {"s": ".", "q": "?", "e": "!"}

def is_name(w):
    return w[:1].isupper() and w not in PRON and w.lower() not in VERBS and w not in ("The", "My", "Our")

def valid(s):
    """True if s is one correctly punctuated dialogue sentence."""
    if s.count('"') != 2: return False
    m = re.fullmatch(r'"([^"]+)([,?!])" ([^".,?!]+)\.', s)
    if m:
        sp, mk, tag = m.groups()
        if not sp[0].isupper() or sp[-1] in ".,?!;:": return False
        k = kind(sp, tag)
        if k is None or END_A[k] != mk: return False
        first = tag.split()[0]
        return first.islower() or is_name(first) or first == "I"
    m = re.fullmatch(r'([A-Z][^".,?!]*), "([^"]+)([.?!])"', s)
    if m:
        tag, sp, mk = m.groups()
        if not sp[0].isupper() or sp[-1] in ".,?!;:": return False
        k = kind(sp, tag)
        return k is not None and END_B[k] == mk
    return False

def build(sp, tag, pos):
    k = kind(sp, tag)
    return f'"{sp}{END_A[k]}" {tag}.' if pos == "a" else f'{tag}, "{sp}{END_B[k]}"'

# ---------- colon / semicolon ----------
ANN = r"\b(two|three|four|five|six|following|these|everything|basics)\b"
JOINW = {"and", "but", "so", "because", "or", "yet"}
def join_mark(s):
    a, b = s.split(" ___ ")
    if re.search(ANN, a, re.I) and ("," in b or " and " in b) and not re.search(r"\b(are|is|include|includes|were|like|as|of|for)$", a):
        return "c"
    if not re.search(ANN, a, re.I) and "," not in b and b.split()[0].lower() not in JOINW and len(a.split()) >= 3 and len(b.split()) >= 3 \
       and (b[0].islower() or is_name(b.split()[0])):
        return "s"
    return None
JLAB = {"c": "Colon :", "s": "Semicolon ;"}

# ---------- reported speech ----------
PR = {"f": {"I": "she", "me": "her", "my": "her", "My": "Her"}, "m": {"I": "he", "me": "him", "my": "his", "My": "His"}, "p": {}}
PL = {"we": "they", "We": "They", "us": "them", "our": "their", "Our": "Their"}
BACK = {"am": "was", "is": "was", "are": "were", "have": "had", "has": "had", "can": "could", "will": "would",
        "don't": "didn't", "doesn't": "didn't", "can't": "couldn't", "won't": "wouldn't", "do": "did",
        "Am": "was", "Is": "was", "Are": "were", "Have": "had", "Has": "had", "Can": "could", "Will": "would"}
FIRST = {"I", "me", "my", "My", "we", "We", "us", "our", "Our"}
PRESENT = {"am", "is", "are", "have", "has", "can", "will", "don't", "doesn't", "can't", "won't", "do"}
TIMEPLACE = {"today", "tomorrow", "yesterday", "now", "here", "this", "tonight"}
# who is speaking: the checker's own list (a "she" for Niamh would be caught)
FEM = {"Niamh", "Leah", "Orla", "Aoife", "Ella", "Ciara", "Róisín", "Gran", "Mam"}
MASC = {"Cian", "Tadhg", "Fionn", "Seán", "Grandad", "Liam", "Oisín", "Darragh", "Dad"}
def gender(tag):
    w = tag.split(" ", 1)[1]
    if w in FEM: return "f"
    if w in MASC: return "m"
    if w in ("the twins", "the girls", "the boys", "the children"): return "p"
    return None
def speaker(tag):
    w = tag.split(" ", 1)[1]
    return w[0].upper() + w[1:]
def swap(w, g):
    return PR[g].get(w) or PL.get(w) or w
def reported(sp, tag, g):
    ws = sp.split()
    if tag.startswith("asked"):
        aux = ws[0]; n = 2 if ws[1] in ("my", "our", "the") else 1
        subj = [swap(w, g) for w in ws[1:1 + n]]
        rest = [BACK.get(w, swap(w, g)) for w in ws[1 + n:]]
        return f"{speaker(tag)} asked if {' '.join(subj)} {BACK[aux]} {' '.join(rest)}.".replace("  ", " ")
    out = [BACK.get(w, swap(w, g)) for w in ws]
    out[0] = out[0][0].lower() + out[0][1:] if out[0] not in ("I",) else out[0]
    return f"{speaker(tag)} said that {' '.join(out)}."
def rep_slip(s):
    """what is wrong with a reported-speech option (empty = nothing found)"""
    toks = re.findall(r"[A-Za-z']+", s)
    slips = []
    if any(t in FIRST for t in toks): slips.append("first person kept")
    if any(t in PRESENT for t in toks[2:]): slips.append("present verb kept")
    if '"' in s: slips.append("speech marks")
    if "?" in s: slips.append("question mark")
    return slips

def load(path):
    s = open(path, encoding="utf-8").read()
    if path.endswith(".json"): return json.loads(s)
    return json.loads(s[s.index("/*DATA*/") + 8:s.index("/*END*/")])

def data_pass(D):
    e = []
    for sp, tag, pos in D["dlg"]:
        k = kind(sp, tag)
        if k is None: e.append(f"dlg: {sp!r} / {tag!r}: tag verb and words disagree (or no reporting verb)"); continue
        if pos not in "ab": e.append(f"dlg: bad position {pos}")
        if pos == "b" and not tag[0].isupper(): e.append(f"dlg: {tag!r} starts the sentence: needs a capital")
        if pos == "a" and not (tag[0].islower() or is_name(tag.split()[0])): e.append(f"dlg: {tag!r} after the speech must start lower case or with a name")
        if re.search(r"[.,?!;:\"]", sp): e.append(f"dlg: {sp!r} has punctuation inside")
        if not valid(build(sp, tag, pos)): e.append(f"dlg: built {build(sp, tag, pos)!r} is not valid")
    for s, k in D["join"]:
        if s.count(" ___ ") != 1: e.append(f"join: {s!r} needs one gap"); continue
        if join_mark(s) != k: e.append(f"join: {s!r} reads as {join_mark(s)}, tagged {k}")
    for sp, tag, g in D["rep"]:
        toks = sp.split()
        if not any(t in FIRST for t in toks): e.append(f"rep: {sp!r} has no I / my / we to change")
        if not any(t in BACK for t in toks): e.append(f"rep: {sp!r} has no verb to move back")
        if any(t.lower() in TIMEPLACE for t in toks) or "you" in [t.lower() for t in toks] or "your" in [t.lower() for t in toks]:
            e.append(f"rep: {sp!r} has a time/place/you word")
        if gender(tag) != g: e.append(f"rep: {tag!r} is {gender(tag)}, tagged {g}")
        r = reported(sp, tag, g)
        if rep_slip(r): e.append(f"rep: {sp!r} -> {r!r} still has {rep_slip(r)}")
        q = tag.startswith("asked")
        if q != (toks[0] in QSTART): e.append(f"rep: {sp!r} question/statement mismatch")
    return e

def strip(h): return H.unescape(re.sub(r"<[^>]+>", "", h))

def check(q, D):
    e = []; d = q["data"]; t = d["t"]; opts = [q["answer"]] + q["wrong"]
    if len(set(opts)) != len(opts): e.append("duplicate options")
    if t == "sprint":
        sp, tag, pos = d["it"]
        if len(q["wrong"]) != 3: e.append(f"wrong count {len(q['wrong'])}")
        if q["answer"] != build(sp, tag, pos): e.append(f"answer {q['answer']!r} != {build(sp, tag, pos)!r}")
        if not valid(q["answer"]): e.append(f"answer not valid: {q['answer']!r}")
        for w in q["wrong"]:
            if valid(w): e.append(f"wrong option is valid: {w!r}")
            if re.sub(r"[^A-Za-zÀ-ÿ' ]", "", w).lower().split() != re.sub(r"[^A-Za-zÀ-ÿ' ]", "", q["answer"]).lower().split():
                e.append(f"wrong option changes the words: {w!r}")
    elif t == "mark":
        sp, tag, pos = d["it"]; k = kind(sp, tag)
        mk = (END_A if pos == "a" else END_B)[k]
        if q["answer"] != MARK_NAME[mk]: e.append(f"mark answer {q['answer']} != {MARK_NAME[mk]}")
        if len(q["wrong"]) != 2: e.append(f"wrong count {len(q['wrong'])}")
        # never offered: "!" for a statement or question; for a shout, the comma (after) / full stop (before) that some books allow
        bad = {MARK_NAME["!"]} if k != "e" else {MARK_NAME["," if pos == "a" else "."]}
        for w in q["wrong"]:
            if w == q["answer"] or w in bad or w not in MARK_NAME.values(): e.append(f"mark: bad wrong option {w} for kind {k}{pos}")
        shown = strip(q["html"])
        if sp not in shown or tag not in shown: e.append("mark: sentence not shown")
        if mk in shown.replace(tag + ",", tag).split(sp, 1)[1].split('"')[0]: e.append("mark: answer leaks into the card")
    elif t == "join":
        s = d["s"]; k = join_mark(s)
        if k is None: e.append(f"join: unreadable {s!r}")
        elif q["answer"] != JLAB[k]: e.append(f"join answer {q['answer']} != {JLAB[k]}")
        if sorted(opts) != sorted(["Colon :", "Semicolon ;", "Comma ,"]): e.append(f"join options {opts}")
    elif t == "report":
        sp, tag, g = d["it"]; r = reported(sp, tag, gender(tag) or g)
        if q["answer"] != r: e.append(f"report answer {q['answer']!r} != {r!r}")
        if len(q["wrong"]) != 3: e.append(f"wrong count {len(q['wrong'])}")
        for w in q["wrong"]:
            if w == r or not rep_slip(w): e.append(f"report: wrong option has no slip: {w!r}")
        shown = strip(q["html"])
        if build(sp, tag, "a") not in shown: e.append("report: direct speech not shown")
    else: e.append(f"unknown type {t}")
    return e

if __name__ == "__main__":
    src = sys.argv[2] if len(sys.argv) > 2 else "speech-marks-sprint.html"
    D = load(src); errs = data_pass(D)
    for x in errs: print("DATA", x)
    n = bad = 0; seen = {}; longest = [0, 0]
    if sys.argv[1] != "-":
        for line in open(sys.argv[1], encoding="utf-8"):
            q = json.loads(line); n += 1; e = check(q, D)
            seen[q["data"]["t"]] = seen.get(q["data"]["t"], 0) + 1
            if q["data"]["t"] in ("sprint", "report"):
                longest[1] += 1; longest[0] += len(q["answer"]) > max(len(x) for x in q["wrong"])
            if e:
                bad += 1
                if bad <= 20: print("BAD", q["mode"], q["data"].get("t"), e[:3])
        print(f"{n} questions, {bad} with problems; types {seen}; answer strictly longest in sprint/report {100 * longest[0] // max(1, longest[1])}%")
    print(f"data pass: {len(errs)} problems")
    sys.exit(1 if errs or bad else 0)
