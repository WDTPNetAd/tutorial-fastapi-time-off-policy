from fastapi import Request
from app.core.exceptions import UnauthorizedException
from app.core.database import get_db

def verify_token(request: Request):
    token = request.headers.get("Authorization")
    if not token:
        # raise UnauthorizedException("Token not found")
        return
    
