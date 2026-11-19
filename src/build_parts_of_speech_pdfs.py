#!/usr/bin/env python3
"""Parts of speech (JC English topic 1, game Word Sort): free sheet + teacher pack + Payhip cover.
Run from the repo root: python3 src/build_parts_of_speech_pdfs.py OUTDIR
Writes src/parts-of-speech-*.html; PDFs/cover PNG go to OUTDIR (free sheet also to printables/).
Sentences come from the game's own data block (word-sort.html) and every word-class answer is re-checked
with spaCy (same rules as src/test_word_sort.py). Styles are read from src/build_money1_pdfs.py."""
import os, sys, random, subprocess, re, json
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC)
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/pos"; os.makedirs(OUT, exist_ok=True)
SLUG = "parts-of-speech"
LO = "W10, W12, R11, OL12"
GAME = "leim.ie/word-sort.html"

import spacy
nlp = spacy.load("en_core_web_sm")
UP = {"n": {"NOUN", "PROPN"}, "v": {"VERB", "AUX"}, "adj": {"ADJ"}, "adv": {"ADV"}, "pron": {"PRON"}, "prep": {"ADP"}, "conj": {"CCONJ", "SCONJ"}}
ALLOW = {("so", "conj")}
NAME = {"n": "noun", "v": "verb", "adj": "adjective", "adv": "adverb", "pron": "pronoun", "prep": "preposition", "conj": "conjunction"}
D = json.loads(open(os.path.join(ROOT, "word-sort.html"), encoding="utf-8").read().split("/*DATA*/")[1].split("/*END*/")[0])

def parse(s):
    """'{word|tag}' sentence -> (plain, [(word, tag, start)])"""
    out, plain = [], ""
    for m in re.finditer(r"\{([^|}]+)\|([^}]+)\}|([^{]+)", s):
        if m.group(1): out.append((m.group(1), m.group(2), len(plain))); plain += m.group(1)
        else: plain += m.group(3)
    return plain, out
def check(plain, word, cls, start=None):
    """spaCy agrees that `word` (at `start`, or its only occurrence) is a `cls`"""
    toks = [t for t in nlp(plain) if t.text == word and (start is None or t.idx == start)]
    assert toks, (plain, word)
    assert all(t.pos_ in UP[cls] or (word.lower(), cls) in ALLOW for t in toks), (plain, word, cls, [t.pos_ for t in toks])
    return True
SENT = [parse(s) for s in D["sent"]]
def find(word):   # the data sentence containing this tagged word
    for p, ws in SENT:
        for w, t, st in ws:
            if w == word: return p, t, st
    raise KeyError(word)
def u(plain, start, word): return plain[:start] + f"<u><b>{word}</b></u>" + plain[start + len(word):]

# ---------- free sheet ----------
FASTI = None
A_words = ["fox", "slept", "creaky", "slowly", "kindness", "shone", "nervously", "huge", "Galway", "patiently", "silent", "wildly"]
A = []
for w in A_words:
    p, t, st = find(w); check(p, w, t, st); A.append((u(p, st, w), NAME[t]))
B_bank = ["robin", "sang", "sweetly", "little", "storm", "flooded", "sudden", "happily", "seagulls", "stole", "hungry", "suddenly"]
B = {}
for w in B_bank:
    p, t, st = find(w); check(p, w, t, st); B.setdefault(t, []).append(w)
assert sorted(B) == ["adj", "adv", "n", "v"] and all(len(v) == 3 for v in B.values()), B
C_words = [("everyone", "pron"), ("across", "prep"), ("because", "conj"), ("them", "pron"), ("behind", "prep"), ("although", "conj")]
C = []
for w, cls in C_words:
    p, t, st = find(w); assert t == cls; check(p, w, t, st); C.append((u(p, st, w), NAME[t]))
PICK = [("run", "v"), ("run", "n"), ("light", "adj"), ("fast", "adj"), ("fast", "adv"), ("hard", "adv")]
Dsw = [x for x in D["switch"] if (x[2], x[1]) in PICK]; assert len(Dsw) == 6
Dq = []
for s, cls, w, why in Dsw:
    p = s.replace("{", "").replace("}", ""); st = s.index("{"); w = p[st:st + len(w)]; check(p, w, cls, st); Dq.append((u(p, st, w), NAME[cls]))
E = [x for x in D["strong"] if x[1] in ("bolted", "devoured", "enormous", "exhausted", "stormed", "deafening")]
assert len(E) == 6
Eq = [(re.sub(r"\{([^}]+)\}", r"<u><b>\1</b></u>", s), a) for s, a, wr, why in E]
F = [("He played <u><b>good</b></u> in the match.", "well"), ("The bus came <u><b>quick</b></u>.", "quickly"),
     ("Please drive <u><b>careful</b></u>.", "carefully"), ("They spoke <u><b>polite</b></u> to the visitor.", "politely"),
     ("I did <u><b>bad</b></u> in the quiz.", "badly")]
for s, a in F:
    p = re.sub(r"<[^>]+>", "", s); w = re.search(r"<b>(\w+)</b>", s).group(1); fixed = p.replace(f" {w}", f" {a}", 1)
    check(fixed, a, "adv")
PASS = "The wind howled around the cottage. Inside, Nora crouched by the dying fire and listened. Something scratched slowly at the door."
for w, cls in [("howled", "v"), ("crouched", "v"), ("scratched", "v"), ("slowly", "adv")]: check(PASS, w, cls)
FASTI = next(i for i, (q, a) in enumerate(Dq) if "drives" in q)
NQ = len(A) + len(B_bank) + len(C) + len(Dq) + len(Eq) + len(F) + 2; assert NQ == 49, NQ

def qs(items): return "".join(f"<li>{q} <span class='line'></span></li>" for q in items)
def style(var):
    return re.search(var + r' = f"""<!doctype.*?<style>(.*?)</style>', open(os.path.join(SRC, "build_money1_pdfs.py"), encoding="utf-8").read(), re.S).group(1).replace("{LO}", LO).replace("{{", "{").replace("}}", "}").replace("JC Maths LOs (2018 spec)", "JC English LOs (2015 spec)")
SHEET_STYLE = style("sheet"); PACK_STYLE = style("pack")
assert "JC English LOs (2015 spec)" in SHEET_STYLE and "Single-teacher licence" in PACK_STYLE and "JC English LOs (2015 spec)" in PACK_STYLE
EXTRA = """.wk{line-height:1.45;border:1.5px solid var(--line);border-radius:8px;padding:2px 7px;margin:3px 0;font-size:9.4pt}.wk b.h{display:block}
table.st{border-collapse:collapse;margin:3px 0;font-size:9.4pt;width:100%}table.st td,table.st th{border:1px solid #C9D1DA;padding:2px 6px;text-align:left}
.bank{border:1.5px solid var(--line);border-radius:8px;padding:4px 10px;margin:4px 0;text-align:center;font-weight:700;word-spacing:9px}
table.sort{border-collapse:collapse;width:100%;margin:4px 0}table.sort th,table.sort td{border:1px solid #C9D1DA;padding:3px 6px;width:25%;text-align:center}table.sort td{height:9mm}
.pass{border-left:4px solid var(--green);background:var(--mist);padding:5px 10px;margin:4px 0;font-style:italic}"""

sheet = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Parts of speech: rules and practice | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{SHEET_STYLE}
{EXTRA}
</style></head><body>
<div class="page tight">
  <div class="band"><div><div class="k">Junior Cycle English · Free revision sheet</div><h1>Parts of speech</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2015 specification): {LO}. Play the game: <b>{GAME}</b></p>
  <div class="two">
   <div><h2>1. Every word has a job</h2>
    <p>The job a word does in a sentence is its <b>word class</b> (or part of speech). Knowing the jobs helps you write accurately and talk about a writer's language.</p>
    <h2>2. The big four</h2>
    <table class="st"><tbody>
     <tr><td><b>Noun</b></td><td>a person, place, thing or idea: Maya, Cork, ball, courage</td></tr>
     <tr><td><b>Verb</b></td><td>an action or a state: kicked, slept, is, seems</td></tr>
     <tr><td><b>Adjective</b></td><td>describes a noun: the <i>muddy</i> ball, it was <i>empty</i></td></tr>
     <tr><td><b>Adverb</b></td><td>how, when, where, how often: ran <i>quickly</i>, <i>never</i> came</td></tr></tbody></table>
    <h2>3. The glue words</h2>
    <table class="st"><tbody>
     <tr><td><b>Pronoun</b></td><td>stands in for a noun: I, you, she, it, we, them</td></tr>
     <tr><td><b>Preposition</b></td><td>where or when: <i>under</i> the oak, <i>after</i> dinner</td></tr>
     <tr><td><b>Conjunction</b></td><td>joins ideas: and, but, so, because, although</td></tr></tbody></table>
    <h2>4. Quick tests</h2>
    <div class="wk">the ___ ? → <b>noun</b> (the fox) &nbsp;·&nbsp; they ___ ? → <b>verb</b> (they slept)<br>Describes a noun? → <b>adjective</b> &nbsp;·&nbsp; Tells you how / when? → <b>adverb</b> (many end in -ly)</div></div>
   <div><h2>5. Same word, different job</h2>
    <p>The class depends on the job <b>in that sentence</b>.</p>
    <div class="wk">I <b>run</b> every day (verb) · a long <b>run</b> (noun)<br>a <b>fast</b> car (adjective) · she drives <b>fast</b> (adverb)<br>turn on the <b>light</b> (noun) · a <b>light</b> bag (adjective)</div>
    <h2>6. Stronger words</h2>
    <p>One strong verb beats a weak verb + adverb. Swap tired words for exact ones.</p>
    <div class="wk">ran very fast → <b>sprinted</b> &nbsp;·&nbsp; ate hungrily → <b>devoured</b><br>very tired → <b>exhausted</b> &nbsp;·&nbsp; nice food → <b>delicious</b> food<br>went across the road → <b>bolted</b> across the road</div>
    <h2>7. Adjective or adverb?</h2>
    <p>Telling us <b>how</b> something was done? Use the adverb.</p>
    <div class="wk">He played <s>good</s> <b>well</b>. &nbsp;She sang <s>beautiful</s> <b>beautifully</b>.</div>
    <div class="note"><b>Classic mistakes:</b> "quick" for quickly · "good" for well · very + a weak word (very big) instead of one strong word (enormous) · calling every -ly word an adverb (friendly, lonely are adjectives).</div></div>
  </div>
  <div class="tip"><b>Exam tip:</b> when you write about a writer's language, quote the exact word and name it: "The verb 'howled' makes the wind sound like an animal."</div>
</div>

<div class="page p2">
  <div class="band"><div><div class="k">Practice · {NQ} questions</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Name the word class of the underlined word</h2><ol class="q" style="columns:2;column-gap:8mm">{qs(q for q, a in A)}</ol>
  <h2>B. Sort the words into the table (questions 13–24)</h2>
  <div class="bank">{" &nbsp; ".join(sorted(B_bank, key=str.lower))}</div>
  <table class="sort"><thead><tr><th>Noun</th><th>Verb</th><th>Adjective</th><th>Adverb</th></tr></thead><tbody><tr><td></td><td></td><td></td><td></td></tr></tbody></table>
  <h2>C. Pronoun, preposition or conjunction?</h2><ol class="q" start="25" style="columns:2;column-gap:8mm">{qs(q for q, a in C)}</ol>
  <h2>D. Same word, different job: name the class</h2><ol class="q" start="31" style="columns:2;column-gap:8mm">{qs(q for q, a in Dq)}</ol>
  <h2>E. Write one stronger word for the underlined words</h2><ol class="q" start="{31 + len(Dq)}" style="columns:2;column-gap:8mm">{qs(q for q, a in Eq)}</ol>
  <h2>F. Fix the mistake (adjective or adverb?)</h2><ol class="q" start="{31 + len(Dq) + len(Eq)}" style="columns:2;column-gap:8mm">{qs(s for s, a in F)}</ol>
  <h2>G. Exam-style</h2>
  <div class="pass">{PASS}</div>
  <ol class="q" start="{NQ - 1}">
   <li>Pick out two verbs that make this scene tense. Explain each choice.<span class="long"></span><span class="long"></span></li>
   <li>Rewrite with stronger words: "The girl went into the big room and looked at the nice painting."<span class="long"></span></li>
  </ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">Check your work</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <table class="ans"><tbody>
   <tr><td><b>A</b></td><td>{" · ".join(f"{i}. {a}" for i, (q, a) in enumerate(A, 1))}</td></tr>
   <tr><td><b>B</b></td><td>Nouns: {", ".join(B["n"])} · Verbs: {", ".join(B["v"])} · Adjectives: {", ".join(B["adj"])} · Adverbs: {", ".join(B["adv"])}</td></tr>
   <tr><td><b>C</b></td><td>{" · ".join(f"{i}. {a}" for i, (q, a) in enumerate(C, 25))}</td></tr>
   <tr><td><b>D</b></td><td>{" · ".join(f"{i}. {a}" for i, (q, a) in enumerate(Dq, 31))}</td></tr>
   <tr><td><b>E</b></td><td>Any strong, exact word that fits, e.g. {" · ".join(f"{i}. {a}" for i, (q, a) in enumerate(Eq, 31 + len(Dq)))}</td></tr>
   <tr><td><b>F</b></td><td>{" · ".join(f"{i}. {a}" for i, (s, a) in enumerate(F, 31 + len(Dq) + len(Eq)))} (each tells us <i>how</i>, so it must be an adverb)</td></tr>
   <tr><td><b>G</b></td><td>{NQ - 1}. Any two of: "howled" (the wind sounds like a wild animal), "crouched" (Nora is hiding, afraid), "scratched" (something is trying to get in). Quote the word + say what it makes you see, hear or feel.<br>{NQ}. e.g. The girl <b>crept</b> into the <b>vast</b> room and <b>gazed</b> at the <b>stunning</b> painting.</td></tr>
  </tbody></table>
  <h2>Worked examples</h2>
  <div class="two">
   <div class="wk"><b class="h">2. slept</b>"The fox slept": try "they slept". It works, and it's something the fox does, so it's a <b>verb</b>.</div>
   <div class="wk"><b class="h">11. silent</b>"Fear kept them silent": silent describes <i>them</i> (a pronoun standing in for people), so it's an <b>adjective</b>, even though it's at the end.</div>
   <div class="wk"><b class="h">{31 + FASTI}. fast</b>"She drives fast": fast tells us <i>how</i> she drives, so here it's an <b>adverb</b>. In "a fast car" it's an adjective.</div>
   <div class="wk"><b class="h">28. them</b>"Fear kept them silent": them stands in for the people, so it's a <b>pronoun</b>.</div>
  </div>
  <div class="note"><b>Got one wrong?</b> Ask: what job is the word doing in <i>this</i> sentence? Then play <b>Word Sort</b> at {GAME}: the "Go back over these" list at the end shows the reason for each mistake.</div>
  <p class="small">All sentences written by Léim. Léim is independent and not connected with the State Examinations Commission or the NCCA.</p>
</div>
</body></html>"""
assert A[10][1] == "adjective" and "silent" in A[10][0] and Dq[FASTI][1] == "adverb" and C[3][1] == "pronoun" and "them" in C[3][0], (A[10], Dq[FASTI], C[3])

# ---------- teacher pack ----------
MATCH = [("ran very fast", "sprinted"), ("ate hungrily", "devoured"), ("very tired", "exhausted"), ("very big", "enormous"),
         ("very cold", "freezing"), ("looked hard at", "stared at"), ("very loud", "deafening"), ("walked angrily", "stormed"),
         ("very happy", "overjoyed"), ("very dirty", "filthy"), ("cried loudly", "wailed"), ("said quietly", "whispered")]
assert len({a for q, a in MATCH}) == 12 and len({q for q, a in MATCH}) == 12
random.seed(101); order = list(range(24)); random.shuffle(order)
cards = [("q", i) for i in range(12)] + [("a", i) for i in range(12)]
match_print = [cards[k] for k in order]
match_html = "".join(f'<div class="c"><span class="tag">Card {k}</span><div class="fc">{MATCH[i][1] if t == "a" else MATCH[i][0]}</div></div>' for k, (t, i) in enumerate(match_print, 1))
match_key = " · ".join(f"{match_print.index(('q', i)) + 1} → {match_print.index(('a', i)) + 1}" for i in range(12))

# Story Swap: each student has a story with labelled gaps and asks the partner for words.
STORY_A = ("The Beach Day", [("adjective", "On a {} morning, Dad packed the car."), ("noun (a thing)", "We forgot the {}, of course."),
           ("verb (past)", "My little brother {} into the sea."), ("adverb (-ly)", "A seagull watched us {}."),
           ("adjective", "Then it stole Mam's {} sandwich."), ("noun (a person)", "Even the {} laughed.")])
STORY_B = ("The School Tour", [("adjective", "Our {} bus left at eight."), ("verb (past)", "Ms Byrne {} at the front."),
           ("noun (a place)", "We stopped at a {} for lunch."), ("adverb (-ly)", "Liam ate his chips {}."),
           ("adjective", "The museum was full of {} statues."), ("noun (an animal)", "On the way home, a {} sat beside me.")])
def story_card(who, title, lines):
    asks = "".join(f"<tr><td>{i}. {k}</td><td></td></tr>" for i, (k, s) in enumerate(lines, 1))
    txt = " ".join(s.format(f"<b>({i})</b> ________") for i, (k, s) in enumerate(lines, 1))
    return f'<div class="idc"><h3>Student {who} · Story Swap: "{title}"</h3><div class="two"><table class="ss"><thead><tr><th>Ask your partner for …</th><th>Their word</th></tr></thead><tbody>{asks}</tbody></table><p style="font-size:8.6pt;margin:0;line-height:1.5">{txt}</p></div></div>'

# Word Class Dominoes: 20 "find the …" clues from the game's sentences, 20 different answers, each class unique in its sentence (spaCy-checked).
DOMS = []
want = [("adverb", "soundly"), ("noun", "door"), ("pronoun", "us"), ("adjective", "huge"), ("verb", "cycled"), ("conjunction", "although"),
        ("preposition", "through"), ("adverb", "shyly"), ("noun", "kindness"), ("adjective", "nervous"), ("verb", "chewed"), ("preposition", "towards"),
        ("adjective", "wise"), ("conjunction", "when"), ("verb", "mended"), ("noun", "Freedom"), ("adverb", "wildly"), ("preposition", "beside"),
        ("pronoun", "me"), ("adjective", "tiny")]
INV = {v: k for k, v in NAME.items()}
for cls, w in want:
    p, t, st = find(w); w0 = w
    assert NAME[t] == cls, (w, t); check(p, w0, t, st)
    hits = [x for x in nlp(p) if x.pos_ in UP[t] or (x.text.lower(), t) in ALLOW]   # the ONLY word of that class (tagger), so the clue has one answer
    assert len(hits) == 1, ("class not unique in sentence", p, cls, [x.text for x in hits])
    DOMS.append((f"The {cls} in: {p}", w0))
assert len(DOMS) == 20 and len({a.lower() for c, a in DOMS}) == 20 and len({c.split(": ")[1] for c, a in DOMS}) == 20
random.seed(1001); chain = DOMS[:]; random.shuffle(chain)
dom = [("START" if k == 0 else chain[k - 1][1], x[0]) for k, x in enumerate(chain)] + [(chain[-1][1], "FINISH")]
dom_print = dom[:]; random.shuffle(dom_print)
dom_html = "".join(f'<div class="dom"><div class="h l{" sm" if len(l) > 8 else ""}">{l}</div><div class="h r">{r}</div></div>' for l, r in dom_print)
chain_key = "".join(f"<li>{c.split(':')[0][4:]}: <b>{a}</b></li>" for c, a in chain)

ERR = [("The cake was <b>real</b> tasty.", "real", "Describes <i>tasty</i> (how tasty), so an adverb: <b>really</b> tasty"),
       ("She finished the race <b>quick</b>.", "quick", "Tells us how she finished: <b>quickly</b>"),
       ("<b>Me and Tom</b> went to the match.", "Me and Tom", "Subject pronoun needed: <b>Tom and I</b> went"),
       ("The dog wagged <b>it's</b> tail.", "it's", "it's = it is. The possessive is <b>its</b> tail"),
       ("He was <b>very very</b> scared.", "very very", "Use one strong adjective: <b>terrified</b>"),
       ("I <b>seen</b> the film last night.", "seen", "Past tense verb: I <b>saw</b> the film (or I have seen)")]
for fixed, w, cls in [("The cake was really tasty.", "really", "adv"), ("She finished the race quickly.", "quickly", "adv"),
                      ("Tom and I went to the match.", "I", "pron"), ("I saw the film last night.", "saw", "v")]:
    check(fixed, w, cls)
WS_PASS = "The old lighthouse stood alone on the cliff. Waves smashed against its walls, and the rusty door groaned whenever the wind blew."
for w, cls in [("old", "adj"), ("lighthouse", "n"), ("stood", "v"), ("smashed", "v"), ("against", "prep"), ("rusty", "adj"), ("groaned", "v"), ("whenever", "conj")]:
    check(WS_PASS, w, cls)

pack = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Parts of Speech Teacher Pack | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{PACK_STYLE}
{EXTRA}
.fym .c{{height:13.6mm}}.fym .fc{{font-size:13pt}}.idc{{padding:1.5mm 4mm}}.idc h3{{margin:0 0 1mm}}.ss td,.ss th{{font-size:8.6pt}}.ss td:nth-child(2){{width:42%}}
.dom .r{{font-size:8.6pt;line-height:1.25}}.dom .l{{font-size:13pt}}.dom .l.sm{{font-size:11pt}}.p1 .proc td{{font-size:8.6pt;padding:2px 6px}}
.ops div{{font-size:12pt;padding:4mm 3mm}}.ops b{{font-size:18pt}}.pass{{font-size:10pt}}
</style></head><body>

<div class="page p1">
  <div class="band"><div><div class="k">Junior Cycle English · Teacher pack</div><h1>Parts of speech</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2015 specification): {LO}</p>
  <div class="two">
    <div><h3>Aims</h3><p>By the end of the lesson students can name the word class of a word from its job in the sentence (noun, verb, adjective, adverb, pronoun, preposition, conjunction), see that one word can change class, swap weak words for strong ones, and fix adjective/adverb slips in their own writing.</p></div>
    <div><h3>In this pack</h3><p>p.1 Teacher notes · p.2 Upgrade Match mingle cards + Story Swap A/B cards · p.3 Word Class Dominoes (cut-up) · p.4 Wall poster · p.5 Worksheet: Error Hunt + exam-style questions · p.6 Answers. Level: 1st year (useful revision in 2nd and 3rd). Time: about 60 minutes. All sentences are original.</p></div>
  </div>
  <h2 style="margin-top:8px">Procedure</h2>
  <table class="proc"><tbody>
    <tr><td>5 min</td><td><b>Lead-in: the jobs game.</b> Write "The tired fox slept soundly under the old oak." Ask: which words could you take out and still have a sentence? Which ones can't go? Elicit that words do different jobs.</td></tr>
    <tr><td>8 min</td><td><b>Guided discovery.</b> Pairs try the tests on each word: "the ___" (noun), "they ___" (verb), "very ___" (adjective or adverb). Then: does it describe a thing, or tell you how? Board the big four, then the glue words (pronoun, preposition, conjunction).</td></tr>
    <tr><td>10 min</td><td><b>Upgrade Match mingle</b> (p.2, 24 cards = 12 weak phrases + 12 strong words; one card each). Find your partner, then say a sentence using the strong word. Feedback: which pairs were verbs, which adjectives?</td></tr>
    <tr><td>12 min</td><td><b>Story Swap</b> (p.2, pairs, don't show your story). A asks B for each word in the list ("Give me an adjective"), writes it in, then reads the silly story aloud. Swap. Then pairs rewrite one story with the <i>best</i> words they can think of.</td></tr>
    <tr><td>10 min</td><td><b>Word Class Dominoes</b> (p.3), groups of 3–4. Start with START, find the word the clue asks for, then find the domino with that word on its left. Build the chain to FINISH.</td></tr>
    <tr><td>12 min</td><td><b>Worksheet</b> (p.5). Error Hunt in pairs (find it, say what's wrong, fix it), then the exam-style questions alone.</td></tr>
    <tr><td>3 min</td><td><b>Exit ticket.</b> "Fear kept them silent." Name each word's class. (noun, verb, pronoun, adjective.) Homework: play <b>Word Sort</b> at {GAME}.</td></tr>
  </tbody></table>
  <div class="note"><b>Mingle key</b> (weak card → strong card): {match_key}.<br>
  <b>Errors to look for:</b> "quick" for quickly, "good" for well · every -ly word called an adverb (friendly, lovely are adjectives) · a word's class decided out of context (run, fast, light) · "Me and Tom went". <b>Support:</b> the poster (p.4) on the desk. <b>Fast finishers:</b> write one sentence where "light" is a noun, a verb and an adjective.</div>
  <p class="small"><b>Domino answer chain</b> (START → FINISH):</p>
  <ol class="small" style="columns:2;column-gap:12px;font-size:7.4pt;line-height:1.22;margin:0;padding-left:16px">{chain_key}</ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">Cut up the cards · one Story Swap card per student</div><h1>Upgrade Match + Story Swap</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:8.8pt;margin:0"><b>Upgrade Match mingle.</b> Cut out the 24 cards and give one to each student. Weak words? Find the one strong word that means the same. Strong word? Find the weak words it replaces. (Fewer students? Take out whole pairs.)</p>
  <div class="fym">{match_html}</div>
  <p style="font-size:8.8pt;margin:3mm 0 0"><b>Story Swap.</b> Don't show your story. Ask your partner for each word in your list and write it in. Then read the story aloud, with their words in the gaps.</p>
  {story_card("A", *STORY_A)}
  {story_card("B", *STORY_B)}
</div>

<div class="page">
  <div class="band"><div><div class="k">Groups of 3–4 · cut along the dashed lines</div><h1>Word Class Dominoes</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.4pt">Start with START. Find the word the clue on the right asks for, then find the domino with that word on its left. Keep going until you reach FINISH.</p>
  <div class="doms">{dom_html}</div>
</div>

<div class="page">
  <div class="poster">
    <h1>Every word has a job</h1>
    <div class="ops">
      <div style="background:var(--green-soft)"><b>Noun</b>person, place, thing, idea<br>the ___ ?<br><i>fox, Cork, courage</i></div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Verb</b>action or state<br>they ___ ?<br><i>slept, kicked, is</i></div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Adjective</b>describes a noun<br><i>the muddy ball</i></div>
      <div style="background:var(--green-soft)"><b>Adverb</b>how, when, where<br><i>ran quickly, never came</i></div>
      <div style="background:var(--green-soft)"><b>Pronoun</b>stands in for a noun<br><i>I, she, it, them</i></div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Preposition + conjunction</b>where/when · joins ideas<br><i>under, after · and, because</i></div>
    </div>
    <p style="text-align:center;font-size:20pt!important;font-weight:800;margin:4mm 0">ran very fast → sprinted</p>
    <p style="text-align:center;font-size:10pt;color:var(--muted)">Léim · leim.ie · Play Word Sort: {GAME}</p>
  </div>
</div>

<div class="page ws">
  <div class="band"><div><div class="k">Worksheet</div><h1>Error Hunt + exam-style questions</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Error Hunt</h2>
  <p>Each sentence has one mistake in bold. Say what's wrong and write it correctly.</p>
  <table class="eh"><thead><tr><th>Sentence</th><th>What's wrong and the fix</th></tr></thead><tbody>
  {"".join(f"<tr><td>{s}</td><td><span class='gap'></span><span class='gap'></span></td></tr>" for s, w, r in ERR)}
  </tbody></table>
  <h2>B. Exam-style questions</h2>
  <div class="pass">{WS_PASS}</div>
  <ol class="q">
    <li>Find one example of each: noun, verb, adjective, preposition, conjunction.<span class="long"></span></li>
    <li>Pick out two verbs that make the lighthouse seem lonely or threatened. Explain each choice.<span class="long"></span><span class="long"></span></li>
    <li>Rewrite with stronger words: "The boat went slowly into the harbour on a very cold night."<span class="long"></span></li>
    <li>Write one sentence where "light" is a noun and another where it is an adjective.<span class="long"></span></li>
    <li>"The lonely girl walked home." Is "lonely" an adverb? Explain.<span class="long"></span></li>
  </ol>
</div>

<div class="page an">
  <div class="band"><div><div class="k">For the teacher</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>Upgrade Match</h2>
  <p>{" · ".join(f"{q} → <b>{a}</b>" for q, a in MATCH)}</p>
  <h2>Story Swap</h2>
  <p>Any word of the right class is correct; check each one fits its label (e.g. an adverb answers "how"). In the rewrite, look for exact, strong verbs and adjectives.</p>
  <h2>A. Error Hunt</h2>
  <table><tbody>{"".join(f"<tr><td style='width:40%'>{s}</td><td>{r}</td></tr>" for s, w, r in ERR)}</tbody></table>
  <h2>B. Exam-style questions</h2>
  <ol class="q">
    <li>e.g. noun: <b>lighthouse</b> · verb: <b>stood</b> · adjective: <b>old</b> or <b>rusty</b> · preposition: <b>on</b> or <b>against</b> · conjunction: <b>and</b> or <b>whenever</b>.</li>
    <li>e.g. <b>"smashed"</b>: the waves attack the walls with force. <b>"groaned"</b>: the door sounds old and in pain, adding to the eerie mood. (Credit: exact word quoted + what it shows.)</li>
    <li>e.g. The boat <b>crept</b> into the harbour on a <b>freezing</b> night.</li>
    <li>e.g. Turn on the <b>light</b> (noun). My bag is <b>light</b> (adjective).</li>
    <li>No. "Lonely" describes the girl (a noun), so it is an <b>adjective</b>, even though it ends in -ly.</li>
  </ol>
  <h2>Marking tip</h2>
  <p>In questions on a writer's language, credit the exact word quoted plus a clear point about its effect; naming the word class makes the point sharper. In students' own writing, adjective/adverb slips and weak, repeated words cost marks for accuracy and style.</p>
</div>
</body></html>"""

cover = """<!doctype html><html><head><meta charset="utf-8"><style>
body{margin:0;width:1200px;height:1200px;background:#1B2430;font-family:Inter,sans-serif;color:#fff;display:flex;flex-direction:column;justify-content:space-between;padding:90px;box-sizing:border-box}
.k{display:inline-block;background:#2E7D57;border-radius:99px;padding:12px 26px;font-weight:700;font-size:28px;letter-spacing:.06em;text-transform:uppercase}
h1{font-size:130px;font-weight:800;line-height:1.15;letter-spacing:-.02em;margin:60px 0 20px}
h1 span{background:#F6CF5A;color:#1B2430;padding:0 18px;border-radius:14px}
.sub{font-size:40px;line-height:1.4;color:#DDE3EA}
.em{font-size:52px;margin-top:30px;font-weight:800;letter-spacing:.01em;color:#F6CF5A}
.foot{display:flex;justify-content:space-between;align-items:center;font-size:34px;font-weight:700}
.price{background:#F6CF5A;color:#1B2430;border-radius:16px;padding:14px 28px}
</style></head><body>
<div><span class="k">Junior Cycle English · Teacher pack</span>
<h1><span>Parts of</span><br><span>speech</span></h1>
<div class="sub">Upgrade Match mingle · Story Swap A/B<br>Dominoes · Poster · Worksheet + answers</div>
<div class="em">noun · verb · adjective · adverb</div></div>
<div class="foot"><span>↗ Léim · leim.ie</span><span class="price">Ready to teach · 60 min</span></div>
</body></html>"""

if __name__ == "__main__":
    for name, txt in [("rules-and-practice", sheet), ("teacher-pack", pack), ("cover", cover)]:
        open(os.path.join(SRC, f"{SLUG}-{name}.html"), "w", encoding="utf-8").write(txt)
    def pdf(name, out):
        subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--no-pdf-header-footer", f"--print-to-pdf={out}",
                        f"{SLUG}-{name}.html"], cwd=SRC, check=True, capture_output=True)
        print(name, subprocess.run(["pdfinfo", out], capture_output=True, text=True).stdout.split("Pages:")[1].split()[0], "pages")
    pdf("rules-and-practice", os.path.join(ROOT, "printables", f"{SLUG}-rules-and-practice.pdf"))
    pdf("teacher-pack", os.path.join(OUT, "Parts-of-Speech-Teacher-Pack-Leim.pdf"))
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--hide-scrollbars", "--window-size=1200,1200",
                    f"--screenshot={os.path.join(OUT, f'{SLUG}-cover.png')}", f"{SLUG}-cover.html"], cwd=SRC, check=True, capture_output=True)
    print("domino chain:", [a for c, a in chain])
