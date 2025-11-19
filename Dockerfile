# Stage 1: Builder
FROM python:3.12-slim AS builder

# Instalar dependências do sistema necessárias para pipenv e compilação
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Instalar pipenv
RUN pip install --no-cache-dir pipenv

# Definir diretório de trabalho
WORKDIR /app

# Copiar arquivos do pipenv
COPY Pipfile Pipfile.lock ./

# Instalar dependências do projeto (apenas production)
# --deploy: garante que Pipfile.lock está atualizado
# --system: instala no sistema Python (sem virtualenv)
# --ignore-pipfile: usa apenas Pipfile.lock
RUN pipenv install --deploy --system --ignore-pipfile

# Stage 2: Runtime
FROM python:3.12-slim

# Criar usuário não-root para segurança
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Instalar pipenv para usar os scripts do Pipfile
RUN pip install --no-cache-dir pipenv

# Copiar dependências instaladas do builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Definir diretório de trabalho
WORKDIR /app

# Copiar Pipfile e Pipfile.lock para usar scripts
COPY Pipfile Pipfile.lock ./

# Copiar código da aplicação
COPY . .

# Criar diretório para armazenamento e dar permissões
RUN mkdir -p /app/storage/resultados && \
    chown -R appuser:appuser /app

# Mudar para usuário não-root
USER appuser

# Expor porta da aplicação
EXPOSE 8005

# Comando para executar a aplicação em produção usando script do Pipfile
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8005"]
