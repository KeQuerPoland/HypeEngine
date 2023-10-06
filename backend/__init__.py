from flask import Flask,request,session,g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
import logging,coloredlogs
from flask.logging import default_handler
from flask_caching import Cache
from logging.config import dictConfig
from datetime import datetime
from flask_mail import Mail,Message
from flask import render_template
import os
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
migrate = Migrate()
cache = Cache(config={'CACHE_TYPE': 'simple'})
mail = Mail()
bcrypt = Bcrypt()

def create_app():
    # Creating WebServer
    app = Flask(__name__)
    
    # Config Initialization
    app.config.from_object(Config)
    
    # BluePrint Initiation
    from backend.blueprints.main import main_bp
    from backend.blueprints.custom_handler import custom_bp
    from backend.blueprints.panel import panel_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(custom_bp)
    app.register_blueprint(panel_bp, url_prefix='/panel')
    
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
    
    # Extentions Initiation
    db.init_app(app)
    migrate.init_app(app,db)
    cache.init_app(app)
    mail.init_app(app)
    bcrypt.init_app(app)
    
    # DB Initiation
    from backend.database.users_db import User
    from backend.database.pages_db import Pages
    from backend.database.config_db import Config as cfg
    
    from sqlalchemy.exc import OperationalError
    from sqlalchemy import text
    
    with app.app_context():
        import backend.assets.login_handler as LoginHandler

    with app.app_context():
        try:
            db.session.execute(text('SELECT 1'))
        except Exception as e:
            app.logger.error(f"Database connection error: {e}")
            os._exit(0)

    with app.app_context():
        db.create_all()
        import backend.init.config_init
    
    with app.app_context():
        from backend.assets.discord_handler import log
        
    @app.context_processor
    def inject_user():
        with app.app_context():
            from backend.assets.login_handler import current_user
            return dict(current_user=current_user())

        
    @app.before_request
    def load_logged_in_user():
        with app.app_context():
            user_id = session.get('user_id')

            if user_id is None:
                g.user = None
            else:
                g.user = User.query.get(user_id)

    
    # Page Entry Log
    @app.before_request
    def log_request_info():
        if not request.endpoint == None:
            if request.endpoint != 'static':
                try:
                    log(f'Page Entry',"#3A94EE")
                except Exception as e:
                    raise e
                app.logger.info('Page Entry - IP: %s, Endpoint: %s', request.remote_addr, request.endpoint)
    
    # Watermark Initialization
    @app.after_request
    def after_request(response):
        from backend.security.cooldown import cooldown as func; func(request)
        from backend.security.add_watermark import add_watermark as func; func(response)
        
        return response
    
    # WebServer Startup Webhook log
    if os.environ.get('RUN_ONCE') is None:
        with app.app_context():
            log(f'Started web server...',"#3A94EE",web=False)
        os.environ['RUN_ONCE'] = 'true'

    return app