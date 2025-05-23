# ./app/services/auth_services.py
from werkzeug.exceptions import Conflict
from sqlalchemy import select
from flask import request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import uuid
from datetime import datetime
from app.extensions import db
from app.models import *


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
class AuthService:
    
    @staticmethod
    def save_file(file):
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            ext = filename.rsplit('.', 1)[1].lower()
            unique_name = f"{uuid.uuid4()}.{ext}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_name)
            file.save(filepath)
            return unique_name
        return None
    
    
    @staticmethod
    def register_visitor(data):
        """ragistor user."""
        email = data["email"].lower()
        with db.session.begin():
            stmt = select(Visitor).where(
                (Visitor.email == data['email']) | 
                (Visitor.phone == data['phone'])
            )
            existing = db.session.execute(stmt).scalars().first()
        if existing:
            if existing.email == data['email'] and existing.phone == data['phone']:
                raise ValueError("Email and phone number already registered.")
            elif existing.email == data['email']:
                raise ValueError("Email already registered.")
            else:
                raise ValueError("Phone number already registered.")
                
        hashed_password = generate_password_hash(data["password"])
        print(data["password"])
        visitor = Visitor(
            full_name=data["full_name"],
            phone=data["phone"],
            email=email,
            password=hashed_password,
            gender=data["gender"],
            dob=datetime.strptime(data["dob"], "%Y-%m-%d").date(),
            address=data["address"],
            city=data["city"],
            state=data["state"],
            country=data["country"],
            pincode=data["pincode"],
            nationality=data["nationality"],
            person_image=AuthService.save_file(request.files.get('person_image')),
            id_proof_type=data["id_proof_type"],
            id_proof_number=data["id_proof_no"],
            id_proof_photo=AuthService.save_file(request.files.get('id_proof_photo'))
        )
        db.session.add(visitor)
        db.session.commit()
        
        return visitor

    @staticmethod
    def login_visitor(data):
        """Authenticate and log in a user."""
        stmt = select(Visitor).where(Visitor.email == data['email'].lower())
        visitor = db.session.execute(stmt).scalars().first()
        print(visitor)
        print(data["password"])

        if not visitor or not check_password_hash(visitor.password, data['password']):
            return None, "Invalid email or password"

        access_token = create_access_token(identity=str(visitor.id))
        refresh_token = create_refresh_token(identity=str(visitor.id))
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "visitor": {
                "id": visitor.id,
                "email": visitor.email,
                "full_name": visitor.full_name,
                "is_email_verified": visitor.is_email_verified,
                "is_payment_done": visitor.is_payment_done
            }
        }, None
        