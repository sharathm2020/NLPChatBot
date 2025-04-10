from fastapi import Request
from bot.chatbot import ChatBot
from model.ml.hf_classifier import TransformerIntentClassifier
from model.db.auth import get_authenticated_user

classifier = TransformerIntentClassifier()
bot = ChatBot(name="NLPBot", intent_classifier=classifier)

def process_message(message: str, user_id: str) -> str:
    """Processes an incoming chat message using the chatbot, requires user_id."""
    if not user_id:
        return "Error: Could not identify user."

    response = bot.chat_with_user(message, user_id=user_id)
    return response

