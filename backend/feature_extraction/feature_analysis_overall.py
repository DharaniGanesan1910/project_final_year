# ==========================================================
# HANDCRAFTED FEATURE PERCENTAGE DISTRIBUTION
# Offensive vs Non-Offensive
# ==========================================================

import pandas as pd
import numpy as np

# ----------------------------------------------------------
# 1️⃣ Load Extracted Handcrafted Features
# ----------------------------------------------------------

df = pd.read_csv("extracted_features_list_final.csv")

if "binary_label" not in df.columns:
    raise ValueError("binary_label column missing")

# Remove text column if exists
if "clean_text" in df.columns:
    df = df.drop(columns=["clean_text"])

print("Total Samples:", df.shape[0])
print("Total Features:", df.shape[1] - 1)

# ----------------------------------------------------------
# 2️⃣ Separate Classes
# ----------------------------------------------------------

offensive_df = df[df["binary_label"] == 1]
non_offensive_df = df[df["binary_label"] == 0]

print("Offensive Samples:", offensive_df.shape[0])
print("Non-Offensive Samples:", non_offensive_df.shape[0])

feature_columns = df.columns.drop("binary_label")

# ----------------------------------------------------------
# 3️⃣ Compute Mean Values
# ----------------------------------------------------------

offensive_means = offensive_df[feature_columns].mean()
non_offensive_means = non_offensive_df[feature_columns].mean()

result_df = pd.DataFrame({
    "Feature": feature_columns,
    "Offensive_%": offensive_means.values,
    "Non_Offensive_%": non_offensive_means.values,
})

# ----------------------------------------------------------
# 4️⃣ Convert to Percentage
# ----------------------------------------------------------

result_df["Offensive_%"] = (result_df["Offensive_%"] * 100).round(2)
result_df["Non_Offensive_%"] = (result_df["Non_Offensive_%"] * 100).round(2)

result_df["Difference_%"] = (
    result_df["Offensive_%"] - result_df["Non_Offensive_%"]
).round(2)

# Sort by most discriminative
result_df = result_df.sort_values(by="Difference_%", ascending=False)

# ----------------------------------------------------------
# 5️⃣ Save for UI
# ----------------------------------------------------------

result_df.to_csv("handcrafted_feature_percentage_distribution.csv", index=False)

print("\nTop 20 Most Discriminative Features:\n")
print(result_df.head(20))

print("\n✅ Saved as: handcrafted_feature_percentage_distribution.csv")