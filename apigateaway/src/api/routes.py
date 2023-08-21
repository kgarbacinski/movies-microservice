from fastapi import APIRouter

from src.api.admin import views as admin_views
from src.api.auth import views as auth_views
from src.api.user import views as user_views

router = APIRouter()
router.include_router(auth_views.router, prefix="/auth")
router.include_router(admin_views.router, prefix="/admin")
router.include_router(user_views.router, prefix="/user")
