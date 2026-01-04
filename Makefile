.PHONY: run
run:
	uv run uvicorn src.example_fastapi.main:app_factory --factory --reload

.PHONY: migrate
migrate:
	uv run alembic upgrade head