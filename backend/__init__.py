from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging,coloredlogs
from flask_caching import Cache
from logging.config import dictConfig
from flask_mail import Mail
import os
from flask_bcrypt import Bcrypt
import flask
from sqlalchemy import text
import sys
import click
import colorama
import speedtest
import threading

db = SQLAlchemy()
migrate = Migrate()
cache = Cache(config={'CACHE_TYPE': 'simple'})
mail = Mail()
bcrypt = Bcrypt()

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
static_folder=os.path.join(project_root, 'public\\static')
template_folder=os.path.join(project_root, 'public\\html')

cli = sys.modules['flask.cli']

def run_speedtest():
    st = speedtest.Speedtest(secure=True)
    download_speed = st.download()
    upload_speed = st.upload()

    banner = f"""
{colorama.Fore.RED}{'*' * 50}
    {colorama.Style.BRIGHT}
    {colorama.Fore.RED}HYPE{colorama.Fore.WHITE}ENGINE - Welcome!{colorama.Fore.RED}

    {colorama.Fore.CYAN}STATUS:    {colorama.Fore.GREEN}ONLINE{colorama.Fore.RED} 
    {colorama.Fore.CYAN}DB STATUS: {colorama.Fore.GREEN}CONNECTED{colorama.Fore.RED}
    {colorama.Fore.CYAN}DOWNLOAD:  {colorama.Fore.GREEN}{download_speed / 1e6:.2f} Mbps{colorama.Fore.RED}
    {colorama.Fore.CYAN}UPLOAD:    {colorama.Fore.GREEN}{upload_speed / 1e6:.2f} Mbps{colorama.Fore.RED}{colorama.Style.RESET_ALL}

{colorama.Fore.RED}{'*' * 50}{colorama.Style.RESET_ALL}
"""
    os.system('cls')
    print(banner)

def show_banner(*args, **kwargs):
    os.system('cls')
    banner = f"""
{colorama.Fore.RED}{'*' * 50}

    {colorama.Fore.RED}HYPE{colorama.Fore.WHITE}ENGINE - Welcome!{colorama.Fore.RED}

    {colorama.Fore.CYAN}STATUS:    {colorama.Fore.GREEN}ONLINE{colorama.Fore.RED} 
    {colorama.Fore.CYAN}DB STATUS: {colorama.Fore.GREEN}CONNECTED{colorama.Fore.RED}
    {colorama.Fore.CYAN}DOWNLOAD:  {colorama.Fore.YELLOW}IN PROCESS...{colorama.Fore.RED}
    {colorama.Fore.CYAN}UPLOAD:    {colorama.Fore.YELLOW}IN PROCESS...{colorama.Fore.RED}

{'*' * 50}{colorama.Style.RESET_ALL}
"""
    cli.show_server_banner = lambda *x:click.echo(banner)
    a = threading.Thread(target=run_speedtest)
    a.start()
    

def create_app():
    # Creating WebServer
    
    app = Flask(__name__,static_folder=static_folder,template_folder=template_folder)
    
    # Config Initialization
    from config import Config
    app.config.from_object(Config)
    
    with app.app_context():
        # Logging Init
        werkzeug_logger = logging.getLogger('werkzeug')
        werkzeug_logger.disabled = True
        
        dictConfig({
            'version': 1,
            'formatters': {'default': {
                '()': 'coloredlogs.ColoredFormatter',
                'format': '[%(asctime)s] %(levelname)-3s %(message)s',
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

        coloredlogs.install(level='INFO', logger=app.logger, fmt='[%(asctime)s] %(levelname)-3s %(message)s')

        
        # DB Initiation
        db.init_app(app)

        # DataBase Handlers
        from database.config_db import Config as cfg
        from database.users_db import User
        from database.pages_db import Pages
        
        # Try DB connect
        try:
            db.session.execute(text('SELECT 1'))
            db.create_all()
        except Exception as e:
            app.logger.error(f"Database connection error: {e}")
            os._exit(0)

        # Add "current_user" to Jinja 
        @app.context_processor
        def inject_user():
            with app.app_context():
                from assets.login_handler import current_user
                return dict(current_user=current_user())


        @app.before_request
        def before_request():
            from security.cooldown import cooldown as func; return func() or None;

        # After Request Security
        @app.after_request
        def after_request(response: flask.Response):
            from security.add_watermark import add_watermark as func; func(response)
            from security.page_entry import page_entry as func; func(response)

            return response

        
        # WebServer Startup Webhook log
        if os.environ.get('RUN_ONCE') is None:
            with app.app_context():
                show_banner()
                #log(f'Started web server...',"#3A94EE",web=False)
            os.environ['RUN_ONCE'] = 'true'
        else:
            app.logger.info("HypeEngine Reloaded!")

        # BluePrints Initiation
        from blueprints.main import main_bp
        from blueprints.custom_handler import custom_bp
        from blueprints.panel import panel_bp
        
        app.register_blueprint(main_bp)
        app.register_blueprint(custom_bp)
        app.register_blueprint(panel_bp, url_prefix='/panel')

        # Database Config Initiation
        import init.config_init
        import init.security_init

        # Extentions Initiation
        migrate.init_app(app,db)
        cache.init_app(app)
        mail.init_app(app)
        bcrypt.init_app(app)


    # Returning App Object
    return app