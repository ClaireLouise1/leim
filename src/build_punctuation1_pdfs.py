#!/usr/bin/env python3
"""Punctuation 1 (JC English topic 3, game Comma Catch): free sheet + teacher pack + Payhip cover.
Run from the repo root: python3 src/build_punctuation1_pdfs.py OUTDIR
Writes src/punctuation-1-*.html; PDFs/cover PNG go to OUTDIR (free sheet also to printables/).
Items come from the game's own data block (comma-catch.html); every answer is re-checked with the rules in
src/test_comma_catch.py (commas, capitals, end marks, short forms with spaCy) and an owner rule for apostrophes.
Styles are read from src/build_money1_pdfs.py."""
import os, sys, random, subprocess, re, json
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC)
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/p1"; os.makedirs(OUT, exist_ok=True)
SLUG = "punctuation-1"
LO = "W11, W6"
GAME = "leim.ie/comma-catch.html"
# the checker's rule functions (comma_ok, caps_ok, end_mark, EXP, POSS, IRR, nlp) — everything above its main loop
_t = open(os.path.join(SRC, "test_comma_catch.py"), encoding="utf-8").read()
exec(_t[:_t.index("bad = 0; n = 0")])
D = json.loads(open(os.path.join(ROOT, "comma-catch.html"), encoding="utf-8").read().split("/*DATA*/")[1].split("/*END*/")[0])

def own(one, n):
    if n == 1: return one + "'s"
    pl = IRR.get(one, one + "s")
    return pl + "'" if pl.endswith("s") else pl + "'s"
def short_ok(sent, ans):
    """spaCy: noun after the gap -> belonging word; otherwise a short form"""
    filled = sent.replace("___", ans); i0 = sent.index("___")
    after = [t for t in nlp(filled) if t.idx >= i0 + len(ans)][0]
    return (ans.lower() in POSS) if after.pos_ in ("NOUN", "PROPN") else (ans.lower() in EXP)
COMMA = {x["s"]: x for x in D["comma"]}
def comma_item(s):
    it = COMMA[s]; assert comma_ok(s, it["c"], it["k"]), s; return s

# ---------- free sheet ----------
A = [s.replace("~", "") for s in D["caps"] if s.replace("~", "").startswith(("On Monday", "My cousin", "We go to", "Can I", "Dr Walsh", "Lisa and"))]
assert len(A) == 6 and all(caps_ok(a) for a in A)
Aq = [a.lower() for a in A]
for q in Aq: assert not caps_ok(q)
BORD = ["Where is my phone", "What a brilliant goal", "The match starts at six", "How old is your brother",
        "How kind you are", "Have you finished your homework", "She asked if I was hungry", "What a mess"]
B = sorted([(s, m) for s, m in D["end"] if s in BORD], key=lambda x: BORD.index(x[0]))
assert len(B) == 8 and all(end_mark(s) == m for s, m in B)
C = [comma_item(s) for s in ["We need eggs, flour, milk and butter.", "However, the bus was late.", "Liam, are you coming?",
     "Yes, I'd love to come.", "Mr Byrne, our maths teacher, was off sick.", "We drove through Kerry, Clare and Galway.",
     "Thanks for the lift, Dad.", "Our dog, a tiny terrier, chased the fox."]]
Cq = [s.replace(",", "") for s in C]
Dl = [("do not", "don't"), ("it is", "it's"), ("we are", "we're"), ("cannot", "can't"), ("will not", "won't"), ("they are", "they're")]
for longf, sh in Dl: assert longf in EXP[sh]
E = [(one, n, thing) for one, many, n, thing, emo, the in D["own"] if (one, n) in
     [("dog", 1), ("dog", 2), ("child", 2), ("teacher", 1), ("woman", 2), ("player", 2)]]
assert len(E) == 6
def of(one, n, thing):
    who = ("one " + one) if n == 1 else (IRR.get(one, one + "s"))
    return f"the {thing} of the {who.replace('one ', '')}" + (" (one)" if n == 1 else "")
Eq = [(of(o, n, t), f"the {own(o, n)} {t}") for o, n, t in E]
F = [(s, a) for s, a, wr, why in D["short"] if s in ("The dog wagged ___ tail.", "___ going to win the cup.", "Is this ___ phone?",
                                                     "___ coming to the party?", "___ been a long day.", "The players left ___ boots outside.")]
assert len(F) == 6 and all(short_ok(s, a) for s, a in F)
CHI = next(i for i, (q, a) in enumerate(Eq) if "children" in a)
NQ = len(A) + len(B) + len(Cq) + len(Dl) + len(Eq) + len(F) + 2; assert NQ == 42, NQ
PASS_RAW = "last saturday orla and i cycled to blarney we brought sandwiches crisps and water orlas bike got a puncture so we walked home its a long way"
PASS_FIX = "Last Saturday, Orla and I cycled to Blarney. We brought sandwiches, crisps and water. Orla's bike got a puncture, so we walked home. It's a long way."
assert PASS_FIX.replace(",", "").replace(".", "").replace("'", "").lower() == PASS_RAW.replace("'", "")
assert comma_ok("We brought sandwiches, crisps and water.", "list", ["sandwiches", "crisps", "water"])

def qs(items): return "".join(f"<li>{q} <span class='line'></span></li>" for q in items)
def style(var):
    return re.search(var + r' = f"""<!doctype.*?<style>(.*?)</style>', open(os.path.join(SRC, "build_money1_pdfs.py"), encoding="utf-8").read(), re.S).group(1).replace("{LO}", LO).replace("{{", "{").replace("}}", "}").replace("JC Maths LOs (2018 spec)", "JC English LOs (2015 spec)")
SHEET_STYLE = style("sheet"); PACK_STYLE = style("pack")
assert "JC English LOs (2015 spec)" in SHEET_STYLE and "Single-teacher licence" in PACK_STYLE and "JC English LOs (2015 spec)" in PACK_STYLE
EXTRA = """.wk{line-height:1.45;border:1.5px solid var(--line);border-radius:8px;padding:2px 7px;margin:3px 0;font-size:9.4pt}.wk b.h{display:block}
table.st{border-collapse:collapse;margin:3px 0;font-size:9.4pt;width:100%}table.st td,table.st th{border:1px solid #C9D1DA;padding:2px 6px;text-align:left}
.pass{border-left:4px solid var(--green);background:var(--mist);padding:5px 10px;margin:4px 0;font-style:italic}
.pu{color:#B03A2E;font-weight:800}"""
def pu(s): return re.sub(r"([,'?!])", r'<span class="pu">\1</span>', s)

sheet = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Punctuation 1: rules and practice | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{SHEET_STYLE}
{EXTRA}
</style></head><body>
<div class="page tight">
  <div class="band"><div><div class="k">Junior Cycle English · Free revision sheet</div><h1>Punctuation 1: capitals, full stops, commas, apostrophes</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2015 specification): {LO}. Play the game: <b>{GAME}</b></p>
  <div class="two">
   <div><h2>1. Capitals</h2>
    <table class="st"><tbody>
     <tr><td><b>Capital</b></td><td>the first word · I · names · places · days · months · languages · festivals: <i>On Monday, Aoife and I have French.</i></td></tr>
     <tr><td><b>No capital</b></td><td>seasons · most school subjects · mum/dad after my or our: <i>my mum loves summer and maths</i></td></tr></tbody></table>
    <h2>2. Full stops and end marks</h2>
    <table class="st"><tbody>
     <tr><td><b>.</b></td><td>ends a statement: <i>We missed the bus.</i></td></tr>
     <tr><td><b>?</b></td><td>ends a question: <i>Where is my phone?</i></td></tr>
     <tr><td><b>!</b></td><td>strong feeling: <i>What a goal!</i> <i>How kind you are!</i></td></tr></tbody></table>
    <div class="wk">A reported question takes a full stop: <i>She asked if I was hungry.</i><br>Two sentences need a full stop between them, not a comma.</div>
    <h2>3. Commas</h2>
    <table class="st"><tbody>
     <tr><td><b>Lists</b></td><td>eggs{pu(",")} milk and bread (no comma before the last “and”)</td></tr>
     <tr><td><b>Opening word</b></td><td>However{pu(",")} the bus was late.</td></tr>
     <tr><td><b>Names</b></td><td>Liam{pu(",")} are you coming? · Thanks{pu(",")} Dad.</td></tr>
     <tr><td><b>Yes / No / Well</b></td><td>Yes{pu(",")} I'd love to.</td></tr>
     <tr><td><b>Extra information</b></td><td>Mr Byrne{pu(",")} our maths teacher{pu(",")} was off sick.</td></tr></tbody></table></div>
   <div><h2>4. Apostrophes: missing letters</h2>
    <div class="wk">do not → don{pu("'")}t · it is / it has → it{pu("'")}s · we are → we{pu("'")}re<br>cannot → can{pu("'")}t · will not → won{pu("'")}t · they are → they{pu("'")}re</div>
    <p>The apostrophe goes <b>where the letters are missing</b>.</p>
    <h2>5. Apostrophes: belonging</h2>
    <p>Write the owner first, then add the apostrophe.</p>
    <table class="st"><tbody>
     <tr><td><b>One owner</b></td><td>add 's: the dog{pu("'")}s bone · Sarah{pu("'")}s phone</td></tr>
     <tr><td><b>More than one, ends in s</b></td><td>add ': the dogs{pu("'")} kennel · the girls{pu("'")} changing room</td></tr>
     <tr><td><b>More than one, no s</b></td><td>add 's: the children{pu("'")}s toys · the men{pu("'")}s team</td></tr></tbody></table>
    <h2>6. It's or its?</h2>
    <div class="wk">Say “it is” or “it has”. Works → <b>it's</b>. Doesn't → <b>its</b>.<br><i>It's raining. The cat licked its paw.</i><br>Same test: <b>you're / your</b> · <b>they're / their</b> · <b>who's / whose</b></div>
    <div class="note"><b>Classic mistakes:</b> no capital for I or names · a comma between two sentences · apostrophes in plurals (<s>apple's for sale</s>) · it's for its · “childrens'” (it's children's).</div></div>
  </div>
  <div class="tip"><b>Exam tip:</b> leave 3 minutes at the end of every writing answer to read it back for capitals, full stops and apostrophes.</div>
</div>

<div class="page p2">
  <div class="band"><div><div class="k">Practice · {NQ} questions</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Rewrite with capital letters</h2><ol class="q" style="columns:2;column-gap:8mm">{qs(Aq)}</ol>
  <h2>B. Add the end mark: . ? or !</h2><ol class="q" start="7" style="columns:2;column-gap:8mm">{qs(s for s, m in B)}</ol>
  <h2>C. Add the commas</h2><ol class="q" start="15" style="columns:2;column-gap:8mm">{qs(Cq)}</ol>
  <h2>D. Write the short form</h2><ol class="q" start="23" style="columns:3;column-gap:8mm">{qs(l for l, s in Dl)}</ol>
  <h2>E. Write it with an apostrophe</h2><ol class="q" start="29" style="columns:2;column-gap:8mm">{qs(q for q, a in Eq)}</ol>
  <h2>F. Fill the gap: it's/its, they're/their, you're/your, who's/whose</h2><ol class="q" start="35" style="columns:2;column-gap:8mm">{qs(s for s, a in F)}</ol>
  <h2>G. Exam-style</h2>
  <div class="pass">{PASS_RAW}</div>
  <ol class="q" start="{NQ - 1}">
   <li>Rewrite the passage with capitals, full stops, commas and apostrophes.<span class="long"></span><span class="long"></span></li>
   <li>Write two sentences about your weekend. Use a list with commas, one apostrophe of belonging and one question.<span class="long"></span></li>
  </ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">Check your work</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <table class="ans"><tbody>
   <tr><td><b>A</b></td><td>{" · ".join(f"{i}. {a}" for i, a in enumerate(A, 1))}</td></tr>
   <tr><td><b>B</b></td><td>{" · ".join(f"{i}. {s}<b>{m}</b> ({ {'?': 'question', '!': 'feeling', '.': 'statement'}[m] })" for i, (s, m) in enumerate(B, 7))}</td></tr>
   <tr><td><b>C</b></td><td>{" · ".join(f"{i}. {pu(a)}" for i, a in enumerate(C, 15))}</td></tr>
   <tr><td><b>D</b></td><td>{" · ".join(f"{i}. {pu(s)}" for i, (l, s) in enumerate(Dl, 23))}</td></tr>
   <tr><td><b>E</b></td><td>{" · ".join(f"{i}. {pu(a)}" for i, (q, a) in enumerate(Eq, 29))}</td></tr>
   <tr><td><b>F</b></td><td>{" · ".join(f"{i}. {pu(a)}" for i, (s, a) in enumerate(F, 35))}</td></tr>
   <tr><td><b>G</b></td><td>{NQ - 1}. {pu(PASS_FIX)} (The comma after “Last Saturday” and before “so” can be left out.)<br>{NQ}. Answers will vary, e.g. On Saturday we had pizza, chips and cake at Ben's house. Were you there?</td></tr>
  </tbody></table>
  <h2>Worked examples</h2>
  <div class="two">
   <div class="wk"><b class="h">11. How kind you are</b>“How” can start a question (How old is your brother?) or an exclamation. Here it's strong feeling, and the words aren't in question order (not “are you”), so <b>!</b></div>
   <div class="wk"><b class="h">12. Have you finished your homework</b>Starts with “Have you…” and asks something, so <b>?</b> Compare 13: “She asked if…” only reports a question, so <b>.</b></div>
   <div class="wk"><b class="h">{29 + CHI}. the children's toys</b>Owner first: children (already plural, no s). No s at the end → add 's: <b>children's</b>.</div>
   <div class="wk"><b class="h">35. The dog wagged its tail.</b>Try “it is”: “the dog wagged it is tail” makes no sense, so no apostrophe: <b>its</b>.</div>
  </div>
  <div class="note"><b>Got one wrong?</b> Find the rule on page 1, then play <b>Comma Catch</b> at {GAME}: the “Go back over these” list at the end shows the reason for each mistake.</div>
  <p class="small">All sentences written by Léim. Léim is independent and not connected with the State Examinations Commission or the NCCA.</p>
</div>
</body></html>"""
assert B[4][0].startswith("How kind") and B[5][0].startswith("Have you") and B[6][0].startswith("She asked"), B
assert Eq[CHI][1] == "the children's toys" and F[0][0].startswith("The dog wagged"), (Eq[2], F[0])

# ---------- teacher pack ----------
MATCH = [("on monday", "On Monday"), ("lisa and i", "Lisa and I"), ("eggs milk and bread", "eggs, milk and bread"), ("Yes I'll come.", "Yes, I'll come."),
         ("Thanks Dad.", "Thanks, Dad."), ("dont stop", "don't stop"), ("Its raining.", "It's raining."), ("The cat licked it's paw.", "The cat licked its paw."),
         ("the childrens' toys", "the children's toys"), ("Your late!", "You're late!"), ("Where are you.", "Where are you?"), ("apple's for sale", "apples for sale")]
assert len({a for q, a in MATCH}) == 12 and len({q for q, a in MATCH}) == 12
assert caps_ok("On Monday we meet.") and caps_ok("Lisa and I went.") and comma_ok("We need eggs, milk and bread.", "list", ["eggs", "milk", "bread"])
assert comma_ok("Yes, I'll come.", "yes", "Yes") and comma_ok("Thanks, Dad.", "address", "Dad") and end_mark("Where are you") == "?"
assert short_ok("___ raining.", "It's") and short_ok("The cat licked ___ paw.", "its") and short_ok("___ late!", "You're")
random.seed(103); order = list(range(24)); random.shuffle(order)
cards = [("q", i) for i in range(12)] + [("a", i) for i in range(12)]
match_print = [cards[k] for k in order]
match_html = "".join(f'<div class="c"><span class="tag">Card {k}</span><div class="fc{' sm' if len(MATCH[i][0 if t == 'q' else 1]) > 16 else ''}">{MATCH[i][1] if t == "a" else MATCH[i][0]}</div></div>' for k, (t, i) in enumerate(match_print, 1))
match_key = " · ".join(f"{match_print.index(('q', i)) + 1} → {match_print.index(('a', i)) + 1}" for i in range(12))

DICT_A = "On Saturday, Aoife's family drove to Kinsale. They bought chips, ice cream and a kite. It's always windy there. Did they get home before dark?"
DICT_B = "Last summer, Liam visited his cousins in Galway. They swam, played hurling and ate far too much. Liam's aunt has a dog called Rex. What a brilliant week!"
for s in DICT_A.split(". ") + DICT_B.split(". "): assert caps_ok(s.rstrip(".?!") + "."), s
assert comma_ok("They bought chips, ice cream and a kite.", "list", ["chips", "ice cream", "a kite"]) and comma_ok("They swam, played hurling and ate far too much.", "list", ["swam", "played hurling", "ate far too much"])
assert end_mark("Did they get home before dark") == "?" and end_mark("What a brilliant week") == "!"
def dict_card(who, mine, other):
    return f'''<div class="idc"><h3>Student {who} · Dictation Swap</h3><div class="two"><div><p style="font-size:8.8pt;margin:0 0 1mm"><b>1. Read this to your partner</b>, slowly, twice. Don't say the punctuation: pause at each comma, stop at each full stop.</p><p style="font-size:10pt;margin:0;line-height:1.45">{pu(mine)}</p></div>
<div><p style="font-size:8.8pt;margin:0 0 1mm"><b>2. Write your partner's text here.</b> Add every capital, comma, apostrophe and end mark. Then check with their card.</p>{'<span class="gap"></span>' * 6}</div></div></div>'''

# Punctuation Dominoes: 20 clues, 20 different answers, each worked out by the rules above
DOMS = [("Short form: do not", "don't"), ("Short form: cannot", "can't"), ("Short form: will not", "won't"), ("Short form: it is", "it's"),
        ("Short form: we are", "we're"), ("Short form: they are", "they're"), ("Short form: I am", "I'm"), ("Short form: she is", "she's"),
        ("Belonging to one dog: the ___ bone", "dog's"), ("Belonging to two dogs: the ___ kennel", "dogs'"), ("Belonging to the children: the ___ toys", "children's"),
        ("Belonging to the men: the ___ team", "men's"), ("Belonging to one teacher: the ___ desk", "teacher's"), ("Belonging to all the teachers: the ___ car park", "teachers'"),
        ("Belonging to the women: the ___ final", "women's"), ("Belonging to one cat: the ___ bowl", "cat's"),
        ("End mark: What a goal_", "!"), ("End mark: Where is my bag_", "?"), ("End mark: She asked if I was hungry_", "."), ("Between list items: eggs_ milk and bread", ",")]
EXP2 = dict(EXP, **{"i'm": ["i am"]})
for c, a in DOMS:
    if c.startswith("Short form: "): assert c[12:].lower() in EXP2[a.lower()], c
    elif c.startswith("Belonging"):
        m = re.match(r"Belonging to (one |two |all the |the )(\w+)", c); w = m.group(2); n = 1 if m.group(1) == "one " else 2
        one = {v: k for k, v in IRR.items()}.get(w, w.rstrip("s") if n == 2 else w); assert own(one, n) == a, (c, a, own(one, n))
    elif c.startswith("End mark"): assert end_mark(c[10:-1]) == a, c
    else: assert comma_ok("We need eggs, milk and bread.", "list", ["eggs", "milk", "bread"]) and a == ","
assert len(DOMS) == 20 and len({a for c, a in DOMS}) == 20
random.seed(1003); chain = DOMS[:]; random.shuffle(chain)
dom = [("START" if k == 0 else chain[k - 1][1], x[0]) for k, x in enumerate(chain)] + [(chain[-1][1], "FINISH")]
dom_print = dom[:]; random.shuffle(dom_print)
NAMEP = {"!": "! (exclamation mark)", "?": "? (question mark)", ".": ". (full stop)", ",": ", (comma)"}
dom_html = "".join(f'<div class="dom"><div class="h l{" sm" if len(NAMEP.get(l, l)) > 8 else ""}">{pu(NAMEP.get(l, l)) if l not in ("START",) else l}</div><div class="h r">{r}</div></div>' for l, r in dom_print)
chain_key = "".join(f"<li>{c}: <b>{pu(NAMEP.get(a, a))}</b></li>" for c, a in chain)

ERR = [("My <b>brothers</b> bike is red. (one brother)", "One owner: add 's → <b>brother's</b> bike"),
       ("<b>Whose</b> coming to the match?", "Who is coming → <b>Who's</b>"),
       ("The match starts at six<b>?</b>", "A statement, not a question → full stop: <b>six.</b>"),
       ("<b>Their</b> going to win.", "They are going → <b>They're</b>"),
       ("We need <b>bread milk and eggs</b>.", "List commas → <b>bread, milk and eggs</b>"),
       ("I love <b>Summer</b>.", "Seasons take no capital → <b>summer</b>")]
assert own("brother", 1) == "brother's" and short_ok("___ coming to the match?", "Who's") and short_ok("___ going to win.", "They're") and end_mark("The match starts at six") == "."
assert comma_ok("We need bread, milk and eggs.", "list", ["bread", "milk", "eggs"]) and caps_ok("I love summer.") and not caps_ok("I love Summer.")
WS_RAW = "my friend niamh lives in cork her house is beside the river lee on fridays we play football eat pizza and watch films niamhs dog sleeps on the sofa its huge"
WS_FIX = "My friend Niamh lives in Cork. Her house is beside the River Lee. On Fridays we play football, eat pizza and watch films. Niamh's dog sleeps on the sofa. It's huge."
assert WS_FIX.replace(",", "").replace(".", "").replace("'", "").lower() == WS_RAW.replace("'", "")
for s in WS_FIX.split(". "): assert caps_ok(s.rstrip(".") + "."), s

pack = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Punctuation 1 Teacher Pack | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{PACK_STYLE}
{EXTRA}
.fym .c{{height:13.6mm}}.fym .fc{{font-size:12pt}}.fym .fc.sm{{font-size:9.6pt;line-height:1.2}}.idc{{padding:1.5mm 4mm}}.idc h3{{margin:0 0 1mm}}.idc .gap{{display:block;border-bottom:1px solid #9AA3AE;height:17px}}
.dom .r{{font-size:8.8pt;line-height:1.25}}.dom .l{{font-size:15pt}}.dom .l.sm{{font-size:11pt}}.p1 .proc td{{font-size:8.6pt;padding:2px 6px}}
.ops div{{font-size:12pt;padding:4mm 3mm}}.ops b{{font-size:18pt}}.pass{{font-size:10pt}}
</style></head><body>

<div class="page p1">
  <div class="band"><div><div class="k">Junior Cycle English · Teacher pack</div><h1>Punctuation 1</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2015 specification): {LO}</p>
  <div class="two">
    <div><h3>Aims</h3><p>By the end of the lesson students can use capitals, full stops, question and exclamation marks correctly, put commas in lists, after opening words, around extra information and around names, and use apostrophes for missing letters and belonging (including its / it's).</p></div>
    <div><h3>In this pack</h3><p>p.1 Teacher notes · p.2 Fix-It Match mingle cards + Dictation Swap A/B cards · p.3 Punctuation Dominoes (cut-up) · p.4 Wall poster · p.5 Worksheet: Error Hunt + exam-style questions · p.6 Answers. Level: 1st year (useful revision in 2nd and 3rd). Time: about 60 minutes. All sentences are original.</p></div>
  </div>
  <h2 style="margin-top:8px">Procedure</h2>
  <table class="proc"><tbody>
    <tr><td>5 min</td><td><b>Lead-in.</b> Board two lines: “Let's eat, Grandad.” / “Let's eat Grandad.” What's the difference? Elicit that punctuation changes meaning.</td></tr>
    <tr><td>8 min</td><td><b>Guided discovery.</b> Board “the dog's bone / the dogs' bone / the children's toys”. Pairs: how many owners in each? What's the rule? Then the it is test for its / it's. Quick board review of capitals and the five comma uses.</td></tr>
    <tr><td>10 min</td><td><b>Fix-It Match mingle</b> (p.2, 24 cards = 12 mistakes + 12 corrected versions; one card each). Find your partner, then tell them the rule. Feedback: which rule caught most pairs?</td></tr>
    <tr><td>12 min</td><td><b>Dictation Swap</b> (p.2, pairs, don't show your card). A reads their text aloud twice, pausing at commas; B writes it with all the punctuation. Swap. Pairs compare with the original and score one point per mark.</td></tr>
    <tr><td>10 min</td><td><b>Punctuation Dominoes</b> (p.3), groups of 3–4. Start with START, work out the answer to the clue, find the domino with that answer on its left. Build the chain to FINISH.</td></tr>
    <tr><td>12 min</td><td><b>Worksheet</b> (p.5). Error Hunt in pairs, then the exam-style questions alone.</td></tr>
    <tr><td>3 min</td><td><b>Exit ticket.</b> “its the girls first match” (many girls) → It's the girls' first match. Homework: play <b>Comma Catch</b> at {GAME}.</td></tr>
  </tbody></table>
  <div class="note"><b>Mingle key</b> (mistake card → corrected card): {match_key}.<br>
  <b>Errors to look for:</b> comma between two sentences · apostrophes in plurals · “childrens'” · it's / its, your / you're · lower-case i and names. <b>Support:</b> the poster (p.4) on the desk. <b>Fast finishers:</b> write one sentence that uses all five comma rules.</div>
  <p class="small"><b>Domino answer chain</b> (START → FINISH):</p>
  <ol class="small" style="columns:2;column-gap:12px;font-size:7.4pt;line-height:1.22;margin:0;padding-left:16px">{chain_key}</ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">Cut up the cards · one Dictation card per student</div><h1>Fix-It Match + Dictation Swap</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:8.8pt;margin:0"><b>Fix-It Match mingle.</b> Cut out the 24 cards and give one to each student. Mistake card? Find the corrected version. Corrected card? Find the mistake it fixes. (Fewer students? Take out whole pairs.)</p>
  <div class="fym">{match_html}</div>
  <p style="font-size:8.8pt;margin:3mm 0 0"><b>Dictation Swap.</b> Don't show your card. Read, listen, write, then compare.</p>
  {dict_card("A", DICT_A, DICT_B)}
  {dict_card("B", DICT_B, DICT_A)}
</div>

<div class="page">
  <div class="band"><div><div class="k">Groups of 3–4 · cut along the dashed lines</div><h1>Punctuation Dominoes</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.4pt">Start with START. Work out the answer to the clue on the right, then find the domino with that answer on its left. Keep going until you reach FINISH.</p>
  <div class="doms">{dom_html}</div>
</div>

<div class="page">
  <div class="poster">
    <h1>Punctuation power</h1>
    <div class="ops">
      <div style="background:var(--green-soft)"><b>Capitals</b>first word · I · names · places · days · months · languages<br><i>not seasons or most subjects</i></div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>. ? !</b>statement · question · strong feeling<br><i>What a goal!</i></div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Commas</b>lists · opening word · names · Yes/No · extra info<br><i>eggs, milk and bread</i></div>
      <div style="background:var(--green-soft)"><b>Missing letters</b><i>don't · it's · we're · can't</i></div>
      <div style="background:var(--green-soft)"><b>Belonging</b>one: dog's · many: dogs'<br><i>children's · men's</i></div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>It's or its?</b>say “it is”<br><i>works → it's · not → its</i></div>
    </div>
    <p style="text-align:center;font-size:20pt!important;font-weight:800;margin:4mm 0">Let's eat, Grandad! (not: Let's eat Grandad!)</p>
    <p style="text-align:center;font-size:10pt;color:var(--muted)">Léim · leim.ie · Play Comma Catch: {GAME}</p>
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
    <li>Rewrite the passage with capitals, full stops, commas and apostrophes.<span class="long"></span><span class="long"></span><span class="long"></span></li>
    <li>Why does “niamhs” need an apostrophe? Where does it go?<span class="long"></span></li>
    <li>“its huge”: it's or its? Explain how you decided.<span class="long"></span></li>
    <li>Write a question you would ask Niamh about her dog. Use the right end mark.<span class="long"></span></li>
    <li>Write one sentence about something that belongs to two or more of your friends. Use an apostrophe.<span class="long"></span></li>
  </ol>
</div>

<div class="page an">
  <div class="band"><div><div class="k">For the teacher</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>Fix-It Match</h2>
  <p>{" · ".join(f"{q} → <b>{pu(a)}</b>" for q, a in MATCH)}</p>
  <h2>Dictation Swap</h2>
  <p>Compare with the original card: one point per capital, comma, apostrophe and end mark (A: {sum(DICT_A.count(c) for c in ",'.?") + sum(1 for w in re.findall(r"[A-Z]", DICT_A))} · B: {sum(DICT_B.count(c) for c in ",'.?!") + sum(1 for w in re.findall(r"[A-Z]", DICT_B))}). Accept a comma or no comma after the opening phrase.</p>
  <h2>A. Error Hunt</h2>
  <table><tbody>{"".join(f"<tr><td style='width:40%'>{s}</td><td>{r}</td></tr>" for s, r in ERR)}</tbody></table>
  <h2>B. Exam-style questions</h2>
  <ol class="q">
    <li>{pu(WS_FIX)} (A comma after “On Fridays” is fine too.)</li>
    <li>The dog belongs to Niamh (one owner), so add 's: <b>Niamh's</b> dog.</li>
    <li><b>It's</b>: “it is huge” makes sense, so it's the short form.</li>
    <li>e.g. What is your dog's name<b>?</b> (capital at the start, question mark at the end)</li>
    <li>e.g. My friends' bikes were locked outside. (more than one friend → friends')</li>
  </ol>
  <h2>Marking tip</h2>
  <p>In students' own writing, punctuation is part of accuracy: look first for full stops between sentences and capitals for names and I, then apostrophes. A paragraph of comma-joined sentences is harder to follow and loses more than a single missing comma.</p>
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
<h1><span>Punctuation 1</span></h1>
<div class="sub">Capitals · full stops · commas · apostrophes<br>Fix-It Match · Dictation Swap A/B · Dominoes<br>Poster · Worksheet + answers</div>
<div class="em">dog's · dogs' · it's · its</div></div>
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
    pdf("teacher-pack", os.path.join(OUT, "Punctuation-1-Teacher-Pack-Leim.pdf"))
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--hide-scrollbars", "--window-size=1200,1200",
                    f"--screenshot={os.path.join(OUT, f'{SLUG}-cover.png')}", f"{SLUG}-cover.html"], cwd=SRC, check=True, capture_output=True)
    print("domino chain:", [a for c, a in chain])
