import re
import pandas as pd

def preprocess_text(text):
    
    if pd.isna(text):
        return ""

    text = str(text).strip()

    text = re.sub(r"http\S+|www\S+", "", text)

    text = re.sub(r"@\w+", "", text)

    text = re.sub(r"#(\w+)", r"\1", text)

    text = re.sub(r"\s+", " ", text)

    return text
