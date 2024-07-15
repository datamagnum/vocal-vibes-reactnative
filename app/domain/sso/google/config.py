from pydantic import BaseModel


class GoogleSSOConfig(BaseModel):
    client_id: str
