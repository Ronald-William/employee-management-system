from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import date
from typing import Optional, List

class EmployeeCreate(BaseModel):
    first_name: str = Field(..., min_length = 1)
    last_name: str =  Field(..., min_length = 1)
    date_of_birth: date
    
    email: EmailStr
    phone: str
    address: str
    
    date_of_joining: date
    designation: str
    salary: float =  Field(..., gt = 0)
   

class EmployeeResponse(EmployeeCreate):
    emp_id: int
    class Config:
        from_attributes = True
        arbitrary_types_allowed=True
        
    
class EmployeeUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    
    date_of_joining: Optional[date] = None
    designation: Optional[str] = None
    salary: Optional[float] = Field(None, gt=1)
    
    
class EmployeeFilters(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    page: int = Field(1, ge = 1)
    limit: int = Field(10, ge=1, le=100)
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    designation: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    

class PaginatedEmployeeResponse(BaseModel):
    total_count: int
    page: int
    limit: int
    total_pages: int
    data: List[EmployeeResponse]