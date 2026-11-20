#!/usr/bin/env python3
"""Independent checker for Mood Match (JC English Order 23, Poetry 2: theme, tone & comparing poems).
It does not trust the game's answers: it re-derives each one with its own word lists (no spaCy needed).
  - mood        each couplet hits exactly ONE tone's word list (TONEW), through exactly one word, the {braced} one
  - mood word   the answer is that word; every wrong option is another word of the couplet (4+ letters, not STOP)
                that is in NO tone list
  - theme       each 4-line poem hits exactly ONE theme's markers (THEMEX) across all its lines
  - mood shift  lines 1-2 hit exactly one tone, lines 3-4 exactly one other tone; line 3 opens with a turn word
  - compare     both short poems hit the same ONE theme, and one tone each (different, not look-alikes)
Look-alike tones (CLOSE: sad / nostalgic) are never offered as a wrong answer for each other.
Usage: N=400 node src/test_mood_match.js mood-match.html > /tmp/mm.jsonl && python3 src/test_mood_match.py /tmp/mm.jsonl mood-match.html
       python3 src/test_mood_match.py - <page or json>   (data pass only)"""
import sys, json, re, html as H

TONE = {"jo": "😊 Joyful", "sa": "😢 Sad", "ca": "😌 Peaceful", "te": "😨 Tense", "an": "😠 Angry", "no": "🕰️ Nostalgic"}
THEME = {"fr": "🤝 Friendship", "lo": "💔 Loss", "na": "🌿 Nature", "ho": "🏡 Home & place", "gr": "🌱 Growing up"}
CLOSE = {("sa", "no"), ("no", "sa")}
TONEW = {
 "jo": "laugh laughed laughing laughs laughter dance danced dances dancing cheer cheered cheering cheers giggle giggled giggles giggling delight delighted joy joyful joyous glee gleeful celebrate celebrated celebrating whoop whooped whooping grinned grinning hooray",
 "sa": "weep weeps wept weeping tears sob sobbed sobbing sobs sorrow sorrowful lonely loneliness ache ached aches aching mourn mourned mourning mourns sigh sighed sighs sighing gloomy grief heartbroken",
 "ca": "calm calmly stillness hush hushed gentle gently quiet quietly peace peaceful softly drowsy lulled serene tranquil",
 "te": "fear feared afraid dread trembling trembled tremble trembles creeping crept terror terrified panic panicked lurking lurks lurked menacing pounding scream screamed screaming",
 "an": "rage raged raging fury furious angry anger angrily snarl snarled snarling glare glared glaring slammed slam slams fists bitter seething spat stomped",
 "no": "remember remembered remembering remembers recall recalled memories memory nostalgic",
}
TONEW = {k: set(v.split()) for k, v in TONEW.items()}
THEMEX = {
 "fr": r"\b(friends?|friendship|mates?|pals?|buddy|side by side)\b",
 "lo": r"\b(gone|graves?|goodbye|funeral|passed away|empty chair|lost|missing)\b",
 "na": r"\b(trees?|rivers?|fields?|hills?|sea|waves?|birds?|leaf|leaves|flowers?|grass|sky|moon|stars?|wind|meadows?|bog|mountains?|forest|woods|rain|snow|frost|sun|blackbird|robin|heather|stream|lake|shore|beach|ocean|ferns?)\b",
 "ho": r"\b(home|homes|house|houses|kitchen|hearth|doorstep|street|hometown|village|town|emigrated|emigrate|emigrant|townland|front door)\b",
 "gr": r"\b(grow up|growing up|grown|grew up|older|taller|childhood|first day|teenagers?|young|small hands)\b",
}
TURN = r"^(But|Then|Until|Now|Suddenly|By morning|At last)\b"
STOP = set("""this that with from have has been were they their them then than into over under after before about
also just very when what where which while will would could should there here your yours ours some such only every
most more much many other another again across along around being does doing done each onto upon like
down first away come comes lies these through nothing begin round something never time last long hold whole
little high only behind""".split())
# words that carry a mood of their own: never offered as a "wrong" mood word
MOODY = set("""dark black cold shadow shadows clenched broken warm slowly faded trampled hurling rattled creak
gloom grey bright sunny storm empty silent alone rain""".split())
assert not any(w in re.findall(r"[a-z]+", " ".join(THEMEX.values())) for k in TONEW for w in TONEW[k] if len(w) > 3), "tone/theme lists overlap"

def plain(s): return s.replace("{", "").replace("}", "")
def toks(s): return re.findall(r"[a-z']+", plain(s).lower())
def tone_hits(s): return [w for w in toks(s) if any(w in TONEW[k] for k in TONEW)]
def tones(s): return sorted({k for w in toks(s) for k in TONEW if w in TONEW[k]})
def themes(s): return [k for k in THEME if re.search(THEMEX[k], plain(s), re.I)]
def braced(s): return re.findall(r"\{([^}]+)\}", s)
def candidates(s):
    """Words of a couplet a 'which word sets the mood?' question may offer as wrong."""
    out = []
    for line in plain(s).split(" / "):
        for i, w in enumerate(re.findall(r"[A-Za-zÀ-ÿ']+", line)):
            lw = w.lower()
            if i > 0 and w != lw: continue   # a name: never offered
            if len(lw) >= 4 and lw not in STOP and lw not in MOODY and "'" not in lw and not tones(lw) and lw not in out: out.append(lw)
    return out
def close(a, b): return a == b or (a, b) in CLOSE

def load(path):
    s = open(path, encoding="utf-8").read()
    if path.endswith(".json"): return json.loads(s)
    return json.loads(s[s.index("/*DATA*/") + 8:s.index("/*END*/")])

def data_pass(D):
    e = []
    for s, k in D["tone"]:
        if tones(s) != [k]: e.append(f"tone: {s!r} hits {tones(s)}, tagged {k}")
        b = braced(s)
        if len(b) != 1 or [h.lower() for h in tone_hits(s)] != [b[0].lower()]: e.append(f"tone: {s!r} braced {b}, tone words {tone_hits(s)}")
        if len(candidates(s)) < 3: e.append(f"tone: {s!r} only {candidates(s)} as wrong words")
        if s.count(" / ") != 1: e.append(f"tone: {s!r} is not a couplet")
    for P in D["theme"]:
        t = themes(" ".join(P["lines"]))
        if t != [P["t"]]: e.append(f"theme: {P['k']} hits {t}, tagged {P['t']}")
        if len(P["lines"]) != 4: e.append(f"theme: {P['k']} needs 4 lines")
    for P in D["shift"]:
        a, b = tones(" ".join(P["lines"][:2])), tones(" ".join(P["lines"][2:]))
        if a != [P["a"]] or b != [P["b"]]: e.append(f"shift: {P['k']} hits {a} → {b}, tagged {P['a']} → {P['b']}")
        if close(P["a"], P["b"]): e.append(f"shift: {P['k']} look-alike tones")
        if not re.search(TURN, P["lines"][2]): e.append(f"shift: {P['k']} line 3 has no turn word")
        if len(P["lines"]) != 4: e.append(f"shift: {P['k']} needs 4 lines")
    for P in D["pair"]:
        for side in "ab":
            L = " ".join(P[side])
            if themes(L) != [P["t"]]: e.append(f"pair: {P['k' + side]} hits theme {themes(L)}, tagged {P['t']}")
            if tones(L) != [P["t" + side]]: e.append(f"pair: {P['k' + side]} hits tone {tones(L)}, tagged {P['t' + side]}")
        if close(P["ta"], P["tb"]): e.append(f"pair: {P['ka']} / {P['kb']} look-alike tones")
    for name, key in (("tone", lambda x: x[0]), ("theme", lambda x: x["k"]), ("shift", lambda x: x["k"]), ("pair", lambda x: x["ka"])):
        ks = [key(x) for x in D[name]]
        if len(set(ks)) != len(ks): e.append(f"{name}: duplicate item")
    for k in TONE:
        if sum(1 for _, t in D["tone"] if t == k) < 4: e.append(f"tone: fewer than 4 {k} couplets")
    for k in THEME:
        if sum(1 for P in D["theme"] if P["t"] == k) < 3: e.append(f"theme: fewer than 3 {k} poems")
    return e

def shown(s, h): return s in h or H.escape(s, quote=False) in h or s.replace("'", "&#39;") in h

def check(q, D):
    t, a, w, d = q["data"]["t"], q["answer"], q["wrong"], q["data"]
    e = []
    if len(w) != q["nw"] or len(set(w)) != len(w) or a in w: e.append("option count/duplicates")
    for line in d.get("lines", []):
        if not shown(line, q["html"]): e.append(f"line not shown: {line!r}")
    inv = {v: k for k, v in TONE.items()}
    if t == "mood":
        k = tones(d["s"])
        if len(k) != 1 or TONE[k[0]] != a: e.append(f"answer {k}")
        for x in w:
            if x not in inv: e.append(f"bad label {x!r}")
            elif k and close(inv[x], k[0]): e.append(f"wrong option {x!r} is right or a look-alike")
        if not all(shown(x, q["html"]) for x in plain(d["s"]).split(" / ")): e.append("couplet not shown")
    elif t == "word":
        hits = tone_hits(d["s"])
        if [h.lower() for h in hits] != [a.lower()]: e.append(f"mood word {hits} vs {a!r}")
        cand = candidates(d["s"])
        if a != a.lower() or any(x != x.lower() for x in w): e.append("capital letter in an option (gives the answer away)")
        for x in w:
            if x not in cand: e.append(f"{x!r} is not a plain word of the couplet")
            if tones(x): e.append(f"wrong word {x!r} is a mood word")
            if len(x) < 4 or x.lower() in STOP or x.lower() in MOODY or "'" in x: e.append(f"weak option {x!r}")
        if not all(shown(x, q["html"]) for x in plain(d["s"]).split(" / ")): e.append("couplet not shown")
    elif t == "theme":
        k = themes(" ".join(d["lines"]))
        if len(k) != 1 or THEME[k[0]] != a: e.append(f"answer {k}")
        for x in w:
            if x not in THEME.values(): e.append(f"bad label {x!r}")
    elif t == "shift":
        L = d["lines"]; x1, x2 = tones(" ".join(L[:2])), tones(" ".join(L[2:]))
        if len(x1) != 1 or len(x2) != 1 or a != f"{TONE[x1[0]]} → {TONE[x2[0]]}": e.append(f"answer {x1} → {x2} vs {a!r}")
        for x in w:
            p = x.split(" → ")
            if len(p) != 2 or p[0] not in inv or p[1] not in inv: e.append(f"bad option {x!r}"); continue
            if x1 and x2 and close(inv[p[0]], x1[0]) and close(inv[p[1]], x2[0]): e.append(f"wrong option {x!r} is right or a look-alike")
            if p[0] == p[1]: e.append(f"no change {x!r}")
    elif t == "share":
        ka, kb = themes(" ".join(d["a"])), themes(" ".join(d["b"]))
        if ka != kb or len(ka) != 1 or THEME[ka[0]] != a: e.append(f"shared theme {ka} / {kb} vs {a!r}")
        for x in w:
            if x not in THEME.values(): e.append(f"bad label {x!r}")
        for line in d["a"] + d["b"]:
            if not shown(line, q["html"]): e.append("poem not shown")
    elif t == "diff":
        ta, tb = tones(" ".join(d["a"])), tones(" ".join(d["b"]))
        if len(ta) != 1 or len(tb) != 1 or a != f"A {TONE[ta[0]]} · B {TONE[tb[0]]}": e.append(f"answer {ta} / {tb} vs {a!r}")
        for x in w:
            m = re.fullmatch(r"A (.+) · B (.+)", x)
            if not m or m.group(1) not in inv or m.group(2) not in inv: e.append(f"bad option {x!r}"); continue
            if ta and tb and close(inv[m.group(1)], ta[0]) and close(inv[m.group(2)], tb[0]): e.append(f"wrong option {x!r} is right or a look-alike")
        for line in d["a"] + d["b"]:
            if not shown(line, q["html"]): e.append("poem not shown")
    else: e.append("unknown type")
    return e

if __name__ == "__main__":
    src = sys.argv[2] if len(sys.argv) > 2 else "mood-match.html"
    D = load(src); errs = data_pass(D)
    for x in errs: print("DATA", x)
    n = bad = 0; seen = {}; longest = [0, 0]
    if sys.argv[1] != "-":
        for line in open(sys.argv[1], encoding="utf-8"):
            q = json.loads(line); n += 1; e = check(q, D)
            seen[q["data"]["t"]] = seen.get(q["data"]["t"], 0) + 1
            if q["data"]["t"] in ("shift", "diff"):
                longest[1] += 1; longest[0] += len(q["answer"]) >= max(len(x) for x in q["wrong"])
            if e:
                bad += 1
                if bad <= 15: print("BAD", q["mode"], q["data"].get("s") or q["data"].get("lines") or q["data"].get("a"), q["answer"], q["wrong"], e)
    print(f"data problems: {len(errs)} · questions: {n} · problems: {bad} · types: {seen}" + (f" · shift/diff answer longest {100 * longest[0] // max(1, longest[1])}%" if longest[1] else ""))
    sys.exit(1 if errs or bad or (sys.argv[1] != "-" and n < 100) else 0)
