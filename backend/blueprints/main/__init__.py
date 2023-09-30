from flask import Blueprint

main_bp = Blueprint('main', __name__)

from backend.blueprints.main import index