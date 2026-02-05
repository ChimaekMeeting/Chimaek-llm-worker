from src.client.weather_client import WeatherClient
from typing import Dict, Tuple, Any
import textwrap

class WeatherChecker:
    def __init__(self):
        self.weather_client = WeatherClient()
        self.init_message = textwrap.dedent("""
            반갑습니다! 현재 위치를 중심으로 최적의 산책로를 추천해 드릴게요.
            원하시는 산책 조건을 말씀해 주시겠어요?
            1. 코스 종류: 순환 vs 편도
            2. 도착 지점: (편도 선택 시) 목적지 명칭
            3. 산책 테마: 운동, 데이트, 반려동물 동반 등
        """).strip()

    async def check_weather(self, lat: float, lon: float) -> Dict[str, Any]:
        """
        날씨를 검색합니다.
        """
        return await self.weather_client.get_weather(lat, lon)
    
    def get_weather_message(self, main_condition: str) -> str:
        """
        날씨별 적절한 메시지를 생성합니다. 
        """
        messages = {
            "Rain": "현재 비가 내리고 있어요. ☔ 외출하실 때 우산 꼭 챙기세요!",
            "Snow": "포근한 눈이 내리고 있네요. ❄️ 길이 미끄러울 수 있으니 주의하세요!",
            "Clear": "날씨가 매우 맑습니다. ☀️ 기분 좋게 산책하기 딱 좋은 날이에요."
        }

        return messages.get(main_condition, "산책하기 참 쾌적한 날씨입니다. 🌿")
    
    async def generate_init_message(self, lat: float, lon: float) -> Tuple[dict, str]:
        """
        초기 메시지를 조립하여 반환합니다.
        """
        # 날씨 검색
        weather_data = await self.check_weather(lat, lon)
        condition = weather_data["weather"][0]["main"]  # 예: "Rain", "Snow" etc

        # 문구 생성
        weather_desc = self.get_weather_message(condition)

        return weather_data, f"{weather_desc}\n\n{self.init_message}"