# ./config/default.py

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') #or 'you-will-never-guess'
    PASSWORD_PEPPER = os.environ.get('PASSWORD_PEPPER')
    UPLOAD_FOLDER = 'app/static/uploads'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    TESTING = False
    
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')