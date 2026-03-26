from flask import Flask, request, jsonify
from flask_cors import CORS

import pandas as pd
import numpy as np
import torch
import joblib
import os
import re

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

    # English + Roman Tamil
    words = re.findall(r'\b\w+\b', text.lower())

    # Tamil script
    tamil_words = re.findall(r'[\u0B80-\u0BFF]+', text)

    # Combine
    all_words = words + tamil_words

    for w in all_words:
        if w in all_offensive_words:
            return True

    return False

# -----------------------------
# Handcrafted features
# -----------------------------
def handcrafted_features(text):

    words = re.findall(r'\b\w+\b', text.lower())
    total_tokens = len(words)

    ta_off = sum(1 for w in words if w in tamil_offensive)
    en_off = sum(1 for w in words if w in english_offensive)

    features = [

        ta_off,
        en_off,
        ta_off + en_off,

        (ta_off + en_off) / total_tokens if total_tokens else 0,

        total_tokens,

        text.count("!"),
        text.count("?"),

        len(re.findall(r'[.,;:]', text)),

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

# -----------------------------
# Prediction API
# -----------------------------
@app.route("/predict", methods=["POST"])
def predict():

    data = request.json
    text = data["text"]

    # -----------------------------
    # 1️⃣ Lexicon rule override
    # -----------------------------
    if contains_offensive_word(text):

        label = "Offensive"
        prob = 1.0

    else:

        # -----------------------------
        # 2️⃣ Hybrid ML Prediction
        # -----------------------------
        hand = handcrafted_features(text)

        cls, att = transformer_features(text)

        fused = np.concatenate([hand, cls, att])

        X = fused.reshape(1, -1)

        X_scaled = scaler.transform(X)

        X_selected = selector.transform(X_scaled)

        prob = model.predict_proba(X_selected)[0][1]

        label = "Offensive" if prob >= threshold else "Non-Offensive"

    # -----------------------------
    # 3️⃣ Store recent predictions
    # -----------------------------
    recent_predictions.append({
        "text": text,
        "prediction": label
    })

    if len(recent_predictions) > 10:
        recent_predictions.pop(0)

    # -----------------------------
    # 4️⃣ Return response
    # -----------------------------
    return jsonify({
        "prediction": label,
        "confidence": round(float(prob), 3)
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