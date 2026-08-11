import os


class Config:
    APP_NAME = os.getenv("APP_NAME", "flask-support-app")
    APP_ENV = os.getenv("APP_ENV", "development")
    APP_VERSION = os.getenv("APP_VERSION", "0.1.0")