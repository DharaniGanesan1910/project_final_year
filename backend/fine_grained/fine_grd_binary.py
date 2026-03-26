import pandas as pd

# =========================
# Step 1: Load your dataset
# =========================
# Replace 'processed_dataset.csv' with your dataset file
df = pd.read_csv('train_fine_grained.csv')

# Check original labels
print("Original label distribution:")
print(df['label_id'].value_counts())

# ====================================
# Step 2: Convert fine-grained labels to binary
# ====================================
# 0 -> non-offensive, everything else -> offensive
df['label_id'] = df['label_id'].apply(lambda x: 0 if x == 0 else 1)

# Verify the change
print("\nBinary label distribution:")
print(df['label_id'].value_counts())

# =========================
# Step 3: Save the updated dataset
# =========================
df.to_csv('fine_grained_train.csv', index=False)
print("\nBinary dataset saved as 'processed_dataset_binary.csv'")

# =========================
# Step 4: Optional - ready for model training
# =========================
# Example: if you have features in X and labels in y
# X = df.drop('label', axis=1)  # features
# y = df['label']               # binary labels
