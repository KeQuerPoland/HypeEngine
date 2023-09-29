from flask import request, jsonify, current_app
from backend.blueprints.main import main_bp
from backend import db

@main_bp.route('/init')
def init():
    with current_app.app_context():
        db.create_all()
    return "OK!",200