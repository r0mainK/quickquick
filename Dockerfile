FROM python:3.10 as builder

RUN pip install poetry==1.6.1
ENV POETRY_NO_INTERACTION=1
ENV POETRY_VIRTUALENVS_IN_PROJECT=1
ENV POETRY_VIRTUALENVS_CREATE=1
ENV POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /opt/app
COPY pyproject.toml poetry.lock ./
RUN touch README.md
RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --without dev --no-root

FROM python:3.10-slim as runtime

WORKDIR /opt/app
ENV VIRTUAL_ENV=/opt/app/.venv
ENV PATH="/opt/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}
COPY quickquick ./quickquick

ENV DISABLE_DOCUMENTATION=true
ENV SQLITE_FILEPATH=/opt/db/sqlite.db
VOLUME /opt/db/
EXPOSE 80

ENTRYPOINT ["python", "-m", "uvicorn", "--proxy-header", "--host", "0.0.0.0", , "--port", "80", "quickquick.server:app"]
