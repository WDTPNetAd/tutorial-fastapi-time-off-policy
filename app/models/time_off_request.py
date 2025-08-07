from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date
from app.core.database import Base
from sqlalchemy.orm import relationship

class TimeOffRequest(Base):
    __tablename__ = "time_off_requests"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    policy_id = Column(Integer, ForeignKey("policies.id"), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    status = Column(String, nullable=False)

    employee = relationship("Employee", back_populates="time_off_requests")
    policy = relationship("Policy", back_populates="time_off_requests")