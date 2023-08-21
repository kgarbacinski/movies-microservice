from typing import List

from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings

API_PREFIX = "/api/v1"

config = Config(".env")

PROJECT_NAME = config("PROJECT_NAME", default="FastAPI application")
DEBUG = config("DEBUG", cast=bool, default=False)
ALLOWED_HOSTS: List[str] = config(
    "ALLOWED_HOSTS", cast=CommaSeparatedStrings, default=""
)

DATABASE_URL = config("DATABASE_URL", default="")
OMBD_API_KEY = config("OMBD_API_KEY", default="")
OMBD_URL = config("OMBD_URL", default="")
