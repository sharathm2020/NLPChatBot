from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_ANON_KEY = os.environ.get("SUPABASE_ANON_KEY")
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_KEY")

if not SUPABASE_URL or not SUPABASE_ANON_KEY or not SUPABASE_SERVICE_KEY:
    raise EnvironmentError("Supabase URL, Anon Key, or Service Role Key not found in environment variables.")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

supabase_service: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

def create_supabase_client(token: str) -> Client | None:
    """Creates a Supabase client authenticated with the user's access token using set_session."""
    if not token:
        print("[ERROR] create_supabase_client called with no token.")
        return None
    try:
        client: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
        client.auth.set_session(access_token=token, refresh_token=None)
        print("[DEBUG] Successfully created Supabase client using set_session.")
        return client
    except Exception as e:
        print(f"[ERROR] Failed to create Supabase client with token using set_session: {e}")
        return None
