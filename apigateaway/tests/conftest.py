import uuid

from fastapi import HTTPException, status
from fastapi.testclient import TestClient
from pytest import fixture

from src.dependencies import check_if_admin, check_if_logged_get_user_uuid
from src.main import app


def override_check_if_admin_true():
    return True


def override_check_if_admin_error():
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


def ovveride_check_if_logged_true():
    return str(uuid.uuid4())


def override_check_if_logged_false():
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@fixture
def client():
    with TestClient(app) as c:
        yield c


@fixture
def m_is_admin_true():
    app.dependency_overrides[check_if_admin] = override_check_if_admin_true


@fixture
def m_user_not_logged():
    app.dependency_overrides[
        check_if_logged_get_user_uuid
    ] = override_check_if_logged_false


@fixture
def m_user_logged():
    app.dependency_overrides[
        check_if_logged_get_user_uuid
    ] = ovveride_check_if_logged_true


@fixture
def m_is_admin_false():
    app.dependency_overrides[check_if_admin] = override_check_if_admin_error


@fixture
def cookies():
    return dict(access_token="123", refresh_token="123", id_token="123")


@fixture
def active_admin_user():
    return {
        "exp": 1673620224,
        "iat": 1673619924,
        "jti": "1fd8fdc2-0cfe-4371-be28-6c854759bfe6",
        "iss": "http://keycloak:8080/realms/movies",
        "aud": "account",
        "sub": "9a7634fa-b735-4d28-94f8-30ab1b25517e",
        "typ": "Bearer",
        "azp": "movies",
        "session_state": "b43c1128-0ff9-48ea-973d-bc606d910833",
        "name": "admin admin",
        "given_name": "admin",
        "family_name": "admin",
        "preferred_username": "admin",
        "email_verified": True,
        "acr": "1",
        "realm_access": {
            "roles": ["offline_access", "uma_authorization", "default-roles-movies"]
        },
        "resource_access": {
            "account": {
                "roles": ["manage-account", "manage-account-links", "view-profile"]
            }
        },
        "scope": "openid profile email",
        "sid": "b43c1128-0ff9-48ea-973d-bc606d910833",
        "groups": ["admin"],
        "client_id": "movies",
        "username": "admin",
        "active": True,
    }


@fixture
def active_normal_user():
    return {
        "exp": 1673620901,
        "iat": 1673620601,
        "jti": "2c06bdc4-a378-4315-bb6d-ee7b4f4d72a4",
        "iss": "http://keycloak:8080/realms/movies",
        "aud": "account",
        "sub": "fe8245d5-2833-4971-8336-2502acf0174b",
        "typ": "Bearer",
        "azp": "movies",
        "session_state": "8cc7f4cf-6f58-47a0-b16c-8b23ceb1df46",
        "name": "test test",
        "given_name": "test",
        "family_name": "test",
        "preferred_username": "test",
        "email": "test@gmail.com",
        "email_verified": True,
        "acr": "1",
        "realm_access": {
            "roles": ["offline_access", "uma_authorization", "default-roles-movies"]
        },
        "resource_access": {
            "account": {
                "roles": ["manage-account", "manage-account-links", "view-profile"]
            }
        },
        "scope": "openid profile email",
        "sid": "8cc7f4cf-6f58-47a0-b16c-8b23ceb1df46",
        "groups": [],
        "client_id": "movies",
        "username": "test",
        "active": True,
    }


@fixture
def unactive_user():
    return {"active": False}
