import numpy as np
from sklearn.preprocessing import StandardScaler
import joblib

# load fused features
X = np.load("fused_features.npy")

print("Original shape:", X.shape)

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

print("Scaled shape:", X_scaled.shape)

np.save("X_scaled.npy", X_scaled)

joblib.dump(scaler, "scaler.pkl")


print("Normalization completed")