from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.api.routes import router
from src.core import config


def get_application() -> FastAPI:
    application = FastAPI(title=config.PROJECT_NAME, debug=config.DEBUG)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=config.ALLOWED_HOSTS or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(router, prefix=config.API_PREFIX)

    return application


app = get_application()
