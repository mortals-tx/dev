import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env') # 读取.env配置

class Config:
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', '654321')
    SQLALCHEMY_DATABASE_URI = os.environ.get('FLASK_SQLALCHEMY_DATABASE_URI',
                                             'mysql+cymysql://mysql:z8zce3Ct34uabtNo@127.0.0.1:3306/atfield')
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TOKEN_EXPIRATION = 30 * 24 * 3600

config = Config
