import logging
from fastapi import APIRouter
from app.schemas import ChatRequest, ChatResponse
from app.services.chatbot_service import process_message

# Setup logger
logger = logging.getLogger(__name__)
if not logger.hasHandlers():
    logging.basicConfig(level=logging.INFO)

# Router instance
router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    logger.info(f"📥 Received message: {request.message}")
    response = process_message(request.message)
    logger.info(f"📤 Responding with: {response}")
    return {"response": response}
