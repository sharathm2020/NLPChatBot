from model.ml.hf_classifier import TransformerIntentClassifier
from model.ml.ner import extract_entities
from model.api.weather_api import get_weather
from model.api.news_api import get_news
from model.api.search_api import search_answer
from model.core.math_engine import calculate
from model.core.memory import save_to_history
from model.core.todo import add_todo, get_todos, clear_todos
from model.core.preprocess import clean_math_input, extract_task
from collections import deque
import datetime

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

    def handle_intent(self, intent, user_input, entities):
        handler = self.intent_handlers.get(intent)
        if handler:
            return handler(user_input, entities)
        return "I'm not sure how to respond to that."

    # Intent handler methods
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
    def handle_add_todo(self, user_input, *_):
        task = extract_task(user_input)
        return add_todo(task)

    def handle_get_todo(self, *_): return get_todos()
    def handle_clear_todo(self, *_): return clear_todos()
    def handle_goodbye(self, *_): return "Goodbye! Talk to you soon."

    def chat(self):
        print(f"{self.name}: Hello! Type 'bye' to exit.")
        while True:
            user_input = input("You: ")
            if user_input.lower() in ["bye", "exit", "quit"]:
                print(f"{self.name}: Goodbye!")
                break

            self.context.append(user_input)
            intent = self.intent_classifier.predict(user_input)
            entities = extract_entities(user_input)
            print(f"(DEBUG - Intent Detected: {intent})")
            response = self.handle_intent(intent, user_input, entities)
            print(f"{self.name}: {response}")
            save_to_history(user_input, response)
