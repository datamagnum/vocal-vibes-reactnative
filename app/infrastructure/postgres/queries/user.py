from sqlalchemy.future import select
from sqlalchemy.orm import scoped_session

from app.infrastructure.postgres.models import User


class UserQueries:
    def __init__(self, db_session: scoped_session) -> None:
        self.__db_session: scoped_session = db_session

    async def create(self, user: User) -> User:
        self.__db_session.add(user)
        await self.__db_session.flush()
        await self.__db_session.refresh(user)

        return user

    async def get_by_email(self, email: str) -> User:
        stmt = select(User).filter_by(email=email)
        result = await self.__db_session.execute(stmt)
        return result.scalars().first()

    async def get_all_users(self) -> list[User]:
        stmt = select(User)
        result = await self.__db_session.execute(stmt)
        return result.scalars().all()
