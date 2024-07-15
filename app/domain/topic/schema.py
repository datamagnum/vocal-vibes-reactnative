from datetime import datetime
from typing import List

from pydantic import BaseModel, Field

from app.infrastructure.postgres.models import Topic as TopicORM
from app.infrastructure.postgres.models import TopicGenerationType


class Topic(BaseModel):
    content: str
    id: int
    title: str
    description: str
    tags: List[str]
    generation_type: TopicGenerationType
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create_from_orm(cls, orm_obj: TopicORM) -> "Topic":
        return cls(**orm_obj.__dict__)


class CreateTopicRequestSchema(BaseModel):
    content: str
    title: str
    description: str = Field(default_factory=str)
    tags: List[str] = Field(default_factory=list)
    generation_type: TopicGenerationType = TopicGenerationType.SEEDED

    @property
    def orm_obj(self) -> TopicORM:
        return TopicORM(
            content=self.content,
            title=self.title,
            description=self.description,
            tags=self.tags,
            generation_type=self.generation_type,
        )


class TopicsResponseSchema(BaseModel):
    topics: List[Topic] = Field(default_factory=list)
    total: int
