from model.db.auth import sign_up, sign_in, get_current_user
from model.db.supabase_client import create_supabase_client

email = "sharathmahadevan3@gmail.com"
password = "Test1234!"

try:
    print("Signing up...")
    user, _ = sign_up(email, password)
    print("Signup success:", get_current_user())
except Exception as e:
    print("User may already exist. Proceeding...")

try:
    print("Signing in...")
    session = sign_in(email, password)
    access_token = session.session.access_token
    user_id = session.user.id
    print("Login success. Token acquired.")

    authed_supabase = create_supabase_client(access_token)

    print("Attempting authenticated insert into users table...")
    user_data = {
        "id": user_id,
        "full_name": "Sharath Mahadevan"
    }
    response = authed_supabase.table("users").insert(user_data).execute()
    print("Insert successful:", response.data)

    print("Attempting authenticated insert into chat_history...")
    response = authed_supabase.table("chat_history").insert({
        "user_id": user_id,
        "user_message": "Hello from test_auth.py!",
        "bot_response": "It worked!"
    }).execute()

    print("Insert successful:", response.data)

except Exception as e:
    print("Error during authenticated insert or login:", e)
