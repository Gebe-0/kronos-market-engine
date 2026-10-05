from fastapi import APIRouter
from ...schemas.models import MacroIndicatorsResponse
from ...services.bcb_service import fetch_macro_indicators

router = APIRouter(prefix="/macro", tags=["Indicadores Macroeconômicos"])

@router.get("/indicators", response_model=MacroIndicatorsResponse, summary="Taxas Oficiais (Selic, CDI, IPCA, Dólar)")
async def get_macro_data():
    """
    Retorna os principais indicadores macroeconômicos brasileiros:
    - **Meta Selic (% a.a.)**
    - **CDI Anualizado (% a.a.)**
    - **IPCA Acumulado 12 Meses (%)**
    - **Câmbio USD/BRL Oficial**
    """
    return await fetch_macro_indicators()
