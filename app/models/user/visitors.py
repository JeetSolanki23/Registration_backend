from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import select
import os
from app.extensions import db 

class Visitor(db.Model):
    __tablename__ = 'visitors'

    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    full_name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    #age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.Enum('Male', 'Female', 'Other'), nullable=False)

    address = db.Column(db.Text, nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    pincode = db.Column(db.String(10), nullable=False)
    nationality = db.Column(db.String(100), nullable=False)

    person_image = db.Column(db.String(255))
    id_proof_type = db.Column(db.Enum('Aadhar', 'Passport', 'VoterID', 'DrivingLicense', 'Other'), nullable=False)
    id_proof_number = db.Column(db.String(50), nullable=False)
    id_proof_photo = db.Column(db.String(255))

    is_email_verified = db.Column(db.Boolean, default=False)
    is_phone_verified = db.Column(db.Boolean, default=False)
    is_payment_done = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship
    payments = db.relationship('Payment', backref='visitor', lazy=True)

    

class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    visitor_id = db.Column(db.Integer, db.ForeignKey('visitors.id'), nullable=False)

    amount = db.Column(db.Numeric(10, 2), nullable=False)
    currency = db.Column(db.String(10), default='INR')
    payment_method = db.Column(db.String(50))
    transaction_id = db.Column(db.String(100), unique=True, nullable=False)
    payment_status = db.Column(db.Enum('Success', 'Pending', 'Failed'), nullable=False)
    paid_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
