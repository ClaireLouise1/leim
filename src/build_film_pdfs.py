#!/usr/bin/env python3
"""Film: camera shots, sound & key scenes (JC English Order 27): free sheet (-> printables/),
6-page teacher pack + 1200x1200 cover (-> OUTDIR).
Usage: python3 src/build_film_pdfs.py /tmp/p27
Text items come from the game's data block (shot-spotter.html) and are re-classified with the checker's own rules
(src/test_shot_spotter.py: why_of, sound_of, edit_of, music_of); every frame drawn here is MEASURED with shot_of /
angle_of and asserted. The checker's data pass runs first. Styles are read from src/build_money1_pdfs.py."""
import os, sys, random, subprocess, re, math
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC); sys.path.insert(0, SRC)
from test_shot_spotter import shot_of, angle_of, why_of, sound_of, edit_of, music_of, load, data_pass, SHOT, ANG, WHY, SND, EDT
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/p27"; os.makedirs(OUT, exist_ok=True)
SLUG = "film-shots-sound-key-scenes"
LO = "R9, R7, OL8, W8"
GAME = "leim.ie/shot-spotter.html"
D = load(os.path.join(ROOT, "shot-spotter.html")); assert not data_pass(D), data_pass(D)

# ---------- drawing (same figure as the game: 100 units tall; frame 320 x 200) ----------
SKIN = ["#F3C9A5", "#E2A97E", "#C68A5E", "#8D5A3B"]; HAIR = ["#3B2A1E", "#7A4A22", "#C9A15A", "#1E1E1E"]; TOP = ["#2E7D57", "#3A6EA5", "#C0392B", "#E0B400", "#7B4FA0"]
def r2(x): return round(x, 2)
def person(x, y, s, c):
    return (f'<g class="fig" transform="translate({r2(x)},{r2(y)}) scale({r2(s)})">'
      '<rect x="-6.5" y="52" width="5.5" height="46" fill="#2C3E50"/><rect x="1" y="52" width="5.5" height="46" fill="#2C3E50"/>'
      '<ellipse cx="-4" cy="99" rx="4" ry="1.6" fill="#222"/><ellipse cx="4" cy="99" rx="4" ry="1.6" fill="#222"/>'
      f'<rect x="-13.5" y="16" width="4.5" height="33" rx="2" fill="{c[2]}"/><rect x="9" y="16" width="4.5" height="33" rx="2" fill="{c[2]}"/>'
      f'<rect x="-9" y="15" width="18" height="39" rx="4" fill="{c[2]}"/><rect x="-2" y="11.5" width="4" height="4.5" fill="{c[0]}"/>'
      f'<circle cx="0" cy="6.6" r="6.4" fill="{c[0]}"/><path d="M-6.6,5.5 C-6.6,-1.2 6.6,-1.2 6.6,5.5 C4,2.6 -4,2.6 -6.6,5.5Z" fill="{c[1]}"/>'
      '<circle cx="-2.3" cy="6.6" r="0.95" fill="#fff"/><circle cx="2.3" cy="6.6" r="0.95" fill="#fff"/>'
      '<circle cx="-2.3" cy="6.7" r="0.55" fill="#1B2430"/><circle cx="2.3" cy="6.7" r="0.55" fill="#1B2430"/>'
      '<rect x="-1.7" y="9.9" width="3.4" height="0.55" fill="#9B4A3A"/></g>')
def col(): return (random.choice(SKIN), random.choice(HAIR), random.choice(TOP))
def U(a, b): return random.uniform(a, b)
def shot_svg(k):
    c = col()
    if k == "els":
        s = U(0.28, 0.4); feet = U(150, 172); y = feet - 100 * s; x = U(40, 280)
        bg = ('<rect width="320" height="200" fill="#CFE8F7"/><path d="M0,120 L60,70 L110,110 L170,55 L240,115 L290,85 L320,100 L320,200 L0,200Z" fill="#8FA9B8"/>'
              f'<rect y="{r2(feet - 6)}" width="320" height="{r2(206 - feet)}" fill="#7DB36B"/><circle cx="270" cy="35" r="14" fill="#F6CF5A"/>')
    elif k == "ls":
        s = U(1.4, 1.7); ft = U(186, 195); y = ft - 100 * s; x = U(110, 210)
        bg = f'<rect width="320" height="200" fill="#DDE7EE"/><rect y="{r2(ft - 4)}" width="320" height="{r2(204 - ft)}" fill="#B9C6A4"/>'
    else:
        bg = f'<rect width="320" height="200" fill="{random.choice(["#E9DFC9", "#D6E4EC", "#E7D7E0"])}"/>'; x = U(145, 175)
        if k == "ms": y = U(12, 28); s = (200 - y) / U(0.45, 0.58) / 100
        elif k == "cu": y = U(8, 20); s = (200 - y) / U(0.22, 0.29) / 100
        else: ey = U(88, 112); s = U(20, 26); y = ey - 6.6 * s
    svg = f'<svg class="fr" viewBox="0 0 320 200" xmlns="http://www.w3.org/2000/svg">{bg}{person(x, y, s, c)}</svg>'
    assert shot_of(svg) == k, (k, shot_of(svg)); return svg
def angle_svg(k):
    c = col(); px, s, top = 225, 1.3, 52; ey = top + 6.6 * s
    if k == "hi": cx, cy = U(55, 80), U(6, 16)
    elif k == "lo": cx, cy = U(55, 80), U(168, 176)
    elif k == "eye": cx, cy = U(50, 85), ey
    else: cx, cy = px + U(-4, 4), U(14, 22)
    rot = 90 if k == "bird" else math.degrees(math.atan2(ey - cy, px - cx))
    tx, ty = (cx, top - 2) if k == "bird" else (px, ey)
    svg = (f'<svg class="fr" viewBox="0 0 320 200" xmlns="http://www.w3.org/2000/svg"><rect width="320" height="200" fill="#F4F7FA"/><rect y="182" width="320" height="18" fill="#B9C6A4"/>'
           f'{person(px, top, s, c)}<line x1="{r2(cx)}" y1="{r2(cy)}" x2="{r2(tx)}" y2="{r2(ty)}" stroke="#E0B400" stroke-width="2.5" stroke-dasharray="6 5"/>'
           f'<g class="cam" transform="translate({r2(cx)},{r2(cy)}) rotate({r2(rot)})"><rect x="-15" y="-8" width="22" height="16" rx="3" fill="#1B2430"/>'
           '<polygon points="7,-5 17,-9 17,9 7,5" fill="#1B2430"/><circle cx="-9" cy="-11" r="4.5" fill="#1B2430"/><circle cx="-1" cy="-11" r="4.5" fill="#1B2430"/></g></svg>')
    assert angle_of(svg) == k, (k, angle_of(svg)); return svg
def lab(L, k): return L[k]

def pick(name, k, n): return random.sample([x for x in D[name] if x[1] == k], n)
def checked(name, items):
    F = {"why": why_of, "sound": sound_of, "edit": edit_of, "music": music_of}[name]
    for s, k in items: assert F(s) == k, (s, k, F(s))
    return items

# ---------- free sheet ----------
random.seed(2701)
A_keys = ["ls", "cu", "els", "ecu", "ms", "ls"]; random.shuffle(A_keys)
A_svgs = [shot_svg(k) for k in A_keys]
B_keys = ["lo", "hi", "eye"]; random.shuffle(B_keys)
B_svgs = [angle_svg(k) for k in B_keys]
C_items = checked("why", [pick("why", k, 1)[0] for k in ["est", "cu", "lo", "hi", "pov"]]); random.shuffle(C_items)
D_items = checked("sound", pick("sound", "di", 3) + pick("sound", "nd", 3)); random.shuffle(D_items)
E_items = checked("edit", [pick("edit", k, 1)[0] for k in ["cut", "slow", "flash", "fade", "mont"]]); random.shuffle(E_items)
nA = 1; nB = nA + 6; nC = nB + 3; nD = nC + 5; nE = nD + 6; nF = nE + 5
NQ = nF + 2 - 1; assert NQ == 27, NQ
SIZES_ROW = "".join(f"<div class='mini'>{shot_svg(k)}<b>{SHOT[k]}</b></div>" for k in ["els", "ls", "ms", "cu", "ecu"])
FERRY = ("<b>A key scene from <i>The Last Ferry</i></b> (an imaginary film). Dara (13) has missed the last ferry home from the island. "
         "<b>Shot 1:</b> a long shot of Dara running down the empty pier as the ferry pulls away. "
         "<b>Shot 2:</b> a high-angle shot of Dara alone at the end of the pier. "
         "<b>Shot 3:</b> a close-up of his face as the ferry's lights get smaller. "
         "<b>Sound:</b> the ferry's horn, then slow, soft piano on the soundtrack. "
         "<b>Shot 4:</b> a low-angle shot of an old fisherman stepping out of the dark: “Need a lift, son?”")

def style(var):
    return re.search(var + r' = f"""<!doctype.*?<style>(.*?)</style>', open(os.path.join(SRC, "build_money1_pdfs.py"), encoding="utf-8").read(), re.S).group(1).replace("{LO}", LO).replace("{{", "{").replace("}}", "}").replace("JC Maths LOs (2018 spec)", "JC English LOs (2015 spec)")
SHEET_STYLE = style("sheet"); PACK_STYLE = style("pack")
assert "JC English LOs (2015 spec)" in SHEET_STYLE and "Single-teacher licence" in PACK_STYLE and "JC English LOs (2015 spec)" in PACK_STYLE
EXTRA = """.wk{line-height:1.4;border:1.5px solid var(--line);border-radius:8px;padding:2px 7px;margin:3px 0;font-size:9.2pt}.wk b.h{display:block}
table.st{border-collapse:collapse;margin:3px 0;font-size:9pt;width:100%}table.st td,table.st th{border:1px solid #C9D1DA;padding:2px 6px;text-align:left;vertical-align:top}
.pass{border-left:4px solid var(--green);background:var(--mist);padding:5px 10px;margin:4px 0;font-size:9.3pt;line-height:1.5}
svg.fr{display:block;width:100%;height:auto;border:1.5px solid #1B2430;border-radius:4px}
.minis{display:grid;grid-template-columns:repeat(5,1fr);gap:3mm;margin:2mm 0}.mini b{display:block;font-size:8.2pt;text-align:center;margin-top:1mm}
.frames{display:grid;grid-template-columns:repeat(3,1fr);gap:3mm 5mm}.frames .f{font-size:9pt}.frames .f b{display:inline-block;margin-right:2mm}"""
L = "<span class='line' style='min-width:40mm'></span>"
def li(i, s): return f"<li value='{i}'>{s}</li>"

sheet = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Film: camera shots, sound and key scenes, rules and practice | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{SHEET_STYLE}
{EXTRA}
.p2 ol.q li{{margin-bottom:2px;font-size:9.2pt}}.p2 h2{{margin:4px 0 2px}}.p2 .two{{gap:5mm}}
</style></head><body>
<div class="page tight">
  <div class="band"><div><div class="k">Junior Cycle English · Free revision sheet</div><h1>Film: shots, sound &amp; key scenes</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2015 specification): {LO}. Play the game: <b>{GAME}</b></p>
  <p>Every shot in a film is a choice. In the exam you name the <b>technique</b>, point to the <b>moment</b>, and explain the <b>effect</b> on the audience.</p>
  <h2>1. Shot sizes: how close is the camera?</h2>
  <div class="minis">{SIZES_ROW}</div>
  <p style="font-size:9pt">The further away, the more we see of the <b>place</b> (an extreme long shot often opens a scene: the <b>establishing shot</b>). The closer, the more we see of the <b>feelings</b>.</p>
  <div class="two">
   <div><h2>2. Camera angles</h2>
    <table class="st"><tbody>
     <tr><td><b>Low angle</b></td><td>camera looks up: big, powerful, frightening</td></tr>
     <tr><td><b>High angle</b></td><td>camera looks down: small, weak, alone</td></tr>
     <tr><td><b>Eye level</b></td><td>normal, like meeting the person</td></tr>
     <tr><td><b>Bird's-eye view</b></td><td>right above, looking straight down</td></tr>
     <tr><td><b>Point-of-view shot</b></td><td>we see through a character's eyes</td></tr></tbody></table>
    <h2>3. Sound and music</h2>
    <div class="wk"><b class="h">Diegetic</b>from inside the story: voices, footsteps, a radio. The characters can hear it.</div>
    <div class="wk"><b class="h">Non-diegetic</b>added for us: soundtrack music, a voice-over. The characters can't hear it.</div>
    <p style="font-size:9pt">Music tells us how to feel: low, faster drums = tension; slow piano = sadness; bright fiddle = joy. <b>Silence</b> makes a moment stand out.</p></div>
   <div><h2>4. Editing</h2>
    <table class="st"><tbody>
     <tr><td><b>Quick cuts</b></td><td>many short shots: speed, panic</td></tr>
     <tr><td><b>Slow motion</b></td><td>a big moment lasts longer</td></tr>
     <tr><td><b>Flashback</b></td><td>a jump back to the past</td></tr>
     <tr><td><b>Fade to black</b></td><td>ends a scene; time passes</td></tr>
     <tr><td><b>Montage</b></td><td>short clips squeeze weeks into a minute</td></tr></tbody></table>
    <h2>5. Writing about a key scene</h2>
    <div class="wk"><b class="h">Name it · describe it · say what it does</b>A <b>low-angle shot</b> looks up at the coach on the touchline, so he seems <b>powerful and frightening</b>, and we fear for the team.</div>
    <p style="font-size:9pt">One sentence of plot, then two or three techniques. Name the film and the director.</p></div>
  </div>
  <div class="tip"><b>Exam tip:</b> “the camera shows” wins nothing. “A close-up of her shaking hands shows she is terrified” wins the marks.</div>
</div>

<div class="page p2">
  <div class="band"><div><div class="k">Practice · {NQ} questions</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Name each shot.</h2>
  <div class="frames">{''.join(f"<div class='f'>{svg}<b>{i}.</b>{L}</div>" for i, svg in enumerate(A_svgs, nA))}</div>
  <h2>B. Where is the camera? Name the angle and what it does to the person.</h2>
  <div class="frames">{''.join(f"<div class='f'>{svg}<b>{i}.</b>{L}</div>" for i, svg in enumerate(B_svgs, nB))}</div>
  <div class="two"><div><h2>C. Which shot or angle does the job?</h2><ol class="q">{''.join(li(i, s) for i, (s, k) in enumerate(C_items, nC))}</ol></div>
  <div><h2>D. Diegetic (D) or non-diegetic (N)?</h2><ol class="q">{''.join(li(i, s + " ____") for i, (s, k) in enumerate(D_items, nD))}</ol></div></div>
  <h2>E. Which editing trick? (quick cuts, slow motion, flashback, fade to black, montage)</h2>
  <ol class="q">{''.join(li(i, s) for i, (s, k) in enumerate(E_items, nE))}</ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">Exam-style · answers</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <h2>F. Exam-style</h2>
  <div class="pass">{FERRY}</div>
  <ol class="q">
   <li value="{nF}">How does the director make Dara seem alone and in trouble in Shots 1 to 3? Refer to two techniques.<span class="long"></span><span class="long"></span><span class="long"></span><span class="long"></span></li>
   <li value="{nF + 1}">Why do you think Shot 4 is a low-angle shot? How might the audience feel about the fisherman at this moment?<span class="long"></span><span class="long"></span><span class="long"></span></li>
  </ol>
  <h2>Answers</h2>
  <table class="ans"><tbody>
   <tr><td><b>A</b></td><td>{" · ".join(f"{i}. {SHOT[k]}" for i, k in enumerate(A_keys, nA))}</td></tr>
   <tr><td><b>B</b></td><td>{" · ".join(f"{i}. {ANG[k]}" + {'lo': ' (looks up: big, powerful)', 'hi': ' (looks down: small, weak)', 'eye': ' (normal)'}[k] for i, k in enumerate(B_keys, nB))}</td></tr>
   <tr><td><b>C</b></td><td>{" · ".join(f"{i}. {WHY[k]}" for i, (s, k) in enumerate(C_items, nC))}</td></tr>
   <tr><td><b>D</b></td><td>{" · ".join(f"{i}. {'D' if k == 'di' else 'N'}" for i, (s, k) in enumerate(D_items, nD))}</td></tr>
   <tr><td><b>E</b></td><td>{" · ".join(f"{i}. {EDT[k]}" for i, (s, k) in enumerate(E_items, nE))}</td></tr>
   <tr><td><b>F</b></td><td>{nF}. For example: the long shot of the <b>empty</b> pier shows nobody is there to help; the <b>high-angle</b> shot looks down on Dara, so he seems small and powerless; the <b>close-up</b> as the lights get smaller shows his worry; the slow piano (non-diegetic) adds sadness. Reward two techniques named, each linked to the effect. · {nF + 1}. The low angle makes the fisherman seem big and a little frightening as he steps out of the dark, so we are unsure at first whether to trust him, until his kind words (“Need a lift, son?”) bring relief. Reward: the angle explained + a feeling with a reason.</td></tr>
  </tbody></table>
  <div class="note"><b>Got one wrong?</b> Go back to page 1, then play <b>Shot Spotter</b> at {GAME}: the “Go back over these” list at the end explains each one.</div>
  <p class="small">All frames, scenes and films here are made up by Léim. Léim is independent and not connected with the State Examinations Commission or the NCCA.</p>
</div>
</body></html>"""

# ---------- teacher pack ----------
random.seed(2702)
SORT = [k for k in ["els", "ls", "ms", "cu", "ecu"] for _ in range(4)]; random.shuffle(SORT)
cards_html = "".join(f'<div class="c"><span class="tag">Card {i}</span>{shot_svg(k)}</div>' for i, k in enumerate(SORT, 1))
ABBR = {"els": "ELS", "ls": "LS", "ms": "MS", "cu": "CU", "ecu": "ECU"}
cards_key = " · ".join(f"<b>{i}</b> {ABBR[k]}" for i, k in enumerate(SORT, 1))

SCENE_A = ("<b>The Match</b> (an imaginary film): Aoife takes the last free of the county final.",
           [("Extreme long shot", "the whole pitch and the packed stand, Aoife a tiny figure in the middle"),
            ("Close-up", "Aoife's face: she bites her lip"),
            ("Low angle", "the goalkeeper on the line, arms spread wide"),
            ("Slow motion", "the ball rising over the bar")],
           "the crowd goes silent; a heartbeat sound is added on the soundtrack; then the roar of the crowd")
SCENE_B = ("<b>The Attic</b> (an imaginary film): Sam goes up to the attic during a power cut.",
           [("Long shot", "Sam at the bottom of the ladder with a torch"),
            ("Point-of-view shot", "the dark attic through Sam's eyes, the torch beam moving"),
            ("Extreme close-up", "Sam's eyes, wide open"),
            ("High angle", "looking down on Sam from the attic hatch")],
           "rain on the roof and creaking wood; low drums on the soundtrack getting faster; then a cat miaows")
def swap_card(who, mine, theirs):
    t, shots, snd = mine
    rows = "".join(f"<tr><td>Shot {i}</td><td><b>{a}</b>: {b}</td></tr>" for i, (a, b) in enumerate(shots, 1))
    boxes = "".join(f"<div class='sbx'><span>Shot {i}</span></div>" for i in range(1, 5))
    return f"""<div class="idc"><h3>Student {who} · Storyboard Swap</h3>
    <p style="font-size:8.8pt;margin:0 0 1mm"><b>1. Read your scene aloud</b>, slowly, shot by shot. Don't show your card.</p>
    <div class="pass" style="font-size:8.8pt">{t}<table class="st" style="margin-top:1mm"><tbody>{rows}<tr><td>Sound</td><td>{snd}</td></tr></tbody></table></div>
    <p style="font-size:8.8pt;margin:1mm 0"><b>2. Listen to your partner's scene.</b> Sketch each shot in a box (stick figures are fine), write the shot or technique under it, and note the sounds: which are diegetic (D) and which non-diegetic (N)?</p>
    <div class="sbs">{boxes}</div>
    <p style="font-size:8.8pt;margin:1mm 0"><b>3. Together:</b> which shot in each scene builds the most tension? Why?</p></div>"""

FIX = [("The camera shows the boy in the field.", "no technique named; which shot? (e.g. “an extreme long shot makes him look tiny and alone in the empty field”)"),
       ("There is music in this scene and it is good.", "name the kind of music and its effect: “slow piano on the soundtrack makes the scene sad”"),
       ("Then she goes home and then her dad is there and then they talk.", "plot retelling, no technique: one sentence of plot, then the film language"),
       ("A close-up is when the camera is close.", "defines the term but says nothing about this scene: what does the close-up show us?"),
       ("The low angle makes him look small.", "wrong effect: a low angle looks up, so he looks big and powerful"),
       ("The music is diegetic because it is sad.", "diegetic means the characters can hear it, not the mood: is it a radio in the scene, or the soundtrack?")]

EXP = ("<b>The Lighthouse</b> (an imaginary film). Night. Ruth (15) climbs the lighthouse steps to light the lamp her grandfather always lit. "
       "<b>Shot 1:</b> a bird's-eye view of the spiral staircase, Ruth tiny at the bottom. "
       "<b>Shot 2:</b> quick cuts: her feet on the steps, her hand on the rail, the storm through a window. "
       "<b>Shot 3:</b> a flashback: Ruth, aged five, on her grandfather's shoulders at the top. "
       "<b>Shot 4:</b> a close-up of her face lit gold as the lamp turns on. "
       "<b>Sound:</b> wind and her breathing (diegetic); the soundtrack is silent until the lamp lights, then strings swell.")

pack = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Film: Camera Shots, Sound &amp; Key Scenes Teacher Pack | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{PACK_STYLE}
{EXTRA}
.fym{{grid-template-columns:repeat(4,1fr)}}.fym .c{{height:auto;padding:5mm 2.5mm 2.5mm;display:block}}.fym svg.fr{{border-width:1px}}
.idc{{padding:2mm 4mm;margin-bottom:3mm}}.idc h3{{margin:0 0 1mm}}.sbs{{display:grid;grid-template-columns:repeat(4,1fr);gap:3mm}}
.sbx{{border:1.5px solid #1B2430;height:26mm;position:relative;border-radius:3px}}.sbx span{{position:absolute;bottom:-4.5mm;left:0;font-size:7.5pt;color:var(--muted)}}
.idc .sbs{{margin-bottom:5mm}}.p1 .proc td{{font-size:8.6pt;padding:2px 6px}}
.ws .eh td{{font-size:8.6pt;padding:2px 6px}}.ws .eh .gap{{height:13px}}.ws ol.q li{{margin-bottom:1px}}
.pmini{{display:grid;grid-template-columns:repeat(5,1fr);gap:3mm;margin:4mm 0}}.pmini b{{display:block;text-align:center;font-size:12pt;margin-top:2mm}}
.prow{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:4mm}}.prow div{{border-radius:14px;padding:5mm 3mm;text-align:center;font-size:12pt;line-height:1.45}}.prow b{{display:block;font-size:17pt}}
</style></head><body>

<div class="page p1">
  <div class="band"><div><div class="k">Junior Cycle English · Teacher pack</div><h1>Film: shots, sound &amp; key scenes</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2015 specification): {LO}</p>
  <div class="two">
    <div><h3>Aims</h3><p>By the end of the lesson students can name the five shot sizes and the main camera angles, tell diegetic from non-diegetic sound, recognise quick cuts, slow motion, flashback, fade and montage, and write about a key scene by naming a technique, describing the moment and explaining its effect.</p></div>
    <div><h3>In this pack</h3><p>p.1 Teacher notes · p.2 Shot Sort (20 cut-up frames) · p.3 Storyboard Swap A/B (pair listening + sketching) · p.4 Wall poster · p.5 Worksheet: Fix the Answer + exam-style questions · p.6 Answers. Level: 3rd year. Time: about 60 minutes. Works with any studied film: every frame and scene here is made up by Léim.</p></div>
  </div>
  <h2 style="margin-top:8px">Procedure</h2>
  <table class="proc"><tbody>
    <tr><td>5 min</td><td><b>Lead-in.</b> Make a frame with your hands and “film” a student from across the room, then from close up. What can we see each time? What do we feel? Introduce shot sizes and angles (poster, p.4).</td></tr>
    <tr><td>12 min</td><td><b>Shot Sort</b> (p.2, groups of 3, one set of 20 frames). Sort into five piles from furthest to closest: extreme long shot, long shot, medium shot, close-up, extreme close-up. 4 cards in each pile. Then pick one card and say what that shot is good for.</td></tr>
    <tr><td>15 min</td><td><b>Storyboard Swap</b> (p.3, pairs). A reads a scene aloud shot by shot; B sketches it and labels the techniques and sounds. Swap. Which shot builds the most tension?</td></tr>
    <tr><td>5 min</td><td><b>Sound.</b> Play 30 seconds of the studied film with eyes closed. List every sound: diegetic or non-diegetic? What does the music tell us to feel?</td></tr>
    <tr><td>18 min</td><td><b>Worksheet</b> (p.5). Fix the Answer in pairs, then the exam-style questions on “The Lighthouse” alone.</td></tr>
    <tr><td>5 min</td><td><b>Exit ticket.</b> One key scene from the studied film + one technique in it + its effect. Homework: play <b>Shot Spotter</b> at {GAME}.</td></tr>
  </tbody></table>
  <div class="note"><b>Errors to look for:</b> “the camera shows” with no technique named · retelling the plot · mixing up low and high angle (low angle = camera low, looking <b>up</b>) · thinking diegetic means sad or happy music · naming a technique without its effect · not naming the film or director. <b>Support:</b> give the poster as a word bank. <b>Fast finishers:</b> storyboard the opening of their studied film in four shots.</div>
</div>

<div class="page">
  <div class="band"><div><div class="k">Groups of 3 · cut up the 20 frames</div><h1>Shot Sort</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.4pt;margin:0 0 2mm">Sort the frames into five piles, from furthest to closest: <b>extreme long shot</b>, <b>long shot</b>, <b>medium shot</b>, <b>close-up</b>, <b>extreme close-up</b>. Then choose one frame from each pile: what would that shot be good for in a film?</p>
  <div class="fym">{cards_html}</div>
</div>

<div class="page">
  <div class="band"><div><div class="k">Pairs · cut along the dashed line</div><h1>Storyboard Swap A/B</h1></div><div class="logo">↗ Léim</div></div>
  {swap_card("A", SCENE_A, SCENE_B)}
  {swap_card("B", SCENE_B, SCENE_A)}
</div>

<div class="page">
  <div class="poster">
    <h1>Every shot is a choice.</h1>
    <div class="pmini">{"".join(f"<div>{shot_svg(k)}<b>{SHOT[k]}</b></div>" for k in ["els", "ls", "ms", "cu", "ecu"])}</div>
    <p style="text-align:center;font-size:13pt!important;margin:0">further away = more <b>place</b> · closer = more <b>feeling</b></p>
    <div class="prow">
      <div style="background:var(--green-soft)"><b>Low angle</b>looks up:<br>powerful</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>High angle</b>looks down:<br>small, weak</div>
      <div style="background:var(--green-soft)"><b>Sound</b>diegetic: they hear it<br>non-diegetic: we do</div>
    </div>
    <p style="text-align:center;font-size:18pt!important;font-weight:800;margin:4mm 0">Name it. Describe it. Say what it does.</p>
    <p style="text-align:center;font-size:10pt;color:var(--muted)">Léim · leim.ie · Play Shot Spotter: {GAME}</p>
  </div>
</div>

<div class="page ws">
  <div class="band"><div><div class="k">Worksheet · exam-style questions</div><h1>Fix the Answer</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Fix the Answer</h2>
  <p>Each line comes from a weak answer about a film. Say what's wrong and write a better version.</p>
  <table class="eh"><thead><tr><th>Weak answer</th><th>What's wrong and a better version</th></tr></thead><tbody>
  {"".join(f"<tr><td style='font-weight:500'>{s}</td><td><span class='gap'></span><span class='gap'></span></td></tr>" for s, r in FIX)}
  </tbody></table>
  <h2>B. Exam-style questions: a key scene</h2>
  <div class="pass">{EXP}</div>
  <ol class="q">
    <li>Why do you think the director uses a bird's-eye view in Shot 1?<span class="long"></span><span class="long"></span></li>
    <li>How do the quick cuts in Shot 2 affect the audience?<span class="long"></span><span class="long"></span></li>
    <li>Why is the flashback placed here, in the middle of the climb?<span class="long"></span><span class="long"></span></li>
    <li>Explain the difference between the diegetic and non-diegetic sound in this scene. Why does the soundtrack stay silent until the lamp lights?<span class="long"></span><span class="long"></span></li>
    <li>Choose a key scene from a film you have studied. Name two techniques the director uses and explain the effect of each.<span class="long"></span><span class="long"></span><span class="long"></span></li>
  </ol>
</div>

<div class="page an">
  <div class="band"><div><div class="k">For the teacher</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>Shot Sort (ELS extreme long shot, LS long shot, MS medium shot, CU close-up, ECU extreme close-up)</h2>
  <p style="font-size:8.6pt">{cards_key}. Good for: ELS where we are; LS what someone is doing; MS two people talking; CU feelings; ECU a detail or a strong feeling.</p>
  <h2>Storyboard Swap</h2>
  <p style="font-size:9pt"><b>A (The Match):</b> {", ".join(a for a, b in SCENE_A[1])}; diegetic: the crowd's silence and roar; non-diegetic: the heartbeat. <b>B (The Attic):</b> {", ".join(a for a, b in SCENE_B[1])}; diegetic: rain, creaking, the cat; non-diegetic: the drums. Most tension: for example the low angle on the goalkeeper (he looks huge) and the point-of-view shot in the dark attic (we don't know what's there).</p>
  <h2>A. Fix the Answer</h2>
  <table><tbody>{"".join(f"<tr><td style='width:36%'>{s}</td><td>{r}</td></tr>" for s, r in FIX)}</tbody></table>
  <h2>B. Exam-style questions</h2>
  <ol class="q">
    <li>Looking straight down the spiral makes the climb look long and dizzying, and Ruth tiny at the bottom: the task seems huge for one girl.</li>
    <li>The short, fast shots speed up the pace and build tension: we feel her rush and her nerves as the storm rages.</li>
    <li>It reminds us why the climb matters: she is doing it for her grandfather, so the moment becomes about memory and love, not just the storm.</li>
    <li>Diegetic: the wind and her breathing (Ruth can hear them); non-diegetic: the strings (added for us). The silence keeps the tension and makes us listen to her breathing; when the strings swell as the lamp lights, it feels like a release and a victory.</li>
    <li>Reward: a specific scene; two techniques correctly named; each described at a moment and linked to its effect on the audience; film title and director named; little plot retelling.</li>
  </ol>
  <h2>Marking tip</h2>
  <p>Answers on the studied film are rewarded for knowledge of the text, use of film terms and a clear, supported response to the question. Our guide, not an official marking scheme.</p>
</div>
</body></html>"""

cover = """<!doctype html><html><head><meta charset="utf-8"><style>
body{margin:0;width:1200px;height:1200px;background:#1B2430;font-family:Inter,sans-serif;color:#fff;display:flex;flex-direction:column;justify-content:space-between;padding:90px;box-sizing:border-box}
.k{display:inline-block;background:#2E7D57;border-radius:99px;padding:12px 26px;font-weight:700;font-size:28px;letter-spacing:.06em;text-transform:uppercase}
h1{font-size:96px;font-weight:800;line-height:1.25;letter-spacing:-.02em;margin:60px 0 20px}
h1 span{background:#F6CF5A;color:#1B2430;padding:0 18px;border-radius:14px}
.sub{font-size:40px;line-height:1.4;color:#DDE3EA}
.em{font-size:46px;margin-top:30px;font-weight:800;letter-spacing:.01em;color:#F6CF5A}
.foot{display:flex;justify-content:space-between;align-items:center;font-size:34px;font-weight:700}
.price{background:#F6CF5A;color:#1B2430;border-radius:16px;padding:14px 28px}
</style></head><body>
<div><span class="k">Junior Cycle English · Teacher pack</span>
<h1><span>Film: shots,</span><br><span>sound &amp; scenes</span></h1>
<div class="sub">Shot Sort · Storyboard Swap A/B<br>Poster · Worksheet + answers</div>
<div class="em">camera shots and angles<br>diegetic sound · editing</div></div>
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
    pdf("teacher-pack", os.path.join(OUT, "Film-Shots-Sound-Key-Scenes-Teacher-Pack-Leim.pdf"))
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--hide-scrollbars", "--window-size=1200,1200",
                    f"--screenshot={os.path.join(OUT, f'{SLUG}-cover.png')}", f"{SLUG}-cover.html"], cwd=SRC, check=True, capture_output=True)
