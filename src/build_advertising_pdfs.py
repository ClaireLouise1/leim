#!/usr/bin/env python3
"""Media 1: advertising (JC English Order 20): free sheet (-> printables/), 6-page teacher pack + 1200x1200 cover (-> OUTDIR).
Usage: python3 src/build_advertising_pdfs.py /tmp/advertising
Items come from the game's data block (ad-breaker.html). Every answer is re-derived with the checker's own rules
(src/test_ad_breaker.py: tricks, audiences, fo, good_slogan) and asserted; the checker's data pass runs first.
Styles are read from src/build_money1_pdfs.py."""
import os, sys, random, subprocess, re
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC); sys.path.insert(0, SRC)
from test_ad_breaker import tricks, audiences, fo, good_slogan, load, data_pass, allit, rhyme, nwords
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/advertising"; os.makedirs(OUT, exist_ok=True)
SLUG = "media-advertising"
LO = "R9, R8, OL8, W3"
GAME = "leim.ie/ad-breaker.html"
D = load(os.path.join(ROOT, "ad-breaker.html")); assert not data_pass(D), data_pass(D)
TN = {"star": "Star power", "free": "Free gift", "band": "Bandwagon", "stat": "Statistic", "exag": "Exaggeration", "hurry": "Hurry"}
AN = {"ki": "Young children", "te": "Teenagers", "pa": "Parents", "ol": "Older people", "sp": "Sporty people"}
L = "abcd"

# ---------- free sheet ----------
random.seed(2020)
A_items = [x for k in TN for x in random.sample([y for y in D["trick"] if y[1] == k], 2)]; random.shuffle(A_items)
for s, k in A_items: assert tricks(s) == [k]
B_items = [random.choice([a for a in D["ads"] if a["who"] == k]) for k in ("ki", "te", "ol", "sp")]; random.shuffle(B_items)
for a in B_items: assert audiences(" ".join(a["lines"])) == [a["who"]]
C_items = random.sample([x for x in D["fo"] if x[1] == "f"], 5) + random.sample([x for x in D["fo"] if x[1] == "o"], 5); random.shuffle(C_items)
for s, k in C_items: assert fo(s) == k
D_items = []
for lab, brand, best, long, dull in random.sample(D["slogan"], 3):
    other = random.choice([x[2] for x in D["slogan"] if x[1] != brand])
    opts = [best, long, dull, other]; random.shuffle(opts)
    right = [i for i, o in enumerate(opts) if good_slogan(brand, o)]; assert len(right) == 1
    D_items.append((lab.split(" ", 1)[1], brand, opts, L[right[0]]))
NQ = len(A_items) + len(B_items) + len(C_items) + len(D_items) + 3; assert NQ == 32, NQ
nA = 1; nB = nA + len(A_items); nC = nB + len(B_items); nD = nC + len(C_items); nE = nD + len(D_items)

def style(var):
    return re.search(var + r' = f"""<!doctype.*?<style>(.*?)</style>', open(os.path.join(SRC, "build_money1_pdfs.py"), encoding="utf-8").read(), re.S).group(1).replace("{LO}", LO).replace("{{", "{").replace("}}", "}").replace("JC Maths LOs (2018 spec)", "JC English LOs (2015 spec)")
SHEET_STYLE = style("sheet"); PACK_STYLE = style("pack")
assert "JC English LOs (2015 spec)" in SHEET_STYLE and "Single-teacher licence" in PACK_STYLE and "JC English LOs (2015 spec)" in PACK_STYLE
EXTRA = """.wk{line-height:1.45;border:1.5px solid var(--line);border-radius:8px;padding:2px 7px;margin:3px 0;font-size:9.4pt}.wk b.h{display:block}
table.st{border-collapse:collapse;margin:3px 0;font-size:9.2pt;width:100%}table.st td,table.st th{border:1px solid #C9D1DA;padding:2px 6px;text-align:left}
.pass{border-left:4px solid var(--green);background:var(--mist);padding:5px 10px;margin:4px 0}
.ad{border:1.5px dashed #9AA6B2;border-radius:8px;padding:3px 8px;margin:2px 0 4px;font-size:9pt}.ad b{display:block;font-size:8pt;letter-spacing:.05em;text-transform:uppercase;color:#5A6673}
.opts{list-style:none;padding-left:0;margin:1px 0 3px}.opts li{margin:0!important;font-size:8.8pt}"""

half = len(A_items) // 2
def a_li(i, s): return f"<li value='{i}'><i>{s}</i><br><span class='line' style='min-width:34mm'></span></li>"
A1 = "".join(a_li(i, s) for i, (s, k) in enumerate(A_items[:half], nA)); A2 = "".join(a_li(i, s) for i, (s, k) in enumerate(A_items[half:], nA + half))
def adbox(a): return f"<div class='ad'><b>{a['brand']}</b>{' '.join(a['lines'])}</div>"
B_html = "".join(f"<li value='{i}'>{adbox(a)}Aimed at: <span class='line' style='min-width:30mm'></span> Clue word: <span class='line' style='min-width:22mm'></span></li>" for i, a in enumerate(B_items, nB))
C_html = "".join(f"<li value='{i}'>{s} &nbsp; <b>F / O</b></li>" for i, (s, k) in enumerate(C_items, nC))
D_html = "".join(f"<li value='{i}'><b>{brand}</b> ({lab.lower()})<ul class='opts'>{''.join(f'<li>({L[j]}) {o}</li>' for j, o in enumerate(opts))}</ul></li>" for i, (lab, brand, opts, a) in enumerate(D_items, nD))

AD = ("Glenmore Adventure Park", "[Picture: a family laughing on a zip line above green trees]",
      ["Glenmore Adventure Park: the most exciting day out in Ireland!", "Zip lines, tree-top walks and a giant maze.",
       "Open every day from 10 am. Family ticket €60.", "Thousands of families visit every summer.", "Book online before 1 June and get a free picnic."])
assert "band" in tricks(AD[2][3]) and "free" in tricks(AD[2][4]) and fo(AD[2][2]) == "f" and fo("Glenmore is the most fun you'll have all year.") == "o"
E_ad = f"<div class='pass'><b>{AD[1]}</b><br>{'<br>'.join(AD[2])}</div>"

sheet = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Media 1: advertising, rules and practice | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{SHEET_STYLE}
{EXTRA}
.p2 ol.q li{{margin-bottom:1px;font-size:9pt}}.p2 h2{{margin:4px 0 2px}}.p2 .two{{gap:5mm}}
</style></head><body>
<div class="page tight">
  <div class="band"><div><div class="k">Junior Cycle English · Free revision sheet</div><h1>Media 1: advertising</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2015 specification): {LO}. Play the game: <b>{GAME}</b></p>
  <p>Every advert wants you to <b>buy</b> or <b>do</b> something. Ask three questions: <b>Who is it for? What is it selling? How does it try to persuade me?</b></p>
  <div class="two">
   <div><h2>1. Six tricks</h2>
    <table class="st"><tbody>
     <tr><td><b>Star power</b></td><td>Famous chef Gráinne Lynch cooks with Crispa oil.</td></tr>
     <tr><td><b>Free gift</b></td><td>Free delivery on all Plantly orders.</td></tr>
     <tr><td><b>Bandwagon</b></td><td>All your friends are wearing Kicks trainers.</td></tr>
     <tr><td><b>Statistic</b></td><td>9 out of 10 dogs prefer Waggo biscuits.</td></tr>
     <tr><td><b>Exaggeration</b></td><td>The greatest pizza in the universe!</td></tr>
     <tr><td><b>Hurry</b></td><td>While stocks last. Today only.</td></tr></tbody></table>
    <p style="font-size:9pt">Ask about every statistic: who counted, and how many? "9 out of 10 dogs" might mean 10 dogs.</p>
    <h2>2. Who is it for?</h2>
    <table class="st"><tbody>
     <tr><td><b>Young children</b></td><td>toys, cartoons, bedtime, "ask your mum or dad"</td></tr>
     <tr><td><b>Teenagers</b></td><td>exams, study, your mates, gaming</td></tr>
     <tr><td><b>Parents</b></td><td>your kids, the school run, family meals</td></tr>
     <tr><td><b>Older people</b></td><td>retirement, grandchildren, reading glasses</td></tr>
     <tr><td><b>Sporty people</b></td><td>training, the gym, a personal best</td></tr></tbody></table></div>
   <div><h2>3. Fact or opinion?</h2>
    <div class="wk"><b class="h">Fact: it can be checked</b><i>Sunny Bay ice cream costs €2.50 a cone.</i></div>
    <div class="wk"><b class="h">Opinion: a judgement nobody can prove</b><i>Sunny Bay ice cream is the tastiest treat around.</i></div>
    <h2>4. A good slogan</h2>
    <p style="font-size:9pt">is <b>short</b>, <b>names the brand</b> and is <b>catchy</b>: alliteration (<i>Fizzpop: feel the fizz!</i>) or rhyme (<i>Sparkle: no mess, no stress.</i>).</p>
    <h2>5. Pictures and layout</h2>
    <p style="font-size:9pt">The picture sends a message before you read a word: fruit and runners = healthy; diamonds and gold = luxury; a family at a table = home; balloons and rides = fun; trees and bees = natural. The eye goes to the biggest thing first, usually the picture or the headline.</p></div>
  </div>
  <div class="tip"><b>Exam tip:</b> for "How does this advert persuade?" <b>name</b> the trick, <b>quote</b> it and <b>explain</b> its effect on the reader. Talk about the picture and the layout too, not only the words.</div>
</div>

<div class="page p2">
  <div class="band"><div><div class="k">Practice · {NQ} questions</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Name the trick in each line</h2>
  <div class="two"><div><ol class="q">{A1}</ol></div><div><ol class="q">{A2}</ol></div></div>
  <h2>B. Who is each ad for? Write a clue word</h2>
  <div class="two"><div><ol class="q">{"".join(B_html.split("</li>")[:2])}</li></ol></div><div><ol class="q">{"</li>".join(B_html.split("</li>")[2:])}</ol></div></div>
  <h2>C. Fact or opinion? Circle F or O</h2>
  <div class="two"><div><ol class="q">{"</li>".join(C_html.split("</li>")[:5])}</li></ol></div><div><ol class="q">{"</li>".join(C_html.split("</li>")[5:])}</ol></div></div>
</div>

<div class="page">
  <div class="band"><div><div class="k">Slogans · exam-style · answers</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <h2>D. Which is the best slogan? Circle a letter</h2>
  <div class="two"><div><ol class="q">{"</li>".join(D_html.split("</li></ul></li>")[:2]).replace("</li><li value", "</li></ul></li><li value")}</li></ul></li></ol></div><div><ol class="q">{D_html.split("</li></ul></li>")[2]}</li></ul></li></ol></div></div>
  <h2>E. Exam-style</h2>
  {E_ad}
  <ol class="q">
   <li value="{nE}">Who is this advert aimed at? Give two pieces of evidence.<span class="long"></span></li>
   <li value="{nE + 1}">Name two persuasive tricks and explain how one works.<span class="long"></span></li>
   <li value="{nE + 2}">Find one fact and one opinion.<span class="long"></span></li>
  </ol>
  <h2>Answers</h2>
  <table class="ans"><tbody>
   <tr><td><b>A</b></td><td>{" · ".join(f"{i}. {TN[tricks(s)[0]]}" for i, (s, k) in enumerate(A_items, nA))}</td></tr>
   <tr><td><b>B</b></td><td>{" · ".join(f"{i}. {AN[audiences(' '.join(a['lines']))[0]]}" for i, a in enumerate(B_items, nB))}</td></tr>
   <tr><td><b>C</b></td><td>{" · ".join(f"{i}. {fo(s).upper()}" for i, (s, k) in enumerate(C_items, nC))}</td></tr>
   <tr><td><b>D</b></td><td>{" · ".join(f"{i}. ({a})" for i, (lab, b, o, a) in enumerate(D_items, nD))}: short, names the brand, catchy. The others are too long, dull, or name another brand.</td></tr>
   <tr><td><b>E</b></td><td>{nE}. Families: "Family ticket €60", "Thousands of families", the picture of a family. {nE + 1}. Exaggeration ("the most exciting day out in Ireland"), bandwagon ("Thousands of families"), free gift ("a free picnic"), hurry ("before 1 June"). {nE + 2}. Fact: "Open every day from 10 am" (it can be checked). Opinion: "the most exciting day out in Ireland".</td></tr>
  </tbody></table>
  <div class="note"><b>Got one wrong?</b> Go back to page 1, then play <b>Ad Breaker</b> at {GAME}: the "Go back over these" list at the end explains each mistake.</div>
  <p class="small">All brands, names and places are made up by Léim. Léim is independent and not connected with the State Examinations Commission or the NCCA.</p>
</div>
</body></html>"""

# ---------- teacher pack ----------
random.seed(2021)
TS = [x for k in TN for x in random.sample([y for y in D["trick"] if y[1] == k], 4)]; random.shuffle(TS)
assert len(TS) == 24
for s, k in TS: assert tricks(s) == [k]
ts_html = "".join(f'<div class="c"><span class="tag">Card {i}</span><div class="fc sm">{s}</div></div>' for i, (s, k) in enumerate(TS, 1))
ts_key = " · ".join(f"<b>{TN[k]}</b>: {', '.join(str(i) for i, (s, kk) in enumerate(TS, 1) if kk == k)}" for k in TN)

ADS_A = [a for a in D["ads"] if a["brand"] in ("Bouncy Bear", "Cramly", "Golden Getaways")]
ADS_B = [a for a in D["ads"] if a["brand"] in ("Roomy", "Fitfirst", "Kerbz")]
FO_A = [x for x in D["fo"] if x[0].startswith(("Rollo", "Pizzazz", "Glide"))]
FO_B = [x for x in D["fo"] if x[0].startswith(("Cosytoes", "Kerbz", "Cramly"))]
assert len(ADS_A) == len(ADS_B) == 3 and len(FO_A) == len(FO_B) == 6
for a in ADS_A + ADS_B: assert len(audiences(" ".join(a["lines"]))) == 1
for s, k in FO_A + FO_B: assert fo(s) == k
def swap_card(who, ads, fos, seed):
    random.seed(seed); f = fos[:]; random.shuffle(f)
    return f"""<div class="idc"><h3>Student {who} · Ad Swap</h3>
    <p style="font-size:8.8pt;margin:0 0 1mm"><b>1. Read</b> each advert to your partner like a radio ad. Your partner says who it is for and the clue word. Tick if they're right.</p>
    <table class="st" style="font-size:8.8pt"><tbody>{"".join(f"<tr><td style='width:4%'><b>{i}</b></td><td><b>{a['brand']}:</b> {' '.join(a['lines'])}</td><td style='width:6%'>☐</td></tr>" for i, a in enumerate(ads, 1))}</tbody></table>
    <p style="font-size:8.8pt;margin:1mm 0"><b>2. Listen</b> to your partner's three adverts. Write who each one is for and the clue word.</p>
    <table class="st" style="font-size:8.8pt"><tbody>{"".join(f"<tr><td style='width:4%'><b>{i}</b></td><td>For: </td><td>Clue: </td></tr>" for i in range(1, 4))}</tbody></table>
    <p style="font-size:8.8pt;margin:1mm 0"><b>3. Read</b> these lines. Your partner calls out "Fact!" or "Opinion!".</p>
    <table class="st" style="font-size:8.8pt"><tbody><tr>{"".join(f"<td>{s}</td>" + ("</tr><tr>" if i % 2 == 1 and i < 5 else "") for i, (s, k) in enumerate(f))}</tr></tbody></table></div>"""

FIX = [("The ad uses a lot of persuasive techniques.", "Too vague. Name one, quote it, explain it: <b>It uses star power (\"Olympic champion Aoife Brennan\"): readers trust a winner.</b>"),
       ("The ad is aimed at people.", "Name the audience and back it up: <b>It's aimed at parents: \"the school run\", \"your children\".</b>"),
       ("The picture is nice.", "Say what the picture suggests: <b>The family laughing on the zip line suggests a fun day out together.</b>"),
       ("\"Delicious\" is a fact because it's in the ad.", "Being in the ad doesn't make it a fact: <b>\"Delicious\" is an opinion; nobody can prove it.</b>"),
       ("9 out of 10 dogs prefer Waggo, so it must be true.", "Question the statistic: <b>We don't know how many dogs were asked, or who asked them.</b>"),
       ("The ad works because I like it.", "Give a reason linked to the audience: <b>It works because the slogan is short and catchy, so teenagers will remember it.</b>")]

ADV = ("Pedal Power Bike Hire, Kilbrack", "[Picture: two teenagers cycling along a sunny coast road, sea on one side]",
       ["Pedal Power: ride the wild coast!", "Bikes for teens and adults, helmets included.", "€15 a day. Open Saturdays from 9 am.",
        "Everyone's cycling the coast road this summer.", "Hurry: only 20 bikes left for July!"])
assert good_slogan("Pedal Power", ADV[2][0])
assert tricks(ADV[2][3]) == ["band"] and tricks(ADV[2][4]) == ["stat", "hurry"]
assert fo(ADV[2][2]) == "f" and audiences(" ".join(ADV[2])) == ["te"]

pack = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Media: Advertising Teacher Pack | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{PACK_STYLE}
{EXTRA}
.fym .c{{height:28mm}}.fym .fc.sm{{font-size:9.6pt;line-height:1.25;margin-top:2mm;font-weight:500}}.idc{{padding:2mm 4mm;margin-bottom:3mm}}.idc h3{{margin:0 0 1mm}}
.idc .st td{{padding:1px 5px}}.p1 .proc td{{font-size:8.6pt;padding:2px 6px}}.ops div{{font-size:12pt;padding:5mm 3mm}}.ops b{{font-size:19pt}}
.ws .eh td{{font-size:8.6pt;padding:2px 6px}}.ws .eh .gap{{height:13px}}.ws ol.q li{{margin-bottom:1px}}.ws .pass{{font-size:9pt}}
</style></head><body>

<div class="page p1">
  <div class="band"><div><div class="k">Junior Cycle English · Teacher pack</div><h1>Media 1: advertising</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2015 specification): {LO}</p>
  <div class="two">
    <div><h3>Aims</h3><p>By the end of the lesson students can say who an advert is aimed at (with evidence), name and explain six persuasive tricks, tell fact from opinion in an ad, judge a slogan and say what a picture suggests.</p></div>
    <div><h3>In this pack</h3><p>p.1 Teacher notes · p.2 Trick Sort cards (cut-up) · p.3 Ad Swap A/B (speaking) · p.4 Wall poster · p.5 Worksheet: Fix the Answer + exam-style questions · p.6 Answers. Level: 2nd year. Time: about 60 minutes. All brands, names and places are made up.</p></div>
  </div>
  <h2 style="margin-top:8px">Procedure</h2>
  <table class="proc"><tbody>
    <tr><td>5 min</td><td><b>Lead-in.</b> Read two ads for the same €12 water bottle (the game's "Spot the pattern"): A gives only facts; B has an Olympic swimmer, "Everyone on the team has one", "The best bottle ever made!", "Today only". Which makes you want it? Why?</td></tr>
    <tr><td>8 min</td><td><b>Guided discovery.</b> Students find four tricks in Ad B. Name them: star power, bandwagon, exaggeration, hurry; add free gift and statistic. Ask: who counted the "9 out of 10"?</td></tr>
    <tr><td>12 min</td><td><b>Trick Sort</b> (p.2, groups of 3, one set of 24 cards). Sort the lines into six groups of four. Each group picks the line most likely to work on them, and says why.</td></tr>
    <tr><td>12 min</td><td><b>Ad Swap</b> (p.3, pairs). A reads three ads like a radio ad; B says who each is for and the clue word; then swap. Finish with the quick-fire fact or opinion round.</td></tr>
    <tr><td>18 min</td><td><b>Worksheet</b> (p.5). Fix the Answer in pairs, then the exam-style questions on the bike-hire advert alone.</td></tr>
    <tr><td>5 min</td><td><b>Exit ticket.</b> Write a slogan for a school tuck shop using alliteration or rhyme. Homework: play <b>Ad Breaker</b> at {GAME}, or bring in a real advert and label its tricks.</td></tr>
  </tbody></table>
  <div class="note"><b>Errors to look for:</b> naming a trick with no quote or explanation · "it's aimed at people" with no evidence · treating anything printed in an ad as a fact · describing the picture instead of saying what it suggests · "it works because I like it". <b>Support:</b> the poster (p.4) on the desk. <b>Fast finishers:</b> design a poster ad for a made-up product using three tricks, then swap and spot them.</div>
</div>

<div class="page">
  <div class="band"><div><div class="k">Groups of 3 · cut up the 24 cards</div><h1>Trick Sort</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.4pt;margin:0 0 2mm">Sort the 24 ad lines into six groups of four: <b>star power · free gift · bandwagon · statistic · exaggeration · hurry</b>.</p>
  <div class="fym">{ts_html}</div>
</div>

<div class="page">
  <div class="band"><div><div class="k">Pairs · cut along the dashed line</div><h1>Ad Swap A/B</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.4pt">Can you tell who an advert is for just by listening?</p>
  {swap_card("A", ADS_A, FO_A, 2022)}
  {swap_card("B", ADS_B, FO_B, 2023)}
</div>

<div class="page">
  <div class="poster">
    <h1>Break the ad</h1>
    <div class="ops">
      <div style="background:var(--green-soft)"><b>1 Who?</b>Who is it for?<br>Find the clue words</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>2 What?</b>What is it selling?<br>What does it want me to do?</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>3 How?</b>Star · Free · Bandwagon<br>Statistic · Exaggeration · Hurry</div>
      <div style="background:var(--green-soft)"><b>4 Fact?</b>Can it be checked?<br>Or is it an opinion?</div>
    </div>
    <p style="text-align:center;font-size:20pt!important;font-weight:800;margin:4mm 0">Every ad wants something from you.</p>
    <p style="text-align:center;font-size:10pt;color:var(--muted)">Léim · leim.ie · Play Ad Breaker: {GAME}</p>
  </div>
</div>

<div class="page ws">
  <div class="band"><div><div class="k">Worksheet · exam-style questions</div><h1>Fix the Answer</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Fix the Answer</h2>
  <p>Each line is a student's answer about an advert. Say what's wrong and write a better answer.</p>
  <table class="eh"><thead><tr><th>Answer</th><th>What's wrong and the fix</th></tr></thead><tbody>
  {"".join(f"<tr><td style='font-weight:500'>{s}</td><td><span class='gap'></span><span class='gap'></span></td></tr>" for s, r in FIX)}
  </tbody></table>
  <h2>B. Exam-style questions: "{ADV[0]}"</h2>
  <div class="pass"><b>{ADV[1]}</b><br>{"<br>".join(ADV[2])}</div>
  <ol class="q">
    <li>Who is this advert aimed at? Give two pieces of evidence.<span class="long"></span></li>
    <li>Find one fact and one opinion in the advert.<span class="long"></span></li>
    <li>Name two persuasive tricks and explain how one of them works.<span class="long"></span></li>
    <li>What does the picture suggest about a day with Pedal Power?<span class="long"></span></li>
    <li>Is this an effective advert? Explain your answer.<span class="long"></span><span class="long"></span></li>
  </ol>
</div>

<div class="page an">
  <div class="band"><div><div class="k">For the teacher</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>Trick Sort (card numbers)</h2>
  <p>{ts_key}</p>
  <h2>Ad Swap</h2>
  <p>{" · ".join(f"<b>{w}{i}</b> {a['brand']}: {AN[audiences(' '.join(a['lines']))[0]]}" for w, LL in (("A", ADS_A), ("B", ADS_B)) for i, a in enumerate(LL, 1))}. Fact or opinion: {" · ".join(f"{s} <b>{fo(s).upper()}</b>" for s, k in FO_A + FO_B)}</p>
  <h2>A. Fix the Answer</h2>
  <table><tbody>{"".join(f"<tr><td style='width:34%'>{s}</td><td>{r}</td></tr>" for s, r in FIX)}</tbody></table>
  <h2>B. Exam-style questions</h2>
  <ol class="q">
    <li>Teenagers: "Bikes for teens", "Everyone's cycling the coast road this summer", and the picture shows two teenagers.</li>
    <li>Fact: "€15 a day" or "Open Saturdays from 9 am". Opinion: "ride the wild coast!" (a claim nobody can check).</li>
    <li>Bandwagon ("Everyone's cycling…"): nobody wants to be left out. Hurry ("only 20 bikes left for July!"): readers book now before they stop to think. Also a statistic (20 bikes).</li>
    <li>Freedom, sunshine and fun with friends: an easy, exciting day out by the sea.</li>
    <li>Any reasoned view, e.g. yes: a short, catchy slogan with alliteration ("Pedal Power"), a clear price, and tricks that suit teenagers. Reward a clear opinion backed up with two quoted reasons.</li>
  </ol>
  <h2>Marking tip</h2>
  <p>Reward a trick named + quoted + explained over a list of names, and comments on the picture and layout as well as the words. Our guide, not an official marking scheme.</p>
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
<h1><span>Media:</span><br><span>advertising</span></h1>
<div class="sub">Trick Sort cards · Ad Swap A/B<br>Poster · Worksheet + answers</div>
<div class="em">who's it for? · what's the trick?<br>fact or opinion?</div></div>
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
    pdf("teacher-pack", os.path.join(OUT, "Media-Advertising-Teacher-Pack-Leim.pdf"))
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--hide-scrollbars", "--window-size=1200,1200",
                    f"--screenshot={os.path.join(OUT, f'{SLUG}-cover.png')}", f"{SLUG}-cover.html"], cwd=SRC, check=True, capture_output=True)
