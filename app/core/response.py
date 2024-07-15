from pydantic import BaseModel


class UserGroupResponse(BaseModel):
    message: str

    @classmethod
    def create_from_message(cls, message: str) -> "UserGroupResponse":
        return cls(message=message)
