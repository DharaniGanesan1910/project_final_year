# !pip install -q spacy stanza
# !python -m spacy download en_core_web_sm


import re
import spacy
import stanza
import pandas as pd
from google.colab import files


stanza.download("ta")

nlp_ta = stanza.Pipeline(
    lang="ta",
    processors="tokenize,mwt,pos,lemma,depparse",
    use_gpu=False
)

ROMAN_TA_VERB_SUFFIXES = (
    "ren","raan","raanga","reenga",
    "kiren","kiraan","kiraanga",
    "en","aen","aan","anga","inga",
    "ttaan","tten","ttanga",
    "ndhaan","ndhen","ndhanga",
    "ven","vaan","vaanga","pen","paan",
    "iruken","irukaan","irukaanga","irukkum",
    "iruka","iruku","irukku","irukanum",
    "poren","poran","poranga",
    "varen","varan","varanga",
    "pannen","pannaan","pannanga","panni",
    "paathen","paathaan","poguthu","podu",
    "vandhen","vandhaan","soldran","soldra",
    "pesura","va","vaa","vanga",
    "po","ponga","paru","parunga",
    "podu","podunga"
)

ROMAN_TA_NEG = (
    "illa","illai","la",
    "varala","pannala","pogala",
    "paakala","theriyala","mudiyala",
    "irukala","irukkala",
    "venam","vena",
    "koodathu","aagathu"
)

ROMAN_TA_ADVERBS = (
    "ippo","inniku","nethu","naalaiku",
    "romba","konjam","semma",
    "inge","ange","enga",
    "seekiram","late","already",
    "again","daily","always",
    "sometimes","suddena","apdiye",
    "seri","ok","correcta"
)

ROMAN_TA_PRONOUNS = (
    "naan","nee","avan","ava",
    "avanga","nanga","enga",
    "unga","ivanga","ivan","ival"
)


ROMAN_VERB_REGEX = re.compile(
    r'(tt|nd|rn|nch|ch|thu|du|ra|ren|raan|vaan|ven|kum|kir|kudhu|pudhu)$'
)

ROMAN_NEG_REGEX = re.compile(
    r'(la|illa|illai|ala|koodathu|aagathu)$'
)


def clean_split(sentence):
    sentence = re.sub(r'[^\w\s?]', '', str(sentence).lower())
    return sentence.split()

def contains_tamil_script(text):
    return bool(re.search(r'[\u0B80-\u0BFF]', str(text)))

def is_roman_verb(word):
    #  suffix list
    if word.endswith(ROMAN_TA_VERB_SUFFIXES):
        return True
    #  regex pattern
    if ROMAN_VERB_REGEX.search(word):
        return True
    return False

def has_neg(words):
    for w in words:
        if w in ROMAN_TA_NEG:
            return True
        if ROMAN_NEG_REGEX.search(w):
            return True
    return False

def has_subject(words):
    return any(w in ROMAN_TA_PRONOUNS for w in words)

def has_object(words):
    for w in words:
        if w.endswith(("a","ah")) and len(w) > 3:
            return True
    return False


def classify_roman_tamil(sentence):
    words = clean_split(sentence)
    if not words:
        return "UNKNOWN"

    verb_final = is_roman_verb(words[-1])
    neg = has_neg(words)
    subj = has_subject(words)
    obj = has_object(words)
    adv_start = words[0] in ROMAN_TA_ADVERBS if words else False
    adv_mid = any(w in ROMAN_TA_ADVERBS for w in words[1:-1])

    if adv_start and verb_final:
        return "ASOV"
    if adv_mid and verb_final:
        return "SOVA"
    if neg and verb_final:
        return "SOV-NEG"
    if subj and obj and verb_final:
        return "SOV"
    if subj and verb_final:
        return "SOV"
    if verb_final and len(words) >= 3:
        return "SOV"
    if verb_final and len(words) == 2:
        return "SV"
    if verb_final:
        return "IMP"
    if len(words) >= 3:
        return "SOV"

    return "UNKNOWN"


def classify_tamil_script(sentence):
    doc = nlp_ta(sentence)

    has_subj = False
    has_obj = False
    has_verb = False
    has_neg_flag = False

    for sent in doc.sentences:
        for word in sent.words:
            if word.deprel == "nsubj":
                has_subj = True
            if word.deprel in ("obj","dobj"):
                has_obj = True
            if word.upos in ("VERB","AUX"):
                has_verb = True
            if word.deprel == "neg":
                has_neg_flag = True

    if has_subj and has_obj and has_neg_flag:
        return "SOV-NEG"
    if has_subj and has_obj:
        return "SOV"
    if has_subj and has_verb:
        return "SV"
    if has_verb and not has_subj:
        return "IMP"
    return "UNKNOWN"




nlp_en = spacy.load("en_core_web_sm")

def classify_english(sentence):
    doc = nlp_en(sentence)

    has_subj = False
    has_obj = False
    has_verb = False
    has_neg_flag = False

    for token in doc:
        if token.dep_ == "nsubj":
            has_subj = True
        if token.dep_ in ("dobj","obj"):
            has_obj = True
        if token.pos_ in ("VERB","AUX"):
            has_verb = True
        if token.dep_ == "neg":
            has_neg_flag = True

    if has_subj and has_obj and has_neg_flag:
        return "SVO-NEG"
    if has_subj and has_obj:
        return "SVO"
    if has_subj and has_verb:
        return "SV"
    if has_verb and not has_subj:
        return "IMP"
    return "UNKNOWN"


def detect_structure(sentence, word_lang=""):

    if not isinstance(sentence, str):
        return "UNKNOWN"

    if contains_tamil_script(sentence):
        return classify_tamil_script(sentence)

    if isinstance(word_lang, str):
        langs = word_lang.split()
        ta = langs.count("TA")
        en = langs.count("EN")

        if ta > en:
            return classify_roman_tamil(sentence)
        if en > ta:
            return classify_english(sentence)

    
    return classify_roman_tamil(sentence)


uploaded = files.upload()
df = pd.read_csv(list(uploaded.keys())[0])
df = df.dropna(subset=["clean_text"])

df["predicted_structure"] = df.apply(
    lambda r: detect_structure(r["clean_text"], r.get("word_lang","")),
    axis=1
)

print("Unique Structures:", df["predicted_structure"].nunique())
print(df["predicted_structure"].value_counts())

df.to_csv("code_mixed_pattern.csv", index=False)
files.download("code_mixed_pattern.csv")