from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from app.core.database import Base
from sqlalchemy.orm import relationship

class Policy(Base):
    __tablename__ = "policies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    comments = relationship("Comment", back_populates="policy")


    