import pandas as pd
import numpy as np

# load handcrafted features
handcrafted = pd.read_csv("../feature_extraction/extracted_features.csv")

# remove non-feature columns if present
handcrafted = handcrafted.drop(
    columns=["text", "label", "binary_label"],
    errors="ignore"
)

# load transformer features
cls = np.load("../transformer_dl/cls_features.npy")
attention = np.load("../transformer_dl/attention_scores_fixed.npy")

print("Handcrafted:", handcrafted.shape)
print("CLS:", cls.shape)
print("Attention:", attention.shape)

# ensure attention is 2D
if attention.ndim == 1:
    attention = attention.reshape(-1,1)

# match row counts
min_rows = min(len(handcrafted), len(cls), len(attention))

handcrafted = handcrafted.iloc[:min_rows]
cls = cls[:min_rows]
attention = attention[:min_rows]

print("\nAfter alignment:")
print("Handcrafted:", handcrafted.shape)
print("CLS:", cls.shape)
print("Attention:", attention.shape)

# convert dataframe → numpy
handcrafted_np = handcrafted.values

# feature fusion
fused_features = np.concatenate(
    [handcrafted_np, cls, attention],
    axis=1
)

print("\nFused shape:", fused_features.shape)

np.save("fused_features.npy", fused_features)

print("Fusion completed successfully")