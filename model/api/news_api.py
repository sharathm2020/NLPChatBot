#News API
import requests
from model.config.config import NEWS_API_KEY

def get_news():
    api_key = NEWS_API_KEY
    if not api_key:
        return "Error: News API key not configured."

    url = f"https://newsapi.org/v2/top-headlines?category=technology&q=stock%20market&language=en&pageSize=3&apiKey={api_key}"

    try:
        res = requests.get(url)
        data = res.json()
        if data["status"] != "ok":
            return "Couldn't fetch news right now."

        headlines = [article["title"] for article in data["articles"][:3]]
        return "Here are some headlines:\n" + "\n".join(f"- {title}" for title in headlines)
    except Exception:
        return "There was an error accessing the news."
