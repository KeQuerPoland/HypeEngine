from flask import Blueprint

custom_bp = Blueprint('custom', __name__)

from backend.blueprints.custom_handler import custom