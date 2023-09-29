from flask import Flask,request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
import logging,coloredlogs
from flask.logging import default_handler
from flask_caching import Cache
from logging.config import dictConfig
from backend.colors import gray,red,yellow,green
from datetime import datetime
from config import Discord
from backend.assets.discord_handler import DiscordHandler
from flask_mail import Mail,Message
from flask import render_template
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required

db = SQLAlchemy()
migrate = Migrate()
cache = Cache(config={'CACHE_TYPE': 'simple'})
dh = DiscordHandler(Discord.LOG_WEBHOOK_URL)
mail = Mail()
login_manager = LoginManager()

def create_app():
    # Creating WebServer
    app = Flask(__name__)
    
    # Config Initialization
    app.config.from_object(Config)
    
    # BluePrint Initiation
    from backend.blueprints.main import main_bp
    
    app.register_blueprint(main_bp)
    
    # Logging Init
    werkzeug_logger = logging.getLogger('werkzeug')
    werkzeug_logger.disabled = True
    
    dictConfig({
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s] %(levelname)-8s %(message)s',
            'datefmt': '%H:%M:%S'
        }},
        'handlers': {'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }},
        'root': {
            'level': 'WARNING',
            'handlers': ['wsgi']
        }
    })

    coloredlogs.install(level='INFO', logger=app.logger, fmt='[%(asctime)s] %(levelname)-8s %(message)s')
    
    # Page Entry Log
    @app.before_request
    def log_request_info():
        if not request.endpoint == None:
            try:
                dh.log(f'Page Entry',"#3A94EE")
            except Exception as e:
                raise e
            app.logger.info('Page Entry - IP: %s, Endpoint: %s', request.remote_addr, request.endpoint)
    
    # Watermark Initialization
    @app.after_request
    def add_watermark(response):
        if response.mimetype == 'text/html':
            response.set_data(response.get_data(as_text=True) + '<div style="position: fixed; right: 0; bottom: 0; font-size: 30px;">Created with WP-OW</div>')
        return response

    @app.route('/mail/test/<name>')
    def mail_test(name):
        try:
            msg = Message("Hello",
                    sender="test@highaccounts.store",
                    recipients=["mail.kequer@gmail.com"])

            msg.html = render_template('/mails/confirm_register/index.html',name=name)

            mail.send(msg)
            return render_template('/mails/confirm_register/index.html',name=name)
        except Exception as e:
            return str(e)

    
    # Extentions Initiation
    db.init_app(app)
    migrate.init_app(app,db)
    cache.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    
    # DB Initiation
    from backend.database.users_db import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    dh.log(f'Started web server...',"#3A94EE",web=False)
    
    return app