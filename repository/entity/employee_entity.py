from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, String,Float, Integer, Date

class Base(DeclarativeBase):
    pass

class Employee(Base):
    __tablename__ = "employees"
    emp_id = Column(Integer, primary_key=True, index = True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    
    email= Column(String(50), unique=True, nullable=False)
    phone = Column(String(20), unique=True, nullable=False)
    address = Column(String(100), nullable=False)
    
    date_of_joining = Column(Date, nullable=False)
    designation = Column(String(50), nullable=False)
    salary = Column(Float, nullable=False)

    
    


