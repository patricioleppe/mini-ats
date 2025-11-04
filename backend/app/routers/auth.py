from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, SecurityScopes
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import Token, JWTPayload
from app.utils.security import verify_password, hash_password, create_access_token
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/token",
    scopes={
        "admin": "Administración total",
        "recruiter": "Gestiona vacantes",
        "viewer": "Lectura",
    },
)

def parse_token(token: str) -> JWTPayload:
    try:
        data = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALG])
        return JWTPayload(**data)
    except JWTError:
        raise HTTPException(401, "Token inválido")

def require_scopes(security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)) -> JWTPayload:
    payload = parse_token(token)
    needed = set(security_scopes.scopes)
    if not needed.issubset(set(payload.scopes)):
        raise HTTPException(403, detail=f"Faltan scopes: {list(needed)}")
    return payload

@router.post("/register", response_model=dict)
def register(email: str, password: str, company_id: int, role: str = "viewer", scopes: List[str] = ["viewer"], db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(400, "Email ya registrado")
    u = User(email=email, hashed_password=hash_password(password), role=role, scopes=" ".join(scopes), company_id=company_id)
    db.add(u); db.commit(); db.refresh(u)
    return {"id": u.id, "email": u.email}

@router.post("/token", response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form.username).first()
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(401, "Credenciales inválidas")
    scopes = form.scopes or user.scopes.split()
    token = create_access_token(str(user.id), user.company_id, user.role, scopes)
    return Token(access_token=token)
