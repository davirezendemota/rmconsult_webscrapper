# RM Consult Scrapers – Documentação do Projeto

## 1. Visão geral

Este repositório concentra os **scrapers de busca de empresas** que serão consumidos por outros serviços (como **n8n**, outros backends, etc.).  
O primeiro módulo implementado é o **scraper da SerpAPI para Google Maps**, responsável por:

- Buscar empresas no Google Maps a partir de um **termo de pesquisa** (ex.: `barbearia recife`)
- Retornar os resultados estruturados via **API FastAPI**
- Opcionalmente, gerar um **arquivo Excel completo e formatado** com todos os campos retornados
- Controlar consumo de **créditos** da SerpAPI via `credits.json`

A arquitetura do projeto foi pensada para ser **escalável**, permitindo adicionar novos scrapers em pastas separadas, reaproveitando a mesma estrutura de **controller → service → repository → utils**.

---

## 2. Arquitetura do projeto

Estrutura lógica em camadas:

- **FastAPI (API HTTP)**
  - Exposição de endpoints REST padronizados
  - Ideal para ser consumido pelo **n8n** ou outros orquestradores

- **Camada de Scraper**
  - Implementa a lógica de consulta à SerpAPI (`serapi_scraper`)
  - Converte o retorno cru em estruturas Python

- **Camada de Serviço (`SerApiService`)**
  - Orquestra o fluxo:
    - chama o scraper
    - atualiza créditos (`credits.json`)
    - aciona formatter de Excel (quando necessário)
    - registra log via repositório

- **Camada de Repositório (`SerApiRepository`)**
  - Por enquanto, apenas encapsula a lógica de logging em memória
  - Fácil de evoluir futuramente para salvar em banco (PostgreSQL, etc.)

- **Camada de Utilitários**
  - `excel_formatter`: monta e estiliza o Excel profissionalmente
  - `credits`: controla os créditos usados e últimos termos
  - `constants`: mapeamento de renomeação de colunas (`RENOMEAR_COLUNAS`)

---

## 3. Estrutura de pastas (projeto base)

Exemplo de estrutura sugerida:

```bash
rmconsult_scrappers/
├── Pipfile
├── Pipfile.lock
├── .env
├── main.py
├── app/
│   ├── __init__.py
│   ├── routers.py
│   └── scrappers/
│       ├── __init__.py
│       └── scrapper_serapi/
│           ├── __init__.py
│           ├── serapi_controller.py
│           ├── serapi_service.py
│           ├── serapi_repository.py
│           ├── serapi_scraper.py
│           ├── scrapper_serapi_dto.py
│           └── utils/
│               ├── __init__.py
│               ├── excel_formatter.py
│               ├── credits.py
│               └── constants.py
└── resultados/
```

- A pasta `scrapper_serapi` representa **uma família de scrapers** (SerpAPI Google Maps).
- Futuramente, você pode criar irmãs como `scrapper_googleplaces/`, `scrapper_instagram/` etc.

---

## 4. Dependências (Pipfile)

O projeto utiliza **Pipenv** para gerenciamento de ambiente.  

```toml
[[source]]
name = "pypi"
url = "https://pypi.org/simple"
verify_ssl = true

[packages]
fastapi = "*"
uvicorn = { extras = ["standard"], version = "*" }
pydantic = "*"
requests = "*"
pandas = "*"
openpyxl = "*"
python-dotenv = "*"
google-search-results = "*"   # serpapi
flet = "*"

[dev-packages]
pytest = "*"
black = "*"
isort = "*"
flake8 = "*"

[scripts]
dev = "uvicorn main:app --reload --port 8000"
prod = "uvicorn main:app --host 0.0.0.0 --port 8000"

[requires]
python_version = "3.12"
```

> Obs.: Em ambiente real, você pode ajustar versões específicas e adicionar outros scrapers ou libs conforme necessário.

---

## 5. Setup do projeto (passo a passo)

### 5.1. Pré-requisitos

- Python **3.12** instalado
- `pip` instalado
- `pipenv` instalado globalmente:

```bash
pip install pipenv
```

### 5.2. Clonar o repositório

```bash
git clone SEU_REPO_AQUI.git
cd rmconsult_scrappers
```

### 5.3. Instalar as dependências (via Pipenv)

```bash
pipenv install
```

Caso queira incluir pacotes de desenvolvimento também (pytest, black, etc.), use:

```bash
pipenv install --dev
```

### 5.4. Ativar o ambiente virtual (opcional)

Você pode simplesmente usar `pipenv run ...` **sem ativar** o ambiente.  
Mas, se quiser ativar o shell virtual:

```bash
pipenv shell
```

---

## 6. Variáveis de ambiente (.env)

Na raiz do projeto, crie um arquivo **`.env`** com:

```env
SERPAPI_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

- `SERPAPI_KEY`: chave da SerpAPI (Google Maps engine).
- Esse valor é carregado por `python-dotenv` dentro do módulo de scraper.

Sem essa variável, o projeto levanta um erro:

```text
RuntimeError: ❌ SERPAPI_KEY não encontrada no .env
```

---

## 7. Comandos do Pipfile (scripts)

No `Pipfile`, foram definidos scripts para facilitar o uso:

```toml
[scripts]
dev = "uvicorn main:app --reload --port 8000"
prod = "uvicorn main:app --host 0.0.0.0 --port 8000"
```

### 7.1. Rodar em ambiente de desenvolvimento

```bash
pipenv run dev
```

- Sobe o FastAPI com **reload automático** na porta `8000`.
- A API fica acessível em `http://127.0.0.1:8000`.
- A documentação Swagger fica em `http://127.0.0.1:8000/docs`.

### 7.2. Rodar em “modo produção” simples (local)

```bash
pipenv run prod
```

- Sobe o servidor na porta `8000`, aceitando conexões externas (`0.0.0.0`).
- Ideal para subir em container ou máquina remota (até integrar com um nginx / proxy reverso).

---

## 8. Endpoints principais

### 8.1. `POST /scrappers/serapi/buscar`

- **Descrição:** Executa busca no Google Maps via SerpAPI e retorna os dados em JSON.
- **Corpo (JSON):**

```json
{
  "termo": "barbearia recife"
}
```

- **Resposta (exemplo simplificado):**

```json
{
  "termo": "barbearia recife",
  "quantidade": 20,
  "meta": {
    "...": "..."
  },
  "credits": {
    "used": 3,
    "limit": 1000
  },
  "empresas": [
    {
      "title": "Barbearia X",
      "address": "Rua tal, 123 - Recife",
      "phone": "+55 ...",
      "...": "..."
    }
  ]
}
```

### 8.2. `POST /scrappers/serapi/buscar/excel`

- **Descrição:** Executa a mesma busca, mas gera um **arquivo Excel** no servidor.
- **Corpo (JSON):**

```json
{
  "termo": "barbearia recife"
}
```

- **Resposta (exemplo):**

```json
{
  "termo": "barbearia recife",
  "quantidade": 20,
  "arquivo": "resultados/barbearia_recife_2025-11-15_12-34-56-123456.xlsx"
}
```

> Observação: esse caminho é relativo ao servidor onde a API está rodando. Um próximo passo pode ser expor esse arquivo diretamente via endpoint de download ou subir para um storage (S3, etc.).

---

## 9. Exemplos de uso via curl

### 9.1. Buscar resultados em JSON

```bash
curl -X POST "http://127.0.0.1:8000/scrappers/serapi/buscar"   -H "Content-Type: application/json"   -d "{"termo": "barbearia recife"}"
```

### 9.2. Buscar e gerar Excel

```bash
curl -X POST "http://127.0.0.1:8000/scrappers/serapi/buscar/excel"   -H "Content-Type: application/json"   -d "{"termo": "barbearia recife"}"
```

---

## 10. Integração com n8n (visão geral)

O n8n poderá:

1. Disparar requisições HTTP para `POST /scrappers/serapi/buscar` ou `/buscar/excel`
2. Passar os parâmetros de **nicho** + **região** como `termo`
3. Consumir o **JSON de saída** para:
   - Salvar no PostgreSQL
   - Encadear outros workflows (enriquecimento, filtros, notificações, etc.)
4. Ou, no caso do Excel, baixar o arquivo e armazenar em outro lugar (Google Drive, S3, etc.)

---

## 11. Próximos passos / extensões

- Adicionar **banco de dados** real (PostgreSQL) e mover `SerApiRepository` para lá
- Criar novos módulos de scrapers:
  - `scrapper_googleplaces`
  - `scrapper_instagram`
  - `scrapper_tiktok`, etc.
- Centralizar logs de execução (nicho, região, timestamp, quantidade de resultados)
- Expor endpoint para leitura de `credits.json` (monitorar consumo da SerpAPI)
- Criar testes automatizados para services e utils

---

## 12. Resumo rápido de comandos

```bash
# 1) Instalar dependências
pipenv install

# 2) (Opcional) Entrar no shell virtual
pipenv shell

# 3) Rodar API em modo desenvolvimento
pipenv run dev

# 4) Rodar API em modo "produção" simples (local)
pipenv run prod
```

- Swagger: `http://127.0.0.1:8005/docs`
- Redoc: `http://127.0.0.1:8005/redoc`