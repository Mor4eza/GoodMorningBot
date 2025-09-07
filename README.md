# GoodMorningBot

**GoodMorningBot** is a Telegram bot written in Python that sends you a personalized morning update, including:

- **Weather Forecast**  
- **Today's Calendar Events**  
- **Daily Quote or Inspiration**  
- **News Highlights (via RSS)**  

Use it to kick off your day informed and inspired with minimal setup.

---

## Features

- Fetches current weather using a weather API.
- Retrieves upcoming calendar events (e.g., via Google Calendar, depending on config).
- Sends a daily quote (motivational, humorous, or curated).
- Pulls the latest news headlines via RSS feeds.
- Combines all updates into a single message and delivers it to your Telegram every morning automatically.

---

## Table of Contents

1. [Requirements](#requirements)  
2. [Setup & Configuration](#setup--configuration)  
3. [Usage](#usage)  
4. [Customization](#customization)  
5. [Contributing](#contributing)  
6. [License](#license)

---

## Requirements

Ensure you have:

- **Python 3.8+**
- `pip` or `venv` for package management
- A **Telegram Bot Token** (via @BotFather)
- API keys and/or credentials for:
  - Weather service
  - Calendar access (e.g., Google Calendar via OAuth) // not implemented yet
  - RSS feed sources *(optional: if you want customized news sources)*

---

## Setup & Configuration

1. **Clone the repository**
   ```bash
   git clone https://github.com/Mor4eza/GoodMorningBot.git
   cd GoodMorningBot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Variables**

   Create a `.env` file or export environment variables:
   ```env
   TELEGRAM_TOKEN=your_bot_token
   WEATHER_API_KEY=your_weather_api_key
   CALENDAR_CREDENTIALS_PATH=path/to/your/calendar_credentials.json
   RSS_FEED_URLS=https://example.com/rss,https://another.com/feed
   ```

4. **Configuration**
   - In `WeatherApi.py`: set up the weather API endpoint and parameters (city, units, etc.).
   - In `News_RSS.py`: add your preferred RSS feed URLs.
   - In `DailyQuotes.py`: choose or customize your quote database or source.
   - In `GoodMorningBot.py`: ensure environment variables are loaded and correctly used.

5. **Authentication (if needed)**
   - For Google Calendar: follow the [Google Calendar API Python Quickstart][gcal_quickstart] to obtain OAuth credentials and token files.

6. **Run the bot manually (once) to test:**
   ```bash
   python GoodMorningBot.py
   ```

---

## Usage

- **Manual Run**  
  Executes the script immediately to receive a morning update:
  ```bash
  python GoodMorningBot.py
  ```

- **Automated Scheduling**  
  Use cron (Linux/macOS) or Task Scheduler (Windows) to run daily. Example cron entry (run at 7 AM every day):
  ```cron
  0 7 * * * cd /path/to/GoodMorningBot && /usr/bin/python3 GoodMorningBot.py >> bot.log 2>&1
  ```

---

## Customization

- **Weather Options**: Change units (metric/imperial), location, or provider.
- **Quotes**: Modify the list or integrate an external API for randomness.
- **RSS News**: Add or remove feed URLs.
- **Message Formatting**: Edit templates in `GoodMorningBot.py` to include emojis, sections, or styles.
- **Additional Features**: Expand to include birthday reminders, task lists, or motivational images.

---



## Contributing

Contributions are welcome! Suggestions include:

- Better error handling and logging
- Support for more APIs (e.g., news articles, inspirational images)
- Language localization for quotes or UI
- Docker Compose setup or Helm chart for Kubernetes deployment

Please open issues or PRs as needed.

---

## License

Distributed under the **MIT License**. See `LICENSE` for details.

---

### Sample /Today Command Message

```
📅 امروز یک‌شنبه، ۱۶ شهریور ۱۴۰۴

🌤 وضعیت هوا در تهران:

هوا گرم است ☀️. آب کافی بنوشید و سبک بپوشید.
 آسمان صاف و بدون ابر است 🌞.

دمای فعلی: ۳۱°
حداکثر: ۳۱° | حداقل: ۳۱°
شرایط: آسمان صاف

📰 سرخط خبرها:

- استیون اسپیلبرگ به کارگردانی فیلم Call of Duty علاقه داشت؛ اما درخواستش رد شد! زومیت | Zoomit
- مرور دوباره معمایی قدیمی؛ سیگنال واو! احتمالاً منشأ فرازمینی و قدرتی بسیار بالا داشت زومیت | Zoomit
- شیائومی ۱۶ باتری غول‌پیکری خواهد داشت زومیت | Zoomit

💡 نقل قول روز:

افسانه‌ها باید تنها به عنوان افسانه و اسطوره‌ها تنها به عنوان اسطوره آموخته شوند. آموزش موهومات به عنوان حقایق چیز وحشتناکی است. ذهن کودک آنها را می‌پذیرد و به آنها اعتقاد می‌آورد و در سالهای بعد تنها با سختی و شکنجه می‌تواند از چنگ آنها رهایی یابد. در حقیقت انسان همان طور که برای برقراری حقیقت می‌جنگد باید با خرافات نیز به مبارزه برخیزد. چرا که موهومات، نامحسوس، درک‌ناکردنی و بغرنج هستند و تکذیب آن‌ها به سختی میسر می‌شود. 
 ✍️ هیپاتیا
```

---

## Acknowledgments

- Built using Python, Telegram Bot API, open weather map APIs, RSS feeds
