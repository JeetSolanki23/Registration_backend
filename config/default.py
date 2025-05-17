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
    
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwtsecret")
    JWT_SECRET_KEY = os.getenv("JWT_ACCESS_TOKEN_EXPIRES", "3600")
    JWT_SECRET_KEY = os.getenv("JWT_REFRESH_TOKEN_EXPIRES", "86400")
    RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID")
    RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET")
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    origins = os.getenv("ALLOWED_ORIGINS", "")
    ALLOWED_ORIGINS = [origin.strip() for origin in origins.split(",") if origin.strip()]