#!/usr/bin/env python3
"""Independent checker for Stage It (JC English Order 21, Drama 1: how plays work).
It does not trust the game's answers: it re-derives each one with its own word lists (no spaCy needed).
  - mood        each scene card hits exactly ONE mood list (MOODX: spooky / happy / sad / danger / peaceful);
                the lighting answer is LIGHT[mood], the sound answer SOUND[mood]
  - direction   each stage direction hits exactly ONE kind (DIRX: how to say it / where to move / what to do / face)
  - backstage   each production note hits exactly ONE job (DEPTX: set / costume / lighting / sound / props)
  - conflict    each situation hits exactly ONE conflict list (CONX: person vs person / self / nature / society)
  - feeling     the stage direction + line together hit exactly ONE feeling list (FEELX); scared ~ nervous are
                never offered as wrong for each other
Usage: N=400 node src/test_stage_it.js stage-it.html > /tmp/si.jsonl && python3 src/test_stage_it.py /tmp/si.jsonl stage-it.html
       python3 src/test_stage_it.py - <page or json>   (data pass only)"""
import sys, json, re, html as H

LIGHT = {"sp": "🌑 Dim, cold blue light", "ha": "☀️ Bright, warm light", "sa": "🌫️ Soft, grey light",
         "da": "🔴 Flashing red light", "pe": "🌅 Gentle golden light"}
SOUND = {"sp": "🦉 An owl and a creaking door", "ha": "🎉 Cheering and lively music", "sa": "🎻 A slow, sad violin",
         "da": "🥁 A fast, pounding drum", "pe": "🐦 Birdsong and gentle waves"}
MOODX = {
 "sp": r"\b(ghosts?|haunted|graveyard|midnight|cobwebs?|eerie|abandoned|creak\w*|spooky|skeleton|witch|halloween)\b",
 "ha": r"\b(wedding|birthday|party|wins?|won|celebrat\w*|cheer\w*|prize|danc\w*|trophy|surprise)\b",
 "sa": r"\b(funeral|goodbye|alone|tears|crying|lonely|empty|emigrat\w*|died|dies)\b",
 "da": r"\b(chase\w*|escape\w*|fire|burning|alarm|thief|thieves|trapped|police|smoke|sinking|running out of time|falling)\b",
 "pe": r"\b(sunrise|calm|picnic|fishing|meadow|rests?|resting|sleeps?|peaceful\w*|quiet|lake)\b",
}
def moods(s): return [k for k in LIGHT if re.search(MOODX[k], s, re.I)]

DIR = {"voi": "🗣️ How to say it", "mov": "🚶 Where to move", "act": "✋ What to do", "face": "🙂 Face"}
DIRX = {
 "voi": r"\b(whisper\w*|shout\w*|softly|quietly|loudly|mutter\w*|stammer\w*|yell\w*|in a low voice|sings?|singing|sarcastically|calling out)\b",
 "mov": r"\b(cross(es)?|exits?|enters?|walks?|runs? (off|on|to)|sits?|stands? up|kneels?|moves?|steps? (forward|back)|paces|downstage|upstage|backs? away|stage (left|right)|climbs|leaves)\b",
 "act": r"\b(picks? up|hands|throws?|opens|pours?|puts? down|tears|drops|grabs?|folds|writes|lights a)\b",
 "face": r"\b(smiles?|frowns?|glares?|rolls (his|her) eyes|grins?|winces?|raises an eyebrow|stares|blushes|scowls?)\b",
}
def dirkind(s): return [k for k in DIR if re.search(DIRX[k], s, re.I)]

DEPT = {"set": "🏠 Set", "cos": "👗 Costume", "lig": "💡 Lighting", "sou": "🔊 Sound", "pro": "🧰 Props"}
DEPTX = {
 "set": r"\b(backdrop|fireplace|staircase|bus shelter|walls?|scenery|bookshel\w+|kitchen)\b",
 "cos": r"\b(cloak|dress|uniform|wig|coat|boots|jumper|scarf|apron|hat|veil|costume)\b",
 "lig": r"\b(spotlights?|lights?|blackout|glow|moonlight|sunlight|dark|dim)\b",
 "sou": r"\b(sound|rings?|music|bang|offstage|thunder|knocking|howl\w*|crash\w*)\b",
 "pro": r"\b(suitcase|letter|hurley|cup|keys?|umbrella|phone|basket|sword|carry)\b",
}
def depts(s): return [k for k in DEPT if re.search(DEPTX[k], s, re.I)]

CON = {"per": "🥊 Person vs person", "self": "🧠 Person vs self", "nat": "🌪️ Person vs nature", "soc": "🏛️ Person vs society"}
CONX = {
 "per": r"\b(argues? with|fight\w*|rival|bull(y|ies)|enemy|blames|accuses|won't speak to|steal\w*|stole)\b",
 "self": r"\b(can't decide|torn between|part of \w+ wants|guilt\w*|conscience|doubts? (himself|herself))\b",
 "nat": r"\b(storm|flood\w*|blizzard|snow|waves|gale|fog|drought|wildfire|mountain)\b",
 "soc": r"\b(rules?|law|banned|ban|not allowed|council|tradition|government)\b",
}
def conflicts(s): return [k for k in CON if re.search(CONX[k], s, re.I)]

FEEL = {"an": "😠 Angry", "sc": "😨 Scared", "ha": "😄 Happy", "sa": "😢 Sad", "ne": "😬 Nervous"}
CLOSE = {"sc": "ne", "ne": "sc"}
FEELX = {
 "an": r"\b(slam\w*|stamp\w*|clench\w*|thump\w*|furious\w*|red in the face|kick\w*|I dare you)\b",
 "sc": r"\b(trembl\w*|shaking|gasp\w*|hid(es|ing)|back\w* away|frozen|clutch\w*|someone out there|something's upstairs)\b",
 "ha": r"\b(beaming|laugh\w*|grinning|hug\w*|jump\w* for joy|clap\w*|best news)\b",
 "sa": r"\b(sob\w*|tears|wiping (his|her) eyes|head in (his|her) hands|sigh\w*|miss you|lost everything)\b",
 "ne": r"\b(biting (his|her) nails|fidget\w*|pacing|paces|stammer\w*|wringing (his|her) hands|tapping (his|her) foot|what if)\b",
}
def feelings(s): return [k for k in FEEL if re.search(FEELX[k], s, re.I)]

def load(path):
    s = open(path, encoding="utf-8").read()
    if path.endswith(".json"): return json.loads(s)
    return json.loads(s[s.index("/*DATA*/") + 8:s.index("/*END*/")])

def data_pass(D):
    e = []
    for s, k in D["scene"]:
        if moods(s) != [k]: e.append(f"scene: {s!r} hits {moods(s)}, tagged {k}")
    for s, k in D["dir"]:
        if dirkind(s) != [k]: e.append(f"dir: {s!r} hits {dirkind(s)}, tagged {k}")
        if not (s.startswith("(") and s.endswith(")")): e.append(f"dir: not in brackets {s!r}")
    for s, k in D["back"]:
        if depts(s) != [k]: e.append(f"back: {s!r} hits {depts(s)}, tagged {k}")
    for s, k in D["con"]:
        if conflicts(s) != [k]: e.append(f"con: {s!r} hits {conflicts(s)}, tagged {k}")
    for d, l, k in D["feel"]:
        if feelings(d + " " + l) != [k]: e.append(f"feel: {d!r} {l!r} hits {feelings(d + ' ' + l)}, tagged {k}")
        if feelings(l) not in ([], [k]): e.append(f"feel: line points elsewhere {l!r}")
    for name, key in (("scene", 1), ("dir", 1), ("back", 1), ("con", 1), ("feel", 2)):
        texts = [x[0] if name != "feel" else x[0] + x[1] for x in D[name]]
        if len(set(texts)) != len(texts): e.append(f"{name}: duplicate item")
    return e

def shown(s, h): return s in h or H.escape(s, quote=False) in h or s.replace("'", "&#39;") in h

def check(q, D):
    t, a, w, d = q["data"]["t"], q["answer"], q["wrong"], q["data"]
    e = []
    if len(w) != q["nw"] or len(set(w)) != len(w) or a in w: e.append("option count/duplicates")
    if t in ("light", "sound"):
        L = LIGHT if t == "light" else SOUND
        k = moods(d["s"])
        if len(k) != 1 or L[k[0]] != a: e.append(f"mood {k}")
        for x in w:
            if x not in L.values(): e.append(f"bad label {x!r}")
        if not shown(d["s"], q["html"]): e.append("scene not shown")
    elif t == "dir":
        k = dirkind(d["s"])
        if len(k) != 1 or DIR[k[0]] != a: e.append(f"direction {k}")
        for x in w:
            if x not in DIR.values(): e.append(f"bad label {x!r}")
        if not shown(d["s"], q["html"]): e.append("direction not shown")
    elif t == "back":
        k = depts(d["s"])
        if len(k) != 1 or DEPT[k[0]] != a: e.append(f"job {k}")
        for x in w:
            if x not in DEPT.values(): e.append(f"bad label {x!r}")
        if not shown(d["s"], q["html"]): e.append("note not shown")
    elif t == "con":
        k = conflicts(d["s"])
        if len(k) != 1 or CON[k[0]] != a: e.append(f"conflict {k}")
        for x in w:
            if x not in CON.values(): e.append(f"bad label {x!r}")
        if not shown(d["s"], q["html"]): e.append("situation not shown")
    elif t == "feel":
        k = feelings(d["d"] + " " + d["l"])
        if len(k) != 1 or FEEL[k[0]] != a: e.append(f"feeling {k}")
        for x in w:
            if x not in FEEL.values(): e.append(f"bad label {x!r}")
            if k and CLOSE.get(k[0]) and FEEL[CLOSE[k[0]]] == x: e.append(f"close feeling offered as wrong {x!r}")
        if not shown(d["d"], q["html"]) or not shown(d["l"], q["html"]): e.append("line not shown")
    else: e.append("unknown type")
    return e

if __name__ == "__main__":
    src = sys.argv[2] if len(sys.argv) > 2 else "stage-it.html"
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
