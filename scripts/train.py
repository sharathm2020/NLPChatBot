#Train the Model
import json
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

#Basic Logistic Regression model for training(used as a very baseline)
with open("data/intents.json") as f:
    data = json.load(f)

X = [item["text"] for item in data]
y = [item["intent"] for item in data]

pipeline = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("clf", LogisticRegression())
])

pipeline.fit(X, y)

joblib.dump(pipeline, "model/model.pkl")

print("Training complete. Model saved to model/model.pkl")
