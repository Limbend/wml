import os
import sys
from typing import AsyncGenerator

import pytest
from pytest_asyncio import is_async_test
from fastapi.testclient import TestClient

from httpx import ASGITransport, AsyncClient

sys.path.append(os.path.join(sys.path[0], ".."))
sys.path.append(os.path.join(sys.path[0], "../api"))

from main import app
from config import settings


# https://pytest-asyncio.readthedocs.io/en/latest/how-to-guides/run_session_tests_in_same_loop.html
def pytest_collection_modifyitems(items):
    pytest_asyncio_tests = (item for item in items if is_async_test(item))
    session_scope_marker = pytest.mark.asyncio(loop_scope="session")
    for async_test in pytest_asyncio_tests:
        async_test.add_marker(session_scope_marker, append=False)


client = TestClient(app)


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    assert settings.launch_mode == "test"

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as async_test_client:
        yield async_test_client
