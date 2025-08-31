# WeatherAPI.py
import requests
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class WeatherAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"

    def _make_api_request(self, url: str) -> Optional[Dict[str, Any]]:
        """Make API request to OpenWeatherMap."""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            return None
        except ValueError as e:
            logger.error(f"JSON parsing failed: {e}")
            return None
    
    def _parse_weather_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse weather data from API response."""

        return {
            'city': data.get('name', 'Unknown'),
            'country': data['sys'].get('country', '') if 'sys' in data else '',
            'temperature': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'humidity': data['main']['humidity'],
            'temp_min': data['main']['temp_min'],
            'temp_max': data['main']['temp_max'],
            'description': data['weather'][0]['description'].title(),
            'main': data['weather'][0]['main'],
            'wind_speed': data['wind']['speed'],
            'pressure': data['main']['pressure'],
            'visibility': data.get('visibility'),
            'weather_icon': data['weather'][0]['icon']
        }
    
    
    def get_weather_by_coords(self, lat: float, lon: float) -> Optional[Dict[str, Any]]:
        """Get weather information using coordinates."""
        url = f"{self.base_url}?lat={lat}&lon={lon}&appid={self.api_key}&units=metric&lang=fa"
        data = self._make_api_request(url)
        
        if data and data.get('cod') == 200:
            return self._parse_weather_data(data)
        return None
    
    def get_weather_by_city(self, city_name: str) -> Optional[Dict[str, Any]]:
        """Get weather information using city name."""
        url = f"{self.base_url}?q={city_name}&appid={self.api_key}&units=metric&lang=fa"
        data = self._make_api_request(url)
        
        if data and data.get('cod') == 200:
            return self._parse_weather_data(data)
        return None
    
    def to_persian_numbers(input_str):
        """Convert English digits to Persian/Arabic digits in a string."""
        return str(input_str).translate(str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹'))


    def format_weather_message(self, weather_data: Dict[str, Any]) -> str:
        """Format weather data into a user-friendly message."""
        try:
            message = (
                
                f"🌤️ وضعیت آب و هوا در {WeatherAPI.to_persian_numbers(weather_data['city'])}, {WeatherAPI.to_persian_numbers(weather_data['country'])}:\n\n"
                f"• دما: {WeatherAPI.to_persian_numbers(weather_data['temperature'])} سانتی گراد ( دمای احساسی {WeatherAPI.to_persian_numbers(weather_data['feels_like'])} سانتی گراد)\n"
                f"• شرایط: {weather_data['description']}\n"
                f"• رطوبت: {WeatherAPI.to_persian_numbers(weather_data['humidity'])}%\n"
                f"• سرعت باد: {WeatherAPI.to_persian_numbers(weather_data['wind_speed'])} متر بر ثانیه\n"
                f"• فشار: {WeatherAPI.to_persian_numbers(weather_data['pressure'])} هکتوپاسکال"
            )
            
            if weather_data.get('visibility'):
                visibility_km = weather_data['visibility'] / 1000
                visibility_km_persian_numbers = WeatherAPI.to_persian_numbers(visibility_km)
                message += f"\n• وسعت دید: {visibility_km_persian_numbers} کیلومتر"
                
            return message
        except KeyError as e:
            logger.error(f"Missing key in weather data: {e}")
            return "❌ Error formatting weather information."
    
    def get_weather_emoji(self, icon_code: str) -> str:
        """Get appropriate emoji based on weather icon code."""
        emoji_map = {
            '01d': '☀️',  # clear sky day
            '01n': '🌙',  # clear sky night
            '02d': '⛅',  # few clouds day
            '02n': '⛅',  # few clouds night
            '03d': '☁️',  # scattered clouds
            '03n': '☁️',
            '04d': '☁️',  # broken clouds
            '04n': '☁️',
            '09d': '🌧️',  # shower rain
            '09n': '🌧️',
            '10d': '🌦️',  # rain day
            '10n': '🌧️',  # rain night
            '11d': '⛈️',  # thunderstorm
            '11n': '⛈️',
            '13d': '❄️',  # snow
            '13n': '❄️',
            '50d': '🌫️',  # mist
            '50n': '🌫️'
        }
        return emoji_map.get(icon_code, '🌤️')