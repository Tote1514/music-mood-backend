
from pydantic import BaseModel


class UserResponse(BaseModel):
    display_name: str
