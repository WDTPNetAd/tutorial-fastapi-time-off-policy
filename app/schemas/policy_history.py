from pydantic import BaseModel, Field
from typing import Optional

class PolicyHistoryBase(BaseModel):
    policy_id: int
    name: str
    days_allowed: int
    policy_type: str

class PolicyHistoryCreate(PolicyHistoryBase):
    pass
    
class PolicyHistoryUpdate(PolicyHistoryBase):
    name: Optional[str] = Field(default=None)
    days_allowed: Optional[int] = Field(default=None)
    policy_type: Optional[str] = Field(default=None)
    
class PolicyHistoryResponse(PolicyHistoryBase):
    id: int
    class Config:
        orm_mode = True

