from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

from app.infrastructure.postgres.models import (
    SelfPracticeSession as SelfPracticeSessionORM,
)
from app.infrastructure.postgres.models import Session as SessionOrm


class SessionType(str, Enum):
    SELF_PRACTICE = "SELF_PRACTICE"
    GROUP = "GROUP"


class SessionMediaType(str, Enum):
    AUDIO = "AUDIO"
    VIDEO = "VIDEO"


class Session(BaseModel):
    id: str
    name: str
    description: str
    session_type: SessionType
    created_by: int
    is_deleted: bool
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create_from_orm(cls, orm_obj: SessionOrm) -> "Session":
        return cls(**orm_obj.__dict__)


class CreateSessionRequestSchema(BaseModel):
    name: str
    description: str = Field(default_factory=str)
    session_type: SessionType = SessionType.SELF_PRACTICE
    created_by: Optional[int] = None

    @property
    def orm_obj(self) -> SessionOrm:
        return SessionOrm(
            name=self.name,
            description=self.description,
            session_type=self.session_type,
            created_by=self.created_by,
        )


class SelfPracticeSession(BaseModel):
    id: int
    session_id: str
    media_type: SessionMediaType
    session_recording_url: Optional[str]
    topic_id: int
    is_deleted: bool
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create_from_orm(
        cls, orm_obj: SelfPracticeSessionORM
    ) -> "SelfPracticeSessionORM":
        return cls(**orm_obj.__dict__)


class CreateSelfPracticeSessionRequestSchema(BaseModel):
    session_id: str
    topic_id: int
    media_type: SessionMediaType = SessionMediaType.AUDIO

    @property
    def orm_obj(self) -> SelfPracticeSessionORM:
        return SelfPracticeSessionORM(
            session_id=self.session_id,
            topic_id=self.topic_id,
            media_type=self.media_type,
        )
