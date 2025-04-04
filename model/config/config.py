# model/config/config.py

import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# Confidence threshold for intent classification (adjustable)
CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", 0.6))
