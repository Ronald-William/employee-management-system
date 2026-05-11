from sqlalchemy.orm import Session
from repository.entity.employee_entity import Employee
from typing import List, Any, Dict, Optional
from sqlalchemy.exc import SQLAlchemyError
from common.middleware.logger import logger

class EmployeeRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, employee_id: int):
        result = self.db.query(Employee).filter(Employee.emp_id == employee_id).first()
        return result
    
    def get_all(self, filters: Dict[str,Any], limit: int = 10, skip: int = 0)->List[Employee]:
        
        base_query = self.db.query(Employee)
        for key,value in filters.items():
            if value is not None:
                column = getattr(Employee, key, None)
                if column is not None:
                    base_query = base_query.filter(column==value)
        
        total_count = base_query.count()
        data = base_query.offset(skip).limit(limit).all()
        return total_count, data
    
    def create(self, employee_data: Employee)->Employee:
        try:
            self.db.add(employee_data)
            self.db.commit()
            self.db.refresh(employee_data)
            return employee_data
        except Exception as e:
            self.db.rollback()
            raise e
    
    def update(self, employee_id: int, updated_data: Dict[str, Any])->Optional[Employee]:
        employee_to_update = self.get_by_id(employee_id)
        if employee_to_update:
            for key,value in updated_data.items():
                if hasattr(employee_to_update, key) and value is not None:
                    setattr(employee_to_update, key, value)
            
            try:
                self.db.commit()
                self.db.refresh(employee_to_update)
                return employee_to_update
            except Exception as e:
                self.db.rollback()
                raise e
        else:
            return None
            
    def delete(self, employee_id: int):
        employee_to_delete = self.get_by_id(employee_id)
        if not employee_to_delete:
            return False
        try:
            self.db.delete(employee_to_delete)
            self.db.commit()
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Database error while deleting employee {employee_id}: {e}")
            raise e
       
            
        