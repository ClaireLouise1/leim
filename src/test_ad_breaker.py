#!/usr/bin/env python3
"""Independent checker for Ad Breaker (JC English Order 20, Media 1: advertising).
It does not trust the game's answers: it re-derives each one with its own rules (no spaCy needed).
  - tricks      star  = a famous person: champion / famous / star / singer / chosen by / recommended by …
                free  = free / gift / bonus
                band  = bandwagon: everyone / everybody / all your friends / don't be left out / join the / thousands of …
                stat  = a digit or "per cent"
                exag  = exaggeration: best / greatest / ever / universe / planet / miracle / magic / unbelievabl- / comfiest …
                hurry = hurry / today only / while stocks last / last chance / limited / ends tonight / don't miss out / before it's gone
                a trick line must hit exactly ONE of these
  - audience    the ad's lines hit exactly ONE audience word list (AUD)
  - fact/opinion  opinion = an OPIN judgement word and no FACT marker; fact = a FACT marker (digit, €, weekday, made in,
                contains, available in, opens) and no OPIN word
  - slogan      good = 6 words or fewer, contains the brand, and has a sound device (alliteration: 2+ different words of 3+
                letters (not in STOP) with the same first letter; or rhyme: 2 different words of 3+ letters with the same last
                3 letters). Every wrong option fails at least one test (too long / no device / another brand)
  - picture     every emoji in the picture belongs to ONE meaning in PIC; close meanings (healthy ~ natural, fun ~ cool)
                are never offered as wrong
Usage: N=400 node src/test_ad_breaker.js ad-breaker.html > /tmp/ab.jsonl && python3 src/test_ad_breaker.py /tmp/ab.jsonl ad-breaker.html
       python3 src/test_ad_breaker.py - <page or json>   (data pass only)"""
import sys, json, re

TRICK = {"star": "⭐ Star power", "free": "🎁 Free gift", "band": "👥 Bandwagon", "stat": "📊 Statistic",
         "exag": "🚀 Exaggeration", "hurry": "⏰ Hurry"}
TRX = {
 "star": r"\b(champion|famous|celebrity|star|singer|chef|captain|hurler|chosen by|recommended by|as seen on)\b",
 "free": r"\b(free|gift|bonus)\b",
 "band": r"\b(everyone|everybody|all your friends|don't be left out|join the|thousands of|millions of|the whole (class|school|town|country))\b",
 "stat": r"\d|per cent",
 "exag": r"\b(best|greatest|ever|universe|planet|miracle|magic|unbelievabl\w*|incredibl\w*|perfect|unbeatable|comfiest|tastiest|never)\b",
 "hurry": r"\b(hurry|today only|while stocks last|last chance|limited|ends (today|tonight|soon|sunday)|don't miss out|before it's gone|selling fast)\b",
}
def tricks(s): return [k for k in TRICK if re.search(TRX[k], s, re.I)]

AUD = {"ki": "🧒 Young children", "te": "🧑 Teenagers", "pa": "👨‍👩‍👧 Parents", "ol": "👵 Older people", "sp": "🏃 Sporty people"}
AUDX = {
 "ki": r"\b(toys?|playground|cartoon|colouring|bedtime|teddy|crayons?|puppets?|little ones|ask your (mum|dad|parents))\b",
 "te": r"\b(teens?|teenagers?|exams?|Junior Cycle|mates|gaming|gamers?|study|secondary)\b",
 "pa": r"\b(your (kids|children|child)|school run|mums and dads|busy parents?|family meals|lunchboxes|nappies)\b",
 "ol": r"\b(retire\w*|grandchildren|grandkids|pension\w*|reading glasses|travel pass)\b",
 "sp": r"\b(training|marathon|gym|athletes?|match fit|workout|personal best|runners)\b",
}
def audiences(text): return [k for k in AUD if re.search(AUDX[k], text, re.I)]

OPIN = r"\b(delicious|tasty|tastiest|best|amazing|perfect|love|lovely|gorgeous|fantastic|comfiest|softest|nicest|great|brilliant|cool|coolest|fun|stylish|beautiful|awesome|must-have|should|wonderful|yummy|favourite)\b"
FACT = r"\d|€|\b(Mondays?|Tuesdays?|Wednesdays?|Thursdays?|Fridays?|Saturdays?|Sundays?|made in|contains?|available in|opens?)\b"
def fo(s):
    o, f = bool(re.search(OPIN, s, re.I)), bool(re.search(FACT, s, re.I))
    return "o" if o and not f else "f" if f and not o else None

STOP = set("the and for with you your are our its all from has have this that".split())
def toks(s): return [w.lower() for w in re.findall(r"[A-Za-z']+", s) if len(w) >= 3 and w.lower() not in STOP]
def allit(s):
    ws = sorted(set(toks(s))); return any(a[0] == b[0] for i, a in enumerate(ws) for b in ws[i + 1:])
def rhyme(s):
    ws = sorted(set(toks(s))); return any(a[-3:] == b[-3:] for i, a in enumerate(ws) for b in ws[i + 1:])
def nwords(s): return len(s.split())
def good_slogan(brand, s): return nwords(s) <= 6 and brand.lower() in s.lower() and (allit(s) or rhyme(s))

PIC = {"hea": ["🍎", "🥦", "🏃", "💪", "🥕", "🍌", "🚴", "🥗"], "lux": ["💎", "👑", "🥂", "✨", "🛥️", "🏰", "💍"], "fam": ["👨‍👩‍👧", "🏡", "🧸", "🛋️", "🍽️", "👶", "🎂", "🤗"],
       "nat": ["🌿", "🌳", "🌊", "🐝", "🌼", "🍃", "⛰️", "🦋"], "fun": ["🎉", "🎢", "🎈", "🎆", "🥳", "🎡", "🎊", "🤩"],
       "coo": ["😎", "🕶️", "🛹", "🎧", "🔥", "🏙️", "🤙", "🎸"]}
MEAN = {"hea": "🥗 Healthy", "lux": "💎 Luxury", "fam": "🏡 Family", "nat": "🌿 Natural", "fun": "🎉 Fun", "coo": "😎 Cool"}
CLOSE = {"hea": "nat", "nat": "hea", "fun": "coo", "coo": "fun"}
def meaning(pics):
    ks = {k for e in pics for k in PIC if e in PIC[k]}
    return ks.pop() if len(ks) == 1 and all(any(e in PIC[k] for k in PIC) for e in pics) else None

def load(path):
    s = open(path, encoding="utf-8").read()
    if path.endswith(".json"): return json.loads(s)
    return json.loads(s[s.index("/*DATA*/") + 8:s.index("/*END*/")])

def data_pass(D):
    e = []
    for s, k in D["trick"]:
        if tricks(s) != [k]: e.append(f"trick: {s!r} hits {tricks(s)}, tagged {k}")
    for a in D["ads"]:
        if audiences(" ".join(a["lines"])) != [a["who"]]: e.append(f"ad {a['brand']}: hits {audiences(' '.join(a['lines']))}, tagged {a['who']}")
    for s, k in D["fo"]:
        if fo(s) != k: e.append(f"fo: {s!r} reads as {fo(s)}, tagged {k}")
    brands = [x[1] for x in D["slogan"]]
    for lab, brand, best, long, dull in D["slogan"]:
        if not good_slogan(brand, best): e.append(f"slogan: best fails {best!r}")
        if nwords(long) <= 6 or brand.lower() not in long.lower(): e.append(f"slogan: long option not long / no brand {long!r}")
        if nwords(dull) > 6 or brand.lower() not in dull.lower() or allit(dull) or rhyme(dull): e.append(f"slogan: dull option has a device or is long {dull!r}")
        for b2 in brands:
            if b2 != brand and b2.lower() in best.lower(): e.append(f"slogan: {best!r} names {b2}")
    for lab, pics, k in D["pic"]:
        if meaning(pics) != k: e.append(f"pic: {lab} {pics} reads as {meaning(pics)}, tagged {k}")
        if lab.split()[0] in sum(PIC.values(), []): e.append(f"pic: product emoji in the table {lab}")
    return e

def check(q, D):
    t, a, w, d = q["data"]["t"], q["answer"], q["wrong"], q["data"]
    e = []
    if len(w) != q["nw"] or len(set(w)) != len(w) or a in w: e.append("option count/duplicates")
    if t == "trick":
        k = tricks(d["s"])
        if len(k) != 1 or TRICK[k[0]] != a: e.append(f"trick {k}")
        for x in w:
            if x not in TRICK.values(): e.append(f"bad label {x!r}")
        if d["s"] not in q["html"]: e.append("line not shown")
    elif t == "who":
        ad = [x for x in D["ads"] if x["brand"] == d["brand"]][0]
        for ln in ad["lines"]:
            if ln.replace("'", "&#39;") not in q["html"] and ln not in q["html"]: e.append("ad line not shown")
        k = audiences(" ".join(ad["lines"]))
        if len(k) != 1 or AUD[k[0]] != a: e.append(f"audience {k}")
        for x in w:
            if x not in AUD.values(): e.append(f"bad label {x!r}")
    elif t == "fo":
        k = fo(d["s"])
        if k is None or a != {"f": "✅ Fact", "o": "💭 Opinion"}[k]: e.append(f"fact/opinion {k}")
        if d["s"] not in q["html"]: e.append("line not shown")
    elif t == "slogan":
        brand = d["brand"]
        if brand not in q["html"]: e.append("brand not shown")
        if not good_slogan(brand, a): e.append("answer is not a good slogan")
        for x in w:
            if good_slogan(brand, x): e.append(f"wrong option is a good slogan {x!r}")
    elif t == "pic":
        k = meaning(d["pics"])
        if k is None or MEAN[k] != a: e.append(f"picture means {k}")
        for x in w:
            if x not in MEAN.values(): e.append(f"bad label {x!r}")
            if k and CLOSE.get(k) and MEAN[CLOSE[k]] == x: e.append(f"close meaning offered as wrong {x!r}")
        for p in d["pics"]:
            if p not in q["html"]: e.append("picture not shown")
    else: e.append("unknown type")
    return e

if __name__ == "__main__":
    src = sys.argv[2] if len(sys.argv) > 2 else "ad-breaker.html"
    D = load(src); errs = data_pass(D)
    for x in errs: print("DATA", x)
    n = bad = 0; seen = {}; longest = [0, 0]
    if sys.argv[1] != "-":
        for line in open(sys.argv[1], encoding="utf-8"):
            q = json.loads(line); n += 1; e = check(q, D)
            seen[q["data"]["t"]] = seen.get(q["data"]["t"], 0) + 1
            if e:
                bad += 1
                if bad <= 15: print("BAD", q["mode"], q["data"], q["answer"], e)
    print(f"data problems: {len(errs)} · questions: {n} · problems: {bad} · types: {seen}")
    sys.exit(1 if errs or bad or (sys.argv[1] != "-" and n < 100) else 0)
