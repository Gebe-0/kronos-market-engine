from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db.database import init_db
from .api.v1 import quotes, macro, alerts

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicialização assíncrona do banco de dados na partida
    await init_db()
    yield

app = FastAPI(
    title="KRONOS Market Engine",
    description="API REST de alta performance para cotações da B3, criptoativos, taxas do Banco Central e alertas de preço.",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Permite acesso cruzado (CORS) para conectar com o frontend do KRONOS ou qualquer cliente
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusão dos roteadores versionados
app.include_router(quotes.router, prefix="/api/v1")
app.include_router(macro.router, prefix="/api/v1")
app.include_router(alerts.router, prefix="/api/v1")

@app.get("/", tags=["Saúde"])
async def root():
    return {
        "service": "KRONOS Market Engine",
        "status": "online",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "quotes": "/api/v1/quotes/{ticker}",
            "macro": "/api/v1/macro/indicators",
            "alerts": "/api/v1/alerts"
        }
    }
