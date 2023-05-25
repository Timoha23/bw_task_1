import asyncio
from typing import Generator

from sqlalchemy import select

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from db.models import Base, Quiz
from db.session import get_db
from main import app
from settings import TEST_DATABASE_URL


engine_test = create_async_engine(TEST_DATABASE_URL)

async_session_test = sessionmaker(
    engine_test,
    expire_on_commit=False,
    class_=AsyncSession
)

metadata = Base.metadata
metadata.bind = engine_test


async def _get_db_test() -> Generator:
    try:
        session: AsyncSession = async_session_test()
        yield session
    finally:
        await session.close()


app.dependency_overrides[get_db] = _get_db_test


@pytest.fixture(autouse=True, scope="session")
async def prepate_databse():
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.drop_all)


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="function")
async def db_session() -> Generator:
    try:
        session: AsyncSession = async_session_test()
        yield session
    finally:
        await session.close()


async def get_questions(db_session: AsyncSession) -> Quiz | list[Quiz]:
    async with db_session.begin():
        query = select(Quiz).order_by(Quiz.pub_date.desc())
        res = await db_session.execute(query)
        return res.fetchall()
