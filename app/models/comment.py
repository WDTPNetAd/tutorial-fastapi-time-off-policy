from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from app.core.database import Base
from sqlalchemy.orm import relationship

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    policy_id = Column(Integer, ForeignKey("policies.id"), nullable=False)
    content = Column(String, nullable=False)

    policy = relationship("Policy", back_populates="comments")