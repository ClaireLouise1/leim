#!/usr/bin/env python3
"""Independent checker for Paragraph Builder (JC English Order 7). It re-derives every answer with its own rules + spaCy:
- topic sentence: the ONLY line that shares a content word (spaCy lemma or word, nouns/verbs/adjectives/names) with all 3 other lines
- odd one out: the ONLY line that shares no content word with any other line (and line 1 = topic sentence)
- order: its own sequence-word ranks (First / Then / Finally …)
- new paragraph (TiPToP): its own opener lists for time, place and new point, spaCy subject for a new person
- linking word: negation flip → contrast; a name or number in the 2nd sentence → example; a result word → result; otherwise → adding
Setup (new session): pip install --break-system-packages spacy + the en_core_web_sm 3.8.0 wheel (github.com/explosion/spacy-models/releases).
Usage: N=400 node src/test_paragraph_builder.js paragraph-builder.html > /tmp/pb.jsonl && python3 src/test_paragraph_builder.py /tmp/pb.jsonl paragraph-builder.html
       python3 src/test_paragraph_builder.py - <data.json or page>   (data pass only)"""
import sys, json, re, html as H, itertools
import spacy
nlp = spacy.load("en_core_web_sm")
_memo = {}
def doc(s):
    if s not in _memo: _memo[s] = nlp(s)
    return _memo[s]
POS = {"NOUN", "PROPN", "VERB", "ADJ"}
SKIP = {"be", "have", "do", "get", "make", "can", "will", "many", "some", "more", "most", "other", "another", "few", "much", "every", "all",
        "one", "lot", "lots", "thing", "way", "really", "very", "even", "also", "often", "first"}
def content(s):
    out = set()
    for t in doc(s):
        if t.pos_ in POS and not t.is_stop and t.lemma_.lower() not in SKIP and t.lower_ not in SKIP and t.is_alpha:
            out |= {t.lemma_.lower(), t.lower_}
    return out
def links(a, b): return bool(content(a) & content(b))
def topic_line(lines):
    """the line linked to all the others; None unless exactly one"""
    c = [i for i, l in enumerate(lines) if all(links(l, m) for j, m in enumerate(lines) if j != i)]
    return c[0] if len(c) == 1 and all(sum(links(l, m) for j, m in enumerate(lines) if j != i) < len(lines) - 1 for i, l in enumerate(lines) if i != c[0]) else None
def odd_line(lines):
    c = [i for i, l in enumerate(lines) if not any(links(l, m) for j, m in enumerate(lines) if j != i)]
    return c[0] if len(c) == 1 else None
RANK = [("to begin with", 1), ("at first", 1), ("first", 1), ("after that", 2), ("then", 2), ("next", 2), ("later", 2),
        ("finally", 3), ("in the end", 3), ("by the end", 3), ("last of all", 3), ("at last", 3)]
def rank(s):
    low = s.lower()
    for w, r in RANK:
        if low.startswith(w + ",") or low.startswith(w + " "): return r
    return None
TIME = re.compile(r"^(the next (morning|day|night)|(one|two|three|four|five|a|an) (hours?|days?|weeks?|months?|years?) later|that (evening|night|morning|afternoon)|"
                  r"at (midnight|dawn|noon|\d+)|on (monday|tuesday|wednesday|thursday|friday|saturday|sunday)( morning| evening| night)?|later that day|years later)\b", re.I)
PLACE = re.compile(r"^(out in|inside|outside|back at|back in|down at|down in|up at|upstairs in|downstairs in|at the (edge|top|bottom|end) of|in the (hall|kitchen|garden|yard))\b", re.I)
POINT = re.compile(r"^(on the other hand|another reason|secondly|thirdly|in addition|what's more|however|also|furthermore|my next point)\b", re.I)
PERSON = {"man", "woman", "boy", "girl", "sister", "brother", "mam", "mum", "dad", "granny", "grandad", "cousin", "teacher", "friend", "aunt", "uncle", "neighbour"}
def subject_people(s):
    """people named or described as the subject (or in apposition to it)"""
    d = doc(s); out = set()
    for t in d:
        if t.dep_ in ("nsubj", "nsubjpass") and t.head.dep_ == "ROOT":
            span = [x for x in t.subtree]
            for x in span:
                if (x.pos_ == "PROPN" and x.ent_type_ in ("PERSON", "") and x.is_title) or x.lemma_.lower() in PERSON: out.add(x.lemma_.lower())
    return out
def mentioned(s): return {t.lemma_.lower() for t in doc(s)} | {t.lower_ for t in doc(s)}
def tip(before, after):
    hits = []
    if TIME.search(after): hits.append("ti")
    if PLACE.search(after): hits.append("pl")
    if POINT.search(after): hits.append("to")
    new = subject_people(after) - mentioned(before)
    if new and not hits: hits.append("pe")
    elif new: hits.append("pe")
    return hits
NEG = {"not", "n't", "never", "no", "nobody", "nothing", "none", "neither"}
RESULT = {"close", "closed", "flood", "flooded", "delay", "delayed", "cancel", "cancelled", "postpone", "postponed"}
def neg(s): return any(t.lower_ in NEG for t in doc(s))
def link_group(a, b):
    if neg(a) != neg(b): return "contrast"
    if any(t.pos_ in ("PROPN", "NUM") or t.like_num for t in doc(b)): return "example"
    low = " " + b.lower() + " "
    if any(t.lemma_.lower() in RESULT or t.lower_ in RESULT for t in doc(b)) or " had to " in low: return "result"
    return "add"
GROUPS = {"add": ["In addition", "Also", "What's more"], "contrast": ["However", "On the other hand"],
          "example": ["For example", "For instance"], "result": ["As a result", "Because of this"]}
GOF = {w: g for g, L in GROUPS.items() for w in L}
TIPLAB = {"⏰ Time": "ti", "📍 Place": "pl", "💡 Topic": "to", "👤 Person": "pe"}

def text(h): return H.unescape(re.sub("<[^>]+>", " ", h))
def card_lines(h): return [H.unescape(re.sub("<[^>]+>", "", m)).strip() for m in re.findall(r"<p[^>]*><b>\d+</b>(.*?)</p>", h)]

def data_pass(D):
    errs = []
    for P in D["paras"]:
        L = [P["topic"]] + P["sup"]
        if topic_line(L) != 0: errs.append(("topic", P["k"], [sorted(content(P["topic"]) & content(s)) for s in P["sup"]],
                                             [[links(a, b) for b in L] for a in L]))
        for s in P["sup"]:
            if links(P["odd"], s) or links(P["odd"], P["topic"]): errs.append(("odd links", P["k"], P["odd"], sorted(content(P["odd"]) & (content(s) | content(P["topic"])))))
        for pair in itertools.combinations(P["sup"], 2):   # every odd-one-out card must work
            if odd_line([P["topic"], *pair, P["odd"]]) != 3: errs.append(("odd card", P["k"], pair))
        if len(P["sup"]) != 3: errs.append(("sup count", P["k"]))
    for S in D["seq"]:
        if [rank(x) for x in S[1:]] != [1, 2, 3]: errs.append(("seq", S[0], [rank(x) for x in S[1:]]))
        if rank(S[0]) is not None: errs.append(("seq topic has a marker", S[0]))
    for b, a, k in D["tip"]:
        if tip(b, a) != [k]: errs.append(("tip", a, tip(b, a), k))
    for a, b, w in D["link"]:
        if link_group(a, b) != GOF[w]: errs.append(("link", a, b, link_group(a, b), w))
        if not b[0].islower() and not b.split()[0] in ("James", "Achill", "I"): errs.append(("link lower", b))
    allt = [P["topic"] for P in D["paras"]] + sum([P["sup"] + [P["odd"]] for P in D["paras"]], [])
    if len(set(allt)) != len(allt): errs.append(("duplicate", ""))
    return errs

def load(path):
    s = open(path, encoding="utf-8").read()
    if "/*DATA*/" in s: s = s.split("/*DATA*/")[1].split("/*END*/")[0]
    return json.loads(s)

if __name__ == "__main__":
    bad = n = 0; seen = set()
    if sys.argv[1] != "-":
        for line in open(sys.argv[1]):
            q = json.loads(line); n += 1; d = q["data"]; t = d["t"]; opts = [q["answer"]] + q["wrong"]
            def fail(msg):
                global bad; bad += 1
                if bad < 30: print("FAIL", t, msg, "|", text(q["html"])[:200], "|", opts)
            if len(set(opts)) != len(opts): fail("duplicate option")
            if any(re.search(r"undefined|NaN|null", o) for o in opts + [q["en"], q["why"], text(q["html"])]): fail("bad text")
            if t == "topic":
                L = card_lines(q["html"]); i = topic_line(L)
                if len(L) != 4 or i is None or q["answer"] != f"Line {i+1}": fail(f"checker says line {i}")
                if sorted(opts) != ["Line 1", "Line 2", "Line 3", "Line 4"]: fail("options")
                seen.add((t, tuple(L)))
            elif t == "odd":
                L = card_lines(q["html"]); i = odd_line(L)
                if len(L) != 4 or i is None or q["answer"] != f"Line {i+1}": fail(f"checker says line {i}")
                R = L[:i] + L[i+1:] if i is not None else L
                if not all(links(R[0], m) for m in R[1:]): fail("line 1 doesn't link to every other on-topic line")
                if sorted(opts) != ["Line 2", "Line 3", "Line 4"]: fail("options")
                seen.add((t, tuple(L)))
            elif t == "order":
                lets = re.findall(r'<p class="pb-l"><b>([ABC])</b>(.*?)</p>', q["html"])
                if len(lets) != 3: fail("not 3 lettered lines")
                want = " → ".join(l for l, s in sorted(lets, key=lambda x: rank(H.unescape(x[1]))))
                if q["answer"] != want: fail("checker order " + want)
                if any(sorted(o.split(" → ")) != ["A", "B", "C"] for o in opts): fail("option isn't an order")
                if len(q["wrong"]) != 3: fail("wrong count")
                seen.add((t, d["topic"]))
            elif t == "tip":
                b, a = d["before"], d["after"]
                if b not in text(q["html"]) or a not in text(q["html"]): fail("sentences not shown")
                got = tip(b, a)
                if got != [TIPLAB[q["answer"]]]: fail(f"checker says {got}")
                if set(opts) != set(TIPLAB): fail("options aren't TiPToP")
                seen.add((t, a))
            elif t == "link":
                a, b = d["a"], d["b"]; g = link_group(a, b)
                if GOF.get(q["answer"]) != g: fail("checker says " + g)
                if len(q["wrong"]) != 3 or len({GOF[w] for w in q["wrong"]} | {g}) != 4: fail("wrong options not one per other group")
                if q["answer"] not in q["why"]: fail("why doesn't name the answer")
                seen.add((t, a))
            else: fail("unknown type")
        print(f"{n} questions, {bad} problems, {len(seen)} different items")
    if len(sys.argv) > 2:
        errs = data_pass(load(sys.argv[2]))
        print("data block:", len(errs), "problems")
        for e in errs[:40]: print("  ", e)
        bad += len(errs)
    sys.exit(1 if bad else 0)
