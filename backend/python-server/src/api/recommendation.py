from fastapi import APIRouter, Depends
from src.schema.recommendation_schema import InitRequest, ChatRequest, ChatResponse
from src.service.recommendation_service import RecommendationService

router = APIRouter(
    prefix="/api/recommendation",
    tags=["recommendation"]
)

# 싱글톤 인스턴스
route_service = RecommendationService()

#서비스 인스턴스를 관리하는 함수(의존성 주입용)
def get_route_service() -> RecommendationService:
    return route_service

@router.post("/init", response_model=ChatResponse)
async def read_init_message(
    request: InitRequest,
    service: RecommendationService = Depends(get_route_service)
):
    """
    산책 추천 챗봇의 첫 번째 메시지입니다.
    현재 좌표의 날씨 정보를 분석하여 환영 인사를 반환합니다.
    """
    return await service.get_init_message(request.user_uuid, request.lat, request.lon)

@router.post("/intent", response_model=ChatResponse)
async def read_message(
    request: ChatRequest,
    service: RecommendationService = Depends(get_route_service)
):
    """
    사용자가 메시지를 보낼 때마다 호출됩니다.
    """
    return await service.orchestrator(request.thread_id, request.user_prompt)
