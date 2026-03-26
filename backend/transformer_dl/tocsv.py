# ==========================================
# Convert CLS + Attention NPY files to CSV
# ==========================================

import numpy as np
import pandas as pd

# -----------------------------
# 1️⃣ Load CLS Features
# -----------------------------
print("Loading cls_features.npy ...")
cls_features = np.load("cls_features.npy")

# Convert to DataFrame
df_cls = pd.DataFrame(cls_features)

# Save to CSV
df_cls.to_csv("cls_features.csv", index=False)
print("Saved: cls_features.csv")

# -----------------------------
# 2️⃣ Load Attention Scores
# -----------------------------
print("Loading attention_scores.npy ...")
attention_scores = np.load("attention_scores.npy", allow_pickle=True)

# Convert to DataFrame
df_attention = pd.DataFrame(attention_scores.tolist())

# Save to CSV
df_attention.to_csv("attention_scores.csv", index=False)
print("Saved: attention_scores.csv")

print("\nConversion Completed Successfully ✅")
