from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from database.database import Base, SessionLocal
import pytest

@pytest.fixture(scope="module")
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    db = SessionLocal(bind=engine)
    try:
        yield db
    finally:
        db.close()

    Base.metadata.drop_all(engine)
