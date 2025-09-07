from database.database import Base, SessionLocal
from sqlalchemy import select
from models.User import User


def test_create_user_table(session): 
    user = User(email="test@example.com", name="Test User", hashed_password="hashedpassword")
    session.add(user)
    session.commit()

    userFound = session.scalar(
        select(User).where(User.email == "test@example.com")
    )

    assert userFound is not None
    assert userFound.email == "test@example.com"
    assert userFound.name == "Test User"
    assert userFound.hashed_password == "hashedpassword"
