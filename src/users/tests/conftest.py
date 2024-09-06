from typing import AsyncGenerator

from httpx import AsyncClient, ASGITransport
from pytest import fixture
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from src.database import get_async_session, Base
# from src.models import User
from src.main import app

DATABASE_URL_TEST = "sqlite+aiosqlite:///:memory:"
engine_test = create_async_engine(DATABASE_URL_TEST, connect_args={"check_same_thread": False})
async_maker_test = async_sessionmaker(engine_test, autocommit=False, autoflush=False)

async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_maker_test() as session:
        yield session


@fixture(autouse=True, scope='session')
async def prepare_database() -> AsyncGenerator[None, None]:
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


app.dependency_overrides[get_async_session] = override_get_async_session


@fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app)) as ac:
        yield ac


# test_user_1 = User(**{
#     "name": "Alice", "email": "alice@mail.com", "address": "123 Main St", "user_type": "consumer"
# })
# test_user_2 = User(**{
#     "name": "Albert", "email": "albert@mail.com", "address": "127 Main St", "user_type": "supplier"
# })


# @fixture(scope='session')
# async def create_test_users():
#     db = await override_get_async_session()
#     db.add(test_user_1)
#     await db.commit()
#     await db.refresh(test_user_1)

#     db.add(test_user_2)
#     await db.commit()
#     await db.refresh(test_user_2)
