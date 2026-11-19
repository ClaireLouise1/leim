#!/usr/bin/env python3
"""Spelling & commonly confused words (JC English topic 6, game Spell Strike): free sheet + teacher pack + Payhip cover.
Run from the repo root: python3 src/build_spelling_pdfs.py OUTDIR
Writes src/spelling-confused-words-*.html; PDFs/cover PNG go to OUTDIR (free sheet also to printables/).
Items come from the game's own data block (spell-strike.html); every answer is re-checked with the rules in
src/test_spell_strike.py (pyspellchecker dictionary, its own mix-up context rules with spaCy, inflect plurals, its own suffix rules).
Styles are read from src/build_money1_pdfs.py."""
import os, sys, random, subprocess, re, json
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC)
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/sp"; os.makedirs(OUT, exist_ok=True)
SLUG = "spelling-confused-words"
LO = "W11, R10"
GAME = "leim.ie/spell-strike.html"
_t = open(os.path.join(SRC, "test_spell_strike.py"), encoding="utf-8").read()
exec(_t[:_t.index("bad = 0")])          # known, dist, rule, add_rule, INF, GROUPS, nlp
D = json.loads(open(os.path.join(ROOT, "spell-strike.html"), encoding="utf-8").read().split("/*DATA*/")[1].split("/*END*/")[0])
SPELL = {w: (s, wr, tip) for w, s, wr, tip in D["spell"]}
def mix_ok(sent, ans, group):
    want = rule(group, sent); return want is not None and want.lower() == ans.lower()

# ---------- free sheet ----------
random.seed(6)
A_W = ["definitely", "necessary", "separate", "receive", "friend", "beginning", "tomorrow", "embarrassed"]
A = []
for w in A_W:
    s, wr, tip = SPELL[w]; opts = [w] + wr[:2]; random.shuffle(opts); A.append((s.replace("___", "(" + " / ".join(opts) + ")"), w))
    assert known(w) and not any(known(x) for x in wr)
B_S = ["The players left ___ boots in the dressing room.", "___ going to be late again.", "Tell me when ___ ready.", "This tea is ___ hot.",
       "I could ___ won that race.", "Cork is bigger ___ Galway.", "The test was ___ hard.", "My tooth is ___.",
       "She ___ her dog to school for the day.", "I don't know ___ to laugh or cry."]
MIX = {s: (a, g) for s, a, g in D["mix"]}
B = []
for s in B_S:
    a, g = MIX[s]; assert mix_ok(s, a, g), s
    opts = [x.capitalize() if s.startswith("___") else x for x in GROUPS[g]]
    B.append((s.replace("___", "(" + " / ".join(opts) + ")"), a))
C_W = ["baby", "knife", "box", "potato", "monkey", "child", "leaf", "tooth"]
C = [(w, INF.plural(w)) for w in C_W]
PL = {o: m for o, m, e in D["plural"]}
for w, p in C: assert PL[w] == p
D_W = [("hop", "ing"), ("hope", "ing"), ("happy", "ness"), ("carry", "ed"), ("begin", "ing"), ("care", "ful"), ("cry", "ing"), ("big", "est")]
Dd = [(w, e, add_rule(w, e)) for w, e in D_W]
for w, e, a in Dd: assert known(a) and [w, e, a] in D["add"], (w, e, a)
E_S = [("I'll see you <b>tommorow</b>.", "tomorrow"), ("My <b>freind</b> lives in Tralee.", "friend"), ("We have PE on <b>Wensday</b>.", "Wednesday"),
       ("Tory is an <b>iland</b> off Donegal.", "island"), ("We had an <b>arguement</b> about the remote.", "argument"), ("That's a <b>wierd</b> noise.", "weird")]
for s, w in E_S:
    wrong = re.search(r"<b>(.*?)</b>", s).group(1); assert known(w) and not known(wrong) and wrong in SPELL[w][1], (s, w)
PASS_RAW = "On <u>wensday</u> my <u>freind</u> and I went to the <u>libary</u>. <u>Their</u> was a <u>wierd</u> man reading a book about <u>potatos</u>. He was <u>quiet</u> funny, but we <u>new</u> we had to be <u>quite</u>."
PASS_FIX = [("wensday", "Wednesday"), ("freind", "friend"), ("libary", "library"), ("Their", "There"), ("wierd", "weird"), ("potatos", "potatoes"), ("quiet", "quite"), ("new", "knew"), ("quite", "quiet")]
assert [x for x, y in PASS_FIX] == re.findall(r"<u>(.*?)</u>", PASS_RAW)
assert mix_ok("___ was a man reading.", "There", "there") and mix_ok("He was ___ funny.", "quite", "quiet") and mix_ok("We had to be ___.", "quiet", "quiet")
assert INF.plural("potato") == "potatoes" and all(known(y.lower()) for x, y in PASS_FIX) and not any(known(x.lower()) for x in ["wensday", "freind", "libary", "wierd", "potatos"])
NQ = len(A) + len(B) + len(C) + len(Dd) + len(E_S) + 2; assert NQ == 42, NQ

def qs(items): return "".join(f"<li>{q} <span class='line'></span></li>" for q in items)
def style(var):
    return re.search(var + r' = f"""<!doctype.*?<style>(.*?)</style>', open(os.path.join(SRC, "build_money1_pdfs.py"), encoding="utf-8").read(), re.S).group(1).replace("{LO}", LO).replace("{{", "{").replace("}}", "}").replace("JC Maths LOs (2018 spec)", "JC English LOs (2015 spec)")
SHEET_STYLE = style("sheet"); PACK_STYLE = style("pack")
assert "JC English LOs (2015 spec)" in SHEET_STYLE and "Single-teacher licence" in PACK_STYLE and "JC English LOs (2015 spec)" in PACK_STYLE
EXTRA = """.wk{line-height:1.45;border:1.5px solid var(--line);border-radius:8px;padding:2px 7px;margin:3px 0;font-size:9.4pt}.wk b.h{display:block}
table.st td:first-child{white-space:nowrap}table.st{border-collapse:collapse;margin:3px 0;font-size:9.2pt;width:100%}table.st td,table.st th{border:1px solid #C9D1DA;padding:1.5px 6px;text-align:left;vertical-align:top}
.pass{border-left:4px solid var(--green);background:var(--mist);padding:5px 10px;margin:4px 0;font-style:italic;line-height:1.6}"""
sheet = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Spelling and commonly confused words: rules and practice | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{SHEET_STYLE}
{EXTRA}
</style></head><body>
<div class="page tight">
  <div class="band"><div><div class="k">Junior Cycle English · Free revision sheet</div><h1>Spelling and commonly confused words</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2015 specification): {LO}. Play the game: <b>{GAME}</b></p>
  <div class="two">
   <div><h2>1. Adding endings</h2>
    <table class="st"><tbody>
     <tr><td><b>Double it</b></td><td>short vowel + one consonant, ending starts with a vowel: hop → hopping, stop → stopped, big → biggest. Two syllables, stress at the end: begin → beginning. (Not w, x, y: snowing, fixing.)</td></tr>
     <tr><td><b>Drop the e</b></td><td>before a vowel ending: hope → hoping, make → making. Keep it before a consonant: careful, lovely.</td></tr>
     <tr><td><b>y → i</b></td><td>consonant + y: happy → happiness, carry → carried. Keep the y before -ing (crying) and after a vowel (played).</td></tr></tbody></table>
    <div class="wk"><b>hopping</b> = jumping · <b>hoping</b> = wishing. One letter, a different word.</div>
    <h2>2. Plurals</h2>
    <table class="st"><tbody>
     <tr><td><b>+ s</b></td><td>most words, vowel + y: days, keys, photos, pianos</td></tr>
     <tr><td><b>+ es</b></td><td>after s, x, ch, sh: buses, boxes, churches, wishes · and potatoes, tomatoes, heroes</td></tr>
     <tr><td><b>y → ies</b></td><td>consonant + y: babies, cities, parties</td></tr>
     <tr><td><b>f → ves</b></td><td>knives, leaves, wolves, loaves, shelves</td></tr>
     <tr><td><b>learn</b></td><td>children, mice, teeth, feet, women, geese, sheep</td></tr></tbody></table>
    <div class="note">Never an apostrophe for a plural: <s>potato's</s> → potatoes.</div>
    <h2>3. Memory tricks</h2>
    <div class="wk">i before e, except after c: believe, friend, receive (weird is weird) · hidden words: de<b>finite</b>ly, sep<b>a rat</b>e, envi<b>ron</b>ment · silent letters: <b>k</b>nife, i<b>s</b>land, ans<b>w</b>er, We<b>d</b>nesday · doubles: ne<b>c</b>e<b>ss</b>ary, e<b>mbarrass</b>ed, a<b>dd</b>re<b>ss</b>, to<b>m</b>o<b>rr</b>ow</div></div>
   <div><h2>4. Commonly confused words</h2>
    <table class="st"><tbody>
     <tr><td><b>there / their / they're</b></td><td>over there · their boots · they're = they are</td></tr>
     <tr><td><b>your / you're</b></td><td>your phone · you're = you are</td></tr>
     <tr><td><b>to / too / two</b></td><td>go to school · too hot, me too · two sisters</td></tr>
     <tr><td><b>could have</b></td><td>could have, should have, must have (never “could of”)</td></tr>
     <tr><td><b>where / were / wear</b></td><td>where is it? · we were late · wear a coat</td></tr>
     <tr><td><b>than / then</b></td><td>taller than me · and then we left</td></tr>
     <tr><td><b>quiet / quite</b></td><td>be quiet · quite hard</td></tr>
     <tr><td><b>lose / loose</b></td><td>lose the match · a loose tooth</td></tr>
     <tr><td><b>accept / except</b></td><td>accept a gift · everyone except me</td></tr>
     <tr><td><b>affect / effect</b></td><td>rain affects the match (verb) · special effects (noun)</td></tr>
     <tr><td><b>weather / whether</b></td><td>sunny weather · whether to go</td></tr>
     <tr><td><b>past / passed</b></td><td>walked past, half past three · she passed the test</td></tr>
     <tr><td><b>bought / brought</b></td><td>bought = buy (money) · brought = bring</td></tr>
     <tr><td><b>hear / here</b></td><td>hear with your ear · come here</td></tr>
     <tr><td><b>know / no · new / knew</b></td><td>I know · no milk left · a new bike · I knew it</td></tr>
     <tr><td><b>our / are</b></td><td>our teacher · we are going</td></tr></tbody></table>
    <div class="wk"><b class="h">The swap test</b>Swap in the long form: “they are”, “you are”. If it makes sense, use the short form with the apostrophe. If not, use their / your.</div></div>
  </div>
  <div class="tip"><b>Exam tip:</b> key words from the question are printed on the paper, so copy them carefully. Not sure of a word? Use one you can spell. Leave 3 minutes to read your answer back, one word at a time.</div>
</div>

<div class="page p2">
  <div class="band"><div><div class="k">Practice · {NQ} questions</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Circle the right spelling</h2><ol class="q" style="columns:2;column-gap:8mm">{qs(q for q, a in A)}</ol>
  <h2>B. Circle the right word</h2><ol class="q" start="9" style="columns:2;column-gap:8mm">{qs(q for q, a in B)}</ol>
  <h2>C. Write the plural</h2><ol class="q" start="19" style="columns:4;column-gap:6mm">{qs("one " + w + " → two" for w, p in C)}</ol>
  <h2>D. Add the ending</h2><ol class="q" start="27" style="columns:4;column-gap:6mm">{qs(f"{w} + {e}" for w, e, a in Dd)}</ol>
  <h2>E. Correct the spelling mistake in bold</h2><ol class="q" start="35" style="columns:2;column-gap:8mm">{qs(s for s, w in E_S)}</ol>
  <h2>F. Exam-style</h2>
  <div class="pass">{PASS_RAW}</div>
  <ol class="q" start="{NQ - 1}">
   <li>Nine words are underlined. Correct each one.<span class="long"></span><span class="long"></span></li>
   <li>Write two sentences of your own: one using <i>their</i> and <i>they're</i>, one using <i>than</i> and <i>then</i>.<span class="long"></span></li>
  </ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">Check your work</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <table class="ans"><tbody>
   <tr><td><b>A</b></td><td>{" · ".join(f"{i}. {a}" for i, (q, a) in enumerate(A, 1))}</td></tr>
   <tr><td><b>B</b></td><td>{" · ".join(f"{i}. {a}" for i, (q, a) in enumerate(B, 9))}</td></tr>
   <tr><td><b>C</b></td><td>{" · ".join(f"{i}. {p}" for i, (w, p) in enumerate(C, 19))}</td></tr>
   <tr><td><b>D</b></td><td>{" · ".join(f"{i}. {a}" for i, (w, e, a) in enumerate(Dd, 27))}</td></tr>
   <tr><td><b>E</b></td><td>{" · ".join(f"{i}. {w}" for i, (s, w) in enumerate(E_S, 35))}</td></tr>
   <tr><td><b>F</b></td><td>{NQ - 1}. {" · ".join(f"{x} → <b>{y}</b>" for x, y in PASS_FIX)}<br>{NQ}. Answers will vary, e.g. They're bringing their dog. We ate, then we watched a film that was longer than the last one.</td></tr>
  </tbody></table>
  <h2>Worked examples</h2>
  <div class="two">
   <div class="wk"><b class="h">10. They're going to be late again.</b>Swap test: “They are going to be late” makes sense, so the short form <b>they're</b>.</div>
   <div class="wk"><b class="h">13. I could have won that race.</b>After could, would, should, must, might it's always <b>have</b>. “Could of” is what “could've” sounds like.</div>
   <div class="wk"><b class="h">27. hop + ing = hopping</b>Short vowel (o) and one consonant (p): double it. Compare 28: hope ends in e, so drop the e: <b>hoping</b>.</div>
   <div class="wk"><b class="h">33. cry + ing = crying</b>Usually consonant + y changes to i, but not before -ing (criing would have two i's). Keep the y.</div>
  </div>
  <div class="note"><b>Got one wrong?</b> Find the rule on page 1, then play <b>Spell Strike</b> at {GAME}: the “Go back over these” list at the end shows the reason for each mistake.</div>
  <p class="small">All sentences written by Léim. Léim is independent and not connected with the State Examinations Commission or the NCCA.</p>
</div>
</body></html>"""
assert B[1][1] == "They're" and B[4][1] == "have" and Dd[0][2] == "hopping" and Dd[6][2] == "crying"

# ---------- teacher pack ----------
MATCH = [("They hung ___ coats on the hooks.", "their"), ("Leave your bag over ___.", "there"), ("I think ___ coming to the match later.", "they're"),
         ("Is ___ brother in first year?", "your"), ("I think ___ the best goalkeeper we have.", "you're"), ("I have ___ cousins in Boston.", "two"),
         ("The soup was ___ salty.", "too"), ("She must ___ forgotten.", "have"), ("My sister is older ___ me.", "than"),
         ("The exam was ___ easy.", "quite"), ("These jeans are ___ on me.", "loose"), ("He ___ his guitar to the party.", "brought")]
GRP = {"their": "there", "there": "there", "they're": "there", "your": "your", "you're": "your", "two": "to", "too": "to", "have": "of",
       "than": "then", "quite": "quiet", "loose": "lose", "brought": "bought"}
for s, a in MATCH: assert mix_ok(s, a, GRP[a]), (s, a)
assert len({a.lower() for s, a in MATCH}) == 12
random.seed(106); order = list(range(24)); random.shuffle(order)
cards = [("q", i) for i in range(12)] + [("a", i) for i in range(12)]
match_print = [cards[k] for k in order]
match_html = "".join(f'<div class="c"><span class="tag">Card {k}</span><div class="fc{" sm" if t == "q" else ""}">{MATCH[i][1] if t == "a" else MATCH[i][0]}</div></div>' for k, (t, i) in enumerate(match_print, 1))
match_key = " · ".join(f"{match_print.index(('q', i)) + 1} → {match_print.index(('a', i)) + 1}" for i in range(12))

SW_A = ["definitely", "necessary", "separate", "receive", "Wednesday", "February", "embarrassed", "island"]
SW_B = ["believe", "beginning", "disappear", "tomorrow", "environment", "library", "rhythm", "address"]
for w in SW_A + SW_B: assert known(w) and w in SPELL
assert not set(SW_A) & set(SW_B)
def sw_card(who, mine):
    lines = "".join(f"<li>{SPELL[w][0].replace('___', '<b>' + w + '</b>')}</li>" for w in mine)
    gaps = "".join(f"<li><span class='gap'></span></li>" for w in mine)
    return f'''<div class="idc"><h3>Student {who} · Spelling Swap</h3><div class="two"><div><p style="font-size:8.6pt;margin:0 0 1mm"><b>1. Read each sentence to your partner.</b> Say the word in bold twice. Don't spell it out!</p><ol class="ss" style="font-size:9pt;margin:0;padding-left:15px;line-height:1.35">{lines}</ol></div>
<div><p style="font-size:8.6pt;margin:0 0 1mm"><b>2. Write your partner's 8 words.</b> Then swap cards and check. Got one wrong? Write it 3 times.</p><ol class="ss" style="font-size:9pt;margin:0;padding-left:15px">{gaps}</ol></div></div></div>'''

# Spelling Dominoes: 20 clues, 20 different answers, each worked out by the checker's rules
DOMS = [(f"{w} + {e}", add_rule(w, e)) for w, e in [("hop", "ing"), ("hope", "ing"), ("happy", "ness"), ("carry", "ed"), ("begin", "ing"), ("make", "ing"), ("stop", "ed")]]
DOMS += [(f"one {w}, two ___", INF.plural(w)) for w in ["baby", "knife", "child", "box", "potato", "mouse"]]
MIXD = [("He is taller ___ me.", "than", "then"), ("Put it over ___.", "there", "there"), ("You should ___ known.", "have", "of"),
        ("___ going home now.", "They're", "there"), ("Is this ___ coat?", "your", "your"), ("It's ___ cold today.", "too", "to")]
for s, a, g in MIXD: assert mix_ok(s, a, g), s
DOMS += [(s, a) for s, a, g in MIXD] + [("Silent k: ___nife", "knife")]
assert len(DOMS) == 20 and len({a.lower() for c, a in DOMS}) == 20 and all(known(a.lower()) for c, a in DOMS)
random.seed(1006); chain = DOMS[:]; random.shuffle(chain)
dom = [("START" if k == 0 else chain[k - 1][1], x[0]) for k, x in enumerate(chain)] + [(chain[-1][1], "FINISH")]
dom_print = dom[:]; random.shuffle(dom_print)
dom_html = "".join(f'<div class="dom"><div class="h l{" sm" if len(l) > 8 else ""}">{l}</div><div class="h r">{r}</div></div>' for l, r in dom_print)
chain_key = "".join(f"<li>{c}: <b>{a}</b></li>" for c, a in chain)

ERR = [("I <b>new</b> the answer straight away.", "Past of know → <b>knew</b> (new = not old)"),
       ("We <b>where</b> late for school.", "Past of are → <b>were</b>"),
       ("Can you <b>here</b> the music?", "With your ear → <b>hear</b>"),
       ("The team lost <b>it's</b> first match.", "Belonging to it, no apostrophe → <b>its</b>"),
       ("I <b>brought</b> a new phone in the sale.", "Paid money, from buy → <b>bought</b>"),
       ("She is <b>to</b> tired to play.", "More than enough → <b>too</b>")]
assert known("knew") and mix_ok("We ___ late for school.", "were", "where") and mix_ok("Can you ___ the music?", "hear", "hear")
assert mix_ok("I ___ a new phone in the sale.", "bought", "bought") and mix_ok("She is ___ tired to play.", "too", "to")
WS_RAW = "Last Febuary our class went to Spike Island. Their was a guide who told us about the prisoners. It was definately the most intresting trip, but my freind got embarassed when she lost her hat in the wind. We should of brought warmer coats. The weather was much colder then we expected."
WS_FIX = [("Febuary", "February"), ("Their", "There"), ("definately", "definitely"), ("intresting", "interesting"), ("freind", "friend"), ("embarassed", "embarrassed"), ("should of", "should have"), ("then", "than")]
for x, y in WS_FIX: assert WS_RAW.count(x + " ") == 1 or WS_RAW.count(" " + x) == 1, x
fixed = WS_RAW
for x, y in WS_FIX: fixed = re.sub(r"\b" + re.escape(x) + r"\b", y, fixed, count=1)
for w in re.findall(r"[A-Za-z]+", fixed): assert known(w.lower()), w
assert not any(known(x.lower()) for x, y in WS_FIX[:6] if x != "Their")
assert mix_ok("___ was a guide.", "There", "there") and mix_ok("We should ___ brought warmer coats.", "have", "of") and mix_ok("It was colder ___ we expected.", "than", "then")
WS_PL = [("prisoner", "prisoners"), ("coat", "coats"), ("class", "classes"), ("story", "stories")]
for w, p in WS_PL: assert INF.plural(w) == p

pack = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Spelling Teacher Pack | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{PACK_STYLE}
{EXTRA}
.fym .c{{height:13.6mm}}.fym .fc{{font-size:13pt;font-weight:800}}.fym .fc.sm{{font-size:9.4pt;line-height:1.2;font-weight:600}}.idc{{padding:1.5mm 4mm}}.idc h3{{margin:0 0 1mm}}
.idc .gap{{display:block;border-bottom:1px solid #9AA3AE;height:15px}}ol.ss li{{margin:0}}
.dom .r{{font-size:9pt;line-height:1.25}}.dom .l{{font-size:13pt}}.dom .l.sm{{font-size:10.5pt}}.p1 .proc td{{font-size:8.6pt;padding:2px 6px}}
.ops div{{font-size:12pt;padding:4mm 3mm}}.ops b{{font-size:17pt}}.pass{{font-size:10pt}}
</style></head><body>

<div class="page p1">
  <div class="band"><div><div class="k">Junior Cycle English · Teacher pack</div><h1>Spelling and commonly confused words</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2015 specification): {LO}</p>
  <div class="two">
    <div><h3>Aims</h3><p>By the end of the lesson students can choose correctly between common mix-ups (there / their / they're, your / you're, to / too / two, could have, than / then …), apply the doubling, drop-the-e and y → i rules when adding endings, form regular and irregular plurals, and use memory tricks for tricky words.</p></div>
    <div><h3>In this pack</h3><p>p.1 Teacher notes · p.2 Gap Match mingle cards + Spelling Swap A/B cards · p.3 Spelling Dominoes (cut-up) · p.4 Wall poster · p.5 Worksheet: Error Hunt + exam-style questions · p.6 Answers. Level: 1st year (useful revision in 2nd and 3rd). Time: about 60 minutes. All sentences are original.</p></div>
  </div>
  <h2 style="margin-top:8px">Procedure</h2>
  <table class="proc"><tbody>
    <tr><td>5 min</td><td><b>Lead-in.</b> Board: “hopping / hoping”. Who is jumping? Who is wishing? Elicit that one letter changes the word.</td></tr>
    <tr><td>8 min</td><td><b>Guided discovery.</b> Board hop → hopping, run → running, hope → hoping, ride → riding. Pairs: when do we double? when do we drop the e? Then happy → happiness, carry → carried, cry → crying, play → played: what happens to y? Quick board review of the swap test (they're = they are).</td></tr>
    <tr><td>10 min</td><td><b>Gap Match mingle</b> (p.2, 24 cards = 12 sentences with a gap + 12 words; one card each). Find your partner, then say the rule or the swap test that proves it.</td></tr>
    <tr><td>12 min</td><td><b>Spelling Swap</b> (p.2, pairs, don't show your card). A reads a sentence and says the bold word twice; B writes it. 8 words each, then swap roles. Swap cards and check; each missed word is written 3 times with its memory trick (poster, p.4).</td></tr>
    <tr><td>10 min</td><td><b>Spelling Dominoes</b> (p.3), groups of 3–4. Start with START, work out the answer to the clue, find the domino with that word on its left. Build the chain to FINISH.</td></tr>
    <tr><td>12 min</td><td><b>Worksheet</b> (p.5). Error Hunt in pairs, then the exam-style questions alone.</td></tr>
    <tr><td>3 min</td><td><b>Exit ticket.</b> “Their going too the shop to buy to apples.” → They're going to the shop to buy two apples. Homework: play <b>Spell Strike</b> at {GAME}.</td></tr>
  </tbody></table>
  <div class="note"><b>Mingle key</b> (sentence card → word card): {match_key}.<br>
  <b>Errors to look for:</b> could of · their / there / they're · to / too · then for than · hopeing / hoping · babys, potatos · i before e slips. <b>Support:</b> the poster (p.4) on the desk. <b>Fast finishers:</b> write one sentence with there, their and they're.</div>
  <p class="small"><b>Domino answer chain</b> (START → FINISH):</p>
  <ol class="small" style="columns:2;column-gap:12px;font-size:7.4pt;line-height:1.22;margin:0;padding-left:16px">{chain_key}</ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">Cut up the cards · one Spelling card per student</div><h1>Gap Match + Spelling Swap</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:8.8pt;margin:0"><b>Gap Match mingle.</b> Cut out the 24 cards and give one to each student. Sentence card? Find the word that fills your gap. Word card? Find the sentence it fits. (Fewer students? Take out whole pairs.)</p>
  <div class="fym">{match_html}</div>
  <p style="font-size:8.8pt;margin:3mm 0 0"><b>Spelling Swap.</b> Don't show your card. Read, listen, write, then check.</p>
  {sw_card("A", SW_A)}
  {sw_card("B", SW_B)}
</div>

<div class="page">
  <div class="band"><div><div class="k">Groups of 3–4 · cut along the dashed lines</div><h1>Spelling Dominoes</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.4pt">Start with START. Work out the answer to the clue on the right, then find the domino with that word on its left. Keep going until you reach FINISH.</p>
  <div class="doms">{dom_html}</div>
</div>

<div class="page">
  <div class="poster">
    <h1>Spell it right</h1>
    <div class="ops">
      <div style="background:var(--green-soft)"><b>Double it</b>hop → hopping<br>big → biggest<br><i>short vowel + 1 consonant</i></div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Drop the e</b>hope → hoping<br>make → making<br><i>but careful, lovely</i></div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>y → i</b>happy → happiness<br>baby → babies<br><i>but crying, played</i></div>
      <div style="background:var(--green-soft)"><b>Swap test</b>they're = they are<br>you're = you are<br><i>doesn't fit? their / your</i></div>
      <div style="background:var(--green-soft)"><b>could have</b>should have · must have<br><i>never “could of”</i></div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Tricks</b>de-FINITE-ly · sep-A-RAT-e<br><i>i before e, except after c</i></div>
    </div>
    <p style="text-align:center;font-size:20pt!important;font-weight:800;margin:4mm 0">I'm hoping, not hopping!</p>
    <p style="text-align:center;font-size:10pt;color:var(--muted)">Léim · leim.ie · Play Spell Strike: {GAME}</p>
  </div>
</div>

<div class="page ws">
  <div class="band"><div><div class="k">Worksheet</div><h1>Error Hunt + exam-style questions</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Error Hunt</h2>
  <p>Each sentence has one mistake in bold. Say what's wrong and write it correctly.</p>
  <table class="eh"><thead><tr><th>Sentence</th><th>What's wrong and the fix</th></tr></thead><tbody>
  {"".join(f"<tr><td>{s}</td><td><span class='gap'></span><span class='gap'></span></td></tr>" for s, r in ERR)}
  </tbody></table>
  <h2>B. Exam-style questions</h2>
  <div class="pass">{WS_RAW}</div>
  <ol class="q">
    <li>Find and correct the 8 spelling mistakes in the passage.<span class="long"></span><span class="long"></span><span class="long"></span></li>
    <li>Three of the mistakes are real words in the wrong place. Which three?<span class="long"></span></li>
    <li>Explain why “should of” is wrong.<span class="long"></span></li>
    <li>Write the plurals: {", ".join(w for w, p in WS_PL)}.<span class="long"></span></li>
    <li>Write one sentence about a school trip that uses there, their and they're correctly.<span class="long"></span></li>
  </ol>
</div>

<div class="page an">
  <div class="band"><div><div class="k">For the teacher</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>Gap Match</h2>
  <p>{" · ".join(s.replace("___", "<b>" + a + "</b>") for s, a in MATCH)}</p>
  <h2>Spelling Swap</h2>
  <p>Students check against their partner's card. A: {", ".join(SW_A)}. B: {", ".join(SW_B)}.</p>
  <h2>A. Error Hunt</h2>
  <table><tbody>{"".join(f"<tr><td style='width:40%'>{s}</td><td>{r}</td></tr>" for s, r in ERR)}</tbody></table>
  <h2>B. Exam-style questions</h2>
  <ol class="q">
    <li>{" · ".join(f"{x} → <b>{y}</b>" for x, y in WS_FIX)}</li>
    <li><b>Their</b> (should be There), <b>of</b> (should have), <b>then</b> (than). A spellchecker won't catch these, so read them yourself.</li>
    <li>After should, could, would, must and might we need the verb <b>have</b>. “Of” only sounds the same as the short form should've.</li>
    <li>{", ".join(p for w, p in WS_PL)} (class ends in s → es; story is consonant + y → ies)</li>
    <li>e.g. They're bringing their lunches, so leave the bags over there.</li>
  </ol>
  <h2>Marking tip</h2>
  <p>In students' own writing, spelling is part of accuracy. Mix-ups (there / their, could of) and words copied wrongly from the question count most against an answer; an occasional slip in a hard word matters less than a pattern of the same mistake.</p>
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
<h1><span>Spelling</span></h1>
<div class="sub">Tricky words · commonly confused words<br>Gap Match · Spelling Swap A/B · Dominoes<br>Poster · Worksheet + answers</div>
<div class="em">there · their · they're</div></div>
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
    pdf("teacher-pack", os.path.join(OUT, "Spelling-Teacher-Pack-Leim.pdf"))
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--hide-scrollbars", "--window-size=1200,1200",
                    f"--screenshot={os.path.join(OUT, f'{SLUG}-cover.png')}", f"{SLUG}-cover.html"], cwd=SRC, check=True, capture_output=True)
    print("domino chain:", [a for c, a in chain])
