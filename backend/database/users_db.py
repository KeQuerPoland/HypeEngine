from backend import db
from datetime import datetime,timedelta
from marshmallow import Schema, fields, validate
from backend.validators.date import validate_not_future_date

class User(db.Model):
    __name__ = 'users'
    
    # Main Data
    id              =   db.Column(db.Integer, primary_key=True)
    name            =   db.Column(db.String(50), nullable=False)
    avatar          =   db.Column(db.String(100), nullable=True)
    email           =   db.Column(db.String(50), nullable=False)
    
    # Discord
    discord_token   =   db.Column(db.String(100),nullable=True)
    
    # Account Secrets
    password        =   db.Column(db.String(100),nullable=False)
    token           =   db.Column(db.String(300),nullable=True)
    
    # Account Details
    creation_date   =   db.Column(db.DateTime,nullable=False,default=datetime.now()+timedelta(hours=2))
    email_verifed   =   db.Column(db.Boolean,nullable=False,default=False)
    account_locked  =   db.Column(db.Boolean,nullable=False,default=False)
    is_active       =   db.Column(db.Boolean,nullable=False,default=True)
    
    @property
    def is_authenticated(self):
        return True
    
    def __repr__(self):
        return {'name:': self.name, 'email': self.email}

class UserSchema(Schema):
    id              =   fields.Int(dump_only=True)
    name            =   fields.Str(required=True, validate=validate.Length(min=1, max=50))
    avatar          =   fields.Str(validate=[validate.Length(max=100),validate.URL()])
    email           =   fields.Email(required=True, validate=[validate.Length(min=1, max=50), validate.Email()])
    discord_token   =   fields.Str(validate=validate.Length(max=100))
    password        =   fields.Str(required=True, validate=validate.Length(min=8, max=100))
    token           =   fields.Str(required=False, validate=validate.Length(min=1, max=300))
    creation_date   =   fields.DateTime(dump_only=True, validate=validate_not_future_date)
    email_verifed   =   fields.Bool(dump_only=True)
    account_locked  =   fields.Bool(dump_only=True)
