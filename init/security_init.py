from database.parmissions_db import Role, Permission
from database.users_db import User
from flask import current_app
from backend import db

def init():
    with current_app.app_context():
        Permission.create_permission('*')
        Permission.create_permission('AccessPanel')
        Permission.create_permission('AccessOffline')

        adm_role = Role.create_role("Admin", "Admin")
        adm_role.add_permission('AccessPanel')
        adm_role.add_permission('*')
        
        adm_role = Role.create_role("Beta", "Beta")
        adm_role.add_permission('AccessOffline')

        user = User.query.filter_by(id="1").first()
        if user:
            role = Role.query.filter_by(name="Admin").first()
            if role:
                if role not in user.roles:
                    user.roles.append(role)
                    db.session.commit()
                else:
                    print("User already has the 'Admin' role")
            else:
                raise Exception("Role Admin not found")

        else:
            raise Exception("User not found")
