import aiosqlite
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "market_engine.db")

async def init_db():
    """Inicializa as tabelas do SQLite de forma assíncrona."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS price_alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticker TEXT NOT NULL,
                target_price REAL NOT NULL,
                condition TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'PENDING',
                notification_label TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                triggered_at TIMESTAMP
            )
        """)
        await db.commit()

async def get_db():
    """Gerador de conexão com o banco de dados SQLite."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        yield db
