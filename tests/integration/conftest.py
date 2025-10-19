import pytest
from game.database import Database

@pytest.fixture(scope='module')
def test_database():
    """Фикстура тестовой базы данных"""
    db = Database(':memory:')  # Используем базу в памяти
    yield db
    db.close()

@pytest.fixture
def clean_database(test_database):
    """Очищает базу данных перед каждым тестом"""
    test_database.reset()
    return test_database