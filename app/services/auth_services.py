# ./app/services/auth_services.py
from werkzeug.exceptions import Conflict
from sqlalchemy import select, literal_column, union_all, func
from flask import request, jsonify, current_app
from flask_jwt_extended import create_access_token, create_refresh_token
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import uuid
from datetime import datetime
from app.extensions import db, redis_client
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
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_name)
            file.save(filepath)
            return unique_name
        return None
    
    
    @staticmethod
    def register_visitor(data):
        """ragistor user."""
        email = data["email"].lower()
        phone = data["phone"]
        with db.session.begin():
            email_query = select(literal_column("'email'").label("field"))
            email_query = email_query.where(func.lower(Visitor.email) == email)

            phone_query = select(literal_column("'phone'").label("field"))
            phone_query = phone_query.where(Visitor.phone == phone)

            union_stmt = union_all(email_query, phone_query)

            existing = db.session.execute(union_stmt).scalars().all()
            print(existing)
        if existing:
            if "email" in existing and "phone" in existing:
                raise ValueError("Email and phone number already registered.")
            elif "email" in existing:
                 raise ValueError("Email already registered.")
            else:
                raise ValueError("Phone number already registered.")
            
        #     if existing.email == email and existing.phone == phone:
        #         raise ValueError("Email and phone number already registered.")
        #     elif existing.email == email:
        #         raise ValueError("Email already registered.")
        #     else:
        #         raise ValueError("Phone number already registered.")
        if not redis_client.get(f"phone:{phone}"):
            raise ValueError("phone number is not verified")
                
        hashed_password = generate_password_hash(data["password"])

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
        