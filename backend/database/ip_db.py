from datetime import datetime, timedelta

from flask import current_app
from marshmallow import Schema, fields, validate

from backend import db
from backend.validators.date import validate_not_future_date


class IP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(15), unique=True, nullable=False)
    blocked = db.Column(db.Boolean, default=False)
    security_vpn = db.Column(db.Boolean, default=False)
    security_proxy = db.Column(db.Boolean, default=False)
    security_tor = db.Column(db.Boolean, default=False)
    security_relay = db.Column(db.Boolean, default=False)
    location_city = db.Column(db.String(50))
    location_region = db.Column(db.String(50))
    location_country = db.Column(db.String(50))
    location_continent = db.Column(db.String(50))
    location_region_code = db.Column(db.String(10))
    location_country_code = db.Column(db.String(10))
    location_continent_code = db.Column(db.String(10))
    location_latitude = db.Column(db.String(20))
    location_longitude = db.Column(db.String(20))
    location_time_zone = db.Column(db.String(50))
    location_locale_code = db.Column(db.String(10))
    location_metro_code = db.Column(db.String(10))
    location_is_in_european_union = db.Column(db.Boolean)
    network_network = db.Column(db.String(20))
    network_autonomous_system_number = db.Column(db.String(20))
    network_autonomous_system_organization = db.Column(db.String(50))
