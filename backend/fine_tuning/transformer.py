# ===============================
# 1 Install dependencies (run once)
# ===============================
#pip install transformers datasets scikit-learn torch pandas

# ===============================
# 2 Import libraries
# ===============================
import pandas as pd
import torch
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from datasets import Dataset

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
    DataCollatorWithPadding
)

# ===============================
# 3 Load dataset
# ===============================
df = pd.read_csv("balanced_5000_dataset.tsv", sep="\t")

print("Dataset size:", len(df))
print(df.head())

# ===============================
# 4 Convert labels
# ===============================
label_map = {
    "not_offensive": 0,
    "offensive": 1
}

df["label"] = df["label"].map(label_map)

# ===============================
# 5 Train / Test split
# ===============================
train_texts, test_texts, train_labels, test_labels = train_test_split(
    df["text"],
    df["label"],
    test_size=0.2,
    random_state=42
)

train_df = pd.DataFrame({
    "text": train_texts,
    "label": train_labels
})

test_df = pd.DataFrame({
    "text": test_texts,
    "label": test_labels
})

train_dataset = Dataset.from_pandas(train_df, preserve_index=False)
test_dataset = Dataset.from_pandas(test_df, preserve_index=False)

# ===============================
# 6 Load tokenizer
# ===============================
MODEL_NAME = "xlm-roberta-base"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

def tokenize(example):
    return tokenizer(
        example["text"],
        truncation=True,
        max_length=128
    )

train_dataset = train_dataset.map(tokenize, batched=True)
test_dataset = test_dataset.map(tokenize, batched=True)

# ===============================
# 7 Format dataset
# ===============================
train_dataset.set_format(
    type="torch",
    columns=["input_ids", "attention_mask", "label"]
)

test_dataset.set_format(
    type="torch",
    columns=["input_ids", "attention_mask", "label"]
)

# ===============================
# 8 Load model
# ===============================
model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_NAME,
    num_labels=2
)

# ===============================
# 9 Data collator
# ===============================
data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

# ===============================
# 10 Metrics
# ===============================
def compute_metrics(eval_pred):

    logits, labels = eval_pred
    predictions = logits.argmax(axis=-1)

    precision, recall, f1, _ = precision_recall_fscore_support(
        labels,
        predictions,
        average="binary"
    )

    acc = accuracy_score(labels, predictions)

    return {
        "accuracy": acc,
        "f1": f1,
        "precision": precision,
        "recall": recall
    }

# ===============================
# 11 Training configuration
# ===============================
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    learning_rate=2e-5,
    logging_dir="./logs",
    logging_strategy="epoch",
    eval_strategy="epoch",
    save_strategy="epoch",
    disable_tqdm=True
)

# ===============================
# 12 Trainer
# ===============================
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
    data_collator=data_collator,
    compute_metrics=compute_metrics
)

# ===============================
# 13 Train model
# ===============================
print("\nStarting training...\n")
trainer.train()

# ===============================
# 14 Evaluate model
# ===============================
print("\nEvaluating model...\n")

results = trainer.evaluate()

print(results)

# ===============================
# 15 Save model
# ===============================
model.save_pretrained("offensive_model")
tokenizer.save_pretrained("offensive_model")

print("\nModel saved in offensive_model/")