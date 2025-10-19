# Билд-стадия
FROM python:3.10-slim as builder

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y --no-install-recommends gcc python3-dev

COPY pyproject.toml poetry.lock ./
RUN pip install --user poetry && \
    /root/.local/bin/poetry config virtualenvs.in-project true && \
    /root/.local/bin/poetry install --no-interaction --no-ansi --only main

# Финальная стадия
FROM python:3.10-slim

WORKDIR /app
ENV PATH="/app/.venv/bin:$PATH"
ENV ENV=production

# Установка runtime зависимостей
RUN apt-get update && apt-get install -y --no-install-recommends libpq5 && \
    rm -rf /var/lib/apt/lists/*

# Копируем только необходимое
COPY --from=builder /app/.venv ./.venv
COPY . .

# Настройка пользователя
RUN useradd -m -u 1001 appuser && chown -R appuser /app
USER appuser

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s \
  CMD curl -f http://localhost:8000/health || exit 1

CMD ["python", "-m", "hype_drakon"]