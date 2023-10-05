from flask import Blueprint

from backend.blueprints.main import index, login

main_bp = Blueprint('main', __name__)
