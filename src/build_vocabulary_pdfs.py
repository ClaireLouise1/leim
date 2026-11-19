#!/usr/bin/env python3
"""Vocabulary & dictionary skills (JC English topic 13, game Word Ladder): free sheet + teacher pack + Payhip cover.
Run from the repo root: python3 src/build_vocabulary_pdfs.py OUTDIR
Writes src/vocabulary-dictionary-skills-*.html; PDFs/cover PNG go to OUTDIR (free sheet also to printables/).
Items come from the game's own data block (word-ladder.html); every answer is re-checked with the functions in
src/test_word_ladder.py (WordNet synonyms / antonyms / word classes, spaCy for the gap's word class).
Needs WordNet: NLTK_ALLOW_PROXIED_URLOPEN=1 python3 -c "import nltk; nltk.download('wordnet')".
Styles are read from src/build_money1_pdfs.py."""
import os, sys, random, subprocess, re
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC)
sys.path.insert(0, SRC)
import test_word_ladder as T
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/vo"; os.makedirs(OUT, exist_ok=True)
SLUG = "vocabulary-dictionary-skills"
LO = "R10, OL13, W5"
GAME = "leim.ie/word-ladder.html"
D = T.load(os.path.join(ROOT, "word-ladder.html"))
assert not T.data_pass(D), T.data_pass(D)
LAD = {L[1][1]: L for L in D["ladder"]}
SYN = {w: (s, a) for w, s, a in D["syn"]}
PRE = {r: item for item in D["pre"] for r in [item[1]]}
FAM = {a: (s, wr, c) for s, a, wr, c in D["fam"]}

# ---------- free sheet ----------
random.seed(13)
A_L = ["tired", "angry", "huge", "rain", "jog", "town"]
A = []
for m in A_L:
    w = LAD[m][1]; sh = w[:]
    while sh == w: random.shuffle(sh)
    A.append((" · ".join(sh), " → ".join(w)))
B_L = ["hungry", "funny", "wet", "dirty", "scared", "beautiful"]
B = []
for m in B_L:
    L = LAD[m]; assert L[2] and T.linked(m, L[1][2])
    B.append((L[2].replace("very " + m, "<u>very " + m + "</u>"), L[1][2]))
B_BOX = sorted([a for q, a in B] + ["microscopic", "deafening"])
for x in ["microscopic", "deafening"]:
    assert all(not T.clash(m, x) for m in B_L)
C_P = [("huge", "enormous"), ("brave", "cowardly"), ("tidy", "neat"), ("permit", "forbid"), ("empty", "vacant"), ("remember", "forget"), ("victory", "defeat"), ("begin", "start")]
C = []
for a, b in C_P:
    s, o = T.synonym(a, b) and not T.antonym(a, b), T.antonym(a, b)
    assert s != o, (a, b); C.append((f"{a} · {b}", "S" if s else "A"))
D_R = ["kind", "honest", "possible", "legal", "regular", "correct", "build", "spell"]
Dd = []
for r in D_R:
    p, root, g = PRE[r][:3]; av = PRE[r][3] if len(PRE[r]) > 3 else []
    assert T.is_word(p + r)
    if g.startswith("not"):
        Dd.append((f"not {r}", p + r))
    else:
        Dd.append((f"{r} → {g}", p + r))
E_A = ["happiness", "carefully", "dangerous", "decide", "strength", "beautiful"]
E = []
for a in E_A:
    s, wr, c = FAM[a]; opts = [a] + wr[:2]; random.shuffle(opts)
    p = T.slot_pos(s.replace("___", a), a); assert p == c and all(p not in T.wn_pos(x) for x in wr)
    E.append((s.replace("___", "(" + " / ".join(opts) + ")"), a))
F_ABC = [["stone", "storm", "story", "stool"], ["clean", "clear", "class", "claim"], ["front", "frost", "frog", "fridge"]]
for ws in F_ABC: assert ws in D["abc"]
F_G = [g for g in D["guide"] if g[0] in ("map", "coat", "wet")]
F_GQ = []
for top, bot, inn, out in F_G:
    opts = [inn] + out[:2]; random.shuffle(opts); F_GQ.append((f"Guide words <b>{top} … {bot}</b>: ({' / '.join(opts)})", inn))
    assert top <= inn <= bot and not any(top <= x <= bot for x in out)
F_M = [m for m in D["mean"] if m[0] in ("I put my money in the {bank}.", "We heard a loud {bark} next door.", "The box was {light} enough to carry.")]
assert len(F_M) == 3
F_MQ = [(m[0].replace("{", "<b>").replace("}", "</b>"), re.sub(r"^\S+ ", "", m[1])) for m in F_M]
PASS_RAW = "Our walk along the cliffs at Kilkee was <u>very hard</u>. The wind was <u>very cold</u> and by the end we were <u>very tired</u>. Then we saw the sunset. It was <u>very beautiful</u>."
PASS_FIX = [("very hard", "gruelling"), ("very cold", "freezing"), ("very tired", "exhausted"), ("very beautiful", "stunning")]
assert [x for x, y in PASS_FIX] == re.findall(r"<u>(.*?)</u>", PASS_RAW)
for x, y in PASS_FIX:
    assert T.linked(x.split()[1], y), (x, y)
NQ = len(A) + len(B) + len(C) + len(Dd) + len(E) + len(F_ABC) + len(F_GQ) + len(F_MQ) + 2; assert NQ == 45, NQ

def qs(items): return "".join(f"<li>{q} <span class='line'></span></li>" for q in items)
def style(var):
    return re.search(var + r' = f"""<!doctype.*?<style>(.*?)</style>', open(os.path.join(SRC, "build_money1_pdfs.py"), encoding="utf-8").read(), re.S).group(1).replace("{LO}", LO).replace("{{", "{").replace("}}", "}").replace("JC Maths LOs (2018 spec)", "JC English LOs (2015 spec)")
SHEET_STYLE = style("sheet"); PACK_STYLE = style("pack")
assert "JC English LOs (2015 spec)" in SHEET_STYLE and "Single-teacher licence" in PACK_STYLE and "JC English LOs (2015 spec)" in PACK_STYLE
EXTRA = """.wk{line-height:1.45;border:1.5px solid var(--line);border-radius:8px;padding:2px 7px;margin:3px 0;font-size:9.4pt}.wk b.h{display:block}
table.st td:first-child{white-space:nowrap}table.st{border-collapse:collapse;margin:3px 0;font-size:9.2pt;width:100%}table.st td,table.st th{border:1px solid #C9D1DA;padding:1.5px 6px;text-align:left;vertical-align:top}
.pass{border-left:4px solid var(--green);background:var(--mist);padding:5px 10px;margin:4px 0;line-height:1.6}
.box{border:1.5px dashed var(--green);border-radius:8px;padding:2px 8px;margin:2px 0 4px;font-weight:700;font-size:9.6pt}"""
sheet = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Vocabulary and dictionary skills: rules and practice | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{SHEET_STYLE}
{EXTRA}
</style></head><body>
<div class="page tight">
  <div class="band"><div><div class="k">Junior Cycle English · Free revision sheet</div><h1>Vocabulary and dictionary skills</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2015 specification): {LO}. Play the game: <b>{GAME}</b></p>
  <div class="two">
   <div><h2>1. Word ladders: shades of meaning</h2>
    <p style="margin:0">Words that mean nearly the same can be weaker or stronger. Weakest at the bottom, strongest at the top:</p>
    <table class="st"><tbody>
     <tr><td><b>heat</b></td><td>warm → hot → sweltering</td></tr>
     <tr><td><b>anger</b></td><td>annoyed → angry → furious</td></tr>
     <tr><td><b>tiredness</b></td><td>sleepy → tired → exhausted</td></tr>
     <tr><td><b>size</b></td><td>big → huge → gigantic</td></tr>
     <tr><td><b>speed</b></td><td>walk → jog → sprint</td></tr>
     <tr><td><b>rain</b></td><td>drizzle → rain → downpour</td></tr></tbody></table>
    <div class="wk"><b class="h">Cut the “very”</b>very hot → <b>sweltering</b> · very hungry → <b>starving</b> · very funny → <b>hilarious</b>. Only use the top word when you mean it.</div>
    <h2>2. Synonyms and antonyms</h2>
    <table class="st"><tbody>
     <tr><td><b>synonym</b></td><td>same meaning: huge = enormous, begin = start</td></tr>
     <tr><td><b>antonym</b></td><td>opposite: huge ↔ tiny, ancient ↔ modern</td></tr>
     <tr><td><b>thesaurus</b></td><td>a list of synonyms. Check a new word in a dictionary before you use it.</td></tr></tbody></table>
    <h2>3. Dictionary skills</h2>
    <div class="wk"><b class="h">ABC order</b>Same first letter? Look at the 2nd letter, then the 3rd: br<b>a</b>nd, br<b>a</b>ve, br<b>e</b>ad.</div>
    <div class="wk"><b class="h">Guide words</b>The first and last word on the page. <i>fish … flag</i>: five is on the page, fly is not.</div>
    <div class="wk"><b class="h">More than one meaning</b>bat, bank, match, light: read the whole sentence to choose.</div>
    <div class="wk"><b class="h">An entry gives you</b>the meaning, how to say it, the word class (n, v, adj, adv) and an example.</div></div>
   <div><h2>4. Prefixes: at the start</h2>
    <table class="st"><tbody>
     <tr><td><b>un-, dis-, in-</b></td><td>not: unhappy, dishonest, incorrect</td></tr>
     <tr><td><b>im-</b></td><td>not, before p or m: impossible, immature</td></tr>
     <tr><td><b>il-</b></td><td>not, before l: illegal, illogical</td></tr>
     <tr><td><b>ir-</b></td><td>not, before r: irregular, irrelevant</td></tr>
     <tr><td><b>re-</b></td><td>again: rebuild, rewrite</td></tr>
     <tr><td><b>mis-</b></td><td>wrongly, badly: misspell, misbehave</td></tr>
     <tr><td><b>pre-</b></td><td>before: preheat, preschool</td></tr></tbody></table>
    <div class="note">Keep the whole prefix AND the whole word: il + legal = i<b>ll</b>egal, mis + spell = mi<b>ss</b>pell.</div>
    <h2>5. Suffixes and word families</h2>
    <table class="st"><tbody>
     <tr><td><b>noun</b></td><td>-ness, -ment, -tion, -th: happiness, decision, strength</td></tr>
     <tr><td><b>adjective</b></td><td>-ful, -ous, -ive, -able: careful, dangerous, creative</td></tr>
     <tr><td><b>adverb</b></td><td>-ly: carefully, happily (how?)</td></tr>
     <tr><td><b>verb</b></td><td>-en, -ify: strengthen, simplify</td></tr></tbody></table>
    <table class="st"><thead><tr><th>Noun</th><th>Verb</th><th>Adjective</th><th>Adverb</th></tr></thead><tbody>
     <tr><td>happiness</td><td>–</td><td>happy</td><td>happily</td></tr>
     <tr><td>decision</td><td>decide</td><td>decisive</td><td>decisively</td></tr>
     <tr><td>strength</td><td>strengthen</td><td>strong</td><td>strongly</td></tr>
     <tr><td>danger</td><td>endanger</td><td>dangerous</td><td>dangerously</td></tr></tbody></table>
    <div class="wk"><b class="h">Which one fits?</b>After <i>the / her / my</i> → a noun. After <i>is / was / very</i> → an adjective. Says how something is done → an adverb.</div></div>
  </div>
  <div class="tip"><b>Exam tip:</b> asked what a word suggests? Give its meaning AND the feeling it creates. In your own writing, one precise word beats “very” + a weak word, but don't use a fancy word you're not sure of.</div>
</div>

<div class="page p2">
  <div class="band"><div><div class="k">Practice · {NQ} questions</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Put each set on the ladder: bottom → top</h2><ol class="q" style="columns:2;column-gap:8mm">{qs(q for q, a in A)}</ol>
  <h2>B. Swap the underlined words for one stronger word from the box</h2>
  <div class="box">{" · ".join(B_BOX)}</div>
  <ol class="q" start="7" style="columns:2;column-gap:8mm">{qs(q for q, a in B)}</ol>
  <h2>C. Synonyms (S) or antonyms (A)?</h2><ol class="q" start="13" style="columns:4;column-gap:6mm">{qs(q for q, a in C)}</ol>
  <h2>D. Add a prefix to make a word that means …</h2><ol class="q" start="21" style="columns:3;column-gap:6mm">{qs(q for q, a in Dd)}</ol>
  <h2>E. Circle the word from the family that fits</h2><ol class="q" start="29" style="columns:2;column-gap:8mm">{qs(q for q, a in E)}</ol>
  <h2>F. Dictionary skills</h2>
  <ol class="q" start="35" style="columns:2;column-gap:8mm">{qs("Put in ABC order: " + ", ".join(ws) for ws in F_ABC)}{qs("Which word is on the page? " + q for q, a in F_GQ)}{qs("What does the bold word mean? " + q for q, a in F_MQ)}</ol>
  <h2>G. Exam-style</h2>
  <div class="pass">{PASS_RAW}</div>
  <ol class="q" start="{NQ - 1}">
   <li>Replace each underlined phrase with one stronger word.<span class="long"></span></li>
   <li>“The old dog <b>limped</b> across the yard.” What does “limped” suggest? Why is it better than “walked”?<span class="long"></span></li>
  </ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">Check your work</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <table class="ans"><tbody>
   <tr><td><b>A</b></td><td>{" · ".join(f"{i}. {a}" for i, (q, a) in enumerate(A, 1))}</td></tr>
   <tr><td><b>B</b></td><td>{" · ".join(f"{i}. {a}" for i, (q, a) in enumerate(B, 7))}</td></tr>
   <tr><td><b>C</b></td><td>{" · ".join(f"{i}. {a}" for i, (q, a) in enumerate(C, 13))}</td></tr>
   <tr><td><b>D</b></td><td>{" · ".join(f"{i}. {a}" for i, (q, a) in enumerate(Dd, 21))}</td></tr>
   <tr><td><b>E</b></td><td>{" · ".join(f"{i}. {a}" for i, (q, a) in enumerate(E, 29))}</td></tr>
   <tr><td><b>F</b></td><td>{" · ".join(f"{i}. {', '.join(sorted(ws))}" for i, ws in enumerate(F_ABC, 35))} · {" · ".join(f"{i}. {a}" for i, (q, a) in enumerate(F_GQ, 38))} · {" · ".join(f"{i}. {a}" for i, (q, a) in enumerate(F_MQ, 41))}</td></tr>
   <tr><td><b>G</b></td><td>{NQ - 1}. {" · ".join(f"{x} → <b>{y}</b>" for x, y in PASS_FIX)} (other strong words that keep the meaning are fine, e.g. tough, icy, worn out, breathtaking)<br>{NQ}. It suggests the dog is hurt, old or in pain: it walks unevenly, favouring one leg. It's better than “walked” because it shows us how the dog moves and makes us feel sorry for it.</td></tr>
  </tbody></table>
  <h2>Worked examples</h2>
  <div class="two">
   <div class="wk"><b class="h">1. {A[0][1]}</b>Ask “which is the mildest?” first, then “which is the most extreme?”. The one left goes in the middle.</div>
   <div class="wk"><b class="h">24. illegal</b>legal starts with l, so “not” is <b>il-</b>. Keep both l's: il + legal.</div>
   <div class="wk"><b class="h">30. carefully</b>The gap says how they should drive, so it needs an adverb: careful + ly.</div>
   <div class="wk"><b class="h">35. stone, stool, storm, story</b>All start “sto”, so look at the 4th letter: n, o, r, r. Then storm before story (m before y).</div>
  </div>
  <div class="note"><b>Got one wrong?</b> Find the rule on page 1, then play <b>Word Ladder</b> at {GAME}: the “Go back over these” list at the end shows the reason for each mistake.</div>
  <p class="small">All sentences written by Léim. Léim is independent and not connected with the State Examinations Commission or the NCCA.</p>
</div>
</body></html>"""
assert sorted(F_ABC[0]) == ["stone", "stool", "storm", "story"] and Dd[3][1] == "illegal" and E[1][1] == "carefully"

# ---------- teacher pack ----------
# Ladder Sort: 8 ladders x 3 cards = 24 cards
LS_KEYS = ["hot", "cold", "happy", "angry", "tired", "hungry", "quiet", "wind"]
LS = [LAD[k] for k in LS_KEYS]
words = [w for L in LS for w in L[1]]; assert len(set(words)) == 24
random.seed(113); cards = words[:]; random.shuffle(cards)
ls_html = "".join(f'<div class="c"><span class="tag">Card {k}</span><div class="fc">{w}</div></div>' for k, w in enumerate(cards, 1))
ls_key = " · ".join(" → ".join(L[1]) for L in LS)

# Guide Word Swap A/B: each student reads 8 words; the partner says which of their 4 dictionary "pages" it is on
PAGES_A = [("bag", "bend"), ("cave", "clap"), ("pack", "pile"), ("sail", "shop")]
PAGES_B = [("dark", "dove"), ("hall", "hunt"), ("mail", "mile"), ("tap", "tidy")]
WORDS_A = ["dentist", "hockey", "mango", "thunder", "dog", "honey", "medal", "tent"]     # A reads these; B finds them on B's pages
WORDS_B = ["bed", "chip", "pencil", "seal", "basket", "city", "panda", "salt"]           # B reads these; A finds them on A's pages
def page_of(w, pages):
    hit = [k for k, (t, b) in enumerate(pages, 1) if t <= w <= b]
    assert len(hit) == 1, (w, hit); return hit[0]
GA = [(w, page_of(w, PAGES_B)) for w in WORDS_A]; GB = [(w, page_of(w, PAGES_A)) for w in WORDS_B]
for w in WORDS_A + WORDS_B: assert T.is_word(w), w
def gw_card(who, mine, pages):
    lines = "".join(f"<li><b>{w}</b></li>" for w in mine)
    pg = "".join(f"<tr><td>Page {k}</td><td><b>{t}</b> … <b>{b}</b></td><td class='gap'></td></tr>" for k, (t, b) in enumerate(pages, 1))
    return f'''<div class="idc"><h3>Student {who} · Guide Word Swap</h3><div class="two"><div><p style="font-size:8.6pt;margin:0 0 1mm"><b>1. Read your words to your partner,</b> one at a time. They tell you which page it's on. Tick if they're right.</p><ol class="ss" style="font-size:9.4pt;margin:0;padding-left:15px;columns:2">{lines}</ol></div>
<div><p style="font-size:8.6pt;margin:0 0 1mm"><b>2. Your dictionary pages.</b> Listen to each word and write it on the right page. Say “Page …!”</p><table class="gw">{pg}</table></div></div></div>'''

# Prefix & Family Dominoes: 20 clues, 20 different answers, each checked in WordNet
DOM_P = [("not + possible", "impossible"), ("not + legal", "illegal"), ("not + regular", "irregular"), ("not + honest", "dishonest"),
         ("not + happy", "unhappy"), ("not + visible", "invisible"), ("not + polite", "impolite"), ("not + responsible", "irresponsible"),
         ("not + agree", "disagree"), ("again + write", "rewrite"), ("wrongly + spell", "misspell"), ("badly + behave", "misbehave")]
for c, a in DOM_P:
    r = c.split(" + ")[1]; assert PRE[r][0] + r == a and T.is_word(a), (c, a)
DOM_F = [("strong → noun", "strength", "n"), ("happy → noun", "happiness", "n"), ("careful → adverb", "carefully", "r"), ("danger → adjective", "dangerous", "a"),
         ("decision → verb", "decide", "v"), ("wide → noun", "width", "n"), ("beauty → adjective", "beautiful", "a"), ("comfort → adjective", "comfortable", "a")]
for c, a, p in DOM_F:
    assert p in T.wn_pos(a) and (p != "r" or "a" not in T.wn_pos(a)), (c, a)
DOMS = DOM_P + [(c, a) for c, a, p in DOM_F]
assert len(DOMS) == 20 and len({a for c, a in DOMS}) == 20
random.seed(1013); chain = DOMS[:]; random.shuffle(chain)
dom = [("START" if k == 0 else chain[k - 1][1], x[0]) for k, x in enumerate(chain)] + [(chain[-1][1], "FINISH")]
dom_print = dom[:]; random.shuffle(dom_print)
dom_html = "".join(f'<div class="dom"><div class="h l{" sm" if len(l) > 10 else ""}">{l}</div><div class="h r">{r}</div></div>' for l, r in dom_print)
chain_key = "".join(f"<li>{c}: <b>{a}</b></li>" for c, a in chain)

ERR = [("The film was <b>very funny</b>, so we laughed all the way through.", "Weak: use one stronger word → <b>hilarious</b>"),
       ("It is <b>unlegal</b> to drive without a licence.", "Wrong prefix: legal starts with l → <b>illegal</b>"),
       ("She sang <b>happy</b> in the shower.", "It says how she sang, so an adverb → <b>happily</b>"),
       ("The <b>deep</b> of the pool is two metres.", "After “the … of” we need a noun → <b>depth</b>"),
       ("I <b>mispelled</b> my own name!", "mis + spelled: keep both s's → <b>misspelled</b>"),
       ("Thanks for being so <b>helpless</b> with my project.", "Wrong word in the family: helpless = can't help → <b>helpful</b>")]
assert T.is_word("illegal") and not T.is_word("unlegal") and "r" in T.wn_pos("happily") and "n" in T.wn_pos("depth") and "n" not in T.wn_pos("deeply")
assert T.is_word("misspelled") and not T.is_word("mispelled") and "a" in T.wn_pos("helpful")
WS_RAW = "The climb up Croagh Patrick was <u>very hard</u>. Halfway up, the rain turned into a <u>very heavy shower</u> and we were <u>very wet</u>. My little brother was <u>very scared</u> of the loose stones, so Dad held his hand. At the top, the view over Clew Bay was <u>very beautiful</u>, and we were all <u>very happy</u>."
WS_FIX = [("very hard", "gruelling"), ("very heavy shower", "downpour"), ("very wet", "soaked"), ("very scared", "terrified"), ("very beautiful", "stunning"), ("very happy", "overjoyed")]
assert [x for x, y in WS_FIX] == re.findall(r"<u>(.*?)</u>", WS_RAW)
for x, y in WS_FIX[2:]:
    assert y == LAD[x.split()[1]][1][2], (x, y)
assert T.linked("rain", "downpour")
WS_PRE = [("possible", "impossible"), ("patient", "impatient"), ("legal", "illegal"), ("responsible", "irresponsible"), ("lucky", "unlucky")]
for r, a in WS_PRE: assert PRE[r][0] + r == a

pack = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Vocabulary Teacher Pack | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{PACK_STYLE}
{EXTRA}
.fym .c{{height:13.6mm}}.fym .fc{{font-size:14pt;font-weight:800}}.idc{{padding:1.5mm 4mm}}.idc h3{{margin:0 0 1mm}}
table.gw{{border-collapse:collapse;width:100%;font-size:9pt}}table.gw td{{border:1px solid #C9D1DA;padding:2px 5px}}table.gw td.gap{{width:42%}}
ol.ss li{{margin:0}}.dom .r{{font-size:9.6pt;line-height:1.25}}.dom .l{{font-size:12pt}}.dom .l.sm{{font-size:10pt}}.p1 .proc td{{font-size:8.6pt;padding:2px 6px}}
.ops div{{font-size:12pt;padding:4mm 3mm}}.ops b{{font-size:17pt}}.pass{{font-size:10pt}}
</style></head><body>

<div class="page p1">
  <div class="band"><div><div class="k">Junior Cycle English · Teacher pack</div><h1>Vocabulary and dictionary skills</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2015 specification): {LO}</p>
  <div class="two">
    <div><h3>Aims</h3><p>By the end of the lesson students can put near-synonyms in order of strength and replace “very” + a weak word with one precise word, tell synonyms from antonyms, use prefixes (un-, dis-, im-, il-, ir-, re-, mis-) and suffixes to build words, choose the right word from a word family, and use ABC order and guide words to find words fast.</p></div>
    <div><h3>In this pack</h3><p>p.1 Teacher notes · p.2 Ladder Sort cards + Guide Word Swap A/B cards · p.3 Prefix &amp; Family Dominoes (cut-up) · p.4 Wall poster · p.5 Worksheet: Error Hunt + exam-style questions · p.6 Answers. Level: 1st year (useful revision in 2nd and 3rd). Time: about 60 minutes. All sentences are original.</p></div>
  </div>
  <h2 style="margin-top:8px">Procedure</h2>
  <table class="proc"><tbody>
    <tr><td>5 min</td><td><b>Lead-in.</b> Board: “The soup was very hot.” Pairs find one word to replace “very hot”. Collect answers on a ladder drawn on the board: warm → hot → boiling.</td></tr>
    <tr><td>8 min</td><td><b>Guided discovery.</b> Board: impossible, impolite, illegal, illogical, irregular, irresponsible. Pairs: all mean “not”, so why does the prefix change? (look at the first letter of the root). Then: why two l's in illegal?</td></tr>
    <tr><td>10 min</td><td><b>Ladder Sort</b> (p.2, 24 cards = 8 ladders of 3; groups of 3–4). Sort the words into 8 families, then order each from bottom (weakest) to top (strongest). Groups compare: did anyone order a ladder differently? Can they defend it?</td></tr>
    <tr><td>12 min</td><td><b>Guide Word Swap</b> (p.2, pairs, don't show your card). A reads a word; B says which of their four dictionary pages it goes on and writes it there. 8 words each, then swap. Check with the key; any mistakes, say the ABC order out loud.</td></tr>
    <tr><td>10 min</td><td><b>Prefix &amp; Family Dominoes</b> (p.3), groups of 3–4. Start with START, make the word the clue asks for, find the domino with that word on its left. Build the chain to FINISH.</td></tr>
    <tr><td>12 min</td><td><b>Worksheet</b> (p.5). Error Hunt in pairs, then the exam-style questions alone.</td></tr>
    <tr><td>3 min</td><td><b>Exit ticket.</b> Write the opposite: possible, legal, regular. Replace: “very tired”. Homework: play <b>Word Ladder</b> at {GAME}.</td></tr>
  </tbody></table>
  <div class="note"><b>Ladder Sort key</b> (bottom → top): {ls_key}.<br>
  <b>Errors to look for:</b> unlegal / inpossible · ilegal (one l) · mispell (one s) · “happy” for “happily” · the strongest word in the wrong place (“furious” about a lost pencil). <b>Support:</b> the poster (p.4) on the desk. <b>Fast finishers:</b> make your own ladder of 4 words and test a partner.</div>
  <p class="small"><b>Domino answer chain</b> (START → FINISH):</p>
  <ol class="small" style="columns:2;column-gap:12px;font-size:7.4pt;line-height:1.22;margin:0;padding-left:16px">{chain_key}</ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">Cut up the cards · one Guide Word card per student</div><h1>Ladder Sort + Guide Word Swap</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:8.8pt;margin:0"><b>Ladder Sort.</b> One set per group. Sort the 24 words into 8 families of 3, then put each family in order from the weakest (bottom) to the strongest (top).</p>
  <div class="fym">{ls_html}</div>
  <p style="font-size:8.8pt;margin:3mm 0 0"><b>Guide Word Swap.</b> Don't show your card. Read, listen, find the page, then check.</p>
  {gw_card("A", WORDS_A, PAGES_A)}
  {gw_card("B", WORDS_B, PAGES_B)}
</div>

<div class="page">
  <div class="band"><div><div class="k">Groups of 3–4 · cut along the dashed lines</div><h1>Prefix &amp; Family Dominoes</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.4pt">Start with START. Make the word the clue on the right asks for, then find the domino with that word on its left. Keep going until you reach FINISH.</p>
  <div class="doms">{dom_html}</div>
</div>

<div class="page">
  <div class="poster">
    <h1>Climb the word ladder</h1>
    <div class="ops">
      <div style="background:var(--green-soft)"><b>Ladder</b>warm → hot<br>→ sweltering<br><i>weakest at the bottom</i></div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Cut “very”</b>very tired<br>→ exhausted<br><i>one strong word</i></div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Not</b>un- dis- in-<br>im (p, m) il (l) ir (r)<br><i>illegal, irregular</i></div>
      <div style="background:var(--green-soft)"><b>re · mis · pre</b>again · wrongly<br>· before<br><i>rewrite, misspell</i></div>
      <div style="background:var(--green-soft)"><b>Families</b>happy · happily<br>· happiness<br><i>which job does the gap need?</i></div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Dictionary</b>ABC: 2nd, 3rd letter<br>guide words<br><i>read the whole sentence</i></div>
    </div>
    <p style="text-align:center;font-size:20pt!important;font-weight:800;margin:4mm 0">Don't say very hungry. Say starving!</p>
    <p style="text-align:center;font-size:10pt;color:var(--muted)">Léim · leim.ie · Play Word Ladder: {GAME}</p>
  </div>
</div>

<div class="page ws">
  <div class="band"><div><div class="k">Worksheet</div><h1>Error Hunt + exam-style questions</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Error Hunt</h2>
  <p>Each sentence has one weak or wrong word in bold. Say what's wrong and write a better word.</p>
  <table class="eh"><thead><tr><th>Sentence</th><th>What's wrong and the fix</th></tr></thead><tbody>
  {"".join(f"<tr><td>{s}</td><td><span class='gap'></span><span class='gap'></span></td></tr>" for s, r in ERR)}
  </tbody></table>
  <h2>B. Exam-style questions</h2>
  <div class="pass">{WS_RAW}</div>
  <ol class="q">
    <li>Replace each underlined phrase with one stronger word that keeps the meaning.<span class="long"></span><span class="long"></span></li>
    <li>Write the opposite of each word with a prefix: {", ".join(r for r, a in WS_PRE)}.<span class="long"></span></li>
    <li>Put these words on a ladder, bottom → top: soaked, damp, wet.<span class="long"></span></li>
    <li>“My little brother <b>clung</b> to Dad's hand.” What does “clung” suggest about how he felt? Why is it better than “held”?<span class="long"></span></li>
    <li>Find a word in the passage that has more than one meaning. Write two sentences that show two different meanings.<span class="long"></span></li>
  </ol>
</div>

<div class="page an">
  <div class="band"><div><div class="k">For the teacher</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>Ladder Sort</h2>
  <p>{ls_key}. Accept a different order if students can defend it (e.g. chilly and cold are close).</p>
  <h2>Guide Word Swap</h2>
  <p>A's words on B's pages: {" · ".join(f"{w} → page {p}" for w, p in GA)}.<br>B's words on A's pages: {" · ".join(f"{w} → page {p}" for w, p in GB)}.</p>
  <h2>A. Error Hunt</h2>
  <table><tbody>{"".join(f"<tr><td style='width:42%'>{s}</td><td>{r}</td></tr>" for s, r in ERR)}</tbody></table>
  <h2>B. Exam-style questions</h2>
  <ol class="q">
    <li>{" · ".join(f"{x} → <b>{y}</b>" for x, y in WS_FIX)}. Accept other strong words that keep the meaning (tough, drenched, petrified, breathtaking, delighted).</li>
    <li>{", ".join(a for r, a in WS_PRE)}</li>
    <li>damp → wet → soaked</li>
    <li>“Clung” suggests he held on tightly because he was frightened and needed to feel safe. It is better than “held” because it shows his fear without saying “he was scared”.</li>
    <li>e.g. <b>shower</b>: “a heavy shower of rain” / “I had a shower after the climb”. Also hand, top, loose, held. Any two sentences that show two clearly different meanings.</li>
  </ol>
  <h2>Marking tip</h2>
  <p>For “what does this word suggest?” questions, reward the meaning AND the effect (feeling, picture, tone). In students' own writing, reward precise words that fit the context over long or rare words used loosely.</p>
</div>
</body></html>"""

cover = """<!doctype html><html><head><meta charset="utf-8"><style>
body{margin:0;width:1200px;height:1200px;background:#1B2430;font-family:Inter,sans-serif;color:#fff;display:flex;flex-direction:column;justify-content:space-between;padding:90px;box-sizing:border-box}
.k{display:inline-block;background:#2E7D57;border-radius:99px;padding:12px 26px;font-weight:700;font-size:28px;letter-spacing:.06em;text-transform:uppercase}
h1{font-size:120px;font-weight:800;line-height:1.15;letter-spacing:-.02em;margin:60px 0 20px}
h1 span{background:#F6CF5A;color:#1B2430;padding:0 18px;border-radius:14px}
.sub{font-size:40px;line-height:1.4;color:#DDE3EA}
.em{font-size:52px;margin-top:30px;font-weight:800;letter-spacing:.01em;color:#F6CF5A}
.foot{display:flex;justify-content:space-between;align-items:center;font-size:34px;font-weight:700}
.price{background:#F6CF5A;color:#1B2430;border-radius:16px;padding:14px 28px}
</style></head><body>
<div><span class="k">Junior Cycle English · Teacher pack</span>
<h1><span>Vocabulary</span></h1>
<div class="sub">Word ladders · prefixes · families · dictionary<br>Ladder Sort · Guide Word Swap A/B · Dominoes<br>Poster · Worksheet + answers</div>
<div class="em">warm → hot → sweltering</div></div>
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
    pdf("teacher-pack", os.path.join(OUT, "Vocabulary-Teacher-Pack-Leim.pdf"))
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--hide-scrollbars", "--window-size=1200,1200",
                    f"--screenshot={os.path.join(OUT, f'{SLUG}-cover.png')}", f"{SLUG}-cover.html"], cwd=SRC, check=True, capture_output=True)
    print("domino chain:", [a for c, a in chain])
