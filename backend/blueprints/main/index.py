from flask import current_app, jsonify, render_template, request

from backend import db
from backend.blueprints.main import main_bp


@main_bp.route('/')
def index():
    return render_template('main/index.html')
