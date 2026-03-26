from .load_csv_data import train_df, test_df, dev_df, full_df
from .preprocess_text import preprocess_text
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
PROCESSED_DIR = BASE_DIR / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def to_binary_label(label):
    
    label = str(label).strip()

    if label.startswith("Offensive_"):
        return 1

    return 0


def process_labeled_split(df, name):
    df["clean_text"] = df["text"].apply(preprocess_text)

    df["binary_label"] = df["label"].apply(to_binary_label)

    out_path = PROCESSED_DIR / f"{name}.csv"
    df[["clean_text", "binary_label"]].to_csv(out_path, index=False)

    print(f"✅ Saved {name} → {out_path}")
    print(df["binary_label"].value_counts(), "\n")


def process_unlabeled_split(df, name):
    df["clean_text"] = df["text"].apply(preprocess_text)

    out_path = PROCESSED_DIR / f"{name}.csv"
    df[["clean_text"]].to_csv(out_path, index=False)

    print(f"✅ Saved {name} (unlabeled) → {out_path}")


# ▶️ RUN PIPELINE
process_labeled_split(train_df, "train")
process_labeled_split(test_df, "test")
process_labeled_split(dev_df, "dev")
process_unlabeled_split(full_df, "full")
