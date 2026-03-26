import pandas as pd

df = pd.read_csv("fine_grained_train.csv")

with open("fine_grained_aligned.txt", "w", encoding="utf-8") as f:
    f.write(df.to_string(index=False))
