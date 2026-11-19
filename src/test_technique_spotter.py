#!/usr/bin/env python3
"""Independent checker for Technique Spotter (JC English Order 8, poetry 1: imagery & sound).
It does not trust the game's answers: it re-derives each one from the LINE with its own rules.
  - simile          spaCy: "like" used as a preposition, or "as <adjective> as"
  - metaphor        spaCy: a form of "be" with a noun subject and a noun after it (attr), and no simile
  - personification spaCy: a non-human noun as the subject of a human action verb (HUMAN list)
  - alliteration    3+ content words starting with the same sound inside any 4 content words in a row
  - onomatopoeia    its own list of sound words (SOUND)
  - rhyme           two lines split by " / " whose last words rhyme (CMU dictionary, pronouncing package)
  - senses          its own word lists per sense (SENSE): exactly one sense in the line
  - what's compared spaCy: subject + the noun after like / the second as / the noun after "be"
Every technique item must show exactly ONE technique by these rules; every poem line too (or none).
Setup (new session): pip install --break-system-packages spacy pronouncing + the en_core_web_sm 3.8.0 wheel.
Usage: N=400 node src/test_technique_spotter.js technique-spotter.html > /tmp/ts.jsonl && python3 src/test_technique_spotter.py /tmp/ts.jsonl technique-spotter.html
       python3 src/test_technique_spotter.py - <page or json>   (data pass only)"""
import sys, json, re, html as H
import spacy, pronouncing
nlp = spacy.load("en_core_web_sm")

LAB = {"sim": "🤝 Simile", "met": "🪞 Metaphor", "per": "🗣️ Personification", "all": "🔤 Alliteration",
       "ono": "💥 Onomatopoeia", "rhy": "🎵 Rhyme"}
SLAB = {"see": "👀 Sight", "hear": "👂 Sound", "smell": "👃 Smell", "taste": "👅 Taste", "touch": "✋ Touch"}
HUMAN = {"whisper", "smile", "dance", "wave", "shout", "complain", "sing", "wink", "weep", "scream", "giggle", "tickle",
         "shiver", "refuse", "laugh", "cry", "sigh", "grumble", "yawn", "frown", "sulk", "chat", "argue", "kiss", "hug"}
PERSON = {"man", "woman", "boy", "girl", "brother", "sister", "mam", "dad", "granny", "grandad", "teacher", "friend",
          "people", "person", "child", "children", "crowd", "driver", "everyone", "nobody", "someone"}
SOUND = {"buzz", "hiss", "sizzle", "pop", "crash", "drip", "crackle", "splash", "thud", "whoosh", "creak", "crunch", "woof",
         "squawk", "bang", "boom", "click", "clang", "ding", "fizz", "gurgle", "munch", "rattle", "rustle", "screech",
         "slurp", "snap", "tick", "tock", "whizz", "zoom", "plop", "squelch", "honk", "beep", "purr", "moo", "quack",
         "oink", "miaow", "thump", "clatter", "bong", "splat", "whack", "sniff", "hum", "tap"}
SENSE = {
    "see": ["glow", "glitter", "golden", "gold", "light", "bright", "red", "pink", "orange", "green", "shadow", "sparkle",
            "shine", "shone", "colour", "dark", "blue", "grey", "yellow", "purple", "gleam", "flash"],
    "hear": ["thunder", "rumble", "roar", "rang", "ring", "echo", "chatter", "growl", "footstep", "noise", "loud", "whisper",
             "quiet", "silent", "sang", "song", "bang", "crash", "scream", "shout", "hum"],
    "smell": ["smell", "stank", "stink", "scent", "perfume", "reek", "whiff", "pong", "stench"],
    "taste": ["taste", "sour", "sweet", "salty", "salt", "bitter", "spicy", "delicious", "tasty", "flavour"],
    "touch": ["rough", "cold", "icy", "stung", "sting", "soft", "warm", "hot", "wet", "soggy", "burn", "smooth", "sticky",
              "prickly", "freezing", "damp"],
}
SMALL = {"the", "a", "an", "and", "of", "in", "on", "to", "at", "for", "with", "from", "its", "it", "is", "was", "my", "her",
         "his", "their", "our", "as", "by", "up", "all", "every", "then", "that", "this", "i", "we", "they", "he", "she", "me",
         "us", "are", "were", "be", "so", "too", "into", "out", "over", "but", "or", "had", "has", "have"}

memo = {}
def doc(s):
    if s not in memo: memo[s] = nlp(s)
    return memo[s]

def is_simile(s):
    d = doc(s)
    if any(t.lower_ == "like" and t.pos_ in ("ADP", "SCONJ") for t in d): return True
    return bool(re.search(r"\bas \w+ as\b", s.lower()))
def is_metaphor(s):
    if is_simile(s): return False
    for t in doc(s):
        if t.lemma_ == "be":
            subj = [c for c in t.children if c.dep_ == "nsubj" and c.pos_ in ("NOUN", "PROPN")]
            attr = [c for c in t.children if c.dep_ == "attr" and c.pos_ == "NOUN"]
            if subj and attr and subj[0].lemma_.lower() != attr[0].lemma_.lower(): return True
    return False
def is_personification(s):
    for t in doc(s):
        if t.pos_ == "VERB" and t.lemma_.lower() in HUMAN:
            subj = [c for c in t.children if c.dep_ in ("nsubj",)]
            if not subj and t.dep_ == "conj": subj = [c for c in t.head.children if c.dep_ == "nsubj"]
            if not subj and t.dep_ == "xcomp": subj = [c for c in t.head.children if c.dep_ == "nsubj"]
            if subj and subj[0].pos_ == "NOUN" and subj[0].lemma_.lower() not in PERSON: return True
    return False
def sound_of(w):
    w = w.lower()
    return w[:2] if w[:2] in ("sh", "ch", "th", "ph", "wh") else ("f" if w[:2] == "ph" else w[0])
def is_alliteration(s):
    words = [w for w in re.findall(r"[A-Za-zÁÉÍÓÚáéíóú']+", s) if w.lower() not in SMALL]
    for i in range(len(words)):
        win = {}
        for w in words[i:i + 4]: win.setdefault(sound_of(w), set()).add(w.lower())   # repeated words don't count
        if any(len(v) >= 3 for v in win.values()): return True
    return False
def is_onomatopoeia(s):
    return any(t.lemma_.lower() in SOUND or t.lower_ in SOUND for t in doc(s))
def last_word(s): return re.findall(r"[A-Za-z']+", s)[-1].lower()
def rhymes(a, b):
    a, b = a.lower(), b.lower()
    if a == b: return False
    pa, pb = pronouncing.phones_for_word(a), pronouncing.phones_for_word(b)
    if not pa or not pb: raise ValueError(f"not in the CMU dictionary: {a if not pa else b}")
    return any(pronouncing.rhyming_part(x) == pronouncing.rhyming_part(y) for x in pa for y in pb)
def is_rhyme(s):
    if " / " not in s: return False
    a, b = s.split(" / ")
    return rhymes(last_word(a), last_word(b))
RULES = {"sim": is_simile, "met": is_metaphor, "per": is_personification, "all": is_alliteration, "ono": is_onomatopoeia, "rhy": is_rhyme}
def techniques(s):
    if " / " in s:   # a couplet: rhyme, plus anything found in either line
        found = {k for k, f in RULES.items() if k != "rhy" and any(f(x) for x in s.split(" / "))}
        return found | ({"rhy"} if is_rhyme(s) else set())
    return {k for k, f in RULES.items() if f(s)}
def senses(s):
    d = doc(s); words = {t.lower_ for t in d} | {t.lemma_.lower() for t in d}
    return {k for k, L in SENSE.items() if any(w in words or any(x.startswith(w) and len(w) > 3 for x in words) for w in L)}
def compared(s):
    d = doc(s)
    def head_noun(t): return t.text if t.pos_ == "PROPN" else t.lemma_.lower()
    for t in d:
        if t.lower_ == "like" and t.pos_ in ("ADP", "SCONJ"):
            obj = [c for c in t.children if c.dep_ == "pobj"]
            v = t.head
            while v.dep_ not in ("ROOT",) and not any(c.dep_ == "nsubj" for c in v.children): v = v.head
            subj = [c for c in v.children if c.dep_ == "nsubj"]
            if obj and subj: return head_noun(subj[0]), obj[0].text.lower()
    m = re.search(r"\bas \w+ as an? (\w+)", s)
    if m:
        root = [t for t in d if t.dep_ == "ROOT"][0]
        subj = [c for c in root.children if c.dep_ == "nsubj"]
        if subj: return head_noun(subj[0]), m.group(1).lower()
    for t in d:
        if t.lemma_ == "be":
            subj = [c for c in t.children if c.dep_ == "nsubj"]; attr = [c for c in t.children if c.dep_ == "attr"]
            if subj and attr: return head_noun(subj[0]), attr[0].text.lower()
    return None
def same_word(a, b):
    a, b = a.lower(), b.lower()
    return a == b or a.rstrip("s") == b.rstrip("s")
def text(h): return H.unescape(re.sub("<[^>]+>", " ", h))

def check_spot(s, k):
    f = techniques(s)
    return [] if f == {k} else [f"rules find {sorted(f)} in “{s}”, not just {k}"]
def check_sense(s, k):
    f = senses(s)
    return [] if f == {k} else [f"sense words {sorted(f)} in “{s}”, not just {k}"]
def check_comp(s, a, b):
    c = compared(s)
    if not c: return [f"no comparison found in “{s}”"]
    return [] if same_word(c[0], a) and same_word(c[1], b) else [f"parse says {c}, data says {(a, b)} in “{s}”"]
def check_poem(P):
    e = []
    for i, l in enumerate(P["lines"]):
        f = techniques(l)
        if len(f) > 1: e.append(f"{P['k']} line {i+1} has {sorted(f)}")
    for k, ln in P["ask"]:
        hits = [i + 1 for i, l in enumerate(P["lines"]) if k in techniques(l)]
        if hits != [ln]: e.append(f"{P['k']}: {k} found in lines {hits}, not only line {ln}")
    return e
def check_rhyme(w, r, wrong):
    e = []
    if not rhymes(w, r): e.append(f"{w}/{r} don't rhyme")
    for x in wrong:
        if rhymes(w, x): e.append(f"wrong option {x} rhymes with {w}")
    if len(set(wrong + [r, w])) != 5: e.append(f"{w}: repeated words")
    return e

def load(path):
    raw_src = open(path, encoding="utf-8").read()
    return json.loads(raw_src.split("/*DATA*/")[1].split("/*END*/")[0]) if "/*DATA*/" in raw_src else json.loads(raw_src)

bad = n = 0
if __name__ == "__main__":
    D = load(sys.argv[2] if len(sys.argv) > 2 else sys.argv[1])
    SPOT = {s[0]: s for s in D["spot"]}; SEN = dict((s, k) for s, k in D["senses"]); RH = {r[0]: r for r in D["rhyme"]}
    seen = set()
    if sys.argv[1] != "-":
        for raw in open(sys.argv[1]):
            q = json.loads(raw); n += 1; d = q["data"]; t = d["t"]; opts = [q["answer"]] + q["wrong"]
            def fail(msg):
                global bad; bad += 1
                if bad < 30: print("FAIL", t, msg, "|", q["en"], "|", opts)
            if len(q["wrong"]) != 3: fail("wrong option count")
            if len(set(o.lower() for o in opts)) != len(opts): fail("duplicate option")
            if any(re.search(r"undefined|NaN|null", o) for o in opts + [q["en"], q["why"], text(q["html"])]): fail("bad text")
            shown = text(q["html"])
            if t == "spot":
                s = d["s"]; f = techniques(s)
                if len(f) != 1: fail(f"rules find {f}"); continue
                if q["answer"] != LAB[list(f)[0]]: fail(f"rule says {LAB[list(f)[0]]}")
                if any(w not in LAB.values() for w in q["wrong"]): fail("odd wrong label")
                for part in s.split(" / "):
                    if part not in shown: fail("line not shown")
            elif t == "line":
                P = D["poems"][d["x"]]; k = [k for k, v in LAB.items() if v in q["en"]]
                if len(k) != 1: fail("question names no technique"); continue
                hits = [i + 1 for i, l in enumerate(P["lines"]) if k[0] in techniques(l)]
                if hits != [int(q["answer"].split()[1])]: fail(f"rules find {k[0]} in lines {hits}")
                if sorted(opts) != ["Line 1", "Line 2", "Line 3", "Line 4"]: fail("options aren't Line 1–4")
                if not all(l in shown for l in P["lines"]): fail("poem not shown")
            elif t == "sense":
                f = senses(d["s"])
                if len(f) != 1 or q["answer"] != SLAB[list(f)[0]]: fail(f"sense rule finds {f}")
                if d["s"] not in shown: fail("line not shown")
            elif t == "comp":
                c = compared(d["s"])
                if not c: fail("no comparison parsed"); continue
                a, b = [x.strip() for x in q["answer"].split("↔")]
                if not (same_word(a, c[0]) and same_word(b, c[1])): fail(f"parse says {c}")
                for w in q["wrong"]:
                    x, y = [z.strip() for z in w.split("↔")]
                    if same_word(x, c[0]) and same_word(y, c[1]): fail("wrong option is the answer")
                if d["s"] not in shown: fail("line not shown")
            elif t == "rhyme":
                w = d["w"]
                if not rhymes(w, q["answer"]): fail("answer doesn't rhyme")
                for x in q["wrong"]:
                    if rhymes(w, x): fail(f"{x} rhymes too")
            seen.add((t, d.get("s") or d.get("w") or (d.get("x"), q["en"])))
        print(f"{n} questions, {bad} problems, {len(seen)} different items")

    errs = []   # full pass over the data block
    for item in D["spot"]:
        errs += check_spot(item[0], item[1])
        if item[1] in ("sim", "met"): errs += check_comp(item[0], item[2], item[3])
    for P in D["poems"]:
        if len(P["lines"]) != 4: errs.append(P["k"] + " not 4 lines")
        errs += check_poem(P)
    for s, k in D["senses"]: errs += check_sense(s, k)
    for w, r, wrong in D["rhyme"]: errs += check_rhyme(w, r, wrong)
    counts = {k: sum(1 for x in D["spot"] if x[1] == k) for k in LAB}
    if min(counts.values()) < 8: errs.append(f"too few items: {counts}")
    allv = [x[0] for x in D["spot"]]
    if len(set(allv)) != len(allv): errs.append("duplicate spot item")
    print("data block:", len(errs), "problems")
    for x in errs[:40]: print("  ", x)
    bad += len(errs)
    sys.exit(1 if bad else 0)
