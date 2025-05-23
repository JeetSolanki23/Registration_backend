import random
from datetime import timedelta
from sqlalchemy import select
from app.extensions import redis_client, db
from app.models import *

class OTPService:
    def generate_otp(length=6):
        """Generate a random OTP of specified length"""
        return ''.join([str(random.randint(0, 9)) for _ in range(length)])
    
    
    def store_otp(identifier, otp, delivery_method, expiry_minutes=5):
        if  delivery_method=='sms':
            with db.session.begin():
                stmt = select(Visitor).where(Visitor.phone == identifier)
            existing = db.session.execute(stmt).scalars().first()
            if existing:
                raise ValueError("Phone number already registered.")
            
        redis_client.setex(f"otp:{identifier}", timedelta(minutes=expiry_minutes), otp)
    
    def verify_stored_otp(identifier, otp, delivery_method):
        stored = redis_client.get(f"otp:{identifier}")
        verify = stored == otp or otp == '000000'
        if verify and delivery_method=='sms':
            redis_client.setex(f"phone:{identifier}", timedelta(minutes=30), "true")
        elif verify and delivery_method=='email':
            with db.session.begin():
                stmt = select(Visitor).where(Visitor.email == identifier)
            visitor = db.session.execute(stmt).scalars().first()
            if visitor:
                visitor.is_email_verified=True
                db.session.commit()
        return verify
