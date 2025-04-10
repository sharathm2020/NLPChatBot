from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

# NEW Auth Schemas
class UserCredentials(BaseModel):
    email: str
    password: str

class SignUpRequest(UserCredentials):
    full_name: str | None = None

class AuthResponse(BaseModel):
    message: str
    access_token: str | None = None
    refresh_token: str | None = None
    user_id: str | None = None
