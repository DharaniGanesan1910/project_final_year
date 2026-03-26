import pandas as pd
import numpy as np
import re


df_main = pd.read_csv("../fine_grained/train_fine_grained_final.csv")
df_struct = pd.read_csv("../structure/pattern.csv")

df = pd.merge(
    df_main,
    df_struct[["clean_text", "predicted_structure"]],
    on="clean_text",
    how="left"
)

df["word_lang"] = df["word_lang"].fillna("")
df["clean_text"] = df["clean_text"].fillna("")
df["num_ta"] = df["num_ta"].fillna(0)
df["num_en"] = df["num_en"].fillna(0)
df["num_switches"] = df["num_switches"].fillna(0)
df["switch_ratio"] = df["switch_ratio"].fillna(0)
df["predicted_structure"] = df["predicted_structure"].fillna("")



def load_lexicon(path):
    with open(path, "r", encoding="utf-8") as f:
        return set(word.strip().lower() for word in f if word.strip())

english_offensive = load_lexicon("english_offensive.txt")
tamil_offensive = load_lexicon("tamil_offensive.txt")


def tamil_script_count(text):
    return sum(1 for c in text if '\u0B80' <= c <= '\u0BFF')

def tamil_suffix_count(words):
    suffixes = [
        "da","di","dei","dai","pa","ma","nga",
        "la","ah","aah","eh","leh",
        "unga","ungal","ngala",
        "machan","machi","mapla","nanba",
        "yaa","ya","ra","ree",
        "an","en","om","inga","iruka","irukku"
    ]
    return sum(1 for w in words if any(w.endswith(s) for s in suffixes))

def emoji_count(text):
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"       # Smileys
        "\U0001F300-\U0001F5FF"       # Symbols
        "\U0001F680-\U0001F6FF"      # Transport
        "\U0001F900-\U0001F9FF"      # Supplemental emojis
        "\U00002700-\U000027BF"      #  Misc symbols
        "]+",
        flags=re.UNICODE
    )
    return len(emoji_pattern.findall(text))

def repeated_char_words(words):
    return sum(1 for w in words if re.search(r'(.)\1{2,}', w))

def elongated_english(word_lang):
    count = 0
    tokens = str(word_lang).split()
    for token in tokens:
        parts = token.rsplit("/", 1)
        if len(parts) != 2:
            continue
        word, lang = parts
        if lang.upper() == "EN" and re.search(r'(.)\1{2,}', word.lower()):
            count += 1
    return count

def english_target_pronouns(word_lang):
    targets = {"you","your","u","ur","you're","yours","ya"}
    count = 0
    tokens = str(word_lang).split()
    for token in tokens:
        parts = token.rsplit("/", 1)
        if len(parts) != 2:
            continue
        word, lang = parts
        if lang.upper() == "EN" and word.lower() in targets:
            count += 1
    return count

def consecutive_offensive(word_lang):
    count = 0
    tokens = str(word_lang).split()
    for i in range(len(tokens) - 1):
        p1 = tokens[i].rsplit("/", 1)
        p2 = tokens[i+1].rsplit("/", 1)
        if len(p1) != 2 or len(p2) != 2:
            continue
        w1, lang1 = p1
        w2, lang2 = p2
        w1 = w1.lower()
        w2 = w2.lower()
        is_off1 = (lang1.upper()=="TA" and w1 in tamil_offensive) or \
                  (lang1.upper()=="EN" and w1 in english_offensive)
        is_off2 = (lang2.upper()=="TA" and w2 in tamil_offensive) or \
                  (lang2.upper()=="EN" and w2 in english_offensive)
        if is_off1 and is_off2:
            count += 1
    return count

def switch_location(word_lang):
    tokens = str(word_lang).split()
    total_words = len(tokens)
    if total_words < 2:
        return 0,0,0
    beginning = middle = end = 0
    for i in range(total_words - 1):
        p1 = tokens[i].rsplit("/",1)
        p2 = tokens[i+1].rsplit("/",1)
        if len(p1)!=2 or len(p2)!=2:
            continue
        if p1[1] != p2[1]:
            ratio = i/total_words
            if ratio < 0.33:
                beginning+=1
            elif ratio < 0.66:
                middle+=1
            else:
                end+=1
    return beginning,middle,end

def switch_direction(word_lang):
    tokens = str(word_lang).split()
    ta_en=en_ta=0
    for i in range(len(tokens)-1):
        p1 = tokens[i].rsplit("/",1)
        p2 = tokens[i+1].rsplit("/",1)
        if len(p1)!=2 or len(p2)!=2:
            continue
        l1=p1[1].upper()
        l2=p2[1].upper()
        if l1=="TA" and l2=="EN":
            ta_en+=1
        elif l1=="EN" and l2=="TA":
            en_ta+=1
    return ta_en,en_ta


def structural_features(pattern):

    if not isinstance(pattern,str) or pattern=="":
        return {
            "has_subject":0,"has_object":0,"has_verb":0,
            "has_complement":0,"has_adverb":0,"has_negation":0,
            "verb_position":-1,"verb_final":0,"verb_initial":0,
            "adverb_initial":0,"adverb_final":0,
            "structure_length":0,"argument_count":0,
            "is_transitive":0,"is_copular":0,"is_imperative":0
        }

    base = pattern.replace("-NEG","")

    return {
        "has_subject":1 if "S" in base else 0,
        "has_object":1 if "O" in base else 0,
        "has_verb":1 if "V" in base else 0,
        "has_complement":1 if "C" in base else 0,
        "has_adverb":1 if "A" in base else 0,
        "has_negation":1 if "-NEG" in pattern else 0,
        "verb_position":base.find("V") if "V" in base else -1,
        "verb_final":1 if base.endswith("V") else 0,
        "verb_initial":1 if base.startswith("V") else 0,
        "adverb_initial":1 if base.startswith("A") else 0,
        "adverb_final":1 if base.endswith("A") else 0,
        "structure_length":len(base),
        "argument_count":base.count("S")+base.count("O")+base.count("C"),
        "is_transitive":1 if "O" in base else 0,
        "is_copular":1 if "C" in base else 0,
        "is_imperative":1 if base in ["V","VO"] else 0
    }



feature_rows=[]

for _,row in df.iterrows():

    text=row["clean_text"]
    word_lang=row["word_lang"]
    pattern=row["predicted_structure"]

    words=text.lower().split()
    total_tokens=len(words)

    
    ta_off=sum(1 for w in words if w in tamil_offensive)
    en_off=sum(1 for w in words if w in english_offensive)
    total_off=ta_off+en_off
    off_ratio=total_off/total_tokens if total_tokens>0 else 0
    ta_off_ratio=ta_off/row["num_ta"] if row["num_ta"]>0 else 0
    en_off_ratio=en_off/row["num_en"] if row["num_en"]>0 else 0


    ta_ratio=row["num_ta"]/total_tokens if total_tokens>0 else 0
    en_ratio=row["num_en"]/total_tokens if total_tokens>0 else 0
    lang_dom=1 if row["num_ta"]>row["num_en"] else 2 if row["num_en"]>row["num_ta"] else 0

    
    switch_begin,switch_mid,switch_end=switch_location(word_lang)
    ta_en,en_ta=switch_direction(word_lang)
    switch_density=row["num_switches"]/total_tokens if total_tokens>0 else 0

    
    struct_feats=structural_features(pattern)

    char_length=len(text)
    avg_word_length=np.mean([len(w) for w in words]) if words else 0
    uppercase_count=sum(1 for c in text if c.isupper())
    uppercase_ratio=uppercase_count/char_length if char_length>0 else 0

    feature_rows.append({

        "clean_text":text,
        "binary_label":row["binary_label"],

        "tamil_offensive_count":ta_off,
        "english_offensive_count":en_off,
        "total_offensive":total_off,
        "offensive_ratio":off_ratio,
        "tamil_offensive_ratio":ta_off_ratio,
        "english_offensive_ratio":en_off_ratio,
        
        "num_ta":row["num_ta"],
        "num_en":row["num_en"],
        "total_tokens":total_tokens,
        "ta_ratio":ta_ratio,
        "en_ratio":en_ratio,
        "language_dominance":lang_dom,

        
        "num_switches":row["num_switches"],
        "switch_ratio":row["switch_ratio"],
        "switch_density":switch_density,
        "switch_beginning":switch_begin,
        "switch_middle":switch_mid,
        "switch_end":switch_end,
        "ta_to_en_switch":ta_en,
        "en_to_ta_switch":en_ta,


        "char_length":char_length,
        "avg_word_length":avg_word_length,
        "exclamation_count":text.count("!"),
        "question_count":text.count("?"),
        "punctuation_count":len(re.findall(r'[.,;:]', text)),
        "digit_count":sum(c.isdigit() for c in text),
        "uppercase_count":uppercase_count,
        "uppercase_ratio":uppercase_ratio,
       
        "tamil_script_count":tamil_script_count(text),
        "tamil_script_ratio":tamil_script_count(text)/char_length if char_length>0 else 0,
        "tamil_suffix_count":tamil_suffix_count(words),

       
        "elongated_english_words":elongated_english(word_lang),
        "english_target_pronouns":english_target_pronouns(word_lang),

       
        "emoji_count":emoji_count(text),
        "repeated_char_words":repeated_char_words(words),
        "offensive_at_beginning":1 if words and words[0] in tamil_offensive.union(english_offensive) else 0,
        "offensive_at_end":1 if words and words[-1] in tamil_offensive.union(english_offensive) else 0,
        "consecutive_offensive_words":consecutive_offensive(word_lang),

      
        "predicted_structure":pattern,
        **struct_feats
    })

features_df=pd.DataFrame(feature_rows)
features_df.to_csv(
    "extracted_features_ALL_features_combined.csv",
    index=False,
    encoding="utf-8-sig"
)     
print("Feature extraction complete.")
print("Total features (excluding text + label):",len(features_df.columns)-2) 