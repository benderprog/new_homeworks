"""
создайте алхимичный engine
добавьте declarative base (свяжите с engine)
создайте объект Session
добавьте модели User и Post, объявите поля:
для модели User обязательными являются name, username, email
для модели Post обязательными являются user_id, title, body
создайте связи relationship между моделями: User.posts и Post.user
"""

import os

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Text,
)
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
)
from sqlalchemy.orm import (
    sessionmaker,
    declarative_base,
    relationship,
)
DB_URL = "postgresql+asyncpg://username:passwd@localhost:5432/hw4"

engine = create_async_engine(
    url=DB_URL,
    echo=False,
)

Base = declarative_base()
Session = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
    )

    name = Column(
        String(32),
        nullable=False,
        unique=False,
        default="",
        server_default="",
    )

    username = Column(
        String(32),
        nullable=False,
        unique=True,
        default="",
        server_default="",
    )

    email = Column(
        String(64),
        nullable=False,
        unique=True,
        default="",
        server_default="",
    )

    posts = relationship(
        "Post",
        back_populates="user",
        # uselist=True,
    )

    def __str__(self):
        return f"{self.__class__.__name__}" \
               f"(id={self.id}, name={self.name!r}, username={self.username!r}, email={self.email!r})"

    def __repr__(self):
        return str(self)

class Post(Base):
    __tablename__ = "posts"

    id = Column(
        Integer,
        primary_key=True,
    )

    user_id = Column(
        Integer,
        ForeignKey(User.id),
        nullable=False,
    )

    title = Column(
        String(120),
        nullable=False,
        unique=False,
    )

    body = Column(
        Text,
        nullable=False,
        unique=False,
        default="",
        server_default="",
    )

    user = relationship(
        "User",
        back_populates="posts",
        # uselist=False,
    )

    def __str__(self):
        return f"{self.__class__.__name__}" \
               f"(user_id={self.user_id}, title={self.title!r}, body={self.body!r})"

    def __repr__(self):
        return str(self)

async def create_tables():
    print("Creating tables for users and posts")
    async with engine.begin() as session:
        await session.run_sync(Base.metadata.drop_all)
        await session.run_sync(Base.metadata.create_all)
    print("Tables users and posts created successfully")

async def add_users_(users_data):
    print("Adding users")
    async with Session() as session:
        session: AsyncSession
        async with session.begin():
            for user_ in users_data:
                new_user = User(name=user_["name"], username=user_["username"], email=user_["email"])
                session.add(new_user)
    print("Users added successfully")

async def add_posts_(posts_data):
    print("Adding posts")
    async with Session() as session:
        session: AsyncSession
        async with session.begin():
            for post_ in posts_data:
                new_post = Post(user_id=post_["userId"], title=post_["title"], body=post_["body"])
                session.add(new_post)
    print("Posts added successfully")