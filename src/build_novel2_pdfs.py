#!/usr/bin/env python3
"""The novel 2: setting, plot, structure & theme (JC English Order 14): free sheet (-> printables/), 6-page teacher pack + 1200x1200 cover (-> OUTDIR).
Usage: python3 src/build_novel2_pdfs.py /tmp/novel2
Items come from the game's data block (plot-line.html). Every answer is re-derived with the checker's own rules
(src/test_plot_line.py: stage, hits(TH/MO), trait) and asserted; the checker's data pass runs first.
Styles are read from src/build_money1_pdfs.py."""
import os, sys, random, subprocess, re
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC); sys.path.insert(0, SRC)
from test_plot_line import stage, stages, hits, trait, load, data_pass, TH, MO, ORDER
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/novel2"; os.makedirs(OUT, exist_ok=True)
SLUG = "novel-setting-plot-theme"
LO = "R6, R7, R9, W8"
GAME = "leim.ie/plot-line.html"
D = load(os.path.join(ROOT, "plot-line.html"))
assert not data_pass(D), data_pass(D)
SN = {"ex": "Exposition", "ri": "Rising action", "cl": "Climax", "fa": "Falling action", "re": "Resolution"}
TN = {"fr": "Friendship", "co": "Courage", "lo": "Loss", "be": "Belonging", "gr": "Growing up", "fa": "Fairness", "fo": "Forgiveness"}
MN = {"te": "Tense", "pe": "Peaceful", "jo": "Joyful", "gl": "Gloomy"}
CN = {"sh": "shy", "cf": "confident", "se": "selfish", "ge": "generous", "sc": "scared", "br": "brave", "lo": "lonely", "ac": "accepted"}
def th(s): h = hits(s, TH); assert len(h) == 1, (s, h); return h[0]
def mo(s): h = hits(s, MO); assert len(h) == 1, (s, h); return h[0]
def tr(s): h = trait(s); assert len(h) == 1, (s, h); return h[0]

# ---------- free sheet ----------
random.seed(1411)
arcs = random.sample(D["arcs"], 8)
A_items = []  # (line, stage)
for n, k in enumerate(["ri", "fa", "ex", "cl", "re", "fa"]):
    A_items.append((arcs[n]["lines"][ORDER.index(k)], k))
for s, k in A_items: assert stage(s) == k, (s, stages(s))
B_items = []
for A in arcs[6:8]:
    idx = [1, 2, 3, 4]
    while idx == [1, 2, 3, 4]: random.shuffle(idx)
    lets = "ABCD"; ans = " → ".join(lets[idx.index(n)] for n in (1, 2, 3, 4))
    rk = sorted(range(4), key=lambda j: {"ri": 1, "cl": 2, "fa": 3, "re": 4}[stage(A["lines"][idx[j]])])
    assert " → ".join(lets[j] for j in rk) == ans
    B_items.append((A, idx, ans))
C_items = [random.choice([x for x in D["theme"] if x[1] == k]) for k in ("co", "be", "lo", "fo", "gr")]
for s, k in C_items: assert th(s) == k
D_items = [random.choice([x for x in D["mood"] if x[1] == k]) for k in ("gl", "te", "jo", "pe")]
for s, k in D_items: assert mo(s) == k
E_items = random.sample(D["change"], 2)
for who, a, b, s, e in E_items: assert tr(a) == s and tr(b) == e
NQ = len(A_items) + len(B_items) + len(C_items) + len(D_items) + len(E_items) + 1; assert NQ == 20, NQ
nA = 1; nB = nA + len(A_items); nC = nB + len(B_items); nD = nC + len(C_items); nE = nD + len(D_items); nF = nE + len(E_items)

def style(var):
    return re.search(var + r' = f"""<!doctype.*?<style>(.*?)</style>', open(os.path.join(SRC, "build_money1_pdfs.py"), encoding="utf-8").read(), re.S).group(1).replace("{LO}", LO).replace("{{", "{").replace("}}", "}").replace("JC Maths LOs (2018 spec)", "JC English LOs (2015 spec)")
SHEET_STYLE = style("sheet"); PACK_STYLE = style("pack")
assert "JC English LOs (2015 spec)" in SHEET_STYLE and "Single-teacher licence" in PACK_STYLE and "JC English LOs (2015 spec)" in PACK_STYLE
EXTRA = """.wk{line-height:1.45;border:1.5px solid var(--line);border-radius:8px;padding:2px 7px;margin:3px 0;font-size:9.4pt}.wk b.h{display:block}
table.st{border-collapse:collapse;margin:3px 0;font-size:9.2pt;width:100%}table.st td,table.st th{border:1px solid #C9D1DA;padding:2px 6px;text-align:left}
.bank{border:1.5px solid var(--line);border-radius:8px;padding:4px 10px;margin:4px 0;text-align:center;font-weight:700;word-spacing:4px}
.pass{border-left:4px solid var(--green);background:var(--mist);padding:5px 10px;margin:4px 0;font-style:italic}
.sty{border:1.5px solid var(--line);border-radius:8px;padding:2px 7px;margin:2px 0 3px;font-size:8.8pt}.sty p{margin:0 0 1px}"""
ARC_SVG = """<svg viewBox="0 0 400 120" style="width:100%;max-width:90mm;display:block;margin:1mm auto"><polyline points="20,90 110,60 200,16 290,60 380,90" fill="none" stroke="#9AA3AE" stroke-width="4"/>
<g font-size="14" font-weight="800" fill="#1B2430" text-anchor="middle"><circle cx="20" cy="90" r="6" fill="#fff" stroke="#1B2430" stroke-width="2"/><text x="4" y="114" text-anchor="start">Exposition</text>
<circle cx="110" cy="60" r="6" fill="#fff" stroke="#1B2430" stroke-width="2"/><text x="110" y="84">Rising action</text>
<circle cx="200" cy="16" r="8" fill="#F6CF5A" stroke="#1B2430" stroke-width="2"/><text x="200" y="44">Climax</text>
<circle cx="290" cy="60" r="6" fill="#fff" stroke="#1B2430" stroke-width="2"/><text x="290" y="84">Falling action</text>
<circle cx="380" cy="90" r="6" fill="#fff" stroke="#1B2430" stroke-width="2"/><text x="396" y="114" text-anchor="end">Resolution</text></g></svg>"""
def li(i, s, w=16): return f"<li value='{i}'><i>{s}</i> <span class='line' style='min-width:{w}mm'></span></li>"
A_html = "".join(li(i, s) for i, (s, k) in enumerate(A_items, nA))
def order_html(A, idx):
    return f"<div class='sty'><p><b>{A['lines'][0]}</b></p>" + "".join(f"<p><b>{'ABCD'[j]}</b> {A['lines'][n]}</p>" for j, n in enumerate(idx)) + "</div>"
B_html = "".join(f"<li value='{i}'>Order: <span class='line' style='min-width:26mm'></span>{order_html(A, idx)}</li>" for i, (A, idx, a) in enumerate(B_items, nB))
C_html = "".join(li(i, s) for i, (s, k) in enumerate(C_items, nC))
D_html = "".join(li(i, s) for i, (s, k) in enumerate(D_items, nD))
E_html = "".join(f"<li value='{i}'><i>Start:</i> {a}<br><i>End:</i> {b}<br>At the start: <span class='line' style='min-width:18mm'></span> At the end: <span class='line' style='min-width:18mm'></span></li>" for i, (w, a, b, s, e) in enumerate(E_items, nE))
EX = ("Rain dripped from the bare trees as Dara walked past the old cinema for the last time. Since Grandad died, nobody had opened its rusty doors. "
      "Tomorrow the builders would knock it down. Dara had always been too shy to speak at the town meetings, but tonight he stood up in the packed hall.")
assert mo("Rain dripped from the bare trees as Dara walked past the old cinema.") == "gl"

sheet = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>The novel: setting, plot and theme, rules and practice | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{SHEET_STYLE}
{EXTRA}
.p2 ol.q li{{margin-bottom:1px;font-size:8.9pt}}.p2 h2{{margin:3px 0 1px}}.p2 .two{{gap:5mm}}.p2 .sty{{font-size:8.3pt;padding:1px 6px}}
</style></head><body>
<div class="page tight">
  <div class="band"><div><div class="k">Junior Cycle English · Free revision sheet</div><h1>The novel: plot, setting &amp; theme</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2015 specification): {LO}. Play the game: <b>{GAME}</b></p>
  <div class="two">
   <div><h2>1. The five stages of a plot</h2>{ARC_SVG}
    <table class="st"><thead><tr><th>Stage</th><th>What happens</th><th>Look for</th></tr></thead><tbody>
     <tr><td><b>Exposition</b></td><td>meet the characters, place, time</td><td><i>a frosty January morning in Tralee</i></td></tr>
     <tr><td><b>Rising action</b></td><td>trouble starts and gets worse</td><td>lost, broken, missed, ruined, refused</td></tr>
     <tr><td><b>Climax</b></td><td>the turning point</td><td>Suddenly · Just then · At that moment</td></tr>
     <tr><td><b>Falling action</b></td><td>what happens after it</td><td>After that · Afterwards · Slowly · Bit by bit</td></tr>
     <tr><td><b>Resolution</b></td><td>how it all ends</td><td>In the end · At last · From that day on</td></tr></tbody></table>
    <p style="font-size:8.8pt">In a novel each stage can last for chapters. The climax is the moment the whole book builds towards.</p></div>
   <div><h2>2. Setting and mood</h2>
    <div class="wk">The <b>setting</b> is where and when. The <b>mood</b> is the feeling it creates. Look at sounds, weather and light:<br>
    <b>tense</b> <i>(creaked, shadow, footsteps)</i> · <b>peaceful</b> <i>(gently, still, softly)</i> · <b>joyful</b> <i>(music, laughed, bunting)</i> · <b>gloomy</b> <i>(grey, drizzle, empty)</i></div>
    <h2>3. Theme</h2>
    <div class="wk">The <b>topic</b> is what the novel is about (<i>a dog, a war, a new school</i>). The <b>theme</b> is the big idea about life it shows (<i>friendship can be found anywhere</i>).
    Common themes: friendship, courage, loss, belonging, growing up, fairness, forgiveness.</div>
    <h2>4. Character change</h2>
    <div class="wk">Compare the start with the end. <i>Start: Leah whispered her answers and hid at the back.</i> <i>End: she volunteered to give the speech.</i> Leah changes from <b>shy</b> to <b>confident</b>. Then ask: what changed her?</div>
    <div class="note"><b>Classic mistakes:</b> retelling the whole plot · no quote or reference · calling the topic a theme · "the setting is a house" with no detail or mood · forgetting the name of the novel and the author.</div></div>
  </div>
  <div class="tip"><b>Exam tip:</b> for every key moment and theme in your novel, learn two short quotes. A good paragraph = the point, a quote, and a sentence on why it matters.</div>
</div>

<div class="page p2">
  <div class="band"><div><div class="k">Practice · {NQ} questions</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <div class="two"><div><h2>A. Which stage of the plot?</h2><div class="bank" style="font-size:8.2pt">Exposition · Rising action · Climax · Falling action · Resolution</div><ol class="q">{A_html}</ol>
  <h2>C. Which theme?</h2><div class="bank" style="font-size:8.2pt">{" · ".join(TN[k] for s, k in sorted(C_items, key=lambda x: x[1]))}</div><ol class="q">{C_html}</ol>
  <h2>D. Which mood?</h2><div class="bank" style="font-size:8.2pt">Tense · Peaceful · Joyful · Gloomy</div><ol class="q">{D_html}</ol></div>
  <div><h2>B. Put the plot in order (line 1 comes first)</h2><ol class="q">{B_html}</ol>
  <h2>E. How does the character change? (one word each)</h2><ol class="q">{E_html}</ol></div></div>
  <h2>F. Exam-style</h2>
  <div class="pass">{EX}</div>
  <ol class="q"><li value="{nF}">What mood does the setting create? Quote one detail. Which theme might this novel explore? Where in the plot might the last sentence come?<span class="long"></span><span class="long"></span></li></ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">Check your work</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <table class="ans"><tbody>
   <tr><td><b>A</b></td><td>{" · ".join(f"{i}. {SN[k]}" for i, (s, k) in enumerate(A_items, nA))}</td></tr>
   <tr><td><b>B</b></td><td>{" · ".join(f"{i}. {a}" for i, (A, idx, a) in enumerate(B_items, nB))} (rising action → climax → falling action → resolution)</td></tr>
   <tr><td><b>C</b></td><td>{" · ".join(f"{i}. {TN[k]}" for i, (s, k) in enumerate(C_items, nC))}</td></tr>
   <tr><td><b>D</b></td><td>{" · ".join(f"{i}. {MN[k]}" for i, (s, k) in enumerate(D_items, nD))}</td></tr>
   <tr><td><b>E</b></td><td>{" · ".join(f"{i}. {CN[s]} → {CN[e]}" for i, (w, a, b, s, e) in enumerate(E_items, nE))}</td></tr>
   <tr><td><b>F</b></td><td>{nF}. Gloomy: "rain dripped from the bare trees", "rusty doors". Themes: loss (Grandad has died, the cinema is going), courage or growing up (Dara stands up although he is shy). The last sentence feels like the climax or the start of it: the moment Dara finally acts.</td></tr>
  </tbody></table>
  <h2>Worked examples</h2>
  <div class="two">
   <div class="wk"><b class="h">Naming the stage</b><i>"Just then, Mr Flynn's dog slipped its lead and ran towards the busy road."</i> This is the <b>climax</b>: "Just then" signals the turning point, and after it Tadhg and Mr Flynn are never enemies again.</div>
   <div class="wk"><b class="h">Setting and mood with evidence</b>The lighthouse is empty and cold. "Grey rain dripped from the bare trees" creates a gloomy, lonely mood that matches Nell's grief.</div>
   <div class="wk"><b class="h">Theme, not topic</b>Not: "The theme is a lighthouse." Better: "One theme is courage: Nell goes in although her hands are shaking, because the boats need the light."</div>
   <div class="wk"><b class="h">Writing about change</b>1. Name the character and the novel. 2. Before, with a quote. 3. The key moment. 4. After, with a quote. 5. What caused it and what it shows.</div>
  </div>
  <div class="note"><b>Got one wrong?</b> Go back to page 1, then play <b>Plot Line</b> at {GAME}: the "Go back over these" list at the end explains each mistake.</div>
  <p class="small">All sentences and extracts written by Léim. Léim is independent and not connected with the State Examinations Commission or the NCCA.</p>
</div>
</body></html>"""

# ---------- teacher pack ----------
random.seed(1412)
JIG = random.sample(D["arcs"], 4)
cards = [(A["lines"][j], pi, j) for pi, A in enumerate(JIG) for j in range(5)]
for s, pi, j in cards: assert stage(s) == ORDER[j], (s, stages(s))
assert len({s for s, a, b in cards}) == 20
random.seed(1413); random.shuffle(cards)
jig_html = "".join(f'<div class="c"><span class="tag">Card {k}</span><div class="fc sm">{s}</div></div>' for k, (s, pi, j) in enumerate(cards, 1))
jig_key = "".join(f"<li><b>{A['k'].split(' ', 1)[1]}</b>: cards {' → '.join(str(next(k for k, (s, a, b) in enumerate(cards, 1) if a == pi and b == j)) for j in range(5))}</li>" for pi, A in enumerate(JIG))

# Novel Swap: each "novel" = setting line (mood), 5 plot lines, a start/end pair for change, a theme moment
SWAP_A = dict(name="The Lighthouse Summer",
    setting="Small waves lapped gently against the harbour wall below the lighthouse.",
    plot=["It was the first day of the summer holidays, and Ruth had been sent to stay with her aunt on Inis Mór.",
          "She missed her phone signal, her friends and her bed, and she refused to leave her room.",
          "Suddenly, a storm blew up, and the island's only ferry was stranded at the pier with a group of tourists on board.",
          "After that, Ruth helped her aunt carry food and blankets down to the pier for a week.",
          "In the end, Ruth cried when the ferry came to take her home."],
    start="At the start, Ruth wouldn't share her room with her cousin.", end="By the end, she gave her cousin her favourite jumper.",
    theme="For the first time, Ruth was trusted to row the boat out on her own.",
    want=("pe", ["ex", "ri", "cl", "fa", "re"], "se", "ge", "gr"))
SWAP_B = dict(name="The Night Match",
    setting="Grey clouds hung low over the empty pitch in Clones.",
    plot=["On a freezing November evening, Odhrán's under-16 team trained for the county final.",
          "Their coach was injured in a fall, and the club wanted to cancel the final.",
          "At that moment, Odhrán's quiet grandad walked onto the pitch with a whistle round his neck.",
          "Slowly, the old man taught them the tricks he had used as a player.",
          "Finally, the team won the final, and Grandad was carried round the pitch."],
    start="At the start, Odhrán never spoke in the dressing room.", end="By the end, he led the team out onto the pitch.",
    theme="When the whole team sang his name, Grandad knew he was one of them again.",
    want=("gl", ["ex", "ri", "cl", "fa", "re"], "sh", "cf", "be"))
for S in (SWAP_A, SWAP_B):
    m, st, a, b, t = S["want"]
    assert mo(S["setting"]) == m, S["name"]
    assert [stage(x) for x in S["plot"]] == st, (S["name"], [stages(x) for x in S["plot"]])
    assert tr(S["start"]) == a and tr(S["end"]) == b, (S["name"], trait(S["start"]), trait(S["end"]))
    assert th(S["theme"]) == t, (S["name"], hits(S["theme"], TH))
def swap_card(who, mine, theirs):
    return f"""<div class="idc"><h3>Student {who} · Novel Swap</h3>
    <p style="font-size:8.6pt;margin:0 0 1mm"><b>1. Read the summary of your novel aloud twice</b>, slowly. Your partner can't see it.</p>
    <div class="pass" style="font-size:9.6pt"><b style="font-style:normal">"{mine['name']}"</b><br>{mine['setting']} {" ".join(mine['plot'])} {mine['start']} {mine['end']} {mine['theme']}</div>
    <p style="font-size:8.6pt;margin:1mm 0"><b>2. Then listen</b> to "{theirs['name']}" and fill in the grid:</p>
    <table class="st" style="font-size:8.6pt"><tbody>{"".join(f"<tr><td style='width:36%'><b>{n}</b></td><td></td></tr>" for n in ["Setting: where and when?", "The mood (one word + a clue)", "The climax", "The resolution", "The main character: start → end", "One theme + the clue"])}</tbody></table>
    <p style="font-size:8.6pt;margin:1mm 0 0"><b>3. Check:</b> read your grid back. Did you get the climax and the theme?</p></div>"""

FIX = [("“The novel is about a boy who moves house and then he goes to school and then he meets a dog and then…”", "Retelling the plot. Pick <b>one</b> key moment and say why it matters."),
       ("“The theme of the novel is a dog.”", "That's the topic. A theme is an idea: <b>friendship can be found in unexpected places</b>."),
       ("“The setting is a house.”", "No detail, no mood. Say where and when, quote a detail and name the mood it creates."),
       ("“Nell is brave.” (nothing else)", "A point with no proof. Add a quote and explain it: <b>her hands were shaking, but she struck the match</b>."),
       ("“The climax is at the end of the book.”", "Too vague. Name the moment and say why it is the turning point."),
       ("“In the book the girl changes.”", "Name the novel, the author and the character, and say <b>from what to what</b>, with a quote for each.")]

MARKET = ["The Saturday market in Ennis had always been full of music and laughter, but this year half the stalls stood empty.",
          "Cathal's mam had run the bakery stall for twenty years, until the new supermarket opened and her customers stopped coming.",
          "Cathal had always been embarrassed by the stall and hid behind it when his friends walked past.",
          "Now, watching his mam pack away the unsold loaves, he felt something he couldn't name.",
          "On the Monday, he set up a stand at school selling her bread at break time.",
          "By Friday, there was a queue out the door, and his friends were the ones serving."]
assert mo("but this year half the stalls stood empty") == "gl" and mo("full of music and laughter") == "jo"

pack = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>The Novel: Setting, Plot &amp; Theme Teacher Pack | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{PACK_STYLE}
{EXTRA}
.fym .c{{height:40mm}}.fym .fc.sm{{font-size:10pt;line-height:1.3;margin-top:2mm;font-weight:600}}.idc{{padding:2mm 4mm;margin-bottom:3mm}}.idc h3{{margin:0 0 1mm}}
.idc .st td{{height:5mm;padding:1px 6px}}.p1 .proc td{{font-size:8.6pt;padding:2px 6px}}.ops div{{font-size:11pt;padding:5mm 3mm}}.ops b{{font-size:17pt}}
.ws .eh td{{font-size:8.6pt;padding:2px 6px}}.ws .eh .gap{{height:13px}}.ws ol.q li{{margin-bottom:1px}}
</style></head><body>

<div class="page p1">
  <div class="band"><div><div class="k">Junior Cycle English · Teacher pack</div><h1>The novel: setting, plot &amp; theme</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2015 specification): {LO}</p>
  <div class="two">
    <div><h3>Aims</h3><p>By the end of the lesson students can name the five stages of a plot, say what mood a setting creates and quote the details that create it, tell a theme from a topic, and describe how a character changes from the start to the end of a novel, with evidence.</p></div>
    <div><h3>In this pack</h3><p>p.1 Teacher notes · p.2 Plot Jigsaw cards (cut-up) · p.3 Novel Swap A/B (speaking + listening) · p.4 Wall poster · p.5 Worksheet: Fix the Answer + exam-style questions · p.6 Answers. Level: 2nd year (works alongside any novel on your course). Time: about 60 minutes. All texts are original.</p></div>
  </div>
  <h2 style="margin-top:8px">Procedure</h2>
  <table class="proc"><tbody>
    <tr><td>5 min</td><td><b>Lead-in.</b> Draw a mountain on the board. Ask: where on it is the most exciting moment of the novel you are reading? Where does it start? Where does it end?</td></tr>
    <tr><td>8 min</td><td><b>Guided discovery.</b> Elicit the five stages and the signal words for each (Suddenly / After that / In the end). Then mood (tense, peaceful, joyful, gloomy) and the difference between a topic and a theme.</td></tr>
    <tr><td>12 min</td><td><b>Plot Jigsaw</b> (p.2, groups of 3–4, one set of 20 cards). Rebuild the 4 mini-novels in order: exposition → rising action → climax → falling action → resolution. Fast groups: give each story a theme.</td></tr>
    <tr><td>15 min</td><td><b>Novel Swap</b> (p.3, pairs). A reads a novel summary aloud; B fills the grid (setting, mood, climax, resolution, change, theme). Swap. Check together.</td></tr>
    <tr><td>15 min</td><td><b>Worksheet</b> (p.5). Fix the Answer in pairs, then the exam-style questions on "The Market" alone.</td></tr>
    <tr><td>5 min</td><td><b>Exit ticket.</b> Your class novel: name its climax in one sentence and one theme with a quote. Homework: play <b>Plot Line</b> at {GAME}.</td></tr>
  </tbody></table>
  <div class="note"><b>Errors to look for:</b> retelling the plot instead of making a point · naming a topic as a theme · "the setting is a house" with no mood · calling the last chapter the climax · points with no quote. <b>Support:</b> the poster (p.4) on the desk; give weaker groups the 4 exposition cards first. <b>Fast finishers:</b> map your class novel onto the five stages, one sentence each.</div>
  <p class="small"><b>Plot Jigsaw key</b> (exposition → rising action → climax → falling action → resolution):</p><ul class="small" style="columns:2;margin:0">{jig_key}</ul>
</div>

<div class="page">
  <div class="band"><div><div class="k">Groups of 3–4 · cut up the 20 cards</div><h1>Plot Jigsaw</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.4pt;margin:0 0 2mm">The cards make <b>4 mini-novels</b>. Rebuild each one in order: <b>exposition → rising action → climax → falling action → resolution</b>. Which words helped you?</p>
  <div class="fym">{jig_html}</div>
</div>

<div class="page">
  <div class="band"><div><div class="k">Pairs · cut along the dashed line</div><h1>Novel Swap A/B</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.4pt">Each card is the summary of a short novel. Listen for the setting, the mood, the plot, how the main character changes and a theme.</p>
  {swap_card("A", SWAP_A, SWAP_B)}
  {swap_card("B", SWAP_B, SWAP_A)}
</div>

<div class="page">
  <div class="poster">
    <h1>Find the shape of the story.</h1>
    {ARC_SVG.replace('max-width:90mm', 'max-width:160mm')}
    <div class="ops">
      <div style="background:var(--green-soft)"><b>Setting</b>where and when<br>what mood?</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Plot</b>five stages<br>find the climax</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Theme</b>the big idea<br>not the topic</div>
      <div style="background:var(--green-soft)"><b>Change</b>start → end<br>what changed them?</div>
    </div>
    <p style="text-align:center;font-size:18pt!important;font-weight:800;margin:4mm 0">Point. Quote. Explain.</p>
    <p style="text-align:center;font-size:10pt;color:var(--muted)">Léim · leim.ie · Play Plot Line: {GAME}</p>
  </div>
</div>

<div class="page ws">
  <div class="band"><div><div class="k">Worksheet · exam-style questions</div><h1>Fix the Answer</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Fix the Answer</h2>
  <p>Each answer about a novel has a problem. Say what's wrong and how to fix it.</p>
  <table class="eh"><thead><tr><th>The student wrote</th><th>What's wrong and the fix</th></tr></thead><tbody>
  {"".join(f"<tr><td style='font-weight:500'>{s}</td><td><span class='gap'></span><span class='gap'></span></td></tr>" for s, r in FIX)}
  </tbody></table>
  <h2>B. Exam-style questions: "The Market"</h2>
  <div class="pass">{" ".join(MARKET)}</div>
  <ol class="q">
    <li>How has the setting changed? Quote two details.<span class="long"></span></li>
    <li>What is the problem in this extract?<span class="long"></span></li>
    <li>Which sentence is the turning point for Cathal? Explain your choice.<span class="long"></span></li>
    <li>How does Cathal change? Use the text.<span class="long"></span></li>
    <li>Name one theme of the extract and explain how it is shown.<span class="long"></span><span class="long"></span></li>
  </ol>
</div>

<div class="page an">
  <div class="band"><div><div class="k">For the teacher</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>Plot Jigsaw</h2>
  <ul style="columns:2;margin:0">{jig_key}</ul>
  <h2>Novel Swap</h2>
  <p><b>{SWAP_A['name']}:</b> Inis Mór, the summer holidays · Peaceful ("lapped gently") · Climax: a storm strands the ferry and its tourists · Resolution: Ruth cries when the ferry comes to take her home · selfish → generous · Growing up ("for the first time… on her own").</p>
  <p><b>{SWAP_B['name']}:</b> a pitch in Clones, a November evening · Gloomy ("grey clouds", "empty pitch") · Climax: Grandad walks onto the pitch with a whistle · Resolution: the team wins and carries Grandad round the pitch · shy → confident · Belonging ("he was one of them again").</p>
  <h2>A. Fix the Answer</h2>
  <table><tbody>{"".join(f"<tr><td style='width:40%'>{s}</td><td>{r}</td></tr>" for s, r in FIX)}</tbody></table>
  <h2>B. Exam-style questions</h2>
  <ol class="q">
    <li>It used to be lively ("full of music and laughter") but now it is gloomy and quiet ("half the stalls stood empty").</li>
    <li>The new supermarket has taken his mam's customers, and her bakery stall is failing.</li>
    <li>"Now, watching his mam pack away the unsold loaves, he felt something he couldn't name." Seeing his mam's loss changes how he feels, and everything after it follows from that moment.</li>
    <li>From embarrassed (he "hid behind" the stall) to proud and active: he sets up a stand at school, and his friends end up "serving".</li>
    <li>Credit family, loyalty, change or growing up, with a quote and a sentence on how it is shown (e.g. Cathal takes responsibility for helping his mam).</li>
  </ol>
  <h2>Marking tip</h2>
  <p>Reward a clear point + a short quote or close reference + a sentence on why it matters, more than length. Retelling the plot with no point earns little. Our guide, not an official marking scheme.</p>
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
<h1><span>The novel:</span><br><span>plot &amp; theme</span></h1>
<div class="sub">Plot Jigsaw cards · Novel Swap A/B<br>Poster · Worksheet + answers</div>
<div class="em">five stages · setting &amp; mood<br>theme · character change</div></div>
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
    pdf("teacher-pack", os.path.join(OUT, "Novel-Setting-Plot-Theme-Teacher-Pack-Leim.pdf"))
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--hide-scrollbars", "--window-size=1200,1200",
                    f"--screenshot={os.path.join(OUT, f'{SLUG}-cover.png')}", f"{SLUG}-cover.html"], cwd=SRC, check=True, capture_output=True)
