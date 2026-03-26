import pandas as pd
import re
import os

INPUT_DIR = "../../data/processed"
OUTPUT_DIR = "../../data/processed"

FILES = ["train.csv", "test.csv", "dev.csv", "full.csv"]

def normalize_text(text):
    text = str(text).lower()

    # reduce elongation
    text = re.sub(r"(.)\1{2,}", r"\1\1", text)

    # remove URLs
    text = re.sub(r"http\S+", "", text)

    # normalize spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()

for file in FILES:
    path = os.path.join(INPUT_DIR, file)
    df = pd.read_csv(path)

    # create normalized_text from clean_text
    df["normalized_text"] = df["clean_text"].apply(normalize_text)

    # drop raw_text if it exists
    if "raw_text" in df.columns:
        df = df.drop(columns=["raw_text"])

    # save updated CSV
    df.to_csv(os.path.join(OUTPUT_DIR, file), index=False)
    print(f"{file} updated successfully")
