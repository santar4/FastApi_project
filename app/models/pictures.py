from datetime import datetime

from sqlalchemy import String, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
import sqlalchemy as sa

from app.models import User
from settings import Base


class Picture(Base):
    __tablename__ = "pictures"

    id: Mapped[int] = mapped_column(primary_key=True)
    image: Mapped[bytes] = mapped_column(sa.LargeBinary, nullable=False)
    name: Mapped[str] = mapped_column(String(25), nullable=False)
    description: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    date: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)
    tag: Mapped[str] = mapped_column(String(25), nullable=False)

    author_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    author: Mapped["User"] = relationship(back_populates='pictures', lazy="selectin")

    comments: Mapped[list['Comment']] = relationship(
        back_populates='picture',
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    def __repr__(self):
        return f"<Picture(name={self.name})>"


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    author: Mapped["User"] = relationship(back_populates='comments', lazy="selectin")

    pictures_id: Mapped[int] = mapped_column(ForeignKey('pictures.id'), nullable=False)
    picture: Mapped["Picture"] = relationship(back_populates='comments', lazy="selectin")

    def __str__(self):
        return f"comment: {self.content}, {self.author.username}"

