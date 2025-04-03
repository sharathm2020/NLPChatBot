#Mathematical Expression Handling
import re

def calculate(expression: str):
    try:
        # Normalize words to symbols
        expression = expression.lower()
        expression = re.sub(r"plus", "+", expression)
        expression = re.sub(r"minus", "-", expression)
        expression = re.sub(r"(x|times|multiplied by)", "*", expression)
        expression = re.sub(r"(divided by|over)", "/", expression)

        # Extract the math part (numbers + ops)
        expression = re.findall(r"[\d+\-*/.]+", expression.replace(" ", ""))
        if not expression:
            return "I couldn’t detect a valid math expression."

        result = eval("".join(expression))
        return f"The answer is {result}"
    except Exception:
        return "Sorry, I couldn’t calculate that."
