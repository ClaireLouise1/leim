"""Find a short Shakespeare quote in the NLTK Shakespeare corpus (Bosak's XML editions) and return who says it and where.
Setup: pip install --break-system-packages nltk ; NLTK_ALLOW_PROXIED_URLOPEN=1 python3 -c "import nltk; nltk.download('shakespeare')"
Plays used on Leim (on the JC 2028-30 list and in the corpus): rj = Romeo and Juliet, mv = The Merchant of Venice, jc = Julius Caesar.
(As You Like It is on the list too but is not in the corpus.)"""
import re
from nltk.corpus import shakespeare as _S
FILES = {"rj": "r_and_j.xml", "mv": "merchant.xml", "jc": "j_caesar.xml"}
ROMAN = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6, "VII": 7, "VIII": 8, "IX": 9}
def words(s):
    s = s.lower().replace("’", "'").replace("‘", "'")
    s = s.replace("-", "")
    return re.findall(r"[a-z]+(?:'[a-z]+)*", s)
_CACHE = {}
def speeches(play):
    """List of dicts: speaker(s), act, scene, words, pos (order in the play), asides (lines marked Aside)."""
    if play in _CACHE: return _CACHE[play]
    out, pos = [], 0
    root = _S.xml(FILES[play])
    for a in root.findall("ACT"):
        act = ROMAN[a.find("TITLE").text.split()[1]]
        for sc in a.findall("SCENE"):
            scene = ROMAN[re.sub(r"[^IVX]", "", sc.find("TITLE").text.split()[1])]
            for sp in sc.iter("SPEECH"):
                who = [x.text.strip().upper() for x in sp.findall("SPEAKER") if x.text]
                lines = []
                for ln in sp.findall("LINE"):
                    lines.append("".join(ln.itertext()))
                txt = " ".join(lines)
                out.append({"who": who, "act": act, "scene": scene, "w": words(txt), "pos": pos, "text": txt})
                pos += 1
    _CACHE[play] = out
    return out
def find(play, quote):
    """All speeches in which the quote's words appear in order, next to each other."""
    q = words(quote); n = len(q); hits = []
    for sp in speeches(play):
        w = sp["w"]
        for i in range(len(w) - n + 1):
            if w[i:i + n] == q:
                hits.append(sp); break
    return hits
def where(play, quote):
    """(speaker, act, scene, pos) of the speech holding the quote; raises if it is missing or two different speakers/scenes say it."""
    h = find(play, quote)
    if not h or len({(x["who"][0], x["act"], x["scene"]) for x in h}) != 1:
        raise ValueError("%s: %r found %d times" % (play, quote, len(h)))
    sp = h[0]
    return (sp["who"][0], sp["act"], sp["scene"], sp["pos"])
