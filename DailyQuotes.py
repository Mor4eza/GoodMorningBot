from datetime import date
import sys
from urllib import response
from bs4 import BeautifulSoup
import requests
class DailyQuotes:
    def get_random_quote(self) -> str:
        """
        Returns a quote dictionary scraped from www.time.ir that contains quote, quote_author and
        an identifier for saving unique quotes to database in case of need.
        if the quote is a not formatted in a single html tag (like poetries), it makes 
        a recursive call. see time.ir for understanding how the quote is represented.
        in case of connection errors related to requests library, it will raise ConnectionError.
        """

        try:
            url = "https://www.time.ir/"
            resp = requests.get(url, timeout=10)
            resp.encoding = "utf-8"
            soup = BeautifulSoup(resp.content, "html.parser")
            text = soup.find("div",{"class":"ExpandableText_text__R_Pv6 ExpandableText_clamped__m5UVT"}).get_text()
            aouthor = soup.find("div",{"class":"BrainyQuoteAuthor_root__6iSkt"}).get_text()
            return f"{text} \n ✍️{aouthor}"

        except Exception as e:
            print("Quote fetch error:", e)

        return "موفقیت نتیجه کوشش‌های کوچک است که هر روز تکرار می‌شوند."

    def get_today_events():
        URL = "https://99taghvim.ir/"

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(URL, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.find(
            string=lambda text: text and "مناسبت امروز چیست" in text
        )

        events = []

        if title:
            # Find the closest element containing the title
            title_element = title.parent

            # Find the next li elements after the title
            for element in title_element.find_all_next("li", class_="cl_li_tryetwer"):
                events.append(element.get_text(" ", strip=True))

        print(events)

                                                                    
if __name__ == '__main__':
    print(DailyQuotes.get_today_events())