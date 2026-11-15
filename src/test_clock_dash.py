#!/usr/bin/env python3
"""Independent checker for Clock Dash. node src/test_clock_dash.js > /tmp/cd.json ; python3 src/test_clock_dash.py /tmp/cd.json
Re-derives every answer from the question TEXT, the clock hands in the SVG and the timetable cells, with exact fractions."""
import json, re, sys, math
from fractions import Fraction as F
d = json.load(open(sys.argv[1]))
U = {'mm': 1, 'cm': 10, 'm': 1000, 'km': 10**6, 'g': 1, 'kg': 1000, 't': 10**6, 'ml': 1, 'l': 1000}
def tmin(s):
    m = re.fullmatch(r'(\d{1,2}):(\d{2})( am| pm)?', s.strip()); assert m, s
    h = int(m[1])
    if m[3]:
        assert 1 <= h <= 12, s; h = h % 12 + (12 if m[3] == ' pm' else 0)
    else: assert len(m[1]) == 2 and h < 24, s
    assert int(m[2]) < 60, s
    return h * 60 + int(m[2])
def dmin(s, lenient=False):
    m = re.fullmatch(r'(?:(\d+) h)?(?: ?(\d+) min)?', s.strip()); assert m and (m[1] or m[2]), s
    if m[2] and not lenient: assert 0 < int(m[2]) < 60 or not m[1], s
    return int(m[1] or 0) * 60 + int(m[2] or 0)
def qty(s):
    m = re.fullmatch(r'([\d.]+) (mm|cm|m|km|g|kg|t|ml|l)', s.strip()); assert m, s
    return F(m[1]) * U[m[2]], m[2]
def val(s, lenient=False):
    s = s.strip()
    if re.fullmatch(r'\d{1,2}:\d{2}( am| pm)?', s): return tmin(s)
    if re.fullmatch(r'(\d+ h)?( ?\d+ min)?', s) and s: return dmin(s, lenient)
    if re.fullmatch(r'[\d.]+ h', s): return F(s[:-2]) * 60
    if re.fullmatch(r'[\d.]+ [a-z]+', s): return qty(s)[0]
    return F(s)
def hm(m): m %= 1440; return '%02d:%02d' % (m // 60, m % 60)
def t12(m): m %= 1440; h = m // 60; return '%d:%02d %s' % (h % 12 or 12, m % 60, 'am' if h < 12 else 'pm')
def dur(m): h, r = divmod(m, 60); return f'{h} h {r} min' if h and r else (f'{h} h' if h else f'{r} min')
def dec(x):
    x = F(x); k = 0
    while (x * 10 ** k).denominator != 1: k += 1
    s = str((x * 10 ** k).numerator).rjust(k + 1, '0'); s = s[:len(s) - k] + ('.' + s[len(s) - k:] if k else ''); return s
probs = []
def bad(q, msg): probs.append((q['mk'], msg, q['en'], q['frame'], q['answer'], q['wrong']))
def numeric(q, true_str):
    if q['answer'] != true_str: bad(q, 'answer should be ' + true_str); return
    try: vs = [val(w, True) for w in q['wrong']]; a = val(q['answer'])
    except AssertionError as e: bad(q, 'bad format ' + str(e)); return
    if len(set(vs)) < 3 or a in vs or any(v <= 0 for v in vs): bad(q, 'wrong options clash')
TIME = r'(\d{2}:\d{2})'
for q in d:
    t = q['data'].get('t'); en = q['en']; fr = q['frame'] or ''
    txt = en + ' ' + fr + ' ' + q['answer'] + ' ' + ' '.join(q['wrong']) + ' ' + q['why']
    if len(q['wrong']) != 3 or q['answer'] in q['wrong']: bad(q, 'options'); continue
    if re.search(r'NaN|undefined|null|Infinity|\b1 hs\b|\b0 h\b', txt): bad(q, 'junk in text'); continue
    try:
        if t == 'to24': numeric(q, hm(tmin(fr)))
        elif t == 'to12': numeric(q, t12(tmin(fr)))
        elif t == 'clock':
            g = lambda c: [float(x) for x in re.search(r'class="%s" x1="100" y1="100" x2="([\d.]+)" y2="([\d.]+)"' % c, q['html']).groups()]
            mx, my = g('mh'); hx, hy = g('hh')
            ma = math.degrees(math.atan2(mx - 100, 100 - my)) % 360; mi = round(ma / 6) % 60
            ha = math.degrees(math.atan2(hx - 100, 100 - hy)) % 360; h = round((ha - mi * 0.5) / 30) % 12
            part = re.search(r'one (morning|afternoon|evening)', en)[1]
            H = h if part == 'morning' else (12 if h == 0 else h + 12)
            if part == 'morning' and h == 0: bad(q, 'midnight morning')
            numeric(q, hm(H * 60 + mi))
        elif t == 'dur':
            a, b = re.findall(TIME, en); numeric(q, dur(tmin(b) - tmin(a)))
        elif t == 'add':
            a = re.search(TIME, en)[1]; dd = re.search(r'(?:takes|needs|lasts) ((?:\d+ h)?(?: ?\d+ min)?)\.', en)[1]
            numeric(q, hm(tmin(a) + dmin(dd)))
        elif t == 'conv':
            m = re.fullmatch(r'([\d.]+ \w+) = \? (\w+)', fr); base, _ = qty(m[1]); u = m[2]
            numeric(q, dec(base / U[u]) + ' ' + u)
        elif t == 'order':
            opts = [q['answer']] + q['wrong']; vals = [qty(o)[0] for o in opts]
            kinds = {('length' if qty(o)[1] in ('mm', 'cm', 'm', 'km') else 'mass' if qty(o)[1] in ('g', 'kg', 't') else 'cap') for o in opts}
            if len(kinds) != 1 or len(set(vals)) != 4: bad(q, 'order opts'); continue
            big = bool(re.search(r'longest|heaviest|most', en))
            if vals[0] != (max(vals) if big else min(vals)): bad(q, 'order answer')
        elif t == 'addu':
            amts = re.findall(r'([\d.]+ (?:mm|cm|m|km|g|kg|t|ml|l))\b', en)
            u = re.search(r'in (litres|ml|mm|cm|m|km|g|kg|t)\?', en)[1]; u = 'l' if u == 'litres' else u
            tot = sum(qty(a)[0] for a in amts); numeric(q, dec(tot / U[u]) + ' ' + u)
        elif t == 'pieces':
            amts = re.findall(r'([\d.]+ (?:mm|cm|m|km|g|kg|t|ml|l))\b', en)
            vals = sorted(qty(a)[0] for a in amts); n = vals[1] / vals[0]
            if n.denominator != 1: bad(q, 'not whole'); continue
            numeric(q, str(n))
        elif t == 'm2h': numeric(q, dec(F(dmin(fr), 60)) + ' h')
        elif t == 'h2m': numeric(q, dur(int(F(fr[:-2]) * 60)))
        elif t == 'tot':
            if (m := re.search(r'minutes are in (.+)\?', en)): numeric(q, str(dmin(m[1])))
            elif (m := re.search(r'seconds are in ([\d.]+) minutes', en)): numeric(q, dec(F(m[1]) * 60))
            elif (m := re.search(r'hours are in (\d+) days', en)): numeric(q, str(int(m[1]) * 24))
            elif (m := re.search(r'hours are in (\d+) weeks', en)): numeric(q, str(int(m[1]) * 168))
            else: bad(q, 'tot parse')
        elif t == 'cook':
            m = re.search(r'needs (\d+) minutes per kg plus (\d+) minutes\. It weighs ([\d.]+) kg', en)
            mins = int(m[1]) * F(m[3]) + int(m[2])
            if mins.denominator != 1: bad(q, 'cook frac'); continue
            st = re.search(r'goes in at ' + TIME, en)
            numeric(q, hm(tmin(st[1]) + int(mins)) if st else dur(int(mins)))
        elif t == 'tt':
            rows = re.findall(r'<tr data-stop="([^"]+)">(.*?)</tr>', q['html'])
            S = [r[0] for r in rows]; cells = [re.findall(r'<td[^>]*>([^<]+)</td>', r[1]) for r in rows]
            T = [[None if c == '—' else tmin(c) for c in col] for col in zip(*cells)]  # T[bus][stop]
            if len(S) != 4 or len(T) != 4: bad(q, 'table shape'); continue
            for b in T:
                ts = [x for x in b if x is not None]
                if ts != sorted(ts) or len(set(ts)) != len(ts) or b[0] is None or b[3] is None: bad(q, 'table times not increasing'); break
            deps = [hm(b[0]) for b in T]
            k = q['data']['k']
            if k == 'jt':
                m = re.match(r'How long does the ' + TIME + r' bus from (.+?) take to get to (.+?)\?', en)
                b = deps.index(m[1]); i, j = S.index(m[2]), S.index(m[3]); numeric(q, dur(T[b][j] - T[b][i]))
            elif k == 'latest':
                m = re.match(r'You need to be at (.+?) by ' + TIME + r'\. What\'s the latest bus you can catch from (.+?)\?', en)
                j, lim, i = S.index(m[1]), tmin(m[2]), S.index(m[3])
                ok = [b for b in T if b[j] is not None and b[j] <= lim]
                want = hm(max(b[i] for b in ok))
                if want != q['answer'] or sorted([q['answer']] + q['wrong']) != sorted(deps): bad(q, 'latest')
            elif k == 'wait':
                m = re.match(r'You get to the (.+?) stop at ' + TIME, en); j, t0 = S.index(m[1]), tmin(m[2])
                nxt = min(b[j] for b in T if b[j] is not None and b[j] > t0)
                if any(b[j] == t0 for b in T): bad(q, 'bus at that minute')
                numeric(q, dur(nxt - t0))
            elif k == 'quick':
                js = [b[3] - b[0] for b in T]
                if js.count(min(js)) != 1 or q['answer'] != deps[js.index(min(js))]: bad(q, 'quick')
            elif k == 'skip':
                j = S.index(re.match(r'Which bus does not stop at (.+?)\?', en)[1])
                miss = [deps[i] for i, b in enumerate(T) if b[j] is None]
                if miss != [q['answer']]: bad(q, 'skip')
        else: bad(q, 'unknown type')
    except (AssertionError, TypeError, AttributeError, ValueError) as e:
        bad(q, 'parse ' + repr(e))
print(len(d), 'questions checked,', len(probs), 'problems')
for p in probs[:15]: print(p)
sys.exit(1 if probs else 0)
