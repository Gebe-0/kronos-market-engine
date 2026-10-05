from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict
from ...schemas.models import QuoteResponse
from ...services.b3_service import fetch_b3_quote
from ...services.crypto_service import fetch_crypto_quote

router = APIRouter(prefix="/quotes", tags=["Cotações de Mercado"])

@router.get("/{ticker}", response_model=QuoteResponse, summary="Obter cotação de ativo individual")
async def get_single_quote(ticker: str):
    """
    Retorna a cotação em tempo real de uma Ação, FII ou Criptoativo.
    Exemplos: `PETR4`, `VALE3`, `HGLG11`, `BTC`, `ETH`.
    """
    # Tenta B3 primeiro, depois Cripto
    quote = await fetch_b3_quote(ticker)
    if not quote:
        quote = await fetch_crypto_quote(ticker)

    if not quote:
        raise HTTPException(
            status_code=404,
            detail=f"Ativo '{ticker}' não encontrado ou dados indisponíveis no momento."
        )
    return quote

@router.get("/crypto/{symbol}", response_model=QuoteResponse, summary="Obter cotação de Criptoativo")
async def get_crypto_quote(symbol: str):
    """Retorna a cotação de um criptoativo (ex: BTC, ETH, SOL) em BRL."""
    quote = await fetch_crypto_quote(symbol)
    if not quote:
        raise HTTPException(status_code=404, detail=f"Criptoativo '{symbol}' não suportado.")
    return quote

@router.get("/batch/multi", response_model=List[QuoteResponse], summary="Obter múltiplas cotações em lote")
async def get_batch_quotes(tickers: str = Query(..., description="Tickers separados por vírgula (ex: PETR4,VALE3,BTC,HGLG11)")):
    """Permite que o frontend consulte vários ativos simultaneamente de forma rápida."""
    ticker_list = [t.strip().upper() for t in tickers.split(",") if t.strip()]
    results = []

    for t in ticker_list:
        q = await fetch_b3_quote(t) or await fetch_crypto_quote(t)
        if q:
            results.append(q)

    return results
