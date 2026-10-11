import requests
import jdatetime

class TodayEvents:
    def get_today_events(self) -> str:
        today = jdatetime.date.today()
        url = f"https://holidayapi.ir/jalali/{today.year}/{today.month}/{today.day}"

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            data = response.json()

            events = [
                event["description"]
                for event in data.get("events", [])
                if event.get("description")
            ]

            holiday_status = "تعطیل رسمی" if data.get("is_holiday") else "تعطیل نیست"

            return f"وضعیت امروز: {holiday_status}\n-" + "\n-".join(events)

        except requests.RequestException as error:
            print(f"Failed to fetch today's events: {error}")
            return ""
    
if __name__ == '__main__':
    print(TodayEvents.get_today_events(""))