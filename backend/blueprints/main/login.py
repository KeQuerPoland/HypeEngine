from flask import request, jsonify, current_app, render_template, redirect, url_for
from werkzeug.security import generate_password_hash
from backend.blueprints.main import main_bp
from backend import db
from backend.assets.login_handler import login_user, logout_user
from backend.database.users_db import User, UserSchema

@main_bp.route('/register', methods=['GET','POST'])
def register():
    with current_app.app_context():
        errors = {}
        if request.method == 'POST':
            user_schema = UserSchema()
            errors = user_schema.validate(request.form)
            if not errors:
                name = request.form.get('name')
                email = request.form.get('email')
                password = generate_password_hash(request.form.get('password'))

                user = User(name=name, email=email, password=password)
                db.session.add(user)
                db.session.commit()

                login_user(email, password)
                return redirect(url_for('main.index'))
        return render_template('register.html', errors=errors)


@main_bp.route('/login', methods=['GET','POST'])
def login():
    with current_app.app_context():
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            if login_user(email, password):
                return redirect(url_for('main.index'))
            else:
                return "Invalid credentials", 401
        else:
            return render_template('login.html')

@main_bp.route('/logout')
def logout():
    with current_app.app_context():
        logout_user()
        return redirect(url_for('main.index'))
