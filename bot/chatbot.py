from model.ml.hf_classifier import TransformerIntentClassifier
from model.ml.ner import extract_entities
from model.api.weather_api import get_weather
from model.api.news_api import get_news
from model.api.search_api import search_answer
from model.core.math_engine import calculate
from model.core.memory import save_to_history
from model.core.todo import add_todo, get_todos, clear_todos
from collections import deque
import datetime

class ChatBot:
    def __init__(self, name="NLPBot"):
        self.name = name
        self.intent_classifier = TransformerIntentClassifier()
        self.context = deque(maxlen=5)

    def handle_intent(self, intent, user_input, entities):
        if intent == "greeting":
            return "Hello! How can I help you?"
        elif intent == "ask_name":
            return "I'm NLPBot, your assistant!"
        elif intent == "ask_age":
            return f"I'm {datetime.datetime.now().year - 2024} years old."
        elif intent == "ask_time":
            return f"The time is {datetime.datetime.now().strftime('%H:%M:%S')}."
        elif intent == "ask_date":
            return f"Today is {datetime.datetime.now().strftime('%Y-%m-%d')}."
        elif intent == "ask_weather":
            for ent in entities:
                if ent[1] == "GPE":
                    return get_weather(ent[0])
            return get_weather()  # default city
        elif intent == "ask_news":
            return get_news()
        elif intent == "ask_math":
            return calculate(user_input)
        elif intent == "ask_search":
            return search_answer(user_input)
        elif intent == "add_todo":
            return add_todo(user_input)
        elif intent == "get_todo":
            return get_todos()
        elif intent == "clear_todo":
            return clear_todos()
        elif intent == "goodbye":
            return "Goodbye! Talk to you soon."
        else:
            return "I'm not sure how to respond to that."

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
