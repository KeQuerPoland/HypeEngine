from flask import request, jsonify, current_app,render_template,abort
from backend.blueprints.custom_handler import custom_bp
from backend import db
from backend.database.pages_db import Pages

@custom_bp.route('/<path:path>')
def catch_all(path):
    a = Pages.get_by_name(path)
    if a != None:
        return render_template(a)
    else:
        return abort(404)
