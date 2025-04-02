#HuggingFace Classifier
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

class TransformerIntentClassifier:
    def __init__(self, model_path="model/transformer_output"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_path)

    def predict(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        outputs = self.model(**inputs)
        predicted = torch.argmax(outputs.logits, dim=1).item()
        label = self.model.config.id2label[predicted]
        return label
