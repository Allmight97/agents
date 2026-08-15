FROM ghcr.io/astral-sh/uv:0.12.4 AS uv

FROM python:3.13-slim

COPY --from=uv /uv /uvx /bin/

RUN groupadd --gid 10001 oura-mcp \
    && useradd --uid 10001 --gid 10001 --create-home oura-mcp \
    && mkdir -p /app /var/lib/oura-mcp \
    && chown -R 10001:10001 /app /var/lib/oura-mcp

WORKDIR /app

COPY --chown=10001:10001 pyproject.toml uv.lock README.md ./
COPY --chown=10001:10001 src ./src

RUN uv sync --frozen --no-dev

USER 10001:10001

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["oura-mcp", "serve"]
