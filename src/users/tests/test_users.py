import pytest
import pytest_asyncio
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from ..main import app
from ..dependencies import get_db
from ..models import Base, User

DATABASE_URL = "sqlite+aiosqlite:///:memory:"
engine = create_async_engine(DATABASE_URL, connect_args={"check_same_thread": False})
TestSessionLocal = async_sessionmaker(engine, autocommit=False, autoflush=False)

async def db_session():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        await db.close()


app.dependency_overrides[get_db] = db_session
client = TestClient(app)


def db_setup(func):
    async def wrapper():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            print("CONNECTED")
        await func()
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            print("DISCONNECTED")
    return wrapper

def create_test_users(func):
    async def wrapper():
        db = TestSessionLocal()
        db.add(test_user_1)
        await db.commit()
        await db.refresh(test_user_1)

        db.add(test_user_2)
        await db.commit()
        await db.refresh(test_user_2)
        await db.close()

        await func()
    return wrapper

test_user_1 = User(**{
    "name": "Alice", "email": "alice@mail.com", "address": "123 Main St", "user_type": "consumer"
})
test_user_2 = User(**{
    "name": "Albert", "email": "albert@mail.com", "address": "127 Main St", "user_type": "supplier"
})

@pytest.mark.asyncio
@db_setup
async def test_create_user():
    json = {
        "name": "Alice", "email": "alice@mail.com", "address": "123 Main St", "user_type": "consumer"
    }
    response = client.post("/users/", json=json)
    assert response.status_code == status.HTTP_201_CREATED

    response = client.post("/users/", json=json)
    assert response.status_code == status.HTTP_409_CONFLICT

# @pytest_asyncio.fixture()
# async def create_test_users():
#     db = TestSessionLocal()
#     db.add(test_user_1)
#     await db.commit()
#     await db.refresh(test_user_1)

#     db.add(test_user_2)
#     await db.commit()
#     await db.refresh(test_user_2)
#     await db.close()

@pytest.mark.asyncio
@db_setup
@create_test_users
async def test_read_users():
    response = client.get("/users/")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()["users"]
    assert isinstance(data, list)
    assert len(data) == 2

@pytest.mark.asyncio
@db_setup
@create_test_users
async def test_read_user():
    response = client.get("/users/")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()["users"]
    assert isinstance(data, list)
    assert len(data) == 2


# @pytest.mark.asyncio
# async def test_update_user(db_setup, create_test_users):
#     new_address = "789 Main St"
#     response = client.put(f"/users/1/", json={"address": new_address})
#     assert response.status_code == status.HTTP_200_OK
#     assert response.json()["address"] == new_address

# @pytest.mark.asyncio
# async def test_delete_user(client: TestClient, db_session: AsyncSession):
#     new_user = User(name="John Doe", address="123 Elm Street", user_type="consumer")
#     db_session.add(new_user)
#     await db_session.commit()
#     await db_session.refresh(new_user)

#     assert client.delete(f"/users/{new_user.id}").status_code == 204

#     assert (await db_session.get(User, new_user.id)) is None
