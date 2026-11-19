#!/usr/bin/env python3
"""Register & tone (JC English Order 16): free sheet (-> printables/), 6-page teacher pack + 1200x1200 cover (-> OUTDIR).
Usage: python3 src/build_register_tone_pdfs.py /tmp/register
Items come from the game's data block (register-switch.html). Every answer is re-derived with the checker's own rules
(src/test_register_switch.py: register, reader, manner, blunt, tones, inf) and asserted; the checker's data pass runs first.
Styles are read from src/build_money1_pdfs.py."""
import os, sys, random, subprocess, re
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC); sys.path.insert(0, SRC)
from test_register_switch import register, reader, manner, blunt, tones, inf, form, slang_word, load, data_pass
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/register"; os.makedirs(OUT, exist_ok=True)
SLUG = "register-tone"
LO = "OL12, R12, R13, W12"
GAME = "leim.ie/register-switch.html"
D = load(os.path.join(ROOT, "register-switch.html")); assert not data_pass(D), data_pass(D)
TN = {"ch": "Cheerful", "sa": "Sad", "an": "Angry", "wo": "Worried"}
TQ = {"ch": r"brilliant|wonderful|delighted|thrilled|lovely|hooray|can't wait|best day|great news",
      "sa": r"miss|lonely|tears|cried|empty|goodbye|never see|Sadly", "an": r"furious|sick of|fed up|unacceptable|How dare|ridiculous|slammed|Never again",
      "wo": r"What if|worried|anxious|nervous|keep thinking|hope nothing|afraid|scared"}
def tq(s, k): return re.search(TQ[k], s, re.I).group(0)

# ---------- free sheet ----------
random.seed(1616)
SW = random.sample(D["switch"], 6)
A_items = [(it[2] if i % 2 == 0 else it[3]) for i, it in enumerate(SW)]; random.shuffle(A_items)
for s in A_items: assert register(s) in ("f", "i")
B_items = random.sample([x for x in D["pol"] if x[1] == "p"], 3) + random.sample([x for x in D["pol"] if x[1] == "b"], 3); random.shuffle(B_items)
for s, k in B_items: assert manner(s) == k
C_items = random.sample(D["mkpol"], 3)
for b, a, w in C_items: assert manner(b) == "b" and manner(a) == "p"
D_items = [x for k in TN for x in random.sample([y for y in D["tone"] if y[1] == k], 2)]; random.shuffle(D_items)
for s, k in D_items: assert tones(s) == [k]
E_items = random.sample(D["slang"], 4)
for s in E_items: assert inf(slang_word(s)) and not inf(s.replace("{" + slang_word(s) + "}", ""))
NQ = len(A_items) + len(B_items) + len(C_items) + len(D_items) + len(E_items) + 2; assert NQ == 29, NQ
nA = 1; nB = nA + len(A_items); nC = nB + len(B_items); nD = nC + len(C_items); nE = nD + len(D_items); nF = nE + len(E_items)
SWAPS = {"deadly": "excellent", "loads": "many", "super": "very", "rank": "poor", "awesome": "excellent", "gonna": "going to",
         "totally": "very", "epic": "very enjoyable", "dodgy": "unsafe", "wrecked": "exhausted", "cool": "excellent", "wanna": "want to",
         "tons": "thousands", "asap": "as soon as possible", "buzzing": "excited", "gutted": "very disappointed", "grand": "fine", "savage": "excellent"}
for s in D["slang"]: assert slang_word(s) in SWAPS, s

def style(var):
    return re.search(var + r' = f"""<!doctype.*?<style>(.*?)</style>', open(os.path.join(SRC, "build_money1_pdfs.py"), encoding="utf-8").read(), re.S).group(1).replace("{LO}", LO).replace("{{", "{").replace("}}", "}").replace("JC Maths LOs (2018 spec)", "JC English LOs (2015 spec)")
SHEET_STYLE = style("sheet"); PACK_STYLE = style("pack")
assert "JC English LOs (2015 spec)" in SHEET_STYLE and "Single-teacher licence" in PACK_STYLE and "JC English LOs (2015 spec)" in PACK_STYLE
EXTRA = """.wk{line-height:1.45;border:1.5px solid var(--line);border-radius:8px;padding:2px 7px;margin:3px 0;font-size:9.4pt}.wk b.h{display:block}
table.st{border-collapse:collapse;margin:3px 0;font-size:9.2pt;width:100%}table.st td,table.st th{border:1px solid #C9D1DA;padding:2px 6px;text-align:left}
.pass{border-left:4px solid var(--green);background:var(--mist);padding:5px 10px;margin:4px 0;font-style:italic}"""

A_html = "".join(f"<li value='{i}'><i>{s}</i><br>Formal / Informal · reader: <span class='line' style='min-width:30mm'></span></li>" for i, s in enumerate(A_items, nA))
B_html = "".join(f"<li value='{i}'><i>{s}</i> &nbsp; <b>Polite / Blunt</b></li>" for i, (s, k) in enumerate(B_items, nB))
C_html = "".join(f"<li value='{i}'><i>{b}</i><span class='long'></span></li>" for i, (b, a, w) in enumerate(C_items, nC))
D_html = "".join(f"<li value='{i}'><i>{s}</i> <span class='line' style='min-width:22mm'></span></li>" for i, (s, k) in enumerate(D_items, nD))
E_html = "".join(f"<li value='{i}'><i>{s.replace('{', '').replace('}', '')}</i><br>slang: <span class='line' style='min-width:20mm'></span> formal word: <span class='line' style='min-width:26mm'></span></li>" for i, s in enumerate(E_items, nE))
def reader_of(line):
    it = [x for x in D["switch"] if line in (x[2], x[3])][0]; return it[0] if line == it[2] else it[1]
def plain_reader(sit): return re.sub(r"^\S+ ", "", sit).split(":")[0].lower()

sheet = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Register and tone, rules and practice | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{SHEET_STYLE}
{EXTRA}
.p2 ol.q li{{margin-bottom:1px;font-size:9pt}}.p2 h2{{margin:4px 0 2px}}.p2 .two{{gap:5mm}}
</style></head><body>
<div class="page tight">
  <div class="band"><div><div class="k">Junior Cycle English · Free revision sheet</div><h1>Register and tone</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2015 specification): {LO}. Play the game: <b>{GAME}</b></p>
  <div class="two">
   <div><h2>1. Register: who is it for?</h2>
    <p style="font-size:9.4pt"><b>Register</b> is how formal your words are. It changes with your <b>reader</b> and your <b>purpose</b>.</p>
    <table class="st"><thead><tr><th>Formal</th><th>Informal</th></tr></thead><tbody>
     <tr><td>a principal, a manager, an editor, the council, an audience, judges, strangers</td><td>friends, family, your team chat</td></tr>
     <tr><td>I am, I cannot, I would like</td><td>I'm, can't, I'd love</td></tr>
     <tr><td>I wish to complain about…</td><td>It's a joke!</td></tr>
     <tr><td>no slang, no "!!"</td><td>slang and "!" are fine</td></tr></tbody></table>
    <h2>2. Same news, two readers</h2>
    <div class="wk"><b class="h">Text to a friend</b><i>Match's off Saturday, pitch is flooded. Gutted!!</i></div>
    <div class="wk"><b class="h">Email to the principal</b><i>I am writing to let you know that Saturday's match has been cancelled because the pitch is flooded.</i></div>
    <p style="font-size:9pt">The facts stay the same. The words change.</p></div>
   <div><h2>3. Polite or blunt?</h2>
    <table class="st"><thead><tr><th>Blunt (an order)</th><th>Polite (a question)</th></tr></thead><tbody>
     <tr><td>Give me that book.</td><td>Could you pass me that book, please?</td></tr>
     <tr><td>Turn the TV down.</td><td>Would you mind turning the TV down?</td></tr>
     <tr><td>Move!</td><td>Excuse me, could I get past?</td></tr></tbody></table>
    <div class="note"><b>Watch out:</b> "Move, please!" is still an order. Polite tools: <b>Could you…? Would you mind…? Excuse me · Sorry · Thank you</b>.</div>
    <h2>4. Tone: the feeling in the words</h2>
    <table class="st"><tbody>
     <tr><td><b>Cheerful</b></td><td>brilliant, thrilled, can't wait</td></tr><tr><td><b>Sad</b></td><td>miss, lonely, tears, goodbye</td></tr>
     <tr><td><b>Angry</b></td><td>furious, fed up, unacceptable</td></tr><tr><td><b>Worried</b></td><td>what if, nervous, anxious, afraid</td></tr></tbody></table>
    <h2>5. Slang to swap in formal writing</h2>
    <div class="wk">deadly / epic → excellent · loads → many · wrecked → exhausted · gonna → going to · asap → as soon as possible</div></div>
  </div>
  <div class="tip"><b>Exam tip:</b> every writing task names a <b>reader</b> and a <b>purpose</b>. Underline them before you write. For a tone question: name the tone, quote the words that create it, and explain.</div>
</div>

<div class="page p2">
  <div class="band"><div><div class="k">Practice · {NQ} questions</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <div class="two"><div><h2>A. Formal or informal? Circle one, then name a reader it suits</h2><ol class="q">{A_html}</ol></div>
  <div><h2>B. Polite or blunt? Circle one</h2><ol class="q">{B_html}</ol>
  <h2>D. Which tone? Cheerful, sad, angry or worried</h2><ol class="q">{D_html}</ol></div></div>
  <h2>C. Make it polite: rewrite each order as a polite request</h2><ol class="q">{C_html}</ol>
  <h2>E. Find the slang word and swap it for a formal word</h2><div class="two"><div><ol class="q">{E_html[:E_html.index("<li value='" + str(nE + 2))]}</ol></div><div><ol class="q">{E_html[E_html.index("<li value='" + str(nE + 2)):]}</ol></div></div>
</div>

<div class="page">
  <div class="band"><div><div class="k">Exam-style + answers</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <h2>F. Exam-style</h2>
  <ol class="q">
   <li value="{nF}">The school disco has been cancelled. Write it as (a) a <b>message to your class group chat</b> and (b) a <b>notice for the school website</b>. Then name <b>two</b> differences.<span class="long"></span><span class="long"></span><span class="long"></span></li>
   <li value="{nF + 1}">What is the tone of this line? Quote <b>two</b> words that show it: <i>"I'm fed up with this. Three times the bin wasn't collected, and nobody answers the phone. It's ridiculous."</i><span class="long"></span><span class="long"></span></li>
  </ol>
  <h2>Answers</h2>
  <table class="ans"><tbody>
   <tr><td><b>A</b></td><td>{" · ".join(f"{i}. {'Formal' if register(s) == 'f' else 'Informal'} ({plain_reader(reader_of(s))})" for i, s in enumerate(A_items, nA))}<br>(Any reader of the right kind is fine.)</td></tr>
   <tr><td><b>B</b></td><td>{" · ".join(f"{i}. {'Polite' if manner(s) == 'p' else 'Blunt'}" for i, (s, k) in enumerate(B_items, nB))}</td></tr>
   <tr><td><b>C</b></td><td>{"<br>".join(f"{i}. {a}" for i, (b, a, w) in enumerate(C_items, nC))}<br>(Other polite versions are fine: a question, softening words, no "!" or "now".)</td></tr>
   <tr><td><b>D</b></td><td>{" · ".join(f"{i}. {TN[tones(s)[0]]} ({tq(s, tones(s)[0])})" for i, (s, k) in enumerate(D_items, nD))}</td></tr>
   <tr><td><b>E</b></td><td>{" · ".join(f"{i}. {slang_word(s)} → {SWAPS[slang_word(s)]}" for i, s in enumerate(E_items, nE))}</td></tr>
   <tr><td><b>F</b></td><td>{nF}. Sample: (a) <i>Disco's off Friday, the hall's flooded. Gutted!!</i> (b) <i>Please note that Friday's school disco has been cancelled because the hall is flooded. Tickets will be refunded.</i> Differences: short forms and slang in (a); full words and extra details (refunds) in (b).<br>
     {nF + 1}. <b>Angry</b>: "fed up" and "ridiculous" show the writer is annoyed; "Three times" shows it keeps happening.</td></tr>
  </tbody></table>
  <div class="note"><b>Got one wrong?</b> Go back to page 1, then play <b>Register Switch</b> at {GAME}: the "Go back over these" list at the end explains each mistake.</div>
  <p class="small">All sentences written by Léim; names and places are made up. Léim is independent and not connected with the State Examinations Commission or the NCCA.</p>
</div>
</body></html>"""
assert tones("I'm fed up with this. Three times the bin wasn't collected, and nobody answers the phone. It's ridiculous.") == ["an"]
assert register("Please note that Friday's school disco has been cancelled because the hall is flooded.") != "i" and inf("Disco's off Friday, the hall's flooded. Gutted!!")

# ---------- teacher pack ----------
random.seed(1617)
RM = random.sample(D["switch"], 6)
CARDS = []
for n, it in enumerate(RM, 1):
    for sit, line in ((it[0], it[2]), (it[1], it[3])):
        assert register(line) == reader(sit)
        CARDS.append(("s", sit, line)); CARDS.append(("l", line, sit))
assert len(CARDS) == 24
order = list(range(24)); random.shuffle(order)
CS = [CARDS[i] for i in order]
def strip_emoji(s): return re.sub(r"^\S+ ", "", s)
rm_html = "".join(f'<div class="c"><span class="tag">{"Reader" if k == "s" else "Line"} · Card {i}</span><div class="fc sm">{strip_emoji(t) if k == "s" else t}</div></div>' for i, (k, t, m) in enumerate(CS, 1))
rm_key = " · ".join(f"{CS.index(c) + 1} ↔ {[j for j, d in enumerate(CS, 1) if d[0] == 'l' and d[1] == c[2]][0]} ({'F' if register(c[2]) == 'f' else 'I'})" for c in CS if c[0] == "s")

PA = D["mkpol"][0:6]; PB = D["mkpol"][6:12]
def swap_card(who, mine, theirs, seed):
    ans = [a for b, a, w in theirs]; random.seed(seed); random.shuffle(ans)
    return f"""<div class="idc"><h3>Student {who} · Polite Swap</h3>
    <p style="font-size:8.8pt;margin:0 0 1mm"><b>1. Bark</b> each order at your partner, one at a time (in a grumpy voice!). Your partner finds the polite version on their card and says it back politely. Tick it if it matches.</p>
    <table class="st" style="font-size:9pt"><tbody>{"".join(f"<tr><td style='width:6%'><b>{i}</b></td><td>{b}</td><td style='width:8%'>☐</td></tr>" for i, (b, a, w) in enumerate(mine, 1))}</tbody></table>
    <p style="font-size:8.8pt;margin:1mm 0"><b>2. Listen</b> to your partner's orders. Find the polite version below and say it. Write their order number in the box.</p>
    <table class="st" style="font-size:9pt"><tbody>{"".join(f"<tr><td>{a}</td><td style='width:10%'></td></tr>" for a in ans)}</tbody></table>
    <p style="font-size:8.8pt;margin:1mm 0 0"><b>3. Together:</b> circle the words that make each version polite.</p></div>"""
for b, a, w in PA + PB: assert manner(b) == "b" and manner(a) == "p"

FIX = [("To the county council: “Hey, the road outside our school is a total disaster!!”", "Too casual for the council: <b>I am writing to report the dangerous state of the road outside our school.</b>"),
       ("Text to your friend: “I am writing to inform you that I will be late.”", "Too stiff for a friend: <b>Running late, soz! Be there in ten.</b>"),
       ("To a hotel manager: “Gimme a refund asap.”", "Blunt and slangy: <b>I would be grateful for a full refund.</b>"),
       ("Speech to the judges: “Cheers, lads, this is deadly!”", "Too casual for judges: <b>Thank you very much for this award.</b>"),
       ("Note to a neighbour: “Move your car now!”", "Blunt: <b>Would you mind moving your car? It is blocking our gate.</b>"),
       ("Letter to the editor: “Loads of people are well fed up with the buses.”", "Slang: <b>Many people in our town are unhappy with the bus service.</b>")]
assert register("I am writing to report the dangerous state of the road outside our school.") == "f" and inf("Hey, the road outside our school is a total disaster!!")
assert inf("Running late, soz! Be there in ten.") and register("I would be grateful for a full refund.") == "f" and register("Thank you very much for this award.") == "f"
assert manner("Would you mind moving your car? It is blocking our gate.") == "p" and manner("Move your car now!") == "b" and inf("Loads of people are well fed up with the buses.")

NOTICE = ("Ballinora Tidy Towns: Clean-Up Day", "We are delighted to announce that our autumn clean-up will take place on Saturday, 10 October, from ten o'clock. "
          "Volunteers are asked to meet at the community hall, where gloves and bags will be provided. Sadly, last year's flower beds were damaged by litter, "
          "so we would be grateful for every pair of hands. Refreshments will be served afterwards.")
REPLY = "omg I'm so in!! Can I bring my dog? He's deadly at finding cans lol"
assert inf(REPLY) and not inf(NOTICE[1]) and "would be grateful" in NOTICE[1] and "We are delighted" in NOTICE[1]

pack = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Register and Tone Teacher Pack | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{PACK_STYLE}
{EXTRA}
.fym .c{{height:30mm}}.fym .fc.sm{{font-size:9.2pt;line-height:1.25;margin-top:2mm;font-weight:500}}.idc{{padding:2mm 4mm;margin-bottom:3mm}}.idc h3{{margin:0 0 1mm}}
.idc .st td{{padding:1px 6px}}.p1 .proc td{{font-size:8.6pt;padding:2px 6px}}.ops div{{font-size:12pt;padding:5mm 3mm}}.ops b{{font-size:19pt}}
.ws .eh td{{font-size:8.6pt;padding:2px 6px}}.ws .eh .gap{{height:13px}}.ws ol.q li{{margin-bottom:1px}}.ws .pass{{font-size:9pt}}
</style></head><body>

<div class="page p1">
  <div class="band"><div><div class="k">Junior Cycle English · Teacher pack</div><h1>Register and tone</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2015 specification): {LO}</p>
  <div class="two">
    <div><h3>Aims</h3><p>By the end of the lesson students can choose a formal or informal register to suit a reader and purpose, turn a blunt order into a polite request, name the tone of a short text with evidence, and swap slang for formal words.</p></div>
    <div><h3>In this pack</h3><p>p.1 Teacher notes · p.2 Reader Match cards (cut-up) · p.3 Polite Swap A/B (speaking) · p.4 Wall poster · p.5 Worksheet: Fix the Register + exam-style questions · p.6 Answers. Level: 2nd year. Time: about 60 minutes. All texts are original; names and places are made up.</p></div>
  </div>
  <h2 style="margin-top:8px">Procedure</h2>
  <table class="proc"><tbody>
    <tr><td>5 min</td><td><b>Lead-in.</b> Say “Give me your pen.” in a grumpy voice, then “Sorry, could I borrow your pen, please?” Which would you say to the principal? Why? Elicit <b>register</b> (how formal) and <b>tone</b> (the feeling).</td></tr>
    <tr><td>8 min</td><td><b>Guided discovery.</b> Show the same news three ways (text to a friend, email to the principal, announcement: the game's “Spot the pattern”). What stays the same? What changes? Elicit: the facts stay, the words change with the reader.</td></tr>
    <tr><td>12 min</td><td><b>Reader Match</b> (p.2, groups of 3, one set of 24 cards). Match each reader card to the line that suits it. Then sort the pairs into formal and informal, and say which words gave it away.</td></tr>
    <tr><td>12 min</td><td><b>Polite Swap</b> (p.3, pairs). A barks an order; B finds and says the polite version; then swap. Together they circle the polite tools (could you, would you mind, sorry…).</td></tr>
    <tr><td>18 min</td><td><b>Worksheet</b> (p.5). Fix the Register in pairs, then the exam-style questions on the Tidy Towns notice alone.</td></tr>
    <tr><td>5 min</td><td><b>Exit ticket.</b> Write one line about a lost dog for (1) your best friend and (2) a local radio announcement. Homework: play <b>Register Switch</b> at {GAME}.</td></tr>
  </tbody></table>
  <div class="note"><b>Errors to look for:</b> one slang word (“loads”, “deadly”) in a formal piece · “please!” added to an order and called polite · stiff formal language to a friend · naming a tone with no quote · confusing tone (the feeling) with register (how formal). <b>Support:</b> the poster (p.4) on the desk. <b>Fast finishers:</b> rewrite the Tidy Towns notice as a text to a friend.</div>
</div>

<div class="page">
  <div class="band"><div><div class="k">Groups of 3 · cut up the 24 cards</div><h1>Reader Match</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.4pt;margin:0 0 2mm">There are 12 <b>reader</b> cards and 12 <b>line</b> cards. Match each reader to the line that suits them. Then sort your pairs into <b>formal</b> and <b>informal</b>.</p>
  <div class="fym">{rm_html}</div>
</div>

<div class="page">
  <div class="band"><div><div class="k">Pairs · cut along the dashed line</div><h1>Polite Swap A/B</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.4pt">Every blunt order has a polite twin on your partner's card. Can you find it by listening?</p>
  {swap_card("A", PA, PB, 1618)}
  {swap_card("B", PB, PA, 1619)}
</div>

<div class="page">
  <div class="poster">
    <h1>Who's listening?</h1>
    <div class="ops">
      <div style="background:var(--green-soft)"><b>Formal</b>principal · manager · council<br>I am · I would like · no slang</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Informal</b>friends · family<br>I'm · can't · Guess what!</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Polite</b>Could you…? Would you mind…?<br>Sorry · Thank you</div>
      <div style="background:var(--green-soft)"><b>Tone</b>name it · quote it<br>explain it</div>
    </div>
    <p style="text-align:center;font-size:20pt!important;font-weight:800;margin:4mm 0">Same facts. Different words.</p>
    <p style="text-align:center;font-size:10pt;color:var(--muted)">Léim · leim.ie · Play Register Switch: {GAME}</p>
  </div>
</div>

<div class="page ws">
  <div class="band"><div><div class="k">Worksheet · exam-style questions</div><h1>Fix the Register</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Fix the Register</h2>
  <p>Each line is wrong for its reader. Say what's wrong and write a better line.</p>
  <table class="eh"><thead><tr><th>Reader and line</th><th>What's wrong and the fix</th></tr></thead><tbody>
  {"".join(f"<tr><td style='font-weight:500'>{s}</td><td><span class='gap'></span><span class='gap'></span></td></tr>" for s, r in FIX)}
  </tbody></table>
  <h2>B. Exam-style questions: "{NOTICE[0]}"</h2>
  <div class="pass"><b style="font-style:normal">{NOTICE[0]}</b><br>{NOTICE[1]}</div>
  <p style="font-size:9pt;margin:1mm 0">A reply posted under the notice:</p>
  <div class="pass">{REPLY}</div>
  <ol class="q">
    <li>Who is the notice written for, and what is its purpose?<span class="long"></span></li>
    <li>Is the notice formal or informal? Give <b>two</b> features that show it.<span class="long"></span></li>
    <li>Find <b>one</b> cheerful word and <b>one</b> sad word in the notice. Why does the writer use both?<span class="long"></span></li>
    <li>Name <b>three</b> things that make the reply informal.<span class="long"></span></li>
    <li>Rewrite the reply so it would suit an email to the Tidy Towns committee.<span class="long"></span><span class="long"></span></li>
  </ol>
</div>

<div class="page an">
  <div class="band"><div><div class="k">For the teacher</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>Reader Match (reader card ↔ line card)</h2>
  <p>{rm_key}</p>
  <p>Formal (F): {", ".join(plain_reader(it[0]) for it in RM)}. Informal (I): {", ".join(plain_reader(it[1]) for it in RM)}. The same news appears twice (once for each kind of reader), so students must read the register, not just the topic.</p>
  <h2>Polite Swap</h2>
  <table class="st"><tbody>{"".join(f"<tr><td style='width:40%'><b>{w} {i}</b> {b}</td><td>{a}</td></tr>" for w, L in (("A", PA), ("B", PB)) for i, (b, a, x) in enumerate(L, 1))}</tbody></table>
  <h2>A. Fix the Register</h2>
  <table><tbody>{"".join(f"<tr><td style='width:40%'>{s}</td><td>{r}</td></tr>" for s, r in FIX)}</tbody></table>
  <h2>B. Exam-style questions</h2>
  <ol class="q">
    <li>People in Ballinora (local residents); to invite volunteers to the clean-up day and give the details.</li>
    <li>Formal: full words (“We are delighted to announce”, “we would be grateful”); polite requests (“Volunteers are asked”); exact details (date, time, place); no slang or “!”.</li>
    <li>Cheerful: “delighted”; sad: “Sadly”. The sad detail (damaged flower beds) shows why help is needed; the cheerful words make people want to come.</li>
    <li>Slang and text speak (“omg”, “deadly”, “lol”); short forms (I'm, He's); “!!”; no capital letter at the start.</li>
    <li>Sample: <i>Thank you for organising the clean-up. I would be happy to help on Saturday. Would it be possible to bring my dog?</i> Credit full words, a polite question and no slang.</li>
  </ol>
  <h2>Marking tip</h2>
  <p>Reward the right register for the reader first, then polite, clear requests, then evidence (quoted words) for any tone named. Our guide, not an official marking scheme.</p>
</div>
</body></html>"""
assert tones("We are delighted") == ["ch"] and tones("Sadly") == ["sa"]

cover = """<!doctype html><html><head><meta charset="utf-8"><style>
body{margin:0;width:1200px;height:1200px;background:#1B2430;font-family:Inter,sans-serif;color:#fff;display:flex;flex-direction:column;justify-content:space-between;padding:90px;box-sizing:border-box}
.k{display:inline-block;background:#2E7D57;border-radius:99px;padding:12px 26px;font-weight:700;font-size:28px;letter-spacing:.06em;text-transform:uppercase}
h1{font-size:104px;font-weight:800;line-height:1.25;letter-spacing:-.02em;margin:60px 0 20px}
h1 span{background:#F6CF5A;color:#1B2430;padding:0 18px;border-radius:14px}
.sub{font-size:40px;line-height:1.4;color:#DDE3EA}
.em{font-size:48px;margin-top:30px;font-weight:800;letter-spacing:.01em;color:#F6CF5A}
.foot{display:flex;justify-content:space-between;align-items:center;font-size:34px;font-weight:700}
.price{background:#F6CF5A;color:#1B2430;border-radius:16px;padding:14px 28px}
</style></head><body>
<div><span class="k">Junior Cycle English · Teacher pack</span>
<h1><span>Register &amp;</span><br><span>tone</span></h1>
<div class="sub">Reader Match cards · Polite Swap A/B<br>Poster · Worksheet + answers</div>
<div class="em">formal or informal · polite or blunt<br>name the tone</div></div>
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
    pdf("teacher-pack", os.path.join(OUT, "Register-Tone-Teacher-Pack-Leim.pdf"))
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--hide-scrollbars", "--window-size=1200,1200",
                    f"--screenshot={os.path.join(OUT, f'{SLUG}-cover.png')}", f"{SLUG}-cover.html"], cwd=SRC, check=True, capture_output=True)
