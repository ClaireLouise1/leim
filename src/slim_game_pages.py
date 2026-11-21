"""Game first, text out of the way (her request, 21 Nov 2026: "straight to games, text somewhere else").
For every game page: replaces the big intro (pill, title, paragraph, buttons) with a compact bar
(‹ Subject · game name · 📖 Rules · 📝 Practice test for Maths and English), so the game is the first thing on the page,
and folds the rules / exam corner / printable section into a closed "📖 Rules, exam tips & printable" box
(it opens automatically from any "Revise the rules" link).
Idempotent: pages already done carry <!--slim-->. Run after any game page is (re)assembled:
  python3 src/slim_game_pages.py            (all games)
  python3 src/slim_game_pages.py SLUG ...   (just these)
assemble_game.py calls it automatically."""
import os, re, sys, importlib.util
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def subjects():
    # read SUBJECTS from build_subject_hub.py without running its build
    src = open(os.path.join(ROOT, 'src', 'build_subject_hub.py'), encoding='utf-8').read()
    block = src[src.index('SUBJECTS = {'):src.index('\nSHORT = {')]
    ns = {}; exec(block, ns); return ns['SUBJECTS']

CSS = ('<style>.gtop{display:flex;flex-wrap:wrap;align-items:center;gap:8px 12px;margin:0 0 14px}'
       '.gtop .gback{font-weight:700;color:var(--muted);text-decoration:none}'
       '.gtop h1{font-size:clamp(24px,6vw,32px);margin:0;flex:1 1 auto;line-height:1.1}'
       '.gtop .gchips{display:flex;gap:8px;flex-wrap:wrap}'
       '.gtop .chip{display:inline-flex;align-items:center;gap:6px;background:#fff;border:2px solid var(--line);border-radius:999px;padding:7px 12px;font-weight:700;color:var(--ink);text-decoration:none;font-size:14px}'
       '.gtop .chip.y{background:var(--sun);border-color:var(--sun)}'
       'details.more{margin-top:24px;border:2px solid var(--line);border-radius:16px;background:#fff}'
       'details.more>summary{cursor:pointer;padding:14px 18px;font-weight:800;font-size:17px;list-style:none}'
       'details.more>summary::-webkit-details-marker{display:none}'
       'details.more>summary::after{content:" ▾";color:var(--muted)}details.more[open]>summary::after{content:" ▴"}'
       'details.more>.panel{margin-top:0!important;border:0;box-shadow:none}</style>')
JS = ('<script>(function(){var d=document.getElementById("more");if(!d)return;'
      'function o(){d.open=true;}if(location.hash==="#revise")o();'
      'document.addEventListener("click",function(e){var a=e.target.closest&&e.target.closest(\'a[href="#revise"]\');if(a)o();});})();</script>')

PT_PAGE = {'maths': 'practice-test.html', 'english': 'english-practice-test.html'}   # same as build_subject_hub.py

def slim(slug, subj_key, subj_title, test):
    p = os.path.join(ROOT, slug + '.html')
    if not os.path.exists(p): return 'missing'
    h = open(p, encoding='utf-8').read()
    pt = PT_PAGE.get(subj_key, 'practice-test.html')
    if '<!--slim-->' in h:
        # pages slimmed before their subject had tests: add the 📝 chip to the bar
        rules = '<a class="chip" href="#revise">📖 Rules</a>'
        if test and f'{pt}?t={slug}"' not in h and h.count(rules) == 1:
            h = h.replace(rules, rules + f'<a class="chip y" href="{pt}?t={slug}">📝 Practice test</a>')
            open(p, 'w', encoding='utf-8').write(h)
            return 'ok'
        return 'already'
    m = re.search(r'<div class="sec-head" style="text-align:center">.*?<h1[^>]*>(.*?)</h1>.*?(?=<div class="panel" id="start")', h, re.S)
    if not m: return 'no sec-head'
    name = m.group(1)
    chips = '<a class="chip" href="#revise">📖 Rules</a>'
    if test: chips += f'<a class="chip y" href="{pt}?t={slug}">📝 Practice test</a>'
    top = (f'<!--slim-->{CSS}<div class="gtop"><a class="gback" href="junior-cycle-{subj_key}.html">‹ {subj_title}</a>'
           f'<h1>{name}</h1><div class="gchips">{chips}</div></div>\n\n      ')
    h = h[:m.start()] + top + h[m.end():]
    # start panel: drop the "Play" pill; move the tip + learning-outcome line into the rules box
    st = h.index('<div class="panel" id="start"')
    rv = h.index('<div class="panel" id="revise"')
    seg = h[st:rv]
    seg = seg.replace('<span class="pill">Play</span>\n', '', 1)
    moved = []
    for pat in (r'\s*<p class="small"[^>]*>.*?</p>', r'\s*<span class="lo">.*?</span>'):
        mm = re.search(pat, seg, re.S)
        if mm: moved.append(mm.group(0).strip()); seg = seg[:mm.start()] + seg[mm.end():]
    h = h[:st] + seg + h[rv:]
    # fold the rules panel (and anything after it inside the game column) into <details>
    rv = h.index('<div class="panel" id="revise"')
    close = h.index('\n    </div>\n  </div>\n</section>', rv)
    inner = h[rv:close]
    gt = inner.index('>') + 1
    inner = inner[:gt] + ''.join('\n        ' + x for x in moved) + inner[gt:]
    h = (h[:rv] + '<details class="more" id="more"><summary>📖 Rules, exam tips &amp; printable</summary>' + inner
         + '\n      </details>' + h[close:])
    h = h.replace('</body>', JS + '\n</body>', 1)
    open(p, 'w', encoding='utf-8').write(h)
    return 'ok'

def main(only=None):
    res = {}
    for key, cfg in subjects().items():
        slugs = [s for _, _, ss in cfg['strands'] for s in ss]
        if cfg.get('mix'): slugs.append(cfg['mix'][0][:-5])
        for s in slugs:
            if only and s not in only: continue
            res[s] = slim(s, key, cfg['title'], bool(cfg.get('tests')) and s in [x for _, _, ss in cfg['strands'] for x in ss])
    bad = {k: v for k, v in res.items() if v not in ('ok', 'already')}
    print('slimmed', sum(v == 'ok' for v in res.values()), 'already', sum(v == 'already' for v in res.values()), 'problems', bad)

if __name__ == '__main__':
    main(set(sys.argv[1:]) or None)
