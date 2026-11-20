#!/usr/bin/env python3
"""Poetry 2: theme, tone & comparing poems (JC English Order 23): free sheet (-> printables/),
6-page teacher pack + 1200x1200 cover (-> OUTDIR).
Usage: python3 src/build_poetry2_pdfs.py /tmp/p2
Items come from the game's data block (mood-match.html). Every answer is re-derived with the checker's own rules
(src/test_mood_match.py: tones, tone_hits, themes, plain) and asserted; the checker's data pass runs first.
Styles are read from src/build_money1_pdfs.py."""
import os, sys, random, subprocess, re
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC); sys.path.insert(0, SRC)
from test_mood_match import tones, tone_hits, themes, plain, load, data_pass, TURN
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/p2"; os.makedirs(OUT, exist_ok=True)
SLUG = "poetry-theme-tone-comparing"
LO = "R7, R8, R9, R4, W8"
GAME = "leim.ie/mood-match.html"
D = load(os.path.join(ROOT, "mood-match.html")); assert not data_pass(D), data_pass(D)
TN = {"jo": "joyful", "sa": "sad", "ca": "peaceful", "te": "tense", "an": "angry", "no": "nostalgic"}
HN = {"fr": "friendship", "lo": "loss", "na": "nature", "ho": "home & place", "gr": "growing up"}
def br(s): return plain(s).replace(" / ", "<br>")
def one(s): return plain(s)
def tone1(s): t = tones(s); assert len(t) == 1, s; return t[0]
def theme1(lines): t = themes(" ".join(lines)); assert len(t) == 1, lines; return t[0]

# ---------- free sheet ----------
random.seed(2321)
A_items = [random.choice([y for y in D["tone"] if y[1] == k]) for k in TN]
for k in random.sample(list(TN), 2): A_items.append(random.choice([y for y in D["tone"] if y[1] == k and y not in A_items]))
A_items = [tuple(x) for x in A_items]; assert len(set(A_items)) == 8
A_items = A_items[:8]; random.shuffle(A_items)
for s, k in A_items: assert tone1(s) == k
B_items = random.sample([x for x in D["tone"] if tuple(x) not in A_items], 6)
for s, k in B_items: assert len(tone_hits(s)) == 1
C_items = random.sample([P for P in D["theme"] if P["t"] in ("fr", "lo", "gr")], 3)
for P in C_items: assert theme1(P["lines"]) == P["t"]
D_items = random.sample(D["shift"], 2)
for P in D_items: assert [tone1(" ".join(P["lines"][:2])), tone1(" ".join(P["lines"][2:]))] == [P["a"], P["b"]]
E_items = random.sample(D["pair"], 2)
for P in E_items: assert theme1(P["a"]) == theme1(P["b"]) == P["t"] and tone1(" ".join(P["a"])) == P["ta"] and tone1(" ".join(P["b"])) == P["tb"]
nA = 1; nB = nA + 8; nC = nB + 6; nD = nC + 3; nE = nD + 2; nF = nE + 2
NQ = nF + 2 - 1; assert NQ == 23, NQ
def turn(P): return re.match(TURN, P["lines"][2]).group(1)

def style(var):
    return re.search(var + r' = f"""<!doctype.*?<style>(.*?)</style>', open(os.path.join(SRC, "build_money1_pdfs.py"), encoding="utf-8").read(), re.S).group(1).replace("{LO}", LO).replace("{{", "{").replace("}}", "}").replace("JC Maths LOs (2018 spec)", "JC English LOs (2015 spec)")
SHEET_STYLE = style("sheet"); PACK_STYLE = style("pack")
assert "JC English LOs (2015 spec)" in SHEET_STYLE and "Single-teacher licence" in PACK_STYLE and "JC English LOs (2015 spec)" in PACK_STYLE
EXTRA = """.wk{line-height:1.45;border:1.5px solid var(--line);border-radius:8px;padding:2px 7px;margin:3px 0;font-size:9.4pt}.wk b.h{display:block}
table.st{border-collapse:collapse;margin:3px 0;font-size:9.2pt;width:100%}table.st td,table.st th{border:1px solid #C9D1DA;padding:2px 6px;text-align:left}
.pass{border-left:4px solid var(--green);background:var(--mist);padding:5px 10px;margin:4px 0;font-family:Georgia,serif;font-size:9.4pt;line-height:1.45}
.pass i{color:#4A5562}.box{border:1.5px dashed #9AA6B2;border-radius:8px;padding:3px 8px;margin:2px 0 4px;font-size:9pt}"""


EXTRA += """
.pm{font-family:Georgia,serif;font-style:italic;font-size:9.3pt;line-height:1.4;border:1.5px solid var(--line);border-radius:8px;padding:3px 8px;margin:2px 0}
.pm b{font-style:normal;font-family:Inter,sans-serif;font-size:8.6pt}.cp{display:grid;grid-template-columns:1fr 1fr;gap:3mm}"""

def two(items_html, cut):
    return f"<div class='two'><div><ol class='q'>{''.join(items_html[:cut])}</ol></div><div><ol class='q'>{''.join(items_html[cut:])}</ol></div></div>"
A_html = [f"<li value='{i}'><i>{br(s)}</i> <span class='line' style='min-width:20mm'></span></li>" for i, (s, k) in enumerate(A_items, nA)]
B_html = [f"<li value='{i}'><i>{br(s)}</i></li>" for i, (s, k) in enumerate(B_items, nB)]
C_html = "".join(f"<div><ol class='q'><li value='{i}'><div class='pm'><b>{P['k'][2:].strip()}</b><br>{'<br>'.join(P['lines'])}</div>Theme: <span class='line' style='min-width:22mm'></span></li></ol></div>" for i, P in enumerate(C_items, nC))
D_html = "".join(f"<div><ol class='q'><li value='{i}'><div class='pm'><b>{P['k'][2:].strip()}</b><br>{'<br>'.join(P['lines'])}</div>Mood: <span class='line' style='min-width:14mm'></span> → <span class='line' style='min-width:14mm'></span> Turn word: <span class='line' style='min-width:12mm'></span></li></ol></div>" for i, P in enumerate(D_items, nD))
E_html = "".join(f"<li value='{i}'><div class='cp'><div class='pm'><b>A · {P['ka'][2:].strip()}</b><br>{'<br>'.join(P['a'])}</div><div class='pm'><b>B · {P['kb'][2:].strip()}</b><br>{'<br>'.join(P['b'])}</div></div>Shared theme: <span class='line' style='min-width:22mm'></span> Mood of A: <span class='line' style='min-width:16mm'></span> Mood of B: <span class='line' style='min-width:16mm'></span></li>" for i, P in enumerate(E_items, nE))

POEM_A = ("Saturday in Ennis", ["The market fills the square by nine,", "striped awnings flapping in the breeze,", "a man selling cheese and jokes,", "a girl with a fiddle by the bank.", "We buy warm bread and eat it walking,", "laughing at nothing at all.", "This town on a Saturday", "is the best place in the world."])
POEM_B = ("The Shop", ["Mr Kelly's shop is closed now.", "The sign still says OPEN,", "faded to the colour of tea.", "I remember the jars of sweets,", "the bell that rang above the door,", "the way he called me \"young lad\".", "Now dust settles on the counter", "and nobody rings the bell."])
assert themes(" ".join(POEM_A[1])) == ["ho"] and tones(" ".join(POEM_A[1])) == ["jo"]
assert tones(" ".join(POEM_B[1][:6])) == ["no"] and tones(" ".join(POEM_B[1][6:])) == [] and re.match(TURN, POEM_B[1][6])
# the sheet's exam poems (different from the game page's Exam corner poems)
POEM_C = ("The Pier at Dawn", ["Grandad and I on the pier at dawn,", "the sea as calm as glass,", "two rods, one flask of tea,", "the gulls not even awake yet."])
POEM_D = ("The Pier in January", ["The waves are raging at the pier,", "spitting salt across the wall,", "and I stand where we used to fish", "with nobody beside me now."])
assert themes(" ".join(POEM_C[1])) == ["na"] and tones(" ".join(POEM_C[1])) == ["ca"] and tones(" ".join(POEM_D[1])) == ["an"] and "na" in themes(" ".join(POEM_D[1]))

sheet = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Poetry 2: theme, tone and comparing poems, rules and practice | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{SHEET_STYLE}
{EXTRA}
.p2 ol.q li{{margin-bottom:1px;font-size:9pt}}.p2 h2{{margin:4px 0 2px}}.p2 .two{{gap:5mm}}.three{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:3mm}}.three ol.q{{margin:0}}
.dd{{display:grid;grid-template-columns:1fr 1fr;gap:4mm}}.dd ol.q{{margin:0}}
</style></head><body>
<div class="page tight">
  <div class="band"><div><div class="k">Junior Cycle English · Free revision sheet</div><h1>Poetry 2: theme &amp; mood</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2015 specification): {LO}. Play the game: <b>{GAME}</b></p>
  <p>In 1st year you learned <b>how</b> poets write: similes, metaphors, sound. Now the questions go deeper: <b>What is the poem really about? How does it make you feel? How does it compare with another poem?</b></p>
  <div class="two">
   <div><h2>1. Theme, mood and tone</h2>
    <table class="st"><tbody>
     <tr><td><b>Theme</b></td><td>the big idea: friendship, loss, nature, home and place, growing up. Say it in a few words.</td></tr>
     <tr><td><b>Mood</b></td><td>the feeling the poem creates in <b>you</b>, the reader.</td></tr>
     <tr><td><b>Tone</b></td><td>the poet's <b>attitude</b>, like a tone of voice: fond, angry, sad, playful.</td></tr>
     <tr><td><b>Topic</b></td><td>what the poem describes (a dog, a kitchen). Not the same as the theme!</td></tr></tbody></table>
    <h2>2. Six moods and their words</h2>
    <table class="st"><tbody>
     <tr><td><b>Joyful</b></td><td>laughter, danced, cheered, giggled</td></tr>
     <tr><td><b>Sad</b></td><td>tears, lonely, sighed, wept</td></tr>
     <tr><td><b>Peaceful</b></td><td>calm, hush, softly, gentle</td></tr>
     <tr><td><b>Tense</b></td><td>lurking, pounding, dread, crept</td></tr>
     <tr><td><b>Angry</b></td><td>slammed, raging, glared, snarled</td></tr>
     <tr><td><b>Nostalgic</b></td><td>remember, memories, recall: looking back fondly</td></tr></tbody></table></div>
   <div><h2>3. Spot the pattern</h2>
    <div class="wk"><b>A</b><i>The sea is calm this morning, / a silver sheet out to the island.</i><br><b>B</b><i>The sea is raging at the harbour, / spitting foam across the pier.</i></div>
    <p style="font-size:9pt">Same <b>theme</b> (nature, the sea), opposite <b>mood</b>: A is peaceful ("calm"), B is angry ("raging", "spitting"). One or two words change everything.</p>
    <h2>4. When the mood turns</h2>
    <p style="font-size:9pt">Watch for a <b>turn word</b> at the start of a line: <b>But</b>, <b>Then</b>, <b>Now</b>, <b>Until</b>. <i>We laughed and raced along the sand ... But then the tide came rushing in / and fear went through me like ice.</i> Joyful → tense.</p>
    <h2>5. Comparing two poems</h2>
    <div class="wk"><b>Both poems</b> are about ... <b>However</b>, poem A feels ..., because "...", <b>whereas</b> poem B feels ..., because "...". <b>I prefer</b> ... because ...</div>
    <p style="font-size:9pt">Quote from <b>both</b> poems. Point, quote, explain: say <b>how</b> the word creates the mood.</p></div>
  </div>
  <div class="tip"><b>Exam tip:</b> name the mood or theme in one word, prove it with a short quote, then explain the word: "raging" makes the sea sound like a furious person. Don't just retell the poem.</div>
</div>

<div class="page p2">
  <div class="band"><div><div class="k">Practice · {NQ} questions</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Which mood? (joyful / sad / peaceful / tense / angry / nostalgic)</h2>
  {two(A_html, 4)}
  <h2>B. Underline the ONE word that sets the mood</h2>
  {two(B_html, 3)}
  <h2>C. What's the theme? (friendship / loss / nature / home and place / growing up)</h2>
  <div class="three">{C_html}</div>
  <h2>D. How does the mood change? Write both moods and the turn word.</h2>
  <div class="dd">{D_html}</div>
</div>

<div class="page">
  <div class="band"><div><div class="k">Compare · exam-style · answers</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <h2>E. Compare two poems</h2>
  <ol class="q">{E_html}</ol>
  <h2>F. Exam-style</h2>
  <div class="cp"><div class="pm"><b>A · {POEM_C[0]}</b><br>{"<br>".join(POEM_C[1])}</div><div class="pm"><b>B · {POEM_D[0]}</b><br>{"<br>".join(POEM_D[1])}</div></div>
  <ol class="q">
   <li value="{nF}">What is the mood of poem A? Support your answer with one quotation.<span class="long"></span></li>
   <li value="{nF + 1}">Both poems are set on the same pier. Compare the moods of the two poems, quoting from both.<span class="long"></span><span class="long"></span></li>
  </ol>
  <h2>Answers</h2>
  <table class="ans"><tbody>
   <tr><td><b>A</b></td><td>{" · ".join(f"{i}. {TN[tone1(s)]}" for i, (s, k) in enumerate(A_items, nA))}</td></tr>
   <tr><td><b>B</b></td><td>{" · ".join(f"{i}. {tone_hits(s)[0]} ({TN[tone1(s)]})" for i, (s, k) in enumerate(B_items, nB))}</td></tr>
   <tr><td><b>C</b></td><td>{" · ".join(f"{i}. {HN[theme1(P['lines'])]}" for i, P in enumerate(C_items, nC))}</td></tr>
   <tr><td><b>D</b></td><td>{" · ".join(f"{i}. {TN[P['a']]} → {TN[P['b']]}, turn word: {turn(P)}" for i, P in enumerate(D_items, nD))}</td></tr>
   <tr><td><b>E</b></td><td>{" · ".join(f"{i}. theme: {HN[P['t']]}; A {TN[P['ta']]}, B {TN[P['tb']]}" for i, P in enumerate(E_items, nE))}</td></tr>
   <tr><td><b>F</b></td><td>{nF}. Peaceful: "the sea as calm as glass", "the gulls not even awake yet". {nF + 1}. Both poems are set on the same pier, but poem A is peaceful ("the sea as calm as glass") and close (Grandad and the speaker share "one flask of tea"), whereas poem B is angry and lonely: the waves are "raging" and "spitting", and the speaker stands "with nobody beside me now". The weather matches the feeling: B suggests a loss.</td></tr>
  </tbody></table>
  <div class="note"><b>Got one wrong?</b> Go back to page 1, then play <b>Mood Match</b> at {GAME}: the "Go back over these" list at the end explains each mistake.</div>
  <p class="small">All poems are written by Léim. Léim is independent and not connected with the State Examinations Commission or the NCCA.</p>
</div>
</body></html>"""

# ---------- teacher pack ----------
random.seed(2322)
MS = [x for k in TN for x in random.sample([y for y in D["tone"] if y[1] == k], 4)]; random.shuffle(MS)
assert len(MS) == 24
for s, k in MS: assert tone1(s) == k
ms_html = "".join(f'<div class="c"><span class="tag">Card {i}</span><div class="fc sm"><i>{br(s)}</i></div></div>' for i, (s, k) in enumerate(MS, 1))
ms_key = " · ".join(f"<b>{TN[k].capitalize()}</b>: {', '.join(str(i) for i, (s, kk) in enumerate(MS, 1) if kk == k)}" for k in TN)

PS = random.sample(D["pair"], 4); PA, PB = PS[:2], PS[2:]
SS = random.sample(D["shift"], 2); SA, SB = SS[:1], SS[1:]
for P in PS: assert theme1(P["a"]) == theme1(P["b"]) == P["t"] and tone1(" ".join(P["a"])) == P["ta"] and tone1(" ".join(P["b"])) == P["tb"]
for P in SS: assert [tone1(" ".join(P["lines"][:2])), tone1(" ".join(P["lines"][2:]))] == [P["a"], P["b"]]
def swap_card(who, pairs, shifts):
    rows = "".join(f"<tr><td style='width:4%'><b>{i}</b></td><td><i>A: {' / '.join(P['a'])}</i><br><i>B: {' / '.join(P['b'])}</i></td></tr>" for i, P in enumerate(pairs, 1))
    grid = "".join(f"<tr><td><b>{i}</b></td><td></td><td></td><td></td><td></td></tr>" for i in range(1, 3))
    sh = "".join(f"<tr><td><i>{' / '.join(P['lines'])}</i></td></tr>" for P in shifts)
    return f"""<div class="idc"><h3>Student {who} · Compare Swap</h3>
    <p style="font-size:8.8pt;margin:0 0 1mm"><b>1. Read</b> each pair of short poems (A, then B) aloud, twice. Don't say the moods!</p>
    <table class="st" style="font-size:8.8pt"><tbody>{rows}</tbody></table>
    <p style="font-size:8.8pt;margin:1mm 0"><b>2. Listen</b> to your partner's two pairs and fill in the grid.</p>
    <table class="st" style="font-size:8.8pt"><thead><tr><th style="width:4%"></th><th>Shared theme</th><th>Mood of A</th><th>Mood of B</th><th>One word that proves it</th></tr></thead><tbody>{grid}</tbody></table>
    <p style="font-size:8.8pt;margin:1mm 0"><b>3. Mood turn.</b> Read this poem aloud. Your partner says the turn word and how the mood changes.</p>
    <table class="st" style="font-size:8.8pt"><tbody>{sh}</tbody></table></div>"""

FIX = [("The poem is about a man in a shop.", "That's the topic, not the theme. Name the big idea: <b>The theme is how places we love change over time.</b>"),
       ("The mood is happy because it is a happy poem.", "No evidence. Quote and explain: <b>The mood is joyful: the friends are \"laughing at nothing at all\", which shows how carefree they feel.</b>"),
       ("First the poet says the market fills the square. Then he says there are awnings. Then ...", "Retelling line by line. Make a point about the poem instead: <b>The poet fills the market with movement and sound to make it feel alive.</b>"),
       ("Poem A is joyful. Poem B is sad.", "Two statements, not a comparison, and no quotes: <b>Both poems are about a town, but A is joyful (\"laughing\") whereas B is sad and empty (\"nobody rings the bell\").</b>"),
       ("The word \"raging\" is a good word.", "Say what the word DOES: <b>\"Raging\" makes the sea sound like a furious person, which creates an angry, threatening mood.</b>"),
       ("I like the poem because it is nice.", "Give a real reason with a reference: <b>I like the poem because the sign that \"still says OPEN\" on a closed shop is a sad, clever detail.</b>")]
assert tones("laughing at nothing at all") == ["jo"] and tones("raging") == ["an"]

EX_A = ("The Kitchen at Christmas", ["Every Christmas Eve the kitchen fills,", "cousins squashed around the table,", "Gran's laughter over the radio,", "the windows steamed and gold."])
EX_B = ("The Kitchen in March", ["I remember the noise, the crowded table.", "Now Gran's chair is pushed against the wall", "and the kitchen is quiet,", "just the clock and the kettle."])
assert themes(" ".join(EX_A[1])) == ["ho"] and tones(" ".join(EX_A[1])) == ["jo"]
assert tones(EX_B[1][0]) == ["no"] and tones(" ".join(EX_B[1][1:])) == ["ca"] and re.match(TURN, EX_B[1][1]) and "ho" in themes(" ".join(EX_B[1]))

pack = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Poetry 2: Theme, Tone &amp; Comparing Poems Teacher Pack | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{PACK_STYLE}
{EXTRA}
.fym .c{{height:36mm}}.fym .fc.sm{{font-size:10pt;line-height:1.35;margin-top:2mm;font-weight:500;font-family:Georgia,serif}}.idc{{padding:2mm 4mm;margin-bottom:3mm}}.idc h3{{margin:0 0 1mm}}
.idc .st td,.idc .st th{{padding:1px 5px}}.idc .st td{{height:5mm}}.p1 .proc td{{font-size:8.6pt;padding:2px 6px}}.ops div{{font-size:12pt;padding:5mm 3mm}}.ops b{{font-size:19pt}}
.ws .eh td{{font-size:8.6pt;padding:2px 6px}}.ws .eh .gap{{height:13px}}.ws ol.q li{{margin-bottom:1px}}
</style></head><body>

<div class="page p1">
  <div class="band"><div><div class="k">Junior Cycle English · Teacher pack</div><h1>Poetry 2: theme &amp; mood</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2015 specification): {LO}</p>
  <div class="two">
    <div><h3>Aims</h3><p>By the end of the lesson students can name the theme of a short poem (and tell it apart from the topic), name its mood and the words that create it, say where and how a mood turns, and compare two poems on the same theme using point, quote, explain.</p></div>
    <div><h3>In this pack</h3><p>p.1 Teacher notes · p.2 Mood Sort cards (cut-up) · p.3 Compare Swap A/B (speaking and listening) · p.4 Wall poster · p.5 Worksheet: Fix the Answer + exam-style questions · p.6 Answers. Level: 2nd year. Time: about 60 minutes. All poems are written by Léim, so they work alongside whatever poems your class studies.</p></div>
  </div>
  <h2 style="margin-top:8px">Procedure</h2>
  <table class="proc"><tbody>
    <tr><td>5 min</td><td><b>Lead-in.</b> Read the two sea couplets (free sheet, box 3). Same theme? Same mood? Which words make the difference? Board: theme / mood / tone / topic.</td></tr>
    <tr><td>8 min</td><td><b>Guided discovery.</b> Read "The Beach" aloud (free sheet, box 4). Where does the mood turn? Which word signals it? Build a list of turn words (But, Then, Now, Until).</td></tr>
    <tr><td>12 min</td><td><b>Mood Sort</b> (p.2, groups of 3, one set of 24 cards). Sort the couplets into six moods and underline the one word that sets each mood. Groups that finish early rank the cards in each pile from strongest to weakest.</td></tr>
    <tr><td>12 min</td><td><b>Compare Swap</b> (p.3, pairs). A reads two pairs of short poems; B fills the grid (shared theme, mood of each, a word that proves it). Then A reads a poem with a turn; B names the turn word and the change. Swap.</td></tr>
    <tr><td>18 min</td><td><b>Worksheet</b> (p.5). Fix the Answer in pairs, then the exam-style questions on "The Kitchen at Christmas" and "The Kitchen in March" alone.</td></tr>
    <tr><td>5 min</td><td><b>Exit ticket.</b> Write one sentence comparing two poems from your anthology using "both" and "whereas". Homework: play <b>Mood Match</b> at {GAME}.</td></tr>
  </tbody></table>
  <div class="note"><b>Errors to look for:</b> naming the topic instead of the theme · "happy / sad" with no quote · retelling the poem line by line · comparing by writing about one poem, then the other, with no linking words · quoting a whole stanza instead of a word or phrase · confusing sad and nostalgic (nostalgic looks back <b>fondly</b>). <b>Support:</b> the poster (p.4) on the desk. <b>Fast finishers:</b> rewrite one Mood Sort card with a different mood word.</div>
</div>

<div class="page">
  <div class="band"><div><div class="k">Groups of 3 · cut up the 24 cards</div><h1>Mood Sort</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.4pt;margin:0 0 2mm">Sort the couplets into six piles: <b>joyful · sad · peaceful · tense · angry · nostalgic</b>. Underline the one word that sets the mood.</p>
  <div class="fym">{ms_html}</div>
</div>

<div class="page">
  <div class="band"><div><div class="k">Pairs · cut along the dashed line</div><h1>Compare Swap A/B</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.4pt">Read, listen, compare: same theme, different mood.</p>
  {swap_card("A", PA, SA)}
  {swap_card("B", PB, SB)}
</div>

<div class="page">
  <div class="poster">
    <h1>Same theme. Different mood.</h1>
    <div class="ops">
      <div style="background:var(--green-soft)"><b>Theme</b>the big idea<br>friendship · loss · home</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Mood</b>how it makes<br>YOU feel</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Turn</b>But · Then<br>Now · Until</div>
      <div style="background:var(--green-soft)"><b>Compare</b>both · whereas<br>however</div>
    </div>
    <p style="text-align:center;font-size:20pt!important;font-weight:800;margin:4mm 0">Point. Quote. Explain the word.</p>
    <p style="text-align:center;font-size:10pt;color:var(--muted)">Léim · leim.ie · Play Mood Match: {GAME}</p>
  </div>
</div>

<div class="page ws">
  <div class="band"><div><div class="k">Worksheet · exam-style questions</div><h1>Fix the Answer</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Fix the Answer</h2>
  <p>Each line is part of a student's answer about the poems on the free sheet's page 3 or the Mood Match page. Say what's wrong and write a better version.</p>
  <table class="eh"><thead><tr><th>Answer</th><th>What's wrong and the fix</th></tr></thead><tbody>
  {"".join(f"<tr><td style='font-weight:500'>{s}</td><td><span class='gap'></span><span class='gap'></span></td></tr>" for s, r in FIX)}
  </tbody></table>
  <h2>B. Exam-style questions</h2>
  <div class="cp"><div class="pm"><b>A · {EX_A[0]}</b><br>{"<br>".join(EX_A[1])}</div><div class="pm"><b>B · {EX_B[0]}</b><br>{"<br>".join(EX_B[1])}</div></div>
  <ol class="q">
    <li>What theme do both poems share?<span class="long"></span></li>
    <li>What is the mood of poem A? Support your answer with two quotations.<span class="long"></span></li>
    <li>Where does the mood change in poem B, and how? Refer to the poem.<span class="long"></span></li>
    <li>Pick one word from poem B and explain how it creates a feeling.<span class="long"></span></li>
    <li>Which poem do you prefer? Compare both poems in your answer.<span class="long"></span><span class="long"></span></li>
  </ol>
</div>

<div class="page an">
  <div class="band"><div><div class="k">For the teacher</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>Mood Sort (card numbers)</h2>
  <p>{ms_key}. Mood words: {" · ".join(f"{i} {tone_hits(s)[0]}" for i, (s, k) in enumerate(MS, 1))}.</p>
  <h2>Compare Swap</h2>
  <p>{" · ".join(f"<b>{w}{i}</b> {HN[P['t']]}: A {TN[P['ta']]} ({tone_hits(' '.join(P['a']))[0]}), B {TN[P['tb']]} ({tone_hits(' '.join(P['b']))[0]})" for w, LL in (("A", PA), ("B", PB)) for i, P in enumerate(LL, 1))}.</p>
  <p>Mood turns: {" · ".join(f"<b>{w}</b> {TN[P['a']]} → {TN[P['b']]}, turn word: {turn(P)}" for w, LL in (("A", SA), ("B", SB)) for P in LL)}.</p>
  <h2>A. Fix the Answer</h2>
  <table><tbody>{"".join(f"<tr><td style='width:34%'>{s}</td><td>{r}</td></tr>" for s, r in FIX)}</tbody></table>
  <h2>B. Exam-style questions</h2>
  <ol class="q">
    <li>Home and place: the family kitchen, and how it changes.</li>
    <li>Joyful and warm: "Gran's laughter over the radio", "cousins squashed around the table", "the windows steamed and gold".</li>
    <li>Line 1 is nostalgic ("I remember the noise"); the turn comes with "Now": Gran's chair is "pushed against the wall" and the kitchen is quiet. The mood becomes still and empty, suggesting Gran is gone.</li>
    <li>E.g. "quiet": after the noise of Christmas, the silence shows how much is missing; "just the clock" makes the time feel slow and lonely.</li>
    <li>Both poems are about the same kitchen, but A is joyful and crowded whereas B is quiet and nostalgic. Reward a clear preference, reference to both poems and comparing words.</li>
  </ol>
  <h2>Marking tip</h2>
  <p>Reward a clear point, a short accurate quote and an explanation of how the word creates the mood; when comparing, reward answers that discuss both poems together. Our guide, not an official marking scheme.</p>
</div>
</body></html>"""

cover = """<!doctype html><html><head><meta charset="utf-8"><style>
body{margin:0;width:1200px;height:1200px;background:#1B2430;font-family:Inter,sans-serif;color:#fff;display:flex;flex-direction:column;justify-content:space-between;padding:90px;box-sizing:border-box}
.k{display:inline-block;background:#2E7D57;border-radius:99px;padding:12px 26px;font-weight:700;font-size:28px;letter-spacing:.06em;text-transform:uppercase}
h1{font-size:100px;font-weight:800;line-height:1.25;letter-spacing:-.02em;margin:60px 0 20px}
h1 span{background:#F6CF5A;color:#1B2430;padding:0 18px;border-radius:14px}
.sub{font-size:40px;line-height:1.4;color:#DDE3EA}
.em{font-size:46px;margin-top:30px;font-weight:800;letter-spacing:.01em;color:#F6CF5A}
.foot{display:flex;justify-content:space-between;align-items:center;font-size:34px;font-weight:700}
.price{background:#F6CF5A;color:#1B2430;border-radius:16px;padding:14px 28px}
</style></head><body>
<div><span class="k">Junior Cycle English · Teacher pack</span>
<h1><span>Poetry 2:</span><br><span>theme &amp; mood</span></h1>
<div class="sub">Mood Sort cards · Compare Swap A/B<br>Poster · Worksheet + answers</div>
<div class="em">theme · mood · tone<br>comparing two poems</div></div>
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
    pdf("teacher-pack", os.path.join(OUT, "Poetry-Theme-Tone-Comparing-Teacher-Pack-Leim.pdf"))
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--hide-scrollbars", "--window-size=1200,1200",
                    f"--screenshot={os.path.join(OUT, f'{SLUG}-cover.png')}", f"{SLUG}-cover.html"], cwd=SRC, check=True, capture_output=True)
