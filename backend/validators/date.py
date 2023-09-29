from marshmallow import ValidationError
from datetime import datetime

def validate_not_future_date(date):
    if date > datetime.now():
        raise ValidationError("Date cannot be in the future.")