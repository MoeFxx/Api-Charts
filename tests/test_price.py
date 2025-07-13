import os
import sys

import pytest
from httpx import AsyncClient, ASGITransport

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from run import app


@pytest.mark.asyncio
async def test_history():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.get("/price/history", params={"symbol": "AAPL:NASDAQ"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["symbol"] == "AAPL:NASDAQ"
    assert len(data["rows"]) > 0
