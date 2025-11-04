from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), default="viewer")  # admin|recruiter|viewer
    scopes = Column(String(255), default="viewer")  # "admin recruiter"
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)

    company = relationship("Company")
