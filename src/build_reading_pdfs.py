#!/usr/bin/env python3
"""Reading for meaning (JC English Order 4): free sheet (-> printables/), 6-page teacher pack + 1200x1200 cover (-> OUTDIR).
Usage: python3 src/build_reading_pdfs.py /tmp/read
Texts come from the game's data block (clue-hunt.html). Every answer is re-checked with the independent rules in
src/test_clue_hunt.py (exec'd: everything above its main loop): clue words only in the answer line, fact answers in exactly one line,
best titles by spaCy lemma coverage, feelings by its own clue-word lexicon, fact/opinion by its judgement-word list.
Styles are read from src/build_money1_pdfs.py."""
import os, sys, random, subprocess, re, json
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC)
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/read"; os.makedirs(OUT, exist_ok=True)
SLUG = "reading-for-meaning"
LO = "R1, R2, R3, OL4"
GAME = "leim.ie/clue-hunt.html"
_argv = sys.argv; sys.argv = ["x", "/dev/null", os.path.join(ROOT, "clue-hunt.html")]
exec(open(os.path.join(SRC, "test_clue_hunt.py"), encoding="utf-8").read().split("bad = n = 0")[0])
sys.argv = _argv
TX = {T["lines"][0].split()[0] + str(i): T for i, T in enumerate(D["texts"])}
def T_(start): return next(T for T in D["texts"] if T["lines"][0].startswith(start))
def card(T, cls="txt"):
    return f'<div class="{cls}"><span class="tk">{re.sub(r"^[^A-Za-z]+", "", T["k"])}</span>' + "".join(f"<p><b>{i}</b>{l}</p>" for i, l in enumerate(T["lines"], 1)) + "</div>"
NO_EMOJI = lambda s: re.sub(r"^[^\w€]+", "", s).strip()
def letters(opts): return " &nbsp; ".join(f"<b>{c}</b> {o}" for c, o in zip("abcd", opts))

# ---------- free sheet ----------
SK, BUS, CAMP, DI = T_("Skellig"), T_("Aoife"), T_("Splash"), T_("Dear diary")
blocks = []   # (text, [(question html, answer text)])
def title_q(T, seed):
    opts = T["main"][:]; random.seed(seed); random.shuffle(opts)
    for m in check_main(T, T["main"][0], T["main"][1:]): raise AssertionError(m)
    return (f"Best title? {letters(opts)}", f"{'abcd'[opts.index(T['main'][0])]} ({T['main'][0]})")
def fact_q(T, f):
    q, a, w, ln = f; assert not check_fact(T, q, a, w, ln), (q, check_fact(T, q, a, w, ln))
    return (NO_EMOJI(q) + " Which line?", f"{a} (line {ln})")
def proof_q(T, p):
    c, ln, clue = p; assert not check_proof(T, c, ln, clue), c
    return (f"“{c}” Which line proves it? Quote it.", f"line {ln}: “{clue}”")
def feel_q(T, f):
    q, k, clues, lines = f; ans = FEELMAP[k]
    assert not check_feel(T, ans, [v for v in FEELMAP.values() if v != ans and v not in CLOSE.get(ans, ())], lines), q
    return (q + " Give the clue.", f"{NO_EMOJI(ans).lower()}: “{clues[-1]}” (line {lines[-1]})")
for T, seed in [(SK, 1), (BUS, 2), (CAMP, 3)]:
    qs_ = [fact_q(T, f) for f in T["facts"]] + [proof_q(T, p) for p in T["proofs"][:2]] + [feel_q(T, f) for f in T["feel"]] + [title_q(T, seed)]
    blocks.append((T, qs_))
FO_ITEMS = [(s, "fact") for s in D["fo"]["f"][:4]] + [(s, "opinion") for s in D["fo"]["o"][:4]]
random.seed(44); random.shuffle(FO_ITEMS)
for s, k in FO_ITEMS: assert is_opinion(s) == (k == "opinion"), s
NQ = sum(len(q) for T, q in blocks) + len(FO_ITEMS) + 2
starts = []; n = 1
for T, q in blocks: starts.append(n); n += len(q)
nFO = n; nG = n + len(FO_ITEMS)
assert NQ == nG + 1

def qs(items, start): return f'<ol class="q" start="{start}">' + "".join(f"<li>{q}<span class='line'></span></li>" for q, a in items) + "</ol>"
def style(var):
    return re.search(var + r' = f"""<!doctype.*?<style>(.*?)</style>', open(os.path.join(SRC, "build_money1_pdfs.py"), encoding="utf-8").read(), re.S).group(1).replace("{LO}", LO).replace("{{", "{").replace("}}", "}").replace("JC Maths LOs (2018 spec)", "JC English LOs (2015 spec)")
SHEET_STYLE = style("sheet"); PACK_STYLE = style("pack")
assert "JC English LOs (2015 spec)" in SHEET_STYLE and "Single-teacher licence" in PACK_STYLE and "JC English LOs (2015 spec)" in PACK_STYLE
EXTRA = """.wk{line-height:1.45;border:1.5px solid var(--line);border-radius:8px;padding:2px 7px;margin:3px 0;font-size:9.4pt}.wk b.h{display:block}
table.st{border-collapse:collapse;margin:3px 0;font-size:9.4pt;width:100%}table.st td,table.st th{border:1px solid #C9D1DA;padding:2px 6px;text-align:left}
.pass{border-left:4px solid var(--green);background:var(--mist);padding:5px 10px;margin:4px 0}
.txt{border:1.5px solid var(--line);border-radius:8px;padding:3px 8px;font-size:9.2pt;line-height:1.3;background:#fff}
.txt p{margin:1.2px 0;display:flex;gap:5px}.txt p b{flex:0 0 13px;height:13px;border-radius:50%;background:#1B2430;color:#fff;font-size:7pt;display:inline-flex;align-items:center;justify-content:center;margin-top:1px}
.txt .tk{font-size:7.6pt;font-weight:800;color:var(--muted);text-transform:uppercase;letter-spacing:.04em}
.rb{display:grid;grid-template-columns:45% 1fr;gap:4mm;margin:1.6mm 0;break-inside:avoid}.rb ol.q{margin:0}"""

blocks_html = "".join(f'<div class="rb">{card(T)}{qs(q, s)}</div>' for (T, q), s in zip(blocks, starts))
sheet = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Reading for meaning: rules and practice | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{SHEET_STYLE}
{EXTRA}
.p2 .line{{margin-top:1px}}
</style></head><body>
<div class="page tight">
  <div class="band"><div><div class="k">Junior Cycle English · Free revision sheet</div><h1>Reading for meaning</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2015 specification): {LO}. Play the game: <b>{GAME}</b></p>
  <div class="two">
   <div><h2>1. Four ways to read</h2>
    <table class="st"><tbody>
     <tr><td><b>Skim</b></td><td>for the big idea: title, first line, last line. What's it about? Who's it for?</td></tr>
     <tr><td><b>Scan</b></td><td>for one fact: run your eye down the text looking for one kind of word.</td></tr>
     <tr><td><b>Infer</b></td><td>read between the lines: the text shows a feeling without naming it.</td></tr>
     <tr><td><b>Prove it</b></td><td>back up every point with a short quote.</td></tr></tbody></table>
    <h2>2. Question words: what to hunt for</h2>
    <table class="st"><tbody>
     <tr><td><b>When? What time?</b></td><td>days, dates, times: <i>at dawn, the 14th, May</i></td></tr>
     <tr><td><b>How many? How much?</b></td><td>numbers, prices: <i>over 600, €95</i></td></tr>
     <tr><td><b>Who? Where?</b></td><td>names and places (capital letters!)</td></tr>
     <tr><td><b>Why?</b></td><td>because, so, as, since</td></tr></tbody></table>
    <h2>3. Read between the lines</h2>
    <table class="st"><tbody>
     <tr><td>hands shaking, froze</td><td>scared</td></tr><tr><td>stomach in knots</td><td>nervous</td></tr>
     <tr><td>face went red</td><td>embarrassed</td></tr><tr><td>sighing, nothing to do</td><td>bored</td></tr>
     <tr><td>grinning, jumped on her</td><td>happy</td></tr><tr><td>writing to complain</td><td>angry</td></tr></tbody></table></div>
   <div><h2>4. Point, quote, explain</h2>
    <div class="wk"><b>Point:</b> Rua is scared.<br><b>Quote:</b> “her hands started shaking”<br><b>Explain:</b> shaking hands show fear: every rattle of the roof frightens her.</div>
    <p>Keep quotes short (3–6 words) and put them in quotation marks. Use your own words for the point.</p>
    <h2>5. Fact or opinion?</h2>
    <div class="wk"><b>Fact</b>: can be checked. <i>The tickets cost €12.</i><br><b>Opinion</b>: what someone thinks. <i>The tickets are too expensive.</i><br>Opinion clue words: best, worst, boring, amazing, should, too, I think.</div>
    <h2>6. The best-title test</h2>
    <p>A good title covers the <b>whole</b> text. A wrong one usually fits just one line: it's a detail, not the main idea.</p>
    <h2>7. Traps</h2>
    <p>Wrong answers are often real words from the text, from the wrong line (the bus trip was on <i>Saturday</i>, but the new date is <i>the 14th</i>). Read the whole line around your answer.</p>
    <div class="note"><b>Classic mistakes:</b> a point with no quote · a quote with no explanation · copying out a whole paragraph · answering a different question · giving one reason when the question asks for two.</div></div>
  </div>
  <div class="tip"><b>Exam tip:</b> read the questions before the text. Then you know what you're hunting for, and you read with a purpose.</div>
</div>

<div class="page p2">
  <div class="band"><div><div class="k">Practice · {NQ} questions</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Three short texts</h2>
  {blocks_html}
  <h2>B. Fact or opinion? Write F or O.</h2><ol class="q" start="{nFO}" style="columns:2;column-gap:8mm">{"".join(f"<li>{s} <span class='box'>&nbsp;</span></li>" for s, k in FO_ITEMS)}</ol>
  <h2>C. Exam-style (use the bus text above)</h2>
  <ol class="q" start="{nG}">
   <li>What impression do you get of Aoife? Use point, quote, explain.<span class="long"></span><span class="long"></span></li>
   <li>Is the driver kind or unkind? Give a reason from the text.<span class="long"></span></li>
  </ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">Check your work</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <table class="ans"><tbody>
   {"".join(f"<tr><td><b>A</b></td><td>{' · '.join(f'{i}. {a}' for i, (q, a) in enumerate(qq, s))}</td></tr>" for (T, qq), s in zip(blocks, starts))}
   <tr><td><b>B</b></td><td>{" · ".join(f"{i}. {'O' if k == 'opinion' else 'F'}" for i, (s, k) in enumerate(FO_ITEMS, nFO))}</td></tr>
   <tr><td><b>C</b></td><td>{nG}. e.g. Aoife is easily distracted: she got on the bus “without looking up from her phone”, so she didn't check where it was going. (Or: she's embarrassed: “her face went red”.)<br>{nG + 1}. Kind: he “laughed” but he “told her the right bus stopped across the road”, so he helped her.</td></tr>
  </tbody></table>
  <h2>Worked examples</h2>
  <div class="two">
   <div class="wk"><b class="h">Skellig: “The sea is rough in winter.”</b>The text never says “rough” or “winter”. But line 4 says boats only sail “when the sea is calmer” (May to September), so the rest of the year it must be rougher. That's an <b>inference</b>.</div>
   <div class="wk"><b class="h">Bus: best title?</b>“A new phone” only fits line 1; “A friendly driver” only fits line 4. “Aoife gets on the wrong bus” covers the whole story: that's the <b>main idea</b>.</div>
   <div class="wk"><b class="h">Camp: “€95” or “€10”?</b>Both are in the text, but “10% off” is a discount, not the price. The cost is in line 3: “€95 a week”. That's a <b>trap</b>: always read the whole line.</div>
   <div class="wk"><b class="h">Fact or opinion?</b>“Hurling is played with a hurley and a sliotar” can be checked: fact. “Hurling is the most exciting sport” is what someone thinks: opinion.</div>
  </div>
  <div class="note"><b>Got one wrong?</b> Find the line again and read the whole sentence around it. Then play <b>Clue Hunt</b> at {GAME}: the "Go back over these" list at the end shows the clue for each mistake.</div>
  <p class="small">All texts written by Léim. Léim is independent and not connected with the State Examinations Commission or the NCCA.</p>
</div>
</body></html>"""
assert CAMP["facts"][0][1] == "€95" and "10% off" in CAMP["lines"][3] and BUS["main"][0].startswith("Aoife") and "calmer" in SK["lines"][3]

# ---------- teacher pack ----------
# Proof Match: 12 claim cards <-> 12 quote cards, each from a different text, each checked by check_proof
PM = []
for T in D["texts"]:
    c, ln, clue = T["proofs"][0] if T is not D["texts"][2] else T["proofs"][1]
    assert not check_proof(T, c, ln, clue); PM.append((c, clue))
assert len(PM) == 12 and len({c for c, q in PM}) == 12 and len({q for c, q in PM}) == 12
cards = [(c, "claim", k) for k, (c, q) in enumerate(PM)] + [(f"“{q}”", "quote", k) for k, (c, q) in enumerate(PM)]
random.seed(4004); random.shuffle(cards)
pm_html = "".join(f'<div class="c"><span class="tag">{"Point" if t == "claim" else "Proof"} {i}</span><div class="fc">{s}</div></div>' for i, (s, t, k) in enumerate(cards, 1))
pm_key = " · ".join(f"{next(i for i, (s, t, kk) in enumerate(cards, 1) if t == 'claim' and kk == k)}–{next(i for i, (s, t, kk) in enumerate(cards, 1) if t == 'quote' and kk == k)}" for k in range(12))

# Scan Swap A/B: each student has one text and asks the partner about the other text
HH, BU = T_("Hedgehogs"), T_("The Burren")
SWAP = {"A": (HH, [("Where is the Burren?", "County Clare"), ("Its plants come from which two places?", "the Arctic and the Mediterranean"),
                   ("What colour are the gentians?", "blue"), ("When do farmers move cattle up the hills?", "for the winter")]),
        "B": (BU, [("When do hedgehogs sleep?", "about November to March"), ("What do they eat before they hibernate?", "beetles and worms"),
                   ("What often hits them?", "cars"), ("What helps them travel safely?", "a small gap at the bottom of your garden fence")])}
for who, (mine, qq) in SWAP.items():
    other = BU if mine is HH else HH
    for q, a in qq: assert len(fact_line(other, a)) == 1 and not fact_line(mine, a), (q, a)
def swap_card(who):
    mine, qq = SWAP[who]
    return (f'<div class="idc"><h3>Student {who}</h3>{card(mine)}<p style="font-size:8.6pt;margin:1.5mm 0 1mm">Your partner asks you about <b>your</b> text. Scan for the answer and read it out. Then ask your questions and write the answers:</p>'
            + "".join(f'<div class="ss">{q} <span class="gap" style="display:inline-block;width:42%"></span></div>' for q, a in qq) + "</div>")
swap_key = " · ".join(f"<b>{w}</b>: " + "; ".join(a for q, a in SWAP[w][1]) for w in "AB")

WEAK = [("Rua is scared.", "No proof. Add a quote: “her hands started shaking”."),
        ("Rua is scared because “Every time the roof rattled, her hands started shaking. At dawn the storm passed, and the beach was covered in seaweed.”", "Quote far too long. Keep 3–6 words: “her hands started shaking”."),
        ("Rua is scared: “her hands started shaking”.", "No explanation. Add: shaking hands are a sign of fear."),
        ("The camp costs €10.", "Trap: 10% is the discount. Line 3: “€95 a week”."),
        ("“Pizza is delicious” is a fact because lots of people like pizza.", "It's an opinion: it can't be checked. Liking something is an opinion."),
        ("Two reasons Aoife was late: she was on her phone.", "Only one reason. Add a second: she got on the wrong bus / went 20 minutes the wrong way.")]
for w, f in WEAK[:3]: assert "shaking" in T_("The wind")["lines"][2]
assert is_opinion("Pizza is delicious.")
SEA = ("Every New Year's Day, hundreds of people gather at the Forty Foot in Dublin for a swim. The sea is usually around nine or ten degrees. "
       "This year, my aunt Gráinne dragged me along. Standing on the steps, I couldn't feel my toes, and my teeth were chattering. "
       "“Just jump!” she shouted, already laughing in the water. I counted to three, held my nose and leapt. For one second I couldn't breathe. "
       "Then I surfaced, gasping and grinning, and I understood why people come back every year.")
assert "😊 Happy" in feelings("gasping and grinning") and "grinning" in SEA and "chattering" in SEA

pack = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Reading for Meaning Teacher Pack | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{PACK_STYLE}
{EXTRA}
.fym .c{{height:24mm}}.fym .fc{{font-size:10.6pt;line-height:1.28;margin-top:2.5mm}}.idc{{padding:2.5mm 4mm;margin-bottom:4mm}}.idc h3{{margin:0 0 1.5mm}}
.idc .txt{{font-size:10pt}}.ss{{font-size:9.6pt;padding:2px 4px;margin:1.6mm 0}}
.p1 .proc td{{font-size:8.6pt;padding:2px 6px}}.ops div{{font-size:12pt;padding:4mm 3mm}}.ops b{{font-size:18pt}}.pass{{font-size:10pt;line-height:1.45}}
</style></head><body>

<div class="page p1">
  <div class="band"><div><div class="k">Junior Cycle English · Teacher pack</div><h1>Reading for meaning</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2015 specification): {LO}</p>
  <div class="two">
    <div><h3>Aims</h3><p>By the end of the lesson students can skim a text for its main idea, scan for a fact, infer a feeling from clues, tell fact from opinion, and back up a point with a short quote (point, quote, explain).</p></div>
    <div><h3>In this pack</h3><p>p.1 Teacher notes · p.2 Proof Match cards (mingle) · p.3 Scan Swap A/B cards (pairs) · p.4 Wall poster · p.5 Worksheet: Fix the Answer + exam-style questions · p.6 Answers. Level: 1st year (useful revision in 2nd and 3rd). Time: about 60 minutes. All texts are original.</p></div>
  </div>
  <h2 style="margin-top:8px">Procedure</h2>
  <table class="proc"><tbody>
    <tr><td>5 min</td><td><b>Lead-in.</b> Board three questions about the storm text (poster or game): When did the storm pass? How does Rua feel? Best title? Pairs: which needs one word, which needs a clue, which needs the whole text? Elicit <b>scan, infer, skim</b>.</td></tr>
    <tr><td>8 min</td><td><b>Guided discovery.</b> Show a point with no quote and a point with a whole-paragraph quote. Which is better? Neither: build <b>point + short quote + explain</b> together.</td></tr>
    <tr><td>12 min</td><td><b>Proof Match</b> (p.2, mingle). Hand out one card each (24 cards: 12 points, 12 proofs). Students read their card aloud to each other and find the partner card. Pairs then explain the link in one sentence ("Shaking shows she's scared").</td></tr>
    <tr><td>12 min</td><td><b>Scan Swap</b> (p.3, pairs, A/B). Each student has one text and questions about the partner's text. They take turns asking; the partner scans and reads the answer aloud. No peeking at each other's card.</td></tr>
    <tr><td>18 min</td><td><b>Worksheet</b> (p.5). Fix the Answer in pairs (what's missing? improve it), then the exam-style questions alone.</td></tr>
    <tr><td>5 min</td><td><b>Exit ticket.</b> One point + quote + explain about Aunt Gráinne. Homework: play <b>Clue Hunt</b> at {GAME}.</td></tr>
  </tbody></table>
  <div class="note"><b>Proof Match pairs (point–proof):</b> {pm_key}.<br>
  <b>Errors to look for:</b> points with no proof · long copied quotes · quotes with no explanation · grabbing a word from the wrong line (the trap) · treating "lots of people think so" as a fact. <b>Support:</b> the poster (p.4) on the desk. <b>Fast finishers:</b> write a 4-line text of their own with one hidden feeling for a partner to infer.</div>
  <p class="small"><b>Scan Swap answers:</b> {swap_key}.</p>
</div>

<div class="page">
  <div class="band"><div><div class="k">Whole class · one card each</div><h1>Proof Match</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.4pt;margin:0 0 2mm">Cut up the 24 cards. <b>Point</b> cards say something about a text; <b>Proof</b> cards are short quotes. Read your card aloud, find your partner, then say how the quote proves the point.</p>
  <div class="fym">{pm_html}</div>
</div>

<div class="page">
  <div class="band"><div><div class="k">Pairs · Student A and Student B</div><h1>Scan Swap</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.4pt">Cut along the middle. Don't show your card. Take turns: ask a question, your partner scans their text and reads the answer aloud, you write it down.</p>
  {swap_card("A")}
  {swap_card("B")}
</div>

<div class="page">
  <div class="poster">
    <h1>Be a reading detective</h1>
    <div class="ops">
      <div style="background:var(--green-soft)"><b>Skim</b>the big idea<br>title · first line · last line</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Scan</b>one fact<br>when · how many · who · where</div>
      <div style="background:var(--green-soft)"><b>Infer</b>read between the lines<br>shaking → scared</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Prove it</b>point · quote · explain</div>
      <div style="background:var(--green-soft)"><b>Fact</b>can be checked<br><b>Opinion</b> what someone thinks</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Traps</b>right word,<br>wrong line</div>
    </div>
    <p style="text-align:center;font-size:20pt!important;font-weight:800;margin:4mm 0">No point without proof.</p>
    <p style="text-align:center;font-size:10pt;color:var(--muted)">Léim · leim.ie · Play Clue Hunt: {GAME}</p>
  </div>
</div>

<div class="page ws">
  <div class="band"><div><div class="k">Worksheet</div><h1>Fix the Answer + exam-style questions</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Fix the Answer</h2>
  <p>Each student answer has one problem. Say what's wrong and improve it. (Texts: the storm, the camp advert and the wrong bus from Clue Hunt.)</p>
  <table class="eh"><thead><tr><th>Student answer</th><th>What's wrong and a better answer</th></tr></thead><tbody>
  {"".join(f"<tr><td>{w}</td><td><span class='gap'></span><span class='gap'></span></td></tr>" for w, f in WEAK)}
  </tbody></table>
  <h2>B. Exam-style questions</h2>
  <div class="pass"><b>The Jump</b><br>{SEA}</div>
  <ol class="q">
    <li>Find two facts about the New Year's Day swim.<span class="long"></span></li>
    <li>How does the writer feel on the steps? Support your answer with reference to the text.<span class="long"></span><span class="long"></span></li>
    <li>What impression do you get of Aunt Gráinne? Point, quote, explain.<span class="long"></span><span class="long"></span></li>
    <li>How do the writer's feelings change by the end? Quote to show the change.<span class="long"></span><span class="long"></span></li>
    <li>Suggest a better title for this text and explain why it fits the whole text.<span class="long"></span></li>
  </ol>
</div>

<div class="page an">
  <div class="band"><div><div class="k">For the teacher</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>Proof Match</h2>
  <p>{pm_key}. (Points: {"; ".join(c for c, q in PM)}.)</p>
  <h2>Scan Swap</h2>
  <p>{swap_key}.</p>
  <h2>A. Fix the Answer</h2>
  <table><tbody>{"".join(f"<tr><td style='width:42%'>{w}</td><td>{f}</td></tr>" for w, f in WEAK)}</tbody></table>
  <h2>B. Exam-style questions</h2>
  <ol class="q">
    <li>Any two: it happens every New Year's Day · it's at the Forty Foot in Dublin · hundreds of people take part · the sea is around nine or ten degrees.</li>
    <li>Cold and nervous: “I couldn't feel my toes” and “my teeth were chattering”; chattering teeth show cold and fear.</li>
    <li>e.g. She is bold and fun-loving: she “dragged me along” and was “already laughing in the water”, so she isn't afraid of the cold and enjoys it.</li>
    <li>From scared and frozen (“teeth were chattering”, “couldn't breathe”) to delighted (“gasping and grinning”); now the writer understands “why people come back”.</li>
    <li>e.g. “My First New Year's Swim” or “Just Jump!”: it covers the build-up, the jump and the happy ending, not just one detail.</li>
  </ol>
  <h2>Marking tip</h2>
  <p>Credit a clear point in the student's own words, a short accurate quote, and a sentence explaining how the quote proves the point. A point without reference to the text is usually worth about half.</p>
</div>
</body></html>"""

cover = """<!doctype html><html><head><meta charset="utf-8"><style>
body{margin:0;width:1200px;height:1200px;background:#1B2430;font-family:Inter,sans-serif;color:#fff;display:flex;flex-direction:column;justify-content:space-between;padding:90px;box-sizing:border-box}
.k{display:inline-block;background:#2E7D57;border-radius:99px;padding:12px 26px;font-weight:700;font-size:28px;letter-spacing:.06em;text-transform:uppercase}
h1{font-size:104px;font-weight:800;line-height:1.3;letter-spacing:-.02em;margin:60px 0 20px}
h1 span{background:#F6CF5A;color:#1B2430;padding:0 18px;border-radius:14px}
.sub{font-size:40px;line-height:1.4;color:#DDE3EA}
.em{font-size:52px;margin-top:30px;font-weight:800;letter-spacing:.01em;color:#F6CF5A}
.foot{display:flex;justify-content:space-between;align-items:center;font-size:34px;font-weight:700}
.price{background:#F6CF5A;color:#1B2430;border-radius:16px;padding:14px 28px}
</style></head><body>
<div><span class="k">Junior Cycle English · Teacher pack</span>
<h1><span>Reading for</span><br><span>meaning</span></h1>
<div class="sub">Proof Match cards · Scan Swap A/B<br>Poster · Worksheet + answers</div>
<div class="em">skim · scan · infer · prove it</div></div>
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
    pdf("teacher-pack", os.path.join(OUT, "Reading-for-Meaning-Teacher-Pack-Leim.pdf"))
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--hide-scrollbars", "--window-size=1200,1200",
                    f"--screenshot={os.path.join(OUT, f'{SLUG}-cover.png')}", f"{SLUG}-cover.html"], cwd=SRC, check=True, capture_output=True)
