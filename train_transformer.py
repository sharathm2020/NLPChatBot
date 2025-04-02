#Train the Transformer Model
from datasets import load_dataset, Dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
import torch
import json

# Load training data
with open("data/intents.json") as f:
    raw_data = json.load(f)

texts = [item["text"] for item in raw_data]
labels = list(set(item["intent"] for item in raw_data))
label2id = {label: i for i, label in enumerate(labels)}
id2label = {i: label for label, i in label2id.items()}

# Create HuggingFace Dataset
dataset = Dataset.from_dict({
    "text": texts,
    "label": [label2id[item["intent"]] for item in raw_data]
})

tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
model = AutoModelForSequenceClassification.from_pretrained(
    "distilbert-base-uncased", num_labels=len(labels),
    id2label=id2label, label2id=label2id
)

def preprocess(examples):
    return tokenizer(examples["text"], truncation=True, padding=True)

tokenized_dataset = dataset.map(preprocess, batched=True)

training_args = TrainingArguments(
    output_dir="./model/transformer_output",
    per_device_train_batch_size=4,
    num_train_epochs=5,
    logging_steps=10,
    save_total_limit=1,
    logging_dir="./logs",
    report_to="none"
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset
)

trainer.train()
trainer.save_model("./model/transformer_output")
tokenizer.save_pretrained("./model/transformer_output")

print("Transformer model trained and saved.")
