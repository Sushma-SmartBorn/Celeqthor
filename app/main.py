from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from routers import auth
from config import settings
from services.redis_service import redis_service
from database import engine, Base
from exceptions import BaseAPIException
from utils.responses import error_response
import models
import logging

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0"
)

logger = logging.getLogger(__name__)

@app.exception_handler(BaseAPIException)
async def base_api_exception_handler(request, exc: BaseAPIException):
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response(
            message=exc.message,
            status=exc.status_code,
            data=exc.data
        )
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        field = ".".join(str(x) for x in error["loc"])
        errors.append({
            "field": field,
            "message": error["msg"]
        })
    
    return JSONResponse(
        status_code=422,
        content=error_response(
            message="Validation failed",
            status=422,
            data=errors
        )
    )

@app.exception_handler(Exception)
async def global_exception_handler(request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content=error_response(
            message="Internal server error",
            status=500
        )
    )


@app.get("/health")
async def health_check():
    redis_healthy = redis_service.check_connection()
    return {
        "status": "online",
        "redis": "healthy" if redis_healthy else "unhealthy"
    }

app.include_router(auth.router, prefix=f"{settings.API_V1_PREFIX}/auth", tags=["Auth"])
