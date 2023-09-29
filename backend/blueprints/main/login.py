from flask import request, jsonify, render_template
from backend.blueprints.main import main_bp
from backend import db
from config import Config
from backend.database.users_db import User, UserSchema
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    errors = {}
    if request.method == 'POST':
        data = request.form
        user_schema = UserSchema()
        validation_errors = user_schema.validate(data)
        if validation_errors:
            errors.update(validation_errors)

        existing_user = User.query.filter_by(name=data['name']).first()
        if existing_user:
            errors['name'] = 'Nazwa użytkownika jest już zajęta'

        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            errors['email'] = 'Adres e-mail jest już zajęty'

        if errors:
            return render_template('register.html', errors=errors)

        hashed_password = generate_password_hash(data['password'], method='sha256')
        new_user = User(name=data['name'], email=data['email'], password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'Registered successfully'})
    return render_template('register.html', errors=errors)


@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            data = request.form
            user = User.query.filter_by(email=data['email']).first()
            if not user or not check_password_hash(user.password, data['password']):
                return 'Login Unsuccessful'
            try:
                a = login_user(user)
            except Exception as e:
                print(e)
            return 'Login Successful'
        except Exception as e:
            print(e)
    return render_template('login.html')

@main_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return 'Logged out successfully'
