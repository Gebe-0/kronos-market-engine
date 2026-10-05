from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime

class QuoteResponse(BaseModel):
    ticker: str = Field(..., description="Código do ativo (ex: PETR4, VALE3, HGLG11)")
    name: str = Field(..., description="Nome do ativo ou empresa")
    price: float = Field(..., description="Preço atual em BRL")
    change_percent: float = Field(..., description="Variação percentual diária")
    high: Optional[float] = Field(None, description="Preço máximo diário")
    low: Optional[float] = Field(None, description="Preço mínimo diário")
    volume: Optional[str] = Field(None, description="Volume financeiro aproximado")
    asset_type: Literal["stock", "fii", "crypto", "index"] = Field(..., description="Classe do ativo")
    updated_at: str = Field(..., description="Timestamp da última atualização")

class MacroIndicatorsResponse(BaseModel):
    selic_rate: float = Field(..., description="Meta Selic anualizada (% a.a.)")
    cdi_rate: float = Field(..., description="Taxa CDI anualizada (% a.a.)")
    ipca_12m: float = Field(..., description="IPCA acumulado em 12 meses (%)")
    usd_brl: float = Field(..., description="Cotação do Dólar Comercial (PTAX venda)")
    updated_at: str = Field(..., description="Data/hora de consulta ao Banco Central")

class AlertCreate(BaseModel):
    ticker: str = Field(..., min_length=2, max_length=15, description="Ticker do ativo monitorado")
    target_price: float = Field(..., gt=0, description="Preço de disparo do alerta")
    condition: Literal["ABOVE", "BELOW"] = Field(..., description="Condição de disparo (ACIMA ou ABAIXO)")
    notification_label: Optional[str] = Field(None, description="Nota descritiva do alerta")

class AlertResponse(BaseModel):
    id: int
    ticker: str
    target_price: float
    condition: str
    current_price: Optional[float]
    status: Literal["PENDING", "TRIGGERED"]
    created_at: str
    triggered_at: Optional[str] = None
    notification_label: Optional[str] = None
