from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

class AppException(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail

# exception types
class NotFoundException(AppException):
    def __init__(self, msg: str = "Resource"):
        super().__init__(status_code=404, detail=f"{msg} not found")

class BadRequestException(AppException):
    def __init__(self, msg: str = "Bad Request"):
        super().__init__(status_code=400, detail=f"{msg}")

class UnauthorizedException(AppException):
    def __init__(self, msg: str = "Unauthorized"):
        super().__init__(status_code=401, detail=f"{msg}")

# list other types if needed

# registering custom handlers
def register_exception_handlers(app: FastAPI):

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "detail": exc.detail
            },
        )

    # @app.exception_handler(HTTPException)
    # async def http_exception_handler(request: Request, exc: HTTPException):
    #     return JSONResponse(
    #         status_code=exc.status_code,
    #         content={"detail": exc.detail},
    #     )

