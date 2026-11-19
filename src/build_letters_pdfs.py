#!/usr/bin/env python3
"""Letters & emails: formal and informal (JC English Order 15): free sheet (-> printables/), 6-page teacher pack + 1200x1200 cover (-> OUTDIR).
Usage: python3 src/build_letters_pdfs.py /tmp/letters
Items come from the game's data block (format-fixer.html). Every answer is re-derived with the checker's own rules
(src/test_format_fixer.py: register, signoff, part, inf) and asserted; the checker's data pass runs first.
Styles are read from src/build_money1_pdfs.py."""
import os, sys, random, subprocess, re
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC); sys.path.insert(0, SRC)
from test_format_fixer import register, signoff, part, inf, load, data_pass, SO
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/letters"; os.makedirs(OUT, exist_ok=True)
SLUG = "letters-emails"
LO = "W4, W12, R13"
GAME = "leim.ie/format-fixer.html"
D = load(os.path.join(ROOT, "format-fixer.html")); assert not data_pass(D), data_pass(D)
SON = {"fa": "Yours faithfully", "si": "Yours sincerely", "in": "Talk soon / Love"}
PN = {"addr": "your address", "date": "the date", "their": "their address", "greet": "greeting", "open": "opening line",
      "body": "body (the main point)", "close": "closing line", "sign": "sign-off", "name": "your full name"}
LETTER = ["addr", "date", "their", "greet", "open", "body", "close", "sign", "name"]
def blk(L, k):
    v = L[k]; return " / ".join(v) if isinstance(v, list) else v

# ---------- free sheet ----------
random.seed(1515)
A_items = random.sample([x for x in D["sort"] if x[1] == "f"], 4) + random.sample([x for x in D["sort"] if x[1] == "i"], 4)
random.shuffle(A_items)
for s, k in A_items: assert register(s) == k
B_items = random.sample([x for x in D["greet"] if x[1] == "fa"], 2) + random.sample([x for x in D["greet"] if x[1] == "si"], 2) + random.sample([x for x in D["greet"] if x[1] == "in"], 2)
random.shuffle(B_items)
for g, k in B_items: assert signoff(g) == k
CL = D["letters"][4]                      # the robotics thank-you letter, parts lettered a-g in a jumbled order
C_keys = ["addr", "date", "their", "greet", "open", "close", "sign"]
for k in LETTER: assert part(blk(CL, k)) == k
C_order = C_keys[:]; random.shuffle(C_order)
LET = "abcdefg"
D_items = random.sample(D["tone"], 4)
for c, a, w in D_items: assert inf(c) and not inf(a)
EL = D["letters"][7]; EM = D["emails"][2]   # E: a letter with no date, an email with no subject line
assert part(EL["date"]) == "date" and part(EM["subj"]) == "subj"
NQ = len(A_items) + len(B_items) + 1 + len(D_items) + 2 + 2; assert NQ == 23, NQ
nA = 1; nB = nA + len(A_items); nC = nB + len(B_items); nD = nC + 1; nE = nD + len(D_items); nF = nE + 2

def style(var):
    return re.search(var + r' = f"""<!doctype.*?<style>(.*?)</style>', open(os.path.join(SRC, "build_money1_pdfs.py"), encoding="utf-8").read(), re.S).group(1).replace("{LO}", LO).replace("{{", "{").replace("}}", "}").replace("JC Maths LOs (2018 spec)", "JC English LOs (2015 spec)")
SHEET_STYLE = style("sheet"); PACK_STYLE = style("pack")
assert "JC English LOs (2015 spec)" in SHEET_STYLE and "Single-teacher licence" in PACK_STYLE and "JC English LOs (2015 spec)" in PACK_STYLE
EXTRA = """.wk{line-height:1.45;border:1.5px solid var(--line);border-radius:8px;padding:2px 7px;margin:3px 0;font-size:9.4pt}.wk b.h{display:block}
table.st{border-collapse:collapse;margin:3px 0;font-size:9.2pt;width:100%}table.st td,table.st th{border:1px solid #C9D1DA;padding:2px 6px;text-align:left}
.bank{border:1.5px solid var(--line);border-radius:8px;padding:4px 10px;margin:4px 0;text-align:center;font-weight:700;word-spacing:4px}
.pass{border-left:4px solid var(--green);background:var(--mist);padding:5px 10px;margin:4px 0;font-style:italic}
.lt{border:1.5px solid #9AA3AE;border-radius:4px;padding:3mm 4mm;font-family:Georgia,'Times New Roman',serif;font-size:9.6pt;line-height:1.35;margin:2mm 0}
.lt .r{text-align:right}.lt div{margin-bottom:1.6mm}.lt .lab{font-family:Inter,sans-serif;font-weight:800;color:var(--green);font-size:9pt;margin-right:2mm}
.lt .em{font-family:Inter,sans-serif;font-size:8.6pt;color:#555;border-bottom:1px solid #C9D1DA;padding-bottom:1mm}"""

def letter_html(L, keys, labels=None, email=False):
    h = '<div class="lt">'
    for k in keys:
        v = L[k]; t = "<br>".join(v) if isinstance(v, list) else v
        if email and k == "to": t = "To: " + t
        lab = f'<span class="lab">({labels[k]})</span>' if labels and k in labels else ""
        cls = ' class="r"' if k in ("addr", "date") else ' class="em"' if k in ("to", "subj") else ""
        h += f"<div{cls}>{lab}{t}</div>"
    return h + "</div>"

A_html = "".join(f"<li value='{i}'><i>{s}</i> &nbsp; <b>Formal / Informal</b></li>" for i, (s, k) in enumerate(A_items, nA))
B_html = "".join(f"<li value='{i}'><i>{g}</i> <span class='line' style='min-width:30mm'></span></li>" for i, (g, k) in enumerate(B_items, nB))
C_labels = {k: LET[i] for i, k in enumerate(C_order)}
C_html = letter_html(CL, LETTER, C_labels)
D_html = "".join(f"<li value='{i}'><i>{c}</i><span class='long'></span></li>" for i, (c, a, w) in enumerate(D_items, nD))
EL_keys = [k for k in LETTER if k != "date"]; EM_keys = [k for k in ["to", "subj", "greet", "open", "body", "close", "sign", "name"] if k != "subj"]
for b in [blk(EL, k) for k in EL_keys]: assert part(b) != "date"
E1 = letter_html(EL, ["addr", "their", "greet"]) ; E2 = letter_html(EM, ["to", "greet", "open"], email=True)
assert "date" not in [part(blk(EL, k)) for k in ["addr", "their", "greet"]]

sheet = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Letters and emails, rules and practice | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{SHEET_STYLE}
{EXTRA}
.p2 ol.q li{{margin-bottom:1px;font-size:9pt}}.p2 h2{{margin:4px 0 2px}}.p2 .two{{gap:5mm}}.p2 .lt{{font-size:8.6pt;padding:2mm 3mm;margin:1mm 0}}.p2 .lt div{{margin-bottom:0.8mm}}
</style></head><body>
<div class="page tight">
  <div class="band"><div><div class="k">Junior Cycle English · Free revision sheet</div><h1>Letters and emails</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2015 specification): {LO}. Play the game: <b>{GAME}</b></p>
  <div class="two">
   <div><h2>1. The layout of a formal letter</h2>
    <div class="lt"><div class="r"><span class="lab">your address</span>27 Oak Park<br>Tralee<br>Co. Kerry</div><div class="r"><span class="lab">date</span>4 January 2026</div>
    <div><span class="lab">their address</span>The Secretary<br>Lakeside Youth Orchestra<br>Killarney<br>Co. Kerry</div><div><span class="lab">greeting</span>Dear Sir/Madam,</div>
    <div><span class="lab">opening line</span>I am writing to ask about joining your orchestra.</div><div>… one point per paragraph …</div>
    <div><span class="lab">closing line</span>I look forward to your reply.</div><div><span class="lab">sign-off</span>Yours faithfully,<br>Oisín Quinn</div></div>
    <p style="font-size:9pt">Your address has <b>no name</b> in it. Your <b>full name</b> goes under the sign-off.</p></div>
   <div><h2>2. Faithfully or sincerely?</h2>
    <table class="st"><thead><tr><th>Greeting</th><th>Sign-off</th></tr></thead><tbody>
     <tr><td>Dear Sir/Madam, (no name)</td><td><b>Yours faithfully,</b></td></tr>
     <tr><td>Dear Ms Kelly, (a name)</td><td><b>Yours sincerely,</b></td></tr>
     <tr><td>Hi Aoife, / Dear Gran, (a friend)</td><td>Talk soon, / Love,</td></tr></tbody></table>
    <div class="wk"><b>Memory trick:</b> <b>S</b>ir and <b>s</b>incerely never go together. Capital Y, small f or s, then a comma.</div>
    <h2>3. Formal or informal?</h2>
    <table class="st"><thead><tr><th>Formal</th><th>Informal</th></tr></thead><tbody>
     <tr><td>I am, I cannot, I would like</td><td>I'm, can't, I'd love</td></tr>
     <tr><td>I am writing to…</td><td>Guess what!</td></tr>
     <tr><td>I would be grateful if…</td><td>Thanks a mil!</td></tr>
     <tr><td>no slang, no "!!", no emoji</td><td>slang is fine with friends</td></tr></tbody></table>
    <h2>4. Emails</h2>
    <div class="wk">A short <b>subject line</b> (Subject: Lost jacket on the 8:15 bus). Then greeting, opening line, paragraphs, closing line, sign-off and full name, just like a letter. No addresses or date needed.</div>
    <div class="note"><b>Classic mistakes:</b> "Hi Manager" · Dear Sir/Madam with Yours sincerely · "Yours Sincerely" with a capital S · your name in your address · one "gonna" in a formal letter · no reason for writing in the first line.</div></div>
  </div>
  <div class="tip"><b>Exam tip:</b> read the question twice. <b>Who</b> are you writing to and <b>why</b>? That decides formal or informal, the layout and the sign-off. Then give one idea per paragraph.</div>
</div>

<div class="page p2">
  <div class="band"><div><div class="k">Practice · {NQ} questions</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <div class="two"><div><h2>A. Formal or informal? Circle one</h2><ol class="q">{A_html}</ol>
  <h2>B. Write the sign-off for each greeting</h2><ol class="q">{B_html}</ol></div>
  <div><h2>C. Name the parts a–g of this letter <span style="font-weight:500">(question {nC})</span></h2>{C_html}
  <p style="font-size:8.6pt;margin:0">a <span class="line" style="min-width:16mm"></span> b <span class="line" style="min-width:16mm"></span> c <span class="line" style="min-width:16mm"></span> d <span class="line" style="min-width:16mm"></span><br>e <span class="line" style="min-width:16mm"></span> f <span class="line" style="min-width:16mm"></span> g <span class="line" style="min-width:16mm"></span></p></div></div>
  <h2>D. Make it formal: rewrite each line</h2><ol class="q">{D_html}</ol>
  <h2>E. What's missing? Write the missing part</h2>
  <div class="two"><div><ol class="q"><li value="{nE}">The start of a letter:{E1}<span class="long"></span></li></ol></div>
  <div><ol class="q"><li value="{nE + 1}">The start of an email:{E2}<span class="long"></span></li></ol></div></div>
</div>

<div class="page">
  <div class="band"><div><div class="k">Exam-style + answers</div><h1>Have a go</h1></div><div class="logo">↗ Léim</div></div>
  <h2>F. Exam-style</h2>
  <ol class="q">
   <li value="{nF}">Your sports club wants a new minibus. Write the <b>greeting, opening line, closing line and sign-off</b> of a letter to <b>Ms Doyle</b>, the manager of a local business, asking her to sponsor it.<span class="long"></span><span class="long"></span><span class="long"></span></li>
   <li value="{nF + 1}">Write a short <b>informal</b> email to a friend telling them about the minibus. Name <b>two</b> things that make it informal.<span class="long"></span><span class="long"></span><span class="long"></span></li>
  </ol>
  <h2>Answers</h2>
  <table class="ans"><tbody>
   <tr><td><b>A</b></td><td>{" · ".join(f"{i}. {'Formal' if register(s) == 'f' else 'Informal'}" for i, (s, k) in enumerate(A_items, nA))}</td></tr>
   <tr><td><b>B</b></td><td>{" · ".join(f"{i}. {SON[signoff(g)]}" for i, (g, k) in enumerate(B_items, nB))}</td></tr>
   <tr><td><b>C</b></td><td>{nC}. {" · ".join(f"{LET[i]} {PN[part(blk(CL, k))]}" for i, k in enumerate(C_order))}</td></tr>
   <tr><td><b>D</b></td><td>{"<br>".join(f"{i}. {a}" for i, (c, a, w) in enumerate(D_items, nD))}<br>(Other formal versions are fine: full words, no slang, polite.)</td></tr>
   <tr><td><b>E</b></td><td>{nE}. The <b>date</b>, under the address on the right ({EL['date']}). · {nE + 1}. The <b>subject line</b> (e.g. {EM['subj']}).</td></tr>
   <tr><td><b>F</b></td><td>{nF}. Sample: <i>Dear Ms Doyle,</i> / <i>I am writing to ask if your business would sponsor a new minibus for Ballyduff Athletics Club.</i> / <i>I look forward to hearing from you.</i> / <i>Yours sincerely,</i> + full name (a name was used, so sincerely).<br>
     {nF + 1}. Sample: <i>Hi Sam, Guess what? We're getting a new minibus for the club! No more squashing into Dad's car. Talk soon, Cian.</i> Informal: short forms (We're), a chatty greeting and sign-off, "!".</td></tr>
  </tbody></table>
  <div class="note"><b>Got one wrong?</b> Go back to page 1, then play <b>Format Fixer</b> at {GAME}: the "Go back over these" list at the end explains each mistake.</div>
  <p class="small">All letters, emails and sentences written by Léim; names, businesses and addresses are made up. Léim is independent and not connected with the State Examinations Commission or the NCCA.</p>
</div>
</body></html>"""
assert signoff("Dear Ms Doyle,") == "si" and not inf("I am writing to ask if your business would sponsor a new minibus for Ballyduff Athletics Club.")
assert inf("Guess what? We're getting a new minibus for the club!")

# ---------- teacher pack ----------
JIG_L = [D["letters"][0], D["letters"][1], D["letters"][5]]
JIG = []
for n, L in enumerate(JIG_L, 1):
    for k in ["addr", "date", "their", "greet", "open", "body", "close", "sign"]:
        t = "<br>".join(L[k]) if isinstance(L[k], list) else L[k]
        if k == "sign": t += "<br>" + L["name"]; assert part(L["name"]) == "name"
        assert part(blk(L, k)) == k
        JIG.append((n, k, t))
assert len(JIG) == 24
order = list(range(24)); random.seed(1516); random.shuffle(order)
JIG_S = [JIG[i] for i in order]
jig_html = "".join(f'<div class="c"><span class="tag">Card {i}</span><div class="fc sm">{t}</div></div>' for i, (n, k, t) in enumerate(JIG_S, 1))
jig_key = "<br>".join(f"<b>Letter {n}</b> ({JIG_L[n-1]['their'][0]}): " + " → ".join(str(JIG_S.index(x) + 1) for x in JIG if x[0] == n) for n in (1, 2, 3))

TA = D["tone"][0:6]; TB = D["tone"][6:12]
for c, a, w in TA + TB: assert inf(c) and not inf(a)
def swap_card(who, mine, theirs, seed):
    ans = [a for c, a, w in theirs]; random.seed(seed); random.shuffle(ans)
    return f"""<div class="idc"><h3>Student {who} · Register Swap</h3>
    <p style="font-size:8.8pt;margin:0 0 1mm"><b>1. Read out</b> your casual lines one at a time. Your partner finds the formal version on their card and reads it back. Tick it if it matches.</p>
    <table class="st" style="font-size:9pt"><tbody>{"".join(f"<tr><td style='width:6%'><b>{i}</b></td><td>{c}</td><td style='width:8%'>☐</td></tr>" for i, (c, a, w) in enumerate(mine, 1))}</tbody></table>
    <p style="font-size:8.8pt;margin:1mm 0"><b>2. Listen</b> to your partner's casual lines. Find the formal version below and read it out. Write their line number in the box.</p>
    <table class="st" style="font-size:9pt"><tbody>{"".join(f"<tr><td>{a}</td><td style='width:10%'></td></tr>" for a in ans)}</tbody></table>
    <p style="font-size:8.8pt;margin:1mm 0 0"><b>3. Together:</b> circle the words that made each casual line too casual.</p></div>"""

FIX = [("Hi Manager,", "Too casual for a stranger: <b>Dear Sir/Madam,</b>"),
       ("Dear Sir/Madam, … Yours sincerely,", "No name in the greeting: <b>Yours faithfully,</b>"),
       ("Yours Faithfully,", "Small f: <b>Yours faithfully,</b>"),
       ("Aoife Murphy, 12 Main Street, Bandon (top right)", "No name in your address: put <b>Aoife Murphy</b> under the sign-off."),
       ("I'm writing cos the boots are wrecked!!", "Informal: <b>I am writing to complain about the boots, which are badly damaged.</b>"),
       ("Subject: hi", "Says nothing: <b>Subject: Damaged football boots, order 2215</b>")]
assert signoff("Dear Sir/Madam,") == "fa" and inf("Hi Manager,") and inf("I'm writing cos the boots are wrecked!!") and not inf("I am writing to complain about the boots, which are badly damaged.")

LIB = {"addr": ["14 Mill Road", "Clonakilty", "Co. Cork"], "date": "6 October 2026", "their": ["The Librarian", "Clonakilty Library", "Clonakilty", "Co. Cork"],
       "greet": "Dear Sir/Madam,", "open": "I am writing to ask if the library could open later on weekday evenings.",
       "body": "At the moment it closes at five o'clock, which is before most students get home from sports training. A quiet place to study until seven would help many of us, especially in exam years.",
       "close": "I would be grateful if you could consider this request.", "sign": "Yours faithfully,", "name": "Ruth Barry"}
for k in ["addr", "date", "greet", "open", "close", "sign", "name"]: assert part(blk(LIB, k)) == k, k
assert not any(inf(blk(LIB, k)) for k in LIB if k != "name") and SO[signoff(LIB["greet"])] == LIB["sign"]
lib_html = letter_html(LIB, LETTER)

pack = f"""<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Letters and Emails Teacher Pack | Léim</title>
<link rel="stylesheet" href="pdf.css"><style>{PACK_STYLE}
{EXTRA}
.fym .c{{height:30mm}}.fym .fc.sm{{font-size:8.8pt;line-height:1.25;margin-top:2mm;font-weight:500;font-family:Georgia,'Times New Roman',serif}}.idc{{padding:2mm 4mm;margin-bottom:3mm}}.idc h3{{margin:0 0 1mm}}
.idc .st td{{padding:1px 6px}}.p1 .proc td{{font-size:8.6pt;padding:2px 6px}}.ops div{{font-size:12pt;padding:5mm 3mm}}.ops b{{font-size:19pt}}
.ws .eh td{{font-size:8.6pt;padding:2px 6px}}.ws .eh .gap{{height:13px}}.ws ol.q li{{margin-bottom:1px}}.ws .lt{{font-size:8.8pt;padding:2mm 4mm}}.ws .lt div{{margin-bottom:1mm}}
</style></head><body>

<div class="page p1">
  <div class="band"><div><div class="k">Junior Cycle English · Teacher pack</div><h1>Letters and emails</h1></div><div class="logo">↗ Léim</div></div>
  <p class="lo">Learning outcomes (2015 specification): {LO}</p>
  <div class="two">
    <div><h3>Aims</h3><p>By the end of the lesson students can lay out a formal letter and email correctly, match the sign-off to the greeting (faithfully / sincerely), tell formal from informal language, and rewrite casual sentences in a formal register for a reader they don't know.</p></div>
    <div><h3>In this pack</h3><p>p.1 Teacher notes · p.2 Letter Jigsaw cards (cut-up) · p.3 Register Swap A/B (speaking) · p.4 Wall poster · p.5 Worksheet: Fix the Letter + exam-style questions · p.6 Answers. Level: 2nd year. Time: about 60 minutes. All letters are original; names and businesses are made up.</p></div>
  </div>
  <h2 style="margin-top:8px">Procedure</h2>
  <table class="proc"><tbody>
    <tr><td>5 min</td><td><b>Lead-in.</b> Write <i>“Hey, gimme my money back asap!”</i> on the board. Who could you send this to? Who couldn't you? Why not? Elicit "register": how formal you are depends on your reader.</td></tr>
    <tr><td>8 min</td><td><b>Guided discovery.</b> Show a note to Gran and a letter to a manager from the same writer (the game's "Spot the pattern"). Students list the differences: their address, Dear Sir/Madam, the reason in line 1, Yours faithfully, full name. Elicit the faithfully / sincerely rule.</td></tr>
    <tr><td>12 min</td><td><b>Letter Jigsaw</b> (p.2, groups of 3, one set of 24 cards). Sort the cards into three letters, then lay each letter out on the desk as it would look on the page (addresses and date in the right places). First group to check against the key wins.</td></tr>
    <tr><td>12 min</td><td><b>Register Swap</b> (p.3, pairs). A reads a casual line; B finds and reads the formal version; then swap. Together they circle the words that made each line casual.</td></tr>
    <tr><td>18 min</td><td><b>Worksheet</b> (p.5). Fix the Letter in pairs, then the exam-style questions on "Library Hours" alone.</td></tr>
    <tr><td>5 min</td><td><b>Exit ticket.</b> Write the greeting and sign-off for a letter to (1) the Principal, Mr Hayes, (2) The Manager of a cinema, (3) your cousin. Homework: play <b>Format Fixer</b> at {GAME}.</td></tr>
  </tbody></table>
  <div class="note"><b>Errors to look for:</b> Dear Sir/Madam + Yours sincerely · capital F or S in faithfully / sincerely · the writer's name in their address · "Hi" or "Hey" in a formal letter · short forms (I'm, can't) and "!!" in a formal letter · no reason for writing in the first line · an email with no subject line. <b>Support:</b> the poster (p.4) on the desk. <b>Fast finishers:</b> write a reply from the manager to Letter 1.</div>
</div>

<div class="page">
  <div class="band"><div><div class="k">Groups of 3 · cut up the 24 cards</div><h1>Letter Jigsaw</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.4pt;margin:0 0 2mm">Three formal letters have been mixed up. Sort the cards into <b>three letters</b> (8 cards each), then lay each one out as it would look on the page: your address and the date on the right, everything else on the left.</p>
  <div class="fym">{jig_html}</div>
</div>

<div class="page">
  <div class="band"><div><div class="k">Pairs · cut along the dashed line</div><h1>Register Swap A/B</h1></div><div class="logo">↗ Léim</div></div>
  <p style="font-size:9.4pt">Every casual line has a formal twin on your partner's card. Can you find it by listening?</p>
  {swap_card("A", TA, TB, 1517)}
  {swap_card("B", TB, TA, 1518)}
</div>

<div class="page">
  <div class="poster">
    <h1>Who am I writing to?</h1>
    <div class="ops">
      <div style="background:var(--green-soft)"><b>No name</b>Dear Sir/Madam,<br>→ Yours faithfully,</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>A name</b>Dear Ms Kelly,<br>→ Yours sincerely,</div>
      <div style="background:var(--cream);border:2px solid var(--cream-line)"><b>Formal</b>I am · I would like<br>no slang · no "!!"</div>
      <div style="background:var(--green-soft)"><b>Layout</b>your address + date top right<br>their address on the left</div>
    </div>
    <p style="text-align:center;font-size:20pt!important;font-weight:800;margin:4mm 0">Sir and sincerely never go together.</p>
    <p style="text-align:center;font-size:10pt;color:var(--muted)">Léim · leim.ie · Play Format Fixer: {GAME}</p>
  </div>
</div>

<div class="page ws">
  <div class="band"><div><div class="k">Worksheet · exam-style questions</div><h1>Fix the Letter</h1></div><div class="logo">↗ Léim</div></div>
  <h2>A. Fix the Letter</h2>
  <p>Each one is from a formal letter or email. Say what's wrong and write the fix.</p>
  <table class="eh"><thead><tr><th>In the letter</th><th>What's wrong and the fix</th></tr></thead><tbody>
  {"".join(f"<tr><td style='font-weight:500'>{s}</td><td><span class='gap'></span><span class='gap'></span></td></tr>" for s, r in FIX)}
  </tbody></table>
  <h2>B. Exam-style questions: "Library Hours"</h2>
  {lib_html}
  <ol class="q">
    <li>Who is Ruth writing to, and why? Use the opening line.<span class="long"></span></li>
    <li>Is the letter formal or informal? Give <b>two</b> features that show it.<span class="long"></span></li>
    <li>Why does Ruth sign off “Yours faithfully” and not “Yours sincerely”?<span class="long"></span></li>
    <li>Give <b>one</b> reason Ruth uses to persuade the library.<span class="long"></span></li>
    <li>Write a short <b>informal</b> email to a friend asking them to sign Ruth's petition. Then name <b>two</b> differences from Ruth's letter.<span class="long"></span><span class="long"></span></li>
  </ol>
</div>

<div class="page an">
  <div class="band"><div><div class="k">For the teacher</div><h1>Answers</h1></div><div class="logo">↗ Léim</div></div>
  <h2>Letter Jigsaw (cards in order: your address, date, their address, greeting, opening, body, closing, sign-off)</h2>
  <p>{jig_key}</p>
  <p>The two “Dear Sir/Madam,” cards and the dates can be swapped between letters; accept any sensible match. Letters 1 and 3 use Dear Sir/Madam, so <i>Yours faithfully</i>; Letter 2 is to Ms Kelly, so <i>Yours sincerely</i>.</p>
  <h2>Register Swap</h2>
  <table class="st"><tbody>{"".join(f"<tr><td style='width:48%'><b>{w} {i}</b> {c}</td><td>{a}</td></tr>" for w, L in (("A", TA), ("B", TB)) for i, (c, a, x) in enumerate(L, 1))}</tbody></table>
  <h2>A. Fix the Letter</h2>
  <table><tbody>{"".join(f"<tr><td style='width:40%'>{s}</td><td>{r}</td></tr>" for s, r in FIX)}</tbody></table>
  <h2>B. Exam-style questions</h2>
  <ol class="q">
    <li>The librarian at Clonakilty Library, to ask if the library could open later on weekday evenings.</li>
    <li>Formal: Dear Sir/Madam / Yours faithfully; full words ("I am writing"); polite request ("I would be grateful"); both addresses and the date; no slang.</li>
    <li>She did not use a name in the greeting (Dear Sir/Madam), so the sign-off is Yours faithfully.</li>
    <li>It closes at five, before students get home from training; a quiet place to study would help, especially in exam years.</li>
    <li>Credit a friendly greeting and sign-off, short forms or chatty words, a clear request. Differences: no addresses or date; first names; informal words.</li>
  </ol>
  <h2>Marking tip</h2>
  <p>Reward the right register for the reader first, then layout and sign-off, then a clear purpose in the first line and one point per paragraph. Our guide, not an official marking scheme.</p>
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
<h1><span>Letters &amp;</span><br><span>emails</span></h1>
<div class="sub">Letter Jigsaw cards · Register Swap A/B<br>Poster · Worksheet + answers</div>
<div class="em">layout · faithfully or sincerely<br>formal or informal</div></div>
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
    pdf("teacher-pack", os.path.join(OUT, "Letters-Emails-Teacher-Pack-Leim.pdf"))
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--hide-scrollbars", "--window-size=1200,1200",
                    f"--screenshot={os.path.join(OUT, f'{SLUG}-cover.png')}", f"{SLUG}-cover.html"], cwd=SRC, check=True, capture_output=True)
