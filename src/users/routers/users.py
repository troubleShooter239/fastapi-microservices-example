from fastapi import APIRouter, HTTPException, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import User
from ..dependencies import db_dependency
from ..schemas import UserModel, UsersModel

router = APIRouter()

# Create a GET endpoint to retrieve all users
@router.get("/users/", response_model=UsersModel)
async def read_users(skip: int = 0, limit: int = 10, db: AsyncSession = db_dependency):
    return (await db.execute(select(User).offset(skip).limit(limit))).scalars().all()

# Create a POST endpoint to create a new user
@router.post("/users/")
async def create_user(user: UserModel, db: AsyncSession = db_dependency):
    try:
        new_user = User(**user.model_dump())
    except Exception:
        return Response("Bad user model", 400)

    if (await db.execute(select(User).where(User.email == new_user.email))).scalar():
        return Response("User already exists", 409)

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return Response(status_code=201)

# Create an UPDATE endpoint to update an existing user by its ID
@router.put("/users/{user_id}/", response_model=UserModel)
async def update_user(user_id: int, updated_user: UserModel, db: AsyncSession = db_dependency):
    user = (await db.execute(select(User).where(User.id == user_id))).scalars().first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in updated_user.model_dump().items():
        if value is None:
            continue
        setattr(user, key, value)

    await db.commit()
    await db.refresh(user)
    return user

# Delete operation
@router.delete("/users/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = db_dependency):
    user = (await db.execute(select(User).where(User.id == user_id))).scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await db.delete(user)
    await db.commit()
    return Response(status_code=204)
