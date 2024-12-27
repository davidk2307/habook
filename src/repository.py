from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import joinedload
from sqlalchemy import Select
from sqlalchemy import Engine
from model import Category
from loguru import logger


class DatabaseRepository:
    def __init__(self, engine: Engine):
        self.engine = engine
        self.session = sessionmaker(engine)

    def create_category(self, name: str, parent_category: Category = None, parent_id: int = None) -> None:
        with self.session.begin() as session:
            if parent_id is not None:
                category = Category(name=name, parent_id=parent_id)
            else:
                category = Category(name=name, parent_category=parent_category)
            session.add(category)
            # session.flush()
            # session.commit()
            logger.info(
                f"new category created - id: '{category.id}', name: '{category.name}"
            )

    def get_category_by_name(self, name: str) -> Category:
        with self.session.begin() as session:
            categories = session.execute(
                Select(Category)
                .where(Category.name == name)
                .options(joinedload(Category.parent_category))
            ).all()
            # TODO: why is there also a tuple inside?
            category = categories[0][0]
            logger.info(f"successfully read category with name: {name}")
            session.expunge_all()
            return category

    def get_categories(self) -> list[Category]:
        with self.session.begin() as session:
            categories = session.execute(
                Select(Category).options(joinedload(Category.parent_category))
            ).all()
            session.expunge_all()
            return categories
