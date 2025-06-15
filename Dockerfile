FROM python:3.13

RUN apt update && apt install -y libgdal-dev gdal-bin libpq5

RUN apt info libgdal-dev

ARG REQUIREMENTS_FILE=requirements.txt

COPY requirements.txt requirements.txt

# https://docs.astral.sh/uv/guides/integration/docker/#installing-uv
COPY --from=ghcr.io/astral-sh/uv:0.7.13 /uv /uvx /bin/

# https://hynek.me/articles/docker-uv/
ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never

# https://docs.docker.com/reference/dockerfile/#run---mounttypecache
# By default, a cache mount is identified by the target path and shared across builds.
# Since uv's cache is safe for threads and concurrent access, this is also safe.
RUN --mount=type=cache,target=/root/.cache \
    uv pip install --system -r requirements.txt

COPY entrypoint.sh .

RUN chmod +x /entrypoint.sh

WORKDIR /app/

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH $PYTHONPATH:/app

ENTRYPOINT ["/entrypoint.sh"]
