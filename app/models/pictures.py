from datetime import datetime

from sqlalchemy import String, func, ForeignKey, Table, Integer, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
import sqlalchemy as sa

from app.models import User
from settings import Base

picture_tag_association = Table(
    'picture_tag_association',
    Base.metadata,
    Column('picture_id', Integer, ForeignKey('pictures.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)

class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    pictures: Mapped[list['Picture']] = relationship(
        'Picture',
        secondary=picture_tag_association,
        foreign_keys=[picture_tag_association.c.picture_id, picture_tag_association.c.tag_id],  # Вказуємо правильні стовпці
        back_populates='tags')

class Picture(Base):
    __tablename__ = "pictures"

    id: Mapped[int] = mapped_column(primary_key=True)
    image: Mapped[bytes] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(String(25), nullable=False)
    description: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    date: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)
    tag: Mapped[str] = mapped_column(String(25), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    author: Mapped['User'] = relationship("User", back_populates="pictures")
    comments: Mapped[list['Comment']] = relationship('Comment', back_populates='picture', cascade="all, delete-orphan")

    tags: Mapped[list['Tag']] = relationship(
        'Tag',
        secondary=picture_tag_association,
        foreign_keys=[picture_tag_association.c.picture_id, picture_tag_association.c.tag_id],  # Вказуємо правильні стовпці
        back_populates='pictures')


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    author: Mapped['User'] = relationship("User", back_populates="comments")
    picture_id: Mapped[int] = mapped_column(ForeignKey('pictures.id'), nullable=False)
    picture: Mapped['Picture'] = relationship("Picture", back_populates="comments")
