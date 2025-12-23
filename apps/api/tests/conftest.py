import json
import asyncio
from pathlib import Path
from datetime import date, datetime
from typing import AsyncGenerator, List

import pytest
from httpx import AsyncClient, ASGITransport
from sqlmodel import SQLModel
from sqlalchemy import text, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from src.main import app
from src import models  # pylint: disable=unused-import
from src.sqldb import get_session


# Test database URL
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test_varinautsqlite.db"

# Test engine and session
test_engine = create_async_engine(TEST_DATABASE_URL, echo=False, future=True)
test_async_session = sessionmaker(
    test_engine, class_=AsyncSession, expire_on_commit=False
)


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def setup_test_database():
    """Set up test database schema."""
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
    # Clean up after all tests
    await test_engine.dispose()


@pytest.fixture
async def test_session() -> AsyncGenerator[AsyncSession, None]:
    """Create a test database session."""
    async with test_async_session() as session:
        # Clear all tables before each test
        def get_table_names(conn):
            inspector = inspect(conn)
            return inspector.get_table_names()

        async with test_engine.begin() as conn:
            table_names = await conn.run_sync(get_table_names)

        for table_name in table_names:
            await session.execute(text(f"DELETE FROM {table_name}"))
        await session.commit()

        yield session

        # Rollback any changes after each test
        await session.rollback()


@pytest.fixture
async def client(test_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Create a test client with dependency override."""

    async def override_get_session() -> AsyncGenerator[AsyncSession, None]:
        yield test_session

    app.dependency_overrides[get_session] = override_get_session

    # Use ASGITransport for FastAPI apps with httpx
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
async def load_test_data(test_session: AsyncSession):
    """Load test data from JSON fixtures."""
    fixtures_dir = Path(__file__).parent / "fixtures"

    # Get all model classes from the models module
    available_models = {
        name: cls
        for name, cls in vars(models).items()
        if isinstance(cls, type)
        and issubclass(cls, SQLModel)
        and cls is not SQLModel  # Exclude SQLModel itself
        and hasattr(cls, "__tablename__")
    }

    # Fields that require date/datetime conversion from ISO strings
    date_fields: List[str] = ["known_date"]
    datetime_fields: List[str] = ["created_at", "updated_at", "resolved_at"]

    # Load each fixture file
    for fixture_file in sorted(fixtures_dir.glob("*.json")):
        model_name = fixture_file.stem  # filename without .json extension

        if model_name not in available_models:
            continue

        model_class = available_models[model_name]

        with open(fixture_file, encoding="utf-8") as f:
            fixture_data = json.load(f)

        for item_data in fixture_data:
            # Convert date/datetime strings to objects for specified fields

            for field_name in date_fields:
                field_value = item_data.get(field_name)
                if field_value is not None:
                    item_data[field_name] = date.fromisoformat(field_value)

            for field_name in datetime_fields:
                field_value = item_data.get(field_name)
                if field_value is not None:
                    item_data[field_name] = datetime.fromisoformat(field_value)

            # Create and save the model instance
            model_instance = model_class(**item_data)
            test_session.add(model_instance)

        await test_session.commit()

    yield
