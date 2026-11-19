#!/usr/bin/env python3
"""Independent checker for Talk Tips (JC English Order 10, speaking & listening: talking to a group).
It does not trust the game's answers: it re-derives each one with its own rules.
  - habits     its own lexicons of good (GOOD) and poor (BAD) speaking/listening habits: each habit line must
               hit exactly one side, and the answer must be that side
  - openers    the best line must be a hook by its own rules (a question / a story opener / a number or fact),
               mention the topic (shared spaCy lemma) and contain no weak-opener marker (WEAK);
               every wrong option must contain a weak marker and the topic
  - hook type  question = ends with "?", story = starts with a time/story opener (STORY), fact = has a number
  - signposts  its own start / next-point / end lists (SIGN), matched at the start of the sentence
  - listening  a good reply asks a question, shares a content word (spaCy lemma) with what the friend said and
               has no put-down (RUDE); exactly one option may pass
  - discussion its own phrase lists (DISC): each phrase must hit exactly one job
Setup (new session): pip install --break-system-packages spacy + the en_core_web_sm 3.8.0 wheel.
Usage: N=400 node src/test_talk_tips.js talk-tips.html > /tmp/tt.jsonl && python3 src/test_talk_tips.py /tmp/tt.jsonl talk-tips.html
       python3 src/test_talk_tips.py - <page or json>   (data pass only)"""
import sys, json, re, html as H
import spacy
nlp = spacy.load("en_core_web_sm")

TIP = {"do": "👍 Do it", "avoid": "👎 Avoid it"}
HOOK = {"q": "❓ Question", "f": "📊 Fact", "s": "📖 Story"}
SIGNL = {"s": "🚀 Start", "m": "➡️ Next point", "e": "🏁 End"}
DISCL = {"ag": "🤝 Agree", "di": "🙅 Disagree politely", "jo": "🙋 Join in", "as": "🤔 Ask for more"}
GOOD = [r"\blook up\b", r"eye contact", r"loud(ly)? enough", r"\bslow down", r"\bpause", r"stand up straight",
        r"cue cards", r"\bsmile", r"\bpractise", r"deep breath", r"let others finish", r"\bnod\b",
        r"ask a question", r"vary your voice", r"time your talk"]
BAD = [r"read every word", r"stare at", r"\bmumble", r"\brush\b", r"“em”", r"\bfidget", r"turn your back",
       r"\binterrupt", r"check your phone", r"flat voice", r"laugh at", r"whisper to", r"long sentences", r"\bsway"]
WEAK = [r"going to talk about", r"\bem\b", r"\blike,", r"\bsorry\b", r"didn't really prepare", r"thanks for listening",
        r"that's all i know"]
STORY = r"^(When (I|my)\b|Last (summer|year|week|night)|(One|Two|Three) (years?|days?|weeks?) ago|One (day|morning|night|wet))"
NUM = r"\d|\b(hundreds?|thousands?|millions?|one|two|three|four|five|six|seven|eight|nine|ten)\b"
SIGN = {"s": r"^(First of all|To begin with|Firstly|I'd like to start|Let me begin|To start)",
        "m": r"^(Moving on|Secondly|Another (reason|point)|Next|On top of that|My second point|Also|In addition)",
        "e": r"^(To sum up|In conclusion|To finish|So, to wrap up|All in all|Thank you (all )?for listening)"}
RUDE = r"overrated|boring|\bdull\b|\bhate\b|waste of time|unhealthy|not a big deal|whatever|a pain|the worst|fail anyway|pointless|way better|cuter|cooler|beaten you|the star\b|\bugh\b"
DISC = {"ag": r"^I agree\b|great point|^exactly|think so too|you're right",
        "di": r"\bdisagree\b|not so sure|\bbut\b|differently",
        "jo": r"^(can|could|may) I\b|^if I could",
        "as": r"\byou\b.*\b(example|mean|explain|think|tell us more)\b.*\?$"}

def tip(s):
    s = s.lower(); g = any(re.search(p, s) for p in GOOD); b = any(re.search(p, s) for p in BAD)
    return {x for x, y in (("do", g), ("avoid", b)) if y}
def weak_marks(s): return [p for p in WEAK if re.search(p, s.lower())]
def hook_types(s):
    t = set()
    if s.rstrip().endswith("?"): t.add("q")
    if re.search(STORY, s): t.add("s")
    if not t and re.search(NUM, s.lower()): t.add("f")
    return t
def lemmas(s):
    return {t.lemma_.lower() for t in nlp(s) if t.pos_ in ("NOUN", "PROPN", "VERB", "ADJ", "NUM") and not t.is_stop and t.is_alpha}
def shares(a, b): return bool(lemmas(a) & lemmas(b))
def good_reply(friend, r):
    return r.rstrip().endswith("?") and shares(friend, r) and not re.search(RUDE, r.lower())
def sign(s): return {k for k, p in SIGN.items() if re.search(p, s)}
def disc(s): return {k for k, p in DISC.items() if re.search(p, s, re.I)}
def text(h): return H.unescape(re.sub("<[^>]+>", " ", h))

def check_open(topic, hook, wrong):
    e = []
    if len(hook_types(hook)) != 1: e.append(f"hook types {hook_types(hook)} in “{hook}”")
    if weak_marks(hook): e.append(f"hook “{hook}” has weak markers {weak_marks(hook)}")
    if not shares(topic, hook): e.append(f"hook “{hook}” doesn't mention {topic}")
    for w in wrong:
        if not weak_marks(w): e.append(f"weak opener “{w}” has no weak marker")
        if topic.lower() not in w.lower(): e.append(f"weak opener “{w}” off topic")
    return e
def check_listen(friend, good, bad):
    e = []
    if not good_reply(friend, good): e.append(f"“{good}” is not a good reply to “{friend}”")
    for b in bad:
        if good_reply(friend, b): e.append(f"“{b}” passes as a good reply to “{friend}”")
    kinds = [("question off topic", lambda b: b.endswith("?") and not shares(friend, b)),
             ("put-down", lambda b: bool(re.search(RUDE, b.lower())))]
    for name, f in kinds:
        if not any(f(b) for b in bad): e.append(f"no {name} among the poor replies to “{friend}”")
    return e

def load(path):
    raw_src = open(path, encoding="utf-8").read()
    return json.loads(raw_src.split("/*DATA*/")[1].split("/*END*/")[0]) if "/*DATA*/" in raw_src else json.loads(raw_src)

bad = n = 0
if __name__ == "__main__":
    D = load(sys.argv[2] if len(sys.argv) > 2 else sys.argv[1])
    OPEN = {o[0]: o for o in D["open"]}; LIST = {l[0]: l for l in D["listen"]}
    seen = set()
    if sys.argv[1] != "-":
        for raw in open(sys.argv[1]):
            q = json.loads(raw); n += 1; d = q["data"]; t = d["t"]; opts = [q["answer"]] + q["wrong"]
            def fail(msg):
                global bad; bad += 1
                if bad < 30: print("FAIL", t, msg, "|", q["en"], "|", opts)
            nw = q.get("nw") or 3
            if len(q["wrong"]) != nw: fail("wrong option count")
            if len(set(o.lower() for o in opts)) != len(opts): fail("duplicate option")
            if any(re.search(r"undefined|NaN|null", o) for o in opts + [q["en"], q["why"], text(q["html"])]): fail("bad text")
            shown = text(q["html"])
            if t == "tip":
                k = tip(d["s"])
                if len(k) != 1 or q["answer"] != TIP[list(k)[0]]: fail(f"habit rule finds {k}")
                if q["wrong"] != [v for v in TIP.values() if v != q["answer"]]: fail("wrong label")
                if d["s"] not in shown: fail("habit not shown")
            elif t == "open":
                topic = d["topic"]
                if topic.lower() not in shown.lower(): fail("topic not shown")
                good = [o for o in opts if hook_types(o) and not weak_marks(o) and shares(topic, o)]
                if good != [q["answer"]]: fail(f"hooks found: {good}")
                if any(not weak_marks(w) for w in q["wrong"]): fail("wrong option without a weak marker")
            elif t == "hook":
                k = hook_types(d["s"])
                if len(k) != 1 or q["answer"] != HOOK[list(k)[0]]: fail(f"hook rule finds {k}")
                if set(q["wrong"]) | {q["answer"]} != set(HOOK.values()): fail("labels")
                if d["s"] not in shown: fail("hook not shown")
            elif t == "sign":
                k = sign(d["s"])
                if len(k) != 1 or q["answer"] != SIGNL[list(k)[0]]: fail(f"signpost rule finds {k}")
                if set(q["wrong"]) | {q["answer"]} != set(SIGNL.values()): fail("labels")
                if d["s"] not in shown: fail("sentence not shown")
            elif t == "listen":
                f = d["s"]
                if f not in shown: fail("friend's line not shown")
                good = [o for o in opts if good_reply(f, o)]
                if good != [q["answer"]]: fail(f"good replies found: {good}")
            elif t == "disc":
                k = disc(d["s"])
                if len(k) != 1 or q["answer"] != DISCL[list(k)[0]]: fail(f"discussion rule finds {k}")
                if d["s"] not in shown: fail("phrase not shown")
            seen.add((t, d.get("s") or d.get("topic")))
        print(f"{n} questions, {bad} problems, {len(seen)} different items")

    errs = []
    for k, s in D["tips"]:
        if tip(s) != {k}: errs.append(f"habit “{s}”: rule finds {tip(s)}, data says {k}")
    W = None
    for topic, emo, hook in D["open"]:
        wrong = [f"Today I'm going to talk about {topic}.", f"Em, so, like, em, it's about {topic}, yeah.",
                 f"Sorry, I didn't really prepare. It's about {topic}.", f"That's all I know about {topic}. Thanks for listening."]
        errs += check_open(topic, hook, wrong)
    types = [list(hook_types(h))[0] for _, _, h in D["open"] if len(hook_types(h)) == 1]
    if min(types.count(x) for x in "qfs") < 4: errs.append(f"hook types unbalanced: {[(x, types.count(x)) for x in 'qfs']}")
    for s, k in D["sign"]:
        if sign(s) != {k}: errs.append(f"signpost “{s}”: rule finds {sign(s)}, data says {k}")
    for f, g, b in D["listen"]: errs += check_listen(f, g, b)
    for s, k in D["discuss"]:
        if disc(s) != {k}: errs.append(f"phrase “{s}”: rule finds {disc(s)}, data says {k}")
    for name, i in (("tips", 1), ("sign", 0), ("discuss", 0)):
        xs = [x[i] for x in D[name]]
        if len(set(xs)) != len(xs): errs.append(f"duplicate in {name}")
    print("data block:", len(errs), "problems")
    for x in errs[:40]: print("  ", x)
    bad += len(errs)
    sys.exit(1 if bad else 0)
