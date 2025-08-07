__all__ = (
    "DepartmentEnum",
    "PolicyTypeEnum"
)

# from enum import Enum
from .base import BaseConstant

class DepartmentEnum(BaseConstant):
    HR = "HR"
    IT = "IT"
    MARKETING = "Marketing"
    FINANCE = "Finance"
    SALES = "Sales"

class PolicyTypeEnum(BaseConstant):
    ANNUAL = "Annual"
    MONTHLY = "Monthly"
    WEEKLY = "Weekly"
