FROM python:3.13-slim-bookworm

RUN apt update && apt install -y libgdal-dev gdal-bin libpq5

RUN apt info libgdal-dev

# https://docs.astral.sh/uv/guides/integration/docker/#installing-uv
COPY --from=ghcr.io/astral-sh/uv:0.7.13 /uv /uvx /bin/

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

ENV JUST_VERSION=1.40.0
ENV JUST_INSTALLER_URL="https://raw.githubusercontent.com/casey/just/3884a4e68395b46c4b3eed694b09955f65b79fcc/www/install.sh"
ENV JUST_INSTALLER_SHA256SUM="2f811850e7833bf2191df55683f861d09b8a9cd2d1aac5f2adff597b3d675aa4  install.sh"

RUN apt install curl \
    && curl --proto '=https' --tlsv1.2 -sSf ${JUST_INSTALLER_URL} -o install.sh \
    && echo ${JUST_INSTALLER_SHA256SUM} > install.sha256 \
    && sha256sum -c install.sha256 \
    && chmod +x install.sh \
    && ./install.sh --tag ${JUST_VERSION} --to /usr/local/bin \
    && rm install.sh install.sha256 \
    && apt remove -y curl

COPY entrypoint.sh .

RUN chmod +x /entrypoint.sh

WORKDIR /app/

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH $PYTHONPATH:/app

ENTRYPOINT ["/entrypoint.sh"]
