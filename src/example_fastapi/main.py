import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from example_fastapi.kafka import broker
from example_fastapi.middleware import setup_middleware
from example_fastapi.config_logging import configuration_logging
from example_fastapi.routers import note_router, user_router
from example_fastapi.routers.kafka_router import router as kafka_router

configuration_logging(logging_level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await broker.start()
    yield
    await broker.stop()


def app_factory():
    app = FastAPI(
        title="FastAPI Example",
        version="1.0.0",
        responses={404: {"description": "Not found"}},
        lifespan=lifespan,
    )

    setup_middleware(app=app)

    app.include_router(user_router.router)
    app.include_router(note_router.router)
    app.include_router(kafka_router)

    return app
