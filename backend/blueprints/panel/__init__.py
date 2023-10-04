from flask import Blueprint

panel_bp = Blueprint('panel', __name__)

from backend.blueprints.panel import main