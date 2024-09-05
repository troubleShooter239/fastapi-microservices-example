from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Base, engine, SessionLocal
# Dependency to get the database session
async def get_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()


db_dependency: AsyncSession = Depends(get_db)
