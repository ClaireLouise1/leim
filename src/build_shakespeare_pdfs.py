#!/usr/bin/env python3
"""Shakespeare, Higher Level (JC English Order 28): free sheet (-> printables/), 6-page teacher pack + 1200x1200 cover (-> OUTDIR).
Usage: python3 src/build_shakespeare_pdfs.py /tmp/p28
Every quote and extract here is looked up in the text of the play (NLTK Shakespeare corpus, src/shakespeare_corpus.py) and
its speaker asserted; answers come from the checker's own functions (src/test_who_said_it.py: speaker, technique, gloss,
order_key). The checker's data pass runs first. Styles are read from src/build_money1_pdfs.py."""
import os, sys, random, subprocess, re
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC); sys.path.insert(0, SRC)
from test_who_said_it import load, data_pass, speaker, technique, gloss, order_key, PLAYS, TLAB
from shakespeare_corpus import where
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/p28"; os.makedirs(OUT, exist_ok=True)
SLUG = "shakespeare"
LO = "R6, R7, R8, R4, OL8"
GAME = "leim.ie/who-said-it.html"
D = load(os.path.join(ROOT, "who-said-it.html")); data_pass(D)
TL = {k: v.split(" ", 1)[1] for k, v in TLAB.items()}

def extract(play, parts):
    """parts = [(SPEAKER, text)]; each text must be in the play and spoken by that speaker."""
    out = []
    for who, txt in parts:
        for chunk in txt.split(" … "):
            w = where(play, chunk)
            assert w[0] == who.upper(), (who, w, chunk)
        out.append(f"<span class='sp'><b>{who.title()}:</b> {txt}</span>")
    return "".join(out)
def q(s): return "“" + s.replace(" / ", " ") + "”"
def strip(s): return s.replace("{", "<b>").replace("}", "</b>")

# ---------- free sheet ----------
random.seed(2801)
A = random.sample(D["lines"], 8)
A_ans = [speaker(p, s)[0] for p, s, k, a, w in A]
B = random.sample(D["old"], 8)
B_ans = [gloss(s) for p, s, m in B]
C = []
for k in ["ox", "si", "co", "qu", "ox", "qu"]:
    C.append(random.choice([x for x in D["tech"] if x[2] == k and x not in C]))
random.shuffle(C)
C_ans = [technique(s) for p, s, k in C]
EV = [x for x in D["plot"] if x[0] == "jc"]
EV = random.sample(EV, 5); random.shuffle(EV)
D_ans = "".join("ABCDE"[i] for i in sorted(range(5), key=lambda i: order_key("jc", EV[i][2])))
nA = 1; nB = nA + 8; nC = nB + 8; nD = nC + 6; nF = nD + 1
NQ = nF + 2 - 1; assert NQ == 25, NQ
F_EX = extract("jc", [("CAESAR", "Let me have men about me that are fat; Sleek-headed men and such as sleep o' nights: Yond Cassius has a lean and hungry look; He thinks too much: such men are dangerous."),
                      ("ANTONY", "Fear him not, Caesar; he's not dangerous; He is a noble Roman and well given."),
                      ("CAESAR", "Would he were fatter! But I fear him not: … Such men as he be never at heart's ease Whiles they behold a greater than themselves, And therefore are they very dangerous.")])

def style(var):
    return re.search(var + r' = f"""<!doctype.*?<style>(.*?)</style>', open(os.path.join(SRC, "build_money1_pdfs.py"), encoding="utf-8").read(), re.S).group(1).replace("{LO}", LO).replace("{{", "{").replace("}}", "}").replace("JC Maths LOs (2018 spec)", "JC English LOs (2015 spec)")
SHEET_STYLE = style("sheet"); PACK_STYLE = style("pack")
assert "JC English LOs (2015 spec)" in SHEET_STYLE and "Single-teacher licence" in PACK_STYLE and "JC English LOs (2015 spec)" in PACK_STYLE
EXTRA = """.wk{line-height:1.4;border:1.5px solid var(--line);border-radius:8px;padding:2px 7px;margin:3px 0;font-size:9.2pt}.wk b.h{display:block}
table.st{border-collapse:collapse;margin:3px 0;font-size:9pt;width:100%}table.st td,table.st th{border:1px solid #C9D1DA;padding:2px 6px;text-align:left;vertical-align:top}
.pass{border-left:4px solid var(--green);background:var(--mist);padding:5px 10px;margin:4px 0;font-size:9.3pt;line-height:1.5}
.pass .sp{display:block;margin:1px 0}.qt{font-family:Georgia,serif;font-style:italic}"""
L = "<span class='line' style='min-width:30mm'></span>"
def li(i, s): return f"<li value='{i}'>{s}</li>"

sheet = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Shakespeare (Higher Level), rules and practice | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{SHEET_STYLE}
{EXTRA}
.p2 ol.q li{{margin-bottom:3px;font-size:9.2pt}}.p2 h2{{margin:5px 0 2px}}.p2 .two{{gap:6mm}}
</style></head><body>
<div class="page tight">
  <div class="band"><div><div class="k">Junior Cycle English · Higher Level · Free revision sheet</div><h1>Shakespeare</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2015 specification): {LO}. Play the game: <b>{GAME}</b></p>
  <p>At Higher Level you study <b>one full Shakespeare play</b>. For the 2028–2030 exams the list is <i>As You Like It</i>, <i>Julius Caesar</i>, <i>The Merchant of Venice</i> and <i>Romeo and Juliet</i> (check which list your year uses). Know the <b>story</b>, the <b>characters</b>, a few <b>key scenes</b> and some <b>short quotes</b>.</p>
  <div class="two">
   <div><h2>1. Old words</h2>
    <table class="st"><tbody>
     <tr><td><b>thou · thee · thy</b></td><td>you (doing it) · you (on the receiving end) · your</td></tr>
     <tr><td><b>art · hath · doth · dost</b></td><td>are · has · does · do</td></tr>
     <tr><td><b>wherefore</b></td><td>why (not where!)</td></tr>
     <tr><td><b>'tis · ere · oft</b></td><td>it is · before · often</td></tr>
     <tr><td><b>ay · nay</b></td><td>yes · no</td></tr>
     <tr><td><b>anon · tarry</b></td><td>in a moment · wait</td></tr>
     <tr><td><b>hence · yond</b></td><td>go away · that (over there)</td></tr>
     <tr><td><b>prithee · sooth</b></td><td>please · truth</td></tr></tbody></table>
    <h2>2. How Shakespeare writes</h2>
    <div class="wk"><b class="h">Verse and prose</b>Verse has a beat (often 10 syllables): noble characters, big feelings. Prose is ordinary sentences: servants, jokes, characters who lose control.</div>
    <div class="wk"><b class="h">Soliloquy · aside</b>A soliloquy is a character alone on stage speaking their thoughts. An aside is a quick comment the others on stage can't hear.</div>
    <div class="wk"><b class="h">Dramatic irony</b>We know something a character doesn't.</div></div>
   <div><h2>3. Techniques to spot</h2>
    <table class="st"><tbody>
     <tr><td><b>Oxymoron</b></td><td>opposites side by side: <span class="qt">“sweet sorrow”</span></td></tr>
     <tr><td><b>Simile</b></td><td>like / as: <span class="qt">“as boundless as the sea”</span></td></tr>
     <tr><td><b>Rhyming couplet</b></td><td>two rhyming lines that close a scene</td></tr>
     <tr><td><b>Rhetorical question</b></td><td>asked for effect: <span class="qt">“Hath not a Jew eyes?”</span></td></tr>
     <tr><td><b>Repetition</b></td><td><span class="qt">“Brutus is an honourable man”</span>, again and again</td></tr>
     <tr><td><b>Pun</b></td><td>a play on words: the dying Mercutio's <span class="qt">“a grave man”</span></td></tr></tbody></table>
    <h2>4. Answering on Shakespeare</h2>
    <div class="wk"><b class="h">Point · short quote · explain</b>Capulet is cruel to Juliet in Act 3, Scene 5: he calls her a <span class="qt">“disobedient wretch”</span> and threatens to throw her out, so we see how little her feelings matter to him.</div>
    <p style="font-size:9pt">Name the act and scene. Say how the audience feels. Mention staging when it helps: lighting, movement, tone of voice. Learn 3–4 short quotes per main character and theme.</p></div>
  </div>
  <div class="tip"><b>Exam tip:</b> a few words quoted accurately beat a long quote misremembered. Every quote needs an explanation.</div>
</div>

<div class="page p2">
  <div class="band"><div><div class="k">Practice · {NQ} questions</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Who said it? (Romeo and Juliet, The Merchant of Venice, Julius Caesar)</h2>
  <ol class="q">{''.join(li(i, f"<span class='qt'>{q(s)}</span> <i>({PLAYS[p]})</i> {L}") for i, (p, s, k, a, w) in enumerate(A, nA))}</ol>
  <div class="two"><div><h2>B. What does the word in bold mean?</h2>
  <ol class="q">{''.join(li(i, f"<span class='qt'>“{strip(s)}”</span> {L}") for i, (p, s, m) in enumerate(B, nB))}</ol></div>
  <div><h2>C. Name the technique.</h2>
  <ol class="q">{''.join(li(i, f"<span class='qt'>{q(s)}</span> {L}") for i, (p, s, k) in enumerate(C, nC))}</ol>
  <h2>D. <i>Julius Caesar</i>: put these in order.</h2>
  <ol class="q"><li value="{nD}">{"<br>".join(f"<b>{'ABCDE'[i]}</b> {e[1]}" for i, e in enumerate(EV))}<br>Order: {L}</li></ol></div></div>
</div>

<div class="page">
  <div class="band"><div><div class="k">Exam-style · answers</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <h2>E. Exam-style: <i>Julius Caesar</i>, Act 1, Scene 2</h2>
  <div class="pass"><i>Caesar is talking to Antony about Cassius.</i>{F_EX}</div>
  <ol class="q">
   <li value="{nF}">What does Caesar think of Cassius, and why? Use two short quotes.<span class="long"></span><span class="long"></span><span class="long"></span><span class="long"></span></li>
   <li value="{nF + 1}">Caesar says <span class="qt">“I fear him not”</span>. Do you believe him? How would you direct the actor playing Caesar to say these lines?<span class="long"></span><span class="long"></span><span class="long"></span></li>
  </ol>
  <h2>Answers</h2>
  <table class="ans"><tbody>
   <tr><td><b>A</b></td><td>{" · ".join(f"{i}. {x}" for i, x in enumerate(A_ans, nA))}</td></tr>
   <tr><td><b>B</b></td><td>{" · ".join(f"{i}. {x}" for i, x in enumerate(B_ans, nB))}</td></tr>
   <tr><td><b>C</b></td><td>{" · ".join(f"{i}. {TL[k]}" for i, k in enumerate(C_ans, nC))}</td></tr>
   <tr><td><b>D</b></td><td>{nD}. {" → ".join(D_ans)}</td></tr>
   <tr><td><b>E</b></td><td>{nF}. He doesn't trust him: Cassius has <span class="qt">“a lean and hungry look”</span> (hungry for power), <span class="qt">“thinks too much”</span>, and men like him are never happy while someone is <span class="qt">“greater than themselves”</span>, so they are <span class="qt">“very dangerous”</span>. Reward a clear point + two quotes explained. · {nF + 1}. For example: no, he says <span class="qt">“dangerous”</span> three times, so he is uneasy. The actor could say <span class="qt">“I fear him not”</span> loudly, for the crowd, but glance at Cassius and lower his voice on <span class="qt">“very dangerous”</span>. (We know he is right: Cassius leads the plot.) Reward an opinion with evidence + a specific staging idea.</td></tr>
  </tbody></table>
  <div class="note"><b>Got one wrong?</b> Go back to page 1, then play <b>Who Said It?</b> at {GAME}: the “Go back over these” list at the end explains each one.</div>
  <p class="small">The quotes are from Shakespeare's plays (public domain), checked against the text. The questions are written by Léim. Léim is independent and not connected with the State Examinations Commission or the NCCA.</p>
</div>
</body></html>"""

# ---------- teacher pack ----------
random.seed(2802)
MATCH = random.sample([x for x in D["lines"] if x[0] == "rj"], 4) + random.sample([x for x in D["lines"] if x[0] == "mv"], 4) + random.sample([x for x in D["lines"] if x[0] == "jc"], 4)
assert len({x[1] for x in MATCH}) == 12
cards = []
for n, (p, s, k, a, w) in enumerate(MATCH):
    who, act_, sc = speaker(p, s)
    cards.append((n, "q", f"<span class='qt'>{q(s)}</span>"))
    cards.append((n, "w", f"<b>{who}</b> · <i>{PLAYS[p]}</i> · Act {act_}<br>{w}"))
random.shuffle(cards)
cards_html = "".join(f'<div class="c"><span class="tag">Card {i}</span><div class="fc sm">{t}</div></div>' for i, (n, kind, t) in enumerate(cards, 1))
pairs = {}
for i, (n, kind, t) in enumerate(cards, 1): pairs.setdefault(n, {})[kind] = i
cards_key = " · ".join(f"{v['q']} ↔ {v['w']}" for n, v in sorted(pairs.items(), key=lambda kv: kv[1]["q"]))

SWAP_A = ("<i>Romeo and Juliet</i>, Act 3, Scene 5. Juliet has refused to marry Paris.", extract("rj", [
    ("JULIET", "Good father, I beseech you on my knees, Hear me with patience but to speak a word."),
    ("CAPULET", "Hang thee, young baggage! disobedient wretch! I tell thee what: get thee to church o' Thursday, Or never after look me in the face: Speak not, reply not, do not answer me; My fingers itch."),
    ("NURSE", "God in heaven bless her! You are to blame, my lord, to rate her so.")]))
SWAP_B = ("<i>The Merchant of Venice</i>, Act 4, Scene 1. Shylock is about to take his pound of flesh from Antonio.", extract("mv", [
    ("PORTIA", "Tarry a little; there is something else. This bond doth give thee here no jot of blood; The words expressly are 'a pound of flesh:' … But, in the cutting it, if thou dost shed One drop of Christian blood, thy lands and goods Are, by the laws of Venice, confiscate Unto the state of Venice."),
    ("GRATIANO", "O upright judge! Mark, Jew: O learned judge!"),
    ("SHYLOCK", "Is that the law?")]))
def swap_card(who, mine):
    t, ex = mine
    return f"""<div class="idc"><h3>Student {who} · Director's Chair</h3>
    <p style="font-size:8.8pt;margin:0 0 1mm"><b>1. You are the director.</b> Read the extract to yourself, then plan it in the grid.</p>
    <div class="pass" style="font-size:8.8pt">{t}{ex}</div>
    <table class="st"><tbody><tr><td style="width:34%">Where is each actor standing? Who moves?</td><td></td></tr><tr><td>Lighting and sound</td><td></td></tr>
    <tr><td>Tone of voice for the key line (which line?)</td><td></td></tr><tr><td>One prop or costume detail</td><td></td></tr></tbody></table>
    <p style="font-size:8.8pt;margin:1mm 0"><b>2. Read it aloud to your partner</b> the way you planned. Your partner says: who has the power here? How did the reading make them feel? <b>3. Swap.</b> Then together: one short quote from each extract that shows a character's feelings.</p></div>"""

FIX = [("Capulet is angry because he is angry with Juliet.", "says nothing new and has no quote: “Capulet's fury shows in his insults, ‘disobedient wretch’, because…”"),
       ("Romeo says “But, soft! what light through yonder window breaks? It is the east, and Juliet is the sun. Arise, fair sun, and kill the envious moon…” which shows he loves her.", "the quote is far too long and isn't explained: quote a few words (“Juliet is the sun”) and say what the image shows"),
       ("In the play Shylock lends money and then there is a trial and then Portia wins.", "plot retelling, no point: what does the trial show about Shylock or Portia?"),
       ("Antony says Brutus is an honourable man so Antony likes Brutus.", "misses the irony: he repeats it until the crowd hears it as a lie"),
       ("Juliet says “Romeo, Romeo, where are you Romeo?”", "misquoted and misread: “wherefore” means why (why are you a Montague?)"),
       ("Mercutio is a funny character.", "a point with no evidence: add a short quote (“a grave man”) and explain the pun")]

WS_EX = extract("jc", [("ANTONY", "Friends, Romans, countrymen, lend me your ears; I come to bury Caesar, not to praise him. … The noble Brutus Hath told you Caesar was ambitious: If it were so, it was a grievous fault, And grievously hath Caesar answer'd it. … For Brutus is an honourable man; So are they all, all honourable men-- Come I to speak in Caesar's funeral. He was my friend, faithful and just to me: But Brutus says he was ambitious; And Brutus is an honourable man.")])

pack = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Shakespeare (Higher Level) Teacher Pack | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{PACK_STYLE}
{EXTRA}
.fym{{grid-template-columns:repeat(4,1fr)}}.fym .c{{height:34mm}}.fym .fc.sm{{font-size:8.6pt;font-weight:500;line-height:1.3}}.fym .fc .qt{{font-size:9.6pt}}
.idc{{padding:2mm 4mm;margin-bottom:3mm}}.idc h3{{margin:0 0 1mm}}.idc table.st td{{height:7mm}}.p1 .proc td{{font-size:8.6pt;padding:2px 6px}}
.ws .eh td{{font-size:8.6pt;padding:2px 6px}}.ws .eh .gap{{height:11px}}.ws .pass{{font-size:8.8pt;line-height:1.4}}.ws ol.q li{{margin-bottom:1px}}
.prow{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:4mm}}.prow div{{border-radius:14px;padding:5mm 3mm;text-align:center;font-size:12pt;line-height:1.45}}.prow b{{display:block;font-size:17pt}}
.pex{{border:3px solid var(--night);border-radius:14px;padding:5mm 7mm;font-size:13pt;line-height:1.5}}
</style></head><body>

<div class="page p1">
  <div class="band"><div><div class="k">Junior Cycle English · Higher Level · Teacher pack</div><h1>Shakespeare</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2015 specification): {LO}</p>
  <div class="two">
    <div><h3>Aims</h3><p>By the end of the lesson students can match key quotes to characters and moments, read Shakespeare's old words (thou, wherefore, hath…), name common techniques (oxymoron, simile, rhyming couplet, rhetorical question, repetition, pun), plan the staging of an extract, and answer with a point, a short quote and an explanation.</p></div>
    <div><h3>In this pack</h3><p>p.1 Teacher notes · p.2 Quote Match (24 mingle cards) · p.3 Director's Chair A/B (pair staging task) · p.4 Wall poster · p.5 Worksheet: Fix the Answer + exam-style questions · p.6 Answers. Level: 3rd year Higher Level. Time: about 60 minutes. Quotes from <i>Romeo and Juliet</i>, <i>The Merchant of Venice</i> and <i>Julius Caesar</i>, checked against the text; the skills work with any play.</p></div>
  </div>
  <h2 style="margin-top:8px">Procedure</h2>
  <table class="proc"><tbody>
    <tr><td>5 min</td><td><b>Lead-in.</b> Write <i>“O Romeo, Romeo! wherefore art thou Romeo?”</i> on the board. Ask: where is Juliet asking Romeo to be? (Nowhere: wherefore = why.) Introduce thou / thee / thy and the old-words table (poster, p.4).</td></tr>
    <tr><td>12 min</td><td><b>Quote Match</b> (p.2, whole class). Each student gets one card: a quote, or a “who + when” card. Find your partner, then together say what the quote shows about the speaker.</td></tr>
    <tr><td>15 min</td><td><b>Director's Chair</b> (p.3, pairs). Each plans the staging of an extract (positions, lighting, tone of voice, a prop) and reads it aloud; the partner says who has the power and how it made them feel.</td></tr>
    <tr><td>5 min</td><td><b>Techniques.</b> Read out three quotes from the studied play: students name the technique and its effect.</td></tr>
    <tr><td>18 min</td><td><b>Worksheet</b> (p.5). Fix the Answer in pairs, then the exam-style questions on Antony's speech alone.</td></tr>
    <tr><td>5 min</td><td><b>Exit ticket.</b> One character from the studied play + one short quote + what it shows. Homework: play <b>Who Said It?</b> at {GAME}.</td></tr>
  </tbody></table>
  <div class="note"><b>Errors to look for:</b> long quotes with no explanation · misquoting (learn a few words exactly) · “wherefore” read as “where” · retelling the plot · missing irony (Antony's “honourable”) · no act or scene · staging answers with no effect on the audience. <b>Support:</b> give the poster as a word bank and a modern-English version of the extracts. <b>Fast finishers:</b> find one example of each technique in the studied play.</div>
</div>

<div class="page">
  <div class="band"><div><div class="k">Whole class · cut up the 24 cards</div><h1>Quote Match</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.4pt;margin:0 0 2mm">12 quotes and 12 “who + when” cards. Find your partner. Then together: what does the quote show about the character? Which word matters most?</p>
  <div class="fym">{cards_html}</div>
</div>

<div class="page">
  <div class="band"><div><div class="k">Pairs · cut along the dashed line</div><h1>Director's Chair A/B</h1></div><div class="logo">↗ Léim</div></div>
  {swap_card("A", SWAP_A)}
  {swap_card("B", SWAP_B)}
</div>

<div class="page">
  <div class="poster">
    <h1>Point. Short quote. Explain.</h1>
    <div class="pex"><b>Point:</b> Capulet is cruel to Juliet.<br><b>Short quote:</b> he calls her a <span class="qt">“disobedient wretch”</span>.<br><b>Explain:</b> “wretch” makes his own daughter sound worthless, so we see how little her feelings matter to him.</div>
    <div class="prow">
      <div style="background:var(--green-soft)"><b>thou · thee · thy</b>you · you · your</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>wherefore</b>why<br>(not where!)</div>
      <div style="background:var(--green-soft)"><b>art · hath · doth</b>are · has · does</div>
    </div>
    <p style="text-align:center;font-size:15pt!important;margin:0">oxymoron · simile · rhyming couplet · rhetorical question · repetition · pun</p>
    <p style="text-align:center;font-size:18pt!important;font-weight:800;margin:4mm 0">Know who. Know when. Know why it matters.</p>
    <p style="text-align:center;font-size:10pt;color:var(--muted)">Léim · leim.ie · Play Who Said It?: {GAME}</p>
  </div>
</div>

<div class="page ws">
  <div class="band"><div><div class="k">Worksheet · exam-style questions</div><h1>Fix the Answer</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Fix the Answer</h2>
  <p>Each line comes from a weak answer on Shakespeare. Say what's wrong and write a better version.</p>
  <table class="eh"><thead><tr><th>Weak answer</th><th>What's wrong and a better version</th></tr></thead><tbody>
  {"".join(f"<tr><td style='font-weight:500'>{s}</td><td><span class='gap'></span><span class='gap'></span></td></tr>" for s, r in FIX)}
  </tbody></table>
  <h2>B. Exam-style questions: <i>Julius Caesar</i>, Act 3, Scene 2</h2>
  <div class="pass"><i>Brutus has just told the crowd why Caesar had to die. Now Antony speaks at Caesar's funeral.</i>{WS_EX}</div>
  <ol class="q">
    <li>Antony says he has come “to bury Caesar, not to praise him”. Is that true? Explain.<span class="long"></span></li>
    <li>Why does Antony keep repeating that Brutus is “an honourable man”? What effect does it have on the crowd?<span class="long"></span></li>
    <li>Find one word or phrase that shows how Antony felt about Caesar. Explain your choice.<span class="long"></span></li>
    <li>How would you stage this speech? Think about where Antony stands, Caesar's body, the crowd and his tone of voice.<span class="long"></span><span class="long"></span></li>
    <li>Choose a key speech from the Shakespeare play you studied. Explain how the speaker uses language to persuade or move the audience.<span class="long"></span><span class="long"></span><span class="long"></span></li>
  </ol>
</div>

<div class="page an">
  <div class="band"><div><div class="k">For the teacher</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>Quote Match (quote card ↔ who + when card)</h2>
  <p style="font-size:8.8pt">{cards_key}</p>
  <h2>Director's Chair</h2>
  <p style="font-size:9pt"><b>A:</b> Capulet has the power: Juliet kneels (“on my knees”), he stands over her; harsh light, his voice rising on “Hang thee” and “disobedient wretch”; the Nurse steps between them. <b>B:</b> the power swings from Shylock to Portia on “Tarry a little”: Shylock frozen with the knife raised, a pause, the light on Portia; Gratiano mocks (“O learned judge!”); Shylock's short, stunned “Is that the law?”. Accept any staging with a reason and an effect.</p>
  <h2>A. Fix the Answer</h2>
  <table><tbody>{"".join(f"<tr><td style='width:40%'>{s}</td><td>{r}</td></tr>" for s, r in FIX)}</tbody></table>
  <h2>B. Exam-style questions</h2>
  <ol class="q">
    <li>No: he says he won't praise Caesar, then does exactly that (“my friend, faithful and just to me”) while turning the crowd against the killers.</li>
    <li>Repetition: each time he lists something good Caesar did, “honourable” sounds less true, until the crowd hears it as sarcasm (irony). It turns them against Brutus without Antony ever attacking him directly.</li>
    <li>For example: “my friend, faithful and just to me”: three warm words, personal and loyal, in contrast with Brutus's cold “ambitious”.</li>
    <li>Reward a specific idea with its effect: for example, standing over Caesar's body, quiet and grieving at first, then louder; a sarcastic pause before each “honourable”; the crowd slowly turning.</li>
    <li>Reward: a specific speech; two techniques (repetition, rhetorical question, imagery…) named, quoted briefly and explained; the effect on the listeners and the audience.</li>
  </ol>
  <h2>Marking tip</h2>
  <p>Answers on the studied play are rewarded for knowledge of the text, short accurate quotes and a clear, supported response to the question. Our guide, not an official marking scheme.</p>
</div>
</body></html>"""

cover = """<!doctype html><html><head><meta charset="utf-8"><style>
body{margin:0;width:1200px;height:1200px;background:#1B2430;font-family:Inter,sans-serif;color:#fff;display:flex;flex-direction:column;justify-content:space-between;padding:90px;box-sizing:border-box}
.k{display:inline-block;background:#2E7D57;border-radius:99px;padding:12px 26px;font-weight:700;font-size:28px;letter-spacing:.06em;text-transform:uppercase}
h1{font-size:112px;font-weight:800;line-height:1.25;letter-spacing:-.02em;margin:60px 0 20px}
h1 span{background:#F6CF5A;color:#1B2430;padding:0 18px;border-radius:14px}
.sub{font-size:40px;line-height:1.4;color:#DDE3EA}
.em{font-size:46px;margin-top:30px;font-weight:800;letter-spacing:.01em;color:#F6CF5A}
.foot{display:flex;justify-content:space-between;align-items:center;font-size:34px;font-weight:700}
.price{background:#F6CF5A;color:#1B2430;border-radius:16px;padding:14px 28px}
</style></head><body>
<div><span class="k">JC English · Higher Level · Teacher pack</span>
<h1><span>Shakespeare</span></h1>
<div class="sub">Quote Match · Director's Chair A/B<br>Poster · Worksheet + answers</div>
<div class="em">who said it · old words<br>techniques · staging</div></div>
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
    assert pdf("teacher-pack", os.path.join(OUT, "Shakespeare-Higher-Level-Teacher-Pack-Leim.pdf")) == 6
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--hide-scrollbars", "--window-size=1200,1200",
                    f"--screenshot={os.path.join(OUT, f'{SLUG}-cover.png')}", f"{SLUG}-cover.html"], cwd=SRC, check=True, capture_output=True)
