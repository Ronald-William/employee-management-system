from sqlalchemy import Column, Integer, String, Boolean
from repository.entity.employee_entity import Base

class User(Base):
    __tablename__ = "users"
    
    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password =Column(String(255), nullable=False)
    is_admin = Column(Boolean, default = False, nullable=False)