#!/usr/bin/env python3
"""Builds the topic checklists (job B1b).
Run from the repo root:  python3 src/build_checklists.py
Makes: junior-cycle-<subject>-checklist.html (web page, ticks saved in localStorage)
       src/<subject>-topic-checklist.html  -> printables/junior-cycle-<subject>-topic-checklist.pdf
Data: src/checklist_data.py (update it when a topic goes live, then re-run)."""
import html, re, subprocess, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from checklist_data import SPANISH, MATHS, ENGLISH

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPL = open(os.path.join(ROOT, "junior-cycle-spanish.html"), encoding="utf-8").read()
HEAD = TPL[:TPL.index('<main id="main">')]
FOOT = TPL[TPL.index("</main>"):]
e = html.escape

def _came(subject, i):
    # "Came up in" line from src/came_up_data.py (facts only: year + question numbers)
    import came_up_data as D
    line = D.came_line(subject, i)
    if not line or line.startswith("every") or line.startswith("the writing") or line.startswith("Q17"):
        return line or ""
    return line + " (" + D.KEYS[subject].replace(" level question", "").rstrip(".") + ")"

def norm(rows, subject):
    out = []
    for i, r in enumerate(rows, 1):
        if subject == "spanish":
            yr, term, title, lo17, lo25, game, url, sheet = r
            lo = f"2017 spec: {lo17} · 2025 spec: {lo25}"
            lo_short = f"{lo17} / {lo25}"
        else:
            yr, term, title, lo, game, url, sheet = r
            lo_short = lo
        out.append(dict(n=i, year=yr, term=term, title=title, lo=lo, lo_short=lo_short, game=game,
                        url=url, sheet=f"printables/{sheet}-rules-and-practice.pdf" if sheet and url else "", came=_came(subject, i)))
    return out

SUBJ = {
  "spanish": dict(name="Spanish", page="junior-cycle-spanish.html", rows=norm(SPANISH, "spanish"),
                  lo_note="Learning outcome codes: 2017 specification (2nd and 3rd years, exams 2027–2028) / 2025 specification (1st years from September 2026)."),
  "maths": dict(name="Maths", page="junior-cycle-maths.html", rows=norm(MATHS, "maths"),
                lo_note="Learning outcome codes from the 2018 Junior Cycle Mathematics specification (U = Unifying, N = Number, GT = Geometry & trigonometry, AF = Algebra & functions, SP = Statistics & probability)."),
  "english": dict(name="English", page="junior-cycle-english.html", rows=norm(ENGLISH, "english"),
                  lo_note="Learning outcome codes from the Junior Cycle English specification (2015): OL = Oral language, R = Reading, W = Writing. The two CBA rows are Classroom-Based Assessments done in class, not topics in the June exam."),
}

CSS = """<style>
.ck-intro{display:flex;flex-wrap:wrap;gap:14px;align-items:center;justify-content:space-between;margin-bottom:22px}
.ck-key{display:flex;flex-wrap:wrap;gap:8px 16px;font-size:14px;color:var(--muted)}
.ck-year{margin:36px 0 10px;display:flex;flex-wrap:wrap;align-items:baseline;justify-content:space-between;gap:8px}
.ck-year h2{font-size:28px}
.ck-prog{height:12px;background:#fff;border:1px solid var(--line);border-radius:99px;overflow:hidden;margin-bottom:16px}
.ck-prog i{display:block;height:100%;width:0;background:var(--green);transition:width .3s}
.ck-pct{font-weight:700;color:var(--green)}
.ck-term{font-size:12px;font-weight:700;letter-spacing:.6px;text-transform:uppercase;color:var(--muted);margin:18px 0 8px}
.ck{background:#fff;border:1px solid var(--line);border-radius:12px;padding:14px 16px;margin-bottom:10px;display:grid;grid-template-columns:1fr auto;gap:10px 16px;align-items:center}
.ck.done{border-color:var(--green);box-shadow:inset 4px 0 0 var(--green)}
.ck h3{font-size:17px;font-weight:700;letter-spacing:-.01em}
.ck h3 a{color:var(--ink);text-decoration:none}.ck h3 a:hover{color:var(--green);text-decoration:underline}
.ck .num{color:var(--green);font-weight:800;margin-right:6px}
.ck .meta{font-size:13px;color:var(--muted);margin-top:3px}
.ck .soon{display:inline-block;font-size:11px;font-weight:700;letter-spacing:.5px;text-transform:uppercase;background:var(--mist);color:var(--muted);border-radius:99px;padding:3px 9px;margin-left:6px;vertical-align:2px}
.ck .came{font-size:13px;margin-top:3px}
.ck .ticks{display:flex;flex-wrap:wrap;gap:6px 14px;grid-column:1/-1}
.ck .ticks label{display:flex;gap:7px;align-items:center;font-size:14px;cursor:pointer}
.ck .ticks input{width:20px;height:20px;accent-color:var(--green)}
.ck .ticks input:disabled+span{color:#9CA3AF}
.rag{display:flex;gap:6px;align-items:center;font-size:13px;color:var(--muted)}
.rag button{font:inherit;font-size:13px;font-weight:700;border:2px solid var(--line);background:#fff;border-radius:99px;padding:5px 11px;cursor:pointer;color:var(--ink)}
.rag button[aria-pressed=true].r{background:#FBE9E8;border-color:#D9534F}
.rag button[aria-pressed=true].a{background:#FFF1C9;border-color:#E0A800}
.rag button[aria-pressed=true].g{background:var(--green-soft);border-color:var(--green)}
@media (max-width:560px){.ck{grid-template-columns:1fr}.rag{flex-wrap:wrap}}
</style>
"""

def page(key):
    s = SUBJ[key]; rows = s["rows"]; name = s["name"]
    live = sum(1 for r in rows if r["url"])
    h = HEAD
    h = re.sub(r"<title>.*?</title>", f"<title>My Junior Cycle {name} topic checklist | Léim</title>", h)
    h = re.sub(r'<meta name="description" content=".*?">',
               f'<meta name="description" content="Every Junior Cycle {name} topic in teaching order, 1st to 3rd year, with learning outcome codes. Tick off the game, the rules and the revision sheet, and rate how confident you feel. Free, no login.">', h)
    h = h.replace(' aria-current="page"', "").replace("</head>", CSS + "</head>")
    h = h.replace('<a href="subjects.html">Subjects</a>', '<a href="subjects.html" aria-current="page">Subjects</a>', 1)  # new tab bar (15 Nov): subject pages highlight "Subjects"
    out = [h, '<main id="main">\n']
    out.append(f'''<section class="hero"><div class="wrap" style="padding-bottom:56px">
  <div class="hero-copy">
    <span class="pill">Junior Cycle {name} · Free checklist</span>
    <h1>My {name} <span class="hl">topic checklist</span></h1>
    <p class="lede">Every topic on the Junior Cycle {name} course, 1st year to 3rd year, in the order most schools teach it. Tick off each step, rate how confident you feel, and see what's left before the exam.</p>
    <div class="hero-actions"><a class="btn" href="#y1">Start ticking</a><a class="btn ghost" href="printables/junior-cycle-{key}-topic-checklist.pdf" target="_blank" rel="noopener">Print it (PDF)</a></div>
  </div>
</div></section>
<section class="block mist"><div class="wrap">
  <div class="ck-intro">
    <div class="ck-key"><span>For each topic: ☐ <b>Played the game</b> · ☐ <b>Read the rules</b> · ☐ <b>Did the revision sheet</b></span><span>How confident? <b style="color:#B42318">Red</b> = not yet · <b style="color:#9A6B00">Amber</b> = getting there · <b style="color:var(--green)">Green</b> = got it</span></div>
  </div>
  <div class="note"><b>Your ticks stay on this phone or computer.</b> There's no login, so nothing is sent to us. If you switch device or clear your browser, the ticks start again. Want a paper copy for the fridge or school folder? <a href="printables/junior-cycle-{key}-topic-checklist.pdf" target="_blank" rel="noopener">Print the checklist</a>.</div>
  <p style="margin-top:14px;color:var(--muted);font-size:15px">{live} of {len(rows)} topics are live. Topics marked <b>coming soon</b> are on the way, so this list doubles as our plan. {e(s["lo_note"])}</p>
''')
    yi = 0
    for yr in ["1st year", "2nd year", "3rd year"]:
        yi += 1
        yrows = [r for r in rows if r["year"].startswith(yr[:3])]
        out.append(f'<div class="ck-year" id="y{yi}" style="scroll-margin-top:90px"><h2>{yr}</h2><span class="ck-pct" data-pct="y{yi}">0% done</span></div><div class="ck-prog"><i data-bar="y{yi}"></i></div>\n')
        term = None
        for r in yrows:
            if r["term"] != term:
                term = r["term"]; out.append(f'<div class="ck-term">{e(term)}</div>\n')
            t = e(r["title"])
            title = f'<a href="{r["url"]}">{t}</a>' if r["url"] else f'{t}<span class="soon">Coming soon</span>'
            lab = "CBA guide" if r["game"] == "CBA guide" else "Game"
            game = (f'{lab}: <a href="{r["url"]}">{e(r["game"])}</a>' if r["url"] else f'{lab}: {e(r["game"])}') if lab == "Game" else ('<a href="%s">Free CBA guide</a>' % r["url"] if r["url"] else "Free CBA guide")
            sheet = f' · <a href="{r["sheet"]}" target="_blank" rel="noopener">Revision sheet (PDF)</a>' if r["sheet"] else ""
            dis = "" if r["url"] else " disabled"
            came = f'<div class="came">Came up in: {e(r["came"])}</div>' if r["came"] else ""
            out.append(f'''<div class="ck" data-id="{r["n"]}" data-y="y{yi}">
  <div><h3><span class="num">{r["n"]}</span>{title}</h3><div class="meta">LO {e(r["lo_short"])} · {game}{sheet}</div>{came}</div>
  <div class="rag" role="group" aria-label="How confident are you?"><span>Confident?</span><button type="button" class="r" data-v="r" aria-pressed="false">Red</button><button type="button" class="a" data-v="a" aria-pressed="false">Amber</button><button type="button" class="g" data-v="g" aria-pressed="false">Green</button></div>
  <div class="ticks"><label><input type="checkbox" data-k="game"{dis}><span>Played the game</span></label><label><input type="checkbox" data-k="rules"{dis}><span>Read the rules</span></label><label><input type="checkbox" data-k="sheet"{dis}><span>Did the revision sheet</span></label></div>
</div>
''')
    out.append(f'''<div class="actions" style="display:flex;gap:10px;flex-wrap:wrap;margin-top:28px"><a class="btn" href="{s["page"]}">Back to Junior Cycle {name}</a><button class="btn ghost" type="button" id="ckReset" style="color:var(--ink);border-color:var(--line)">Clear all my ticks</button></div>
</div></section>
''')
    out.append(f'''<script>
(function(){{
  var KEY="leim-checklist-{key}-v1",st={{}};
  try{{st=JSON.parse(localStorage.getItem(KEY)||"{{}}")||{{}};}}catch(x){{st={{}};}}
  function save(){{try{{localStorage.setItem(KEY,JSON.stringify(st));}}catch(x){{}}}}
  var cards=[].slice.call(document.querySelectorAll(".ck"));
  function refresh(){{
    var tot={{}},done={{}};
    cards.forEach(function(c){{
      var s=st[c.dataset.id]||{{}},y=c.dataset.y,n=0;
      [].forEach.call(c.querySelectorAll("input"),function(i){{i.checked=!!s[i.dataset.k];if(i.checked)n++;}});
      [].forEach.call(c.querySelectorAll(".rag button"),function(b){{b.setAttribute("aria-pressed",s.c===b.dataset.v?"true":"false");}});
      c.classList.toggle("done",n===3);
      tot[y]=(tot[y]||0)+3;done[y]=(done[y]||0)+n;
    }});
    Object.keys(tot).forEach(function(y){{
      var p=Math.round(100*done[y]/tot[y]);
      document.querySelector('[data-bar="'+y+'"]').style.width=p+"%";
      document.querySelector('[data-pct="'+y+'"]').textContent=p+"% done";
    }});
  }}
  cards.forEach(function(c){{
    var id=c.dataset.id;
    [].forEach.call(c.querySelectorAll("input"),function(i){{i.onchange=function(){{st[id]=st[id]||{{}};st[id][i.dataset.k]=i.checked;save();refresh();}};}});
    [].forEach.call(c.querySelectorAll(".rag button"),function(b){{b.onclick=function(){{st[id]=st[id]||{{}};st[id].c=(st[id].c===b.dataset.v)?"":b.dataset.v;save();refresh();}};}});
  }});
  document.getElementById("ckReset").onclick=function(){{if(window.confirm("Clear all your ticks and colours on this device?")){{st={{}};save();refresh();}}}};
  refresh();
}})();
</script>
''')
    out.append(FOOT.replace("</main>", "</main>", 1))
    return "".join(out)

PDF_CSS = """<style>
@page{margin:12mm 13mm 14mm;@bottom-left{content:var(--foot)}}
body{font-size:8.6pt;line-height:1.3}
.band{padding:10px 14px;margin-bottom:6px}
.band h1{font-size:17pt}
.how{display:flex;justify-content:space-between;gap:10px;font-size:8pt;color:var(--muted);margin:2px 0 6px}
h2{font-size:11.5pt;margin:8px 0 3px;color:var(--green)}
table{margin:0 0 2px}
th{font-size:7.4pt;padding:3px 5px;text-transform:uppercase;letter-spacing:.04em}
td{padding:3.2px 5px;border-bottom:1px solid #E5E7EB}
td.n{width:6mm;font-weight:800;color:var(--green)}
td.t b{font-weight:700}
td.t .lo{font-size:6.8pt;color:var(--muted);margin:0}
td.term{width:13mm;font-size:7.3pt;color:var(--muted)}
td.box,th.box{width:11mm;text-align:center}
td.rag{width:22mm;text-align:center;font-size:7pt;color:var(--muted);white-space:nowrap}
.sq{display:inline-block;width:3.4mm;height:3.4mm;border:1.2px solid #1B2430;border-radius:1px}
.dot{display:inline-block;width:3.3mm;height:3.3mm;border-radius:50%;border:1.3px solid;margin:0 1.2mm;vertical-align:-0.5mm}
.dot.r{border-color:#D9534F}.dot.a{border-color:#E0A800}.dot.g{border-color:#2E7D57}
.soon{font-size:6.5pt;font-weight:700;color:var(--muted);text-transform:uppercase;letter-spacing:.04em}
</style>"""

def pdf(key):
    s = SUBJ[key]; rows = s["rows"]; name = s["name"]
    foot = f'"Léim · leim.ie/junior-cycle-{key}-checklist.html · Tick online too: the web version saves your ticks on your device"'
    o = [f'<!doctype html><html lang="en-IE"><head><meta charset="utf-8"><title>Junior Cycle {name} topic checklist | Léim</title><link rel="stylesheet" href="pdf.css">{PDF_CSS}<style>:root{{--foot:{foot}}}</style></head><body>']
    o.append(f'<div class="band"><div><div class="k">Free checklist · Junior Cycle {name}</div><h1>My {name} topic checklist</h1></div><div class="logo">Léim ↗</div></div>')
    o.append(f'<div class="how"><span>Tick each box when it\'s done: <b>Game</b> (played the free game on leim.ie) · <b>Rules</b> (read the rules) · <b>Sheet</b> (did the revision sheet). Then colour a dot: <b style="color:#D9534F">red</b> not yet · <b style="color:#9A6B00">amber</b> getting there · <b style="color:#2E7D57">green</b> got it.</span></div>')
    o.append(f'<p class="small" style="margin:0 0 4px">{e(s["lo_note"])} Topics in the order most schools teach them; "coming soon" = not on leim.ie yet.</p>')
    for yr in ["1st year", "2nd year", "3rd year"]:
        yrows = [r for r in rows if r["year"].startswith(yr[:3])]
        o.append(f'<h2>{yr}</h2><table><thead><tr><th>#</th><th>Topic and learning outcomes</th><th>Term</th><th class="box">Game</th><th class="box">Rules</th><th class="box">Sheet</th><th class="box" style="width:22mm">Confident?</th></tr></thead><tbody>')
        for r in yrows:
            soon = "" if r["url"] else ' <span class="soon">· coming soon</span>'
            o.append(f'<tr><td class="n">{r["n"]}</td><td class="t"><b>{e(r["title"])}</b>{soon}<div class="lo">LO {e(r["lo_short"])}</div></td><td class="term">{e(r["term"])}</td>'
                     + '<td class="box"><span class="sq"></span></td>' * 3
                     + '<td class="rag"><span class="dot r"></span><span class="dot a"></span><span class="dot g"></span></td></tr>')
        o.append('</tbody></table>')
    o.append('</body></html>')
    return "".join(o)

def pages_of(p):
    d = open(p, "rb").read()
    return len(re.findall(rb"/Type\s*/Page[^s]", d))

if __name__ == "__main__":
    # optional: python3 src/build_checklists.py english  (only rebuild the subjects named)
    for key in (sys.argv[1:] or SUBJ):
        open(os.path.join(ROOT, f"junior-cycle-{key}-checklist.html"), "w", encoding="utf-8").write(page(key))
        src = os.path.join(ROOT, "src", f"{key}-topic-checklist.html")
        open(src, "w", encoding="utf-8").write(pdf(key))
        out = os.path.join(ROOT, "printables", f"junior-cycle-{key}-topic-checklist.pdf")
        subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--no-pdf-header-footer",
                        f"--print-to-pdf={out}", os.path.basename(src)], cwd=os.path.join(ROOT, "src"),
                       check=True, capture_output=True)
        print(key, "pdf pages:", pages_of(out))
