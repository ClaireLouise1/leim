#!/usr/bin/env python3
"""Assemble a JC Maths game page from src/<slug>.main.html + src/<slug>.script.html,
using integer-rush.html for the head/header and footer.
Usage (repo root): python3 src/assemble_game.py SLUG "Title | Léim" "Meta description" """
import sys, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
slug, title, desc = sys.argv[1:4]
t = open(os.path.join(ROOT, "integer-rush.html"), encoding="utf-8").read()
head = t[:t.index('<main id="main">')]
head = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", head, count=1)
head = re.sub(r'<meta name="description" content=".*?">', f'<meta name="description" content="{desc}">', head, count=1)
after = t[t.index("</main>") + len("</main>"):]
foot = after[:after.index("<script")]
main = open(os.path.join(ROOT, "src", f"{slug}.main.html"), encoding="utf-8").read().strip()
script = open(os.path.join(ROOT, "src", f"{slug}.script.html"), encoding="utf-8").read().strip()
out = head + main + foot + script + '\n<script src="site.js"></script>\n</body>\n</html>\n'
open(os.path.join(ROOT, f"{slug}.html"), "w", encoding="utf-8").write(out)
print("wrote", slug + ".html", len(out))
