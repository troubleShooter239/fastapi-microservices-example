from fastapi import FastAPI, HTTPException, Depends, Response
from sqlalchemy.orm import Session

from models import User, get_db
from schemas import UserModel

app = FastAPI()

# Create a GET endpoint to retrieve all users
@app.get("/users/")
async def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users


# Create a POST endpoint to create a new user
@app.post("/users/")
async def create_user(user: UserModel, db: Session = Depends(get_db)):
    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# Create an UPDATE endpoint to update an existing user by its ID
@app.put("/users/{user_id}/")
async def update_user(user_id: int, updated_user: UserModel, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in updated_user.dict().items():
        if value is None:
            continue
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user


# Delete operation
@app.delete("/users/{user_id}", response_model=UserModel)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return Response(status_code=204)
