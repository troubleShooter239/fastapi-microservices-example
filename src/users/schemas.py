from typing import Literal

from pydantic import BaseModel


class UserModel(BaseModel):
    name: str | None = None
    address: str | None = None
    user_type: Literal['supplier', 'consumer', 'admin', 'super_admin'] | None = None
    class Config:
        orm_mode = True
