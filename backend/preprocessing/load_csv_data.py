# backend/preprocessing/load_csv_data.py
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data" / "raw"

TRAIN_PATH = DATA_DIR / "tamil_offensive_full_train.tsv"
TEST_PATH  = DATA_DIR / "tamil_offensive_full_test.tsv"
DEV_PATH   = DATA_DIR / "tamil_offensive_full_dev.tsv"
FULL_PATH  = DATA_DIR / "tamil_offensive_full.tsv"

def load_tsv(path, is_full=False):
    if not path.exists():
        raise FileNotFoundError(f"❌ File not found: {path}")
    
    if is_full:
        # FULL file: label first, text second
        df = pd.read_csv(
            path,
            sep="\t",
            header=None,
            names=["label", "text"]
        )
    else:
        df = pd.read_csv(path, sep="\t", header=None, names=["text", "label", "extra"], usecols=[0,1])
    return df

train_df = load_tsv(TRAIN_PATH)
test_df  = load_tsv(TEST_PATH)
dev_df   = load_tsv(DEV_PATH)
full_df  = load_tsv(FULL_PATH, is_full=True)

print("Train shape:", train_df.shape)
print("Test shape:", test_df.shape)
print("Dev shape:", dev_df.shape)
print("Full shape:", full_df.shape)
