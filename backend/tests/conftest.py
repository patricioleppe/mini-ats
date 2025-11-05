# backend/tests/conftest.py
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 👇 Agregamos la carpeta backend al sys.path
ROOT = Path(__file__).resolve().parents[1]  # .../backend
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# 👇 Ahora importamos desde app.*, igual que en uvicorn app.main:app
from app.main import app
from app.db.session import Base, get_db

TEST_DATABASE_URL = (
    "postgresql+psycopg2://postgres:postgres123@localhost:5455/mini_ats_test"
)

engine_test = create_engine(TEST_DATABASE_URL, future=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)


@pytest.fixture(scope="session", autouse=True)
def prepare_test_database():
    Base.metadata.drop_all(bind=engine_test)
    Base.metadata.create_all(bind=engine_test)
    yield
    Base.metadata.drop_all(bind=engine_test)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

# Ahora los tests pueden usar el fixture `client` para hacer requests al API
# Ejemplo:
# def test_some_endpoint(client: TestClient):
#     response = client.get("/some-endpoint")
#     assert response.status_code == 200

# backend/tests/test_companies.py
# tests/test_companies.py
