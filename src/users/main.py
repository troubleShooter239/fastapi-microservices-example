from fastapi import FastAPI, HTTPException, Depends, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import get_db, User
from schemas import UserModel, UsersModel

app = FastAPI()

# Create a GET endpoint to retrieve all users
@app.get("/users/", response_model=UsersModel)
async def read_users(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    return (await db.execute(select(User).offset(skip).limit(limit))).scalars().all()

# Create a POST endpoint to create a new user
@app.post("/users/", response_model=UserModel)
async def create_user(user: UserModel, db: AsyncSession = Depends(get_db)):
    new_user = User(**user.model_dump())
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

# Create an UPDATE endpoint to update an existing user by its ID
@app.put("/users/{user_id}/", response_model=UserModel)
async def update_user(user_id: int, updated_user: UserModel, db: AsyncSession = Depends(get_db)):
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
@app.delete("/users/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = (await db.execute(select(User).where(User.id == user_id))).scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await db.delete(user)
    await db.commit()
    return Response(status_code=204)
