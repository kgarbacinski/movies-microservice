from fastapi import Cookie, HTTPException, Response
from keycloak import KeycloakOpenID, KeycloakPostError
from starlette.requests import Request

from src.core.config import COOKIES, IS_HTTPS
from src.core.keycloak_config import keycloak_openid_config


def create_registration_payload_from_request(request):
    return {
        "email": request.email,
        "username": request.username,
        "enabled": True,
        "emailVerified": True,  # TODO emailverification
        "firstName": request.firstName,
        "lastName": request.lastName,
        "credentials": [
            {
                "value": request.password.get_secret_value(),
                "type": "password",
            }
        ],
    }


async def verify_token(
    request: Request,
    id_token: str = Cookie(""),
    access_token: str = Cookie(""),
    refresh_token: str = Cookie(""),
):
    keycloak_openid = KeycloakOpenID(**keycloak_openid_config)
    fresh_tokens = keycloak_openid.introspect(access_token)["active"]
    if not fresh_tokens:
        try:
            return keycloak_openid.refresh_token(refresh_token)
        except KeycloakPostError:
            raise HTTPException(
                status_code=401, detail={"error": "Credentials are expired"}
            )


def set_fresh_cookies(response: Response, token: dict):
    for cookie in COOKIES:
        response.set_cookie(
            key=cookie,
            value=token[cookie],
            secure=IS_HTTPS,
            samesite="none",
            httponly=True,
        )

    return response
