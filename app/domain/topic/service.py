from typing import List

from sqlalchemy.orm import scoped_session

from app.domain.topic.schema import (
    CreateTopicRequestSchema,
    Topic,
    TopicsResponseSchema,
)
from app.infrastructure.postgres.models import Topic as TopicORM
from app.infrastructure.postgres.queries.topic import TopicQueries


class TopicService:
    def __init__(self, db_session: scoped_session) -> None:
        self.__topic_queries: TopicQueries = TopicQueries(db_session=db_session)

    async def create_topic(self, payload: CreateTopicRequestSchema) -> Topic:
        topic_orm = await self.__topic_queries.create(payload.orm_obj)
        return Topic.create_from_orm(topic_orm)

    async def get_topics(self, page: int, per_page: int) -> TopicsResponseSchema:

        total_topics = await self.__topic_queries.get_total_topics()

        result = await self.__topic_queries.get_paginated_topics(
            page=page, per_page=per_page
        )

        response = TopicsResponseSchema(total=total_topics)

        if not result:
            return response

        for topic_orm in result:
            response.topics.append(Topic.create_from_orm(topic_orm))

        return response
