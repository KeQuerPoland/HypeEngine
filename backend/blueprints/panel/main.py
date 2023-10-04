from flask import request, jsonify, current_app,render_template
from backend.blueprints.panel import panel_bp
from backend import db
from backend.assets.login_handler import login_required

@panel_bp.route('/')
@login_required
def index():
    return render_template('panel/panel_main.html')