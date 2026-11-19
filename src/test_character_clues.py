#!/usr/bin/env python3
"""Independent checker for Character Clues (JC English Order 5, the novel 1: character).
It does not trust the game's answers: it re-derives each one from the TEXT with its own rules.
  - STEAL method of a line   its own rules: words in “ ” with the character as speaker = speech (another speaker = effect on others);
                             a be/wear/have line about the character's appearance = looks; a line whose subject (spaCy) is someone
                             else = effect on others; a thinking verb = thoughts; otherwise = actions.
  - Traits                   its own clue-word lexicon (TRAIT below): the trait must be found in the answer line's quote and in no
                             other line of the extract; wrong trait options must not be found anywhere in the extract, and look-alike
                             traits (CLOSE) are never offered as wrong.
  - Which line / best quote  the trait's clue words sit in the answer line / quote and in no other option.
Setup (new session): pip install --break-system-packages spacy + the en_core_web_sm 3.8.0 wheel.
Usage: N=400 node src/test_character_clues.js character-clues.html > /tmp/cc.jsonl && python3 src/test_character_clues.py /tmp/cc.jsonl character-clues.html"""
import sys, json, re, html as H
import spacy
nlp = spacy.load("en_core_web_sm")

TRAIT = {   # label -> clue words / phrases that show it
    "🤝 Kind": ["gave half", "help", "cup of tea", "shared", "comforted"],
    "🦁 Brave": ["waded in", "walked on stage", "dived in", "stood up to"],
    "🙈 Shy": ["going red", "stared at her shoes", "whispered", "blushed", "mumbled"],
    "📣 Bossy": ["nobody talks", "told them exactly", "ordered"],
    "🙅 Selfish": ["biggest slice", "bought both", "for himself", "for herself"],
    "🛋️ Lazy": ["stayed in bed", "lying on the crash mat", "couldn't be bothered"],
    "💯 Honest": ["handed it in", "owned up", "told the truth"],
    "😒 Jealous": ["scowled", "should have been me"],
    "😂 Funny": ["laughed", "laugh", "joke"],
    "🧠 Clever": ["worked out", "spotted the mistake", "solved"],
    "🙄 Rude": ["rolled her eyes", "rolled his eyes", "whatever", "slammed"],
}
CLOSE = {"📣 Bossy": {"🙄 Rude"}, "🙄 Rude": {"📣 Bossy", "🙅 Selfish"}, "🙅 Selfish": {"😒 Jealous", "🙄 Rude"}, "😒 Jealous": {"🙅 Selfish"}}
METHOD = {"say": "💬 Speech", "think": "💭 Thoughts", "effect": "👥 Effect on others", "act": "🎬 Actions", "look": "👀 Looks"}
THINKF = {"thought", "wondered", "wished", "knew", "hoped", "remembered", "worried", "realised"}
THINK = {"think", "wonder", "wish", "know", "hope", "remember", "worry", "realise", "realize"}
LOOKW = ["jumper", "shoelace", "runners", "hood", "glasses", "shirt", "chin", "face", "lips", "jacket", "armband", "hair", "freckles", "uniform"]
SAYV = {"say", "shout", "mutter", "whisper", "snap", "ask", "reply", "yell", "call", "order"}

def traits(s):
    s = s.lower(); found = set()
    for f, L in TRAIT.items():
        for p in L:
            if p in s: found.add(f)
    return found
def method(line, who, pr):
    me = {who.lower(), pr.lower()}
    quotes = re.findall(r"“[^”]*”", line)
    if quotes:
        rest = re.sub(r"“[^”]*”", " ", line)
        d = nlp(rest)
        for t in d:
            if t.lemma_.lower() in SAYV:
                subj = [c.text.lower() for c in t.children if c.dep_ in ("nsubj",)]
                if subj: return "say" if subj[0] in me else "effect"
        return "?"
    d = nlp(line)
    root = [t for t in d if t.dep_ == "ROOT"][0]
    subj = [c for c in root.children if c.dep_ in ("nsubj", "nsubjpass")]
    if not subj: return "?"
    s = subj[0]
    owner = s.text.lower() in me or any(c.dep_ == "poss" and c.text.lower().replace("'s", "") in me | {"his", "her"} for c in s.children)
    if root.lemma_ in ("be", "wear", "have") and any(w in line.lower() for w in LOOKW) and owner:
        return "look"
    if s.text.lower() not in me: return "effect"
    if root.lemma_ in THINK or root.text.lower() in THINKF: return "think"   # spaCy lemmatises "hoped" as "hop"
    return "act"

D = json.loads(open(sys.argv[2], encoding="utf-8").read().split("/*DATA*/")[1].split("/*END*/")[0])
errs = []
# ---------- full pass over the data ----------
for n, T in enumerate(D["texts"]):
    tag = f"text {n} ({T['who']})"
    if not (len(T["lines"]) == len(T["how"]) == len(T["q"]) == 4): errs.append(tag + ": not 4 lines/how/q")
    for i, l in enumerate(T["lines"]):
        m = method(l, T["who"], T["pr"])
        if m != T["how"][i]: errs.append(f"{tag} line {i+1}: method {T['how'][i]} but rules say {m}: {l}")
        hits = [j for j, l2 in enumerate(T["lines"]) if T["q"][i].lower() in l2.lower()]
        if hits != [i]: errs.append(f"{tag}: quote “{T['q'][i]}” found in lines {[h+1 for h in hits]}")
    for tr, ln in T["traits"]:
        lab = [k for k in TRAIT if k.split(" ")[1].lower() == tr][0]
        if lab not in traits(T["q"][ln - 1]): errs.append(f"{tag}: quote of line {ln} doesn't show {tr}")
        where = [j + 1 for j, l in enumerate(T["lines"]) if lab in traits(l)]
        if where != [ln]: errs.append(f"{tag}: {tr} found in lines {where}, not only {ln}")
    for j, l in enumerate(T["lines"]):
        if len(traits(l)) > 1: errs.append(f"{tag} line {j+1}: two traits {traits(l)}")

def card_lines(h):
    out, hl = [], None
    for m in re.finditer(r'<p( class="hl")?><b>(\d)</b>(.*?)</p>', h):
        out.append(H.unescape(m.group(3)))
        if m.group(1): hl = int(m.group(2))
    return out, hl
def claim_trait(h):
    m = re.search(r'ch-claim">🔎 (.*?) is (\w+)\.</p>', h)
    return m.group(1), [k for k in TRAIT if k.split(" ")[1].lower() == m.group(2)][0]

n = 0
for row in open(sys.argv[1], encoding="utf-8"):
    q = json.loads(row); n += 1; t = q["data"]["t"]; h = q["html"]; e = []
    lines, hl = card_lines(h)
    T = D["texts"][q["data"]["x"]]
    if lines != T["lines"]: e.append("card text differs from data")
    opts = [q["answer"]] + q["wrong"]
    if len(set(opts)) != len(opts): e.append("duplicate options")
    if t == "line":
        who, lab = claim_trait(h)
        found = [i + 1 for i, l in enumerate(lines) if lab in traits(l)]
        if found != [int(q["answer"].split()[1])]: e.append(f"trait {lab} in lines {found}, answer {q['answer']}")
        if len(q["wrong"]) != 3: e.append("not 3 wrong")
    elif t == "how":
        m = method(lines[hl - 1], T["who"], T["pr"])
        if METHOD.get(m) != q["answer"]: e.append(f"rules say {m}, answer {q['answer']}")
        if len(q["wrong"]) != 4 or not set(q["wrong"]) <= set(METHOD.values()): e.append("wrong options not the 4 other methods")
    elif t == "trait":
        f = traits(lines[hl - 1])
        if f != {q["answer"]}: e.append(f"highlighted line shows {f}, answer {q['answer']}")
        alltr = set().union(*[traits(l) for l in lines])
        for w in q["wrong"]:
            if w in alltr: e.append(f"wrong option {w} is shown in the extract")
            if w in CLOSE.get(q["answer"], set()): e.append(f"look-alike {w} offered")
            if w not in TRAIT: e.append(f"unknown trait {w}")
        if len(q["wrong"]) != 3: e.append("not 3 wrong")
    elif t == "quote":
        who, lab = claim_trait(h)
        if lab not in traits(q["answer"]): e.append(f"answer quote doesn't show {lab}")
        for w in q["wrong"]:
            if lab in traits(w): e.append(f"wrong quote {w} also shows {lab}")
        for o in opts:
            if not any(o.strip("“”").lower() in l.lower() for l in lines): e.append(f"quote {o} not in the extract")
        if len(q["wrong"]) != 3: e.append("not 3 wrong")
    if e: errs.append(f"[{q['mode']}] {q['en']} → {q['answer']}: " + "; ".join(e))
for x in sorted(set(errs))[:60]: print("PROBLEM", x)
print(f"{n} questions checked, {len(set(errs))} problems")
sys.exit(1 if errs else 0)
