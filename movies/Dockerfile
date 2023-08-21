FROM python:3.10-slim-bullseye AS base
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_NO_CACHE_DIR=1
RUN apt-get update && apt-get install -y --no-install-recommends && rm -rf /var/lib/apt/lists/*
RUN useradd -m user

FROM base AS builder
WORKDIR /app

COPY Pipfile.lock Pipfile ./

RUN pip install --upgrade pip
RUN pip install  pipenv
RUN pipenv install --dev --system --deploy


FROM base AS final-image

WORKDIR /app
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY . .
RUN chown -R user:user src/ tests/ && chmod -R 550 src/ tests/
USER user

EXPOSE 8000
