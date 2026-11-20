# "What came up" data for the Exam Centres, checklists and game pages (job 7, 20 Nov 2026).
# FACTS ONLY: which kind of question / topic appeared in which year and question number.
# Read from the SEC papers 2022-2026 (examinations.ie Exam Material Archive). Never copy
# questions, texts, answers or marking-scheme wording here or on the site (SEC reply 20 Nov 2026).
# Labels are Léim's own. Maths/English refs: H = Higher level question, O = Ordinary level question.
# Spanish refs: L = Listening question, R = Reading question, Q16-Q18 = Writing questions.
# Rows: (label, {year: "refs"}, [Léim topic orders this row counts for])

YEARS = ["2022", "2023", "2024", "2025", "2026"]
ARCHIVE = "https://www.examinations.ie/exammaterialarchive/"

SPANISH = [
    ("Weather forecast", {"2022": "L4", "2023": "L3", "2024": "L5", "2025": "L6", "2026": "L4"}, [17]),
    ("Shopping, offers & prices", {"2022": "L2, L6", "2023": "L6", "2024": "L1, R14", "2025": "L5", "2026": "L6, R12"}, [16]),
    ("Family & describing people", {"2022": "L3", "2023": "R13", "2024": "L2, R12, R13", "2025": "L2, R13", "2026": "R14"}, [6, 7]),
    ("Free time, hobbies & going out", {"2022": "L1, R10", "2023": "R10", "2024": "R10", "2025": "L1, R10", "2026": "L2, R10"}, [8, 12]),
    ("Holidays, hotels & travel", {"2022": "R15", "2023": "R14, R15", "2024": "L7, R15", "2025": "L8", "2026": "L3, L7, R15"}, [21]),
    ("Directions & getting around town", {"2022": "L5", "2023": "L5", "2024": "L3", "2026": "L5"}, [19]),
    ("School life", {"2022": "L8", "2023": "L1, L2, L7", "2025": "L4", "2026": "L1"}, [9]),
    ("Festivals & music events", {"2022": "R11", "2024": "R11, R15", "2025": "R11, R15", "2026": "R11"}, [26]),
    ("A Spanish city or region", {"2023": "L8", "2024": "L8", "2025": "R14", "2026": "L8"}, [26]),
    ("Transport & announcements", {"2022": "R14", "2024": "L4", "2025": "L3, R12", "2026": "L5"}, [19]),
    ("Health, illness & injury", {"2022": "R13", "2025": "L4", "2026": "L1"}, [22]),
    ("Clothes", {"2023": "L2", "2024": "L1", "2026": "R9"}, [16]),
    ("Daily routine & chores", {"2023": "R10", "2024": "R10", "2026": "R10"}, [13]),
    ("Sport & sports stars", {"2022": "R12", "2025": "R10", "2026": "R14"}, [12]),
    ("Food & ordering", {"2024": "L6", "2025": "L7"}, [15]),
    ("Pets & animals", {"2023": "R12", "2026": "R13"}, [6]),
]

# Writing: points asked in Q17 (5-point email or blog) and Q18 (8-point letter to a friend / exchange student)
SPANISH_WRITING = [
    ("Describe people (family, a friend, a teacher)", {"2022": "Q17", "2023": "Q17", "2024": "Q18", "2025": "Q17", "2026": "Q17, Q18"}, [6, 7]),
    ("Your school", {"2022": "Q18", "2023": "Q18", "2024": "Q17", "2025": "Q18", "2026": "Q18"}, [9]),
    ("Future plans", {"2022": "Q18", "2023": "Q18", "2024": "Q18", "2025": "Q17, Q18", "2026": "Q17, Q18"}, [18, 25]),
    ("A past holiday or weekend", {"2022": "Q18", "2023": "Q18", "2024": "Q18", "2025": "Q17, Q18", "2026": "Q18"}, [20, 21]),
    ("Your house or bedroom", {"2022": "Q18", "2023": "Q18", "2024": "Q18", "2026": "Q17"}, [10]),
    ("Your area", {"2022": "Q18", "2023": "Q18", "2025": "Q18", "2026": "Q18"}, [10]),
    ("Daily routine / a typical day", {"2022": "Q18", "2023": "Q17", "2025": "Q18", "2026": "Q17"}, [13]),
    ("A Spanish city, or what you like about Spain", {"2022": "Q17", "2023": "Q17", "2025": "Q17", "2026": "Q17"}, [26]),
    ("Hobbies & weekends", {"2022": "Q18", "2024": "Q18", "2026": "Q18"}, [8, 12]),
    ("Weather in Ireland", {"2022": "Q18", "2025": "Q18", "2026": "Q18"}, [17]),
    ("Food", {"2022": "Q17", "2023": "Q18", "2025": "Q18"}, [15]),
    ("Birthday or a celebration", {"2023": "Q18", "2025": "Q17"}, [2]),
]
# Topics used in every paper rather than as one question
SPANISH_EVERY = {5: "the writing section (Q16–Q18) every year, 2022–2026: answers need the present tense",
                 20: None, 23: "Q17 every year, 2022–2026 (an email, a blog in 2024)",
                 27: "every paper, 2022–2026: 8 listening and 7 reading questions each year"}

MATHS = [
    ("Sets & Venn diagrams", {"2022": "H6, O5", "2023": "H6, O3", "2024": "H5, O3", "2025": "H10, O5", "2026": "H7, O10"}, [5]),
    ("Money: income tax, pay & interest", {"2022": "H1", "2023": "H10", "2024": "H3", "2025": "O9", "2026": "H3, O9"}, [19]),
    ("Money: bills, VAT, profit & loss", {"2022": "O2, O9", "2023": "O1", "2024": "H4, O2", "2025": "H3, O2", "2026": "O2"}, [18]),
    ("Area, perimeter & scale drawings", {"2022": "H4, O11, O12", "2023": "H12, O4", "2024": "O11", "2025": "H7, O4, O11", "2026": "H10, O5"}, [21]),
    ("Statistics: grouped data, histograms, stem & leaf", {"2022": "O6", "2023": "H4, O8", "2024": "H2, O8", "2025": "H4, O3", "2026": "H2, O7"}, [22]),
    ("Coordinate geometry of the line", {"2022": "H3, H11", "2023": "H7, O9", "2024": "H9, H10, O10", "2025": "H5, O14", "2026": "H4, O8"}, [28]),
    ("Functions & graphs", {"2022": "O8", "2023": "H2, H11, O7, O11", "2024": "H8", "2025": "H9, H12", "2026": "H6, H8, H9, O12"}, [31]),
    ("Trigonometry", {"2022": "H8, H12", "2023": "H8, O8", "2024": "H13", "2025": "H8", "2026": "H11, O13"}, [32]),
    ("Volume, surface area & nets", {"2022": "H5, O3", "2023": "H3, O10", "2024": "H6, H7, O9", "2025": "O12", "2026": "H13, O11"}, [33]),
    ("Algebra: simplify & substitute", {"2022": "H9, O13", "2023": "O12, O14", "2024": "H11, O12", "2025": "H11, O10", "2026": "O12"}, [8]),
    ("Factorising", {"2022": "H9, O13", "2023": "H9", "2024": "H11, O12", "2025": "O10", "2026": "O12"}, [27]),
    ("Probability: outcomes & sample spaces", {"2022": "H2", "2023": "O6", "2024": "H1", "2025": "O6", "2026": "H1"}, [11]),
    ("Statistics: surveys, charts & the mean", {"2022": "O4", "2023": "O5", "2024": "O8", "2025": "O1", "2026": "O3"}, [12]),
    ("Number operations", {"2022": "O1", "2023": "H5, O1, O12", "2024": "O1", "2025": "O1", "2026": "O1"}, [1]),
    ("Factors, multiples & primes", {"2023": "H5", "2024": "O1", "2025": "O8", "2026": "O1"}, [2]),
    ("Constructions", {"2022": "O11", "2023": "H12", "2024": "O6", "2025": "H6"}, [14]),
    ("Expanding brackets", {"2023": "H9", "2024": "O12", "2025": "O10", "2026": "O5"}, [15]),
    ("Theorems, similar triangles & circles", {"2022": "H12", "2023": "H14", "2025": "H6", "2026": "H12"}, [24]),
    ("Speed, distance, time & currency", {"2022": "H1, H10", "2024": "O4", "2025": "O13", "2026": "H3, H5, O4"}, [20]),
    ("Linear equations", {"2022": "O10", "2023": "O2", "2025": "O7, O10"}, [16]),
    ("Indices & standard form", {"2022": "H7", "2023": "H9", "2026": "H5"}, [17]),
    ("Linear patterns", {"2024": "H12", "2025": "H2", "2026": "O6"}, [9]),
    ("Units & time", {"2022": "O8", "2023": "H8", "2025": "O12"}, [10]),
    ("Ratio & proportion", {"2024": "H4", "2025": "O2", "2026": "H5"}, [7]),
    ("Transformations & symmetry", {"2023": "O13", "2024": "H9", "2026": "O8"}, [23]),
    ("Pythagoras", {"2023": "O13", "2024": "H13, O11", "2026": "H13, O13"}, [25]),
    ("Quadratic equations", {"2023": "H13", "2025": "H13", "2026": "H9"}, [30]),
    ("Algebraic fractions & long division", {"2022": "H9", "2025": "H11", "2026": "H9"}, [35]),
    ("Angles & triangles", {"2022": "O7", "2024": "O5"}, [13]),
    ("Percentages", {"2022": "H6", "2026": "H3"}, [6]),
    ("Decimals, rounding & estimation", {"2022": "O1", "2023": "H1"}, [4]),
    ("Quadratic & exponential patterns", {"2025": "H2", "2026": "H8"}, [36]),
    ("Fractions", {"2022": "H6, O10"}, [3]),
    ("Counting (how many choices?)", {"2025": "H1, O6"}, [26]),
    ("Simultaneous equations", {"2024": "O7"}, [29]),
    ("Inequalities", {"2024": "H11"}, [34]),
]
MATHS_EVERY = {38: "every paper, 2022–2026: most questions join two or more topics in a real-life problem"}

ENGLISH = [
    ("An unseen poem on the paper", {"2022": "H4, O12", "2023": "H3–4, O1–2", "2024": "O8–9", "2025": "H1–2, O4–5", "2026": "H7, O7–8"}, [8, 23]),
    ("A poem you studied", {"2022": "H5–6, O13", "2023": "H5, O4", "2024": "H8, O11", "2025": "H3, O6", "2026": "H8, O9"}, [23, 29, 30]),
    ("A novel you studied", {"2022": "H10, O10", "2023": "O10", "2024": "H4, O7", "2025": "H6, O12", "2026": "H4, O6"}, [5, 14, 29]),
    ("A film you studied", {"2022": "H8, O8", "2023": "H1–2, O14", "2024": "H9", "2025": "H6", "2026": "H2, O12"}, [27]),
    ("A play you studied", {"2022": "H10, O8", "2024": "H4", "2025": "O10", "2026": "O12"}, [21]),
    ("Shakespeare (Higher Level)", {"2023": "H6", "2024": "H1–4", "2025": "H4–5", "2026": "H5–6"}, [28]),
    ("A short story you studied", {"2025": "H7", "2026": "O6"}, [11]),
    ("Character: what they're like, how they change", {"2022": "O8", "2023": "H1, H10", "2024": "H4, H7, O7", "2025": "H6, H7, O10", "2026": "H4, H6, O4, O11"}, [5]),
    ("Setting, or the world of a text", {"2022": "O11", "2025": "H7", "2026": "O6"}, [14]),
    ("An unseen prose extract (novel or story)", {"2022": "H9, O5–7", "2024": "H5–7", "2025": "O8", "2026": "H3, O3–4"}, [4]),
    ("An unseen drama extract", {"2023": "H6", "2024": "H1–3", "2026": "O10–11"}, [21, 28]),
    ("Non-literary & visual texts: posters, articles, reviews, podcasts", {"2022": "H7, O9", "2023": "O5–7, O11–12", "2024": "H3, O1–5", "2025": "H8, O1–3, O11", "2026": "H1, H9, O1–2"}, [4, 20, 31]),
    ("Film techniques: shots, images, atmosphere", {"2022": "H7–8", "2023": "H2", "2024": "H9"}, [27]),
    ("Naming poetic techniques", {"2022": "H5", "2023": "H4", "2025": "H2", "2026": "O7"}, [8]),
    ("Word meanings, grammar & punctuation", {"2022": "H3, O5", "2023": "H9, O1, O5", "2024": "O8", "2025": "O2, O4", "2026": "O3"}, [1, 2, 3, 6, 13, 17, 24, 26]),
    ("Creative writing: an opening, a scene, what happens next", {"2022": "O4, O7", "2023": "H10, O8", "2024": "H6", "2025": "H10", "2026": "O2, O11"}, [9, 12]),
    ("Diary entry", {"2022": "H2", "2023": "O3", "2024": "O3", "2026": "O5"}, [9]),
    ("Article, report, blog, post, advert or voice-over", {"2023": "O13–14", "2024": "O4, O6, O10", "2025": "H9, O9", "2026": "H9"}, [18, 20, 22]),
    ("Speech or talk", {"2023": "H7", "2024": "H2", "2026": "H8"}, [10, 16, 18]),
    ("Letter, postcard or email", {"2022": "O14", "2023": "O9", "2025": "O7"}, [15, 16]),
    ("Review of a film or book", {"2025": "O12", "2026": "H2"}, [22]),
]
ENGLISH_EVERY = {7: "not a question of its own, but every longer written answer on the 2022–2026 papers needed well-organised paragraphs",
                 32: "every paper, 2022–2026: one 2-hour paper, 180 marks, built around a theme"}
ENGLISH_THEMES = {"2022": ("Hope", "A World of Wonder"), "2023": ("The Art of Storytelling", "People and Places"),
                  "2024": ("Interesting Interactions", "Journeys and Adventure"), "2025": ("Perception", "Different Viewpoints"),
                  "2026": ("Critical Reflection", "Interesting Worlds")}

KEYS = {"maths": "H = Higher level question, O = Ordinary level question.",
        "english": "H = Higher level question, O = Ordinary level question.",
        "spanish": "L = Listening question, R = Reading question, Q16–Q18 = Writing questions."}


def _rows(subject):
    if subject == "spanish":
        return SPANISH + SPANISH_WRITING
    return {"maths": MATHS, "english": ENGLISH}[subject]


def came_line(subject, order):
    """Plain-text "Came up in" line for a topic (Léim order number), or None."""
    every = {"spanish": SPANISH_EVERY, "maths": MATHS_EVERY, "english": ENGLISH_EVERY}[subject]
    if every.get(order):
        return every[order]
    refs = {y: [] for y in YEARS}
    for _, d, topics in _rows(subject):
        if order in topics:
            for y, r in d.items():
                for x in r.split(", "):
                    if x not in refs[y]:
                        refs[y].append(x)
    used = [y for y in reversed(YEARS) if refs[y]]
    if not used:
        return None
    return " · ".join(f"{y} ({_merge(refs[y])})" for y in used)


def _merge(tokens):
    # "H1–2", "H2", "O7" -> "H1–2, O7": expand ranges, drop repeats, sort, re-join runs
    import re
    seen = set()
    for t in tokens:
        m = re.fullmatch(r"([A-Z])(\d+)(?:–(\d+))?", t)
        p, a, b = m.group(1), int(m.group(2)), int(m.group(3) or m.group(2))
        for n in range(a, b + 1):
            seen.add((p, n))
    order = "HOLRQ"
    out, items = [], sorted(seen, key=lambda x: (order.index(x[0]), x[1]))
    i = 0
    while i < len(items):
        p, a = items[i]; b = a
        while i + 1 < len(items) and items[i + 1] == (p, b + 1):
            i += 1; b += 1
        out.append(f"{p}{a}" if a == b else f"{p}{a}–{b}")
        i += 1
    return ", ".join(out)


def _esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def grid_table(rows, first_col="Topic"):
    head = "".join(f"<th>{y}</th>" for y in YEARS)
    body = []
    for label, d, _ in rows:
        n = len(d)
        cells = "".join(f'<td>{_esc(d[y]) if y in d else "—"}</td>' for y in YEARS)
        body.append(f'<tr><td><strong>{_esc(label)}</strong></td>{cells}<td><strong>{n}/5</strong></td></tr>')
    return (f'<div class="cameup-wrap"><table class="cameup"><thead><tr><th>{first_col}</th>{head}<th>Years</th></tr></thead>'
            f'<tbody>{"".join(body)}</tbody></table></div><p class="cameup-hint">Swipe the table sideways to see every year.</p>')


CSS = ('<style>.cameup-wrap{overflow-x:auto;-webkit-overflow-scrolling:touch;margin:12px 0 16px;border:1px solid var(--line,#E3E7EC);border-radius:12px}'
       '.cameup{min-width:600px;width:100%;border-collapse:collapse}'
       '.cameup td,.cameup th{font-size:13px;padding:7px 9px;vertical-align:top;text-align:left;border-bottom:1px solid var(--line,#E3E7EC)}'
       '.cameup th{background:var(--green,#1F7A4D);color:#fff;text-transform:none;letter-spacing:0}'
       '.cameup td:first-child{min-width:170px;position:sticky;left:0;background:#fff}'
       '.cameup td:last-child,.cameup td:not(:first-child){white-space:nowrap}'
       '.cameup-hint{font-size:13px;color:var(--muted,#5B6672)}@media(min-width:700px){.cameup-hint{display:none}}</style>')
