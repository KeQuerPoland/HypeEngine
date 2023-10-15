from flask import Blueprint
from backend import static_folder,template_folder

main_bp = Blueprint('main', __name__,static_folder=static_folder,template_folder=template_folder)

from blueprints.main import index, login
