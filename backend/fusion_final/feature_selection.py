import numpy as np
import pandas as pd
from sklearn.feature_selection import SelectKBest, f_classif
import joblib

# load scaled features
X = np.load("X_scaled.npy")

# load labels from handcrafted CSV
data = pd.read_csv("../feature_extraction/extracted_features.csv")

y = data["binary_label"].values

# match row count
y = y[:len(X)]

print("Features:", X.shape)
print("Labels:", y.shape)

selector = SelectKBest(score_func=f_classif, k=300)

X_selected = selector.fit_transform(X, y)

print("Selected features:", X_selected.shape)

np.save("X_selected.npy", X_selected)
np.save("y.npy", y)
joblib.dump(selector, "selector.pkl")
print("Feature selection completed")