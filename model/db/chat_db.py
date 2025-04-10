from model.db.supabase_client import supabase_service
from datetime import datetime

def save_chat_to_db(user_msg: str, bot_msg: str, user_id: str):
    """Saves chat message to the database using the service role client."""
    try:
        data = {
            "user_id": user_id,
            "user_message": user_msg,
            "bot_response": bot_msg,
        }
        response = supabase_service.table("chat_history").insert(data).execute()

        if response.data:
            print(f"[✅ DB] Insert successful: {response.data}")
        else:
            print(f"[❌ DB ERROR] Insert failed. Response: {response}")

    except Exception as e:
        print(f"[❌ DB EXCEPTION] Supabase insert failed: {e}")

def get_chat_history(user_id: str):
    """Fetches chat history for a user using the service role client."""
    try:
        response = (supabase_service.table("chat_history")
                           .select("*")
                           .eq("user_id", user_id)
                           .order("timestamp", desc=True)
                           .limit(100)
                           .execute())

        return response.data if response.data else []
    except Exception as e:
        print(f"[ERROR] Failed to fetch chat history for user {user_id}: {e}")
        return []
