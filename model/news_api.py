#News API
import requests

def get_news():
    api_key = "e265e272b73c408d8ce6a4954e5baa3b"
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
