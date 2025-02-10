import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback-key")
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@localhost/bullbear"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


    # Basic configurations
    LOGGING_LEVEL = "DEBUG"  # or "INFO", "WARNING"
    LOG_FILE_PATH = os.path.join(os.getcwd(), 'app', 'logs', 'app.log')
