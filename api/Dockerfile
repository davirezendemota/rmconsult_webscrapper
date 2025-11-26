# ---------- STAGE 1: BUILDER ----------
FROM python:3.12-slim AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir pipenv

# Diretório de build (igual à raiz do seu backend)
WORKDIR /api

# Copia apenas os arquivos do pipenv
COPY Pipfile Pipfile.lock ./

# Instala dependências NO SISTEMA (sem virtualenv)
RUN pipenv install --deploy --system --ignore-pipfile


# ---------- STAGE 2: RUNTIME ----------
FROM python:3.12-slim

RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copia libs instaladas do builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Diretório onde o código vai ficar
WORKDIR /api

# Copia TODO o backend
COPY . .

# Cria pasta para resultados
RUN mkdir -p /api/storage/resultados && \
    chown -R appuser:appuser /api

USER appuser

EXPOSE 8005

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8005"]
