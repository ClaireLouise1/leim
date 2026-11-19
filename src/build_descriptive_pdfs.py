#!/usr/bin/env python3
"""Personal & descriptive writing (JC English Order 9): free sheet (-> printables/), 6-page teacher pack + 1200x1200 cover (-> OUTDIR).
Usage: python3 src/build_descriptive_pdfs.py /tmp/descriptive
Items come from the game's data block (show-dont-tell.html). Every answer is re-derived with the checker's own rules
(src/test_show_dont_tell.py: feelings, names_feeling, cue + VERB, detail; senses from src/test_technique_spotter.py) and asserted.
Styles are read from src/build_money1_pdfs.py."""
import os, sys, random, subprocess, re
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC); sys.path.insert(0, SRC)
from test_show_dont_tell import feelings, names_feeling, cue, VERB, detail, senses, load, FL
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/descriptive"; os.makedirs(OUT, exist_ok=True)
SLUG = "personal-descriptive-writing"
LO = "W3, W4, W9, W7"
GAME = "leim.ie/show-dont-tell.html"
D = load(os.path.join(ROOT, "show-dont-tell.html"))
FN = {k: v.split(" ", 1)[1] for k, v in FL.items()}
SN = {"see": "Sight", "hear": "Sound", "smell": "Smell", "taste": "Taste", "touch": "Touch"}
def feel1(s):
    f = feelings(s); assert len(f) == 1 and not names_feeling(s), (s, f); return list(f)[0]
def sense1(s):
    f = senses(s); assert len(f) == 1, (s, f); return list(f)[0]

# ---------- free sheet ----------
random.seed(99)
A_items = []
for k in random.sample(list(FL), 6):
    A_items.append(random.choice([x for x in D["show"] if x[0] == k]))
for k, s in A_items: assert feel1(s) == k
used = {s for k, s in A_items}
B_items = [("I was very nervous before the test.", "T"), (next(s for k, s in D["show"] if k == "sad" and s not in used), "S"),
           ("My brother was furious with me.", "T"), (next(s for k, s in D["show"] if k == "exc" and s not in used), "S")]
for s, a in B_items: assert bool(names_feeling(s)) == (a == "T") and (a == "T" or len(feelings(s)) == 1), s
C_items = []
for k in ("touch", "hear", "taste", "see", "smell"):
    x = random.choice([y for y in D["senses"] if y[1] == k]); C_items.append(x); assert sense1(x[0]) == k
random.shuffle(C_items)
G = {"walked": [["trudged", "plodded"], ["crept", "tiptoed"], ["raced", "dashed"], ["strolled", "wandered"], ["stormed", "stomped"]],
     "said": [["whispered"], ["shouted", "yelled"], ["muttered", "grumbled"], ["sobbed"], ["giggled"], ["stammered"]],
     "looked": [["glanced"], ["stared", "gazed"], ["peered"], ["glared"]], "ate": [["gobbled", "wolfed"], ["nibbled"], ["slurped"]]}
D_items = []
for w in ("walked", "said", "looked", "ate", "walked"):
    it = random.choice([x for x in D["verb"] if x[1] == w and x not in D_items]); D_items.append(it)
D_opts = []
for s, w, a in D_items:
    c = cue(s); assert len(c) == 1 and VERB[a][1] in c, (s, c)
    o = [a] + [random.choice(S) for S in random.sample([S for S in G[w] if a not in S], 2)]
    for x in o[1:]: assert VERB[x][0] == w and VERB[x][1] not in c
    random.shuffle(o); D_opts.append(o)
E_items = random.sample(D["zoom"], 3); E_opts = []
for fr, a, wrong in E_items:
    assert all(detail(x) <= detail(a) - 2 for x in wrong)
    o = [a] + wrong; random.shuffle(o); E_opts.append(o)
FAIR = "The fair was nice. There were lots of things to do. I was excited. We went on a ride and it was good. Then I went on the big wheel and I was scared."
FAIR_TELL = ["nice", "things", "excited", "good", "scared"]
for w in FAIR_TELL: assert re.search(r"\b" + w + r"\b", FAIR)
NQ = len(A_items) + len(B_items) + len(C_items) + len(D_items) + len(E_items) + 2; assert NQ == 25, NQ
nA = 1; nB = nA + len(A_items); nC = nB + len(B_items); nD = nC + len(C_items); nE = nD + len(D_items); nF = nE + len(E_items)

def style(var):
    return re.search(var + r' = f"""<!doctype.*?<style>(.*?)</style>', open(os.path.join(SRC, "build_money1_pdfs.py"), encoding="utf-8").read(), re.S).group(1).replace("{LO}", LO).replace("{{", "{").replace("}}", "}").replace("JC Maths LOs (2018 spec)", "JC English LOs (2015 spec)")
SHEET_STYLE = style("sheet"); PACK_STYLE = style("pack")
assert "JC English LOs (2015 spec)" in SHEET_STYLE and "Single-teacher licence" in PACK_STYLE and "JC English LOs (2015 spec)" in PACK_STYLE
EXTRA = """.wk{line-height:1.45;border:1.5px solid var(--line);border-radius:8px;padding:2px 7px;margin:3px 0;font-size:9.4pt}.wk b.h{display:block}
table.st{border-collapse:collapse;margin:3px 0;font-size:9.2pt;width:100%}table.st td,table.st th{border:1px solid #C9D1DA;padding:2px 6px;text-align:left}
.bank{border:1.5px solid var(--line);border-radius:8px;padding:4px 10px;margin:4px 0;text-align:center;font-weight:700;word-spacing:4px}
.pass{border-left:4px solid var(--green);background:var(--mist);padding:5px 10px;margin:4px 0;font-style:italic}"""
def gap(s): return s.replace("___", "<b>________</b>")
A_html = "".join(f"<li value='{i}'><i>{s}</i> <span class='line' style='min-width:22mm'></span></li>" for i, (k, s) in enumerate(A_items, nA))
B_html = "".join(f"<li value='{i}'><i>{s}</i> &nbsp; <b>S / T</b></li>" for i, (s, a) in enumerate(B_items, nB))
C_html = "".join(f"<li value='{i}'><i>{s}</i> <span class='line' style='min-width:16mm'></span></li>" for i, (s, k) in enumerate(C_items, nC))
D_html = "".join(f"<li value='{i}'>{gap(s)} <span style='color:#5B6573'>({w})</span><br>{' &nbsp;/&nbsp; '.join(o)}</li>" for i, ((s, w, a), o) in enumerate(zip(D_items, D_opts), nD))
E_html = "".join(f"<li value='{i}'>{gap(fr)}<br>{' &nbsp;/&nbsp; '.join(o)}</li>" for i, ((fr, a, w), o) in enumerate(zip(E_items, E_opts), nE))

sheet = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Personal and descriptive writing, rules and practice | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{SHEET_STYLE}
{EXTRA}
.p2 ol.q li{{margin-bottom:1px;font-size:9pt}}.p2 h2{{margin:4px 0 2px}}.p2 .two{{gap:5mm}}
</style></head><body>
<div class="page tight">
  <div class="band"><div><div class="k">Junior Cycle English · Free revision sheet</div><h1>Personal and descriptive writing</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2015 specification): {LO}. Play the game: <b>{GAME}</b></p>
  <div class="two">
   <div><h2>1. Show, don't tell</h2>
    <div class="wk"><b>Tell:</b> <i>I was scared.</i><br><b>Show:</b> <i>My heart pounded. I froze at the bottom of the stairs.</i><br>Don't name the feeling. Give the body clues and let the reader work it out.</div>
    <table class="st"><thead><tr><th>Feeling</th><th>Body clues</th></tr></thead><tbody>
     <tr><td><b>Happy</b></td><td><i>grinned, beamed, laughed</i></td></tr>
     <tr><td><b>Excited</b></td><td><i>bounced, squealed, couldn't sit still</i></td></tr>
     <tr><td><b>Scared</b></td><td><i>froze, gasped, heart pounded</i></td></tr>
     <tr><td><b>Nervous</b></td><td><i>bit my nails, fidgeted, butterflies</i></td></tr>
     <tr><td><b>Angry</b></td><td><i>clenched my fists, slammed, glared</i></td></tr>
     <tr><td><b>Sad</b></td><td><i>tears, a lump in my throat, slumped</i></td></tr>
     <tr><td><b>Bored</b></td><td><i>yawned, doodled, watched the clock</i></td></tr>
     <tr><td><b>Embarrassed</b></td><td><i>cheeks burned, blushed, stared at my shoes</i></td></tr></tbody></table>
    <h2>2. Use all five senses</h2>
    <div class="wk"><b>Sight</b> colours, light · <b>Sound</b> roared, hummed · <b>Smell</b> scent, reeked · <b>Taste</b> salty, sour · <b>Touch</b> icy, rough, damp. Most students only write what they see: one sound or smell makes the scene real.</div></div>
   <div><h2>3. Strong verbs</h2>
    <table class="st"><tbody>
     <tr><td><b>walked</b></td><td>trudged (tired) · crept (quietly) · raced (fast) · strolled (relaxed) · stormed (angry)</td></tr>
     <tr><td><b>said</b></td><td>whispered · shouted · muttered · sobbed · giggled · stammered</td></tr>
     <tr><td><b>looked</b></td><td>glanced (quick) · stared (long) · peered (hard to see) · glared (angry)</td></tr>
     <tr><td><b>ate</b></td><td>gobbled (hungry) · nibbled (not hungry) · slurped (soup)</td></tr></tbody></table>
    <div class="wk">One strong verb beats a weak verb + adverb: <i>walked slowly</i> → <i>trudged</i>.</div>
    <h2>4. Zoom in</h2>
    <div class="wk"><i>a dog</i> → <i>a scruffy brown terrier</i> · <i>food</i> → <i>a warm cheese and ham toastie</i>. Cut <b>nice, good, thing, stuff, lots</b>.</div>
    <h2>5. Personal or descriptive?</h2>
    <p><b>Personal writing:</b> a real moment from your life, told with "I", with how you felt and what you learned. <b>Descriptive writing:</b> paints a place or a moment so the reader feels they are there. Less story, more detail.</p>
    <div class="note"><b>Classic mistakes:</b> naming feelings (I was so happy) · only sight · nice / good / things · five adjectives in a row · "and then… and then…" · ending with "it was all a dream".</div></div>
  </div>
  <div class="tip"><b>Exam tip:</b> quality beats length. One vivid paragraph that shows a feeling, uses two senses and has sharp verbs earns more than a page of "it was nice".</div>
</div>

<div class="page p2">
  <div class="band"><div><div class="k">Practice · {NQ} questions</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <div class="two"><div><h2>A. Which feeling is shown?</h2><div class="bank" style="font-size:8.4pt">{" · ".join(FN.values())}</div><ol class="q">{A_html}</ol>
  <h2>B. Show (S) or tell (T)?</h2><ol class="q">{B_html}</ol></div>
  <div><h2>C. Which sense? (sight, sound, smell, taste, touch)</h2><ol class="q">{C_html}</ol>
  <h2>D. Circle the strongest verb for the gap</h2><ol class="q">{D_html}</ol></div></div>
  <h2>E. Zoom in: circle the most specific detail</h2><ol class="q">{E_html}</ol>
  <h2>F. Exam-style: "The Fair"</h2>
  <div class="pass">{FAIR}</div>
  <ol class="q">
   <li value="{nF}">Underline five words that tell or are vague.<span class="long"></span></li>
   <li value="{nF + 1}">Rewrite the paragraph so it <b>shows</b>: use two senses, one strong verb and one feeling shown, not named.<span class="long"></span><span class="long"></span><span class="long"></span><span class="long"></span></li>
  </ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">Check your work</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <table class="ans"><tbody>
   <tr><td><b>A</b></td><td>{" · ".join(f"{i}. {FN[k]}" for i, (k, s) in enumerate(A_items, nA))}</td></tr>
   <tr><td><b>B</b></td><td>{" · ".join(f"{i}. {'Tell (it names the feeling)' if a == 'T' else 'Show'}" for i, (s, a) in enumerate(B_items, nB))}</td></tr>
   <tr><td><b>C</b></td><td>{" · ".join(f"{i}. {SN[k]}" for i, (s, k) in enumerate(C_items, nC))}</td></tr>
   <tr><td><b>D</b></td><td>{" · ".join(f"{i}. {a}" for i, (s, w, a) in enumerate(D_items, nD))}<br>(The clue in the sentence tells you how: tired → trudged, starving → gobbled, under his breath → muttered.)</td></tr>
   <tr><td><b>E</b></td><td>{" · ".join(f"{i}. {a}" for i, (fr, a, w) in enumerate(E_items, nE))}</td></tr>
   <tr><td><b>F</b></td><td>{nF}. nice · things · excited · good · scared.<br>
     {nF + 1}. Sample: <i>The fairground hummed with music and screams. The air smelled of candyfloss and hot chips. I bounced on my toes in the queue for the Waltzer, then we spun so fast that my hair whipped my face. When the big wheel stopped at the very top, I froze and gripped the bar until my knuckles went white.</i> (Sound, smell, touch; strong verbs bounced, spun, whipped, gripped; excited and scared shown, never named.)</td></tr>
  </tbody></table>
  <h2>Worked examples</h2>
  <div class="two">
   <div class="wk"><b class="h">Turning tell into show</b>"I was nervous." Ask: what would my body do? → <i>I bit my nails and checked the clock again.</i> Then add where you are: <i>outside the principal's office.</i></div>
   <div class="wk"><b class="h">Choosing a strong verb</b>Find the clue in the sentence. <i>"Exhausted after training, I ___ up the hill"</i>: exhausted → slow and heavy → <b>trudged</b>, not raced or tiptoed.</div>
   <div class="wk"><b class="h">Zooming in</b>Ask: which one could I draw? "a nice car" (no) → "Dad's rusty red Fiesta" (yes). Colour, size, age, a name or a place make it specific.</div>
   <div class="wk"><b class="h">Using the senses</b>Write one sentence per sense, then keep the best two or three. Don't list all five in one sentence: spread them out.</div>
  </div>
  <div class="note"><b>Got one wrong?</b> Go back to page 1, then play <b>Show, Don't Tell</b> at {GAME}: the "Go back over these" list at the end explains each mistake.</div>
  <p class="small">All sentences and passages written by Léim. Léim is independent and not connected with the State Examinations Commission or the NCCA.</p>
</div>
</body></html>"""

# ---------- teacher pack ----------
SORT = []
for k in FL:
    L = [x for x in D["show"] if x[0] == k]; random.seed(900 + len(SORT)); SORT += random.sample(L, 3)
for k, s in SORT: assert feel1(s) == k
random.seed(909); random.shuffle(SORT)
sort_html = "".join(f'<div class="c"><span class="tag">Card {i}</span><div class="fc sm">{s}</div></div>' for i, (k, s) in enumerate(SORT, 1))
sort_key = " · ".join(f"<b>{FN[k]}</b>: " + ", ".join(str(i) for i, x in enumerate(SORT, 1) if x[0] == k) for k in FL)

SWAP_A = ("The Beach at Dawn", ["Pale pink light spread across the sky.", "Waves rumbled against the rocks.", "The air smelled of seaweed.",
          "I could taste salt on my lips.", "The sand was cold and damp under my feet.", "I grinned and raced towards the water."])
SWAP_B = ("The School Canteen", ["Bright orange trays slid along the counter.", "Chairs scraped and the whole room roared.", "The canteen smelled of chips and gravy.",
          "My chicken curry was spicy and delicious.", "The sticky table clung to my elbows.", "I yawned and watched the clock until the bell."])
SWAP_KEY = {}
for name, L in (SWAP_A, SWAP_B):
    sk = {}
    for i, l in enumerate(L[:5], 1): sk[sense1(l)] = i
    assert set(sk) == set(SN), (name, sk)
    assert not senses(L[5]) and len(feelings(L[5])) == 1 and not names_feeling(L[5]), (name, L[5])
    SWAP_KEY[name] = (sk, list(feelings(L[5]))[0])
assert SWAP_KEY["The Beach at Dawn"][1] == "hap" and SWAP_KEY["The School Canteen"][1] == "bor"
def swap_card(who, mine, theirs):
    name, L = mine
    return f"""<div class="idc"><h3>Student {who} · Picture This</h3>
    <p style="font-size:8.6pt;margin:0 0 1mm"><b>1. Read your description aloud twice</b>, slowly. Your partner listens with their eyes closed, then fills in the grid.</p>
    <div class="pass" style="font-size:10.4pt"><b style="font-style:normal">"{name}"</b><br>{" ".join(L)}</div>
    <p style="font-size:8.6pt;margin:1mm 0"><b>2. Then listen</b> to "{theirs[0]}". Write the words you hear for each sense, and the feeling:</p>
    <table class="st" style="font-size:8.6pt"><tbody>{"".join(f"<tr><td style='width:28%'><b>{n}</b></td><td></td></tr>" for n in list(SN.values()) + ["Feeling shown (not named)", "Best strong verb"])}</tbody></table>
    <p style="font-size:8.6pt;margin:1mm 0 0"><b>3. Talk:</b> which detail helped you picture the place best? Why?</p></div>"""

FIX = [("I was really scared.", "Tells the feeling. Show it: <b>I froze. My heart pounded so hard I could hear it.</b>"),
       ("The food was nice.", "Vague. Zoom in: <b>The lasagne was hot and cheesy, with crispy edges.</b>"),
       ("I walked slowly up the hill.", "Weak verb + adverb. One strong verb: <b>I trudged up the hill.</b>"),
       ("It was a big, dark, old, scary, creepy house.", "Too many adjectives. Pick two and add a sense: <b>The old house was dark, and the gate creaked in the wind.</b>"),
       ("“Hi,” I said. “Hello,” he said. “Where's Mam?” I said.", "“Said” three times. Vary it or cut it: <b>“Hi,” I whispered. “Where's Mam?”</b>"),
       ("Then I woke up and it was all a dream.", "A let-down ending. End on a feeling or a final image: <b>I still keep that shell on my windowsill.</b>")]
assert names_feeling(FIX[0][0]) and feelings("I froze. My heart pounded so hard I could hear it.") == {"sca"}
assert cue("Exhausted after training, I ___ up the hill.") == {"tired"} and VERB["trudged"][1] == "tired"

MARKET = ["The English Market was already busy when we squeezed through the gates.",
          "Bright red apples were piled high beside the fish stall, where silver mackerel glittered on the ice.",
          "Traders shouted prices over the noise.", "The air smelled of fresh bread and coffee.",
          "Mam handed me a warm doughnut and I bit into it: the sugar was sweet on my tongue.", "I grinned. This was the best part of Saturday."]
assert senses(MARKET[1]) == {"see"} and senses(MARKET[2]) == {"hear"} and senses(MARKET[3]) == {"smell"}
assert {"taste", "touch"} <= senses(MARKET[4]) and feelings(MARKET[5]) == {"hap"} and not names_feeling(" ".join(MARKET))

pack = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Personal and Descriptive Writing Teacher Pack | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{PACK_STYLE}
{EXTRA}
.fym .c{{height:28mm}}.fym .fc.sm{{font-size:9.8pt;line-height:1.28;margin-top:2mm;font-weight:600}}.idc{{padding:2mm 4mm;margin-bottom:3mm}}.idc h3{{margin:0 0 1mm}}
.idc .st td{{height:5mm;padding:1px 6px}}.p1 .proc td{{font-size:8.6pt;padding:2px 6px}}.ops div{{font-size:12pt;padding:5mm 3mm}}.ops b{{font-size:19pt}}
.ws .eh td{{font-size:8.6pt;padding:2px 6px}}.ws .eh .gap{{height:13px}}.ws ol.q li{{margin-bottom:1px}}
</style></head><body>

<div class="page p1">
  <div class="band"><div><div class="k">Junior Cycle English · Teacher pack</div><h1>Personal and descriptive writing</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2015 specification): {LO}</p>
  <div class="two">
    <div><h3>Aims</h3><p>By the end of the lesson students can show a feeling through actions and body language instead of naming it, use more than one sense in a description, choose strong verbs and specific details, and spot vague writing in their own drafts.</p></div>
    <div><h3>In this pack</h3><p>p.1 Teacher notes · p.2 Show It Sort cards (cut-up) · p.3 Picture This A/B (speaking + listening) · p.4 Wall poster · p.5 Worksheet: Fix the Writing + exam-style questions · p.6 Answers. Level: 1st year (useful revision in 2nd and 3rd). Time: about 60 minutes. All texts are original.</p></div>
  </div>
  <h2 style="margin-top:8px">Procedure</h2>
  <table class="proc"><tbody>
    <tr><td>5 min</td><td><b>Lead-in.</b> Board two versions: <i>I was scared. The house was dark.</i> / <i>My heart pounded. I froze at the bottom of the stairs as the floorboards creaked above me.</i> Which one lets you picture it? What does the second never say, but you still know?</td></tr>
    <tr><td>8 min</td><td><b>Guided discovery.</b> Students find the words that show fear (pounded, froze, creaked). Elicit the toolkit: body clues, the five senses, strong verbs, zooming in. Model turning "I was bored" into a showing sentence together.</td></tr>
    <tr><td>12 min</td><td><b>Show It Sort</b> (p.2, groups of 3–4, one set of 24 cards). Sort the cards into eight feelings (3 each). Then each student mimes one card for the group to guess.</td></tr>
    <tr><td>12 min</td><td><b>Picture This</b> (p.3, pairs). A reads "The Beach at Dawn" aloud twice; B listens with eyes closed, then writes the words for each sense, the feeling and the best verb. Swap for "The School Canteen".</td></tr>
    <tr><td>18 min</td><td><b>Worksheet</b> (p.5). Fix the Writing in pairs, then the exam-style questions on "Market Morning" alone.</td></tr>
    <tr><td>5 min</td><td><b>Exit ticket.</b> Describe the classroom right now in three sentences: no "nice", one sound, one feeling shown. Homework: play <b>Show, Don't Tell</b> at {GAME}.</td></tr>
  </tbody></table>
  <div class="note"><b>Errors to look for:</b> naming the feeling and adding a body clue ("I was scared and I froze") · sight only · nice / good / things · adverbs propping up weak verbs · piles of adjectives. <b>Support:</b> the poster (p.4) on the desk; give weaker groups the eight feeling labels. <b>Fast finishers:</b> write the same moment twice, once happy and once nervous, without naming either feeling.</div>
  <p class="small"><b>Show It Sort key:</b> {sort_key}</p>
</div>

<div class="page">
  <div class="band"><div><div class="k">Groups of 3–4 · cut up the 24 cards</div><h1>Show It Sort</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.4pt;margin:0 0 2mm">Sort the cards into <b>eight feelings</b>: happy, excited, scared, nervous, angry, sad, bored, embarrassed. Each feeling has 3 cards. No card names its feeling: look for the clues.</p>
  <div class="fym">{sort_html}</div>
</div>

<div class="page">
  <div class="band"><div><div class="k">Pairs · cut along the dashed line</div><h1>Picture This A/B</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.4pt">Each description uses all five senses and shows one feeling without naming it. Listen carefully: can you catch them all?</p>
  {swap_card("A", SWAP_A, SWAP_B)}
  {swap_card("B", SWAP_B, SWAP_A)}
</div>

<div class="page">
  <div class="poster">
    <h1>Show it. Don't tell it.</h1>
    <div class="ops">
      <div style="background:var(--green-soft)"><b>Body clues</b>not "I was scared"<br>My heart pounded. I froze.</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Five senses</b>see · hear · smell<br>taste · touch</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Strong verbs</b>walked → trudged · crept<br>said → whispered · muttered</div>
      <div style="background:var(--green-soft)"><b>Zoom in</b>a dog → a scruffy<br>brown terrier</div>
    </div>
    <p style="text-align:center;font-size:20pt!important;font-weight:800;margin:4mm 0">Cut: nice · good · thing · stuff · lots</p>
    <p style="text-align:center;font-size:10pt;color:var(--muted)">Léim · leim.ie · Play Show, Don't Tell: {GAME}</p>
  </div>
</div>

<div class="page ws">
  <div class="band"><div><div class="k">Worksheet · exam-style questions</div><h1>Fix the Writing</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Fix the Writing</h2>
  <p>Each sentence has one problem. Say what's wrong and write a better version.</p>
  <table class="eh"><thead><tr><th>Student writing</th><th>What's wrong and the fix</th></tr></thead><tbody>
  {"".join(f"<tr><td style='font-weight:500'>{s}</td><td><span class='gap'></span><span class='gap'></span></td></tr>" for s, r in FIX)}
  </tbody></table>
  <h2>B. Exam-style questions: "Market Morning"</h2>
  <div class="pass">{" ".join(MARKET)}</div>
  <ol class="q">
    <li>Find one detail the writer can see and one they can hear.<span class="long"></span></li>
    <li>Pick out a strong verb. Why is it better than a plainer verb?<span class="long"></span></li>
    <li>How does the writer show how they feel without naming the feeling?<span class="long"></span></li>
    <li>Find one detail that "zooms in". What does it help you picture?<span class="long"></span></li>
    <li>Write a paragraph about a busy place you know. Use three senses and show one feeling.<span class="long"></span><span class="long"></span></li>
  </ol>
</div>

<div class="page an">
  <div class="band"><div><div class="k">For the teacher</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>Show It Sort</h2>
  <p>{sort_key}</p>
  <h2>Picture This</h2>
  {"".join(f"<p><b>{n}:</b> " + " · ".join(f"{SN[k]}: <i>{dict((SWAP_A, SWAP_B))[n][ln - 1]}</i>" for k, ln in sorted(SWAP_KEY[n][0].items(), key=lambda z: z[1])) + f" · Feeling shown: <b>{FN[SWAP_KEY[n][1]]}</b> (<i>{dict((SWAP_A, SWAP_B))[n][5]}</i>)</p>" for n in SWAP_KEY)}
  <p>Best strong verbs: raced, rumbled, spread (A) · slid, scraped, roared, clung (B). Accept any well-chosen verb with a reason.</p>
  <h2>A. Fix the Writing</h2>
  <table><tbody>{"".join(f"<tr><td style='width:40%'>{s}</td><td>{r}</td></tr>" for s, r in FIX)}</tbody></table>
  <h2>B. Exam-style questions</h2>
  <ol class="q">
    <li>See: "bright red apples", "silver mackerel glittered on the ice". Hear: "traders shouted prices over the noise".</li>
    <li>"squeezed" (or "glittered", "shouted"): it shows how crowded the gates were, which "went" or "walked" would not.</li>
    <li>"I grinned" and "the best part of Saturday": the reader can tell they are happy from the action and the final thought.</li>
    <li>"silver mackerel glittered on the ice": colour, the kind of fish and the ice let us picture the stall exactly.</li>
    <li>Credit three different senses, specific details, strong verbs and a feeling shown through actions or body language.</li>
  </ol>
  <h2>Marking tip</h2>
  <p>Reward precision over length: a short paragraph with a shown feeling, two or three senses and strong verbs beats a long one full of "nice" and "really". Our guide, not an official marking scheme.</p>
</div>
</body></html>"""

cover = """<!doctype html><html><head><meta charset="utf-8"><style>
body{margin:0;width:1200px;height:1200px;background:#1B2430;font-family:Inter,sans-serif;color:#fff;display:flex;flex-direction:column;justify-content:space-between;padding:90px;box-sizing:border-box}
.k{display:inline-block;background:#2E7D57;border-radius:99px;padding:12px 26px;font-weight:700;font-size:28px;letter-spacing:.06em;text-transform:uppercase}
h1{font-size:96px;font-weight:800;line-height:1.25;letter-spacing:-.02em;margin:60px 0 20px}
h1 span{background:#F6CF5A;color:#1B2430;padding:0 18px;border-radius:14px}
.sub{font-size:40px;line-height:1.4;color:#DDE3EA}
.em{font-size:48px;margin-top:30px;font-weight:800;letter-spacing:.01em;color:#F6CF5A}
.foot{display:flex;justify-content:space-between;align-items:center;font-size:34px;font-weight:700}
.price{background:#F6CF5A;color:#1B2430;border-radius:16px;padding:14px 28px}
</style></head><body>
<div><span class="k">Junior Cycle English · Teacher pack</span>
<h1><span>Personal &amp;</span><br><span>descriptive writing</span></h1>
<div class="sub">Show It Sort cards · Picture This A/B<br>Poster · Worksheet + answers</div>
<div class="em">show, don't tell · five senses<br>strong verbs · zoom in</div></div>
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
    pdf("teacher-pack", os.path.join(OUT, "Personal-Descriptive-Writing-Teacher-Pack-Leim.pdf"))
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--hide-scrollbars", "--window-size=1200,1200",
                    f"--screenshot={os.path.join(OUT, f'{SLUG}-cover.png')}", f"{SLUG}-cover.html"], cwd=SRC, check=True, capture_output=True)
