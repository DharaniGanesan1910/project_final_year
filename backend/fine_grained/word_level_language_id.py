import os
import pandas as pd
import re
import enchant

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "..", "data", "processed", "train.csv")
OUTPUT_PATH = os.path.join(BASE_DIR, "train_word_level_lang.csv")

if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(f"❌ File not found: {DATA_PATH}")

df = pd.read_csv(DATA_PATH)
print("✅ File loaded:", DATA_PATH)
print("Columns:", df.columns)

TEXT_COL = df.columns[0]  # assuming first column contains text

# Initialize English dictionary
english_dict = enchant.Dict("en_US")

def clean_text(text):
    text = str(text).lower()
    # keep only letters (a-z, A-Z) and Tamil Unicode range
    text = re.sub(r"[^a-zA-Z\u0B80-\u0BFF\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def word_level_lang_id(text):
    words = clean_text(text).split()
    labeled = []
    
    for word in words:
        if any("\u0B80" <= c <= "\u0BFF" for c in word):  # Tamil script present
            lang = "TA"
        elif english_dict.check(word):  # English word
            lang = "EN"
        else:  # Romanized Tamil
            lang = "TA"
        labeled.append(f"{word}/{lang}")
    
    return " ".join(labeled)

df["word_lang"] = df[TEXT_COL].apply(word_level_lang_id)
df.to_csv(OUTPUT_PATH, index=False)
print(f"✅ Word-level language tagging complete. Saved to {OUTPUT_PATH}")
