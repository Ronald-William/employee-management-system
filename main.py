from fastapi import FastAPI
from controller.employee_controller import employee_route
from controller.auth_controller import auth_route
from common.config.database_config import db_engine
from repository.entity.employee_entity import Base
import repository.entity.user_entity
from common.error.exception_handler import register_exception_handlers

Base.metadata.create_all(bind=db_engine)

app = FastAPI(title="Employee Management API")
register_exception_handlers(app)

@app.get("/health", tags=["System"])
def health_check():
    return {"status": "healthy", "service": "employee_management_system"}

app.include_router(auth_route)
app.include_router(employee_route)

