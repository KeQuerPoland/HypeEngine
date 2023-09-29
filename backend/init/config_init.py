from backend.database.config_db import Config
from flask import current_app

with current_app.app_context():

    Config.add_value_or_pass('DISCORD_WEBHOOK_ENABLE', False)
    Config.add_value_or_pass('DISCORD_WEBHOOK_URL', '')