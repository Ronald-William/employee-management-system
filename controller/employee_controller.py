from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from application.model.employee_model import (EmployeeCreate, EmployeeResponse, EmployeeUpdate,EmployeeFilters, PaginatedEmployeeResponse)
from application.service.employee_service import EmployeeService
from repository.employee_repository import EmployeeRepository
from common.config.database_config import get_db
from common.middleware.auth_middleware import get_current_user, get_admin_user
from common.error.exception import NotFoundException

employee_route = APIRouter(
    prefix="/employee",
    tags=["Employee"],
    dependencies=[Depends(get_current_user)]
)


def get_employee_service(db: Session = Depends(get_db)) -> EmployeeService:
    repository = EmployeeRepository(db)
    return EmployeeService(repository)


@employee_route.get("/", response_model=PaginatedEmployeeResponse, status_code=status.HTTP_200_OK)
def get_all(filters: EmployeeFilters = Depends(), service: EmployeeService = Depends(get_employee_service)):
    return service.list_employees(filters)


@employee_route.get("/{employee_id}", response_model=EmployeeResponse)
def get_by_id(employee_id: int, service: EmployeeService = Depends(get_employee_service)):
    result = service.get_details(employee_id)
    if not result:
        raise NotFoundException(employee_id)
    return result


@employee_route.post("/", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_admin_user)])
def create(employee: EmployeeCreate, service: EmployeeService = Depends(get_employee_service)):
    return service.create(employee)


@employee_route.put("/employee_id}", response_model=EmployeeResponse, dependencies=[Depends(get_admin_user)])
def update(employee_id: int, employee: EmployeeUpdate, service: EmployeeService = Depends(get_employee_service)):
    data_to_update = employee.model_dump(exclude_unset=True)
    result = service.update(employee_id, data_to_update)
    if not result:
        raise NotFoundException(employee_id)
    return result


@employee_route.delete("/{employee_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(get_admin_user)])
def delete(employee_id: int, service: EmployeeService = Depends(get_employee_service)):
    deleted = service.delete(employee_id)
    if not deleted:
        raise NotFoundException(employee_id)
    return {"message": "Employee deleted successfully."}