import pytest
from sqlalchemy import create_engine
from repository import DatabaseRepository
from model import Base, BookingLine
import tempfile
import logging
from datetime import date

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.DEBUG)


@pytest.fixture(scope="session", autouse=True)
def database_repository(request):
    with tempfile.TemporaryDirectory() as tmpdirname:
        print(f"created temporary directory: {tmpdirname}")
        db_url = "sqlite:///" + tmpdirname + "/habook-test.db"
        # echo is needed forlogging
        engine = create_engine(db_url, echo=True)
        Base.metadata.create_all(engine)
        yield DatabaseRepository(engine)
        print("teardown completed")


@pytest.fixture(scope="function")
def parent_category(database_repository):
    database_repository.create_category("Mobilität")
    parent_category = database_repository.get_category_by_name("Mobilität")
    parent_category_id = parent_category.id
    yield parent_category
    database_repository.delete_category_by_id(parent_category_id)


def test_create_category(database_repository):
    database_repository.create_category("Haushalt")
    category = database_repository.get_category_by_name("Haushalt")
    assert category.name == "Haushalt"
    assert category.id is not None
    database_repository.delete_category_by_id(category.id)


def test_create_category_with_parent_category(database_repository, parent_category):
    database_repository.create_category("Auto", parent_category)
    category = database_repository.get_category_by_name("Auto")
    assert category.name == "Auto"
    assert category.id is not None
    assert category.parent_category.name == "Mobilität"
    database_repository.delete_category_by_id(category.id)


def test_create_category_with_parent_id(database_repository, parent_category):
    database_repository.create_category("Auto", parent_id=parent_category.id)
    category = database_repository.get_category_by_name("Auto")
    assert category.name == "Auto"
    assert category.id is not None
    assert category.parent_category.name == "Mobilität"


def test_delete_category_by_id(database_repository):
    database_repository.create_category("Haushalt")
    category = database_repository.get_category_by_name("Haushalt")
    database_repository.delete_category_by_id(category.id)
    with pytest.raises(ValueError):
        database_repository.get_category_by_name("Haushalt")


# TODO: parametrized tests to check all constraints
def test_create_booking_line(database_repository, parent_category):
    booking_line = BookingLine(
        description="Lebensmittel",
        amount=100.0,
        date=date(2024, 10, 1),
        category=parent_category,
        notes="Mehl",
    )
    database_repository.create_booking_line(booking_line)
    booking_line_reloaded = database_repository.get_booking_line_by_id(booking_line.id)
    assert booking_line_reloaded.amount == 100.0
    assert booking_line_reloaded.date == date(2024, 10, 1)
    assert booking_line_reloaded.category.name == "Mobilität"
    assert booking_line_reloaded.description == "Lebensmittel"
    assert booking_line_reloaded.notes == "Mehl"
