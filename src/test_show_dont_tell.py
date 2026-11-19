#!/usr/bin/env python3
"""Independent checker for Show, Don't Tell (JC English Order 9, personal & descriptive writing).
It does not trust the game's answers: it re-derives each one with its own rules.
  - feelings     its own body-language clue lexicon (FEEL, regexes): a "show" line must hit exactly ONE feeling
                 and name NO feeling word (NAMES); a "tell" line names the feeling
  - strong verbs its own verb → manner map (VERB) and clue words in the sentence (CUE): exactly one manner
                 in the sentence, the answer's manner matches it, every wrong verb belongs to the same weak verb
                 but has a different manner
  - zoom in      spaCy: counts detail words (nouns, names, numbers, adjectives, not vague words like nice/thing);
                 the answer must have at least 2 more than every wrong option
  - five senses  Technique Spotter's sense lists (imported from src/test_technique_spotter.py)
Setup (new session): pip install --break-system-packages spacy pronouncing + the en_core_web_sm 3.8.0 wheel.
Usage: N=400 node src/test_show_dont_tell.js show-dont-tell.html > /tmp/sd.jsonl && python3 src/test_show_dont_tell.py /tmp/sd.jsonl show-dont-tell.html
       python3 src/test_show_dont_tell.py - <page or json>   (data pass only)"""
import sys, os, json, re, html as H
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from test_technique_spotter import senses, nlp, SLAB

FL = {"hap": "😊 Happy", "exc": "🤩 Excited", "sca": "😨 Scared", "ner": "😬 Nervous",
      "ang": "😠 Angry", "sad": "😢 Sad", "bor": "🥱 Bored", "emb": "😳 Embarrassed"}
CLOSE = [{"hap", "exc"}, {"sca", "ner"}, {"ner", "emb"}]
FEEL = {
    "hap": [r"\bgrin", r"\bbeam", r"\bsmil", r"\blaugh", r"\bhumm", r"\bwhistl", r"\bskipp"],
    "exc": [r"\bbounc", r"\bsqueal", r"jump\w* up and down", r"couldn't sit still", r"counted down",
            r"ran to the window"],
    "sca": [r"\bfroze", r"heart (pounded|hammered)", r"\bgasp", r"hairs on the back", r"\bscream", r"\btrembl"],
    "ner": [r"bit my nails", r"\bfidget", r"\bsweaty", r"swallowed hard", r"butterflies", r"tapped my foot"],
    "ang": [r"\bclench", r"\bslamm", r"\bstomp", r"gritted", r"\bglar", r"\bkicked"],
    "sad": [r"\btears", r"\bsniff", r"\bsob", r"lump in my throat", r"\bslump", r"wiped my eyes"],
    "bor": [r"\byawn", r"\bclock", r"rested my chin", r"\bdoodl", r"ceiling tiles", r"droned"],
    "emb": [r"\bblush", r"cheeks (burned|went red|turned red)", r"ground to swallow", r"stared at my shoes",
            r"look anyone in the eye"],
}
NAMES = r"\b(happy|glad|joyful|excited|scared|afraid|frightened|terrified|nervous|worried|anxious|angry|furious|cross|mad|sad|upset|unhappy|bored|embarrassed|ashamed)\b"
VERB = {  # strong verb → (weak verb it replaces, manner)
    "trudged": ("walked", "tired"), "plodded": ("walked", "tired"), "crept": ("walked", "quiet"),
    "tiptoed": ("walked", "quiet"), "raced": ("walked", "fast"), "dashed": ("walked", "fast"),
    "sprinted": ("walked", "fast"), "strolled": ("walked", "relaxed"), "wandered": ("walked", "relaxed"),
    "stormed": ("walked", "angry"), "stomped": ("walked", "angry"),
    "whispered": ("said", "quiet"), "shouted": ("said", "loud"), "yelled": ("said", "loud"),
    "muttered": ("said", "grumpy"), "grumbled": ("said", "grumpy"), "sobbed": ("said", "upset"),
    "giggled": ("said", "funny"), "stammered": ("said", "nervous"),
    "glanced": ("looked", "quick"), "stared": ("looked", "long"), "gazed": ("looked", "long"),
    "peered": ("looked", "dim"), "glared": ("looked", "angry"),
    "gobbled": ("ate", "hungry"), "wolfed": ("ate", "hungry"), "nibbled": ("ate", "small"), "slurped": ("ate", "soup"),
}
CUE = {
    "tired": r"exhausted|worn out|\btired", "quiet": r"asleep|nobody would wake|without a sound",
    "fast": r"late for|about to ring|in a hurry", "relaxed": r"no rush|plenty of time",
    "angry": r"furious|in a temper", "loud": r"across the pitch|from upstairs|over the noise",
    "grumpy": r"under (his|her|my) breath", "upset": r"tears|crying", "funny": r"tickl", "nervous": r"nervously",
    "quick": r"for a second", "long": r"for ages|for a long time", "dim": r"\bfog|keyhole|\bdark\b",
    "hungry": r"starving", "small": r"wasn't hungry|not hungry|a corner of", "soup": r"\bsoup|noodles",
}
VAGUE = {"nice", "good", "bad", "big", "small", "lovely", "great", "thing", "things", "stuff", "something",
         "some", "really", "very", "strange", "weird", "cool", "okay", "lot", "cute", "sweet", "sort", "kind", "bit", "quite"}

def feelings(s):
    s = s.lower()
    return {k for k, L in FEEL.items() if any(re.search(p, s) for p in L)}
def names_feeling(s): return re.findall(NAMES, s.lower())
def close(a, b): return {a, b} in CLOSE
def cue(s):
    return {m for m, p in CUE.items() if re.search(p, s.lower())}
def detail(phrase):
    d = nlp(phrase)
    return sum(1 for t in d if t.pos_ in ("NOUN", "PROPN", "NUM", "ADJ") and t.lower_ not in VAGUE and t.lemma_.lower() not in VAGUE)
def text(h): return H.unescape(re.sub("<[^>]+>", " ", h))

def check_show(k, s):
    e = []
    f = feelings(s)
    if f != {k}: e.append(f"clues {sorted(f)} in “{s}”, not just {k}")
    if names_feeling(s): e.append(f"“{s}” names a feeling: {names_feeling(s)}")
    if not s.startswith(("I ", "My ", "The ", "Tears", "There")): e.append(f"“{s}” not personal")
    return e
def check_verb(s, weak, ans):
    e = []
    c = cue(s)
    if len(c) != 1: e.append(f"cues {sorted(c)} in “{s}”")
    if ans not in VERB: return e + [f"{ans} not in VERB"]
    if VERB[ans][0] != weak: e.append(f"{ans} doesn't replace {weak}")
    if c and VERB[ans][1] not in c: e.append(f"“{s}” cues {sorted(c)}, {ans} is {VERB[ans][1]}")
    if s.count("___") != 1: e.append(f"gap count in “{s}”")
    return e
def check_zoom(fr, ans, wrong):
    e = []
    a = detail(ans)
    for w in wrong:
        if detail(w) > a - 2: e.append(f"“{w}” ({detail(w)}) nearly as detailed as “{ans}” ({a})")
    if len(set(wrong + [ans])) != 4: e.append("repeated option")
    return e
def check_sense(s, k):
    f = senses(s)
    return [] if f == {k} else [f"sense words {sorted(f)} in “{s}”, not just {k}"]

def load(path):
    raw_src = open(path, encoding="utf-8").read()
    return json.loads(raw_src.split("/*DATA*/")[1].split("/*END*/")[0]) if "/*DATA*/" in raw_src else json.loads(raw_src)

bad = n = 0
if __name__ == "__main__":
    D = load(sys.argv[2] if len(sys.argv) > 2 else sys.argv[1])
    SHOWS = [s for k, s in D["show"]]
    seen = set()
    if sys.argv[1] != "-":
        for raw in open(sys.argv[1]):
            q = json.loads(raw); n += 1; d = q["data"]; t = d["t"]; opts = [q["answer"]] + q["wrong"]
            def fail(msg):
                global bad; bad += 1
                if bad < 30: print("FAIL", t, msg, "|", q["en"], "|", opts)
            nw = q.get("nw") or 3
            if len(q["wrong"]) != nw: fail("wrong option count")
            if len(set(o.lower() for o in opts)) != len(opts): fail("duplicate option")
            if any(re.search(r"undefined|NaN|null", o) for o in opts + [q["en"], q["why"], text(q["html"])]): fail("bad text")
            shown = text(q["html"])
            if t == "show":   # tell card shown; pick the line that SHOWS that feeling
                k = [k for k, v in FL.items() if v.split()[1].lower() in shown.lower()]
                if len(k) != 1: fail("tell card names no single feeling"); continue
                k = k[0]
                f = feelings(q["answer"])
                if f != {k} or names_feeling(q["answer"]): fail(f"answer clues {f}, names {names_feeling(q['answer'])}")
                tells = [w for w in q["wrong"] if names_feeling(w)]
                if len(tells) != 1: fail(f"{len(tells)} telling options")
                for w in q["wrong"]:
                    if w in tells: continue
                    g = feelings(w)
                    if k in g or any(close(k, x) for x in g) or len(g) != 1: fail(f"wrong “{w}” shows {g}")
            elif t == "feel":
                f = feelings(d["s"])
                if len(f) != 1 or q["answer"] != FL[list(f)[0]]: fail(f"clues {f}")
                k = list(f)[0]
                for w in q["wrong"]:
                    x = [a for a, v in FL.items() if v == w]
                    if len(x) != 1 or x[0] == k or close(k, x[0]): fail(f"wrong {w}")
                if d["s"] not in shown: fail("line not shown")
            elif t == "verb":
                s = d["s"]; c = cue(s)
                if len(c) != 1: fail(f"cues {c}"); continue
                if VERB.get(q["answer"], ("", ""))[1] not in c: fail(f"answer manner {VERB.get(q['answer'])} vs cue {c}")
                for w in q["wrong"]:
                    if w not in VERB or VERB[w][0] != d["w"] or VERB[w][1] in c: fail(f"wrong {w}")
                if len({VERB[w][1] for w in q["wrong"] if w in VERB}) != len(q["wrong"]): fail("two wrong verbs mean the same")
                if s.replace("___", "").split()[0] not in shown: fail("sentence not shown")
            elif t == "zoom":
                a = detail(q["answer"])
                for w in q["wrong"]:
                    if detail(w) > a - 2: fail(f"“{w}” nearly as detailed")
            elif t == "sense":
                f = senses(d["s"])
                if len(f) != 1 or q["answer"] != SLAB[list(f)[0]]: fail(f"sense rule finds {f}")
                if d["s"] not in shown: fail("line not shown")
            seen.add((t, d.get("s") or q["answer"]))
        print(f"{n} questions, {bad} problems, {len(seen)} different items")

    errs = []
    for k, s in D["show"]: errs += check_show(k, s)
    for s, w, a in D["verb"]: errs += check_verb(s, w, a)
    for fr, a, wrong in D["zoom"]: errs += check_zoom(fr, a, wrong)
    for s, k in D["senses"]: errs += check_sense(s, k)
    cnt = {k: sum(1 for x in D["show"] if x[0] == k) for k in FL}
    if min(cnt.values()) < 4: errs.append(f"too few show lines: {cnt}")
    if len(set(SHOWS)) != len(SHOWS): errs.append("duplicate show line")
    print("data block:", len(errs), "problems")
    for x in errs[:40]: print("  ", x)
    bad += len(errs)
    sys.exit(1 if bad else 0)
