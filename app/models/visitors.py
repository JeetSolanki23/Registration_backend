from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app.extensions import db

class Visitor(db.Model):
    __tablename__ = 'visitors'

    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(15), unique=True, nullable=False, index=True)
    email = db.Column(db.String(100), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)

    full_name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    gender = db.Column(db.Enum('male', 'female', 'other'), nullable=False)

    address = db.Column(db.Text, nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    pincode = db.Column(db.String(10), nullable=False)
    nationality = db.Column(db.String(100), nullable=False)

    person_image = db.Column(db.String(255))  # Suggest specifying format: "image_path", "image_url", etc.
    id_proof_type = db.Column(db.Enum('aadhar', 'passport', 'voter_id', 'driving_license', 'other'), nullable=False)
    id_proof_number = db.Column(db.String(50), nullable=False)
    id_proof_photo = db.Column(db.String(255))

    is_email_verified = db.Column(db.Boolean, default=False)
    #is_phone_verified = db.Column(db.Boolean, default=False)
    is_payment_done = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    payments = db.relationship('Payment', backref='visitor', lazy=True)

    def __repr__(self):
        return f"<Visitor {self.email}>"
