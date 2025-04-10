import logging
from fastapi import APIRouter, UploadFile, File, Request, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from app.schemas import ChatRequest, ChatResponse
from app.services.chatbot_service import process_message
from model.core.storage import save_uploaded_file
from model.db.auth import get_authenticated_user
from model.db.chat_db import get_chat_history
from typing import List, Dict, Any
from app.todo_routes import get_current_user_id

logger = logging.getLogger(__name__)
if not logger.hasHandlers():
    logging.basicConfig(level=logging.INFO)

router = APIRouter(prefix="/chat", tags=["Chat"])

# -----------------------------
# Chat Message Endpoint
# -----------------------------
@router.post("/", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest, user_id: str = Depends(get_current_user_id)):
    logger.info(f"Received message from user {user_id}: {request.message}")

    response = process_message(request.message, user_id=user_id)

    logger.info(f"Responding to user {user_id} with: {response}")
    return {"response": response}

# -----------------------------
# Chat History Endpoint
# -----------------------------
@router.get("/history", response_model=List[Dict[str, Any]])
async def get_chat_history_endpoint(user_id: str = Depends(get_current_user_id)):
    """Fetches chat history for the authenticated user."""
    logger.info(f"Fetching chat history for user: {user_id}")
    try:
        history = get_chat_history(user_id=user_id)
        return history
    except Exception as e:
        logger.error(f"Error fetching chat history for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve chat history.")

# -----------------------------
# File Upload Endpoint
# -----------------------------
@router.post("/upload")
async def upload_file(file: UploadFile = File(...), user_id: str = Depends(get_current_user_id)):
    logger.info(f"📎 Receiving file upload from user {user_id}: {file.filename}")

    try:
        content = await file.read()
        saved_path = save_uploaded_file(file.filename, content, user_id=user_id)

        logger.info(f"File saved for user {user_id}: {file.filename} -> {saved_path}")
        message = f"File **{file.filename}** uploaded successfully and saved."

        return JSONResponse(content={"success": True, "response": message}, status_code=200)

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"File upload failed for user {user_id}: {e}")
        return JSONResponse(content={"success": False, "response": f"Upload failed: {e}"}, status_code=500)
