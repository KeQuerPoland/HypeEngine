from flask import abort, current_app, jsonify, render_template, request

from backend import db
from assets.global_handler import get_all_routes
from blueprints.custom_handler import custom_bp
from database.pages_db import Pages


@custom_bp.route('/<path:path>')
def catch_all(path):
    a = Pages.get_by_name(path)
    if a != None:
        return render_template(a)
    else:
        return abort(404)
