#Store chat history
import json
import os
from model.core.storage import append_to_chat_history

def save_to_history(user_input, bot_response):
    append_to_chat_history(user_input, bot_response)
