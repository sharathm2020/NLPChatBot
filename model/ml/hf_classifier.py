from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from model.config.config import CONFIDENCE_THRESHOLD

class TransformerIntentClassifier:
    def __init__(self, model_path="model/transformer_output"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_path)

    def predict(self, text: str) -> tuple[str, float]:
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            logits = self.model(**inputs).logits
            probs = torch.softmax(logits, dim=1)
        confidence, prediction = torch.max(probs, dim=1)
        intent = self.model.config.id2label[prediction.item()]
        return intent, confidence.item()

    def predict_with_confidence(self, text: str) -> tuple[str, float]:
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            logits = self.model(**inputs).logits
            probs = torch.nn.functional.softmax(logits, dim=1)
            confidence, prediction = torch.max(probs, dim=1)
            label = self.model.config.id2label[prediction.item()]
            return label, confidence.item()
