import logging
import time
from collections.abc import Callable

from fastapi import Request
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


async def log_requests_middleware(request: Request, call_next: Callable):
    """Middleware для логирования запросов"""
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    logger.info(
        f"Handled request {request.method} {request.url.path} "
        f"in {duration:.4f} seconds. Status code: {response.status_code}"
    )
    return response


async def unhandled_exception_handler(request: Request, exc: Exception):
    """Глобальный обработчик исключений"""
    logger.error("Unhandled exception", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error"},
    )
