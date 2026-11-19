#!/usr/bin/env python3
"""Independent checker for Format Fixer (JC English Order 15, letters & emails: formal and informal).
It does not trust the game's answers: it re-derives each one with its own rules.
  - register   its own lists of informal markers (INF: short forms, slang, "!!", text speak, first-name
               greetings) and formal markers (FORM: Dear Sir/Madam, Yours faithfully, I am writing, I would be
               grateful …): a line is formal if it hits FORM and no INF, informal if it hits INF and no FORM
  - sign-off   greeting rule: no name (Sir/Madam, To whom it may concern) → Yours faithfully; a title + surname
               (Mr / Ms / Mrs / Dr) → Yours sincerely; anything else (a first name, Gran) → Talk soon
  - parts      its own part rules (date pattern, "their address" starts with a role or title, your address
               has a county and no role, greeting, "I am writing" opening, closing phrases, Yours …)
  - next       reads the shown letter line by line, classifies each line, checks they are in letter order,
               and works out the next part
  - missing    reads the shown letter / email, finds which required part no line belongs to
  - tone       the formal version must have no informal marker; every wrong option must have at least one
Usage: N=400 node src/test_format_fixer.js format-fixer.html > /tmp/ff.jsonl && python3 src/test_format_fixer.py /tmp/ff.jsonl format-fixer.html
       python3 src/test_format_fixer.py - <page or json>   (data pass only)"""
import sys, json, re, html as H

FI = {"f": "📨 Formal", "i": "😊 Informal"}
SO = {"fa": "Yours faithfully,", "si": "Yours sincerely,", "in": "Talk soon,"}
PART = {"addr": "🏠 Your address", "date": "📅 Date", "their": "🏢 Their address", "greet": "👋 Greeting",
        "open": "🎯 Opening line", "close": "🙏 Closing line", "sign": "✍️ Sign-off"}
MISS = {"addr": "🏠 Your address", "date": "📅 Date", "subj": "📌 Subject line", "greet": "👋 Greeting",
        "sign": "✍️ Sign-off", "name": "🙋 Your name"}
LETTER = ["addr", "date", "their", "greet", "open", "body", "close", "sign", "name"]
EMAIL = ["to", "subj", "greet", "open", "body", "close", "sign", "name"]

TITLE = r"(Mr|Ms|Mrs|Dr|Miss|Professor)"
INF = [r"\b\w+n't\b", r"\b(I|you|we|they)'(m|re|ve|ll|d)\b", r"\b(it|that|what|there|he|she|let)'s\b", r"\b(she|he|it)'ll\b",
       r"!!", r"\b(hey|hi|hiya|gimme|gonna|wanna|yeah|ya|ye|u|cheers|lol|btw|asap|cool|deadly|grand|soz|ugh|rank|gross|"
       r"loads|tons|heaps|super|totally|wrecked|mad busy|well up for|no way|no worries|guess what|thanks a mil|"
       r"chat soon|talk soon|see you|mam|xx|grab)\b", r"\bso{3,}\b", r"\blike,|, like\b", r"to be honest",
       r"^Love,", r"of love\b", r"^Dear (?!" + TITLE + r"\b|Sir\b)[A-Z]\w*,", r"\bOK\b"]
FORM = [r"^Dear (Sir|Madam|" + TITLE + r" )", r"^To whom it may concern", r"^Yours (faithfully|sincerely),$", r"^Kind regards,$",
        r"\bI am writing\b", r"\bI would be (grateful|happy)\b", r"\bI look forward\b", r"\bI wish to\b", r"^Thank you\b",
        r"\bI would (like|appreciate)\b", r"\bI apologise\b", r"^Could you please\b", r"\bI regret\b", r"\bWe would like\b"]
MONTHS = "January|February|March|April|May|June|July|August|September|October|November|December"
ROLE = r"^(The (Manager|Editor|Principal|Secretary)|Customer Service|" + TITLE + r" [A-Z])"
STOP = set("the a an and to of for my your our in on at is was be i you we it that with this if could would".split())

def inf(s): return [p for p in INF if re.search(p, s, flags=0 if p.startswith("^Dear") or p.startswith("^Love") or "OK" in p else re.I)]
def form(s): return [p for p in FORM if re.search(p, s)]
def register(s):
    a, b = bool(inf(s)), bool(form(s))
    return "i" if a and not b else "f" if b and not a else None

def signoff(g):
    if re.match(r"^(Dear Sir(/| or )Madam|To whom it may concern),$", g): return "fa"
    if re.match(r"^Dear " + TITLE + r" [A-Z][\w'ÁÉÍÓÚáéíóú ]+,$", g): return "si"
    return "in"

def part(s):
    """s = one block of a letter (multi-line blocks joined with ' / ')."""
    ls = s.split(" / ")
    hits = []
    if re.fullmatch(r"\d{1,2} (" + MONTHS + r") 20\d\d", s): hits.append("date")
    if len(ls) >= 3 and re.match(ROLE, ls[0]) and re.match(r"^Co\. [A-Z]", ls[-1]): hits.append("their")
    if len(ls) >= 3 and not re.match(ROLE, ls[0]) and re.match(r"^Co\. [A-Z]", ls[-1]): hits.append("addr")
    if re.match(r"^(Dear .+|To whom it may concern),$", s): hits.append("greet")
    if re.match(r"^I am writing\b", s): hits.append("open")
    if re.match(r"^(I look forward|Thank you|I would be grateful|I hope you will)\b", s): hits.append("close")
    if re.fullmatch(r"Yours (faithfully|sincerely),", s): hits.append("sign")
    if s.startswith("To: "): hits.append("to")
    if s.startswith("Subject: "): hits.append("subj")
    if re.fullmatch(r"[A-ZÁÉÍÓÚ][\wáéíóú']+ [A-ZÁÉÍÓÚ][\wáéíóú']+", s): hits.append("name")
    if not hits and len(ls) == 1 and s.endswith(".") and not re.match(r"^I am writing", s): hits.append("body")
    return hits[0] if len(hits) == 1 else None

def blocks(h):
    out = []
    for m in re.finditer(r'<div class="ffl([^"]*)">(.*?)</div>', h):
        if "gap" in m.group(1): continue
        t = re.sub(r"<br>", " / ", m.group(2)); t = H.unescape(re.sub(r"<[^>]+>", "", t))
        out.append(t)
    return out

def load(path):
    s = open(path, encoding="utf-8").read()
    if path.endswith(".json"): return json.loads(s)
    return json.loads(s[s.index("/*DATA*/") + 8:s.index("/*END*/")])

def data_pass(D):
    errs = []
    for line, k in D["sort"]:
        if register(line) != k: errs.append(f"sort: {line!r} reads as {register(line)}, tagged {k} (inf={inf(line)}, form={form(line)})")
    for g, k in D["greet"]:
        if signoff(g) != k: errs.append(f"greet: {g!r} → {signoff(g)}, tagged {k}")
    for kind, items, order in (("letter", D["letters"], LETTER), ("email", D["emails"], EMAIL)):
        for L in items:
            for k in order:
                v = L[k]; s = " / ".join(v) if isinstance(v, list) else ("To: " + v if k == "to" else v)
                if part(s) != k: errs.append(f"{kind}: {s!r} reads as part {part(s)}, should be {k}")
                if k != "name" and inf(s): errs.append(f"{kind}: informal marker in {s!r}: {inf(s)}")
            if SO[signoff(L["greet"])] != L["sign"]: errs.append(f"{kind}: {L['greet']!r} needs {SO[signoff(L['greet'])]} not {L['sign']}")
    for cas, ans, wr in D["tone"]:
        if not inf(cas): errs.append(f"tone: casual line has no informal marker: {cas!r}")
        if inf(ans): errs.append(f"tone: answer {ans!r} is informal: {inf(ans)}")
        for w in wr:
            if not inf(w): errs.append(f"tone: wrong option {w!r} has no informal marker")
        if len(set(wr + [ans])) != 4: errs.append(f"tone: duplicate options {cas!r}")
    return errs

def check(q, D):
    t, a, w, h = q["data"]["t"], q["answer"], q["wrong"], q["html"]
    e = []
    if len(w) != q["nw"] or len(set(w)) != len(w) or a in w: e.append("option count/duplicates")
    if t == "sort":
        k = register(q["data"]["s"])
        if FI.get(k) != a: e.append(f"register {k}")
        if set(w) != set(FI.values()) - {a}: e.append("wrong set")
    elif t == "sign":
        k = signoff(q["data"]["s"])
        if SO[k] != a: e.append(f"sign-off should be {SO[k]}")
        if set(w) != set(SO.values()) - {a}: e.append("wrong set")
    elif t == "part":
        k = part(q["data"]["s"])
        if PART.get(k) != a: e.append(f"part {k}")
        if not set(w) <= set(PART.values()): e.append("wrong labels")
    elif t == "next":
        if "ffl gap" not in h: e.append("no gap")
        ks = [part(b) for b in blocks(h)]
        if None in ks or ks != LETTER[:len(ks)]: e.append(f"shown parts {ks}")
        nxt = [k for k in LETTER[len(ks):] if k != "body"]
        if not nxt or PART.get(nxt[0]) != a: e.append(f"next should be {nxt[:1]}")
        if not set(w) <= set(PART.values()): e.append("wrong labels")
    elif t == "miss":
        bs = blocks(h); ks = [part(b) for b in bs]
        if None in ks: e.append(f"unreadable line {bs[ks.index(None)]!r}")
        email = "to" in ks
        need = ["subj", "greet", "sign", "name"] if email else ["addr", "date", "greet", "sign"]
        if email != (q["data"]["kind"] == "email"): e.append("kind")
        miss = [k for k in need if k not in ks]
        if len(miss) != 1 or MISS[miss[0]] != a: e.append(f"missing {miss}")
        if set(w) != {MISS[k] for k in need} - {a}: e.append("wrong set")
        order = EMAIL if email else LETTER
        if [k for k in order if k in ks] != ks: e.append("lines out of order")
    elif t == "tone":
        if inf(a): e.append(f"answer informal {inf(a)}")
        for x in w:
            if not inf(x): e.append(f"wrong option formal: {x!r}")
        if not inf(q["data"]["s"]): e.append("prompt not casual")
    else: e.append("unknown type")
    return e

if __name__ == "__main__":
    src = sys.argv[2] if len(sys.argv) > 2 else "format-fixer.html"
    D = load(src); errs = data_pass(D)
    for x in errs: print("DATA", x)
    n = bad = 0; seen = {}
    if sys.argv[1] != "-":
        for line in open(sys.argv[1], encoding="utf-8"):
            q = json.loads(line); n += 1; e = check(q, D)
            seen[q["data"]["t"]] = seen.get(q["data"]["t"], 0) + 1
            if e:
                bad += 1
                if bad <= 15: print("BAD", q["mode"], q["data"].get("s", q["data"].get("rv")), q["answer"], e)
    print(f"data problems: {len(errs)} · questions: {n} · problems: {bad} · types: {seen}")
    sys.exit(1 if errs or bad or (sys.argv[1] != "-" and n < 100) else 0)
