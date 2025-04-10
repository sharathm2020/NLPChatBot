#Train the Transformer Model
import json
import torch
from torch.utils.data import Dataset
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from tabulate import tabulate
from model.core.storage import BASE_DIR
import pprint
import os

# Load data
with open(os.path.join(BASE_DIR, "intents.json")) as f:
    raw_data = json.load(f)

texts = [item["text"] for item in raw_data]
labels = sorted(set(item["intent"] for item in raw_data))
label2id = {label: i for i, label in enumerate(labels)}
id2label = {i: label for label, i in label2id.items()}
intents = [label2id[item["intent"]] for item in raw_data]

# Split dataset use 1/3 for testing, rest for training
train_texts, test_texts, train_labels, test_labels = train_test_split(
    texts, intents, test_size=0.2, stratify=intents, random_state=42
)

class IntentDataset(Dataset):
    def __init__(self, texts, labels, tokenizer):
        self.encodings = tokenizer(texts, truncation=True, padding=True)
        self.labels = labels

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        return {
            "input_ids": torch.tensor(self.encodings["input_ids"][idx]),
            "attention_mask": torch.tensor(self.encodings["attention_mask"][idx]),
            "labels": torch.tensor(self.labels[idx]),
        }

#Use DistilBERT as the base model -> Will upgrade to BERT model at some point
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

train_dataset = IntentDataset(train_texts, train_labels, tokenizer)
test_dataset = IntentDataset(test_texts, test_labels, tokenizer)

model = AutoModelForSequenceClassification.from_pretrained(
    "distilbert-base-uncased",
    num_labels=len(label2id),
    id2label=id2label,
    label2id=label2id
)

training_args = TrainingArguments(
    output_dir="./model/transformer_output",
    per_device_train_batch_size=4,
    num_train_epochs=5,
    logging_dir="./logs",
    save_strategy="epoch",
    report_to="none"
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
)

trainer.train()

model.save_pretrained("./model/transformer_output")
tokenizer.save_pretrained("./model/transformer_output")

print("Transformer fine-tuning complete. Model saved.")

# Ideally want to evaulate on a validation set, but for now we use the test
predictions = trainer.predict(test_dataset)
preds = torch.argmax(torch.tensor(predictions.predictions), axis=1)

all_label_ids = sorted(id2label.keys()) 

report = classification_report(
    test_labels,
    preds.numpy(),
    labels=all_label_ids,
    target_names=[id2label[i] for i in all_label_ids],
    output_dict=True,
    zero_division=0
)

os.makedirs("model", exist_ok=True)
with open("model/metrics.json", "w") as f:
    json.dump(report, f, indent=2)

print("📊 Evaluation complete. Metrics saved to model/metrics.json")

#Print out metric table from Intent Classifier training/testing runs
#Include all pertaining metrics such as precision, recall, f1 etc..
print("\n Intent Classification Report:")
headers = ["Intent", "Precision", "Recall", "F1-Score", "Support"]
rows = []

for label in all_label_ids:
    intent = id2label[label]
    row = report.get(intent)
    if row:
        rows.append([
            intent,
            f"{row['precision']:.2f}",
            f"{row['recall']:.2f}",
            f"{row['f1-score']:.2f}",
            int(row['support'])
        ])
print(tabulate(rows, headers=headers, tablefmt="pretty"))

#Print out stats of micro/macro/weighted averages of scores
print("\n Averages:")
summary_keys = ["micro avg", "macro avg", "weighted avg"]
for key in summary_keys:
    avg = report.get(key)
    if avg:
        print(f"- {key}: F1 = {avg['f1-score']:.2f}, Precision = {avg['precision']:.2f}, Recall = {avg['recall']:.2f}")
