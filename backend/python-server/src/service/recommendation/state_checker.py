from src.repository.chat_state_repository import ChatStateRepository
from typing import Dict, Any
from src.service.recommendation.extractor import Extractor
from src.service.recommendation.decision_maker import DecisionMaker

class StateChecker:
    def __init__(self, gpt_client):
        self.gpt_client = gpt_client
        self.extractor = Extractor(gpt_client)
        self.decision_maker = DecisionMaker(gpt_client)

    def is_context_complete(self, context: Dict[str, Any]) -> bool:
        """
        필수 필드(순환 여부, 출발지, 목적지, 목적)가 채워졌는지 검사합니다.
        """
        # 순환 여부가 결정되지 않았으면 False
        if context.get("is_circular") is None:
            return False
        
        # 순환이라면 출발지, 산책 목적이 무조건 있어야 함
        if context.get("is_circular"):
            if context.get("origin") and context.get("purpose"):
                return True
            return False
        
        # 편도라면 출발지, 목적지, 산책 목적이 무조건 있어야 함
        if context.get("is_circular") is False:
            if context.get("origin") and context.get("destination") and context.get("purpose"):
                return True
            return False
        
        return False
    
    async def update_and_check(self, thread_id: str, user_prompt: str) -> Dict[str, Any]:
        """
        사용자 프롬프트를 분석하여 상태를 업데이트하고, 다음 단계를 결정합니다.
        """
        # --- 1. 현재 상태 로드 ---
        state = await ChatStateRepository.get_state(thread_id)

        # --- 2. 확정 판정 ---
        if state.get("next_node") == "decision":
            is_positive = await self.decision_maker.is_user_confirmed(user_prompt)

            # 확정O -> feature별 가중치 결정
            if is_positive:
                state["is_confirmed"] = True
                state["next_node"] = "weighting"
                await ChatStateRepository.save_state(thread_id, state)
                return state
            # 확정X -> 정보 추출 반복
            else:
                state["is_confirmed"] = False
                state["next_node"] = "extraction"

        # --- 3. 정보 추출 및 검사 ---
        state["user_prompt"] = user_prompt

        extracted_context = await self.extractor.extract_info(
            user_prompt=user_prompt,
            context=state["user_context"]
        )

        # 상태 업데이트
        state["user_context"].update(extracted_context)

        # --- 4. 필수 정보가 다 모였는지 확인 ---
        if self.is_context_complete(state["user_context"]):
            state["next_node"] = "final_review"
        else:
            state["next_node"] = "interview"

        # --- 5. 상태 저장 및 반환 ---
        await ChatStateRepository.save_state(thread_id, state)
        return state