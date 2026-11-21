#!/usr/bin/env python3
"""Independent checker for Compare Cards (Order 30, comparing texts & characters).
It works out every text's features from the WORDS of its lines with its own word lists
(narrator, time, place, ending, main character) and never trusts the game's `f` keys
(it only compares them with what it found). Then it re-derives every sampled question.
Usage: N=400 node src/test_compare_cards.js compare-cards.html > /tmp/cc.jsonl && python3 src/test_compare_cards.py /tmp/cc.jsonl compare-cards.html
       python3 src/test_compare_cards.py - <page or json>   (data pass only)  — no spaCy needed."""
import json, re, sys, html as H
from collections import Counter

FIRST = r"\b(I|my|me|we|our|us)\b"
LISTS = {
 "t": {"night": r"\b(night|midnight|moon|stars?|dark|torch)\b", "day": r"\b(morning|sun|sunshine|noon|afternoon|daylight)\b"},
 "pl": {"sea": r"\b(sea|beach|waves?|harbour|pier|sand)\b", "farm": r"\b(farm|field|hens?|cows?|tractor|barn)\b",
        "town": r"\b(street|traffic|shop|square|bus stop)\b", "school": r"\b(school|classroom|corridor|teacher)\b",
        "mountain": r"\b(mountain|summit|ridge|slopes?)\b", "home": r"\b(kitchen|bedroom|sofa|stairs)\b"},
 "e": {"happy": r"\b(smiled|grinned|laughed|cheered|beamed|hugged)\b", "sad": r"\b(cried|tears|sobbed|alone|wept|sighed)\b"},
 "tr": {"kind": r"\b(shared|helped|offered|gave)\b", "brave": r"\b(dived|climbed down|stepped forward)\b",
        "determined": r"\b(kept going|tried again)\b", "honest": r"\b(owned up|admitted|the truth|handed (it )?back)\b"},
}
LABEL = {
 ("p", "1"): "🙋 First person", ("p", "3"): "👀 Third person",
 ("t", "night"): "🌙 Set at night", ("t", "day"): "☀️ Set by day",
 ("pl", "sea"): "🌊 By the sea", ("pl", "farm"): "🐄 On a farm", ("pl", "town"): "🏙️ In a town",
 ("pl", "school"): "🏫 At school", ("pl", "mountain"): "⛰️ On a mountain", ("pl", "home"): "🏠 At home",
 ("e", "happy"): "😊 Happy ending", ("e", "sad"): "😢 Sad ending",
 ("tr", "kind"): "🤝 Kind hero", ("tr", "brave"): "🦁 Brave hero", ("tr", "determined"): "💪 Determined hero", ("tr", "honest"): "💯 Honest hero",
}
BYLAB = {v: k for k, v in LABEL.items()}
# phrases a comparison sentence can use, read back to (category, value)
PHRASE = [
 (r"told in the first person", ("p", "1")), (r"told in the third person", ("p", "3")),
 (r"set at night", ("t", "night")), (r"set during the day", ("t", "day")),
 (r"set by the sea", ("pl", "sea")), (r"set on a farm", ("pl", "farm")), (r"set in a town", ("pl", "town")),
 (r"set in a school", ("pl", "school")), (r"set on a mountain", ("pl", "mountain")), (r"set at home", ("pl", "home")),
 (r"end(s)? happily", ("e", "happy")), (r"end(s)? sadly", ("e", "sad")),
 (r"ha(s|ve) a kind main character", ("tr", "kind")), (r"ha(s|ve) a brave main character", ("tr", "brave")),
 (r"ha(s|ve) a determined main character", ("tr", "determined")), (r"ha(s|ve) an honest main character", ("tr", "honest")),
]
SIM = ["Similarly,", "Likewise,", "In the same way,"]
CON = ["However,", "In contrast,", "On the other hand,"]
CMP = r"\b(both|whereas|while|however|similarly|likewise|unlike|in contrast)\b"
VENN = ["🅰️ Only A", "🅱️ Only B", "🤝 Both"]

def features(T):
    txt = " ".join(T["lines"]); f = {}
    f["p"] = "1" if re.search(FIRST, txt) else "3"
    for c in ("t", "pl", "tr"):
        hits = [v for v, rx in LISTS[c].items() if re.search(rx, txt, re.I)]
        assert len(hits) == 1, (T["title"], c, hits)
        f[c] = hits[0]
    hits = [v for v, rx in LISTS["e"].items() if re.search(rx, T["lines"][-1], re.I)]
    assert len(hits) == 1, (T["title"], "ending", hits)
    f["e"] = hits[0]
    return f

def load(path):
    s = open(path, encoding="utf-8").read()
    if path.endswith(".json"): return json.loads(s)
    return json.loads(s.split("/*DATA*/", 1)[1].split("/*END*/", 1)[0])

def data_pass(D):
    F = {}
    titles = [T["title"] for T in D["texts"]]
    assert len(set(titles)) == len(titles), "titles not unique"
    for T in D["texts"]:
        assert len(T["lines"]) == 3, T["title"]
        f = features(T)
        assert f == T["f"], ("keys don't match the words", T["title"], f, T["f"])
        F[T["title"]] = f
    for c in ("p", "t", "e", "tr"):
        cnt = Counter(f[c] for f in F.values())
        assert min(cnt.values()) >= 3 and len(cnt) == len({k for k in LABEL if k[0] == c}), (c, cnt)
    return F

def titles_in(s, F):
    return [t for t in F if "“" + t + "”" in s]

def claims(clause):
    return [cv for rx, cv in PHRASE if re.search(rx, clause)]

def sentence_ok(s, F):
    """A good comparison: names both texts, uses a comparing word, and every claim is true."""
    ts = titles_in(s, F)
    if len(ts) != 2 or not re.search(CMP, s, re.I): return False
    if re.search(r"\bwhereas\b|\bwhile\b", s):
        a, b = re.split(r",? (?:whereas|while) ", s, maxsplit=1)
        ta, tb = titles_in(a, F), titles_in(b, F)
        ca, cb = claims(a), claims(b)
        if len(ta) != 1 or len(tb) != 1 or len(ca) != 1 or len(cb) != 1 or ca[0][0] != cb[0][0]: return False
        return F[ta[0]][ca[0][0]] == ca[0][1] and F[tb[0]][cb[0][0]] == cb[0][1] and ca[0][1] != cb[0][1]
    if re.search(r"\bboth\b", s):
        cs = claims(s)
        return len(cs) == 1 and all(F[t][cs[0][0]] == cs[0][1] for t in ts)
    return False

def check(q, F):
    m, d, a, W = q["mode"], q["data"], q["answer"], q["wrong"]
    assert len(W) == q["nw"] and len(set(W + [a])) == len(W) + 1, "options not distinct / wrong count"
    t = d["t"]
    if t in ("both", "venn", "best"):
        ts = titles_in(H.unescape(q["html"]), F)
        assert len(ts) == 2, ("cards", ts)
        A, B = d["a"], d["b"]
        assert set(ts) == {A, B}, "cards don't match"
        cardA = re.search(r'cc-card a.*?</div>', q["html"], re.S).group(0)
        assert "“" + A + "”" in H.unescape(cardA), "card A isn't text A"
    if t == "both":
        c, v = BYLAB[a]; assert F[A][c] == v and F[B][c] == v, ("answer not shared", a)
        for w in W:
            c, v = BYLAB[w]; assert not (F[A][c] == v and F[B][c] == v), ("wrong option is shared too", w)
    elif t == "venn":
        lab = H.unescape(re.search(r'class="cc-st">(.*?)</div>', q["html"]).group(1))
        c, v = BYLAB[lab]; ina, inb = F[A][c] == v, F[B][c] == v
        assert ina or inb, ("label fits neither", lab)
        exp = VENN[2] if ina and inb else VENN[0] if ina else VENN[1]
        assert a == exp, ("venn", lab, a, exp)
        assert set(W + [a]) == set(VENN)
    elif t == "link":
        s = H.unescape(re.sub(r"<[^>]+>", "", q["html"]))
        one, two = s.split("?", 1)
        ta, tb = titles_in(one, F), titles_in(two, F)
        ca, cb = claims(one), claims(two)
        assert len(ta) == len(tb) == len(ca) == len(cb) == 1 and ta != tb and ca[0][0] == cb[0][0], ("link parse", s)
        assert F[ta[0]][ca[0][0]] == ca[0][1] and F[tb[0]][cb[0][0]] == cb[0][1], ("link claim false", s)
        same = ca[0][1] == cb[0][1]
        assert a in (SIM if same else CON), ("link answer", s, a)
        assert all(w in (CON if same else SIM) for w in W), ("link wrong", W)
    elif t == "best":
        assert sentence_ok(a, F), ("best answer fails", a)
        for w in W: assert not sentence_ok(w, F), ("wrong comparison passes", w)
    else:
        raise AssertionError("unknown type " + t)

def main():
    src, page = sys.argv[1], sys.argv[2]
    F = data_pass(load(page))
    print(f"data pass OK: {len(F)} texts")
    if src == "-": return
    n = bad = 0; longest = Counter(); tot = Counter()
    for line in open(src, encoding="utf-8"):
        q = json.loads(line); n += 1
        try: check(q, F)
        except AssertionError as e:
            bad += 1
            if bad <= 12: print("PROBLEM", q["mode"], q["data"].get("t"), e)
        if q["data"].get("t") == "best":
            tot["best"] += 1; longest["best"] += len(q["answer"]) > max(len(w) for w in q["wrong"])
    print(f"{n} questions, {bad} problems")
    if tot["best"]: print(f"best: answer is the longest option {100*longest['best']//tot['best']} %")
    sys.exit(1 if bad or n == 0 else 0)

if __name__ == "__main__":
    main()
