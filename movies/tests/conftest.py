from _pytest.fixtures import fixture
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src import schemas
from src.cruds.movie import add_movie
from src.db.base_class import Base
from src.main import app
from src.utils import get_db
from tests.fixtures import movies_dict

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@fixture
def client(db):
    # Dependency override

    def override_get_db():
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)


@fixture
def db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


@fixture
def insert_movie(db):
    movie = schemas.MovieSchemaOMBD(**movies_dict)
    add_movie(db, movie)
    return movie
