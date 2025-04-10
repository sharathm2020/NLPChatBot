# model/db/auth.py

from model.db.supabase_client import supabase, supabase_service, SUPABASE_ANON_KEY, SUPABASE_URL, SUPABASE_SERVICE_KEY
from supabase import Client
import httpx
import jwt

def _insert_user_details(user_id: str, email: str, full_name: str = None):
    """Inserts user details into the users table using the service role client."""
    print(f"[DEBUG] Attempting to insert/verify user in users table: ID={user_id}, Email={email}")
    try:
        insert_data = {
            "id": user_id,
            "email": email,
            "full_name": full_name
        }
        response = supabase_service.table("users").insert(insert_data).execute()

        if response.data:
            print(f"[DB] User {user_id} inserted into users table.")
        else:
             existing = supabase_service.table("users").select("id", count='exact').eq("id", user_id).execute()
             if existing.count == 0:
                 print(f"[ERROR] Failed to insert user {user_id}. Response: {response}")
             else:
                  print(f"[DB] User {user_id} already exists in users table (insert skipped). Data: {response}")

    except Exception as e:
        if "duplicate key value violates unique constraint" in str(e):
             print(f"[DB] User {user_id} already exists in users table (duplicate key). Error: {e}")
        else:
             print(f"[ERROR] Failed to insert/verify user {user_id} in users table: {e}")


def sign_up(email: str, password: str, user_metadata: dict = None):
    """Performs Supabase signup, optionally including user metadata."""
    print(f"[DEBUG] Starting sign_up process for email: {email}")
    signup_options = {
        "email": email,
        "password": password,
        **({"options": {"data": user_metadata}} if user_metadata else {})
    }
    result = supabase.auth.sign_up(signup_options)

    if result and result.user:
        print(f"[DEBUG] Supabase sign_up successful for {email}. User ID: {result.user.id}.")
    else:
        print(f"[DEBUG] Supabase sign_up might require verification or failed for {email}. Result: {result}")
    return result

def sign_in(email: str, password: str):
    result = supabase.auth.sign_in_with_password({"email": email, "password": password})
    if result and result.user:
        user_id = result.user.id
        try:
            print(f"[DEBUG] Validating user {user_id} exists in users table.")
            user_check = supabase.table("users").select("id", count='exact').eq("id", user_id).execute()
            if user_check.count == 0:
                print(f"[AUTH FAILURE] User {user_id} authenticated with Supabase but not found in local users table. Denying sign-in.")
                return None
            else:
                print(f"[DEBUG] User {user_id} validated successfully in users table.")

        except Exception as e:
            print(f"[ERROR] Failed to validate user {user_id} in users table during sign_in: {e}")
            print(f"[AUTH FAILURE] DB error during user validation for {user_id}. Denying sign-in.")
            return None

    return result

def get_current_user():
    session = supabase.auth.get_session()
    return session.user if session else None

def delete_user(email: str, password: str):
    try:
        session = sign_in(email, password)
        if session and session.user:
             supabase_service.auth.admin.delete_user(session.user.id)
             print(f"[AUTH] User {session.user.id} deleted.")
        else:
            print(f"[AUTH ERROR] Could not sign in to delete user {email}")
    except Exception as e:
         print(f"[AUTH ERROR] Failed to delete user {email}: {e}")

def get_user_id_from_token(token: str) -> str:
    try:
        decoded = jwt.decode(token, options={"verify_signature": False})
        return decoded.get("sub")
    except Exception as e:
        print("Error decoding token:", e)
        return None

def get_authenticated_user(token: str):
    """
    Queries the Supabase Auth endpoint to get user info from a token.
    Uses the /auth/v1/user endpoint.
    Requires SUPABASE_ANON_KEY.
    """
    headers = {
        "Authorization": f"Bearer {token}",
        "apikey": SUPABASE_ANON_KEY
    }

    try:
        response = httpx.get(f"{SUPABASE_URL}/auth/v1/user", headers=headers)
        response.raise_for_status()

        user_data = response.json()
        user_id = user_data.get("id") or user_data.get("sub")

        if not user_id:
            print("[AUTH ERROR] User id not found in Supabase user data:", user_data)
            return None

        print("[DEBUG] Supabase auth check successful for user_id:", user_id)
        return user_id

    except httpx.HTTPStatusError as http_err:
        print(f"[AUTH ERROR] HTTP error fetching Supabase user: {http_err.response.status_code} - {http_err.response.text}")
        return None
    except Exception as e:
        print(f"[AUTH ERROR] Exception fetching Supabase user: {e}")
        return None
    