#!/usr/bin/env python3
"""Non-literary & visual texts (JC English Order 31): free sheet (-> printables/), 6-page teacher pack + 1200x1200 cover (-> OUTDIR).
Usage: python3 src/build_nonliterary_pdfs.py /tmp/p31
Reads the game's data block (fact-or-opinion.html) and re-checks every answer with the checker's own functions
(src/test_fact_or_opinion.py: kind, judgements, measure, name_parts). The checker's data pass runs first.
Styles are read from src/build_money1_pdfs.py."""
import os, sys, random, subprocess, re
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC); sys.path.insert(0, SRC)
from test_fact_or_opinion import load, data_pass, kind, judgements, measure, name_parts, FO
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/p31"; os.makedirs(OUT, exist_ok=True)
SLUG = "non-literary-visual-texts"
LO = "R3, R9, R12, OL8"
GAME = "leim.ie/fact-or-opinion.html"
D = load(os.path.join(ROOT, "fact-or-opinion.html")); data_pass(D)
F, O = "Fact", "Opinion"
def ko(s): return F if kind(s) == FO[0] else O

def style(var):
    return re.search(var + r' = f"""<!doctype.*?<style>(.*?)</style>', open(os.path.join(SRC, "build_money1_pdfs.py"), encoding="utf-8").read(), re.S).group(1).replace("{LO}", LO).replace("{{", "{").replace("}}", "}").replace("JC Maths LOs (2018 spec)", "JC English LOs (2015 spec)")
SHEET_STYLE = style("sheet"); PACK_STYLE = style("pack")
assert "JC English LOs (2015 spec)" in SHEET_STYLE and "Single-teacher licence" in PACK_STYLE and "JC English LOs (2015 spec)" in PACK_STYLE
EXTRA = """.wk{line-height:1.4;border:1.5px solid var(--line);border-radius:8px;padding:2px 7px;margin:3px 0;font-size:9.2pt}.wk b.h{display:block}
table.st{border-collapse:collapse;margin:3px 0;font-size:9pt;width:100%}table.st td,table.st th{border:1px solid #C9D1DA;padding:2px 6px;text-align:left;vertical-align:top}
.pass{border-left:4px solid var(--green);background:var(--mist);padding:5px 10px;margin:4px 0;font-size:9.3pt;line-height:1.5}
.pass .sp{display:block;margin:1px 0}.qt{font-family:Georgia,serif;font-style:italic}.tc{border:1.5px solid var(--line);border-radius:8px;padding:3px 8px;margin:3px 0;font-size:9.2pt;line-height:1.45}.tc .k{font-size:8pt;font-weight:700;color:var(--muted)}
svg.ch{display:block;width:100%;max-width:92mm;margin:2px auto}
.post{border:2.5px solid #1B2A3A;border-radius:4px;padding:3px 8px;background:#FFFDF5;font-size:9pt;line-height:1.35}
.post .h{font-size:14pt;font-weight:800;text-transform:uppercase;color:#B4322E}.post .pic{font-size:9pt;background:#EAF3FB;padding:3px;text-align:center;color:#55606C}.post .cap{font-size:8pt;font-style:italic;color:#55606C}
.post div{margin:2px 0}.post .lab{display:inline-block;min-width:14px;font-weight:800;color:var(--green)}"""
L = "<span class='line' style='min-width:22mm'></span>"
def li(i, s): return f"<li value='{i}'>{s}</li>"
def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;")

# ---------- the same bar chart the game draws (measured back with the checker's measure()) ----------
X0, X1, Y0, TOP, MAXV = 56, 390, 214, 24, 50; S = (Y0 - TOP) / MAXV
def chart(G, blank=False):
    n = len(G["bars"]); w = (X1 - X0) / n
    s = f'<svg class="ch" viewBox="0 0 400 264"><text x="200" y="14" text-anchor="middle" font-size="16" font-weight="700" fill="#1B2A3A">{esc(G["title"])}</text>'
    for v in range(0, MAXV + 1, 10):
        y = Y0 - v * S
        s += f'<g class="tick"><line x1="{X0}" x2="{X1}" y1="{y}" y2="{y}" stroke="#C9D1DA"{"" if not v else " stroke-dasharray=\"3 3\""}/><text x="{X0-6}" y="{y+5}" text-anchor="end" font-size="15" fill="#55606C">{v}</text></g>'
        if v < MAXV: s += f'<line x1="{X0}" x2="{X1}" y1="{Y0-(v+5)*S}" y2="{Y0-(v+5)*S}" stroke="#E6EAEE"/>'
    for i, (lab, val) in enumerate(G["bars"]):
        h = val * S; x = X0 + i * w + w * .18; bw = w * .64
        if not blank: s += f'<rect class="bar" x="{x:.1f}" y="{Y0-h:.2f}" width="{bw:.1f}" height="{h:.2f}" rx="3" fill="#4C8BC9"/>'
        s += f'<text class="bl" x="{x+bw/2:.1f}" y="{Y0+20}" text-anchor="middle" font-size="15" fill="#1B2A3A">{esc(lab)}</text>'
    mid = (Y0 + TOP) / 2
    s += f'<text x="14" y="{mid}" font-size="14" fill="#55606C" transform="rotate(-90 14 {mid})" text-anchor="middle">{esc(G["y"])}</text></svg>'
    if not blank: assert measure(s) == dict(G["bars"]), G["title"]
    return s

def poster(P, order, labels=None):
    cls = {"head": "h", "img": "pic", "cap": "cap", "when": "w", "con": "c"}
    body = []
    for i, k in enumerate(order):
        t = P[k] if k != "img" else f"[picture: {P['img_txt']}]"
        lab = f"<span class='lab'>{labels[i]}</span> " if labels else ""
        body.append(f"<div class='{cls[k]}'>{lab}{esc(t)}</div>")
    return "<div class='post'>" + "".join(body) + "</div>"
PIC = {"Spooky Night Walk": "a pumpkin and a torch", "Summer Surf Camp": "a surfer on a wave", "Big Book Swap": "piles of books",
       "Talent Show Auditions": "a microphone and a guitar", "Tidy Towns Clean-Up": "gloves and a bin", "Christmas Craft Fair": "a tree and wool",
       "Free Bike Repair Day": "a bike and a spanner", "Dog Show": "a dog and a trophy", "Science Week Open Night": "a microscope",
       "Coastal Bird Watch": "a bird and binoculars", "Junior Chess Tournament": "a chess piece and a medal", "Fun Run for the Hospice": "a runner"}
for P in D["posters"]: P["img_txt"] = PIC[P["head"]]
PNAME = {"head": "Headline", "img": "Picture", "cap": "Caption", "when": "When & where", "con": "Contact details"}

# ---------- free sheet ----------
rng = random.Random(3101)
A_items = rng.sample(D["fo"]["f"], 5) + rng.sample(D["fo"]["o"], 5); rng.shuffle(A_items)
SP = rng.sample(D["spot"], 2)
B_items = []
for T in SP:
    ks = [ko(l) for l in T["lines"]]; odd = min(set(ks), key=ks.count); B_items.append((T, odd, ks.index(odd) + 1))
G1 = rng.choice(D["charts"]); V = dict(G1["bars"]); labs = list(V)
hi = max(V, key=V.get); lo = min(V, key=V.get); a1, b1 = rng.sample(labs, 2)
if V[a1] < V[b1]: a1, b1 = b1, a1
C_items = [("Which bar is the highest?", hi), ("Which bar is the lowest?", lo), (f"How many for {a1}?", str(V[a1])),
           (f"How many more for {a1} than for {b1}?", str(V[a1] - V[b1]))]
P1 = rng.choice(D["posters"]); ORD1 = ["head", "img", "cap", "con", "when"]
names = name_parts([P1[k] for k in ORD1]); assert [n.split(" ", 1)[1] for n in names] == [PNAME[k] for k in ORD1]
LETTERS = "abcde"
nA = 1; nB = nA + 10; nC = nB + 2; nD = nC + 4; nF = nD + 5; NQ = nF + 1; assert NQ == 23, NQ

FX = ("Ballyvale Farmers' Market", ["FRESH FROM THE FIELD!", "[photo: a smiling stallholder with a basket of apples, caption: “Maura Healy and her Bramley apples”]",
      "Every Saturday, 9 a.m. to 1 p.m., Ballyvale Square.", "Over 20 stalls: vegetables, cheese, bread and honey.",
      "Our food is the freshest in Kildare, and our prices are better than any supermarket's.", "Phone 045 555 0128 · www.ballyvalemarket.ie"])
assert ko(FX[1][2]) == F and ko(FX[1][3]) == F and ko(FX[1][4]) == O

sheet = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Non-literary and visual texts, rules and practice | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{SHEET_STYLE}
{EXTRA}
.p2 ol.q li{{margin-bottom:2px;font-size:9pt}}.p2 h2{{margin:4px 0 2px}}.p2 .two{{gap:6mm}}.p2 .tc{{font-size:8.6pt;line-height:1.33;margin:2px 0}}
</style></head><body>
<div class="page tight">
  <div class="band"><div><div class="k">Junior Cycle English · Free revision sheet</div><h1>Non-literary and visual texts</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2015 specification): {LO}. Play the game: <b>{GAME}</b></p>
  <p><b>Non-literary texts</b> are everyday texts: posters, leaflets, adverts, reviews, reports, articles, blogs, web pages, podcasts. <b>Visual texts</b> use pictures, charts, colour and layout. The exam asks what they say, how they say it, and whether you can trust them.</p>
  <div class="two">
   <div><h2>1. Fact or opinion?</h2>
    <table class="st"><thead><tr><th>Fact</th><th>Opinion</th></tr></thead><tbody>
     <tr><td>Can be checked or proved: numbers, dates, times, prices, places.</td><td>Someone's view: judgement words like best, worst, tastiest, amazing, boring, too, better, should, I think.</td></tr>
     <tr><td><i>The Greenway is 42 kilometres long.</i></td><td><i>The Greenway is the most beautiful cycle in Ireland.</i></td></tr></tbody></table>
    <p style="font-size:9.2pt">Ask: <b>could I check this?</b> Adverts and reviews mix the two on purpose: a fact builds trust, then an opinion slips in beside it.</p>
    <h2>2. Reading a chart</h2>
    <ul style="font-size:9.2pt;margin:2px 0 2px 14px;padding:0"><li>Read the <b>title</b> and the <b>axis labels</b> first.</li><li>Read across from the <b>top of each bar</b>. Halfway between two lines = the number in between.</li>
     <li>“How many more?” = bigger − smaller.</li><li>Quote the numbers in your answer.</li></ul></div>
   <div><h2>3. Parts of a poster or leaflet</h2>
    <table class="st"><tbody>
     <tr><td><b>Headline</b></td><td>big, bold words at the top to grab attention</td></tr>
     <tr><td><b>Picture</b></td><td>shows the event or product, sets the mood</td></tr>
     <tr><td><b>Caption</b></td><td>the small line under a picture that explains it</td></tr>
     <tr><td><b>When &amp; where</b></td><td>day, date, time, place</td></tr>
     <tr><td><b>Contact details</b></td><td>phone, website, email: what to do next</td></tr></tbody></table>
    <h2>4. Writing about a visual text</h2>
    <div class="wk"><b class="h">Weak</b>The poster has a picture and it is good.</div>
    <div class="wk"><b class="h">Strong (name it + what it does)</b>The photo of children laughing in the pool makes the club look fun and friendly, so young readers want to join.</div></div>
  </div>
  <div class="tip"><b>Exam tip:</b> name the feature, give the words or the number, then say what it does for the reader.</div>
</div>

<div class="page p2">
  <div class="band"><div><div class="k">Practice · {NQ} questions</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Fact or opinion? Write F or O.</h2>
  <div class="two"><ol class="q">{''.join(li(i, f"{esc(s)} ____") for i, s in enumerate(A_items[:5], nA))}</ol><ol class="q">{''.join(li(i, f"{esc(s)} ____") for i, s in enumerate(A_items[5:], nA + 5))}</ol></div>
  <h2>B. One line is different from the other three. Which line, and is it a fact or an opinion?</h2>
  <div class="two">{''.join(f"<div><div class='tc'><span class='k'>{esc(T['k'][2:].strip())} · {esc(T['title'])}</span><br>" + "<br>".join(f"{j}. {esc(l)}" for j, l in enumerate(T['lines'], 1)) + f"</div><ol class='q'>{li(nB + i, 'Line ____ is the only ________.')}</ol></div>" for i, (T, o, n) in enumerate(B_items))}</div>
  <div class="two"><div><h2>C. Read the chart.</h2>{chart(G1)}
   <ol class="q">{''.join(li(i, f"{q} {L}") for i, (q, a) in enumerate(C_items, nC))}</ol></div>
   <div><h2>D. Label the parts of the poster.</h2>{poster(P1, ORD1, list(LETTERS))}
   <ol class="q">{''.join(li(nD + i, f"{L}") for i in range(5))}</ol>
   <p style="font-size:8.6pt;color:var(--muted)">Write the part for a, b, c, d, e: headline, picture, caption, when &amp; where, contact details.</p></div></div>
</div>

<div class="page">
  <div class="band"><div><div class="k">Exam-style · answers</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <h2>F. Exam-style: an original leaflet</h2>
  <div class="pass"><b>Leaflet: {FX[0]}</b>{''.join(f"<span class='sp'>{esc(l)}</span>" for l in FX[1])}</div>
  <ol class="q">
   <li value="{nF}">Write down one fact and one opinion from the leaflet. Explain how you know which is which.<span class="long"></span><span class="long"></span><span class="long"></span></li>
   <li value="{nF + 1}">How do the headline and the photograph try to persuade people to come to the market?<span class="long"></span><span class="long"></span><span class="long"></span></li>
  </ol>
  <h2>Answers</h2>
  <table class="ans"><tbody>
   <tr><td><b>A</b></td><td>{" · ".join(f"{i}. {ko(s)[0]}" for i, s in enumerate(A_items, nA))}</td></tr>
   <tr><td><b>B</b></td><td>{" · ".join(f"{nB + i}. Line {n}, the only {o.lower()}" for i, (T, o, n) in enumerate(B_items))}</td></tr>
   <tr><td><b>C</b></td><td>{" · ".join(f"{i}. {a}" for i, (q, a) in enumerate(C_items, nC))} ({esc(a1)} {V[a1]} − {esc(b1)} {V[b1]})</td></tr>
   <tr><td><b>D</b></td><td>{" · ".join(f"{nD + i}. {LETTERS[i]} = {n.split(' ', 1)[1].lower()}" for i, n in enumerate(names))}</td></tr>
   <tr><td><b>F</b></td><td>{nF}. Fact: <span class="qt">“Every Saturday, 9 a.m. to 1 p.m., Ballyvale Square”</span> (it can be checked). Opinion: <span class="qt">“the freshest in Kildare”</span> (“freshest” is a judgement word; someone could disagree). · {nF + 1}. The headline “FRESH FROM THE FIELD!” is in capitals with an exclamation mark, so it sounds lively and makes you think of fresh food; the photo of a smiling stallholder with apples makes the market look friendly and local, and the caption names her, so it feels personal.</td></tr>
  </tbody></table>
  <div class="note"><b>Got one wrong?</b> Go back to page 1, then play <b>Fact or Opinion</b> at {GAME}: the “Go back over these” list at the end explains each one.</div>
  <p class="small">All texts, charts and posters are made up by Léim (no real brands). Léim is independent and not connected with the State Examinations Commission or the NCCA.</p>
</div>
</body></html>"""

# ---------- teacher pack ----------
rng = random.Random(3102)
cards = [(s, F) for s in rng.sample(D["fo"]["f"], 12)] + [(s, O) for s in rng.sample(D["fo"]["o"], 12)]
rng.shuffle(cards)
for s, k in cards: assert ko(s) == k
cards_html = "".join(f'<div class="c"><span class="tag">{i}</span><div class="fc sm">{esc(s)}</div></div>' for i, (s, k) in enumerate(cards, 1))
ckey = " · ".join(f"{i} {k[0]}" for i, (s, k) in enumerate(cards, 1))

GA, GB = rng.sample([G for G in D["charts"] if len(G["bars"]) == 4], 2)
def swap_card(who, mine, theirs):
    V = dict(mine["bars"])
    return f"""<div class="idc"><h3>Student {who} · Chart Swap</h3>
    <div class="two" style="gap:4mm"><div><p style="font-size:8.8pt;margin:0 0 1mm"><b>1. Your data (keep it hidden).</b> Read it out: “{esc(mine['title'])}. {esc(mine['bars'][0][0])}: {mine['bars'][0][1]} …”</p>
    <table class="st"><tbody>{''.join(f"<tr><td>{esc(l)}</td><td>{v}</td></tr>" for l, v in mine['bars'])}</tbody></table>
    <p style="font-size:8.8pt;margin:1mm 0"><b>3. Then ask your partner:</b> Which is the highest? How many more {esc(max(V, key=V.get))} than {esc(min(V, key=V.get))}?</p></div>
    <div><p style="font-size:8.8pt;margin:0 0 1mm"><b>2. Draw your partner's bars</b> as they read out their data.</p>{chart(theirs, blank=True)}</div></div></div>"""
CARD_A = swap_card("A", GA, GB); CARD_B = swap_card("B", GB, GA)
def qa(G):
    V = dict(G["bars"]); h, l = max(V, key=V.get), min(V, key=V.get); return f"{esc(G['title'])}: highest {esc(h)} ({V[h]}); {esc(h)} − {esc(l)} = {V[h] - V[l]}"

FIX = [("The poster is good because it has a picture.", "names a feature but not what it does: say what the picture shows and why it was chosen"),
       ("“The café makes the tastiest scones in Ireland” is a fact because it is in the leaflet.", "being printed doesn't make it a fact: “tastiest” is a judgement word, so it's an opinion"),
       ("The chart shows lots of people like PE.", "no number: “PE was the favourite, with 45 votes”"),
       ("The headline is big.", "say what it does: big, bold capitals grab the reader's attention first"),
       ("“Tickets cost €9 on Tuesdays” is an opinion because I think it's too dear.", "the line itself can be checked, so it's a fact; your view about it is the opinion"),
       ("The leaflet is persuasive.", "no evidence: quote the words or name the feature that persuades (“the friendliest in the Midlands”, the photo)")]
assert ko("The café makes the tastiest scones in Ireland.") == O and ko("Tickets are €9 on Tuesdays.") == F

GW = {"title": "Members of the cinema club", "y": "Members", "bars": [["2022", 15], ["2023", 25], ["2024", 40], ["2025", 45]]}
assert len({v for l, v in GW["bars"]}) == 4
WX = ("Riverside Cinema Club, Carrick-on-Shannon", ["FILM NIGHTS ARE BACK!", "[photo: teenagers with popcorn in front of a big screen, caption: “Our autumn opening night”]",
      "Every Friday at 7 p.m. in the Riverside Hall. Tickets €4, popcorn included.", "We show 30 films a year, from cartoons to classics.",
      "It is the best night out in Leitrim, with the comfiest seats in the county!", "Email films@riversidecinema.ie"])
assert ko(WX[1][2]) == F and ko(WX[1][3]) == F and ko(WX[1][4]) == O
WV = dict(GW["bars"])

pack = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Non-literary and Visual Texts Teacher Pack | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{PACK_STYLE}
{EXTRA}
.fym{{grid-template-columns:repeat(4,1fr)}}.fym .c{{height:30mm}}.fym .fc.sm{{font-size:9.6pt;font-weight:600;line-height:1.3}}
.idc{{padding:2mm 4mm;margin-bottom:3mm}}.idc h3{{margin:0 0 1mm}}.idc svg.ch{{max-width:80mm}}.p1 .proc td{{font-size:8.6pt;padding:2px 6px}}
.ws .eh td{{font-size:8.6pt;padding:2px 6px}}.ws .eh .gap{{height:11px}}.ws .pass{{font-size:8.6pt;line-height:1.35}}.ws ol.q li{{margin-bottom:1px}}.ws svg.ch{{max-width:62mm}}
.prow{{display:grid;grid-template-columns:1fr 1fr;gap:4mm}}.prow div{{border-radius:14px;padding:5mm 3mm;text-align:center;font-size:12pt;line-height:1.45}}.prow b{{display:block;font-size:20pt}}
.pex{{border:3px solid var(--night);border-radius:14px;padding:5mm 7mm;font-size:13pt;line-height:1.5}}
</style></head><body>

<div class="page p1">
  <div class="band"><div><div class="k">Junior Cycle English · Teacher pack</div><h1>Non-literary &amp; Visual Texts</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2015 specification): {LO}</p>
  <div class="two">
    <div><h3>Aims</h3><p>By the end of the lesson students can tell fact from opinion and explain how they know, read a bar chart accurately and quote its numbers, name the parts of a poster or leaflet, and explain how headlines, pictures and layout work on the reader.</p></div>
    <div><h3>In this pack</h3><p>p.1 Teacher notes · p.2 Fact or Opinion Sort (24 cards) · p.3 Chart Swap A/B (pair listening task) · p.4 Wall poster · p.5 Worksheet: Fix the Answer + exam-style questions · p.6 Answers. Level: 3rd year (works from 1st year), Higher and Ordinary. Time: about 60 minutes. All texts and charts are original, with invented brands only.</p></div>
  </div>
  <h2 style="margin-top:8px">Procedure</h2>
  <table class="proc"><tbody>
    <tr><td>5 min</td><td><b>Lead-in.</b> Bring in (or project) a real local leaflet. Students shout “Fact!” or “Opinion!” as you read lines aloud. Ask: how did you know?</td></tr>
    <tr><td>12 min</td><td><b>Fact or Opinion Sort</b> (p.2, groups of 3–4). Sort the 24 cards into two piles. Then each group turns three opinion cards into facts (“The skate park is far too small” → “The skate park has 6 ramps”) and underlines the judgement words.</td></tr>
    <tr><td>15 min</td><td><b>Chart Swap</b> (p.3, pairs). Each reads their hidden data aloud; the partner draws the bars on the blank grid. Compare, then ask each other the questions on the card.</td></tr>
    <tr><td>5 min</td><td><b>Poster walk.</b> Show the poster (p.4) or a real one: name each part and what it does.</td></tr>
    <tr><td>18 min</td><td><b>Worksheet</b> (p.5). Fix the Answer in pairs, then the exam-style questions on the Riverside Cinema Club leaflet alone.</td></tr>
    <tr><td>5 min</td><td><b>Exit ticket.</b> One fact and one opinion from any advert, with a reason for each. Homework: play <b>Fact or Opinion</b> at {GAME}.</td></tr>
  </tbody></table>
  <div class="note"><b>Errors to look for:</b> “it's in the leaflet, so it's a fact” · calling a fact an opinion because they disagree with it · reading a bar from the wrong gridline · adding instead of subtracting for “how many more” · naming a feature without saying what it does · no quote or number as evidence. <b>Support:</b> give a list of judgement words. <b>Fast finishers:</b> design a poster for a school event with all five parts, one fact-based line and one opinion line.</div>
</div>

<div class="page">
  <div class="band"><div><div class="k">Groups · cut up the cards</div><h1>Fact or Opinion Sort</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.4pt;margin:0 0 2mm">Sort the 24 cards into two piles: <b>Fact</b> (can be checked) and <b>Opinion</b> (someone's view). Underline the word that tells you. Then turn three opinions into facts.</p>
  <div class="fym">{cards_html}</div>
</div>

<div class="page">
  <div class="band"><div><div class="k">Pairs · cut along the dashed line</div><h1>Chart Swap A/B</h1></div><div class="logo">↗ Léim</div></div>
  {CARD_A}
  {CARD_B}
</div>

<div class="page">
  <div class="poster">
    <h1>Can you check it?</h1>
    <div class="prow">
      <div style="background:var(--green-soft)"><b>Fact</b>Numbers · dates · times · prices · places<br><i>Tickets cost €8.</i></div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Opinion</b>best · tastiest · amazing · boring · too · should · I think<br><i>The show is a brilliant night out.</i></div>
    </div>
    <div class="pex"><b>Visual texts:</b> Headline · Picture · Caption · When &amp; where · Contact details<br><b>Charts:</b> title → axis → top of each bar → quote the numbers.</div>
    <p style="text-align:center;font-size:18pt!important;font-weight:800;margin:4mm 0">Name it. Quote it. Say what it does.</p>
    <p style="text-align:center;font-size:10pt;color:var(--muted)">Léim · leim.ie · Play Fact or Opinion: {GAME}</p>
  </div>
</div>

<div class="page ws">
  <div class="band"><div><div class="k">Worksheet · exam-style questions</div><h1>Fix the Answer</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Fix the Answer</h2>
  <p>Each line comes from a weak answer about a leaflet, poster or chart. Say what's wrong and write a better version.</p>
  <table class="eh"><thead><tr><th>Weak answer</th><th>What's wrong and a better version</th></tr></thead><tbody>
  {"".join(f"<tr><td style='font-weight:500'>{esc(s)}</td><td><span class='gap'></span><span class='gap'></span></td></tr>" for s, r in FIX)}
  </tbody></table>
  <h2>B. Exam-style questions: an original leaflet and chart</h2>
  <div class="two" style="gap:4mm"><div class="pass"><b>Leaflet: {WX[0]}</b>{''.join(f"<span class='sp'>{esc(l)}</span>" for l in WX[1])}</div><div>{chart(GW)}</div></div>
  <ol class="q">
    <li>Write down two facts and one opinion from the leaflet.<span class="long"></span></li>
    <li>How many more members did the club have in 2025 than in 2022?<span class="long"></span></li>
    <li>What does the chart suggest about the club? Use the numbers.<span class="long"></span></li>
    <li>How do the headline and the photograph try to attract teenagers?<span class="long"></span><span class="long"></span></li>
    <li>Which line of the leaflet is all opinion? Which words tell you?<span class="long"></span></li>
  </ol>
</div>

<div class="page an">
  <div class="band"><div><div class="k">For the teacher</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>Fact or Opinion Sort</h2>
  <p style="font-size:9pt">{ckey} (F = fact, O = opinion)</p>
  <h2>Chart Swap</h2>
  <p style="font-size:9pt">A's data: {qa(GA)} · B's data: {qa(GB)}. Check the drawn bars against the tables on the cards.</p>
  <h2>A. Fix the Answer</h2>
  <table><tbody>{"".join(f"<tr><td style='width:42%'>{esc(s)}</td><td>{esc(r)}</td></tr>" for s, r in FIX)}</tbody></table>
  <h2>B. Exam-style questions</h2>
  <ol class="q">
    <li>Facts: “Every Friday at 7 p.m. in the Riverside Hall”; “Tickets €4, popcorn included”; “30 films a year”. Opinion: “the best night out in Leitrim”.</li>
    <li>{WV['2025']} − {WV['2022']} = {WV['2025'] - WV['2022']} more members.</li>
    <li>It is growing every year ({' → '.join(str(v) for l, v in GW['bars'])}), so the club is popular, which makes a new member trust it.</li>
    <li>“FILM NIGHTS ARE BACK!”: capitals and an exclamation mark sound exciting; the photo of teenagers with popcorn shows people the reader's age having fun; the caption makes it a real event.</li>
    <li>“It is the best night out in Leitrim, with the comfiest seats in the county!”: “best” and “comfiest” are judgement words; nobody could prove them.</li>
  </ol>
  <h2>Marking tip</h2>
  <p>Answers on non-literary and visual texts are rewarded for naming the feature, quoting the words or numbers, and explaining the effect on the reader. Our guide, not an official marking scheme.</p>
</div>
</body></html>"""

cover = """<!doctype html><html><head><meta charset="utf-8"><style>
body{margin:0;width:1200px;height:1200px;background:#1B2430;font-family:Inter,sans-serif;color:#fff;display:flex;flex-direction:column;justify-content:space-between;padding:90px;box-sizing:border-box}
.k{display:inline-block;background:#2E7D57;border-radius:99px;padding:12px 26px;font-weight:700;font-size:28px;letter-spacing:.06em;text-transform:uppercase}
h1{font-size:96px;font-weight:800;line-height:1.3;letter-spacing:-.02em;margin:60px 0 20px}
h1 span{background:#F6CF5A;color:#1B2430;padding:0 18px;border-radius:14px}
.sub{font-size:40px;line-height:1.4;color:#DDE3EA}
.em{font-size:46px;margin-top:30px;font-weight:800;letter-spacing:.01em;color:#F6CF5A}
.foot{display:flex;justify-content:space-between;align-items:center;font-size:34px;font-weight:700}
.price{background:#F6CF5A;color:#1B2430;border-radius:16px;padding:14px 28px}
</style></head><body>
<div><span class="k">JC English · Teacher pack</span>
<h1><span>Non-literary</span><br><span>&amp; Visual Texts</span></h1>
<div class="sub">Fact or Opinion Sort · Chart Swap A/B<br>Poster · Worksheet + answers</div>
<div class="em">fact, opinion, charts &amp; posters</div></div>
<div class="foot"><span>↗ Léim · leim.ie</span><span class="price">Ready to teach · 60 min</span></div>
</body></html>"""

if __name__ == "__main__":
    for name, txt in [("rules-and-practice", sheet), ("teacher-pack", pack), ("cover", cover)]:
        open(os.path.join(SRC, f"{SLUG}-{name}.html"), "w", encoding="utf-8").write(txt)
    def pdf(name, out):
        subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--no-pdf-header-footer", f"--print-to-pdf={out}",
                        f"{SLUG}-{name}.html"], cwd=SRC, check=True, capture_output=True)
        n = subprocess.run(["pdfinfo", out], capture_output=True, text=True).stdout.split("Pages:")[1].split()[0]
        print(name, n, "pages"); return int(n)
    a = pdf("rules-and-practice", os.path.join(ROOT, "printables", f"{SLUG}-rules-and-practice.pdf"))
    b = pdf("teacher-pack", os.path.join(OUT, "Non-Literary-Visual-Texts-Teacher-Pack-Leim.pdf"))
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--hide-scrollbars", "--window-size=1200,1200",
                    f"--screenshot={os.path.join(OUT, f'{SLUG}-cover.png')}", f"{SLUG}-cover.html"], cwd=SRC, check=True, capture_output=True)
    assert a == 3 and b == 6, (a, b)
