import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from WeatherApi import WeatherAPI

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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    welcome_text = (
        f"🌤️ Welcome to Weather Bot {update.effective_user.first_name}!\n\n"
        "I can provide weather information for any location.\n"
        "You can:\n"
        "• Send your current location 📍\n"
        "• Type a city name 🌆\n"
        "• Use /weather command followed by city name\n\n"
        "Send your location or type a city name to get started!"
    )
    
    # Create a keyboard with location button
    location_keyboard = KeyboardButton(text="📍 Send Location", request_location=True)
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
            await update.message.reply_text("❌ Sorry, I couldn't fetch weather data for your location.")
        
    except Exception as e:
        logger.error(f"Error in handle_location: {e}")
        await update.message.reply_text("❌ Sorry, I couldn't process your location.")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle text messages (city names)."""
    try:
        city_name = update.message.text.strip()
        
        if not city_name:
            await update.message.reply_text("Please provide a city name.")
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
            await update.message.reply_text("❌ City not found or weather data unavailable. Please check the city name and try again.")
        
    except Exception as e:
        logger.error(f"Error in handle_text: {e}")
        await update.message.reply_text("❌ Sorry, I couldn't process your request.")

async def weather_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /weather command with city name."""
    if not context.args:
        await update.message.reply_text("Please provide a city name. Example: /weather London")
        return
    
    city_name = " ".join(context.args)
    
    # Show typing indicator
    await update.message.reply_chat_action(action="typing")
    
    # Get weather information using WeatherAPI
    weather_data = weather_api.get_weather_by_city(city_name)
    
    if weather_data:
        weather_info = weather_api.format_weather_message(weather_data)
        emoji = weather_api.get_weather_emoji(weather_data['weather_icon'])
        await update.message.reply_text(f"{emoji} {weather_info}")
    else:
        await update.message.reply_text("❌ City not found or weather data unavailable. Please check the city name and try again.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /help is issued."""
    help_text = (
        "🤖 Weather Bot Help\n\n"
        "Available commands:\n"
        "/start - Start the bot\n"
        "/weather [city] - Get weather for a specific city\n"
        "/help - Show this help message\n\n"
        "You can also:\n"
        "• Send your current location 📍\n"
        "• Type any city name 🌆"
    )
    await update.message.reply_text(help_text)

def main():
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("weather", weather_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.LOCATION, handle_location))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    # Start the Bot
    print("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()