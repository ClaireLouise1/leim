#!/usr/bin/env python3
"""Independent checker for Format Sort (JC English Order 22, Functional writing: reports, reviews, articles & blogs).
It does not trust the game's answers: it re-derives each one with its own word lists (no spaCy needed).
  - text type   each extract hits exactly ONE type's markers (TYPEX: report / review / article / blog / speech)
  - headline    the right headline shares a content word (CW: 4+ letters, not in STOP, plural -s stripped) with the
                opening; every wrong headline shares NONE (other stories' headlines + a vague one); headlines <= 8 words
  - report part each report line hits exactly ONE part (REPX: title / introduction / findings / recommendation / sign-off)
  - review part each review line hits exactly ONE part (REVX: details / praise / criticism / verdict)
Usage: N=400 node src/test_format_sort.js format-sort.html > /tmp/fs.jsonl && python3 src/test_format_sort.py /tmp/fs.jsonl format-sort.html
       python3 src/test_format_sort.py - <page or json>   (data pass only)"""
import sys, json, re, html as H

TYPE = {"rep": "📊 Report", "rev": "⭐ Review", "art": "📰 Article", "blo": "💻 Blog", "spe": "🎤 Speech"}
TYPEX = {
 "rep": r"\b(this report|report on|recommendations?|I recommend that|findings|surveyed|terms of reference|was asked to)\b",
 "rev": r"\b(stars|out of (five|ten)|directed by|starring|gameplay|soundtrack|the acting|the plot|verdict|worth (the|a|every)|I'd recommend (it|this))\b",
 "art": r"\b(according to|residents|locals|spokesperson|said yesterday|our reporter)\b",
 "blo": r"(\b(my blog|hi everyone|hey guys|followers|comments?( below)?|let me know|subscribe|week's post|new post)\b|#\w+)",
 "spe": r"\b(good (morning|afternoon|evening),? everyone|ladies and gentlemen|fellow students|thank you for listening|stand before you|principal, teachers|members of the (council|board))\b",
}
BYLINE = r"^By [A-Z][a-zé]+ [A-Z][a-zé']+:"   # a byline (case-sensitive) also marks an article
def types(s): return [k for k in TYPE if re.search(TYPEX[k], s, re.I) or (k == "art" and re.search(BYLINE, s))]

REP = {"ti": "📌 Title", "in": "📋 Introduction", "fi": "🔍 Findings", "re": "💡 Recommendation", "si": "✍️ Sign-off"}
REPX = {
 "ti": r"^Report on\b",
 "in": r"\b(this report (was|is)|was asked (by|to)|terms of reference|aim of this report|purpose of this report|requested by)\b",
 "fi": r"(\d+%|\b\d+ out of \d+\b|\bof the \d+\b|\b(surveyed|most students|majority|half of|found that)\b)",
 "re": r"\b(recommend\w*|should)\b",
 "si": r"^(Signed:|Report prepared by|Submitted by)",
}
def rparts(s): return [k for k in REP if re.search(REPX[k], s, re.I if k not in ("ti", "si") else 0)]

REV = {"de": "ℹ️ Details", "pr": "👍 Praise", "cr": "👎 Criticism", "ve": "⭐ Verdict"}
REVX = {
 "de": r"\b(directed by|written by|starring|released|published|available on|costs? €\d+|\d+ pages|\d+ minutes|rated (PG|12A|15A)|episodes|songs)\b",
 "pr": r"\b(brilliant\w*|stunning|hilarious|gripping|superb|loved|outstanding|beautiful\w*|clever|the highlight)\b",
 "cr": r"\b(disappointing|drags?|too long|too slow|weak|boring|confusing|let (me|it) down|predictable|repetitive)\b",
 "ve": r"\b(out of (five|ten)|stars|overall|my verdict|I'd recommend|worth (the|a|every)|give it a miss|don't miss)\b",
}
def vparts(s): return [k for k in REV if re.search(REVX[k], s, re.I)]

STOP = set("""this that with from have has been were they their them then than into over under after before about
also just very when what where which while will would could should there here your yours ours some such only every
most more much many other another again across along around being does doing done each into onto upon""".split())
def cw(s):
    out = set()
    for w in re.findall(r"[A-Za-zÀ-ÿ']+", s.lower()):
        w = w.replace("'s", "").strip("'")
        if len(w) >= 4 and w not in STOP: out.add(w[:-1] if w.endswith("s") and len(w) > 4 else w)
    return out
def shares(a, b): return bool(cw(a) & cw(b))

def load(path):
    s = open(path, encoding="utf-8").read()
    if path.endswith(".json"): return json.loads(s)
    return json.loads(s[s.index("/*DATA*/") + 8:s.index("/*END*/")])

def data_pass(D):
    e = []
    for s, k in D["type"]:
        if types(s) != [k]: e.append(f"type: {s!r} hits {types(s)}, tagged {k}")
    for s, k in D["rep"]:
        if rparts(s) != [k]: e.append(f"rep: {s!r} hits {rparts(s)}, tagged {k}")
    for s, k in D["rev"]:
        if vparts(s) != [k]: e.append(f"rev: {s!r} hits {vparts(s)}, tagged {k}")
    for i, (t, h) in enumerate(D["heads"]):
        if not shares(t, h): e.append(f"head: {h!r} shares nothing with its story")
        if len(h.split()) > 8: e.append(f"head: too long {h!r}")
        for j, (t2, h2) in enumerate(D["heads"]):
            if i != j and shares(t, h2): e.append(f"head: {h2!r} shares {cw(t) & cw(h2)} with story {i}")
        for v in D["vague"]:
            if shares(t, v): e.append(f"head: vague {v!r} shares {cw(t) & cw(v)} with story {i}")
    for name in ("type", "rep", "rev", "heads"):
        texts = [x[0] for x in D[name]]
        if len(set(texts)) != len(texts): e.append(f"{name}: duplicate item")
    if len(D["vague"]) < 2: e.append("vague: need at least 2")
    return e

def shown(s, h): return s in h or H.escape(s, quote=False) in h or s.replace("'", "&#39;") in h

def check(q, D):
    t, a, w, d = q["data"]["t"], q["answer"], q["wrong"], q["data"]
    e = []
    if len(w) != q["nw"] or len(set(w)) != len(w) or a in w: e.append("option count/duplicates")
    def lab(L, ks):
        if len(ks) != 1 or L[ks[0]] != a: e.append(f"answer {ks}")
        for x in w:
            if x not in L.values(): e.append(f"bad label {x!r}")
        if not shown(d["s"], q["html"]): e.append("text not shown")
    if t == "type": lab(TYPE, types(d["s"]))
    elif t == "rep": lab(REP, rparts(d["s"]))
    elif t == "rev": lab(REV, vparts(d["s"]))
    elif t == "head":
        s = d["s"]
        if not shown(s, q["html"]): e.append("story not shown")
        good = [x for x in [a] + w if shares(s, x)]
        if good != [a]: e.append(f"headlines sharing a word: {good}")
        if not any(x in D["vague"] for x in w): e.append("no vague headline")
        heads = [h for _, h in D["heads"]]
        for x in [a] + w:
            if x not in heads and x not in D["vague"]: e.append(f"unknown headline {x!r}")
            if len(x.split()) > 8: e.append(f"long headline {x!r}")
    else: e.append("unknown type")
    return e

if __name__ == "__main__":
    src = sys.argv[2] if len(sys.argv) > 2 else "format-sort.html"
    D = load(src); errs = data_pass(D)
    for x in errs: print("DATA", x)
    n = bad = 0; seen = {}
    if sys.argv[1] != "-":
        for line in open(sys.argv[1], encoding="utf-8"):
            q = json.loads(line); n += 1; e = check(q, D)
            seen[q["data"]["t"]] = seen.get(q["data"]["t"], 0) + 1
            if e:
                bad += 1
                if bad <= 15: print("BAD", q["mode"], q["data"], q["answer"], e)
    print(f"data problems: {len(errs)} · questions: {n} · problems: {bad} · types: {seen}")
    sys.exit(1 if errs or bad or (sys.argv[1] != "-" and n < 100) else 0)
