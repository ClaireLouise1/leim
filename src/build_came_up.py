# Builds the "What came up" sections (job 7) and the "Came up in" lines on game pages.
#   python3 src/build_came_up.py      -> rewrites the Spanish Exam Centre's #came-up section and every
#                                        Maths/English game page's "Came up in" line (src main + built page)
# The Maths Exam Centre and the English subject page import maths_section() / english_section()
# from here (src/build_maths_exam_centre.py, src/build_english_page.py), so re-run those too.
import os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import came_up_data as D
import checklist_data as C

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARCH = f'<a href="{D.ARCHIVE}" target="_blank" rel="noopener">State Examinations Commission\'s archive ↗</a>'
NOTE = ('<strong>Patterns, not predictions.</strong> The exam can ask about any part of the course, so revise every topic. '
        'The grid shows only which topics the questions were mainly about; the topic labels are ours. '
        f'Every paper and marking scheme is free on the {ARCH}.')


def spanish_section():
    return f'''<section id="came-up">
  <h2>What came up</h2>
  <p>The first common-level Junior Cycle Spanish paper was in 2022, so there are five papers so far. Here is what each listening and reading question was mainly about, year by year. {D.KEYS["spanish"]}</p>
  {D.CSS}
  {D.grid_table(D.SPANISH)}
  <h3>The writing section</h3>
  <p>Every year: Q16 is a short task worth 10 marks (a translation into Spanish in 2022, 2023 and 2025, a form in 2024, fill-the-gap sentences in 2026). Q17 is an email or blog with 5 points (30 marks): in four of the five years you were staying in Spain and writing home. Q18 is a letter to a friend or exchange student answering 8 questions (40 marks, about 200 words). These are the points the writing asked about:</p>
  {D.grid_table(D.SPANISH_WRITING, "Writing point")}
  <p><strong>What stands out:</strong> weather, shopping, family and describing people, free time, and holidays came up every single year. Every writing section mixed the present, the past (<em lang="es">¿Qué hiciste…?</em>) and the future (<em lang="es">¿Qué vas a hacer…?</em>), so revise all three tenses.</p>
  <p class="small" style="color:var(--muted)">{NOTE}</p>
</section>'''


def maths_section():
    return f'''<section id="came-up">
  <h2>What came up</h2>
  <p>Here is what each question on the 2022–2026 papers was mainly about, at both levels. {D.KEYS["maths"]} Many questions have later parts on a second topic, so a topic can come up more often than the grid shows.</p>
  {D.CSS}
  {D.grid_table(D.MATHS)}
  <p><strong>What stands out:</strong> every year, at one level or both, there was a Venn diagram question, money, area and perimeter, statistics, coordinate geometry, functions and graphs, trigonometry, volume, and algebra. Ordinary level Question 1 is always a number warm-up. Surds were not the main topic of any question in these five years, but they're still on the course.</p>
  <p class="small" style="color:var(--muted)">{NOTE}</p>
</section>'''


def english_section():
    th = "".join(f'<tr><td><strong>{y}</strong></td><td>{h}</td><td>{o}</td></tr>' for y, (h, o) in D.ENGLISH_THEMES.items())
    return f'''<section class="block" id="came-up" style="scroll-margin-top:90px">
  <div class="wrap">
    <div class="sec-head">
      <h2>What came up</h2>
      <p>The layout changes every year, but the same kinds of question keep coming back. Here is what each question on the 2022–2026 papers asked you to do. {D.KEYS["english"]}</p>
    </div>
    {D.CSS}
    <h3 style="margin:8px 0">The themes</h3>
    <div class="table-wrap"><table><thead><tr><th>Year</th><th>Higher level theme</th><th>Ordinary level theme</th></tr></thead><tbody>{th}</tbody></table></div>
    <h3 style="margin:22px 0 8px">The questions</h3>
    {D.grid_table(D.ENGLISH, "What was asked")}
    <div class="note" style="margin-top:18px"><b>What stands out:</b> every year, at both levels, there was an unseen poem, a poem you studied, a novel, a film, a non-literary or visual text, questions on character, creative writing and some word-level questions. Shakespeare was on every Higher paper from 2023 to 2026. Most questions on studied texts ask for a <b>key moment</b>, backed up with quotes, so learn two or three key moments for each text.</div>
    <p style="margin-top:14px;font-size:14px;color:var(--muted)">{NOTE}</p>
  </div>
</section>'''


def game_line(subject, order):
    line = D.came_line(subject, order)
    link = f'<a href="{D.ARCHIVE}" target="_blank" rel="noopener">past papers ↗</a>'
    if line:
        key = "" if subject == "maths" and order == 38 or subject == "english" and order in D.ENGLISH_EVERY else f" ({D.KEYS[subject].rstrip('.')})"
        return f'<b>Came up in:</b> {line}{key}. See the {link}.'
    return f'<b>Came up in:</b> no 2022–2026 question was mainly about this topic, but it can still come up inside other questions. See the {link}.'


def update_games():
    n = 0
    for subject, rows in (("maths", C.MATHS), ("english", C.ENGLISH)):
        for i, r in enumerate(rows, 1):
            page = r[5]
            if not page:
                continue
            slug = page[:-5]
            new = game_line(subject, i)
            for f in (f"src/{slug}.main.html", page):
                p = os.path.join(ROOT, f)
                if not os.path.exists(p):
                    continue
                s = open(p, encoding="utf-8").read()
                s2, k = re.subn(r'(<p class="came"[^>]*>).*?(</p>)', lambda m: m.group(1) + new + m.group(2), s, count=1, flags=re.S)
                if k:
                    open(p, "w", encoding="utf-8").write(s2)
                    n += 1
                else:
                    print("no Came up line in", f)
    return n


def update_spanish_ec():
    p = os.path.join(ROOT, "junior-cycle-spanish-exam-centre.html")
    s = open(p, encoding="utf-8").read()
    s2, k = re.subn(r'<section id="came-up">.*?</section>', lambda m: spanish_section(), s, count=1, flags=re.S)
    assert k == 1
    open(p, "w", encoding="utf-8").write(s2)


if __name__ == "__main__":
    update_spanish_ec()
    print("game lines updated:", update_games())
