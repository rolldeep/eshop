import os


class Config:
    DEBUG = True
    SECRET_KEY = "secretnoneofthemwouldgeas19203332_key"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
