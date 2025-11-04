from fastapi import FastAPI
from app.core.config import settings
from app.db.session import Base, engine
from app.routers import auth, users, companies
print(">>> DB URL:", settings.DATABASE_URL)

app = FastAPI(title=settings.APP_NAME)

# Crear tablas simples al inicio (más adelante Alembic)
Base.metadata.create_all(bind=engine)

app.include_router(companies.router)
app.include_router(auth.router)
app.include_router(users.router)

@app.get("/health")
def health():
    return {"status": "ok"}
