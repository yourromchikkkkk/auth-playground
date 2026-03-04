from app.modules.role.controller import RoleController
from app.modules.role.models import AvailableRoles

def populate_user_into_db(db):
    try:
        for role in AvailableRoles:
            RoleController.create_role(db, role.value)
    except Exception as e:
        print(e)