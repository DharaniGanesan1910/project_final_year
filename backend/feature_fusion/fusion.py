import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import pickle

print("Loading features...")

handcrafted = np.load("handcrafted_features.npy")
cls = np.load("../transformer_dl/cls_features.npy")
attention = np.load("../transformer_dl/attention_scores.npy")
labels = np.load("labels.npy")

print("Handcrafted:", handcrafted.shape)
print("CLS:", cls.shape)
print("Attention:", attention.shape)

# Ensure same number of samples
min_samples = min(handcrafted.shape[0], cls.shape[0], attention.shape[0])

handcrafted = handcrafted[:min_samples]
cls = cls[:min_samples]
attention = attention[:min_samples]
labels = labels[:min_samples]

print("After alignment:", handcrafted.shape, cls.shape, attention.shape)

print("\nNormalizing handcrafted features...")

scaler = StandardScaler()
handcrafted_scaled = scaler.fit_transform(handcrafted)

with open("scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)

print("Scaler saved as scaler.pkl")

print("\nFusing features...")

fused_features = np.concatenate(
    [handcrafted_scaled, cls, attention],
    axis=1
)

print("Fused feature shape:", fused_features.shape)

print("\nSaving fused features...")

np.save("fused_features.npy", fused_features)
np.save("labels.npy", labels)

print("Saved fused_features.npy")
print("Saved labels.npy")