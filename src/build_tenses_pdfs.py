#!/usr/bin/env python3
"""Grammar 2: tenses, agreement & pronouns (JC English Order 17): free sheet (-> printables/), 6-page teacher pack + 1200x1200 cover (-> OUTDIR).
Usage: python3 src/build_tenses_pdfs.py /tmp/tenses
Items come from the game's data block (tense-trap.html). Every answer is re-derived with the checker's own rules
(src/test_tense_trap.py: tense_item, cue, slip, number, irr_form, role) and asserted; the checker's data pass runs first.
Styles are read from src/build_money1_pdfs.py."""
import os, sys, random, subprocess, re
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC); sys.path.insert(0, SRC)
from test_tense_trap import tense_item, cue, slip, number, irr_form, role, IRR, SUBJ, OBJ, load, data_pass
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/tenses"; os.makedirs(OUT, exist_ok=True)
SLUG = "tenses-agreement-pronouns"
LO = "W10, W12, OL12"
GAME = "leim.ie/tense-trap.html"
D = load(os.path.join(ROOT, "tense-trap.html")); assert not data_pass(D), data_pass(D)
TN = {"pa": "past", "pr": "present", "fu": "future"}
PAST = {"opened": "opened", "sees": "saw", "finds": "found", "kicks": "kicked", "tells": "told", "creeps": "crept", "forget": "forgot",
        "rises": "rose", "takes": "took", "race": "raced", "shouts": "shouted", "says": "said", "see": "saw", "look": "looked",
        "picks": "picked", "knocks": "knocked", "switch": "switched", "hears": "heard", "grabs": "grabbed", "is": "was", "laughs": "laughed",
        "runs": "ran", "drops": "dropped", "comes": "came", "wakes": "woke"}
def slipped(s): return [x for x, tg, m in slip(s) if m][0]
def plain(s): return re.sub(r"[{}*]", "", s)

# ---------- free sheet ----------
random.seed(1717)
A_items = [x for k in TN for x in random.sample([y for y in D["tense"] if cue(y[0]) == k], 2)]; random.shuffle(A_items)
for s, a, w in A_items: assert not tense_item(s, a, w)
B_items = random.sample(D["slip"], 3)
for s in B_items: assert slipped(s) in PAST
C_items = random.sample(D["agree"], 8)
for s, a, w in C_items: assert (number(s) == "s") == a.endswith("s")
E_items = random.sample(D["irr"], 8)
E_ans = [irr_form(s, b)[0] for s, b in E_items]
F_items = random.sample(D["pron"], 6)
for s, k, a in F_items: assert (SUBJ if role(s) == "subj" else OBJ)[k] == a
NQ = len(A_items) + len(B_items) + len(C_items) + len(E_items) + len(F_items) + 2; assert NQ == 33, NQ
nA = 1; nB = nA + len(A_items); nC = nB + len(B_items); nE = nC + len(C_items); nF = nE + len(E_items); nG = nF + len(F_items)

def style(var):
    return re.search(var + r' = f"""<!doctype.*?<style>(.*?)</style>', open(os.path.join(SRC, "build_money1_pdfs.py"), encoding="utf-8").read(), re.S).group(1).replace("{LO}", LO).replace("{{", "{").replace("}}", "}").replace("JC Maths LOs (2018 spec)", "JC English LOs (2015 spec)")
SHEET_STYLE = style("sheet"); PACK_STYLE = style("pack")
assert "JC English LOs (2015 spec)" in SHEET_STYLE and "Single-teacher licence" in PACK_STYLE and "JC English LOs (2015 spec)" in PACK_STYLE
EXTRA = """.wk{line-height:1.45;border:1.5px solid var(--line);border-radius:8px;padding:2px 7px;margin:3px 0;font-size:9.4pt}.wk b.h{display:block}
table.st{border-collapse:collapse;margin:3px 0;font-size:9.2pt;width:100%}table.st td,table.st th{border:1px solid #C9D1DA;padding:2px 6px;text-align:left}
.pass{border-left:4px solid var(--green);background:var(--mist);padding:5px 10px;margin:4px 0;font-style:italic}"""


def base(a, w): return [x for x in [a] + w if x.startswith("will ")][0][5:]
A_html = "".join(f"<li value='{i}'>{s.replace('___', '<span class=\"line\" style=\"min-width:22mm\"></span>')} <span class='small'>({base(a, w)})</span></li>" for i, (s, a, w) in enumerate(A_items, nA))
B_html = "".join(f"<li value='{i}'><i>{plain(s)}</i><br>slipped verb: <span class='line' style='min-width:20mm'></span> → <span class='line' style='min-width:20mm'></span></li>" for i, s in enumerate(B_items, nB))
C_html = "".join(f"<li value='{i}'>{s.replace('___', '(' + ' / '.join(sorted([a, w], key=lambda x: not x.endswith('s'))) + ')')}</li>" for i, (s, a, w) in enumerate(C_items, nC))
E_html = "".join(f"<li value='{i}'>{s.replace('___', '<span class=\"line\" style=\"min-width:18mm\"></span>')} <span class='small'>({b})</span></li>" for i, (s, b) in enumerate(E_items, nE))
F_html = "".join(f"<li value='{i}'>{s.replace('___', '(' + SUBJ[k] + ' / ' + OBJ[k] + ')')}</li>" for i, (s, k, a) in enumerate(F_items, nF))
for s, a, w in A_items: assert base(a, w) != a, (s, a)

EX1 = "The bell {rang} and everyone {*runs} outside. Aoife {grabbed} her coat and {*drops} her phone. It {*is} smashed."
v = slip(EX1); assert [x for x, tg, m in v if m] == [x for x, tg, m in v if tg in ("VBZ", "VBP")] == ["runs", "drops", "is"], v
EX2 = [("My friends and me is going to the cinema.", "My friends and I are going to the cinema."), ("I seen it last week.", "I saw it last week.")]
assert number("My friends and I ___ going to the cinema.") == "p" and role("My friends and ___ are going to the cinema.") == "subj" and irr_form("I ___ it last week.", "see")[0] == "saw"

sheet = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Tenses, agreement and pronouns, rules and practice | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{SHEET_STYLE}
{EXTRA}
.p2 ol.q li{{margin-bottom:1px;font-size:9pt}}.p2 h2{{margin:4px 0 2px}}.p2 .two{{gap:5mm}}.small{{color:var(--muted);font-size:8.6pt}}
</style></head><body>
<div class="page tight">
  <div class="band"><div><div class="k">Junior Cycle English · Free revision sheet</div><h1>Tenses, agreement and pronouns</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2015 specification): {LO}. Play the game: <b>{GAME}</b></p>
  <div class="two">
   <div><h2>1. The time word decides the tense</h2>
    <table class="st"><thead><tr><th>Time words</th><th>Tense</th><th>Example</th></tr></thead><tbody>
     <tr><td>yesterday, last week, two years ago</td><td>past</td><td>I <b>walked</b> to school.</td></tr>
     <tr><td>every day, always, usually, often</td><td>present</td><td>Gran <b>walks</b> to Mass.</td></tr>
     <tr><td>tomorrow, next year, soon</td><td>future</td><td>I <b>will walk</b> to school.</td></tr></tbody></table>
    <h2>2. Keep it steady</h2>
    <p style="font-size:9.4pt">A story in the past stays in the past. Check every verb when you read your work back.</p>
    <div class="wk"><i>I opened the door and <s>see</s> <b>saw</b> a fox.</i></div>
    <h2>3. Make it agree</h2>
    <table class="st"><thead><tr><th>Singular → is, was, has, plays</th><th>Plural → are, were, have, play</th></tr></thead><tbody>
     <tr><td>each, every, everyone, nobody</td><td>Tom <b>and</b> Aoife</td></tr>
     <tr><td><b>one</b> of my friends</td><td>the players, my shoes</td></tr>
     <tr><td>the <b>box</b> of apples</td><td>there <b>are</b> three dogs</td></tr></tbody></table></div>
   <div><h2>4. Saw or seen?</h2>
    <table class="st"><thead><tr><th>Verb</th><th>No helper</th><th>After has / have / had / was</th></tr></thead><tbody>
     {"".join(f"<tr><td>{b}</td><td>{IRR[b][0]}</td><td>{IRR[b][1]}</td></tr>" for b in ["see", "do", "go", "write", "break", "eat", "give", "ring"])}</tbody></table>
    <p style="font-size:9pt">“I seen it” and “I done it” are common in spoken Irish English. In standard written English (and in the exam) write <i>I saw it</i>, <i>I did it</i>.</p>
    <h2>5. I or me?</h2>
    <table class="st"><thead><tr><th>Doing it</th><th>Getting it</th></tr></thead><tbody>
     <tr><td>I · he · she · we · they</td><td>me · him · her · us · them</td></tr>
     <tr><td>Tom and <b>I</b> went.</td><td>The coach picked Tom and <b>me</b>.</td></tr></tbody></table>
    <div class="note"><b>The test:</b> take away the other person. “picked Tom and I” → “picked I”? No: “picked <b>me</b>”.</div>
    <p style="font-size:9pt"><b>Clear pronouns:</b> if “she” could mean two people, use a name.</p></div>
  </div>
  <div class="tip"><b>Exam tip:</b> there is no separate grammar question, but every writing answer is marked partly on accuracy. Save two minutes to read your answer back and check every verb and pronoun.</div>
</div>

<div class="page p2">
  <div class="band"><div><div class="k">Practice · {NQ} questions</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <div class="two"><div><h2>A. Circle the time word, then fill the gap</h2><ol class="q">{A_html}</ol>
  <h2>C. Circle the verb that agrees</h2><ol class="q">{C_html}</ol></div>
  <div><h2>D. Saw or seen? Use the verb in brackets</h2><ol class="q">{E_html}</ol>
  <h2>E. I or me? Circle one</h2><ol class="q">{F_html}</ol></div></div>
  <h2>B. Each story is in the past, but one verb slipped. Find it and correct it</h2><ol class="q">{B_html}</ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">Exam-style + answers</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <h2>F. Exam-style</h2>
  <ol class="q">
   <li value="{nG}">Rewrite this so every verb is in the past: <i>“{plain(EX1)}”</i><span class="long"></span><span class="long"></span></li>
   <li value="{nG + 1}">Correct the mistakes: (a) <i>{EX2[0][0]}</i> (b) <i>{EX2[1][0]}</i> Explain each fix in a few words.<span class="long"></span><span class="long"></span></li>
  </ol>
  <h2>Answers</h2>
  <table class="ans"><tbody>
   <tr><td><b>A</b></td><td>{" · ".join(f"{i}. {a} ({TN[cue(s)]})" for i, (s, a, w) in enumerate(A_items, nA))}</td></tr>
   <tr><td><b>B</b></td><td>{" · ".join(f"{i}. {slipped(s)} → {PAST[slipped(s)]}" for i, s in enumerate(B_items, nB))}</td></tr>
   <tr><td><b>C</b></td><td>{" · ".join(f"{i}. {a}" for i, (s, a, w) in enumerate(C_items, nC))}</td></tr>
   <tr><td><b>D</b></td><td>{" · ".join(f"{i}. {x}" for i, x in enumerate(E_ans, nE))}</td></tr>
   <tr><td><b>E</b></td><td>{" · ".join(f"{i}. {a}" for i, (s, k, a) in enumerate(F_items, nF))}</td></tr>
   <tr><td><b>F</b></td><td>{nG}. <i>The bell rang and everyone <b>ran</b> outside. Aoife grabbed her coat and <b>dropped</b> her phone. It <b>was</b> smashed.</i><br>
     {nG + 1}. (a) <i>{EX2[0][1]}</i> (“I” because it is doing the going; “are” because two people is plural; putting yourself last is good manners.) (b) <i>{EX2[1][1]}</i> (no helper verb, so “saw”; “seen” needs has / have.)</td></tr>
  </tbody></table>
  <div class="note"><b>Got one wrong?</b> Go back to page 1, then play <b>Tense Trap</b> at {GAME}: the "Go back over these" list at the end explains each mistake.</div>
  <p class="small">All sentences written by Léim; names and places are made up. Léim is independent and not connected with the State Examinations Commission or the NCCA.</p>
</div>
</body></html>"""

# ---------- teacher pack ----------
random.seed(1718)
TM = [x for k in TN for x in random.sample([y for y in D["tense"] if cue(y[0]) == k], 4)]
for s, a, w in TM: assert not tense_item(s, a, w)
assert len({a for s, a, w in TM}) == 12
CARDS = [("s", s, a) for s, a, w in TM] + [("v", a, s) for s, a, w in TM]
order = list(range(24)); random.shuffle(order); CS = [CARDS[i] for i in order]
tm_html = "".join(f'<div class="c"><span class="tag">{"Sentence" if k == "s" else "Verb"} · Card {i}</span><div class="fc {"sm" if k == "s" else ""}">{t.replace("___", "______") if k == "s" else t}</div></div>' for i, (k, t, m) in enumerate(CS, 1))
tm_key = " · ".join(f"{CS.index(c) + 1} ↔ {[j for j, d in enumerate(CS, 1) if d[0] == 'v' and d[1] == c[2]][0]} ({TN[cue(c[1])][:2]})" for c in CS if c[0] == "s")

# Slip Detective: each student reads a past story with 3 slipped verbs; the partner shouts "Slip!" and corrects it
STA = ("The Lost Kayak", ["Last summer Cian {hired} a kayak at Lough Hyne.", "He {paddled} out to the middle and the wind {*picks} up.",
       "A wave {tipped} him in and the kayak {*drifts} away.", "He {struggled} back to the shore and {*tells} the man at the hut.", "Together they {rowed} out and {found} it."])
STB = ("The Talent Show", ["Last Friday Orla {entered} the school talent show.", "She {waited} backstage and her hands {*shake}.",
       "When her name {came}, she {*walks} out and {started} to sing.", "The hall {went} quiet and then everyone {*claps}.", "She {won} second prize."])
PAST.update({"picks": "picked", "drifts": "drifted", "tells": "told", "shake": "shook", "walks": "walked", "claps": "clapped"})
def story_check(lines):
    sl = []
    for ln in lines:
        v = slip(ln)
        for x, tg, m in v:
            assert (tg in ("VBZ", "VBP")) == m and (m or tg == "VBD"), (ln, v)
            if m: sl.append(x)
    return sl
SLA = story_check(STA[1]); SLB = story_check(STB[1]); assert len(SLA) == len(SLB) == 3
def swap_card(who, mine, theirs):
    t, lines = mine; ot, olines = theirs
    other_bases = [(x, PAST[x]) for x in story_check(olines)]
    return f"""<div class="idc"><h3>Student {who} · Slip Detective</h3>
    <p style="font-size:8.8pt;margin:0 0 1mm"><b>1. Read</b> your story “{t}” aloud, slowly. It's in the past, but <b>3 verbs slipped</b> into the present (underlined). Read them as they are! Your partner says <b>“Slip!”</b> and gives the past form. Tick each one they catch.</p>
    <div class="pass" style="font-style:normal">{" ".join(re.sub(r"\{\*([^}]+)\}", r"<u>\1</u> ☐", re.sub(r"\{([^*][^}]*)\}", r"\1", l)) for l in lines)}</div>
    <p style="font-size:8.8pt;margin:1mm 0"><b>2. Listen</b> to your partner's story “{ot}”. Say “Slip!” when you hear a verb in the present. Write the past forms here:</p>
    <table class="st" style="font-size:9pt"><tbody><tr>{"".join("<td style='height:7mm'></td>" for _ in other_bases)}</tr></tbody></table>
    <p style="font-size:8.8pt;margin:1mm 0 0"><b>3. Together:</b> retell both stories in the past without looking.</p></div>"""

FIX = [("Me and Ciara was late for the bus.", "<b>Ciara and I were</b> late for the bus. (I = subject; two people = plural)"),
       ("Each of the players have a new jersey.", "Each of the players <b>has</b> a new jersey. (each = singular)"),
       ("We done the project last week.", "We <b>did</b> the project last week. (no helper verb → did)"),
       ("Yesterday I walk to the shop and buy milk.", "Yesterday I <b>walked</b> to the shop and <b>bought</b> milk. (yesterday → past)"),
       ("The teacher gave Seán and I a merit.", "The teacher gave Seán and <b>me</b> a merit. (take away Seán: gave me)"),
       ("There is three cakes left.", "There <b>are</b> three cakes left. (three cakes = plural)")]
assert role("Ciara and ___ were late for the bus.") == "subj" and number("Ciara and I ___ late for the bus.") == "p"
assert number("Each of the players ___ a new jersey.") == "s" and irr_form("We ___ the project last week.", "do")[0] == "did"
assert role("The teacher gave Seán and ___ a merit.") == "obj" and number("There ___ three cakes left.") == "p"
assert not tense_item("Yesterday I ___ to the shop.", "walked", ["walk", "will walk"])

PASS = ("The Cliff Walk", ["Last Sunday Fiona and me {*walk} the cliff path at Ballycotton.",
        "The sea was rough and the wind {*blows} so hard that each of us {*were} holding the rail.",
        "Halfway along, we {seen} a seal on the rocks below.", "Fiona {took} a photo and {*sends} it to Gran, who {loved} it."])
PASS_FIX = ["me → I (subject: take away Fiona: “I walked”)", "walk → walked (Last Sunday → past)", "blows → blew (keep the past)",
            "were → was (each of us = singular)", "seen → saw (no helper verb)", "sends → sent (keep the past)"]
assert role("Last Sunday Fiona and ___ walked the cliff path at Ballycotton.") == "subj"
assert number("each of us ___ holding the rail.".capitalize()) == "s" and irr_form("Halfway along, we ___ a seal on the rocks below.", "see")[0] == "saw"
assert not tense_item("Last Sunday we ___ the cliff path.", "walked", ["walk", "will walk"])
pass_html = " ".join(re.sub(r"\{\*?([^}]+)\}", r"\1", l) for l in PASS[1])

pack = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Tenses, Agreement and Pronouns Teacher Pack | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{PACK_STYLE}
{EXTRA}
.fym .c{{height:30mm}}.fym .fc{{font-size:13pt;margin-top:3mm}}.fym .fc.sm{{font-size:9.6pt;line-height:1.3;margin-top:2mm;font-weight:500}}.idc{{padding:2mm 4mm;margin-bottom:3mm}}.idc h3{{margin:0 0 1mm}}
.idc .st td{{padding:1px 6px}}.idc .pass{{font-size:9.6pt;line-height:1.5}}.p1 .proc td{{font-size:8.6pt;padding:2px 6px}}.ops div{{font-size:12pt;padding:5mm 3mm}}.ops b{{font-size:19pt}}
.ws .eh td{{font-size:8.8pt;padding:2px 6px}}.ws .eh .gap{{height:13px}}.ws ol.q li{{margin-bottom:1px}}.ws .pass{{font-size:9.4pt}}
</style></head><body>

<div class="page p1">
  <div class="band"><div><div class="k">Junior Cycle English · Teacher pack</div><h1>Tenses, agreement and pronouns</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2015 specification): {LO}</p>
  <div class="two">
    <div><h3>Aims</h3><p>By the end of the lesson students can use time words to choose the past, present or future, keep a story in one tense, make verbs agree with tricky subjects (each, one of, and), use the past and past participle of common irregular verbs, and choose I or me.</p></div>
    <div><h3>In this pack</h3><p>p.1 Teacher notes · p.2 Time Match cards (cut-up) · p.3 Slip Detective A/B (speaking) · p.4 Wall poster · p.5 Worksheet: Fix the Sentence + exam-style questions · p.6 Answers. Level: 2nd year. Time: about 60 minutes. All texts are original; names and places are made up.</p></div>
  </div>
  <h2 style="margin-top:8px">Procedure</h2>
  <table class="proc"><tbody>
    <tr><td>5 min</td><td><b>Lead-in.</b> Write “Yesterday I seen a fox.” Is it OK? Where would you hear it? Where would you not write it? Elicit spoken Irish English vs standard written English.</td></tr>
    <tr><td>8 min</td><td><b>Guided discovery.</b> Show “Yesterday I walked / Every day I walk / Tomorrow I will walk / Every day Gran walks / Every day my cousins walk”. Which word tells you the time? When does the verb get an -s? Elicit the rules (poster, p.4).</td></tr>
    <tr><td>10 min</td><td><b>Time Match</b> (p.2, groups of 3, one set of 24 cards). Match each sentence to the verb that fits its time word. Then sort the pairs into past, present and future.</td></tr>
    <tr><td>12 min</td><td><b>Slip Detective</b> (p.3, pairs). A reads a past story with 3 slipped verbs; B shouts “Slip!” and gives the past form. Swap. Then retell both stories in the past.</td></tr>
    <tr><td>20 min</td><td><b>Worksheet</b> (p.5). Fix the Sentence in pairs, then the exam-style questions on “{PASS[0]}” alone.</td></tr>
    <tr><td>5 min</td><td><b>Exit ticket.</b> Write three sentences about last weekend with one “Each of…”, one “…and I” and one “have + seen / done / gone”. Homework: play <b>Tense Trap</b> at {GAME}.</td></tr>
  </tbody></table>
  <div class="note"><b>Errors to look for:</b> drifting into the present in a past story · “each of them have”, “one of my friends play” · “I seen / I done / we was” · “Me and him went” · “between you and I” · a “he” that could mean two people. <b>Note:</b> treat “I seen” and “youse” as spoken Irish English, not as “wrong English”; the point is choosing standard English for writing. <b>Support:</b> the poster (p.4) on the desk. <b>Fast finishers:</b> write a 5-line story about a storm with no tense slips.</div>
</div>

<div class="page">
  <div class="band"><div><div class="k">Groups of 3 · cut up the 24 cards</div><h1>Time Match</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.4pt;margin:0 0 2mm">There are 12 <b>sentence</b> cards and 12 <b>verb</b> cards. Find the time word in each sentence, then match it to the verb that fits. Sort your pairs into <b>past</b>, <b>present</b> and <b>future</b>.</p>
  <div class="fym">{tm_html}</div>
</div>

<div class="page">
  <div class="band"><div><div class="k">Pairs · cut along the dashed line</div><h1>Slip Detective A/B</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.4pt">Each story is in the past, but three verbs slipped into the present. Can your partner hear them?</p>
  {swap_card("A", STA, STB)}
  {swap_card("B", STB, STA)}
</div>

<div class="page">
  <div class="poster">
    <h1>Check it before you hand it up</h1>
    <div class="ops">
      <div style="background:var(--green-soft)"><b>Time</b>yesterday → walked<br>every day → walks<br>tomorrow → will walk</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Agree</b>each · one of → is, has<br>Tom and Aoife → are, have</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Saw / seen</b>I saw it<br>I have seen it</div>
      <div style="background:var(--green-soft)"><b>I / me</b>Tom and I went<br>picked Tom and me</div>
    </div>
    <p style="text-align:center;font-size:20pt!important;font-weight:800;margin:4mm 0">Take away the other person.</p>
    <p style="text-align:center;font-size:10pt;color:var(--muted)">Léim · leim.ie · Play Tense Trap: {GAME}</p>
  </div>
</div>

<div class="page ws">
  <div class="band"><div><div class="k">Worksheet · exam-style questions</div><h1>Fix the Sentence</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Fix the Sentence</h2>
  <p>Each sentence has a mistake in standard written English. Write it correctly and say why.</p>
  <table class="eh"><thead><tr><th>Sentence</th><th>Correct version and why</th></tr></thead><tbody>
  {"".join(f"<tr><td style='font-weight:500'>{s}</td><td><span class='gap'></span><span class='gap'></span></td></tr>" for s, r in FIX)}
  </tbody></table>
  <h2>B. Exam-style questions: "{PASS[0]}"</h2>
  <div class="pass">{pass_html}</div>
  <ol class="q">
    <li>The writer meant to write this in the past. Find <b>three</b> verbs that slipped into the present and correct them.<span class="long"></span></li>
    <li>Find and correct the mistake with “I / me” in the first sentence. Explain the fix.<span class="long"></span></li>
    <li>Find and correct the agreement mistake (subject and verb) in the second sentence.<span class="long"></span></li>
    <li>Find and correct the “saw / seen” mistake. Why is it wrong in standard written English?<span class="long"></span></li>
    <li>Write <b>two</b> more sentences to finish the story, in the past, with one “and I” and one “has / have + seen / done / gone”.<span class="long"></span><span class="long"></span></li>
  </ol>
</div>

<div class="page an">
  <div class="band"><div><div class="k">For the teacher</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>Time Match (sentence card ↔ verb card)</h2>
  <p>{tm_key}</p>
  <p>pa = past, pr = present, fu = future. Each verb card fits only its sentence: check the time word first, then the subject (he / she / it → -s in the present).</p>
  <h2>Slip Detective</h2>
  <p><b>A</b> “{STA[0]}”: {", ".join(f"{x} → {PAST[x]}" for x in SLA)} · <b>B</b> “{STB[0]}”: {", ".join(f"{x} → {PAST[x]}" for x in SLB)}</p>
  <h2>A. Fix the Sentence</h2>
  <table><tbody>{"".join(f"<tr><td style='width:38%'>{s}</td><td>{r}</td></tr>" for s, r in FIX)}</tbody></table>
  <h2>B. Exam-style questions</h2>
  <ol class="q">
    <li>Any three of: walk → walked, blows → blew, sends → sent (the story is set “Last Sunday”).</li>
    <li>“Fiona and me walk” → “Fiona and I walked”: the pronoun is part of the subject (take away Fiona: “I walked”).</li>
    <li>“each of us were” → “each of us was”: each = one person at a time, so singular.</li>
    <li>“we seen” → “we saw”: there is no helper verb (has / have / had), so the past form “saw” is needed. “We seen” is spoken Irish English, not standard written English.</li>
    <li>Sample: <i>Fiona and I stopped for chips in the village. I have never seen the sea so wild.</i> Credit past tense throughout and the two required forms.</li>
  </ol>
  <p style="font-size:9pt">All six fixes in the passage: {" · ".join(PASS_FIX)}.</p>
  <h2>Marking tip</h2>
  <p>In writing tasks, reward one steady tense and correct agreement as part of accuracy; quote the student's own slips back to them so they learn to spot them. Our guide, not an official marking scheme.</p>
</div>
</body></html>"""

cover = """<!doctype html><html><head><meta charset="utf-8"><style>
body{margin:0;width:1200px;height:1200px;background:#1B2430;font-family:Inter,sans-serif;color:#fff;display:flex;flex-direction:column;justify-content:space-between;padding:90px;box-sizing:border-box}
.k{display:inline-block;background:#2E7D57;border-radius:99px;padding:12px 26px;font-weight:700;font-size:28px;letter-spacing:.06em;text-transform:uppercase}
h1{font-size:92px;font-weight:800;line-height:1.25;letter-spacing:-.02em;margin:60px 0 20px}
h1 span{background:#F6CF5A;color:#1B2430;padding:0 18px;border-radius:14px}
.sub{font-size:40px;line-height:1.4;color:#DDE3EA}
.em{font-size:48px;margin-top:30px;font-weight:800;letter-spacing:.01em;color:#F6CF5A}
.foot{display:flex;justify-content:space-between;align-items:center;font-size:34px;font-weight:700}
.price{background:#F6CF5A;color:#1B2430;border-radius:16px;padding:14px 28px}
</style></head><body>
<div><span class="k">Junior Cycle English · Teacher pack</span>
<h1><span>Tenses, agreement</span><br><span>&amp; pronouns</span></h1>
<div class="sub">Time Match cards · Slip Detective A/B<br>Poster · Worksheet + answers</div>
<div class="em">saw or seen? · is or are?<br>I or me?</div></div>
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
    pdf("teacher-pack", os.path.join(OUT, "Tenses-Agreement-Pronouns-Teacher-Pack-Leim.pdf"))
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--hide-scrollbars", "--window-size=1200,1200",
                    f"--screenshot={os.path.join(OUT, f'{SLUG}-cover.png')}", f"{SLUG}-cover.html"], cwd=SRC, check=True, capture_output=True)
