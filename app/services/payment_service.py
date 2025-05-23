import razorpay
from flask import current_app
from sqlalchemy import select, update
from sqlalchemy.orm import joinedload
import hmac, hashlib
from datetime import datetime
from app.models import *
from app.extensions import db

def get_razorpay_client():
    return razorpay.Client(auth=(
        current_app.config['RAZORPAY_KEY_ID'],
        current_app.config['RAZORPAY_KEY_SECRET']
    ))

def create_payment_order(visitor_id, amount=15000, currency="INR"):
    client = get_razorpay_client()
    order = client.order.create({
        "amount": amount * 100,  # ₹15000 → 1500000 paise
        "currency": currency,
        "payment_capture": 1
    })
    
    payment = Payment(
        visitor_id=visitor_id,
        amount=amount/100.0,
        currency="INR",
        order_id=order["id"],
        payment_method="Razorpay",
        payment_status="pending"
    )
    db.session.add(payment)
    db.session.commit()
    
    return order


def verify_razorpay_payment(visitor_id, razorpay_payment_id, razorpay_order_id, razorpay_signature):
    """
    Verifies Razorpay signature, updates Payment & Visitor tables.
    """
    
    RAZORPAY_KEY_SECRET=current_app.config['RAZORPAY_KEY_SECRET']
    expected_signature = hmac.new(
        key=RAZORPAY_KEY_SECRET.encode("utf-8"),
        msg=f"{razorpay_order_id}|{razorpay_payment_id}".encode("utf-8"),
        digestmod=hashlib.sha256,
    ).hexdigest()

    if expected_signature != razorpay_signature:
        return {"verified": False, "message": "Invalid Razorpay signature."}

    # Fetch payment by visitor_id and order_id
    stmt = select(Payment).where(
        Payment.visitor_id == visitor_id,
        Payment.order_id == razorpay_order_id
    ).options(joinedload(Payment.visitor))

    payment = db.session.scalar(stmt)

    if not payment:
        return {"verified": False, "message": "Payment not found for visitor and order_id."}

    # Update Payment and Visitor in one transaction
    payment.transaction_id = razorpay_payment_id
    payment.payment_signature = razorpay_signature
    payment.payment_status = "success"
    payment.paid_at = datetime.utcnow()
    payment.updated_at = datetime.utcnow()

    if payment.visitor:
        payment.visitor.is_payment_done = True
        payment.visitor.updated_at = datetime.utcnow()

    db.session.commit()

    return {"verified": True, "message": "Payment verified and records updated."}
