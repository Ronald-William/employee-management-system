
from application.model.employee_model import EmployeeCreate, EmployeeResponse, PaginatedEmployeeResponse
from repository.entity.employee_entity import Employee
from typing import Optional, Dict, Any, List
from repository.employee_repository import EmployeeRepository
from common.middleware.logger import logger
from math import ceil

class EmployeeService:
    def __init__(self, repository: EmployeeRepository):
        self.repository = repository

    def create(self, employee_record: EmployeeCreate) -> EmployeeResponse:
        new_emp_entity = Employee(**employee_record.model_dump())
        created_entity = self.repository.create(new_emp_entity)
        logger.info(f"Employee created: ID {created_entity.emp_id}, name: {created_entity.first_name} {created_entity.last_name}.")
        return EmployeeResponse.model_validate(created_entity)
    
    def get_details(self, employee_id: int) -> Optional[EmployeeResponse]:
        result = self.repository.get_by_id(employee_id)
        if not result:
            logger.warning(f"Employee not found: ID {employee_id}.")
            return None
        return EmployeeResponse.model_validate(result)
    
    def list_employees(self, filters: Dict[str, Any], limit: int = 10, page: int = 1) -> List[EmployeeResponse]:
        skip = (page - 1) * limit
        filters_dict = filters.model_dump(exclude = {'page', 'limit'}, exclude_none = True)
        (total_count, entities) = self.repository.get_all(filters = filters_dict, limit = filters.limit, skip = skip)
        total_pages = ceil(total_count / filters.limit ) if total_count > 0 else 0
        logger.info(f"Employee list fetched: filters={filters_dict}, page={filters.page}, total={total_count}.")
        return PaginatedEmployeeResponse(
            total_count = total_count,
            page = filters.page,
            limit = filters.limit,
            total_pages = total_pages,
            data = [EmployeeResponse.model_validate(e) for e in entities]
        )
    
    def update(self, employee_id: int, updated_details: dict) -> Optional[EmployeeResponse]:
        updated_entity = self.repository.update(employee_id, updated_details)
        if not updated_entity:
            logger.warning(f"Update failed: Employee ID {employee_id} not found.")
            return None
        logger.info(f"Employee updated: ID {employee_id}, fields changed: {list(updated_details.keys())}.")
        return EmployeeResponse.model_validate(updated_entity)
    
    def delete(self, employee_id: int):
        deleted = self.repository.delete(employee_id)
        if not deleted:
            logger.warning(f"Delete failed: Employee ID {employee_id} not found.")
            return False
        logger.info(f"Employee deleted: ID {employee_id}")
        return True