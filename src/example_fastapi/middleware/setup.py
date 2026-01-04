from fastapi import FastAPI

from example_fastapi.middleware.middleware import (
    log_requests_middleware,
    unhandled_exception_handler,
)


def setup_middleware(app: FastAPI):
    """Функция для регистрации всех middleware"""
    app.middleware("http")(log_requests_middleware)
    app.add_exception_handler(Exception, unhandled_exception_handler)
