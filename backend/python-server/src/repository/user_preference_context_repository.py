from src.database.postgresql import get_postgresql_db
from src.entity.user_preference_context import UserPreferenceContext
from typing import Dict

class UserPreferenceContextRepository:
    @staticmethod
    def get_state_by_session(session_id: int) -> Dict:
        """
        세션 ID를 기준으로 해당 대화의 컨텍스트를 가져옵니다.
        """
        with get_postgresql_db() as db:
            entity = db.query(UserPreferenceContext).filter_by(session_id=session_id).first()
            
            return {
                "is_circular": entity.is_circular,
                "origin": entity.origin_name,
                "destination": entity.destination_name,
                "purpose": entity.purpose
            }
