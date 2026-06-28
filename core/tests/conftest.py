import pytest

from core.database import create_engine, Base, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./memory.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args = {"check_same_thread":False}
)

testsessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

""" create fake database """
@pytest.fixture(scope="package")
def test_db():
    db = testsessionlocal()
    try:
        yield db
    finally:
        db.close()