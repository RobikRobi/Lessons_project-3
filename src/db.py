from fastapi import APIRouter
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import create_engine, ForeignKey, select
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker
from sqlalchemy.orm import DeclarativeBase, relationship
from .config import config

app = APIRouter(prefix="/db")

engine = create_async_engine(url=f'postgresql+asyncpg://{config.user}:{config.password}@localhost/lessons')
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session():
    async with  async_session() as session:
        yield session
        await session.commit()

class Base(DeclarativeBase):
    pass

@app.get("/")
def creat_db():
    Base.metadata.create_all(engine)
    return {"msg":"db creat"}