# GymManager — imagem do backend (GYM-IAC-001)
# Contexto de build: raiz do repositório (para incluir banco-de-dados/migracoes/).
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    MIGRACOES_DIR=/app/migracoes

WORKDIR /app

COPY codigo-fonte/backend/requirements.txt .
RUN pip install -r requirements.txt

COPY codigo-fonte/backend/ .
COPY banco-de-dados/migracoes/ /app/migracoes/

RUN useradd --create-home --uid 10001 gymmanager && chown -R gymmanager /app
USER gymmanager

EXPOSE 5000
HEALTHCHECK --interval=10s --timeout=3s --start-period=60s --retries=5 \
    CMD python -c "import socket; socket.create_connection(('127.0.0.1', 5000), 2)" || exit 1

CMD ["python", "iniciar.py"]
