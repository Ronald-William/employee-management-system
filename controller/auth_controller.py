from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from application.model.auth_model import RegisterRequest,TokenResponse
from application.service.auth_service import AuthService
from common.config.database_config import get_db
from fastapi.security import OAuth2PasswordRequestForm 
from common.middleware.logger import logger

auth_route = APIRouter(prefix="/auth", tags=["Auth"])


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(db)


@auth_route.post("/register", status_code=201)
def register(body: RegisterRequest, service: AuthService = Depends(get_auth_service)):
    return service.register(body.email, body.password)

@auth_route.post("/login", response_model=TokenResponse)
def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), service: AuthService = Depends(get_auth_service)):
    logger.info(f"Login attempt initiated for user: {form_data.username}")
    return service.login(form_data.username, form_data.password)