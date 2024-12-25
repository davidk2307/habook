import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from repository import DatabaseRepository
from model import Base
import tempfile
import logging

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)

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
    yield database_repository.get_category_by_name("Mobilität")
    

def test_create_category(database_repository):
    database_repository.create_category("Haushalt")
    category = database_repository.get_category_by_name("Haushalt")
    assert category.name == "Haushalt"
    assert category.id is not None

def test_create_category_with_parent(database_repository, parent_category):
    database_repository.create_category("Auto", parent_category)
    category = database_repository.get_category_by_name("Auto")
    assert category.name == "Auto"
    assert category.id is not None
    assert category.parent_category.name == "Mobilität"
    #assert category.parent_id == parent_category.id