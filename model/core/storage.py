import os
import json
from datetime import datetime

BASE_DIR = "data"
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
TODO_FILE = os.path.join(BASE_DIR, "todos.json")
CHAT_HISTORY_FILE = os.path.join(BASE_DIR, "chat_history.json")

os.makedirs(BASE_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)


#THIS GETS REPLACED BY SUPABASE STORING LOGIC, CAN BE REVERSED EASILY

# -------------------------
# FILE UPLOAD LOGIC
# -------------------------
def save_uploaded_file(filename: str, content: bytes) -> str:
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, "wb") as f:
        f.write(content)
    return file_path


# -------------------------
# CHAT HISTORY LOGIC
# -------------------------
def append_to_chat_history(user_input: str, bot_response: str):
    history = load_chat_history()
    history.append({
        "timestamp": datetime.now().isoformat(),
        "user": user_input,
        "bot": bot_response
    })
    with open(CHAT_HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)


def load_chat_history():
    if not os.path.exists(CHAT_HISTORY_FILE):
        return []
    with open(CHAT_HISTORY_FILE, "r") as f:
        return json.load(f)


# -------------------------
# TO-DO LIST LOGIC
# -------------------------
def load_todos():
    if not os.path.exists(TODO_FILE):
        return []
    with open(TODO_FILE, "r") as f:
        return json.load(f)


def save_todos(todos: list):
    with open(TODO_FILE, "w") as f:
        json.dump(todos, f, indent=2)
