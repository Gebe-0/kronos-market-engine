import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.db.database import init_db

@pytest_asyncio.fixture(autouse=True)
async def prepare_database():
    """Garante que a tabela do SQLite esteja inicializada antes de rodar os testes."""
    await init_db()

@pytest.mark.asyncio
async def test_root_endpoint():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "KRONOS Market Engine"
    assert data["status"] == "online"

@pytest.mark.asyncio
async def test_macro_indicators():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/v1/macro/indicators")
    assert response.status_code == 200
    data = response.json()
    assert "selic_rate" in data
    assert "cdi_rate" in data
    assert "ipca_12m" in data
    assert data["selic_rate"] > 0

@pytest.mark.asyncio
async def test_crypto_quote():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/v1/quotes/crypto/BTC")
    assert response.status_code == 200
    data = response.json()
    assert data["ticker"] == "BTC"
    assert data["price"] > 0
    assert data["asset_type"] == "crypto"

@pytest.mark.asyncio
async def test_b3_quote():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/v1/quotes/PETR4")
    assert response.status_code == 200
    data = response.json()
    assert data["ticker"] == "PETR4"
    assert data["price"] > 0
    assert data["asset_type"] == "stock"

@pytest.mark.asyncio
async def test_alerts_lifecycle():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # 1. Cria alerta
        payload = {
            "ticker": "PETR4",
            "target_price": 50.0,
            "condition": "ABOVE",
            "notification_label": "Alvo para realização parcial de lucros"
        }
        create_resp = await ac.post("/api/v1/alerts", json=payload)
        assert create_resp.status_code == 200
        alert_data = create_resp.json()
        assert alert_data["ticker"] == "PETR4"
        alert_id = alert_data["id"]

        # 2. Lista alertas
        list_resp = await ac.get("/api/v1/alerts")
        assert list_resp.status_code == 200
        alerts = list_resp.json()
        assert any(a["id"] == alert_id for a in alerts)

        # 3. Exclui alerta
        del_resp = await ac.delete(f"/api/v1/alerts/{alert_id}")
        assert del_resp.status_code == 200
