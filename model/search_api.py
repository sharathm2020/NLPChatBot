#SearchAPI
import wikipedia

def search_answer(query):
    try:
        summary = wikipedia.summary(query, sentences=2)
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        return f"That’s too vague. Did you mean: {', '.join(e.options[:3])}?"
    except wikipedia.exceptions.PageError:
        return "I couldn't find anything on that topic."
    except Exception:
        return "Something went wrong while searching."
