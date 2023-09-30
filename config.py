import os 
from dotenv import load_dotenv
from pathlib import Path

base_dir = Path(__file__).resolve().parent
env_file = base_dir / '.env'
load_dotenv(env_file)
local=True

class Config():
    SECRET_KEY=os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI=os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    DEBUG=True

"""
class Discord():
    from backend.database.config_db import Config as cfg
    
    WEBHOOK_ENABLE=cfg.get_by_name('WEBHOOK_ENABLE')
    LOG_WEBHOOK_URL=r'https://discord.com/api/webhooks/1157324640222457909/yXtZT4kpeo8CQcd3nDPDO_trEB-hPALSPM-4MdScDHMllwuYEsElwBcQfPRo7paLSFZ7'
    
    DISCORD_LOGIN_ENABLE=False
    BOT_TOKEN=''
    BOT_ID=''
    BOT_SECRET=''
"""    
    
# HypeEngine Temp Config