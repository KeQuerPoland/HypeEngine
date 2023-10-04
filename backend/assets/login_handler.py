from flask import session, g, current_app
from werkzeug.security import check_password_hash
from backend.database.users_db import User
from backend import bcrypt
from functools import wraps
from datetime import datetime, timedelta

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return "Please log in first", 401
        return f(*args, **kwargs)
    return decorated_function

def refresh_login(minutes):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            last_login = session.get('last_login')
            if last_login is None or datetime.now() - last_login > timedelta(minutes=minutes):
                return "Please log in again", 401
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def login_user(email, password):
    with current_app.app_context():
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            if user.account_locked == False:
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
