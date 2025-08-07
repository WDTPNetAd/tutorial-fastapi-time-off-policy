from pydantic import BaseModel, Field
from typing import List, Optional
from .time_off_request import TimeOffRequestResponse
from app.constants.enum import DepartmentEnum

# Use forward references as strings in Response model
class EmployeeBase(BaseModel):
    name: str
    email: str
    department: DepartmentEnum

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(BaseModel):
    name: Optional[str] = Field(default=None)
    email: Optional[str] = Field(default=None)
    department: Optional[DepartmentEnum] = Field(default=None)

class EmployeeResponse(EmployeeBase):
    id: int
    time_off_requests: List[TimeOffRequestResponse] = []

    class Config:
        orm_mode = True

class PaginatedEmployeeResponse(BaseModel):
    total: int
    skip: int
    limit: int
    data: List[EmployeeResponse]
    