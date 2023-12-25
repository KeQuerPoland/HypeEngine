import os 
from dotenv import load_dotenv
from pathlib import Path

base_dir = Path(__file__).resolve().parent
env_file = base_dir / '.env'
load_dotenv(env_file)
local=True
version="0.1"

class Config():
    SECRET_KEY=os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SECURITY_PASSWORD_SALT='f^Rk*2A%V%@eM3hUcgyoRrS33CRWs8qWMByvUmdH5jdux9QLrSHv!wBwr*4uKnjh2aJpv28DMt!zUjJ^Xb6!8b^Aq%^i9742jQxh9xBWvcJ9Kg$w28%oNnX4Lh*Lu%^L'
    DEBUG=True # If you not edit a source code - replace it to False
    
    if DEBUG == False:
        SQLALCHEMY_DATABASE_URI=os.environ.get('SQLALCHEMY_DATABASE_URI')
    elif DEBUG == True:
        ldp = base_dir / 'storage' / 'data.db'
        SQLALCHEMY_DATABASE_URI = "sqlite:///"+f"{ldp}"

    
# HypeEngine Temp Config
