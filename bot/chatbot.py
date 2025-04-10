from model.ml.hf_classifier import TransformerIntentClassifier
from model.ml.ner import extract_entities
from model.api.weather_api import get_weather
from model.api.news_api import get_news
from model.api.search_api import search_answer
from model.core.math_engine import calculate
from model.db.chat_db import save_chat_to_db
from model.db.todo_db import add_todo_to_db, get_todos_from_db, clear_todos_from_db
from model.db.auth import get_authenticated_user
from model.core.preprocess import clean_math_input, extract_task
from model.config.config import CONFIDENCE_THRESHOLD
from collections import deque
import datetime
import logging

logger = logging.getLogger(__name__)

class ChatBot:
    def __init__(self, name="NLPBot", intent_classifier=None):
        self.name = name
        self.intent_classifier = intent_classifier or TransformerIntentClassifier()
        self.context = deque(maxlen=5)

        self.intent_handlers = {
            "greeting": self.handle_greeting,
            "ask_name": self.handle_ask_name,
            "ask_age": self.handle_ask_age,
            "ask_time": self.handle_ask_time,
            "ask_date": self.handle_ask_date,
            "ask_weather": self.handle_ask_weather,
            "ask_news": self.handle_ask_news,
            "ask_math": self.handle_ask_math,
            "ask_search": self.handle_ask_search,
            "add_todo": self.handle_add_todo,
            "get_todo": self.handle_get_todo,
            "clear_todo": self.handle_clear_todo,
            "goodbye": self.handle_goodbye
        }

    def handle_intent(self, intent, user_input, entities, user_id):
        handler = self.intent_handlers.get(intent)
        if handler:
            return handler(user_input, entities, user_id)
        return "I'm not sure how to respond to that."

    def handle_greeting(self, *_): return "Hello! How can I help you?"
    def handle_ask_name(self, *_): return f"I'm {self.name}, your assistant!"
    def handle_ask_age(self, *_): return f"I'm {datetime.datetime.now().year - 2024} years old."
    def handle_ask_time(self, *_): return f"The time is {datetime.datetime.now().strftime('%H:%M:%S')}."
    def handle_ask_date(self, *_): return f"Today is {datetime.datetime.now().strftime('%Y-%m-%d')}."
    def handle_ask_weather(self, _, entities):
        for ent in entities:
            if ent[1] == "GPE":
                return get_weather(ent[0])
        return get_weather()
    def handle_ask_news(self, *_): return get_news()
    def handle_ask_math(self, user_input, *_):
        cleaned = clean_math_input(user_input)
        return calculate(cleaned)
    def handle_ask_search(self, clean_input, *_): return search_answer(clean_input)
    def handle_add_todo(self, user_input, entities, user_id):
        task = extract_task(user_input)
        return add_todo_to_db(task, user_id=user_id)
    def handle_get_todo(self, user_input, entities, user_id):
        return get_todos_from_db(user_id=user_id)
    def handle_clear_todo(self, user_input, entities, user_id):
        return clear_todos_from_db(user_id=user_id)
    def handle_goodbye(self, *_): return "Goodbye! Talk to you soon."

    def chat(self):
        print(f"{self.name}: Hello! Type 'bye' to exit.")
        while True:
            user_input = input("You: ")
            if user_input.lower() in ["bye", "exit", "quit"]:
                print(f"{self.name}: Goodbye!")
                break

            self.context.append(user_input)

            intent, confidence = self.intent_classifier.predict(user_input)
            print(f"(DEBUG - Intent Detected: {intent} | Confidence: {confidence:.2f})")

            entities = extract_entities(user_input)

            if confidence < CONFIDENCE_THRESHOLD:
                response = "I'm not sure what you meant. Could you rephrase that?"
            else:
                response = self.handle_intent(intent, user_input, entities)

            print(f"{self.name}: {response}")
            save_chat_to_db(user_input, response)

    def chat_with_user(self, user_input: str, user_id: str) -> str:
        self.context.append(user_input)

        if not user_id or user_id == "default":
            logger.warning(f"chat_with_user called with invalid user_id: {user_id}")
            return "Sorry, I couldn't identify you to process the request."

        intent, confidence = self.intent_classifier.predict(user_input)
        print(f"(DEBUG - Intent Detected: {intent} | Confidence: {confidence:.2f}) User: {user_id}")

        entities = extract_entities(user_input)

        if confidence < CONFIDENCE_THRESHOLD:
            response = "I'm not sure what you meant. Could you rephrase that?"
        else:
            response = self.handle_intent(intent, user_input, entities, user_id=user_id)
            save_chat_to_db(user_input, response, user_id)

        return response


