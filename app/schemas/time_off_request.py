from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
# from .employee import EmployeeResponseLite
# from .policy import PolicyResponseLite

# Forward references via string annotations
class TimeOffRequestBase(BaseModel):
    employee_id: int
    policy_id: int
    start_date: date
    end_date: date


class TimeOffRequestCreate(TimeOffRequestBase):
    pass

class TimeOffRequestUpdate(TimeOffRequestBase):
    employee_id: Optional[int] = Field(default=None)
    policy_id: Optional[int] = Field(default=None)
    start_date: Optional[date] = Field(default=None)
    end_date: Optional[date] = Field(default=None)
    # status: Optional[str] = Field(default=None)

class TimeOffRequest(TimeOffRequestBase):
    id: int
    status: str

    class Config:
        orm_mode = True

class TimeOffRequestResponse(TimeOffRequest):
    pass
    # employee: EmployeeResponseLite
    # policy: PolicyResponseLite

    class Config:
        orm_mode = True

class TimeOffStatusResponse(BaseModel):
    id: int
    employee_name: str
    policy_name: str
    start_date: date
    end_date: date
    total_days: int
    remaining_days: int
    is_ongoing: bool

    class Config:
        orm_mode = True

