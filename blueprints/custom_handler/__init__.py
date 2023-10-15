from flask import Blueprint
from backend import static_folder,template_folder

custom_bp = Blueprint('custom', __name__,static_folder=static_folder,template_folder=template_folder)

from blueprints.custom_handler import custom