# conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base, get_db
from app.main import app
from fastapi.testclient import TestClient
from app.tests.factories import create_policies

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"  # in-memory DB
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
    # poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)  # creates tables before tests
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client(db_session):
    def _get_test_db():
        yield db_session
    app.dependency_overrides[get_db] = _get_test_db
    test_client = TestClient(app)
    # attach factory to client
    test_client.create_policies = lambda count=1, **kwargs: create_policies(db_session, count, **kwargs)
    return test_client
