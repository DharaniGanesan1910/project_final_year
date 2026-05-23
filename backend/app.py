from flask import Flask, request, jsonify
from flask_cors import CORS

import pandas as pd
import numpy as np
import torch
import joblib
import os
import re
import enchant
english_dict = enchant.Dict("en_US")
from transformers import AutoTokenizer, AutoModel

app = Flask(__name__)
CORS(app)

# -----------------------------
# Store recent predictions
# -----------------------------
recent_predictions = []

# -----------------------------
# Base directory
# -----------------------------
BASE_DIR = os.path.dirname(__file__)

# -----------------------------
# Load Fusion ML Model
# -----------------------------
model = joblib.load(os.path.join(BASE_DIR, "fusion_final", "offensive_model.pkl"))
scaler = joblib.load(os.path.join(BASE_DIR, "fusion_final", "scaler.pkl"))
selector = joblib.load(os.path.join(BASE_DIR, "fusion_final", "selector.pkl"))

# -----------------------------
# Prediction threshold
# -----------------------------
threshold = 0.75

# -----------------------------
# Load Fine-Tuned Transformer
# -----------------------------
MODEL_PATH = os.path.join(BASE_DIR, "offensive_model")
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, local_files_only=True)

bert = AutoModel.from_pretrained(
    MODEL_PATH,
    output_attentions=True,
    local_files_only=True
)

device = "cuda" if torch.cuda.is_available() else "cpu"

bert.to(device)
bert.eval()

torch.set_grad_enabled(False)

# -----------------------------
# Load lexicons
# -----------------------------
FEATURE_DIR = os.path.join(BASE_DIR, "feature_extraction")
def load_lexicon(file):
    with open(os.path.join(FEATURE_DIR, file), "r", encoding="utf-8") as f:
        return set(w.strip() for w in f if w.strip())   # ❌ removed .lower()

english_offensive = load_lexicon("english_offensive.txt")
tamil_offensive = load_lexicon("tamil_offensive.txt")

# ✅ lowercase only English
all_offensive_words = set(w.lower() for w in english_offensive).union(tamil_offensive)

# -----------------------------
# Lexicon check function
# -----------------------------
def contains_offensive_word(text):

    import unicodedata
    text = unicodedata.normalize('NFC', text)

    words = re.findall(r'\b\w+\b', text.lower())
    tamil_words = re.findall(r'[\u0B80-\u0BFF]+', text)

    all_words = words + tamil_words

    for w in all_words:
        if w in all_offensive_words:
            return w   # return matched word

    return None

# -----------------------------
# Handcrafted features
# -----------------------------
def preprocess_text(text):
    text = text.lower()

    # remove URLs
    text = re.sub(r'http\S+|www\.\S+', '', text)

    # remove mentions and hashtags
    text = re.sub(r'@\w+', '', text)
    text = re.sub(r'#\w+', '', text)

    # keep only Tamil + English letters
    text = re.sub(r'[^a-zA-Z\u0B80-\u0BFF\s]', '', text)

    # normalize spaces
    text = re.sub(r'\s+', ' ', text).strip()

    return text
def get_tokens(text):
    text = text.lower()

    # remove extra spaces first
    text = re.sub(r'\s+', ' ', text).strip()

    # split but keep only words
    return re.findall(r"[a-zA-Z\u0B80-\u0BFF]+", text)
def count_punctuations(text):
    return len(re.findall(r"[.,!?;:()\"']", text))
def handcrafted_features(text):

    words = re.findall(r'\b\w+\b', text.lower())
    total = len(words)

    tamil_off = sum(1 for w in words if w in tamil_offensive)
    english_off = sum(1 for w in words if w in english_offensive)

    punct_count = count_punctuations(text)

    features = [
        tamil_off,
        english_off,
        tamil_off + english_off,   # total offensive

        (tamil_off + english_off) / total if total else 0,

        total,
        punct_count,

        text.count("!"),
        text.count("?"),
        sum(c.isdigit() for c in text),
        sum(1 for c in text if c.isupper()),
        len(re.findall(r'(.)\1{2,}', text)),
    ]

    vec = np.zeros(55)
    vec[:len(features)] = features
    return vec
# -----------------------------
# Transformer features
# -----------------------------
def transformer_features(text):

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding="max_length",
        max_length=64
    )

    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = bert(**inputs)

    cls_embedding = outputs.last_hidden_state[:,0,:].cpu().numpy().flatten()

    attentions = outputs.attentions[-1][0]
    cls_attention = attentions.mean(dim=0)[0].cpu().numpy()

    cls_attention = np.pad(cls_attention,(0,128-len(cls_attention)))[:128]

    return cls_embedding, cls_attention
 # IMPORTANT: use split, not regex
def get_language_stats(words):

    tamil_count = 0
    english_count = 0

    for w in words:
        if english_dict.check(w):
            english_count += 1
        else:
            tamil_count += 1

    return {
        "total_tokens": len(words),
        "tamil_tokens": tamil_count,
        "english_tokens": english_count
    }
def get_token_languages(tokens):
    result = []

    for t in tokens:
        if re.fullmatch(r'[\u0B80-\u0BFF]+', t):
            lang = "Tamil"
        elif english_dict.check(t):
            lang = "English"
        else:
            lang = "Tamil"

        result.append({
            "token": t,
            "language": lang
        })

    return result
def get_code_switching_position(tokens):

    n = len(tokens)

    if n < 2:
        return {
            "total_switches": 0,
            "beginning_switches": 0,
            "middle_switches": 0,
            "end_switches": 0,
            "switch_frequency": 0
        }

    total_transitions = n - 1

    begin_switch = 0
    mid_switch = 0
    end_switch = 0
    total_switches = 0

    for i in range(total_transitions):
        prev_lang = detect_lang(tokens[i])
        curr_lang = detect_lang(tokens[i + 1])

        if prev_lang != curr_lang:
            total_switches += 1

            ratio = i / total_transitions

            if ratio < 0.33:
                begin_switch += 1
            elif ratio < 0.66:
                mid_switch += 1
            else:
                end_switch += 1

    return {
        "total_switches": total_switches,
        "beginning_switches": begin_switch,
        "middle_switches": mid_switch,
        "end_switches": end_switch,
        "switch_frequency": round(total_switches / total_transitions, 3)
    }
import re
import enchant

english_dict = enchant.Dict("en_US")

def detect_lang(token):
    # Tamil script
    if re.fullmatch(r'[\u0B80-\u0BFF]+', token):
        return "TA"

    # English word
    elif english_dict.check(token):
        return "EN"

    # fallback → treat non-English dictionary words as Tamil (NO unknown category)
    return "TA"


def get_token_languages(tokens):
    return [
        {
            "token": t,
            "language": detect_lang(t)
        }
        for t in tokens
    ]


def get_code_switching(tokens):

    transitions = {
        "TA->EN": 0,
        "EN->TA": 0,
        "TA->TA": 0,
        "EN->EN": 0
    }

    if not tokens:
        return transitions

    prev = detect_lang(tokens[0])

    for t in tokens[1:]:
        curr = detect_lang(t)

        key = f"{prev}->{curr}"
        transitions[key] += 1

        prev = curr

    return transitions
def count_digits(text):
    return sum(c.isdigit() for c in text)

import re

def count_emojis(text):

    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map
        "\U0001F1E0-\U0001F1FF"  # flags
        "\U00002700-\U000027BF"  # dingbats
        "\U000024C2-\U0001F251"
        "]+",
        flags=re.UNICODE
    )

    return len(emoji_pattern.findall(text))
def count_total_characters(text):
    return len(text)
def uppercase_count(text):
    return sum(1 for c in text if c.isupper())

def uppercase_ratio(text):
    return uppercase_count(text) / len(text) if text else 0

import re

def repeated_char_count(text):
    return len(re.findall(r"(.)\1{2,}", text))  # 3+ repeated chars

# -----------------------------
# Prediction API
@app.route("/predict", methods=["POST"])
def predict():

    data = request.json
    text = data["text"]

    # -----------------------------
    # PREPROCESS FIRST
    # -----------------------------
    processed_text = preprocess_text(text)

    # -----------------------------
    # TOKENS FROM CLEAN TEXT
    # -----------------------------
    tokens = get_tokens(processed_text)

    # -----------------------------
    # LANGUAGE STATS (FIXED INPUT)
    # -----------------------------
    lang_stats = get_language_stats(tokens)
    code_switch = get_code_switching(tokens)
    position_switch = get_code_switching_position(tokens)
    uppercase_cnt = sum(1 for c in text if c.isupper())
    uppercase_ratio = uppercase_cnt / len(text) if text else 0

    repeated_chars = len(re.findall(r"(.)\1{2,}", text))
    # -----------------------------
    # LEXICON CHECK
    # -----------------------------
    matched_word = contains_offensive_word(processed_text)

    reason = ""

    # -----------------------------
    # CASE 1: LEXICON MATCH
    # -----------------------------
    if matched_word:

        label = "Offensive"
        prob = 1.0
        reason = f"Offensive word '{matched_word}' detected from lexicon"

        # still run ML features for consistency (optional but good)
        hand = handcrafted_features(processed_text)
        cls, att = transformer_features(processed_text)

    # -----------------------------
    # CASE 2: ML MODEL
    # -----------------------------
    else:

        hand = handcrafted_features(processed_text)
        cls, att = transformer_features(processed_text)

        fused = np.concatenate([hand, cls, att])
        X = fused.reshape(1, -1)

        X_scaled = scaler.transform(X)
        X_selected = selector.transform(X_scaled)

        prob = model.predict_proba(X_selected)[0][1]

        label = "Offensive" if prob >= threshold else "Non-Offensive"
        reason = "No offensive words detected"

    # -----------------------------
    # HISTORY
    # -----------------------------
    recent_predictions.append({
        "text": text,
        "prediction": label
    })

    if len(recent_predictions) > 10:
        recent_predictions.pop(0)
    token_languages = get_token_languages(tokens)

    bert_tokens = tokenizer.tokenize(processed_text)

    attention_scores = []

    for i, token in enumerate(bert_tokens):
       score = float(att[i+1]) if i+1 < len(att) else 0

       attention_scores.append({
        "token": token,
        "score": round(score, 3)
    })


    # -----------------------------
    # RESPONSE
    # -----------------------------
    return jsonify({
    "prediction": label,
    "confidence": round(float(prob), 3),
    "reason": reason,

    "processed_text": processed_text,

    "tokens": tokens,
    "token_count": len(tokens),
    "token_languages": token_languages, 
     "code_switching": code_switch, 
     "code_switching_position": position_switch,
     "attention_scores": attention_scores, 
   "features": {
    "total_tokens": lang_stats["total_tokens"],
    "tamil_tokens": lang_stats["tamil_tokens"],
    "english_tokens": lang_stats["english_tokens"],

    "tamil_offensive": sum(1 for w in tokens if w in tamil_offensive),
    "english_offensive": sum(1 for w in tokens if w in english_offensive),
    "total_offensive": sum(
        1 for w in tokens if (w in tamil_offensive or w in english_offensive)
    ),

    "total_characters": len(text),

    "punctuation_count": count_punctuations(text),
    "digit_count": count_digits(text),
    "emoji_count": count_emojis(text), "uppercase_count": uppercase_cnt,
        "uppercase_ratio": round(uppercase_ratio, 3),

        "repeated_char_count": repeated_chars
}
})
# -----------------------------
# Pattern analytics API
# -----------------------------
@app.route("/pattern-data")
def pattern_data():

    df = pd.read_csv(os.path.join(BASE_DIR, "structure", "pattern.csv"))

    # 🏆 Pattern counts (top 8)
    pattern_counts = df["predicted_structure"].value_counts().head(8)

    # 📊 Total stats
    total_sentences = len(df)

    # If you have label column (Offensive / Non-Offensive)
    offensive_count = 0
    non_offensive_count = 0

    if "label" in df.columns:
        offensive_count = len(df[df["label"] == "Offensive"])
        non_offensive_count = len(df[df["label"] == "Non-Offensive"])

    # 🧾 Example sentences per pattern
    examples = {}
    if "text" in df.columns:
        for pattern in pattern_counts.index:
            sample_texts = df[df["predicted_structure"] == pattern]["text"].dropna().tolist()
            examples[pattern] = sample_texts[:5]  # top 5 examples

    return jsonify({
        "labels": pattern_counts.index.tolist(),
        "values": pattern_counts.values.tolist(),

        # 📊 stats
        "total": total_sentences,
        "offensive": offensive_count,
        "non_offensive": non_offensive_count,

        # 🧠 extra
        "examples": examples
    })

# -----------------------------
# Dataset insights API
# -----------------------------
@app.route("/dataset_insights")
def dataset_insights():

    df = pd.read_csv(os.path.join(BASE_DIR, "structure", "pattern.csv"))

    text_col = "clean_text"

    # 📊 Language Composition
    tamil_words = 0
    english_words = 0

    for text in df[text_col].dropna():
        words = str(text).split()
        for w in words:
            if any('\u0B80' <= ch <= '\u0BFF' for ch in w):
                tamil_words += 1
            else:
                english_words += 1

    # 📏 Sentence Length
    df["length"] = df[text_col].apply(lambda x: len(str(x).split()))
    length_bins = pd.cut(df["length"], bins=[0, 3, 6, 10, 20],
                         labels=["Short", "Medium", "Long", "Very Long"])
    length_counts = length_bins.value_counts().sort_index()

    # 🔁 Code Switching
    pure_tamil = 0
    pure_english = 0
    mixed = 0

    for text in df[text_col].dropna():
        has_tamil = any('\u0B80' <= ch <= '\u0BFF' for ch in text)
        has_english = any(ch.isalpha() and ord(ch) < 128 for ch in text)

        if has_tamil and has_english:
            mixed += 1
        elif has_tamil:
            pure_tamil += 1
        else:
            pure_english += 1

    # ⚠️ Offensive Distribution
    offensive = len(df[df["binary_label"] == 1])
    non_offensive = len(df[df["binary_label"] == 0])

    # 🔥 Top Offensive Words
    from collections import Counter
    offensive_text = df[df["binary_label"] == 1][text_col].dropna()
    words = " ".join(offensive_text).split()
    top_words = Counter(words).most_common(5)

    # 🧩 Structure vs Offensiveness
    structure_offense = {}

    for structure in df["predicted_structure"].unique():
        subset = df[df["predicted_structure"] == structure]
        total = len(subset)
        off = len(subset[subset["binary_label"] == 1])

        if total > 0:
            structure_offense[structure] = round((off / total) * 100, 2)

    # 📌 Samples
    samples = df[text_col].dropna().sample(min(5, len(df))).tolist()

    return jsonify({
        "language_composition": {
            "labels": ["Tamil", "English"],
            "values": [tamil_words, english_words]
        },
        "sentence_length": {
            "labels": length_counts.index.tolist(),
            "values": length_counts.values.tolist()
        },
        "code_switching": {
            "labels": ["Mixed", "Tamil Only", "English Only"],
            "values": [mixed, pure_tamil, pure_english]
        },
        "offensive_distribution": {
            "labels": ["Offensive", "Non-Offensive"],
            "values": [offensive, non_offensive]
        },
        "top_offensive_words": {
            "labels": [w[0] for w in top_words],
            "values": [w[1] for w in top_words]
        },
        "structure_offense": {
            "labels": list(structure_offense.keys()),
            "values": list(structure_offense.values())
        },
        "samples": samples,
        "avg_length": round(df["length"].mean(), 2),
        "total_sentences": len(df)
    })
# -----------------------------
# Recent predictions API
# -----------------------------
@app.route("/recent_predictions")
def recent_predictions_api():
    return jsonify(recent_predictions[::-1])

# -----------------------------
# Run server
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)