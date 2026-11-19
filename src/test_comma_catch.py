#!/usr/bin/env python3
"""Independent checker for Comma Catch (JC English Order 3, Punctuation 1).
Re-derives every answer from its own rules (not the game's code):
  commas      -> where the commas must go, from the rule + key words in the data (list / opening words / name / Yes-No-Well / extra info)
  capitals    -> its own lists of words that always / never take a capital
  apostrophes -> owner + how many (read from the picture), with its own irregular-plural list
  it's / its  -> spaCy tags the word after the gap: a noun there means a belonging word (its, your, their, whose), otherwise a short form
  end marks   -> question / exclamation / statement rules
Usage: N=400 node src/test_comma_catch.js comma-catch.html > /tmp/cc.jsonl && python3 src/test_comma_catch.py /tmp/cc.jsonl comma-catch.html"""
import sys, json, re, html as H
import spacy
nlp = spacy.load("en_core_web_sm")

# ---------- capitals ----------
PROPER = {"monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday",
          "january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december",
          "irish", "english", "french", "spanish", "german", "easter", "christmas", "i", "dr", "mr", "mrs", "ms",
          "spain", "ireland", "paris", "dublin", "cork", "limerick", "sligo", "kerry", "kilkenny", "galway", "mars", "river", "shannon",
          "aoife", "tom", "lisa", "seamus", "heaney", "walsh", "seán", "ciara", "liam", "niall", "sarah",
          "fridays", "saturdays", "mondays", "kinsale", "blarney", "lee", "niamh", "orla", "rex", "ben", "byrne", "croke", "park"}
LOWER = {"summer", "winter", "autumn", "spring", "maths", "science", "history", "geography", "mum", "dad", "school", "doctor", "teacher", "birthday"}
def caps_ok(s):
    w = [re.sub(r"[^\wáéíóú]", "", re.sub(r"'s?[.,?!]*$", "", x)) for x in s.split(" ")]   # Aoife's -> Aoife
    if not w[0][:1].isupper(): return False
    for i, x in enumerate(w):
        lo = x.lower()
        if lo in PROPER and not x[:1].isupper(): return False
        if i > 0 and x[:1].isupper() and lo not in PROPER: return False
        if lo in LOWER and i > 0 and x[:1].isupper(): return False
    return True

# ---------- commas ----------
def comma_ok(s, c, k):
    n = s.count(",")
    if c == "list":
        return (", ".join(k[:-1]) + " and " + k[-1]) in s and n == len(k) - 2
    if c in ("intro", "yes"):
        return s.startswith(k + ", ") and n == 1
    if c == "address":
        return (s.startswith(k + ", ") or re.search(", " + re.escape(k) + r"[.?!]$", s) is not None) and n == 1
    if c == "aside":
        return (", " + k + ", ") in s and n == 2
    raise ValueError(c)
def nocomma(s): return s.replace(",", "")

# ---------- apostrophes ----------
IRR = {"child": "children", "man": "men", "woman": "women"}

# ---------- short forms ----------
EXP = {"it's": ["it is", "it has"], "can't": ["cannot"], "we're": ["we are"], "she's": ["she is", "she has"], "don't": ["do not"],
       "who's": ["who is", "who has"], "you're": ["you are"], "won't": ["will not"], "they're": ["they are"]}
POSS = {"its", "your", "their", "whose"}

# ---------- end marks ----------
QW = {"who", "what", "where", "when", "why", "how", "do", "does", "did", "is", "are", "was", "were", "can", "could", "will", "would", "have", "has", "should"}
SUBJ = {"i", "you", "he", "she", "it", "we", "they"}
def end_mark(s):
    w = s.lower().split()
    if w[0] == "what" and w[1] in ("a", "an"): return "!"
    if w[0] == "how" and len(w) > 2 and w[2] in SUBJ: return "!"   # How kind you are! / How old is your brother?
    if w[0] in QW: return "?"
    return "."
MARK = {"Full stop .": ".", "Question mark ?": "?", "Exclamation mark !": "!", "Comma ,": ","}

bad = 0; n = 0; seen = set()
page = open(sys.argv[2], encoding="utf-8").read() if len(sys.argv) > 2 else None
D = json.loads(page.split("/*DATA*/")[1].split("/*END*/")[0]) if page else None
COMMA = {x["s"]: x for x in D["comma"]} if D else {}
def problem(*a):
    global bad; bad += 1
    if bad < 30: print("FAIL", *a)
for line in open(sys.argv[1]):
    q = json.loads(line); n += 1; d = q["data"]; t = d["t"]; a = q["answer"]; W = q["wrong"]; opts = [a] + W
    frame = H.unescape(re.sub("<[^>]+>", " ", q["html"]))
    if len(W) != 3: problem("not 3 wrong options", a, W)
    if len(set(opts)) != 4: problem("duplicate option", opts)
    if any(re.search(r"undefined|NaN|null", o) for o in opts + [q["en"], q["why"]]): problem("bad text", opts)
    seen.add((t, a, frame))
    if t == "comma":
        c, k = d["c"], d["k"]
        if not comma_ok(a, c, k): problem("answer breaks the comma rule", a)
        it = COMMA.get(a)
        for w in W:
            if nocomma(w) != nocomma(a): problem("wrong option changes the words", w)
            if comma_ok(w, c, k): problem("wrong option is also right", w)
            if it and w in it.get("ok", []): problem("offered an accepted version as wrong", w)
            if it and not it["req"] and "," not in w: problem("no-comma version offered where it's acceptable", w)
            if w.count(",") > 0 and re.search(r",\s*[.?!]|^,|,,", w): problem("comma in a silly place", w)
    elif t == "caps":
        if not caps_ok(a): problem("answer breaks the capitals rules", a)
        for w in W:
            if w.lower() != a.lower(): problem("wrong option changes the words", w)
            if caps_ok(w): problem("wrong option is also right", w)
    elif t == "own":
        label = frame.split()[-1]                      # the owner as the picture shows it: "dog", "dogs", "children", "Sarah"
        nn = 2 if "more than one" in frame else 1
        if nn != d["n"]: problem("picture and data disagree", frame)
        pic = frame.split()[0]
        if nn == 2 and not (len(pic) % 3 == 0 and pic[:len(pic) // 3] * 3 == pic): problem("many owners but not 3 pictures", frame)
        form = label + "'s" if nn == 1 or not label.endswith("s") else label + "'"
        if form not in a.split(" "): problem(f"answer should use {form}", a, frame)
        for w in W:
            if form in w.split(" "): problem("wrong option uses the right form", w)
    elif t == "short":
        s = d["sent"]; filled = s.replace("___", a)
        doc = nlp(filled); i0 = len(s.split("___")[0]); after = [tk for tk in doc if tk.idx >= i0 + len(a)][0]
        lo = a.lower()
        if after.pos_ in ("NOUN", "PROPN"):
            if lo not in POSS: problem("noun after the gap needs a belonging word", filled)
        else:
            if lo not in EXP: problem("no noun after the gap: needs a short form", filled, after.pos_)
            elif not any(e in q["why"].lower() for e in EXP[lo]): problem("why doesn't give the long form", q["why"])
        for w in W:
            if w.lower() == lo: problem("wrong option same as answer", w)
    elif t == "end":
        if MARK[a] != end_mark(d["sent"]) or MARK[a] != d["mark"]: problem("end mark", d["sent"], a)
        if "Comma ," == a: problem("comma as an ending")
# ---------- full pass over the data block ----------
if D:
    for it in D["comma"]:
        if not comma_ok(it["s"], it["c"], it["k"]): problem("DATA comma", it["s"])
        for o in it.get("ok", []):
            if nocomma(o) != nocomma(it["s"]): problem("DATA ok version changes words", o)
    for s in D["caps"]:
        a = s.replace("~", "")
        if not caps_ok(a): problem("DATA caps", a)
        for w in s.split(" "):
            if w.startswith("~") and re.sub(r"\W", "", w[1:]).lower() not in LOWER: problem("DATA trap word not in LOWER list", w)
    for one, many, nn, thing, emo, the in D["own"]:
        if many and IRR.get(one, one + "s") != many: problem("DATA plural", one, many)
    for s, a, wr, why in D["short"]:
        if a in wr or len(set(wr)) != 3 or s.count("___") != 1: problem("DATA short", s)
    for s, m in D["end"]:
        if end_mark(s) != m: problem("DATA end", s, m)
print(n, "questions,", len(seen), "different,", bad, "problems")
sys.exit(1 if bad else 0)
