from flask import Blueprint

from backend.blueprints.custom_handler import custom

custom_bp = Blueprint('custom', __name__)
