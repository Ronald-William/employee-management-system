import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from common.config.jwt_config import JwtConfig
from common.config.database_config import get_db
from common.error.exception import AuthException, ForbiddenException
from repository.user_repository import UserRepository
from repository.entity.user_entity import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


class AuthMiddleware:

    @staticmethod
    def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> dict:
        try:
            payload = JwtConfig.decode_access_token(token)
            user_id: str = payload.get("sub")

        except jwt.ExpiredSignatureError:
            raise AuthException("Your session has expired. Please log in again.")
        except jwt.InvalidTokenError:
            raise AuthException("The token provided is invalid. Please log in again.")

        user = UserRepository(db).get_by_id(int(user_id))
        if not user:
            raise AuthException("User account no longer exists. Please register again.")
        return user
        
    @staticmethod
    def get_admin_user(current_user: User = Depends(get_current_user))->User:
        if not current_user.is_admin:
            raise ForbiddenException()
        return current_user



get_current_user = AuthMiddleware.get_current_user
get_admin_user = AuthMiddleware.get_admin_user
