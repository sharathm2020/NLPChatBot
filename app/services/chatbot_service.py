from bot.chatbot import ChatBot
from model.ml.hf_classifier import TransformerIntentClassifier
from model.ml.ner import extract_entities

# Load classifier and bot once (keep alive)
classifier = TransformerIntentClassifier()
bot = ChatBot(name="NLPBot", intent_classifier=classifier)

def process_message(message: str) -> str:
    intent = classifier.predict(message)
    entities = extract_entities(message)
    return bot.handle_intent(intent, message, entities)
