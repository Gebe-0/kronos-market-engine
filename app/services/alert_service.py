import aiosqlite
from datetime import datetime
from typing import List, Optional
from ..schemas.models import AlertCreate, AlertResponse
from .b3_service import fetch_b3_quote
from .crypto_service import fetch_crypto_quote

async def create_alert(db: aiosqlite.Connection, alert: AlertCreate) -> AlertResponse:
    ticker = alert.ticker.upper().strip()
    cursor = await db.execute(
        """
        INSERT INTO price_alerts (ticker, target_price, condition, notification_label)
        VALUES (?, ?, ?, ?)
        """,
        (ticker, alert.target_price, alert.condition, alert.notification_label)
    )
    await db.commit()
    alert_id = cursor.lastrowid

    # Busca preço atual
    current = await fetch_b3_quote(ticker) or await fetch_crypto_quote(ticker)
    curr_price = current.price if current else None

    return AlertResponse(
        id=alert_id,
        ticker=ticker,
        target_price=alert.target_price,
        condition=alert.condition,
        current_price=curr_price,
        status="PENDING",
        created_at=datetime.utcnow().isoformat(),
        notification_label=alert.notification_label
    )

async def list_alerts(db: aiosqlite.Connection) -> List[AlertResponse]:
    cursor = await db.execute("SELECT * FROM price_alerts ORDER BY id DESC")
    rows = await cursor.fetchall()
    results = []

    for row in rows:
        ticker = row["ticker"]
        current = await fetch_b3_quote(ticker) or await fetch_crypto_quote(ticker)
        curr_price = current.price if current else None
        
        status = row["status"]
        triggered_at = row["triggered_at"]

        # Checa se o alerta deve ser disparado em tempo de consulta
        if status == "PENDING" and curr_price is not None:
            cond = row["condition"]
            target = row["target_price"]
            if (cond == "ABOVE" and curr_price >= target) or (cond == "BELOW" and curr_price <= target):
                status = "TRIGGERED"
                triggered_at = datetime.utcnow().isoformat()
                await db.execute(
                    "UPDATE price_alerts SET status = ?, triggered_at = ? WHERE id = ?",
                    (status, triggered_at, row["id"])
                )
                await db.commit()

        results.append(AlertResponse(
            id=row["id"],
            ticker=ticker,
            target_price=row["target_price"],
            condition=row["condition"],
            current_price=curr_price,
            status=status,
            created_at=str(row["created_at"]),
            triggered_at=str(triggered_at) if triggered_at else None,
            notification_label=row["notification_label"]
        ))

    return results

async def delete_alert(db: aiosqlite.Connection, alert_id: int) -> bool:
    cursor = await db.execute("DELETE FROM price_alerts WHERE id = ?", (alert_id,))
    await db.commit()
    return cursor.rowcount > 0
