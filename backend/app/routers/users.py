from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from fastapi.security import SecurityScopes
from app.routers.auth import require_scopes
from app.schemas.auth import JWTPayload

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me")
def me(payload: JWTPayload = Depends(require_scopes)):
    return payload

@router.get("", dependencies=[Depends(require_scopes)])
def list_users(payload: JWTPayload = Depends(require_scopes), db: Session = Depends(get_db)):
    users = db.query(User).filter(User.company_id == payload.company_id).all()
    return [{"id": u.id, "email": u.email, "role": u.role, "scopes": u.scopes.split()} for u in users]
