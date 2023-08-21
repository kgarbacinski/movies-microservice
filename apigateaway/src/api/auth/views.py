import json

from fastapi import APIRouter, Cookie, HTTPException, Response, status
from keycloak import (
    KeycloakAdmin,
    KeycloakAuthenticationError,
    KeycloakOpenID,
    KeycloakPostError,
)

from src.api.auth import schemas
from src.api.utils import create_registration_payload_from_request, set_fresh_cookies
from src.core.config import COOKIES
from src.core.keycloak_admin import keycloak_admin_config
from src.core.keycloak_config import keycloak_admin_config, keycloak_openid_config

router = APIRouter()


@router.post(
    "/register", tags=["register"], response_model=schemas.UserCreated, status_code=201
)
def register(request: schemas.UserRegister):
    payload = create_registration_payload_from_request(request)
    keycloak_admin = KeycloakAdmin(**keycloak_admin_config)
    try:
        user_id = keycloak_admin.create_user(payload, exist_ok=False)

    except KeycloakPostError as e:
        raise HTTPException(
            status_code=e.response_code, detail=json.loads(e.response_body)
        )

    return request


@router.get("/logout", tags=["logout"], status_code=200)
def logout():
    response = Response()
    for cookie in COOKIES:
        response.delete_cookie(key=cookie)
    return response


@router.post("/login", tags=["login"], status_code=200)
def login(request: schemas.UserLogin):
    user_credentials = request.dict()
    keycloak_openid = KeycloakOpenID(**keycloak_openid_config)
    try:
        token = keycloak_openid.token(**user_credentials)
    except KeycloakAuthenticationError as e:
        raise HTTPException(
            status_code=e.response_code, detail=json.loads(e.response_body)
        )
    response = Response()
    return set_fresh_cookies(response, token)


@router.get("/refresh", tags=["refresh"], status_code=200)
def refresh_token(refresh_token: str = Cookie(None), access_token: str = Cookie(None)):
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    keycloak_openid = KeycloakOpenID(**keycloak_openid_config)
    if keycloak_openid.introspect(access_token)["active"]:
        return Response(status_code=200)
    try:
        token = keycloak_openid.refresh_token(refresh_token)
    except KeycloakPostError as e:
        raise HTTPException(
            status_code=e.response_code, detail=json.loads(e.response_body)
        )
    response = Response()
    return set_fresh_cookies(response, token)
