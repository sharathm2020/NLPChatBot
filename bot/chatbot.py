from model.classifier import IntentClassifier
from model.ner import extract_entities
import datetime


class ChatBot:
    def __init__(self, name="NLPBot"):
        self.name = name
        self.intent_classifier = IntentClassifier()

    def handle_intent(self, intent, user_input):
        if intent == "greeting":
            return "Hello! How can I help you?"
        elif intent == "ask_name":
            return "I'm NLPBot, your friendly assistant!"
        elif intent == "ask_age":
            age = datetime.datetime.now().year - 2024
            return f"I'm {age} years old!"
        elif intent == "ask_time":
            return f"The current time is {datetime.datetime.now().strftime('%H:%M:%S')}."
        elif intent == "ask_date":
            return f"Today's date is {datetime.datetime.now().strftime('%Y-%m-%d')}."
        elif intent == "goodbye":
            return "Goodbye! See you soon."
        else:
            return "I'm not sure how to respond to that."

    def chat(self):
        print(f"{self.name}: Hello! Type 'bye' to exit.")
        while True:
            user_input = input("You: ")
            if user_input.lower() in ["bye", "exit", "quit"]:
                print(f"{self.name}: Goodbye!")
                break

            intent = self.intent_classifier.predict(user_input)
            entities = extract_entities(user_input)
            response = self.handle_intent(intent, user_input)

            print(f"{self.name}: {response}")
            if entities:
                print(f"(Entities detected: {entities})")
