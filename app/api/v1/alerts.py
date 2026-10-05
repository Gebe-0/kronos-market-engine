from fastapi import APIRouter, Depends, HTTPException
from typing import List
import aiosqlite
from ...schemas.models import AlertCreate, AlertResponse
from ...db.database import get_db
from ...services.alert_service import create_alert, list_alerts, delete_alert

router = APIRouter(prefix="/alerts", tags=["Watchlist & Alertas de Preço"])

@router.post("", response_model=AlertResponse, summary="Criar novo alerta de preço")
async def post_alert(alert: AlertCreate, db: aiosqlite.Connection = Depends(get_db)):
    """Cadastra um gatilho de preço para um ativo (Ações, FIIs ou Cripto)."""
    return await create_alert(db, alert)

@router.get("", response_model=List[AlertResponse], summary="Listar todos os alertas")
async def get_alerts(db: aiosqlite.Connection = Depends(get_db)):
    """Retorna os alertas cadastrados e checa se foram disparados em tempo real."""
    return await list_alerts(db)

@router.delete("/{alert_id}", summary="Excluir alerta")
async def remove_alert(alert_id: int, db: aiosqlite.Connection = Depends(get_db)):
    """Remove um alerta de preço pelo ID."""
    deleted = await delete_alert(db, alert_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Alerta não encontrado.")
    return {"message": f"Alerta {alert_id} removido com sucesso."}
