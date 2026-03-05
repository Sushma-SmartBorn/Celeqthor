from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    email = Column(String(100), unique=True, nullable=True)
    mobile_number = Column(String(20), unique=True, nullable=False)
    user_type = Column(String(50), nullable=True)  
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.now(), server_default=func.now())

class UserSession(Base):
    __tablename__ = "user_sessions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    mobile_number = Column(String(20), nullable=False, index=True)
    session_token = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    login_time = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.now(), server_default=func.now())
