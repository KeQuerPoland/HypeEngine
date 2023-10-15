from flask import Blueprint
from backend import static_folder,template_folder

panel_bp = Blueprint('panel', __name__,static_folder=static_folder,template_folder=template_folder)

from blueprints.panel import main
