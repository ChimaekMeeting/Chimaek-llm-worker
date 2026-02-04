from src.entity.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, func, ForeignKey, Boolean, JSON
from datetime import datetime
from typing import TYPE_CHECKING, Optional

# 실행 시점이 아닌 타입 체크 시점에만 참조(순환 참조 방지)
if TYPE_CHECKING:
    from src.entity.chat_session import ChatSession

class UserPreferenceContext(Base):
    """
    사용자의 의도를 관리하는 엔티티입니다.
    """
    __tablename__ = "user_preference_contexts"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    # ChatSession과 1:1 관계
    session_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("chat_sessions.id", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )

    # 순환 여부
    is_circular: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )
    
    # 위치 정보
    origin_name: Mapped[Optional[str]] = mapped_column(String(100))
    origin_location: Mapped[Optional[dict]] = mapped_column(JSON)  # e.g., {"lat": 37.5, "lng": 127.0}
    origin_h3_cell: Mapped[Optional[str]] = mapped_column(String(20))

    # is_circular가 False일 때 필요
    destination_name: Mapped[Optional[str]] = mapped_column(String(100))
    destination_location: Mapped[Optional[dict]] = mapped_column(JSON)
    destination_h3_cell: Mapped[Optional[str]] = mapped_column(String(20))

    # 산책 목적
    purpose: Mapped[Optional[str]] = mapped_column(String(255))
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
    
    # 관계 설정: ChatSession과 1:1 관계
    chat_session: Mapped["ChatSession"] = relationship(
        "ChatSession",
        back_populates="user_preference_context"
    )