from fastapi import APIRouter
from sqlalchemy import create_engine, ForeignKey, select
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker
from sqlalchemy.orm import DeclarativeBase, relationship
from .config import config

app = APIRouter(prefix="/db")

engine = create_engine(url=f'postgresql://{config.user}:{config.password}@localhost/lessons')
Session = sessionmaker(bind=engine)
session = Session()


def get_session():
    with Session() as session:
        yield session
        session.commit()

class Base(DeclarativeBase):
    pass

@app.get("/")
def creat_db():
    Base.metadata.create_all(engine)
    return {"msg":"db creat"}