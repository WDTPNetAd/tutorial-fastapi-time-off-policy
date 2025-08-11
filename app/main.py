from fastapi import FastAPI
from app.core.exceptions import register_exception_handlers
# from app.models import policy as models
# import app.models.policy as models
from app.core.database import engine, Base

from app.api.v1.endpoints.policies import router as policy_router
from app.api.v1.endpoints.employees import router as employee_router
from app.api.v1.endpoints.time_off_requests import router as time_off_request_router

app = FastAPI()

# Create DB tables
# Base.metadata.create_all(bind=engine)

# Register global exception handlers
register_exception_handlers(app)

# Register router(s)
app.include_router(policy_router, prefix="/api/v1", tags=["Policies"])
app.include_router(employee_router, prefix="/api/v1", tags=["Employees"])
app.include_router(time_off_request_router, prefix="/api/v1", tags=["Time Off Requests"])