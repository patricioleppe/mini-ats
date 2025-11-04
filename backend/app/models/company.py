from sqlalchemy import Column, Integer, String
from app.db.session import Base


class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), unique=True, index=True, nullable=False)
    razon_social = Column(String(200), nullable=True)
    rut = Column(String(50), unique=True, index=True, nullable=False)
    giro = Column(String(200), nullable=True)
    direccion = Column(String(200), nullable=True)
    ciudad = Column(String(100), nullable=True)
    telefono = Column(String(50), nullable=True)
    email = Column(String(120), unique=True, index=True, nullable=False)
