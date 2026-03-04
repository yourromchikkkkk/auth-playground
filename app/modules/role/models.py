from .db_models import Role as RoleModel
from enum import Enum

class AvailableRoles(Enum):
    SUPER_ADMIN = 'super-admin'
    ADMIN =  'admin'
    SUPPORT = 'support'

class Role:
    def __init__(
        self, id: str, role: str
    ):
        self.id = id
        self.role = role

    @classmethod
    def from_db_model(cls, db_role: RoleModel) -> "Role":
        """Create a Role from a database Role model"""
        return cls(
            id=db_role.id,
            role=db_role.email,
        )

    def __repr__(self):
        return f"<Role(id={self.id}, role={self.role})>"
