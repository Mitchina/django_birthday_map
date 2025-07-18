FROM python:3.13-slim-bookworm

RUN --mount=type=cache,target=/var/cache/apt --mount=type=cache,target=/var/lib/apt \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        # required by PostGIS
        gdal-bin

# https://docs.astral.sh/uv/guides/integration/docker/#installing-uv
COPY --from=ghcr.io/astral-sh/uv:0.7.19 /uv /uvx /bin/

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1
# Silence uv complaining about not being able to use hard links.
ENV UV_LINK_MODE=copy
# https://github.com/astral-sh/uv/pull/6834#issuecomment-2319253359
ENV UV_PROJECT_ENVIRONMENT="/usr/local/"
ENV UV_PYTHON_PREFERENCE=only-system

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project

COPY entrypoint.sh .

RUN chmod +x /entrypoint.sh

WORKDIR /app/

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH $PYTHONPATH:/app

ENTRYPOINT ["/entrypoint.sh"]
