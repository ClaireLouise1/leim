#!/usr/bin/env python3
"""Independent checker for Word Sort: re-tags every sentence with spaCy (en_core_web_sm) and checks each question.
Setup (new session): pip install --break-system-packages spacy + the en_core_web_sm 3.8.0 wheel from github.com/explosion/spacy-models/releases.
Usage: N=400 node src/test_word_sort.js word-sort.html > /tmp/ws.jsonl && python3 src/test_word_sort.py /tmp/ws.jsonl word-sort.html"""
import sys, json, re, html as H, spacy
nlp = spacy.load("en_core_web_sm")
UP = {"n": {"NOUN", "PROPN"}, "v": {"VERB", "AUX"}, "adj": {"ADJ"}, "adv": {"ADV"}, "pron": {"PRON"}, "prep": {"ADP"}, "conj": {"CCONJ", "SCONJ"}}
NAME = {"Noun": "n", "Verb": "v", "Adjective": "adj", "Adverb": "adv", "Pronoun": "pron", "Preposition": "prep", "Conjunction": "conj"}
# school-grammar answers where spaCy's universal tags differ (each checked by hand)
ALLOW = {("so", "conj")}
cache = {}
def tags(plain):
    if plain not in cache: cache[plain] = [(t.text, t.pos_, t.idx) for t in nlp(plain)]
    return cache[plain]
def cls_of(label): return NAME[label.split(" ", 1)[1]]
def agrees(word, cls, pos): return pos in UP[cls] or (word.lower(), cls) in ALLOW
bad = 0; n = 0; seen = set()
for line in open(sys.argv[1]):
    q = json.loads(line); n += 1; d = q["data"]; opts = [q["answer"]] + q["wrong"]
    def fail(msg):
        global bad; bad += 1
        if bad < 25: print("FAIL", msg, q["mode"], q["en"], H.unescape(re.sub("<[^>]+>", "", q["html"])), opts)
    if len(q["wrong"]) != 3: fail("not 3 wrong options")
    if len(set(opts)) != 4: fail("duplicate option")
    if any(re.search(r"undefined|NaN|null", o) for o in opts + [q["en"], q["why"]]): fail("bad text")
    frame = H.unescape(re.sub("<[^>]+>", "", q["html"]))
    if q["answer"] in q["en"] and d["t"] != "find": fail("answer leaks into question")
    t = d["t"]
    if t in ("sort", "glue", "switch"):
        m = re.search(r'<mark class="hl">(.*?)</mark>', q["html"]); word = H.unescape(m.group(1)); start = len(H.unescape(re.sub("<[^>]+>", "", q["html"][:m.start()]))) - len(H.unescape(re.sub("<[^>]+>", "", q["html"][:q["html"].index(">") + 1])))
        cls = cls_of(q["answer"])
        tk = [x for x in tags(frame) if x[2] == start and x[0] == word]
        if not tk: fail("can't find word " + word)
        elif not agrees(word, cls, tk[0][1]): fail(f"tagger says {tk[0][1]} for {word}, game says {cls}")
        for w in q["wrong"]:
            if cls_of(w) == cls: fail("wrong option is the answer class")
        seen.add((t, word, frame))
    elif t == "find":
        cls = d["cls"]; tk = tags(frame)
        hits = [x for x in tk if x[0] == q["answer"]]
        if not hits or not any(agrees(x[0], cls, x[1]) for x in hits): fail("tagger disagrees on answer " + q["answer"])
        for w in q["wrong"]:
            wh = [x for x in tk if x[0] == w]
            if not wh: fail("wrong option not in sentence " + w)
            elif any(agrees(x[0], cls, x[1]) for x in wh): fail(f"wrong option {w} could also be a {cls}")
        if cls in ("n", "v", "adj", "adv", "pron", "prep", "conj"):
            others = [x for x in tk if agrees(x[0], cls, x[1]) and x[0] != q["answer"] and x[0] in q["wrong"]]
            if others: fail("two right answers")
        seen.add((t, q["answer"], frame))
    elif t == "strong":
        if q["answer"] in q["wrong"]: fail("answer in wrong")
        if d["word"] not in d["sent"]: fail("weak word missing")
        if q["answer"].lower() not in q["why"].lower(): fail("why doesn't name the answer")
        seen.add((t, q["answer"]))
# full pass over the data block itself (catches tags the random sample missed)
if len(sys.argv) > 2:
    page = open(sys.argv[2], encoding="utf-8").read()
    D = json.loads(page.split("/*DATA*/")[1].split("/*END*/")[0])
    for s in D["sent"]:
        plain = re.sub(r"\{([^|}]+)\|[^}]+\}", r"\1", s)
        for m in re.finditer(r"\{([^|}]+)\|([^}]+)\}", s):
            start = len(re.sub(r"\{([^|}]+)\|[^}]+\}", r"\1", s[:m.start()]))
            tk = [x for x in tags(plain) if x[2] == start]
            if not tk or not agrees(m.group(1), m.group(2), tk[0][1]):
                bad += 1; print("DATA", m.group(1), m.group(2), tk and tk[0][1], "|", plain)
    for s, cls, w, why in D["switch"]:
        plain = s.replace("{", "").replace("}", ""); tk = [x for x in tags(plain) if x[2] == s.index("{")]
        if not agrees(w, cls, tk[0][1]): bad += 1; print("DATA switch", w, cls, tk[0][1], "|", plain)
        if w.lower() not in why.lower(): bad += 1; print("DATA switch why", w)
    for s, a, wr, why in D["strong"]:
        if a in wr or len(set(wr)) != 3 or s.count("{") != 1 or a.lower() not in why.lower(): bad += 1; print("DATA strong", s)
print(n, "questions,", len(seen), "different,", bad, "problems")
sys.exit(1 if bad else 0)
