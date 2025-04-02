import datetime

RULES = {
    "hi": "Hello! How can I help you today?",
    "hello": "Hi there! What can I do for you?",
    "how are you": "I'm just a bot, but I'm doing fine! How about you?",
    "bye": "Goodbye! Have a great day.",
    "help": "I can answer greetings and simple questions. Try saying 'hi' or 'bye'.",
    "how old are you": "I am " + str(datetime.datetime.now().year - 2024) + " years old."
}


def get_response(user_input: str) -> str:
    """Return a response based on keyword matching."""
    user_input = user_input.lower()
    for key in RULES:
        if key in user_input:
            return RULES[key]
    return "I'm not sure how to respond to that. Try asking something else."
