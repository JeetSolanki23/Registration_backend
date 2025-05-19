import razorpay
from flask import current_app
import hmac, hashlib
from app.models import *

client = razorpay.Client(auth=(current_app.config['RAZORPAY_KEY_ID'], current_app.config['RAZORPAY_KEY_SECRET']))

def create_payment_order(amount=15000, currency="INR"):
    order = client.order.create({
        "amount": amount * 100,  # ₹15000 → 1500000 paise
        "currency": currency,
        "payment_capture": 1
    })
    
    payment = Payment(
        visitor_id=visitor_id,
        amount=Decimal(str(amount)),
        currency="INR",
        transaction_id=order["id"],
        payment_method="Razorpay",
        payment_status="Pending",
        created_at=datetime.utcnow()
    )
    db.session.add(payment)
    db.session.commit()
    
    return order


def verify_payment_signature(order_id, payment_id, signature):

    generated_signature = hmac.new(
        current_app.config['RAZORPAY_KEY_SECRET'].encode(),
        f"{order_id}|{payment_id}".encode(),
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(generated_signature, signature)
