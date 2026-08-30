FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        default-libmysqlclient-dev \
        build-essential \
        pkg-config \
        gosu \
    && rm -rf /var/lib/apt/lists/*

COPY requirements/ /app/requirements/

RUN pip install --upgrade pip \
    && pip install -r /app/requirements/production.txt

COPY . /app

RUN chmod +x /app/deployment/docker/entrypoint.sh

RUN useradd \
    --create-home \
    --shell /bin/bash \
    appuser

RUN chown -R appuser:appuser /app

ENTRYPOINT ["/app/deployment/docker/entrypoint.sh"]
