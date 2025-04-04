import logging
import os
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from app.schemas import ChatRequest, ChatResponse
from app.services.chatbot_service import process_message

logger = logging.getLogger(__name__)
if not logger.hasHandlers():
    logging.basicConfig(level=logging.INFO)

router = APIRouter(prefix="/chat", tags=["Chat"])

UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    logger.info(f"📥 Received message: {request.message}")
    response = process_message(request.message)
    logger.info(f"📤 Responding with: {response}")
    return {"response": response}

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        logger.info(f"📎 File saved: {file.filename} -> {file_path}")

        # 🔥 Enhanced message for chatbot UI
        message = f"📁 File **{file.filename}** uploaded successfully. Saved to `temp_uploads/`."
        return JSONResponse(content={"success": True, "response": message}, status_code=200)

    except Exception as e:
        logger.error(f"❌ File upload failed: {e}")
        return JSONResponse(content={"success": False, "response": f"Upload failed: {e}"}, status_code=500)

