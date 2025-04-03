#HuggingFace Classifier
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

class TransformerIntentClassifier:
    def __init__(self, model_path="model/transformer_output"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_path)

    def predict(self, text: str) -> str:
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            logits = self.model(**inputs).logits
        prediction = torch.argmax(logits, dim=1).item()
        return self.model.config.id2label[prediction]
