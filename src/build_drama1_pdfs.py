#!/usr/bin/env python3
"""Drama 1: how plays work (JC English Order 21): free sheet (-> printables/), 6-page teacher pack + 1200x1200 cover (-> OUTDIR).
Usage: python3 src/build_drama1_pdfs.py /tmp/drama1
Items come from the game's data block (stage-it.html). Every answer is re-derived with the checker's own rules
(src/test_stage_it.py: moods, dirkind, depts, conflicts, feelings) and asserted; the checker's data pass runs first.
Styles are read from src/build_money1_pdfs.py."""
import os, sys, random, subprocess, re
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC); sys.path.insert(0, SRC)
from test_stage_it import moods, dirkind, depts, conflicts, feelings, load, data_pass
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/drama1"; os.makedirs(OUT, exist_ok=True)
SLUG = "drama-how-plays-work"
LO = "R6, R7, R9, OL8"
GAME = "leim.ie/stage-it.html"
D = load(os.path.join(ROOT, "stage-it.html")); assert not data_pass(D), data_pass(D)
LN = {"sp": "dim, cold blue light", "ha": "bright, warm light", "sa": "soft, grey light", "da": "flashing red light", "pe": "gentle golden light"}
SN = {"sp": "an owl and a creaking door", "ha": "cheering and lively music", "sa": "a slow, sad violin", "da": "a fast, pounding drum", "pe": "birdsong and gentle waves"}
MN = {"sp": "Spooky", "ha": "Happy", "sa": "Sad", "da": "Danger", "pe": "Peaceful"}
DN = {"voi": "How to say it", "mov": "Where to move", "act": "What to do", "face": "Face"}
BN = {"set": "Set", "cos": "Costume", "lig": "Lighting", "sou": "Sound", "pro": "Props"}
CN = {"per": "Person vs person", "self": "Person vs self", "nat": "Person vs nature", "soc": "Person vs society"}
FN = {"an": "Angry", "sc": "Scared", "ha": "Happy", "sa": "Sad", "ne": "Nervous"}
MK = list(LN); L = "abcde"
SK = ["pe", "da", "sp", "sa", "ha"]  # sound box in a different order, so the two letters never match
def strip(s): return s.split(" ", 1)[1]

# ---------- free sheet ----------
random.seed(2121)
A_items = [x for k in DN for x in random.sample([y for y in D["dir"] if y[1] == k], 2)]; random.shuffle(A_items)
for s, k in A_items: assert dirkind(s) == [k]
B_items = [x for k in BN for x in random.sample([y for y in D["back"] if y[1] == k], 2)]; random.shuffle(B_items)
for s, k in B_items: assert depts(s) == [k]
C_items = [x for k in CN for x in random.sample([y for y in D["con"] if y[1] == k], 1)] + random.sample([y for y in D["con"] if y[1] in ("per", "self")], 2)
C_items = list(dict.fromkeys(map(tuple, C_items)))
while len(C_items) < 6: C_items = list(dict.fromkeys(C_items + [tuple(random.choice(D["con"]))]))
random.shuffle(C_items)
for s, k in C_items: assert conflicts(s) == [k]
D_items = [tuple(random.choice([y for y in D["feel"] if y[2] == k])) for k in FN] + [tuple(random.choice([y for y in D["feel"] if y[2] == "sa" and tuple(y) not in []]))]
D_items = list(dict.fromkeys(D_items))
while len(D_items) < 6: D_items = list(dict.fromkeys(D_items + [tuple(random.choice(D["feel"]))]))
random.shuffle(D_items)
for d, l, k in D_items: assert feelings(d + " " + l) == [k]
E_items = [random.choice([y for y in D["scene"] if y[1] == k]) for k in random.sample(MK, 3)]
for s, k in E_items: assert moods(s) == [k]
NQ = len(A_items) + len(B_items) + len(C_items) + len(D_items) + len(E_items) + 3; assert NQ == 36, NQ
nA = 1; nB = nA + len(A_items); nC = nB + len(B_items); nD = nC + len(C_items); nE = nD + len(D_items); nF = nE + len(E_items)

def style(var):
    return re.search(var + r' = f"""<!doctype.*?<style>(.*?)</style>', open(os.path.join(SRC, "build_money1_pdfs.py"), encoding="utf-8").read(), re.S).group(1).replace("{LO}", LO).replace("{{", "{").replace("}}", "}").replace("JC Maths LOs (2018 spec)", "JC English LOs (2015 spec)")
SHEET_STYLE = style("sheet"); PACK_STYLE = style("pack")
assert "JC English LOs (2015 spec)" in SHEET_STYLE and "Single-teacher licence" in PACK_STYLE and "JC English LOs (2015 spec)" in PACK_STYLE
EXTRA = """.wk{line-height:1.45;border:1.5px solid var(--line);border-radius:8px;padding:2px 7px;margin:3px 0;font-size:9.4pt}.wk b.h{display:block}
table.st{border-collapse:collapse;margin:3px 0;font-size:9.2pt;width:100%}table.st td,table.st th{border:1px solid #C9D1DA;padding:2px 6px;text-align:left}
.pass{border-left:4px solid var(--green);background:var(--mist);padding:5px 10px;margin:4px 0;font-family:Georgia,serif;font-size:9.4pt;line-height:1.45}
.pass i{color:#4A5562}.box{border:1.5px dashed #9AA6B2;border-radius:8px;padding:3px 8px;margin:2px 0 4px;font-size:9pt}"""

def two(items_html, cut):
    return f"<div class='two'><div><ol class='q'>{''.join(items_html[:cut])}</ol></div><div><ol class='q'>{''.join(items_html[cut:])}</ol></div></div>"
A_html = [f"<li value='{i}'><i>{s}</i> <span class='line' style='min-width:26mm'></span></li>" for i, (s, k) in enumerate(A_items, nA)]
B_html = [f"<li value='{i}'>{s} <span class='line' style='min-width:20mm'></span></li>" for i, (s, k) in enumerate(B_items, nB)]
C_html = [f"<li value='{i}'>{s}<br><span class='line' style='min-width:40mm'></span></li>" for i, (s, k) in enumerate(C_items, nC)]
D_html = [f"<li value='{i}'><i>({d})</i> {l} <span class='line' style='min-width:18mm'></span></li>" for i, (d, l, k) in enumerate(D_items, nD)]
E_html = "".join(f"<li value='{i}'>{strip(s)}<br>Lighting: <span class='line' style='min-width:12mm'></span> Sound: <span class='line' style='min-width:12mm'></span></li>" for i, (s, k) in enumerate(E_items, nE))
E_box = ("<div class='box'><b>Lighting:</b> " + " · ".join(f"({L[i]}) {LN[k]}" for i, k in enumerate(MK)) +
         "<br><b>Sound:</b> " + " · ".join(f"({L[i]}) {SN[k]}" for i, k in enumerate(SK)) + "</div>")

MATCH = ("THE MATCH",
  "(A dressing room, minutes before the county final. Bright, harsh light. CIARÁN, sixteen, sits alone, his helmet in his hands. His coach, DEIRDRE, enters.)",
  [("DEIRDRE", "gently", "They're waiting for you, Ciarán."), ("CIARÁN", "staring at the floor", "What if I miss again? Like last year?"),
   ("DEIRDRE", "kneels beside him", "Then you pick up the next ball.")],
  "(Outside, the crowd begins to roar. CIARÁN stands up slowly and pulls on his helmet.)")
assert feelings("staring at the floor What if I miss again?") == ["ne"] and dirkind("(kneels beside him)") == ["mov"] and dirkind("(gently)") == []
def extract(X):
    return (f"<div class='pass'><b>{X[0]}</b> (an extract from an imaginary play)<br><i>{X[1]}</i><br>" +
            "".join(f"<b>{w}:</b> <i>({d})</i> {t}<br>" for w, d, t in X[2]) + f"<i>{X[3]}</i></div>")

sheet = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Drama 1: how plays work, rules and practice | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{SHEET_STYLE}
{EXTRA}
.p2 ol.q li{{margin-bottom:1px;font-size:9pt}}.p2 h2{{margin:4px 0 2px}}.p2 .two{{gap:5mm}}
</style></head><body>
<div class="page tight">
  <div class="band"><div><div class="k">Junior Cycle English · Free revision sheet</div><h1>Drama 1: how plays work</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2015 specification): {LO}. Play the game: <b>{GAME}</b></p>
  <p>A play is written to be <b>seen and heard</b>. When you read one, picture it on a stage: <b>What do we see? What do we hear? How do the characters move and speak?</b></p>
  <div class="two">
   <div><h2>1. Reading a script</h2>
    <div class="pass"><i>(A kitchen, late at night. Rain against the window. DAN sits at the table.)</i><br><b>NUALA:</b> <i>(entering, out of breath)</i> Did you hear that?<br><b>DAN:</b> <i>(not looking up)</i> Hear what?</div>
    <table class="st"><tbody>
     <tr><td><b>Character names</b></td><td>in capitals, before each line</td></tr>
     <tr><td><b>Dialogue</b></td><td>the words the actors say (no speech marks)</td></tr>
     <tr><td><b>Stage directions</b></td><td>in brackets and italics, present tense: where we are, how to <b>say</b> it, where to <b>move</b>, what to <b>do</b>, what the <b>face</b> shows</td></tr></tbody></table>
    <h2>2. The stage</h2>
    <p style="font-size:9pt"><b>Upstage</b> = the back. <b>Downstage</b> = nearest the audience. <b>Stage left / right</b> = the actor's left / right as they face the audience.</p>
    <h2>3. Five backstage jobs</h2>
    <table class="st"><tbody>
     <tr><td><b>Set</b></td><td>the place: backdrop, walls, furniture</td></tr>
     <tr><td><b>Costume</b></td><td>what the actors wear</td></tr>
     <tr><td><b>Lighting</b></td><td>spotlights, blackouts, a glow</td></tr>
     <tr><td><b>Sound</b></td><td>effects and music: thunder, a doorbell</td></tr>
     <tr><td><b>Props</b></td><td>objects actors hold: a letter, keys, a cup</td></tr></tbody></table></div>
   <div><h2>4. Lighting and sound set the mood</h2>
    <table class="st"><thead><tr><th>Mood</th><th>Lighting</th><th>Sound</th></tr></thead><tbody>
     {"".join(f"<tr><td><b>{MN[k]}</b></td><td>{LN[k]}</td><td>{SN[k]}</td></tr>" for k in MK)}</tbody></table>
    <p style="font-size:9pt">A <b>blackout</b> ends a scene with a shock. A <b>spotlight</b> on one character shows they matter most, or that they're alone.</p>
    <h2>5. Conflict drives every play</h2>
    <table class="st"><tbody>
     <tr><td><b>Person vs person</b></td><td>two characters clash</td></tr>
     <tr><td><b>Person vs self</b></td><td>guilt, doubt, a hard choice</td></tr>
     <tr><td><b>Person vs nature</b></td><td>a storm, a flood, the sea</td></tr>
     <tr><td><b>Person vs society</b></td><td>rules, laws, tradition</td></tr></tbody></table>
    <h2>6. Same words, new meaning</h2>
    <div class="wk"><i>(smiling, hugging her mam)</i> I'm fine. = happy<br><i>(slamming the bedroom door)</i> I'm fine. = angry</div>
    <p style="font-size:9pt">In a play, what characters <b>do</b> often tells us more than what they <b>say</b>.</p></div>
  </div>
  <div class="tip"><b>Exam tip:</b> use the <b>stage directions</b> as evidence, not just the dialogue, and give a <b>reason</b> for every staging choice: "a single spotlight, to show how alone he is".</div>
</div>

<div class="page p2">
  <div class="band"><div><div class="k">Practice · {NQ} questions</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. What does each stage direction tell the actor? (say it / move / do / face)</h2>
  {two(A_html, 4)}
  <h2>B. Whose job? (set / costume / lighting / sound / props)</h2>
  {two(B_html, 5)}
  <h2>C. What kind of conflict?</h2>
  {two(C_html, 3)}
  <h2>D. How does the character feel? Use the stage direction</h2>
  {two(D_html, 3)}
  <h2>E. You're the director: pick a letter for the lighting and the sound</h2>
  {E_box}
  <ol class="q">{E_html}</ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">Exam-style · answers</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <h2>F. Exam-style</h2>
  {extract(MATCH)}
  <ol class="q">
   <li value="{nF}">Where and when is this scene set? Use two details from the stage directions.<span class="long"></span></li>
   <li value="{nF + 1}">What is Ciarán's conflict? Quote one line that shows it.<span class="long"></span></li>
   <li value="{nF + 2}">Choose the lighting and one sound effect for the last moment. Explain your choices.<span class="long"></span></li>
  </ol>
  <h2>Answers</h2>
  <table class="ans"><tbody>
   <tr><td><b>A</b></td><td>{" · ".join(f"{i}. {DN[dirkind(s)[0]]}" for i, (s, k) in enumerate(A_items, nA))}</td></tr>
   <tr><td><b>B</b></td><td>{" · ".join(f"{i}. {BN[depts(s)[0]]}" for i, (s, k) in enumerate(B_items, nB))}</td></tr>
   <tr><td><b>C</b></td><td>{" · ".join(f"{i}. {CN[conflicts(s)[0]]}" for i, (s, k) in enumerate(C_items, nC))}</td></tr>
   <tr><td><b>D</b></td><td>{" · ".join(f"{i}. {FN[feelings(d + ' ' + l)[0]]}" for i, (d, l, k) in enumerate(D_items, nD))}</td></tr>
   <tr><td><b>E</b></td><td>{" · ".join(f"{i}. {MN[moods(s)[0]].lower()}: lighting ({L[MK.index(moods(s)[0])]}), sound ({L[SK.index(moods(s)[0])]})" for i, (s, k) in enumerate(E_items, nE))}</td></tr>
   <tr><td><b>F</b></td><td>{nF}. A dressing room, minutes before the county final ("Bright, harsh light"; "his helmet in his hands"). {nF + 1}. Person vs self: his fear of failing again, "What if I miss again? Like last year?" {nF + 2}. E.g. the lights grow brighter as he stands, with the crowd's roar getting louder: he is ready to face his fear. Any choice with a reason.</td></tr>
  </tbody></table>
  <div class="note"><b>Got one wrong?</b> Go back to page 1, then play <b>Stage It</b> at {GAME}: the "Go back over these" list at the end explains each mistake.</div>
  <p class="small">All plays, names and places are made up by Léim. Léim is independent and not connected with the State Examinations Commission or the NCCA.</p>
</div>
</body></html>"""

# ---------- teacher pack ----------
random.seed(2122)
BS = [x for k in BN for x in random.sample([y for y in D["back"] if y[1] == k], 4)]; random.shuffle(BS)
assert len(BS) == 20
for s, k in BS: assert depts(s) == [k]
bs_html = "".join(f'<div class="c"><span class="tag">Card {i}</span><div class="fc sm">{s}</div></div>' for i, (s, k) in enumerate(BS, 1))
bs_key = " · ".join(f"<b>{BN[k]}</b>: {', '.join(str(i) for i, (s, kk) in enumerate(BS, 1) if kk == k)}" for k in BN)

SC_A = [x for x in D["scene"] if x[0].split(" ", 1)[1].startswith(("Midnight", "Seán says", "Smoke fills"))]
SC_B = [x for x in D["scene"] if x[0].split(" ", 1)[1].startswith(("The team lifts", "Sunrise", "A girl knocks"))]
FE_A = [x for x in D["feel"] if x[0] in ("thumping the table", "biting her nails", "beaming")]
FE_B = [x for x in D["feel"] if x[0] in ("trembling", "wiping her eyes", "clapping her hands")]
assert len(SC_A) == len(SC_B) == len(FE_A) == len(FE_B) == 3
for s, k in SC_A + SC_B: assert moods(s) == [k]
for d, l, k in FE_A + FE_B: assert feelings(d + " " + l) == [k]
assert len({k for s, k in SC_A}) == 3 and len({k for s, k in SC_B}) == 3
def swap_card(who, scs, fes):
    return f"""<div class="idc"><h3>Student {who} · Director's Chair</h3>
    <p style="font-size:8.8pt;margin:0 0 1mm"><b>1. Read</b> each scene to your partner. They choose the lighting and the sound from the box and say why. Tick if they match the mood.</p>
    <table class="st" style="font-size:8.8pt"><tbody>{"".join(f"<tr><td style='width:4%'><b>{i}</b></td><td>{strip(s)}</td><td style='width:22%'>Mood: {MN[moods(s)[0]].lower()}</td><td style='width:5%'>☐</td></tr>" for i, (s, k) in enumerate(scs, 1))}</tbody></table>
    <p style="font-size:8.8pt;margin:1mm 0"><b>2. Listen</b> to your partner's three scenes. Choose a letter for each. <b>Lighting:</b> {" · ".join(f"({L[i]}) {LN[k]}" for i, k in enumerate(MK))}. <b>Sound:</b> {" · ".join(f"({L[i]}) {SN[k]}" for i, k in enumerate(SK))}.</p>
    <table class="st" style="font-size:8.8pt"><tbody><tr>{"".join(f"<td><b>{i}</b> Lighting: ___ Sound: ___</td>" for i in range(1, 4))}</tr></tbody></table>
    <p style="font-size:8.8pt;margin:1mm 0"><b>3. Say it like this.</b> Act out each line the way the secret stage direction says (don't read the direction out!). Your partner names the feeling.</p>
    <table class="st" style="font-size:8.8pt"><tbody>{"".join(f"<tr><td style='width:4%'><b>{i}</b></td><td><i>({d})</i> {l}</td><td style='width:5%'>☐</td></tr>" for i, (d, l, k) in enumerate(fes, 1))}</tbody></table></div>"""

FIX = [("The play is set in a room.", "Be precise and use the stage directions: <b>It is set in a small ferry waiting room on an island, late in the evening, in a storm.</b>"),
       ("The stage directions are in brackets.", "Say what they tell us, not what they look like: <b>\"(her hands shaking)\" shows that Mam is frightened.</b>"),
       ("There is a lot of conflict in the scene.", "Name it and say who or what is in the way: <b>Person vs person: Jack is angry with Mam for still hoping Dad will come home.</b>"),
       ("I would use good lighting.", "Choose a specific effect and give a reason: <b>A spotlight on the empty chair, to show that everyone is thinking about the missing father.</b>"),
       ("Then Jack picks up the plate and then Mam says put it back and then the lights come.", "Don't retell the plot. <b>Pick one moment and explain why it works on stage.</b>"),
       ("Mam is sad.", "Back it up with evidence from the script: <b>Mam is hopeful but fragile: she is \"still smiling\" but her hands shake when Jack takes the plate.</b>")]

CHAIR = ("THE EMPTY CHAIR",
  "(A farmhouse kitchen on Christmas Eve. Warm, golden light. Paper chains hang from the ceiling. MAM sets the table. JACK, fifteen, stares at the empty chair at the end.)",
  [("JACK", "bitterly", "You've set a place for him again."), ("MAM", "still smiling, not looking up", "He might come."),
   ("JACK", "picking up the plate", "He said that last year."), ("MAM", "stopping, her hands shaking", "Put it back, Jack.")],
  "(A car's headlights sweep across the window. They both freeze.)")
assert dirkind("(picking up the plate)") == [] and dirkind("(He picks up the plate.)") == ["act"]

pack = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Drama: How Plays Work Teacher Pack | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{PACK_STYLE}
{EXTRA}
.fym .c{{height:36mm}}.fym .fc.sm{{font-size:10.4pt;line-height:1.3;margin-top:2mm;font-weight:500}}.idc{{padding:2mm 4mm;margin-bottom:3mm}}.idc h3{{margin:0 0 1mm}}
.idc .st td{{padding:1px 5px}}.p1 .proc td{{font-size:8.6pt;padding:2px 6px}}.ops div{{font-size:12pt;padding:5mm 3mm}}.ops b{{font-size:19pt}}
.ws .eh td{{font-size:8.6pt;padding:2px 6px}}.ws .eh .gap{{height:13px}}.ws ol.q li{{margin-bottom:1px}}.ws .pass{{font-size:9pt}}
</style></head><body>

<div class="page p1">
  <div class="band"><div><div class="k">Junior Cycle English · Teacher pack</div><h1>Drama 1: how plays work</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2015 specification): {LO}</p>
  <div class="two">
    <div><h3>Aims</h3><p>By the end of the lesson students can read a script (character names, dialogue, stage directions), say what a stage direction tells the actor, name the five backstage jobs, choose lighting and sound to suit a mood, name the conflict in a scene, and explain a staging choice.</p></div>
    <div><h3>In this pack</h3><p>p.1 Teacher notes · p.2 Backstage Sort cards (cut-up) · p.3 Director's Chair A/B (speaking) · p.4 Wall poster · p.5 Worksheet: Fix the Answer + exam-style questions · p.6 Answers. Level: 2nd year. Time: about 60 minutes. Works with any studied play: all scenes are made up.</p></div>
  </div>
  <h2 style="margin-top:8px">Procedure</h2>
  <table class="proc"><tbody>
    <tr><td>5 min</td><td><b>Lead-in.</b> Two volunteers say "I'm fine." twice: once <i>(smiling, hugging her mam)</i>, once <i>(slamming the bedroom door)</i>. Same words: what changed? Introduce stage directions.</td></tr>
    <tr><td>8 min</td><td><b>Guided discovery.</b> Read the NUALA / DAN script on the free sheet. Label character names, dialogue, stage directions. Sort directions into say it / move / do / face. Draw the stage map (upstage, downstage, stage left and right from the actor's view).</td></tr>
    <tr><td>12 min</td><td><b>Backstage Sort</b> (p.2, groups of 3, one set of 20 cards). Sort the production notes into set, costume, lighting, sound and props. Then each group adds one note of its own for a scene from the class play.</td></tr>
    <tr><td>12 min</td><td><b>Director's Chair</b> (p.3, pairs). A reads three scenes; B picks the lighting and sound and says why. Then "Say it like this": A acts out three lines with a secret stage direction; B names the feeling. Swap.</td></tr>
    <tr><td>18 min</td><td><b>Worksheet</b> (p.5). Fix the Answer in pairs, then the exam-style questions on "The Empty Chair" alone.</td></tr>
    <tr><td>5 min</td><td><b>Exit ticket.</b> One key moment from your class play: one lighting choice, one sound, one stage direction, each with a reason. Homework: play <b>Stage It</b> at {GAME}.</td></tr>
  </tbody></table>
  <div class="note"><b>Errors to look for:</b> quoting dialogue only and ignoring the stage directions · "good lighting" with no specific effect or reason · retelling the plot · mixing up stage left and right (it's the actor's left) · calling every disagreement "conflict" without saying who or what is in the way. <b>Support:</b> the poster (p.4) on the desk. <b>Fast finishers:</b> write a 6-line scene with three stage directions and swap it with a partner to stage.</div>
</div>

<div class="page">
  <div class="band"><div><div class="k">Groups of 3 · cut up the 20 cards</div><h1>Backstage Sort</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.4pt;margin:0 0 2mm">You're the backstage team. Sort the 20 production notes into five piles: <b>set · costume · lighting · sound · props</b>.</p>
  <div class="fym">{bs_html}</div>
</div>

<div class="page">
  <div class="band"><div><div class="k">Pairs · cut along the dashed line</div><h1>Director's Chair A/B</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.4pt">Light it, add the sound, then act it out.</p>
  {swap_card("A", SC_A, FE_A)}
  {swap_card("B", SC_B, FE_B)}
</div>

<div class="page">
  <div class="poster">
    <h1>Stage it</h1>
    <div class="ops">
      <div style="background:var(--green-soft)"><b>1 See</b>Set · costume · props<br>Where are we? Who are they?</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>2 Light</b>Bright · dim · spotlight<br>What's the mood?</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>3 Hear</b>Sound effects · music<br>Silence can speak too</div>
      <div style="background:var(--green-soft)"><b>4 Move</b>Stage directions<br>How do they move and speak?</div>
    </div>
    <p style="text-align:center;font-size:20pt!important;font-weight:800;margin:4mm 0">Every choice tells the audience something.</p>
    <p style="text-align:center;font-size:10pt;color:var(--muted)">Léim · leim.ie · Play Stage It: {GAME}</p>
  </div>
</div>

<div class="page ws">
  <div class="band"><div><div class="k">Worksheet · exam-style questions</div><h1>Fix the Answer</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Fix the Answer</h2>
  <p>Each line is a student's answer about a play. Say what's wrong and write a better answer.</p>
  <table class="eh"><thead><tr><th>Answer</th><th>What's wrong and the fix</th></tr></thead><tbody>
  {"".join(f"<tr><td style='font-weight:500'>{s}</td><td><span class='gap'></span><span class='gap'></span></td></tr>" for s, r in FIX)}
  </tbody></table>
  <h2>B. Exam-style questions: "{CHAIR[0].title()}"</h2>
  {extract(CHAIR)}
  <ol class="q">
    <li>Where and when is this scene set? What mood do the opening stage directions create?<span class="long"></span></li>
    <li>What is the conflict between Jack and Mam?<span class="long"></span></li>
    <li>What does "<i>(stopping, her hands shaking)</i>" tell us about Mam?<span class="long"></span></li>
    <li>You are directing. Choose the lighting and one sound for the final moment and explain.<span class="long"></span></li>
    <li>Would this scene work well on stage? Give two reasons.<span class="long"></span><span class="long"></span></li>
  </ol>
</div>

<div class="page an">
  <div class="band"><div><div class="k">For the teacher</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>Backstage Sort (card numbers)</h2>
  <p>{bs_key}</p>
  <h2>Director's Chair</h2>
  <p>{" · ".join(f"<b>{w}{i}</b> {MN[moods(s)[0]]}: {LN[moods(s)[0]]}, {SN[moods(s)[0]]}" for w, LL in (("A", SC_A), ("B", SC_B)) for i, (s, k) in enumerate(LL, 1))}. Say it like this: {" · ".join(f"<b>{w}{i}</b> {FN[feelings(d + ' ' + l)[0]]}" for w, LL in (("A", FE_A), ("B", FE_B)) for i, (d, l, k) in enumerate(LL, 1))}. Accept other lighting and sound choices that come with a good reason.</p>
  <h2>A. Fix the Answer</h2>
  <table><tbody>{"".join(f"<tr><td style='width:34%'>{s}</td><td>{r}</td></tr>" for s, r in FIX)}</tbody></table>
  <h2>B. Exam-style questions</h2>
  <ol class="q">
    <li>A farmhouse kitchen on Christmas Eve. "Warm, golden light" and "Paper chains" create a cosy, festive mood, which makes the empty chair stand out even more.</li>
    <li>Person vs person: Jack is angry and hurt that Mam still sets a place for his father ("You've set a place for him again"); Mam still hopes he will come ("He might come").</li>
    <li>Mam is not as calm as her smile suggests: she is upset and afraid of losing hope. Her hands give her away.</li>
    <li>E.g. the warm light dims to one spotlight on the empty chair as the headlights sweep the room; the sound of a car engine stopping, then silence. It leaves the audience wondering if the father has come home.</li>
    <li>Any two reasons, e.g. strong conflict between two characters; a powerful prop (the plate, the empty chair); a cliffhanger ending with the headlights.</li>
  </ol>
  <h2>Marking tip</h2>
  <p>Reward answers that use stage directions as evidence and give a reason for every staging choice. Our guide, not an official marking scheme.</p>
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
<h1><span>Drama:</span><br><span>how plays work</span></h1>
<div class="sub">Backstage Sort cards · Director's Chair A/B<br>Poster · Worksheet + answers</div>
<div class="em">stage directions · lighting & sound<br>set, costume, props · conflict</div></div>
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
    pdf("teacher-pack", os.path.join(OUT, "Drama-How-Plays-Work-Teacher-Pack-Leim.pdf"))
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--hide-scrollbars", "--window-size=1200,1200",
                    f"--screenshot={os.path.join(OUT, f'{SLUG}-cover.png')}", f"{SLUG}-cover.html"], cwd=SRC, check=True, capture_output=True)
