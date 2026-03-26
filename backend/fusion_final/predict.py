from flask import Flask, request, jsonify
from flask_cors import CORS

import numpy as np
import torch
import joblib
import re
import os
from transformers import AutoTokenizer, AutoModel

app = Flask(__name__)
CORS(app)

# -----------------------------
# Paths
# -----------------------------

BASE_DIR = os.path.dirname(__file__)
FEATURE_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "feature_extraction"))

# -----------------------------
# Load lexicons
# -----------------------------

def load_lexicon(file):
    with open(os.path.join(FEATURE_DIR, file), "r", encoding="utf-8") as f:
        return set(w.strip().lower() for w in f if w.strip())

english_offensive = load_lexicon("english_offensive.txt")
tamil_offensive = load_lexicon("tamil_offensive.txt")

# -----------------------------
# Handcrafted features
# -----------------------------

def handcrafted_features(text):

    words = text.lower().split()
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
# Load trained components
# -----------------------------

model = joblib.load("offensive_model.pkl")
scaler = joblib.load("scaler.pkl")
selector = joblib.load("selector.pkl")

# -----------------------------
# Load transformer
# -----------------------------

MODEL_NAME = "xlm-roberta-base"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
bert = AutoModel.from_pretrained(MODEL_NAME, output_attentions=True)

device = "cuda" if torch.cuda.is_available() else "cpu"
bert.to(device)
bert.eval()
torch.set_grad_enabled(False)
# -----------------------------
# Transformer features
# -----------------------------

def transformer_features(text):

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=128
    ).to(device)

    with torch.no_grad():
        outputs = bert(**inputs)

    cls_embedding = outputs.last_hidden_state[:,0,:].cpu().numpy().flatten()

    attentions = outputs.attentions
    last_layer = attentions[-1][0]

    avg_attention = last_layer.mean(dim=0)
    cls_attention = avg_attention[0].cpu().numpy()

    if len(cls_attention) > 128:
        cls_attention = cls_attention[:128]
    else:
        cls_attention = np.pad(cls_attention,(0,128-len(cls_attention)))

    return cls_embedding, cls_attention


# -----------------------------
# Prediction function
# -----------------------------

def predict_text(text):

    hand = handcrafted_features(text)

    cls, att = transformer_features(text)

    fused = np.concatenate([hand, cls, att])

    X = fused.reshape(1,-1)

    X_scaled = scaler.transform(X)
    X_selected = selector.transform(X_scaled)

    prob = model.predict_proba(X_selected)[0][1]

    words = text.lower().split()

    if any(w in english_offensive for w in words) or any(w in tamil_offensive for w in words):
        label = "Offensive"
    else:
        threshold = 0.8
        label = "Offensive" if prob >= threshold else "Non-Offensive"

    return label, prob


# -----------------------------
# API Endpoint
# -----------------------------

@app.route("/predict", methods=["POST"])
def predict():

    data = request.json
    text = data["text"]

    label, prob = predict_text(text)

    return jsonify({
        "prediction": label,
        "confidence": round(float(prob),3)
    })


# -----------------------------
# Run server
# -----------------------------

if __name__ == "__main__":
    app.run(debug=True)