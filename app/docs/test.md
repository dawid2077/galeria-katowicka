# test_routes.py
from httpx import ASGITransport, AsyncClient
import pytest
from main import app  # Your FastAPI instance


@pytest.mark.asyncio
async def test_endpoint():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get(
            "/test/endpoint",
            headers={"Authorization": "Bearer MOCK_OR_REAL_JWT_TOKEN"},
        )
        assert response.status_code == 200