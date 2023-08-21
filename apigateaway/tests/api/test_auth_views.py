from httpx import Cookies
from keycloak import KeycloakAuthenticationError, KeycloakPostError
from pytest import fixture

from src.api.auth import schemas
from tests.fixtures import MockFixture

mock = MockFixture("src.api.auth.views")


class TestRegisterView:
    URL = "/api/v1/auth/register"
    m_create_registration_payload_from_request = mock(
        "create_registration_payload_from_request"
    )
    m_keycloak_admin = mock("KeycloakAdmin")
    m_keycloak_admin_config = mock("keycloak_admin_config")

    @fixture
    def body(self):
        return dict(
            username="user",
            email="email@email.com",
            password="super_secret",
            confirmPassword="super_secret",
            firstName="name",
            lastName="lastname",
        )

    def test_normal(
        self,
        client,
        m_create_registration_payload_from_request,
        m_keycloak_admin,
        m_keycloak_admin_config,
        body,
    ):
        response = client.post(self.URL, json=body)
        m_create_registration_payload_from_request.assert_called_once_with(
            schemas.UserRegister(**body)
        )
        m_keycloak_admin.assert_called_once_with(**m_keycloak_admin_config)
        m_keycloak_admin.return_value.create_user.assert_called_once_with(
            m_create_registration_payload_from_request.return_value, exist_ok=False
        )
        assert response.status_code == 201
        assert response.json() == schemas.UserCreated(**body)

    def test_keycloak_error(
        self,
        client,
        m_create_registration_payload_from_request,
        m_keycloak_admin,
        m_keycloak_admin_config,
        body,
    ):
        m_keycloak_admin.return_value.create_user.side_effect = KeycloakPostError(
            response_body=b'{"errorMessage":"User exists with same username"}',
            response_code=409,
        )
        response = client.post(self.URL, json=body)
        m_create_registration_payload_from_request.assert_called_once_with(
            schemas.UserRegister(**body)
        )
        m_keycloak_admin.assert_called_once_with(**m_keycloak_admin_config)
        m_keycloak_admin.return_value.create_user.assert_called_once_with(
            m_create_registration_payload_from_request.return_value, exist_ok=False
        )
        assert response.status_code == 409
        assert response.json() == {
            "detail": {"errorMessage": "User exists with same username"}
        }


class TestLoginView:
    URL = "/api/v1/auth/login"
    m_keycloak_open_id = mock("KeycloakOpenID")
    m_keycloak_openid_config = mock("keycloak_openid_config")

    @fixture
    def body(self):
        return dict(username="user", password="super_secret")

    def test_normal(self, client, body, m_keycloak_open_id, m_keycloak_openid_config):
        response = client.post(self.URL, json=body)
        m_keycloak_open_id.assert_called_once_with(**m_keycloak_openid_config)
        m_keycloak_open_id.return_value.token.assert_called_once_with(**body)
        assert response.status_code == 200
        assert "access_token" in response.cookies
        assert "refresh_token" in response.cookies
        assert "id_token" in response.cookies

    def test_keycloak_error(
        self, client, body, m_keycloak_open_id, m_keycloak_openid_config
    ):
        m_keycloak_open_id.return_value.token.side_effect = KeycloakAuthenticationError(
            response_body=b'{"errorMessage":"Wrong_credentials"}',
            response_code=401,
        )
        response = client.post(self.URL, json=body)
        m_keycloak_open_id.assert_called_once_with(**m_keycloak_openid_config)
        assert response.status_code == 401
        assert response.json() == {"detail": {"errorMessage": "Wrong_credentials"}}


class TestLogoutView:
    URL = "/api/v1/auth/logout"
    m_response = mock("Response")

    def test_normal(self, client):
        response = client.get(self.URL)
        assert response.cookies == Cookies()


class TestRefresh:
    URL = "/api/v1/auth/refresh"
    m_keycloak_open_id = mock("KeycloakOpenID")
    m_keycloak_openid_config = mock("keycloak_openid_config")

    def test_access_token_ok(
        self, client, cookies, m_keycloak_open_id, m_keycloak_openid_config
    ):
        m_keycloak_open_id.return_value.introspect.return_value = {"active": True}
        response = client.get(self.URL, cookies=cookies)
        m_keycloak_open_id.assert_called_once_with(**m_keycloak_openid_config)
        m_keycloak_open_id.return_value.introspect_assert_called_once_with(
            cookies["access_token"]
        )
        assert response.status_code == 200

    def test_access_token_expired_refresh_token_ok(
        self, client, cookies, m_keycloak_open_id, m_keycloak_openid_config
    ):
        m_keycloak_open_id.return_value.introspect.return_value = {"active": False}
        response = client.get(self.URL, cookies=cookies)
        m_keycloak_open_id.assert_called_once_with(**m_keycloak_openid_config)
        m_keycloak_open_id.return_value.introspect.assert_called_once_with(
            cookies["access_token"]
        )
        assert "access_token" in response.cookies
        assert "refresh_token" in response.cookies
        assert "id_token" in response.cookies
        assert response.status_code == 200

    def test_access_token_expired_refresh_token_expired(
        self, client, cookies, m_keycloak_open_id, m_keycloak_openid_config
    ):
        m_keycloak_open_id.return_value.introspect.return_value = {"active": False}
        m_keycloak_open_id.return_value.refresh_token.side_effect = KeycloakPostError(
            response_body=b'{"errorMessage":"Token_expired"}', response_code=401
        )
        response = client.get(self.URL, cookies=cookies)
        m_keycloak_open_id.assert_called_once_with(**m_keycloak_openid_config)
        m_keycloak_open_id.return_value.introspect_assert_called_once_with(
            cookies["access_token"]
        )

        assert response.status_code == 401
        assert response.json() == {"detail": {"errorMessage": "Token_expired"}}

    def test_no_access_token(self, client):
        response = client.get(self.URL)
        assert response.json() == {"detail": "Unauthorized"}
        assert response.status_code == 401
