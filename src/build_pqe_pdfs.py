#!/usr/bin/env python3
"""Answering on texts: point, quote, explain (JC English Order 29): free sheet (-> printables/), 6-page teacher pack + 1200x1200 cover (-> OUTDIR).
Usage: python3 src/build_pqe_pdfs.py /tmp/p29
Reads the game's data block (pqe-builder.html) and re-checks every answer with the checker's own functions
(src/test_pqe_builder.py: shows, names, key_of, part, why_bad, quote_kind). The checker's data pass runs first.
Styles are read from src/build_money1_pdfs.py."""
import os, sys, random, subprocess, re
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC); sys.path.insert(0, SRC)
from test_pqe_builder import load, data_pass, shows, names, key_of, part, why_bad, quote_kind
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/p29"; os.makedirs(OUT, exist_ok=True)
SLUG = "answering-on-texts-pqe"
LO = "R3, R4, R7, W7, W8"
GAME = "leim.ie/pqe-builder.html"
D = load(os.path.join(ROOT, "pqe-builder.html")); data_pass(D)
PL = {"p": "Point", "q": "Quote", "e": "Explain"}

def style(var):
    return re.search(var + r' = f"""<!doctype.*?<style>(.*?)</style>', open(os.path.join(SRC, "build_money1_pdfs.py"), encoding="utf-8").read(), re.S).group(1).replace("{LO}", LO).replace("{{", "{").replace("}}", "}").replace("JC Maths LOs (2018 spec)", "JC English LOs (2015 spec)")
SHEET_STYLE = style("sheet"); PACK_STYLE = style("pack")
assert "JC English LOs (2015 spec)" in SHEET_STYLE and "Single-teacher licence" in PACK_STYLE and "JC English LOs (2015 spec)" in PACK_STYLE
EXTRA = """.wk{line-height:1.4;border:1.5px solid var(--line);border-radius:8px;padding:2px 7px;margin:3px 0;font-size:9.2pt}.wk b.h{display:block}
table.st{border-collapse:collapse;margin:3px 0;font-size:9pt;width:100%}table.st td,table.st th{border:1px solid #C9D1DA;padding:2px 6px;text-align:left;vertical-align:top}
.pass{border-left:4px solid var(--green);background:var(--mist);padding:5px 10px;margin:4px 0;font-size:9.3pt;line-height:1.5}
.pass .sp{display:block;margin:1px 0}.qt{font-family:Georgia,serif;font-style:italic}.tc{border:1.5px solid var(--line);border-radius:8px;padding:3px 8px;margin:3px 0;font-size:9.2pt;line-height:1.45}.tc .k{font-size:8pt;font-weight:700;color:var(--muted)}"""
L = "<span class='line' style='min-width:34mm'></span>"
def li(i, s): return f"<li value='{i}'>{s}</li>"
def tcard(T): return f"<div class='tc'><span class='k'>{T['title']}</span><br>" + "<br>".join(T["lines"]) + "</div>"

# ---------- free sheet ----------
random.seed(2901)
TA = random.sample(D["texts"], 2)
A = []
for T in TA:
    for i in [i for i, k in enumerate(T["keys"]) if k]:
        k = key_of(T["pts"][i]); assert shows(T["q"][i]) == {k}
        A.append((T["pts"][i], T["q"][i]))
A = A[:6]; assert len(A) == 6
B = []
for a in random.sample(D["answers"], 3):
    for s in a: B.append((s, part(s)))
random.shuffle(B)
C = random.sample(D["explain"], 2)
C_items = []
for p, q, good, *bad in C:
    k = key_of(p); opts = [good] + bad; random.shuffle(opts)
    assert [not why_bad(k, q, o) for o in opts].count(True) == 1
    C_items.append((p, q, opts, "abcd"[[not why_bad(k, q, o) for o in opts].index(True)]))
Dx = random.sample(D["exact"], 3)
for p, line, q, mis, para in Dx: assert quote_kind(line, key_of(p), "“" + q + "”") == "good"
E = random.sample(D["qs"], 2)
E_items = []
for qn, right, wrong in E:
    k = key_of(qn); opts = [right] + wrong; random.shuffle(opts)
    assert [k in names(o) for o in opts].count(True) == 1
    E_items.append((qn, opts, "abcd"[[k in names(o) for o in opts].index(True)]))
nA = 1; nB = nA + 6; nC = nB + 9; nD = nC + 2; nE = nD + 3; nF = nE + 2
NQ = nF + 1; assert NQ == 24, NQ

F_TEXT = ("The Bake Sale", "Ciara set her lemon cake on the table and stepped back. Around her the hall buzzed with parents and pushing children. "
          "She checked the price card for the third time and smoothed her apron. When a woman finally bought a slice, Ciara's face lit up, "
          "and she counted the coins twice before dropping them into the tin.")
assert shows("she counted the coins twice") == set()

sheet = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Answering on texts: point, quote, explain, rules and practice | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{SHEET_STYLE}
{EXTRA}
.p2 ol.q li{{margin-bottom:2px;font-size:9pt}}.p2 h2{{margin:4px 0 2px}}.p2 .two{{gap:6mm}}.p2 .tc{{font-size:8.8pt;line-height:1.35}}
ol.ab{{list-style:lower-alpha;margin:1px 0 2px 16px;padding:0}}ol.ab li{{margin:0!important}}
</style></head><body>
<div class="page tight">
  <div class="band"><div><div class="k">Junior Cycle English · Free revision sheet</div><h1>Point, quote, explain</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2015 specification): {LO}. Play the game: <b>{GAME}</b></p>
  <p>Almost every question on a text (an unseen extract, a poem, your novel, play or film) wants three things: a <b>point</b> that answers the question, a <b>quote</b> that proves it, and an <b>explanation</b> of how the words prove it. Some schools call it PQE, PEE or PIE.</p>
  <div class="two">
   <div><h2>1. The three parts</h2>
    <div class="wk"><b class="h">Point</b>Answer the question in your own words, in one sentence. Use the question's key word: Cian is lonely at his new school.</div>
    <div class="wk"><b class="h">Quote</b>A few words, copied exactly, in quotation marks, built into your sentence: On his first day he <span class="qt">“ate his lunch alone”</span>.</div>
    <div class="wk"><b class="h">Explain</b>Zoom in on one word and say how it proves the point: The word ‘alone’ suggests nobody wants to know him yet.</div>
    <h2>2. Quoting well</h2>
    <table class="st"><tbody>
     <tr><td><b>Short</b></td><td>2–6 words is usually enough</td></tr>
     <tr><td><b>Exact</b></td><td>“hands were shaking” is not “hands trembled”</td></tr>
     <tr><td><b>Marked</b></td><td>quotation marks round the writer's words</td></tr>
     <tr><td><b>Built in</b></td><td>Saoirse <span class="qt">“clenched”</span> her fists when the ref gave a free.</td></tr></tbody></table></div>
   <div><h2>3. Explaining well</h2>
    <p style="font-size:9.2pt">Starters: <b>The word ‘…’ suggests …</b> · <b>This shows …</b> · <b>The verb ‘…’ makes … sound …</b> · <b>This tells us …</b></p>
    <table class="st"><thead><tr><th>Weak explanation</th><th>What's wrong</th></tr></thead><tbody>
     <tr><td>This means her hands were trembling while she opened the case.</td><td>Retelling: it only says the quote again.</td></tr>
     <tr><td>‘Trembled’ shows she is angry.</td><td>Off the point: it argues a different feeling.</td></tr>
     <tr><td>This is a good quote because it shows what she is like.</td><td>Vague: which word? Like what?</td></tr></tbody></table>
    <h2>4. A full PQE</h2>
    <div class="wk">Aoife is nervous before her audition. As she opens the case, <span class="qt">“her hands trembled”</span>. The word ‘trembled’ shows how anxious she is: her body gives her away.</div>
    <p style="font-size:9pt">Two or three short PQEs beat one long paragraph. Don't retell the story.</p></div>
  </div>
  <div class="tip"><b>Exam tip:</b> “Use evidence from the text” or “Support your answer” means: quote (or refer to) the words, then explain them.</div>
</div>

<div class="page p2">
  <div class="band"><div><div class="k">Practice · {NQ} questions</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Write the short quote (2–6 words) that proves each point.</h2>
  <div class="two"><div>{tcard(TA[0])}</div><div>{tcard(TA[1])}</div></div>
  <ol class="q" style="columns:2">{''.join(li(i, f"{p} {L}") for i, (p, q) in enumerate(A, nA))}</ol>
  <h2>B. Point, quote or explain? Write P, Q or E.</h2>
  <ol class="q" style="columns:2">{''.join(li(i, f"{s} ___") for i, (s, k) in enumerate(B, nB))}</ol>
  <div class="two"><div><h2>C. Which is the best explanation?</h2>
  <ol class="q">{''.join(li(i, f"<b>{p}</b> <span class='qt'>“{q}”</span><ol class='ab'>{''.join(f'<li>{o}</li>' for o in opts)}</ol>") for i, (p, q, opts, a) in enumerate(C_items, nC))}</ol></div>
  <div><h2>D. Quote it short and exact.</h2>
  <ol class="q">{''.join(li(i, f"<b>{p}</b> {line}<br>{L}") for i, (p, line, q, m, pa) in enumerate(Dx, nD))}</ol>
  <h2>E. Which point answers the question?</h2>
  <ol class="q">{''.join(li(i, f"<b>{qn}</b><ol class='ab'>{''.join(f'<li>{o}</li>' for o in opts)}</ol>") for i, (qn, opts, a) in enumerate(E_items, nE))}</ol></div></div>
</div>

<div class="page">
  <div class="band"><div><div class="k">Exam-style · answers</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <h2>F. Exam-style: an original extract</h2>
  <div class="pass"><b>{F_TEXT[0]}</b><span class="sp">{F_TEXT[1]}</span></div>
  <ol class="q">
   <li value="{nF}">How does Ciara feel before anyone buys her cake? Make a point, use a short quote and explain it.<span class="long"></span><span class="long"></span><span class="long"></span><span class="long"></span></li>
   <li value="{nF + 1}">How does Ciara feel at the end? Write a full PQE.<span class="long"></span><span class="long"></span><span class="long"></span></li>
  </ol>
  <h2>Answers</h2>
  <table class="ans"><tbody>
   <tr><td><b>A</b></td><td>{" · ".join(f"{i}. “{q}”" for i, (p, q) in enumerate(A, nA))}</td></tr>
   <tr><td><b>B</b></td><td>{" · ".join(f"{i}. {k.upper()}" for i, (s, k) in enumerate(B, nB))}</td></tr>
   <tr><td><b>C</b></td><td>{" · ".join(f"{i}. {a}" for i, (p, q, o, a) in enumerate(C_items, nC))} (the others retell the quote, argue a different feeling or name no word)</td></tr>
   <tr><td><b>D</b></td><td>{" · ".join(f"{i}. “{q}”" for i, (p, l, q, m, pa) in enumerate(Dx, nD))} (or another 2–6 exact words that prove the point)</td></tr>
   <tr><td><b>E</b></td><td>{" · ".join(f"{i}. {a}" for i, (qn, o, a) in enumerate(E_items, nE))}</td></tr>
   <tr><td><b>F</b></td><td>{nF}. Nervous / anxious: she <span class="qt">“checked the price card for the third time”</span> and <span class="qt">“smoothed her apron”</span>; ‘third time’ suggests she can't stop worrying that something is wrong. · {nF + 1}. Delighted and proud: her <span class="qt">“face lit up”</span>; ‘lit up’ suggests a sudden, bright smile, and counting the coins <span class="qt">“twice”</span> shows how much the sale means to her. Reward a clear point + a short, exact quote + an explanation of one word.</td></tr>
  </tbody></table>
  <div class="note"><b>Got one wrong?</b> Go back to page 1, then play <b>PQE Builder</b> at {GAME}: the “Go back over these” list at the end explains each one.</div>
  <p class="small">All texts are written by Léim. Léim is independent and not connected with the State Examinations Commission or the NCCA.</p>
</div>
</body></html>"""

# ---------- teacher pack ----------
random.seed(2902)
JIG = random.sample(D["answers"], 8)
cards = []
for n, a in enumerate(JIG):
    for s in a:
        cards.append((n, part(s), s))
assert [c[1] for c in cards].count("p") == 8 and [c[1] for c in cards].count("e") == 8
random.shuffle(cards)
cards_html = "".join(f'<div class="c"><span class="tag">Card {i}</span><div class="fc sm">{s}</div></div>' for i, (n, k, s) in enumerate(cards, 1))
groups = {}
for i, (n, k, s) in enumerate(cards, 1): groups.setdefault(n, {})[k] = i
cards_key = " · ".join(f"{g['p']} → {g['q']} → {g['e']}" for n, g in sorted(groups.items(), key=lambda kv: kv[1]["p"]))


SW = random.sample([T for T in D["texts"] if sum(1 for k in T["keys"] if k) >= 3 and T not in TA], 2)
def swap_card(who, mine, theirs):
    pts = [(theirs["pts"][i], theirs["q"][i]) for i, k in enumerate(theirs["keys"]) if k][:3]
    for p, q in pts: assert key_of(p) in shows(q)
    return f"""<div class="idc"><h3>Student {who} · Evidence Swap</h3>
    <p style="font-size:8.8pt;margin:0 0 1mm"><b>1. Read your text aloud to your partner, twice, slowly.</b> They will listen for the evidence.</p>
    {tcard(mine)}
    <p style="font-size:8.8pt;margin:1mm 0"><b>2. Now listen to your partner's text, twice.</b> For each point below, write the short quote (2–6 words) that proves it.</p>
    <table class="st"><tbody>{''.join(f"<tr><td style='width:45%'>{p}</td><td>“</td></tr>" for p, q in pts)}</tbody></table>
    <p style="font-size:8.8pt;margin:1mm 0"><b>3. Check together</b> against the text, then each choose one of your quotes and say the explanation out loud: “The word ‘…’ suggests …”.</p></div>""", pts
CARD_A, PTS_B_FOR_A = swap_card("A", SW[0], SW[1])
CARD_B, PTS_A_FOR_B = swap_card("B", SW[1], SW[0])

FIX = [("Aoife is nervous. She goes into the music room and plays her violin and then she is happy.", "retells the story and has no quote: add “her hands trembled” and explain ‘trembled’"),
       ("Cian is lonely: “On his first day in Athlone, Cian ate his lunch alone on the wall.”", "the quote is the whole sentence: cut it to “ate his lunch alone” and explain ‘alone’"),
       ("Saoirse is angry because she “clenched her hands”.", "misquoted: the text says “clenched my fists”; copy the words exactly"),
       ("Kevin is worried. “his stomach churned”", "a quote dropped in with no explanation: say what ‘churned’ suggests (feeling sick with worry)"),
       ("Hana is kind. She “offered him half her orange”. This shows she is shy.", "the explanation argues a different point: link ‘offered’ back to kindness"),
       ("The poem is good because the poet uses lots of good words.", "vague: no point about the poem, no quote, no word explained")]

WS_TITLE = "The Lifeboat"
WS_TEXT = ("The pager went off at midnight, and Dara was out of bed before it stopped beeping. At the pier the sea heaved and the rain stung his face. "
           "His hands fumbled with the straps of his lifejacket, and he had to try three times. Out past the harbour wall, a small torch flashed and flashed. "
           "When they finally pulled the soaked fisherman on board, Dara gripped his shoulder and grinned until his cheeks hurt.")
for w in ["fumbled", "grinned", "rain"]: assert w in WS_TEXT

pack = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Answering on Texts: Point, Quote, Explain Teacher Pack | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{PACK_STYLE}
{EXTRA}
.fym{{grid-template-columns:repeat(4,1fr)}}.fym .c{{height:33mm}}.fym .fc.sm{{font-size:9pt;font-weight:500;line-height:1.3}}
.idc{{padding:2mm 4mm;margin-bottom:3mm}}.idc h3{{margin:0 0 1mm}}.idc table.st td{{height:7mm}}.p1 .proc td{{font-size:8.6pt;padding:2px 6px}}
.ws .eh td{{font-size:8.6pt;padding:2px 6px}}.ws .eh .gap{{height:11px}}.ws .pass{{font-size:8.8pt;line-height:1.4}}.ws ol.q li{{margin-bottom:1px}}
.prow{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:4mm}}.prow div{{border-radius:14px;padding:5mm 3mm;text-align:center;font-size:12pt;line-height:1.45}}.prow b{{display:block;font-size:20pt}}
.pex{{border:3px solid var(--night);border-radius:14px;padding:5mm 7mm;font-size:13pt;line-height:1.5}}
</style></head><body>

<div class="page p1">
  <div class="band"><div><div class="k">Junior Cycle English · Teacher pack</div><h1>Point, Quote, Explain</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2015 specification): {LO}</p>
  <div class="two">
    <div><h3>Aims</h3><p>By the end of the lesson students can make a point that answers the question, choose a short, exact quote that proves it, explain how one word in the quote proves the point, and spot the three common weak explanations (retelling, off the point, vague).</p></div>
    <div><h3>In this pack</h3><p>p.1 Teacher notes · p.2 PQE Jigsaw (24 cards = 8 answers) · p.3 Evidence Swap A/B (pair listening task) · p.4 Wall poster · p.5 Worksheet: Fix the Answer + exam-style questions · p.6 Answers. Level: 3rd year (works from 2nd year), Higher and Ordinary. Time: about 60 minutes. All texts are original and the skill works with any studied text.</p></div>
  </div>
  <h2 style="margin-top:8px">Procedure</h2>
  <table class="proc"><tbody>
    <tr><td>5 min</td><td><b>Lead-in.</b> Show two answers to “How does Aoife feel?”: one that retells the story, one with a point, “her hands trembled” and an explanation of ‘trembled’. Ask: which gets more marks, and why? Name the parts: point, quote, explain (poster, p.4).</td></tr>
    <tr><td>12 min</td><td><b>PQE Jigsaw</b> (p.2, groups of 3–4). Cut up the 24 cards. Groups sort them into 8 answers, each in the order point → quote → explain, and label each card P, Q or E.</td></tr>
    <tr><td>15 min</td><td><b>Evidence Swap</b> (p.3, pairs). Each reads a short text aloud twice; the partner listens for the evidence and writes the quote that proves each point. Then each says one explanation aloud.</td></tr>
    <tr><td>5 min</td><td><b>Quote surgery.</b> Write a long quote on the board; students cut it to the 2–6 words that matter.</td></tr>
    <tr><td>18 min</td><td><b>Worksheet</b> (p.5). Fix the Answer in pairs, then the exam-style questions on “The Lifeboat” alone.</td></tr>
    <tr><td>5 min</td><td><b>Exit ticket.</b> One PQE on a character from the studied novel or play. Homework: play <b>PQE Builder</b> at {GAME}.</td></tr>
  </tbody></table>
  <div class="note"><b>Errors to look for:</b> retelling the story · a quote with no explanation · whole sentences quoted · misquoting (learn a few words exactly) · explanations that argue a different point · “This shows what she is like” (vague) · a point that doesn't use the question's key word. <b>Support:</b> give the sentence starters on the poster; let students highlight the evidence before writing. <b>Fast finishers:</b> write a second explanation for the same quote, on a different word.</div>
</div>

<div class="page">
  <div class="band"><div><div class="k">Groups · cut up the 24 cards</div><h1>PQE Jigsaw</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.4pt;margin:0 0 2mm">8 answers, cut into point, quote and explain. Rebuild each answer in order: point → quote → explain. Label each card P, Q or E.</p>
  <div class="fym">{cards_html}</div>
</div>

<div class="page">
  <div class="band"><div><div class="k">Pairs · cut along the dashed line</div><h1>Evidence Swap A/B</h1></div><div class="logo">↗ Léim</div></div>
  {CARD_A}
  {CARD_B}
</div>

<div class="page">
  <div class="poster">
    <h1>Point. Quote. Explain.</h1>
    <div class="prow">
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Point</b>Answer the question in one sentence. Use its key word.</div>
      <div style="background:var(--green-soft)"><b>Quote</b>2–6 words. Exact. In quotation marks.</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Explain</b>Zoom in on one word. How does it prove the point?</div>
    </div>
    <div class="pex"><b>Point:</b> Aoife is nervous before her audition.<br><b>Quote:</b> As she opens the case, <span class="qt">“her hands trembled”</span>.<br><b>Explain:</b> The word ‘trembled’ shows how anxious she is: her body gives her away.</div>
    <p style="text-align:center;font-size:14pt!important;margin:0">The word ‘…’ suggests … · This shows … · The verb ‘…’ makes … sound …</p>
    <p style="text-align:center;font-size:18pt!important;font-weight:800;margin:4mm 0">Prove it. Don't retell it.</p>
    <p style="text-align:center;font-size:10pt;color:var(--muted)">Léim · leim.ie · Play PQE Builder: {GAME}</p>
  </div>
</div>

<div class="page ws">
  <div class="band"><div><div class="k">Worksheet · exam-style questions</div><h1>Fix the Answer</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Fix the Answer</h2>
  <p>Each line comes from a weak answer on the texts in this pack. Say what's wrong and write a better version.</p>
  <table class="eh"><thead><tr><th>Weak answer</th><th>What's wrong and a better version</th></tr></thead><tbody>
  {"".join(f"<tr><td style='font-weight:500'>{s}</td><td><span class='gap'></span><span class='gap'></span></td></tr>" for s, r in FIX)}
  </tbody></table>
  <h2>B. Exam-style questions: an original extract</h2>
  <div class="pass"><b>{WS_TITLE}</b><span class="sp">{WS_TEXT}</span></div>
  <ol class="q">
    <li>Find one short quote that shows the weather is wild. Explain one word in it.<span class="long"></span></li>
    <li>How does Dara feel at the pier? Write a full PQE.<span class="long"></span><span class="long"></span></li>
    <li>“a small torch flashed and flashed”: why do you think the writer repeats “flashed”?<span class="long"></span></li>
    <li>How does Dara feel at the end? Use a quote and explain it.<span class="long"></span></li>
    <li>Choose a character from a novel or play you studied. Write two PQEs about them, each on a different quality.<span class="long"></span><span class="long"></span><span class="long"></span></li>
  </ol>
</div>

<div class="page an">
  <div class="band"><div><div class="k">For the teacher</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>PQE Jigsaw (point → quote → explain)</h2>
  <p style="font-size:9pt">{cards_key}</p>
  <h2>Evidence Swap</h2>
  <p style="font-size:9pt"><b>A writes</b> ({SW[1]['title']}): {" · ".join(f"{p} “{q}”" for p, q in PTS_B_FOR_A)}<br><b>B writes</b> ({SW[0]['title']}): {" · ".join(f"{p} “{q}”" for p, q in PTS_A_FOR_B)}<br>Accept any other short, exact words from the same line.</p>
  <h2>A. Fix the Answer</h2>
  <table><tbody>{"".join(f"<tr><td style='width:42%'>{s}</td><td>{r}</td></tr>" for s, r in FIX)}</tbody></table>
  <h2>B. Exam-style questions</h2>
  <ol class="q">
    <li>“the sea heaved” or “the rain stung his face”: ‘heaved’ makes the sea sound alive and powerful; ‘stung’ suggests the rain hurts.</li>
    <li>Nervous / tense: “His hands fumbled” and he “had to try three times”; ‘fumbled’ suggests his fingers won't do what he wants, because of nerves (and the cold).</li>
    <li>Repetition makes the signal feel urgent and desperate: someone out there is calling for help again and again, and the reader feels the tension.</li>
    <li>Relieved and happy: he “grinned until his cheeks hurt”; ‘until his cheeks hurt’ suggests his relief is so strong he can't stop smiling.</li>
    <li>Reward two clear points on different qualities, each with a short, exact quote and an explanation of a word; no retelling.</li>
  </ol>
  <h2>Marking tip</h2>
  <p>Answers on texts are rewarded for a clear response to the question, supported by reference to the text and explained. Our guide, not an official marking scheme.</p>
</div>
</body></html>"""

cover = """<!doctype html><html><head><meta charset="utf-8"><style>
body{margin:0;width:1200px;height:1200px;background:#1B2430;font-family:Inter,sans-serif;color:#fff;display:flex;flex-direction:column;justify-content:space-between;padding:90px;box-sizing:border-box}
.k{display:inline-block;background:#2E7D57;border-radius:99px;padding:12px 26px;font-weight:700;font-size:28px;letter-spacing:.06em;text-transform:uppercase}
h1{font-size:100px;font-weight:800;line-height:1.3;letter-spacing:-.02em;margin:60px 0 20px}
h1 span{background:#F6CF5A;color:#1B2430;padding:0 18px;border-radius:14px}
.sub{font-size:40px;line-height:1.4;color:#DDE3EA}
.em{font-size:46px;margin-top:30px;font-weight:800;letter-spacing:.01em;color:#F6CF5A}
.foot{display:flex;justify-content:space-between;align-items:center;font-size:34px;font-weight:700}
.price{background:#F6CF5A;color:#1B2430;border-radius:16px;padding:14px 28px}
</style></head><body>
<div><span class="k">JC English · Teacher pack</span>
<h1><span>Point, Quote,</span><br><span>Explain</span></h1>
<div class="sub">PQE Jigsaw · Evidence Swap A/B<br>Poster · Worksheet + answers</div>
<div class="em">answering on texts</div></div>
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
    assert pdf("rules-and-practice", os.path.join(ROOT, "printables", f"{SLUG}-rules-and-practice.pdf")) == 3
    assert pdf("teacher-pack", os.path.join(OUT, "Answering-on-Texts-PQE-Teacher-Pack-Leim.pdf")) == 6
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--hide-scrollbars", "--window-size=1200,1200",
                    f"--screenshot={os.path.join(OUT, f'{SLUG}-cover.png')}", f"{SLUG}-cover.html"], cwd=SRC, check=True, capture_output=True)
