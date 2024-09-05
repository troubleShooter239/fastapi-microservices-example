from fastapi import APIRouter, HTTPException, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import db_dependency
from models import User
from schemas import UserModel

router = APIRouter(prefix="/users")

# Create a POST endpoint to create a new user
@router.post("")
async def create_user(user: UserModel, db: AsyncSession = db_dependency):
    new_user = User(**user.model_dump())

    if (await db.execute(select(User).where(User.email == new_user.email))).scalar():
        return Response("User already exists", 409)

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return Response(status_code=201)

# Create a GET endpoint to retrieve all users
@router.get("")
async def read_users(skip: int = 0, limit: int = 10, db: AsyncSession = db_dependency):
    return (await db.execute(select(User).offset(skip).limit(limit))).scalars().all()

# Create an UPDATE endpoint to update an existing user by its ID
@router.put("/{user_id}", response_model=UserModel)
async def update_user(user_id: int, updated_user: UserModel, db: AsyncSession = db_dependency):
    user = (await db.execute(select(User).where(User.id == user_id))).scalars().first()
    if user is None:
        raise HTTPException(404, "User not found")

    for key, value in updated_user.model_dump().items():
        if value:
            setattr(user, key, value)

    await db.commit()
    await db.refresh(user)
    return user

# Delete operation
@router.delete("/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = db_dependency):
    user = (await db.execute(select(User).where(User.id == user_id))).scalars().first()
    if not user:
        raise HTTPException(404, "User not found")
    await db.delete(user)
    await db.commit()
    return Response(status_code=204)
