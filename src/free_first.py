#!/usr/bin/env python3
"""Free first (her decision, 21 Nov 2026): hide the shop until launch (January 2027).

Run from the repo root:
  python3 src/free_first.py          -> hide every buy link on every root *.html page (safe to run again)
  python3 src/free_first.py --check  -> list any buy link still on the site (exit 1 if any)
  python3 src/free_first.py --restore -> LAUNCH DAY: put every original buy box back

Every replaced piece keeps the original HTML inside <!--ff:BASE64--> ... <!--/ff-->,
so --restore puts it back exactly. Pages are never deleted; their content stays.
The page builders (assemble_game.py, build_english_page.py, build_maths_page.py, ...)
call hide_all() at the end, so rebuilding a page can't bring the buy buttons back.
"""
import base64, glob, os, re, sys

ON = True  # launch day: set to False (and run --restore) to switch the shop back on

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAY = r'https://payhip\.com/'
WRAP = re.compile(r'<!--ff:([A-Za-z0-9+/=]*)-->.*?<!--/ff-->', re.S)


def wrap(orig, new):
    return '<!--ff:' + base64.b64encode(orig.encode()).decode() + '-->' + new + '<!--/ff-->'


def box(join, small=False):
    cls = 'soon-box small' if small else 'soon-box'
    return ('<div class="%s"><p class="soon-t">🛒 Coming soon: join the list to hear first</p>'
            '<p>Printable packs for teachers and students are on the way. Everything free stays free.</p>'
            '<a class="btn" href="%s">Join the list</a></div>' % (cls, join))


def join_link(name, html):
    if re.search(r'id="join"', html):
        return '#join'
    m = re.search(r'href="(junior-cycle-[a-z-]+\.html)#join"', html)
    return (m.group(1) if m else 'index.html') + '#join'


def protect(html):
    """Swap already-wrapped parts out so they're never touched twice."""
    keep = []
    def sub(m):
        keep.append(m.group(0))
        return '\x00%d\x00' % (len(keep) - 1)
    return WRAP.sub(sub, html), keep


def unprotect(html, keep):
    return re.sub('\x00(\\d+)\x00', lambda m: keep[int(m.group(1))], html)


# Page-specific wording (teachers page talks about the packs).
TEXT = {
    'junior-cycle-spanish-exam-pack-listening.html': [
        ("Don't have the Exam Pack yet? <a href=\"https://payhip.com/b/IAjDY\">Get it here (€10)</a>",
         "The printable Exam Pack is coming soon: <a href=\"junior-cycle-spanish.html#join\">join the list to hear first</a>"),
    ],
    'teachers.html': [
        ('plus €5 printable teacher packs mapped to the specification.',
         'plus printable teacher packs (coming soon) mapped to the specification.'),
        ('and €5 printable teacher packs mapped to the Junior Cycle specification.',
         'and printable teacher packs, coming soon, mapped to the Junior Cycle specification.'),
        ('<strong>A teacher pack (€5)</strong>', '<strong>A teacher pack (coming soon)</strong>'),
        ('<p>Open any Spanish topic game to find its free sheet and teacher pack.</p>',
         '<p>Open any Spanish topic game to find its free sheet.</p>'),
    ],
}


def hide(name, html):
    html, keep = protect(html)
    j = join_link(name, html)

    def put(orig, new):
        keep.append(wrap(orig, new))
        return '\x00%d\x00' % (len(keep) - 1)

    # 0. Page-specific wording
    for a, b in TEXT.get(name, []):
        if a in html:
            html = html.replace(a, put(a, b), 1)
    # 1. Shop tab in the menu
    html = re.sub(r'<a class="shop" href="' + PAY + r'[^"]*">Shop</a>', lambda m: put(m.group(0), ''), html)
    # 2. "Teachers: ... Get the X Teacher Pack" / "Students and parents: ..." lines on game pages
    #    (one Coming soon box per page; a second line just disappears)
    seen = []
    def line(m):
        new = '' if seen else box(j, small=True)
        seen.append(1)
        return put(m.group(0), new)
    html = re.sub(r'<p[^>]*>\s*<b>(?:Teachers|Students and parents):</b>(?:(?!</p>).)*?' + PAY + r'(?:(?!</p>).)*</p>',
                  line, html, flags=re.S)
    # 3. Product cards (keep the card and its text, drop the link and the price)
    cards = []
    def card(m):
        inner = re.sub(r'\s*·\s*€\d+(?:\.\d\d)?', '', m.group(3))
        inner = re.sub(r'<p[^>]*>(?:(?!</p>).)*(?:Payhip|Open the shop|Get it|Buy|↗)(?:(?!</p>).)*</p>', '', inner, flags=re.S)
        cards.append(1)
        if 'cardlink' in m.group(1):  # a single card on its own: say so inside it
            inner += ('<p class="soon-t" style="margin-top:8px">🛒 Coming soon: join the list to hear first</p>'
                      '<a class="btn" href="%s">Join the list</a>' % j)
        return put(m.group(0), '<div class="%s ff-card"%s>%s</div>' % (m.group(1), m.group(2).replace(' target="_blank" rel="noopener"', ''), inner))
    html = re.sub(r'<a class="(card[^"]*)" href="' + PAY + r'[^"]*"([^>]*)>(.*?)</a>', card, html, flags=re.S)
    # one box at the top of each grid of hidden cards
    def grid(m):
        return put(m.group(0), box(j) + m.group(0))
    html = re.sub(r'<div class="grid">(?=\s*\x00\d+\x00)', lambda m: grid(m) if 'ff-card' in keep[int(re.match(r'\s*\x00(\d+)\x00', html[m.end():]).group(1))] else m.group(0), html)
    # 4. Paragraphs built around a buy link or button -> box
    html = re.sub(r'<p[^>]*>(?:(?!</p>|<p[ >]).)*?<a [^>]*href="' + PAY + r'b/[^"]*"(?:(?!</p>).)*</p>',
                  lambda m: put(m.group(0), box(j, small=True)) if not re.search(r'<li', m.group(0)) else m.group(0),
                  html, flags=re.S)
    # 5. Any other buy link: keep the words, drop the link
    html = re.sub(r'<a [^>]*href="' + PAY + r'[^"]*"[^>]*>(.*?)</a>',
                  lambda m: put(m.group(0), m.group(1) + ' (coming soon)'), html, flags=re.S)
    return unprotect(html, keep)


def restore(html):
    return WRAP.sub(lambda m: base64.b64decode(m.group(1)).decode(), html)


def pages():
    return sorted(glob.glob(os.path.join(ROOT, '*.html')))


def hide_all(quiet=True):
    if not ON:
        return 0
    n = 0
    for p in pages():
        s = open(p, encoding='utf-8').read()
        t = hide(os.path.basename(p), s)
        if t != s:
            open(p, 'w', encoding='utf-8').write(t)
            n += 1
    if not quiet:
        print('free_first: changed %d pages' % n)
    return n


def leftovers():
    bad = []
    for p in pages():
        s = WRAP.sub('', open(p, encoding='utf-8').read())
        for m in re.finditer(r'href="https://payhip\.com[^"]*"', s):
            bad.append('%s: %s' % (os.path.basename(p), m.group(0)))
    return bad


if __name__ == '__main__':
    if '--restore' in sys.argv:
        n = 0
        for p in pages():
            s = open(p, encoding='utf-8').read()
            t = restore(s)
            if t != s:
                open(p, 'w', encoding='utf-8').write(t); n += 1
        print('free_first: restored %d pages' % n)
    elif '--check' in sys.argv:
        b = leftovers()
        print('\n'.join(b) or 'free_first: no buy links left ✓')
        sys.exit(1 if b else 0)
    else:
        hide_all(quiet=False)
        b = leftovers()
        print('\n'.join(b) or 'free_first: no buy links left ✓')
