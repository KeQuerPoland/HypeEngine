from backend import db
from datetime import datetime,timedelta
from marshmallow import Schema, fields, validate
from backend.validators.date import validate_not_future_date
from flask_login import UserMixin

class Config(db.Model, UserMixin):
    __name__ = 'config'
    
    # Main Config
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    value = db.Column(db.String(50), nullable=False)

    @staticmethod
    def get_by_name(name):
        return Config.query.filter_by(name=name).first()

    @staticmethod
    def change_value(name, value):
        config_item = Config.get_by_name(name)
        if config_item:
            config_item.value = value
            db.session.commit()

    @staticmethod
    def add_value_or_pass(name, value):
        config_item = Config.get_by_name(name)
        if not config_item:
            new_config_item = Config(name=name, value=value)
            db.session.add(new_config_item)
            db.session.commit()

    
    


