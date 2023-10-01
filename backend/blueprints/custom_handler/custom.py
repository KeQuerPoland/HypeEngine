from flask import request, jsonify, current_app,render_template
from backend.blueprints.custom_handler import custom_bp
from backend import db

@custom_bp.route('/<path:path>')
def catch_all(path):
    segments = path.split('/')
    return render_template('main/custom.html', a=segments)
