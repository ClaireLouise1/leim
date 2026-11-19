#!/usr/bin/env python3
"""Independent checker for Word Ladder (word-ladder.html, JC English Order 13).

Re-derives every answer with WordNet (a separate dictionary) and spaCy (word classes), not with the game's own code.
Usage:  N=400 node src/test_word_ladder.js word-ladder.html > /tmp/wl.jsonl && python3 src/test_word_ladder.py /tmp/wl.jsonl word-ladder.html
        python3 src/test_word_ladder.py - <page or json>     (data pass only)
Needs:  pip install --break-system-packages spacy nltk  (+ the en_core_web_sm wheel)
        NLTK_ALLOW_PROXIED_URLOPEN=1 python3 -c "import nltk; nltk.download('wordnet')"   (once per session)
"""
import sys, json, re
from functools import lru_cache
from nltk.corpus import wordnet as wn

# ---------- WordNet relations ----------
def lemmas(s): return {l.name().lower().replace("_", " ") for l in s.lemmas()}

def synsets(w, pos=None):
    out = list(wn.synsets(w.replace(" ", "_"), pos=pos))
    return out

def neighbours(s):
    n = set(s.similar_tos()) | set(s.also_sees()) | set(s.verb_groups())
    for l in s.lemmas():
        for d in l.derivationally_related_forms(): n.add(d.synset())
        for p in l.pertainyms(): n.add(p.synset())
    n |= set(s.hypernyms()) | set(s.hyponyms())
    return n

@lru_cache(None)
def near(w, depth=2):
    """lemma names reachable from w's synsets within `depth` steps"""
    seen = set(synsets(w)); front = set(seen)
    for _ in range(depth):
        nxt = set()
        for s in front: nxt |= neighbours(s)
        nxt -= seen; seen |= nxt; front = nxt
    out = set()
    for s in seen: out |= lemmas(s)
    return out

def related(a, b, depth=2):
    a, b = a.lower(), b.lower()
    return b in near(a, depth) or a in near(b, depth)

def _close_sets(s):
    """a synset, the heads it is a satellite of, and the satellites of those heads (siblings)"""
    out = {s} | set(s.also_sees()) | set(s.verb_groups())
    for h in set(s.similar_tos()):
        out.add(h); out |= set(h.similar_tos())
    return out

def strict_synonym(a, b, senses=None):
    """same synset, a similar-to head, or a sibling satellite (no definitions, no hypernyms)"""
    for x, y in ((a, b), (b, a)):
        for s in synsets(x)[:senses]:
            for t in _close_sets(s):
                if y.lower() in lemmas(t): return True
    return False

WORD = re.compile(r"[a-z]+")
NEG = re.compile(r"\b(not|no|lacking|without|un\w+|less|opposite)\b")
def gloss_words(w, senses=None):
    """words used in the (positive) definitions of w's commonest senses; definitions with not / lacking / without are skipped"""
    out = set()
    for s in synsets(w)[:senses]:
        d = s.definition().lower()
        if NEG.search(d): continue
        out |= set(WORD.findall(d))
    return out

def forms(w):
    """the word, its WordNet base forms and derivationally related words"""
    out = {w.lower()}
    for p in "nvar":
        b = wn.morphy(w, p)
        if b: out.add(b)
    for s in synsets(w):
        for l in s.lemmas():
            if l.name().lower() in out:
                for d in l.derivationally_related_forms(): out.add(d.name().lower())
    return out

def defined_by(a, b, senses=None):
    return bool(forms(a) & gloss_words(b, senses)) or bool(forms(b) & gloss_words(a, senses))

def synonym(a, b):
    """strict synonym, or one's positive definition uses the other ("win: a victory")"""
    return strict_synonym(a, b) or defined_by(a, b, 2)

# ladder pairs WordNet doesn't link, confirmed by hand (school-dictionary meanings): keep this list short
ALLOW = {("tired", "sleepy")}
def linked(a, b):
    """for ladder words: related in the graph, or one's definition uses the other (or its root word)"""
    return (a, b) in ALLOW or (b, a) in ALLOW or related(a, b, 3) or synonym(a, b)

@lru_cache(None)
def ants(w):
    """direct antonyms of w, plus indirect ones (antonyms of the heads its satellites hang from, and their satellites)"""
    out = set()
    for s in synsets(w):
        heads = {s} | set(s.similar_tos())
        for h in heads:
            for l in h.lemmas():
                for a in l.antonyms():
                    out |= lemmas(a.synset())
                    for t in a.synset().similar_tos(): out |= lemmas(t)
    return out

def antonym(a, b, senses=None):
    if senses: return b.lower() in ants_n(a, senses) or a.lower() in ants_n(b, senses)
    if b.lower() in ants(a) or a.lower() in ants(b): return True
    # indirect: b's definition uses an antonym of a ("sad: showing sorrow or unhappiness" ↔ happy), and they aren't synonyms
    if strict_synonym(a, b): return False
    return bool(ants(a) & gloss_words(b, 2)) or bool(ants(b) & gloss_words(a, 2))

def ants_n(w, senses):
    out = set()
    for s in synsets(w)[:senses]:
        for h in {s} | set(s.similar_tos()):
            for l in h.lemmas():
                for x in l.antonyms():
                    out |= lemmas(x.synset())
                    for t in x.synset().similar_tos(): out |= lemmas(t)
    return out

def is_word(w):
    return bool(wn.synsets(w)) or any(wn.morphy(w, p) == w for p in "nvar")

def adj_slot(sentence, word):
    for t in nlp()(sentence):
        if t.text.lower() == word.lower():
            return t.pos_ == "ADJ" or t.tag_ in ("VBG", "VBN", "JJ")
    return False

POSMAP = {"NOUN": "n", "VERB": "v", "ADJ": "a", "ADV": "r"}
def wn_pos(w):
    """word classes WordNet allows for this exact form (inflections via morphy)"""
    out = set()
    for p in "nvar":
        base = wn.morphy(w, p)
        if base and wn.synsets(base, pos=p): out.add(p)
    if "s" in out: out.add("a")
    return out

_nlp = None
def nlp():
    global _nlp
    if _nlp is None:
        import spacy; _nlp = spacy.load("en_core_web_sm")
    return _nlp

@lru_cache(None)
def slot_pos(sentence, word):
    """spaCy's word class for `word` placed in the sentence"""
    doc = nlp()(sentence)
    for t in doc:
        if t.text.lower() == word.lower():
            return POSMAP.get(t.pos_, t.pos_)
    raise AssertionError(f"{word!r} not found in {sentence!r}")

PREFIX_MEANING = {"un": "not", "dis": "not", "im": "not", "in": "not", "il": "not", "ir": "not",
                  "re": "again", "mis": "wrong|bad", "pre": "before"}
PRE_ORDER = ["un", "dis", "im", "in", "il", "ir", "re", "mis", "pre"]
CLASS_WORD = {"n": "a noun", "v": "a verb", "a": "an adjective", "r": "an adverb"}

def clash(a, b):
    """could b pass for a? (same meaning in one of the 3 commonest senses, or one defined with the other)"""
    return strict_synonym(a, b, 1) or defined_by(a, b, 1)

# context clues for each meaning (by its emoji): the sentence must contain a clue for the right meaning and none for
# the others. Meanings with a different word class (right, light, fair, match the verb) are also checked with spaCy.
CLUES = {"🦇": r"\b(cave|flew|fly|night|wings?)\b", "🏏": r"\b(hold|hands?|swing|hit|ball|cricket|hurl)\b",
         "🏞️": r"\b(river|sat|grass|fish)\b", "💶": r"\b(money|savings?|account|cash)\b",
         "🌳": r"\b(tree|trunk|oak)\b", "🐕": r"\b(heard|loud|dog|next door)\b",
         "💍": r"\b(wore|gold|finger|silver)\b", "📞": r"\b(phone|waited|answer)\b",
         "➡️": r"\b(turn|left|church|road)\b", "✅": r"\b(answer|correct|is right)\b",
         "🧦": r"\b(socks?|pairs?|colours?)\b", "⚽": r"\b(won|lost|score|team|\d+–\d+)\b", "🔥": r"\b(strike|candle|fire|light)\b",
         "💡": r"\b(bright|switch|lamp|dark)\b", "🪶": r"\b(carry|lift|heavy|weigh)\b",
         "⚖️": r"\b(result|each|share|rules?)\b", "🎡": r"\b(rides?|went on|stalls?)\b"}

# ---------- load the data block from the page ----------
def load(path):
    t = open(path, encoding="utf-8").read()
    if path.endswith(".json"): return json.loads(t)
    m = re.search(r"/\*DATA\*/(.*?)/\*END\*/", t, re.S)
    return json.loads(m.group(1))

# ---------- data pass ----------
def data_pass(D):
    errs = []
    def E(m): errs.append(m)
    strongs = [L[1][2] for L in D["ladder"] if L[2]]
    for L in D["ladder"]:
        w = L[1]
        if len(set(w)) != 3: E(f"ladder repeats a word {w}")
        for x in w:
            if not is_word(x): E(f"ladder word not in WordNet: {x}")
        for x in (w[0], w[2]):
            if not linked(w[1], x): E(f"ladder words not linked in WordNet: {w[1]} / {x}")
        if L[2] and "very " + w[1] not in L[2]: E(f"sentence lacks 'very {w[1]}': {L[2]}")
        elif L[2]:
            # the strong word must fit where 'very <middle>' was: an adjective (or a participle used as one)
            if not adj_slot(L[2].replace("very " + w[1], w[2]), w[2]): E(f"strong word isn't an adjective in {L[2]}")
    # the strongest word of another ladder must not be related to this ladder's middle word (it's offered as wrong)
    for L in D["ladder"]:
        if not L[2]: continue
        for s in strongs:
            if s == L[1][2]: continue
            if (clash(L[1][1], s) or clash(L[1][2], s)) and s not in (L[3] if len(L) > 3 else []):
                E(f"very-{L[1][1]}: other ladder's strong word {s!r} is related: add it to the ladder's avoid list")
    for it in D["syn"]:
        w, s, a = it
        if not synonym(w, s): E(f"not synonyms in WordNet: {w} = {s}")
        if not antonym(w, a): E(f"not antonyms in WordNet: {w} ↔ {a}")
        if s.lower() in ants(w) or w.lower() in ants(s): E(f"synonym also an antonym: {w}/{s}")
        if strict_synonym(w, a): E(f"antonym also a synonym: {w}/{a}")
    # other items' synonyms / antonyms are offered as wrong: none may be a synonym or antonym of this word
    for it in D["syn"]:
        for jt in D["syn"]:
            if it is jt: continue
            for x in (jt[1], jt[2]):
                if x in (it[1], it[2]): E(f"{it[0]}: {x} is used by two items"); continue
                if clash(it[0], x) or antonym(it[0], x, 2):
                    E(f"{it[0]}: other item's word {x!r} is a synonym/antonym")
    for item in D["pre"]:
        p, r, g = item[:3]; av = item[3] if len(item) > 3 else []
        if p not in PRE_ORDER: E(f"unknown prefix {p}")
        if not is_word(p + r): E(f"{p}{r} is not a word in WordNet")
        if not re.search(PREFIX_MEANING[p], g): E(f"{p}{r}: meaning '{g}' doesn't say {PREFIX_MEANING[p]}")
        if r not in g: E(f"{p}{r}: meaning '{g}' doesn't use the root")
        for q in PRE_ORDER:
            if q != p and is_word(q + r) and q not in av:
                E(f"{q}{r} is also a word: add {q!r} to the avoid list of {p}{r}")
        if len([q for q in PRE_ORDER if q != p and q not in av]) < 3: E(f"{p}{r}: fewer than 3 prefixes left to offer")
    for s, a, wr, c in D["fam"]:
        if s.count("___") != 1: E(f"fam gap: {s}")
        full = s.replace("___", a)
        p = slot_pos(full, a)
        if p not in wn_pos(a): E(f"fam: {a} can't be {p} (WordNet {wn_pos(a)}) in {full}")
        if c != p: E(f"fam: data says the gap needs {c}, spaCy says {p}: {full}")
        for x in wr:
            if p in wn_pos(x): E(f"fam: wrong option {x} can also be {p} in {s}")
            if not wn_pos(x): E(f"fam: {x} not in WordNet")
        for x in wr:
            if not (x[:2].lower() == a[:2].lower() or x.lower().startswith(("un", "en")) and x[2:4].lower() == a[:2].lower() or forms(x) & forms(a)):
                E(f"fam: {x} doesn't look like the family of {a}")
    for ws in D["abc"]:
        if len(set(ws)) != 4 or len({w[0] for w in ws}) != 1: E(f"abc set {ws}")
        for w in ws:
            if not is_word(w): E(f"abc word not in WordNet: {w}")
    for top, bot, inn, out in D["guide"]:
        if not (top < bot): E(f"guide words out of order {top} {bot}")
        if not (top <= inn <= bot): E(f"{inn} not between {top} and {bot}")
        for x in out:
            if top <= x <= bot: E(f"{x} IS between {top} and {bot}")
        for w in [top, bot, inn] + out:
            if not is_word(w): E(f"guide word not in WordNet: {w}")
    for s, right, wrong in D["mean"]:
        w = re.search(r"\{(\w+)\}", s).group(1)
        if len(synsets(w)) < 2: E(f"{w} has only one meaning in WordNet")
        cls = lambda d: "a" if re.match(r"^\S+ (not|correct|equal|the opposite)", d) else "n" if re.match(r"^\S+ (a|an|the) ", d) else "v"
        sp = slot_pos(s.replace("{", "").replace("}", ""), w)
        sp = "a" if sp in ("a", "r") else sp
        if cls(right) != sp and not (cls(right) == "n" and sp == "n"):
            E(f"meaning '{right}' is {cls(right)} but '{w}' is {sp} in {s}")
        if right in wrong: E(f"meaning repeated: {s}")
        plain = s.replace("{", "").replace("}", "")
        ctx = re.sub(r"\b" + w + r"\b", "", plain.lower())
        emo = lambda d: d.split(" ")[0]
        if emo(right) not in CLUES or not re.search(CLUES[emo(right)], ctx): E(f"no context clue for '{right}' in {plain}")
        for x in wrong:
            if emo(x) in CLUES and re.search(CLUES[emo(x)], ctx) and not re.search(CLUES[emo(right)], ctx): E(f"clue points to '{x}' in {plain}")
            if emo(x) in CLUES and re.search(CLUES[emo(x)], ctx): E(f"sentence also has a clue for '{x}': {plain}")
    # each ambiguous word has the same set of meanings in every sentence
    by = {}
    for s, right, wrong in D["mean"]:
        w = re.search(r"\{(\w+)\}", s).group(1)
        by.setdefault(w, set()).add(frozenset([right] + wrong))
    for w, v in by.items():
        if len(v) != 1: E(f"{w}: meaning lists differ")
    return errs

# ---------- question pass ----------
def check_q(q, D):
    errs = []
    def E(m): errs.append(f"{q['data'].get('t')}: {m} | {q['answer']} | {q['wrong']}")
    a, wr, d, t = q["answer"], q["wrong"], q["data"], q["data"].get("t")
    if a in wr: E("answer among wrong options")
    if len(set(wr)) != len(wr): E("repeated wrong option")
    if len(wr) != q["nw"]: E(f"{len(wr)} wrong options, expected {q['nw']}")
    if q.get("fixed") and sorted(q["fixed"]) != sorted([a] + wr): E("fixed buttons don't match the options")
    if t in ("strong", "weak", "climb"):
        lad = next(L for L in D["ladder"] if L[1] == d["ladder"])[1]
        if t == "strong" and (a != lad[2] or set(wr) != {lad[0], lad[1]}): E("strongest wrong")
        if t == "weak" and (a != lad[0] or set(wr) != {lad[1], lad[2]}): E("weakest wrong")
        if t == "climb":
            if a.split(" → ") != lad: E("climb order wrong")
            for x in wr:
                if sorted(x.split(" → ")) != sorted(lad) or x.split(" → ") == lad: E(f"bad climb option {x}")
    elif t == "very":
        base, weak = d["base"], d["weak"]
        if f"very {base}" not in d["sent"]: E("sentence")
        if not linked(base, a): E(f"{a} not related to {base}")
        if weak not in wr: E("weaker trap missing")
        for x in wr:
            if x == weak: continue
            if clash(base, x) or clash(a, x): E(f"wrong option {x} related to {base}")
    elif t in ("same", "opp"):
        w = d["word"]
        good = synonym if t == "same" else antonym
        if not good(w, a): E(f"{a} is not a {'synonym' if t=='same' else 'antonym'} of {w}")
        item = next(i for i in D["syn"] if i[0] == w)
        trapw = item[2] if t == "same" else item[1]
        for x in wr:
            if x == trapw: continue
            if clash(w, x) or antonym(w, x, 2): E(f"wrong option {x} is also right")
        trap = [x for x in wr if x == trapw and (antonym if t == "same" else synonym)(w, x)]
        if len(trap) != 1: E(f"expected exactly one trap, got {trap}")
    elif t == "pair":
        o = antonym(d["a"], d["b"]); s = synonym(d["a"], d["b"]) and not (d["b"].lower() in ants(d["a"]) or d["a"].lower() in ants(d["b"]))
        if s == o: E(f"{d['a']}/{d['b']} both or neither")
        if a != ("🟰 Same" if s else "↔️ Opposite"): E("pair answer")
    elif t == "pre":
        r = d["root"]
        if not is_word(a + r): E(f"{a}{r} not a word")
        for x in wr:
            if is_word(x + r): E(f"{x}{r} is also a word")
        if q["fixed"] != [p for p in PRE_ORDER if p in q["fixed"]]: E("prefix buttons not in the fixed order")
    elif t == "fam":
        full = d["sent"].replace("___", a)
        p = slot_pos(full, a)
        if p not in wn_pos(a): E(f"{a} can't be {p}")
        for x in wr:
            if p in wn_pos(x): E(f"{x} could also be {p}")
        if CLASS_WORD[p] not in q["why"]: E(f"why names the wrong class (slot is {CLASS_WORD[p]}): {q['why']}")
    elif t in ("abcFirst", "abcLast"):
        s = sorted(d["words"])
        if a != (s[0] if t == "abcFirst" else s[-1]): E("ABC answer")
        if sorted([a] + wr) != s: E("ABC options")
    elif t == "guide":
        if not (d["top"] <= a <= d["bottom"]): E("guide answer off the page")
        for x in wr:
            if d["top"] <= x <= d["bottom"]: E(f"{x} is on the page")
    elif t == "mean":
        item = next(m for m in D["mean"] if m[0].replace("{", "").replace("}", "") == d["sent"])
        if a != item[1] or sorted(wr) != sorted(item[2]): E("meaning answer")
    else:
        E("unknown type")
    # nothing leaks: the answer isn't printed in the question card (except where the card must show it)
    if t in ("same", "opp", "very", "fam", "pre", "strong", "weak") and re.search(r"\b" + re.escape(a) + r"\b", re.sub("<[^>]+>", " ", q["html"])):
        E("answer shown in the card")
    return errs

def main():
    src, page = sys.argv[1], sys.argv[2]
    D = load(page)
    errs = data_pass(D)
    for e in errs: print("DATA:", e)
    n = 0; qerrs = []
    if src != "-":
        for line in open(src, encoding="utf-8"):
            q = json.loads(line); n += 1
            qerrs += check_q(q, D)
    seen = set()
    for e in qerrs:
        if e not in seen: print("Q:", e); seen.add(e)
    print(f"{n} questions, {len(errs)} data problems, {len(qerrs)} question problems")
    sys.exit(1 if errs or qerrs else 0)

if __name__ == "__main__":
    main()
