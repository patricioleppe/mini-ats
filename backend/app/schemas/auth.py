from pydantic import BaseModel
from typing import List

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class LoginIn(BaseModel):
    email: str
    password: str

class JWTPayload(BaseModel):
    sub: str
    company_id: int
    role: str
    scopes: List[str]
