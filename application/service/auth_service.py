from pwdlib import PasswordHash
from sqlalchemy.orm import Session

from repository.user_repository import UserRepository
from fastapi import Response
from application.model.auth_model import TokenResponse
from common.config.jwt_config import JwtConfig
from common.middleware.logger import logger
from common.error.exception import ConflictException, AuthException

password_hash = PasswordHash.recommended()

class AuthService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)
    
    def register(self, email: str, password: str):
        existing = self.repository.get_by_email(email)
        if existing:
            logger.warning(f"Registration failed: Email {email} already exists.")
            raise ConflictException("email", email)
        hashed = password_hash.hash(password)
        user = self.repository.create(email, hashed)
        logger.info(f"Registered Succesfully: User {email} registered")
        return {"message" : "User registered successfully", "email": user.email}


    def login(self, email: str, password: str)->TokenResponse:
        user = self.repository.get_by_email(email)
        if not user or not password_hash.verify(password, user.password):
            logger.warning(f"Login failed: Invalid credentials for user {email}")
            raise AuthException("Incorrect email or password. Please try again.")
        token = JwtConfig.create_access_token({"sub" : str(user.user_id), "email": user.email})
        
        logger.info(f"Login successful: User {email} authenticated.")
        return TokenResponse(access_token=token)
    