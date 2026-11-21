#!/usr/bin/env python3
"""Independent checker for Fact or Opinion (Order 31, non-literary & visual texts).
It never trusts the game's answers:
 - every sentence is sorted into fact / opinion with its OWN judgement-word list (facts must also hold something checkable),
 - every bar chart is MEASURED from the drawn SVG (gridline positions + tick numbers → scale; bar heights → values; labels by x position),
 - every poster part is named from its content and position (first block = headline, emoji-only = picture, the block after the picture = caption,
   phone / web / email = contact, day / month + time = when & where).
Usage: N=400 node src/test_fact_or_opinion.js fact-or-opinion.html > /tmp/fo.jsonl && python3 src/test_fact_or_opinion.py /tmp/fo.jsonl fact-or-opinion.html
       python3 src/test_fact_or_opinion.py - <page or json>   (data pass only) — no spaCy needed."""
import json, re, sys, html as H
from collections import Counter

# judgement words: adjectives of praise / blame, comparisons, advice, "I think"
PRAISE = "best worst greatest finest nicest tastiest comfiest friendliest loveliest better worse easier harder boring dull brilliant amazing stunning " \
         "terrible awful perfect fantastic wonderful ugly delicious lovely hilarious gorgeous beautiful exciting rewarding useful fun dirty waste deserves love unmissable comfy salty expensive".split()
PHRASES = [r"\btoo\b", r"\bshould\b", r"\bI think\b", r"\bI believe\b", r"\bin my (view|opinion)\b", r"\bmost \w+\b(?! of)"]
CHECKABLE = r"\d|\b(one|two|three|four|five|six|seven|eight|nine|ten|twelve|twenty|hundred|half|quarter)\b|\b(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday|Mondays|Wednesdays|January|February|March|April|May|June|July|August|September|October|November|December)\b"
FO = ["🧾 Fact", "💭 Opinion"]
LINES = ["Line 1", "Line 2", "Line 3", "Line 4"]
PARTS = ["📢 Headline", "🖼️ Picture", "📝 Caption", "📅 When & where", "📞 Contact details"]

def judgements(s):
    words = re.findall(r"[a-z']+", s.lower())
    hits = [w for w in words if w in PRAISE]
    hits += [m.group(0) for rx in PHRASES for m in [re.search(rx, s, re.I)] if m]
    return hits

def kind(s):
    return FO[1] if judgements(s) else FO[0]

def text(h): return H.unescape(re.sub(r"<[^>]+>", " ", h)).strip()

# ---------- poster parts ----------
PHONE = r"\b0\d{1,2} \d{3} \d{4}\b"
CONTACT = PHONE + r"|www\.|@|\.ie\b"
DAY = r"\b(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday|January|February|March|April|May|June|July|August|September|October|November|December)\b"
TIME = r"\b(\d{1,2}(\.\d\d)? ?(a\.m\.|p\.m\.)|noon|midnight)(?!\w)"

def name_parts(blocks):
    """blocks: list of plain-text blocks in poster order → list of part labels"""
    out = [None] * len(blocks)
    letters = [bool(re.search(r"[A-Za-z]", b)) for b in blocks]
    pic = [i for i, b in enumerate(blocks) if not letters[i]]
    assert len(pic) == 1, ("pictures", blocks)
    out[pic[0]] = PARTS[1]
    assert pic[0] + 1 < len(blocks)
    for i, b in enumerate(blocks):
        if out[i]: continue
        c, w = bool(re.search(CONTACT, b)), bool(re.search(DAY, b) and re.search(TIME, b))
        if i == 0: assert not (c or w), ("headline has details", b); out[i] = PARTS[0]
        elif i == pic[0] + 1: assert not (c or w or re.search(r"\d", b)), ("caption has details", b); out[i] = PARTS[2]
        else:
            assert c != w, ("block is both / neither contact and when", b)
            out[i] = PARTS[4] if c else PARTS[3]
    assert sorted(out) == sorted(PARTS), ("parts", out)
    return out

# ---------- chart measuring ----------
def measure(svg):
    ticks = [(float(y), int(v)) for y, v in re.findall(r'<g class="tick"><line [^>]*y1="([\d.]+)"[^>]*/><text[^>]*>(\d+)</text></g>', svg)]
    assert len(ticks) >= 3, "ticks"
    (ya, va), (yb, vb) = ticks[0], ticks[-1]
    per = (ya - yb) / (vb - va)             # pixels per unit
    for y, v in ticks: assert abs((ya - y) - (v - va) * per) < 0.05, "ticks not evenly spaced"
    base = ya + va * per                     # y of zero
    bars = [(float(x), float(y), float(w), float(h)) for x, y, w, h in re.findall(r'<rect class="bar" x="([\d.]+)" y="([\d.]+)" width="([\d.]+)" height="([\d.]+)"', svg)]
    labs = [(float(x), H.unescape(t)) for x, t in re.findall(r'<text class="bl" x="([\d.]+)"[^>]*>([^<]+)</text>', svg)]
    assert len(bars) == len(labs) >= 3
    vals = {}
    for x, y, w, h in bars:
        assert abs((y + h) - base) < 0.05, "bar not on the axis"
        v = h / per; assert abs(v - round(v)) < 0.02 and round(v) % 5 == 0, ("bar not on a 5-line", v)
        cx = x + w / 2
        lab = min(labs, key=lambda L: abs(L[0] - cx)); assert abs(lab[0] - cx) < 1, "label not under bar"
        vals[lab[1]] = round(v)
    assert len(set(vals.values())) == len(vals), "two bars the same height"
    return vals

def load(path):
    s = open(path, encoding="utf-8").read()
    if path.endswith(".json"): return json.loads(s)
    return json.loads(s.split("/*DATA*/", 1)[1].split("/*END*/", 1)[0])

def data_pass(D):
    for s in D["fo"]["f"]:
        assert kind(s) == FO[0], ("fact list holds an opinion", s, judgements(s))
        assert re.search(CHECKABLE, s, re.I), ("fact has nothing checkable", s)
    for s in D["fo"]["o"]:
        assert kind(s) == FO[1], ("opinion list holds a fact", s)
    allfo = D["fo"]["f"] + D["fo"]["o"]; assert len(set(allfo)) == len(allfo)
    for T in D["spot"]:
        assert len(T["lines"]) == 4, T["title"]
        c = Counter(kind(l) for l in T["lines"])
        assert sorted(c.values()) == [1, 3], ("spot text needs exactly one odd line", T["title"], c)
        assert T["op"] == [i + 1 for i, l in enumerate(T["lines"]) if kind(l) == FO[1]], ("op keys don't match the words", T["title"])
    odd = Counter(min(Counter(kind(l) for l in T["lines"]).items(), key=lambda x: x[1])[0] for T in D["spot"])
    pos = Counter()
    for T in D["spot"]:
        ks = [kind(l) for l in T["lines"]]; odd_k = min(set(ks), key=ks.count); pos[ks.index(odd_k)] += 1
    assert len(odd) == 2 and min(pos.values()) >= 2 and len(pos) == 4, ("odd lines bunched", odd, pos)
    for G in D["charts"]:
        v = [b[1] for b in G["bars"]]
        assert len(set(v)) == len(v) and all(5 <= x <= 50 and x % 5 == 0 for x in v), G["title"]
    for P in D["posters"]:
        name_parts([P["head"], P["img"], P["cap"], P["when"], P["con"]])
        name_parts([P["head"], P["img"], P["cap"], P["con"], P["when"]])
    return True

def check(q, D):
    d, a, W, t = q["data"], q["answer"], q["wrong"], q["data"]["t"]
    assert len(W) == q["nw"] and len(set(W + [a])) == len(W) + 1, "options not distinct / wrong count"
    if t == "fo":
        s = text(q["html"]); assert s == d["s"]
        assert a == kind(s), ("fo", s, a); assert W == [x for x in FO if x != a]
    elif t in ("spot", "line"):
        lines = [H.unescape(re.sub(r"<[^>]+>", "", x)).strip() for x in re.findall(r"<p[^>]*>(.*?)</p>", q["html"])]
        lines = [re.sub(r"^\d+\s+", "", l) for l in lines]
        assert len(lines) == 4
        ks = [kind(l) for l in lines]
        if t == "spot":
            odd = min(set(ks), key=ks.count); assert ks.count(odd) == 1
            assert ("only fact" in q["en"]) == (odd == FO[0]) and ("only opinion" in q["en"]) == (odd == FO[1]), ("question asks for the wrong kind", q["en"])
            assert a == "Line %d" % (ks.index(odd) + 1), ("spot answer", lines, a)
            assert set(W) == set(LINES) - {a}
        else:
            hl = [i for i, x in enumerate(re.findall(r"<p([^>]*)>", q["html"])) if "hl" in x]
            assert len(hl) == 1 and q["en"].startswith("Line %d" % (hl[0] + 1)), "highlighted line ≠ asked line"
            assert a == ks[hl[0]], ("line kind", lines[hl[0]], a)
    elif t in ("most", "least", "value", "diff"):
        v = measure(q["html"])
        if t == "most": assert a == max(v, key=v.get) and set(W) <= set(v)
        elif t == "least": assert a == min(v, key=v.get) and set(W) <= set(v)
        elif t == "value":
            lab = re.match(r"📊 How many: (.+)\?$", q["en"]).group(1); assert int(a) == v[lab], ("value", lab, a, v[lab])
            assert all(int(w) > 0 and int(w) != v[lab] for w in W)
        else:
            m = re.match(r"📊 How many more: (.+) than (.+)\?$", q["en"]); x, y = m.group(1), m.group(2)
            assert v[x] > v[y] and int(a) == v[x] - v[y], ("diff", x, y, a)
            assert all(int(w) > 0 and int(w) != int(a) for w in W)
    elif t == "poster":
        blocks = re.findall(r'<div class="pp ([^"]*)">(.*?)</div>', q["html"])
        names = name_parts([H.unescape(b) for _, b in blocks])
        hl = [i for i, (c, _) in enumerate(blocks) if "hl" in c.split()]
        assert len(hl) == 1, "one highlighted part"
        assert a == names[hl[0]], ("poster part", blocks[hl[0]], a, names[hl[0]])
        assert set(W) <= set(PARTS) - {a}
    else:
        raise AssertionError("unknown type " + t)

def main():
    src, page = sys.argv[1], sys.argv[2]
    D = load(page); data_pass(D)
    print(f"data pass OK: {len(D['fo']['f'])} facts, {len(D['fo']['o'])} opinions, {len(D['spot'])} texts, {len(D['charts'])} charts, {len(D['posters'])} posters")
    if src == "-": return
    n = bad = 0; types = Counter()
    for line in open(src, encoding="utf-8"):
        q = json.loads(line); n += 1; types[q["data"].get("t")] += 1
        try: check(q, D)
        except (AssertionError, KeyError, AttributeError) as e:
            bad += 1
            if bad <= 12: print("PROBLEM", q["mode"], q["data"].get("t"), repr(e)[:200])
    print(f"{n} questions, {bad} problems; types {dict(types)}")
    sys.exit(1 if bad or n == 0 else 0)

if __name__ == "__main__":
    main()
