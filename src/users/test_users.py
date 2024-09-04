from fastapi.testclient import TestClient
import pytest

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from .main import app
from .dependencies import get_db
from .models import Base, User

DATABASE_URL = "sqlite+aiosqlite:///:memory:"
engine = create_async_engine(DATABASE_URL, connect_args={"check_same_thread": False})
TestSessionLocal = async_sessionmaker(engine, autocommit=False, autoflush=False)

# Base.metadata.create_all(bind=engine)

async def db_session():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    db = TestSessionLocal()
    try:
        yield db
    finally:
        await db.close()
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

app.dependency_overrides[get_db] = db_session
client = TestClient(app)

# @pytest.fixture(scope="module", autouse=True)
# async def setup_database():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#     yield
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)


def test_create_user():
    request_json = {
        "name": "Alice", "email": "alice@mail.com", "address": "123 Main St", "user_type": "consumer"
    }
    response = client.post("/users/", json=request_json)

    assert response.status_code == 201
    assert response.json() == request_json


# @pytest.mark.asyncio
# async def test_read_users(client: TestClient, db_session):
#     new_user = User(name="Jane Doe", address="456 Oak Street", user_type="supplier")
#     db_session.add(new_user)
#     await db_session.commit()
#     await db_session.refresh(new_user)

#     new_user = User(name="Don Don", address="123 Amog`Us Street", user_type="supplier")
#     db_session.add(new_user)
#     await db_session.commit()
#     await db_session.refresh(new_user)

#     response = await client.get("/users/")
#     assert response.status_code == 200
#     data = response.json()
#     assert isinstance(data, list)
#     assert len(data) > 0

# @pytest.mark.asyncio
# async def test_update_user(client: TestClient, db_session: AsyncSession):
#     new_user = User(name="Jane Doe", address="456 Oak Street", user_type="supplier")
#     db_session.add(new_user)
#     await db_session.commit()
#     await db_session.refresh(new_user)

#     new_address = "789 Main St"
#     update_response = await client.put(f"/users/{new_user.id}/", json={"address": new_address})
#     assert update_response.status_code == 200
#     assert update_response.json()["address"] == new_address

# @pytest.mark.asyncio
# async def test_delete_user(client: TestClient, db_session: AsyncSession):
#     new_user = User(name="John Doe", address="123 Elm Street", user_type="consumer")
#     db_session.add(new_user)
#     await db_session.commit()
#     await db_session.refresh(new_user)

#     assert client.delete(f"/users/{new_user.id}").status_code == 204

#     assert (await db_session.get(User, new_user.id)) is None
