FROM python:3.13-slim-bookworm

RUN --mount=type=cache,target=/var/cache/apt --mount=type=cache,target=/var/lib/apt \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates curl \
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

ENV JUST_VERSION=1.41.0
ENV JUST_INSTALLER_URL="https://raw.githubusercontent.com/casey/just/3884a4e68395b46c4b3eed694b09955f65b79fcc/www/install.sh"
ADD --checksum=sha256:2f811850e7833bf2191df55683f861d09b8a9cd2d1aac5f2adff597b3d675aa4 ${JUST_INSTALLER_URL} install.sh
RUN chmod +x install.sh && ./install.sh --tag ${JUST_VERSION} --to /usr/local/bin
RUN just --completions bash > ~/.bashrc

COPY entrypoint.sh .

RUN chmod +x /entrypoint.sh

WORKDIR /app/

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH $PYTHONPATH:/app

ENTRYPOINT ["/entrypoint.sh"]
