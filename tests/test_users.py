import pytest
from jose import jwt
from app import models, schemas
from app.config import settings


def test_create_user(client):
    res = client.post("/users/", json={"email": "john100@gmail.com", "password": "123"})
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "john100@gmail.com"
    assert res.status_code == 201


def test_login_user(client, test_user):
    # login via API
    res = client.post(
        "/auth/login",
        data={"username": test_user["email"], "password": test_user["password"]},
    )
    assert res.status_code == 200

    # parse token response
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(
        login_res.access_token,
        settings.secret_key,
        algorithms=[settings.algorithm],
    )

    user_id = payload.get("user_id")
    assert user_id == test_user["id"]
    assert login_res.token_type == "bearer"


# def test_login_user_incorrect(client, test_user):
#     # try logging in with wrong password
#     res = client.post(
#         "/auth/login",
#         data={"username": test_user["email"], "password": "wrongpassword"},
#     )
#     assert res.status_code == 403  # should forbid login
#     data = res.json()
#     assert "detail" in data
#     assert data["detail"] == "Invalid Credentials"  # match your API error message

#     # try logging in with wrong email
#     res = client.post(
#         "/auth/login",
#         data={"username": "wrongemail@gmail.com", "password": test_user["password"]},
#     )
#     assert res.status_code == 403
#     data = res.json()
#     assert "detail" in data
#     assert data["detail"] == "Invalid Credentials"


@pytest.mark.parametrize(
    "email,password,status_code",
    [
        (
            "test@gmail.com",
            "wrongpassword",
            403,
        ),  # wrong password
        ("wrong@gmail.com", "123", 403),  # wrong email
        ("wrong@gmail.com", "wrongpassword", 403),  # both wrong
        (None, "123", 422),  # missing email
        ("test@gmail.com", None, 422),  # missing password
    ],
)
def test_incorrect_login(client, test_user, email, password, status_code):
    res = client.post(
        "/auth/login",
        data={"username": email, "password": password},
    )

    assert res.status_code == status_code
