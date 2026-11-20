"""Independent checker for Who Said It? (Order 28, Shakespeare, Higher Level).
Every quote is looked up in the NLTK Shakespeare corpus (src/shakespeare_corpus.py): the speaker, act and scene come
from the play's text, not from the game. Techniques are judged by this file's own rules, old words by its own glossary,
and plot order by where each moment's quote sits in the play.
Usage:  N=400 node src/test_who_said_it.js who-said-it.html > /tmp/wsi.jsonl && python3 src/test_who_said_it.py /tmp/wsi.jsonl who-said-it.html
        python3 src/test_who_said_it.py - <page or json>     (data pass only)
Importable: load, data_pass, speaker, technique, gloss, play_of, order_key, PLAYS, LABEL"""
import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shakespeare_corpus import where, find, words, speeches
import pronouncing

PLAYS = {"rj": "Romeo and Juliet", "mv": "The Merchant of Venice", "jc": "Julius Caesar"}
LABEL = {"rj": "📕 Romeo and Juliet", "mv": "💰 The Merchant of Venice", "jc": "🗡️ Julius Caesar"}

def load(path):
    s = open(path, encoding="utf8").read()
    if path.endswith(".json"):
        return json.loads(s)
    m = re.search(r"/\*DATA\*/(.*?)/\*END\*/", s, re.S)
    return json.loads(m.group(1))

def plain(q):
    return q.replace(" / ", " ").replace("{", "").replace("}", "")

def speaker(play, quote):
    """(Speaker name as on the site, act, scene) from the corpus."""
    who, a, sc, pos = where(play, plain(quote))
    return who.title(), a, sc

def play_of(quote):
    hits = [p for p in PLAYS if find(p, plain(quote))]
    assert len(hits) == 1, (quote, hits)
    return hits[0]

def order_key(play, quote):
    return where(play, plain(quote))[3]

# ---------- techniques: this file's own rules ----------
OPP = [("love", "hate"), ("loving", "hate"), ("brawling", "love"), ("sweet", "sorrow"), ("beautiful", "tyrant"),
       ("fiend", "angelical"), ("bright", "smoke"), ("cold", "fire"), ("sick", "health"), ("heavy", "lightness"),
       ("serious", "vanity"), ("feather", "lead")]
def is_oxy(s):
    w = words(s)
    for a, b in OPP:
        for i, x in enumerate(w):
            if x == a and b in w[i + 1:i + 6]:
                return True
    return False
def is_simile(s):
    t = " " + s.lower() + " "
    return bool(re.search(r"\blike (a|an|the)\b|\bas \w+ as\b|\bas (a|an|the)\b|, as \w+ from\b", t))
def rhyme_part(w):
    p = pronouncing.phones_for_word(w)
    return re.sub(r"\d", "", pronouncing.rhyming_part(p[0])) if p else None
def is_couplet(s):
    if " / " not in s:
        return False
    a, b = s.split(" / ")
    la, lb = words(a)[-1], words(b)[-1]
    ra, rb = rhyme_part(la), rhyme_part(lb)
    return ra is not None and ra == rb and la != lb
def is_question(s):
    return s.rstrip().endswith("?")
TECH = {"ox": is_oxy, "si": is_simile, "co": is_couplet, "qu": is_question}
def technique(s):
    hits = [k for k, f in TECH.items() if f(s)]
    assert len(hits) == 1, (s, hits)
    return hits[0]
TLAB = {"ox": "🔀 Oxymoron", "si": "🤝 Simile", "co": "🎵 Rhyming couplet", "qu": "❓ Rhetorical question"}

# ---------- old words: this file's own glossary ----------
GLOSS = {"wherefore": "why", "thy": "your", "'tis": "it is", "wilt": "will", "thee": "you", "thou": "you", "anon": "in a moment",
         "art": "are", "nay": "no", "ay": "yes", "ere": "before", "sooth": "truth", "hath": "has", "oft": "often", "tarry": "wait",
         "yond": "that (over there)", "hence": "go away", "dost": "do", "doth": "does", "prithee": "please"}
CLOSE = [{"do", "does"}, {"you", "your"}, {"has", "does"}, {"in a moment", "wait"}]
def gloss(item):
    w = re.search(r"\{([^}]*)\}", item).group(1).lower()
    return GLOSS[w]

def data_pass(D):
    n = 0
    for p, q, k, asc, why in D["lines"]:
        who, a, sc = speaker(p, q)
        assert "%d.%d" % (a, sc) == asc, (q, a, sc, asc)
        assert play_of(q) == p, q
        n += 1
    for p, q, k in D["tech"]:
        assert find(p, plain(q)), q
        assert technique(q) == k, (q, technique(q), k)
        n += 1
    for p, q, m in D["old"]:
        assert find(p, plain(q)), q
        assert gloss(q) == m, (q, gloss(q), m)
        n += 1
    seen = {}
    for p, ev, q in D["plot"]:
        pos = order_key(p, q)
        assert (p, pos) not in seen, (ev, seen.get((p, pos)))
        seen[(p, pos)] = ev
        n += 1
    return n

def check(rows, D):
    keys = {(p, q): (p, q, k, a, w) for p, q, k, a, w in D["lines"]}
    ev2q = {ev: (p, q) for p, ev, q in D["plot"]}
    bad = 0; seen = 0
    for r in rows:
        d = r["data"]; t = d["t"]; ans = r["answer"]; wr = r["wrong"]; nw = r.get("nw") or 3
        try:
            assert len(wr) == nw and len(set(wr)) == nw and ans not in wr, "options"
            assert "{" not in r["html"], "gap brace leaked"
            if t == "who":
                who, a, sc = speaker(d["p"], d["q"])
                assert ans == who, (ans, who)
                assert LABEL[d["p"]] in r["html"], "play label missing"
                cast = {w.title() for sp in speeches(d["p"]) for w in sp["who"]}
                for x in wr:
                    assert x.upper() != who.upper(), (x, who)
                    assert x in cast, ("not a speaker in this play", x)
                assert ("Act %d, Scene %d" % (a, sc)) in r["why"], r["why"]
            elif t == "play":
                p = play_of(d["q"])
                assert ans == LABEL[p], (ans, p)
                assert set(wr) == set(LABEL.values()) - {ans}
            elif t == "tech":
                k = technique(d["q"])
                assert ans == TLAB[k], (ans, k)
                assert set(wr) <= set(TLAB.values())
            elif t == "old":
                m = gloss(d["q"])
                assert ans == m, (ans, m)
                for x in wr:
                    assert x != m and {x, m} not in CLOSE, (x, m)
                    assert x in GLOSS.values()
            elif t == "order":
                p = d["p"]; evs = d["ev"]
                for e in evs:
                    assert ev2q[e][0] == p
                order = sorted(range(4), key=lambda i: order_key(p, ev2q[evs[i]][1]))
                right = " → ".join("ABCD"[i] for i in order)
                assert ans == right, (ans, right)
                for x in wr:
                    assert sorted(x.split(" → ")) == list("ABCD")
            else:
                raise AssertionError("unknown type " + t)
            seen += 1
        except AssertionError as e:
            bad += 1
            if bad <= 10:
                print("PROBLEM", t, e, json.dumps(r, ensure_ascii=False)[:300])
    return seen, bad

if __name__ == "__main__":
    if sys.argv[1] == "-":
        D = load(sys.argv[2]); print("data pass OK:", data_pass(D), "items"); sys.exit(0)
    D = load(sys.argv[2])
    print("data pass OK:", data_pass(D), "items")
    rows = [json.loads(l) for l in open(sys.argv[1], encoding="utf8") if l.strip()]
    seen, bad = check(rows, D)
    from collections import Counter
    print(Counter(r["data"]["t"] for r in rows))
    print("checked", seen + bad, "questions,", bad, "problems")
    sys.exit(1 if bad else 0)
