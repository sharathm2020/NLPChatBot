from model.db.supabase_client import supabase, supabase_service
from datetime import datetime

TABLE = "todos"
DEFAULT_USER = "default"

def add_todo_to_db(task: str, user_id: str):
    """Adds a todo item using the service role client."""
    try:
        response = supabase_service.table(TABLE).insert({
            "task": task,
            "user_id": user_id
        }).execute()
        if response.data:
             print(f"[DB] Todo added for user {user_id}: {task}")
             return f"Got it! I've added '{task}' to your to-do list."
        else:
             print(f"[DB ERROR] Failed to add todo for user {user_id}. Response: {response}")
             return f"Sorry, I couldn't add '{task}' to your list right now."
    except Exception as e:
         print(f"[DB EXCEPTION] Failed to add todo for user {user_id}: {e}")
         return "An error occurred while adding your to-do item."

def get_todos_from_db(user_id: str):
    """Gets todos using the service role client."""
    try:
        response = supabase_service.table(TABLE).select("task").eq("user_id", user_id).execute()
        if response.data is not None:
            todos = [item["task"] for item in response.data]
            if not todos:
                return "Your to-do list is empty."
            return "Here's your current to-do list:\n" + "\n".join(f"- {task}" for task in todos)
        else:
            print(f"[DB ERROR] Failed to get todos for user {user_id}. Response: {response}")
            return "Sorry, I couldn't retrieve your to-do list right now."
    except Exception as e:
        print(f"[DB EXCEPTION] Failed to get todos for user {user_id}: {e}")
        return "An error occurred while retrieving your to-do list."

def clear_todos_from_db(user_id: str):
    """Clears todos using the service role client."""
    try:
        response = supabase_service.table(TABLE).delete().eq("user_id", user_id).execute()
        if response.data is not None:
             print(f"[DB] Todos cleared for user {user_id}. Count: {len(response.data)}")
             return "Your to-do list has been cleared."
        else:
             print(f"[DB WARN/ERROR] Failed to clear todos for user {user_id} or list was empty. Response: {response}")
             return "Your to-do list has been cleared (or was already empty)."
    except Exception as e:
        print(f"[DB EXCEPTION] Failed to clear todos for user {user_id}: {e}")
        return "An error occurred while clearing your to-do list."

