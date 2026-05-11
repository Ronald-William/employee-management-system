from sqlalchemy.orm import Session
from repository.entity.user_entity import User
from typing import Optional

class UserRepository:
    def __init__(self, db: Session):
        self.db = db
        
    def get_by_id(self, id: int)->Optional[User]:
        return self.db.query(User).filter(User.user_id == id).first()
    
    def get_by_email(self, email: str)->Optional[User]:
        return self.db.query(User).filter(User.email == email).first()

    def create(self, email: str, hashed_password: str)->User:
        user = User(email = email, password = hashed_password)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    