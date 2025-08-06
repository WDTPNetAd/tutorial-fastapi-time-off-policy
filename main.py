from fastapi import FastAPI
from app.core.exceptions import register_exception_handlers
from app.models import policy as models
# import app.models.policy as models
from app.core.database import engine

from app.api.v1.endpoints.policies import router as policy_router

app = FastAPI()

# Create DB tables
models.Base.metadata.create_all(bind=engine)

# Register global exception handlers
register_exception_handlers(app)

# Register router(s)
app.include_router(policy_router, prefix="/api/v1", tags=["Policies"])