from typing import AsyncGenerator, Generator

from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Session, scoped_session

from app.core.config import settings

aengine = create_async_engine(
    url=settings.ASYNC_SQLALCHEMY_DATABASE_URI, pool_pre_ping=True
)


def acreate_sessionmaker(connection_uri: str) -> scoped_session:
    engine = create_async_engine(connection_uri, pool_pre_ping=True)
    return async_sessionmaker(autoflush=True, bind=engine)


async def aget_session() -> AsyncGenerator:
    SessionLocal = AsyncSession(autocommit=False, autoflush=False, bind=aengine)
    try:
        yield SessionLocal
        await SessionLocal.commit()
    except Exception as ex:
        logger.error(f"Something failed, rolling back database transaction. {ex}")
        await SessionLocal.rollback()
        raise
    finally:
        await SessionLocal.close()
