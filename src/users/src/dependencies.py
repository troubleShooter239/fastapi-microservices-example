from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session

# Dependency to get the database session
db_dependency: AsyncSession = Depends(get_async_session)
