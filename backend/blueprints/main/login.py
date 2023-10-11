from flask import (current_app, jsonify, redirect, render_template, request,
                   url_for,flash)
from werkzeug.security import generate_password_hash

from backend import bcrypt, db
from backend.assets.login_handler import login_user, logout_user
from backend.blueprints.main import main_bp
from backend.database.users_db import User, UserSchema
from backend.security.ec_token import generate_confirmation_token, confirm_token
from backend.assets.login_handler import login_user, logout_user, login_required
import datetime


@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    with current_app.app_context():
        errors = {}
        if request.method == 'POST':
            user_schema = UserSchema()
            errors = user_schema.validate(request.form)
            if not errors:
                name = request.form.get('name')
                email = request.form.get('email')
                password = bcrypt.generate_password_hash(
                    request.form.get('password')).decode('utf-8')

                user = User(name=name, email=email, password=password)
                db.session.add(user)
                db.session.commit()

                login_user(email, password)
                return render_template('register_scc.html')
        return render_template('register.html', errors=errors)


@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    with current_app.app_context():
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            if login_user(email, password):
                return render_template('login_scc.html')
            else:
                return render_template('login_err.html'), 401
        else:
            return render_template('login.html')


@main_bp.route('/logout')
def logout():
    with current_app.app_context():
        logout_user()
        return redirect(url_for('main.index'))
    
@main_bp.route('/confirm/<token>')
@login_required
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    user = User.query.filter_by(email=email).first_or_404()
    if user.email_verifed:
        flash('Account already confirmed. Please login.', 'success')
    else:
        user.email_verifed = True
        #user.confirmed_on = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('main.index'))
