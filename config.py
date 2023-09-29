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
    MAIL_SERVER="serwer2385933.home.pl"
    MAIL_PORT="587"
    MAIL_USERNAME="test@highaccounts.store"
    MAIL_PASSWORD=r"test!!#%%"
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_DEFAULT_SENDER = "test@highaccounts.store"
    MAIL_SERVER_DOMAIN = "highaccounts.store"
    
class Discord():
    WEBHOOK_ENABLE=True
    LOG_WEBHOOK_URL=r'https://discord.com/api/webhooks/1157324640222457909/yXtZT4kpeo8CQcd3nDPDO_trEB-hPALSPM-4MdScDHMllwuYEsElwBcQfPRo7paLSFZ7'
    
    DISCORD_LOGIN_ENABLE=False
    BOT_TOKEN=''
    BOT_ID=''
    BOT_SECRET=''
    
    
# HypeEngine Temp Config