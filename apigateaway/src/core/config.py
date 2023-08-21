from typing import List

from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret

API_PREFIX = "/api/v1"

config = Config(".env")

PROJECT_NAME = config("PROJECT_NAME", default="FastAPI application")
DEBUG = config("DEBUG", cast=bool, default=False)
ALLOWED_HOSTS: List[str] = config(
    "ALLOWED_HOSTS", cast=CommaSeparatedStrings, default=""
)

KEYCLOAK_SERVER_URL = config("KEYCLOAK_SERVER_URL", default="localhost:80")
KEYCLOAK_ADMIN_USER = config("KEYCLOAK_ADMIN_USER", default="")
KEYCLOAK_ADMIN_PASSWORD = config("KEYCLOAK_ADMIN_PASSWORD", cast=Secret, default="")
KEYCLOAK_ADMIN_CLIENT_SECRET_KEY = config(
    "KEYCLOAK_ADMIN_CLIENT_SECRET_KEY", cast=Secret, default=""
)
KEYCLOAK_ADMIN_CLIENT_ID = config("KEYCLOAK_ADMIN_CLIENT_ID", default="")

KEYCLOAK_OPENID_CLIENT_SECRET_KEY = config(
    "KEYCLOAK_OPENID_CLIENT_SECRET_KEY", cast=Secret, default=""
)
KEYCLOAK_OPENID_CLIENT_ID = config("KEYCLOAK_OPENID_CLIENT_ID", default="")
KEYCLOAK_REALM_NAME = config("KEYCLOAK_REALM_NAME", default="")
MOVIES_API_URL = config("MOVIES_API_URL", default="")
IS_HTTPS = config("IS_HTTPS", cast=bool, default=False)
COOKIES = ["id_token", "access_token", "refresh_token"]
