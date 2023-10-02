from flask import session, g, current_app
from werkzeug.security import check_password_hash
from backend.database.users_db import User
from backend import bcrypt

def login_user(email, password):
    with current_app.app_context():
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            print(user.account_locked)
            if user.account_locked == False:
                print("1")
                session['user_id'] = user.id
                return True
        return False

def logout_user():
    with current_app.app_context():
        session.pop('user_id', None)

class CurrentUser:
    def __init__(self):
        self.id = session.get('user_id')
        self.user = self.load_user()
    
    @property
    def is_authenticated(self):
        return self.user is not None

    def load_user(self):
        if self.id is not None:
            user = User.query.get(self.id)
            return user
        else:
            return None

    def __getattr__(self, name):
        if self.user is not None:
            return getattr(self.user, name)
        else:
            return None

def current_user():
    return CurrentUser()
