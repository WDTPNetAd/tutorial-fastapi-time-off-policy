from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from app.core.database import Base

class PolicyHistory(Base):
    __tablename__ = "policy_histories"
    
    id = Column(Integer, primary_key=True, index=True)
    policy_id = Column(Integer, ForeignKey("policies.id"), nullable=False)
    name = Column(String, nullable=False)
    days_allowed = Column(Integer, nullable=False)
    policy_type = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

#CONSIDER USING AN FK ON POLICY SO WE CAN TRACK THE CORRECT CHANGES
    