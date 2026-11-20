#!/usr/bin/env python3
"""Independent checker for Shot Spotter (JC English Order 27, film).
Usage: N=400 node src/test_shot_spotter.js shot-spotter.html > /tmp/sh.jsonl && python3 src/test_shot_spotter.py /tmp/sh.jsonl shot-spotter.html
       python3 src/test_shot_spotter.py - <page or json>   (data pass only)
Shot sizes and angles are MEASURED from the drawn SVG (the figure's transform: person 100 units tall, head top 0,
eyes 6.6, chin 13, shoulders 15, waist 52, feet 100; frame 320 x 200). Text items are classified by this file's own
word rules (no spaCy needed). Importable: shot_of, angle_of, why_of, sound_of, music_of, edit_of, data_pass, load."""
import json, re, sys, math
H = 200.0

SHOT = {"els": "Extreme long shot", "ls": "Long shot", "ms": "Medium shot", "cu": "Close-up", "ecu": "Extreme close-up"}
ANG = {"hi": "High angle", "lo": "Low angle", "eye": "Eye level", "bird": "Bird's-eye view"}
WHY = {"est": "Establishing shot", "cu": "Close-up", "lo": "Low angle", "hi": "High angle", "pov": "Point-of-view shot"}
SND = {"di": "Diegetic (in the scene)", "nd": "Non-diegetic (added)"}
MUS = {"te": "Low drums, getting faster", "jo": "Bright, bouncy fiddle", "sa": "Slow, soft piano", "ca": "Gentle, quiet flute"}
EDT = {"cut": "Quick cuts", "slow": "Slow motion", "flash": "Flashback", "fade": "Fade to black", "mont": "Montage"}

def strip(lab): return re.sub(r"^\S+\s", "", lab)  # drop the emoji

FIG = re.compile(r'<g class="fig" transform="translate\(([-\d.]+),([-\d.]+)\) scale\(([-\d.]+)\)"')
CAM = re.compile(r'<g class="cam" transform="translate\(([-\d.]+),([-\d.]+)\) rotate\(([-\d.]+)\)"')

def shot_of(html):
    """measure which part of the body is inside the 200-high frame"""
    m = FIG.findall(html); assert len(m) == 1, "one figure expected"
    x, y, s = map(float, m[0]); P = 100 * s
    top, eyes, chin, feet = y, y + 6.6 * s, y + 13 * s, y + P
    if not (-0.5 * 320 < x < 1.5 * 320): return None
    if feet <= H and top >= 0:
        r = P / H
        if r <= 0.3: return "els"
        if r >= 0.5: return "ls"
        return None
    if feet <= H: return None
    if top < 0 and chin > H and 0 < eyes < H: return "ecu"
    if top < -0.02 * P: return None
    f = (H - y) / P  # how far down the body the frame's bottom edge cuts
    if 0.17 <= f <= 0.35: return "cu"
    if 0.40 <= f <= 0.65: return "ms"
    return None

def angle_of(html):
    """where the camera is, from the camera's position and which way it points"""
    m = FIG.findall(html); c = CAM.findall(html); assert len(m) == 1 and len(c) == 1
    px, py, s = map(float, m[0]); cx, cy, rot = map(float, c[0])
    ey = py + 6.6 * s
    if abs(px - cx) < 15 and cy < py:
        return "bird" if abs(rot - 90) < 3 else None
    a = math.degrees(math.atan2(ey - cy, px - cx))
    if abs(a - rot) > 3: return None  # the lens must point at the eyes
    if a > 10: return "hi"
    if a < -10: return "lo"
    if abs(a) < 2: return "eye"
    return None

R_WHY = {
 "est": r"\bwhere (the story is set|we are)\b|\bthe whole (\w+ )?(village|city|town|valley)\b|\bset the scene\b|\bbefore we meet anyone\b|\bat night\b",
 "cu": r"\b(face|tears|reaction|expression)\b",
 "lo": r"\b(powerful|strong|in charge|towering|threat|frightening)\b",
 "hi": r"\b(tiny|small|weak|helpless|powerless)\b",
 "pov": r"\b(sees it|through [\w']+ eyes|as if we are|what the \w+ sees)\b"}
R_SND = {
 "di": r"\bradio\b|\bphone rings\b|\bwhistle|\bfootsteps\b|\bdog barks\b|\bband at\b|\bthunder\b|\bwe hear every word\b|\bbell rings\b|\bcar horn\b|\bcrowd chants\b",
 "nd": r"\bsoundtrack\b|\bvoice-over\b|\bnarrator\b|\bover the scene\b|\bcan't hear\b|\bnobody in the room can hear\b|\borchestra\b|\btheme tune\b|\badded over\b"}
R_MUS = {
 "te": r"\b(hides|dark|ticking|creeps|chase|danger)\b",
 "jo": r"\b(wins|dancing|celebrate|party|cheer\w*)\b",
 "sa": r"\b(goodbye|grave|alone|cries|funeral)\b",
 "ca": r"\b(drifts|sunrise|sleeps|still|calm|silent)\b"}
R_EDT = {
 "cut": r"\bflicks between\b|\bquickly between\b|\bevery second\b|\bhalf a second\b|\brapid\b",
 "slow": r"\bfloats\b|\bhangs in the air\b|\btake forever\b|\bslower than real life\b|\bdrop by drop\b",
 "flash": r"\byears (earlier|before)\b|\bas a (little )?(girl|boy|child)\b|\bback to the day\b|\bback in time\b|\bwhen (he|she) was (five|six|young)\b",
 "fade": r"\b(goes|turns) black\b|\bdarkens until\b",
 "mont": r"\bweeks\b|\bmonths\b|\bover the summer\b|\bdays pass\b|\bseries of short clips\b"}
LEAK = r"close-up|establishing|\bangle\b|point of view|point-of-view|slow motion|flashback|montage|\bfade|diegetic|quick cuts|long shot|medium shot"

def classify(s, R):
    hits = [k for k, r in R.items() if re.search(r, s, re.I)]
    return hits[0] if len(hits) == 1 else None
def why_of(s): return classify(s, R_WHY)
def sound_of(s): return classify(s, R_SND)
def music_of(s): return classify(s, R_MUS)
def edit_of(s): return classify(s, R_EDT)

def load(path):
    t = open(path, encoding="utf-8").read()
    if path.endswith(".json"): return json.loads(t)
    return json.loads(t.split("/*DATA*/", 1)[1].split("/*END*/", 1)[0])

def data_pass(D):
    errs = []
    for name, R, F in [("why", R_WHY, why_of), ("sound", R_SND, sound_of), ("music", R_MUS, music_of), ("edit", R_EDT, edit_of)]:
        seen = set()
        for s, k in D[name]:
            got = F(s)
            if got != k: errs.append(f"{name}: {s!r} is {k}, rules say {got} (hits {[x for x, r in R.items() if re.search(r, s, re.I)]})")
            if re.search(LEAK, s, re.I): errs.append(f"{name}: {s!r} names a technique")
            if s in seen: errs.append(f"{name}: duplicate {s!r}")
            seen.add(s)
        for k in R:
            if sum(1 for s, kk in D[name] if kk == k) < 4: errs.append(f"{name}: fewer than 4 items for {k}")
    return errs

def check(q):
    t = q["data"]["t"]; a = q["answer"]; w = q["wrong"]
    L = {"shot": SHOT, "angle": ANG, "why": WHY, "sound": SND, "music": MUS, "edit": EDT}[t]
    if t == "shot": k = shot_of(q["html"])
    elif t == "angle": k = angle_of(q["html"])
    else: k = {"why": why_of, "sound": sound_of, "music": music_of, "edit": edit_of}[t](q["data"]["s"])
    if k is None: return f"{t}: can't classify ({q['data'].get('s', 'drawing')})"
    if strip(a) != L[k]: return f"{t}: answer {a!r}, measured/ruled {L[k]!r}"
    want = 1 if t == "sound" else 3
    if len(w) != want or q["nw"] != want: return f"{t}: {len(w)} wrong options, want {want}"
    if len(set(w)) != len(w) or a in w: return f"{t}: duplicate options"
    for x in w:
        if strip(x) not in L.values() or strip(x) == L[k]: return f"{t}: odd wrong option {x!r}"
    if t in ("why", "sound", "music", "edit") and re.search(LEAK, q["data"]["s"], re.I): return f"{t}: question names a technique"
    if strip(a).lower() in re.sub("<[^>]+>", " ", q["html"]).lower(): return f"{t}: answer leaks into the card"
    return None

if __name__ == "__main__":
    src, page = sys.argv[1], sys.argv[2]
    D = load(page); errs = data_pass(D)
    for e in errs[:30]: print("DATA", e)
    n = 0; bad = 0; seen = {}
    if src != "-":
        for line in open(src, encoding="utf-8"):
            q = json.loads(line); n += 1
            e = check(q)
            if e:
                bad += 1
                if bad <= 20: print("BAD", e)
            else:
                seen.setdefault(q["data"]["t"], set()).add(q["answer"])
        for t, want in [("shot", 5), ("angle", 4), ("why", 5), ("sound", 2), ("music", 4), ("edit", 5)]:
            if n and len(seen.get(t, ())) != want: print("COVER", t, sorted(seen.get(t, ()))); bad += 1
    print(f"{n} questions, {bad} problems, {len(errs)} data problems")
    sys.exit(1 if bad or errs else 0)
