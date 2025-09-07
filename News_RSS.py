import feedparser
import ssl
from enum import Enum

class News:
    class NewsSources(Enum):
        zoomit = "https://www.zoomit.ir/feed/"
        digiato = "https://www.digiato.com/feed/"
        # isna = "https://www.isna.ir/rss"
        bbc_persian = "https://feeds.bbci.co.uk/persian/rss.xml"
        irna = "https://www.irna.ir/rss"
     
    def get_news(self, source: NewsSources.digiato, count: int = 1) -> str:
        ssl._create_default_https_context = ssl._create_unverified_context
        print(source.value)
        rss_url = source.value
        feed = feedparser.parse(rss_url)
        headlines = []
        for entry in feed.entries[:count]:
            entry_link = f"<a href='{entry.link}'>{source.name}</a>"
            headlines.append(f"- {entry.title} {entry_link}")
        return "\n".join(headlines)
    
       

