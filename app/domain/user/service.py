from app.domain.user.schema import ListUserResponseSchema, User
from app.infrastructure.postgres.queries.user import UserQueries


class UserService:
    def __init__(self, user_queries: UserQueries) -> None:
        self.user_queries = user_queries

    async def get_users(self) -> ListUserResponseSchema:
        users_orm = await self.user_queries.get_all_users()
        users = [User.create_from_orm(user_obj) for user_obj in users_orm]
        return ListUserResponseSchema(users=users)
