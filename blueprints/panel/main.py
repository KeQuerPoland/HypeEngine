from flask import current_app, jsonify, render_template, request

from backend import db
from assets.login_handler import login_required
from blueprints.panel import panel_bp
from security.__base__ import permission_required


@panel_bp.route('/')
@login_required
@permission_required('AccessPanel')
def index():
    return render_template('panel/panel_main.html')
