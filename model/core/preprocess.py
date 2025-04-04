import re

def clean_math_input(text: str) -> str:
    # Remove only the filler prefix
    return re.sub(r"^(what\s+is|calculate|compute|solve)\s+", "", text, flags=re.IGNORECASE).strip()


def extract_task(text: str) -> str:
    text = text.lower().strip()
    patterns = [
        r"(remind me to|remember to|add|note down|put|save)\s+(.*)",
        r"add\s+'?(.*?)'?\s+to my to-do list"
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(2 if len(match.groups()) > 1 else 1).strip()
    return text

def preprocess_input(intent: str, user_input: str) -> str:
    if intent == "ask_math":
        return clean_math_input(user_input)
    elif intent == "add_todo":
        return extract_task(user_input)
    return user_input
