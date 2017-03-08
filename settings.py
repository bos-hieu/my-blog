import os

#Generic app settings.
APP_HOST = "127.0.0.1"
APP_PORT = "5000"
DEBUG = True
SECRET_KEY = 'secret key'
TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
#STATIC_PATH = os.path.dirname(os.path.abspath(__file__))
#'/static'

#Database app settings
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:123456@localhost/blog'
SQLALCHEMY_ECHO = False

#For testing
