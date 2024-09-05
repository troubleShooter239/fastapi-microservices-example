from httpx import AsyncClient
from fastapi import status


async def test_create_user(ac: AsyncClient):
    json = {
        "name": "Alice", "email": "alice@mail.com", "address": "123 Main St", "user_type": "consumer"
    }
    response = await ac.post("/users/", json=json)
    assert response.status_code == status.HTTP_201_CREATED

    response = await ac.post("/users/", json=json)
    assert response.status_code == status.HTTP_409_CONFLICT


# async def test_read_users(ac: AsyncClient):
#     response = await ac.get("/users/")
#     assert response.status_code == status.HTTP_200_OK

#     data = response.json()["users"]
#     assert isinstance(data, list)
#     assert len(data) == 2


# async def test_read_user(ac: AsyncClient):
#     response = await ac.get("/users/")
#     assert response.status_code == status.HTTP_200_OK

#     data = response.json()["users"]
#     assert isinstance(data, list)
#     assert len(data) == 2


# async def test_update_user(ac: AsyncClient):
#     new_address = "789 Main St"
#     response = await ac.put(f"/users/1/", json={"address": new_address})
#     assert response.status_code == status.HTTP_200_OK
#     assert response.json()["address"] == new_address

# async def test_delete_user(ac: AsyncClient):
#     new_user = User(name="John Doe", address="123 Elm Street", user_type="consumer")
#     db_session.add(new_user)
#     await db_session.commit()
#     await db_session.refresh(new_user)

#     assert client.delete(f"/users/{new_user.id}").status_code == 204

#     assert (await db_session.get(User, new_user.id)) is None
