from sympy import sympify
import re

def calculate(expression: str) -> str:
    try:
        # Normalize spoken math terms into operators
        expression = expression.lower()
        expression = re.sub(r"plus", "+", expression)
        expression = re.sub(r"minus", "-", expression)
        expression = re.sub(r"(x|times|multiplied by)", "*", expression)
        expression = re.sub(r"(divided by|over)", "/", expression)
        expression = re.sub(r"to the power of", "**", expression)

        # Remove leading filler words (if needed)
        expression = re.sub(r"^(what is|calculate|compute|solve)\s+", "", expression)

        # Strip trailing punctuation (like '?')
        expression = expression.strip(" ?.")

        # Evaluate the cleaned expression
        result = sympify(expression).evalf()
        return f"The answer is {result}"
    except Exception as e:
        return "Sorry, I couldn't calculate that."
