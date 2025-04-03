#TO-DO Functionality
import os
import json

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

def add_todo(item):
    todos = load_todos()
    todos.append(item)
    save_todos(todos)
    return f"Got it! I’ve added '{item}' to your to-do list."

def get_todos():
    todos = load_todos()
    if not todos:
        return "Your to-do list is empty."
    return "Here’s your current to-do list:\n" + "\n".join(f"- {task}" for task in todos)

def clear_todos():
    save_todos([])
    return "Your to-do list has been cleared."
