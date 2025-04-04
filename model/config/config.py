import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# Add other configuration variables as needed
# For example:
# MODEL_PATH = os.getenv("MODEL_PATH", "model/ml/model.pkl")
# VECTORIZER_PATH = os.getenv("VECTORIZER_PATH", "model/ml/vectorizer.pkl") 