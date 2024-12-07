from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import Base


# модель для сохранения данный в БД
class Products(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column (primary_key=True)
    name: Mapped[str] = mapped_column()
    price: Mapped[int] = mapped_column()
    description: Mapped[str] = mapped_column()

