import pytest

from database.database import Db


@pytest.fixture(scope="module")
def db():
    db = Db('data/database', clear=False)
    db.__enter__()
    db.create_tables()
    yield db
    db.__exit__(None, None, None)


def test_create_tables(db):
    db.create_tables()
    db.cursor.execute('SELECT name FROM sqlite_master WHERE type="table"')
    assert db.cursor.fetchall() == [('tokens',)]


## Faire le reste des tests de la base de données

if __name__ == '__main__':
    pytest.main(['-v'])
