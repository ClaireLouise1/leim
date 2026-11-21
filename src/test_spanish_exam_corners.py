#!/usr/bin/env python3
"""Checks the Spanish Exam corners (src/spanish_exam_corner_data.py + the built pages).

  python3 src/test_spanish_exam_corners.py          # exit 1 on any problem
Needs: pip install --break-system-packages wordfreq
Spanish spelling: every word must be a common Spanish word (wordfreq zipf >= 2), and not a
missing-accent form of a much commoner word (habitacion → habitación). Names go in OK_WORDS.
(pyspellchecker's Spanish list was tried and is missing words like soy / años / gracias.)
"""
import os, re, sys, json
from html.parser import HTMLParser
sys.path.insert(0, os.path.dirname(__file__))
ROOT = os.path.join(os.path.dirname(__file__), '..')

OK_WORDS = {'aoife', 'brennan', 'galway', 'irlanda', 'javier', 'niamh', 'kilkenny', 'valencia', 'madrid', 'raúl', 'lucía', 'salamanca',
            'seán', 'cork', 'ballincollig', 'ayudarle', 'preocupes', 'be', 'erre', 'ene', 'sevilla',
            'toledo', 'marta', 'ciara', 'málaga', 'pablo', 'clodagh', 'athlone'}
VOID = {'br', 'img', 'hr', 'input', 'meta', 'link', 'source', 'wbr'}


def text(h):
    return re.sub(r'<[^>]+>', ' ', h)


def spanish_words(s):
    return [w.lower() for w in re.findall(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+", s)]


class Balance(HTMLParser):
    def __init__(self):
        super().__init__(); self.stack = []; self.bad = []
    def handle_starttag(self, t, a):
        if t not in VOID: self.stack.append(t)
    def handle_endtag(self, t):
        if t in VOID: return
        if not self.stack or self.stack[-1] != t:
            # <li> / <p> may close implicitly
            while self.stack and self.stack[-1] in ('li', 'p') and self.stack[-1] != t: self.stack.pop()
            if not self.stack or self.stack[-1] != t: self.bad.append(t); return
        self.stack.pop()


def check(corners, pages):
    from wordfreq import zipf_frequency as zf
    ACC = {'a': 'á', 'e': 'é', 'i': 'í', 'o': 'ó', 'u': 'ú', 'n': 'ñ'}
    def bad(w):
        f = zf(w, 'es')
        if f < 2.0: return True
        for j, ch in enumerate(w):
            if ch in ACC:
                v = w[:j] + ACC[ch] + w[j + 1:]
                if zf(v, 'es') - f > 1.0 and f < 4.0: return True
        return False
    probs = []
    for slug, c in corners.items():
        es = []
        for i, k in enumerate(c['tasks']):
            for key in ('title', 'q', 'model', 'marks'):
                if not k.get(key): probs.append(f'{slug} task {i}: no {key}')
            if k['kind'] == 'listen':
                who = k['audio']['who']
                for L in k['audio']['lines']:
                    if L[0] >= len(who): probs.append(f'{slug} task {i}: bad speaker {L}')
                    if '<' in L[1]: probs.append(f'{slug} task {i}: HTML in audio {L[1]}')
                    es.append(L[1])
            elif k['kind'] == 'read':
                es.append(text(k['text']))
            elif k['kind'] == 'write':
                es.append(text(k['model']))
            if k['kind'] in ('listen', 'read'):
                labels = re.findall(r'\(([a-z])\)', k['model'])
                want = [chr(97 + j) for j in range(len(k['qs']))]
                if labels != want: probs.append(f'{slug} task {i}: model labels {labels} ≠ questions {want}')
            if k['kind'] == 'listen':
                heard = ' '.join(L[1] for L in k['audio']['lines']).lower()
                for num, word in (('14', 'catorce'), ('15', 'quince'), ('13', 'trece'), ('three', 'tres')):
                    if f'<b>{num}</b>' in k['model'].lower() or f'<b>{num} ' in k['model'].lower() or f'<b>{num}</b>' in k['model']:
                        if word not in heard: probs.append(f'{slug} task {i}: answer {num} but "{word}" is not in the audio')
        unknown = sorted(set(w for s in es for w in spanish_words(s) if w not in OK_WORDS and bad(w)))
        if unknown: probs.append(f'{slug}: Spanish words not in the dictionary: {unknown}')
        page = pages[slug]
        if page.count('<!--sec-->') != 1 or page.count('id="exam"') != 1: probs.append(f'{slug}: corner not on the page exactly once')
        blk = page[page.find('<!--sec-->'):page.find('<!--/sec-->')]
        if 'payhip' in blk.lower(): probs.append(f'{slug}: Payhip link in the corner')
        b = Balance(); b.feed(blk.replace('<!--sec-->', ''))
        if b.bad or b.stack: probs.append(f'{slug}: unbalanced HTML {b.bad} {b.stack}')
        ids = re.findall(r'data-au="([^"]+)"', blk)
        m = re.search(r'var DATA=(\{.*?\});\n', page)
        data = json.loads(m.group(1)) if m else {}
        if sorted(ids) != sorted(data): probs.append(f'{slug}: audio boxes {ids} ≠ player data {list(data)}')
        if ids and page.count('id="auRate"') != 1: probs.append(f'{slug}: speed control missing or doubled')
        if page.find('<!--sec-->') > page.find('<div class="actions"><a class="btn" href="#game">'): probs.append(f'{slug}: corner after the buttons')
        if page.find('<!--sec-->') < page.find('id="revise"'): probs.append(f'{slug}: corner outside the rules panel')
    return probs


if __name__ == '__main__':
    from spanish_exam_corner_data import CORNERS
    pages = {s: open(os.path.join(ROOT, s + '.html'), encoding='utf-8').read() for s in CORNERS}
    p = check(CORNERS, pages)
    for x in p: print('✗', x)
    n = sum(len(c['tasks']) for c in CORNERS.values())
    print(f'{len(CORNERS)} page(s), {n} tasks: {len(p)} problem(s)')
    sys.exit(1 if p else 0)
