from __future__ import annotations

from sqlalchemy.orm import Session

from app.utils import ResponseSchema

from .db_models import Role as RoleModel

class RoleController:
    """Controller for roles operations"""
    @staticmethod
    def create_role(db: Session, role: str) -> ResponseSchema[None]:
        """Create a new role"""
        try:
            existing_role = (
                db.query(RoleModel).filter(RoleModel.role == role).first()
            )
            if existing_role:
                print(f"Role already exists: {existing_role.role}")
                return ResponseSchema[None](
                    status=400,
                    message="Role already exists",
                    error="Role already exists",
                )
            new_role = RoleModel(role=role)
            db.add(new_role)
            db.commit()
            print(f"Role created: {new_role}")
            return ResponseSchema[None](
                status=201, message="User created successfully"
            )
        except Exception as e:
            return ResponseSchema[None](
                status=500, message="Error creating user", error=str(e)
            )
        