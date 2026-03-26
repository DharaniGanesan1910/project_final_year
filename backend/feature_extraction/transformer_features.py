# ===============================
# INSTALL (Safe for Colab)
# ===============================
#!pip install -U transformers matplotlib seaborn -q

# ===============================
# IMPORTS
# ===============================
import torch
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from transformers import AutoTokenizer, AutoModel

# ===============================
# SETTINGS
# ===============================
MODEL_NAME = "xlm-roberta-base"
MAX_LENGTH = 128

device = "cuda" if torch.cuda.is_available() else "cpu"
print("Using device:", device)

# ===============================
# LOAD MODEL (NO TRAINING)
# ===============================
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

model = AutoModel.from_pretrained(
    MODEL_NAME,
    output_attentions=True
).to(device)

model.eval()

# ===============================
# LOAD YOUR DATA
# Must contain column: clean_text
# ===============================
df = pd.read_csv("dataset.csv")
df = df.dropna(subset=["clean_text"])

texts = df["clean_text"].astype(str).tolist()

all_cls_embeddings = []
all_token_embeddings = []
all_attention_scores = []

# ===============================
# PROCESS EACH SENTENCE
# ===============================
for text in texts:

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=MAX_LENGTH
    ).to(device)

    with torch.no_grad():
        outputs = model(**inputs)

    # ---- Contextual Embeddings ----
    last_hidden = outputs.last_hidden_state  # (1, seq_len, 768)
    cls_embedding = last_hidden[:, 0, :]     # sentence embedding
    
    all_cls_embeddings.append(cls_embedding.cpu().numpy())
    all_token_embeddings.append(last_hidden.cpu().numpy())

    # ---- Attention Extraction ----
    attentions = outputs.attentions
    last_layer_attention = attentions[-1][0]  # (heads, seq, seq)
    avg_attention = last_layer_attention.mean(dim=0)

    cls_attention = avg_attention[0]
    all_attention_scores.append(cls_attention.cpu().numpy())

# ===============================
# CONVERT TO NUMPY
# ===============================
cls_features = np.vstack(all_cls_embeddings)

print("\nExtraction Complete ✅")
print("CLS Feature Shape:", cls_features.shape)
print("Total Sentences:", len(texts))

# ===============================
# OFFENSIVE CUE ANALYSIS FOR ONE SAMPLE
# ===============================
sample_text = texts[0]
print("\nSample Sentence:\n", sample_text)

inputs = tokenizer(sample_text, return_tensors="pt").to(device)

with torch.no_grad():
    outputs = model(**inputs)

attentions = outputs.attentions
last_layer_attention = attentions[-1][0]
avg_attention = last_layer_attention.mean(dim=0)
cls_attention = avg_attention[0]

tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])

token_importance = list(zip(tokens, cls_attention.cpu().numpy()))
sorted_tokens = sorted(token_importance, key=lambda x: x[1], reverse=True)

print("\nTop Attention Tokens (Potential Cues):\n")
for token, score in sorted_tokens[:10]:
    print(token, "→", round(float(score), 4))
