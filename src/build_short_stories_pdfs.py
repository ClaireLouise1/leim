#!/usr/bin/env python3
"""Short stories (JC English Order 11): free sheet (-> printables/), 6-page teacher pack + 1200x1200 cover (-> OUTDIR).
Usage: python3 src/build_short_stories_pdfs.py /tmp/shortstories
Items come from the game's data block (twist-detector.html). Every answer is re-derived with the checker's own rules
(src/test_twist_detector.py: part, kind, linked, hook, places) and asserted.
Styles are read from src/build_money1_pdfs.py."""
import os, sys, random, subprocess, re
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC); sys.path.insert(0, SRC)
from test_twist_detector import part, parts, kind, linked, hook, places, load, WEAK, PLACEW
def clues(s, k): return ", ".join(m.group(0) for m in PLACEW[k].finditer(s))
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/shortstories"; os.makedirs(OUT, exist_ok=True)
SLUG = "short-stories"
LO = "R6, R8, R9, W7"
GAME = "leim.ie/twist-detector.html"
D = load(os.path.join(ROOT, "twist-detector.html"))
PN = {"se": "Setting", "pr": "Problem", "cl": "Climax", "en": "Ending"}
ON = {"d": "Dialogue", "a": "Action", "m": "Mystery"}
PLN = {"be": "Beach", "sc": "School", "fo": "Forest", "ho": "Hospital", "pi": "Match", "ki": "Kitchen", "fa": "Farm", "ci": "City"}
PK = ["se", "pr", "cl", "en"]
DREAM = "Then I woke up. It was all a dream."
assert kind(DREAM, ["x"]) == "dream"

# ---------- free sheet ----------
random.seed(1111)
stories = random.sample(D["stories"], 8)
A_items = []  # (line, part)
for n, k in enumerate(["pr", "se", "cl", "en", "pr", "se"]):
    S = stories[n]; A_items.append((S["lines"][PK.index(k)], k))
for s, k in A_items: assert part(s) == k, (s, parts(s))
B_items = []
for S in stories[7:8] + [random.choice([x for x in D["stories"] if x not in stories])]:
    idx = [1, 2, 3]; random.shuffle(idx)
    while idx == [1, 2, 3]: random.shuffle(idx)
    lets = "ABC"; ans = " → ".join(lets[idx.index(n)] for n in (1, 2, 3))
    rk = sorted(range(3), key=lambda j: {"pr": 1, "cl": 2, "en": 3}[part(S["lines"][idx[j]])])
    assert " → ".join(lets[j] for j in rk) == ans
    B_items.append((S, idx, ans))
C_items = []
for k in ("m", "d", "a"):
    C_items.append(random.choice([o for o in D["open"] if hook(o[2]) == k and o not in C_items]))
D_items = []
for k in ("fa", "ho", "ci", "be", "sc"):
    D_items.append(random.choice([x for x in D["place"] if x[1] == k]))
for s, k in D_items: assert places(s) == [k]
E_items = random.sample(D["twists"], 1); E_opts = []
for T in E_items:
    o = [T["twist"], T["plain"], T["random"], DREAM]; random.shuffle(o); E_opts.append(o)
    assert [x for x in o if kind(x, T["lines"]) == "twist"] == [T["twist"]] and linked(T["twist"], T["lines"]) == [T["clue"] - 1]
EX_LINES = ["Every night, a light flickered in the window of the empty house next door.", "Mam said nobody had lived there for years.",
            "My friend Conor had started carrying a torch in his schoolbag."]
EX_TWIST = "It turned out Conor had built a secret den in the attic and was reading comics by torch."
assert kind(EX_TWIST, EX_LINES) == "twist" and linked(EX_TWIST, EX_LINES) == [2]
NQ = len(A_items) + len(B_items) + len(C_items) + len(D_items) + 2 * len(E_items) + 2; assert NQ == 20, NQ
nA = 1; nE = nA + len(A_items); nB = nE + 2 * len(E_items); nC = nB + len(B_items); nD = nC + len(C_items); nF = nD + len(D_items)  # sheet order: A parts, B twist (E_items), C order (B_items), D openings (C_items), E setting (D_items)
def style(var):
    return re.search(var + r' = f"""<!doctype.*?<style>(.*?)</style>', open(os.path.join(SRC, "build_money1_pdfs.py"), encoding="utf-8").read(), re.S).group(1).replace("{LO}", LO).replace("{{", "{").replace("}}", "}").replace("JC Maths LOs (2018 spec)", "JC English LOs (2015 spec)")
SHEET_STYLE = style("sheet"); PACK_STYLE = style("pack")
assert "JC English LOs (2015 spec)" in SHEET_STYLE and "Single-teacher licence" in PACK_STYLE and "JC English LOs (2015 spec)" in PACK_STYLE
EXTRA = """.wk{line-height:1.45;border:1.5px solid var(--line);border-radius:8px;padding:2px 7px;margin:3px 0;font-size:9.4pt}.wk b.h{display:block}
table.st{border-collapse:collapse;margin:3px 0;font-size:9.2pt;width:100%}table.st td,table.st th{border:1px solid #C9D1DA;padding:2px 6px;text-align:left}
.bank{border:1.5px solid var(--line);border-radius:8px;padding:4px 10px;margin:4px 0;text-align:center;font-weight:700;word-spacing:4px}
.pass{border-left:4px solid var(--green);background:var(--mist);padding:5px 10px;margin:4px 0;font-style:italic}
.sty{border:1.5px solid var(--line);border-radius:8px;padding:2px 7px;margin:2px 0 3px;font-size:8.8pt}.sty p{margin:0 0 1px}"""
A_html = "".join(f"<li value='{i}'><i>{s}</i> <span class='line' style='min-width:16mm'></span></li>" for i, (s, k) in enumerate(A_items, nA))
def order_html(S, idx):
    return f"<div class='sty'><p><b>{S['lines'][0]}</b></p>" + "".join(f"<p><b>{'ABC'[j]}</b> {S['lines'][n]}</p>" for j, n in enumerate(idx)) + "</div>"
B_html = "".join(f"<li value='{i}'>Order: <span class='line' style='min-width:22mm'></span>{order_html(S, idx)}</li>" for i, (S, idx, a) in enumerate(B_items, nB))
C_html = "".join(f"<li value='{i}'><i>{h}</i> <span class='line' style='min-width:16mm'></span></li>" for i, (x, e, h, k) in enumerate(C_items, nC))
D_html = "".join(f"<li value='{i}'><i>{s}</i> <span class='line' style='min-width:16mm'></span></li>" for i, (s, k) in enumerate(D_items, nD))
def twist_html(i, T, o):
    return (f"<li value='{i}'><b>{T['k'][2:]}</b>: " + " ".join(f"({n}) {l}" for n, l in enumerate(T["lines"], 1)) +
            "<br>Circle the twist ending:<br>" + "<br>".join(f"&nbsp; {'abcd'[j]}) {x}" for j, x in enumerate(o)) + "</li>"
            f"<li value='{i+1}'>Which line (1, 2 or 3) planted the clue for that twist? <span class='line' style='min-width:12mm'></span></li>")
E_html = "".join(twist_html(nE + 2 * j, T, o) for j, (T, o) in enumerate(zip(E_items, E_opts)))

sheet = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Short stories, rules and practice | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{SHEET_STYLE}
{EXTRA}
.p2 ol.q li{{margin-bottom:1px;font-size:8.9pt}}.p2 h2{{margin:3px 0 1px}}.p2 .two{{gap:5mm}}.p2 .sty{{font-size:8.4pt;padding:1px 6px}}
</style></head><body>
<div class="page tight">
  <div class="band"><div><div class="k">Junior Cycle English · Free revision sheet</div><h1>Short stories</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2015 specification): {LO}. Play the game: <b>{GAME}</b></p>
  <div class="two">
   <div><h2>1. The shape of a story</h2>
    <table class="st"><thead><tr><th>Part</th><th>What it does</th><th>Look for</th></tr></thead><tbody>
     <tr><td><b>Setting</b></td><td>where and when</td><td>a time and a place: <i>a wet Saturday morning on Kilkee beach</i></td></tr>
     <tr><td><b>Problem</b></td><td>something goes wrong</td><td>lost, missing, stuck, locked, broken, couldn't</td></tr>
     <tr><td><b>Climax</b></td><td>the big moment where everything turns</td><td>Suddenly · Just then · At that moment · All at once</td></tr>
     <tr><td><b>Ending</b></td><td>how it works out</td><td>In the end · Finally · At last · From that day on</td></tr></tbody></table>
    <p style="font-size:8.8pt">Your teacher may call these <b>exposition, rising action, climax</b> and <b>resolution</b>.</p>
    <h2>2. A strong first line</h2>
    <table class="st"><tbody>
     <tr><td><b>Dialogue</b></td><td><i>“Don't open that door!” screamed Tara.</i></td></tr>
     <tr><td><b>Action</b></td><td><i>Oisín dived into the freezing lake before anyone could stop him.</i></td></tr>
     <tr><td><b>Mystery</b></td><td><i>There was something strange about the new boy's shadow.</i></td></tr></tbody></table>
    <p style="font-size:8.8pt">Not: <i>This is a story about…</i> · <i>Hi, I'm going to tell you a story…</i></p></div>
   <div><h2>3. Twist endings</h2>
    <div class="wk">A twist <b>surprises</b> the reader but was <b>set up by a clue</b> earlier. When you look back, it makes sense.<br>
    <i>(1) A parcel arrived. (2) It ticked quietly. (3) Grandad had been talking about his broken alarm clock.</i><br>
    Twist: <b>It turned out to be a new alarm clock that Grandad had ordered online.</b> (clue: line 3)<br>
    Cheats: an ending that nothing set up · <i>It was all a dream.</i></div>
    <h2>4. Setting clues</h2>
    <div class="wk">Writers rarely say "at the beach". They <b>show</b> it with clue words: <i>sand, gulls, the tide, seaweed</i>.
    In an answer, <b>quote the clue words</b> and say what they help you picture.</div>
    <div class="note"><b>Classic mistakes:</b> too many characters for a short story · no real problem · "It was all a dream" · an ending from nowhere · telling the reader the place instead of showing it · retelling the whole plot when the question asks about one part.</div></div>
  </div>
  <div class="tip"><b>Exam tip:</b> when you write a short story, plan the ending <b>first</b>, then plant one clue for it early on. One problem, two or three characters, a strong first line.</div>
</div>

<div class="page p2">
  <div class="band"><div><div class="k">Practice · {NQ} questions</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <div class="two"><div><h2>A. Which part of the story?</h2><div class="bank" style="font-size:8.4pt">Setting · Problem · Climax · Ending</div><ol class="q">{A_html}</ol>
  <h2>B. Twist Detector</h2><ol class="q">{E_html}</ol></div>
  <div><h2>C. Put the plot in order (the setting comes first)</h2><ol class="q">{B_html}</ol>
  <h2>D. Which kind of opening? (dialogue, action, mystery)</h2><ol class="q">{C_html}</ol>
  <h2>E. Where is it set?</h2><div class="bank" style="font-size:8.4pt">{" · ".join(PLN[k] for s, k in sorted(D_items, key=lambda x: x[1]))}</div><ol class="q">{D_html}</ol></div></div>
  <h2>F. Exam-style</h2>
  <ol class="q">
   <li value="{nF}">Write a strong first line for a story called <b>"The Missing Key"</b>. Use dialogue, action or mystery.<span class="long"></span></li>
   <li value="{nF + 1}">(1) {EX_LINES[0]} (2) {EX_LINES[1]} (3) {EX_LINES[2]}<br>Write a twist ending (1–2 sentences) that is set up by one of these lines.<span class="long"></span></li>
  </ol>
</div>

<div class="page">
  <div class="band"><div><div class="k">Check your work</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <table class="ans"><tbody>
   <tr><td><b>A</b></td><td>{" · ".join(f"{i}. {PN[k]}" for i, (s, k) in enumerate(A_items, nA))}</td></tr>
   <tr><td><b>B</b></td><td>{" · ".join(f"{nE + 2*j}. {'abcd'[o.index(T['twist'])]}) {T['twist']} &nbsp; {nE + 2*j + 1}. Line {T['clue']}" for j, (T, o) in enumerate(zip(E_items, E_opts)))}</td></tr>
   <tr><td><b>C</b></td><td>{" · ".join(f"{i}. {a}" for i, (S, idx, a) in enumerate(B_items, nB))} (problem → climax → ending)</td></tr>
   <tr><td><b>D</b></td><td>{" · ".join(f"{i}. {ON[hook(h)]}" for i, (x, e, h, k) in enumerate(C_items, nC))}</td></tr>
   <tr><td><b>E</b></td><td>{" · ".join(f"{i}. {PLN[k]} ({clues(s, k)})" for i, (s, k) in enumerate(D_items, nD))}</td></tr>
   <tr><td><b>F</b></td><td>{nF}. Sample: <i>“Has anyone seen my key?” Mam shouted, and the whole house froze.</i> (dialogue)<br>
     {nF + 1}. Sample: <i>{EX_TWIST}</i> (set up by line 3: the torch).</td></tr>
  </tbody></table>
  <h2>Worked examples</h2>
  <div class="two">
   <div class="wk"><b class="h">Naming the part</b><i>"Suddenly, a muddy brown head popped up from behind a rock pool."</i> This is the <b>climax</b>: "Suddenly" signals the big moment, and the problem (the missing dog) is about to be solved.</div>
   <div class="wk"><b class="h">Setting with evidence</b>The story is set at a beach on a summer day. "Gulls screamed overhead" and "our sandcastle" help me hear and see the seaside.</div>
   <div class="wk"><b class="h">Spotting the twist</b>Read the ending, then look back: which line does it reach back to? That line is the planted clue. An ending that reaches back to nothing is not a twist.</div>
   <div class="wk"><b class="h">Writing a twist</b>1. Decide the surprise. 2. Plant one small clue early (an object, a habit, a remark). 3. Distract the reader with a more obvious explanation. 4. Reveal it in one or two sentences.</div>
  </div>
  <div class="note"><b>Got one wrong?</b> Go back to page 1, then play <b>Twist Detector</b> at {GAME}: the "Go back over these" list at the end explains each mistake.</div>
  <p class="small">All sentences and stories written by Léim. Léim is independent and not connected with the State Examinations Commission or the NCCA.</p>
</div>
</body></html>"""

# ---------- teacher pack ----------
random.seed(1112)
JIG = random.sample(D["stories"], 6)
cards = [(S["lines"][j], pi, j) for pi, S in enumerate(JIG) for j in range(4)]
for s, pi, j in cards: assert part(s) == PK[j], (s, parts(s))
assert len({s for s, a, b in cards}) == 24
random.seed(1113); random.shuffle(cards)
jig_html = "".join(f'<div class="c"><span class="tag">Card {k}</span><div class="fc sm">{s}</div></div>' for k, (s, pi, j) in enumerate(cards, 1))
jig_key = "".join(f"<li><b>{S['k'][2:].strip()}</b>: cards {' → '.join(str(next(k for k, (s, a, b) in enumerate(cards, 1) if a == pi and b == j)) for j in range(4))}</li>" for pi, S in enumerate(JIG))

SWAP_A = ("The Haunted Classroom", [
    "It was a dark November evening, and Jamie had stayed late at school to finish a project.",
    "On the way in, he had noticed a mop and bucket outside Room 9.",
    "Then the lights in the corridor went out, and the door of Room 9 was locked.",
    "Suddenly, a low moaning sound came from inside, and the handle began to turn."],
    "It turned out the cleaner had been singing along to her headphones while she mopped.", 1)
SWAP_B = ("The Footprints", [
    "On a frosty January morning, Aoife's dad found huge footprints across the back garden.",
    "Her little brother had asked for giant slippers with claws for his birthday.",
    "The footprints led to the shed, but the shed door was locked from the inside.",
    "All at once, the door creaked open and something with claws stepped out."],
    "It turned out to be her brother, wearing his brand-new monster slippers.", 1)
for name, L, tw, c in (SWAP_A, SWAP_B):
    assert [part(L[0]), part(L[2]), part(L[3])] == ["se", "pr", "cl"], (name, [parts(x) for x in L])
    assert kind(tw, L) == "twist" and linked(tw, L) == [c], (name, linked(tw, L))
def swap_card(who, mine, theirs):
    name, L, tw, c = mine
    return f"""<div class="idc"><h3>Student {who} · Twist Swap</h3>
    <p style="font-size:8.6pt;margin:0 0 1mm"><b>1. Read your story aloud twice</b>, slowly. <b>Stop before the ending.</b> Let your partner guess the ending, then read it out.</p>
    <div class="pass" style="font-size:10pt"><b style="font-style:normal">"{name}"</b><br>{" ".join(L)}<br><b style="font-style:normal">Ending (read it last):</b> {tw}</div>
    <p style="font-size:8.6pt;margin:1mm 0"><b>2. Then listen</b> to "{theirs[0]}" without looking at the text. Fill in the grid:</p>
    <table class="st" style="font-size:8.6pt"><tbody>{"".join(f"<tr><td style='width:34%'><b>{n}</b></td><td></td></tr>" for n in ["Setting: where and when?", "The problem", "The climax", "Your guess for the ending", "The real ending", "The clue that set it up"])}</tbody></table>
    <p style="font-size:8.6pt;margin:1mm 0 0"><b>3. Talk about it:</b> was your guess more obvious? Was the twist fair?</p></div>"""

FIX = [("“This is a story about a boy called Jack who went to the beach.”", "Flat opening. Start with dialogue, action or mystery: <b>Jack ran straight into the waves, still wearing his runners.</b>"),
       ("“We were at the beach. It was nice.”", "Setting told, not shown. Use clue words: <b>Gulls screamed and the wet sand squelched under our feet.</b>"),
       ("A story with eleven characters in two pages.", "Too many characters for a short story. Keep two or three and give each one a job."),
       ("“…and then I woke up. It was all a dream.”", "A cheat ending: nothing was at stake. Plan a real ending and set it up."),
       ("“It turned out the teacher was an alien.” (no clue anywhere)", "An ending from nowhere. Plant a clue early, e.g. <b>Ms Doyle never ate lunch and her eyes glowed in the dark.</b>"),
       ("A whole page of the friends chatting, and nothing goes wrong.", "No problem, so no story. Give the characters something to solve.")]
assert WEAK.search("This is a story about a boy called Jack who went to the beach.") and hook("Jack ran straight into the waves, still wearing his runners.") == "a"
assert places("Gulls screamed and the wet sand squelched under our feet.") == ["be"] and kind("…and then I woke up. It was all a dream.", ["x"]) == "dream"

BUS = ["It was a foggy Friday night in Skibbereen, and Niamh had just missed the last bus home.",
       "Her phone was dead, and the only other person at the stop was an old man in a long grey coat.",
       "He smiled and said, “Don't worry. Someone always comes for the Friday girl.”",
       "Just then, headlights cut through the fog, and a battered red van pulled up beside them.",
       "The driver leaned out, and Niamh gasped.",
       "It was her grandad, who drove the hospital night shift and passed the stop every Friday."]
assert sorted(parts(BUS[0])) == ["pr", "se"] and part(BUS[3]) == "cl"  # line 1 = setting + problem together

pack = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Short Stories Teacher Pack | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{PACK_STYLE}
{EXTRA}
.fym .c{{height:30mm}}.fym .fc.sm{{font-size:9.6pt;line-height:1.28;margin-top:2mm;font-weight:600}}.idc{{padding:2mm 4mm;margin-bottom:3mm}}.idc h3{{margin:0 0 1mm}}
.idc .st td{{height:5mm;padding:1px 6px}}.p1 .proc td{{font-size:8.6pt;padding:2px 6px}}.ops div{{font-size:12pt;padding:5mm 3mm}}.ops b{{font-size:19pt}}
.ws .eh td{{font-size:8.6pt;padding:2px 6px}}.ws .eh .gap{{height:13px}}.ws ol.q li{{margin-bottom:1px}}
</style></head><body>

<div class="page p1">
  <div class="band"><div><div class="k">Junior Cycle English · Teacher pack</div><h1>Short stories</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2015 specification): {LO}</p>
  <div class="two">
    <div><h3>Aims</h3><p>By the end of the lesson students can name the setting, problem, climax and ending of a short story, recognise a strong first line (dialogue, action, mystery), find the clue words that show a setting, and tell a fair twist (set up by a clue) from a cheat ending.</p></div>
    <div><h3>In this pack</h3><p>p.1 Teacher notes · p.2 Story Jigsaw cards (cut-up) · p.3 Twist Swap A/B (speaking + listening) · p.4 Wall poster · p.5 Worksheet: Fix the Story + exam-style questions · p.6 Answers. Level: 1st year (useful for any short story on your course). Time: about 60 minutes. All stories are original.</p></div>
  </div>
  <h2 style="margin-top:8px">Procedure</h2>
  <table class="proc"><tbody>
    <tr><td>5 min</td><td><b>Lead-in.</b> Read three lines: <i>A parcel arrived. It ticked quietly. Grandad had been talking about his broken alarm clock.</i> Give two endings: an alien bomb / a new alarm clock Grandad ordered. Which is the better surprise? Why?</td></tr>
    <tr><td>8 min</td><td><b>Guided discovery.</b> Elicit the four parts (setting, problem, climax, ending) and the signal words for each. Then the three kinds of first line, and the rule for a twist: surprising, but set up by a clue.</td></tr>
    <tr><td>12 min</td><td><b>Story Jigsaw</b> (p.2, groups of 3–4, one set of 24 cards). Rebuild the 6 mini-stories in order: setting, problem, climax, ending. Fast groups: choose one story and write a twist ending for it.</td></tr>
    <tr><td>15 min</td><td><b>Twist Swap</b> (p.3, pairs). A reads the story aloud and stops before the ending; B fills the grid and guesses the ending; A reads the real ending; B finds the clue. Swap.</td></tr>
    <tr><td>15 min</td><td><b>Worksheet</b> (p.5). Fix the Story in pairs, then the exam-style questions on "The Last Bus" alone.</td></tr>
    <tr><td>5 min</td><td><b>Exit ticket.</b> Write a first line and a planted clue for a story called "The Locked Box". Homework: play <b>Twist Detector</b> at {GAME}.</td></tr>
  </tbody></table>
  <div class="note"><b>Errors to look for:</b> retelling the plot instead of naming the part · calling any surprise a twist · "It was all a dream" · naming the setting without quoting clue words · too many characters in students' own stories. <b>Support:</b> the poster (p.4) on the desk; give weaker groups the 6 setting cards of the jigsaw first. <b>Fast finishers:</b> rewrite one jigsaw story with a mystery first line.</div>
  <p class="small"><b>Story Jigsaw key</b> (setting → problem → climax → ending):</p><ul class="small" style="columns:2;margin:0">{jig_key}</ul>
</div>

<div class="page">
  <div class="band"><div><div class="k">Groups of 3–4 · cut up the 24 cards</div><h1>Story Jigsaw</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.4pt;margin:0 0 2mm">The cards make <b>6 mini-stories</b>. Rebuild each one in order: <b>setting → problem → climax → ending</b>. Which words helped you?</p>
  <div class="fym">{jig_html}</div>
</div>

<div class="page">
  <div class="band"><div><div class="k">Pairs · cut along the dashed line</div><h1>Twist Swap A/B</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.4pt">Each story has a setting, a problem, a climax and a twist ending set up by a clue. Can your partner spot the clue just by listening?</p>
  {swap_card("A", SWAP_A, SWAP_B)}
  {swap_card("B", SWAP_B, SWAP_A)}
</div>

<div class="page">
  <div class="poster">
    <h1>Set it up. Pay it off.</h1>
    <div class="ops">
      <div style="background:var(--green-soft)"><b>Setting</b>where and when<br>show it with clue words</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Problem</b>something goes wrong<br>one problem is enough</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Climax</b>the big moment<br>Suddenly · Just then</div>
      <div style="background:var(--green-soft)"><b>Ending</b>plant a clue early<br>pay it off at the end</div>
    </div>
    <p style="text-align:center;font-size:20pt!important;font-weight:800;margin:4mm 0">Not "…and then I woke up."</p>
    <p style="text-align:center;font-size:10pt;color:var(--muted)">Léim · leim.ie · Play Twist Detector: {GAME}</p>
  </div>
</div>

<div class="page ws">
  <div class="band"><div><div class="k">Worksheet · exam-style questions</div><h1>Fix the Story</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Fix the Story</h2>
  <p>Each one has a problem. Say what's wrong and write or describe a better version.</p>
  <table class="eh"><thead><tr><th>What the writer did</th><th>What's wrong and the fix</th></tr></thead><tbody>
  {"".join(f"<tr><td style='font-weight:500'>{s}</td><td><span class='gap'></span><span class='gap'></span></td></tr>" for s, r in FIX)}
  </tbody></table>
  <h2>B. Exam-style questions: "The Last Bus"</h2>
  <div class="pass">{" ".join(BUS)}</div>
  <ol class="q">
    <li>Where and when is the story set? Quote two words or phrases that help you picture it.<span class="long"></span></li>
    <li>What is Niamh's problem?<span class="long"></span></li>
    <li>Which sentence is the climax? Explain your choice.<span class="long"></span></li>
    <li>The old man's words are a clue. What do they set up?<span class="long"></span></li>
    <li>Write a different twist ending for the story, set up by a clue that is already in the text.<span class="long"></span><span class="long"></span></li>
  </ol>
</div>

<div class="page an">
  <div class="band"><div><div class="k">For the teacher</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>Story Jigsaw</h2>
  <ul style="columns:2;margin:0">{jig_key}</ul>
  <h2>Twist Swap</h2>
  {"".join(f"<p><b>{n}:</b> Setting: {L[0].split(', ')[0].replace('It was a ', '').replace('On a ', '')} · Problem: {L[2]} · Climax: {L[3]} · Clue: <i>{L[c]}</i> · Twist: {tw}</p>" for n, L, tw, c in (SWAP_A, SWAP_B))}
  <h2>A. Fix the Story</h2>
  <table><tbody>{"".join(f"<tr><td style='width:40%'>{s}</td><td>{r}</td></tr>" for s, r in FIX)}</tbody></table>
  <h2>B. Exam-style questions</h2>
  <ol class="q">
    <li>A bus stop in Skibbereen on a foggy Friday night. "foggy Friday night", "headlights cut through the fog", "battered red van" (any two).</li>
    <li>She has missed the last bus home, her phone is dead and she is alone at the stop with a stranger.</li>
    <li>"Just then, headlights cut through the fog…": "Just then" signals the big moment, and the problem is about to be solved.</li>
    <li>That someone comes every Friday: the stranger already knows the grandad passes the stop, so the ending makes sense when you look back.</li>
    <li>Credit an ending that follows on, a surprise, and a clue already in the text (the grey coat, "the Friday girl", the dead phone).</li>
  </ol>
  <h2>Marking tip</h2>
  <p>In reading answers, reward a clear point + a short quote + a sentence on its effect. In students' own stories, reward a strong first line, one clear problem and an ending that was planned, more than length. Our guide, not an official marking scheme.</p>
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
<h1><span>Short</span><br><span>stories</span></h1>
<div class="sub">Story Jigsaw cards · Twist Swap A/B<br>Poster · Worksheet + answers</div>
<div class="em">setting · problem · climax<br>first lines · twist endings</div></div>
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
    pdf("teacher-pack", os.path.join(OUT, "Short-Stories-Teacher-Pack-Leim.pdf"))
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--hide-scrollbars", "--window-size=1200,1200",
                    f"--screenshot={os.path.join(OUT, f'{SLUG}-cover.png')}", f"{SLUG}-cover.html"], cwd=SRC, check=True, capture_output=True)
