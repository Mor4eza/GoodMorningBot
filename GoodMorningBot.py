import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.error import TelegramError
from telegram.constants import ParseMode
from WeatherApi import WeatherAPI
from DailyQuotes import DailyQuotes
from News_RSS import News
import jdatetime

CITY = "Tehran"

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Your API tokens
TELEGRAM_BOT_TOKEN = "8000264991:AAE4fWZNbTvM8KqPhBK4_83Vu4xlEtXIOIw"
OPENWEATHER_API_KEY = "634fe78358fb2c0da4e326c38d56a475"

# Initialize WeatherAPI
weather_api = WeatherAPI(OPENWEATHER_API_KEY)

#initialize DailyQuote
daily_quote = DailyQuotes()

#initialize News_RSS
news_feeds = News()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    welcome_text = (
       f"🌤️ به ربات هواشناسی خوش آمدی {update.effective_user.first_name}!\n\n" \
        "من می‌توانم اطلاعات آب و هوا را برای هر مکانی ارائه دهم.\n" \
        "شما می‌توانید:\n" \
        "• موقعیت فعلی خود را ارسال کنید 📍\n" \
        "• نام یک شهر را تایپ کنید 🌆\n" \
        "• از دستور /weather به همراه نام شهر استفاده کنید\n\n" \
        "برای شروع، موقعیت خود را ارسال کنید یا نام یک شهر را تایپ کنید!"
    )
    
    # Create a keyboard with location button
    location_keyboard = KeyboardButton(text="📍ارسال موقعیت", request_location=True)
    reply_markup = ReplyKeyboardMarkup(
        [[location_keyboard]], 
        resize_keyboard=True, 
        one_time_keyboard=True
    )
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming location messages."""
    try:
        location = update.message.location
        lat = location.latitude
        lon = location.longitude
        
        # Show typing indicator
        await update.message.reply_chat_action(action="typing")
        
        # Get weather information using WeatherAPI
        weather_data = weather_api.get_weather_by_coords(lat, lon)
        
        if weather_data:
            weather_info = weather_api.format_weather_message(weather_data)
            emoji = weather_api.get_weather_emoji(weather_data['weather_icon'])
            await update.message.reply_text(f"{emoji} {weather_info}")
        else:
            await update.message.reply_text("❌ متاسفانه اطلاعات آب و هوای این موقعیت در درسترس نمی‌باشد")
        
    except Exception as e:
        logger.error(f"Error in handle_location: {e}")
        await update.message.reply_text("❌ متاسفانه اطلاعات آب و هوای این موقعیت در درسترس نمی‌باشد")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle text messages (city names)."""
    try:
        city_name = update.message.text.strip()
        
        if not city_name:
            await update.message.reply_text("نام شهر را وارد کنید")
            return
        
        # Show typing indicator
        await update.message.reply_chat_action(action="typing")
        
        # Get weather information using WeatherAPI
        weather_data = weather_api.get_weather_by_city(city_name)
        
        if weather_data:
            weather_info = weather_api.format_weather_message(weather_data)
            emoji = weather_api.get_weather_emoji(weather_data['weather_icon'])
            await update.message.reply_text(f"{emoji} {weather_info}")
        else:
            await update.message.reply_text("❌ شهر پیدا نشد یا اطلاعات آب و هوا در دسترس نیست. لطفاً نام شهر را بررسی کرده و دوباره تلاش کنید."
)
        
    except Exception as e:
        logger.error(f"Error in handle_text: {e}")
        await update.message.reply_text("❌ متأسفم، نتوانستم درخواست شما را پردازش کنم.")

async def weather_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /weather command with city name."""
    if not context.args:
        await update.message.reply_text("لطفاً نام یک شهر را وارد کنید. مثال: /weather London")
        return
    city_name = " ".join(context.args)
    #5014301407
    # Show typing indicator
    await update.message.reply_chat_action(action="typing")
    
    # Get weather information using WeatherAPI
    weather_data = weather_api.get_weather_by_city(city_name)
    
    if weather_data:
        weather_info = weather_api.format_weather_message(weather_data)
        emoji = weather_api.get_weather_emoji(weather_data['weather_icon'])
        await update.message.reply_text(f"{emoji} {weather_info}")
    else:
        await update.message.reply_text("❌ شهر پیدا نشد یا اطلاعات آب و هوا در دسترس نیست. لطفاً نام شهر را بررسی کرده و دوباره تلاش کنید."
)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #Send a message when the command /help is issued
    help_text = (
       f"🤖 راهنمای ربات هواشناسی\n\n" \
        "دستورات موجود:\n" \
        "/start - راه‌اندازی ربات\n" \
        "/weather [شهر] - دریافت وضعیت هوا برای یک شهر خاص\n" \
        "/help - نمایش این پیام راهنما\n" \
        "/today - نمایش اطلاعات امروز\n\n" \
        "شما همچنین می‌توانید:\n" \
        "• موقعیت فعلی خود را ارسال کنید 📍\n" \
        "• نام هر شهری را تایپ کنید 🌆"

    )
    await update.message.reply_text(help_text)

async def today_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #Send Today Message when the command /today is issued
    try:
        msg = build_message()
        await update.message.reply_text(msg, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    except Exception as e:
        await update.message.reply_text("⚠️ خطا در گرفتن اطلاعات روزانه")
        print("Today command error:", e)

# ---------------------------------------- #
# Build Daily Message
def build_message():
    dateTime = jdatetime
    jdatetime.set_locale(jdatetime.FA_LOCALE)
    today = dateTime.date.today().strftime("%A، %d %B %Y")
    weather_data = weather_api.get_weather_by_city(CITY)
    city = weather_data["city"]
    temp = weather_data["temperature"] 
    max_temp = weather_data["temp_max"]
    min_temp = weather_data["temp_min"]
    main = weather_data["main"]
    condition = weather_data["description"]
    weather_message = weather_tip(temp, main)

    news = news_feeds.get_news()
    quote = daily_quote.get_random_quote()
    
    message = f"""
📅 امروز {today}

🌤 وضعیت هوا در {city}:

{weather_message}

دمای فعلی: {int(temp)}°
حداکثر: {int(max_temp)}° | حداقل: {int(min_temp)}°
شرایط: {condition}

📰 سرخط خبرها:

{news}

💡 نقل قول روز:

{quote}
"""
    return WeatherAPI.to_persian_numbers(message)


# ---------------------------------------- #
# Persian Weather Interpretation
def weather_tip(temp, condition):
    condition = condition.lower()
    advice = ""

    if temp < 5:
        advice = "هوا بسیار سرد است 🥶. لباس‌های خیلی گرم بپوشید."
    elif 5 <= temp < 15:
        advice = "هوا سرد است ❄️. ژاکت یا کاپشن فراموش نشود."
    elif 15 <= temp < 25:
        advice = "هوا معتدل و دلپذیر است 🌤."
    elif 25 <= temp < 35:
        advice = "هوا گرم است ☀️. آب کافی بنوشید و سبک بپوشید."
    else:
        advice = "هوا بسیار داغ است 🔥. مراقب گرمازدگی باشید."

    advice += "\n"
    
    if "rain" in condition:
        advice += " احتمال بارش وجود دارد ☔. چتر همراه داشته باشید."
    elif "snow" in condition:
        advice += " برف در راه است ❄️. مراقب لغزندگی باشید."
    elif "storm" in condition or "thunder" in condition:
        advice += " طوفان و رعد و برق ⚡. در خانه بمانید در صورت امکان."
    elif "wind" in condition:
        advice += " هوا بادخیز است 💨. مراقب وسایل سبک باشید."
    elif "cloud" in condition:
        advice += " آسمان نیمه‌ابری ☁️."
    elif "clear" in condition:
        advice += " آسمان صاف و بدون ابر است 🌞."

    return advice



def main():
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("weather", weather_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("today", today_command))
    application.add_handler(MessageHandler(filters.LOCATION, handle_location))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    application.add_error_handler(error_handler)
    # Start the Bot
    print("Bot is running...")
    application.run_polling()

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(f"Exception: {context.error}")  # log full error
    try:
        if update and hasattr(update, "message") and update.message:
            await update.message.reply_text("⚠️ خطایی رخ داد، لطفاً دوباره تلاش کنید.")
    except TelegramError:
        pass

if __name__ == "__main__":
    main()