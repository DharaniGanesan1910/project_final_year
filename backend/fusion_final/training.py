import pandas as pd
import numpy as np
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score, precision_recall_curve
from sklearn.utils import shuffle
import joblib

# ==========================
# 1️⃣ Load Features
# ==========================
features_df = pd.read_csv("../feature_extraction/extracted_features.csv")

# Drop text columns for training
X = features_df.drop(columns=["clean_text", "binary_label"])
y = features_df["binary_label"]

# Convert to numpy
X = X.values
y = y.values

# ==========================
# 2️⃣ Train-Test Split
# ==========================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ==========================
# 3️⃣ Handle Class Imbalance
# ==========================
# Compute scale_pos_weight for XGBoost
n_pos = sum(y_train == 1)
n_neg = sum(y_train == 0)
scale_pos_weight = n_neg / n_pos
print(f"Class imbalance: 0->{n_neg}, 1->{n_pos}, scale_pos_weight={scale_pos_weight:.2f}")

# ==========================
# 4️⃣ Train XGBoost
# ==========================
model = XGBClassifier(
    n_estimators=300,
    max_depth=6,
    learning_rate=0.1,
    objective="binary:logistic",
    eval_metric="logloss",
    use_label_encoder=False,
    scale_pos_weight=scale_pos_weight,
    random_state=42
)

model.fit(X_train, y_train)

# ==========================
# 5️⃣ Predict & Evaluate
# ==========================
y_probs = model.predict_proba(X_test)[:,1]

# Find optimal threshold using Precision-Recall curve
precision, recall, thresholds = precision_recall_curve(y_test, y_probs)
f1_scores = 2 * precision * recall / (precision + recall + 1e-6)
best_idx = np.argmax(f1_scores)
optimal_threshold = thresholds[best_idx]
print(f"Optimal threshold based on F1: {optimal_threshold:.3f}")

# Final predictions
y_pred = (y_probs >= optimal_threshold).astype(int)

print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))

# ==========================
# 6️⃣ Save Model + Threshold
# ==========================
joblib.dump(model, "offensive_model_xgb.pkl")
np.save("optimal_threshold.npy", np.array([optimal_threshold]))

print("\nModel and threshold saved successfully ✅")