from fastapi import Cookie, HTTPException, status
from keycloak import KeycloakOpenID, KeycloakPostError

from src.core.keycloak_config import keycloak_openid_config


def check_if_admin(access_token: str = Cookie(None)):
    keycloak_openid = KeycloakOpenID(**keycloak_openid_config)
    try:
        introspect = keycloak_openid.introspect(access_token)
    except KeycloakPostError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if (
        not introspect["active"]
        or not introspect.get("groups")
        or "admin" not in introspect.get("groups")
    ):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return True


def check_if_logged_get_user_uuid(access_token: str = Cookie(None)):
    keycloak_openid = KeycloakOpenID(**keycloak_openid_config)
    try:
        introspect = keycloak_openid.introspect(access_token)
    except KeycloakPostError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if not introspect["active"]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return introspect["sub"]
