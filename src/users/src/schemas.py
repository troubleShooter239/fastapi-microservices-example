from typing import Literal

from pydantic import BaseModel, ConfigDict


class UserModel(BaseModel):
    name: str
    email: str
    address: str
    user_type: Literal['supplier', 'consumer', 'admin', 'super_admin']
    model_config = ConfigDict(from_attributes=True)
