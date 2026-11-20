FROM python:3.14-slim

WORKDIR /app

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock README.md ./

RUN poetry install --only main --no-root --no-interaction

COPY hobby_tracker_api/ ./hobby_tracker_api/

RUN poetry install --only-root --no-interaction

EXPOSE 8000

CMD ["poetry", "run", "fastapi", "run"]
