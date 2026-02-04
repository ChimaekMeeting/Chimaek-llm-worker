from dotenv import load_dotenv
import os
import httpx

load_dotenv()

class WeatherClient:
    def __init__(self):
        self.WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"

    async def get_weather(self, lat:float, lon:float):
        async with httpx.AsyncClient() as client:
            params = {
                "lat": lat,
                "lon": lon,
                "appid": self.WEATHER_API_KEY,
                "units": "metric"
            }

            response = await client.get(self.base_url, params=params)

            return response.json()