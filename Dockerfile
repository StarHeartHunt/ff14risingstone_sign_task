FROM python:3.12-bookworm as requirements-stage

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /tmp

COPY ./pyproject.toml ./uv.lock* /tmp/

RUN uv export --format requirements-txt --output-file requirements.txt --no-hashes

FROM python:3.12-slim-bookworm

WORKDIR /app

COPY --from=requirements-stage /tmp/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./src /app/src

ENV PYTHONPATH=/app

CMD ["python", "-m", "src"]
