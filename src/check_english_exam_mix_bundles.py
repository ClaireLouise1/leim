#!/usr/bin/env python3
"""Runs each English game's OWN independent checker on the questions its Exam Mix bundle made
(written by src/test_english_exam_mix_bundles.js to $OUT/<slug>.jsonl). Proves the borrowed questions
are as right as the ones in the game itself.
Needs the checkers' libraries (spaCy + en_core_web_sm, pyspellchecker, inflect, pronouncing, nltk wordnet + shakespeare).
Usage: N=40 OUT=/tmp/eem node src/test_english_exam_mix_bundles.js && OUT=/tmp/eem python3 src/check_english_exam_mix_bundles.py [slug …]"""
import os, sys, subprocess, time
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC)
sys.path.insert(0, SRC)
from build_english_exam_mix import SECTIONS
OUT = os.environ.get("OUT", "/tmp/eem")
CHECKER = {"speech-marks-sprint": "test_speech_marks.py"}
slugs = sys.argv[1:] or [s for v in SECTIONS.values() for s in v]
fails = 0
for s in slugs:
    chk = os.path.join(SRC, CHECKER.get(s, "test_" + s.replace("-", "_") + ".py"))
    t = time.time()
    r = subprocess.run([sys.executable, chk, os.path.join(OUT, s + ".jsonl"), os.path.join(ROOT, s + ".html")],
                       capture_output=True, text=True, cwd=ROOT)
    last = (r.stdout + r.stderr).strip().splitlines()
    ok = r.returncode == 0
    fails += not ok
    print("OK  " if ok else "FAIL", s, "·", (last[-1] if last else "")[:140], "· %.0fs" % (time.time() - t), flush=True)
    if not ok:
        print("\n".join(last[-8:]))
print(f"{len(slugs) - fails}/{len(slugs)} games' checkers pass on the Exam Mix questions")
sys.exit(1 if fails else 0)
