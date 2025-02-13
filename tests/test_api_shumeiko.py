import pytest
from httpx import ASGITransport, AsyncClient
from src.main import app

@pytest.fixture
async def async_client():
    async with AsyncClient(
        base_url="http://test", transport=ASGITransport(app=app)
    ) as ac:
        yield ac

@pytest.mark.asyncio
async def test_get_items(async_client):
    response = await async_client.get("/items/")
    assert response.status_code == 200
    assert response.json() == [{"name": "Foo"}]

@pytest.mark.asyncio
async def test_post_item(async_client):
    response = await async_client.post("/items/", json={"name": "Bar"})
    assert response.status_code == 201
    assert response.json() == {"name": "Bar"}

@pytest.mark.asyncio
async def test_get_item_by_id(async_client):
    response = await async_client.get("/items/1")
    assert response.status_code == 200
    assert response.json() == {"name": "Foo"}

@pytest.mark.asyncio
async def test_update_item(async_client):
    response = await async_client.put("/items/1", json={"name": "Baz"})
    assert response.status_code == 200
    assert response.json() == {"name": "Baz"}

@pytest.mark.asyncio
async def test_delete_item(async_client):
    response = await async_client.delete("/items/1")
    assert response.status_code == 204
