from pydantic import BaseModel, Field
from typing import List
from .comment import Comment

# Policy

class PolicyBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=254, description="Name of the policy")

class Policy(PolicyBase):
    id: int = Field(..., description="ID of the policy")
    comments: List[Comment] = []
    class Config:
        orm_mode = True

class PaginatedPolicyResponse(BaseModel):
    total: int
    skip: int
    limit: int
    data: List[Policy]


    
    
