from pydantic import BaseModel, Field

# Comment

class CommentBase(BaseModel):
    content: str = Field(..., min_length=1, max_length=254, description="Content of the comment")

class Comment(CommentBase):
    id: int = Field(..., description="ID of the comment")
    class Config:
        orm_mode = True