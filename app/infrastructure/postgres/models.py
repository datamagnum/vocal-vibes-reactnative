import uuid
from enum import Enum as PyEnum

from sqlalchemy import (
    ARRAY,
    JSON,
    BigInteger,
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Text,
    text,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()
metadata = Base.metadata


class TopicGenerationType(PyEnum):
    SEEDED = "SEEDED"
    AI_GENERATED = "AI_GENERATED"


class SSOType(str, PyEnum):
    GOOGLE = "GOOGLE"
    FACEBOOK = "FACEBOOK"


class SessionType(PyEnum):
    SELF_PRACTICE = "SELF_PRACTICE"
    GROUP = "GROUP"


class SessionMediaType(PyEnum):
    AUDIO = "AUDIO"
    VIDEO = "VIDEO"


class User(Base):

    __tablename__ = "user"

    id = Column(BigInteger, primary_key=True)
    first_name = Column(Text)
    middle_name = Column(Text, nullable=True)
    last_name = Column(Text, nullable=True)
    email = Column(Text, unique=True)
    password = Column(Text)
    sso_provider = Column(Enum(SSOType), nullable=True)
    traits = Column(JSON, server_default=text("'{}'"))
    is_active = Column(Boolean, nullable=False, server_default=text("true"))
    is_deleted = Column(Boolean, nullable=False, server_default=text("false"))
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now())


class Topic(Base):

    __tablename__ = "topic"

    id = Column(BigInteger, primary_key=True)
    title = Column(Text)
    description = Column(Text)
    tags = Column(ARRAY(Text))
    content = Column(Text)
    generation_type = Column(Enum(TopicGenerationType), server_default="SEEDED")
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now())


class Session(Base):

    __tablename__ = "session"

    id = Column(Text, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(Text)
    description = Column(Text)
    created_by = Column(BigInteger, ForeignKey("user.id"), index=True, nullable=False)
    session_type = Column(Enum(SessionType), server_default="SELF_PRACTICE")
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now())
    is_deleted = Column(Boolean, nullable=False, server_default=text("false"))

    user = relationship("User")
    self_practice_session = relationship(
        "SelfPracticeSession", uselist=False, back_populates="session"
    )


class SelfPracticeSession(Base):

    __tablename__ = "self_practice_session"

    id = Column(Text, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(Text, ForeignKey("session.id"), unique=True, nullable=False)
    topic_id = Column(BigInteger, ForeignKey("topic.id"), nullable=False)
    media_type = Column(Enum(SessionMediaType), server_default="AUDIO")
    session_recording_url = Column(Text)
    is_deleted = Column(Boolean, nullable=False, server_default=text("false"))
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now())

    session = relationship("Session", back_populates="self_practice_session")
    topic = relationship("Topic")


class Group(Base):

    __tablename__ = "group"

    id = Column(Text, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(Text, nullable=False)
    description = Column(Text)
    created_by = Column(BigInteger, ForeignKey("user.id"), index=True, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now())
    is_deleted = Column(Boolean, nullable=False, server_default=text("false"))

    user = relationship("User")


class GroupUsers(Base):

    __tablename__ = "group_users"

    group_id = Column(Text, ForeignKey("group.id"), primary_key=True)
    user_id = Column(BigInteger, ForeignKey("user.id"), primary_key=True)
    user = relationship("User")
    group = relationship("Group")
