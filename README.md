# ⚡ KRONOS Market Engine — FastAPI Financial Data Service

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Pydantic v2](https://img.shields.io/badge/Pydantic-v2-E92063?style=flat&logo=pydantic&logoColor=white)](https://docs.pydantic.dev/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![SQLite](https://img.shields.io/badge/SQLite-aiosqlite-07405E?style=flat&logo=sqlite&logoColor=white)](https://sqlite.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **KRONOS Market Engine** é uma API REST assíncrona de alta performance desenvolvida em **Python + FastAPI**, projetada para coleta, tratamento, cache e monitoramento de cotações em tempo real da **B3 (Ações & FIIs)**, **Criptoativos**, **Indicadores Oficiais do Banco Central do Brasil (Selic, CDI, IPCA)** e gerenciamento de **Alertas de Preço (Watchlist)** com persistência SQLite.

---

## 🚀 Funcionalidades Principais

- 📈 **Cotações B3 & Cripto em Tempo Real**: Consulta individual ou em lote (`/batch/multi`) para ativos como `PETR4`, `VALE3`, `HGLG11`, `BTC` e `ETH`.
- 🏛️ **Indicadores Macroeconômicos Oficiais**: Integração direta com a API pública do Banco Central do Brasil (BCB SGS) para obtenção de Meta Selic, CDI, IPCA 12m e Câmbio PTAX.
- ⚡ **Cache TTL Inteligente**: Sistema em memória que reduz chamadas a APIs externas, acelerando as respostas para `< 5ms`.
- 🎯 **Watchlist com Gatilhos de Alerta**: CRUD assíncrono para monitorar preços alvos (`ABOVE` / `BELOW`) com persistência em SQLite (`aiosqlite`).
- 📚 **Swagger UI Interativa**: Documentação OpenAPI gerada automaticamente em `/docs` e `/redoc`.
- 🐳 **Pronto para Produção**: Multi-stage `Dockerfile` e `docker-compose.yml` inclusos.

---

## 🛠️ Stack Tecnológica

| Componente | Tecnologia |
| :--- | :--- |
| **Linguagem** | Python 3.12+ (Type Hints e async/await) |
| **Framework Web** | FastAPI + Uvicorn |
| **Requisições Assíncronas** | HTTPX (HTTP/2) + BeautifulSoup4 |
| **Validação de Dados** | Pydantic v2 |
| **Banco de Dados** | SQLite3 assíncrono via `aiosqlite` |
| **Testes Automatizados** | Pytest + Pytest-Asyncio |
| **Conteinerização** | Docker & Docker Compose |

---

## 📋 Endpoints da API

### Cotações (`/api/v1/quotes`)
- `GET /api/v1/quotes/{ticker}` — Retorna preço, máxima, mínima e variação do dia.
- `GET /api/v1/quotes/crypto/{symbol}` — Retorna cotação em BRL de Bitcoin, Ethereum ou Solana.
- `GET /api/v1/quotes/batch/multi?tickers=PETR4,VALE3,BTC` — Retorna dados em lote em uma única chamada.

### Macroeconômico (`/api/v1/macro`)
- `GET /api/v1/macro/indicators` — Taxa Selic, CDI, IPCA acumulado e Cotação do Dólar.

### Alertas de Preço (`/api/v1/alerts`)
- `POST /api/v1/alerts` — Cria um gatilho de preço para um ativo.
- `GET /api/v1/alerts` — Lista alertas e verifica se foram disparados.
- `DELETE /api/v1/alerts/{id}` — Remove um alerta pelo ID.

---

## 💻 Como Rodar Localmente

### Pré-requisitos
- Python 3.12+ instalado
- Git

### 1. Clonar o Repositório e Instalar Dependências
```bash
git clone https://github.com/Gebe-0/kronos-market-engine.git
cd kronos-market-engine
pip install -r requirements.txt
```

### 2. Iniciar a API
```bash
uvicorn app.main:app --reload --port 8000
```

Acesse a documentação interativa no navegador:
👉 **[http://localhost:8000/docs](http://localhost:8000/docs)**

---

## 🐳 Rodando via Docker

```bash
docker compose up -d --build
```
A API estará disponível imediatamente na porta `8000`.

---

## 🧪 Executando os Testes Automatizados

```bash
pytest tests/ -v
```

---

## 📄 Licença
Distribuído sob a licença MIT.
