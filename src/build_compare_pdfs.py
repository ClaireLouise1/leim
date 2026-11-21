#!/usr/bin/env python3
"""Comparing texts & characters (JC English Order 30): free sheet (-> printables/), 6-page teacher pack + 1200x1200 cover (-> OUTDIR).
Usage: python3 src/build_compare_pdfs.py /tmp/p30
Reads the game's data block (compare-cards.html) and re-checks every answer with the checker's own functions
(src/test_compare_cards.py: features, sentence_ok, claims, titles_in). The checker's data pass runs first.
Styles are read from src/build_money1_pdfs.py."""
import os, sys, random, subprocess, re
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC); sys.path.insert(0, SRC)
from test_compare_cards import load, data_pass, features, sentence_ok, claims, titles_in, SIM, CON
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/p30"; os.makedirs(OUT, exist_ok=True)
SLUG = "comparing-texts-characters"
LO = "R6, R7, R9, W8"
GAME = "leim.ie/compare-cards.html"
D = load(os.path.join(ROOT, "compare-cards.html")); F = data_pass(D)
TX = {T["title"]: T for T in D["texts"]}
CATS = ["p", "t", "pl", "e", "tr"]
VALS = {"p": ["1", "3"], "t": ["night", "day"], "pl": ["sea", "farm", "town", "school", "mountain", "home"], "e": ["happy", "sad"], "tr": ["kind", "brave", "determined", "honest"]}
STMT = {("p", "1"): "Told in the first person (“I”)", ("p", "3"): "Told in the third person (he / she)",
        ("t", "night"): "Set at night", ("t", "day"): "Set during the day",
        ("pl", "sea"): "Set by the sea", ("pl", "farm"): "Set on a farm", ("pl", "town"): "Set in a town", ("pl", "school"): "Set in a school",
        ("pl", "mountain"): "Set on a mountain", ("pl", "home"): "Set at home",
        ("e", "happy"): "Ends happily", ("e", "sad"): "Ends sadly",
        ("tr", "kind"): "The main character is kind", ("tr", "brave"): "The main character is brave",
        ("tr", "determined"): "The main character is determined", ("tr", "honest"): "The main character is honest"}
PH = {("p", "1"): "is told in the first person", ("p", "3"): "is told in the third person", ("t", "night"): "is set at night", ("t", "day"): "is set during the day",
      ("pl", "sea"): "is set by the sea", ("pl", "farm"): "is set on a farm", ("pl", "town"): "is set in a town", ("pl", "school"): "is set in a school",
      ("pl", "mountain"): "is set on a mountain", ("pl", "home"): "is set at home", ("e", "happy"): "ends happily", ("e", "sad"): "ends sadly",
      ("tr", "kind"): "has a kind main character", ("tr", "brave"): "has a brave main character", ("tr", "determined"): "has a determined main character", ("tr", "honest"): "has an honest main character"}
def both(ph): return re.sub(r"^is ", "are both ", re.sub(r"^ends ", "both end ", re.sub(r"^has ", "both have ", ph)))
def q(t): return f"“{t}”"
def shared(a, b): return [c for c in CATS if F[a][c] == F[b][c]]
def where(a, b, c, v):
    ia, ib = F[a][c] == v, F[b][c] == v
    return "Both" if ia and ib else "A" if ia else "B" if ib else "Neither"

def style(var):
    return re.search(var + r' = f"""<!doctype.*?<style>(.*?)</style>', open(os.path.join(SRC, "build_money1_pdfs.py"), encoding="utf-8").read(), re.S).group(1).replace("{LO}", LO).replace("{{", "{").replace("}}", "}").replace("JC Maths LOs (2018 spec)", "JC English LOs (2015 spec)")
SHEET_STYLE = style("sheet"); PACK_STYLE = style("pack")
assert "JC English LOs (2015 spec)" in SHEET_STYLE and "Single-teacher licence" in PACK_STYLE and "JC English LOs (2015 spec)" in PACK_STYLE
EXTRA = """.wk{line-height:1.4;border:1.5px solid var(--line);border-radius:8px;padding:2px 7px;margin:3px 0;font-size:9.2pt}.wk b.h{display:block}
table.st{border-collapse:collapse;margin:3px 0;font-size:9pt;width:100%}table.st td,table.st th{border:1px solid #C9D1DA;padding:2px 6px;text-align:left;vertical-align:top}
.pass{border-left:4px solid var(--green);background:var(--mist);padding:5px 10px;margin:4px 0;font-size:9.3pt;line-height:1.5}
.pass .sp{display:block;margin:1px 0}.qt{font-family:Georgia,serif;font-style:italic}.tc{border:1.5px solid var(--line);border-radius:8px;padding:3px 8px;margin:3px 0;font-size:9.2pt;line-height:1.45}.tc .k{font-size:8pt;font-weight:700;color:var(--muted)}"""
L = "<span class='line' style='min-width:30mm'></span>"
def li(i, s): return f"<li value='{i}'>{s}</li>"
def tcard(T, ab=""): return f"<div class='tc'><span class='k'>{ab}{q(T['title'])}</span><br>" + "<br>".join(T["lines"]) + "</div>"
TITLES = list(TX)

def pick_pair(rng, used, lo=1, hi=3):
    while True:
        a, b = rng.sample(TITLES, 2)
        if a in used or b in used: continue
        if lo <= len(shared(a, b)) <= hi: used.update([a, b]); return a, b

# ---------- free sheet ----------
rng = random.Random(3001); used = set()
P1, P2 = pick_pair(rng, used), pick_pair(rng, used)
A_items = []
for a, b in (P1, P2):
    st = []
    for c in CATS:
        st.append((c, F[a][c]))
        if F[b][c] != F[a][c]: st.append((c, F[b][c]))
    rng.shuffle(st)
    pick = st[:4]
    nv = [(c, v) for c in ("pl", "tr") for v in VALS[c] if F[a][c] != v and F[b][c] != v]
    pick.append(rng.choice(nv)); rng.shuffle(pick)
    A_items.append([(STMT[cv], where(a, b, *cv)) for cv in pick])
assert all(any(x[1] == "Neither" for x in g) for g in A_items)
B_items = []
pairs_b = [tuple(rng.sample(TITLES, 2)) for _ in range(20)]
for k in range(6):
    same = k % 2 == 0
    for a, b in pairs_b:
        cs = [c for c in CATS if (F[a][c] == F[b][c]) == same]
        if cs and (a, b) not in [x[3] for x in B_items]:
            c = rng.choice(cs); s1 = f"{q(a)} {PH[(c, F[a][c])]}."; s2 = f"{q(b)} {PH[(c, F[b][c])]}."
            assert (claims(s1)[0][1] == claims(s2)[0][1]) == same
            B_items.append((s1, s2, "S" if same else "C", (a, b))); break
rng.shuffle(B_items); assert len(B_items) == 6
C_items = []
FOUR = [P1[0], P1[1], P2[0], P2[1]]
CAND = [(a, b) for i, a in enumerate(FOUR) for b in FOUR[i + 1:] if (a, b) not in (P1, P2) and shared(a, b) and len(shared(a, b)) < 5]
rng.shuffle(CAND); assert len(CAND) >= 4, CAND
for a, b in CAND[:2]:
    c = rng.choice(shared(a, b)); v = F[a][c]; w = rng.choice([x for x in VALS[c] if x != v])
    d = rng.choice([x for x in CATS if F[a][x] != F[b][x]])
    good = f"{q(a)} and {q(b)} {both(PH[(c, v)])}."
    opts = [good, f"{q(a)} and {q(b)} {both(PH[(c, w)])}.", f"{q(a)} {PH[(d, F[a][d])]}.",
            f"{q(a)} {PH[(d, F[b][d])]}, whereas {q(b)} {PH[(d, F[a][d])]}."]
    rng.shuffle(opts); ok = [sentence_ok(o, F) for o in opts]; assert ok.count(True) == 1
    C_items.append((a, b, opts, "abcd"[ok.index(True)]))
D_items = []
for a, b in CAND[2:4]:
    c = rng.choice([x for x in CATS if F[a][x] != F[b][x]])
    model = f"{q(a)} {PH[(c, F[a][c])]}, whereas {q(b)} {PH[(c, F[b][c])]}."
    assert sentence_ok(model, F)
    D_items.append((a, b, {"p": "the narrators", "t": "when they are set", "pl": "where they are set", "e": "the endings", "tr": "the main characters"}[c], model))
nA = 1; nB = nA + 10; nC = nB + 6; nD = nC + 2; nF = nD + 2
NQ = nF + 1; assert NQ == 22, NQ

FA = ("The School Bus", "Every morning I sit at the back of the school bus with my headphones on. Nobody talks to me, and I like it that way. Outside, the wet green fields of Offaly roll past. When the bus finally stops at the gate, I'm the last one off.")
FB = ("The Walk to School", "Every morning Jack walks to school with his twin sisters, one on each hand. They chatter and skip and ask him a hundred questions. He answers every one. At the gate, they hug him goodbye and run off laughing.")

sheet = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Comparing texts and characters, rules and practice | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{SHEET_STYLE}
{EXTRA}
.p2 ol.q li{{margin-bottom:2px;font-size:9pt}}.p2 h2{{margin:4px 0 2px}}.p2 .two{{gap:6mm}}.p2 .tc{{font-size:8.6pt;line-height:1.33;margin:2px 0}}
ol.ab{{list-style:lower-alpha;margin:1px 0 2px 16px;padding:0}}ol.ab li{{margin:0!important}}
</style></head><body>
<div class="page tight">
  <div class="band"><div><div class="k">Junior Cycle English · Free revision sheet</div><h1>Comparing texts</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2015 specification): {LO}. Play the game: <b>{GAME}</b></p>
  <p>A comparing question gives you two texts (two poems, two extracts, or two texts you studied) and asks how they are <b>alike</b> and how they are <b>different</b>. Write about <b>both texts together</b>, point by point, not one essay on each.</p>
  <div class="two">
   <div><h2>1. What to compare</h2>
    <table class="st"><tbody>
     <tr><td><b>Narrator</b></td><td>first person (“I”) or third person (he / she)?</td></tr>
     <tr><td><b>Setting</b></td><td>where and when? by the sea, on a farm, at night …</td></tr>
     <tr><td><b>Main character</b></td><td>kind, brave, determined, honest …? A quote from each text.</td></tr>
     <tr><td><b>Mood and ending</b></td><td>happy or sad? Does the mood change?</td></tr>
     <tr><td><b>Theme</b></td><td>what is each text about underneath? (friendship, loss, courage)</td></tr></tbody></table>
    <h2>2. Linking words</h2>
    <table class="st"><thead><tr><th>Alike</th><th>Different</th></tr></thead><tbody>
     <tr><td>Both … · Similarly, … · Likewise, … · In the same way, … · also · too</td><td>However, … · In contrast, … · On the other hand, … · whereas · while · unlike</td></tr></tbody></table></div>
   <div><h2>3. Compare, don't retell</h2>
    <div class="wk"><b class="h">Weak (two summaries)</b>“The Calf” is about Ruth in a barn at night. She gives her coat to a calf. “Inis Oírr” is about Nuala on a ferry. She gives her seat to an old man.</div>
    <div class="wk"><b class="h">Strong (point by point)</b>Both main characters are kind: Ruth <span class="qt">“shared her coat”</span> and Nuala <span class="qt">“offered her seat”</span>. However, “The Calf” is set on a farm at night, whereas “Inis Oírr” is set by the sea in bright sunshine.</div>
    <h2>4. A frame that works</h2>
    <p style="font-size:9.2pt"><b>Both texts …</b> (similarity + a short quote from each) → <b>However, …</b> or <b>…, whereas …</b> (difference + a quote from each) → <b>Overall, …</b> (your view, if the question asks).</p></div>
  </div>
  <div class="tip"><b>Exam tip:</b> every paragraph should mention <b>both</b> texts. One short quote from each beats three from one.</div>
</div>

<div class="page p2">
  <div class="band"><div><div class="k">Practice · {NQ} questions</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Only A, only B, both or neither? Write A, B, Both or Neither.</h2>
  <div class="two"><div>{tcard(TX[P1[0]], "A · ")}{tcard(TX[P1[1]], "B · ")}<ol class="q">{''.join(li(i, f"{s} ______") for i, (s, w) in enumerate(A_items[0], nA))}</ol></div>
  <div>{tcard(TX[P2[0]], "A · ")}{tcard(TX[P2[1]], "B · ")}<ol class="q">{''.join(li(i, f"{s} ______") for i, (s, w) in enumerate(A_items[1], nA + 5))}</ol></div></div>
  <h2>B. Fill the gap with a linking word: a similarity word or a contrast word.</h2>
  <ol class="q">{''.join(li(i, f"{s1} {L} {s2}") for i, (s1, s2, k, p) in enumerate(B_items, nB))}</ol>
  <div class="two"><div><h2>C. Which is the best comparison?</h2>
  <ol class="q">{''.join(li(i, f"<ol class='ab'>{''.join(f'<li>{o}</li>' for o in opts)}</ol>") for i, (a, b, opts, ans) in enumerate(C_items, nC))}</ol>
  <p style="font-size:8.6pt;color:var(--muted)">(Use the four texts in A.)</p></div>
  <div><h2>D. Write one sentence using “whereas”.</h2>
  <ol class="q">{''.join(li(i, f"Compare {w} in {q(a)} and {q(b)}.<span class='long'></span><span class='long'></span>") for i, (a, b, w, m) in enumerate(D_items, nD))}</ol></div></div>
</div>

<div class="page">
  <div class="band"><div><div class="k">Exam-style · answers</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <h2>F. Exam-style: two original texts</h2>
  <div class="pass"><b>Text A: {FA[0]}</b><span class="sp">{FA[1]}</span></div>
  <div class="pass"><b>Text B: {FB[0]}</b><span class="sp">{FB[1]}</span></div>
  <ol class="q">
   <li value="{nF}">Name one way the texts are similar and one way they are different. Use a short quote from each text.<span class="long"></span><span class="long"></span><span class="long"></span><span class="long"></span></li>
   <li value="{nF + 1}">Which character would you rather share the journey with? Refer to both texts.<span class="long"></span><span class="long"></span><span class="long"></span></li>
  </ol>
  <h2>Answers</h2>
  <table class="ans"><tbody>
   <tr><td><b>A</b></td><td>{" · ".join(f"{i}. {w}" for i, (s, w) in enumerate(A_items[0] + A_items[1], nA))}</td></tr>
   <tr><td><b>B</b></td><td>{" · ".join(f"{i}. {k}" for i, (s1, s2, k, p) in enumerate(B_items, nB))} (S = a similarity word: Similarly, / Likewise, / In the same way, · C = a contrast word: However, / In contrast, / On the other hand,)</td></tr>
   <tr><td><b>C</b></td><td>{" · ".join(f"{i}. {ans}" for i, (a, b, o, ans) in enumerate(C_items, nC))} (the others compare something untrue, mention only one text, or swap the facts)</td></tr>
   <tr><td><b>D</b></td><td>{" · ".join(f"{i}. {m}" for i, (a, b, w, m) in enumerate(D_items, nD))}</td></tr>
   <tr><td><b>F</b></td><td>{nF}. Similar: both are journeys to school <span class="qt">“Every morning”</span>, and both end <span class="qt">“at the gate”</span>. Different: Text A is told in the first person and the narrator is alone by choice (<span class="qt">“Nobody talks to me, and I like it that way”</span>), whereas Text B is told in the third person and Jack is surrounded by his sisters, who <span class="qt">“chatter and skip”</span>. · {nF + 1}. Any choice, with a reason and a quote from each text (e.g. Jack: he is patient, <span class="qt">“He answers every one”</span>; the narrator of A wants quiet).</td></tr>
  </tbody></table>
  <div class="note"><b>Got one wrong?</b> Go back to page 1, then play <b>Compare Cards</b> at {GAME}: the “Go back over these” list at the end explains each one.</div>
  <p class="small">All texts are written by Léim. Léim is independent and not connected with the State Examinations Commission or the NCCA.</p>
</div>
</body></html>"""

# ---------- teacher pack ----------
rng = random.Random(3002); used2 = set()
VP = [pick_pair(rng, used2, 1, 2), pick_pair(rng, used2, 1, 2)]
vcards = []
for n, (a, b) in enumerate(VP):
    st = []
    for c in CATS:
        st.append((c, F[a][c]))
        if F[b][c] != F[a][c]: st.append((c, F[b][c]))
    nv = [(c, v) for c in ("pl", "tr") for v in VALS[c] if F[a][c] != v and F[b][c] != v]
    rng.shuffle(nv)
    st = st + nv[:10 - len(st)]; assert len(st) == 10
    for cv in st: vcards.append((n, STMT[cv], where(a, b, *cv)))
rng.shuffle(vcards)
SET = "XY"
vc_html = "".join(f'<div class="c"><span class="tag">Set {SET[n]} · {i}</span><div class="fc sm">{s}</div></div>' for i, (n, s, w) in enumerate(vcards, 1))
tcards_html = "".join(f'<div class="c big"><span class="tag">Set {SET[n]} · Text {ab}</span><div class="fc tx"><b>{q(t)}</b><br>{"<br>".join(TX[t]["lines"])}</div></div>'
                      for n, (a, b) in enumerate(VP) for ab, t in (("A", a), ("B", b)))
vkey = " · ".join(f"{i} {w}" for i, (n, s, w) in enumerate(vcards, 1))

SP = pick_pair(rng, used2, 1, 2)
GRID = [("Narrator", "p"), ("When is it set?", "t"), ("Where is it set?", "pl"), ("Main character is …", "tr"), ("Ending", "e")]
NICE = {"1": "first person", "3": "third person", "night": "night", "day": "day", "happy": "happy", "sad": "sad"}
def nice(c, v): return NICE.get(v, v)
def swap_card(who, mine, theirs):
    return f"""<div class="idc"><h3>Student {who} · Compare Swap</h3>
    <p style="font-size:8.8pt;margin:0 0 1mm"><b>1. Read your text aloud to your partner, twice, slowly.</b></p>
    {tcard(TX[mine])}
    <p style="font-size:8.8pt;margin:1mm 0"><b>2. Listen to your partner's text, twice.</b> Fill in the grid for BOTH texts (yours from the card).</p>
    <table class="st"><thead><tr><th style="width:30%"></th><th>My text: {q(mine)}</th><th>Partner's text: {q(theirs)}</th></tr></thead>
    <tbody>{''.join(f"<tr><td>{g}</td><td></td><td></td></tr>" for g, c in GRID)}</tbody></table>
    <p style="font-size:8.8pt;margin:1mm 0"><b>3. Together,</b> write one sentence with <b>Both</b> and one with <b>whereas</b>.</p></div>"""
CARD_A = swap_card("A", SP[0], SP[1]); CARD_B = swap_card("B", SP[1], SP[0])
sp_both = [c for c in CATS if F[SP[0]][c] == F[SP[1]][c]]; sp_diff = [c for c in CATS if F[SP[0]][c] != F[SP[1]][c]]
sp_model1 = f"{q(SP[0])} and {q(SP[1])} {both(PH[(sp_both[0], F[SP[0]][sp_both[0]])])}."
sp_model2 = f"{q(SP[0])} {PH[(sp_diff[0], F[SP[0]][sp_diff[0]])]}, whereas {q(SP[1])} {PH[(sp_diff[0], F[SP[1]][sp_diff[0]])]}."
assert sentence_ok(sp_model1, F) and sentence_ok(sp_model2, F)

FIX = [("“The Calf” is about Ruth and a calf in a barn. “Inis Oírr” is about Nuala on a ferry.", "two summaries, no comparison: link them, e.g. “Both main characters are kind …”"),
       ("Both texts are good and I liked them both.", "vague: no point about the texts and no evidence"),
       ("“The Rescue” is told in the first person, whereas “The Summit” is told in the third person.", "wrong fact: both are told in the third person (Orla, Fiachra); check the text"),
       ("“Lahinch” ends sadly. Similarly, “The Concert” ends happily.", "wrong linking word: the endings differ, so use However / In contrast"),
       ("Both main characters are brave: Orla “climbed down the ladder”.", "evidence from one text only: add a quote from the other text"),
       ("“The Window” has an honest main character. “Market Day” is set in a town.", "not like with like: compare the same thing in both (both have honest main characters)")]
assert not sentence_ok(FIX[2][0], F) and F["The Rescue"]["p"] == F["The Summit"]["p"] == "3"
assert F["Lahinch"]["e"] != F["The Concert"]["e"] and F["The Window"]["tr"] == F["Market Day"]["tr"] == "honest"
assert F["The Calf"]["tr"] == F["Inis Oírr"]["tr"] == "kind" and F["The Rescue"]["tr"] == "brave"

WA = ("The Cup", "The final whistle blew at Croke Park and I sank to my knees. Thirty years my town had waited for this cup. Around me, men who had cried at the last final were hugging strangers. I held the cup above my head and laughed until I couldn't breathe.")
WB = ("The Empty Stand", "Long after the match, Tom sat alone in the empty stand. The floodlights clicked off one by one. His team had lost the final by a single point, the same as last year. He folded his flag carefully and walked out into the dark.")

pack = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Comparing Texts and Characters Teacher Pack | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{PACK_STYLE}
{EXTRA}
.fym{{grid-template-columns:repeat(4,1fr)}}.fym .c{{height:17mm}}.fym .fc.sm{{font-size:9.6pt;font-weight:600;line-height:1.25}}
.fym .c.big{{grid-column:span 2;height:30mm}}.fym .fc.tx{{font-size:8.4pt;font-weight:500;line-height:1.3;text-align:left}}
.idc{{padding:2mm 4mm;margin-bottom:3mm}}.idc h3{{margin:0 0 1mm}}.idc table.st td{{height:6mm}}.p1 .proc td{{font-size:8.6pt;padding:2px 6px}}
.ws .eh td{{font-size:8.6pt;padding:2px 6px}}.ws .eh .gap{{height:11px}}.ws .pass{{font-size:8.8pt;line-height:1.4}}.ws ol.q li{{margin-bottom:1px}}
.prow{{display:grid;grid-template-columns:1fr 1fr;gap:4mm}}.prow div{{border-radius:14px;padding:5mm 3mm;text-align:center;font-size:12pt;line-height:1.45}}.prow b{{display:block;font-size:20pt}}
.pex{{border:3px solid var(--night);border-radius:14px;padding:5mm 7mm;font-size:13pt;line-height:1.5}}
</style></head><body>

<div class="page p1">
  <div class="band"><div><div class="k">Junior Cycle English · Teacher pack</div><h1>Comparing Texts</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2015 specification): {LO}</p>
  <div class="two">
    <div><h3>Aims</h3><p>By the end of the lesson students can find similarities and differences between two texts (narrator, setting, main character, ending, theme), use similarity and contrast linking words correctly, and write point-by-point comparison sentences with evidence from both texts.</p></div>
    <div><h3>In this pack</h3><p>p.1 Teacher notes · p.2 Venn Sort (4 text cards + 20 statement cards) · p.3 Compare Swap A/B (pair listening task) · p.4 Wall poster · p.5 Worksheet: Fix the Comparison + exam-style questions · p.6 Answers. Level: 3rd year (works from 2nd year), Higher and Ordinary. Time: about 60 minutes. All texts are original and the skill works with any two texts.</p></div>
  </div>
  <h2 style="margin-top:8px">Procedure</h2>
  <table class="proc"><tbody>
    <tr><td>5 min</td><td><b>Lead-in.</b> Show the weak and strong answers from the poster (p.4): two summaries vs point-by-point. Ask: which one is comparing? Underline the linking words.</td></tr>
    <tr><td>12 min</td><td><b>Venn Sort</b> (p.2, groups of 3–4). Each group gets one set (X or Y): 2 text cards + 10 statement cards. Draw a large Venn diagram (A, Both, B, with “Neither” outside) and place every card. Groups then swap sets.</td></tr>
    <tr><td>15 min</td><td><b>Compare Swap</b> (p.3, pairs). Each reads a short text aloud twice; both fill a grid for the two texts, then write a “Both” sentence and a “whereas” sentence together.</td></tr>
    <tr><td>5 min</td><td><b>Linking-word race.</b> Read out pairs of facts; students hold up S (similarity word) or C (contrast word).</td></tr>
    <tr><td>18 min</td><td><b>Worksheet</b> (p.5). Fix the Comparison in pairs, then the exam-style questions on “The Cup” and “The Empty Stand” alone.</td></tr>
    <tr><td>5 min</td><td><b>Exit ticket.</b> One comparison sentence on two studied texts (e.g. two poems). Homework: play <b>Compare Cards</b> at {GAME}.</td></tr>
  </tbody></table>
  <div class="note"><b>Errors to look for:</b> two separate summaries · evidence from one text only · a contrast word between two matching facts (or a similarity word between two different ones) · comparing different things (setting in one, character in the other) · retelling · facts that aren't true of the text. <b>Support:</b> give students the grid from p.3 for any two texts. <b>Fast finishers:</b> add a theme comparison (friendship, loss, courage) with a quote from each text.</div>
</div>

<div class="page">
  <div class="band"><div><div class="k">Groups · cut up the cards</div><h1>Venn Sort</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.4pt;margin:0 0 2mm">Two sets (X and Y). Each set: 2 text cards + 10 statement cards. Place each statement in a Venn diagram: <b>A only</b>, <b>Both</b>, <b>B only</b>, or <b>Neither</b> (outside the circles).</p>
  <div class="fym">{tcards_html}{vc_html}</div>
</div>

<div class="page">
  <div class="band"><div><div class="k">Pairs · cut along the dashed line</div><h1>Compare Swap A/B</h1></div><div class="logo">↗ Léim</div></div>
  {CARD_A}
  {CARD_B}
</div>

<div class="page">
  <div class="poster">
    <h1>Compare, don't retell.</h1>
    <div class="prow">
      <div style="background:var(--green-soft)"><b>Alike</b>Both … · Similarly, … · Likewise, … · In the same way, …</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Different</b>However, … · In contrast, … · On the other hand, … · whereas · while</div>
    </div>
    <div class="pex"><b>Both</b> main characters are kind: Ruth <span class="qt">“shared her coat”</span> and Nuala <span class="qt">“offered her seat”</span>.<br><b>However,</b> “The Calf” is set on a farm at night, <b>whereas</b> “Inis Oírr” is set by the sea in bright sunshine.</div>
    <p style="text-align:center;font-size:14pt!important;margin:0">Narrator · Setting · Main character · Mood and ending · Theme</p>
    <p style="text-align:center;font-size:18pt!important;font-weight:800;margin:4mm 0">Both texts in every paragraph.</p>
    <p style="text-align:center;font-size:10pt;color:var(--muted)">Léim · leim.ie · Play Compare Cards: {GAME}</p>
  </div>
</div>

<div class="page ws">
  <div class="band"><div><div class="k">Worksheet · exam-style questions</div><h1>Fix the Comparison</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Fix the Comparison</h2>
  <p>Each line comes from a weak answer on the texts in the game. Say what's wrong and write a better version.</p>
  <table class="eh"><thead><tr><th>Weak answer</th><th>What's wrong and a better version</th></tr></thead><tbody>
  {"".join(f"<tr><td style='font-weight:500'>{s}</td><td><span class='gap'></span><span class='gap'></span></td></tr>" for s, r in FIX)}
  </tbody></table>
  <h2>B. Exam-style questions: two original texts</h2>
  <div class="pass"><b>Text A: {WA[0]}</b><span class="sp">{WA[1]}</span></div>
  <div class="pass"><b>Text B: {WB[0]}</b><span class="sp">{WB[1]}</span></div>
  <ol class="q">
    <li>Name one way the two texts are similar. Use a short quote from each.<span class="long"></span></li>
    <li>Name two ways the texts are different.<span class="long"></span><span class="long"></span></li>
    <li>Join these into one sentence with a contrast word: Text A ends with laughter. Text B ends in the dark.<span class="long"></span></li>
    <li>Which text made you feel more? Refer to both texts.<span class="long"></span><span class="long"></span></li>
    <li>Plan a comparison of two texts you studied on one theme: a similarity, two differences, evidence from each.<span class="long"></span><span class="long"></span></li>
  </ol>
</div>

<div class="page an">
  <div class="band"><div><div class="k">For the teacher</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>Venn Sort</h2>
  <p style="font-size:9pt">Set X: A = {q(VP[0][0])}, B = {q(VP[0][1])} · Set Y: A = {q(VP[1][0])}, B = {q(VP[1][1])}<br>{vkey}</p>
  <h2>Compare Swap</h2>
  <table class="st"><thead><tr><th></th><th>{q(SP[0])} (A's text)</th><th>{q(SP[1])} (B's text)</th></tr></thead><tbody>
  {"".join(f"<tr><td>{g}</td><td>{nice(c, F[SP[0]][c])}</td><td>{nice(c, F[SP[1]][c])}</td></tr>" for g, c in GRID)}</tbody></table>
  <p style="font-size:9pt">Sample sentences: {sp_model1} · {sp_model2}</p>
  <h2>A. Fix the Comparison</h2>
  <table><tbody>{"".join(f"<tr><td style='width:42%'>{s}</td><td>{r}</td></tr>" for s, r in FIX)}</tbody></table>
  <h2>B. Exam-style questions</h2>
  <ol class="q">
    <li>Both are about the end of a final: A <span class="qt">“The final whistle blew”</span>, B <span class="qt">“Long after the match”</span>.</li>
    <li>Any two: first person (“I sank to my knees”) vs third person (Tom); a win vs a loss (“lost the final by a single point”); crowded and joyful (“hugging strangers”) vs alone (“sat alone”); daylight vs the dark.</li>
    <li>Text A ends with laughter, whereas Text B ends in the dark. (Or: …laughter. However, Text B …)</li>
    <li>Any view with a quote from each text and a reason that compares them.</li>
    <li>Reward a similarity and two differences, evidence from both texts, and clear linking words.</li>
  </ol>
  <h2>Marking tip</h2>
  <p>Comparing answers are rewarded for points that link both texts, supported by reference to each. Our guide, not an official marking scheme.</p>
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
<h1><span>Comparing</span><br><span>Texts</span></h1>
<div class="sub">Venn Sort · Compare Swap A/B<br>Poster · Worksheet + answers</div>
<div class="em">texts &amp; characters</div></div>
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
    assert pdf("teacher-pack", os.path.join(OUT, "Comparing-Texts-Characters-Teacher-Pack-Leim.pdf")) == 6
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--hide-scrollbars", "--window-size=1200,1200",
                    f"--screenshot={os.path.join(OUT, f'{SLUG}-cover.png')}", f"{SLUG}-cover.html"], cwd=SRC, check=True, capture_output=True)
