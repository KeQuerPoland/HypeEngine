from flask import request, jsonify, current_app,render_template
from backend.blueprints.main import main_bp
from backend import db

@main_bp.route('/')
def index():
    return render_template('main/index.html')