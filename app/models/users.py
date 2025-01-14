from datetime import datetime

from sqlalchemy import String, Enum, Integer, Column, ForeignKey, Float, func
from sqlalchemy.orm import mapped_column, Mapped, relationship


from settings import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    bio_profile: Mapped[str] = mapped_column(nullable=True)

    create_date: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)

    pictures = relationship(
        'Picture',
        back_populates='author',
        cascade="all, delete-orphan",
        lazy="selectin"
    )
    comments = relationship(
        'Comment',
        back_populates='author',
        cascade="all, delete-orphan",
        lazy="selectin"
    )
