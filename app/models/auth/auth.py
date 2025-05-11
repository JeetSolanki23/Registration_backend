# ./app/models/auth/auth.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime
from flask import current_app
from app.extensions import db

class Auth(db.Model):
    __tablename__ = 'auth'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Auth {self.user_id}>'