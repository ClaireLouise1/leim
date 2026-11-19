#!/usr/bin/env python3
"""Poetry 1: imagery & sound (JC English Order 8): free sheet (-> printables/), 6-page teacher pack + 1200x1200 cover (-> OUTDIR).
Usage: python3 src/build_poetry1_pdfs.py /tmp/poetry
Items come from the game's data block (technique-spotter.html). Every answer is re-derived with the checker's own rules
(src/test_technique_spotter.py: techniques, senses, compared, rhymes) and asserted. Styles are read from src/build_money1_pdfs.py."""
import os, sys, random, subprocess, re
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC); sys.path.insert(0, SRC)
from test_technique_spotter import techniques, senses, compared, rhymes, last_word, load
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/poetry"; os.makedirs(OUT, exist_ok=True)
SLUG = "poetry-imagery-sound"
LO = "R8, R11, R4, OL8"
GAME = "leim.ie/technique-spotter.html"
D = load(os.path.join(ROOT, "technique-spotter.html"))
NAME = {"sim": "Simile", "met": "Metaphor", "per": "Personification", "all": "Alliteration", "ono": "Onomatopoeia", "rhy": "Rhyme"}
SNAME = {"see": "Sight", "hear": "Sound", "smell": "Smell", "taste": "Taste", "touch": "Touch"}
def one(s):
    f = techniques(s); assert len(f) == 1, (s, f); return list(f)[0]
def art(b): return b if b.endswith("s") else ("an " if b[0] in "aeiou" else "a ") + b
def the(a): return a if a[0].isupper() else "the " + a
def by(k): return [x for x in D["spot"] if x[1] == k]

# ---------- free sheet ----------
random.seed(88)
A_items = []
for k in ("sim", "met", "per", "all", "ono", "sim", "per", "met"):
    x = random.choice([y for y in by(k) if y not in A_items]); A_items.append(x)
random.shuffle(A_items)
for x in A_items: assert one(x[0]) == x[1]
B_items = [x for x in by("sim") + by("met") if x[0] not in [a[0] for a in A_items]]
random.shuffle(B_items); B_items = B_items[:3]
for s, k, a, b in B_items:
    c = compared(s); assert c[0].lower().rstrip("s") == a.lower().rstrip("s") and c[1].rstrip("s") == b.rstrip("s"), (s, c)
C_items = []
for k in ("touch", "hear", "taste", "see", "smell"):
    x = random.choice([y for y in D["senses"] if y[1] == k]); C_items.append(x); assert senses(x[0]) == {k}
random.shuffle(C_items)
D_items = random.sample(D["rhyme"], 4)
for w, r, wrong in D_items:
    assert rhymes(w, r) and not any(rhymes(w, x) for x in wrong)
D_opts = []
for i, (w, r, wrong) in enumerate(D_items):
    o = [r] + wrong; random.shuffle(o); D_opts.append(o)
POEM = next(P for P in D["poems"] if P["k"].endswith("Monday"))
E_items = sorted(POEM["ask"], key=lambda a: a[0])
for k, ln in E_items:
    assert [i + 1 for i, l in enumerate(POEM["lines"]) if k in techniques(l)] == [ln]
RAIN = ["The rain is a drummer on our roof,", "tap, tap, tapping through the night.", "The gutters gurgle, gulp and gush,", "and puddles spread like ink."]
assert "met" in techniques(RAIN[0]) and "ono" in techniques(RAIN[1]) and "all" in techniques(RAIN[2]) and "ono" in techniques(RAIN[2]) and "sim" in techniques(RAIN[3])
NQ = len(A_items) + len(B_items) + len(C_items) + len(D_items) + len(E_items) + 2; assert NQ == 26, NQ
nA = 1; nB = nA + len(A_items); nC = nB + len(B_items); nD = nC + len(C_items); nE = nD + len(D_items); nF = nE + len(E_items)

def style(var):
    return re.search(var + r' = f"""<!doctype.*?<style>(.*?)</style>', open(os.path.join(SRC, "build_money1_pdfs.py"), encoding="utf-8").read(), re.S).group(1).replace("{LO}", LO).replace("{{", "{").replace("}}", "}").replace("JC Maths LOs (2018 spec)", "JC English LOs (2015 spec)")
SHEET_STYLE = style("sheet"); PACK_STYLE = style("pack")
assert "JC English LOs (2015 spec)" in SHEET_STYLE and "Single-teacher licence" in PACK_STYLE and "JC English LOs (2015 spec)" in PACK_STYLE
EXTRA = """.wk{line-height:1.45;border:1.5px solid var(--line);border-radius:8px;padding:2px 7px;margin:3px 0;font-size:9.4pt}.wk b.h{display:block}
table.st{border-collapse:collapse;margin:3px 0;font-size:9.2pt;width:100%}table.st td,table.st th{border:1px solid #C9D1DA;padding:2px 6px;text-align:left}
.bank{border:1.5px solid var(--line);border-radius:8px;padding:4px 10px;margin:4px 0;text-align:center;font-weight:700;word-spacing:4px}
.pass{border-left:4px solid var(--green);background:var(--mist);padding:5px 10px;margin:4px 0;font-style:italic}
.pm{border:1.5px solid var(--line);border-radius:8px;padding:3px 8px;margin:2px 0 3px;font-size:9.2pt;line-height:1.4;font-style:italic}
.pm .n{display:inline-block;min-width:13px;height:13px;border-radius:50%;background:#1B2430;color:#fff;font-size:7pt;font-weight:800;text-align:center;line-height:13px;margin-right:3px;font-style:normal}
i.ln{font-style:italic}"""
def poem_html(L): return "<div class='pm'>" + "<br>".join(f"<span class='n'>{i}</span>{l}" for i, l in enumerate(L, 1)) + "</div>"
TECHS = "Simile · Metaphor · Personification · Alliteration · Onomatopoeia"
A_html = "".join(f"<li value='{i}'><i>{s}</i> <span class='line' style='min-width:26mm'></span></li>" for i, (s, k, *r) in enumerate(A_items, nA))
B_html = "".join(f"<li value='{i}'><i>{s}</i><br>The ________ is compared to ________.</li>" for i, (s, k, a, b) in enumerate(B_items, nB))
C_html = "".join(f"<li value='{i}'><i>{s}</i> <span class='line' style='min-width:16mm'></span></li>" for i, (s, k) in enumerate(C_items, nC))
D_html = "".join(f"<li value='{i}'><b>{w}</b> &nbsp; → &nbsp; {' &nbsp; / &nbsp; '.join(o)}</li>" for i, ((w, r, x), o) in enumerate(zip(D_items, D_opts), nD))
E_html = "".join(f"<li value='{i}'>Which line uses {('an ' if NAME[k][0] in 'AEIOU' else 'a ') + NAME[k].lower()}? <span class='line' style='min-width:10mm'></span></li>" for i, (k, ln) in enumerate(E_items, nE))

sheet = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Poetry: imagery and sound, rules and practice | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{SHEET_STYLE}
{EXTRA}
.p2 ol.q li{{margin-bottom:1px;font-size:9pt}}.p2 h2{{margin:4px 0 2px}}.p2 .two{{gap:5mm}}
</style></head><body>
<div class="page tight">
  <div class="band"><div><div class="k">Junior Cycle English · Free revision sheet</div><h1>Poetry: imagery and sound</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2015 specification): {LO}. Play the game: <b>{GAME}</b></p>
  <div class="two">
   <div><h2>1. Six techniques to spot</h2>
    <table class="st"><thead><tr><th>Technique</th><th>What it is</th><th>Example</th></tr></thead><tbody>
     <tr><td><b>Simile</b></td><td>compares two things using <b>like</b> or <b>as</b></td><td><i>Rain fell like tiny needles.</i></td></tr>
     <tr><td><b>Metaphor</b></td><td>says one thing <b>is</b> another</td><td><i>The classroom was a zoo.</i></td></tr>
     <tr><td><b>Personification</b></td><td>a thing does something only a person can do</td><td><i>The wind whispered.</i></td></tr>
     <tr><td><b>Alliteration</b></td><td>words close together start with the same sound</td><td><i>Fierce flames flickered.</i></td></tr>
     <tr><td><b>Onomatopoeia</b></td><td>a word that sounds like the noise it names</td><td><i>sizzle, crash, creak</i></td></tr>
     <tr><td><b>Rhyme</b></td><td>words end with the same sound</td><td><i>night / bright</i></td></tr></tbody></table>
    <h2>2. Simile or metaphor?</h2>
    <div class="wk">Look for the small word. <i>Her eyes shone <b>like</b> stars</i> → simile. <i>The stars <b>were</b> diamonds</i> → metaphor. A metaphor is stronger: it doesn't say "a bit like", it says "is".</div>
    <h2>3. Rhyme is about sound, not spelling</h2>
    <div class="wk"><i>wood / good</i> rhyme. <i>wood / food</i> look alike but don't. Say them out loud. A poem that rhymes in pairs (side / tide, eye / sky) is in <b>rhyming couplets</b>.</div></div>
   <div><h2>4. Imagery: the five senses</h2>
    <table class="st"><tbody>
     <tr><td><b>Sight</b></td><td>colours, light, shapes: <i>golden, glittered, shadows</i></td></tr>
     <tr><td><b>Sound</b></td><td><i>roared, echoed, rang, rumbled</i></td></tr>
     <tr><td><b>Smell</b></td><td><i>scent, stank, perfume, reeked</i></td></tr>
     <tr><td><b>Taste</b></td><td><i>sour, salty, bitter, spicy</i></td></tr>
     <tr><td><b>Touch</b></td><td><i>rough, icy, soft, soggy</i></td></tr></tbody></table>
    <h2>5. Name it, quote it, explain it</h2>
    <div class="wk"><b>Name:</b> The poet uses personification.<br><b>Quote:</b> "The wind whispered secrets to the trees."<br><b>Explain:</b> It makes the wind seem gentle and mysterious, as if it is sharing a secret. The mood is quiet and calm.</div>
    <h2>6. Words for the effect</h2>
    <p>The technique creates a <b>picture</b> (it helps us imagine…), a <b>mood</b> (calm, eerie, lonely, joyful, tense) or a <b>sound</b> (harsh, soft, fast, slow).</p>
    <div class="note"><b>Classic mistakes:</b> naming a technique and stopping · "it makes the poem more interesting" (say HOW) · calling a simile a metaphor · quoting the whole verse · "rhymes" that only look the same.</div></div>
  </div>
  <div class="tip"><b>Exam tip:</b> two techniques, each explained well, beat a list of five names. Always ask "So what? What does it make me see, hear or feel?"</div>
</div>

<div class="page p2">
  <div class="band"><div><div class="k">Practice · {NQ} questions</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <div class="two"><div><h2>A. Name the technique</h2><div class="bank" style="font-size:8.4pt">{TECHS}</div><ol class="q">{A_html}</ol></div>
  <div><h2>B. What is compared?</h2><ol class="q">{B_html}</ol>
  <h2>C. Which sense? (sight, sound, smell, taste, touch)</h2><ol class="q">{C_html}</ol></div></div>
  <div class="two"><div><h2>D. Circle the word that rhymes</h2><ol class="q">{D_html}</ol></div>
  <div><h2>E. "{POEM['k'].split(' ', 1)[1]}"</h2>{poem_html(POEM["lines"])}<ol class="q">{E_html}</ol></div></div>
  <h2>F. Exam-style: "Rain on the Roof"</h2>
  <div class="pass">{"<br>".join(RAIN)}</div>
  <ol class="q">
   <li value="{nF}">Find a metaphor in the poem. What does it suggest about the rain?<span class="long"></span><span class="long"></span></li>
   <li value="{nF + 1}">How does the poet use sound in lines 2 and 3? Quote and explain two examples.<span class="long"></span><span class="long"></span><span class="long"></span></li>
  </ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">Check your work</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <table class="ans"><tbody>
   <tr><td><b>A</b></td><td>{" · ".join(f"{i}. {NAME[k]}" for i, (s, k, *r) in enumerate(A_items, nA))}</td></tr>
   <tr><td><b>B</b></td><td>{" · ".join(f"{i}. {the(a)} → {art(b)}" for i, (s, k, a, b) in enumerate(B_items, nB))}</td></tr>
   <tr><td><b>C</b></td><td>{" · ".join(f"{i}. {SNAME[k]}" for i, (s, k) in enumerate(C_items, nC))}</td></tr>
   <tr><td><b>D</b></td><td>{" · ".join(f"{i}. {r}" for i, (w, r, x) in enumerate(D_items, nD))}<br>(The others look or sound close, but the end sound is different: say them out loud.)</td></tr>
   <tr><td><b>E</b></td><td>{" · ".join(f"{i}. line {ln} ({NAME[k].lower()})" for i, (k, ln) in enumerate(E_items, nE))}</td></tr>
   <tr><td><b>F</b></td><td>{nF}. "The rain is a drummer on our roof": the rain makes a steady, loud beat, like someone playing drums. It suggests the rain is heavy and keeps going all night.<br>
     {nF + 1}. Onomatopoeia: "tap, tap, tapping" lets us hear the rain; repeating it gives a steady rhythm. Alliteration + onomatopoeia: "gutters gurgle, gulp and gush": the repeated g sound is thick and watery, like water rushing down the drain.</td></tr>
  </tbody></table>
  <h2>Worked examples</h2>
  <div class="two">
   <div class="wk"><b class="h">Simile or metaphor?</b>"{B_items[0][0]}" — {"it uses <b>like</b> or <b>as</b>, so it's a simile" if B_items[0][1] == "sim" else "it says one thing <b>is</b> another, so it's a metaphor"}. {the(B_items[0][2]).capitalize() if B_items[0][2].islower() else B_items[0][2]} is compared to {art(B_items[0][3])}.</div>
   <div class="wk"><b class="h">Personification</b>Ask: could this thing really do it? An alarm clock can't shout and a kettle can't sing. Only people can.</div>
   <div class="wk"><b class="h">Alliteration</b>Three or more words close together with the same first sound: "Fierce flames flickered". One word said three times (crunch, crunch, crunch) is repetition, not alliteration.</div>
   <div class="wk"><b class="h">Explaining the effect</b>Not "it makes it interesting" but "it makes the rain sound heavy and steady, like a drum".</div>
  </div>
  <div class="note"><b>Got one wrong?</b> Go back to the table on page 1, then play <b>Technique Spotter</b> at {GAME}: the "Go back over these" list at the end explains each mistake.</div>
  <p class="small">All poems and lines written by Léim. Léim is independent and not connected with the State Examinations Commission or the NCCA.</p>
</div>
</body></html>"""

# ---------- teacher pack ----------
SORT = []
for k in ("sim", "met", "per", "all", "ono", "rhy"):
    L = [x for x in by(k) if x not in A_items]; random.seed(800 + len(SORT)); SORT += random.sample(L, 4)
for x in SORT: assert one(x[0]) == x[1]
random.seed(808); random.shuffle(SORT)
sort_html = "".join(f'<div class="c"><span class="tag">Card {i}</span><div class="fc sm">{x[0].replace(" / ", "<br>")}</div></div>' for i, x in enumerate(SORT, 1))
sort_key = " · ".join(f"<b>{NAME[k]}</b>: " + ", ".join(str(i) for i, x in enumerate(SORT, 1) if x[1] == k) for k in NAME)

SWAP_A = ("Saturday Morning", ["The toast pops up, golden and hot.", "Dad's singing is as loud as a foghorn.", "The sleepy sun yawns over the roofs.",
          "My brother is a grumpy bear until ten.", "Soft, silky slippers slide across the floor.", "And Saturday has only just begun."])
SWAP_B = ("The Match", ["The crowd is a sea of red and white.", "Flags flap and flutter in the wind.", "The whistle blows. Thud! The ball is kicked.",
          "Our captain runs like a greyhound.", "The goalposts shiver as the ball flies in.", "And twenty thousand voices cheer."])
SWAP_KEY = {}
for name, L in (SWAP_A, SWAP_B):
    found = [techniques(l) for l in L]
    assert all(len(f) <= 1 for f in found), (name, found)
    SWAP_KEY[name] = {list(f)[0]: i for i, f in enumerate(found, 1) if f}
    assert set(SWAP_KEY[name]) == {"sim", "met", "per", "all", "ono"}, (name, SWAP_KEY[name])
def swap_card(who, mine, theirs):
    name, L = mine
    return f"""<div class="idc"><h3>Student {who} · Poem Swap</h3>
    <p style="font-size:8.6pt;margin:0 0 1mm"><b>1. Read your poem aloud twice</b>, slowly. Your partner listens with their book closed and fills in the grid.</p>
    <div class="pm" style="font-size:10.4pt"><b style="font-style:normal">"{name}"</b><br>{"<br>".join(L)}</div>
    <p style="font-size:8.6pt;margin:1mm 0"><b>2. Then listen</b> to "{theirs[0]}". Write the words you hear for each technique:</p>
    <table class="st" style="font-size:8.6pt"><tbody>{"".join(f"<tr><td style='width:28%'><b>{NAME[k]}</b></td><td></td></tr>" for k in ("sim", "met", "per", "all", "ono"))}</tbody></table>
    <p style="font-size:8.6pt;margin:1mm 0 0"><b>3. Talk:</b> which technique do you like best in your partner's poem? What does it make you see or hear?</p></div>"""

FIX = [("The poet uses a simile.", "Names it only. Add the quote and the effect: <b>\"Rain fell like tiny needles\": the rain feels sharp and painful.</b>"),
       ("\"The classroom was a zoo\" is a simile.", "Wrong technique: no like / as, so it's a <b>metaphor</b>."),
       ("\"The wind whispered\" is personification and it makes the poem more interesting.", "Effect too vague. Say how: <b>it makes the wind sound gentle and secretive, so the mood is calm.</b>"),
       ("\"My boots go crunch, crunch, crunch\" is alliteration.", "One word repeated is repetition. \"Crunch\" is <b>onomatopoeia</b>: it sounds like boots on snow."),
       ("\"wood\" rhymes with \"food\".", "They only look alike. <b>wood / good</b> rhyme; say them aloud."),
       ("The poet appeals to the senses: \"Golden light glowed in every window and the bakery smelled of fresh bread and the stone wall felt rough and cold.\"", "Quote far too long. Use short quotes and name each sense: <b>sight (\"golden light\"), smell (\"fresh bread\").</b>")]
assert one("Rain fell like tiny needles on the roof.") == "sim" and one("The classroom was a zoo after lunch.") == "met"
assert one("The wind whispered secrets to the trees.") == "per" and techniques("My boots go crunch, crunch, crunch.") == {"ono"}
assert not rhymes("wood", "food") and rhymes("wood", "good")

BONFIRE = ["The bonfire is a dragon in the dark,", "its flames crackle, spit and spark.", "Sparks rise like bees into the night,",
           "and smoke hides every star from sight.", "The air smells of burning wood;", "our cold hands warm. The heat feels good."]
assert "met" in techniques(BONFIRE[0]) and "ono" in techniques(BONFIRE[1]) and "sim" in techniques(BONFIRE[2])
assert "smell" in senses(BONFIRE[4]) and "touch" in senses(BONFIRE[5])
for a, b in ((0, 1), (2, 3), (4, 5)): assert rhymes(last_word(BONFIRE[a]), last_word(BONFIRE[b])), (a, b)
assert compared(BONFIRE[0].rstrip(",") + ".")[1] == "dragon"

pack = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Poetry: Imagery and Sound Teacher Pack | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{PACK_STYLE}
{EXTRA}
.fym .c{{height:28mm}}.fym .fc.sm{{font-size:9.6pt;line-height:1.28;margin-top:2mm;font-weight:600;font-style:italic}}.idc{{padding:2mm 4mm;margin-bottom:3mm}}.idc h3{{margin:0 0 1mm}}
.idc .st td{{height:5.2mm;padding:1px 6px}}.p1 .proc td{{font-size:8.6pt;padding:2px 6px}}.ops div{{font-size:12pt;padding:4mm 3mm}}.ops b{{font-size:18pt}}
.ws .eh td{{font-size:8.6pt;padding:2px 6px}}.ws .eh .gap{{height:13px}}.ws ol.q li{{margin-bottom:1px}}
</style></head><body>

<div class="page p1">
  <div class="band"><div><div class="k">Junior Cycle English · Teacher pack</div><h1>Poetry: imagery and sound</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2015 specification): {LO}</p>
  <div class="two">
    <div><h3>Aims</h3><p>By the end of the lesson students can spot simile, metaphor, personification, alliteration, onomatopoeia and rhyme, say which sense an image appeals to, and write a point that names a technique, quotes it and explains its effect.</p></div>
    <div><h3>In this pack</h3><p>p.1 Teacher notes · p.2 Technique Sort cards (cut-up) · p.3 Poem Swap A/B (speaking + listening) · p.4 Wall poster · p.5 Worksheet: Fix the Answer + exam-style questions · p.6 Answers. Level: 1st year (useful revision in 2nd and 3rd). Time: about 60 minutes. All poems are original.</p></div>
  </div>
  <h2 style="margin-top:8px">Procedure</h2>
  <table class="proc"><tbody>
    <tr><td>5 min</td><td><b>Lead-in.</b> Write three lines about the moon: <i>The moon hung like a silver coin. / The moon is a lamp above our town. / The moon frowned down from behind a cloud.</i> Which two compare? What's the one small word that's different? What can't a moon really do?</td></tr>
    <tr><td>8 min</td><td><b>Guided discovery.</b> Elicit simile (like / as), metaphor (is), personification (a human action). Then say <i>sizzle</i> and <i>fierce flames flickered</i> aloud: what do students notice? Board the six techniques and the five senses, then model one "name it, quote it, explain it" answer.</td></tr>
    <tr><td>12 min</td><td><b>Technique Sort</b> (p.2, groups of 3–4, one set of 24 cards). Sort the cards into six piles. Then each group picks one card per pile and says what it makes them see or hear.</td></tr>
    <tr><td>12 min</td><td><b>Poem Swap</b> (p.3, pairs). A reads "Saturday Morning" aloud twice; B listens with the book closed and writes the words for each technique. Swap for "The Match". Check together.</td></tr>
    <tr><td>18 min</td><td><b>Worksheet</b> (p.5). Fix the Answer in pairs, then the exam-style questions on "Bonfire Night" alone.</td></tr>
    <tr><td>5 min</td><td><b>Exit ticket.</b> Write one simile and one metaphor about your school on a Monday morning. Homework: play <b>Technique Spotter</b> at {GAME}.</td></tr>
  </tbody></table>
  <div class="note"><b>Errors to look for:</b> naming a technique with no effect · "it makes it more interesting" · simile and metaphor mixed up · one repeated word called alliteration · rhymes that only look alike (wood / food). <b>Support:</b> the poster (p.4) on the desk; give weaker groups the six pile labels. <b>Fast finishers:</b> write a 4-line poem about the weather with three different techniques.</div>
  <p class="small"><b>Technique Sort key:</b> {sort_key}</p>
</div>

<div class="page">
  <div class="band"><div><div class="k">Groups of 3–4 · cut up the 24 cards</div><h1>Technique Sort</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.4pt;margin:0 0 2mm">Sort the cards into <b>six piles</b>: simile, metaphor, personification, alliteration, onomatopoeia, rhyme. Each pile has 4 cards.</p>
  <div class="fym">{sort_html}</div>
</div>

<div class="page">
  <div class="band"><div><div class="k">Pairs · cut along the dashed line</div><h1>Poem Swap A/B</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.4pt">Each poem has a simile, a metaphor, personification, alliteration and onomatopoeia. Listen carefully: can you hear all five?</p>
  {swap_card("A", SWAP_A, SWAP_B)}
  {swap_card("B", SWAP_B, SWAP_A)}
</div>

<div class="page">
  <div class="poster">
    <h1>Name it. Quote it. Explain it.</h1>
    <div class="ops">
      <div style="background:var(--green-soft)"><b>Simile</b>like · as<br>Rain fell like needles.</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Metaphor</b>is · was<br>The classroom was a zoo.</div>
      <div style="background:var(--green-soft)"><b>Personification</b>a thing acts human<br>The wind whispered.</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Alliteration</b>same first sound<br>Fierce flames flickered.</div>
      <div style="background:var(--green-soft)"><b>Onomatopoeia</b>sounds like the noise<br>sizzle · crash · creak</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Rhyme</b>same end sound<br>night / bright</div>
    </div>
    <p style="text-align:center;font-size:20pt!important;font-weight:800;margin:4mm 0">So what? What does it make you see, hear or feel?</p>
    <p style="text-align:center;font-size:10pt;color:var(--muted)">Léim · leim.ie · Play Technique Spotter: {GAME}</p>
  </div>
</div>

<div class="page ws">
  <div class="band"><div><div class="k">Worksheet · exam-style questions</div><h1>Fix the Answer</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Fix the Answer</h2>
  <p>Each student answer has one problem. Say what's wrong and write a better answer.</p>
  <table class="eh"><thead><tr><th>Student answer</th><th>What's wrong and the fix</th></tr></thead><tbody>
  {"".join(f"<tr><td style='font-weight:500'>{s}</td><td><span class='gap'></span><span class='gap'></span></td></tr>" for s, r in FIX)}
  </tbody></table>
  <h2>B. Exam-style questions: "Bonfire Night"</h2>
  <div class="pass">{"<br>".join(BONFIRE)}</div>
  <ol class="q">
    <li>Find a metaphor in the poem. What picture does it create?<span class="long"></span></li>
    <li>Pick out two sound words. What do they help you hear?<span class="long"></span></li>
    <li>"Sparks rise like bees into the night": what is compared, and why is it a good comparison?<span class="long"></span></li>
    <li>Which senses does the poet appeal to? Give a short quote for two of them.<span class="long"></span></li>
    <li>Describe the rhyme in the poem. What effect does it have?<span class="long"></span></li>
  </ol>
</div>

<div class="page an">
  <div class="band"><div><div class="k">For the teacher</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>Technique Sort</h2>
  <p>{sort_key}</p>
  <h2>Poem Swap</h2>
  {"".join(f"<p><b>{n}:</b> " + " · ".join(f"{NAME[k]}: line {ln} (<i>{dict((SWAP_A, SWAP_B))[n][ln - 1]}</i>)" for k, ln in sorted(SWAP_KEY[n].items(), key=lambda z: z[1])) + "</p>" for n in SWAP_KEY)}
  <h2>A. Fix the Answer</h2>
  <table><tbody>{"".join(f"<tr><td style='width:42%'>{s}</td><td>{r}</td></tr>" for s, r in FIX)}</tbody></table>
  <h2>B. Exam-style questions</h2>
  <ol class="q">
    <li>"The bonfire is a dragon in the dark": it pictures the fire as huge, wild and fierce, breathing flames into the night.</li>
    <li>"crackle" and "spit" (onomatopoeia): the snapping and popping of the burning wood.</li>
    <li>Sparks are compared to bees: they are small, bright and fly up in a busy swarm.</li>
    <li>Sight ("smoke hides every star"), sound ("crackle, spit"), smell ("smells of burning wood"), touch ("our cold hands warm"). Any two with quotes.</li>
    <li>Rhyming couplets: dark / spark, night / sight, wood / good. The steady rhyme gives a warm, cosy, sing-song feel, like friends gathered round the fire.</li>
  </ol>
  <h2>Marking tip</h2>
  <p>Credit the technique (named correctly), a short accurate quote and a clear effect. The effect carries the most weight: "it makes it interesting" is not an effect.</p>
</div>
</body></html>"""

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
<h1><span>Poetry:</span><br><span>imagery &amp; sound</span></h1>
<div class="sub">Technique Sort cards · Poem Swap A/B<br>Poster · Worksheet + answers</div>
<div class="em">simile · metaphor · personification<br>alliteration · onomatopoeia · rhyme</div></div>
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
    pdf("teacher-pack", os.path.join(OUT, "Poetry-Imagery-Sound-Teacher-Pack-Leim.pdf"))
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--hide-scrollbars", "--window-size=1200,1200",
                    f"--screenshot={os.path.join(OUT, f'{SLUG}-cover.png')}", f"{SLUG}-cover.html"], cwd=SRC, check=True, capture_output=True)
