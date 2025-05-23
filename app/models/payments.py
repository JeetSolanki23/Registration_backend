from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app.extensions import db

class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    visitor_id = db.Column(db.Integer, db.ForeignKey('visitors.id'), nullable=False)

    order_id = db.Column(db.String(100), unique=True, nullable=False)
    #receipt = db.Column(db.String(100), nullable=True)  # Optional: your custom receipt/identifier

    amount = db.Column(db.Numeric(10, 2), nullable=False)
    currency = db.Column(db.String(10), default='INR')
    payment_method = db.Column(db.String(50), nullable=True)  # e.g., card, upi, netbanking

    transaction_id = db.Column(db.String(100), unique=True, nullable=True)  # Payment ID (only available after success)
    payment_signature = db.Column(db.String(255), nullable=True)  # Razorpay Signature
    payment_status = db.Column(db.Enum('created', 'success', 'pending', 'failed'), nullable=False, default='created')

    paid_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    visitor = db.relationship("Visitor", back_populates="payments")

    def __repr__(self):
        return f"<Payment {self.order_id} - {self.payment_status}>"
