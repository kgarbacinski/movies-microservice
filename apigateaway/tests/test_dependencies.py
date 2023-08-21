from _pytest.python_api import raises
from fastapi import HTTPException
from keycloak import KeycloakPostError

from src.dependencies import check_if_admin, check_if_logged_get_user_uuid
from tests.fixtures import MockFixture

mock = MockFixture("src.dependencies")


class TestCheckIfAdmin:
    m_keycloak_open_id = mock("KeycloakOpenID")
    m_keycloak_openid_config = mock("keycloak_openid_config")

    def test_normal(
        self, m_keycloak_open_id, m_keycloak_openid_config, cookies, active_admin_user
    ):
        m_keycloak_open_id.return_value.introspect.return_value = active_admin_user
        result = check_if_admin(cookies["access_token"])
        m_keycloak_open_id.assert_called_once_with(**m_keycloak_openid_config)

        m_keycloak_open_id.return_value.introspect_assert_called_once_with(
            cookies["access_token"]
        )
        assert result is True

    def test_user_not_admin(
        self, m_keycloak_open_id, m_keycloak_openid_config, cookies, active_normal_user
    ):
        m_keycloak_open_id.return_value.introspect.return_value = active_normal_user

        with raises(HTTPException):
            check_if_admin(cookies["access_token"])

        m_keycloak_open_id.assert_called_once_with(**m_keycloak_openid_config)

        m_keycloak_open_id.return_value.introspect_assert_called_once_with(
            cookies["access_token"]
        )

    def test_unactive_user(
        self, m_keycloak_open_id, m_keycloak_openid_config, cookies, unactive_user
    ):
        m_keycloak_open_id.return_value.introspect.return_value = unactive_user

        with raises(HTTPException):
            check_if_admin(cookies["access_token"])

        m_keycloak_open_id.assert_called_once_with(**m_keycloak_openid_config)
        m_keycloak_open_id.return_value.introspect_assert_called_once_with(
            cookies["access_token"]
        )

    def test_no_cookies(self, m_keycloak_open_id, m_keycloak_openid_config):
        m_keycloak_open_id.return_value.introspect.side_effect = KeycloakPostError
        with raises(HTTPException):
            check_if_admin()
        m_keycloak_open_id.assert_called_once_with(**m_keycloak_openid_config)


class TestCheckIfLoggedGetUserUUID:
    m_keycloak_open_id = mock("KeycloakOpenID")
    m_keycloak_openid_config = mock("keycloak_openid_config")

    def test_normal(
        self, m_keycloak_open_id, m_keycloak_openid_config, active_normal_user, cookies
    ):
        m_keycloak_open_id.return_value.introspect.return_value = active_normal_user
        result = check_if_logged_get_user_uuid(cookies["access_token"])
        m_keycloak_open_id.assert_called_once_with(**m_keycloak_openid_config)
        m_keycloak_open_id.return_value.introspect_assert_called_once_with(
            cookies["access_token"]
        )
        assert result == active_normal_user["sub"]

    def test_unactive_user(
        self, m_keycloak_open_id, m_keycloak_openid_config, cookies, unactive_user
    ):
        m_keycloak_open_id.return_value.introspect.return_value = unactive_user

        with raises(HTTPException):
            check_if_logged_get_user_uuid(cookies["access_token"])

        m_keycloak_open_id.assert_called_once_with(**m_keycloak_openid_config)
        m_keycloak_open_id.return_value.introspect_assert_called_once_with(
            cookies["access_token"]
        )

    def test_no_cookies(self, m_keycloak_open_id, m_keycloak_openid_config):
        m_keycloak_open_id.return_value.introspect.side_effect = KeycloakPostError
        with raises(HTTPException):
            check_if_logged_get_user_uuid()
        m_keycloak_open_id.assert_called_once_with(**m_keycloak_openid_config)
