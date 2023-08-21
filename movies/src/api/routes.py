from fastapi import APIRouter

from src.api import admin_views as admin_views
from src.api import user_views as user_views

router = APIRouter()
router.include_router(admin_views.router, prefix="/admin")
router.include_router(user_views.router, prefix="/user")
