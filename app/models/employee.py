from sqlalchemy import Column, Integer, String
from app.core.database import Base
from sqlalchemy.orm import relationship

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    department = Column(String, nullable=False)

    time_off_requests = relationship("TimeOffRequest", back_populates="employee")