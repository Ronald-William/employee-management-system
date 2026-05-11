from common.error.exception import NotFoundException, ConflictException, AuthException, ForbiddenException, ValidationException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from fastapi import FastAPI, Request, status


def error_response(status_code: int, detail)->JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={"error" : {"status_code": status_code, "detail": detail}}
    )

def not_found_handler(request: Request, exc: NotFoundException)->JSONResponse:
    return error_response(exc.status_code, exc.detail)

def conflict_handler(request: Request, exc: ConflictException)->JSONResponse:
    return error_response(exc.status_code, exc.detail)

def auth_exception_handler(request: Request, exc: AuthException)->JSONResponse:
    return error_response(exc.status_code, exc.detail)

def integrity_error_handler(request: Request, exc: IntegrityError)->JSONResponse:
    return error_response(status.HTTP_409_CONFLICT, "A record with the provided email or phone number already exists")

def unhandled_exception_handler(request: Request, exc: Exception)->JSONResponse:
    return error_response(status.HTTP_500_INTERNAL_SERVER_ERROR, "Something went wrong on our end. Please try again later.")

def forbidden_handler(request: Request, exc: ForbiddenException) -> JSONResponse:
    return error_response(exc.status_code, exc.detail)

def validation_exception_handler(request: Request, exc: ValidationException)->JSONResponse:
    return error_response(exc.status_code, exc.detail)

def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(NotFoundException, not_found_handler)
    app.add_exception_handler(ConflictException, conflict_handler)
    app.add_exception_handler(AuthException, auth_exception_handler)
    app.add_exception_handler(IntegrityError, integrity_error_handler)
    app.add_exception_handler(ForbiddenException, forbidden_handler)
    app.add_exception_handler(ValidationException, validation_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)   
    