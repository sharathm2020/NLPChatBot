#TO-DO Functionality
import os
import json
import re

TODO_FILE = "data/todos.json"

def load_todos():
    if not os.path.exists(TODO_FILE):
        return []
    with open(TODO_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_todos(todos):
    with open(TODO_FILE, "w") as f:
        json.dump(todos, f, indent=2)

def extract_task_text(raw_input: str) -> str:
    """
    Cleans up the user's input to extract just the task content.
    """
    # Common lead-in phrases to remove
    raw_input = raw_input.lower().strip()

    patterns = [
        r"remind me to ",
        r"add ",
        r"note to ",
        r"remember to ",
        r"put ",
        r"add '", r"add \"",
        r" to (my )?to-?do list",
        r" to my list",
        r" on the list"
    ]

    # Remove patterns
    for pattern in patterns:
        raw_input = re.sub(pattern, "", raw_input, flags=re.IGNORECASE)

    return raw_input.strip("\"' ")

def add_todo(item):
    todos = load_todos()
    cleaned = extract_task_text(item)
    todos.append(cleaned)
    save_todos(todos)
    return f"Got it! I’ve added '{cleaned}' to your to-do list."

def get_todos():
    todos = load_todos()
    if not todos:
        return "Your to-do list is empty."
    return "Here’s your current to-do list:\n" + "\n".join(f"- {task}" for task in todos)

def clear_todos():
    save_todos([])
    return "Your to-do list has been cleared."
