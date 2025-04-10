#TO-DO Functionality
import os
import json
import re
from model.core.storage import load_todos as load_from_storage, save_todos as save_to_storage

def extract_task_text(raw_input: str) -> str:
    """
    Cleans up the user's input to extract just the task content.
    """
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

    for pattern in patterns:
        raw_input = re.sub(pattern, "", raw_input, flags=re.IGNORECASE)

    return raw_input.strip("\"' ")

def add_todo(item):
    todos = load_from_storage()
    cleaned = extract_task_text(item)
    todos.append(cleaned)
    save_to_storage(todos)
    return f"Got it! I’ve added '{cleaned}' to your to-do list."

def get_todos():
    todos = load_from_storage()
    if not todos:
        return "Your to-do list is empty."
    return "Here’s your current to-do list:\n" + "\n".join(f"- {task}" for task in todos)

def clear_todos():
    save_to_storage([])
    return "Your to-do list has been cleared."

