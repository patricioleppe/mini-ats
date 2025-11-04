from pydantic import BaseModel, EmailStr, ConfigDict
from typing import List

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: str = "viewer"
    scopes: List[str] = ["viewer"]
    company_id: int

class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: str
    scopes: list[str]
    company_id: int
    model_config = ConfigDict(from_attributes=True)
