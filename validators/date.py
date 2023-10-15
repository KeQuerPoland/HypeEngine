from datetime import datetime
from marshmallow import ValidationError

def validate_not_future_date(date):
    if date > datetime.now():
        raise ValidationError("Date cannot be in the future.")
