#!/usr/bin/env python3
"""The novel 1: character (JC English Order 5): free sheet (-> printables/), 6-page teacher pack + 1200x1200 cover (-> OUTDIR).
Usage: python3 src/build_character_pdfs.py /tmp/char
Extracts come from the game's data block (character-clues.html). Every answer is re-checked with the independent rules in
src/test_character_clues.py (exec'd: everything above its main loop): STEAL method by its own rules (quotes + speaker, spaCy subject,
looks words, thinking verbs), traits by its own clue-word lexicon. Styles are read from src/build_money1_pdfs.py."""
import os, sys, random, subprocess, re
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC)
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/char"; os.makedirs(OUT, exist_ok=True)
SLUG = "novel-character"
LO = "R6, R7, R4, W8"
GAME = "leim.ie/character-clues.html"
_argv = sys.argv; sys.argv = ["x", "/dev/null", os.path.join(ROOT, "character-clues.html")]
exec(open(os.path.join(SRC, "test_character_clues.py"), encoding="utf-8").read().split("errs = []")[0])
sys.argv = _argv
def W(who): return next(T for T in D["texts"] if T["who"] == who)
def card(T, cls="txt"):
    return f'<div class="{cls}"><span class="tk">{T["who"]}</span>' + "".join(f"<p><b>{i}</b>{l}</p>" for i, l in enumerate(T["lines"], 1)) + "</div>"
NAME = {k: v.split(" ")[1] for k, v in METHOD.items()} | {"effect": "Effect on others"}
def tr_word(lab): return lab.split(" ")[1].lower()
def trait_of(T, ln):
    f = traits(T["lines"][ln - 1]); assert len(f) == 1, (T["who"], ln, f)
    return tr_word(next(iter(f)))
def meth(T, ln):
    m = method(T["lines"][ln - 1], T["who"], T["pr"]); assert m == T["how"][ln - 1], (T["who"], ln, m); return NAME[m]

# ---------- free sheet ----------
FI, LE, AI = W("Fionn"), W("Leah"), W("Aisling")
def mq(T, ln): return (f"Line {ln}: which STEAL method?", f"{meth(T, ln)}")
def tq(T, ln, q): return (q, f"{trait_of(T, ln)}: “{T['q'][ln - 1]}” (line {ln})")
blocks = [(FI, [mq(FI, 2), mq(FI, 4), tq(FI, 3, "What is Fionn like? Which line proves it? Quote it.")]),
          (LE, [mq(LE, 1), mq(LE, 3), tq(LE, 2, "What is Leah like in line 2? Quote it."), tq(LE, 4, "What is she like in line 4? Quote it.")]),
          (AI, [mq(AI, 1), mq(AI, 4), tq(AI, 1, "Aisling is bossy. Which line shows it? Quote it."), tq(AI, 3, "What is she like in line 3? Quote it.")])]
assert trait_of(FI, 3) == "honest" and trait_of(LE, 2) == "shy" and trait_of(LE, 4) == "brave" and trait_of(AI, 1) == "bossy"
TF = [("kind", "T"), ("scared", "F"), ("brave", "T"), ("bored", "F"), ("honest", "T"), ("embarrassed", "F"), ("selfish", "T"), ("happy", "F")]
random.seed(55); random.shuffle(TF)
TRAITW = {tr_word(k) for k in TRAIT}
for w, a in TF: assert (w in TRAITW) == (a == "T"), w
MATCH = [(W(w), ln) for w, ln in [("Darragh", 2), ("Tadhg", 3), ("Conor", 2), ("Ciarán", 1), ("Saoirse", 1), ("Niamh", 1)]]
MATCH_ITEMS = [(f"{T['who']}: “{T['q'][ln - 1]}”", trait_of(T, ln)) for T, ln in MATCH]
assert len({a for q, a in MATCH_ITEMS}) == 6
BANK = sorted(a for q, a in MATCH_ITEMS)
SA = W("Saoirse")
assert trait_of(SA, 1) == "rude" and trait_of(SA, 4) == "kind" and meth(SA, 2) == "Effect on others"

starts = []; n = 1
for T, q in blocks: starts.append(n); n += len(q)
nTF = n; nM = nTF + len(TF); nG = nM + len(MATCH_ITEMS)
NQ = nG + 2 - 1

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
sheet = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>The novel 1: character: rules and practice | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{SHEET_STYLE}
{EXTRA}
.p2 .line{{margin-top:1px}}
</style></head><body>
<div class="page tight">
  <div class="band"><div><div class="k">Junior Cycle English · Free revision sheet</div><h1>The novel 1: character</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2015 specification): {LO}. Play the game: <b>{GAME}</b></p>
  <div class="two">
   <div><h2>1. Show, don't tell</h2>
    <p>Writers rarely say "Mia is kind". They <b>show</b> it, and you find the clues: “Mia gave half of her lunch to the new boy.”</p>
    <h2>2. STEAL: five ways to show a character</h2>
    <table class="st"><tbody>
     <tr><td><b>S</b>peech</td><td>what they say, and how: <i>“It should have been me.”</i></td></tr>
     <tr><td><b>T</b>houghts</td><td>what goes on in their head: <i>He wished he had trained harder.</i></td></tr>
     <tr><td><b>E</b>ffect on others</td><td>how other people react: <i>The others groaned but did what she said.</i></td></tr>
     <tr><td><b>A</b>ctions</td><td>what they do: <i>He handed the wallet in.</i></td></tr>
     <tr><td><b>L</b>ooks</td><td>what they look like or wear: <i>His jumper was creased.</i></td></tr></tbody></table>
    <h2>3. Words for what a character is like</h2>
    <p>kind · brave · shy · bossy · selfish · lazy · honest · jealous · funny · clever · rude<br>Stronger words for the exam: generous, loyal, determined, confident, arrogant, sly, caring, hard-working, stubborn.</p></div>
   <div><h2>4. Trait or feeling?</h2>
    <div class="wk">A <b>trait</b> is what someone is like (it lasts): <i>brave, honest</i>.<br>A <b>feeling</b> is how they feel right now (it passes): <i>scared, happy</i>.<br>Character questions want <b>traits</b>.</div>
    <h2>5. Point, quote, explain</h2>
    <div class="wk"><b>Point:</b> Ciarán is selfish.<br><b>Quote:</b> he “grabbed the biggest slice”<br><b>Explain:</b> he takes the most before anyone else sits down, so he thinks only of himself.</div>
    <h2>6. Characters change</h2>
    <p>Say what they are like at the <b>start</b> and at the <b>end</b>, with a quote for each. Leah: shy (“stared at her shoes”) → brave (“walked on stage”).</p>
    <div class="note"><b>Classic mistakes:</b> a feeling instead of a trait · a point with no quote · a quote that doesn't prove the point · copying a whole sentence · two traits with only one quote · describing what happens instead of what the character is like.</div></div>
  </div>
  <div class="tip"><b>Exam tip:</b> one trait per paragraph, each with its own short quote. "Two qualities" means two separate points.</div>
</div>

<div class="page p2">
  <div class="band"><div><div class="k">Practice · {NQ} questions</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Three short extracts</h2>
  {blocks_html}
  <h2>B. Trait or feeling? Write T or F.</h2><ol class="q" start="{nTF}" style="columns:4;column-gap:6mm">{"".join(f"<li>{w} <span class='box'>&nbsp;</span></li>" for w, a in TF)}</ol>
  <h2>C. What does each quote show? Word bank: {", ".join(BANK)}</h2>
  <ol class="q" start="{nM}" style="columns:2;column-gap:8mm">{"".join(f"<li>{q} <span class='box' style='width:22mm'>&nbsp;</span></li>" for q, a in MATCH_ITEMS)}</ol>
  <h2>D. Exam-style</h2>
  <div class="rb">{card(SA)}<ol class="q" start="{nG}">
   <li>How does Saoirse change? Quote once for the start and once for the end.<span class="long"></span><span class="long"></span></li>
   <li>What does her nan's reaction in line 2 tell you about her nan?<span class="long"></span></li></ol></div>
</div>

<div class="page">
  <div class="band"><div><div class="k">Check your work</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <table class="ans"><tbody>
   {"".join(f"<tr><td><b>A</b></td><td>{' · '.join(f'{i}. {a}' for i, (q, a) in enumerate(qq, s))}</td></tr>" for (T, qq), s in zip(blocks, starts))}
   <tr><td><b>B</b></td><td>{" · ".join(f"{i}. {a}" for i, (w, a) in enumerate(TF, nTF))}</td></tr>
   <tr><td><b>C</b></td><td>{" · ".join(f"{i}. {a}" for i, (q, a) in enumerate(MATCH_ITEMS, nM))}</td></tr>
   <tr><td><b>D</b></td><td>{nG}. At the start she is rude: she “rolled her eyes” when her nan asked about school. By the end she is kind: she “made her nan a cup of tea” and sat with her.<br>{nG + 1}. Her nan is patient and forgiving: she just “smiled and went back to her knitting” instead of getting cross.</td></tr>
  </tbody></table>
  <h2>Worked examples</h2>
  <div class="two">
   <div class="wk"><b class="h">Fionn, line 2: Thoughts</b>“For a second he thought about the new football boots he wanted.” We see inside his head: he is tempted. That makes handing the wallet in (line 3) even more <b>honest</b>.</div>
   <div class="wk"><b class="h">Leah, line 3: Effect on others</b>“Nobody in the new class knew she could sing.” The line is about other people, not Leah's own words or actions. Their surprise at the talent show is coming.</div>
   <div class="wk"><b class="h">Trait or feeling?</b>“Scared” is how Niamh might feel in the river. “Brave” is what she is like: she is scared and still “waded in after it”.</div>
   <div class="wk"><b class="h">Aisling: two traits, two quotes</b>Bossy: “and nobody talks”. Clever: she “worked out which way was north”. One quote can't prove both.</div>
  </div>
  <div class="note"><b>Got one wrong?</b> Find the line again and ask: does the character DO, SAY or THINK this, or is it someone else? Then play <b>Character Clues</b> at {GAME}: the "Go back over these" list at the end shows the clue for each mistake.</div>
  <p class="small">All extracts written by Léim. Léim is independent and not connected with the State Examinations Commission or the NCCA.</p>
</div>
</body></html>"""

# ---------- teacher pack ----------
# Trait Match: 11 point cards <-> 11 proof cards, one per trait (so every pair is unique)
TM = [("Mia", 1), ("Niamh", 1), ("Leah", 2), ("Seán", 1), ("Ciarán", 1), ("Darragh", 2), ("Fionn", 3), ("Conor", 2), ("Tadhg", 3), ("Aisling", 3), ("Saoirse", 1)]
PM = []
for who, ln in TM:
    T = W(who); t = trait_of(T, ln); q = T["q"][ln - 1]
    assert {tr_word(x) for x in traits(q)} == {t}; PM.append((f"{who} is {t}.", f"“{q}”", t))
assert len({t for c, q, t in PM}) == 11 == len(TRAIT)
cards = [(c, "claim", k) for k, (c, q, t) in enumerate(PM)] + [(q, "quote", k) for k, (c, q, t) in enumerate(PM)]
random.seed(5005); random.shuffle(cards)
pm_html = "".join(f'<div class="c"><span class="tag">{"Point" if t == "claim" else "Proof"} {i}</span><div class="fc">{s}</div></div>' for i, (s, t, k) in enumerate(cards, 1))
pm_key = " · ".join(f"{next(i for i, (s, t, kk) in enumerate(cards, 1) if t == 'claim' and kk == k)}–{next(i for i, (s, t, kk) in enumerate(cards, 1) if t == 'quote' and kk == k)}" for k in range(11))

# STEAL Swap A/B: each student reads their extract aloud; the partner labels each line S/T/E/A/L and names the trait
RO, OI = W("Róisín"), W("Oisín")
SWAP = {"A": (RO, OI), "B": (OI, RO)}
def swap_ans(T): return [(ln, meth(T, ln), next((tr for tr, l in T["traits"] if l == ln), "")) for ln in range(1, 5)]
for T in (RO, OI):
    for ln, m, tr in swap_ans(T):
        if tr: assert trait_of(T, ln) == tr
def swap_card(who):
    mine, other = SWAP[who]
    return (f'<div class="idc"><h3>Student {who}</h3>{card(mine)}<p style="font-size:8.6pt;margin:1.5mm 0 1mm">Read your extract aloud, slowly, one line at a time. Then listen to your partner\'s extract about <b>{other["who"]}</b>. For each line, write S, T, E, A or L, and the trait if the line shows one:</p>'
            + "".join(f'<div class="ss">Line {ln}: <span class="gap" style="display:inline-block;width:12%"></span> &nbsp; Trait (if any): <span class="gap" style="display:inline-block;width:40%"></span></div>' for ln in range(1, 5)) + "</div>")
def swap_line(T): return "; ".join(f"{ln} {m[0]}" + (f" ({tr})" if tr else "") for ln, m, tr in swap_ans(T))
swap_key = f"<b>A</b> (about Oisín): {swap_line(OI)} · <b>B</b> (about Róisín): {swap_line(RO)}"

WEAK = [("Mia is kind.", "No proof. Add a quote: she “gave half of her lunch”."),
        ("Mia is happy because she gave half of her lunch.", "“Happy” is a feeling, not a trait. Say kind (or generous), and quote: “gave half of her lunch”."),
        ("Ciarán is selfish: “Ciarán grabbed the biggest slice of pizza before anyone else sat down.”", "Whole sentence copied and no explanation. Quote “grabbed the biggest slice” and say why it shows selfishness."),
        ("Does Leah change? Leah is shy: “stared at her shoes”.", "Only the start. Add the end: she is brave when she “walked on stage”."),
        ("Niamh is brave: “Got him!”", "The quote doesn't prove it. Use “waded in after it”: she goes into a river for the dog."),
        ("Aisling is bossy and clever: she “worked out which way was north”.", "Two traits, one quote. Bossy needs its own proof: “and nobody talks”.")]
assert not traits("Got him!") and {tr_word(x) for x in traits("worked out which way was north")} == {"clever"}
assert "happy" not in TRAITW
SHOP = ("Everyone on Main Street knew Mrs Keane. She was seventy-eight, wore the same green cardigan every day and ran the tiny shop beside the church. "
        "Children were a little afraid of her: she frowned over her glasses and never let anyone pay later. "
        "One wet Tuesday, Josh came in soaked, counting coins that didn't add up to the price of a sandwich. "
        "“Put those away,” Mrs Keane snapped, and she handed him the sandwich anyway, with a carton of milk. "
        "“And don't tell anyone,” she muttered, turning back to her newspaper. Josh never did. "
        "But from then on, he noticed the bread she left out for the birds, and the way she always kept the last paper for old Mr Walsh.")
assert "green cardigan" in SHOP and "a little afraid" in SHOP and "handed him the sandwich" in SHOP and "don't tell anyone" in SHOP

pack = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Novel Character Teacher Pack | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{PACK_STYLE}
{EXTRA}
.fym .c{{height:26mm}}.fym .fc{{font-size:11pt;line-height:1.28;margin-top:2.5mm}}.idc{{padding:2.5mm 4mm;margin-bottom:4mm}}.idc h3{{margin:0 0 1.5mm}}
.idc .txt{{font-size:10pt}}.ss{{font-size:9.6pt;padding:2px 4px;margin:2.6mm 0}}.ss .gap{{border-bottom:1px solid #9AA3AE;height:13px;vertical-align:bottom}}
.p1 .proc td{{font-size:8.6pt;padding:2px 6px}}.ops div{{font-size:12pt;padding:4mm 3mm}}.ops b{{font-size:18pt}}.pass{{font-size:10pt;line-height:1.45}}
</style></head><body>

<div class="page p1">
  <div class="band"><div><div class="k">Junior Cycle English · Teacher pack</div><h1>The novel 1: character</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2015 specification): {LO}</p>
  <div class="two">
    <div><h3>Aims</h3><p>By the end of the lesson students can name five ways a writer shows a character (STEAL), choose a trait word rather than a feeling, back it up with a short quote (point, quote, explain), and say how a character changes.</p></div>
    <div><h3>In this pack</h3><p>p.1 Teacher notes · p.2 Trait Match cards (mingle) · p.3 STEAL Swap A/B cards (pairs) · p.4 Wall poster · p.5 Worksheet: Fix the Answer + exam-style questions · p.6 Answers. Level: 1st year (works with any class novel). Time: about 60 minutes. All extracts are original.</p></div>
  </div>
  <h2 style="margin-top:8px">Procedure</h2>
  <table class="proc"><tbody>
    <tr><td>5 min</td><td><b>Lead-in.</b> Board: “Mia gave half of her lunch to the new boy.” Is Mia kind? How do you know, if the word isn't there? Elicit <b>show, don't tell</b>.</td></tr>
    <tr><td>8 min</td><td><b>Guided discovery.</b> Show the Mia extract (poster or game). For each line, pairs decide: does Mia do, say or think it, or is it someone else? Build <b>STEAL</b> on the board.</td></tr>
    <tr><td>12 min</td><td><b>Trait Match</b> (p.2, mingle). Hand out one card each (22 cards: 11 points, 11 proofs). Students read their card aloud and find the partner card, then explain the link in one sentence ("Grabbing the biggest slice shows he's selfish").</td></tr>
    <tr><td>12 min</td><td><b>STEAL Swap</b> (p.3, pairs, A/B). Each student reads their extract aloud line by line; the partner listens and labels each line S, T, E, A or L, plus the trait it shows. Then swap.</td></tr>
    <tr><td>18 min</td><td><b>Worksheet</b> (p.5). Fix the Answer in pairs (what's missing? improve it), then the exam-style questions on “Mrs Keane” alone.</td></tr>
    <tr><td>5 min</td><td><b>Exit ticket.</b> One trait of a character from the class novel, with a quote and an explanation. Homework: play <b>Character Clues</b> at {GAME}.</td></tr>
  </tbody></table>
  <div class="note"><b>Trait Match pairs (point–proof):</b> {pm_key}.<br>
  <b>Errors to look for:</b> feelings instead of traits · points with no quote · quotes that don't prove the point · retelling the plot · one quote for two traits. <b>Support:</b> the poster (p.4) on the desk. <b>Fast finishers:</b> write a 4-line extract that shows a character using all five STEAL methods.</div>
  <p class="small"><b>STEAL Swap answers:</b> {swap_key}.</p>
</div>

<div class="page">
  <div class="band"><div><div class="k">Whole class · one card each</div><h1>Trait Match</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.4pt;margin:0 0 2mm">Cut up the 22 cards. <b>Point</b> cards say what a character is like; <b>Proof</b> cards are short quotes. Read your card aloud, find your partner, then say how the quote proves the point.</p>
  <div class="fym">{pm_html}</div>
</div>

<div class="page">
  <div class="band"><div><div class="k">Pairs · Student A and Student B</div><h1>STEAL Swap</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.4pt">Cut along the middle. Don't show your card. Take turns: read your extract aloud; your partner listens and labels each line. S = Speech, T = Thoughts, E = Effect on others, A = Actions, L = Looks.</p>
  {swap_card("A")}
  {swap_card("B")}
</div>

<div class="page">
  <div class="poster">
    <h1>STEAL a character</h1>
    <div class="ops">
      <div style="background:var(--green-soft)"><b>Speech</b>what they say<br>and how they say it</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Thoughts</b>what goes on<br>in their head</div>
      <div style="background:var(--green-soft)"><b>Effect on others</b>how other people<br>react to them</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Actions</b>what they do</div>
      <div style="background:var(--green-soft)"><b>Looks</b>what they look like<br>or wear</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Prove it</b>trait · quote · explain</div>
    </div>
    <p style="text-align:center;font-size:20pt!important;font-weight:800;margin:4mm 0">Don't tell me. Show me.</p>
    <p style="text-align:center;font-size:10pt;color:var(--muted)">Léim · leim.ie · Play Character Clues: {GAME}</p>
  </div>
</div>

<div class="page ws">
  <div class="band"><div><div class="k">Worksheet</div><h1>Fix the Answer + exam-style questions</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Fix the Answer</h2>
  <p>Each student answer has one problem. Say what's wrong and improve it. (Characters from Character Clues: Mia, Ciarán, Leah, Niamh and Aisling.)</p>
  <table class="eh"><thead><tr><th>Student answer</th><th>What's wrong and a better answer</th></tr></thead><tbody>
  {"".join(f"<tr><td>{w}</td><td><span class='gap'></span><span class='gap'></span></td></tr>" for w, f in WEAK)}
  </tbody></table>
  <h2>B. Exam-style questions</h2>
  <div class="pass"><b>Mrs Keane</b><br>{SHOP}</div>
  <ol class="q">
    <li>What do we learn about Mrs Keane from her looks? Give one detail.<span class="long"></span></li>
    <li>How do the children react to Mrs Keane at first, and why?<span class="long"></span></li>
    <li>What kind of person is Mrs Keane really? Give two qualities, with a quote for each.<span class="long"></span><span class="long"></span></li>
    <li>Why do you think she says, “And don't tell anyone”?<span class="long"></span></li>
    <li>Would you like to have Mrs Keane as a neighbour? Give a reason based on the text.<span class="long"></span></li>
  </ol>
</div>

<div class="page an">
  <div class="band"><div><div class="k">For the teacher</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>Trait Match</h2>
  <p>{pm_key}. (Points: {"; ".join(c.rstrip(".") for c, q, t in PM)}.)</p>
  <h2>STEAL Swap</h2>
  <p>{swap_key}.</p>
  <h2>A. Fix the Answer</h2>
  <table><tbody>{"".join(f"<tr><td style='width:42%'>{w}</td><td>{f}</td></tr>" for w, f in WEAK)}</tbody></table>
  <h2>B. Exam-style questions</h2>
  <ol class="q">
    <li>e.g. She is old (“seventy-eight”) and wears “the same green cardigan every day”: she is plain and set in her ways, not fussy about clothes.</li>
    <li>They are “a little afraid of her”, because she “frowned over her glasses” and never let anyone pay later: she seems strict and unfriendly.</li>
    <li>e.g. Generous: she “handed him the sandwich anyway, with a carton of milk”. Caring: she leaves “bread … for the birds” and keeps “the last paper for old Mr Walsh”. (Also accept modest or private, with proof.)</li>
    <li>e.g. She doesn't want praise, or she wants to keep her strict image: she is kind in private, not for show.</li>
    <li>Either answer, backed up: e.g. yes, because under the frown she quietly looks after people (“kept the last paper for old Mr Walsh”).</li>
  </ol>
  <h2>Marking tip</h2>
  <p>Credit a trait word (not a feeling), a short accurate quote, and a sentence explaining how the quote shows the trait. Retelling the plot without naming a trait is usually worth little.</p>
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
<h1><span>The novel:</span><br><span>character</span></h1>
<div class="sub">Trait Match cards · STEAL Swap A/B<br>Poster · Worksheet + answers</div>
<div class="em">S · T · E · A · L</div></div>
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
    pdf("teacher-pack", os.path.join(OUT, "Novel-Character-Teacher-Pack-Leim.pdf"))
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--hide-scrollbars", "--window-size=1200,1200",
                    f"--screenshot={os.path.join(OUT, f'{SLUG}-cover.png')}", f"{SLUG}-cover.html"], cwd=SRC, check=True, capture_output=True)
