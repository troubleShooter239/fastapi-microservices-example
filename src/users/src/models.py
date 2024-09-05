from sqlalchemy.orm import Mapped, mapped_column

from database import Base


# Define an SQLAlchemy models for the database
class User(Base):
    __tablename__ = "users"
    id: Mapped[int]= mapped_column(primary_key=True, index=True, autoincrement=True)
    email: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str] = mapped_column()
    address: Mapped[str] = mapped_column()
    user_type: Mapped[str] = mapped_column()
