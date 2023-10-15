from flask import current_app, jsonify, render_template, request

from backend import db
from blueprints.main import main_bp


@main_bp.route('/')
def index():
    return render_template('main/index.html')

@main_bp.route('/test')
def test():
    with current_app.app_context():
        import assets.mail_handler as mh
        mh.send_with_app_context("mail.kequer@gmail.com","test","Test122333")
    return "sended"
