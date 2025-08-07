from pydantic import BaseModel, Field
from typing import List, Optional
from .time_off_request import TimeOffRequestResponse
from app.constants.enum import PolicyTypeEnum
from .policy_history import PolicyHistoryResponse

class PolicyBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=254, description="Name of the policy")
    days_allowed: int = Field(..., description="Number of days allowed")
    policy_type: PolicyTypeEnum = Field(..., description="Type of policy")

class PolicyCreate(PolicyBase):
    pass

class PolicyUpdate(BaseModel):
    name: Optional[str] = Field(default=None)
    days_allowed: Optional[int] = Field(default=None)
    policy_type: Optional[PolicyTypeEnum] = Field(default=None)

class PolicyResponse(PolicyBase):
    id: int = Field(..., description="ID of the policy")
    time_off_requests: List[TimeOffRequestResponse] = []
    policy_histories: List[PolicyHistoryResponse] = []

    class Config:
        orm_mode = True

class PaginatedPolicyResponse(BaseModel):
    total: int
    skip: int
    limit: int
    data: List[PolicyResponse]
