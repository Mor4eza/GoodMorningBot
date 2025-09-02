
import feedparser
import ssl
class News:
    def get_news(self) -> str:
        ssl._create_default_https_context = ssl._create_unverified_context
        rss_url = "https://www.zoomit.ir/feed/"
        feed = feedparser.parse(rss_url)
        print('[test](https://example.com) (test)')
        headlines = []
        for entry in feed.entries[:3]:
            entry_link = f"[{feed.feed.description}]({entry.link})"
            headlines.append(f"- {entry.title}")
        return "\n".join(headlines)