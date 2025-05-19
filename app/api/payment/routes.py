# ./app/api/main/routes.py
from flask import Blueprint, jsonify
from . import payment
from app.services.payment_service import create_payment_order, verify_payment_signature

@payment.route('/create-order', methods=['POST'])
def create_order():
    try:
        order = create_payment_order()
        return jsonify({
            "order_id": order['id'],
            "amount": order['amount'],
            "currency": order['currency'],
            "key": current_app.config['RAZORPAY_KEY_ID']
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@payment.route("/verify-payment", methods=["POST"])
def verify_payment():
    data = request.get_json()

    required_fields = {"razorpay_order_id", "razorpay_payment_id", "razorpay_signature"}
    if not required_fields.issubset(data):
        return jsonify({"error": "Missing required fields"}), 400

    order_id = data["razorpay_order_id"]
    payment_id = data["razorpay_payment_id"]
    signature = data["razorpay_signature"]

    if verify_payment_signature(order_id, payment_id, signature):
        return jsonify({"status": "success", "message": "Payment verified successfully"}), 200
    else:
        return jsonify({"status": "failed", "message": "Signature verification failed"}), 400