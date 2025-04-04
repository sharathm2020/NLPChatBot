#Store chat history
import json
import os
from datetime import datetime

HISTORY_FILE = "data/chat_history.json"

def save_to_history(user_input, bot_response):
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            try:
                history = json.load(f)
            except json.JSONDecodeError:
                history = []

    history.append({
        "timestamp": datetime.now().isoformat(),
        "user": user_input,
        "bot": bot_response
    })

    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)
