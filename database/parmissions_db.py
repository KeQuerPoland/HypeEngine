from backend import db

user_roles = db.Table(
    'user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey(
        'user.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey(
        'role.id'), primary_key=True)
)

role_permissions = db.Table(
    'role_permissions',
    db.Column('role_id', db.Integer, db.ForeignKey(
        'role.id'), primary_key=True),
    db.Column('permission_id', db.Integer, db.ForeignKey(
        'permission.id'), primary_key=True)
)


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    permissions = db.relationship('Permission', secondary=role_permissions)

    def add_permission(self, permission_name):
        permission = Permission.query.filter_by(name=permission_name).first()
        if permission:
            if permission not in self.permissions:
                self.permissions.append(permission)
                db.session.commit()
        else:
            raise Exception("Permission not found")

    def remove_permission(self, permission_name):
        permission = Permission.query.filter_by(name=permission_name).first()
        if permission:
            if permission in self.permissions:
                self.permissions.remove(permission)
                db.session.commit()
        else:
            raise Exception("Permission not found")

    def create_role(self, role_name):
        role = Role.query.filter_by(name=role_name).first()
        if role is None:
            role = Role(name=role_name)
            db.session.add(role)
            db.session.commit()
        role = Role.query.filter_by(name=role_name).first()
        return role


class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def create_permission(permission_name):
        permission = Permission.query.filter_by(name=permission_name).first()
        if permission is None:
            permission = Permission(name=permission_name)
            db.session.add(permission)
            db.session.commit()
