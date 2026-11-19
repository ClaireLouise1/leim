#!/usr/bin/env python3
"""Independent checker for Plot Line (JC English Order 14, the novel 2: setting, plot, structure & theme).
It re-derives every answer with its own rules + spaCy lemmas (the game only carries tags):
- plot stage: climax = opens with a sudden-moment phrase, falling action = opens with an aftermath phrase,
  resolution = opens with an ending phrase, rising action = a trouble word (and no opener), exposition = a time word
  (and nothing else); every arc line must hit exactly ONE stage, and an arc's lines must run E → R → C → F → Res
- order: lines B-E sorted by stage
- theme: spaCy lemmas + phrases per theme; a moment must hit exactly one theme; no wrong option may be hit,
  and look-alike themes (friendship ↔ belonging, courage ↔ growing up) are never offered as wrong
- mood: lemmas per mood; exactly one mood per line
- change: trait lemmas/phrases; the start line hits exactly one trait, the end line exactly one, the answer is
  start → end, and no wrong option is the same pair
Usage: N=400 node src/test_plot_line.js plot-line.html > /tmp/pl.jsonl && python3 src/test_plot_line.py /tmp/pl.jsonl plot-line.html
       python3 src/test_plot_line.py - <page or data.json>   (data pass only)"""
import sys, json, re, html as H
import spacy
nlp = spacy.load("en_core_web_sm")
_memo = {}
def lem(s):
    if s not in _memo: _memo[s] = {t.lemma_.lower() for t in nlp(s)} | {t.text.lower() for t in nlp(s)}
    return _memo[s]

TIMEW = re.compile(r"\b(morning|afternoon|evening|night|dawn|dusk|midnight|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday|"
                   r"January|February|March|April|May|June|July|August|September|October|November|December|summer|winter|autumn|spring|Christmas|Halloween|Easter)\b")
PROB = re.compile(r"\b(lost|missing|gone|locked|stuck|broke|broken|couldn't|wouldn't|no sign of|forg[oe]t\w*|ruined|trapped|losing|injured|missed|stealing|worse|refused|torn|cancelled)\b", re.I)
CLIM = re.compile(r"^(Suddenly|Just then|At that moment|All at once|Without warning)\b")
FALL = re.compile(r"^(Afterwards|After that|Slowly|Bit by bit|Later that|The next day)\b")
ENDO = re.compile(r"^(In the end|At last|Finally|From that day on|Ever since|By the end of)\b")
ORDER = ["ex", "ri", "cl", "fa", "re"]
LAB = {"ex": "🏠 Exposition", "ri": "📈 Rising action", "cl": "💥 Climax", "fa": "📉 Falling action", "re": "🏁 Resolution"}
def stages(s):
    h = []
    if CLIM.search(s): h.append("cl")
    if FALL.search(s): h.append("fa")
    if ENDO.search(s): h.append("re")
    if PROB.search(s): h.append("ri")
    if TIMEW.search(s): h.append("ex")
    return h
def stage(s):
    h = stages(s); return h[0] if len(h) == 1 else None

# theme: lemma words + phrases
TH = {
 "fr": ({"friend", "friendship"}, r"stood by|best mate"),
 "co": ({"brave", "courage", "afraid", "terrified", "scared", "trembling", "tremble", "shaking", "fear"}, None),
 "lo": ({"die", "died", "funeral", "grave", "grief", "cry", "cried"}, r"gone forever|empty chair|passed away"),
 "be": ({"belong", "outsider"}, r"fit in|left out|one of them|felt at home"),
 "gr": ({"childish", "responsibility"}, r"first time|no longer a child|old enough|grew up|on (his|her) own"),
 "fa": ({"unfair", "blame", "blamed", "wrongly", "cheat", "punish", "punished"}, None),
 "fo": ({"forgive", "forgave", "sorry", "apologise"}, r"second chance|made up"),
}
TLAB = {"fr": "🤝 Friendship", "co": "🦁 Courage", "lo": "💔 Loss", "be": "🏡 Belonging", "gr": "🌱 Growing up", "fa": "⚖️ Fairness", "fo": "🕊️ Forgiveness"}
TCLOSE = [{"fr", "be"}, {"co", "gr"}]
def hits(s, LEX):
    L = lem(s); out = []
    for k, (words, ph) in LEX.items():
        if (L & words) or (ph and re.search(r"\b(" + ph + r")\b", s, re.I)): out.append(k)
    return out

MO = {
 "te": ({"creak", "creaked", "shadow", "howl", "howled", "footstep", "darkness", "flicker", "thud", "whisper", "whispered", "slam", "slammed", "scream"}, None),
 "pe": ({"gently", "calm", "calmly", "still", "softly", "lap", "lapped", "drift", "drifted", "quiet", "hum", "hummed", "breeze"}, None),
 "jo": ({"laugh", "laughed", "music", "bunting", "dance", "dancing", "balloon", "sparkle", "sparkled", "bright", "cheer", "cheered", "firework"}, None),
 "gl": ({"grey", "drizzle", "bare", "empty", "drip", "dripped", "damp", "faded", "rusty", "lonely"}, None),
}
MLAB = {"te": "😨 Tense", "pe": "😌 Peaceful", "jo": "🎉 Joyful", "gl": "😔 Gloomy"}

TR = {
 "sh": ({"whisper", "whispered", "hid", "hide", "blush", "blushed"}, r"never spoke|looked at the floor"),
 "cf": ({"volunteer", "volunteered", "loudly", "grin", "grinned", "led"}, r"spoke up"),
 "se": ({"grab", "grabbed"}, r"wouldn't share|kept every"),
 "ge": (set(), r"shared|gave|handed"),
 "sc": ({"froze", "freeze", "afraid", "tremble", "trembled", "scared"}, r"ran away"),
 "br": ({"bravely", "dive", "dived"}, r"stepped forward|faced"),
 "lo": ({"alone", "lonely"}, r"on (his|her) own|by (himself|herself)"),
 "ac": ({"invite", "invited", "welcome", "welcomed"}, None),
}
CLAB = {"sh": "🙈 Shy", "cf": "😎 Confident", "se": "🙅 Selfish", "ge": "🎁 Generous", "sc": "😨 Scared", "br": "🦁 Brave", "lo": "😔 Lonely", "ac": "🤗 Accepted"}
def trait(s):
    h = hits(s, TR)
    # "wouldn't share" contains share (generous lemma): the phrase wins
    if "se" in h and "ge" in h and re.search(r"wouldn't share", s): h.remove("ge")
    return h

INV = lambda d: {v: k for k, v in d.items()}
def load(path):
    t = open(path, encoding="utf-8").read()
    if "/*DATA*/" in t: t = t[t.index("/*DATA*/") + 8:t.index("/*END*/")]
    return json.loads(t)

def data_pass(D):
    errs = []
    for A in D["arcs"]:
        got = [stage(l) for l in A["lines"]]
        if got != ORDER: errs.append(("arc stages", A["k"], [stages(l) for l in A["lines"]]))
    for s, k in D["theme"]:
        if hits(s, TH) != [k]: errs.append(("theme", s, hits(s, TH), k))
    for s, k in D["mood"]:
        if hits(s, MO) != [k]: errs.append(("mood", s, hits(s, MO), k))
    for who, a, b, s, e in D["change"]:
        if trait(a) != [s]: errs.append(("change start", a, trait(a), s))
        if trait(b) != [e]: errs.append(("change end", b, trait(b), e))
        if s == e: errs.append(("no change", who))
    return errs

def strip(h): return H.unescape(re.sub(r"<[^>]+>", " ", h))

def check(q, D):
    t, a, w = q["data"]["t"], q["answer"], q["wrong"]
    opts = [a] + w
    if len(set(opts)) != len(opts): return "duplicate options"
    if len(w) != q["nw"]: return "wrong count"
    if t == "stage":
        s = q["data"]["s"]
        if stage(s) is None or LAB[stage(s)] != a: return f"stage {stages(s)}"
        if s not in strip(q["html"]): return "stage card"
        if not all(o in LAB.values() for o in opts): return "stage labels"
    elif t == "order":
        lets = re.findall(r'<p class="pl-l"><b>([A-D])</b>(.*?)</p>', q["html"])
        if len(lets) != 4: return "order letters"
        rk = {"ri": 1, "cl": 2, "fa": 3, "re": 4}
        try: order = sorted(lets, key=lambda x: rk[stage(H.unescape(x[1]))])
        except KeyError: return "order unparsed"
        if " → ".join(l for l, _ in order) != a: return "order"
        top = re.search(r'<p class="pl-t">🏠 (.*?)</p>', q["html"]).group(1)
        if stage(H.unescape(top)) != "ex": return "order top"
        if any(sorted(o.split(" → ")) != ["A", "B", "C", "D"] for o in opts): return "order options"
    elif t == "theme":
        s = q["data"]["s"]; h = hits(s, TH)
        if len(h) != 1 or TLAB[h[0]] != a: return f"theme {h}"
        inv = INV(TLAB)
        for o in w:
            if inv[o] in h: return "theme wrong hit"
            if {inv[o], h[0]} in TCLOSE: return "theme look-alike offered"
        if s not in strip(q["html"]): return "theme card"
    elif t == "mood":
        s = q["data"]["s"]; h = hits(s, MO)
        if len(h) != 1 or MLAB[h[0]] != a: return f"mood {h}"
        if s not in strip(q["html"]): return "mood card"
    elif t == "change":
        ls = [H.unescape(x) for x in re.findall(r'<p class="pl-c"><i>[^<]*</i>(.*?)</p>', q["html"])]
        if len(ls) != 2: return "change card"
        s, e = trait(ls[0]), trait(ls[1])
        if len(s) != 1 or len(e) != 1: return f"change traits {s} {e}"
        if a != CLAB[s[0]] + " → " + CLAB[e[0]]: return "change answer"
        inv = INV(CLAB)
        for o in w:
            x, y = o.split(" → ")
            if x not in inv or y not in inv: return "change label"
    else: return "unknown type " + t
    return None

if __name__ == "__main__":
    if sys.argv[1] == "-":
        e = data_pass(load(sys.argv[2])); [print(x) for x in e]; print("data errors:", len(e)); sys.exit(1 if e else 0)
    D = load(sys.argv[2]); errs = data_pass(D)
    for x in errs: print("DATA", x)
    n = bad = 0; seen = {}; longest = {}
    for line in open(sys.argv[1], encoding="utf-8"):
        q = json.loads(line); n += 1; tt = q["data"]["t"]; seen[tt] = seen.get(tt, 0) + 1
        if len(q["answer"]) >= max(len(x) for x in q["wrong"]): longest[tt] = longest.get(tt, 0) + 1
        r = check(q, D)
        if r:
            bad += 1
            if bad <= 15: print("BAD", r, "|", q["answer"], q["wrong"], q["data"])
    print("answer is the longest option:", {k: f"{100*longest.get(k,0)//v}%" for k, v in seen.items()})
    print("questions:", n, "types:", seen, "problems:", bad, "data errors:", len(errs))
    sys.exit(1 if bad or errs else 0)
