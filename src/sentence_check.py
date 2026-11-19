"""Independent sentence-grammar checks with spaCy (en_core_web_sm), used by src/test_sentence_surgeon.py and the PDF builder.
A clause = a verb (or copula head) with its own subject. Subordinate = opened by because/when/if/that…, or a relative clause.
Setup (new session): pip install --break-system-packages spacy + the en_core_web_sm 3.8.0 wheel from github.com/explosion/spacy-models/releases."""
import spacy
nlp = spacy.load("en_core_web_sm")
SUBJ = {"nsubj", "nsubjpass", "expl"}
MARKS = {"because", "when", "although", "if", "after", "until", "while", "before", "since", "though", "unless", "that", "who", "which", "whenever"}
LINK = {"and", "but", "or", "so", "yet"}
def subj(t): return any(c.dep_ in SUBJ for c in t.children)
def is_finite(t):
    if t.pos_ in ("VERB", "AUX"):
        if t.tag_ in ("VBG", "VBN") and not any(c.dep_ in ("aux", "auxpass") for c in t.children): return False
        return True
    return any(c.dep_ in ("cop", "aux") for c in t.children)
def heads(doc): return [t for t in doc if subj(t) and is_finite(t)]
def sub(t):
    if t.dep_ in ("relcl",): return True
    return any(c.i < t.i and c.lower_ in MARKS and c.dep_ in ("mark", "advmod", "nsubj", "nsubjpass", "dobj") for c in t.children)
def imperative(doc):
    r = list(doc.sents)[0].root
    return r.tag_ == "VB" and not subj(r) and r.i <= 2
def kind(text):
    doc = nlp(text); hs = heads(doc); ind = [h for h in hs if not sub(h)]
    if not ind and not imperative(doc): return "fragment"
    ind.sort(key=lambda t: t.i)
    for a, b in zip(ind, ind[1:]):
        start = min([c.i for c in b.children if c.dep_ in SUBJ] + [b.i])
        between = [doc[i] for i in range(a.i + 1, start + 1)]
        if not any(x.lower_ in LINK for x in between): return "runon"
    return "sentence"
def structure(text):
    doc = nlp(text); hs = heads(doc)
    if len(hs) <= 1: return "si"
    if any(sub(h) for h in hs): return "cx"
    return "co"
def stype(text):
    doc = nlp(text)
    if text.endswith("?"): return "qu"
    if text.endswith("!") and doc[0].lower_ in ("what", "how"): return "ex"
    if text.endswith(".") and (imperative(doc) or (doc[0].lower_ == "don't") or (doc[0].lower_ == "do" and doc[1].lower_ in ("n't", "not"))): return "cm"
    if text.endswith(".") and heads(doc): return "st"
    return "?"
