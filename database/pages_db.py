from flask import current_app
from backend import db


class Pages(db.Model):
    __name__ = 'pages'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    value = db.Column(db.String(50), nullable=False)

    @staticmethod
    def get_by_name(name):
        with current_app.app_context():
            a = Pages.query.filter_by(name=name).first()
            if a != None:
                a = a.value
            return a
