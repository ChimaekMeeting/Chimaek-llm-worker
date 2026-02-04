from sqlalchemy.orm import declarative_base
from src.database.postgresql import engine

# 모델 생성을 위한 기본 클래스
Base = declarative_base()

def init_db():
    """
    테이블 생성을 위한 초기화 함수입니다.
    """
    from src.entity.user import User
    from src.entity.chat_session import ChatSession
    from src.entity.user_preference_context import UserPreferenceContext

    Base.metadata.create_all(bind=engine)