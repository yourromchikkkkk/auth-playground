from app.modules.user.controller import UserController
from app.modules.user.schemas import UserCreate
from app.modules.role.models import AvailableRoles
from app.modules.core import settings


def create_super_admin_user(db):
    """Creates initial super user"""
    UserController.create_user(
        db,
        UserCreate(email=settings.SUPER_USER_EMAIL, password=settings.SUPER_USER_PASS),
        AvailableRoles.SUPER_ADMIN,
    )