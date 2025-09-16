import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import get_db, Base
from app import models
from app.config import settings
from app.oauth2 import create_access_token
from jose import jwt

# Test DB
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:toor@localhost:5432/fastapi_test"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# -----------------
# DB + client
# -----------------
@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


# -----------------
# Users + tokens
# -----------------
@pytest.fixture
def test_user(client):
    user_data = {"email": "test@gmail.com", "password": "123"}
    res = client.post("/users/", json=user_data)

    # allow both 201 (created) or 409 (already exists)
    if res.status_code == 201:
        new_user = res.json()
    elif res.status_code == 409:
        # fetch existing user manually
        new_user = client.post(
            "/auth/login",
            data={"username": user_data["email"], "password": user_data["password"]},
        ).json()
    else:
        raise Exception(f"Unexpected status code: {res.status_code}")

    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}
    return client


# -----------------
# Posts
# -----------------
@pytest.fixture
def test_posts(test_user, session):
    posts_data = [
        {
            "title": "First Post",
            "content": "Content of the first post",
            "owner_id": test_user["id"],
        },
        {
            "title": "Second Post",
            "content": "Content of the second post",
            "owner_id": test_user["id"],
        },
        {
            "title": "Third Post",
            "content": "Content of the third post",
            "owner_id": test_user["id"],
        },
        {
            "title": "Fourth Post",
            "content": "Content of the fourth post",
            "owner_id": test_user["id"],
        },
    ]

    posts = [models.Post(**data) for data in posts_data]
    session.add_all(posts)
    session.commit()
    return session.query(models.Post).all()


@pytest.fixture
def test_user2(client):
    user_data = {"email": "otheruser@gmail.com", "password": "123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user
