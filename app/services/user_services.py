# ./app/services/user_services.py
from flask import session, redirect, url_for, flash
from app.extensions import db
from app.models import *

class UserService:

    @staticmethod
    def add_user(form):
        """Add a new user with specified roles."""
        if form.validate():
            try:
                pass
                
            except SQLAlchemyError as e:
                db.session.rollback()
                
