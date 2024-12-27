from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.types import String, Integer
from sqlalchemy import ForeignKey
from sqlalchemy import create_engine
from typing import Optional


class Base(DeclarativeBase):
    pass


class Category(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement="auto")
    name: Mapped[str] = mapped_column(String(50))
    parent_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("category.id"))

    parent_category = relationship(lambda: Category, remote_side=id)

    def __repr__(self) -> str:
        return f"Category(id={self.id}, name={self.name})"


if __name__ == "__main__":
    engine = create_engine("sqlite:////Users/david/Documents/projects/habook/habook.db")
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
