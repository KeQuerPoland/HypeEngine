from flask import current_app
from backend import db


class Config(db.Model):
    __name__ = 'config'

    # Main Config
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    value = db.Column(db.String(150), nullable=False)

    @staticmethod
    def get_by_name(name):
        with current_app.app_context():
            a = Config.query.filter_by(name=name).first()
            a = a.value
            if a == "0":
                a = False
            elif a == "1":
                a = True
            return a

    @staticmethod
    def change_value(name, value):
        with current_app.app_context():
            config_item = Config.get_by_name(name)
            if config_item:
                config_item.value = value
                db.session.commit()

    @staticmethod
    def add_value_or_pass(name, value):
        with current_app.app_context():
            config_item = Config.query.filter_by(name=name).first()
            if not config_item:
                new_config_item = Config(name=name, value=value)
                db.session.add(new_config_item)
                db.session.commit()
