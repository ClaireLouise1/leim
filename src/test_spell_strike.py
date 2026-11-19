#!/usr/bin/env python3
"""Independent checker for Spell Strike (JC English Order 6, Spelling & commonly confused words).
Re-derives every answer without the game's code:
  spell   -> pyspellchecker's dictionary: the answer must be a real word, every wrong option must NOT be one,
             and each wrong option must be a near miss (edit distance 1-3)
  mix     -> its own context rules per mix-up group (spaCy tags the words around the gap)
  plural  -> the `inflect` library makes the plural
  add     -> its own suffix rules (double / drop e / y -> i), and the result must be a dictionary word
Usage: N=400 node src/test_spell_strike.js spell-strike.html > /tmp/sp.jsonl && python3 src/test_spell_strike.py /tmp/sp.jsonl spell-strike.html"""
import sys, json, re
import spacy, inflect
from spellchecker import SpellChecker
nlp = spacy.load("en_core_web_sm")
SP = SpellChecker()
INF = inflect.engine()

def known(w): return w.lower() in SP
def dist(a, b):
    a, b = a.lower(), b.lower(); d = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        p, d[0] = d[0], i
        for j, y in enumerate(b, 1):
            p, d[j] = d[j], min(d[j] + 1, d[j - 1] + 1, p + (x != y))
    return d[-1]

# ---------- mix-ups: context rules ----------
GROUPS = {"there": ["there", "their", "they're"], "your": ["your", "you're"], "to": ["to", "too", "two"], "of": ["of", "have"],
          "where": ["where", "were", "wear"], "then": ["then", "than"], "quiet": ["quiet", "quite"], "lose": ["lose", "loose"],
          "accept": ["accept", "except"], "affect": ["affect", "effect"], "effects": ["affects", "effects"], "weather": ["weather", "whether"],
          "past": ["past", "passed"], "bought": ["bought", "brought"], "hear": ["hear", "here"], "know": ["know", "no"], "our": ["our", "are"]}
MODALS = {"could", "would", "should", "must", "might"}
CLOTHES = {"jacket", "coat", "hat", "jumper", "hoodie", "uniform", "scarf", "shoes", "boots", "dress", "jersey"}
MOTION = {"walked", "ran", "drove", "went", "raced", "flew", "cycled", "rushed"}
DETS = {"the", "a", "an", "this", "that", "no", "some", "any", "special", "side", "big"}
MONEY = {"€", "euro", "euros", "sale", "shop", "paid", "cost", "money", "price"}
BRING = {"to", "home", "back", "along", "with"}
SUBJ = {"i", "we", "you", "they", "he", "she", "it"}

def ctx(sent, word):
    """spaCy tokens of the sentence with `word` in the gap; returns (before tokens, after tokens) as lists."""
    filled = sent.replace("___", word); i0 = sent.index("___")
    doc = nlp(filled)
    before = [t for t in doc if t.idx + len(t.text) <= i0]
    after = [t for t in doc if t.idx >= i0 + len(word)]
    return before, after

def possessive_next(after):
    """a noun (maybe after one adjective) straight after the gap = a belonging word fits"""
    if not after: return False
    if after[0].pos_ in ("NOUN", "PROPN"): return True
    return after[0].pos_ == "ADJ" and len(after) > 1 and after[1].pos_ == "NOUN"

def rule(group, sent):
    """which word of the group fits, decided from the words around the gap"""
    b, a = ctx(sent, "it")          # a neutral filler so the tagger sees an ordinary sentence
    prev = b[-1].lower_ if b else ""
    nxt = a[0].lower_ if a else ""
    words = [t.lower_ for t in nlp(sent.replace("___", "it"))]
    if group == "there":
        if nxt in ("is", "are", "was", "were") or prev in ("over", "in", "from", "go", "went", "get", "stay") or (a and a[0].is_punct):
            return "there"
        b2, a2 = ctx(sent, "their")
        return "their" if possessive_next(a2) else "they're"
    if group == "your":
        b2, a2 = ctx(sent, "your")
        return "your" if possessive_next(a2) else "you're"
    if group == "to":
        b2, a2 = ctx(sent, "to")
        if not a2 or a2[0].is_punct: return "too"
        if a2[0].pos_ in ("ADJ", "ADV") and a2[0].lower_ not in ("the",): return "too"
        if a2[0].tag_ == "NNS": return "two"
        return "to"
    if group == "of":
        return "have" if prev in MODALS else "of"
    if group == "where":
        if set(words[words.index("it") + 1:][:3]) & CLOTHES: return "wear"
        if not b:     # first word: Where + question; Were + subject
            return "were" if nxt in SUBJ else "where"
        return "were" if prev in SUBJ or b[-1].pos_ in ("NOUN", "PROPN") else "where"
    if group == "then":
        return "than" if (b and b[-1].tag_ in ("JJR", "RBR")) or prev in ("more", "less", "rather", "other") else "then"
    if group == "quiet":
        b2, a2 = ctx(sent, "quite")
        return "quite" if a2 and a2[0].pos_ in ("ADJ", "ADV", "DET") else "quiet"
    if group == "lose":
        return "lose" if prev in ("to", "will", "n't", "not", "might", "can", "could", "never", "'ll", "do") else "loose"
    if group == "accept":
        return "except" if nxt == "for" or prev in ("came", "everyone", "all", "everything", "everybody") else "accept"
    if group in ("affect", "effects"):
        noun = prev in DETS or (b and b[-1].pos_ == "ADJ")
        base = "effect" if noun else "affect"
        return base + ("s" if group == "effects" else "")
    if group == "weather":
        return "weather" if prev in DETS else "whether"
    if group == "past":
        return "past" if prev in MOTION | {"half", "quarter", "the", "in", "ten", "five", "twenty"} else "passed"
    if group == "bought":
        m, br = bool(set(words) & MONEY), bool(set(words[words.index("it") + 1:]) & BRING)
        if m == br: return None
        return "bought" if m else "brought"
    if group == "hear":
        return "hear" if prev in ("can", "to", "could", "n't", "will", "did", "you") else "here"
    if group == "know":
        return "know" if prev in ("n't", "i", "you", "we", "they", "to", "do", "did") else "no"
    if group == "our":
        b2, a2 = ctx(sent, "our")
        return "our" if possessive_next(a2) and prev not in SUBJ else "are"
    return None

# ---------- adding endings: own rules ----------
STRESS_LAST = {"begin", "forget", "prefer", "occur", "regret", "admit", "refer", "permit", "commit"}
V = "aeiou"
def syllables(w): return len(re.findall(r"[aeiouy]+", w.rstrip("e"))) or 1
def add_rule(w, e):
    vowel_end = e[0] in V or e == "y"
    if w.endswith("y") and len(w) > 1 and w[-2] not in V and not e.startswith("i"):
        return w[:-1] + "i" + e
    if w.endswith("e") and w[-2] not in V and vowel_end:
        return w[:-1] + e
    cvc = len(w) >= 3 and w[-1] not in V + "wxy" and w[-2] in V and w[-3] not in V
    if cvc and vowel_end and (syllables(w) == 1 or w in STRESS_LAST):
        return w + w[-1] + e
    return w + e

bad = 0
def problem(*a):
    global bad
    bad += 1
    if bad <= 40: print("PROBLEM:", *a)

D = None
if len(sys.argv) > 2:
    src = open(sys.argv[2], encoding="utf-8").read()
    D = json.loads(src[src.index("/*DATA*/") + 8:src.index("/*END*/")])

RULE_CACHE = {}
def mix_rule(g, s):
    if (g, s) not in RULE_CACHE: RULE_CACHE[(g, s)] = rule(g, s)
    return RULE_CACHE[(g, s)]

n = 0; seen = set()
for line in open(sys.argv[1], encoding="utf-8"):
    q = json.loads(line); n += 1; d = q["data"]; a = q["answer"]; W = q["wrong"]; t = d.get("t")
    seen.add((q["en"], q["html"], a))
    nw = q.get("nw") or 3
    if len(W) != nw or len(set(W)) != len(W): problem("wrong-option count", q)
    if a in W: problem("answer among wrong options", q)
    if not q.get("why"): problem("no why", q)
    if t == "spell":
        if not known(a): problem("answer not in dictionary", a)
        for w in W:
            if known(w): problem("wrong option is a real word", w, a)
            if not 1 <= dist(w, a) <= 3: problem("wrong option not a near miss", w, a)
        if nw != 3: problem("spell needs 3 wrong options")
    elif t == "mix":
        g = d["group"]; s = d["sent"]; want = mix_rule(g, s)
        if want is None: problem("rule can't decide", s)
        elif want.lower() != a.lower(): problem("mix answer", s, a, "rule says", want)
        opts = GROUPS[g]
        if sorted(x.lower() for x in [a] + W) != sorted(opts): problem("options aren't the group", s, [a] + W)
        if s.startswith("___") != a[0].isupper(): problem("capital at the start only", s, a)
        if [x.lower() for x in q["fixed"]] != opts: problem("buttons not in the fixed order", q["fixed"])
    elif t == "plural":
        one = d["one"]; want = INF.plural(one)
        if want != a: problem("plural", one, a, "inflect says", want)
        if f"one {one}" not in q["html"]: problem("picture label", q["html"])
        for w in W:
            if w == want: problem("wrong plural option is right", w)
        if nw < 2: problem("plural needs 2+ wrong options", one)
    elif t == "add":
        want = add_rule(d["w"], d["e"])
        if want != a: problem("ending", d["w"], d["e"], a, "rule says", want)
        if not known(a): problem("ending answer not in dictionary", a)
        for w in W:
            if w == want: problem("wrong ending option is right", w)
    else:
        problem("unknown type", t)

# ---------- full pass over the data block ----------
if D:
    for w, s, wr, tip in D["spell"]:
        if s.count("___") != 1 or len(set(wr)) != 3 or not known(w): problem("DATA spell", w)
        for x in wr:
            if known(x): problem("DATA spell wrong is a word", x)
    for s, a, g in D["mix"]:
        if s.count("___") != 1 or g not in GROUPS or a.lower() not in GROUPS[g]: problem("DATA mix", s)
        want = mix_rule(g, s)
        if want is None or want.lower() != a.lower(): problem("DATA mix rule", s, a, want)
    for one, many, emo in D["plural"]:
        if INF.plural(one) != many: problem("DATA plural", one, many, INF.plural(one))
    for w, e, a in D["add"]:
        if add_rule(w, e) != a: problem("DATA add", w, e, a, add_rule(w, e))
    used = {g for _, _, g in D["mix"]}
    if used != set(GROUPS): problem("DATA mix groups not all used", set(GROUPS) - used)
print(n, "questions,", len(seen), "different,", bad, "problems")
sys.exit(1 if bad else 0)
