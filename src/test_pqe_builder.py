#!/usr/bin/env python3
"""Independent checker for PQE Builder (JC English Order 29: answering on texts — point, quote, explain).
Usage: N=400 node src/test_pqe_builder.js pqe-builder.html > /tmp/pq.jsonl && python3 src/test_pqe_builder.py /tmp/pq.jsonl pqe-builder.html
       python3 src/test_pqe_builder.py - <page or json>     (data pass only)
It never trusts the game's labels: the feeling / mood a line SHOWS comes from its own clue-word lists (TEXT), the feeling a
point or explanation NAMES from a second list (NAME), and each sentence of an answer is classed point / quote / explain by its
own rules. Importable: shows, names, key_of, part, good_expl, why_bad, quote_kind, load, data_pass."""
import json, re, sys

# words in a TEXT that show a feeling / mood (the evidence)
TEXT = {
    "nervous": r"trembl\w*|shook|shaking|fidget\w*|churn\w*|swallowed hard|bit (?:her|his|my) nails",
    "angry": r"clench\w*|slammed|stormed|glared|scowl\w*|stomp\w*|threw",
    "lonely": r"alone|no one|nobody|by (?:my|him|her)self|on (?:my|his|her) own",
    "joyful": r"grin\w*|laugh\w*|danc\w*|cheer\w*|whoop\w*|giggl\w*|smil\w*|beam\w*",
    "determined": r"kept going|gritted|again and again|refused to give up",
    "kind": r"shared|helped|offered|handed|put an arm",
    "proud": r"held it up|stood (?:a little )?taller|chest out",
    "tense": r"creak\w*|footsteps|howl\w*|silence|shadow\w*",
    "gloomy": r"grey|drizzle|puddles?|fog|bare|faded|rain",
    "peaceful": r"lapped|gentl\w*|soft\w*|still|drift\w*",
}
# words a POINT or an EXPLANATION uses to name the feeling / mood
NAME = {
    "nervous": r"nervous|anxious|worried|worry|uneasy|fear",
    "angry": r"angry|furious|cross|rage|temper|anger",
    "lonely": r"lonely|alone|isolated|left out|shut out",
    "joyful": r"happy|joyful|joy|delighted|excited|overjoyed|glee",
    "determined": r"determined|give up|stubborn",
    "kind": r"kind|generous|caring|thoughtful|welcome",
    "proud": r"proud|pride",
    "tense": r"tense|tension|suspense|on edge|frightening|eerie",
    "gloomy": r"gloomy|dreary|miserable|grim",
    "peaceful": r"peaceful|calm|relaxed|restful",
}
TEXT_RE = {k: re.compile(r"\b(?:" + v + r")\b", re.I) for k, v in TEXT.items()}
NAME_RE = {k: re.compile(r"\b(?:" + v + r")\b", re.I) for k, v in NAME.items()}
HOW = re.compile(r"\b(?:shows?|suggests?|tells us|hints?|makes?|creates?|adds?)\b", re.I)
EXPL_START = re.compile(r"^(?:This|These|Here|It|Repeating|The (?:word|words|phrase|verb|adjective|repeated word|soft verb|sound|image))\b|^‘", re.I)
DQ = re.compile(r"“([^”]+)”")
SQ = re.compile(r"‘([^’]+)’")
LAB = {"p": "💡 Point", "q": "🔎 Quote", "e": "🧠 Explain"}

def shows(s): return {k for k, r in TEXT_RE.items() if r.search(s)}
def names(s): return {k for k, r in NAME_RE.items() if r.search(s)}
def key_of(s):
    n = names(s); assert len(n) == 1, ("point/question must name exactly one feeling", s, n); return n.pop()
def part(s):
    """p / q / e by the sentence's own form."""
    dq = DQ.findall(s)
    if any(len(x.split()) >= 2 for x in dq): return "q"
    if not dq and EXPL_START.search(s) and HOW.search(s): return "e"
    if not dq and not SQ.search(s) and not EXPL_START.search(s): return "p"
    return None
def why_bad(key, quote, e):
    """Reasons an explanation fails (empty list = a good explanation)."""
    bad = []
    q = [x.lower() for x in SQ.findall(e)]
    if not q: bad.append("names no word from the quote")
    elif not all(x in quote.lower() for x in q): bad.append("quotes a word that isn't in the quote")
    if not HOW.search(e): bad.append("no 'shows / suggests / makes'")
    n = names(e)
    if key not in n: bad.append("doesn't link back to the point")
    if n - {key}: bad.append("argues a different feeling")
    return bad
def good_expl(key, quote, e): return not why_bad(key, quote, e)
def quote_kind(line, key, opt):
    """good / long / misquote / nomarks"""
    m = re.fullmatch(r"“(.+)”", opt)
    if not m: return "nomarks"
    t = m.group(1)
    if t not in line: return "misquote"
    if len(t.split()) > 6: return "long"
    assert key in shows(t), ("short exact quote doesn't show the point", t, key)
    return "good"

def load(path):
    s = open(path, encoding="utf-8").read()
    if path.endswith(".json"): return json.loads(s)
    return json.loads(s.split("/*DATA*/", 1)[1].split("/*END*/", 1)[0])

def data_pass(D):
    n = 0
    for T in D["texts"]:
        assert len(T["lines"]) == len(T["q"]) == len(T["keys"]) == len(T["pts"]) == 4, T["title"]
        for i, (ln, q, k, p) in enumerate(zip(T["lines"], T["q"], T["keys"], T["pts"])):
            assert q in ln, (T["title"], q)
            sh = shows(ln)
            if k:
                assert sh == {k}, (T["title"], ln, "shows", sh, "label", k)
                assert shows(q) == {k}, (T["title"], q, shows(q))
                assert key_of(p) == k, (T["title"], p)
            else:
                assert not sh and not p, (T["title"], ln, sh)
        ks = [k for k in T["keys"] if k]
        assert len(ks) == len(set(ks)) and len(ks) >= 2, (T["title"], "one line per feeling")
        n += 1
    for a in D["answers"]:
        got = [part(s) for s in a]
        assert got == ["p", "q", "e"], (a, got)
    for p, quote, good, *bad in D["explain"]:
        k = key_of(p)
        assert good_expl(k, quote, good), (good, why_bad(k, quote, good))
        assert len(bad) == 3
        for b in bad: assert why_bad(k, quote, b), ("a wrong explanation passes", b)
    for p, line, q, mis, para in D["exact"]:
        k = key_of(p)
        assert len(line.split()) > 10, line
        assert shows(line) == {k}, (line, shows(line))
        kinds = [quote_kind(line, k, o) for o in ["“" + q + "”", "“" + line + "”", "“" + mis + "”", para]]
        assert kinds == ["good", "long", "misquote", "nomarks"], (line, kinds)
    for qn, right, wrong in D["qs"]:
        k = key_of(qn)
        assert k in names(right), (qn, right)
        assert len(wrong) == 3 and all(k not in names(w) for w in wrong), (qn, wrong)
    return n

def check(path, page):
    D = load(page); data_pass(D)
    bad = 0; cnt = {}
    for line in open(path, encoding="utf-8"):
        r = json.loads(line); d = r["data"]; t = d["t"]; cnt[t] = cnt.get(t, 0) + 1
        opts = [r["answer"]] + r["wrong"]
        try:
            assert len(set(opts)) == len(opts) == (r["nw"] or 3) + 1, "options"
            if t == "pqe":
                T = D["texts"][d["ti"]]; text = " ".join(T["lines"]); p = T["pts"][d["li"]]
                assert p and p in r["html"], "point not shown"
                assert all(l in r["html"] for l in T["lines"]), "text not shown"
                k = key_of(p)
                for o in opts:
                    m = re.fullmatch(r"“(.+)”", o); assert m and m.group(1) in text, ("not a quote from the text", o)
                    assert (k in shows(m.group(1))) == (o == r["answer"]), ("proves the point?", o, k)
            elif t == "point":
                qn = d["q"]; assert qn in r["html"]; k = key_of(qn)
                for o in opts: assert (k in names(o)) == (o == r["answer"]), ("answers the question?", o)
            elif t == "part":
                s = d["s"]; assert s in r["html"]
                assert r["answer"] == LAB[part(s)], (s, part(s))
                assert set(opts) == set(LAB.values())
            elif t == "explain":
                k = key_of(d["p"]); assert d["p"] in r["html"] and d["q"] in r["html"]
                for o in opts: assert good_expl(k, d["q"], o) == (o == r["answer"]), ("explanation", o, why_bad(k, d["q"], o))
            elif t == "exact":
                k = key_of(d["p"]); line = d["line"]; assert line in r["html"]
                kinds = {o: quote_kind(line, k, o) for o in opts}
                assert kinds[r["answer"]] == "good" and sorted(kinds.values()) == ["good", "long", "misquote", "nomarks"], kinds
            else: raise AssertionError("unknown type " + t)
            assert r["why"], "no why"
        except AssertionError as e:
            bad += 1
            if bad <= 10: print("PROBLEM", t, e, r["answer"], r["wrong"])
    print(f"{sum(cnt.values())} questions {cnt}, {bad} problems")
    return bad

if __name__ == "__main__":
    if sys.argv[1] == "-":
        print(data_pass(load(sys.argv[2])), "texts: data pass OK"); sys.exit(0)
    sys.exit(1 if check(sys.argv[1], sys.argv[2]) else 0)
