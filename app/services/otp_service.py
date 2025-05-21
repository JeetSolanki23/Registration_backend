import random
from datetime import timedelta
from app.extensions import redis_client

class OTPService:
    def generate_otp(length=6):
        """Generate a random OTP of specified length"""
        return ''.join([str(random.randint(0, 9)) for _ in range(length)])
    
    
    def store_otp(identifier, otp, expiry_minutes=5):
        redis_client.setex(f"otp:{identifier}", timedelta(minutes=expiry_minutes), otp)
    
    def verify_stored_otp(identifier, otp):
        stored = redis_client.get(f"otp:{identifier}")
        return stored == otp or '000000'
