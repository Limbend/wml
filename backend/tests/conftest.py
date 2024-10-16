from typing import AsyncGenerator

import pytest
from pytest_asyncio import is_async_test
from fastapi.testclient import TestClient

from httpx import ASGITransport, AsyncClient

from api.main import app


# import asyncio
# from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
# from sqlalchemy.pool import NullPool

# from api.config import settings
# from api.repository import new_session


# engine_test = create_async_engine(
#     settings.db.connection_url, poolclass=NullPool, echo=False
# )
# override_new_session = async_sessionmaker(engine_test, expire_on_commit=False)
# app.dependency_overrides[new_session] = override_new_session


# metadata.bind = engine_test
# @pytest.fixture(autouse=True, scope="session")
# async def prepare_database():
#     async with engine_test.begin() as conn:
#         await conn.run_sync(metadata.create_all)
#     yield
#     async with engine_test.begin() as conn:
#         await conn.run_sync(metadata.drop_all)


# https://pytest-asyncio.readthedocs.io/en/latest/how-to-guides/run_session_tests_in_same_loop.html
def pytest_collection_modifyitems(items):
    pytest_asyncio_tests = (item for item in items if is_async_test(item))
    session_scope_marker = pytest.mark.asyncio(loop_scope="session")
    for async_test in pytest_asyncio_tests:
        async_test.add_marker(session_scope_marker, append=False)


client = TestClient(app)


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as async_test_client:
        yield async_test_client
