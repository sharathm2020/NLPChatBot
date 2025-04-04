#Classifier to used the trained model
import joblib
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")

class IntentClassifier:
    def __init__(self):
        self.pipeline = joblib.load(MODEL_PATH)

    def predict(self, text: str) -> str:
        text = text.lower().strip()  # Normalize
        return self.pipeline.predict([text])[0]

