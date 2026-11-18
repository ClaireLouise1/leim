#!/usr/bin/env python3
"""Independent checker for Average Ace (Order 22, Statistics 2).
node src/test_average_ace.js > /tmp/aa.json ; python3 src/test_average_ace.py /tmp/aa.json
Recomputes every answer from the question TEXT and the PICTURE (SVG charts are measured: bar heights
from the gridlines, pie angles from the arc end points, dot positions from the number line, histogram
bars from the class boundaries; stem-and-leaf tables are parsed and checked to be ordered)."""
import json, re, sys, math, html as H
from fractions import Fraction as Fr
from collections import Counter

def num(x):
    x = Fr(x)
    if x.denominator == 1: return str(x.numerator)
    d = Fr(round(x * 100), 100)
    assert d == x, f"not 2dp {x}"
    s = f"{float(d):.2f}".rstrip('0').rstrip('.')
    return s
def half_up_1(x):
    x = Fr(x); return Fr(math.floor(x * 10 + Fr(1, 2)), 10)
def median(a):
    s = sorted(a); n = len(s)
    return Fr(s[(n - 1) // 2]) if n % 2 else Fr(s[n // 2 - 1] + s[n // 2], 2)
def nums(s): return [int(x) for x in re.findall(r'\d+', s)]
def val(opt):
    t = opt.replace('−', '-').replace('°', '').replace('%', '').strip()
    if '/' in t: a, b = t.split('/'); return Fr(int(a), int(b))
    return Fr(t)

def attrs(tag):
    return dict(re.findall(r'([\w-]+)="([^"]*)"', tag))
def texts(svg, cls):
    out = []
    for m in re.finditer(r'<text class="' + cls + r'"([^>]*)>(.*?)</text>', svg):
        a = attrs(m.group(1)); a['_t'] = H.unescape(m.group(2)); out.append(a)
    return out
def charts(h):
    return re.findall(r'<svg class="chart".*?</svg>', h, re.S)

# ---------- chart readers ----------
def yscale(svg):
    """gridlines + tick labels -> function y -> value (piecewise straight)."""
    gl = [float(attrs(t)['y1']) for t in re.findall(r'<line class="gl"[^>]*>', svg)]
    yt = texts(svg, 'yt')
    assert len(gl) == len(yt) and len(gl) >= 2
    pts = []
    for g, t in zip(gl, yt):
        assert t['_t'] == num(Fr(t['data-v'])), 'tick text'
        assert abs(float(t['y']) - g - 4) < 1 or abs(float(t['y']) - g - 3.5) < 1, 'tick label off its line'
        pts.append((g, Fr(t['_t'])))
    pts.sort(key=lambda p: -p[0])  # bottom first
    for i in range(1, len(pts)): assert pts[i][1] > pts[i - 1][1]
    def f(y):
        for (y0, v0), (y1, v1) in zip(pts, pts[1:]):
            if y1 - 0.06 <= y <= y0 + 0.06:
                return v0 + (v1 - v0) * Fr(round((y0 - y) * 100), round((y0 - y1) * 100))
        raise AssertionError('y off scale')
    return f, pts

def read_bar(svg, need_grid=True):
    f, pts = yscale(svg)
    xl = texts(svg, 'xl'); bars = []
    for t in re.findall(r'<rect class="bar"[^>]*>', svg):
        a = attrs(t); x = float(a['x']) + float(a['width']) / 2; top = float(a['y'])
        assert abs(top + float(a['height']) - 180) < 0.11, 'bar not on the axis'
        v = f(top)
        # snap to 1/2-step accuracy and require exactness
        vr = Fr(round(float(v) * 2), 2)
        assert abs(float(v) - float(vr)) < 0.02, f'bar value not readable {float(v)}'
        if need_grid: assert any(vr == p[1] for p in pts), 'bar top not on a gridline'
        lab = min(xl, key=lambda t: abs(float(t['x']) - x))
        assert abs(float(lab['x']) - x) < 0.2, 'label not under bar'
        bars.append((lab['_t'], vr, float(a['width'])))
    return bars, pts

def read_pie(svg):
    secs = []
    leg = {}
    for m in re.finditer(r'<rect x="214" y="([\d.]+)"[^>]*fill="([^"]+)"/><text class="lg"[^>]*>(.*?)</text>', svg):
        leg[m.group(2)] = H.unescape(m.group(3))
    pa = texts(svg, 'pa')
    for t in re.findall(r'<path class="sec"[^>]*>', svg):
        a = attrs(t); d = a['d']
        n = [float(x) for x in re.findall(r'-?[\d.]+', d)]
        cx, cy, x0, y0, r = n[0], n[1], n[2], n[3], n[4]
        large, sweep, x1, y1 = int(n[7]), int(n[8]), n[9], n[10]
        assert abs(math.hypot(x0 - cx, y0 - cy) - r) < 0.05 and abs(math.hypot(x1 - cx, y1 - cy) - r) < 0.05
        a0 = math.degrees(math.atan2(y0 - cy, x0 - cx)); a1 = math.degrees(math.atan2(y1 - cy, x1 - cx))
        ang = (a1 - a0) % 360
        assert abs(ang - 180) < 0.01 or (ang > 180) == bool(large), 'large-arc flag'
        secs.append({'cat': leg[a['fill']], 'ang': ang, 'mid': math.radians(a0 + ang / 2), 'cx': cx, 'cy': cy, 'r': r})
    assert abs(sum(s['ang'] for s in secs) - 360) < 0.05
    for s in secs:  # sector labels must sit inside their own sector
        for t in pa:
            lx, ly = float(t['x']), float(t['y']) - 5
            ang = math.atan2(ly - s['cy'], lx - s['cx'])
            if abs(math.hypot(lx - s['cx'], ly - s['cy']) - s['r'] * .6) < 1 and abs(((ang - s['mid'] + math.pi) % (2 * math.pi)) - math.pi) < 0.02:
                s['label'] = t['_t']
    return secs

def read_dots(svg):
    lx = texts(svg, 'lx'); vals = []
    stacks = Counter()
    for t in re.findall(r'<circle class="dot"[^>]*>', svg):
        a = attrs(t); x = float(a['cx'])
        lab = min(lx, key=lambda t: abs(float(t['x']) - x)); assert abs(float(lab['x']) - x) < 0.2
        v = int(lab['_t']); stacks[(v, a['cy'])] += 1; vals.append(v)
    assert all(c == 1 for c in stacks.values()), 'dots on top of each other'
    return vals

def read_hist(svg):
    f, pts = yscale(svg)
    hx = texts(svg, 'hx'); out = []
    for t in re.findall(r'<rect class="hb"[^>]*>', svg):
        a = attrs(t); x0 = float(a['x']); x1 = x0 + float(a['width'])
        L = min(hx, key=lambda t: abs(float(t['x']) - x0)); R = min(hx, key=lambda t: abs(float(t['x']) - x1))
        assert abs(float(L['x']) - x0) < 0.2 and abs(float(R['x']) - x1) < 0.2
        v = f(float(a['y'])); vr = round(float(v)); assert abs(float(v) - vr) < 0.02 and any(p[1] == vr for p in pts)
        out.append((int(L['_t']), int(R['_t']), vr))
    out.sort()
    w = {b - a for a, b, _ in out}; assert len(w) == 1, 'unequal classes'
    for (a, b, _), (c, d, _) in zip(out, out[1:]): assert b == c, 'gap between classes'
    return out

def read_table(h):
    rows = re.findall(r'<tr>(.*?)</tr>', h, re.S)
    head = [H.unescape(re.sub('<[^>]+>', '', c)) for c in re.findall(r'<th[^>]*>(.*?)</th>', rows[0])]
    body = [[H.unescape(re.sub('<[^>]+>', '', c)) for c in re.findall(r'<td[^>]*>(.*?)</td>', r)] for r in rows[1:]]
    return head, body

def read_sl(h):
    t = re.search(r'<table class="sl".*?</table>', h, re.S).group(0)
    vals = []; prev = None
    for st, lv in re.findall(r'<td class="st"[^>]*>(\d+)</td><td class="lv"[^>]*>(.*?)</td>', t):
        st = int(st); ls = [int(x) for x in lv.replace('&nbsp;', ' ').split()]
        assert ls == sorted(ls), 'leaves not in order'
        if prev is not None: assert st == prev + 1, 'missing stem'
        prev = st; vals += [st * 10 + l for l in ls]
    k = re.search(r'Key: (\d+) \| (\d) = (\d+) ', h)
    assert k and int(k.group(1)) * 10 + int(k.group(2)) == int(k.group(3)) and int(k.group(3)) in vals, 'bad key'
    return vals

def read_btb(h):
    t = re.search(r'<table class="btb".*?</table>', h, re.S).group(0)
    na = H.unescape(re.search(r'class="na">(.*?)</th>', t).group(1)); nb = H.unescape(re.search(r'class="nb">(.*?)</th>', t).group(1))
    A = []; B = []; prev = None
    for la, st, lv in re.findall(r'<td class="la"[^>]*>(.*?)</td><td class="st"[^>]*>(\d+)</td><td class="lv"[^>]*>(.*?)</td>', t):
        st = int(st); l1 = [int(x) for x in la.replace('&nbsp;', ' ').split()]; l2 = [int(x) for x in lv.replace('&nbsp;', ' ').split()]
        assert l1 == sorted(l1, reverse=True), 'left leaves must grow outwards'
        assert l2 == sorted(l2), 'right leaves not in order'
        if prev is not None: assert st == prev + 1
        prev = st; A += [st * 10 + l for l in l1]; B += [st * 10 + l for l in l2]
    k = re.search(r'Key: (\d) \| (\d+) \| (\d) = (\d+) for (.+?) and (\d+) for (.+?)</p>', h)
    if k:
        s = int(k.group(2)); assert int(k.group(4)) == s * 10 + int(k.group(1)) and int(k.group(6)) == s * 10 + int(k.group(3))
        assert k.group(5) == na and k.group(7) == nb and int(k.group(4)) in A and int(k.group(6)) in B, 'bad key'
    else:
        k = re.search(r'Key: (\d) \| (\d+) = (\d+) for (.+?)</p>', h); assert k and int(k.group(3)) == int(k.group(2)) * 10 + int(k.group(1)) and int(k.group(3)) in A
    return na, nb, A, B

# ---------- own classifiers (written separately from the game's lists) ----------
def best_display(s):
    s = s.lower()
    if re.search(r'compare.*(boys and girls|two classes|two groups)|(boys and girls|two classes).*compare', s): return 'Back-to-back stem-and-leaf plot'
    if re.search(r'share of the whole|fraction of all|parts? of (a|the) whole', s): return 'Pie chart'
    if re.search(r'classes|grouped', s): return 'Histogram'
    if re.search(r'dot', s): return 'Line plot'
    if re.search(r'keeps? every|keep every', s): return 'Stem-and-leaf plot'
    if re.search(r'compare (the number|how many)', s): return 'Bar chart'
    raise AssertionError('display: no rule fits ' + s)

problems = []
def bad(q, msg): problems.append((q.get('mk'), msg, q['en'][:110], q['answer'], q['wrong']))

def check(q):
    en, fr, h, ans, wr = q['en'], q['frame'] or '', q['html'] or '', q['answer'], q['wrong']
    t = q['data'].get('t')
    alltext = json.dumps(q, ensure_ascii=False)
    if re.search(r'undefined|NaN|null|Infinity', en + fr + (q['why'] or '') + ans + ''.join(wr)): return bad(q, 'undefined/NaN')
    if len(wr) != 3 or len(set(wr)) != 3 or ans in wr: return bad(q, 'options')
    numeric = bool(re.fullmatch(r'[\d./]+[°%]?', ans))
    if re.search(r'\b(\w+) \1\b', en + ' ' + fr + ' ' + (q['why'] or '')): return bad(q, 'doubled word')
    if numeric:
        try:
            av = val(ans)
            for w in wr:
                if val(w) == av: return bad(q, 'wrong option equal in value')
                if val(w) < 0: return bad(q, 'negative option')
        except Exception as e:
            return bad(q, 'option format ' + str(e))
        bare = ans.replace('°', '').replace('%', '')
        if '/' not in bare and not re.search(r'(?<![\d.])' + re.escape(bare) + r'(?![\d])', q['why']): return bad(q, 'why does not show the answer')
    exp = None
    L = lambda s: [int(x) for x in re.findall(r'\d+', s)]
    if t in ('mean', 'median', 'mode', 'range'):
        a = L(fr); n = int(re.search(r'(\d+) (?:matches|games|students|days)', en).group(1)) if re.search(r'(\d+) (?:matches|games|students|days)', en) else len(a)
        if n != len(a): return bad(q, 'count in text != list length')
        if t == 'mean':
            m = Fr(sum(a), len(a)); assert (m * 10).denominator == 1; exp = num(m)
        elif t == 'median': exp = num(median(a))
        elif t == 'mode':
            c = Counter(a).most_common(); assert c[0][1] > c[1][1], 'no unique mode'; exp = num(c[0][0])
        else: exp = num(max(a) - min(a))
    elif t == 'missing':
        n, m = map(int, re.search(r'The mean of (\d+) numbers is (\d+)', en).groups()); a = L(fr)
        assert len(a) == n - 1 and fr.endswith('?'); exp = num(n * m - sum(a))
    elif t == 'newmean':
        n, m = map(int, re.search(r'over (\d+) \w+ is (\d+)\.', en).groups() if re.search(r'over (\d+) \w+ is (\d+)\.', en) else re.search(r'in (\d+) \w+ is (\d+)\.', en).groups())
        x = int(re.search(r'result is (\d+)', en).group(1)); nm = Fr(n * m + x, n + 1); assert (nm * 10).denominator == 1; exp = num(nm)
    elif t in ('fmean', 'fmedian', 'fmode'):
        head, body = read_table(h); xs = [int(r[0]) for r in body]; fs = [int(r[1]) for r in body]
        N = sum(fs); assert str(N) in en.split('.')[0], 'total in text'
        if t == 'fmean':
            m = Fr(sum(x * f for x, f in zip(xs, fs)), N)
            if '1 decimal place' in en: exp = num(half_up_1(m))
            else: assert (m * 10).denominator == 1, 'mean not exact but no rounding asked'; exp = num(m)
        elif t == 'fmedian':
            exp = num(median([x for x, f in zip(xs, fs) for _ in range(f)]))
        else:
            mf = max(fs); assert fs.count(mf) == 1; exp = num(xs[fs.index(mf)])
    elif t == 'grouped':
        head, body = read_table(h); cl = [tuple(map(int, r[0].split('–'))) for r in body]; fs = [int(r[1]) for r in body]
        assert all(b - a == cl[0][1] - cl[0][0] for a, b in cl) and all(cl[i][1] == cl[i + 1][0] for i in range(len(cl) - 1))
        N = sum(fs); assert str(N) in en; m = Fr(sum(Fr(a + b, 2) * f for (a, b), f in zip(cl, fs)), N); exp = num(half_up_1(m))
    elif t and t.startswith('bar'):
        svg = charts(h)[0]; bars, _ = read_bar(svg); cats = [b[0] for b in bars]; v = {b[0]: b[1] for b in bars}
        if t == 'barread': c = re.search(r'(?:said|were) (\w+)\?', en).group(1); exp = num(v[c])
        elif t == 'bartotal': exp = num(sum(v.values()))
        elif t == 'bardiff':
            a, b = re.search(r'(?:said|were) (\w+) than (\w+)\?', en).groups(); assert v[a] > v[b]; exp = num(v[a] - v[b])
        elif t == 'barmode':
            mx = max(v.values()); top = [c for c in cats if v[c] == mx]; assert len(top) == 1; exp = top[0]
        elif t == 'barpct':
            N = int(re.search(r'\((\d+) ', en).group(1)); assert sum(v.values()) == N, 'bars do not add to N'
            c = re.search(r'(?:said|were) (\w+)\?', en).group(1); exp = num(v[c] * 100 / Fr(N)) + '%'
    elif t == 'pieangle':
        head, body = read_table(h); fs = {r[0]: int(r[1]) for r in body}; N = sum(fs.values())
        assert 360 % N == 0; c = re.search(r'of the (\w+) sector', en).group(1); exp = num(Fr(fs[c] * 360, N)) + '°'
    elif t in ('piefreq', 'piefrac', 'piebig'):
        secs = read_pie(charts(h)[0])
        for s in secs:
            if 'label' in s: assert abs(float(s['label'].rstrip('°')) - s['ang']) < 0.05, 'pie label does not match the drawing'
        ang = {s['cat']: Fr(round(s['ang'] * 1000), 1000) for s in secs}
        ang = {k: Fr(round(float(a))) if abs(float(a) - round(float(a))) < 0.01 else a for k, a in ang.items()}
        if t == 'piefreq':
            N = int(re.search(r'\((\d+) [\w ]+ in total\)', en).group(1)); c = re.search(r'(?:said|were) (\w+)\?', en).group(1)
            f = ang[c] * N / 360; assert f.denominator == 1; assert sum(a * N / 360 for a in ang.values()) == N; exp = num(f)
        elif t == 'piefrac':
            c = re.search(r'(?:said|were) (\w+)\?', en).group(1); f = ang[c] / 360
            exp = f"{f.numerator}/{f.denominator}"
        else:
            least = 'LEAST' in en; tgt = min(ang.values()) if least else max(ang.values())
            top = [k for k, a in ang.items() if a == tgt]; assert len(top) == 1
            srt = sorted(ang.values()); assert all(b - a >= 24 for a, b in zip(srt, srt[1:])), 'slices too close to compare by eye'
            exp = top[0]
    elif t and t.startswith('dot'):
        v = read_dots(charts(h)[0])
        if t == 'dotn': exp = num(len(v))
        elif t == 'dotmode':
            c = Counter(v).most_common(); assert c[0][1] > c[1][1]; exp = num(c[0][0])
        elif t == 'dotrange': exp = num(max(v) - min(v))
        else: exp = num(median(v))
    elif t and t.startswith('hist'):
        hb = read_hist(charts(h)[0]); N = sum(f for _, _, f in hb); lab = lambda a, b: f'{a}–{b}'
        if t == 'histclass':
            c = re.search(r'in the (\d+)–(\d+) class', en).groups(); exp = num([f for a, b, f in hb if (a, b) == tuple(map(int, c))][0])
        elif t == 'histtotal': exp = num(N)
        elif t == 'histatleast':
            x = int(re.search(r'at least (\d+)\?', en).group(1)); assert any(a == x for a, _, _ in hb); exp = num(sum(f for a, _, f in hb if a >= x))
        elif t == 'histmodal':
            mx = max(f for *_, f in hb); top = [lab(a, b) for a, b, f in hb if f == mx]; assert len(top) == 1; exp = top[0]
        else:
            n2 = int(re.search(r'\((\d+) ', en).group(1)); assert n2 == N
            cum = 0; where = set()
            for a, b, f in hb:
                for i in range(f):
                    cum += 1
                    if cum in (math.floor((N + 1) / 2), math.ceil((N + 1) / 2)): where.add(lab(a, b))
            assert len(where) == 1; exp = where.pop()
    elif t and t.startswith('sl'):
        v = read_sl(h); n = len(v)
        if t == 'slmedian': exp = num(median(v))
        elif t == 'slrange': exp = num(max(v) - min(v))
        elif t == 'slmode':
            c = Counter(v).most_common(); assert c[0][1] > c[1][1]; exp = num(c[0][0])
        elif t == 'slmore': x = int(re.search(r'MORE THAN (\d+)', en).group(1)); exp = num(sum(1 for a in v if a > x))
        elif t == 'sln': exp = num(n)
        elif t == 'slmax': exp = num(max(v))
        elif t == 'slmin': exp = num(min(v))
    elif t and t.startswith('btb'):
        na, nb, A, B = read_btb(h); G = {na: A, nb: B}
        if t in ('btbmedian', 'btbrange'):
            g = re.search(r'for (.+?)\?$', en).group(1); X = G[g]
            exp = num(median(X)) if t == 'btbmedian' else num(max(X) - min(X))
        elif t == 'btbhigher':
            assert median(A) != median(B); exp = na if median(A) > median(B) else nb
        elif t == 'btbdiff': exp = num(abs(median(A) - median(B)))
        else:
            def truth(s):
                m = re.match(r'(.+) has the higher median$', s)
                if m: o = nb if m.group(1) == na else na; return median(G[m.group(1)]) > median(G[o])
                m = re.match(r'(.+) has the bigger range$', s)
                if m: o = nb if m.group(1) == na else na; r = lambda X: max(X) - min(X); return r(G[m.group(1)]) > r(G[o])
                if s == 'Both groups have the same median': return median(A) == median(B)
                if s == 'Both groups have the same range': return max(A) - min(A) == max(B) - min(B)
                raise AssertionError('unknown statement ' + s)
            tr = [o for o in [ans] + wr if truth(o)]
            assert len(tr) == 1, f'{len(tr)} true statements'; exp = tr[0]
    elif t == 'display':
        exp = best_display(fr)
    elif t == 'bestavg':
        if 'only one you can use' in en:
            items = fr.split(': ', 1)[1].rstrip('.').split(', '); assert all(re.fullmatch(r'[a-z]+', w) for w in items); exp = 'Mode'
        elif 'TYPICAL' in en:
            a = [int(x) for x in fr.split(': ', 1)[1].rstrip('.').split(', ')]; assert len(set(a)) == len(a), 'values repeat'
            assert max(a) > 2 * median(a) and sorted(a)[-2] < Fr(3, 2) * median(a), 'no clear outlier'; exp = 'Median'
        elif 'EVERY value' in en: exp = 'Mean'
    elif t == 'effect':
        m = re.match(r'.*?: ([\d, ]+)\. One more value, (\d+), is added', en); a = [int(x) for x in m.group(1).split(', ')]; x = int(m.group(2))
        mu = Fr(sum(a), len(a)); exp = 'The mean goes up' if x > mu else 'The mean goes down' if x < mu else 'The mean stays the same'
        assert Fr(sum(a) + x, len(a) + 1).__eq__(mu) == (x == mu)
    elif t == 'mislead':
        svg = charts(h)[0]
        truth = {}
        is_pie = '<path class="sec"' in svg
        ttl = texts(svg, 'ttl'); has_title = bool(ttl and ttl[0]['_t'].strip())
        if is_pie:
            p = [int(s['_t'].rstrip('%')) for s in texts(svg, 'pa')]
            truth["The percentages add up to more than 100%"] = sum(p) > 100
            truth["The vertical axis doesn't start at 0"] = False; truth["The gaps on the vertical scale aren't equal"] = False
            truth["The bars are different widths"] = False
            secs = read_pie(svg)
            for s in secs: assert abs(float(s['label'].rstrip('%')) / sum(p) * 360 - s['ang']) < 0.05
        else:
            bars, pts = read_bar(svg, need_grid=False); tv = [p[1] for p in pts]
            truth["The vertical axis doesn't start at 0"] = tv[0] > 0
            d = {b - a for a, b in zip(tv, tv[1:])}; truth["The gaps on the vertical scale aren't equal"] = len(d) > 1
            truth["The percentages add up to more than 100%"] = False
            truth["The bars are different widths"] = len({round(b[2], 1) for b in bars}) > 1
        truth["The chart has no title"] = not has_title
        tr = [o for o in [ans] + wr if truth[o]]; assert len(tr) == 1, f'{len(tr)} true reasons'; exp = tr[0]
    elif t == 'samplelimit':
        k = int(re.search(r'(\d+) of them', en).group(1)); n = int(re.search(r'asked \D*?(\d+)', en).group(1))
        ok = [o for o in [ans] + wr if re.match(rf'{k} of .*{n}', o) and 'sample' in o and not re.match(r'(Most|All|Exactly)', o)]
        assert len(ok) == 1; exp = ok[0]
    else:
        return bad(q, 'unknown type ' + str(t))
    if exp != ans: bad(q, f'expected {exp}')

if __name__ == '__main__':
    data = json.load(open(sys.argv[1]))
    n = 0
    for q in data:
        n += 1
        try: check(q)
        except Exception as e: bad(q, 'ERROR ' + repr(e)[:150])
    c = Counter(p[0] for p in problems)
    print(f'{n} questions, {len(problems)} problems', dict(c))
    for p in problems[:12]: print(p)
    sys.exit(1 if problems else 0)
