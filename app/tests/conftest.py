from typing import Generator

import pytest
import uvicorn
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from app.api.dependencies import get_db
from app.core.record.infra.model import Record
from app.main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Record.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session")
def db() -> Generator:
    yield TestingSessionLocal()


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)