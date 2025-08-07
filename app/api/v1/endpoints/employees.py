from fastapi import APIRouter, Depends
from typing import Annotated, List
from sqlalchemy.orm import Session
from app.schemas.employee import EmployeeCreate, EmployeeUpdate, EmployeeResponse

import app.models as models
from app.core.exceptions import NotFoundException
from app.api.v1.deps import get_db

router = APIRouter()

db_dependency = Annotated[Session, Depends(get_db)]

@router.get(
    '/employees',
    response_model=List[EmployeeResponse],
)
def get_employees(db: db_dependency):
    employees = db.query(models.Employee).all()
    return employees

@router.post('/employees', response_model=EmployeeResponse)
def create_employee(employee: EmployeeCreate, db: db_dependency):
    employee_data = employee.dict(exclude_unset=True)
    db_employee = models.Employee(**employee_data)
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

@router.get('/employees/{employee_id}', response_model=EmployeeResponse)
def get_employee(employee_id: int, db: db_dependency):
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not employee:
        raise NotFoundException('Employee')
    return employee

@router.put('/employees/{employee_id}', response_model=EmployeeResponse)
def update_employee(employee_id: int, employee: EmployeeUpdate, db: db_dependency):
    db_employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not db_employee:
        raise NotFoundException('Employee')
    update_data = employee.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_employee, key, value)
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

@router.delete('/employees/{employee_id}')
def delete_employee(employee_id: int, db: db_dependency):
    db_employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not db_employee:
        raise NotFoundException('Employee')
    db.delete(db_employee)
    db.commit()
    return {"message": "Employee deleted successfully"}