import pandas as pd

file_path = "../../data/raw/tamil_offensive_full.tsv"

df = pd.read_csv(file_path, sep="\t", header=None)

df = df[[0,1]]
df.columns = ["label","text"]

print("Original dataset:", len(df))

# remove not-tamil
df = df[df["label"] != "not-Tamil"]

# convert labels
df["label"] = df["label"].apply(
    lambda x: "not_offensive" if x == "Not_offensive" else "offensive"
)

print("\nAfter conversion:")
print(df["label"].value_counts())

# remove duplicates
df = df.drop_duplicates(subset="text")

# remove empty rows
df = df[df["text"].notna()]
df = df[df["text"].str.strip() != ""]

# split classes
offensive = df[df["label"] == "offensive"]
non_offensive = df[df["label"] == "not_offensive"]

print("\nOffensive:", len(offensive))
print("Non offensive:", len(non_offensive))

# balanced sampling
offensive_sample = offensive.sample(n=2500, random_state=42)
non_offensive_sample = non_offensive.sample(n=2500, random_state=42)

balanced_df = pd.concat([offensive_sample, non_offensive_sample])

# shuffle dataset
balanced_df = balanced_df.sample(frac=1).reset_index(drop=True)

print("\nFinal dataset:")
print(balanced_df["label"].value_counts())

# save dataset
balanced_df.to_csv("balanced_5000_dataset.tsv", sep="\t", index=False)

print("\nSaved balanced_5000_dataset.tsv")