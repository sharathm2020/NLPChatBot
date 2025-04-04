from bot.chatbot import ChatBot
from model.ml.hf_classifier import TransformerIntentClassifier
from model.ml.ner import extract_entities
from model.config.config import CONFIDENCE_THRESHOLD

# Load classifier and bot once (keep alive)
classifier = TransformerIntentClassifier()
bot = ChatBot(name="NLPBot", intent_classifier=classifier)

def process_message(message: str) -> str:
    intent, confidence = classifier.predict_with_confidence(message)
    print(f"[DEBUG] Intent: {intent}, Confidence: {confidence:.2f}")

    if confidence < CONFIDENCE_THRESHOLD:
        return "I'm not sure what you meant. Could you rephrase that?"

    entities = extract_entities(message)
    return bot.handle_intent(intent, message, entities)
