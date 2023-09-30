from backend.database.config_db import Config
from flask import current_app

with current_app.app_context():

    Config.add_value_or_pass('DISCORD_WEBHOOK_ENABLE', False)
    Config.add_value_or_pass('DISCORD_WEBHOOK_URL', '')
    Config.add_value_or_pass('MAIL_SERVER', '')
    Config.add_value_or_pass('MAIL_PORT', '')
    Config.add_value_or_pass('MAIL_USERNAME', '')
    Config.add_value_or_pass('MAIL_PASSWORD', '')
    Config.add_value_or_pass('MAIL_USE_TLS', True)
    Config.add_value_or_pass('MAIL_USE_SSL', False)
    Config.add_value_or_pass('MAIL_DEFAULT_SENDER', '')
    Config.add_value_or_pass('MAIL_SERVER_DOMAIN', '')
    
    # Apply Global Config
    current_app.config['MAIL_SERVER'] = Config.get_by_name('MAIL_SERVER')
    current_app.config['MAIL_PORT'] = Config.get_by_name('MAIL_PORT')
    current_app.config['MAIL_USERNAME'] = Config.get_by_name('MAIL_USERNAME')
    current_app.config['MAIL_PASSWORD'] = Config.get_by_name('MAIL_PASSWORD')
    current_app.config['MAIL_USE_TLS'] = Config.get_by_name('MAIL_USE_TLS')
    current_app.config['MAIL_DEFAULT_SENDER'] = Config.get_by_name('MAIL_DEFAULT_SENDER')
    current_app.config['MAIL_SERVER_DOMAIN'] = Config.get_by_name('MAIL_SERVER_DOMAIN')