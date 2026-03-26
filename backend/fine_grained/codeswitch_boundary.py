import os
import pandas as pd


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_CSV = os.path.join(BASE_DIR, "train_word_level_lang.csv")  # from previous step
OUTPUT_CSV = os.path.join(BASE_DIR, "train_fine_grained_final.csv")


if not os.path.exists(INPUT_CSV):
    raise FileNotFoundError(f"❌ File not found: {INPUT_CSV}")

df = pd.read_csv(INPUT_CSV)
print("✅ Loaded:", INPUT_CSV)


def code_switch_boundaries(tagged_sentence):
    """
    Input: "i/EN love/EN vijay/TA anna/TA u/EN r/EN so/EN cute/EN anna/TA"
    Output: [0,0,1,0,1,0,0,0,1]
    """
    words = str(tagged_sentence).split()
    boundaries = []
    prev_lang = None
    for w in words:
        lang = w.split('/')[-1]
        if prev_lang is None:
            boundaries.append(0)  # first word has no boundary
        else:
            boundaries.append(1 if lang != prev_lang else 0)
        prev_lang = lang
    return boundaries


def compute_stats(tagged_sentence):
    words = str(tagged_sentence).split()
    num_ta = sum(1 for w in words if w.split('/')[-1] == "TA")
    num_en = sum(1 for w in words if w.split('/')[-1] == "EN")
    boundaries = code_switch_boundaries(tagged_sentence)
    num_switches = sum(boundaries)
    total_words = len(words) if len(words) > 0 else 1
    switch_ratio = num_switches / total_words
    return pd.Series([num_ta, num_en,  num_switches, switch_ratio, boundaries])


df[["num_ta", "num_en", "num_switches", "switch_ratio", "code_switch_boundaries"]] = \
    df["word_lang"].apply(compute_stats)


df.to_csv(OUTPUT_CSV, index=False)
print(f"✅ Fine-grained preprocessing complete. Saved to {OUTPUT_CSV}")
