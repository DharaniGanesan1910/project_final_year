import os
import pandas as pd
import re
from collections import Counter
import enchant  

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "data","processed", "train.csv")
RESOURCES_DIR = os.path.join(BASE_DIR, "resources")

os.makedirs(RESOURCES_DIR, exist_ok=True)


if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(f"❌ File not found: {DATA_PATH}")

df = pd.read_csv(DATA_PATH)
print("✅ File loaded successfully")
print("Columns:", df.columns)


TEXT_COL = df.columns[0]

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


all_words = []
for text in df[TEXT_COL]:
    all_words.extend(clean_text(text).split())

print(f"Total words extracted: {len(all_words)}")


word_freq = Counter(all_words)
common_words = [w for w, _ in word_freq.most_common(5000)]


dictionary = enchant.Dict("en_US")

english_words = []
tamil_words = []

for word in common_words:
    if dictionary.check(word):
        english_words.append(word)
    else:
        if len(word) > 2:  
            tamil_words.append(word)


english_path = os.path.join(RESOURCES_DIR, "english_words.txt")
tamil_path = os.path.join(RESOURCES_DIR, "tamil_words.txt")

with open(english_path, "w", encoding="utf-8") as f:
    for w in sorted(set(english_words)):
        f.write(w + "\n")

with open(tamil_path, "w", encoding="utf-8") as f:
    for w in sorted(set(tamil_words)):
        f.write(w + "\n")

print(f"✅ English words saved: {english_path}")
print(f"✅ Tamil words saved: {tamil_path}")
