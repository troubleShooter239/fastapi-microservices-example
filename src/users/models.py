from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


# Create an SQLite database
DATABASE_URL = "sqlite+aiosqlite:///./users.db"
engine = create_async_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = async_sessionmaker(engine, autocommit=False, autoflush=False)


# Define an SQLAlchemy models for the database
class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int]= mapped_column(primary_key=True, index=True, autoincrement=True)
    email: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str] = mapped_column()
    address: Mapped[str] = mapped_column()
    user_type: Mapped[str] = mapped_column()
