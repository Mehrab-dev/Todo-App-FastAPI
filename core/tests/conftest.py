from fastapi.testclient import TestClient
import pytest
import random

from core.database import create_engine, Base, sessionmaker, get_db
from main import app
from users.models import UserModel
from tasks.models import TaskModel
from auth.jwt_auth import generate_access_token


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


""" replacing the fake database with the original database for testing """
@pytest.fixture(scope="package",autouse=True)
def override_dependencies(test_db):
    app.dependency_overrides[get_db] = lambda: test_db
    yield
    app.dependency_overrides.pop(get_db)


""" create tables for database """
@pytest.fixture(scope="session",autouse=True)
def tear_up_and_down_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


""" not authentication user """
@pytest.fixture(scope="function")
def anon_user():
    client = TestClient(app)
    yield client


""" authentication user """
@pytest.fixture(scope="function")
def auth_user(test_db):
    client = TestClient(app)
    user = test_db.query(UserModel).filter_by(email="test@gmail.com").one()
    access_token = generate_access_token(user_id=user.id)
    client.headers.update({"Authorization":f"Bearer {access_token}"})
    yield client


""" create fake data (user, tasks) """
@pytest.fixture(scope="package",autouse=True)
def generate_mock_data(test_db):
    """ create fake user """
    user = UserModel(email="test@gmail.com")
    user.set_password("1234")
    test_db.add(user)
    test_db.commit()

    """ create fake tasks """
    tasks_list = []
    for _ in range(10):
        tasks_list.append(
            TaskModel(
                user_id = user.id,
                title = "test",
                description = "description",
                is_completed = random.choice([True, False])
            )
        )

        test_db.add_all(tasks_list)
        test_db.commit()


""" choose a random task """
@pytest.fixture(scope="function")
def random_task(test_db):
    user = test_db.query(UserModel).filter_by(email="test@gmail.com").one()
    task = test_db.query(TaskModel).filter_by(user_id=user.id).first()
    return task
