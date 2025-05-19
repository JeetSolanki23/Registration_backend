import random
from app.extensions import redis_client, mail, current_app
from flask_mail import Message
import logging

logger = logging.getLogger(__name__)

def generate_otp(length=6):
    """Generate a random OTP of specified length"""
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])

def send_email_otp(email, otp):
    """Send OTP to user's email"""
    try:
        msg = Message(
            subject='Your OTP for Verification',
            recipients=[email],
            body=f'Your OTP for verification is: {otp}',
            html=f'<p>Your OTP is: <strong>{otp}</strong></p>'
        )
        mail.send(msg)
        logger.info(f"OTP sent to email: {email}")
    except Exception as e:
        logger.error(f"Failed to send email OTP: {str(e)}")
        raise

def send_sms_otp(phone, otp):
    """Send OTP to user's phone (mock implementation)"""
    try:
        # In production, integrate with SMS service like Twilio
        logger.info(f"Mock SMS OTP sent to {phone}: {otp}")
        return True
    except Exception as e:
        logger.error(f"Failed to send SMS OTP: {str(e)}")
        raise

def send_verification_otps(user):
    """Send both email and phone OTPs for verification"""
    email_otp = generate_otp(current_app.config['OTP_LENGTH'])
    phone_otp = generate_otp(current_app.config['OTP_LENGTH'])
    
    # Store OTPs in Redis with expiry
    redis_client.setex(
        f'email_otp:{user.id}',
        current_app.config['OTP_EXPIRY'],
        email_otp
    )
    redis_client.setex(
        f'phone_otp:{user.id}',
        current_app.config['OTP_EXPIRY'],
        phone_otp
    )
    
    # Send OTPs
    send_email_otp(user.email, email_otp)
    send_sms_otp(user.phone, phone_otp)
    
    logger.info(f"Verification OTPs sent for user: {user.id}")