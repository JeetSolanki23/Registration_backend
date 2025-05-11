# ./app/models/user/user.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.extensions import db

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    
    def __repr__(self):
        return f'<User {self.email}>'
