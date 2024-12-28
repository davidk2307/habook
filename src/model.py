from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.types import String, Integer, DECIMAL
from sqlalchemy import ForeignKey
from sqlalchemy import create_engine
from typing import Optional
import datetime
import locale


class Base(DeclarativeBase):
    pass


class Category(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement="auto")
    name: Mapped[str] = mapped_column(String(50), unique=True)
    parent_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("category.id"))

    parent_category = relationship(lambda: Category, remote_side=id)

    def __repr__(self) -> str:
        return f"Category(id={self.id}, name={self.name})"


class Person(Base):
    __tablename__ = "person"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement="auto")
    surname: Mapped[str] = mapped_column(String(30))
    lastname: Mapped[Optional[str]] = mapped_column(String(30))


class BookingLine(Base):
    __tablename__ = "booking_line"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement="auto")
    description: Mapped[str] = mapped_column(String(50))
    amount: Mapped[float] = mapped_column(DECIMAL(9, 2))
    date: Mapped[datetime.date] = mapped_column()
    notes: Mapped[Optional[str]] = mapped_column(String(255))
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"))
    category: Mapped["Category"] = relationship()

    def __repr__(self) -> str:
        return f"BookingLine(id={self.id}, amount={self.amount}, category_id={self.category_id})"
    
    @property
    def amount_formatted(self) -> str:
        # TODO: locale wo anders setzen?
        locale.setlocale(locale.LC_ALL, 'de_DE')
        return locale.format_string('%.2f', self.amount, True, True)
    
    @property
    def amount_negative(self) -> bool:
        return self.amount < 0


if __name__ == "__main__":
    engine = create_engine("sqlite:////Users/david/Documents/projects/habook/habook.db")
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
